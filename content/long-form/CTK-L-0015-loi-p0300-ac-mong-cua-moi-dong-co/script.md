# Long-form script — CTK-L-0015: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

<!-- Kịch bản long-form, khán giả: thợ sửa chữa ô tô (technician, advanced). Mục tiêu 5-8 phút.
     Giọng: thợ nói với thợ, câu ngắn, nói được thành tiếng. Không dùng câu mở bài kiểu "hôm nay chúng ta sẽ cùng nhau...".
     Mọi câu kỹ thuật dẫn claim trong item.yaml. Không có số liệu dựng: phần demo đọc số liệu thật trên xe thử.
     Không nêu tính năng Cartek 2 (sổ tính năng đang trống): đoạn demo dùng "máy chẩn đoán". -->

## Hook candidates (Các phương án hook)

1. Máy báo P0300, khách hỏi: thay bugi luôn hả anh? Khoan. Mã này chỉ nói máy bỏ máy, không nói vì sao.
2. Bốn bugi mới, bốn bô-bin mới, một tuần sau P0300 quay lại. Tiền khách mất, lỗi vẫn còn. Sai ở bước nào?
3. Xóa lỗi là đèn tắt. Nhưng anh em vừa xóa luôn thứ quý nhất để bắt bệnh. Đó là gì?

## Selected hook (Hook được chọn)

- **HOOK:** Phương án 1, viết lại cho tự nhiên: "Máy báo P0300. Khách đứng cạnh hỏi: thay bugi luôn hả anh? Khoan đã."
- **RATIONALE:** Đúng tình huống thợ gặp mỗi ngày (nỗi đau "xử lý sự cố phức tạp", 'Khán giả'!C4). Câu hỏi của khách mở ra vòng mở "vậy làm gì trước", được trả lời ở S06. Phương án 2 hấp dẫn nhưng ngầm khẳng định một tình huống chưa có nguồn; phương án 3 hay nhưng đẩy trọng tâm sang chuyện xóa mã.

## Outline (Dàn ý)

1. Hook: P0300 không nói nguyên nhân (C01)
2. Lộ trình video: đọc mã, đọc freeze frame, khoanh vùng, thử xác nhận
3. P0300 và P0301 đến P0312 khác nhau ở đâu (C01, C02)
4. Đọc và ghi freeze frame trước khi đụng vào bất cứ thứ gì (C03, C04, C05)
5. Demo trên xe thử: đọc freeze frame thật (C03)
6. Bốn nhóm nguyên nhân và phép thử xác nhận từng nhóm (C08, C09, C10)
7. Ba cái sai hay gặp: thay bugi ngay, đoán xi-lanh từ P0300, xóa mã trước (C01, C02, C04, C05, C08)
8. Sửa xong, chạy thử lại đúng điều kiện freeze frame (C03, C04, C05)
9. Xóa mã, mã permanent và đèn check engine nhấp nháy (C05, C06, C07, C12)
10. Tóm tắt và lưu ý thị trường Việt Nam (C08, C11)
11. Kêu gọi hành động

## Script (Kịch bản chi tiết)

### S01 — Hook

- **TYPE:** hook
- **VO:** Máy báo P0300. Khách đứng cạnh hỏi: thay bugi luôn hả anh? Khoan đã. P0300 chỉ nói một điều: ECU thấy động cơ đang bỏ máy, ngẫu nhiên hoặc ở nhiều xi-lanh. Nó không nói vì sao.
- **VISUAL:** Cận màn hình máy chẩn đoán hiện P0300; cắt nhanh sang khoang máy đang rung nhẹ, quay từ khoảng cách an toàn.
- **ON-SCREEN:** P0300 = có bỏ máy. Vì sao? Chưa biết.
- **CLAIMS:** C01

### S02 — Lộ trình

- **TYPE:** intro
- **VO:** Thay bừa thì tốn tiền khách mà lỗi vẫn có thể quay lại. Nên video này đi đúng trình tự làm ngoài xưởng: đọc mã, đọc freeze frame, khoanh vùng nhóm nguyên nhân, thử cho ra rồi mới thay đồ. Cuối video có phần xóa mã và đèn check engine nhấp nháy. Nói trước luôn: xóa mã không sửa được nguyên nhân. Phần đó anh em đừng bỏ qua.
- **VISUAL:** Kỹ thuật viên cắm máy chẩn đoán vào cổng OBD2 dưới táp-lô; bốn bước hiện lần lượt.
- **ON-SCREEN:** Đọc mã → Freeze frame → Khoanh vùng → Thử xác nhận
- **CLAIMS:** C05

### S03 — P0300 và P0301 đến P0312

- **TYPE:** body
- **VO:** Nói kỹ hơn chút. P0300 nghĩa là ECU phát hiện bỏ máy ngẫu nhiên, hoặc bỏ máy ở nhiều xi-lanh. Còn P0301 đến P0312 thì chỉ đích danh: hai số cuối là số thứ tự xi-lanh, P0301 là máy số một. Vậy nên nếu xe chỉ báo P0300, đừng vội đoán xi-lanh nào. Cái mã chỉ là triệu chứng, chưa phải bệnh.
- **VISUAL:** Đồ họa động cơ bốn xi-lanh; P0301 đến P0304 gắn vào từng xi-lanh, P0300 phủ lên cả khối.
- **ON-SCREEN:** P0300: nhiều xi-lanh / ngẫu nhiên · P0301 = xi-lanh 1
- **B-ROLL:** Animation đánh số xi-lanh.
- **CLAIMS:** C01, C02

