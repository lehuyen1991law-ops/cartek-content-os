# Voice demo notes — P0300 dual demo

**REVIEW REQUIRED.** The renders below are machine voices (Microsoft Edge neural TTS via `edge-tts` 7.3.1). They were made to
measure timing and to check that the spelled-out pronunciations work. Whether they sound natural, whether the English words
("Cartek", "freeze frame", "Check Engine", "readiness", "Check your car") come out right, and whether the pauses feel like a
person speaking has **not** been checked by a human listener. A Vietnamese speaker must listen before any decision about
voice casting or using TTS in a published video. Nothing here was uploaded anywhere.

## What was rendered

Scratch directory (outside Git; mp3 is excluded by `.gitignore`):
`/tmp/claude-0/-workspace/424a71e8-a70a-517e-a5be-60c17c231195/scratchpad/render/dual/voice/`

Method: each script segment (VO + SAFETY line) was converted with the TTS column of `pronunciation.md` (P0300 → "pê không ba trăm",
OBD-II/OBD2 → "ô-bê-đê hai", ECU → "i-xi-u", brand line "Cartek. Check your car."), rendered to one mp3 per segment,
trimmed of edge-tts' own lead/tail silence (to 50 ms), then joined with 0.5 s gaps using ffmpeg and measured with ffprobe.
Render script: `/tmp/claude-0/-workspace/424a71e8-a70a-517e-a5be-60c17c231195/scratchpad/render/dual/render.py`
(uses the agent proxy and the `/root/.ccr/ca-bundle.crt` SSL context).

| File (in the scratch directory) | Content | Voice | Rate | Measured |
|---|---|---|---|---|
| `long-hook25-namminh-ratem5.mp3` (+ `long-hook25-namminh-ratem5/S01.mp3`, `S02.mp3`) | Long S01+S02 (hook + first 25 s) | vi-VN-NamMinhNeural | −5 % | 23.47 s with gap |
| `long-hook25-namminh-rate0.mp3` (+ segments) | Long S01+S02 | vi-VN-NamMinhNeural | 0 % | 22.34 s |
| `long-hook25-hoaimy-ratem5.mp3` (+ segments) | Long S01+S02 | vi-VN-HoaiMyNeural | −5 % | 23.74 s |
| `long-hook25-hoaimy-rate0.mp3` (+ segments) | Long S01+S02 | vi-VN-HoaiMyNeural | 0 % | 22.58 s |
| `long-full-namminh-ratem5.mp3` (+ `long-full-namminh-ratem5/S01..S09.mp3`) | Full Video A | vi-VN-NamMinhNeural | −5 % | 175.10 s with 8 gaps (limit 176) |
| `short-full-namminh-ratem5.mp3` (+ `short-full-namminh-ratem5/S01..S06.mp3`) | Full Video B | vi-VN-NamMinhNeural | −5 % | 51.91 s with 5 gaps (limit 56) |
| `timing_<variant>.json` | Per-segment durations for each variant | | | source of `timing.json` |

Final counts: Long 510 syllables (budget 560), Short 159 syllables (budget 175). Details and the trimming iterations are in `timing.json`.

## Observations from the render (measurements, not listening)

- Measured pace at −5 % was about 179 syl/min on the Long and 193 syl/min on the Short, below the 200/220 planning values in
  `config/production.yaml`: colon lists, numbered steps and sentence ends add pauses that the syllable count does not see.
  The Long needed three wording passes (602 → 551 → 506 → 510 syllables) to fit 176 s; the rate was kept at −5 % as requested.
- The Long fits with 0.9 s to spare. If the human read is slower than the TTS, the editor should take the time from the S07
  illustration or the S09 CTA, not from the S03 safety line.
- The planned 25 s slots hold: S03 24.7 s, S04 25.1 s, S05 25.2 s raw (each about 1.1 s shorter after trimming); S06 (30.1 s) and
  S07 (27.8 s raw) are the longest.
- Both hook variants at 0 % are about 1.1 s faster than at −5 % over 25 s; the choice between NamMinh (male) and HoaiMy (female)
  is a brand decision that needs the listening check.
- edge-tts pads every clip with about 0.3 s of lead and 0.8–1.0 s of tail silence; the editor would trim it anyway, so the
  reported totals use trimmed clips plus explicit 0.5 s gaps. Raw totals are also in `timing.json`.

## Open items for the listening check

1. Does "pê không ba trăm" / "pê không ba trăm lẻ một" sound right at this pace, or does the voice swallow "lẻ một"?
2. "Cartek", "Check your car", "freeze frame", "readiness": keep the English spelling or switch to the fallbacks in `pronunciation.md`?
3. Are the numbered steps in Long S06 ("Một, ... Hai, ...") clearly separated without sounding mechanical?
4. Does the SAFETY sentence in Long S03 read as calm advice (brand voice) rather than a warning tone?
5. Which voice (NamMinh / HoaiMy) and rate (−5 % / 0 %) for the demo cut, if TTS is used at all; a human voice-over remains the
   default for release videos.
