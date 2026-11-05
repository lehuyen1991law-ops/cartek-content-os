# Content brief — CTK-L-9001: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

> **TEST ITEM — NOT FOR PUBLICATION.** This workspace exists to test the workflow. Its research is not done and nothing in it is verified fact.

<!-- Acceptance test 2026-11-05. Based on the real sheet idea CTK-L-0015 ('Content Direction'!F12).
     The brief is complete as a planning document. Technical statements below are planning
     hypotheses that point to claims C01-C07 in item.yaml, all still "unverified". -->

| Field | Value |
|---|---|
| Content ID | CTK-L-9001 (test item based on CTK-L-0015) |
| Format | Long-form (16:9) |
| Pillar / category | P4 — Kiến thức chuyên sâu về hệ thống OBD2 |
| Source idea | CTK-L-0015 — 'Content Direction'!F12 |
| Target runtime | 5-8 phút (nguồn: sheet 'Content Direction'!B3) |

## Audience (Khán giả mục tiêu)

- **Primary persona:** Thợ sửa chữa ô tô (`technician`)
- **Secondary persona:** Chủ Garage ô tô (`garage-owner`): cùng quy trình, góc nhìn chi phí sửa chữa.
- **Technical depth:** intermediate to advanced. Người xem đã dùng máy đọc lỗi và biết thay bugi, bô-bin.
- **What they already know:** đọc mã lỗi cơ bản, hệ thống đánh lửa và nhiên liệu ở mức sửa chữa.
- **Why they would watch:** sheet ghi nỗi đau của thợ là "Cập nhật kiến thức, tìm kiếm thông tin , xử lý sự cố phức tạp" ('Khán giả'!C4). Bỏ máy nhiều xi-lanh là sự cố khó khoanh vùng.

## Problem (Vấn đề cần giải quyết)

Giả định cần xác nhận với kỹ thuật viên Cartek: khi máy đọc báo P0300, thợ thường thay bugi hoặc bô-bin theo kinh nghiệm trước khi xác định nguyên nhân, tốn chi phí cho khách và lỗi có thể quay lại.

## Takeaway (Điều người xem mang về)

Người xem có một quy trình khoanh vùng P0300: đọc mã và dữ liệu đi kèm, xếp nhóm nguyên nhân, chọn phép thử xác nhận trước khi thay linh kiện. Quy trình chỉ được trình bày sau khi các claim C01-C05 được kiểm chứng.

## Angle (Góc tiếp cận)

Trong sheet ('Đối thủ'!B6:F6), bốn trên năm kênh đối thủ bị ghi điểm yếu "chất lượng video chưa cao". Cartek làm khác bằng quy trình có nguồn kiểm chứng (chuẩn SAE/ISO, tài liệu hãng), phân biệt rõ "mã lỗi" với "nguyên nhân gốc", và minh họa trên xe thật khi có xe thử.

## Scope (Phạm vi)

- **In scope:** ý nghĩa của P0300 và các mã P0301-P0312 (C01, C02); dữ liệu đóng băng (C03); vì sao xóa mã không sửa lỗi (C04); nhóm nguyên nhân và phép thử xác nhận (C05); cảnh báo khi đèn báo lỗi nhấp nháy (C06).
- **Out of scope:** quy trình riêng của từng hãng, thao tác tháo hệ thống nhiên liệu, xe hybrid/điện.
- **Vehicles covered:** OBD-II chung (generic). Nếu quay demo, ghi rõ hãng/model/đời/động cơ của xe thử.

## Search intent and keywords (Ý định tìm kiếm)

- **Search intent:** troubleshooting
- **Primary keyword:** lỗi P0300
- **Secondary keywords:** P0300 là gì, bỏ máy ngẫu nhiên, chẩn đoán bỏ máy, mã lỗi OBD2

## Risks (Rủi ro kỹ thuật và an toàn)

- **Technical claims that need sources:** C01-C06 trong item.yaml, tất cả đang `unverified`. Nguồn dự kiến: SAE J2012 / ISO 15031-6 (định nghĩa mã), SAE J1979 (dữ liệu đóng băng, xóa mã), quy định OBD II của CARB (đèn nhấp nháy), tài liệu hãng cho phép thử.
- **Safety topics:** `fuel-system` (kim phun là nguyên nhân khả dĩ; phép thử áp suất nhiên liệu) và `hot-or-moving-parts` (kiểm tra khi động cơ đang chạy). Cần kỹ thuật viên có chuyên môn duyệt.
- **Cartek 2 features mentioned:** đọc mã và dữ liệu đóng băng bằng Cartek 2 (C07). Sổ đăng ký tính năng đang trống nên đoạn demo bị chặn cho đến khi đội sản phẩm xác nhận.

## Demonstration plan (Kế hoạch demo)

- Chưa chọn xe thử có P0300 thật và chưa xác nhận tính năng Cartek 2. Kế hoạch: quay màn hình máy đọc (mã + dữ liệu đóng băng), cận cảnh đèn báo lỗi, đồ họa sơ đồ xi-lanh. Ghi vào `production.demo_setup` khi có xe và thiết bị.
