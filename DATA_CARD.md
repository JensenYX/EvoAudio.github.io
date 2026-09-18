# Demo data card

How the audio on this page was chosen, stage by stage. Every number below is written by the scripts in `tools/`; the machine-readable summaries live in `curation/*_summary.json`.

## Why a selection pipeline at all

EvoAudio generates training data at scale and much of it is not fit for a demo page. On a 48-item random sample of already-gated candidates, an early blind listening audit returned 21% showcase, 33% acceptable and 46% reject, with audible distortion, abrupt cuts, robotic synthesis and one clip that was pure silence. The pipeline is therefore built to discard most of what it sees.

That first 21% was pessimistic for one avoidable reason: the draft rubric counted deliberate structure as damage. Many question types are *built* by concatenating unrelated segments -- that is the item, not a flaw -- and the draft was rejecting them for "obvious splices", along with marking sound-event clips down for containing no speech. The production rubric states the intended segment count up front and asks whether each join is *clean* rather than whether a join exists. With that corrected, 4288 of 8953 shortlisted candidates (48%) came back showcase-grade from both passes.

## Stages

| Stage | In | Out | Gate |
| --- | --- | --- | --- |
| 1. Metadata gates | 78869 | 45120 | audio present, acoustic checks hold (incl. `measured_ok`), not answerable from the question text alone, 1-60 s, at least 3 tools and 2 core transforms, deduplicated |
| 2. Signal screen | 45120 | 37203 | inaudible level, dead HF band, DC offset, unexplained dead air, clip starting/ending mid-sound, clicks at declared seams |
| 2b. Stratified shortlist | 37203 | 9727 | rare skills taken whole, artifact-prone skills over-sampled, spread over contrast bands and clip lengths |
| 3. Two blind listening audits | 8953 | 4288 | both passes: quality >= 4/5, no artifact, clean joins, speech not robotic, at least one pass would showcase it |
| 4. Difficulty probe | 4288 | 4284 | 5 blind attempts, options reshuffled each time, temperature 1.0 |
| 5. Informed correctness audit | 4284 | 2013 | both passes: cue audible, intended answer defensible and unique |
| 6. Diversity-constrained selection | 2013 | 180 | no repeated skill or tool combination per cell until forced, clip-length spread per family, quality breaks ties |

## What shipped

- **180 demos**, 57 of the system's question types, 21 distinct tools
- 39.7 minutes of audio, 72.7 MB as lossless 16 kHz mono WAV
- mean audited audio quality 4.99/5

| Family | L1 | L2 | L3 | L4 | L5 | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Speech Prosody | 6 | 6 | 6 | 6 | 6 | 30 |
| Speakers & Dialogue | 6 | 6 | 6 | 6 | 6 | 30 |
| Speech Content | 6 | 6 | 6 | 6 | 6 | 30 |
| Sound Events | 6 | 6 | 6 | 6 | 6 | 30 |
| Music | 6 | 6 | 6 | 6 | 6 | 30 |
| Multi-clip & Long Scene | 6 | 6 | 6 | 6 | 6 | 30 |

## Difficulty

No single model defines difficulty. The auditor is strong enough that answering correctly says little about whether an item is easy, and when it answers wrongly the cause is often a broken item rather than a hard one -- which is why difficulty is computed only after verification. The score combines how often the audio LLM under training missed the item, how often the auditor missed it under repeated blind attempts, the generator's own cue-salience setting, how far the background masks the foreground, and how much there is to hold in mind. Scores are ranked within each family and cut into five equal bands.

Signal weights: solver_miss 0.3, auditor_miss 0.25, cue_subtlety 0.25, masking 0.1, load 0.1

| Level | Band |
| --- | --- |
| L1 Salient | easiest fifth of the family's verified pool |
| L2 Clear | middle fifth of the family's verified pool |
| L3 Moderate | middle fifth of the family's verified pool |
| L4 Subtle | middle fifth of the family's verified pool |
| L5 Near-threshold | hardest fifth of the family's verified pool |

Auditor blind-score distribution over the probed pool (one input among several, not the level itself): 0/5 -> 828, 1/5 -> 299, 2/5 -> 262, 3/5 -> 274, 4/5 -> 343, 5/5 -> 2278

## Role of the auditing model

Gemini 3.5 Flash is used only as a listening instrument: it rates audio quality, measures difficulty, and checks that the constructed answer survives rendering. It never supplies an answer. Every label on the page comes from the construction record of the audio itself, which is the property that makes EvoAudio's supervision verifiable.

## Reproducing

```bash
python3.12 tools/01_scan_pool.py
python3.12 tools/02_signal_screen.py
python3.12 tools/02b_shortlist.py
python3.12 tools/03_gemini_quality.py      # resumable, cached
python3.12 tools/04_gemini_probe.py        # resumable, cached
python3.12 tools/05_gemini_correctness.py  # resumable, cached
python3.12 tools/06_select.py
python3.12 tools/07_export.py
python3.12 tools/make_evolution_figure.py
```

The three Gemini stages cache every call in `curation/*_cache.jsonl` and skip what is already done, so an interrupted run can simply be restarted. Credentials come from `EVOAUDIO_GEMINI_APP_ID` and `EVOAUDIO_GEMINI_APP_KEY`.
