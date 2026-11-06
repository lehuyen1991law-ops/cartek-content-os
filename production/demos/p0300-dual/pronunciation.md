# Pronunciation dictionary — P0300 dual demo (Long A + Short B)

One spoken form per code or term, used in both scripts, the TTS text and the human voice-over
(strategy/brand-voice.md, Vietnamese style rule 6). On screen and in captions the written form stays
exactly as in the script (`P0300`, `OBD2`, `ECU`): only the *spoken* text is spelled out.

## Decision: how to read P0300

| Option | Example | Decision |
|---|---|---|
| Vietnamese digits, "trăm" grouping | "pê không ba trăm" | **Chosen.** Natural for Vietnamese technicians and car owners; matches CTK-L-0015 script NOTES. |
| Digit by digit, English letters | "P-zero-three-zero-zero" | Rejected: foreign cadence, longer, mixes languages mid-sentence. |
| Digit by digit, Vietnamese | "pê không ba không không" | Rejected: harder to hear than "ba trăm", and nobody in a garage says it. |

The same grouping applies to every P03xx code: `P0301` = "pê không ba trăm lẻ một", `P0304` = "pê không ba trăm lẻ bốn",
`P0312` = "pê không ba trăm mười hai". The letter is always "pê" (Vietnamese letter name), never "pi".

## Dictionary

| Written (on screen / captions) | Spoken form (voice artist) | TTS text (edge-tts, SSML-friendly) | Notes |
|---|---|---|---|
| P0300 | pê không ba trăm | `pê không ba trăm` | Never "pê không nghìn ba trăm". |
| P0301 | pê không ba trăm lẻ một | `pê không ba trăm lẻ một` | |
| P0312 | pê không ba trăm mười hai | `pê không ba trăm mười hai` | |
| P0301 đến P0312 | pê không ba trăm lẻ một đến pê không ba trăm mười hai | same | Read both codes in full; do not shorten to "lẻ một đến mười hai". |
| OBD2 (cổng, máy quét) | ô-bê-đê hai | `ô-bê-đê hai` | Vietnamese letter names. "OBD2" is the channel spelling for narration and titles. |
| OBD-II (tên chuẩn) | ô-bê-đê hai | `ô-bê-đê hai` | Same sound as OBD2; the hyphenated form is only written when naming the standard. |
| ECU | i-xi-u | `i-xi-u` | English letter names, as technicians in Vietnam say it. Not "ê-xê-u". |
| xi-lanh | xi-lanh | `xi-lanh` | Standard Vietnamese loanword; no change. |
| bô-bin (đánh lửa) | bô-bin | `bô-bin` | One spelling per script (glossary); never mix with "mô-bin" or "cuộn đánh lửa" in narration. |
| bugi | bu-gi | `bugi` | Standard; TTS reads it correctly as written. |
| Cartek | Ca-tếch (stress on "tếch", short) | `Cartek` (fallback: `Ca-tếch`) | TTS: keep the English spelling first; the vi-VN neural voices switch to English pronunciation for known words. If the listening check finds "Cartek" garbled, use `Ca-tếch`. |
| freeze frame | phờ-ri phrêm (English, light Vietnamese accent) | `freeze frame` (fallback: `phờ-ri phrêm`) | Technicians say it in English. The spelled form is for a human reader who is unsure; for TTS the English spelling renders better. On first mention the script adds "tức dữ liệu đóng băng". |
| Check Engine (đèn) | chéc en-gin | `Check Engine` (fallback: `chéc en-gin`) | Always "đèn Check Engine" for a mixed audience (glossary: car owners). |
| readiness | re-đi-nét | `readiness` (fallback: `re-đi-nét`) | Only in Long S06. |
| like / subscribe / comment | lai / sắp-xờ-crai / com-men | keep English | Common YouTube words; keep English spelling for TTS. |
| Cartek - Check your car | Ca-tếch. Chéc do ca. | `Cartek. Check your car.` | The hyphen in the brand line is written on screen, spoken as a short pause (TTS: full stop). Fallback: `Ca-tếch. Chéc do ca.` |
| Mỹ (quy định OBD-II của Mỹ) | Mỹ | `Mỹ` | Refers to 13 CCR 1968.2 (CARB) as applied by EPA (claims C06, C11). |

## SSML notes for the TTS render

- The render replaces the written forms with the TTS column before synthesis (longest match first: "P0301 đến P0312" before "P0301").
- Spelled-out forms are plain text, not `<say-as>`: edge-tts accepts plain text only, and the plain text keeps the Vietnamese grouping.
- A sentence boundary (". ") after "Khoan đã!" and before "Cartek" gives the voice a natural pause; the editor adds the 0.5 s gaps between segments.
- Do not spell out numbers that are already Vietnamese words ("năm bước", "số một"); they read correctly as written.

## Open items (REVIEW REQUIRED)

- A Vietnamese speaker must listen to the demo renders and confirm "Cartek", "freeze frame", "Check Engine", "readiness" and the brand line. If any is garbled, switch that entry to its fallback spelling in both the TTS text and this table, and re-render.
- The glossary in strategy/brand-voice.md marks "bù nhiên liệu / fuel trim" and "mã lỗi chờ / pending" as proposals; neither word appears in these two demo scripts.
