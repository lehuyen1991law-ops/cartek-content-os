"""Read-only capture of the spreadsheet into a *capture bundle*.

Methods (all read-only, GET requests only):
  * ``api``  Google Sheets API v4 with an OAuth access token
             (GOOGLE_OAUTH_ACCESS_TOKEN) or an API key (GOOGLE_API_KEY, only
             works when the sheet is shared "anyone with the link").
  * ``csv``  Public CSV export per tab (link-shared sheets only; no hyperlinks).

A capture bundle can also be produced by an AI agent through a Google Sheets
connector; see workflows/sheet-import.md. Credentials are read from the
environment and never written to disk.
"""

from __future__ import annotations

import csv
import io
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Callable

from .sheet import a1, canonical_row

SHEETS_API = "https://sheets.googleapis.com/v4/spreadsheets"
Opener = Callable[[urllib.request.Request], Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _get(url: str, opener: Opener | None, token: str | None = None) -> bytes:
    request = urllib.request.Request(url, method="GET")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    open_fn = opener or (lambda req: urllib.request.urlopen(req, timeout=60))  # noqa: S310 - fixed https hosts
    with open_fn(request) as response:
        return response.read()


def _api_url(spreadsheet_id: str, suffix: str = "", params: dict[str, Any] | None = None, api_key: str | None = None) -> str:
    query = dict(params or {})
    if api_key:
        query["key"] = api_key
    url = f"{SHEETS_API}/{urllib.parse.quote(spreadsheet_id)}{suffix}"
    return f"{url}?{urllib.parse.urlencode(query, doseq=True)}" if query else url


def _quote_range(title: str, a1_range: str | None = None) -> str:
    escaped = title.replace("'", "''")
    return f"'{escaped}'" + (f"!{a1_range}" if a1_range else "")


def fetch_bundle_api(
    spreadsheet_id: str,
    token: str | None = None,
    api_key: str | None = None,
    opener: Opener | None = None,
    captured_at: str | None = None,
) -> dict[str, Any]:
    if not token and not api_key:
        raise RuntimeError("Set GOOGLE_OAUTH_ACCESS_TOKEN (or GOOGLE_API_KEY for link-shared sheets).")
    meta_fields = "properties(title,locale,timeZone),sheets(properties(sheetId,title,index,gridProperties))"
    meta = json.loads(_get(_api_url(spreadsheet_id, params={"fields": meta_fields}, api_key=api_key), opener, token))
    tabs = []
    for sheet_meta in meta.get("sheets", []):
        props = sheet_meta["properties"]
        title = props["title"]
        grid_props = props.get("gridProperties", {})
        values_url = _api_url(
            spreadsheet_id,
            "/values/" + urllib.parse.quote(_quote_range(title), safe=""),
            {"valueRenderOption": "FORMATTED_VALUE", "majorDimension": "ROWS"},
            api_key,
        )
        values = json.loads(_get(values_url, opener, token)).get("values", [])
        grid_fields = "sheets(data(startRow,startColumn,rowData(values(hyperlink,note,dataValidation,textFormatRuns(format(link))))))"
        grid_url = _api_url(
            spreadsheet_id,
            params={"ranges": _quote_range(title), "includeGridData": "true", "fields": grid_fields},
            api_key=api_key,
        )
        grid = json.loads(_get(grid_url, opener, token))
        hyperlinks, notes, validation = _extract_grid_extras(grid)
        tabs.append(
            {
                "sheet_id": props.get("sheetId"),
                "title": title,
                "index": props.get("index"),
                "grid": {
                    "row_count": grid_props.get("rowCount"),
                    "column_count": grid_props.get("columnCount"),
                    "frozen_row_count": grid_props.get("frozenRowCount", 0),
                },
                "values": [canonical_row(row) for row in values],
                "hyperlinks": hyperlinks,
                "notes": notes,
                "data_validation": validation,
            }
        )
    props = meta.get("properties", {})
    return {
        "capture_format": 1,
        "spreadsheet": {"id": spreadsheet_id, "title": props.get("title"), "locale": props.get("locale"), "time_zone": props.get("timeZone")},
        "captured_at": captured_at or utc_now(),
        "capture_method": "sheets-api-v4",
        "tabs": tabs,
    }


def _extract_grid_extras(grid: dict[str, Any]) -> tuple[dict[str, str], dict[str, str], list[dict[str, Any]]]:
    hyperlinks: dict[str, str] = {}
    notes: dict[str, str] = {}
    validation: list[dict[str, Any]] = []
    for sheet_data in grid.get("sheets", []):
        for block in sheet_data.get("data", []):
            start_row = block.get("startRow", 0)
            start_col = block.get("startColumn", 0)
            for r_offset, row in enumerate(block.get("rowData", []) or []):
                for c_offset, cell in enumerate(row.get("values", []) or []):
                    ref = a1(start_row + r_offset + 1, start_col + c_offset)
                    link = cell.get("hyperlink")
                    if not link:
                        for run in cell.get("textFormatRuns", []) or []:
                            uri = ((run.get("format") or {}).get("link") or {}).get("uri")
                            if uri:
                                link = uri
                                break
                    if link:
                        hyperlinks[ref] = link
                    if cell.get("note"):
                        notes[ref] = cell["note"]
                    if cell.get("dataValidation"):
                        validation.append({"ref": ref, "rule": cell["dataValidation"]})
    return hyperlinks, notes, validation


def fetch_bundle_csv(
    spreadsheet_id: str,
    tabs_cfg: list[dict[str, Any]],
    opener: Opener | None = None,
    captured_at: str | None = None,
) -> dict[str, Any]:
    tabs = []
    for tab_cfg in tabs_cfg:
        url = f"https://docs.google.com/spreadsheets/d/{urllib.parse.quote(spreadsheet_id)}/export?format=csv&gid={tab_cfg['sheet_id']}"
        raw = _get(url, opener)
        text = raw.decode("utf-8-sig")
        if text.lstrip().lower().startswith("<!doctype html") or "<html" in text[:500].lower():
            raise RuntimeError("CSV export returned an HTML page: the sheet is not link-shared. Use --fetch api or a connector capture.")
        rows = [canonical_row(row) for row in csv.reader(io.StringIO(text))]
        while rows and not rows[-1]:
            rows.pop()
        tabs.append({"sheet_id": tab_cfg["sheet_id"], "title": tab_cfg["title"], "values": rows, "hyperlinks": None, "notes": None, "data_validation": None})
    return {
        "capture_format": 1,
        "spreadsheet": {"id": spreadsheet_id},
        "captured_at": captured_at or utc_now(),
        "capture_method": "csv-export",
        "tabs": tabs,
    }


def load_dotenv(path) -> None:
    """Read KEY=VALUE lines from a local .env (never committed) without overriding the environment."""
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def env_credentials(root=None) -> tuple[str | None, str | None]:
    if root is not None:
        load_dotenv(os.path.join(str(root), ".env"))
    return os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN") or None, os.environ.get("GOOGLE_API_KEY") or None