### S04 — Freeze frame trước đã

- **TYPE:** body
- **VO:** Trước khi làm gì, đọc freeze frame. Đây là bản ghi điều kiện ngay lúc ECU bắt lỗi. Trong đó có mã nào gây ra bản ghi, rồi tải động cơ, nhiệt độ nước làm mát, vòng tua, tốc độ xe. Xe nào có trang bị thì có thêm trạng thái hệ thống nhiên liệu, fuel trim, áp suất đường ống nạp, lưu lượng khí nạp. Mỗi ô là một manh mối. Nhiệt độ nước cho biết lúc đó máy còn nguội hay đã nóng. Tải và vòng tua cho biết máy đang chạy nhẹ hay đang gánh nặng. Tốc độ xe cho biết xe đứng yên hay đang chạy. Chụp màn hình lại, ghi vào phiếu sửa chữa. Vì chỉ một lệnh xóa mã lỗi là mấy dữ liệu này mất hết, mất luôn trạng thái readiness. Xóa không sửa được gì, chỉ xóa bằng chứng.
- **VISUAL:** Màn hình freeze frame trên máy chẩn đoán; tay kỹ thuật viên chụp ảnh màn hình và ghi phiếu.
- **ON-SCREEN:** Đọc và lưu freeze frame TRƯỚC khi xóa
- **CLAIMS:** C03, C04, C05

### S05 — Demo trên xe thử

- **TYPE:** demo
- **VO:** Đây là freeze frame của xe thử. Anh em nhìn ba thứ trước: lỗi bắt ở vòng tua nào, tải cao hay thấp, máy nóng hay còn nguội. Ba con số này cho biết bỏ máy xảy ra trong điều kiện nào, để lát nữa thử lại đúng điều kiện đó chứ không thử mò.
- **VISUAL:** Quay màn hình máy chẩn đoán (trung tính, không nêu tên thiết bị) trên xe thử có P0300 thật; đọc đúng số liệu trên màn hình, không dựng số liệu. Khoanh tròn vòng tua, tải, nhiệt độ nước làm mát.
- **ON-SCREEN:** Vòng tua · Tải · Nhiệt độ nước làm mát
- **SAFETY:** Khi nổ máy để đọc dữ liệu, tránh xa quạt và dây curoa, làm trong chỗ thông thoáng.
- **CLAIMS:** C03
- **DEMO-SECONDS:** 15

### S06 — Bốn nhóm, mỗi nhóm một phép thử

- **TYPE:** body
- **VO:** Giờ mới khoanh vùng. Nguyên nhân bỏ máy nằm trong bốn nhóm: đánh lửa, nhiên liệu, rò khí nạp, và cơ khí. Mỗi nhóm có phép thử riêng để xác nhận. Đánh lửa: kiểm tra bô-bin, bugi theo quy trình của hãng; có thể hoán đổi bô-bin giữa hai máy xem bỏ máy có chạy theo không. Nhiên liệu: đo áp suất nhiên liệu, kiểm tra kim phun, theo thông số của hãng cho đúng xe. Rò khí nạp: thử khói, đối chiếu với fuel trim. Cơ khí: đo áp suất nén, hoặc thử độ lọt khí. Thử ra nhóm nào thì thay đồ nhóm đó.
- **VISUAL:** Sơ đồ cây bốn nhánh; mỗi nhánh hiện tên phép thử. Cảnh minh họa ngắn từng phép thử trên xe thử.
- **ON-SCREEN:** Đánh lửa · Nhiên liệu · Rò khí nạp · Cơ khí → thử trước, thay sau
- **B-ROLL:** Hoán đổi bô-bin; đồng hồ đo áp suất nhiên liệu; máy thử khói; đồng hồ đo áp suất nén.
- **SAFETY:** Đo áp suất nhiên liệu là đụng vào hệ thống xăng có áp: xả áp đúng quy trình của hãng, để sẵn bình chữa cháy, không có lửa gần. Thử khi động cơ đang chạy thì giữ tay và dây đo tránh xa quạt, dây curoa.
- **CLAIMS:** C08, C09, C10

### S07 — Ba cái sai hay gặp

