# Script production

The script is both the narration a presenter reads and a machine-readable file. QC (gate G4) and the production package export parse it, so the conventions below are strict.

**Skills used:** [youtube-scriptwriter](../skills/youtube-scriptwriter/SKILL.md) for long-form, [shorts-content-specialist](../skills/shorts-content-specialist/SKILL.md) for Shorts. Brand rules: [strategy/brand-voice.md](../strategy/brand-voice.md) and [strategy/editorial-guidelines.md](../strategy/editorial-guidelines.md).

**Done when:** `script.md` has no `[TODO]` markers, gate G4 is PASS, the estimated runtime is inside the target, and every technical statement cites a claim ID.

## Targets

| Format | Template | Runtime target (source) | Aspect ratio |
|---|---|---|---|
| Long-form | [templates/long-form-script.md](../templates/long-form-script.md) | 5-8 phút = 300-480 s, inclusive (sheet `'Content Direction'!B3`) | 16:9 |
| Shorts | [templates/short-script.md](../templates/short-script.md) | < 60 giây = under 60 s, exclusive (sheet `'Short'!B2`) | 9:16 |

The targets are read from [data/normalized/channel.json](../data/normalized/channel.json) because [config/production.yaml](../config/production.yaml) sets `runtime_targets: from-source`. They are starting requirements, not fixed rules. A deliberate exception goes in `item.yaml` → `production.runtime_exception` with `min_seconds`, `max_seconds` and a rationale of at least 20 characters. QC then uses that range instead.

YouTube accepts vertical Shorts up to 3 minutes ([config/platform-limits.yaml](../config/platform-limits.yaml)), but Cartek's own Shorts target stays under 60 seconds.

## Machine-readable conventions

Rules enforced by [scripts/ctk/mdparse.py](../scripts/ctk/mdparse.py):

1. Keep the level-2 headings of the template. QC finds them by their English key, case-insensitive, at the start of the heading: `## Hook candidates`, `## Selected hook`, `## Outline`, `## Script` (all required) and `## Retention notes` (missing → warning).
2. Inside `## Script`, each segment is a level-3 heading: `### S01 — Title`. IDs are `S` plus two or three digits and must be unique.
3. Each segment holds field lines: `- **FIELD:** value`. A following line that is not a field continues the value, so a long VO can span several lines.
4. Unknown field names are a G4 FAIL. The known fields are:

| Field | Content |
|---|---|
| `TYPE` | `hook`, `intro`, `body`, `demo`, `safety`, `recap` or `cta` |
| `VO` | Voice-over in Vietnamese, exactly as it will be read |
| `VISUAL` | What is on screen: shot, device screen, action |
| `ON-SCREEN` | Short text overlay |
| `B-ROLL` | Cut-aways, animation, graphics |
| `CLAIMS` | Claim IDs from `item.yaml` this segment relies on, e.g. `C01, C02` |
| `DEMO-SECONDS` | Seconds of silent demonstration (number, default 0) |
| `SAFETY` | Safety warning spoken or shown here (required somewhere when `safety.flags` is set) |
| `NOTES` | Production notes, not exported as narration |

5. `## Selected hook` uses two fields: `- **HOOK:**` and `- **RATIONALE:**`.
6. `[TODO ...]` marks unfinished text. Any marker outside an HTML comment keeps G4 BLOCKED. Other placeholder wording in narration, on-screen or safety lines ("chờ xác minh", "bản nháp", "TBD", "XXX", "lorem ipsum", "placeholder"; `draft_markers` in [config/qc-policy.yaml](../config/qc-policy.yaml)) also keeps G4 BLOCKED, so it never reaches the export.
7. HTML comments (`<!-- ... -->`) are guidance. QC ignores them and they are not part of the content fingerprint.

Example segment:

```markdown
### S01 — Hook

- **TYPE:** hook
- **VO:** Xe rung giật khi chờ đèn đỏ, máy chẩn đoán báo P0300. Mã này cho biết điều gì, và điều gì nó không nói?
- **VISUAL:** Cận cảnh màn hình máy chẩn đoán hiển thị mã lỗi.
- **ON-SCREEN:** P0300 = ?
- **CLAIMS:** C01
```

Any DTC that appears in narration, on-screen text or SEO text must also appear in the text of a claim that is not `removed`. Otherwise G5 FAILs.

## Procedure

1. Re-read `brief.md`: audience, problem, takeaway, angle, scope, risks.
2. Write at least three hook candidates under `## Hook candidates`. Each is one or two sentences: a symptom the viewer recognises, the cost of ignoring it, or the result the demo will show.
3. Choose one. Write the final hook text and the reason under `## Selected hook`. The reason names the primary persona and the search intent.
4. Write the outline: at least 3 items for long-form, 2 for Shorts.
5. Write the segments. Start with `TYPE: hook`, end with `TYPE: cta`. Long-form needs at least 4 segments; Shorts at least 2.
6. Give every segment a `VO` and a `VISUAL`. A silent demo may have no VO when `DEMO-SECONDS` is above 0.
7. Cite claim IDs in `CLAIMS` wherever a segment states a technical fact. Do not add facts that are not claims.
8. When the item has safety flags, add a `TYPE: safety` segment or `SAFETY:` lines where the risk occurs.
9. Write the CTA. It must contain the brand line `Cartek - Check your car` in the VO or on-screen text.
10. Fill `## Retention notes`.
11. Check runtime and gates, then move the stage on:

