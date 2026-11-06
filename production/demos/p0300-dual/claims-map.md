# Claims map — P0300 dual demo (Long A + Short B)

Every technical sentence of `long-script.md` and `short-script.md` mapped to the claim register of CTK-L-0015
(`content/long-form/CTK-L-0015-loi-p0300-ac-mong-cua-moi-dong-co/item.yaml`, claims C01–C13). No new technical fact
was added: if a sentence was not covered, it was rewritten to fit a claim or made explicitly non-technical (see
"Sentences rewritten or removed").

**Status warning:** all 13 claims are `unverified` on 2026-11-06 (C01, C02, C08–C10 have no accepted-type source yet;
C07 is partly sourced). The demos may be produced as internal demos but may not be published until the
technical-fact-checker verifies the claims the segments cite (CLAUDE.md §10).

Legend: **T** = technical sentence (needs a claim) · **N** = non-technical (framing, CTA, label) · **S** = spoken safety warning.

## Video A — Long (long-script.md)

| Seg | Sentence (VO / SAFETY) | Type | Claims | Note |
|---|---|---|---|---|
| S01 | Máy quét báo P0300. | T | C01 | Code named on screen and in VO: defined by C01. |
| S01 | Vậy có phải thay bugi ngay không? | N | — | Question, no assertion. |
| S01 | Khoan đã! | N | — | |
| S02 | Mã lỗi không phải là nguyên nhân. | T | C01 | "bản thân mã này không chỉ ra nguyên nhân". |
| S02 | P0300 chỉ nói một điều: ECU phát hiện động cơ bỏ máy, ngẫu nhiên hoặc ở nhiều xi-lanh. | T | C01 | |
| S02 | Vì sao bỏ máy? Mã này không nói. | T | C01 | |
| S02 | Thay đồ trước khi biết nguyên nhân, lỗi có thể quay lại. | T | C05, C08 | "có thể" hedge: C05 (cause still present → re-detected), C08 (confirm before replacing). |
| S03 | ECU theo dõi động cơ để bắt bỏ máy. | T | C05 | Monitoring is implicit in C05 ("ECU sẽ phát hiện lại"); C05 notes cite SRC01 (e)(3.1.1) "monitor the engine for misfire". Reviewer: confirm this reading. |
| S03 | Khi phát hiện, nó ghi mã lỗi và lưu freeze frame, tức dữ liệu đóng băng: tải, nhiệt độ nước, vòng tua, tốc độ xe lúc đó. | T | C01, C03 | Four parameters are the "all vehicles" list in C03; no values spoken or shown. |
| S03 | (SAFETY) Trên xe theo quy định OBD-II của Mỹ, đèn Check Engine nhấp nháy là bỏ máy nặng, có thể làm hỏng bộ xúc tác. | S/T | C06, C11 | Scope "của Mỹ" = 13 CCR 1968.2 as applied by EPA (C11). Does not say a steady lamp rules out heavy misfire. |
| S03 | (SAFETY) Khi đó các bạn giảm tải, hạn chế chạy và kiểm tra sớm. | S | C07 | C07 is partly sourced (regulation gives the reason, not the advice): reviewer must accept or add OEM owner's information. |
| S04 | P0300: bỏ máy ngẫu nhiên hoặc nhiều xi-lanh. | T | C01 | |
| S04 | P0301 đến P0312: bỏ máy ở một xi-lanh cụ thể, hai số cuối là số xi-lanh. | T | C02 | |
| S04 | Nhưng cùng một bệnh, xe này báo P0300, xe kia báo P0301, tùy chiến lược hãng. | T | C13 | 90 % threshold and 2005+ scope omitted for time; wording stays within C13. |
| S04 | Thứ tự xi-lanh thì tra tài liệu hãng. | T | C13 | Second half of C13 (inference flagged in item.yaml notes). |
| S04 | Nên đừng vội đoán xi-lanh. | T | C01 | Editorial conclusion of C01 (code does not identify the cylinder). |
| S05 | Bugi chỉ là một ứng viên. | T | C08 | |
| S05 | Nguyên nhân khả dĩ của P0300 nằm trong bốn nhóm: đánh lửa, như bugi và bô-bin; nhiên liệu, như áp suất và kim phun; rò rỉ khí nạp hay chân không; và cơ khí, như độ nén. | T | C08, C09, C10 | Groups from C08; examples from C09 (bô-bin/bugi, áp suất nhiên liệu, kim phun) and C10 (độ nén). No group called "thường gặp". |
| S05 | Mỗi nhóm có phép thử xác nhận riêng, theo quy trình của hãng. | T | C08, C09 | |
| S05 | Thay bugi khi lỗi ở nhóm khác, tiền mất mà mã vẫn có thể quay lại. | T | C05, C08 | "tiền mất" is editorial; "mã vẫn có thể quay lại" is C05. |
| S06 | Năm bước. | N | — | Structure of the demo, not a sourced procedure name. |
| S06 | Một, đọc và ghi lại mã, đừng xóa vội, vì xóa là mất freeze frame và readiness. | T | C04 | |
| S06 | Hai, kiểm tra triệu chứng và dữ liệu liên quan, nhất là freeze frame, xem lỗi xảy ra ở vòng tua nào, tải nào, máy nóng hay nguội. | T | C03 | Reads the three "all vehicles" freeze frame items. |
| S06 | Ba, thu thập thông tin xe, gồm hãng, đời xe, động cơ, thị trường. | T | C11, C13 | Market/model-year/engine differences (C11); cylinder numbering per OEM (C13). |
| S06 | Bốn, kiểm tra theo quy trình của hãng. | T | C09, C10 | |
| S06 | Năm, xác nhận nguyên nhân rồi mới sửa. | T | C08 | |
| S07 | Tình huống minh họa, không phải ca thật. | N | — | Mandatory label: no real vehicle, data or repair behind it. |
| S07 | Xe báo P0300, freeze frame ghi lỗi xảy ra khi máy còn nguội. | T (illustrative) | C01, C03 | Coolant temperature is a freeze frame item (C03). No numeric value. |
| S07 | Thợ không thay bugi ngay, mà hoán đổi bô-bin giữa hai xi-lanh rồi chạy lại đúng điều kiện đó. | T | C09 | Coil-swap test as listed in C09; not called "common". |
| S07 | Bỏ máy đi theo bô-bin thì nghi bô-bin. | T | C09 | "để xem bỏ máy có đi theo bô-bin không". |
| S07 | Không thì sang nhóm khác. Thử trước, thay sau. | T | C08 | |
| S07 | (SAFETY) Tháo lắp bô-bin khi máy đã tắt; máy chạy thì tránh xa quạt và dây curoa. | S | — (gap, kept) | Spoken warning required by `safety.flags: hot-or-moving-parts`. No claim covers workshop safety practice; same situation as CTK-L-0015 S05/S06/S08 SAFETY lines (research.md → Safety notes: no accepted source yet). REVIEW REQUIRED by a qualified technical reviewer. |
| S08 | Tóm lại, P0300 là điểm bắt đầu để tìm nguyên nhân, không phải danh sách linh kiện cần thay. | T | C01, C08 | |
| S08 | Đọc mã, giữ freeze frame, hiểu xe, kiểm tra theo hãng, xác nhận rồi mới sửa. | T | C03, C04, C08, C09, C10, C11 | Recap of S06. |
| S09 | Có ca P0300 khó, các bạn để lại comment, bấm like và subscribe. | N | C01 (code name only) | CTA. |
| S09 | Cartek - Check your car. | N | — | Brand line ('Content Direction'!B4 / 'Short'!B3). |

