/* Demo browser: family tabs crossed with a draggable difficulty slider.
 *
 * The page shows one (family, level) cell at a time. That is deliberate --
 * ~150 clips stacked in one column tells you nothing about difficulty, whereas
 * holding the family fixed and dragging the level lets you hear a skill get
 * harder, which is the claim the page is making.
 *
 * Players are destroyed and rebuilt on every cell change so no audio keeps
 * downloading for cards that are no longer on screen.
 */

import { mountPlayer, destroyAllPlayers } from "./audio-player.js";

const DATA_URL = "assets/data/demos.json";

const state = {
  data: null,
  family: null,
  level: 3,
};

const escapeHtml = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (char) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char])
  );

const byId = (id) => document.getElementById(id);

/* ------------------------------------------------------------------ helpers */

function demosFor(family, level) {
  if (!state.data) return [];
  return state.data.demos.filter(
    (demo) => demo.family === family && demo.level === level
  );
}

function countsForFamily(family) {
  const counts = {};
  for (const level of state.data.levels) {
    counts[level.level] = demosFor(family, level.level).length;
  }
  return counts;
}

function levelMeta(level) {
  return state.data.levels.find((entry) => entry.level === level) || null;
}

/* --------------------------------------------------------------- family rail */

function buildFamilyRail() {
  const rail = byId("family-rail");
  rail.setAttribute("role", "tablist");
  rail.innerHTML = state.data.families
    .map((family) => {
      const total = state.data.demos.filter((d) => d.family === family.id).length;
      return `<button type="button" role="tab" data-family="${escapeHtml(family.id)}"
        aria-selected="${family.id === state.family}"
        aria-controls="demo-panel">${escapeHtml(family.name)}<span class="count">${total}</span></button>`;
    })
    .join("");

  rail.querySelectorAll("button[data-family]").forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.family === state.family) return;
      state.family = button.dataset.family;
      syncRail();
      // A family may not carry every level; land on the nearest one that does.
      state.level = nearestPopulatedLevel(state.level);
      syncSlider();
      renderCell();
      writeHash();
    });
  });
}

function syncRail() {
  byId("family-rail")
    .querySelectorAll("button[data-family]")
    .forEach((button) => {
      button.setAttribute(
        "aria-selected",
        button.dataset.family === state.family ? "true" : "false"
      );
    });
}

function nearestPopulatedLevel(preferred) {
  const counts = countsForFamily(state.family);
  if (counts[preferred]) return preferred;
  const levels = state.data.levels.map((entry) => entry.level);
  const sorted = levels
    .filter((level) => counts[level] > 0)
    .sort((a, b) => Math.abs(a - preferred) - Math.abs(b - preferred));
  return sorted.length ? sorted[0] : preferred;
}

/* ----------------------------------------------------------------- slider */

function buildSlider() {
  const levels = state.data.levels;
  const wrap = byId("difficulty-slider");
  const pct = (index) => (levels.length > 1 ? (index / (levels.length - 1)) * 100 : 0);

  wrap.innerHTML = `
    <div class="slider__labels">
      ${levels
        .map(
          (entry, index) => `<button type="button" class="slider__stop"
            data-level="${entry.level}" style="left:${pct(index)}%"
            aria-pressed="${entry.level === state.level}"
            aria-label="Level ${entry.level}, ${escapeHtml(entry.name)}">
            <b>L${entry.level}</b><span class="slider__stop-name">${escapeHtml(
            entry.name
          )}</span></button>`
        )
        .join("")}
    </div>
    <div class="slider__rail" role="slider" tabindex="0"
         aria-label="Difficulty level"
         aria-valuemin="${levels[0].level}" aria-valuemax="${levels[levels.length - 1].level}"
         aria-valuenow="${state.level}">
      <div class="slider__ticks">
        ${levels
          .map((_, index) => `<span class="slider__tick" style="left:${pct(index)}%"></span>`)
          .join("")}
      </div>
      <div class="slider__fill"></div>
      <div class="slider__thumb"></div>
    </div>`;

  const rail = wrap.querySelector(".slider__rail");

  const levelFromX = (clientX) => {
    const rect = rail.getBoundingClientRect();
    if (!rect.width) return state.level;
    const ratio = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width));
    const index = Math.round(ratio * (levels.length - 1));
    return levels[index].level;
  };

  // Dragging previews the level continuously but only rebuilds the cards when
  // the level actually changes, so sweeping the rail does not thrash the DOM.
  let dragging = false;
  const apply = (clientX) => {
    const next = levelFromX(clientX);
    if (next === state.level) return;
    state.level = next;
    syncSlider();
    renderCell();
    writeHash();
  };

  rail.addEventListener("pointerdown", (event) => {
    dragging = true;
    // Capture keeps the drag alive when the pointer leaves the rail, but it
    // must not be allowed to abort the interaction if the id is not capturable.
    try {
      rail.setPointerCapture(event.pointerId);
    } catch (_) {
      /* proceed without capture */
    }
    apply(event.clientX);
  });
  rail.addEventListener("pointermove", (event) => {
    if (dragging) apply(event.clientX);
  });
  const endDrag = (event) => {
    if (!dragging) return;
    dragging = false;
    try {
      rail.releasePointerCapture(event.pointerId);
    } catch (_) {
      /* already released */
    }
  };
  rail.addEventListener("pointerup", endDrag);
  rail.addEventListener("pointercancel", endDrag);

  rail.addEventListener("keydown", (event) => {
    const index = levels.findIndex((entry) => entry.level === state.level);
    let next = index;
    if (event.key === "ArrowRight" || event.key === "ArrowUp") next = index + 1;
    else if (event.key === "ArrowLeft" || event.key === "ArrowDown") next = index - 1;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = levels.length - 1;
    else return;
    event.preventDefault();
    next = Math.min(levels.length - 1, Math.max(0, next));
    if (levels[next].level === state.level) return;
    state.level = levels[next].level;
    syncSlider();
    renderCell();
    writeHash();
  });

  wrap.querySelectorAll(".slider__stop").forEach((stop) => {
    stop.addEventListener("click", () => {
      const level = Number(stop.dataset.level);
      if (level === state.level) return;
      state.level = level;
      syncSlider();
      renderCell();
      writeHash();
    });
  });
}

function syncSlider() {
  const levels = state.data.levels;
  const index = Math.max(
    levels.findIndex((entry) => entry.level === state.level),
    0
  );
  const ratio = levels.length > 1 ? index / (levels.length - 1) : 0;
  const wrap = byId("difficulty-slider");
  wrap.querySelector(".slider__fill").style.width = `${ratio * 100}%`;
  const thumb = wrap.querySelector(".slider__thumb");
  thumb.style.left = `${ratio * 100}%`;
  thumb.style.borderColor = `var(--lvl-${state.level})`;
  wrap.querySelector(".slider__rail").setAttribute("aria-valuenow", String(state.level));
  wrap.querySelectorAll(".slider__stop").forEach((stop) => {
    stop.setAttribute(
      "aria-pressed",
      Number(stop.dataset.level) === state.level ? "true" : "false"
    );
  });

  const meta = levelMeta(state.level);
  if (meta) {
    byId("difficulty-readout").innerHTML =
      `<strong>L${meta.level} &middot; ${escapeHtml(meta.name)}</strong>`;
  }
}

/* ------------------------------------------------------------------- cards */

function renderCard(demo) {
  const clips = demo.clips
    .map((clip, index) => {
      const label =
        demo.clips.length > 1
          ? `<div class="card__clip-label">Clip ${index + 1}</div>`
          : "";
      return `${label}<div class="player-mount" data-clip="${index}"></div>`;
    })
    .join("");

  const options = demo.options
    .map(
      (option) =>
        `<li data-correct="${option.id === demo.answer}"><b>${escapeHtml(
          option.id
        )}</b><span>${escapeHtml(option.text)}</span></li>`
    )
    .join("");

  const tools = demo.tools
    .map(
      (tool) =>
        `<span class="tool-chip" data-core="${tool.core}">${escapeHtml(tool.label)}</span>`
    )
    .join("");

  const evidence = demo.evidence.length
    ? `<div class="detail-row"><span class="detail-row__label">Verifiable evidence from construction</span>
         <div class="evidence">${demo.evidence
           .map((line) => `<div>${escapeHtml(line)}</div>`)
           .join("")}</div></div>`
    : "";

  const transcript = demo.transcript
    ? `<div class="detail-row"><span class="detail-row__label">Spoken text</span>
         <div class="transcript">${escapeHtml(demo.transcript)}</div></div>`
    : "";

  return `
    <article class="card" data-demo-id="${escapeHtml(demo.id)}">
      <div class="card__top">
        <span class="card__skill">${escapeHtml(demo.skill_label)}</span>
        <span class="card__badges">
          <span class="chip chip--level" data-level="${demo.level}">L${demo.level}</span>
          <span class="chip chip--dur">${demo.duration_sec.toFixed(1)}s</span>
          <span class="chip">${demo.n_tools} tools</span>
        </span>
      </div>
      <p class="card__question">${escapeHtml(demo.question)}</p>
      ${clips}
      <ul class="card__options">${options}</ul>
      <div class="card__actions">
        <button type="button" class="reveal-btn" aria-expanded="false">Show answer &amp; evidence</button>
      </div>
      <div class="card__detail">
        <div class="detail-row">
          <span class="detail-row__label">Answer</span>
          <strong>${escapeHtml(demo.answer)}. ${escapeHtml(demo.answer_text)}</strong>
        </div>
        ${transcript}
        <div class="detail-row">
          <span class="detail-row__label">Tools that built this audio</span>
          <div class="tool-chips">${tools}</div>
        </div>
        ${evidence}
      </div>
    </article>`;
}

function renderCell() {
  destroyAllPlayers();
  const panel = byId("demo-panel");
  const family = state.data.families.find((entry) => entry.id === state.family);
  const demos = demosFor(state.family, state.level);

  const intro = `
    <div class="family-intro">
      <h3>${escapeHtml(family.name)}</h3>
      <p>${escapeHtml(family.blurb)}</p>
    </div>`;

  if (!demos.length) {
    const counts = countsForFamily(state.family);
    const available = state.data.levels
      .filter((entry) => counts[entry.level] > 0)
      .map((entry) => `L${entry.level}`)
      .join(", ");
    panel.innerHTML = `${intro}
      <div class="demo-empty">
        ${escapeHtml(state.data.empty_cell_note || "")}
        ${available ? ` Available here: ${escapeHtml(available)}.` : ""}
      </div>`;
    return;
  }

  panel.innerHTML = `${intro}<div class="demo-list">${demos.map(renderCard).join("")}</div>`;

  panel.querySelectorAll(".card").forEach((card) => {
    const demo = demos.find((entry) => entry.id === card.dataset.demoId);
    card.querySelectorAll(".player-mount").forEach((mount) => {
      const clip = demo.clips[Number(mount.dataset.clip)];
      mountPlayer(mount, {
        url: clip.url,
        peaks: clip.peaks,
        duration: clip.duration_sec,
      });
    });
    const button = card.querySelector(".reveal-btn");
    button.addEventListener("click", () => {
      const open = card.classList.toggle("is-revealed");
      button.setAttribute("aria-expanded", String(open));
      button.textContent = open ? "Hide answer & evidence" : "Show answer & evidence";
    });
  });
}

/* -------------------------------------------------------------- deep links */

function writeHash() {
  history.replaceState(null, "", `#${state.family}-L${state.level}`);
}

function readHash() {
  const match = window.location.hash.match(/^#([a-z]+)-L([1-5])$/);
  if (!match) return;
  const [, family, level] = match;
  if (state.data.families.some((entry) => entry.id === family)) {
    state.family = family;
    state.level = Number(level);
  }
}

/* ------------------------------------------------------------------- setup */

function fillSummary() {
  const system = state.data.system || {};
  const strip = byId("stat-strip");
  if (!strip) return;
  const stats = [
    [system.question_types, "verifiable question types"],
    [system.audio_tools, "audio tools"],
    [system.families, "task families"],
    [system.evolution_rounds, "evolution rounds"],
  ];
  strip.innerHTML = stats
    .map(
      ([value, label]) =>
        `<div class="stat"><div class="stat__value">${escapeHtml(
          value
        )}</div><div class="stat__label">${escapeHtml(label)}</div></div>`
    )
    .join("");
}

/** Fetch the index, retrying a couple of times.
 *
 * The page asks for the figures and this ~900 KB index at once, which a
 * single-connection dev server (`python -m http.server`) can drop outright.
 * Rather than leave a blank page in that case, back off briefly and retry.
 */
async function loadIndex(attempts = 3) {
  let lastError;
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      const response = await fetch(DATA_URL, { cache: "no-cache" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      lastError = error;
      await new Promise((resolve) => setTimeout(resolve, 400 * (attempt + 1)));
    }
  }
  throw lastError;
}

async function init() {
  try {
    state.data = await loadIndex();
  } catch (error) {
    byId("demo-panel").innerHTML =
      `<div class="demo-empty"><strong>Could not load the demo index.</strong>
       ${escapeHtml(String(error))}</div>`;
    return;
  }

  state.family = state.data.families[0].id;
  state.level = state.data.default_level || 3;
  readHash();

  fillSummary();
  buildFamilyRail();
  buildSlider();
  state.level = nearestPopulatedLevel(state.level);
  syncSlider();
  renderCell();

  const note = byId("difficulty-note");
  if (note) note.textContent = state.data.difficulty_note;
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
