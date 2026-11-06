# Visual identity

How Cartek videos look and sound on screen: typography for Vietnamese text, colour tokens, the library of sound and visual effects, and the subtitle rules. The machine-readable version is [config/visual-style.yaml](../config/visual-style.yaml); QC gate G7 and the production package read that file, this page explains it.

Related: [brand voice](brand-voice.md) · [channel positioning](channel-positioning.md) · [editorial guidelines](editorial-guidelines.md) · [storyboard template](../templates/storyboard.md) · [idea-to-publish workflow](../workflows/idea-to-publish.md)

## From the sheet (source)

The spreadsheet *Cartek: Youtube Release* contains **no** typography, colour, logo, sound or effects guidance. The only related facts are indirect:

| Item | Value | Source |
|---|---|---|
| Brand line shown and spoken in every CTA | "Cartek - Check your car" | 'Content Direction'!B4, 'Short'!B3 |
| Competitor weakness the channel answers | "Chất lượng video chưa cao" (four of five competitors) | 'Đối thủ'!B6, D6, E6, F6 |
| Formats | 16:9 long-form "5-8 phút"; 9:16 Shorts "< 60 giây" | 'Content Direction'!B3, 'Short'!B2 |

No official Cartek logo file, palette or font is stored in this repository.

## Repository guidance (added 2026-11-06; production assumption, change freely)

Everything below is a **repository default** chosen on 2026-11-06 so that storyboards, QC and the production package share one vocabulary. It is not a brand-team decision. Change [config/visual-style.yaml](../config/visual-style.yaml) and this page together; the IDs are what storyboards reference.

### Principles

- **Readable on a phone.** Most viewers watch on a phone. Text sizes below are for a 1080p frame and were chosen for that, not for a desktop monitor. Validate on a real phone before locking.
- **The real screen is the evidence.** Graphics point at, repeat or enlarge what the scan tool really showed in that shot. No code, value or menu appears on screen that the tool did not display and that no claim in `item.yaml` defines ([CLAUDE.md](../CLAUDE.md) §7: never invent diagnostic data).
- **Calm about faults.** From the [brand voice](brand-voice.md): codes and lamps are information, not disasters. No horror sound design, no sirens, no fake engine-failure sounds.
- **Safety is shown where the risk occurs.** Every segment with a `SAFETY:` line gets the safety banner in at least one shot; G7 warns when it is missing.
- **Cartek 2 is shown, not claimed.** The logo and the brand line are allowed anywhere; a statement about what Cartek 2 can do still needs a verified `cartek-feature` claim ([product facts](product-facts.md)). G5 enforces this.

### Fonts

Fonts were evaluated on 2026-11-06 for licence, Vietnamese coverage and on-screen legibility. Licence and Vietnamese support were confirmed from the `google/fonts` repository metadata (`METADATA.pb`, `vietnamese` subset), because the Google Fonts site was not reachable from the session. **Not verified:** glyph-by-glyph presence of every precomposed Vietnamese code point, and legibility in a rendered test; the legibility notes rest on design characteristics (x-height, counters, 0/O and 1/l/I shapes).

| Library id | Family | Use | Licence | Vietnamese |
|---|---|---|---|---|
| `be-vietnam-pro` | Be Vietnam Pro (500/600/700) | Primary: captions, lower thirds, callouts, end screen. Google Fonts subsets latin, latin-ext, vietnamese; glyph table not inspected. | SIL OFL 1.1, free for commercial video | confirmed (subset metadata) |
| `inter` | Inter | Fallback for the primary; tabular figures for numeric tables | SIL OFL 1.1 | confirmed (subset metadata) |
| `jetbrains-mono` | JetBrains Mono (500/700) | DTC codes and live-data numbers: clearest 0/O and 1/l/I, so P0300 never reads as PO3OO | SIL OFL 1.1 | confirmed (subset metadata only; upstream README silent) |
| `roboto-mono` | Roboto Mono | Fallback monospace | SIL OFL 1.1 in google/fonts (older releases Apache 2.0) | confirmed (subset metadata) |

Also evaluated and not chosen: Montserrat (wide set width fits less caption text per line), Roboto and Noto Sans (solid but generic), Source Code Pro (lighter strokes than JetBrains Mono). All are OFL with a Vietnamese subset and remain acceptable substitutes.

Text rules for every role: precomposed **NFC** diacritics (never combining marks or stacked characters faked in the editor); **sentence case** with proper nouns and codes as written ([brand voice](brand-voice.md)); codes and numbers copied exactly from `script.md` and the claim register; everything inside the title-safe area.

### Typography roles

Storyboard column **Text style** lists these ids. Sizes are px on a 1920×1080 frame; scale proportionally for 9:16 Shorts.

| Role id | Vietnamese | Font / weight | Size | Limits | Where |
|---|---|---|---|---|---|
| `caption` | Phụ đề / caption | Be Vietnam Pro 500 | 44 px | 2 lines × 38 chars | Centered, bottom edge ≥ 120 px above the frame bottom (YouTube progress bar, phone UI) |
| `lower_third` | Tên và chức danh | Be Vietnam Pro 700 (title line 500, 32 px) | 48 px | 2 lines × 32 chars | Lower-left; never at the same time as captions |
| `callout` | Tiêu đề / nhấn mạnh | Be Vietnam Pro 600 | 56 px | 2 lines × 24 chars | Upper third or center; never over the scan-tool screen |
| `dtc_code` | Mã lỗi (DTC) | JetBrains Mono 700 | 72 px | 1 line × 16 chars | Center or upper-right, clear of the real tool screen |
| `live_data_number` | Số liệu dữ liệu trực tiếp | JetBrains Mono 500 | 48 px | 3 lines × 28 chars | Side panel, right-aligned numbers; only values actually read during recording |
| `end_screen` | Màn hình kết thúc | Be Vietnam Pro 600 | 40 px | 2 lines × 36 chars | Left half; YouTube end-screen elements on the right; carries the brand line and logo only |

