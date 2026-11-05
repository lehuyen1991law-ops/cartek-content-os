# Brand voice

How Cartek sounds on screen and in writing: tone, Vietnamese style, calls to action, words to avoid, and a technical glossary.

Related: [audience personas](audience-personas.md) · [editorial guidelines](editorial-guidelines.md) · [script production workflow](../workflows/script-production.md)

## From the sheet (source)

| Item | Value | Source |
|---|---|---|
| Long-form call to action | "Để lại comment nếu cần tư vấn và hãy bấm like, subcribe, bật nút chuông thông báo để không bỏ lỡ những video hữu ích. Cartek - Check your car" | 'Content Direction'!B4 |
| Shorts call to action | "Cartek - Check your car" | 'Short'!B3 |
| Channel topic | "Chia sẻ kinh nghiệm sửa chữa ô tô qua hệ thống OBD2" | 'Content Direction'!B1 |
| Video types | "How - to Tutorials, Giới thiệu sản phẩm (review), tips - trick, phỏng vấn chuyên gia (Q&A), Vlogs." | 'Content Direction'!B2, 'Short'!B1 |

The sheet spells "subcribe". Scripts use "subscribe": `scripts/new_content.py` applies that fix when it fills the CTA into a new script. The sheet itself is left unchanged.

## Repository guidance (added 2026-11-05; editorial assumption, change freely)

### Tone

- **Practical.** Every video leaves the viewer able to do or understand one specific thing.
- **Honest.** Say what is known, what depends on the vehicle, and what still needs a test. Admit limits, including the tool's.
- **Respectful of expertise.** Many viewers repair cars for a living. Explain clearly without talking down.
- **Calm about faults.** Warning lamps and codes are information, not disasters. Urgency is stated only when a source supports it.
- **Safety first.** Warnings are spoken and shown where the risk occurs, not buried at the end.

### Vietnamese style rules

1. Write with full diacritics in standard Unicode (precomposed, NFC).
2. Use sentence case for titles and on-screen text; keep proper nouns and codes as written (Cartek 2, Toyota, P0300). Some sheet ideas use Title Case; that stays in the working title only.
3. On first mention, give the Vietnamese term and then the English acronym: "mã lỗi (DTC)", "đèn báo lỗi động cơ (MIL)".
4. Write "OBD2" in titles and narration, as the sheet does. Write "OBD-II" when naming the standard.
5. Keep model and engine designations as the manufacturer writes them ("1.5 AT").
6. Choose one spoken form for each code or acronym in a script and keep it. Note the chosen pronunciation in the segment's `**NOTES:**` line for the voice-over artist.
7. Narration uses short sentences, one idea each. Read every line aloud before it goes to technical review.
8. Address viewers as "các bạn" by default, or "anh chị em kỹ thuật viên" for technicians.

### Voice by persona

| Persona | Register | Pace | Typical opening |
|---|---|---|---|
| garage-owner | Professional peer | Steady, focused on method and outcome | A workshop problem that costs time or brings cars back |
| technician | Technical peer | Dense, data on screen | A case that resists the obvious fix |
| automotive-student | Teacher | Step by step, with the "why" | A question about how a system works |
| car-owner | Helpful expert | Simple, reassuring, clear limits | A symptom the driver sees |

Details per persona: [audience personas](audience-personas.md#repository-guidance-added-2026-11-05-editorial-assumption-change-freely).

### Calls to action

- **Long-form:** close with the sheet CTA (spelling fixed to "subscribe"). A persona-specific line can come before it, for example "Kể cho Cartek về ca P0300 khó nhất bạn từng gặp ở phần bình luận."
- **Shorts:** close with "Cartek - Check your car" ('Short'!B3).
- **Brand line:** every CTA segment contains "Cartek - Check your car" in the voice-over or on screen. QC gate G4 checks this.
- **Car owners and safety systems:** when the topic involves brakes, airbags, steering or high-voltage parts, the CTA recommends a qualified garage instead of DIY.

### Words and habits to avoid

| Avoid | Why | Say instead |
|---|---|---|
| "xóa lỗi là xong", "tắt đèn là hết bệnh" | Clearing never repairs a fault (QC gate G5 fails it) | "Xóa mã lỗi chỉ xóa bản ghi; nếu chưa sửa nguyên nhân, đèn sẽ sáng lại." |
| "100%", "chắc chắn", "đảm bảo", "tuyệt đối" | Certainty that needs proof (reviewed in G5) | State the evidence, or "trong trường hợp này" |
| "tất cả các dòng xe", "mọi xe" | Unverified compatibility (reviewed in G5) | Name the vehicles tested |
| "không cần thợ" | Pushes unsafe DIY | "Nếu không chắc chắn, hãy nhờ kỹ thuật viên." |
| "lên top", "triệu view", "viral", CTR promises | Unbacked performance claims (QC gate G6 fails them) | Describe the content, not the outcome |
| Fear wording ("xe sẽ hỏng ngay") | Alarmist without a source | Give the sourced risk and the next step |
| Mocking a competitor or a viewer | Unfair and off-brand | Compare methods with facts |
| Unexplained acronyms, heavy slang | Loses car owners and students | Define the term once |

### Technical glossary

A style choice for consistent wording. **Confirm each pair with the technical reviewer before relying on it;** add terms as the team agrees on them. Entries marked "proposal" have no team decision yet.

| Tiếng Việt | English | Notes |
|---|---|---|
| mã lỗi | DTC (Diagnostic Trouble Code) | |
| đèn báo lỗi động cơ / đèn Check Engine | MIL (Malfunction Indicator Lamp) | Use "đèn Check Engine" for car owners |
| bỏ máy | misfire | |
| dữ liệu đóng băng | freeze frame data | |
| dữ liệu trực tiếp | live data | |
| trạng thái sẵn sàng | readiness monitors | |
| cổng OBD2 | DLC / OBD port | |
| máy chẩn đoán | scan tool / diagnostic scanner | |
| xóa mã lỗi | clear codes | Always with the "not a repair" caveat |
| bugi | spark plug | |
| bô-bin đánh lửa (mô-bin) | ignition coil | Pick one spelling per script |
| kim phun | fuel injector | |
| cảm biến | sensor | |
| hộp điều khiển động cơ | ECU / ECM | |
| xi-lanh | cylinder | |
| hệ thống đánh lửa | ignition system | |
| mã lỗi chờ | pending DTC | proposal |
| bù nhiên liệu ngắn hạn / dài hạn | short-term / long-term fuel trim | proposal |
| giao thức | protocol | |
| túi khí | airbag (SRS) | Safety-flagged topic |
