# Channel positioning

What the Cartek YouTube channel is about, who it serves, and how it differs from the channels it competes with.

Related: [content pillars](content-pillars.md) · [audience personas](audience-personas.md) · [competitor analysis](competitor-analysis.md) · [brand voice](brand-voice.md) · [editorial guidelines](editorial-guidelines.md)

## From the sheet (source)

Values are quoted from the spreadsheet *Cartek: Youtube Release* as imported into [`data/normalized/channel.json`](../data/normalized/channel.json). Outer whitespace is trimmed.

| Setting | Long-form (tab `Content Direction`) | Shorts (tab `Short`) |
|---|---|---|
| Channel topic | "Chia sẻ kinh nghiệm sửa chữa ô tô qua hệ thống OBD2" ('Content Direction'!B1) | — (not set in the tab) |
| Video types | "How - to Tutorials, Giới thiệu sản phẩm (review), tips - trick, phỏng vấn chuyên gia (Q&A), Vlogs." ('Content Direction'!B2) | Same text ('Short'!B1) |
| Duration | "5-8 phút" ('Content Direction'!B3) | "< 60 giây" ('Short'!B2) |
| Call to action | "Để lại comment nếu cần tư vấn và hãy bấm like, subcribe, bật nút chuông thông báo để không bỏ lỡ những video hữu ích. Cartek - Check your car" ('Content Direction'!B4) | "Cartek - Check your car" ('Short'!B3) |

Other source facts:

- The product named in the sheet is "Cartek 2" (pillar 1 name, 'Content Direction'!B5). The sheet documents none of its functions. See [product facts](product-facts.md).
- 'Content Direction'!D1 links to a second spreadsheet, *Cartek_Youtube Channel*. It was audited on 2026-11-05 and holds only sample rows, so it is not imported. Details: [import report](../reports/import-report.md).
- Competitor weaknesses recorded in the sheet ('Đối thủ'!B6:F6):
  - Ecuboot: "Lịch upload video không đều; đa số đều ở dạng POV; chất lượng video chưa cao, còn khá nghiệp dư" (B6)
  - OBD Viet Nam: "Nội dung chưa được đa dạng ngoài việc chia sẻ tính năng sản phẩm" (C6)
  - ASCOM - Thiết bị Garage: "Chất lượng video chưa cao" (D6)
  - Kênh kiến thức ô tô: "Chất lượng video chưa cao." (E6)
  - VATC - Huấn luyện kỹ thuật ô tô: "Chất lượng video chưa được cao" (F6)

## Repository guidance (added 2026-11-05; editorial assumption, change freely)

### Positioning statement

> Cartek is the practical OBD2 diagnostics channel for Vietnamese garages, technicians, automotive students and car owners. Every technical statement is sourced, every procedure is shown safely, and every demonstration is real.

This statement is an interpretation of the channel topic above. It is not a sheet value.

### Differentiation

The points below are interpretations of the competitor notes in the sheet. They are not measured facts.

| Gap noted in the sheet | How Cartek answers it |
|---|---|
| Four of five competitors are noted for low video quality ('Đối thủ'!B6, D6, E6, F6). | Plan every video with a storyboard and shot list. Use clean audio, readable screen captures of diagnostic data and stable framing. |
| Irregular upload schedule (Ecuboot, 'Đối thủ'!B6). | Publish on a cadence the team can sustain. Track it on the [content board](../reports/content-board.md). The sheet sets no cadence, so none is fixed here. |
| Content limited to product features (OBD Viet Nam, 'Đối thủ'!C6). | Lead with diagnostic knowledge that is useful with any scan tool. Show Cartek 2 only where it is the right tool and its features are verified. |
| Strong competitors are noted for depth and academic quality (Kênh kiến thức ô tô, 'Đối thủ'!E5). | Match depth with traceable sources: standards, OEM service information and recorded tests. |

### What Cartek content is not

- **Not unverified product claims.** No Cartek 2 capability, vehicle coverage or protocol support appears in content until it is a verified entry in the [feature register](../data/reference/cartek-2-feature-register.yaml).
- **Not "clear the code and it is fixed".** Clearing a code removes the record and the lamp. It never repairs the cause. QC enforces this wording rule ([config/qc-policy.yaml](../config/qc-policy.yaml)).
- **Not a diagnosis by code alone.** A trouble code tells you what the control unit detected, not the confirmed root cause.
- **Not unsafe DIY.** Brakes, airbags, high-voltage systems, fuel systems and work under a lifted car need a qualified technical review and on-screen safety warnings.
- **Not invented numbers.** No made-up views, CTR, rankings, search volumes or market statistics.
- **Not attacks on competitors.** Compare tools and methods factually; never mock a channel or a person.

### Formats

| Format | Aspect ratio | Duration target | Where it comes from |
|---|---|---|---|
| Long-form | 16:9 | "5-8 phút" | Sheet ('Content Direction'!B3). The runtime is calculated from the narration and the speech rate in [config/production.yaml](../config/production.yaml), not guessed. |
| Shorts | 9:16 | "< 60 giây" | Sheet ('Short'!B2). |

YouTube now classifies square or vertical uploads of up to 3 minutes as Shorts (uploads since 2024-10-15; see [config/platform-limits.yaml](../config/platform-limits.yaml)). Cartek's own Shorts target stays under 60 seconds, as the sheet sets it. Change the target only by an explicit strategy decision, recorded here and in the item's `production.runtime_exception`.

The durations are starting requirements, not fixed rules. A long-form video may run outside 5-8 minutes when an item records a `runtime_exception` with a rationale (see [schemas/content.schema.json](../schemas/content.schema.json)).

### How this file is used

- [cartek-content-strategist](../skills/cartek-content-strategist/SKILL.md) uses it to choose angles that fit the channel.
- The [idea-to-publish workflow](../workflows/idea-to-publish.md) treats this file as the authority on positioning.
- Review it after each [post-publish analysis](../workflows/post-publish-analysis.md) cycle, based on real YouTube Studio data only.
