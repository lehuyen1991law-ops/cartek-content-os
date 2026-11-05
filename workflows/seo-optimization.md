# SEO optimization

The SEO package makes a finished script findable without overpromising. Final values live in `item.yaml` → `seo`. The analysis, the evidence and the publishing checklist live in `seo.md` ([templates/seo-package.md](../templates/seo-package.md)).

**Skills used:** [youtube-seo-specialist](../skills/youtube-seo-specialist/SKILL.md).

**Done when:** gate G6 is PASS, every keyword choice in `seo.md` has evidence, and the pre-approval checklist in `seo.md` is ticked only for what is actually true (G8). Upload-time steps live in `item.yaml` → `publication.upload_checklist` ([publishing.md](publishing.md)).

## Rules

1. Never claim or imply a CTR, a ranking, a view count or virality. G6 FAILs on such wording (see the list below).
2. Never invent search volumes or keyword data. Record where each keyword came from and when you observed it.
3. Titles and thumbnails must match what the video delivers. No clickbait that the script does not pay off.
4. Use only verified claims in titles, descriptions and thumbnail text. G5 scans SEO text for DTCs and banned wording too.
5. Platform limits come from [config/platform-limits.yaml](../config/platform-limits.yaml), verified on 2026-11-05 against YouTube Help and the YouTube Data API documentation. Re-verify before relying on them.

## Platform limits

| Item | Limit | Source |
|---|---|---|
| Title | 100 characters (QC warns above 70: long titles get truncated) | https://support.google.com/youtube/answer/57404 |
| Description | 5,000 characters | https://support.google.com/youtube/answer/57404 |
| Tags | 500 characters in total, as YouTube counts them: commas between tags count, and a tag containing a space counts 2 extra characters for its quotes | https://developers.google.com/youtube/v3/docs/videos |
| Chapters | First timestamp 00:00, at least 3 timestamps in ascending order, each chapter at least 10 seconds | https://support.google.com/youtube/answer/9884579 |
| Shorts | Square or vertical uploads up to 3 minutes count as Shorts; Cartek's own target stays under 60 s | https://support.google.com/youtube/answer/15424877 |

## Procedure

1. **Search intent.** Write what the viewer types or asks, and which intent applies, under `seo.md` → "Search intent". Intents: `informational`, `how-to`, `troubleshooting`, `comparison`, `product`, `news` ([config/taxonomy.yaml](../config/taxonomy.yaml)). Keep `item.yaml` → `search_intent` consistent.
2. **Keyword evidence.** Fill the "Keyword notes" table with keyword, role (primary/secondary), evidence and date observed. Acceptable evidence:
   - YouTube search suggestions you observed, with the date.
   - Competitor titles and keywords in [data/normalized/competitors.json](../data/normalized/competitors.json) and [strategy/competitor-analysis.md](../strategy/competitor-analysis.md). Those figures are historical and unverified; use them for wording, not for numbers.
   - Real viewer comments or questions.
   Set `item.yaml` → `keywords.primary` and `keywords.secondary`.
3. **Titles.** Write at least three candidates in `item.yaml` → `seo.title_candidates` (mirror them in `seo.md` → "Title candidates"). Put the problem and the primary keyword early. Pick one as `seo.recommended_title` (at most 100 characters) and explain the choice in `seo.title_rationale` and `seo.md` → "Title rationale".
4. **Description.** Write `seo.description` (at most 5,000 characters). The first two lines state the problem and the takeaway. Use the primary keyword naturally; QC warns when it is in neither title nor description.
5. **Tags.** At least 3 tags in `seo.tags`, at most 500 characters as YouTube counts them. Optional hashtags go in `seo.hashtags`, each starting with `#`.
6. **Chapters (long-form).** Get segment start times from the narration estimate and build `seo.chapters`:

```bash
python3 scripts/qc_content.py runtime <ID>
```

```yaml
chapters:
  - {time: "00:00", title: "Mở đầu"}
  - {time: "00:45", title: "Mã lỗi nói gì"}
  - {time: "02:30", title: "Kiểm tra trên xe"}
```

   The first chapter is 00:00; at least 3 entries; each at least 10 s; the last one starts at least 10 s before the estimated end. YouTube creates chapters from timestamps in the description. Keep timestamps out of `seo.description`: the export appends one line per chapter and provides the paste-ready `seo.description_with_chapters`, and G6 checks that the combined text fits 5,000 characters (see [publishing.md](publishing.md)).
7. **Thumbnails.** At least 2 concepts for long-form, 1 for Shorts, in `seo.thumbnail_concepts` (`concept`, `on_image_text`). Keep on-image text to about 4-5 words; QC warns above 6 words.
8. **Related content.** List registered content IDs in `seo.related_content` (end screens, cards, playlists). Unknown IDs FAIL. Write "none yet" in `seo.md` when there are none.
9. **Pinned comment.** Optional draft in `seo.pinned_comment`.
10. **Checklist.** Work through `seo.md` → "Publishing checklist" (pre-approval items) and tick (`[x]`) each item only when it is true. Gate G8 stays BLOCKED until every box is ticked. Do not tick upload steps here: they are in `publication.upload_checklist`.
11. Run QC and move on:

```bash
python3 scripts/qc_content.py run <ID>
python3 scripts/set_status.py <ID> --stage PRODUCTION_PACKAGE --note "SEO package complete"
```

## Performance-claim wording that FAILs

[config/qc-policy.yaml](../config/qc-policy.yaml) → `performance_claim_patterns` (matched without accents): "CTR", "lên/lọt/vào top", "triệu view", "triệu lượt xem", "viral", "top 1", "chắc chắn được đề xuất / lên xu hướng". The check covers the public SEO fields and `seo.md`, outside HTML comments and `[TODO]` prompts.

## What QC checks (G6)

[scripts/ctk/qc.py](../scripts/ctk/qc.py) → `gate_g6`:

- `seo.md` exists (else BLOCKED), has "Search intent", "Keyword notes", "Title rationale", "Publishing checklist" (else FAIL), and no `[TODO]` markers (else BLOCKED).
- The public SEO fields in `item.yaml` (titles, description, tags, thumbnail text, pinned comment) contain no placeholder wording (`draft_markers`, including `[TODO`) (else BLOCKED).
- Missing or invalid chapters are BLOCKED while the narration is unfinished (no timing exists yet) and FAIL once it is finished.
- At least 3 title candidates; a recommended title of at most 100 characters; a title rationale (else FAIL). Over 70 characters: warning.
- A description of at most 5,000 characters (else FAIL).
- At least 3 tags within 500 characters as YouTube counts them (else FAIL).
- Long-form chapters valid as above (else FAIL).
- Enough thumbnail concepts (else FAIL); long on-image text: warning.
- No performance claims (else FAIL).
- Primary keyword in neither title nor description: warning.
- Related content IDs registered (else FAIL).

G8 checks the checklist, the target date and the visibility plan; see [publishing.md](publishing.md).
