# Competitor analysis

The five channels the sheet tracks, quoted verbatim, followed by the gaps Cartek can serve and the rules for using this research.

Related: [channel positioning](channel-positioning.md) · [SEO workflow](../workflows/seo-optimization.md) · [editorial guidelines](editorial-guidelines.md)

## From the sheet (source)

Quoted from tab `Đối thủ` as imported into [`data/normalized/competitors.json`](../data/normalized/competitors.json). Outer whitespace is trimmed. Rows: 1 name, 2 YouTube link, 3 content strategy, 4 reach metrics, 5 strengths, 6 weaknesses, 7 SEO keywords.

> **The reach metrics are historical.** They were recorded in the sheet at an unknown date. They are not current and have not been verified. Do not quote them as today's figures in content, reports or pitches.

### Ecuboot ('Đối thủ'!B1:B7)

- **Link youtube:** https://www.youtube.com/c/EcubootVi%E1%BB%87tNam (B2)
- **Chiến lược content:** "Chia sẻ kiến thức, giới thiệu dịch vụ, quảng bá sản phẩm" (B3)
- **Đo lường tiếp cận viewer (historical, unverified):** "Avg Views: 1-2000, Avg Comments: 1-2, Subscriber : 4.28k" (B4)
- **Thế Mạnh:** "Video đa chủ đề; chia sẻ gần gũi - mộc mạc; Có các kiến thức rất chuyên sâu" (B5)
- **Điểm Yếu:** "Lịch upload video không đều; đa số đều ở dạng POV; chất lượng video chưa cao, còn khá nghiệp dư" (B6)
- **SEO/Keywords:** "Chẩn đoán ô tô", "Chẩn đoán xe Châu Âu", "chẩn đoán xe BMW", "Khóa học chẩn đoán" (B7)

### OBD Viet Nam ('Đối thủ'!C1:C7)

- **Link youtube:** https://www.youtube.com/@kenhchuyengiachandoanoto/featured (C2)
- **Chiến lược content:** "Giới thiệu dịch vụ, quảng bá sản phẩm, How - to video" (C3)
- **Đo lường tiếp cận viewer (historical, unverified):** "Avg Views: 100-300, Avg Comments: 1-2, Subscriber : 29.2k" (C4)
- **Thế Mạnh:** "Là kênh youtube của OBD Việt nam, được đầu tư nhiều. Video được xuất bản liên tục hàng ngày. Giới thiệu cách sử dụng các sản phẩm kĩ lưỡng" (C5)
- **Điểm Yếu:** "Nội dung chưa được đa dạng ngoài việc chia sẻ tính năng sản phẩm" (C6)
- **SEO/Keywords:** "Autel"; "Gscan"; "OBD"; "liqui moly"; "Autel Việt nam"; "Phần mềm ô tô". (C7)

### ASCOM - Thiết bị Garage ('Đối thủ'!D1:D7)

- **Link youtube:** https://www.youtube.com/@giaiphapotoascom/featured (D2)
- **Chiến lược content:** "Chia sẻ thông tin - kiến thức, giới thiệu sản phẩm, giới thiệu dịch vụ" (D3)
- **Đo lường tiếp cận viewer (historical, unverified):** "Avg Views: 100-200, Avg Comments: 0, Subscriber : 546" (D4)
- **Thế Mạnh:** "Nội dung rất đa dạng thể loại, video upload đều hàng tuần" (D5)
- **Điểm Yếu:** "Chất lượng video chưa cao" (D6)
- **SEO/Keywords:** "Launch"; "Thinktool"; "Launchtech"; "X431"; "ô tô"; "sửa chữa ô tô". (D7)

### Kênh kiến thức ô tô ('Đối thủ'!E1:E7)

- **Link youtube:** https://www.youtube.com/@KENHKIENTHUCOTO/videos (E2)
- **Chiến lược content:** "Chia sẻ kiến thức" (E3)
- **Đo lường tiếp cận viewer (historical, unverified):** "Avg Views: 3-5k, Avg Comments: 10 - 15, Subscriber : 46k" (E4)
- **Thế Mạnh:** "Nội dung kiến thức chuyên sâu, nhiều thể loại, tính học thuật cao" (E5)
- **Điểm Yếu:** "Chất lượng video chưa cao." (E6)
- **SEO/Keywords:** "KKTOT"; "Kenh kien thuc oto"; "Kiến thức ô tô". (E7)

### VATC - Huấn luyện kỹ thuật ô tô ('Đối thủ'!F1:F7)

