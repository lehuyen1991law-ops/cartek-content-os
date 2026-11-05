# Research report — CTK-L-9001: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

> **TEST ITEM — NOT FOR PUBLICATION.** This workspace exists to test the workflow. Its research is not done and nothing in it is verified fact.

<!-- Acceptance test 2026-11-05: research was deliberately NOT performed. The question, the claim
     register (item.yaml, all "unverified") and the candidate sources are prepared so the gates can be
     exercised. QC gate G3 must stay BLOCKED until a researcher completes this file. -->

## Research question (Câu hỏi nghiên cứu)

Khi máy đọc lỗi báo P0300, kỹ thuật viên cần biết gì và kiểm tra theo thứ tự nào để tìm nguyên nhân gốc trước khi thay linh kiện?

## Findings (Kết quả nghiên cứu)

[TODO: Research not performed in the acceptance test. Verify C01-C06 against the candidate sources SRC01-SRC03 and OEM service information, then write the findings with claim IDs.]

## Standard vs manufacturer-specific (Chuẩn OBD-II và đặc thù hãng)

| Topic | OBD-II / EOBD standard | Manufacturer-specific | Claim |
|---|---|---|---|
| Định nghĩa P0300, P0301-P0312 | Cần kiểm chứng (SAE J2012 / ISO 15031-6) | — | C01, C02 |
| Dữ liệu đóng băng, xóa mã | Cần kiểm chứng (SAE J1979) | — | C03, C04 |
| Ngưỡng phát hiện bỏ máy, phép thử chi tiết | — | Theo tài liệu từng hãng | C05 |

## Codes vs root causes (Mã lỗi và nguyên nhân gốc)

| Symptom / code | Candidate cause | Confirming test | Claim |
|---|---|---|---|
| P0300 | [TODO: nhóm nguyên nhân cần nguồn tài liệu hãng hoặc giáo trình] | [TODO] | C05 |

## Vehicle and model-year differences (Khác biệt theo xe/đời xe)

[TODO: chưa chọn xe thử; nếu video giữ ở mức OBD-II chung, ghi rõ giới hạn này.]

## Cartek 2 features used (Tính năng Cartek 2)

None. C07 (Cartek 2 đọc mã và dữ liệu đóng băng) đã bị gỡ khỏi kịch bản ngày 2026-11-05 sau review R003/R004, vì `data/reference/cartek-2-feature-register.yaml` đang trống. Đoạn demo dùng máy chẩn đoán trung tính.

## Safety notes (An toàn)

[TODO: cảnh báo khi đèn báo lỗi nhấp nháy (C06), an toàn khi đo áp suất nhiên liệu và khi làm việc với động cơ đang chạy; cần kỹ thuật viên có chuyên môn xác nhận.]

## Open questions (Câu hỏi còn mở)

- Văn bản SAE J2012 / ISO 15031-6 và SAE J1979 hiện hành (cần quyền truy cập tài liệu có phí).
- Xe thử nào có P0300 thật để quay demo?
- Cartek 2 có đọc được dữ liệu đóng băng và bộ đếm bỏ máy theo xi-lanh không (hỏi đội sản phẩm)?

## Fact-check log (Nhật ký kiểm chứng)

| Claim | Decision | Evidence | Checked by | Date |
|---|---|---|---|---|
| C01-C07 | Not checked | Acceptance test: no source consulted | — | 2026-11-05 |
