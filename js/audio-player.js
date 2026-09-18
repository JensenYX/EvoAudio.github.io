/* Canvas waveform player.
 *
 * Structure follows the AuK project page's player -- play button, clickable
 * canvas scrubber, elapsed/duration readout, download -- with one difference:
 * the waveform envelope is precomputed at export time and shipped inside
 * demos.json, so nothing here decodes audio. That keeps a page holding ~150
 * clips responsive, and lets every card draw its shape before its audio has
 * been fetched.
 *
 * Audio is only fetched on first play. A page-level registry enforces that one
 * clip plays at a time.
 */

const WAVE_TRACK = "rgba(11, 87, 208, 0.26)";
const WAVE_PLAYED = "#0b57d0";
const WAVE_CURSOR = "rgba(11, 87, 208, 0.85)";

/** @type {Set<Player>} */
const registry = new Set();
/** @type {Player | null} */
let playing = null;

const PLAY_ICON =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>';
const PAUSE_ICON =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z" fill="currentColor"/></svg>';
const DOWNLOAD_ICON =
  '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M11 2a1 1 0 1 1 2 0v9.586l2.293-2.293a1 1 0 0 1 1.414 1.414l-4 4a1 1 0 0 1-1.414 0l-4-4a1 1 0 1 1 1.414-1.414L11 11.586V2zM4 15a1 1 0 0 1 1 1v2a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-2a1 1 0 1 1 2 0v2a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4v-2a1 1 0 0 1 1-1z"/></svg>';

function formatTime(seconds) {
  if (!Number.isFinite(seconds) || seconds < 0) return "0:00";
  const total = Math.floor(seconds);
  const mins = Math.floor(total / 60);
  const secs = total % 60;
  return `${mins}:${String(secs).padStart(2, "0")}`;
}

class Player {
  /**
   * @param {HTMLElement} root
   * @param {{url: string, peaks: number[], duration: number}} track
   */
  constructor(root, track) {
    this.root = root;
    this.track = track;
    this.audio = null;
    this.ready = false;
    this.failed = false;
    this.position = 0;
    this.raf = null;
    // Whether the user has asked for playback. The progress loop follows this
    // rather than `audio.paused`: right after play() the element is still
    // paused while it buffers, so a loop keyed on `paused` would exit on its
    // first frame and never restart.
    this.wantsPlayback = false;
    this.build();
    registry.add(this);
  }

  build() {
    this.root.classList.add("player");
    this.root.innerHTML = `
      <div class="player__control">
        <button type="button" class="player__play" aria-label="Play">${PLAY_ICON}</button>
        <div class="player__scrubber" role="slider" tabindex="0"
             aria-label="Seek within the clip" aria-valuemin="0"
             aria-valuemax="${Math.round(this.track.duration)}" aria-valuenow="0">
          <canvas class="player__wave" aria-hidden="true"></canvas>
        </div>
        <span class="player__time"><span class="player__elapsed">0:00</span> / <span class="player__total">${formatTime(
          this.track.duration
        )}</span></span>
        <button type="button" class="player__download" title="Download this clip"
                aria-label="Download this clip">${DOWNLOAD_ICON}</button>
      </div>`;

    this.playBtn = this.root.querySelector(".player__play");
    this.scrubber = this.root.querySelector(".player__scrubber");
    this.canvas = this.root.querySelector(".player__wave");
    this.elapsedEl = this.root.querySelector(".player__elapsed");

    this.playBtn.addEventListener("click", () => this.toggle());
    this.root
      .querySelector(".player__download")
      .addEventListener("click", () => this.download());

    this.attachSeek();
    this.draw();
  }

  attachSeek() {
    const seek = (clientX) => {
      const rect = this.scrubber.getBoundingClientRect();
      if (!rect.width) return;
      const ratio = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width));
      this.position = ratio * this.duration();
      if (this.audio && this.ready) this.audio.currentTime = this.position;
      this.render();
    };

    this.scrubber.addEventListener("pointerdown", (event) => {
      try {
        this.scrubber.setPointerCapture(event.pointerId);
      } catch (_) {
        /* proceed without capture */
      }
      seek(event.clientX);
      const move = (ev) => seek(ev.clientX);
      const up = (ev) => {
        this.scrubber.removeEventListener("pointermove", move);
        this.scrubber.removeEventListener("pointerup", up);
        this.scrubber.removeEventListener("pointercancel", up);
        try {
          this.scrubber.releasePointerCapture(ev.pointerId);
        } catch (_) {
          /* pointer already released */
        }
      };
      this.scrubber.addEventListener("pointermove", move);
      this.scrubber.addEventListener("pointerup", up);
      this.scrubber.addEventListener("pointercancel", up);
    });

    this.scrubber.addEventListener("keydown", (event) => {
      const duration = this.duration();
      let next = this.position;
      if (event.key === "ArrowRight") next = Math.min(duration, this.position + 1);
      else if (event.key === "ArrowLeft") next = Math.max(0, this.position - 1);
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = duration;
      else if (event.key === " " || event.key === "Enter") {
        event.preventDefault();
        this.toggle();
        return;
      } else return;
      event.preventDefault();
      this.position = next;
      if (this.audio && this.ready) this.audio.currentTime = next;
      this.render();
    });
  }

  duration() {
    if (this.audio && Number.isFinite(this.audio.duration) && this.audio.duration > 0) {
      return this.audio.duration;
    }
    return this.track.duration || 0;
  }

  ensureAudio() {
    if (this.audio) return this.audio;
    const audio = new Audio();
    audio.preload = "auto";
    audio.src = this.track.url;
    audio.addEventListener("loadedmetadata", () => {
      this.ready = true;
      this.scrubber.setAttribute("aria-valuemax", String(Math.round(this.duration())));
      this.root.querySelector(".player__total").textContent = formatTime(this.duration());
      if (this.position > 0) audio.currentTime = this.position;
    });
    // Keep the readout truthful even if rAF is throttled (background tab).
    audio.addEventListener("timeupdate", () => {
      if (this.wantsPlayback) {
        this.position = audio.currentTime;
        this.render();
      }
    });
    audio.addEventListener("ended", () => {
      this.wantsPlayback = false;
      this.position = 0;
      this.setPlayingState(false);
      this.render();
    });
    audio.addEventListener("pause", () => {
      // Covers a pause that did not come through toggle(), e.g. the OS.
      if (audio.ended) return;
      this.wantsPlayback = false;
      this.setPlayingState(false);
    });
    audio.addEventListener("error", () => {
      this.failed = true;
      this.wantsPlayback = false;
      this.setPlayingState(false);
      this.playBtn.setAttribute("aria-label", "Audio failed to load");
      this.playBtn.disabled = true;
    });
    this.audio = audio;
    return audio;
  }

  toggle() {
    if (this.failed) return;
    const audio = this.ensureAudio();
    if (this.wantsPlayback) {
      this.pause();
      return;
    }
    if (playing && playing !== this) playing.pause();
    if (this.position > 0 && this.ready) audio.currentTime = this.position;
    this.wantsPlayback = true;
    playing = this;
    this.setPlayingState(true);
    const started = audio.play();
    if (started && typeof started.catch === "function") {
      started.catch(() => {
        // Autoplay refusal or a failed fetch; drop back to the paused look
        // instead of showing a pause button over silence.
        this.wantsPlayback = false;
        this.setPlayingState(false);
      });
    }
  }

  pause() {
    this.wantsPlayback = false;
    if (this.audio) this.audio.pause();
    this.setPlayingState(false);
  }

  setPlayingState(active) {
    this.playBtn.innerHTML = active ? PAUSE_ICON : PLAY_ICON;
    this.playBtn.setAttribute("aria-label", active ? "Pause" : "Play");
    if (active) {
      if (this.raf === null) this.tick();
    } else {
      if (this.raf !== null) cancelAnimationFrame(this.raf);
      this.raf = null;
      if (playing === this) playing = null;
    }
  }

  tick() {
    this.raf = requestAnimationFrame(() => {
      this.raf = null;
      if (!this.wantsPlayback) return;
      if (this.audio) {
        this.position = this.audio.currentTime;
        this.render();
      }
      this.tick();
    });
  }

  render() {
    this.elapsedEl.textContent = formatTime(this.position);
    this.scrubber.setAttribute("aria-valuenow", String(Math.round(this.position)));
    this.draw();
  }

  draw() {
    const canvas = this.canvas;
    const rect = canvas.getBoundingClientRect();
    const width = Math.max(Math.floor(rect.width), 1);
    const height = Math.max(Math.floor(rect.height), 1);
    const dpr = window.devicePixelRatio || 1;
    if (canvas.width !== width * dpr || canvas.height !== height * dpr) {
      canvas.width = width * dpr;
      canvas.height = height * dpr;
    }
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, width, height);

    const peaks = this.track.peaks || [];
    if (!peaks.length) return;

    const duration = this.duration();
    const progress = duration > 0 ? Math.min(1, this.position / duration) : 0;

    // One bar per ~3 device-independent pixels, resampled from the shipped
    // envelope so the shape is stable at any card width.
    const barWidth = 2;
    const gap = 1;
    const step = barWidth + gap;
    const bars = Math.max(Math.floor(width / step), 1);
    const mid = height / 2;
    const playedBars = progress * bars;

    for (let i = 0; i < bars; i += 1) {
      const from = Math.floor((i / bars) * peaks.length);
      const to = Math.max(Math.floor(((i + 1) / bars) * peaks.length), from + 1);
      let peak = 0;
      for (let j = from; j < to && j < peaks.length; j += 1) {
        if (peaks[j] > peak) peak = peaks[j];
      }
      // A floor keeps silent stretches visible as a hairline rather than a gap.
      const barHeight = Math.max(peak * (height - 4), 1.5);
      ctx.fillStyle = i < playedBars ? WAVE_PLAYED : WAVE_TRACK;
      ctx.fillRect(i * step, mid - barHeight / 2, barWidth, barHeight);
    }

    if (progress > 0 && progress < 1) {
      ctx.fillStyle = WAVE_CURSOR;
      ctx.fillRect(Math.min(playedBars * step, width - 1.5), 0, 1.5, height);
    }
  }

  download() {
    const link = document.createElement("a");
    link.href = this.track.url;
    link.download = this.track.url.split("/").pop() || "clip.wav";
    document.body.appendChild(link);
    link.click();
    link.remove();
  }

  destroy() {
    this.pause();
    if (this.audio) {
      this.audio.src = "";
      this.audio = null;
    }
    registry.delete(this);
  }
}

/** Build a player inside `root`. */
export function mountPlayer(root, track) {
  return new Player(root, track);
}

/** Tear down every player -- used when the visible demo set changes. */
export function destroyAllPlayers() {
  for (const player of Array.from(registry)) player.destroy();
  playing = null;
}

/** Redraw on resize: bar count depends on the card's pixel width. */
export function redrawAllPlayers() {
  for (const player of registry) player.draw();
}

let resizeTimer = null;
window.addEventListener("resize", () => {
  if (resizeTimer !== null) clearTimeout(resizeTimer);
  resizeTimer = window.setTimeout(redrawAllPlayers, 120);
});