## Video B — Short (short-script.md)

| Seg | Sentence | Type | Claims | Note |
|---|---|---|---|---|
| S01 | Đừng vội thay bugi chỉ vì máy báo P0300! | T | C01, C08 | Imperative derived from C01 (code ≠ cause) and C08 (confirm before replacing). |
| S02 | P0300 chỉ nói ECU phát hiện động cơ bỏ máy, ngẫu nhiên hoặc ở nhiều xi-lanh. | T | C01 | |
| S02 | Nó không nói vì sao. | T | C01 | |
| S03 | Bỏ máy có thể do bugi, do bô-bin đánh lửa, do nhiên liệu, hay do rò khí nạp. | T | C08 | Three of the four C08 groups (mechanical group left to the Long for time). No ranking. |
| S03 | Mỗi nhóm cần một phép thử xác nhận trước khi thay. | T | C08 | |
| S04 | Việc cần làm: đọc và ghi lại mã. | T | C04 | Record before clearing (clearing erases the evidence). |
| S04 | Xem freeze frame: lỗi xảy ra ở vòng tua nào, tải nào, máy nóng hay nguội. | T | C03 | |
| S04 | Rồi kiểm tra theo quy trình của hãng cho đúng xe. | T | C09, C11 | |
| S04 | Xóa mã không sửa được lỗi, lại làm mất freeze frame. | T | C05, C04 | G5-compliant wording: clearing never repairs. |
| S05 | ECU phát hiện lỗi. | T | C01 | Rewritten from "Máy quét phát hiện lỗi" (see below). |
| S05 | Còn xác nhận nguyên nhân là việc của người thợ. | T | C08 | |
| S05 | P0300 là điểm bắt đầu, không phải danh sách linh kiện cần thay. | T | C01, C08 | |
| S06 | Muốn hiểu mã lỗi ô tô dễ hơn? Theo dõi Cartek! | N | — | CTA; brand line on screen. |

