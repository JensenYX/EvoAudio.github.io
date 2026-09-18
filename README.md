# EvoAudio project page

Project page for *EvoAudio: Recursive Self-Improvement for Audio Understanding*.

The page presents the paper's abstract and system figure, redraws its
self-evolution curves for the screen, and — the main event — lets you listen to
the verifiable training audio EvoAudio's tool library builds, browsable by task
family and by measured difficulty.

Live at <https://jensenyx.github.io/EvoAudio.github.io/>.

## Layout

```
index.html                  the whole page; no build step
css/site.css                styling
js/main.js                  renders the demo browser from assets/data/demos.json
js/audio-player.js          canvas waveform player
assets/data/demos.json      the demo index: questions, answers, tools, evidence, peaks
assets/audio/<family>/      the clips, lossless 16 kHz mono WAV
assets/figures/             system figure and the redrawn evolution charts
tools/                      the curation pipeline that produced the above
curation/                   pipeline summaries and the Gemini call caches
DATA_CARD.md                what every pipeline stage did, with counts
REVIEW.md                   contact sheet of every shipping demo
```

There is no bundler, package manager, or build step: GitHub Pages serves the
repository root as-is. Editing `index.html`, the CSS, or the JS is immediately
what ships.

To preview locally:

```bash
python3 tools/serve.py 8811
# then open http://127.0.0.1:8811/
```

Use that rather than `python3 -m http.server`: the stock server handles one
request at a time, and this page asks for the framework figure, two chart SVGs
and a ~900 KB demo index at once, which is enough to make it drop connections
and leave the demo browser empty. `tools/serve.py` is the same server with
threading enabled.

A plain `file://` open will not work either, because `js/main.js` fetches
`assets/data/demos.json` and ES modules are subject to CORS.

## The demos

Each card carries the question, a waveform player, the options, and — behind
one click — the answer, the chain of audio tools that built the clip, and the
measured evidence that fixes the answer (per-segment F0 in Hz, segment level in
dBFS, tempo in BPM, applied stretch ratio, mixing SNR, and so on). Nothing on a
card is a model's opinion about the audio: every answer follows from how the
audio was constructed.

Difficulty is measured rather than asserted. The generators' own easy/medium/hard
tags turned out not to predict real difficulty, so each clip was answered five
times blind with the options reshuffled every time, and its level is how often
the answer came back correct. `DATA_CARD.md` has the full accounting, including
how many candidates each stage discarded and which grid cells shipped short.

## Regenerating

The pipeline reads the EvoAudio execution outputs, which are not part of this
repository, and needs credentials for the auditing model:

```bash
export EVOAUDIO_GEMINI_APP_ID=...
export EVOAUDIO_GEMINI_APP_KEY=...

python3.12 tools/01_scan_pool.py           # candidate pool + metadata gates
python3.12 tools/02_signal_screen.py       # local DSP reject pass
python3.12 tools/02b_shortlist.py          # stratified shortlist
python3.12 tools/03_gemini_quality.py      # two blind listening audits
python3.12 tools/04_gemini_probe.py        # 5 blind attempts -> difficulty
python3.12 tools/05_gemini_correctness.py  # informed answer verification
python3.12 tools/06_select.py              # diversity-constrained selection
python3.12 tools/07_export.py              # assets + demos.json + docs

python3.12 tools/make_evolution_figure.py  # redraw the evolution charts
```

The three auditing stages cache every API call under `curation/`, skip work
already done, and can be restarted after an interruption.
