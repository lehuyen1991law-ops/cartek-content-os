"""Content workspaces: scaffolding, IDs, status changes, validation, export, parsing."""

from __future__ import annotations

import unittest

from helpers import REPO_ROOT, Sandbox, created_id, run, write_complete_fixture

from ctk import fileio, mdparse, schema
from ctk import textutil as tu
from ctk.items import find_item


class ContentTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.box = Sandbox()
        self.repo = self.box.repo

    def tearDown(self) -> None:
        self.box.cleanup()


class TestNewContent(ContentTestCase):
    def test_scaffold_from_idea(self):
        code, out = run("new_content", self.repo.root, "--from-idea", "CTK-S-0010")
        self.assertEqual(code, 0, out)
        item = find_item(self.repo, "CTK-S-0010")
        self.assertEqual(item.path.parent.name, "shorts")
        for name in ("item.yaml", "brief.md", "research.md", "script.md", "seo.md", "storyboard.md"):
            self.assertTrue((item.path / name).exists(), name)
        self.assertEqual(schema.validate(item.data, self.repo.schemas_dir / "content.schema.json"), [])
        self.assertEqual(item.data["provenance"]["source_ref"], "'Short'!D11")
        self.assertEqual(item.data["history"][0]["stage"], "IDEA")
        script = (item.path / "script.md").read_text(encoding="utf-8")
        self.assertIn("Cartek - Check your car", script)

    def test_never_overwrites_existing_workspace(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0001")
        item = find_item(self.repo, "CTK-L-0001")
        (item.path / "brief.md").write_text("edited", encoding="utf-8")
        code, out = run("new_content", self.repo.root, "--from-idea", "CTK-L-0001")
        self.assertEqual(code, 1)
        self.assertEqual((item.path / "brief.md").read_text(encoding="utf-8"), "edited")

    def test_test_and_manual_ids(self):
        before = fileio.load_json(self.repo.registry_path)["entries"]
        numbers = [int(cid[-4:]) for cid in before if cid.startswith("CTK-L-")]
        code, out = run("new_content", self.repo.root, "--from-idea", "CTK-L-0015", "--test")
        self.assertEqual(code, 0, out)
        first = created_id(out)
        code, out = run("new_content", self.repo.root, "--from-idea", "CTK-L-0015", "--test")
        second = created_id(out)
        code, out = run("new_content", self.repo.root, "--format", "long-form", "--title", "Chủ đề mới ngoài sheet", "--pillar", "P2")
        self.assertEqual(code, 0, out)
        manual = created_id(out)
        self.assertEqual(int(first[-4:]), max([n for n in numbers if n > 9000], default=9000) + 1)
        self.assertEqual(int(second[-4:]), int(first[-4:]) + 1)
        self.assertEqual(int(manual[-4:]), max(n for n in numbers if n < 9000) + 1)
        registry = fileio.load_json(self.repo.registry_path)["entries"]
        self.assertEqual(registry[first]["origin"], "test")
        self.assertEqual(registry[manual]["origin"], "manual")
        self.assertTrue(find_item(self.repo, second).is_test)
        self.assertFalse(find_item(self.repo, manual).is_test)

    def test_rejects_wrong_pillar_for_format(self):
        code, _ = run("new_content", self.repo.root, "--format", "short", "--title", "Sai nhóm", "--pillar", "P1")
        self.assertNotEqual(code, 0)


class TestConcurrentEdits(ContentTestCase):
    def test_save_refuses_when_item_changed_on_disk(self):
        from ctk.items import ConcurrentEditError

        run("new_content", self.repo.root, "--from-idea", "CTK-L-0002")
        first = find_item(self.repo, "CTK-L-0002")
        second = find_item(self.repo, "CTK-L-0002")
        second.data["owner"] = "Session two"
        second.save()
        first.data["owner"] = "Session one"
        with self.assertRaises(ConcurrentEditError):
            first.save()
        self.assertEqual(find_item(self.repo, "CTK-L-0002").data["owner"], "Session two")
        self.assertEqual([p.name for p in first.path.iterdir() if p.name.endswith(".tmp")], [])

    def test_crlf_file_is_not_a_false_conflict(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0002")
        path = find_item(self.repo, "CTK-L-0002").path / "item.yaml"
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        item = find_item(self.repo, "CTK-L-0002")
        item.data["owner"] = "An"
        item.save()
        self.assertEqual(find_item(self.repo, "CTK-L-0002").data["owner"], "An")


class TestStatus(ContentTestCase):
    def setUp(self) -> None:
        super().setUp()
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0009")

    def test_stage_change_and_hold_are_recorded(self):
        self.assertEqual(run("set_status", self.repo.root, "CTK-L-0009", "--stage", "RESEARCH", "--by", "An")[0], 0)
        self.assertEqual(run("set_status", self.repo.root, "CTK-L-0009", "--hold", "Chờ xe thử")[0], 0)
        item = find_item(self.repo, "CTK-L-0009")
        self.assertTrue(item.data["status"]["on_hold"])
        self.assertEqual([h["stage"] for h in item.data["history"]], ["IDEA", "RESEARCH", "RESEARCH"])
        self.assertEqual(run("set_status", self.repo.root, "CTK-L-0009", "--resume")[0], 0)
        self.assertFalse(find_item(self.repo, "CTK-L-0009").data["status"]["on_hold"])

    def test_guarded_stages(self):
        code, out = run("set_status", self.repo.root, "CTK-L-0009", "--stage", "APPROVED")
        self.assertEqual(code, 1)
        self.assertIn("qc_content.py approve", out)
        code, _ = run("set_status", self.repo.root, "CTK-L-0009", "--stage", "PUBLISHED", "--url", "https://youtu.be/x", "--date", "2026-11-01")
        self.assertEqual(code, 1)


class TestValidation(ContentTestCase):
    def test_fresh_workspace_is_valid(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0002")
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 0, out)

    def test_manual_stage_edit_to_approved_is_an_error(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0002")
        item = find_item(self.repo, "CTK-L-0002")
        item.data["status"]["stage"] = "APPROVED"
        item.save()
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 1)
        self.assertIn("without a valid approval", out)

    def test_published_without_url_is_an_error(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0002")
        item = find_item(self.repo, "CTK-L-0002")
        item.data["status"]["stage"] = "PUBLISHED"
        item.save()
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 1)
        self.assertIn("without a YouTube URL", out)

    def test_unregistered_id_and_bad_vocabulary(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0002")
        item = find_item(self.repo, "CTK-L-0002")
        item.data["audience"]["primary"] = "everyone"
        item.save()
        target = item.path.parent / "CTK-L-0999-copy"
        item.path.rename(target)
        data = fileio.load_yaml(target / "item.yaml")
        data["id"] = "CTK-L-0999"
        fileio.write_text(target / "item.yaml", fileio.dumps_yaml(data))
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 1)
        self.assertIn("not registered", out)
        self.assertIn("'everyone'", out)

    def test_checklist_drift_is_a_warning(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0002")
        seo = find_item(self.repo, "CTK-L-0002").path / "seo.md"
        seo.write_text(seo.read_text(encoding="utf-8") + "- [ ] Vietnamese captions checked against the final voice-over\n", encoding="utf-8")
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 0, out)
        self.assertIn("Publishing checklist differs", out)

    def test_hand_edited_normalized_data_is_an_error(self):
        path = self.repo.normalized_dir / "personas.json"
        path.write_text(path.read_text(encoding="utf-8").replace("Chủ Garage ô tô", "Garage"), encoding="utf-8")
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 1)
        self.assertIn("edited by hand", out)


class TestExport(ContentTestCase):
    def test_draft_package_validates_and_lists_blockers(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0015")
        code, out = run("export_package", self.repo.root, "CTK-L-0015", "--draft")
        self.assertEqual(code, 0, out)
        package = fileio.load_json(find_item(self.repo, "CTK-L-0015").path / "exports" / "production-package.draft.json")
        self.assertEqual(package["package_status"], "DRAFT_NOT_APPROVED")
        self.assertTrue(package["blocking_issues"])
        self.assertEqual(schema.validate(package, REPO_ROOT / "schemas" / "production-package.schema.json"), [])

    def test_release_refused_until_approved(self):
        write_complete_fixture(self.repo)
        code, out = run("export_package", self.repo.root, "CTK-L-0015")
        self.assertEqual(code, 1)
        self.assertIn("approve first", out)

    def test_package_contract_rejects_approved_test_items(self):
        package = {"package_status": "APPROVED", "test_item": True}
        errors = schema.validate(package, REPO_ROOT / "schemas" / "production-package.schema.json")
        self.assertTrue(any("test_item" in e or "False was expected" in e for e in errors))

    def test_package_has_handoff_sections(self):
        write_complete_fixture(self.repo)
        code, out = run("export_package", self.repo.root, "CTK-L-0015", "--stdout", "--draft")
        self.assertEqual(code, 0)
        package = fileio.loads_yaml(out)
        for key in ("script", "voiceover", "shot_list", "storyboard_shots", "visual_style", "on_screen_text", "broll_and_animation", "timing", "seo", "technical_claims", "sources", "assets"):
            self.assertIn(key, package)
        self.assertEqual(len(package["script"]["segments"]), 7)
        self.assertGreater(package["timing"]["estimated_total_seconds"], 300)


class TestLinkChecker(unittest.TestCase):
    def test_links_to_missing_files_and_empty_folders_are_broken(self):
        import tempfile
        from pathlib import Path

        from helpers import load_script

        checker = load_script("check_links")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "empty").mkdir()
            (root / "full").mkdir()
            (root / "full" / "a.md").write_text("x", encoding="utf-8")
            (root / "doc.md").write_text("[a](full/) [b](empty/) [c](missing.md) [d](https://example.com) `[e](code.md)`", encoding="utf-8")
            problems = checker.broken_links(root)
        self.assertEqual(len(problems), 2, problems)
        self.assertTrue(any("empty folder" in p for p in problems))


class TestMarkdownConventions(unittest.TestCase):
    def test_templates_parse(self):
        for name in ("long-form-script.md", "short-script.md"):
            doc = mdparse.parse_script((REPO_ROOT / "templates" / name).read_text(encoding="utf-8"))
            self.assertEqual(doc.missing_sections, [], name)
            self.assertEqual(doc.problems, [], name)
            self.assertEqual(doc.segments[0].type, "hook")
            self.assertEqual(doc.segments[-1].type, "cta")
            self.assertGreater(doc.todo_count, 0)

    def test_fields_and_continuation_lines(self):
        text = "## Script\n\n### S01 — Hook\n\n- **TYPE:** hook\n- **VO:** Dòng một.\n  Dòng hai.\n- **CLAIMS:** C01, C02\n- **DEMO-SECONDS:** 12\n"
        segment = mdparse.parse_script(text).segments[0]
        self.assertEqual(segment.get("VO"), "Dòng một.\nDòng hai.")
        self.assertEqual(segment.claims, ["C01", "C02"])
        self.assertEqual(segment.demo_seconds, 12.0)

    def test_comments_and_todo_prompts_are_not_content(self):
        text = "<!-- [TODO hidden] -->\nText [TODO: phanh] more"
        self.assertEqual(mdparse.todo_count(text), 1)
        self.assertNotIn("phanh", mdparse.without_todos(text))

    def test_syllable_count(self):
        self.assertEqual(tu.count_syllables("Lỗi P0300 trên xe"), 3 + 5)
        self.assertEqual(tu.count_syllables("Cổng OBD2 và ECU"), 1 + 4 + 1 + 3)

    def test_timestamps(self):
        self.assertEqual(mdparse.parse_timestamp("01:05"), 65)
        self.assertEqual(mdparse.parse_timestamp("1:02:03"), 3723)
        self.assertIsNone(mdparse.parse_timestamp("1:75"))
        self.assertEqual(mdparse.format_timestamp(65), "01:05")

    def test_slug_and_keys(self):
        self.assertEqual(tu.slugify("Lỗi P0300 - Ác Mộng của Mọi Động Cơ?"), "loi-p0300-ac-mong-cua-moi-dong-co")
        self.assertEqual(tu.loose_key("Giới thiệu sản phẩm/ thiết bị"), tu.loose_key("Giới thiệu sản phẩm/thiết bị"))


if __name__ == "__main__":
    unittest.main()
