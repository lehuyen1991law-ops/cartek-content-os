"""Visual style layer: config/visual-style.yaml, storyboard Effects / Text style columns, G7 warnings,
the G5 brand-mark exemption and the production package's visual_style section."""

from __future__ import annotations

import re
import unittest

from helpers import REPO_ROOT, Sandbox, run, write_complete_fixture

from ctk import fileio, qc, schema, visual
from ctk.context import build_context
from ctk.items import find_item

LIBRARY = fileio.load_yaml(REPO_ROOT / "config" / "visual-style.yaml")
EFFECT_KEYS = ("id", "kind", "name_vi", "description", "when_to_use", "max_uses_per_video", "never_use")
ROLE_KEYS = ("label_vi", "font", "weight", "size_px_1080p", "colour", "max_lines", "max_chars_per_line", "safe_area")
STORYBOARD_HEAD = "# Storyboard (SYNTHETIC TEST FIXTURE)\n\n## Shot list\n\n| Shot | Segment | Framing | Description | Effects | Text style |\n|---|---|---|---|---|---|\n"


def storyboard(*rows: str) -> str:
    return STORYBOARD_HEAD + "".join(f"{row}\n" for row in rows)


class TestLibrary(unittest.TestCase):
    def test_library_is_declared_as_a_repository_default(self):
        self.assertEqual(LIBRARY["status"], "repository-default")
        self.assertEqual(str(LIBRARY["added"]), "2026-11-06")
        self.assertTrue((REPO_ROOT / LIBRARY["guide"]).exists(), LIBRARY["guide"])

    def test_every_effect_has_required_keys_and_a_unique_id(self):
        ids = [e["id"] for e in LIBRARY["effects"]]
        self.assertEqual(len(ids), len(set(ids)), ids)
        for effect in LIBRARY["effects"]:
            for key in EFFECT_KEYS:
                self.assertIn(key, effect, effect.get("id"))
            self.assertRegex(effect["id"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
            self.assertIn(effect["kind"], ("sfx", "vfx", "transition", "lower-third"))
            self.assertTrue(effect["max_uses_per_video"] is None or isinstance(effect["max_uses_per_video"], int))
        for required in ("hard-cut", "soft-dissolve", "code-popup", "highlight-circle", "zoom-punch", "lower-third", "safety-banner", "freeze-frame-snapshot", "checklist-tick", "sfx-whoosh", "sfx-ui-click", "sfx-low-thud"):
            self.assertIn(required, ids)
        self.assertEqual(visual.SAFETY_EFFECT, "safety-banner")

    def test_roles_fonts_and_colours_are_consistent(self):
        roles = LIBRARY["typography"]["roles"]
        for role in ("caption", "lower_third", "callout", "dtc_code", "live_data_number", "end_screen"):
            self.assertIn(role, roles)
        for name, role in roles.items():
            for key in ROLE_KEYS:
                self.assertIn(key, role, name)
            self.assertIn(role["font"], LIBRARY["fonts"], name)
            self.assertIn(role["colour"], LIBRARY["colours"], name)
        for key, font in LIBRARY["fonts"].items():
            for field in ("name", "licence", "source", "evidence", "vietnamese_coverage", "coverage_note"):
                self.assertIn(field, font, key)
            self.assertIn(font["vietnamese_coverage"], ("confirmed", "unconfirmed"))
        for token in LIBRARY["colours"].values():
            self.assertTrue(token.get("placeholder"), "colour tokens are placeholders until the brand team decides")
        rules = " ".join(LIBRARY["sound_rules"]).lower()
        for word in ("siren", "narration", "ducked"):
            self.assertIn(word, rules)
        self.assertTrue(LIBRARY["captions"]["mandatory"])
        self.assertTrue(any("NFC" in r for r in LIBRARY["text_rules"]))

    def test_split_ids_and_columns_tolerate_old_storyboards(self):
        self.assertEqual(visual.split_ids(" code-popup, SFX-UI-BEEP ;hard-cut "), ["code-popup", "sfx-ui-beep", "hard-cut"])
        self.assertEqual(visual.split_ids("[TODO: chọn hiệu ứng]"), [])
        self.assertEqual(visual.split_ids("none"), [])
        self.assertEqual(visual.shots(""), [])
        old = visual.shots("## Shot list\n\n| Shot | Segment | Framing |\n|---|---|---|\n| 1 | s02 | Wide |\n")
        self.assertEqual((old[0].shot, old[0].segment, old[0].effects, old[0].text_styles), ("1", "S02", [], []))


class VisualQCTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.box = Sandbox()
        self.repo = self.box.repo
        write_complete_fixture(self.repo)

    def tearDown(self) -> None:
        self.box.cleanup()

    def gates(self, content_id: str = "CTK-L-0015"):
        ctx = build_context(self.repo, find_item(self.repo, content_id))
        return ctx, qc.run_gates(ctx)

    def findings(self, results, gate: str, level: str) -> list[str]:
        return [evidence for lvl, evidence, _ in results[gate].findings if lvl == level]

    def write(self, name: str, text: str, content_id: str = "CTK-L-0015") -> None:
        (find_item(self.repo, content_id).path / name).write_text(text, encoding="utf-8")

    def edit(self, name: str, change, content_id: str = "CTK-L-0015") -> None:
        path = find_item(self.repo, content_id).path / name
        path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")


class TestG7VisualWarnings(VisualQCTestCase):
    def test_fixture_without_visual_columns_passes_without_warnings(self):
        _, results = self.gates()
        self.assertEqual(results["G7"].result, qc.PASS, results["G7"].evidence_lines())
        self.assertEqual(self.findings(results, "G7", "WARN"), [])
        self.assertTrue(any("No effects declared" in e for e in self.findings(results, "G7", "INFO")))

    def test_unknown_effect_id_is_a_warning_not_a_failure(self):
        self.write("storyboard.md", storyboard("| 1 | S01 | Wide | Synthetic shot | code-popup, laser-explosion | caption |"))
        _, results = self.gates()
        self.assertEqual(results["G7"].result, qc.PASS, results["G7"].evidence_lines())
        warnings = self.findings(results, "G7", "WARN")
        self.assertTrue(any("laser-explosion" in w and "Effects" in w for w in warnings), warnings)
        self.assertTrue(any("code-popup ×1" in e for e in self.findings(results, "G7", "INFO")))
        self.assertTrue(any("library first" in c for c in results["G7"].corrections()))

    def test_unknown_text_style_is_a_warning(self):
        self.write("storyboard.md", storyboard("| 1 | S01 | Wide | Synthetic shot | hard-cut | comic_sans |"))
        _, results = self.gates()
        self.assertEqual(results["G7"].result, qc.PASS)
        self.assertTrue(any("comic_sans" in w and "Text style" in w for w in self.findings(results, "G7", "WARN")))

    def test_safety_segment_without_safety_banner_is_a_warning(self):
        self.edit("script.md", lambda t: t.replace("- **VISUAL:** Synthetic visual.", "- **VISUAL:** Synthetic visual.\n- **SAFETY:** Synthetic safety note about hot parts.", 1))
        self.write("storyboard.md", storyboard("| 1 | S01 | Wide | Synthetic shot | code-popup | dtc_code |"))
        _, results = self.gates()
        self.assertEqual(results["G7"].result, qc.PASS, results["G7"].evidence_lines())
        self.assertTrue(any("S01" in w and "safety-banner" in w for w in self.findings(results, "G7", "WARN")))
        self.write("storyboard.md", storyboard("| 1 | S01 | Wide | Synthetic shot | code-popup, safety-banner, sfx-low-thud | dtc_code, caption |"))
        _, results = self.gates()
        self.assertFalse(any("safety-banner" in w for w in self.findings(results, "G7", "WARN")), results["G7"].evidence_lines())
        self.assertTrue(any("Typography roles used: caption ×1, dtc_code ×1" in e for e in self.findings(results, "G7", "INFO")))

    def test_safety_segment_with_old_storyboard_layout_is_not_a_warning(self):
        # No Effects column at all (old layout): the safety-banner check does not apply, only the INFO line.
        self.edit("script.md", lambda t: t.replace("- **VISUAL:** Synthetic visual.", "- **VISUAL:** Synthetic visual.\n- **SAFETY:** Synthetic safety note about hot parts.", 1))
        self.write("storyboard.md", "# Storyboard (SYNTHETIC TEST FIXTURE)\n\n## Shot list\n\n| Shot | Segment | Framing | Description |\n|---|---|---|---|\n| 1 | S01 | Wide | Synthetic shot |\n")
        _, results = self.gates()
        self.assertEqual(results["G7"].result, qc.PASS, results["G7"].evidence_lines())
        self.assertEqual(self.findings(results, "G7", "WARN"), [])
        self.assertTrue(any("No effects declared" in e for e in self.findings(results, "G7", "INFO")))

    def test_exceeding_suggested_max_uses_is_a_warning(self):
        rows = [f"| {n} | S0{min(n, 7)} | Wide | Synthetic shot {n} | zoom-punch | |" for n in range(1, 8)]
        self.write("storyboard.md", storyboard(*rows))
        _, results = self.gates()
        self.assertEqual(results["G7"].result, qc.PASS)
        self.assertTrue(any("zoom-punch" in w and "at most 6" in w for w in self.findings(results, "G7", "WARN")))

    def test_old_items_without_the_columns_and_shorts_without_storyboard_do_not_break(self):
        code, out = run("new_content", self.repo.root, "--from-idea", "CTK-S-0010")
        self.assertEqual(code, 0, out)
        (find_item(self.repo, "CTK-S-0010").path / "storyboard.md").unlink()
        _, results = self.gates("CTK-S-0010")
        self.assertFalse(any("could not be built" in e for e in self.findings(results, "G7", qc.FAIL)), results["G7"].evidence_lines())
        self.assertFalse(any("does not validate" in e for e in self.findings(results, "G7", qc.FAIL)), results["G7"].evidence_lines())


class TestG5BrandMarks(VisualQCTestCase):
    def set_cta_visual(self, text: str) -> None:
        # The CTA segment S07 is the last segment; replace its VISUAL only.
        def change(script: str) -> str:
            head, _, tail = script.rpartition("- **VISUAL:** Synthetic visual.")
            return head + f"- **VISUAL:** {text}" + tail
        self.edit("script.md", change)

    def test_logo_and_end_screen_in_cta_visual_do_not_need_a_feature_claim(self):
        self.set_cta_visual("Logo Cartek; màn hình kết thúc Cartek với video liên quan.")
        _, results = self.gates()
        self.assertEqual(results["G5"].result, qc.PASS, results["G5"].evidence_lines())
        self.assertFalse(any("cartek-feature" in e for e in self.findings(results, "G5", qc.FAIL)))

    def test_cartek_2_capability_in_cta_visual_still_fails(self):
        self.set_cta_visual("Màn hình Cartek 2 đọc freeze frame; logo Cartek.")
        _, results = self.gates()
        self.assertTrue(any("S07" in e and "cartek-feature" in e for e in self.findings(results, "G5", qc.FAIL)), results["G5"].evidence_lines())

    def test_logo_cartek_2_is_the_product_not_a_brand_mark(self):
        self.set_cta_visual("Logo Cartek 2 đọc được dữ liệu đóng băng.")
        _, results = self.gates()
        self.assertTrue(any("S07" in e and "cartek-feature" in e for e in self.findings(results, "G5", qc.FAIL)), results["G5"].evidence_lines())

    def test_capability_statement_after_a_brand_mark_still_fails(self):
        # The exemption strips only a mark whose clause ends after it (or goes on with a placement
        # word); a capability statement that follows the mark keeps the segment subject to the rule.
        for visual in (
            "Thương hiệu Cartek chẩn đoán được mọi xe.",
            "Logo Cartek: đọc freeze frame mọi xe.",
            "Dòng chữ Cartek đọc được dữ liệu đóng băng của mọi xe.",
        ):
            with self.subTest(visual=visual):
                self.set_cta_visual(visual)
                _, results = self.gates()
                self.assertTrue(any("S07" in e and "cartek-feature" in e for e in self.findings(results, "G5", qc.FAIL)), results["G5"].evidence_lines())
                self.tearDown()
                self.setUp()

    def test_brand_mark_with_a_placement_word_is_still_exempt(self):
        self.set_cta_visual("Logo Cartek ở góc trên phải, màn hình kết thúc Cartek với video liên quan.")
        _, results = self.gates()
        self.assertFalse(any("cartek-feature" in e for e in self.findings(results, "G5", qc.FAIL)), results["G5"].evidence_lines())

    def test_cartek_2_claim_in_narration_still_fails(self):
        self.edit("script.md", lambda t: t.replace("Mã P0300 xuất hiện trong ví dụ này.", "Mã P0300 xuất hiện. Cartek 2 đọc được dữ liệu đóng băng của mọi xe.", 1))
        _, results = self.gates()
        self.assertTrue(any("S01" in e and "cartek-feature" in e for e in self.findings(results, "G5", qc.FAIL)))


class TestExportVisualStyle(VisualQCTestCase):
    SCHEMA = REPO_ROOT / "schemas" / "production-package.schema.json"

    def test_visual_style_is_resolved_from_the_storyboard(self):
        self.write("storyboard.md", storyboard(
            "| 1 | S01 | Wide | Synthetic shot | code-popup, sfx-ui-beep | dtc_code, caption |",
            "| 2 | S02 | Close | Synthetic shot two | code-popup, mystery-fx | caption |",
        ))
        code, out = run("export_package", self.repo.root, "CTK-L-0015", "--stdout", "--draft")
        self.assertEqual(code, 0, out)
        package = fileio.loads_yaml(out)
        self.assertEqual(schema.validate(package, self.SCHEMA), [])
        vs = package["visual_style"]
        self.assertEqual(vs["source"], "config/visual-style.yaml")
        self.assertEqual(vs["status"], "repository-default")
        self.assertEqual([e["id"] for e in vs["effects_used"]], ["code-popup", "sfx-ui-beep"])
        popup = vs["effects_used"][0]
        self.assertEqual(popup["shots"], ["1", "2"])
        self.assertEqual(popup["kind"], "vfx")
        self.assertTrue(popup["description"])
        self.assertEqual(vs["unknown_effects"], ["mystery-fx"])
        self.assertEqual([r["id"] for r in vs["typography_roles_used"]], ["caption", "dtc_code"])
        fonts = {f["id"]: f for f in vs["fonts"]}
        self.assertEqual(fonts["be-vietnam-pro"]["name"], "Be Vietnam Pro")
        self.assertIn("Open Font License", fonts["jetbrains-mono"]["licence"])
        self.assertTrue(fonts["be-vietnam-pro"]["used_by_storyboard"])
        self.assertTrue(fonts["jetbrains-mono"]["used_by_storyboard"])
        self.assertFalse(fonts["roboto-mono"]["used_by_storyboard"])
        self.assertTrue(vs["caption_rules"]["mandatory"])
        self.assertTrue(vs["sound_rules"])
        # Deterministic: a second build is identical apart from the date.
        code, again = run("export_package", self.repo.root, "CTK-L-0015", "--stdout", "--draft")
        second = fileio.loads_yaml(again)
        for pkg in (package, second):
            pkg["generated"].pop("date")
        self.assertEqual(package, second)

    def test_fresh_long_form_and_short_scaffolds_still_validate(self):
        for idea in ("CTK-L-0002", "CTK-S-0010"):
            code, out = run("new_content", self.repo.root, "--from-idea", idea)
            self.assertEqual(code, 0, out)
            code, out = run("export_package", self.repo.root, idea, "--stdout", "--draft")
            self.assertEqual(code, 0, out)
            package = fileio.loads_yaml(out)
            self.assertEqual(schema.validate(package, self.SCHEMA), [], idea)
            self.assertEqual(package["visual_style"]["unknown_effects"], [], idea)
        text = (find_item(self.repo, "CTK-L-0002").path / "storyboard.md").read_text(encoding="utf-8")
        self.assertNotIn("{{", text)
        self.assertIn("| Effects | Text style |", text)
        for heading in ("## Shot list", "## Sound and effects (Âm thanh và hiệu ứng)", "## Typography (Chữ trên hình)"):
            self.assertIn(heading, text)
        self.assertEqual(len(visual.shots(text)), 1)
        self.assertEqual(visual.shots(text)[0].effects, ["hard-cut"])

    def test_approved_release_package_carries_visual_style_and_validates_repo(self):
        from helpers import record_passing_reviews

        record_passing_reviews(self.repo, "CTK-L-0015", self.box.root)
        code, out = run("qc_content", self.repo.root, "approve", "CTK-L-0015", "--by", "Biên tập viên B")
        self.assertEqual(code, 0, out)
        package = fileio.load_json(find_item(self.repo, "CTK-L-0015").path / "exports" / "production-package.json")
        self.assertIn("visual_style", package)
        self.assertEqual(run("validate_content", self.repo.root)[0], 0)


class TestVisualIdentityDoc(unittest.TestCase):
    def test_guide_lists_every_effect_and_role_id(self):
        guide = (REPO_ROOT / "strategy" / "visual-identity.md").read_text(encoding="utf-8")
        for effect in LIBRARY["effects"]:
            self.assertIn(f"`{effect['id']}`", guide)
        for role in LIBRARY["typography"]["roles"]:
            self.assertIn(f"`{role}`", guide)
        self.assertRegex(guide, re.compile(r"added 2026-11-06", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
