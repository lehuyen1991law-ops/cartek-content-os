"""Integrity of the committed repository itself (not a sandbox copy)."""

from __future__ import annotations

import re
import subprocess
import unittest

from helpers import REPO_ROOT, Sandbox, run

from ctk import fileio, importer
from ctk.repo import Repo
from ctk.validate import validate_repo

SKILLS = (
    "cartek-content-strategist",
    "automotive-researcher",
    "youtube-scriptwriter",
    "technical-fact-checker",
    "youtube-seo-specialist",
    "shorts-content-specialist",
    "content-qc-inspector",
)
WORKFLOWS = ("idea-to-publish", "research", "script-production", "technical-review", "seo-optimization", "publishing", "post-publish-analysis", "sheet-import")
STRATEGY = ("channel-positioning", "content-pillars", "audience-personas", "competitor-analysis", "editorial-guidelines", "brand-voice", "visual-identity", "product-facts")
SECRET_PATTERNS = (
    r"ghp_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}",
    r"AIza[0-9A-Za-z_\-]{30,}",
    r"ya29\.[0-9A-Za-z_\-]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\"type\":\s*\"service_account\"",
)


class TestRepository(unittest.TestCase):
    repo = Repo(REPO_ROOT)

    def test_validate_has_no_errors(self):
        errors = [f"{f.where}: {f.message}" for f in validate_repo(self.repo) if f.level == "error"]
        self.assertEqual(errors, [])

    def test_import_outputs_are_current(self):
        self.assertEqual(importer.check(self.repo, importer.build(self.repo)), [])

    def test_no_broken_relative_links(self):
        code, out = run("check_links", REPO_ROOT)
        self.assertEqual(code, 0, out)

    def test_content_board_is_current(self):
        code, out = run("generate_board", REPO_ROOT, "--check")
        self.assertEqual(code, 0, out)

    def test_operating_docs_exist(self):
        for name in ("README.md", "CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md", ".env.example", ".gitignore", "requirements.txt"):
            self.assertTrue((REPO_ROOT / name).exists(), name)
        for name in WORKFLOWS:
            self.assertTrue((REPO_ROOT / "workflows" / f"{name}.md").exists(), name)
        for name in STRATEGY:
            self.assertTrue((REPO_ROOT / "strategy" / f"{name}.md").exists(), name)

    def test_every_skill_is_present_linked_and_referenced(self):
        claude = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for name in SKILLS:
            self.assertTrue((REPO_ROOT / "skills" / name / "SKILL.md").exists(), name)
            self.assertTrue((REPO_ROOT / ".claude" / "skills" / name / "SKILL.md").exists(), f".claude/skills/{name}")
            self.assertIn(name, claude)
        self.assertEqual(sorted(p.name for p in (REPO_ROOT / "skills").iterdir() if p.is_dir()), sorted(SKILLS))

    def test_workflow_stages_match_schema(self):
        stages = [s["id"] for s in self.repo.config["workflow"]["stages"]]
        schema = fileio.load_json(REPO_ROOT / "schemas" / "content.schema.json")
        self.assertEqual(stages, schema["$defs"]["stage"]["enum"])

    def test_gitignore_protects_secrets_and_drafts(self):
        ignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in (".env", "*service-account*.json", "content/**/exports/*.draft.json", "*.mp4"):
            self.assertIn(pattern, ignore)

    def test_no_secrets_in_tracked_files(self):
        files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout.split()
        hits = []
        for name in files:
            path = REPO_ROOT / name
            if not path.is_file() or path.suffix in (".png", ".jpg"):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, text):
                    hits.append(f"{name}: {pattern}")
        self.assertEqual(hits, [])

    def test_ci_runs_the_same_checks_as_make(self):
        ci = (REPO_ROOT / ".github" / "workflows" / "content-qc.yml").read_text(encoding="utf-8")
        for command in ("unittest discover", "import_sheet.py --check", "validate_content.py", "check_links.py", "generate_board.py --check"):
            self.assertIn(command, ci)
        self.assertNotIn("secrets.", ci, "CI must not need private credentials")

    def test_feature_register_is_empty_until_verified(self):
        register = fileio.load_yaml(REPO_ROOT / "data" / "reference" / "cartek-2-feature-register.yaml")
        for feature in register["features"]:
            self.assertIn(feature.get("status"), ("verified", "unverified", "unsupported"))
            if feature.get("status") == "verified":
                self.assertTrue((feature.get("evidence") or {}).get("reference"), feature)


class TestScaffoldRendering(unittest.TestCase):
    def test_no_unrendered_placeholders(self):
        box = Sandbox()
        try:
            for idea in ("CTK-L-0001", "CTK-S-0001"):
                code, out = run("new_content", box.root, "--from-idea", idea)
                self.assertEqual(code, 0, out)
            for path in box.root.joinpath("content").rglob("*.md"):
                self.assertNotIn("{{", path.read_text(encoding="utf-8"), str(path))
        finally:
            box.cleanup()


if __name__ == "__main__":
    unittest.main()