## Claim usage summary

| Claim | Long segments | Short segments |
|---|---|---|
| C01 | S01, S02, S03, S04, S07, S08, S09 | S01, S02, S05 |
| C02 | S04 | — |
| C03 | S03, S06, S07, S08 | S04 |
| C04 | S06, S08 | S04 |
| C05 | S02, S03, S05 | S04 |
| C06 | S03 (SAFETY) | — |
| C07 | S03 (SAFETY) | — |
| C08 | S02, S05, S06, S07, S08 | S01, S03, S05 |
| C09 | S05, S06, S07, S08 | S04 |
| C10 | S05, S06, S08 | — |
| C11 | S03, S06, S08 | S04 |
| C12 | — (permanent codes left out of both demos) | — |
| C13 | S04, S06 | — |

## Sentences rewritten or removed

| Script | Original | Action | Reason |
|---|---|---|---|
| Short S05 | "Máy quét phát hiện lỗi." | Rewritten → "ECU phát hiện lỗi." | The scan tool reads what the ECU stored; detection is the ECU's (C01). No claim says the tool "detects". |
| Long S03 | "Trên xe theo quy định OBD-II của California, nếu mức bỏ máy nặng tới mức có thể làm hỏng bộ xúc tác, đèn Check Engine nhấp nháy mỗi giây một lần." (VO) | Merged into the SAFETY line; "mỗi giây một lần" dropped | Timing (segment over 25 s). The remaining wording stays inside C06; the once-per-second detail lives in CTK-L-0015. |
| Long S04 | "P0301 là xi-lanh số một." | Removed | Timing; already implied by C02 wording "hai số cuối là số xi-lanh". |
| Long S04 | "Nên thấy P0300, đừng đoán xi-lanh nào." | Shortened → "Nên đừng vội đoán xi-lanh." | Timing; same C01 conclusion. |
| Long S07 | "... khi máy còn nguội, vòng tua thấp." | "vòng tua thấp" removed | Timing; the illustration keeps one freeze frame item (C03). |
| Long S09 | Full sheet CTA ("Để lại comment nếu cần tư vấn và hãy bấm like, subscribe, bật nút chuông thông báo...") | Shortened (non-technical) | TTS measured ~12 s for the full line; the demo has an 8 s slot. Release version uses the full sheet CTA. |
| Both | Any mention of "thường gặp" / "phổ biến" for a cause group | Never written | C08 has no source for frequency (research.md). |
| Both | Permanent fault codes (C12) | Not used | Left out to keep the demos within 3:00 / 0:59; no sentence depends on C12. |
