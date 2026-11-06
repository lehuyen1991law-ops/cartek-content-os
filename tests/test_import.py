"""Spreadsheet import: idempotency, provenance, stable IDs, classification, protection of local edits."""

from __future__ import annotations

import json
import unittest

from helpers import REPO_ROOT, Sandbox, edit_snapshot, run

from ctk import fetch, fileio, importer, schema, sheet
from ctk.repo import Repo
from ctk.sheet import TabSnapshot


def issue_codes(result) -> list[str]:
    return [i.code for i in result.issues]


class ImportTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.box = Sandbox()
        self.repo = self.box.repo

    def tearDown(self) -> None:
        self.box.cleanup()

    def reimport(self, force: bool = False):
        result = importer.build(Repo(self.repo.root))
        outcome = importer.apply(Repo(self.repo.root), result, force=force)
        return result, outcome

    def ideas(self) -> dict[str, dict]:
        return {i["id"]: i for i in fileio.load_json(self.repo.normalized_dir / "ideas.json")["records"]}


class TestCommittedData(ImportTestCase):
    def test_committed_outputs_match_snapshots(self):
        result = importer.build(self.repo)
        self.assertEqual(importer.check(self.repo, result), [])
        self.assertEqual(result.errors, [])

    def test_all_six_tabs_accounted_for(self):
        result = importer.build(self.repo)
        titles = [t["title"] for t in result.tabs]
        self.assertEqual(titles, ["Đối thủ", "Khán giả", "Content Direction", "Short", "Video Publish", "Short Publish"])
        self.assertTrue(all(t["status"] == "imported" for t in result.tabs))

    def test_expected_record_counts(self):
        self.assertEqual(len(self.ideas()), 28)
        competitors = fileio.load_json(self.repo.normalized_dir / "competitors.json")["records"]
        self.assertEqual(len(competitors), 5)
        self.assertTrue(all(c["reach_metrics"]["status"] == "historical-unverified" for c in competitors))
        personas = {p["id"]: p for p in fileio.load_json(self.repo.normalized_dir / "personas.json")["records"]}
        self.assertEqual(set(personas), {"garage-owner", "technician", "automotive-student", "car-owner"})
        self.assertEqual(personas["car-owner"]["priority"], "low")

    def test_template_rows_are_not_production_records(self):
        tracker = fileio.load_json(self.repo.normalized_dir / "tracker.json")
        self.assertEqual(tracker["records"], [])
        for tab in tracker["tabs"]:
            self.assertEqual(tab["counts"], {"blank": 1, "placeholder-filler": 1007, "template-example": 6})

    def test_every_idea_has_provenance(self):
        for idea in self.ideas().values():
            self.assertRegex(idea["source"]["ref"], r"^'(Content Direction|Short)'![D-G]\d+$")

    def test_p0300_idea_id(self):
        self.assertEqual(self.ideas()["CTK-L-0015"]["title"], "Lỗi P0300 - Ác Mộng của Mọi Động Cơ?")


class TestIdempotency(ImportTestCase):
    def test_repeated_import_writes_nothing(self):
        _, first = self.reimport()
        self.assertEqual(first["conflicts"], [])
        before = {p: p.read_bytes() for p in self.repo.root.joinpath("data").rglob("*.json")}
        _, second = self.reimport()
        self.assertEqual(second["written"], [])
        after = {p: p.read_bytes() for p in self.repo.root.joinpath("data").rglob("*.json")}
        self.assertEqual(before, after)

    def test_reingesting_same_capture_keeps_snapshots(self):
        bundle = {"capture_format": 1, "spreadsheet": {"id": self.repo.config["sources"]["spreadsheet"]["id"]}, "captured_at": "2030-01-01T00:00:00Z", "capture_method": "unit-test", "tabs": []}
        for tab in self.repo.config["sources"]["tabs"]:
            data = fileio.load_json(self.repo.path(tab["snapshot"]))
            bundle["tabs"].append({"sheet_id": data["sheet_id"], "title": data["sheet_title"], "index": data["sheet_index"], "grid": data["grid"], "values": data["values"], "hyperlinks": data["hyperlinks"], "notes": data["notes"], "data_validation": data["data_validation"]})
        self.assertEqual(schema.validate(bundle, self.repo.schemas_dir / "source-capture.schema.json"), [])
        events = importer.ingest_bundle(self.repo, bundle)
        self.assertTrue(all(e["event"] == "unchanged" for e in events), events)
        snapshot = fileio.load_json(self.repo.path("data/source/02-content-direction.json"))
        self.assertEqual(snapshot["captured_at"], "2026-11-05T06:10:44Z", "unchanged tabs keep their original capture time")

    def test_rle_round_trip(self):
        rows = [["a"], *([["", "", "0"]] * 7), [], ["b"]]
        self.assertEqual(sheet.expand_values(sheet.compress_rows(rows)), rows)


