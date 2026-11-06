# SFX and BGM cue sheet — P0300 dual demo

Sound rules come from `config/visual-style.yaml` → `sound_rules` and the brand voice ("calm about faults"): no alarmist
sound design, no sirens, no fake engine-failure sounds, SFX never over a spoken word, music ducked under the voice and
silent under safety warnings. SFX ids are the library ids (`sfx-ui-click`, `sfx-ui-beep`, `sfx-whoosh`, `sfx-low-thud`)
plus one proposed accent (`mechanical-accent`, see README.md).

## Loudness targets

| Element | Target | Notes |
|---|---|---|
| Voice-over (final mix reference) | **−16 LUFS integrated**, true peak ≤ −1 dBTP | YouTube normalises to about −14 LUFS; a −16 LUFS VO-led mix keeps headroom and stays natural. Short-term loudness of the VO should stay within ±3 LU; use gentle compression (2:1), no brick-wall limiting on the voice. |
| BGM under VO | **−28 to −24 LUFS** (short-term), i.e. about −18 LU below the voice | Sidechain or manual ducking: −18 LU under speech, attack 150 ms, release 600–800 ms so the bed breathes in sentence pauses but never pumps. In VO-free holds (shot 3 of the Long, end cards) the bed may rise to −22 LUFS. |
| BGM under a safety banner | **silent** (full fade-out 1.5–2 s before the banner, fade-in 1 s after) | Long shots 10–11 and 31. The low-thud is the only sound cue on a banner. |
| SFX | **peaks ≤ −6 dBTP**, typical −20 to −16 dBFS as the library states | ui-click about −20 dBFS, ui-beep about −20 dBFS, whoosh about −18 dBFS, low-thud about −16 dBFS. An SFX starts after the word ends or sits in a pause. |
| Dialogue/mechanical accents (real tool or engine sound) | kept at natural level, ≤ −12 dBFS | Never dubbed in to make a fault sound worse. |
| Final programme | about −15 to −14 LUFS integrated, true peak ≤ −1 dBTP | Measure with a loudness meter on the full mix; do not master louder than −14 LUFS. |

## BGM choice

- One bed per video, steady tempo, no risers or trailer hits. Long: calm mid-tempo electronic/acoustic bed (about 90–100 BPM).
  Short: brighter, slightly faster bed (about 110–120 BPM) that resolves cleanly at 00:59 so the loop point is clean.
- Licence: royalty-free with written proof of licence stored outside Git; record track name and licence in the storyboard
  of the release item. No track name is fixed here.
- Music ducking is under VO everywhere; the only full stops are the safety banners (Long) and the 0.5 s silence after "Khoan đã!".

## Video A — Long (3:00)

