# Research report — CTK-L-0015: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

<!-- Báo cáo nghiên cứu. Quy tắc: workflows/research.md.
     - Mỗi luận điểm kỹ thuật dùng trong kịch bản = một claim trong item.yaml (claims:) có nguồn (sources:).
     - Không bịa dữ liệu chẩn đoán, tương thích xe, nguyên nhân lỗi hay tính năng Cartek 2.
     - Thiếu bằng chứng -> giữ claim ở trạng thái "unverified": QC sẽ chặn duyệt kỹ thuật. -->

> **Trạng thái nghiên cứu (2026-11-06):** đã đọc 2 nguồn quy định (SRC01: CARB 13 CCR 1968.2 bản trên LII;
> SRC02: 40 CFR 86.1806-17 trên eCFR). C03-C07, C11, C12 có nguồn. C01, C02 (định nghĩa mã) và C08-C10 (quy trình
> kiểm tra) chưa có nguồn thuộc loại được chấp nhận: cần SAE J2012 / tài liệu hãng / giáo trình. Cả 12 claim đều `unverified`.

## Research question (Câu hỏi nghiên cứu)

Khi xe báo P0300, thợ sửa chữa (persona `technician`, độ sâu advanced) cần hiểu mã này nói gì và không nói gì,
và làm thế nào để khoanh vùng nguyên nhân bằng freeze frame, dữ liệu trực tiếp và phép thử xác nhận trước khi
thay phụ tùng; đồng thời vì sao xóa mã không sửa được lỗi và đèn MIL nhấp nháy có ý nghĩa gì.

## Findings (Kết quả nghiên cứu)

Nguồn: SRC01 = Cal. Code Regs. tit. 13, § 1968.2 (CARB, văn bản trên LII Cornell); SRC02 = 40 CFR 86.1806-17 (EPA, eCFR).

1. **Ý nghĩa P0300.** P0300 cho biết ECU phát hiện bỏ máy ngẫu nhiên/nhiều xi-lanh và không chỉ ra nguyên nhân [C01].
   Chưa có nguồn chấp nhận được. Bối cảnh từ SRC01 (e)(3.1.3): quy định yêu cầu một mã riêng cho bỏ máy nhiều xi-lanh,
   nhưng không nêu số mã.
2. **P0301-P0312.** Bỏ máy ở một xi-lanh xác định [C02]. Chưa có nguồn chấp nhận được. Bối cảnh từ SRC01 (e)(3.1.2)-(3.1.3):
   hệ thống phải xác định xi-lanh bỏ máy; từ đời 2005, nếu hơn 90% số lần bỏ máy nằm ở một xi-lanh, hãng được phép lưu mã
   của xi-lanh đó thay cho mã nhiều xi-lanh. Nghĩa là P0300 và P030x có thể xuất hiện khác nhau tùy chiến lược của hãng.
3. **Freeze frame.** Ghi mã lỗi gây ra bản ghi và các thông số như tải tính toán, nhiệt độ nước làm mát, tốc độ động cơ,
   tốc độ xe; trên xe có trang bị còn có trạng thái hệ thống nhiên liệu, fuel trim, áp suất đường ống nạp, lưu lượng khí nạp
   [C03] (SRC01 (g)(4.3.1)(B), (g)(4.2.1)). Mã bỏ máy được ưu tiên: freeze frame của lỗi khác (trừ hệ thống nhiên liệu) bị
   thay bằng freeze frame của bỏ máy (SRC01 (e)(3.4.4)(A)(ii)). Đây là lý do nên đọc freeze frame trước khi xóa.
4. **Xóa mã.** Lệnh xóa từ máy chẩn đoán xóa toàn bộ thông tin chẩn đoán liên quan khí thải: mã pending và confirmed,
   freeze frame, readiness, kết quả test [C04] (SRC01 (g)(4.10.1)-(4.10.2)). Quy định gọi lệnh này là Service $04 (SAE J1979)
   và Service $14 (SAE J1979-2). Monitor bỏ máy tiếp tục giám sát, nên nếu nguyên nhân còn, mã sẽ được ghi lại [C05]
   (SRC01 (e)(3.1.1), (e)(3.4.1)). Mã permanent không xóa được bằng máy chẩn đoán hay ngắt điện; ECU tự xóa khi xác định
   lỗi không còn [C12] (SRC01 (g)(4.4.6), (d)(2.5)).
5. **MIL nhấp nháy.** Hãng xác định tỷ lệ bỏ máy (theo từng 200 vòng quay) gây nhiệt độ làm hỏng bộ xúc tác; khi vượt
   ngưỡng này, MIL nhấp nháy mỗi giây một lần trong lúc bỏ máy đang xảy ra [C06] (SRC01 (e)(3.2.1)(A), (e)(3.4.1)(A)(ii)).
   Ngoại lệ: xe cắt nhiên liệu khi bỏ máy được phép chỉ sáng liên tục ((e)(3.4.1)(D)), và chiến lược sáng liên tục khi bỏ máy
   ở mọi chế độ có thể được duyệt ((e)(3.4.1)(E)). Kịch bản không được nói "đèn sáng đứng thì không có bỏ máy nặng".
   Hành động khuyến nghị [C07] mới có nguồn một phần: quy định nêu lý do (nhiệt độ hỏng xúc tác, vận hành ở tốc độ/tải thấp
   giảm hư hỏng) nhưng không đưa lời khuyên cho người lái.