class TestRowHandling(ImportTestCase):
    def test_blank_rows_between_ideas_are_ignored(self):
        def insert_blanks(rows):
            rows.insert(5, [])
            rows.insert(6, ["", "", "", "   "])

        edit_snapshot(self.repo, "Content Direction", insert_blanks)
        result, _ = self.reimport()
        self.assertEqual(result.errors, [])
        self.assertEqual(len(self.ideas()), 28)
        self.assertNotIn("allocated", [e["event"] for e in result.id_events])

    def test_ids_stable_when_rows_reordered(self):
        def swap(rows):
            rows[5][3], rows[5][4] = rows[5][4], rows[5][3]

        edit_snapshot(self.repo, "Content Direction", swap)
        self.reimport()
        ideas = self.ideas()
        self.assertEqual(ideas["CTK-L-0001"]["title"], "Cách kết nối Cartek 2 với các dòng xe phổ biến tại Việt Nam")
        self.assertEqual(ideas["CTK-L-0001"]["source"]["ref"], "'Content Direction'!E6")

    def test_title_edited_in_place_keeps_id(self):
        def rename(rows):
            rows[11][5] = "Lỗi P0300: nguyên nhân và cách chẩn đoán"

        edit_snapshot(self.repo, "Content Direction", rename)
        result, _ = self.reimport()
        self.assertEqual(self.ideas()["CTK-L-0015"]["title"], "Lỗi P0300: nguyên nhân và cách chẩn đoán")
        entry = fileio.load_json(self.repo.registry_path)["entries"]["CTK-L-0015"]
        self.assertIn("Lỗi P0300 - Ác Mộng của Mọi Động Cơ?", entry["previous_titles"])
        self.assertIn("renamed", [e["event"] for e in result.id_events])

    def test_new_idea_gets_next_id_and_removed_ids_are_never_reused(self):
        def add(rows):
            rows[11].append("Ý tưởng mới cho kiểm thử")

        edit_snapshot(self.repo, "Content Direction", add)
        self.reimport()
        self.assertEqual(self.ideas()["CTK-L-0017"]["title"], "Ý tưởng mới cho kiểm thử")

        def remove(rows):
            rows[11].pop()

        edit_snapshot(self.repo, "Content Direction", remove)
        self.reimport()
        registry = fileio.load_json(self.repo.registry_path)["entries"]
        self.assertEqual(registry["CTK-L-0017"]["state"], "missing-upstream")

        def add_other(rows):
            rows[11].append("Một ý tưởng khác")

        edit_snapshot(self.repo, "Content Direction", add_other)
        self.reimport()
        self.assertEqual(self.ideas()["CTK-L-0018"]["title"], "Một ý tưởng khác")

    def test_duplicate_and_near_duplicate_ideas(self):
        def duplicate(rows):
            rows[11].append("Lỗi P0300 - Ác Mộng của Mọi Động Cơ?")
            rows[9].append("lỗi p0300 – ác mộng của mọi động cơ")

        edit_snapshot(self.repo, "Content Direction", duplicate)
        result, _ = self.reimport()
        codes = issue_codes(result)
        self.assertIn("duplicate-idea", codes)
        self.assertIn("near-duplicate-idea", codes)
        dupes = [i for i in fileio.load_json(self.repo.normalized_dir / "ideas.json")["records"] if i.get("duplicate_of")]
        self.assertEqual(dupes[0]["id"], "CTK-L-0015", "an exact duplicate shares the original ID")


