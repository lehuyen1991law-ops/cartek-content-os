# QC report — CTK-L-9001: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

> **TEST ITEM — NOT FOR PUBLICATION.** This workspace exists to test the workflow. Its research is not done and nothing in it is verified fact.

| Field | Value |
|---|---|
| Run date | 2026-11-05 |
| Stage | RESEARCH |
| Content fingerprint | `sha256:e4ab245a848cf2a7b0542cfbbf41665b3b7ed0a525f51e27520134cca6007207` |
| Automated result | **FAIL** |
| Approval status | **NOT APPROVABLE** |

## Gate summary

| Gate | Check | Result | Summary |
|---|---|---|---|
| G1 | Source data and metadata validation | **PASS** | Provenance: CTK-L-0015 from 'Content Direction'!F12. |
| G2 | Audience and topic relevance | **PASS** | Brief complete for primary audience Thợ sửa chữa ô tô. |
| G3 | Research completeness and factual accuracy | **BLOCKED** | research.md still has 5 [TODO] marker(s). |
| G4 | Script coherence, clarity and retention quality | **BLOCKED** | script.md still has 9 [TODO] marker(s). |
| G5 | Automotive technical and safety review | **BLOCKED** | The script is not finished; the technical and safety review needs the final narration. |
| G6 | SEO package completeness | **FAIL** | Chapters: 0 chapter(s); YouTube needs at least 3. |
| G7 | Production handoff readiness | **FAIL** | Demo segments exist but production.demo_setup lacks the tool and vehicle/location. |
| G8 | Publishing metadata validation | **FAIL** | No target publish date. |

## Gate details

### G1 — Source data and metadata validation: PASS

Evidence:

- [PASS] Provenance: CTK-L-0015 from 'Content Direction'!F12.
- [PASS] P4: Kiến thức chuyên sâu về hệ thống OBD2.
- [PASS] Metadata complete; ID, folder, provenance and vocabularies consistent.

### G2 — Audience and topic relevance: PASS

Evidence:

- [PASS] Brief complete for primary audience Thợ sửa chữa ô tô.
- [INFO] Relevance and audience fit also need an independent judgment review (role qc).

### G3 — Research completeness and factual accuracy: BLOCKED

Evidence:

- [BLOCKED] research.md still has 5 [TODO] marker(s).
- [BLOCKED] C01 is unverified: "P0300 là mã lỗi chuẩn (generic) nghĩa là phát hiện bỏ máy ngẫu nhiên/nhiều xi-lanh (Rando…"
- [BLOCKED] C02 is unverified: "Các mã P0301-P0312 chỉ hiện tượng bỏ máy được phát hiện ở xi-lanh số 1-12."
- [BLOCKED] C03 is unverified: "Dữ liệu đóng băng (freeze frame) ghi lại điều kiện vận hành tại thời điểm mã lỗi được lưu."
- [BLOCKED] C04 is unverified: "Xóa mã lỗi chỉ xóa mã và dữ liệu chẩn đoán liên quan, đặt lại trạng thái sẵn sàng; không …"
- [BLOCKED] C05 is unverified: "Nhóm nguyên nhân cần kiểm tra khi có P0300: đánh lửa, nhiên liệu, khí nạp (rò chân không)…"
- [BLOCKED] C06 is unverified: "Đèn báo lỗi động cơ nhấp nháy khi mức bỏ máy đủ để làm hỏng bộ xúc tác; cần giảm tải và d…"
- [BLOCKED] C07 is unverified: "Cartek 2 đọc được mã P0300 và dữ liệu đóng băng."
- [BLOCKED] C07 describes a Cartek 2 capability that is not in the feature register.

Corrections:

- Complete the research (skill: automotive-researcher).
- Verify it with an accepted source, or mark it removed and take it out of the script (skill: technical-fact-checker).
- Add it to data/reference/cartek-2-feature-register.yaml with product-team evidence, then set feature_id.

