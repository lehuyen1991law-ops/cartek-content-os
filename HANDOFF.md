# HANDOFF — Cartek Content OS (bàn giao cho tài khoản/agent khác)

Cập nhật: 2026-11-06. Đọc `CLAUDE.md` trước, rồi file này.

## 1. Trạng thái repo

- Repo: `lehuyen1991law-ops/cartek-content-os` (private).
- Nhánh làm việc: `claude/epic-turing-1lotwr`.
- `main` có PR #1 (merge `3aa2d59`) nhưng **chưa có** commit hardening `a585060` và các commit sau. Cần mở PR mới vào `main` khi người dùng đồng ý.
- 133 test pass (`make check` chạy tests + import check + validate + links). CI: `.github/workflows/content-qc.yml`.
- Sheet nguồn (chỉ đọc): ID `1r4dfNOPGx50rXMuhZL6Tm0B5XG8nb47t7mSjVdDY-F4`. Không bao giờ ghi vào sheet.

## 2. Yêu cầu của người dùng (tiếng Việt)

- Muốn hoàn thiện video thật **CTK-L-0015 "Lỗi P0300 - Ác Mộng của Mọi Động Cơ?"** theo văn phong thợ nói với thợ, **giọng tiếng Việt tự nhiên, bớt "AI"**.
- Thư mục Codex trên máy người dùng `C:\Users\LeeA\Documents\Codex\2026-11-05` **không truy cập được từ cloud**. Cần người dùng push nhánh hoặc chia sẻ thư mục, rồi so sánh và gộp phần tốt.
- Repo đang private. Muốn ChatGPT Work/tài khoản khác truy cập: mời làm collaborator (read) hoặc dùng token read-only do người dùng tự tạo. Không public repo khi chưa được cho phép.

## 3. CTK-L-0015 — còn việc gì

Workspace: `content/long-form/CTK-L-0015-loi-p0300-ac-mong-cua-moi-dong-co/`. Stage hiện tại: RESEARCH. Audience: technician. `safety.flags`: fuel-system, hot-or-moving-parts.

Đã xong: `research.md` (nguồn SRC01 = 13 CCR 1968.2, SRC02 = 40 CFR 86.1806-17; claims C01–C12 đều `unverified`), `script.md` bản nháp mới (9 đoạn S01–S09, chưa commit).

Kết quả `python3 scripts/qc_content.py run CTK-L-0015` gần nhất:

| Gate | Kết quả | Việc cần làm |
|---|---|---|
| G1 | PASS | — |
| G2 | BLOCKED | `brief.md` còn `[TODO]`: viết brief (skill cartek-content-strategist) |
| G3 | BLOCKED | claims chưa verified. C01, C02, C08–C10 cần nguồn được chấp nhận (SAE J2012, tài liệu OEM hoặc giáo trình). Chạy skill technical-fact-checker |
| G4 | FAIL | Runtime ước tính 04:04, mục tiêu 05:00–08:00. Mở rộng lời thoại ~1–3 phút bằng chi tiết xưởng thật, không bịa số liệu. Kiểm tra: `python3 scripts/qc_content.py runtime CTK-L-0015` |
| G5 | FAIL | (a) S02 nhắc "xóa mã" mà caveat nằm ở S04: thêm câu "xóa mã không sửa nguyên nhân" ngay S02 hoặc S03, hoặc bỏ nhắc xóa ở S02. (b) Đã xử lý 2026-11-06: "Logo Cartek" / màn hình kết thúc Cartek không còn bị báo (`config/qc-policy.yaml` → `brand_mark_mentions`); mọi câu nói về tính năng Cartek 2 vẫn FAIL nếu không có claim `cartek-feature` |
| G6 | FAIL | SEO trống: khối `seo` trong `item.yaml` (title ≤100 ký tự, mô tả ≤5000 và phải có caveat xóa mã, tags ≤500 ký tự, ≥3 chapter từ bảng runtime, ≥2 ý tưởng thumbnail) và `seo.md` (skill youtube-seo-specialist) |
| G7 | FAIL | `storyboard.md` còn template; thiếu assets, `demo_setup`, owner, `target_publish_date`, `visibility_plan`. Khi viết storyboard, điền cột `Effects` / `Text style` theo `config/visual-style.yaml` (xem mục Visual style bên dưới) |
| G8 | FAIL | Owner và ngày trống |

Sau khi sửa: chạy `qc_content.py run`, ghi 2 review độc lập (qc + technical) bằng `qc_content.py review --file` (mẫu `templates/review.yaml`), vì có safety flags nên **cần review kỹ thuật bởi người có chuyên môn**. Phê duyệt (`qc_content.py approve --by`) và chốt biên tập là việc của **con người**. Không được tự khai đã duyệt hoặc đã xuất bản.