### Colour tokens (placeholders)

| Token | Placeholder value | Meaning |
|---|---|---|
| `background` | `#101418` | Dark panel background behind text |
| `text` | `#F5F7FA` | Primary text |
| `accent_safety` | `#E0A100` (amber; `#C62828` red for high-risk systems) | Safety banner |
| `accent_code` | `#4FC3F7` | DTC codes and highlighted values |

These are contrast-tested placeholders for a dark workshop frame, **to be replaced by the brand team**. Roles reference tokens, so swapping the palette changes nothing in storyboards.

### Effects library

Storyboard column **Effects** lists these ids, comma-separated. `hard-cut` is the default transition. "Max" is a suggestion per video; G7 warns above it and the storyboard's "Sound and effects" section records the reason.

| Id | Kind | Vietnamese | Use it for | Max | Never |
|---|---|---|---|---|---|
| `hard-cut` | transition | Cắt thẳng | Everything unless another transition is listed | — | A sound on a plain cut |
| `soft-dissolve` | transition | Mờ chồng nhẹ | Change of place or time | 6 | Between consecutive tool screens |
| `code-popup` | vfx | Mã lỗi hiện lên | First naming of each code; the recap (`dtc_code` + meaning in `caption` size) | — | A code no claim defines; in a shot with a real tool screen, a code that screen did not show (explanatory animations without a tool screen may show claim-defined codes) |
| `highlight-circle` | vfx | Khoanh tròn | One reading or menu item while narration names it | — | Covering the value; marking an unmentioned value |
| `highlight-arrow` | vfx | Mũi tên chỉ | Parts, connectors, multi-step menu paths | — | A part the script does not name |
| `zoom-punch` | vfx | Zoom nhấn | One key sentence per segment at most | 6 | Safety warnings; twice in a row |
| `lower-third` | lower-third | Lower third | First appearance of a presenter or guest | 4 | While captions are shown; an unconfirmed title |
| `safety-banner` | vfx | Băng cảnh báo an toàn | Every segment with `SAFETY:` or `TYPE: safety`: full-width `accent_safety` banner, icon, the SAFETY text verbatim, held for the whole warning | — | Paraphrasing the warning; alarm or siren sounds |
| `freeze-frame-snapshot` | vfx | Đóng băng khung hình | Stored data (freeze frame) or the moment a reading is captured | 4 | Implying the tool took a snapshot it did not |
| `checklist-tick` | vfx | Dấu tích | Recaps and step-by-step procedures | — | Ticking a step the video did not show |
| `sfx-whoosh` | sfx | Tiếng lướt nhẹ | With code-popup, lower-third, checklist-tick | 12 | Over a spoken word; the loud cinematic variant |
| `sfx-ui-click` | sfx | Tiếng click | Menu navigation when the tool is silent | 12 | On top of the tool's real sounds |
| `sfx-ui-beep` | sfx | Tiếng bíp | A reading or code appears | 8 | Repeated or rising alarm tones |
| `sfx-low-thud` | sfx | Tiếng trầm cảnh báo | Entry of the safety banner; a "common mistake" reveal | 6 | Layered into a drone or rumble |

Sound rules for the whole video: no alarmist horror SFX, sirens or fake engine-failure sounds; sound effects never cover narration; music ducked about 18 LU under the voice and faded under safety warnings; the vehicle's and the tool's real sounds are kept; only library effects are used (add new ones to the library first).

### Captions

Subtitles are **mandatory** for every video, burned in (`caption` role) or uploaded as a track. One idea per line; at most 2 lines on screen; codes, acronyms and numbers exactly as in `script.md`; captions follow the final recorded voice-over (`publication.upload_checklist`).

### How this file is used

- The producer fills the **Effects** and **Text style** columns and the "Sound and effects" / "Typography" sections of [storyboard.md](../templates/storyboard.md) (stage PRODUCTION_PACKAGE).
- Gate **G7** ([scripts/ctk/qc.py](../scripts/ctk/qc.py)) warns on unknown effect ids, unknown typography roles, a safety segment without `safety-banner`, and effects above their suggested maximum; it never fails on them. It adds an INFO line listing the effects used.
- Gate **G5** allows the Cartek logo, brand name and end screen in any segment ([config/qc-policy.yaml](../config/qc-policy.yaml) → `brand_mark_mentions`) when the clause ends after the mark or goes on with a placement word ("Logo Cartek ở góc trên phải"); a capability statement in the same clause ("Thương hiệu Cartek chẩn đoán được mọi xe") or anywhere about Cartek 2 still needs a verified feature claim.
- The production package ([schemas/production-package.schema.json](../schemas/production-package.schema.json) → `visual_style`) carries the fonts, the roles and effects the storyboard uses with their descriptions, the caption and sound rules, and the source file. Library values are copied at export time and the library is not part of the content fingerprint: after changing `config/visual-style.yaml`, re-export release packages (`validate_content.py` reports the difference).
- Review this page with the brand team; replace the placeholder colours and confirm the fonts before the first published video.