### G4 — Script coherence, clarity and retention quality: BLOCKED

Evidence:

- [BLOCKED] script.md still has 9 [TODO] marker(s).
- [INFO] Runtime estimate so far: 00:07 (narration incomplete).
- [INFO] Clarity, coherence and retention quality also need an independent judgment review (role qc).

Corrections:

- Finish the script (skill: youtube-scriptwriter).

### G5 — Automotive technical and safety review: BLOCKED

Evidence:

- [BLOCKED] The script is not finished; the technical and safety review needs the final narration.
- [BLOCKED] research.md is not finished; technical accuracy cannot be reviewed yet.
- [INFO] Safety flags fuel-system, hot-or-moving-parts: a qualified human technical review is required before approval.
- [BLOCKED] C05 (diagnostic-procedure) is unverified: technical approval is blocked.
- [BLOCKED] C06 (safety) is unverified: technical approval is blocked.
- [INFO] Automotive accuracy also needs an independent technical review (role technical).

Corrections:

- Finish script.md first (G4), then re-run QC.
- Finish the research first (G3).
- Verify the procedure/safety statement with OEM or standard sources, or remove it.

### G6 — SEO package completeness: FAIL

Evidence:

- [BLOCKED] seo.md still has 3 [TODO] marker(s).
- [FAIL] Chapters: 0 chapter(s); YouTube needs at least 3.

Corrections:

- Complete the SEO analysis (skill: youtube-seo-specialist).
- Build chapters from `python3 scripts/qc_content.py runtime <ID>` timings.

### G7 — Production handoff readiness: FAIL

Evidence:

- [BLOCKED] Script gate G4 is BLOCKED; the production handoff needs a finished script.
- [BLOCKED] storyboard.md still has 5 [TODO] marker(s).
- [BLOCKED] Assets not yet available: Thiết bị Cartek 2 (tính năng cần xác nhận trong sổ đăng ký), Xe thử có mã P0300 thật, Đồ họa sơ đồ xi-lanh, bảng dữ liệu đóng băng, sơ đồ cây nguyên nhân, Kỹ thuật viên có chuyên môn duyệt nội dung an toàn.
- [FAIL] Demo segments exist but production.demo_setup lacks the tool and vehicle/location.
- [FAIL] No responsible person (owner).
- [FAIL] No target publish date.

Corrections:

- Resolve G4 first.
- Complete the shot list.
- Confirm availability and set status to available or confirmed.
- Record tool, tool version, vehicle and location.
- Set item.yaml -> owner (Người phụ trách).
- Set item.yaml -> target_publish_date.

### G8 — Publishing metadata validation: FAIL

Evidence:

- [FAIL] No target publish date.
- [FAIL] No visibility plan.
- [BLOCKED] 8 of 8 publishing checklist item(s) in seo.md are not ticked.

Corrections:

- Set item.yaml -> target_publish_date.
- Set publication.visibility_plan (public, scheduled, unlisted or private).
- Complete each item and tick it ([x]) before publishing.

## Approval requirements

| Requirement | Met | Detail |
|---|---|---|
| Automated gates G1-G8 all PASS on the current content | no | not PASS: G3, G4, G5, G6, G7, G8 |
| Not a test item | no | Test items (IDs 9001-9999) can never be approved for release. |
| Independent qc review (G2, G4, G6, G7) by agent or human | no | no review for G2, G4, G6, G7 |
| Independent technical review (G3, G5) by agent or human | no | no review for G3, G5 |
| Qualified human technical review of G3 and G5 (safety flags: fuel-system, hot-or-moving-parts) | no | none on the current content |
| Human editorial sign-off | no | none on the current content |

## Review history

| Review | Date | Reviewer | Type | Role | Decision | On current content |
|---|---|---|---|---|---|---|
| R001 | 2026-11-05 | scripts/qc_content.py | automated | qc | FAIL | yes |
| R002 | 2026-11-05 | scripts/qc_content.py | automated | qc | FAIL | yes |
