"""Quality-control gates G1-G8 and approval rules.

Gate results:
  PASS     the gate's criteria are met, with evidence.
  FAIL     a deliverable exists and breaks a rule: the writer must correct it.
  BLOCKED  the gate cannot pass yet: a deliverable is unfinished, evidence is
           missing, or a prerequisite (source, sign-off, asset) is outstanding.

The automated gates never look at the stage the writer chose: an item is
evaluated on its files only. Approval additionally requires independent
judgment reviews recorded on the *current* content fingerprint.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from . import export, mdparse, schema
from . import textutil as tu
from .context import Context, describe_target, within_target
from .items import DELIVERABLES, today
from .registry import is_test_id
from .sheet import is_youtube_url

PASS, FAIL, BLOCKED = "PASS", "FAIL", "BLOCKED"
GATES = ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8")


@dataclass
class GateResult:
    gate: str
    name: str
    findings: list[tuple[str, str, str]] = field(default_factory=list)

    def ok(self, evidence: str) -> None:
        self.findings.append(("PASS", evidence, ""))

    def fail(self, evidence: str, correction: str) -> None:
        self.findings.append((FAIL, evidence, correction))

    def block(self, evidence: str, correction: str) -> None:
        self.findings.append((BLOCKED, evidence, correction))

    def warn(self, evidence: str, correction: str = "") -> None:
        self.findings.append(("WARN", evidence, correction))

    def info(self, evidence: str) -> None:
        self.findings.append(("INFO", evidence, ""))

    @property
    def problems(self) -> bool:
        return any(level in (FAIL, BLOCKED) for level, _, _ in self.findings)

    @property
    def result(self) -> str:
        levels = {level for level, _, _ in self.findings}
        return FAIL if FAIL in levels else BLOCKED if BLOCKED in levels else PASS

    def evidence_lines(self) -> list[str]:
        return [f"[{level}] {evidence}" for level, evidence, _ in self.findings]

    def corrections(self) -> list[str]:
        out = []
        for level, _, correction in self.findings:
            if correction and correction not in out and level in (FAIL, BLOCKED, "WARN"):
                out.append(correction)
        return out

    def summary(self) -> str:
        for wanted in (FAIL, BLOCKED):
            for level, evidence, _ in self.findings:
                if level == wanted:
                    return evidence
        passes = [evidence for level, evidence, _ in self.findings if level == "PASS"]
        return passes[0] if passes else "No problems found."


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?…])\s+|\n+", text) if s.strip()]


def _public_script_text(ctx: Context) -> str:
    parts = []
    for segment in ctx.script.segments:
        parts.extend([segment.get("VO"), segment.get("ON-SCREEN"), segment.get("SAFETY")])
    return "\n".join(p for p in parts if p)


def _public_seo_text(ctx: Context) -> str:
    seo = ctx.data.get("seo") or {}
    parts = [seo.get("recommended_title", ""), seo.get("description", ""), seo.get("pinned_comment", "")]
    parts += list(seo.get("title_candidates") or []) + list(seo.get("tags") or [])
    parts += [c.get("on_image_text", "") for c in seo.get("thumbnail_concepts") or []]
    return "\n".join(p for p in parts if p)


_DTC_RANGE = re.compile(r"\b([PBCU][0-3])([0-9A-F]{3})\s*(?:-|–|—|to|đến|den)\s*([PBCU][0-3])([0-9A-F]{3})\b", re.IGNORECASE)


def codes_covered(text: str, dtc_pattern: str) -> set[str]:
    """DTCs a claim text covers: single codes plus expanded ranges ("P0301-P0312")."""
    covered = {m.upper() for m in re.findall(dtc_pattern, text, flags=re.IGNORECASE)}
    for match in _DTC_RANGE.finditer(text):
        prefix, start, prefix_end, end = (g.upper() for g in match.groups())
        if prefix != prefix_end:
            continue
        base = 10 if (start + end).isdigit() else 16
        low, high = int(start, base), int(end, base)
        if 0 <= high - low <= 512:
            width = "03d" if base == 10 else "03X"
            covered.update(f"{prefix}{format(n, width)}" for n in range(low, high + 1))
    return covered


def draft_marker_hits(text: str, markers: list[str]) -> list[str]:
    """Sentences of ``text`` that contain placeholder wording."""
    hits = []
    for sentence in _sentences(text):
        plain = tu.match_text(sentence)
        if any(re.search(marker, plain) for marker in markers):
            hits.append(sentence)
    return hits


def _snippet(text: str, limit: int = 90) -> str:
    text = tu.clean(text)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def youtube_tags_length(tags: list[str]) -> int:
    """Length as YouTube counts it: commas count, tags with spaces count 2 extra (quotes)."""
    if not tags:
        return 0
    return sum(len(tag) + (2 if " " in tag else 0) for tag in tags) + len(tags) - 1


def chapter_problems(chapters: list[dict[str, Any]], min_count: int, min_seconds: int, runtime: float | None) -> list[str]:
    problems = []
    if len(chapters) < min_count:
        problems.append(f"{len(chapters)} chapter(s); YouTube needs at least {min_count}.")
    times = [mdparse.parse_timestamp(c.get("time", "")) for c in chapters]
    if any(t is None for t in times):
        problems.append("A chapter time is not a valid timestamp (use MM:SS or H:MM:SS).")
        return problems
    if times and times[0] != 0:
        problems.append("The first chapter must start at 00:00.")
    for (a, b), chapter in zip(zip(times, times[1:]), chapters[1:]):
        if b <= a:
            problems.append(f"Chapter '{chapter['title']}' ({chapter['time']}) is not after the previous one.")
        elif b - a < min_seconds:
            problems.append(f"The chapter before {chapter['time']} is shorter than {min_seconds} s.")
    if runtime and times and runtime - times[-1] < min_seconds:
        problems.append(f"The last chapter ({chapters[-1]['time']}) starts less than {min_seconds} s before the estimated end ({mdparse.format_timestamp(runtime)}).")
    return problems


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------
def integrity_problems(ctx: Context) -> list[tuple[str, str]]:
    """Structural problems that make the repository inconsistent (also used by validate_content)."""
    problems: list[tuple[str, str]] = []
    item, data, repo = ctx.item, ctx.data, ctx.repo
    fmt = item.format
    expected = repo.format_dir(fmt).resolve()
    if item.path.parent.resolve() != expected:
        problems.append((f"Workspace is in {repo.rel(item.path.parent)}, expected {repo.rel(expected)} for format {fmt}.", "Move the workspace folder to the directory for its format."))
    if not item.path.name.startswith(item.id):
        problems.append((f"Folder {item.path.name} does not start with {item.id}.", "Rename the folder to <ID>-<slug>."))
    if item.id.split("-")[1] != repo.format_codes()[fmt]:
        problems.append((f"{item.id} has the wrong letter for format {fmt}.", "Long-form IDs use L, Shorts use S."))
    if item.id not in ctx.registry.entries:
        problems.append((f"{item.id} is not registered in data/id-registry.json.", "Create workspaces with scripts/new_content.py so IDs are registered."))
    if is_test_id(item.id) != item.is_test:
        problems.append(("test_item does not match the ID range (9001-9999 = test items only).", "Use a production ID for real content and keep test items in the 9xxx range."))
    if data["provenance"]["origin"] == "test" and not item.is_test:
        problems.append(("provenance.origin is 'test' but test_item is false.", "Test provenance is only for test items."))
    pillar = data["pillar"]
    prefix = "P" if fmt == "long-form" else "S"
    if ctx.groups.get(pillar) is None or not pillar.startswith(prefix):
        options = ", ".join(code for code in ctx.groups if code.startswith(prefix))
        problems.append((f"'{pillar}' is not a {fmt} pillar/category in data/normalized/taxonomy.json.", f"Use one of: {options}."))
    audience = data["audience"]
    for persona in [audience["primary"], *audience["secondary"]]:
        if persona not in ctx.personas:
            problems.append((f"Audience '{persona}' is not a persona in data/normalized/personas.json.", f"Use one of: {', '.join(ctx.personas)}."))
    if data["video_type"] not in ctx.taxonomy["video_types"]:
        problems.append((f"video_type '{data['video_type']}' is not in config/taxonomy.yaml.", f"Use one of: {', '.join(ctx.taxonomy['video_types'])}."))
    if data["search_intent"] not in ctx.taxonomy["search_intents"]:
        problems.append((f"search_intent '{data['search_intent']}' is not in config/taxonomy.yaml.", f"Use one of: {', '.join(ctx.taxonomy['search_intents'])}."))
    for key in DELIVERABLES:
        if key == "storyboard" and fmt == "short":
            continue
        if not item.deliverable(key).exists():
            problems.append((f"{DELIVERABLES[key]} is missing.", "Restore it from templates/ (scripts/new_content.py creates it)."))
    return problems


def gate_g1(ctx: Context, schema_errors: list[str]) -> GateResult:
    g = GateResult("G1", ctx.policy["gates"]["G1"])
    data = ctx.data
    for error in schema_errors[:20]:
        g.fail(f"item.yaml: {error}", "Fix item.yaml to match schemas/content.schema.json (field guide: templates/item.yaml).")
    if len(schema_errors) > 20:
        g.fail(f"{len(schema_errors) - 20} more schema errors.", "")
    if schema_errors:
        return g
    for evidence, correction in integrity_problems(ctx):
        g.fail(evidence, correction)
    provenance = data["provenance"]
    source = provenance.get("source_record")
    if source:
        idea = ctx.ideas.get(source)
        if idea is None:
            g.warn(f"Source idea {source} is not an active record in data/normalized/ideas.json.", "Check reports/import-report.md; the idea may have been renamed or removed in the sheet.")
        elif tu.clean(provenance.get("source_title")) != idea["title"]:
            g.warn(f"Upstream title of {source} is now '{idea['title']}'.", "Review the change; update provenance.source_title once the workspace reflects it.")
        else:
            g.ok(f"Provenance: {source} from {provenance.get('source_ref')}.")
    group = ctx.groups.get(data["pillar"])
    if group:
        g.ok(f"{data['pillar']}: {group['name']}.")
    if data["vehicle"]["scope"] == "specific" and not data["vehicle"]["brands"]:
        g.fail("vehicle.scope is 'specific' but no brand is named.", "Name the brand(s), model(s), years and engines covered.")
    for key in ("working_title", "problem", "takeaway"):
        if not tu.clean(data.get(key)):
            g.fail(f"item.yaml -> {key} is empty.", f"Fill in item.yaml -> {key}.")
    if not tu.clean(data["keywords"]["primary"]):
        g.fail("item.yaml -> keywords.primary is empty.", "Fill in item.yaml -> keywords.primary.")
    if not g.problems:
        g.ok("Metadata complete; ID, folder, provenance and vocabularies consistent.")
    return g


def gate_g2(ctx: Context) -> GateResult:
    g = GateResult("G2", ctx.policy["gates"]["G2"])
    text = ctx.texts["brief"]
    if not text:
        g.block("brief.md is missing.", "Create it from templates/content-brief.md.")
        return g
    for section in ctx.policy["brief_required_sections"]:
        body = mdparse.find_section(text, section)
        if body is None:
            g.fail(f"brief.md has no '## {section}' section.", f"Add '## {section}' (see templates/content-brief.md).")
        elif not body.strip():
            g.fail(f"brief.md '## {section}' is empty.", f"Write the {section.lower()} section.")
    todos = mdparse.todo_count(text)
    if todos:
        g.block(f"brief.md still has {todos} [TODO] marker(s).", "Complete the brief (skill: cartek-content-strategist).")
    primary = ctx.data["audience"]["primary"]
    persona = ctx.personas.get(primary)
    if persona and persona.get("priority") == "low":
        g.warn(f"Primary audience '{primary}' is marked '(ít)' (smaller segment) in the sheet.", "Confirm that targeting this segment is deliberate.")
    if not g.problems:
        name = persona["name"] if persona else primary
        g.ok(f"Brief complete for primary audience {name}.")
    g.info("Relevance and audience fit also need an independent judgment review (role qc).")
    return g


def gate_g3(ctx: Context) -> GateResult:
    g = GateResult("G3", ctx.policy["gates"]["G3"])
    data = ctx.data
    text = ctx.texts["research"]
    if not text:
        g.block("research.md is missing.", "Create it from templates/research-report.md.")
    else:
        for section in ctx.policy["research_required_sections"]:
            if mdparse.find_section(text, section) is None:
                g.fail(f"research.md has no '## {section}' section.", f"Add '## {section}' (see templates/research-report.md).")
        todos = mdparse.todo_count(text)
        if todos:
            g.block(f"research.md still has {todos} [TODO] marker(s).", "Complete the research (skill: automotive-researcher).")
    sources: dict[str, dict[str, Any]] = {}
    for source in data["sources"]:
        if source["id"] in sources:
            g.fail(f"Source ID {source['id']} is used twice.", "Give every source a unique ID.")
        sources[source["id"]] = source
        if source["type"] not in ctx.taxonomy["source_types"]:
            g.fail(f"{source['id']} has unknown type '{source['type']}'.", f"Use one of: {', '.join(ctx.taxonomy['source_types'])}.")
        if source.get("url") and not source.get("accessed"):
            g.fail(f"{source['id']} has a URL but no access date.", "Record the date you read it (accessed: YYYY-MM-DD).")
    claims = data["claims"]
    seen: set[str] = set()
    for claim in claims:
        if claim["id"] in seen:
            g.fail(f"Claim ID {claim['id']} is used twice.", "Give every claim a unique ID.")
        seen.add(claim["id"])
    active = [c for c in claims if c["status"] != "removed"]
    if len(active) < ctx.policy["min_claims"]:
        g.block("No technical claims are registered.", "Register every technical statement as a claim with sources (skill: automotive-researcher).")
    requirements = ctx.policy["claim_source_requirements"]
    for claim in claims:
        cid = claim["id"]
        if claim["category"] not in ctx.taxonomy["claim_categories"]:
            g.fail(f"{cid} has unknown category '{claim['category']}'.", f"Use one of: {', '.join(ctx.taxonomy['claim_categories'])}.")
        dangling = [s for s in claim["sources"] if s not in sources]
        if dangling:
            g.fail(f"{cid} cites unknown source(s) {', '.join(dangling)}.", "Add the sources to item.yaml -> sources or fix the IDs.")
        if claim["status"] == "removed":
            continue
        if claim["status"] in ("unverified", "disputed"):
            g.block(f"{cid} is {claim['status']}: \"{_snippet(claim['text'])}\"", "Verify it with an accepted source, or mark it removed and take it out of the script (skill: technical-fact-checker).")
        if claim["status"] == "verified":
            accepted = requirements.get(claim["category"], [])
            types = [sources[s]["type"] for s in claim["sources"] if s in sources]
            if not types:
                g.fail(f"{cid} is marked verified but cites no source.", "Cite the evidence or set status: unverified.")
            elif accepted and not any(t in accepted for t in types):
                g.fail(f"{cid} ({claim['category']}) is verified only by {', '.join(sorted(set(types)))}.", f"Add a source of an accepted type: {', '.join(accepted)}.")
            if not claim.get("verified_by") or not claim.get("verified_on"):
                g.fail(f"{cid} is verified but has no verified_by/verified_on.", "Record who verified it and when.")
        if claim["category"] == "cartek-feature":
            feature_id = claim.get("feature_id")
            feature = ctx.features.get(feature_id) if feature_id else None
            if feature is None:
                g.block(f"{cid} describes a Cartek 2 capability that is not in the feature register.", "Add it to data/reference/cartek-2-feature-register.yaml with product-team evidence, then set feature_id.")
            elif feature.get("status") != "verified":
                g.block(f"{cid}: Cartek 2 feature {feature_id} is '{feature.get('status')}' in the register.", "Obtain written product-team confirmation or a recorded hands-on test.")
    claim_index = {c["id"]: c for c in claims}
    cited: dict[str, list[str]] = {}
    for segment in ctx.script.segments:
        for cid in segment.claims:
            cited.setdefault(cid, []).append(segment.id)
    for cid, segments in sorted(cited.items()):
        if cid not in claim_index:
            g.fail(f"script.md {', '.join(segments)} cite {cid}, which is not in item.yaml claims.", "Register the claim or fix the reference.")
        elif claim_index[cid]["status"] == "removed":
            g.fail(f"script.md {', '.join(segments)} still cite removed claim {cid}.", "Remove the statement from the script.")
    unused = [c["id"] for c in claims if c["status"] == "verified" and c["id"] not in cited]
    if unused:
        g.info(f"Verified claims not cited by any script segment: {', '.join(unused)}.")
    if not g.problems:
        verified = sum(1 for c in claims if c["status"] == "verified")
        g.ok(f"{verified} claim(s) verified with accepted sources; {len(sources)} source(s) registered.")
    return g


def gate_g4(ctx: Context) -> GateResult:
    g = GateResult("G4", ctx.policy["gates"]["G4"])
    fmt = ctx.item.format
    policy = ctx.policy
    if not ctx.texts["script"]:
        g.block("script.md is missing.", "Create it from the script template for the format.")
        return g
    doc = ctx.script
    for section in doc.missing_sections:
        g.fail(f"script.md has no '## {section}' section.", "Keep the section headings from the script template.")
    for problem in doc.problems:
        g.fail(f"script.md: {problem}", "Follow the segment conventions in templates/long-form-script.md.")
    if doc.todo_count:
        g.block(f"script.md still has {doc.todo_count} [TODO] marker(s).", "Finish the script (skill: youtube-scriptwriter).")
    hooks = [h for h in doc.hook_candidates if not mdparse.TODO.search(h)]
    if not doc.todo_count and len(hooks) < policy["min_hook_candidates"]:
        g.fail(f"{len(hooks)} hook candidate(s); at least {policy['min_hook_candidates']} required.", "Write more hook candidates under '## Hook candidates'.")
    selected = doc.selected_hook
    if not doc.todo_count and (not selected.get("HOOK") or not selected.get("RATIONALE")):
        g.fail("Selected hook or its rationale is missing.", "Fill **HOOK:** and **RATIONALE:** under '## Selected hook'.")
    if not doc.todo_count and len(doc.outline) < policy["min_outline_items"][fmt]:
        g.fail(f"Outline has {len(doc.outline)} item(s); at least {policy['min_outline_items'][fmt]} required.", "Complete '## Outline'.")
    segments = doc.segments
    if len(segments) < policy["min_segments"][fmt]:
        g.fail(f"{len(segments)} segment(s); at least {policy['min_segments'][fmt]} required for {fmt}.", "Add segments under '## Script'.")
    for segment in segments:
        if segment.type not in mdparse.SEGMENT_TYPES:
            g.fail(f"{segment.id}: TYPE '{segment.get('TYPE')}' is not one of {', '.join(mdparse.SEGMENT_TYPES)}.", "Set a valid **TYPE:**.")
        if not segment.get("VO") and not (segment.type == "demo" and segment.demo_seconds > 0):
            g.fail(f"{segment.id} has no narration (**VO:**).", "Write the voice-over, or give a silent demo DEMO-SECONDS > 0.")
        if not segment.get("VISUAL"):
            g.fail(f"{segment.id} has no **VISUAL:** instruction.", "Describe what is on screen.")
        if segment.demo_seconds < 0:
            g.fail(f"{segment.id}: DEMO-SECONDS is not a number.", "Use a number of seconds, e.g. 12.")
    if segments:
        if segments[0].type != "hook":
            g.fail(f"The first segment ({segments[0].id}) is not TYPE hook.", "Open with the selected hook.")
        last = segments[-1]
        if last.type != "cta":
            g.fail(f"The last segment ({last.id}) is not TYPE cta.", "End with the call to action.")
        tagline = policy["brand_tagline"]
        if last.type == "cta" and tu.match_text(tagline) not in tu.match_text(last.get("VO") + " " + last.get("ON-SCREEN")):
            g.fail(f"The CTA does not include the brand line '{tagline}'.", f"Add '{tagline}' to the CTA voice-over or on-screen text.")
    total = ctx.total_seconds
    if doc.todo_count or not segments:
        g.info(f"Runtime estimate so far: {mdparse.format_timestamp(total)} (narration incomplete).")
    elif not within_target(total, ctx.target):
        g.fail(
            f"Estimated runtime {mdparse.format_timestamp(total)} is outside the target {describe_target(ctx.target)} ({ctx.target['source']}).",
            "Cut or expand narration, adjust DEMO-SECONDS, or record production.runtime_exception with a rationale.",
        )
    else:
        g.ok(f"Estimated runtime {mdparse.format_timestamp(total)} within target {describe_target(ctx.target)}.")
        hook_limit = ctx.production["hook_max_seconds"][fmt]
        if ctx.timing and ctx.timing[0]["seconds"] > hook_limit:
            g.warn(f"Hook segment runs about {ctx.timing[0]['seconds']} s (guide: ≤ {hook_limit} s).", "Tighten the hook.")
    for sentence in draft_marker_hits(mdparse.without_todos(_public_script_text(ctx)), policy.get("draft_markers", [])):
        g.block(f"Placeholder wording in narration or on-screen text: \"{_snippet(sentence)}\"", "Replace the placeholder with final wording before review.")
    if not doc.retention_notes or all(mdparse.TODO.search(n) for n in doc.retention_notes):
        g.warn("No retention notes.", "List open loops, pattern changes and payoffs under '## Retention notes'.")
    if not g.problems:
        g.ok(f"{len(segments)} segments with narration and visuals; hook first, CTA last.")
    g.info("Clarity, coherence and retention quality also need an independent judgment review (role qc).")
    return g


def gate_g5(ctx: Context) -> GateResult:
    g = GateResult("G5", ctx.policy["gates"]["G5"])
    policy, data = ctx.policy, ctx.data
    if ctx.script.todo_count or not ctx.script.segments:
        g.block("The script is not finished; the technical and safety review needs the final narration.", "Finish script.md first (G4), then re-run QC.")
    if not ctx.texts["research"] or mdparse.todo_count(ctx.texts["research"]):
        g.block("research.md is not finished; technical accuracy cannot be reviewed yet.", "Finish the research first (G3).")
    public = mdparse.without_todos(_public_script_text(ctx) + "\n" + _public_seo_text(ctx))
    debunk = [re.compile(p) for p in policy.get("debunk_markers", [])]
    for rule in policy["banned_patterns"]:
        pattern = re.compile(rule["pattern"])
        for sentence in _sentences(public):
            plain = tu.match_text(sentence)
            if pattern.search(plain):
                if any(marker.search(plain) for marker in debunk):
                    g.warn(f"Possible myth-debunking use of banned wording: \"{_snippet(sentence)}\"", "Reviewer: confirm the sentence clearly says this is wrong.")
                else:
                    g.fail(f"{rule['reason']} \"{_snippet(sentence)}\"", "Rewrite: clearing a code removes the record/lamp only; the cause must be diagnosed and repaired.")
    for rule in policy["review_patterns"]:
        pattern = re.compile(rule["pattern"])
        for sentence in _sentences(public):
            if pattern.search(tu.match_text(sentence)):
                g.warn(f"{rule['reason']} \"{_snippet(sentence)}\"", "Reviewer: confirm this wording is supported by a verified claim.")
    vo_text = tu.match_text(mdparse.without_todos("\n".join(s.get("VO") for s in ctx.script.segments)))
    if any(re.search(p, vo_text) for p in policy["clear_codes_mentions"]):
        if not any(re.search(p, vo_text) for p in policy["clear_codes_caveat_markers"]):
            g.fail("The narration mentions clearing codes/resetting the lamp without saying it does not fix the cause.", "Add a caveat: clearing removes the code and the lamp; the fault returns if the cause is not repaired.")
    covered: set[str] = set()
    for claim in data["claims"]:
        if claim["status"] != "removed":
            covered |= codes_covered(claim["text"], policy["dtc_pattern"])
    # Codes shown on screen count too: VISUAL and B-ROLL describe what the camera shows.
    shown = "\n".join(s.get(field) for s in ctx.script.segments for field in ("VISUAL", "B-ROLL"))
    codes = sorted({m.upper() for m in re.findall(policy["dtc_pattern"], public + "\n" + mdparse.without_todos(shown), flags=re.IGNORECASE)})
    manufacturer = [re.compile(p) for p in policy["manufacturer_specific_dtc_patterns"]]
    for code in codes:
        if code not in covered:
            g.fail(f"DTC {code} appears in public text or on screen but no claim defines it.", f"Register a claim stating what {code} means, with a standard or OEM source.")
        if any(p.search(code) for p in manufacturer) and (data["vehicle"]["scope"] != "specific" or not data["vehicle"]["brands"]):
            g.fail(f"{code} is a manufacturer-controlled code range but the item is not vehicle-specific.", "Name the make/model/year whose service information defines this code.")
    corpus = tu.match_text(" ".join([data.get("working_title", ""), *(mdparse.without_todos(ctx.texts[k]) for k in ("brief", "research", "script"))]))
    flags = list(data["safety"]["flags"])
    dismissed = {d["flag"] for d in data["safety"]["dismissed"]}
    for flag in flags + sorted(dismissed):
        if flag not in ctx.taxonomy["safety_flags"]:
            g.fail(f"Unknown safety flag '{flag}'.", f"Use one of: {', '.join(ctx.taxonomy['safety_flags'])}.")
    for flag, patterns in policy["safety_terms"].items():
        hit = next((m.group(0) for p in patterns if (m := re.search(p, corpus))), None)
        if hit and flag not in flags and flag not in dismissed:
            g.fail(f"Safety-relevant wording for '{flag}' found (\"{hit}\") but the item neither flags nor dismisses it.", "Add the flag to safety.flags (needs a qualified human technical review) or add safety.dismissed with a rationale.")
    if flags:
        has_safety_text = any(s.type == "safety" or s.get("SAFETY") for s in ctx.script.segments)
        if not has_safety_text and ctx.script.segments:
            g.fail(f"Safety flags ({', '.join(flags)}) but the script has no safety warning.", "Add a TYPE safety segment or a **SAFETY:** line where the risk occurs.")
        g.info(f"Safety flags {', '.join(flags)}: a qualified human technical review is required before approval.")
    for claim in data["claims"]:
        if claim["category"] in ("safety", "diagnostic-procedure") and claim["status"] in ("unverified", "disputed"):
            g.block(f"{claim['id']} ({claim['category']}) is {claim['status']}: technical approval is blocked.", "Verify the procedure/safety statement with OEM or standard sources, or remove it.")
    if not g.problems:
        g.ok("No banned wording; DTCs covered by claims; safety topics flagged or dismissed with rationale.")
    g.info("Automotive accuracy also needs an independent technical review (role technical).")
    return g


def gate_g6(ctx: Context) -> GateResult:
    g = GateResult("G6", ctx.policy["gates"]["G6"])
    policy, limits, fmt = ctx.policy, ctx.platform, ctx.item.format
    seo = ctx.data["seo"]
    text = ctx.texts["seo"]
    if not text:
        g.block("seo.md is missing.", "Create it from templates/seo-package.md.")
    else:
        for section in policy["seo_required_sections"]:
            if mdparse.find_section(text, section) is None:
                g.fail(f"seo.md has no '## {section}' section.", f"Add '## {section}' (see templates/seo-package.md).")
        todos = mdparse.todo_count(text)
        if todos:
            g.block(f"seo.md still has {todos} [TODO] marker(s).", "Complete the SEO analysis (skill: youtube-seo-specialist).")
    candidates = [t for t in seo["title_candidates"] if tu.clean(t)]
    if len(candidates) < policy["min_title_candidates"]:
        g.fail(f"{len(candidates)} title candidate(s) in item.yaml; at least {policy['min_title_candidates']} required.", "Fill seo.title_candidates.")
    title = tu.clean(seo["recommended_title"])
    if not title:
        g.fail("No recommended title.", "Fill seo.recommended_title.")
    elif len(title) > limits["title"]["max_chars"]:
        g.fail(f"Title has {len(title)} characters; YouTube allows {limits['title']['max_chars']}.", "Shorten the title.")
    elif len(title) > limits["title_soft_max_chars"]:
        g.warn(f"Title has {len(title)} characters; it may be truncated in search results.", "Put the key words first.")
    if not tu.clean(seo["title_rationale"]):
        g.fail("No rationale for the recommended title.", "Fill seo.title_rationale.")
    description = seo["description"] or ""
    full_description = export.description_with_chapters(seo) if fmt == "long-form" else description
    if not description.strip():
        g.fail("No description.", "Write seo.description.")
    elif len(full_description) > limits["description"]["max_chars"]:
        g.fail(f"Description with chapter lines has {len(full_description)} characters; YouTube allows {limits['description']['max_chars']}.", "Shorten the description.")
    if re.search(r"(?m)^\s*0?0:00\b", description):
        g.warn("seo.description already contains chapter timestamps.", "Keep chapters only in seo.chapters; the export appends them to the description.")
    tags = [t for t in seo["tags"] if tu.clean(t)]
    if len(tags) < policy["min_tags"]:
        g.fail(f"{len(tags)} tag(s); at least {policy['min_tags']} required.", "Add tags from the keyword notes.")
    tag_length = youtube_tags_length(tags)
    if tag_length > limits["tags"]["max_chars_total"]:
        g.fail(f"Tags total {tag_length} characters as YouTube counts them; limit {limits['tags']['max_chars_total']}.", "Remove or shorten tags.")
    for sentence in draft_marker_hits(_public_seo_text(ctx), policy.get("draft_markers", [])):
        g.block(f"Placeholder wording in the SEO metadata (item.yaml seo): \"{_snippet(sentence)}\"", "Replace the placeholder with final wording.")
    if fmt == "long-form":
        chapters = seo["chapters"]
        narration_done = bool(ctx.script.segments) and not ctx.script.todo_count
        runtime = ctx.total_seconds if narration_done else None
        problems = chapter_problems(chapters, limits["chapters"]["min_count"], limits["chapters"]["min_chapter_seconds"], runtime)
        if problems and not narration_done:
            g.block("Chapters cannot be set yet: they need the timing of the finished narration.", "Finish script.md, then build chapters from `python3 scripts/qc_content.py runtime <ID>`.")
        else:
            for problem in problems:
                g.fail(f"Chapters: {problem}", "Build chapters from `python3 scripts/qc_content.py runtime <ID>` timings.")
    thumbnails = seo["thumbnail_concepts"]
    needed = policy["min_thumbnail_concepts"][fmt]
    if len(thumbnails) < needed:
        g.fail(f"{len(thumbnails)} thumbnail concept(s); at least {needed} required.", "Add thumbnail concepts with on-image text.")
    for concept in thumbnails:
        if len(tu.clean(concept.get("on_image_text")).split()) > 6:
            g.warn(f"Thumbnail text \"{concept['on_image_text']}\" is long for a phone screen.", "Keep on-image text to about 4-5 words.")
    public = mdparse.without_todos(_public_seo_text(ctx) + "\n" + text)
    for pattern in policy["performance_claim_patterns"]:
        for sentence in _sentences(public):
            if re.search(pattern, tu.match_text(sentence)):
                g.fail(f"Unsupported performance claim: \"{_snippet(sentence)}\"", "Remove promises about CTR, ranking, views or virality.")
    keyword = tu.match_text(ctx.data["keywords"]["primary"])
    if keyword and title and keyword not in tu.match_text(title) and keyword not in tu.match_text(description):
        g.warn("The primary keyword appears in neither the title nor the description.", "Use the primary keyword naturally in the title or the first description lines.")
    for related in seo["related_content"]:
        if related not in ctx.registry.entries:
            g.fail(f"Related content {related} is not a registered ID.", "Fix the ID.")
    if not g.problems:
        g.ok(f"Title ({len(title)} chars), description, {len(tags)} tags, thumbnails{', chapters' if fmt == 'long-form' else ''} complete.")
    return g


def gate_g7(ctx: Context, g4: GateResult) -> GateResult:
    g = GateResult("G7", ctx.policy["gates"]["G7"])
    data, fmt = ctx.data, ctx.item.format
    if g4.result != PASS:
        g.block(f"Script gate G4 is {g4.result}; the production handoff needs a finished script.", "Resolve G4 first.")
    storyboard = ctx.texts["storyboard"]
    if fmt == "long-form":
        if not storyboard:
            g.block("storyboard.md is missing.", "Create it from templates/storyboard.md.")
        elif mdparse.todo_count(storyboard):
            g.block(f"storyboard.md still has {mdparse.todo_count(storyboard)} [TODO] marker(s).", "Complete the shot list.")
        elif not mdparse.parse_table(mdparse.find_section(storyboard, "Shot list")):
            g.fail("storyboard.md has no shots in '## Shot list'.", "List the shots.")
    production = data["production"]
    assets = production["assets_required"]
    if not assets:
        g.fail("No production assets are listed.", "List tools, vehicles, graphics and footage in production.assets_required.")
    for asset in assets:
        if asset["type"] not in ctx.taxonomy["asset_types"] or asset["status"] not in ctx.taxonomy["asset_statuses"]:
            g.fail(f"Asset '{asset['item']}' has an unknown type or status.", f"Types: {', '.join(ctx.taxonomy['asset_types'])}; statuses: {', '.join(ctx.taxonomy['asset_statuses'])}.")
    pending = [a["item"] for a in assets if a["status"] in ("needed", "requested")]
    if pending:
        g.block(f"Assets not yet available: {', '.join(pending)}.", "Confirm availability and set status to available or confirmed.")
    if any(s.type == "demo" for s in ctx.script.segments):
        setup = production.get("demo_setup") or {}
        if not setup.get("tool") or not (setup.get("vehicle") or setup.get("location")):
            g.fail("Demo segments exist but production.demo_setup lacks the tool and vehicle/location.", "Record tool, tool version, vehicle and location.")
    if not tu.clean(data.get("owner")):
        g.fail("No responsible person (owner).", "Set item.yaml -> owner (Người phụ trách).")
    if not data.get("target_publish_date"):
        g.fail("No target publish date.", "Set item.yaml -> target_publish_date.")
    try:
        package = export.build_package(ctx, approved=False, blocking=[])
        errors = schema.validate(package, ctx.repo.schemas_dir / "production-package.schema.json")
        for error in errors[:5]:
            g.fail(f"Production package does not validate: {error}", "Fix the source fields the error points to.")
    except Exception as exc:  # noqa: BLE001 - surface any build failure as a finding
        g.fail(f"Production package could not be built: {exc}", "Check script.md and item.yaml structure.")
    if not g.problems:
        g.ok(f"Script, {'storyboard, ' if fmt == 'long-form' else ''}{len(assets)} confirmed asset(s), owner and date ready; draft package validates.")
    return g


def gate_g8(ctx: Context) -> GateResult:
    g = GateResult("G8", ctx.policy["gates"]["G8"])
    data = ctx.data
    publication = data["publication"]
    stage = ctx.item.stage
    if not data.get("target_publish_date"):
        g.fail("No target publish date.", "Set item.yaml -> target_publish_date.")
    if not publication.get("visibility_plan"):
        g.fail("No visibility plan.", "Set publication.visibility_plan (public, scheduled, unlisted or private).")
    boxes = mdparse.checkboxes(mdparse.find_section(ctx.texts["seo"], "Publishing checklist"))
    if not boxes:
        g.fail("seo.md has no publishing checklist items.", "Restore the checklist from templates/seo-package.md.")
    else:
        unchecked = [label for done, label in boxes if not done]
        if unchecked:
            g.block(f"{len(unchecked)} of {len(boxes)} publishing checklist item(s) in seo.md are not ticked.", "Complete each item and tick it ([x]) before approval.")
    published = stage in ("PUBLISHED", "PERFORMANCE_REVIEW")
    unpublished = [cid for cid in data["seo"]["related_content"] if not _is_published(ctx, cid)]
    if unpublished:
        g.warn(f"Related content not yet published: {', '.join(unpublished)}; YouTube end screens and cards can only link published videos.", "Link only published videos at upload; keep the others for later updates.")
    if published:
        if not publication.get("url") or not is_youtube_url(publication["url"]):
            g.fail("Stage is published but publication.url is not a YouTube URL.", "Record the real video URL with scripts/set_status.py.")
        published_at = publication.get("published_at")
        if not published_at:
            g.fail("Stage is published but publication.published_at is empty.", "Record the real publish date.")
        elif date.fromisoformat(published_at) > date.today():
            g.fail(f"published_at {published_at} is in the future.", "Use the actual publish date.")
    elif publication.get("url") or publication.get("published_at"):
        g.fail(f"A publish URL/date is recorded but the stage is {stage}.", "Use scripts/set_status.py --stage PUBLISHED --url ... --date ... after the video is live.")
    if not g.problems:
        g.ok("Publishing metadata complete" + (" and publication recorded." if published else "; checklist ticked."))
    return g


def _is_published(ctx: Context, content_id: str) -> bool:
    """A related item counts as published when its workspace or a sheet tracker row says so."""
    from .items import workspace_for, load_item  # local import: avoids a cycle at module load

    workspace = workspace_for(ctx.repo, content_id)
    if workspace is not None and (workspace / "item.yaml").exists():
        return load_item(workspace).stage in ("PUBLISHED", "PERFORMANCE_REVIEW")
    tracker = ctx.repo.normalized("tracker") or {}
    return any(r.get("id") == content_id and r.get("stage_hint") == "PUBLISHED" for r in tracker.get("records", []))


# ---------------------------------------------------------------------------
# Runs and approval
# ---------------------------------------------------------------------------
def run_gates(ctx: Context) -> dict[str, GateResult]:
    errors = schema.validate(ctx.data, ctx.repo.schemas_dir / "content.schema.json")
    results = {"G1": gate_g1(ctx, errors)}
    if errors:
        for gate in GATES[1:]:
            blocked = GateResult(gate, ctx.policy["gates"][gate])
            blocked.block("item.yaml does not match the schema (see G1).", "Fix G1 first.")
            results[gate] = blocked
        return results
    results["G2"] = gate_g2(ctx)
    results["G3"] = gate_g3(ctx)
    results["G4"] = gate_g4(ctx)
    results["G5"] = gate_g5(ctx)
    results["G6"] = gate_g6(ctx)
    results["G7"] = gate_g7(ctx, results["G4"])
    results["G8"] = gate_g8(ctx)
    return results


def overall(results: dict[str, GateResult]) -> str:
    values = {r.result for r in results.values()}
    return FAIL if FAIL in values else BLOCKED if BLOCKED in values else PASS


def approval(ctx: Context, results: dict[str, GateResult]) -> dict[str, Any]:
    policy = ctx.policy["approval"]
    reviews = [r for r in ctx.data.get("reviews") or [] if ctx.is_current(r)]
    requirements: list[dict[str, Any]] = []

    def add(name: str, satisfied: bool, detail: str) -> None:
        requirements.append({"requirement": name, "satisfied": satisfied, "detail": detail})

    failing = [g for g, r in results.items() if r.result != PASS]
    add("Automated gates G1-G8 all PASS on the current content", not failing, "all PASS" if not failing else "not PASS: " + ", ".join(failing))
    if ctx.item.is_test:
        add("Not a test item", False, "Test items (IDs 9001-9999) can never be approved for release.")
    for rule in policy["judgment_reviews"]:
        missing, failed, used = [], [], []
        for gate in rule["gates"]:
            latest = None
            for review in reviews:
                if review["role"] == rule["role"] and review["reviewer_type"] in rule["reviewer_types"] and gate in review.get("gates", {}):
                    latest = review
            if latest is None:
                missing.append(gate)
            elif latest["gates"][gate]["result"] != PASS:
                failed.append(f"{gate}={latest['gates'][gate]['result']} ({latest['id']})")
            elif latest["id"] not in used:
                used.append(latest["id"])
        detail = "; ".join(filter(None, [f"no review for {', '.join(missing)}" if missing else "", ", ".join(failed), f"PASS in {', '.join(used)}" if used and not missing and not failed else ""]))
        add(f"Independent {rule['role']} review ({', '.join(rule['gates'])}) by {' or '.join(rule['reviewer_types'])}", not missing and not failed, detail)
    flags = ctx.data["safety"]["flags"]
    mode = policy.get("human_technical_review", "safety_flagged")
    if mode == "always" or (mode == "safety_flagged" and flags):
        latest = None
        for review in reviews:
            if review["role"] == "technical" and review["reviewer_type"] == "human" and review.get("qualified"):
                latest = review
        ok = bool(latest) and all(latest["gates"].get(g, {}).get("result") == PASS for g in ("G3", "G5"))
        reason = f"safety flags: {', '.join(flags)}" if flags else "policy: always"
        add(f"Qualified human technical review of G3 and G5 ({reason})", ok, latest["id"] if latest else "none on the current content")
    if policy.get("require_human_final_signoff"):
        latest = None
        for review in reviews:
            if review["role"] == "editorial" and review["reviewer_type"] == "human":
                latest = review
        add("Human editorial sign-off", bool(latest) and latest["decision"] == PASS, f"{latest['id']}: {latest['decision']}" if latest else "none on the current content")
    approvable = all(r["satisfied"] for r in requirements)
    return {"status": "APPROVABLE" if approvable else "NOT APPROVABLE", "requirements": requirements, "fingerprint": ctx.fingerprint}


def next_review_id(data: dict[str, Any]) -> str:
    numbers = [int(r["id"][1:]) for r in data.get("reviews") or [] if re.fullmatch(r"R[0-9]+", str(r.get("id", "")))]
    return f"R{(max(numbers) + 1) if numbers else 1:03d}"


def automated_review(ctx: Context, results: dict[str, GateResult]) -> dict[str, Any]:
    return {
        "id": next_review_id(ctx.data),
        "date": today(),
        "reviewer": "scripts/qc_content.py",
        "reviewer_type": "automated",
        "role": "qc",
        "fingerprint": ctx.fingerprint,
        "gates": {
            gate: {"result": result.result, "evidence": "\n".join(result.evidence_lines()), "corrections": result.corrections()}
            for gate, result in results.items()
        },
        "decision": overall(results),
        "notes": "Automated structural checks. Judgment gates also need independent reviews.",
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def render_report(ctx: Context, results: dict[str, GateResult], approval_info: dict[str, Any]) -> str:
    template = (ctx.repo.templates_dir / "qc-report.md").read_text(encoding="utf-8")
    template = re.sub(r"\n<!--.*?-->\n", "\n", template, flags=re.DOTALL)
    gate_rows = ["| Gate | Check | Result | Summary |", "|---|---|---|---|"]
    for gate, result in results.items():
        gate_rows.append(f"| {gate} | {result.name} | **{result.result}** | {_snippet(result.summary(), 140).replace('|', '/')} |")
    details = []
    for gate, result in results.items():
        details.append(f"### {gate} — {result.name}: {result.result}\n")
        details.append("Evidence:\n")
        details.extend(f"- {line}" for line in result.evidence_lines())
        corrections = result.corrections()
        if corrections:
            details.append("\nCorrections:\n")
            details.extend(f"- {c}" for c in corrections)
        details.append("")
    approval_rows = ["| Requirement | Met | Detail |", "|---|---|---|"]
    for req in approval_info["requirements"]:
        approval_rows.append(f"| {req['requirement']} | {'yes' if req['satisfied'] else 'no'} | {req['detail'] or '—'} |")
    history_rows = ["| Review | Date | Reviewer | Type | Role | Decision | On current content |", "|---|---|---|---|---|---|---|"]
    for review in ctx.data.get("reviews") or []:
        current = "yes" if ctx.is_current(review) else "no (content changed since)"
        history_rows.append(f"| {review['id']} | {review['date']} | {review['reviewer']} | {review['reviewer_type']} | {review['role']} | {review['decision']} | {current} |")
    if len(history_rows) == 2:
        history_rows.append("| — | — | — | — | — | — | — |")
    values = {
        "id": ctx.item.id,
        "working_title": ctx.data.get("working_title", ""),
        "test_banner": test_banner(ctx.item.is_test),
        "run_date": today(),
        "stage": ctx.item.stage + (" (on hold)" if (ctx.data.get("status") or {}).get("on_hold") else ""),
        "fingerprint": ctx.fingerprint,
        "overall": overall(results),
        "approval": approval_info["status"],
        "gate_table": "\n".join(gate_rows),
        "gate_details": "\n".join(details).rstrip(),
        "approval_details": "\n".join(approval_rows),
        "review_history": "\n".join(history_rows),
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    return re.sub(r"\n{3,}", "\n\n", template).rstrip() + "\n"


def test_banner(is_test: bool) -> str:
    if not is_test:
        return ""
    return (
        "> **TEST ITEM — NOT FOR PUBLICATION.** This workspace exists to test the workflow. "
        "Its research is not done and nothing in it is verified fact."
    )
