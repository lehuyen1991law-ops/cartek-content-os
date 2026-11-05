# Post-publish analysis

Real performance data, read from YouTube Studio, turned into insights and actions for the next videos.

**Skills used:** [cartek-content-strategist](../skills/cartek-content-strategist/SKILL.md) for insights and actions; [youtube-seo-specialist](../skills/youtube-seo-specialist/SKILL.md) for title, thumbnail and search findings.

**Done when:** `performance.yaml` validates against [schemas/performance.schema.json](../schemas/performance.schema.json) with at least one snapshot of real data, insights cite their evidence, actions have owners, and the item is at `PERFORMANCE_REVIEW`.

## Rules

1. Only real numbers, copied from YouTube Studio, its export, or the YouTube Analytics API. Never estimate, extrapolate, round up or fill gaps.
2. A metric you do not have is left out or `null`. It is never guessed.
3. Every snapshot names its source and its evidence: a path or link to the export or screenshot. Keep private exports outside Git.
4. Competitor figures in [data/normalized/competitors.json](../data/normalized/competitors.json) are historical and unverified. Do not use them as benchmarks.
5. No conclusion from one video alone is "high" confidence.

## When to collect

| Window (`window`) | When to read it | Typical use |
|---|---|---|
| `first-48-hours` | 2 days after publishing | Hook and thumbnail: impressions, CTR, early retention |
| `first-7-days` | 7 days after | Retention curve, traffic sources |
| `first-28-days` | 28 days after | Search and suggested traffic, subscribers gained |
| `lifetime` | any later date | Long-tail search performance |
| `custom` | any other range | Explain it in `window_note` |

## Procedure

1. Copy [templates/performance.yaml](../templates/performance.yaml) into the workspace as `performance.yaml`.
2. Set `content_id` and `video_url` (the URL recorded in `item.yaml` → `publication.url`).
3. Open the video in YouTube Studio → Analytics. Choose the window.
4. Add a snapshot:
   - `captured_on`: today, `YYYY-MM-DD`.
   - `window`, and `window_note` for `custom`.
   - `source`: `youtube-studio`, `youtube-studio-export` or `youtube-analytics-api`.
   - `evidence`: where the export or screenshot is stored.
   - `entered_by`: your name.
   - `metrics`: copy exactly what Studio shows. Allowed keys: `views`, `watch_time_hours`, `average_view_duration_seconds`, `average_percentage_viewed`, `impressions`, `impressions_ctr_percent`, `subscribers_gained`, `likes`, `comments`, `shares`.
   - `retention_notes`: where viewers drop off, read from the retention graph, with timestamps.
   - `traffic_sources_notes`: search terms, suggested videos, external sources.
5. Map drop-off timestamps to script segments with the estimate from `python3 scripts/qc_content.py runtime <ID>`, then correct with the real edit.
6. Write insights. Each has an `observation`, its `evidence` (snapshot, metric, timestamp) and a `confidence` of `low`, `medium` or `high`.
7. Write actions. Each has an `action`, `applies_to` (content IDs or `future`), an `owner` and a `status` (`proposed`, `accepted`, `done`, `rejected`).
8. Validate and move the stage:

```bash
python3 scripts/validate_content.py
python3 scripts/set_status.py <ID> --stage PERFORMANCE_REVIEW --by "<name>"
```

   `set_status.py` refuses unless the item is published and `performance.yaml` validates. `validate_content.py` reports `performance.yaml` on an unpublished item as an error.

Example snapshot (structure only; every number must come from Studio):

```yaml
content_id: CTK-L-0015
video_url: "https://youtu.be/<video-id>"
snapshots:
  - captured_on: "YYYY-MM-DD"
    window: first-7-days
    window_note: ""
    source: youtube-studio
    evidence: "<link to the Studio export in shared storage>"
    entered_by: "<name>"
    metrics:
      views: null
      average_percentage_viewed: null
      impressions_ctr_percent: null
    retention_notes: "<timestamps where the graph drops, read from Studio>"
    traffic_sources_notes: ""
insights: []
actions: []
```

## Feeding results back

1. **Briefs.** The strategist reads `performance.yaml` of related items before writing a new brief in the same pillar.
2. **Hooks and structure.** A drop in the first 30 seconds points at the hook. A drop at a segment points at its pacing or relevance. Record the finding as an insight, then as an action for future scripts.
3. **Titles and thumbnails.** Low impressions CTR with good retention points at packaging, not content. Test a new title or thumbnail only as an action with an owner. Applying it changes the published metadata, so it goes through re-approval ([publishing.md](publishing.md#corrections-after-publishing), case B); record the date of the change in the action so later snapshots can be compared.
4. **Strategy.** Patterns across several items go into [strategy/content-pillars.md](../strategy/content-pillars.md) or [strategy/audience-personas.md](../strategy/audience-personas.md) with links to the evidence, through a pull request.
5. **Speech rate.** The measured runtime of real voice-overs calibrates `config/production.yaml` ([script-production.md](script-production.md#calibrating-the-speech-rate)).

Never rewrite the script of a published item to "match" results: it records what was approved and published. Factual corrections are logged in `item.yaml` → `corrections`; metadata changes go through re-approval. Both follow [publishing.md](publishing.md#corrections-after-publishing).