6. **Khoanh vùng nguyên nhân.** Bốn nhóm nguyên nhân khả dĩ, mỗi nhóm cần phép thử xác nhận [C08]; phép thử cho đánh
   lửa/nhiên liệu theo quy trình hãng [C09]; rò rỉ khí nạp và cơ khí [C10]. Chưa có nguồn: quy định không liệt kê nguyên nhân.
7. **Phạm vi.** 13 CCR 1968.2 áp dụng cho xe du lịch, xe tải nhẹ, xe tải hạng trung từ đời 2004 (SRC01 (b)); EPA yêu cầu
   xe đời 2017+ tuân theo bản 2013 của 1968.2 (SRC02 (a)). Không mặc nhiên áp dụng cho xe bán tại Việt Nam [C11].

## Standard vs manufacturer-specific (Chuẩn OBD-II và đặc thù hãng)

| Topic | OBD-II / EOBD standard | Manufacturer-specific | Claim |
|---|---|---|---|
| Định nghĩa P0300, P0301-P0312 | Mã generic `P0xxx` (SAE J2012 / ISO 15031-6; chưa đọc). Quy định yêu cầu mã theo xi-lanh và mã nhiều xi-lanh (SRC01 (e)(3.1)) | Thứ tự đánh số xi-lanh; khi nào lưu mã xi-lanh thay cho mã nhiều xi-lanh (ngưỡng 90%, SRC01 (e)(3.1.3)) | C01, C02 |
| Freeze frame | Nội dung tối thiểu theo SRC01 (g)(4.3.1), truy cập theo SAE J1979 / J1979-2 | Thông số chỉ có "nếu xe có trang bị"; dữ liệu bỏ máy mở rộng qua chẩn đoán hãng | C03 |
| Xóa mã | Xóa toàn bộ thông tin chẩn đoán liên quan khí thải (SRC01 (g)(4.10)) | Chức năng reset/học lại của hãng (ngoài phạm vi) | C04, C05 |
| Mã permanent | Không xóa bằng máy chẩn đoán; lưu dần từ đời 2010-2012 (SRC01 (d)(2.2.5), (g)(4.4.6)) | Điều kiện monitor chạy lại do hãng hiệu chỉnh | C12 |
| MIL nhấp nháy | Nhấp nháy 1 lần/giây khi bỏ máy gây hỏng xúc tác (SRC01 (e)(3.4.1)) | Ngưỡng % bỏ máy do hãng xác định; ngoại lệ cắt nhiên liệu / sáng liên tục | C06, C07 |
| Phép thử xác nhận | Không thuộc chuẩn OBD-II | Quy trình, thông số và giá trị chuẩn theo tài liệu hãng cho xe cụ thể | C08, C09, C10 |

## Codes vs root causes (Mã lỗi và nguyên nhân gốc)

<!-- Mã lỗi cho biết ECU phát hiện một điều kiện, KHÔNG phải nguyên nhân đã xác nhận.
     Mỗi nguyên nhân khả dĩ cần một phép kiểm tra để xác nhận. -->
| Symptom / code | Candidate cause | Confirming test | Claim |
|---|---|---|---|
| P0300 (± P030x) | Đánh lửa (bugi, bô-bin, dây bugi) | Kiểm tra theo quy trình hãng; hoán đổi bô-bin giữa hai xi-lanh để xem bỏ máy có đi theo không | C08, C09 (unverified, chưa có nguồn) |
| P0300 (± P030x) | Nhiên liệu (áp suất, kim phun) | Đo áp suất nhiên liệu và kiểm tra kim phun theo quy trình và thông số của hãng | C08, C09 (unverified, chưa có nguồn) |
| P0300 + fuel trim lệch | Rò rỉ khí nạp / chân không | Thử khói (smoke test) kết hợp đọc fuel trim | C08, C10 (unverified, chưa có nguồn) |
| P0300 (± P030x) | Cơ khí (độ nén, xu-páp) | Đo áp suất nén hoặc thử độ lọt khí (leak-down) | C08, C10 (unverified, chưa có nguồn) |

Không có hàng nào là nguyên nhân đã xác nhận. Kịch bản không được nói một nguyên nhân là chắc chắn chỉ từ mã P0300,
và không dùng từ "thường gặp"/"phổ biến" cho nhóm nào khi chưa có nguồn.

## Vehicle and model-year differences (Khác biệt theo xe/đời xe)

Nội dung ở mức generic (`vehicle.scope: generic`), nhưng có khác biệt theo đời xe ngay trong quy định đã đọc:
mã permanent được lưu dần cho đời 2010-2012 trở lên (SRC01 (d)(2.2.5)); quy tắc lưu mã xi-lanh thay mã nhiều xi-lanh
áp dụng từ đời 2005 (SRC01 (e)(3.1.3)); xóa thông tin trên mọi ECU khi dùng máy chẩn đoán được áp dụng dần đời
2019-2021 (SRC01 (g)(4.10.2)); xe dùng SAE J1979-2 có lệnh và cách lưu freeze frame khác. Ngưỡng phát hiện bỏ máy, chiến
lược bảo vệ bộ xúc tác, thứ tự xi-lanh, quy trình và giá trị chuẩn thay đổi theo hãng, đời xe và động cơ. Section (e) của
SRC01 chỉ áp dụng cho động cơ xăng/đánh lửa cưỡng bức. Quy định Mỹ (SRC01 (b), SRC02 (a)) và EOBD châu Âu áp dụng cho xe
chứng nhận tại thị trường đó; chúng không mặc nhiên mô tả mọi xe bán tại Việt Nam [C11]. Video phải nói rõ: kiểm tra theo
tài liệu của hãng cho đúng thị trường, đời xe và động cơ. Không trích giá trị số nào khi chưa có tài liệu hãng cho xe cụ thể.

## Cartek 2 features used (Tính năng Cartek 2)

<!-- Chỉ dùng tính năng có status "verified" trong data/reference/cartek-2-feature-register.yaml. -->
None. Feature register đang trống; không có claim `cartek-feature`. Nếu kịch bản muốn quay Cartek 2 đọc freeze frame
hay dữ liệu trực tiếp, cần product team xác nhận tính năng trong register trước.

## Safety notes (An toàn)

- **MIL nhấp nháy:** cần cảnh báo bằng lời rằng mức bỏ máy này được xác định là mức gây nhiệt độ làm hỏng bộ xúc tác (SRC01 (e)(3.2.1)(A)); lời khuyên giảm tải và kiểm tra sớm [C07] cần thêm nguồn từ tài liệu hãng.
- **Hệ thống nhiên liệu (`fuel-system`):** đo áp suất nhiên liệu hoặc kiểm tra kim phun có nguy cơ phun xăng và cháy. Chỉ thực hiện theo quy trình xả áp của hãng, có bình chữa cháy, không có nguồn lửa. Cần cảnh báo bằng lời trong video.
- **Động cơ đang chạy, chi tiết nóng/quay (`hot-or-moving-parts`):** đọc dữ liệu trực tiếp, hoán đổi bô-bin, thử khói và đo áp suất nén liên quan đến động cơ đang chạy hoặc vừa tắt: quạt, dây curoa, ống xả và cổ góp nóng. Cần cảnh báo bằng lời.
- **Đoàn quay:** giữ khoảng cách với quạt và dây curoa khi quay cận cảnh khoang máy, thông gió khi nổ máy trong xưởng.
- Đề xuất `safety.flags: [fuel-system, hot-or-moving-parts]`; technical-fact-checker quyết định cuối cùng. Cần review kỹ thuật bởi người có chuyên môn.
- Các cảnh báo an toàn trên chưa có nguồn thuộc loại được chấp nhận (tài liệu hãng/giáo trình); quy định đã đọc không đề cập.

## Open questions (Câu hỏi còn mở)

- C01, C02: định nghĩa P0300 và P0301-P0312 cần SAE J2012 / ISO 15031-6 (trả phí) hoặc tài liệu sửa chữa hãng công khai. Quy định (SRC01) chỉ là bối cảnh và không thuộc loại nguồn được chấp nhận cho `dtc-definition`.
- C05: quy định mô tả việc phát hiện lại, không nói về sửa chữa; "xóa mã không sửa được lỗi" là suy luận, fact-checker cần chấp nhận hoặc bổ sung nguồn hãng.
- C07: hành động khuyến nghị khi MIL nhấp nháy cần sách hướng dẫn sử dụng hoặc tài liệu hãng.
- C08, C09, C10: nhóm nguyên nhân và quy trình kiểm tra cần tài liệu hãng hoặc giáo trình; xe demo chưa được chọn nên chưa có tài liệu hãng cụ thể.
- C11: chưa đọc quy định OBD nào áp dụng cho xe tại Việt Nam; nửa sau của claim là suy luận từ phạm vi của SRC01/SRC02.
- SRC01 là văn bản do LII đăng lại (bản sửa đổi đến Register 2022); fact-checker nên đối chiếu với bản chính thức của CARB/OAL nếu cần. Bản CARB 2006 (https://ww2.arb.ca.gov/sites/default/files/barcu/regact/obdii06/19682clean.pdf) đã tải nhưng không dùng vì là bản cũ.
- Safety notes chưa có nguồn chấp nhận được cho các bước an toàn khi đo áp suất nhiên liệu.

## Fact-check log (Nhật ký kiểm chứng)

<!-- technical-fact-checker ghi mỗi quyết định: claim, kết luận, bằng chứng, người kiểm, ngày. -->
| Claim | Decision | Evidence | Checked by | Date |
|---|---|---|---|---|
