# Long-form script — DEMO-P0300-A: Cartek Long — P0300 không phải danh sách linh kiện cần thay

<!-- Kịch bản demo (VIDEO A "Cartek Long", 16:9, mục tiêu 03:00). Không phải content item chính thức:
     dùng chung kiến thức và sổ claim của CTK-L-0015 (content/long-form/CTK-L-0015-loi-p0300-ac-mong-cua-moi-dong-co/item.yaml),
     cấu trúc khác. Mọi claim trong file này đang ở trạng thái "unverified" trong item.yaml: demo này KHÔNG được
     phát hành khi chưa qua technical-fact-checker.
     Khán giả hỗn hợp (người dùng Cartek, thợ garage, chủ xe): xưng "các bạn", câu ngắn, chính xác kỹ thuật.
     Mốc thời gian trong tiêu đề đoạn là kế hoạch dựng; thời lượng thật đo ở timing.json.
     Cách đọc mã/từ viết tắt: pronunciation.md (một cách đọc cho cả video). Cùng quy ước máy đọc với
     templates/long-form-script.md (scripts/ctk/mdparse.parse_script đọc được file này). -->

## Hook candidates (Các phương án hook)

1. Máy quét báo P0300. Vậy có phải thay bugi ngay không? Khoan đã!
2. Bốn bugi mới, một tuần sau P0300 quay lại. Sai ở bước nào?
3. Xóa mã là đèn tắt. Nhưng các bạn vừa xóa luôn bằng chứng để tìm bệnh.

## Selected hook (Hook được chọn)

- **HOOK:** Phương án 1: "Máy quét báo P0300. Vậy có phải thay bugi ngay không? Khoan đã!"
- **RATIONALE:** Câu hỏi đúng thứ mọi nhóm khán giả đều từng nghĩ (chủ xe hỏi, thợ bị hỏi). "Khoan đã" mở vòng mở được trả ở S05 (vì sao chưa thay bugi) và S06 (quy trình). Phương án 2 ngầm kể một tình huống không có nguồn; phương án 3 đẩy trọng tâm sang chuyện xóa mã.

## Outline (Dàn ý)

1. 00:00–00:07 Hook: máy quét báo P0300, có thay bugi ngay không? (C01)
2. 00:07–00:25 Pattern interrupt: mã lỗi không phải nguyên nhân (C01, C05)
3. 00:25–00:50 ECU phát hiện bỏ máy thế nào: mã, freeze frame, đèn nhấp nháy + câu an toàn (C01, C03, C05, C06, C07)
4. 00:50–01:15 P0300 và P0301: khác nhau ở đâu, vì sao cùng bệnh mà mã khác (C01, C02, C13)
5. 01:15–01:45 Vì sao chưa thay bugi: bốn nhóm nguyên nhân, mỗi nhóm một phép thử (C05, C08, C09, C10)
6. 01:45–02:15 Quy trình năm bước (C03, C04, C08, C09, C10, C11)
7. 02:15–02:40 Tình huống minh họa: thử trước, thay sau (C03, C05, C08, C09)
8. 02:40–02:52 Tóm lại (C01, C04, C08)
9. 02:52–03:00 Kêu gọi hành động

## Script (Kịch bản chi tiết)

### S01 — Hook (00:00–00:07)

- **TYPE:** hook
- **VO:** Máy quét báo P0300. Vậy có phải thay bugi ngay không? Khoan đã!
- **VISUAL:** Cận màn hình máy chẩn đoán hiện P0300 (màn hình thật hoặc đồ họa giao diện trung tính, không nêu tên thiết bị). Cắt sang bàn tay cầm bugi mới dừng lại giữa không trung.
- **ON-SCREEN:** P0300 → thay bugi?
- **B-ROLL:** Đèn Check Engine sáng trên táp-lô.
- **NOTES:** Đọc "P0300" là "pê không ba trăm" (pronunciation.md). Nhịp: hai câu đầu đều, "Khoan đã!" dừng hẳn 0,5 giây rồi mới sang S02.
- **CLAIMS:** C01

### S02 — Mã lỗi không phải nguyên nhân (00:07–00:25)

- **TYPE:** intro
- **VO:** Mã lỗi không phải là nguyên nhân. P0300 chỉ nói một điều: ECU phát hiện động cơ bỏ máy, ngẫu nhiên hoặc ở nhiều xi-lanh. Vì sao bỏ máy? Mã này không nói. Thay đồ trước khi biết nguyên nhân, lỗi có thể quay lại.
- **VISUAL:** Chữ lớn "MÃ LỖI ≠ NGUYÊN NHÂN" dựng kiểu kinetic typography trên nền tối; P0300 tách ra khỏi dòng chữ "nguyên nhân".
- **ON-SCREEN:** Mã lỗi ≠ nguyên nhân
- **B-ROLL:** Khoang máy đang nổ, quay từ khoảng cách an toàn.
- **NOTES:** "ECU" đọc "i-xi-u". Câu "Vì sao bỏ máy?" lên giọng hỏi, "Mã này không nói." hạ giọng, chậm.
- **CLAIMS:** C01, C05

