---
name: youtube-seo-specialist
description: Builds the YouTube SEO package for a Cartek video or Short. Covers search intent, evidence-based keyword notes, title candidates and the recommended title with rationale, description, tags within YouTube's limits, chapters from the measured script timing, thumbnail concepts, related internal content and the publishing checklist. Never promises CTR, rankings or views. Use at stage SEO, when QC gate G6 is not PASS, or to propose changes from real post-publication data.
---

# YouTube SEO specialist

## Purpose

Make each video findable and accurately represented on YouTube. You own `seo.md` (analysis, evidence, checklist) and the `seo:` block of `item.yaml` (the final metadata that gets published and exported). Gate **G6 (SEO package completeness)** checks your work; gate **G8** later checks the publishing checklist.

## When to use

- Stage SEO: script finished, technical review done.
- QC reports G6 FAIL or BLOCKED.
- After publication, when `performance.yaml` holds real YouTube Studio data and a title or thumbnail change is being considered.

## Inputs

| Read | Why |
|---|---|
| [CLAUDE.md](../../CLAUDE.md) | Repository rules |
| Workspace `brief.md`, `script.md`, `item.yaml` (`keywords`, `search_intent`, `audience`, `claims`) | What the video actually says and for whom |
| [strategy/competitor-analysis.md](../../strategy/competitor-analysis.md) | Competitor keywords recorded in the sheet (historical) |
| [strategy/brand-voice.md](../../strategy/brand-voice.md) | Terminology and tone |
| [workflows/seo-optimization.md](../../workflows/seo-optimization.md) | Process |
| [config/platform-limits.yaml](../../config/platform-limits.yaml) | Title, description, tags and chapter limits with sources |
| [config/qc-policy.yaml](../../config/qc-policy.yaml) | `performance_claim_patterns`, minimum counts |
| [templates/seo-package.md](../../templates/seo-package.md) | Required sections |

## Procedure

1. Start the stage: `python3 scripts/set_status.py <ID> --stage SEO --by "<tên>"`.
2. **Search intent** (`seo.md`): what the viewer types or asks, in their words, and which intent from `config/taxonomy.yaml` applies. It must match `item.yaml` `search_intent`.
3. **Keyword notes** (`seo.md` table): every keyword with its evidence and date: YouTube search suggestions you observed, competitor keywords from the sheet, viewer questions, or search terms from YouTube Studio for existing Cartek videos. Never write a search volume or difficulty score unless you attach the tool export it came from.
4. **Titles**: at least 3 candidates in `seo.title_candidates` (and the `seo.md` list). Choose `seo.recommended_title`:
   - at most 100 characters (YouTube limit); aim for 70 or fewer so it is not truncated;
   - primary keyword early, natural Vietnamese, accurate to what the video delivers;
   - no clickbait that the video does not pay off, no claims beyond verified claims.
   Explain the choice in `seo.title_rationale` and in `## Title rationale`.
5. **Description** (`seo.description`, at most 5,000 characters):
   - first two lines: the problem and the takeaway;
   - a short summary of what the video covers;
   - no timestamps: the export appends one line per `seo.chapters` entry (long-form) as `seo.description_with_chapters`;
   - no technical statement that is not a verified claim; no invented links.
6. **Tags** (`seo.tags`, at least 3): the total must stay at or under 500 characters as YouTube counts them (commas between tags count; a tag containing a space counts 2 extra characters for quotes). YouTube's help pages say tags play a minor role in discovery, useful mainly for common misspellings, so keep them few and relevant. Do not use competitor brand names unless the video genuinely covers them.
7. **Chapters** (long-form only, `seo.chapters`): take start times from the runtime table:
   ```bash
   python3 scripts/qc_content.py runtime <ID>
   ```
   Rules: first chapter `00:00`, at least 3 chapters, each at least 10 seconds, ascending, and the last chapter starting at least 10 seconds before the estimated end. Titles are short Vietnamese phrases. Re-check chapters whenever the script changes. Do not put timestamps in `seo.description`: the export appends the chapter lines (`seo.description_with_chapters`) and G6 checks the combined length against 5,000 characters.
