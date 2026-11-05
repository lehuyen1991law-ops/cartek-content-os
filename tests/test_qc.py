"""QC gates G1-G8, independent approval, and the protections around them."""

from __future__ import annotations

import unittest

from helpers import Sandbox, created_id, record_passing_reviews, review_file, run, write_complete_fixture

from ctk import fileio, qc
from ctk.context import build_context
from ctk.items import find_item


class QCTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.box = Sandbox()
        self.repo = self.box.repo

    def tearDown(self) -> None:
        self.box.cleanup()

    def gates(self, content_id: str = "CTK-L-0015"):
        ctx = build_context(self.repo, find_item(self.repo, content_id))
        results = qc.run_gates(ctx)
        return ctx, results

    def findings(self, results, gate: str, level: str) -> list[str]:
        return [evidence for lvl, evidence, _ in results[gate].findings if lvl == level]

    def edit_item(self, content_id: str, change) -> None:
        item = find_item(self.repo, content_id)
        change(item.data)
        item.save()

    def edit_file(self, content_id: str, name: str, change) -> None:
        path = find_item(self.repo, content_id).path / name
        path.write_text(change(path.read_text(encoding="utf-8")), encoding="utf-8")


class TestFreshScaffold(QCTestCase):
    def test_new_item_is_blocked_not_passed(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0015")
        _, results = self.gates()
        for gate in ("G2", "G3", "G4", "G5"):
            self.assertEqual(results[gate].result, qc.BLOCKED, gate)
        self.assertNotEqual(qc.overall(results), qc.PASS)

    def test_writer_stage_is_not_evidence(self):
        run("new_content", self.repo.root, "--from-idea", "CTK-L-0015")
        self.edit_item("CTK-L-0015", lambda d: d["status"].update(stage="QC"))
        ctx, results = self.gates()
        self.assertNotEqual(qc.overall(results), qc.PASS)
        self.assertEqual(qc.approval(ctx, results)["status"], "NOT APPROVABLE")


class TestCompleteFixture(QCTestCase):
    def setUp(self) -> None:
        super().setUp()
        write_complete_fixture(self.repo)

    def test_all_automated_gates_pass(self):
        _, results = self.gates()
        failing = {g: r.summary() for g, r in results.items() if r.result != qc.PASS}
        self.assertEqual(failing, {})

    def test_automated_pass_alone_is_not_approval(self):
        ctx, results = self.gates()
        info = qc.approval(ctx, results)
        self.assertEqual(info["status"], "NOT APPROVABLE")
        unmet = [r["requirement"] for r in info["requirements"] if not r["satisfied"]]
        self.assertEqual(len(unmet), 3, unmet)

    def test_independent_reviews_then_approve_then_stale(self):
        record_passing_reviews(self.repo, "CTK-L-0015", self.box.root)
        ctx, results = self.gates()
        self.assertEqual(qc.approval(ctx, results)["status"], "APPROVABLE")
        code, out = run("qc_content", self.repo.root, "approve", "CTK-L-0015", "--by", "Biên tập viên B")
        self.assertEqual(code, 0, out)
        item = find_item(self.repo, "CTK-L-0015")
        self.assertEqual(item.stage, "APPROVED")
        package = fileio.load_json(item.path / "exports" / "production-package.json")
        self.assertEqual(package["package_status"], "APPROVED")
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 0, out)
        # Any content change after approval invalidates it.
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Synthetic visual.", "Changed visual.", 1))
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 1)
        self.assertIn("without a valid approval", out)
        self.assertIn("Release package is stale", out)
        code, out = run("export_package", self.repo.root, "CTK-L-0015")
        self.assertEqual(code, 1, out)
        code, out = run("set_status", self.repo.root, "CTK-L-0015", "--stage", "PUBLISHED", "--url", "https://youtu.be/abc", "--date", "2026-11-01")
        self.assertEqual(code, 1, out)

    def test_review_on_old_content_does_not_count(self):
        record_passing_reviews(self.repo, "CTK-L-0015", self.box.root)
        self.edit_item("CTK-L-0015", lambda d: d.update(takeaway="A different takeaway."))
        ctx, results = self.gates()
        self.assertEqual(qc.approval(ctx, results)["status"], "NOT APPROVABLE")

    def test_editorial_signoff_must_be_human(self):
        path = review_file(self.box.root, "bad.yaml", reviewer="bot", reviewer_type="agent", role="editorial", gates={}, decision="PASS")
        code, out = run("qc_content", self.repo.root, "review", "CTK-L-0015", "--file", str(path))
        self.assertEqual(code, 1)
        self.assertIn("must be a human", out)

    def test_review_needs_evidence_and_corrections(self):
        path = review_file(self.box.root, "thin.yaml", reviewer="x agent", reviewer_type="agent", role="qc", gates={"G4": {"result": "FAIL", "evidence": "bad"}}, decision="FAIL")
        code, out = run("qc_content", self.repo.root, "review", "CTK-L-0015", "--file", str(path))
        self.assertEqual(code, 1)
        self.assertIn("evidence", out)
        self.assertIn("correction", out)

    def test_safety_flag_requires_qualified_human_technical_review(self):
        self.edit_item("CTK-L-0015", lambda d: d["safety"].update(flags=["brakes"]))
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("- **VISUAL:** Synthetic visual.", "- **VISUAL:** Synthetic visual.\n- **SAFETY:** Synthetic safety note.", 1))
        record_passing_reviews(self.repo, "CTK-L-0015", self.box.root, human_technical=False)
        ctx, results = self.gates()
        info = qc.approval(ctx, results)
        self.assertEqual(info["status"], "NOT APPROVABLE")
        self.assertTrue(any("Qualified human technical review" in r["requirement"] and not r["satisfied"] for r in info["requirements"]))
        record_passing_reviews(self.repo, "CTK-L-0015", self.box.root, human_technical=True)
        ctx, results = self.gates()
        self.assertEqual(qc.approval(ctx, results)["status"], "APPROVABLE")

    def test_unverified_claim_blocks_g3(self):
        self.edit_item("CTK-L-0015", lambda d: d["claims"][0].update(status="unverified"))
        _, results = self.gates()
        self.assertEqual(results["G3"].result, qc.BLOCKED)

    def test_verified_claim_needs_accepted_source_type(self):
        self.edit_item("CTK-L-0015", lambda d: d["sources"][0].update(type="other"))
        _, results = self.gates()
        self.assertEqual(results["G3"].result, qc.FAIL)

    def test_cartek_feature_claim_needs_register_entry(self):
        def add_feature_claim(data):
            data["sources"].append({"id": "SRC02", "title": "Synthetic hands-on log", "type": "hands-on-test", "citation": "SYNTHETIC"})
            data["claims"].append({"id": "C02", "text": "Cartek 2 reads freeze frame data (synthetic).", "category": "cartek-feature", "sources": ["SRC02"], "status": "verified", "feature_id": "F001", "verified_by": "unit-test", "verified_on": "2026-11-05"})

        self.edit_item("CTK-L-0015", add_feature_claim)
        _, results = self.gates()
        self.assertEqual(results["G3"].result, qc.BLOCKED)
        self.assertTrue(any("not in the feature register" in e for e in self.findings(results, "G3", qc.BLOCKED)))

    def test_clearing_codes_as_a_fix_fails(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Mã P0300 xuất hiện trong ví dụ này.", "Xóa lỗi là xong, xe chạy bình thường.", 1))
        _, results = self.gates()
        self.assertEqual(results["G5"].result, qc.FAIL)

    def test_myth_debunking_is_flagged_for_review_not_failed(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Mã P0300 xuất hiện trong ví dụ này.", "Mã P0300 xuất hiện. Nhiều người lầm tưởng xóa lỗi là xong nhưng lỗi sẽ sáng lại.", 1))
        _, results = self.gates()
        self.assertEqual(results["G5"].result, qc.PASS, results["G5"].evidence_lines())
        self.assertTrue(self.findings(results, "G5", "WARN"))

    def test_common_negation_does_not_hide_banned_wording(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Mã P0300 xuất hiện trong ví dụ này.", "Mã P0300 xuất hiện. Xóa lỗi là xong, không cần ra garage.", 1))
        _, results = self.gates()
        self.assertEqual(results["G5"].result, qc.FAIL)

    def test_mentioning_code_clearing_needs_caveat(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Mã P0300 xuất hiện trong ví dụ này.", "Mã P0300 xuất hiện. Bạn có thể xóa mã lỗi bằng máy.", 1))
        _, results = self.gates()
        self.assertEqual(results["G5"].result, qc.FAIL)

    def test_dtc_without_claim_fails(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Mã P0300 xuất hiện", "Mã P0301 xuất hiện", 1))
        _, results = self.gates()
        self.assertTrue(any("P0301" in e for e in self.findings(results, "G5", qc.FAIL)))

    def test_manufacturer_code_needs_specific_vehicle(self):
        def change(data):
            data["claims"][0]["text"] = "SYNTHETIC fixture claim mentioning P1345 for unit tests."
        self.edit_item("CTK-L-0015", change)
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Mã P0300 xuất hiện", "Mã P1345 xuất hiện", 1))
        _, results = self.gates()
        self.assertTrue(any("manufacturer-controlled" in e for e in self.findings(results, "G5", qc.FAIL)))

    def test_unflagged_safety_topic_fails(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Synthetic visual.", "Kiểm tra má phanh trên cầu nâng.", 1))
        _, results = self.gates()
        failures = self.findings(results, "G5", qc.FAIL)
        self.assertTrue(any("'brakes'" in e for e in failures))
        self.assertTrue(any("'lifting'" in e for e in failures))
        self.edit_item("CTK-L-0015", lambda d: d["safety"].update(dismissed=[
            {"flag": "brakes", "rationale": "Synthetic: brakes mentioned only as an example, no procedure."},
            {"flag": "lifting", "rationale": "Synthetic: lift visible in background, nobody works under it."},
        ]))
        _, results = self.gates()
        self.assertEqual(results["G5"].result, qc.PASS, results["G5"].evidence_lines())

    def test_runtime_outside_target_fails_unless_exception(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Đây là lời thoại mẫu", "Câu", 200))
        _, results = self.gates()
        self.assertEqual(results["G4"].result, qc.FAIL)
        self.edit_item("CTK-L-0015", lambda d: d["production"].update(runtime_exception={"min_seconds": 30, "max_seconds": 600, "rationale": "Synthetic exception rationale for the unit test."}))
        _, results = self.gates()
        self.assertEqual(results["G4"].result, qc.PASS, results["G4"].evidence_lines())

    def test_cta_needs_brand_line(self):
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace(" Cartek - Check your car", ""))
        _, results = self.gates()
        self.assertTrue(any("brand line" in e for e in self.findings(results, "G4", qc.FAIL)))

    def test_seo_limits(self):
        def change(data):
            data["seo"]["recommended_title"] = "x" * 101
            data["seo"]["tags"] = ["tag with spaces number %d" % i for i in range(30)]
            data["seo"]["chapters"] = [{"time": "00:05", "title": "A"}, {"time": "00:10", "title": "B"}]
            data["seo"]["description"] = "Video này chắc chắn lên top và đạt CTR 15%."
        self.edit_item("CTK-L-0015", change)
        _, results = self.gates()
        failures = " ".join(self.findings(results, "G6", qc.FAIL))
        for expected in ("YouTube allows 100", "limit 500", "at least 3", "00:00", "performance claim"):
            self.assertIn(expected, failures)

    def test_unchecked_publishing_checklist_blocks_g8(self):
        self.edit_file("CTK-L-0015", "seo.md", lambda t: t.replace("- [x] Synthetic item two", "- [ ] Synthetic item two"))
        _, results = self.gates()
        self.assertEqual(results["G8"].result, qc.BLOCKED)

    def test_pending_assets_block_g7(self):
        self.edit_item("CTK-L-0015", lambda d: d["production"]["assets_required"][0].update(status="needed"))
        _, results = self.gates()
        self.assertEqual(results["G7"].result, qc.BLOCKED)

    def test_schema_errors_stop_other_gates(self):
        self.edit_item("CTK-L-0015", lambda d: d.update(unexpected_field=True))
        _, results = self.gates()
        self.assertEqual(results["G1"].result, qc.FAIL)
        self.assertTrue(all(results[g].result == qc.BLOCKED for g in qc.GATES[1:]))

    def test_record_flag_appends_review_history(self):
        code, out = run("qc_content", self.repo.root, "run", "CTK-L-0015", "--record")
        self.assertEqual(code, 0, out)
        reviews = find_item(self.repo, "CTK-L-0015").data["reviews"]
        self.assertEqual(reviews[-1]["reviewer_type"], "automated")
        self.assertEqual(set(reviews[-1]["gates"]), set(qc.GATES))
        report = (find_item(self.repo, "CTK-L-0015").path / "qc-report.md").read_text(encoding="utf-8")
        self.assertIn("Gate summary", report)


class TestLifecycle(QCTestCase):
    def setUp(self) -> None:
        super().setUp()
        write_complete_fixture(self.repo)

    def approve(self) -> None:
        record_passing_reviews(self.repo, "CTK-L-0015", self.box.root)
        code, out = run("qc_content", self.repo.root, "approve", "CTK-L-0015", "--by", "Biên tập viên B")
        self.assertEqual(code, 0, out)

    def test_full_lifecycle_to_performance_review(self):
        self.approve()
        code, out = run("set_status", self.repo.root, "CTK-L-0015", "--stage", "PUBLISHED", "--url", "https://youtu.be/abc123", "--date", "2026-11-01")
        self.assertEqual(code, 1, "the upload checklist is not done yet")
        self.assertIn("upload_checklist", out)
        self.edit_item("CTK-L-0015", lambda d: [entry.update(done=True) for entry in d["publication"]["upload_checklist"]])
        code, out = run("set_status", self.repo.root, "CTK-L-0015", "--stage", "PUBLISHED", "--url", "https://youtu.be/abc123", "--date", "2026-11-01")
        self.assertEqual(code, 0, out)
        self.assertEqual(run("validate_content", self.repo.root)[0], 0)
        code, out = run("set_status", self.repo.root, "CTK-L-0015", "--stage", "PERFORMANCE_REVIEW")
        self.assertEqual(code, 1, "performance.yaml is required")
        workspace = find_item(self.repo, "CTK-L-0015").path
        fileio.write_text(workspace / "performance.yaml", fileio.dumps_yaml({
            "content_id": "CTK-L-0015", "video_url": "https://youtu.be/abc123",
            "snapshots": [{"captured_on": "2026-11-05", "window": "first-7-days", "source": "youtube-studio",
                           "evidence": "SYNTHETIC test value", "entered_by": "unit-test", "metrics": {"views": 1}}],
        }))
        code, out = run("set_status", self.repo.root, "CTK-L-0015", "--stage", "PERFORMANCE_REVIEW")
        self.assertEqual(code, 0, out)
        # A correction after publishing is logged without voiding the approval.
        self.edit_item("CTK-L-0015", lambda d: d["corrections"].append({"date": "2026-11-05", "description": "Synthetic correction", "action": "Pinned comment added", "by": "unit-test"}))
        self.assertEqual(run("validate_content", self.repo.root)[0], 0)

    def test_post_publish_seo_change_needs_reapproval_and_keeps_stage(self):
        self.approve()
        self.edit_item("CTK-L-0015", lambda d: [entry.update(done=True) for entry in d["publication"]["upload_checklist"]])
        run("set_status", self.repo.root, "CTK-L-0015", "--stage", "PUBLISHED", "--url", "https://youtu.be/abc123", "--date", "2026-11-01")
        self.edit_item("CTK-L-0015", lambda d: d["seo"].update(recommended_title="Synthetic P0300 title B"))
        code, out = run("validate_content", self.repo.root)
        self.assertEqual(code, 1, "a changed published item needs re-approval")
        self.approve()
        item = find_item(self.repo, "CTK-L-0015")
        self.assertEqual(item.stage, "PUBLISHED")
        self.assertIn("Re-approved", item.data["history"][-1]["note"])
        self.assertEqual(run("validate_content", self.repo.root)[0], 0)

    def test_technical_review_survives_seo_work_but_qc_review_does_not(self):
        record_passing_reviews(self.repo, "CTK-L-0015", self.box.root)
        self.edit_item("CTK-L-0015", lambda d: d["seo"].update(description="Synthetic description about p0300, revised."))
        ctx, results = self.gates()
        requirements = {r["requirement"].split(" (")[0]: r["satisfied"] for r in qc.approval(ctx, results)["requirements"]}
        self.assertTrue(requirements["Independent technical review"])
        self.assertFalse(requirements["Independent qc review"])
        self.edit_file("CTK-L-0015", "script.md", lambda t: t.replace("Synthetic visual.", "Changed visual.", 1))
        ctx, results = self.gates()
        requirements = {r["requirement"].split(" (")[0]: r["satisfied"] for r in qc.approval(ctx, results)["requirements"]}
        self.assertFalse(requirements["Independent technical review"])

    def test_description_with_chapters_counts_toward_limit(self):
        self.edit_item("CTK-L-0015", lambda d: d["seo"].update(description="x" * 4990))
        _, results = self.gates()
        self.assertTrue(any("with chapter lines" in e for e in self.findings(results, "G6", qc.FAIL)))


class TestTestItems(QCTestCase):
    def test_test_item_can_never_be_approved(self):
        code, out = run("new_content", self.repo.root, "--from-idea", "CTK-L-0015", "--test")
        self.assertEqual(code, 0, out)
        test_id = created_id(out)
        self.assertGreater(int(test_id[-4:]), 9000)
        ctx, results = self.gates(test_id)
        info = qc.approval(ctx, results)
        self.assertTrue(any(r["requirement"] == "Not a test item" and not r["satisfied"] for r in info["requirements"]))
        code, out = run("export_package", self.repo.root, test_id)
        self.assertEqual(code, 1)
        self.assertIn("Test items never get a release package", out)


if __name__ == "__main__":
    unittest.main()
