# P0300 dual demo — pre-production package

Two demo videos on P0300 built from the knowledge and claim register of
[CTK-L-0015](../../../content/long-form/CTK-L-0015-loi-p0300-ac-mong-cua-moi-dong-co/item.yaml) with a different structure:

- **Video A "Cartek Long"** — 16:9, 3:00, explainer with a pattern interrupt and a five-step procedure.
- **Video B "Cartek Short"** — 9:16, 0:59, one problem, one takeaway.

Audience is mixed (Cartek users, garage technicians, car owners): register "các bạn", plain but technically exact.
These are **demos, not content items**: no ID from `data/id-registry.json`, no QC record, and every cited claim is still
`unverified` (CLAUDE.md §10: not publishable until the technical-fact-checker verifies them).

## Files

| File | What it is |
|---|---|
| `long-script.md` | Video A script in the machine-readable segment format (`scripts/ctk/mdparse.parse_script` reads it), 9 segments with planned time ranges in the titles. |
| `short-script.md` | Video B script, same format, 6 segments. |
| `claims-map.md` | Every technical sentence of both scripts → claim IDs C01–C13; sentences rewritten or removed. |
| `pronunciation.md` | Spoken forms for codes and terms (P0300 = "pê không ba trăm"), TTS text column, fallbacks. |
| `shotlist-long.csv` / `shotlist-short.csv` | Shot lists: timing, VO excerpt, real footage vs motion graphic, English footage search keywords, effect ids, on-screen text, SFX cue, BGM note. |
| `sfx-bgm-cuesheet.md` | Cue list with timestamps and loudness guidance (VO −16 LUFS, BGM −28 to −24 LUFS under VO, SFX ≤ −6 dBTP). |
| `timing.json` | Syllable counts and measured TTS durations (numbers only). |
| `voice-demo-notes.md` | What was rendered with edge-tts, file names, and the human listening check still required. |

Voice demo audio lives outside the repository (`.gitignore` excludes mp3/wav/mp4); paths are in `voice-demo-notes.md`.

## Effect ids used

Existing ids come from [`config/visual-style.yaml`](../../../config/visual-style.yaml) (hard-cut, soft-dissolve, code-popup,
highlight-circle, highlight-arrow, zoom-punch, lower-third, safety-banner, freeze-frame-snapshot, checklist-tick,
sfx-whoosh, sfx-ui-click, sfx-ui-beep, sfx-low-thud). The shot lists also use **five additional ids** that the library does not
have yet. They are proposals for the brand team; if adopted they go into `config/visual-style.yaml` → `effects` first
(G7 warns on unknown ids in a real storyboard).

| Proposed id | Kind | Description | When to use | Never use |
|---|---|---|---|---|
| `kinetic-typography` | vfx | One short sentence (typography role `callout`, 1–2 lines) builds word by word with a quick ease-out; the key word lands last and holds. Sentence case, Be Vietnam Pro 600; keeps inside the title-safe area. | Pattern interrupts and the closing takeaway: "Mã lỗi ≠ nguyên nhân", "P0300 là điểm bắt đầu...". At most 3 per video. | Never for a whole paragraph; never with letter-by-letter "typewriter" sounds; never for a safety warning (safety-banner carries those). |
| `mask-reveal` | vfx | A card or tile is revealed by a wipe mask (left→right in 16:9, top→bottom in 9:16) over the footage behind it, about 10 frames, paired with sfx-whoosh. | Lists revealed item by item in sync with the voice (the four cause groups). | Never faster than the narration names the item; never to reveal a code the claim register does not define. |
| `animated-comparison` | vfx | Two columns (16:9) or two stacked halves (9:16) with a thin divider; both sides animate in sequence and the differing element is highlighted in `accent_code`. | "P0300 vs P0301", "cùng bệnh, khác mã", "PHÁT HIỆN LỖI ↔ XÁC NHẬN NGUYÊN NHÂN". | Never with contradicting readings next to a real tool screen; never more than two sides. |
| `ui-callout` | vfx | A rounded rectangle in `accent_code` boxes one element of a scan-tool UI or a graphic (a button, a row), with an optional short label in `caption` size and a cross for "do not". | Pointing at "Xóa mã", "Đọc mã", a freeze frame row, "thứ tự xi-lanh: theo tài liệu hãng". | Never on a value the narration does not name; never covers the element it boxes. |
| `branded-ending` | vfx | End card: Cartek logo slides in on the left, brand line "Cartek - Check your car" in typography role `end_screen`, background from the last shot blurred; right half stays free for YouTube end-screen elements (16:9). In 9:16 the logo is centred with a follow prompt below. 4–6 s, pairs with sfx-whoosh. | The last shot of every demo. | Never with a capability statement about Cartek 2 (feature register is empty); never with a sound louder than the whoosh. |

`mechanical-accent` in the cue sheet is not an effect: it marks the real sound of the footage (a connector click, a coil clip)
kept at natural level, as `sound_rules` require.

## Checks run

- `python3 scripts/validate_content.py` and `python3 scripts/check_links.py` pass with this folder present (text files only).
- Both scripts parse with `scripts/ctk/mdparse.parse_script` (no problems, no TODOs).
- Syllables counted with `scripts/ctk/textutil.count_syllables`; durations measured with ffprobe on edge-tts renders (`timing.json`).