- **Link youtube:** https://www.youtube.com/@vatc.dayngheoto/videos (F2)
- **Chiến lược content:** "Vlog, Chia sẻ kiến thức, giới thiệu dịch vụ" (F3)
- **Đo lường tiếp cận viewer (historical, unverified):** "Avg Views: 100-200, Avg Comments: 0, Subscriber : 25.7k" (F4)
- **Thế Mạnh:** "Nội dung được đầu tư nhiều, đa dạng góc nhìn cho viewer, lịch ra video khá đều đặn" (F5)
- **Điểm Yếu:** "Chất lượng video chưa được cao" (F6)
- **SEO/Keywords:** "VATC"; "Oto"; "Học sửa chữa ô tô"; "Nghề sửa chữa ô tô"; "Đào tạo ô tô" (F7)

Cell 'Đối thủ'!C8 holds a single space and is ignored by the importer.

## Repository guidance (added 2026-11-05; editorial assumption, change freely)

### Keyword landscape

Built from row 7 above. It shows which words competitors target; it says nothing about search volume, which the sheet does not record.

| Keyword theme | Keywords from the sheet | Channels | Relevance to Cartek |
|---|---|---|---|
| Diagnostics (generic) | Chẩn đoán ô tô, OBD | Ecuboot, OBD Viet Nam | Core: matches the channel topic ('Content Direction'!B1). |
| European / German cars | Chẩn đoán xe Châu Âu, chẩn đoán xe BMW | Ecuboot | Fits idea CTK-L-0012; needs OEM sources per model. |
| Scan-tool brands | Autel, Autel Việt nam, Gscan, Launch, Launchtech, X431, Thinktool | OBD Viet Nam, ASCOM | Trademarks of other companies; see the rules below. |
| Lubricant brand | liqui moly | OBD Viet Nam | Unrelated to Cartek's pillars. |
| Software | Phần mềm ô tô | OBD Viet Nam | Only if a video covers diagnostic software. |
| Repair and training | sửa chữa ô tô, Học sửa chữa ô tô, Nghề sửa chữa ô tô, Đào tạo ô tô, Khóa học chẩn đoán | ASCOM, VATC, Ecuboot | Fits P2 and P4 for technicians and students. |
| General / channel names | ô tô, Oto, Kiến thức ô tô, Kenh kien thuc oto, KKTOT, VATC | ASCOM, VATC, Kênh kiến thức ô tô | Broad terms; channel names belong to those channels. |

Before using any keyword, record where you saw it and when in `seo.md` → "Keyword notes" ([SEO workflow](../workflows/seo-optimization.md)).

### Gaps Cartek can serve (interpretation)

These readings come from the strengths and weaknesses above. They are hypotheses to test with real channel data, not findings.

1. **Production quality.** Four of the five channels are noted for low video quality (B6, D6, E6, F6). Clear audio, readable scan-tool screens and a planned shot list are a visible difference.
2. **Consistency.** Ecuboot is noted for an irregular schedule (B6), while ASCOM and VATC are noted for regular uploads (D5, F5). Regularity is expected in this niche.
3. **Education beyond product promotion.** OBD Viet Nam is noted for content that rarely goes beyond product features (C6). Cartek can lead with diagnostic knowledge and show the tool only where it fits.
4. **Depth with sources.** The channel with the highest reach recorded in the sheet (historical figures, E4) is also the one noted for academic depth (E5). Cartek can match that depth and add traceable sources for every claim.

### Rules for using competitor research

- **No disparagement.** Never mock, name-and-shame or misrepresent a competitor or its presenters. Compare methods and verified facts only.
- **Trademarks.** Autel, Launch, Launchtech, X431, Thinktool, Gscan, Liqui Moly and the channel names above belong to their owners. Use them in titles, tags or descriptions only when the video genuinely discusses that product or channel. Never imply an endorsement, partnership or compatibility that is not verified. Misleading metadata also breaks YouTube's spam and deceptive-practices policies.
- **No copying.** Do not reuse competitors' footage, thumbnails, scripts or titles.
- **Metrics stay historical.** The figures in row 4 are a record of what someone saw at an unknown date. Do not present them as current.

### Refresh procedure

1. Open each channel from its link above and read the current public figures (subscribers, recent video views).
2. Record the date, what you measured and how, in a new dated section at the end of this file (for example "Re-measured on 2026-12-01 from the public channel pages"). Mark it as a manual observation.
3. Keep the sheet values above unchanged. They are the historical record; the importer also keeps them in [`data/source/`](../data/source/).
4. If the team wants the sheet itself updated, a person edits the sheet; then follow the [sheet import workflow](../workflows/sheet-import.md). This repository never writes to the sheet.
