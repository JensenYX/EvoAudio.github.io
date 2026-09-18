"""Shared helpers for the EvoAudio demo-page curation pipeline.

The pipeline reads generated training items out of the EvoAudio execution
outputs, screens them, and exports the survivors as demo-page assets. Nothing
here writes into the source tree; every output lands under `curation/` or
`assets/` in this repository.
"""

from __future__ import annotations

import base64
import json
import os
import re
import time
import wave
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import requests

REPO = Path(__file__).resolve().parent.parent
CURATION = REPO / "curation"
SELF_EVOLVING = Path(
    "/apdcephfs_tj6/share_303840540/hunyuan/jensenwang/git_warehouse/self_envolving"
)
EXEC_OUTPUTS = SELF_EVOLVING / "evoaudio-exec" / "outputs"
LEGACY_INVENTORY = (
    SELF_EVOLVING / "demo_audio_curated_20260912" / "audit" / "inventory.jsonl.gz"
)

# ---------------------------------------------------------------------------
# Families
# ---------------------------------------------------------------------------

# The generators tag each item with a benchmark-oriented family (`mmsu:*`,
# `mmau_pro:*`, `mmar:*`, `mmau:*`). The paper groups the same 47 question
# types into six families, which is what the page shows.
FAMILY_OF_SOURCE: dict[str, str] = {
    # Speech prosody -- rate, pitch, loudness, intonation, pauses, syllables,
    # disfluency.
    "mmsu:speed_comparison": "prosody",
    "mmsu:pitch_comparison": "prosody",
    "mmsu:volume_comparison": "prosody",
    "mmsu:intonation_perception": "prosody",
    "mmsu:pause_perception": "prosody",
    "mmsu:syllable_perception": "prosody",
    "mmsu:disfluency_detection": "prosody",
    "mmsu:vocal_range_comparison": "prosody",
    "mmsu:consonant_vowel_perception": "prosody",
    "mmar:speech_attribute_content_reasoning": "prosody",
    # Speakers and dialogue -- identity, counts, gender, language.
    "mmsu:speaker_identity_recognition": "speakers",
    "mmsu:total_speaker_counting": "speakers",
    "mmsu:dialogue_turn_counting": "speakers",
    "mmsu:gender_prediction": "speakers",
    "mmsu:language_identification": "speakers",
    # Speech content -- speech QA, intent, emotion.
    "mmsu:content_grounding": "content",
    "mmsu:dialogue_reasoning": "content",
    "mmsu:intent_detection": "content",
    "mmsu:emotion_recognition": "content",
    # Sound events -- count, order, presence, mixtures, level, duration,
    # cause, context.
    "mmau_pro:sound_mixture": "sound",
    "mmau_pro:sound_counting": "sound",
    "mmau_pro:sound_ordering": "sound",
    "mmau_pro:scene_inference": "sound",
    "mmau:sound_identification": "sound",
    "mmau:sound_reasoning": "sound",
    "mmar:signal_loudness": "sound",
    "mmar:signal_duration": "sound",
    "mmar:perception_change": "sound",
    "mmar:speech_sound_mixture": "sound",
    # Music -- tempo, pitch, dynamics, repetition, instruments, genre, vocals.
    "mmau:music_tempo": "music",
    "mmau:music_pitch": "music",
    "mmau:music_genre": "music",
    "mmau:music_vocals": "music",
    "mmau:instrument_identification": "music",
    "mmau_pro:music_dynamics": "music",
    "mmau_pro:music_structure": "music",
    "mmau_pro:music_ordering": "music",
    # Multi clip and long scene.
    "mmau_pro:multi_audio": "multi",
    "mmau_pro:long_audio": "multi",
}

FAMILY_ORDER = ["prosody", "speakers", "content", "sound", "music", "multi"]

