# Research report — CTK-L-0015: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

<!-- Báo cáo nghiên cứu. Quy tắc: workflows/research.md.
     - Mỗi luận điểm kỹ thuật dùng trong kịch bản = một claim trong item.yaml (claims:) có nguồn (sources:).
     - Không bịa dữ liệu chẩn đoán, tương thích xe, nguyên nhân lỗi hay tính năng Cartek 2.
     - Thiếu bằng chứng -> giữ claim ở trạng thái "unverified": QC sẽ chặn duyệt kỹ thuật. -->

> **Trạng thái nghiên cứu (2026-11-06):** CHƯA CÓ NGUỒN NÀO ĐƯỢC ĐỌC. Mọi lần tải tài liệu (WebFetch) tới
> ww2.arb.ca.gov và www.law.cornell.edu đều thất bại vì host không nằm trong danh sách mạng được phép của
> phiên làm việc. Vì vậy `item.yaml` -> `sources` để trống và cả 11 claim đều `unverified` với `sources: []`.
> Các URL ở mục "Open questions" chỉ là đầu mối tìm được qua công cụ tìm kiếm, chưa được đọc, không phải nguồn.

## Research question (Câu hỏi nghiên cứu)

Khi xe báo P0300, thợ sửa chữa (persona `technician`, độ sâu advanced) cần hiểu mã này nói gì và không nói gì,
và làm thế nào để khoanh vùng nguyên nhân bằng freeze frame, dữ liệu trực tiếp và phép thử xác nhận trước khi
thay phụ tùng; đồng thời vì sao xóa mã không sửa được lỗi và đèn MIL nhấp nháy có ý nghĩa gì.

## Findings (Kết quả nghiên cứu)

Các điểm dưới đây là luận điểm kịch bản cần dùng. Tất cả đang chờ nguồn: chưa điểm nào được xác nhận.

1. **Ý nghĩa P0300.** P0300 cho biết ECU phát hiện bỏ máy ngẫu nhiên/nhiều xi-lanh và không chỉ ra nguyên nhân [C01].
   Nguồn cần: SAE J2012 / ISO 15031-6 hoặc tài liệu sửa chữa của hãng.
2. **P0301-P0312.** Bỏ máy ở một xi-lanh xác định; số cuối là số xi-lanh [C02]. Thứ tự đánh số xi-lanh do hãng quy định.
3. **Freeze frame.** Bản ghi điều kiện vận hành tại thời điểm lưu mã [C03]. Danh sách thông số cụ thể chưa xác nhận.
4. **Xóa mã.** Service $04 xóa mã, freeze frame và đặt lại readiness [C04]; xóa mã không sửa nguyên nhân và mã sẽ quay lại khi nguyên nhân còn [C05].
5. **MIL nhấp nháy.** Trên xe chứng nhận theo quy định OBD-II của Mỹ, MIL nhấp nháy khi mức bỏ máy có thể làm hỏng bộ xúc tác [C06];
   hành động khuyến nghị cho người lái/thợ [C07].
6. **Khoanh vùng nguyên nhân.** Bốn nhóm nguyên nhân khả dĩ, mỗi nhóm cần phép thử xác nhận [C08]; phép thử cho đánh lửa/nhiên liệu theo quy trình hãng [C09];
   rò rỉ khí nạp và cơ khí [C10].
7. **Phạm vi.** Quy định Mỹ áp dụng cho xe chứng nhận tại Mỹ, không mặc nhiên mô tả xe bán tại Việt Nam [C11].

## Standard vs manufacturer-specific (Chuẩn OBD-II và đặc thù hãng)

| Topic | OBD-II / EOBD standard | Manufacturer-specific | Claim |
|---|---|---|---|
| Định nghĩa P0300, P0301-P0312 | Mã generic `P0xxx` (SAE J2012 / ISO 15031-6) | Thứ tự đánh số xi-lanh; một số hãng có thêm mã bỏ máy riêng ngoài dải generic | C01, C02 |
| Freeze frame | Service $02 (SAE J1979 / ISO 15031-5) | Thông số mở rộng (dữ liệu bỏ máy theo xi-lanh, bộ đếm misfire) qua chẩn đoán hãng | C03 |
| Xóa mã | Service $04 xóa thông tin chẩn đoán liên quan khí thải | Chức năng reset/học lại của hãng | C04, C05 |
| MIL nhấp nháy | Yêu cầu trong quy định OBD-II của Mỹ (CARB/EPA) cho bỏ máy gây hỏng xúc tác | Ngưỡng phát hiện và chiến lược bảo vệ (ví dụ cắt nhiên liệu) do hãng hiệu chỉnh | C06, C07 |
| Phép thử xác nhận | Không thuộc chuẩn OBD-II | Quy trình, thông số và giá trị chuẩn theo tài liệu hãng cho xe cụ thể | C08, C09, C10 |

## Codes vs root causes (Mã lỗi và nguyên nhân gốc)

<!-- Mã lỗi cho biết ECU phát hiện một điều kiện, KHÔNG phải nguyên nhân đã xác nhận.
     Mỗi nguyên nhân khả dĩ cần một phép kiểm tra để xác nhận. -->
| Symptom / code | Candidate cause | Confirming test | Claim |
|---|---|---|---|
| P0300 (± P030x) | Đánh lửa (bugi, bô-bin, dây bugi) | Kiểm tra theo quy trình hãng; hoán đổi bô-bin giữa hai xi-lanh để xem bỏ máy có đi theo không | C08, C09 (unverified) |
| P0300 (± P030x) | Nhiên liệu (áp suất, kim phun) | Đo áp suất nhiên liệu và kiểm tra kim phun theo quy trình và thông số của hãng | C08, C09 (unverified) |
| P0300 + fuel trim lệch | Rò rỉ khí nạp / chân không | Thử khói (smoke test) kết hợp đọc fuel trim | C08, C10 (unverified) |
| P0300 (± P030x) | Cơ khí (độ nén, xu-páp) | Đo áp suất nén hoặc thử độ lọt khí (leak-down) | C08, C10 (unverified) |

Không có hàng nào là nguyên nhân đã xác nhận. Kịch bản không được nói một nguyên nhân là chắc chắn chỉ từ mã P0300,
và không dùng từ "thường gặp"/"phổ biến" cho nhóm nào khi chưa có nguồn.

## Vehicle and model-year differences (Khác biệt theo xe/đời xe)

Nội dung ở mức generic (`vehicle.scope: generic`): định nghĩa mã P0300-P0312 và các dịch vụ OBD-II là chung, nhưng
ngưỡng phát hiện bỏ máy, cách ECU bảo vệ bộ xúc tác, thứ tự xi-lanh, quy trình kiểm tra và giá trị chuẩn (áp suất
nhiên liệu, áp suất nén) thay đổi theo hãng, đời xe và động cơ. Quy định OBD-II của Mỹ (CARB 13 CCR 1968.2, EPA 40 CFR
86.1806) và quy định EOBD của châu Âu áp dụng cho xe được chứng nhận tại các thị trường đó; chúng không mặc nhiên mô tả
mọi xe bán tại Việt Nam [C11]. Video phải nói rõ: kiểm tra theo tài liệu của hãng cho đúng thị trường, đời xe và động cơ.
Không trích giá trị số nào khi chưa có tài liệu hãng cho xe cụ thể.

## Cartek 2 features used (Tính năng Cartek 2)

<!-- Chỉ dùng tính năng có status "verified" trong data/reference/cartek-2-feature-register.yaml. -->
None. Feature register đang trống; không có claim `cartek-feature`. Nếu kịch bản muốn quay Cartek 2 đọc freeze frame
hay dữ liệu trực tiếp, cần product team xác nhận tính năng trong register trước.

## Safety notes (An toàn)

- **MIL nhấp nháy:** cần cảnh báo bằng lời rằng tiếp tục chạy xe khi bỏ máy nặng có thể làm bộ xúc tác quá nhiệt và hư hỏng; giảm tải và kiểm tra sớm [C07].
- **Hệ thống nhiên liệu (`fuel-system`):** đo áp suất nhiên liệu hoặc kiểm tra kim phun có nguy cơ phun xăng và cháy. Chỉ thực hiện theo quy trình xả áp của hãng, có bình chữa cháy, không có nguồn lửa. Cần cảnh báo bằng lời trong video.
- **Động cơ đang chạy, chi tiết nóng/quay (`hot-or-moving-parts`):** đọc dữ liệu trực tiếp, hoán đổi bô-bin, thử khói và đo áp suất nén liên quan đến động cơ đang chạy hoặc vừa tắt: quạt, dây curoa, ống xả và cổ góp nóng. Cần cảnh báo bằng lời.
- **Đoàn quay:** giữ khoảng cách với quạt và dây curoa khi quay cận cảnh khoang máy, thông gió khi nổ máy trong xưởng.
- Đề xuất `safety.flags: [fuel-system, hot-or-moving-parts]`; technical-fact-checker quyết định cuối cùng. Cần review kỹ thuật bởi người có chuyên môn.

## Open questions (Câu hỏi còn mở)

- **Không đọc được nguồn nào (2026-11-06).** ww2.arb.ca.gov và www.law.cornell.edu bị chặn bởi chính sách mạng của phiên; cần cho phép các host này (hoặc nguồn tương đương) rồi chạy lại nghiên cứu. Cả C01-C11 đều `sources: []`.
- Đầu mối tìm được qua tìm kiếm, **chưa đọc, không được trích dẫn**:
  - CARB, 13 CCR 1968.2 (bản sạch 2006): https://ww2.arb.ca.gov/sites/default/files/barcu/regact/obdii06/19682clean.pdf
  - CARB, 1968.2 (02/2006): https://arb.ca.gov/msprog/obdprog/1968.2_feb072006.pdf
  - 40 CFR 86.099-17 (ấn bản 2004, lưu trữ): https://webarchive.library.unt.edu/eot2008/20081106174501/http://edocket.access.gpo.gov/cfr_2004/julqtr/40cfr86.099-17.htm
  - Motor magazine 04/2007 (bài về misfire Type A/B, trade publication): https://motor.com/magazine/pdfs/042007_02.pdf
  - Cần bản hiện hành của 13 CCR 1968.2 và 40 CFR 86.1806, không dùng bản nháp cũ.
- C01, C02: định nghĩa mã cần SAE J2012 / ISO 15031-6 (trả phí) hoặc tài liệu sửa chữa hãng công khai.
- C03, C04: danh sách thông số freeze frame và phạm vi xóa của Service $04 cần SAE J1979 hoặc văn bản quy định.
- C06: chưa xác nhận chi tiết nhịp nháy và ngoại lệ (ví dụ xe cắt nhiên liệu khi bỏ máy) vì chưa đọc văn bản.
- C09, C10: quy trình và giá trị chuẩn của phép thử cần tài liệu hãng cho xe được dùng để demo; xe demo chưa được chọn.
- C11: phạm vi áp dụng của quy định Mỹ cần đọc điều khoản applicability; quy định OBD áp dụng cho xe tại Việt Nam chưa được nghiên cứu.

## Fact-check log (Nhật ký kiểm chứng)

<!-- technical-fact-checker ghi mỗi quyết định: claim, kết luận, bằng chứng, người kiểm, ngày. -->
| Claim | Decision | Evidence | Checked by | Date |
|---|---|---|---|---|