**Visual style (thêm 2026-11-06, mặc định của repo, chưa phải quyết định của đội thương hiệu):** `config/visual-style.yaml` + `strategy/visual-identity.md` định nghĩa vai chữ (`caption`, `lower_third`, `callout`, `dtc_code`, `live_data_number`, `end_screen`), font OFL có hỗ trợ tiếng Việt (Be Vietnam Pro, JetBrains Mono cho mã lỗi; chưa kiểm tra từng glyph), bảng màu tạm, thư viện hiệu ứng (vd. `code-popup`, `highlight-circle`, `safety-banner`, `sfx-ui-beep`; không âm thanh hù dọa/còi, SFX không chồng lời thoại) và quy tắc phụ đề bắt buộc. `templates/storyboard.md` có thêm cột `Effects`, `Text style` và mục "Sound and effects", "Typography". G7 chỉ **cảnh báo** (WARN) khi ID lạ, đoạn có `SAFETY:` mà không shot nào dùng `safety-banner`, hoặc dùng hiệu ứng quá mức gợi ý; gói sản xuất có thêm khối `visual_style`. Lưu ý: file config này không nằm trong fingerprint, đổi thư viện thì phải export lại gói release. Storyboard của CTK-L-0015 đã dùng cột mới (34 shot cho 11 đoạn, 13 ID hiệu ứng, 6 vai chữ; G7 chỉ có INFO). Chỉ CTK-L-9001 (test item) còn theo mẫu cũ không có cột `Effects`: G7 không cảnh báo thiếu `safety-banner` cho storyboard không khai báo hiệu ứng nào, chỉ ghi INFO "No effects declared".

Quy tắc giọng văn đã chốt cho script: câu ngắn, nói được thành tiếng, không mở bài kiểu "hôm nay chúng ta sẽ cùng nhau", demo dùng "máy chẩn đoán" (không nêu tính năng Cartek 2 vì sổ tính năng `data/reference/cartek-2-feature-register.yaml` đang trống), CTA kết bằng "Cartek - Check your car".

## 4. Việc dọn repo còn tồn

- `reports/acceptance/2026-11-05-end-to-end.md` đang cũ: ghi review "Pending" và 94 test. Thực tế R003 (qc) và R004 (technical) đã ghi, cả hai FAIL, sau đó đã sửa 13 vấn đề; hiện 115 test.
- Cập nhật `CHANGELOG.md`, tài liệu cho hành vi mới (technical fingerprint gồm storyboard và SEO công khai; ID tường minh; fingerprint scope `video`).
- Chạy lại `python3 scripts/generate_board.py`, `make check`.
- Còn ~100 finding mức thấp/trung bình chưa xử lý, nằm ở `/tmp/.../scratchpad/review.json` (có thể đã mất, chạy lại review nếu cần). Ví dụ: `check_links.py` bỏ sót anchor và link ảnh, ca biên về tiêu đề/ID trùng, caveat DTC permanent, quy trình sửa sau khi xuất bản vs tái duyệt, danh tính reviewer tự khai, cờ `--record`.

## 5. Lệnh hữu ích

```bash
python3 scripts/qc_content.py runtime CTK-L-0015
python3 scripts/qc_content.py run CTK-L-0015
python3 scripts/qc_content.py status CTK-L-0015
python3 scripts/set_status.py CTK-L-0015 --stage SCRIPT
python3 scripts/validate_content.py
make check
```

## 6. Quy tắc cứng (tóm tắt)

- Không bịa dữ liệu chẩn đoán, tương thích xe, nguyên nhân lỗi, thông số hay tính năng Cartek 2.
- Xóa mã không sửa lỗi; mọi chỗ nhắc xóa mã phải nói rõ.
- Mọi câu kỹ thuật là một claim trong `item.yaml` có nguồn hợp lệ; thiếu bằng chứng thì giữ `unverified` hoặc bỏ.
- Không bịa chỉ số YouTube, không hứa CTR/xếp hạng/view. Không đăng lên YouTube. Không sửa Google Sheet. Không commit secret. Không sửa tay file sinh tự động (`data/source`, `data/normalized`, `reports/*`, `qc-report.md`, `exports/`).
- Item `CTK-?-9xxx` là item test, không bao giờ duyệt.

## 7. Môi trường (cloud)

- `gh` CLI token không dùng được; dùng GitHub MCP tools.
- Mạng qua proxy; môi trường cá nhân `cartek-content-os` (`env_01NZA95u2zG1ugAaUSwdMbsS`) đã cho phép arb.ca.gov, www.law.cornell.edu, www.ecfr.gov. Tài khoản khác cần tự cấu hình lại nếu cần tra cứu quy định.
- Python 3.13 cục bộ, CI dùng 3.12; chạy test bằng `unittest` (không có pytest).