class TestTrackerRecords(ImportTestCase):
    def add_tracker_rows(self, *rows_to_add):
        def edit(rows):
            for offset, row in enumerate(rows_to_add):
                rows[8 + offset] = row

        edit_snapshot(self.repo, "Video Publish", edit)
        return self.reimport()[0]

    def tracker(self):
        return fileio.load_json(self.repo.normalized_dir / "tracker.json")["records"]

    def test_invalid_and_implausible_dates_are_flagged(self):
        result = self.add_tracker_rows(
            ["Video A", "Các vấn đề lỗi xe thường gặp", "TOYOTA", "", "NONE", "Đang thực hiện", "32/13/2026"],
            ["Video B", "Các vấn đề lỗi xe thường gặp", "FORD", "", "NONE", "Đang thực hiện", "28/08/1999"],
        )
        codes = issue_codes(result)
        self.assertIn("invalid-date", codes)
        self.assertIn("implausible-date", codes)
        records = {r["title"]: r for r in self.tracker()}
        self.assertIsNone(records["Video A"]["publish_date"])
        self.assertIn("invalid-date", records["Video A"]["flags"])

    def test_published_status_needs_date_and_link(self):
        self.add_tracker_rows(
            ["Video C", "Các vấn đề lỗi xe thường gặp", "MAZDA", "", "An", "Đã xuất bản"],
            ["Video D", "Các vấn đề lỗi xe thường gặp", "MAZDA", "CX5", "An", "Đã xuất bản", "01/10/2026", "", "https://youtu.be/abc123"],
        )
        records = {r["title"]: r for r in self.tracker()}
        self.assertIsNone(records["Video C"]["stage_hint"])
        self.assertIn("published-without-evidence", records["Video C"]["flags"])
        self.assertEqual(records["Video D"]["stage_hint"], "PUBLISHED")
        self.assertEqual(records["Video D"]["publish_date"], "2026-10-01")
        self.assertEqual(records["Video D"]["owner"], "An")

    def test_duplicate_titles_detected(self):
        result = self.add_tracker_rows(
            ["Video E", "Các vấn đề lỗi xe thường gặp", "", "", "", "Mới"],
            ["Video E", "Các vấn đề lỗi xe thường gặp", "", "", "", "Mới"],
        )
        self.assertIn("duplicate-title", issue_codes(result))
        records = self.tracker()
        self.assertEqual(records[0]["id"], records[1]["id"])
        self.assertEqual(records[1]["duplicate_of_row"], 9)

    def test_tracker_title_matching_an_idea_reuses_its_id(self):
        self.add_tracker_rows(["Lỗi P0300 - Ác Mộng của Mọi Động Cơ?", "Kiến thức chuyên sâu về hệ thống OBD2", "", "", "", "Mới"])
        record = self.tracker()[0]
        self.assertEqual(record["id"], "CTK-L-0015")
        self.assertTrue(record["linked_idea"])
        self.assertEqual(record["group"], "P4")

    def test_explicit_content_id_links_a_retitled_video(self):
        self.add_tracker_rows(["Lỗi P0300: 3 bước chẩn đoán (tiêu đề đăng thật)", "Kiến thức chuyên sâu về hệ thống OBD2", "", "", "An", "Đang thực hiện", "", "CTK-L-0015"])
        record = self.tracker()[0]
        self.assertEqual(record["id"], "CTK-L-0015")
        self.assertEqual(record["link_method"], "explicit-id")

    def test_test_ids_in_the_sheet_are_ignored(self):
        result = self.add_tracker_rows(["Video thử", "Kiến thức chuyên sâu về hệ thống OBD2", "", "", "", "Mới", "", "CTK-L-9001"])
        self.assertIn("test-content-id", issue_codes(result))
        self.assertNotEqual(self.tracker()[0]["id"], "CTK-L-9001")

    def test_hand_edited_snapshot_is_reported(self):
        from ctk.validate import validate_repo
        path = self.repo.path("data/source/03-short.json")
        path.write_text(path.read_text(encoding="utf-8").replace("Cartek - Check your car", "Cartek - Check"), encoding="utf-8")
        messages = [f.message for f in validate_repo(Repo(self.repo.root)) if f.level == "error"]
        self.assertTrue(any("edited by hand" in m for m in messages), messages)

    def test_record_without_title_is_flagged_not_imported(self):
        result = self.add_tracker_rows(["", "Các vấn đề lỗi xe thường gặp", "", "", "", "Đã xuất bản", "01/10/2026", "", "https://youtu.be/xyz"])
        self.assertIn("record-without-title", issue_codes(result))
        self.assertEqual(self.tracker(), [])


class TestLocalEdits(ImportTestCase):
    def test_hand_edited_generated_file_is_not_overwritten(self):
        path = self.repo.normalized_dir / "ideas.json"
        data = fileio.load_json(path)
        data["records"][0]["title"] = "Edited by hand"
        fileio.write_text(path, fileio.dumps_json(data))
        edited = path.read_text(encoding="utf-8")
        code, out = run("import_sheet", self.repo.root)
        self.assertEqual(code, 2, out)
        self.assertIn("data/normalized/ideas.json", out)
        self.assertEqual(path.read_text(encoding="utf-8"), edited)
        code, out = run("import_sheet", self.repo.root, "--force")
        self.assertEqual(code, 0, out)
        self.assertNotIn("Edited by hand", path.read_text(encoding="utf-8"))

    def test_workspaces_are_never_written_and_drift_is_reported(self):
        code, out = run("new_content", self.repo.root, "--from-idea", "CTK-L-0015")
        self.assertEqual(code, 0, out)
        item_file = next(self.repo.content_dir.glob("long-form/CTK-L-0015-*/item.yaml"))
        before = item_file.read_bytes()

        def rename(rows):
            rows[11][5] = "Tiêu đề đã đổi trên sheet"

        edit_snapshot(self.repo, "Content Direction", rename)
        result, _ = self.reimport()
        self.assertEqual(item_file.read_bytes(), before)
        self.assertEqual([d["event"] for d in result.drift], ["source-changed"])

    def test_check_mode_detects_stale_outputs(self):
        def rename(rows):
            rows[11][5] = "Một tiêu đề khác"

        edit_snapshot(self.repo, "Content Direction", rename)
        code, out = run("import_sheet", self.repo.root, "--check")
        self.assertEqual(code, 1)
        self.assertIn("data/normalized/ideas.json", out)


class TestFetchers(unittest.TestCase):
    class FakeResponse:
        def __init__(self, payload: bytes) -> None:
            self.payload = payload

        def read(self) -> bytes:
            return self.payload

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def test_api_capture_builds_valid_bundle(self):
        meta = {"properties": {"title": "Cartek: Youtube Release", "locale": "en_US", "timeZone": "America/Los_Angeles"},
                "sheets": [{"properties": {"sheetId": 1, "title": "Short", "index": 0, "gridProperties": {"rowCount": 10, "columnCount": 5}}}]}
        values = {"values": [["thời lượng", "< 60 giây"], ["Call to Action ", "Cartek - Check your car"]]}
        grid = {"sheets": [{"data": [{"startRow": 0, "startColumn": 0, "rowData": [{"values": [{}, {"hyperlink": "https://example.com"}]}]}]}]}
        calls = []

        def opener(request):
            calls.append(request)
            assert request.get_method() == "GET"
            url = request.full_url
            if "/values/" in url:
                return self.FakeResponse(json.dumps(values).encode())
            if "includeGridData" in url:
                return self.FakeResponse(json.dumps(grid).encode())
            return self.FakeResponse(json.dumps(meta).encode())

        bundle = fetch.fetch_bundle_api("1r4dfNOPGx50rXMuhZL6Tm0B5XG8nb47t7mSjVdDY-F4", token="test-token", opener=opener, captured_at="2026-11-05T00:00:00Z")
        self.assertEqual(schema.validate(bundle, REPO_ROOT / "schemas" / "source-capture.schema.json"), [])
        self.assertEqual(bundle["tabs"][0]["hyperlinks"], {"B1": "https://example.com"})
        self.assertTrue(all(c.get_header("Authorization") == "Bearer test-token" for c in calls))

    def test_csv_capture_rejects_login_page(self):
        def opener(request):
            return self.FakeResponse(b"<!DOCTYPE html><html>Sign in</html>")

        with self.assertRaises(RuntimeError):
            fetch.fetch_bundle_csv("1r4dfNOPGx50rXMuhZL6Tm0B5XG8nb47t7mSjVdDY-F4", [{"title": "Short", "sheet_id": 1}], opener=opener)

    def test_capture_requires_credentials(self):
        with self.assertRaises(RuntimeError):
            fetch.fetch_bundle_api("x" * 20)


class TestParsers(unittest.TestCase):
    def test_parse_duration(self):
        self.assertEqual(sheet.parse_duration("5-8 phút"), {"min_seconds": 300, "max_seconds": 480, "max_inclusive": True})
        self.assertEqual(sheet.parse_duration("< 60 giây"), {"min_seconds": None, "max_seconds": 60, "max_inclusive": False})
        self.assertIsNone(sheet.parse_duration("khoảng vài phút"))

    def test_parse_date(self):
        formats = ["%d/%m/%Y", "%Y-%m-%d"]
        self.assertEqual(str(sheet.parse_date("01/10/2026", formats)), "2026-10-01")
        self.assertIsNone(sheet.parse_date("32/13/2026", formats))
        self.assertIsNone(sheet.parse_date("", formats))

    def test_snapshot_hash_ignores_capture_time(self):
        a = TabSnapshot("id", "T", [["x"]], "2026-01-01T00:00:00Z", "m1")
        b = TabSnapshot("id", "T", [["x"]], "2027-01-01T00:00:00Z", "m2")
        self.assertEqual(a.content_hash(), b.content_hash())


if __name__ == "__main__":
    unittest.main()
