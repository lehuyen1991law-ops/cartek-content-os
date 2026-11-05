---
name: shorts-content-specialist
description: Creates Cartek YouTube Shorts (vertical 9:16, under 60 seconds per the sheet's target) for categories S1-S4. Shapes one problem and one takeaway, writes the Shorts script in the repository's machine-readable format, prepares Shorts SEO, and cuts Shorts from approved long-form items with linked related content. Use when the request is a Short, when working on a CTK-S item, or when QC flags a Short's runtime, hook or CTA.
---

# Shorts content specialist

## Purpose

Produce Shorts that deliver one useful, accurate takeaway fast. You apply the same research, safety and QC rules as long-form, with tighter limits. You own `script.md` and the Shorts-specific parts of `seo:` for `format: short` items (IDs `CTK-S-xxxx`).

## When to use

- A Short is requested, or a sheet idea from the `Short` tab (CTK-S-0001 to CTK-S-0012) is picked.
- A long-form item should be cut into Shorts.
- QC flags a Short: runtime over target, hook too long, missing CTA, G4 or G6 findings.

## Inputs

| Read | Why |
|---|---|
| [CLAUDE.md](../../CLAUDE.md) | Repository rules |
| Workspace `brief.md`, `research.md`, `item.yaml` | One problem, one takeaway, verified claims |
| [strategy/content-pillars.md](../../strategy/content-pillars.md) | Shorts categories S1-S4 and their purpose |
| [strategy/audience-personas.md](../../strategy/audience-personas.md), [strategy/brand-voice.md](../../strategy/brand-voice.md) | Persona fit, tone, terminology |
| [templates/short-script.md](../../templates/short-script.md) | Format to keep |
| [workflows/script-production.md](../../workflows/script-production.md) | Shared scripting rules |
| [config/production.yaml](../../config/production.yaml), [config/platform-limits.yaml](../../config/platform-limits.yaml) | Speech rate, hook limit, Shorts platform limit |
| [youtube-scriptwriter](../youtube-scriptwriter/SKILL.md) and its [reference](../youtube-scriptwriter/reference.md) | The full format contract (identical for Shorts) |

## Shorts categories (from the sheet tab `Short`)

| Code | Category | Typical persona |
|---|---|---|
| S1 | Mẹo nhanh và thủ thuật | car-owner, technician |
| S2 | Giới thiệu sản phẩm/ thiết bị | garage-owner, technician |
| S3 | Hướng dẫn sửa chữa đơn giản | car-owner |
| S4 | Giải đáp thắc mắc thường gặp | car-owner |

The persona column holds the repository's starting defaults (`config/taxonomy.yaml` `pillar_defaults`), not sheet data. Confirm the persona in the brief.

## Targets

- **Duration**: under 60 seconds (sheet `'Short'!B2`, "< 60 giây"). YouTube accepts square or vertical uploads up to 3 minutes as Shorts, but the Cartek target is the sheet's. Going over needs `production.runtime_exception` with a rationale, reviewed by QC.
- **Narration budget**: at the assumed 220 syllables/min, a 4-segment Short with about 5 s of silent demo leaves roughly 190-200 narrated syllables. The rate is uncalibrated: measure with `python3 scripts/qc_content.py runtime <ID>`.
- **Hook**: the first segment, about 5 seconds or less (about 18 syllables).
- **Format**: vertical 9:16; keep on-screen text inside the central safe area, large and short.
- **CTA**: the sheet's Shorts CTA, "Cartek - Check your car", in the last segment.

## Procedure

1. If the item does not exist yet, ask [cartek-content-strategist](../cartek-content-strategist/SKILL.md) to scaffold it, or run it yourself:
   ```bash
   python3 scripts/new_content.py --list-ideas --format short
   python3 scripts/new_content.py --from-idea CTK-S-0010 --audience car-owner
   ```
2. Narrow to one problem and one takeaway. If the sheet title promises a list ("Top 3...", "3 mẹo..."), each point still needs a verified claim; consider one Short per point.
3. Write `script.md` from `templates/short-script.md`:
   - at least 3 hook candidates; the selected hook with rationale; an outline with at least 2 items;
   - segments: S01 `hook`, a `body` and/or `demo`, last `cta`; every segment has VO and VISUAL;
   - every technical sentence cites a claim; clearing codes always comes with the "it returns if the cause remains" caveat;
   - S3 repair Shorts: show only procedures backed by OEM-sourced claims. Mark hazards (hot engine, battery, lifting, fuel) for the fact-checker, and include a `SAFETY:` line when `safety.flags` is set.
4. Check timing and gates:
   ```bash
   python3 scripts/qc_content.py runtime <ID>
   python3 scripts/qc_content.py run <ID>
   ```
5. Shorts SEO (`item.yaml` `seo:`): at least 3 title candidates and a recommended title of at most 100 characters; a short description that states the takeaway; at least 3 tags; optional `hashtags` (each written as `#word`); at least 1 thumbnail concept. Shorts do not use chapters. Follow [youtube-seo-specialist](../youtube-seo-specialist/SKILL.md) for evidence and wording rules.
6. Storyboard is optional for Shorts (G7 does not require it); write one when the Short has a demo.

## Cutting a Short from a long-form item

1. Create a separate Short item: `python3 scripts/new_content.py --format short --title "<tiêu đề>" --pillar S1 --audience <persona>`. Every Short has its own ID, review and QC.
2. Reuse only claims that are `verified` in the long-form item: copy the claim and its sources into the Short's `item.yaml`. The fact-checker must confirm them again for the Short's scope.
3. Link both ways through `seo.related_content` (the Short lists the long-form ID; the long-form lists the Short).
4. Never cut a Short from a long-form item that is not approved: its claims may still change.

## Rules and hard constraints

- Same evidence rules as long-form: no invented facts, codes, compatibility or Cartek 2 features; feature claims need the register.
- No banned wording, no guarantees, no performance promises.
- Short does not mean simplified into something wrong: if a point cannot be said accurately in the time, drop it.
- Test items (`CTK-S-9xxx`) are never published.

## Output

- `script.md`, Shorts `seo:` fields and, when used, `storyboard.md` and `production.demo_setup` in the Short's workspace.

## Acceptance criteria

- [ ] One problem, one takeaway, stated in the brief.
- [ ] Runtime estimate under 60 s (or an exception with rationale); hook at or under about 5 s.
- [ ] First segment `hook`, last `cta` with "Cartek - Check your car"; every segment has VO and VISUAL.
- [ ] Every technical sentence cites a claim; caveats and safety lines present where needed.
- [ ] Shorts SEO complete (titles, description, tags, thumbnail); no chapters required.
- [ ] `qc_content.py run` shows G4 and G6 PASS.

## Example (illustrative only)

CTK-S-0010 "Đèn Check Engine sáng có phải là vấn đề nghiêm trọng?", persona `car-owner`. Claims C01 and C02 are unverified examples, not facts.

```markdown
### S01 — Hook

- **TYPE:** hook
- **VO:** Đèn check engine sáng: chạy tiếp hay dừng xe?
- **VISUAL:** Cận cảnh táp-lô, đèn sáng; khung dọc 9:16.
- **ON-SCREEN:** Sáng đứng hay nhấp nháy?
- **CLAIMS:**

### S02 — Phân biệt

- **TYPE:** body
- **VO:** Nếu đèn nhấp nháy, nên giảm tải và đưa xe đi kiểm tra sớm. Nếu đèn sáng đứng, hãy đọc mã lỗi để biết hệ thống nào được ghi nhận.
- **VISUAL:** Hai khung so sánh: đèn nhấp nháy và đèn sáng đứng.
- **ON-SCREEN:** Nhấp nháy = kiểm tra sớm
- **CLAIMS:** C01, C02

### S03 — Kêu gọi hành động

- **TYPE:** cta
- **VO:** Đọc mã trước khi đoán bệnh. Cartek - Check your car.
- **VISUAL:** Logo Cartek.
- **ON-SCREEN:** Cartek - Check your car
- **CLAIMS:**
```

## Hand-off

- [technical-fact-checker](../technical-fact-checker/SKILL.md) (stage TECHNICAL_REVIEW), then [content-qc-inspector](../content-qc-inspector/SKILL.md) (stage QC).