```bash
python3 scripts/qc_content.py runtime <ID>
python3 scripts/qc_content.py run <ID>
python3 scripts/set_status.py <ID> --stage TECHNICAL_REVIEW --note "Script complete"
```

## Long-form structure (5-8 minutes)

The template proposes seven segments. Adapt them to the topic.

| Segment | Type | Purpose |
|---|---|---|
| S01 Hook | hook | The problem in the viewer's words. About 15-30 s. |
| S02 Giới thiệu và lời hứa | intro | What the viewer will be able to do or understand. |
| S03 Giải thích | body | The concept, at the persona's technical depth. |
| S04 Demo thực tế | demo | The procedure on a real vehicle or the device. Verified Cartek 2 features only. |
| S05 Lỗi thường gặp khi chẩn đoán | body | Common mistakes and limits; where code and root cause differ. |
| S06 Tóm tắt | recap | Three or fewer takeaways. |
| S07 Kêu gọi hành động | cta | CTA with the brand line. |

## Shorts structure (under 60 seconds)

One problem, one takeaway.

| Segment | Type | Purpose |
|---|---|---|
| S01 Hook | hook | Spoken in about 3 seconds; strong opening frame. |
| S02 Nội dung chính | body | The one insight. |
| S03 Kết quả | demo | The visible result. |
| S04 Kêu gọi hành động | cta | `Cartek - Check your car`. |

## Runtime calculation

[scripts/ctk/mdparse.py](../scripts/ctk/mdparse.py) estimates runtime from the actual narration:

1. Count syllables in each segment's VO. Vietnamese writes one syllable per space-separated token. Tokens with digits, and upper-case acronyms of 2-5 letters, count one syllable per character ("P0300" = 5, "OBD2" = 4, "ECU" = 3).
2. VO seconds = syllables ÷ speech rate × 60.
3. Add `DEMO-SECONDS`.
4. Add a transition gap between segments (not after the last one).

Current values in [config/production.yaml](../config/production.yaml):

| Setting | Long-form | Shorts |
|---|---|---|
| `speech_rate_syllables_per_minute` | 200 | 220 |
| `segment_transition_seconds` | 1.0 | 0.3 |
| `hook_max_seconds` (warning above) | 30 | 5 |

These rates are planning assumptions. `speech_rate_calibrated` is `false`. Narration that still contains `[TODO` counts as zero.

### Calibrating the speech rate

1. Take three real recorded Cartek voice-overs of the same format.
2. For each, count the syllables of the narration that was actually read (`python3 scripts/qc_content.py runtime <ID>` prints them per segment when the script is in a workspace).
3. Measure the spoken duration in minutes, excluding silent demonstration.
4. Rate = total syllables ÷ total minutes. Average the three.
5. Update `speech_rate_syllables_per_minute` for that format, set `speech_rate_calibrated: true`, and note the change in `CHANGELOG.md`.

## Retention techniques

Write them where they happen and list them under `## Retention notes`.

- **Open loop:** promise an answer early ("cuối video là cách kiểm tra nhanh nhất") and pay it off later.
- **Pattern change:** switch between presenter, device screen and B-roll at least every segment.
- **Show, then explain:** start a demo segment with the visible result.
- **Concrete stakes:** what happens if the viewer ignores the symptom, stated only from verified claims.
- **Payoff check:** every promise in the hook or intro is delivered before the CTA.

## CTA rules

- The last segment is `TYPE: cta`.
- It contains `Cartek - Check your car` (G4 checks this, ignoring accents and case).
- Long-form: the sheet CTA asks viewers to comment for advice, like, subscribe and turn on notifications. The sheet spells "subcribe"; write "subscribe" ([strategy/brand-voice.md](../strategy/brand-voice.md)).
- Shorts: `Cartek - Check your car` alone is the sheet CTA.
- Adapt the CTA to the persona (see [strategy/audience-personas.md](../strategy/audience-personas.md)).

## What QC checks (G4)

[scripts/ctk/qc.py](../scripts/ctk/qc.py) → `gate_g4`:

- `script.md` exists (else BLOCKED); required sections present and parse problems absent (else FAIL).
- No `[TODO]` markers (else BLOCKED).
- At least 3 hook candidates; selected hook and rationale; outline of at least 3 items (long-form) or 2 (Shorts) (else FAIL).
- At least 4 segments (long-form) or 2 (Shorts); each with a valid `TYPE`, a `VO` (unless a silent demo), a `VISUAL`, and a numeric `DEMO-SECONDS` (else FAIL).
- First segment `hook`, last segment `cta`, CTA contains the brand line (else FAIL).
- Estimated runtime inside the target or the recorded exception (else FAIL).
- Hook longer than `hook_max_seconds`, or no retention notes: warnings.

Clarity, coherence and retention quality also need an independent `qc` review ([content-qc-inspector](../skills/content-qc-inspector/SKILL.md)). G5 checks the public wording of the script; see [technical-review.md](technical-review.md).