### S03 — ECU phát hiện bỏ máy thế nào (00:25–00:50)

- **TYPE:** body
- **VO:** ECU theo dõi động cơ để bắt bỏ máy. Khi phát hiện, nó ghi mã lỗi và lưu freeze frame, tức dữ liệu đóng băng: tải, nhiệt độ nước, vòng tua, tốc độ xe lúc đó.
- **VISUAL:** Đồ họa: khối ECU ở giữa, mũi tên vào từ động cơ, mũi tên ra là "mã lỗi" và "freeze frame"; bảng freeze frame hiện bốn dòng (không có số liệu, chỉ tên thông số). Đèn Check Engine trên táp-lô: sáng đứng rồi nhấp nháy.
- **ON-SCREEN:** Phát hiện bỏ máy → mã lỗi + freeze frame
- **B-ROLL:** Táp-lô với đèn Check Engine.
- **SAFETY:** Trên xe theo quy định OBD-II của Mỹ, đèn Check Engine nhấp nháy là bỏ máy nặng, có thể làm hỏng bộ xúc tác. Khi đó các bạn giảm tải, hạn chế chạy và kiểm tra sớm.
- **NOTES:** "freeze frame" đọc "phờ-ri phrêm"; "OBD-II" đọc "ô-bê-đê hai" (đang gọi tên chuẩn); "Check Engine" đọc "chéc en-gin". "Quy định OBD-II của Mỹ" = 13 CCR 1968.2 (CARB) mà EPA áp cho xe đời 2017+ (C06, C11); không mặc nhiên áp dụng cho xe bán tại Việt Nam. Không nói "đèn sáng đứng thì nhẹ" (C06). Đồ họa không hiện con số freeze frame nào (không bịa số liệu).
- **CLAIMS:** C01, C03, C05, C06, C07

### S04 — P0300 và P0301 (00:50–01:15)

- **TYPE:** body
- **VO:** P0300: bỏ máy ngẫu nhiên hoặc nhiều xi-lanh. P0301 đến P0312: bỏ máy ở một xi-lanh cụ thể, hai số cuối là số xi-lanh. Nhưng cùng một bệnh, xe này báo P0300, xe kia báo P0301, tùy chiến lược hãng. Thứ tự xi-lanh thì tra tài liệu hãng. Nên đừng vội đoán xi-lanh.
- **VISUAL:** So sánh động hai cột: trái "P0300" phủ lên cả khối động cơ bốn xi-lanh, phải "P0301" gắn vào xi-lanh số một. Khung nhỏ "thứ tự xi-lanh: theo tài liệu hãng".
- **ON-SCREEN:** P0300: nhiều xi-lanh / ngẫu nhiên · P0301: xi-lanh 1
- **B-ROLL:** Animation động cơ bốn xi-lanh.
- **NOTES:** "P0301" đọc "pê không ba trăm lẻ một"; "P0312" đọc "pê không ba trăm mười hai". Không nói ngưỡng 90% để giữ nhịp (chi tiết nằm trong C13, dành cho bản dài CTK-L-0015).
- **CLAIMS:** C01, C02, C13

### S05 — Vì sao chưa thay bugi ngay (01:15–01:45)

- **TYPE:** body
- **VO:** Bugi chỉ là một ứng viên. Nguyên nhân khả dĩ của P0300 nằm trong bốn nhóm: đánh lửa, như bugi và bô-bin; nhiên liệu, như áp suất và kim phun; rò rỉ khí nạp hay chân không; và cơ khí, như độ nén. Mỗi nhóm có phép thử xác nhận riêng, theo quy trình của hãng. Thay bugi khi lỗi ở nhóm khác, tiền mất mà mã vẫn có thể quay lại.
- **VISUAL:** Bốn thẻ hiện lần lượt theo lời thoại (mask reveal từ trái sang): Đánh lửa, Nhiên liệu, Khí nạp, Cơ khí; dưới mỗi thẻ một dòng "phép thử xác nhận". Thẻ Đánh lửa chứa bugi và bô-bin, bugi chỉ là một ô nhỏ.
- **ON-SCREEN:** Đánh lửa · Nhiên liệu · Khí nạp · Cơ khí → thử trước, thay sau
- **B-ROLL:** Cận bugi; bô-bin; kim phun; đồng hồ đo áp suất nén (không quay rõ mặt số).
- **NOTES:** "bô-bin" là cách viết dùng cho cả video (glossary brand-voice; không dùng "mô-bin"). Không nói nhóm nào "thường gặp" (chưa có nguồn, C08). Không đọc giá trị áp suất hay độ nén nào.
- **CLAIMS:** C05, C08, C09, C10

### S06 — Quy trình năm bước (01:45–02:15)

- **TYPE:** body
- **VO:** Năm bước. Một, đọc và ghi lại mã, đừng xóa vội, vì xóa là mất freeze frame và readiness. Hai, kiểm tra triệu chứng và dữ liệu liên quan, nhất là freeze frame, xem lỗi xảy ra ở vòng tua nào, tải nào, máy nóng hay nguội. Ba, thu thập thông tin xe, gồm hãng, đời xe, động cơ, thị trường. Bốn, kiểm tra theo quy trình của hãng. Năm, xác nhận nguyên nhân rồi mới sửa.
- **VISUAL:** Danh sách năm bước, mỗi bước hiện kèm dấu tích khi lời thoại nhắc tới; bước Một có ui-callout quanh nút "Xóa mã" với dấu gạch chéo; bước Hai có khung freeze frame (tên thông số, không số liệu).
- **ON-SCREEN:** 1. Đọc và ghi mã · 2. Triệu chứng + freeze frame · 3. Thông tin xe · 4. Quy trình hãng · 5. Xác nhận rồi mới sửa
- **B-ROLL:** Tay cắm máy chẩn đoán vào cổng OBD2; chụp màn hình máy chẩn đoán bằng điện thoại; sổ ghi phiếu.
- **NOTES:** "readiness" đọc "re-đi-nét"; "OBD2" (cổng) đọc "ô-bê-đê hai". Nhịp đọc: dừng ngắn sau mỗi số thứ tự. Bước Bốn cố ý không kể tên phép thử (đã nói ở S05) để giữ 30 giây.
- **CLAIMS:** C03, C04, C05, C09, C10, C11

### S07 — Tình huống minh họa (02:15–02:40)

- **TYPE:** body
- **VO:** Tình huống minh họa, không phải ca thật. Xe báo P0300, freeze frame ghi lỗi xảy ra khi máy còn nguội. Thợ không thay bugi ngay, mà hoán đổi bô-bin giữa hai xi-lanh rồi chạy lại đúng điều kiện đó. Bỏ máy đi theo bô-bin thì nghi bô-bin. Không thì sang nhóm khác. Thử trước, thay sau.
- **VISUAL:** Nhãn góc trên "Tình huống minh họa" giữ suốt đoạn. Đồ họa đơn giản: hai xi-lanh, hai bô-bin đổi chỗ (mũi tên vòng), biểu tượng bỏ máy đi theo hoặc không. Không có số liệu freeze frame, chỉ nhãn "máy còn nguội".
- **ON-SCREEN:** Tình huống minh họa · Bỏ máy đi theo bô-bin? → Có: nghi bô-bin · Không: nhóm khác
- **B-ROLL:** Tay thợ tháo bô-bin (quay thật, động cơ đã tắt).
- **SAFETY:** Tháo lắp bô-bin khi máy đã tắt; máy chạy thì tránh xa quạt và dây curoa.
- **NOTES:** Nhãn "Tình huống minh họa" là bắt buộc: không có xe, số liệu hay ca sửa chữa thật nào phía sau. Không nói "phép thử này hay dùng" (C09).
- **CLAIMS:** C03, C05, C08, C09

### S08 — Tóm lại (02:40–02:52)

- **TYPE:** recap
- **VO:** Tóm lại, P0300 là điểm bắt đầu để tìm nguyên nhân, không phải danh sách linh kiện cần thay. Đọc mã, giữ freeze frame, hiểu xe, kiểm tra theo hãng, xác nhận rồi mới sửa.
- **VISUAL:** Câu chốt hiện lớn giữa khung (kinetic typography), rồi thu nhỏ lên trên; năm bước dạng dấu tích hiện nhanh phía dưới.
- **ON-SCREEN:** P0300 là điểm bắt đầu, không phải danh sách linh kiện cần thay
- **NOTES:** Đọc câu chốt chậm hơn phần còn lại.
- **CLAIMS:** C01, C04, C08

### S09 — Kêu gọi hành động (02:52–03:00)

- **TYPE:** cta
- **VO:** Có ca P0300 khó, các bạn để lại comment, bấm like và subscribe. Cartek - Check your car.
- **VISUAL:** Màn hình kết thúc có logo Cartek (branded ending), vùng bên phải để trống cho end-screen YouTube.
- **ON-SCREEN:** Cartek - Check your car
- **NOTES:** CTA rút gọn từ câu CTA của sheet ('Content Direction'!B4) để vừa 8 giây của demo (đo bằng TTS: câu đầy đủ cần khoảng 12 giây); bản phát hành dùng câu đầy đủ. "like", "subscribe", "comment", "Check your car" đọc tiếng Anh thông dụng (pronunciation.md).
- **CLAIMS:**

## Retention notes (Giữ chân người xem)

- Vòng mở S01 ("có thay bugi ngay không?") được trả ở S05 (bugi chỉ là một ứng viên) và S06 (quy trình).
- S02 cắt nhịp bằng chữ lớn "Mã lỗi ≠ nguyên nhân" trong 18 giây đầu, trước khi vào phần giải thích.
- S04 có điểm bất ngờ: cùng bệnh, xe này báo P0300, xe kia báo P0301.
- Đổi nhịp hình: kinetic typography (S02, S08), đồ họa hệ thống (S03), so sánh động (S04), thẻ mask reveal (S05), danh sách tick (S06), minh họa có nhãn (S07).
- S07 là chỗ duy nhất "kể chuyện"; nhãn minh họa giữ sự trung thực của thương hiệu.