| Time | Shot | Cue | Element | Level / behaviour |
|---|---|---|---|---|
| 00:00.0 | 1 | Intro bed in | BGM | Fade in 0.5 s to −26 LUFS; duck −18 LU under VO from the first word |
| 00:00.8 | 1 | P0300 code-popup | sfx-ui-beep | Single beep after "P0300" is spoken, −20 dBFS |
| 00:06.2 | 3 | "Khoan đã!" lands | sfx-low-thud | One soft thud at the end of the word, −16 dBFS |
| 00:06.5–00:07.0 | 3 | Hold | BGM | Bed drops to silence for 0.5 s |
| 00:07.0 | 4 | Kinetic typography | sfx-whoosh | Light whoosh under −18 dBFS on the ≠ landing, in the pause before the next sentence |
| 00:07.0 | 4 | Main bed in | BGM | −26 LUFS, ducked under VO |
| 00:17.5 | 6 | Empty box reveal | sfx-ui-click | After "bỏ máy?" |
| 00:30.5 | 9 | Code card | sfx-ui-beep | After "mã lỗi" |
| 00:33.0 | 9 | Freeze frame snapshot | shutter (effect sound) | Built into freeze-frame-snapshot; keep ≤ −18 dBFS |
| 00:39.0 | 10 | Pre-banner | BGM | Fade out over 2 s to silence |
| 00:41.0 | 11 | Safety banner entry | sfx-low-thud | One thud; no other sound under the warning |
| 00:50.0 | 12 | Post-banner | BGM | Fade in 1 s to −28 LUFS |
| 00:55.5 | 13 | P0301 lands on cylinder 1 | sfx-ui-beep | After "P0312" is spoken |
| 01:19.0 / 01:22.0 / 01:25.0 / 01:28.0 | 18–21 | Four group cards | sfx-whoosh ×4 | Each in the pause between list items |
| 01:44.0 | 23 | Lamp back on | sfx-low-thud | After "quay lại" |
| 01:45.5 | 24 | "Năm bước" list builds | sfx-whoosh | |
| 01:49.0 | 25 | Scanner UI | sfx-ui-click | Only if the tool footage is silent; never over the real tool sound |
| 01:50.0 | 25 | Scanner plugged in | mechanical-accent (real connector click) | Natural sound from footage, ≤ −12 dBFS |
| 01:58.0 | 26 | Freeze frame panel | shutter (effect sound) | |
| 02:25.0 | 31 | Pre-banner | BGM | Fade out 1.5 s |
| 02:19.5 | 31 | Coil removal | mechanical-accent (real clip sound) | Natural, ≤ −12 dBFS; no added "clunk" |
| 02:22.0 | 31 | Safety banner entry | sfx-low-thud | |
| 02:27.0 | 32 | Post-banner | BGM | Fade in 1 s to −28 LUFS |
| 02:28.5 | 32 | Coil swap animation | sfx-ui-click | On the swap arrow, in a pause |
| 02:34.5 | 33 | Arrow to other groups | sfx-whoosh | |
| 02:40.5 | 34 | Closing sentence | sfx-whoosh | On the typography landing, before the VO sentence starts |
| 02:46.0 | 35 | Five ticks | none | Visual ticks only; no five-beep run (never repeated beeps) |
| 02:52.0 | 36 | Outro | BGM | Gentle outro section, still ducked |
| 02:56.0 | 37 | Branded ending | sfx-whoosh | On logo reveal, in the pause before "Cartek" |
| 03:00.0 | 37 | End | BGM | Resolves and stops; no tail past 03:00 |

Library usage count (Long): sfx-whoosh 10/12 · sfx-ui-beep 3/8 · sfx-ui-click 3/12 · sfx-low-thud 4/6 · zoom-punch 2/6 ·
freeze-frame-snapshot 2/4 · soft-dissolve 0/6. All within `max_uses_per_video`.

## Video B — Short (0:59, 9:16)

| Time | Shot | Cue | Element | Level / behaviour |
|---|---|---|---|---|
| 00:00.0 | 1 | Bed in | BGM | Fade in 0.3 s to −24 LUFS, ducked −18 LU under VO |
| 00:02.6 | 2 | P0300 code-popup | sfx-ui-beep | After "P0300!" |
| 00:10.5 | 4 | Empty cause box | sfx-ui-click | After "vì sao" |
| 00:12.0 / 00:15.0 / 00:18.0 / 00:21.0 | 5–8 | Four tiles | sfx-whoosh ×4 | Between list items |
| 00:24.5 | 9 | Scanner UI callout | sfx-ui-click | Only if footage is silent |
| 00:30.0 | 10 | Freeze frame panel | shutter (effect sound) | ≤ −18 dBFS |
| 00:41.0 | 12 | "Xóa mã" crossed out | sfx-low-thud | After "freeze frame"; bed dips −3 dB for the line |
| 00:42.0 | 13 | Split screen | sfx-whoosh | On the split wipe |
| 00:48.0 | 14 | Closing sentence | none | Zoom-punch is silent |
| 00:53.0 | 15 | Branded ending | sfx-whoosh | On logo reveal |
| 00:59.0 | 15 | End | BGM | Resolves; last 0.3 s silent for a clean loop |

Library usage count (Short): sfx-whoosh 6/12 · sfx-ui-beep 1/8 · sfx-ui-click 2/12 · sfx-low-thud 1/6 · zoom-punch 1/6 ·
freeze-frame-snapshot 1/4.

## Do-not list (brand voice)

- No sirens, alarm tones, rising beeps, heartbeat, drone or rumble layers, trailer hits or "glitch" stingers.
- No sound added to a plain cut.
- No engine-failure, backfire or crash sound effects; the only engine sound is the real footage at natural level.
- The low-thud is a cue, not a threat: one hit, never layered.