# The `evo4` generation predates the `family` field and names its skills
# differently, so it is mapped by skill instead. It is worth carrying because it
# is the only run that draws on real emotional-speech corpora (MSP-Podcast,
# MELD, RAVDESS), and emotion is a Speech Content capability that no later run
# produces in usable quantity.
FAMILY_OF_EVO4_SKILL: dict[str, str] = {
    # Speech prosody
    "speech_pause": "prosody",
    "speaking_rate": "prosody",
    "speech_pitch": "prosody",
    "speech_loudness": "prosody",
    "intonation": "prosody",
    "emphasis": "prosody",
    "disfluency": "prosody",
    # Speakers and dialogue
    "speaker_count": "speakers",
    "real_speaker_count": "speakers",
    "turn_order": "speakers",
    "speaker_gender": "speakers",
    "speaker_binding": "speakers",
    "dialogue_language": "speakers",
    "language_id": "speakers",
    # Speech content
    "real_dialogue_qa": "content",
    "dialogue_qa": "content",
    "content_qa": "content",
    "long_content_qa": "content",
    "real_long_qa": "content",
    "lyric_qa": "content",
    "real_emotion": "content",
    "speech_emotion": "content",
    "real_dialogue_emotion": "content",
    "dialogue_emotion": "content",
    # Sound events
    "sound_count": "sound",
    "sound_reasoning": "sound",
    "sound_mixture": "sound",
    "sound_timing": "sound",
    "sound_change": "sound",
    "sound_duration": "sound",
    "sound_order": "sound",
    "sound_loudness": "sound",
    "sound_identification": "sound",
    "sound_category": "sound",
    "scene_inference": "sound",
    "speech_in_scene": "sound",
    "real_speech_in_scene": "sound",
    # Music
    "melodic_contour": "music",
    "chord": "music",
    "instrument_count": "music",
    "meter": "music",
    "tempo": "music",
    "tempo_change": "music",
    "mode": "music",
    "instrument_order": "music",
    "instrument_id": "music",
    "music_pitch": "music",
    "dynamics": "music",
    "song_change": "music",
    "song_tempo": "music",
    "song_genre": "music",
    "song_mood": "music",
    "song_instrument": "music",
    "song_vocal": "music",
    "music_genre": "music",
    "music_in_scene": "music",
    "song_in_scene": "music",
    # Multi clip and long scene
    "long_scene": "multi",
    "multi_audio": "multi",
}

FAMILY_META = {
    "prosody": {
        "name": "Speech Prosody",
        "blurb": "Rate, pitch, loudness, intonation, pauses, syllables and "
        "disfluency, built with TTS plus time stretch, pitch shift, gain and "
        "silence insertion.",
    },
    "speakers": {
        "name": "Speakers & Dialogue",
        "blurb": "Speaker identity and similarity, speaker and turn counts, "
        "gender and language, built by voice selection, multilingual TTS, "
        "trimming and concatenation.",
    },
    "content": {
        "name": "Speech Content",
        "blurb": "Speech QA, intent and emotion, grounded in scripted TTS and "
        "labelled recordings from LibriSpeech and emotional speech corpora.",
    },
    "sound": {
        "name": "Sound Events",
        "blurb": "Counting, ordering, presence, mixtures, level, duration, "
        "cause and context, assembled from FSD50K and AudioSet by overlay, "
        "mixing, filtering and gain control.",
    },
    "music": {
        "name": "Music",
        "blurb": "Tempo, pitch, dynamics, repetition, instruments, genre and "
        "vocals, built from real recordings, MIDI through FluidSynth and LeVo "
        "song generation, with stretch, pitch shift, gain ramps and repetition.",
    },
    "multi": {
        "name": "Multi-clip & Long Scene",
        "blurb": "Cross-clip retrieval, sparse event localization and long "
        "sequence QA, assembled by concatenation, long scene layout, reverb "
        "and codecs.",
    },
}

# ---------------------------------------------------------------------------
# Tool chain
# ---------------------------------------------------------------------------

# Display names for every transform / source the generators record in their
# provenance tree. `core` marks an actual waveform operation, as opposed to
# picking source material or conditioning a synthesiser.
TOOL_META: dict[str, dict[str, Any]] = {
    "concat": {"label": "Segment concatenation", "core": True},
    "crop": {"label": "Audio crop", "core": True},
    "mix": {"label": "SNR background mixing", "core": True},
    "overlay": {"label": "Timeline event overlay", "core": True},
    "gain_db": {"label": "Gain / loudness control", "core": True},
    "ramp_gain": {"label": "Gain ramp envelope", "core": True},
    "peak_limit": {"label": "Peak limiting", "core": False},
    "time_stretch": {"label": "Pitch-preserving time stretch", "core": True},
    "pitch_shift": {"label": "Pitch shift", "core": True},
    "trim_silence": {"label": "Edge silence trim", "core": False},
    "silence_insertion": {"label": "Silence gap insertion", "core": True},
    "reverb": {"label": "Room reverberation", "core": True},
    "codec": {"label": "Codec round-trip", "core": True},
    "lowpass": {"label": "Low-pass filtering", "core": True},
    "highpass": {"label": "High-pass filtering", "core": True},
    "tts": {"label": "Qwen3-TTS synthesis", "core": False},
    "tts_style": {"label": "TTS style conditioning", "core": False},
    "src:librispeech": {"label": "LibriSpeech recording", "core": False},
    "src:fsd50k": {"label": "FSD50K recording", "core": False},
    "src:audioset": {"label": "AudioSet recording", "core": False},
    "src:ravdess": {"label": "RAVDESS emotional speech", "core": False},
    "src:meld": {"label": "MELD dialogue", "core": False},
    "src:msp": {"label": "MSP-Podcast emotional speech", "core": False},
    "src:iemocap": {"label": "IEMOCAP emotional speech", "core": False},
    "src:savee": {"label": "SAVEE emotional speech", "core": False},
    "src:gigaspeech": {"label": "GigaSpeech recording", "core": False},
    "src:levo": {"label": "LeVo song generation", "core": False},
    "src:midi": {"label": "MIDI + FluidSynth", "core": False},
    "src:tts": {"label": "Qwen3-TTS synthesis", "core": False},
}

# `sources` trees from the older runs use a handful of aliases.
TOOL_ALIASES = {
    "gain": "gain_db",
    "db": "gain_db",
    "gain_control": "gain_db",
    "concatenation": "concat",
    "snr_mixing": "mix",
    "timeline_overlay": "overlay",
    "real_audio_selection": None,  # implied by the src:* entries
    "tts_style_conditioning": "tts_style",
}


def _canonical_tool(name: str) -> str | None:
    if name in TOOL_ALIASES:
        return TOOL_ALIASES[name]
    return name


def extract_tools(item: dict) -> list[str]:
    """Walk an item's provenance tree and collect the tools that built it."""
    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            transform = node.get("transform")
            if isinstance(transform, str):
                canon = _canonical_tool(transform)
                if canon:
                    found.add(canon)
            source = node.get("source")
            if isinstance(source, str):
                found.add(f"src:{source.lower()}")
            if "gap" in node and node.get("gap"):
                found.add("silence_insertion")
            if node.get("snr_db") is not None:
                found.add("mix")
            if node.get("max_dur") is not None or node.get("offset"):
                found.add("crop")
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(item.get("sources"))
    walk(item.get("assets"))

    if item.get("tts_utts"):
        found.add("tts")
        found.add("src:tts")
    # Every generator normalizes level and limits peaks on the way out.
    found.add("gain_db")
    found.add("peak_limit")
    # `src:tts` and `tts` are the same story told twice.
    if "src:tts" in found and "tts" in found:
        found.discard("src:tts")
    return sorted(t for t in found if t in TOOL_META)


def core_tool_count(tools: Iterable[str]) -> int:
    return sum(1 for t in tools if TOOL_META.get(t, {}).get("core"))


# `evo4` records its provenance with a different vocabulary: a flat list of
# source entries carrying `kind` (fsd / tts / file / midi), numeric `gain_db`
# and `stretch`, and an `onset` that is either an absolute time or
# `{after: "prev", gap: s}`. Nothing in it looks like the `transform` keys the
# later runs use, so it needs its own reader.
_EVO4_KIND_SOURCE = {
    "fsd": "src:fsd50k",
    "tts": "tts",
    "midi": "src:midi",
}


def extract_tools_evo4(item: dict) -> list[str]:
    found: set[str] = {"gain_db", "peak_limit"}
    entries = [s for s in (item.get("sources") or []) if isinstance(s, dict)]
    corpus = ((item.get("facts") or {}).get("source") or "").lower()

    roles = [str(s.get("role") or "") for s in entries]
    sequenced = 0

    for entry in entries:
        kind = str(entry.get("kind") or "").lower()
        mapped = _EVO4_KIND_SOURCE.get(kind)
        if mapped:
            found.add(mapped)
        if kind == "tts" and str(entry.get("instruct") or "").strip():
            found.add("tts_style")
        if kind == "file" and corpus:
            candidate = f"src:{corpus}"
            if candidate in TOOL_META:
                found.add(candidate)

        stretch = entry.get("stretch")
        if isinstance(stretch, (int, float)) and abs(float(stretch) - 1.0) > 1e-3:
            found.add("time_stretch")
        semitones = entry.get("semitones")
        if isinstance(semitones, (int, float)) and abs(float(semitones)) > 1e-3:
            found.add("pitch_shift")

        onset = entry.get("onset")
        if isinstance(onset, dict):
            sequenced += 1
            if onset.get("gap"):
                found.add("silence_insertion")
        if str(entry.get("role") or "") == "background":
            found.add("mix")

    # Pieces laid end to end are a concatenation; several events placed at
    # different points on one timeline are an overlay.
    if sequenced >= 1:
        found.add("concat")
    if roles.count("event") + roles.count("distractor") >= 2:
        found.add("overlay")
    if len(entries) >= 2:
        found.add("crop")

    return sorted(t for t in found if t in TOOL_META)


# ---------------------------------------------------------------------------
# Item helpers
# ---------------------------------------------------------------------------


def audio_paths(item: dict) -> list[str]:
    audio = item.get("audio")
    paths = audio if isinstance(audio, list) else [audio]
    return [p for p in paths if isinstance(p, str)]


def generator_checks_ok(item: dict) -> bool:
    """True when every acoustic check the generator ran still holds.

    `measured_ok is False` means an independent measurement could not confirm
    the rendered cue -- the case that produced the inverted `music_tempo_change`
    label found while planning -- so it is treated as a failure.
    """
    for check in (item.get("facts") or {}).get("checks") or []:
        if check.get("ok") is False:
            return False
        if check.get("measured_ok") is False:
            return False
    return True


def option_texts(item: dict) -> list[str]:
    out = []
    for opt in item.get("options") or []:
        out.append(opt["text"] if isinstance(opt, dict) else str(opt))
    return out


def gold_text(item: dict) -> str:
    for opt in item.get("options") or []:
        if isinstance(opt, dict) and opt.get("id") == item.get("answer"):
            return opt["text"]
    return ""


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------


def read_wav(path: str) -> tuple[np.ndarray, int]:
    """Read a 16-bit PCM WAV as float32 in [-1, 1]. No soundfile on this box."""
    with wave.open(path) as w:
        if w.getsampwidth() != 2:
            raise ValueError(f"expected 16-bit PCM, got {w.getsampwidth()*8}-bit")
        sr = w.getframerate()
        channels = w.getnchannels()
        raw = w.readframes(w.getnframes())
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if channels > 1:
        x = x.reshape(-1, channels).mean(axis=1)
    return x, sr


def waveform_peaks(x: np.ndarray, buckets: int = 640) -> list[float]:
    """Min/max envelope reduced to `buckets` absolute peaks, as the page draws."""
    if x.size == 0:
        return [0.0] * buckets
    edges = np.linspace(0, x.size, buckets + 1).astype(int)
    peaks = []
    for i in range(buckets):
        lo, hi = edges[i], max(edges[i + 1], edges[i] + 1)
        peaks.append(round(float(np.max(np.abs(x[lo:hi]))), 4))
    return peaks


# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------

GEMINI_URL = "http://llm-api.model-eval.woa.com/v1/chat/completions"
GEMINI_MODEL = "api_google_gemini-3.5-flash"
_APP_ID = os.environ.get("EVOAUDIO_GEMINI_APP_ID", "YwPTqKKZ_jensenywang")
_APP_KEY = os.environ.get("EVOAUDIO_GEMINI_APP_KEY", "QWIWIirvX6azNyil")
GEMINI_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {_APP_ID}:{_APP_KEY}?api=gemini_api",
}

_session_local = None


def _session() -> requests.Session:
    global _session_local
    if _session_local is None:
        s = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=256, pool_maxsize=256)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        _session_local = s
    return _session_local


def audio_b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("utf-8")


def gemini_call(
    prompt: str,
    wav_paths: list[str],
    *,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    tries: int = 4,
) -> str | None:
    """One chat completion with audio attached. Returns raw text or None.

    `max_tokens` has to stay generous: the model reasons before answering and
    returns empty content at small limits. The `star-proxy` hop in front of the
    API also drops connections now and then, hence the retries.
    """
    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    for p in wav_paths:
        content.append(
            {
                "type": "input_audio",
                "input_audio": {"data": audio_b64(p), "format": "wav"},
            }
        )
    payload = {
        "model": GEMINI_MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    for attempt in range(tries):
        try:
            r = _session().post(
                GEMINI_URL, headers=GEMINI_HEADERS, json=payload, timeout=(10, 300)
            )
            if r.status_code == 200:
                msg = r.json()["choices"][0]["message"]
                text = msg.get("content")
                if text:
                    return text
        except Exception:
            pass
        time.sleep(min(2 ** attempt, 10))
    return None


def parse_json_block(text: str | None) -> dict | None:
    if not text:
        return None
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except Exception:
        # Models occasionally emit trailing commas or stray prose.
        cleaned = re.sub(r",\s*([}\]])", r"\1", match.group(0))
        try:
            return json.loads(cleaned)
        except Exception:
            return None


def parse_choice_letter(text: str | None) -> str:
    """Pull an A-D answer out of a response.

    A bare `[ABCD]` regex is wrong here: it matches the `A` in `"answer"`.
    """
    if not text:
        return ""
    obj = parse_json_block(text)
    if obj and obj.get("answer"):
        letter = str(obj["answer"]).strip().upper()
        if letter[:1] in "ABCD":
            return letter[:1]
    match = re.search(r"answer\W{0,6}([ABCD])\b", text, re.I)
    if match:
        return match.group(1).upper()
    match = re.search(r"\b([ABCD])\b", text)
    return match.group(1) if match else ""


# ---------------------------------------------------------------------------
# JSONL helpers
# ---------------------------------------------------------------------------


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows
