# Storyboard and shot list — CTK-L-0015: Lỗi P0300 - Ác Mộng của Mọi Động Cơ?

<!-- Danh sách cảnh quay. Mỗi dòng là một shot; cột Segment trỏ tới đoạn Sxx trong script.md.
     Export đưa bảng này vào gói sản xuất (storyboard_shots) và cột Effects / Text style vào visual_style.
     - Effects: các ID hiệu ứng trong config/visual-style.yaml, cách nhau bằng dấu phẩy
       (vd. "code-popup, sfx-ui-beep"; chuyển cảnh mặc định: hard-cut). Đoạn có dòng SAFETY
       phải có ít nhất một shot dùng "safety-banner" (G7 cảnh báo nếu thiếu).
     - Text style: các vai chữ trong config/visual-style.yaml -> typography.roles
       (caption, lower_third, callout, dtc_code, live_data_number, end_screen).
     Hướng dẫn đọc được: strategy/visual-identity.md. Không dùng ký tự "|" trong ô.
     Không lưu video gốc trong Git: ghi đường dẫn kho lưu trữ vào item.yaml -> production.footage_links.
     Giây mỗi đoạn khớp bảng "python3 scripts/qc_content.py runtime CTK-L-0015" (07:41, 461 s):
     S01 14 · S02 25 · S03 55 · S04 54 · S05 67 · S06 85 · S07 36 · S08 30 · S09 49 · S10 32 · S11 13.
     Xe thử: vehicle.scope = generic, chưa chốt hãng/đời xe. Mọi số liệu trên màn hình là số thật đọc lúc quay. -->

## Shot list

| Shot | Segment | Framing | Description | Vehicle / location | Assets | Seconds | Effects | Text style |
|---|---|---|---|---|---|---|---|---|
| 1 | S01 | Cận màn hình | Màn hình máy chẩn đoán hiện P0300 trong danh sách mã; code-popup ghi "P0300" và nghĩa tiếng Việt bên dưới | Xe thử có P0300 thật (chưa chốt đời xe), trong xưởng | Máy chẩn đoán đọc được freeze frame; đồ họa code-popup | 7 | hard-cut, code-popup, sfx-ui-beep | dtc_code, caption |
| 2 | S01 | Trung cảnh | Khoang máy đang nổ, rung nhẹ, quay từ khoảng cách an toàn; người dẫn vào hình nói "Nó không nói vì sao" | Xe thử, khoang máy, xưởng | Camera chính, đèn LED | 7 | hard-cut, zoom-punch | callout |
| 3 | S02 | Trung cảnh | Người dẫn đứng cạnh xe nói với máy; lower third tên và vai trò (tên do người dẫn xác nhận) | Xưởng (chưa chốt địa điểm) | Lower third | 8 | hard-cut, lower-third, sfx-whoosh | lower_third |
| 4 | S02 | Cận tay | Tay cắm máy chẩn đoán vào cổng OBD2 dưới táp-lô; mũi tên chỉ cổng | Xe thử, ghế lái | Máy chẩn đoán | 6 | hard-cut, highlight-arrow | callout |
| 5 | S02 | Đồ họa toàn khung | Bốn bước hiện lần lượt "Đọc mã → Freeze frame → Khoanh vùng → Thử xác nhận"; dòng cuối "Xóa mã lỗi chỉ xóa bản ghi" | Đồ họa, không quay xe | Đồ họa bốn bước | 11 | hard-cut, checklist-tick, sfx-whoosh | callout |
| 6 | S03 | Đồ họa toàn khung | Động cơ bốn xi-lanh; "P0300" phủ lên cả khối với nghĩa "bỏ máy ngẫu nhiên / nhiều xi-lanh" | Đồ họa | Animation động cơ bốn xi-lanh | 12 | soft-dissolve, code-popup, sfx-ui-beep | dtc_code, caption |
| 7 | S03 | Đồ họa toàn khung | "P0301" đến "P0304" gắn vào từng xi-lanh theo lời thoại | Đồ họa | Animation đánh số xi-lanh | 12 | hard-cut, code-popup, sfx-whoosh | dtc_code, callout |
| 8 | S03 | Đồ họa toàn khung | Hai xe cạnh nhau, cùng bệnh: xe này báo "P0300", xe kia báo "P0301"; khung "thứ tự xi-lanh: theo sơ đồ hãng"; dòng phụ "xe theo quy định OBD-II California từ đời 2005" khi lời thoại nêu điều kiện 90% | Đồ họa | Animation hai xe | 17 | hard-cut, highlight-arrow | dtc_code, callout |
| 9 | S03 | Trung cảnh | Người dẫn chốt "Cái mã chỉ là triệu chứng, chưa phải bệnh" | Xưởng | Camera chính | 14 | hard-cut, zoom-punch | callout |
| 10 | S04 | Cận màn hình | Màn hình freeze frame trên máy chẩn đoán; khoanh từng dòng khi lời thoại nhắc: mã gây bản ghi, tải, nhiệt độ nước làm mát, vòng tua, tốc độ xe | Xe thử, máy đang nổ hoặc vừa tắt theo yêu cầu của máy chẩn đoán | Máy chẩn đoán | 21 | hard-cut, highlight-circle, sfx-ui-beep | live_data_number, caption |
| 11 | S04 | Cận màn hình | Khoanh các dòng "xe nào có trang bị": trạng thái hệ thống nhiên liệu, fuel trim, áp suất đường ống nạp, lưu lượng khí nạp; chỉ khoanh dòng máy thật đang hiện | Xe thử | Máy chẩn đoán | 15 | hard-cut, highlight-circle | live_data_number |
| 12 | S04 | Cận tay | Chụp ảnh màn hình bằng điện thoại rồi ghi phiếu; đóng băng khung hình đúng lúc bấm chụp | Bàn ghi phiếu cạnh xe thử | Phiếu công việc, điện thoại để chụp màn hình | 10 | hard-cut, freeze-frame-snapshot | callout |
| 13 | S04 | Đồ họa toàn khung | Danh sách bị mất khi bấm xóa: mã chờ (pending), mã xác nhận (confirmed), freeze frame, trạng thái sẵn sàng (readiness); callout "Đọc và lưu freeze frame trước khi xóa" (viết thường, nhấn bằng kiểu callout, không viết hoa) | Đồ họa | Đồ họa danh sách | 8 | hard-cut, sfx-low-thud | callout |
| 14 | S05 | Cận màn hình | Freeze frame thật của xe thử, quay liên tục không cắt; không nêu tên thiết bị; không dựng số; đóng băng khung khi người dẫn nói "Đây là freeze frame của xe thử" | Xe thử có P0300 thật, máy nổ, chỗ thông thoáng trong xưởng | Máy chẩn đoán | 25 | hard-cut, freeze-frame-snapshot, safety-banner | live_data_number, caption |
| 15 | S05 | Cận màn hình | Khoanh tròn vòng tua, tải, nhiệt độ nước làm mát theo đúng thứ tự lời thoại; rồi dòng fuel trim và trạng thái hệ thống nhiên liệu nếu xe có | Xe thử | Máy chẩn đoán | 20 | hard-cut, highlight-circle, sfx-ui-beep, safety-banner | live_data_number |
| 16 | S05 | Cận tay | Ghi phiếu: mã lỗi, từng dòng freeze frame, danh sách mã còn trên máy (pending, confirmed) | Bàn ghi phiếu cạnh xe thử | Phiếu công việc, bút | 22 | hard-cut, safety-banner | callout |
| 17 | S06 | Đồ họa toàn khung | Sơ đồ cây bốn nhánh: đánh lửa, nhiên liệu, rò khí nạp, cơ khí; mỗi nhánh hiện tên phép thử và được tick khi lời thoại nhắc | Đồ họa | Đồ họa sơ đồ cây | 13 | soft-dissolve, checklist-tick, sfx-whoosh, safety-banner | callout |
| 18 | S06 | Cận tay | Tháo và đổi chỗ hai bô-bin khi máy tắt; mũi tên chỉ hai bô-bin được hoán đổi; sau đó nổ máy lại | Xe thử, khoang máy | Dụng cụ tháo bô-bin, găng tay | 20 | hard-cut, highlight-arrow, safety-banner | callout |
| 19 | S06 | Trung cảnh | Nối đồng hồ áp suất nhiên liệu theo quy trình hãng; bình chữa cháy để trong khung hình; không quay cận mặt số để không đọc giá trị | Xe thử, khoang máy | Đồng hồ đo áp suất nhiên liệu, bình chữa cháy | 16 | hard-cut, safety-banner | callout |
| 20 | S06 | Trung cảnh | Máy thử khói nối vào đường nạp; cắt sang màn hình máy chẩn đoán đang hiện fuel trim thật | Xe thử, khoang máy | Máy thử khói, máy chẩn đoán | 14 | hard-cut, highlight-arrow, safety-banner | callout, live_data_number |
| 21 | S06 | Cận | Đồng hồ đo áp suất nén lắp vào lỗ bugi; không quay rõ mặt số để không đọc giá trị | Xe thử, khoang máy, máy tắt | Đồng hồ đo áp suất nén | 12 | hard-cut, safety-banner | callout |
| 22 | S06 | Cận tay | Ghi phép thử và kết quả vào phiếu; tick dòng "thử trước, thay sau" | Bàn ghi phiếu | Phiếu công việc | 10 | hard-cut, checklist-tick, sfx-whoosh, safety-banner | callout |
| 23 | S07 | Đồ họa toàn khung | Ba thẻ lần lượt bật lên: "Thay bugi ngay", "Đoán xi-lanh từ P0300", "Xóa mã trước"; mỗi thẻ bị gạch chéo khi lời thoại nói lý do; tiếng trầm một lần cho mỗi thẻ, không chồng lời | Đồ họa | Đồ họa ba thẻ | 12 | hard-cut, sfx-low-thud | callout |
| 24 | S07 | Cận | Hộp bugi mới trên bàn, chưa mở; cắt sang màn hình máy chẩn đoán danh sách mã chỉ có P0300 (mã thật của xe thử, không thêm mã nào) | Bàn dụng cụ cạnh xe thử; xe thử | Hộp bugi mới, máy chẩn đoán | 12 | hard-cut, highlight-circle | callout |
| 25 | S07 | Cận tay | Ngón tay dừng trên nút xóa mã của máy chẩn đoán rồi rút lại, không bấm; callout "Thiệt hai lần" khi lời thoại chốt | Xe thử, ghế lái | Máy chẩn đoán | 12 | hard-cut, zoom-punch | callout |
| 26 | S08 | Cận | Ảnh chụp freeze frame trên điện thoại đặt cạnh màn hình dữ liệu trực tiếp của máy chẩn đoán; đóng băng khung hình khi lời thoại nói "Mở lại freeze frame đã chụp lúc đầu" | Xe thử, máy nổ, trong xưởng | Điện thoại có ảnh chụp từ shot 12, máy chẩn đoán | 15 | hard-cut, freeze-frame-snapshot, safety-banner | live_data_number, callout |
| 27 | S08 | Cận màn hình | Khoanh từng ô vòng tua, tải, nhiệt độ nước làm mát trên màn hình dữ liệu trực tiếp theo lời thoại; băng cảnh báo giữ nguyên câu SAFETY của S08 (một người lái, một người theo dõi) | Xe thử | Máy chẩn đoán | 15 | hard-cut, highlight-circle, safety-banner | live_data_number, callout |
| 28 | S09 | Cận táp-lô | Đèn check engine sáng đứng trên táp-lô xe thử | Xe thử, ghế lái | Camera chính | 10 | soft-dissolve, safety-banner | callout |
| 29 | S09 | Cận màn hình | Mục mã permanent trên máy chẩn đoán; chỉ quay nếu xe thử có mã permanent thật, nếu không thì thay bằng đồ họa chữ "mã permanent" không kèm số liệu | Xe thử | Máy chẩn đoán hoặc đồ họa chữ | 14 | hard-cut, highlight-circle, safety-banner | dtc_code, caption |
| 30 | S09 | Cận táp-lô | Đèn check engine nhấp nháy; quay thật nếu xe thử nháy đèn lúc bỏ máy, nếu không thì đồ họa mô phỏng có nhãn "mô phỏng" | Xe thử hoặc đồ họa | Camera chính hoặc đồ họa đèn | 12 | hard-cut, sfx-low-thud, safety-banner | callout |
| 31 | S09 | Đồ họa toàn khung | Đồ họa bộ xúc tác; callout "Xóa mã lỗi ≠ sửa lỗi · Đèn nháy = bỏ máy nặng"; băng cảnh báo giữ nguyên câu SAFETY của S09 | Đồ họa | Đồ họa bộ xúc tác | 13 | hard-cut, safety-banner | callout |
| 32 | S10 | Đồ họa toàn khung | Bốn bước dạng danh sách, tick lần lượt theo lời thoại | Đồ họa | Đồ họa danh sách bốn bước | 14 | soft-dissolve, checklist-tick, sfx-whoosh | callout |
| 33 | S10 | Trung cảnh | Người dẫn nói phần quy định Mỹ và xe ở Việt Nam; khung "tra tài liệu hãng" hiện ở câu cuối | Xưởng | Camera chính | 18 | hard-cut, zoom-punch | callout |
| 34 | S11 | Đồ họa toàn khung | Màn hình kết thúc: logo và dòng "Cartek - Check your car" bên trái, nửa phải để trống cho end-screen của YouTube | Đồ họa | Logo, nền màn hình kết thúc | 13 | soft-dissolve, sfx-whoosh | end_screen |

## Sound and effects (Âm thanh và hiệu ứng)

<!-- Nhạc nền, SFX và hiệu ứng hình ngoài bảng trên. Quy tắc chung trong config/visual-style.yaml -> sound_rules:
     không âm thanh hù dọa, không còi báo động, SFX không chồng lên lời thoại, nhạc hạ dưới VO. -->

- Nhạc nền: một bản nhạc nền nhẹ, không lời, có giấy phép dùng cho YouTube (tên bản nhạc và giấy phép ghi vào phiếu dựng khi chốt); hạ khoảng -18 LU dưới lời thoại, tắt hẳn dưới các băng cảnh báo an toàn (S05, S06, S08, S09).
- Giữ nguyên tiếng thật của động cơ và của máy chẩn đoán; không lồng thêm tiếng máy để lỗi nghe nặng hơn.
- Hiệu ứng dùng vượt gợi ý max_uses_per_video: none. Số lần dự kiến: soft-dissolve 5 (tối đa 6), zoom-punch 4 (tối đa 6), lower-third 1 (tối đa 4), freeze-frame-snapshot 3 (tối đa 4), sfx-whoosh 7 (tối đa 12), sfx-ui-beep 4 (tối đa 8), sfx-low-thud 3 (tối đa 6: một lần cho mỗi thẻ ở shot 23 tính là ba lần dùng), sfx-ui-click 0.
- safety-banner dùng trong mọi shot của S05, S06, S08, S09 với đúng câu SAFETY trong script.md (không rút gọn); vào bằng sfx-low-thud hoặc im lặng, không có còi.
- zoom-punch không dùng trong S09 (đoạn safety) theo quy tắc never_use của hiệu ứng.
- SFX bắt đầu sau khi từ vừa nói kết thúc hoặc nằm trong khoảng ngắt; không chồng lên lời thoại.

## Typography (Chữ trên hình)

<!-- Font và vai chữ theo config/visual-style.yaml. Chữ tiếng Việt viết dấu chuẩn NFC; mã lỗi ghi đúng như script.md. -->

- Vai chữ dùng: theo thư viện, không lệch. dtc_code (JetBrains Mono 700, 72 px) cho mọi mã lỗi hiện trên hình: shot 1, 6, 7, 8, 29; mã ghi đúng như script.md (P0300, P0301 đến P0304; P0312 không hiện trên hình), đặt cách xa vùng màn hình máy chẩn đoán thật để hai số không chồng nhau. live_data_number (JetBrains Mono 500, 48 px) cho bảng số liệu trong shot 10, 11, 14, 15, 20, 26, 27: chỉ ghi lại đúng giá trị máy chẩn đoán đang hiện lúc quay, không gõ số ví dụ. callout (Be Vietnam Pro 600, 56 px) cho các dòng ON-SCREEN và tiêu đề bước. lower_third (Be Vietnam Pro 700/500) một lần ở shot 3. end_screen (Be Vietnam Pro 600, 40 px) ở shot 34 với dòng "Cartek - Check your car". caption (Be Vietnam Pro 500, 44 px) cho dòng nghĩa tiếng Việt dưới mỗi code-popup.
- Font chính Be Vietnam Pro, dự phòng Inter; font mã JetBrains Mono, dự phòng Roboto Mono (đều OFL). Mọi chữ tiếng Việt gõ dấu NFC; kiểm tra trên điện thoại trước khi khóa.
- Phụ đề: tải lên YouTube dạng file phụ đề tiếng Việt (không burned-in), để lower third ở shot 3 và băng cảnh báo không chồng phụ đề. File phụ đề làm từ lời thoại thu thật, không từ bản nháp; mã và từ viết tắt ghi đúng như script.md (P0300, ECU; "OBD2" cho cổng ở S02, "OBD-II" khi gọi tên chuẩn ở S03, S09, S10 theo brand-voice quy tắc 4); tối đa 2 dòng, mỗi dòng một ý.
- Màu dùng token placeholder của thư viện (background, text, accent_code cho mã và số liệu, accent_safety cho băng cảnh báo) cho tới khi brand team chốt bảng màu.

## Graphics and animation (Đồ họa)

- Code-popup cho P0300 (shot 1, 6) và P0301 đến P0304 (shot 7) với nghĩa tiếng Việt lấy từ claim C01, C02; không hiện mã nào ngoài các mã có trong claim. Shot 6, 7, 8 là animation giải thích, không có màn hình máy chẩn đoán thật trong khung (xe thử chỉ lưu P0300), nên không mâu thuẫn với quy tắc never_use của code-popup (mã trên màn hình thật chỉ ở shot 1 và 24: P0300).
- Animation động cơ bốn xi-lanh có đánh số (shot 6, 7) và khung "thứ tự xi-lanh: theo sơ đồ hãng" (shot 8); hình minh họa chung, không ghi hãng hay đời xe.
- Đồ họa bốn bước "Đọc mã → Freeze frame → Khoanh vùng → Thử xác nhận" (shot 5, 32) dùng checklist-tick.
- Đồ họa danh sách dữ liệu bị mất khi xóa mã (shot 13): mã chờ (pending), mã xác nhận (confirmed), freeze frame, trạng thái sẵn sàng (readiness) (claim C04).
- Sơ đồ cây bốn nhánh nguyên nhân với tên phép thử (shot 17), không ghi giá trị chuẩn nào.
- Đồ họa ba thẻ "ba cái sai" với gạch chéo (shot 23): chữ trên thẻ lấy đúng dòng ON-SCREEN của S07, không thêm số liệu hay tên hãng.
- Đồ họa bộ xúc tác và đèn check engine (shot 30, 31); nếu dùng đồ họa mô phỏng đèn nháy thì ghi nhãn "mô phỏng" trên hình.
- Lower third tên và vai trò người dẫn (shot 3); màn hình kết thúc với logo và dòng "Cartek - Check your car", nửa phải để trống cho end-screen YouTube (shot 34).
- Băng cảnh báo an toàn (safety-banner) với nguyên văn bốn câu SAFETY của S05, S06, S08, S09.

## Filming notes (Ghi chú quay)

- Xe thử phải đang lưu P0300 thật và có freeze frame đọc được trước ngày quay; không dàn dựng hay gõ số liệu. Nếu xe thử không có mã permanent hoặc không nháy đèn, dùng phương án đồ họa đã ghi ở shot 29, 30.
- Màn hình máy chẩn đoán: quay vuông góc, tắt đèn chiếu thẳng để không lóa; không để tên thiết bị lọt vào khung (dùng "máy chẩn đoán", không nêu tính năng Cartek 2 vì sổ tính năng đang trống).
- Khi nổ máy để đọc dữ liệu (shot 2, 10, 14, 15, 18, 20, 26, 27): mọi người và dây cáp cách xa quạt làm mát và dây curoa; ống xả và cổ góp nóng, không chạm; nổ máy trong chỗ thông thoáng hoặc có ống hút khí xả.
- Đo áp suất nhiên liệu (shot 19): xả áp hệ thống theo quy trình của hãng cho xe thử, không có nguồn lửa và không hút thuốc trong khu vực, bình chữa cháy để sẵn trong tầm tay và trong khung hình; lau sạch xăng rò trước khi nổ máy.
- Hoán đổi bô-bin và lắp đồng hồ nén (shot 18, 21): làm khi máy tắt và đã nguội đủ để chạm; tháo bô-bin đúng quy trình hãng.
- Không quay rõ mặt số áp suất nhiên liệu hay áp suất nén (shot 19, 21) để video không đọc giá trị chuẩn; giá trị chuẩn tùy hãng và động cơ.
- Ánh sáng: đèn LED mềm từ phía trên cho khoang máy, đèn phụ thấp cho tay và phiếu; góc máy khoang máy từ phía trước-bên để không đứng đối diện quạt.
- Lower third: tên và chức danh người dẫn phải được người đó xác nhận trước khi dựng.
- Chạy thử trên đường (S08) nếu có quay: một người lái, một người cầm máy chẩn đoán và máy quay; không gắn màn hình trước mặt người lái; quay cảnh so freeze frame (shot 26, 27) khi xe đứng yên trong xưởng, máy nổ.
- Người dẫn đọc đúng số đang hiện trên màn hình lúc quay (S05); nếu quay lại cảnh thì đọc lại theo số mới, không ghép tiếng của lần quay cũ vào hình mới.