8. **Thumbnails** (`seo.thumbnail_concepts`; at least 2 for long-form, 1 for Shorts): `concept` describes the image; `on_image_text` stays around 4-5 words, readable on a phone. Show only what the video shows; Cartek 2 appears only doing verified register features.
9. **Related content** (`seo.related_content`): registered content IDs (existing workspaces or sheet ideas) for cards, end screens and the description. **Pinned comment** (`seo.pinned_comment`): a question that invites the persona's real cases.
10. Tick the **Publishing checklist** in `seo.md` (pre-approval items) only for what is true now; gate G8 blocks approval until all are ticked. Upload-time steps belong to `item.yaml` → `publication.upload_checklist`, ticked by the uploader.
11. Check and hand over:
    ```bash
    python3 scripts/qc_content.py run <ID>
    python3 scripts/set_status.py <ID> --stage PRODUCTION_PACKAGE --by "<tên>"
    ```
    G6 must be PASS. Fix every limit or wording finding; warnings (long title, keyword missing from title and description) need a conscious decision noted in the rationale.

## Rules and hard constraints

- Never promise or predict CTR, ranking, views, "viral", "lên top" or "triệu view". QC fails these phrases (`performance_claim_patterns`).
- Never fabricate search volumes, competitor statistics or YouTube metrics. Competitor numbers from the sheet are historical and unverified.
- Metadata must describe the video truthfully; misleading metadata breaks YouTube's spam and deceptive-practices policies.
- Post-publication changes use real `performance.yaml` data only. Record proposals as `actions` in `performance.yaml` first. Editing the `seo:` block of a published item changes the content fingerprint, so it goes through QC reviews and a re-approval (`qc_content.py approve` keeps the PUBLISHED stage) before it is applied ([workflows/publishing.md](../../workflows/publishing.md#corrections-after-publishing)).
- Do not edit the script, claims or reviews.

## Output

- `seo.md` complete without `[TODO]`; pre-approval checklist ticked only where true.
- `item.yaml` `seo:` block: `title_candidates`, `recommended_title`, `title_rationale`, `description`, `tags`, optional `hashtags`, `chapters` (long-form), `thumbnail_concepts`, `related_content`, `pinned_comment`.

## Acceptance criteria

- [ ] Search intent stated and consistent with `item.yaml`.
- [ ] Every keyword has dated evidence; no unsourced numbers.
- [ ] At least 3 title candidates; recommended title at most 100 characters, with rationale.
- [ ] Description opens with problem and takeaway, has no timestamps, and stays within 5,000 characters together with the chapter lines (long-form).
- [ ] Tags at most 500 characters as YouTube counts them.
- [ ] Chapters valid against the current runtime (long-form).
- [ ] Thumbnail concepts with short on-image text.
- [ ] No performance promises anywhere; `qc_content.py run` shows G6 PASS.

## Example (illustrative only)

CTK-L-0015, persona `technician`. Keywords are hypotheses until observed evidence is recorded; times come from a hypothetical runtime table.

```yaml
seo:
  title_candidates:
    - "Lỗi P0300 là gì? Khoanh vùng nguyên nhân bỏ máy từng bước"
    - "P0300: Xóa lỗi rồi vẫn sáng lại? Chẩn đoán đúng cách"
    - "Bỏ máy ngẫu nhiên P0300: quy trình chẩn đoán cho thợ"
  recommended_title: "Lỗi P0300 là gì? Khoanh vùng nguyên nhân bỏ máy từng bước"
  title_rationale: "Từ khóa chính ở đầu; hứa hẹn đúng nội dung (quy trình), không phóng đại."
  tags: ["lỗi P0300", "bỏ máy", "đèn check engine", "chẩn đoán OBD2", "Cartek"]
  chapters:
    - {time: "00:00", title: "Vì sao P0300 sáng lại"}
    - {time: "00:40", title: "P0300 nghĩa là gì"}
    - {time: "01:55", title: "Lưu freeze frame"}
    - {time: "03:20", title: "Khoanh vùng nguyên nhân"}
    - {time: "05:30", title: "Tóm tắt"}
  thumbnail_concepts:
    - {concept: "Màn hình máy chẩn đoán hiện P0300 cạnh bugi và bô-bin", on_image_text: "P0300: tìm đúng bệnh"}
    - {concept: "Đèn check engine trên táp-lô, mũi tên tới 4 nhóm nguyên nhân", on_image_text: "Đừng chỉ xóa lỗi"}
```

`seo.md` keyword-notes row format (fill in what you actually observed): `| lỗi P0300 | primary | <evidence, e.g. YouTube search suggestion seen when typing "lỗi p03"> | <YYYY-MM-DD> |`.

## Hand-off

- Stage PRODUCTION_PACKAGE: storyboard (with effects and text styles from `config/visual-style.yaml`), assets and the draft export (`python3 scripts/export_package.py <ID> --draft`).
- Then the independent [content-qc-inspector](../content-qc-inspector/SKILL.md) at stage QC.