- **TYPE:** body
- **VO:** Giờ nói mấy cái sai hay gặp ngoài xưởng. Cái thứ nhất: thấy P0300 là thay bugi. Bugi có thể đúng, mà cũng có thể không. Mã không nói nguyên nhân, chưa thử thì chưa biết. Cái thứ hai: đoán xi-lanh từ P0300. P0300 không chỉ đích danh máy nào. Muốn biết máy nào thì phải thử, hoặc xem xe có báo thêm mã từ P0301 trở lên không. Cái thứ ba: xóa mã trước cho chắc, rồi chạy thử xem có ra lại không. Làm vậy là mất freeze frame, mất readiness. Mà nguyên nhân còn thì lỗi sẽ sáng lại. Thiệt hai lần.
- **VISUAL:** Ba thẻ lần lượt bật lên, mỗi thẻ một cái sai, gạch chéo đỏ khi VO nói lý do. Cảnh minh họa: hộp bugi mới trên bàn, màn hình máy chẩn đoán chỉ có P0300, ngón tay dừng trên nút xóa mã.
- **ON-SCREEN:** ✗ Thay bugi ngay · ✗ Đoán xi-lanh từ P0300 · ✗ Xóa mã trước
- **CLAIMS:** C01, C02, C04, C05, C08

### S08 — Sửa xong, thử lại cho chắc

- **TYPE:** body
- **VO:** Thay xong rồi, chưa giao xe vội. Xóa mã xong thì readiness về lại từ đầu, ECU phải tự kiểm tra lại. Mở lại freeze frame đã chụp lúc đầu. Lỗi bắt ở vòng tua nào, tải nào, máy nóng hay nguội, thì chạy thử lại đúng điều kiện đó. Nguyên nhân còn thì ECU bắt lại, mã sẽ báo lại. Đừng chạy một vòng quanh xưởng rồi kết luận vội.
- **VISUAL:** Ảnh chụp freeze frame trên điện thoại đặt cạnh màn hình dữ liệu trực tiếp; kỹ thuật viên so từng ô vòng tua, tải, nhiệt độ nước làm mát trước khi chạy thử.
- **ON-SCREEN:** Chạy thử lại ĐÚNG điều kiện trong freeze frame
- **SAFETY:** Chạy thử trên đường thì một người lái, một người theo dõi máy chẩn đoán. Không vừa lái vừa nhìn màn hình.
- **CLAIMS:** C03, C04, C05

### S09 — Xóa mã và đèn nhấp nháy

- **TYPE:** safety
- **VO:** Còn xóa mã thì sao? Xóa mã lỗi chỉ xóa bản ghi. Nguyên nhân còn thì ECU bắt lại, mã quay lại. Xe đời mới theo chuẩn OBD II của Mỹ còn có mã permanent: máy chẩn đoán không xóa được, ngắt điện cũng không, ECU tự xóa khi nó xác nhận lỗi đã hết. Một chuyện nữa: trên xe theo quy định này, đèn check engine nhấp nháy nghĩa là bỏ máy đủ nặng để làm hỏng bộ xúc tác. Có xe được thiết kế chỉ sáng đứng chứ không nháy, nên đèn sáng đứng chưa chắc là nhẹ.
- **VISUAL:** Đèn check engine trên táp-lô: sáng đứng, rồi nhấp nháy; đồ họa bộ xúc tác.
- **ON-SCREEN:** Xóa mã lỗi ≠ sửa lỗi · Đèn nháy = bỏ máy nặng
- **SAFETY:** Đèn check engine nhấp nháy thì giảm tải, hạn chế chạy và đưa xe đi kiểm tra sớm.
- **CLAIMS:** C05, C06, C07, C12

### S10 — Tóm lại

- **TYPE:** recap
- **VO:** Tóm lại: P0300 là triệu chứng, không phải bệnh. Đọc mã, lưu freeze frame, khoanh vùng, thử từng nhóm, rồi mới thay đồ. Và kiểm tra theo tài liệu của hãng cho đúng thị trường, đời xe và động cơ, vì quy định OBD II của Mỹ không tự động áp cho xe bán ở Việt Nam.
- **VISUAL:** Bốn bước dạng danh sách, đánh dấu lần lượt.
- **ON-SCREEN:** 1. Đọc mã 2. Lưu freeze frame 3. Khoanh vùng 4. Thử rồi mới thay
- **CLAIMS:** C03, C08, C11

### S11 — Kêu gọi hành động

- **TYPE:** cta
- **VO:** Anh em có ca P0300 nào khó thì để lại comment, kèm đời xe và freeze frame, mình xem cùng. Thấy video có ích thì bấm like, subscribe, bật chuông để không lỡ video sau. Cartek - Check your car.
- **VISUAL:** Màn hình kết thúc, dòng thương hiệu.
- **ON-SCREEN:** Cartek - Check your car
- **CLAIMS:**

## Retention notes (Giữ chân người xem)

- Vòng mở ở S01 ("thay bugi luôn hả anh?") được trả lời ở S06: thử trước, thay sau.
- S02 hứa phần xóa mã và đèn nháy ở cuối, giữ người xem tới S09.
- Đổi nhịp hình: đồ họa (S03), quay màn hình thật (S05), sơ đồ cây và cảnh thử (S06).
- S07 đổi nhịp bằng danh sách "ba cái sai": thợ tự soi mình, dễ giữ người xem qua giữa video.
- S08 nối lại freeze frame ở S04/S05: thứ đã chụp ở đầu được dùng lại ở cuối.
- S09 có điểm bất ngờ: đèn sáng đứng chưa chắc là nhẹ.
