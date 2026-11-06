# QC report — CTK-L-0015: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

| Field | Value |
|---|---|
| Run date | 2026-11-06 |
| Stage | RESEARCH |
| Content fingerprint | `sha256:979c495924836edefe5efa4ef37695fb1404f415fe9a99de0838422b019f3f34` |
| Automated result | **FAIL** |
| Approval status | **NOT APPROVABLE** |

## Gate summary

| Gate | Check | Result | Summary |
|---|---|---|---|
| G1 | Source data and metadata validation | **PASS** | Provenance: CTK-L-0015 from 'Content Direction'!F12. |
| G2 | Audience and topic relevance | **BLOCKED** | brief.md still has 16 [TODO] marker(s). |
| G3 | Research completeness and factual accuracy | **BLOCKED** | C01 is unverified: "P0300 cho biết ECU đã phát hiện bỏ máy ngẫu nhiên hoặc ở nhiều xi-lanh (Random/Multiple C…" |
| G4 | Script coherence, clarity and retention quality | **BLOCKED** | script.md still has 29 [TODO] marker(s). |
| G5 | Automotive technical and safety review | **FAIL** | Safety flags (fuel-system, hot-or-moving-parts) but the script has no safety warning. |
| G6 | SEO package completeness | **FAIL** | 0 title candidate(s) in item.yaml; at least 3 required. |
| G7 | Production handoff readiness | **FAIL** | No production assets are listed. |
| G8 | Publishing metadata validation | **FAIL** | No target publish date. |

## Gate details

### G1 — Source data and metadata validation: PASS

Evidence:

- [PASS] Provenance: CTK-L-0015 from 'Content Direction'!F12.
- [PASS] P4: Kiến thức chuyên sâu về hệ thống OBD2.
- [PASS] Metadata complete; ID, folder, provenance and vocabularies consistent.

### G2 — Audience and topic relevance: BLOCKED

Evidence:

- [BLOCKED] brief.md still has 16 [TODO] marker(s).
- [INFO] Relevance and audience fit also need an independent judgment review (role qc).

Corrections:

- Complete the brief (skill: cartek-content-strategist).

### G3 — Research completeness and factual accuracy: BLOCKED

Evidence:

- [BLOCKED] C01 is unverified: "P0300 cho biết ECU đã phát hiện bỏ máy ngẫu nhiên hoặc ở nhiều xi-lanh (Random/Multiple C…"
- [BLOCKED] C02 is unverified: "Các mã P0301 đến P0312 cho biết ECU phát hiện bỏ máy ở một xi-lanh cụ thể; hai số cuối là…"
- [BLOCKED] C03 is unverified: "Freeze frame là bản ghi các thông số động cơ (ví dụ tốc độ động cơ, tải, nhiệt độ nước là…"
- [BLOCKED] C04 is unverified: "Xóa mã lỗi bằng máy chẩn đoán (Service $04) đồng thời xóa dữ liệu freeze frame và đặt lại…"
- [BLOCKED] C05 is unverified: "Xóa mã lỗi không sửa được nguyên nhân bỏ máy: nếu nguyên nhân còn, ECU sẽ phát hiện lại v…"
- [BLOCKED] C06 is unverified: "Trên xe được chứng nhận theo quy định OBD-II của Mỹ, đèn báo lỗi động cơ (MIL) nhấp nháy …"
- [BLOCKED] C07 is unverified: "Khi đèn check engine nhấp nháy, nên giảm tải, hạn chế chạy xe và kiểm tra sớm, vì tiếp tụ…"
- [BLOCKED] C08 is unverified: "Nguyên nhân khả dĩ của P0300 gồm các nhóm đánh lửa, nhiên liệu, rò rỉ khí nạp/chân không …"
- [BLOCKED] C09 is unverified: "Với nhóm đánh lửa và nhiên liệu, kiểm tra theo quy trình của hãng cho xe cụ thể (ví dụ ki…"
- [BLOCKED] C10 is unverified: "Với nhóm rò rỉ khí nạp, có thể xác nhận bằng thử khói (smoke test) kết hợp đọc fuel trim;…"
- [BLOCKED] C11 is unverified: "Quy định OBD-II của CARB/EPA áp dụng cho xe được chứng nhận để bán tại Mỹ; với xe bán tại…"

Corrections:

- Verify it with an accepted source, or mark it removed and take it out of the script (skill: technical-fact-checker).

### G4 — Script coherence, clarity and retention quality: BLOCKED

Evidence:

- [BLOCKED] script.md still has 29 [TODO] marker(s).
- [INFO] Runtime estimate so far: 00:06 (narration incomplete).
- [WARN] No retention notes.
- [INFO] Clarity, coherence and retention quality also need an independent judgment review (role qc).

Corrections:

- Finish the script (skill: youtube-scriptwriter).
- List open loops, pattern changes and payoffs under '## Retention notes'.

### G5 — Automotive technical and safety review: FAIL

Evidence:

- [BLOCKED] The script is not finished; the technical and safety review needs the final narration.
- [FAIL] Safety flags (fuel-system, hot-or-moving-parts) but the script has no safety warning.
- [INFO] Safety flags fuel-system, hot-or-moving-parts: a qualified human technical review is required before approval.
- [BLOCKED] C07 (safety) is unverified: technical approval is blocked.
- [BLOCKED] C08 (diagnostic-procedure) is unverified: technical approval is blocked.
- [BLOCKED] C09 (diagnostic-procedure) is unverified: technical approval is blocked.
- [BLOCKED] C10 (diagnostic-procedure) is unverified: technical approval is blocked.
- [INFO] Automotive accuracy also needs an independent technical review (role technical).

Corrections:

- Finish script.md first (G4), then re-run QC.
- Add a TYPE safety segment or a **SAFETY:** line where the risk occurs.
- Verify the procedure/safety statement with OEM or standard sources, or remove it.

### G6 — SEO package completeness: FAIL

Evidence:

- [BLOCKED] seo.md still has 9 [TODO] marker(s).
- [FAIL] 0 title candidate(s) in item.yaml; at least 3 required.
- [FAIL] No recommended title.
- [FAIL] No rationale for the recommended title.
- [FAIL] No description.
- [FAIL] 0 tag(s); at least 3 required.
- [BLOCKED] Chapters cannot be set yet: they need the timing of the finished narration.
- [FAIL] 0 thumbnail concept(s); at least 2 required.

Corrections:

- Complete the SEO analysis (skill: youtube-seo-specialist).
- Fill seo.title_candidates.
- Fill seo.recommended_title.
- Fill seo.title_rationale.
- Write seo.description.
- Add tags from the keyword notes.
- Finish script.md, then build chapters from `python3 scripts/qc_content.py runtime <ID>`.
- Add thumbnail concepts with on-image text.

### G7 — Production handoff readiness: FAIL

Evidence:

- [BLOCKED] Script gate G4 is BLOCKED; the production handoff needs a finished script.
- [BLOCKED] storyboard.md still has 4 [TODO] marker(s).
- [FAIL] No production assets are listed.
- [FAIL] Demo segments exist but production.demo_setup lacks the tool and vehicle/location.
- [FAIL] No responsible person (owner).
- [FAIL] No target publish date.

Corrections:

- Resolve G4 first.
- Complete the shot list.
- List tools, vehicles, graphics and footage in production.assets_required.
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
- Complete each item and tick it ([x]) before approval.

## Approval requirements

| Requirement | Met | Detail |
|---|---|---|
| Automated gates G1-G8 all PASS on the current content | no | not PASS: G2, G3, G4, G5, G6, G7, G8 |
| Independent qc review (G2, G4, G6, G7) by agent or human | no | no review for G2, G4, G6, G7 |
| Independent technical review (G3, G5) by agent or human | no | no review for G3, G5 |
| Qualified human technical review of G3 and G5 (safety flags: fuel-system, hot-or-moving-parts) | no | none on the current content |
| Human editorial sign-off | no | none on the current content |

## Review history

| Review | Date | Reviewer | Type | Role | Decision | On current content |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |
