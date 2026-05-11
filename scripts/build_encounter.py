#!/usr/bin/env python3
"""Build an interactive HTML encounter worksheet from a JSON spec.

Produces a single self-contained .html file (no external dependencies)
suitable for offline use on iPad during a session. State persists in
the browser's localStorage keyed by the encounter slug.

Usage:
    python3 scripts/build_encounter.py spec.json
    python3 scripts/build_encounter.py - < spec.json
    python3 scripts/build_encounter.py '{"name": "...", ...}'

Spec shape:
{
  "name": "Winter Farm Encounter",
  "slug": "winter_farm_encounter",        # optional, derived from name
  "combatants": [
    {
      "id": "skull_cracker",              # optional
      "kind": "npc" | "pc",
      "name": "Skull-Cracker",
      "ac": 16,
      "hp_max": 162,
      "hp_current": 162,                  # NPC: rolled HP. PC: hp_max or null.
      "speed": "30/c20",
      "initiative": 4,                    # NPC: rolled. PC: null (DM fills at table).
      "init_mod": "+5",                   # display-only label for PC reminder
      "group": "A",                       # initiative group tag (optional)
      "notes": ""
    }, ...
  ],
  "npc_blocks": [
    {
      "title": "Skull-Cracker (Spring) - Large Monstrosity (ant), Lawful Evil",
      "stats": "AC 16 (natural armor) | HP 162 (16d10+64) | Speed ...",
      "defenses": "Skills: ... | CR 6 (2300 XP) | PB +3",
      "sections": [
        {"label": "TRAITS", "entries": [
          {"name": "Heated Body", "text": "..."}, ...
        ]},
        {"label": "ACTIONS", "entries": [...]}, ...
      ]
    }, ...
  ],
  "pc_blocks": [
    {
      "header": "Drix - Bard 6 (College of Lore) | Cricket | AC 15 | ...",
      "abilities": "STR 6 (-2) DEX 16 (+3) ...",
      "saves": "DEX +6 (prof), CHA +8 (prof). ...",
      "attacks": "Rapier +6, 1d8+3 piercing | ...",
      "spells": "Cantrips: ...",          # optional
      "features": "Bardic Inspiration (d8, 5 uses) ..."
    }, ...
  ],
  "notes": [
    {"label": "Setup", "text": "..."}, ...
  ]
}

Output: encounters/<slug>.html (path printed to stdout)
"""

import json
import re
import sys
from pathlib import Path


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#4472c4">
<title>Encounter - __NAME__</title>
<style>
__CSS__
</style>
</head>
<body>
<header class="topbar">
  <div class="topbar-left">
    <h1 id="encounter-name">__NAME__</h1>
    <span class="round-pill">Round <strong id="round-num">1</strong></span>
  </div>
  <div class="topbar-right">
    <button id="prev-btn" title="Previous turn">&#9664;</button>
    <button id="next-btn" class="primary" title="Next turn">Next &#9654;</button>
    <button id="reset-btn" class="danger" title="Reset to starting state">&#x21bb;</button>
  </div>
</header>

<noscript>
  <div style="padding:16px;background:#ffe0e0;color:#7a0000;border:1px solid #c62828;margin:12px;border-radius:8px;font-family:sans-serif;">
    <strong>JavaScript is disabled or this preview isn't running scripts.</strong><br>
    On iPhone/iPad, open this file in <em>Safari</em> (not the Files app's Quick Look preview).
    From the Files app: tap the share icon &rarr; "Open in Safari". On a Mac/PC, just double-click to open in your browser.
  </div>
</noscript>

<div id="boot-error" style="display:none;padding:16px;background:#ffe0e0;color:#7a0000;border:1px solid #c62828;margin:12px;border-radius:8px;font-family:sans-serif;"></div>

<main>
  <section class="tracker">
    <div class="tracker-header">
      <h2>Initiative</h2>
      <span class="hint">Tap init to edit. Tap a row to make it the active turn.</span>
    </div>
    <div id="tracker-rows"></div>
  </section>

  <section class="reference">
    <details open id="npc-section">
      <summary><span class="section-title">NPC Reference</span></summary>
      <div id="npc-blocks"></div>
    </details>
    <details open id="pc-section">
      <summary><span class="section-title">Party Reference</span></summary>
      <div id="pc-blocks"></div>
    </details>
    <details open id="notes-section-wrap">
      <summary><span class="section-title">Encounter Details</span></summary>
      <div id="notes-section"></div>
    </details>
  </section>
</main>

<script>
window.addEventListener("error", function (e) {
  var box = document.getElementById("boot-error");
  if (!box) return;
  box.style.display = "block";
  box.textContent = "Encounter worksheet failed to load: " + (e && e.message ? e.message : "unknown error");
});
var ENCOUNTER = __DATA__;
__JS__
</script>
</body>
</html>
"""


CSS = r"""
* { box-sizing: border-box; }
:root {
  --bg: #1f1a16;             /* dark warm brown */
  --panel: #2b2520;          /* slightly lighter brown */
  --panel-2: #342d27;        /* hover/contrast brown */
  --ink: #f0e8d8;            /* warm off-white */
  --muted: #a89e8c;          /* dim cream */
  --accent: #6b8fd8;          /* brighter blue for dark bg */
  --accent-light: #2c3a55;   /* dark blue for badges */
  --shade: #1a1612;           /* darker brown for nested cards */
  --border: #4a3f35;          /* warm brown border */
  --good: #7cc47c;            /* green */
  --bad: #e57373;             /* light red */
  --warn: #ffb74d;            /* amber */
  --active: #4a3a1f;          /* dark amber for active row */
  --active-border: #ffb74d;
}
html, body {
  margin: 0; padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  background: var(--bg); color: var(--ink);
  font-size: 16px;
  -webkit-text-size-adjust: 100%;
  -webkit-tap-highlight-color: rgba(0,0,0,0);
}
button { font: inherit; cursor: pointer; }
h1, h2, h3 { margin: 0; }

/* Topbar */
.topbar {
  position: sticky; top: 0; z-index: 50;
  background: var(--accent-light); color: var(--ink);
  display: flex; align-items: center; justify-content: space-between;
  padding: 6px 12px;
  gap: 10px;
  border-bottom: 1px solid var(--border);
  box-shadow: 0 2px 6px rgba(0,0,0,0.4);
}
.topbar-left { display: flex; align-items: baseline; gap: 10px; min-width: 0; }
.topbar h1 {
  font-size: 16px; font-weight: 600;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.topbar .round-pill {
  background: rgba(255,255,255,0.10); padding: 3px 9px;
  border-radius: 10px; font-size: 13px; white-space: nowrap;
}
.topbar-right { display: flex; gap: 5px; align-items: center; }
.topbar button {
  min-height: 36px; min-width: 36px;
  padding: 0 10px;
  border: 1px solid rgba(255,255,255,0.20);
  background: rgba(255,255,255,0.06);
  color: var(--ink); border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
}
.topbar button.primary {
  background: var(--accent); color: white; border-color: var(--accent);
}
.topbar button.danger { background: rgba(0,0,0,0.25); }
.topbar button:active { opacity: 0.6; }

main { padding: 0; max-width: 1400px; margin: 0 auto; }

/* Tracker */
.tracker {
  background: var(--bg);
  padding: 6px 8px 4px;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 48px;
  z-index: 40;
  max-height: 70vh;
  overflow-y: auto;
}
.tracker-header {
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 4px;
  gap: 10px;
  padding: 0 2px;
}
.tracker h2 {
  font-size: 11px; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.08em;
}
.tracker .hint { font-size: 11px; color: var(--muted); }

#tracker-rows { display: grid; gap: 3px; }

.row {
  display: grid;
  grid-template-columns: 48px 1fr auto;
  gap: 8px;
  padding: 4px 6px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 6px;
  align-items: center;
}
.row.npc { border-left: 3px solid var(--accent); }
.row.pc  { border-left: 3px solid var(--good); }
.row.active {
  background: var(--active);
  border-color: var(--active-border);
  box-shadow: 0 0 0 1px var(--active-border);
}
.row.dead { opacity: 0.45; background: var(--shade); }
.row.dead .name { text-decoration: line-through; }

.row input.init {
  font-family: inherit;
  font-size: 20px; font-weight: 700; text-align: center;
  color: var(--ink);
  background: var(--accent-light);
  border: 0;
  border-radius: 5px;
  padding: 4px 0;
  width: 48px; height: 40px;
  -webkit-appearance: none;
  appearance: none;
  outline: none;
}
.row input.init.empty { background: var(--shade); color: var(--muted); }
.row input.init:focus {
  background: var(--panel-2);
  box-shadow: 0 0 0 2px var(--accent);
}
.row input.init::placeholder { color: var(--muted); opacity: 1; }

.row .info { min-width: 0; }
.row .name {
  font-weight: 600; font-size: 15px; line-height: 1.2;
  word-wrap: break-word;
}
.row .name .group-tag {
  color: var(--muted); font-weight: 500; font-size: 12px;
  margin-left: 4px;
}
.row .meta {
  color: var(--muted); font-size: 12px; margin-top: 1px;
  line-height: 1.3;
}
.row .meta .ac { font-weight: 600; color: var(--ink); }
.row .meta .pc-init-mod {
  display: inline-block;
  background: var(--accent-light);
  color: var(--ink);
  font-weight: 600;
  padding: 0 6px; border-radius: 3px;
  margin-left: 4px;
  font-size: 11px;
}
.row .conditions-pills {
  display: flex; gap: 3px; flex-wrap: wrap; margin-top: 2px;
}
.row .conditions-pills .pill {
  background: rgba(229,115,115,0.20); color: var(--bad);
  border: 1px solid rgba(229,115,115,0.40);
  border-radius: 10px; padding: 0 7px; font-size: 11px;
  font-weight: 600; line-height: 1.4;
}

.row .hp {
  display: flex; flex-direction: row; align-items: center;
  gap: 4px;
}
.row .hp-display {
  font-size: 17px; font-weight: 700;
  min-width: 70px; text-align: right;
  padding-right: 4px;
}
.row .hp-display .sep { color: var(--muted); font-weight: 400; }
.row .hp-display.low { color: var(--warn); }
.row .hp-display.bloodied { color: var(--bad); }

.row .hp-controls { display: flex; gap: 3px; align-items: center; }
.row .hp-controls input {
  width: 52px; height: 34px;
  font-size: 14px; text-align: center;
  background: var(--bg); color: var(--ink);
  border: 1px solid var(--border); border-radius: 5px;
  font-family: inherit;
}
.row .hp-controls button {
  min-height: 34px; min-width: 34px;
  padding: 0 9px;
  border: 1px solid var(--border); border-radius: 5px;
  background: var(--shade); color: var(--ink);
  font-weight: 700;
  font-size: 16px;
}
.row .hp-controls .dmg {
  background: rgba(229,115,115,0.18); color: var(--bad);
  border-color: rgba(229,115,115,0.45);
}
.row .hp-controls .heal {
  background: rgba(124,196,124,0.18); color: var(--good);
  border-color: rgba(124,196,124,0.45);
}

.row .controls {
  display: flex; gap: 3px; align-items: center;
  margin-left: 4px;
}
.row .controls button {
  min-height: 34px;
  padding: 0 10px;
  border: 1px solid var(--border); border-radius: 5px;
  background: var(--shade); color: var(--ink);
  font-size: 12px; font-weight: 600;
}
.row .controls button.active {
  background: var(--accent); color: white; border-color: var(--accent);
}

.row .conditions-panel {
  grid-column: 1 / -1;
  margin-top: 4px; padding: 6px;
  background: var(--shade); border-radius: 5px;
  display: none;
}
.row .conditions-panel.open { display: block; }
.row .conditions-panel .pills {
  display: flex; flex-wrap: wrap; gap: 4px;
}
.row .conditions-panel .pill-toggle {
  min-height: 32px; padding: 0 10px;
  background: var(--panel-2); color: var(--ink);
  border: 1px solid var(--border); border-radius: 16px;
  font-size: 12px; font-weight: 500;
}
.row .conditions-panel .pill-toggle.active {
  background: var(--bad); color: white; border-color: var(--bad);
}
.row .conditions-panel .pill-toggle:active { opacity: 0.7; }

/* Reference */
.reference { padding: 8px; }
.reference details {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 6px;
  overflow: hidden;
}
.reference summary {
  padding: 6px 12px;
  background: var(--accent-light); color: var(--ink);
  cursor: pointer;
  list-style: none;
  user-select: none;
  display: flex; align-items: center; justify-content: space-between;
}
.reference summary::-webkit-details-marker { display: none; }
.reference summary .section-title {
  font-size: 13px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.06em;
}
.reference summary::after { content: "\25be"; font-size: 12px; color: var(--muted); }
.reference details[open] summary::after { content: "\25b4"; }
.reference details > div { padding: 6px 10px; }

.npc-block, .pc-block {
  margin-bottom: 6px; padding: 8px 10px;
  border: 1px solid var(--border); border-radius: 6px;
  background: var(--shade);
}
.npc-block:last-child, .pc-block:last-child { margin-bottom: 0; }
.npc-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; line-height: 1.25; color: var(--ink); }
.npc-stats, .npc-defenses {
  font-size: 12px; color: var(--ink);
  margin-bottom: 4px; line-height: 1.4;
}
.npc-section-label {
  font-size: 11px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.08em;
  margin: 6px 0 3px;
  padding-bottom: 2px;
  border-bottom: 1px solid var(--border);
}
.npc-entry { margin-bottom: 4px; line-height: 1.4; font-size: 12px; }
.npc-entry .entry-name { font-weight: 700; color: var(--ink); }
.npc-entry .entry-name::after { content: ". "; }

.pc-row { margin-bottom: 3px; line-height: 1.4; font-size: 12px; }
.pc-row .label {
  font-weight: 700; color: var(--accent);
  margin-right: 4px;
}

.notes-row { margin-bottom: 6px; line-height: 1.45; font-size: 12px; }
.notes-row .label {
  font-weight: 700; color: var(--accent);
  display: block; margin-bottom: 1px;
}

/* Narrow / portrait iPad */
@media (max-width: 820px) {
  .row { grid-template-columns: 48px 1fr; }
  .row .hp { grid-column: 1 / -1; justify-content: flex-end; }
  .tracker { max-height: 60vh; }
}

@media (max-width: 540px) {
  .topbar h1 { font-size: 14px; }
  .topbar .round-pill { font-size: 11px; }
  .topbar button { padding: 0 6px; font-size: 12px; min-width: 32px; }
}
"""


JS = r"""
(function() {
  const slug = (ENCOUNTER.slug || ENCOUNTER.name || "encounter")
    .replace(/[^a-z0-9]+/gi, "_").toLowerCase();
  const STORAGE_KEY = "encounter:" + slug;

  const CONDITIONS = [
    "Blinded", "Charmed", "Concentration", "Deafened", "Frightened",
    "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified",
    "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious"
  ];

  function combatantId(c, i) {
    return c.id || (c.name || "c").replace(/[^a-z0-9]+/gi, "_").toLowerCase() + "_" + i;
  }

  function defaultState() {
    return {
      round: 1,
      activeId: null,
      combatants: ENCOUNTER.combatants.map((c, i) => ({
        id: combatantId(c, i),
        kind: c.kind || "npc",
        name: c.name,
        ac: c.ac,
        hp_max: c.hp_max,
        hp_current: (c.hp_current === null || c.hp_current === undefined) ? c.hp_max : c.hp_current,
        speed: c.speed || "",
        initiative: (c.initiative === undefined ? null : c.initiative),
        init_mod: c.init_mod || "",
        group: c.group || null,
        notes: c.notes || "",
        conditions: Array.isArray(c.conditions) ? c.conditions.slice() : []
      }))
    };
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || !Array.isArray(parsed.combatants)) return null;
      return parsed;
    } catch (e) { return null; }
  }
  function saveState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
  }

  let state = loadState() || defaultState();

  // ── Helpers ──────────────────────────────────────────────────────────────
  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, m =>
      ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[m]));
  }

  function sortedCombatants() {
    const list = state.combatants.slice();
    const origIndex = new Map(state.combatants.map((c, i) => [c.id, i]));
    list.sort((a, b) => {
      const ai = (a.initiative === null || a.initiative === undefined) ? -Infinity : a.initiative;
      const bi = (b.initiative === null || b.initiative === undefined) ? -Infinity : b.initiative;
      if (bi !== ai) return bi - ai;
      return origIndex.get(a.id) - origIndex.get(b.id);
    });
    return list;
  }

  function commitInit(c, inputEl) {
    const t = inputEl.value.trim();
    let newVal;
    if (t === "") {
      newVal = null;
    } else {
      const n = parseInt(t, 10);
      if (Number.isNaN(n)) {
        // revert to last good value
        inputEl.value = c.initiative === null ? "" : String(c.initiative);
        return;
      }
      newVal = n;
    }
    if (newVal === c.initiative) return;
    c.initiative = newVal;
    saveState();
    renderTracker();
  }

  function hpClass(hpCur, hpMax) {
    if (hpCur <= 0) return "bloodied";
    if (hpCur <= hpMax * 0.5) return "bloodied";
    if (hpCur <= hpMax * 0.75) return "low";
    return "";
  }

  // ── Tracker render ───────────────────────────────────────────────────────
  function renderTracker() {
    const root = document.getElementById("tracker-rows");
    root.innerHTML = "";
    const list = sortedCombatants();

    list.forEach(c => {
      const row = document.createElement("div");
      row.className = "row " + (c.kind || "npc");
      row.dataset.id = c.id;
      if (c.id === state.activeId) row.classList.add("active");
      if (c.hp_current <= 0) row.classList.add("dead");

      // Init (always-editable input; tapping it brings up the numeric keypad on iOS)
      const init = document.createElement("input");
      init.type = "text";
      init.inputMode = "numeric";
      init.pattern = "-?[0-9]*";
      init.maxLength = 3;
      init.className = "init" + (c.initiative === null ? " empty" : "");
      init.value = c.initiative === null ? "" : String(c.initiative);
      init.placeholder = "—";
      init.setAttribute("aria-label", "Initiative for " + c.name);
      // Don't let taps on the input toggle the row's active state.
      ["click", "touchstart", "mousedown"].forEach(ev => {
        init.addEventListener(ev, e => e.stopPropagation());
      });
      init.addEventListener("focus", () => init.select());
      init.addEventListener("blur", () => commitInit(c, init));
      init.addEventListener("keydown", (e) => {
        if (e.key === "Enter") { e.preventDefault(); init.blur(); }
      });
      row.appendChild(init);

      // Info
      const info = document.createElement("div");
      info.className = "info";
      const groupTag = c.group ? ' <span class="group-tag">[Group ' + escapeHtml(c.group) + ']</span>' : '';
      const initModBadge = (c.kind === "pc" && c.init_mod)
        ? '<span class="pc-init-mod">Init ' + escapeHtml(c.init_mod) + '</span>' : '';
      const speedBit = c.speed ? ' &middot; ' + escapeHtml(c.speed) : '';
      const conditionsHtml = c.conditions.length
        ? '<div class="conditions-pills">' +
            c.conditions.map(cn => '<span class="pill">' + escapeHtml(cn) + '</span>').join('') +
          '</div>'
        : '';
      info.innerHTML =
        '<div class="name">' + escapeHtml(c.name) + groupTag + '</div>' +
        '<div class="meta">' +
          '<span class="ac">AC ' + escapeHtml(c.ac) + '</span>' +
          speedBit +
          (initModBadge ? ' ' + initModBadge : '') +
        '</div>' +
        conditionsHtml;
      info.addEventListener("click", () => {
        state.activeId = (state.activeId === c.id) ? null : c.id;
        saveState(); renderTracker();
      });
      row.appendChild(info);

      // HP (horizontal: display + amt input + −/+ + conditions button on one line)
      const hp = document.createElement("div");
      hp.className = "hp";
      const cls = hpClass(c.hp_current, c.hp_max);
      hp.innerHTML =
        '<div class="hp-display ' + cls + '">' +
          escapeHtml(c.hp_current) + '<span class="sep">/</span>' + escapeHtml(c.hp_max) +
        '</div>' +
        '<div class="hp-controls">' +
          '<input type="number" inputmode="numeric" placeholder="amt" min="0">' +
          '<button class="dmg" title="Apply damage">&minus;</button>' +
          '<button class="heal" title="Apply healing">+</button>' +
        '</div>' +
        '<div class="controls">' +
          '<button class="cond-btn" title="Toggle conditions">Cond' +
            (c.conditions.length ? ' (' + c.conditions.length + ')' : '') +
          '</button>' +
        '</div>';
      const amt = hp.querySelector("input");
      hp.querySelector(".dmg").addEventListener("click", (ev) => {
        ev.stopPropagation();
        const n = parseInt(amt.value, 10);
        if (Number.isNaN(n) || n < 0) return;
        c.hp_current = Math.max(0, c.hp_current - n);
        amt.value = "";
        saveState(); renderTracker();
      });
      hp.querySelector(".heal").addEventListener("click", (ev) => {
        ev.stopPropagation();
        const n = parseInt(amt.value, 10);
        if (Number.isNaN(n) || n < 0) return;
        c.hp_current = Math.min(c.hp_max, c.hp_current + n);
        amt.value = "";
        saveState(); renderTracker();
      });
      const condBtn = hp.querySelector(".cond-btn");
      // Stop click propagation on the input/buttons so tapping them doesn't toggle active row.
      ["click", "touchstart"].forEach(ev => {
        amt.addEventListener(ev, e => e.stopPropagation());
      });
      row.appendChild(hp);

      // Conditions panel
      const condPanel = document.createElement("div");
      condPanel.className = "conditions-panel";
      condPanel.innerHTML = '<div class="pills">' +
        CONDITIONS.map(cn => {
          const on = c.conditions.indexOf(cn) >= 0;
          return '<button class="pill-toggle ' + (on ? 'active' : '') + '" data-c="' + cn + '">' + cn + '</button>';
        }).join('') + '</div>';
      condPanel.addEventListener("click", e => e.stopPropagation());
      condPanel.querySelectorAll(".pill-toggle").forEach(btn => {
        btn.addEventListener("click", () => {
          const cn = btn.dataset.c;
          const idx = c.conditions.indexOf(cn);
          if (idx >= 0) c.conditions.splice(idx, 1); else c.conditions.push(cn);
          saveState(); renderTracker();
        });
      });
      condBtn.addEventListener("click", (ev) => {
        ev.stopPropagation();
        condPanel.classList.toggle("open");
        condBtn.classList.toggle("active", condPanel.classList.contains("open"));
      });
      row.appendChild(condPanel);

      root.appendChild(row);
    });

    document.getElementById("round-num").textContent = state.round;
  }

  // ── Reference render ─────────────────────────────────────────────────────
  function renderReference() {
    const npcRoot = document.getElementById("npc-blocks");
    npcRoot.innerHTML = "";
    (ENCOUNTER.npc_blocks || []).forEach(b => {
      const div = document.createElement("div");
      div.className = "npc-block";
      let html = '<div class="npc-title">' + escapeHtml(b.title || b.name || '') + '</div>';
      if (b.stats)    html += '<div class="npc-stats">' + escapeHtml(b.stats) + '</div>';
      if (b.defenses) html += '<div class="npc-defenses">' + escapeHtml(b.defenses) + '</div>';
      (b.sections || []).forEach(s => {
        if (s.label) html += '<div class="npc-section-label">' + escapeHtml(s.label) + '</div>';
        (s.entries || []).forEach(e => {
          html += '<div class="npc-entry"><span class="entry-name">' +
            escapeHtml(e.name) + '</span>' + escapeHtml(e.text) + '</div>';
        });
      });
      div.innerHTML = html;
      npcRoot.appendChild(div);
    });

    const pcRoot = document.getElementById("pc-blocks");
    pcRoot.innerHTML = "";
    (ENCOUNTER.pc_blocks || []).forEach(p => {
      const div = document.createElement("div");
      div.className = "pc-block";
      const rows = [];
      const fields = [
        ["Name", p.header], ["Abilities", p.abilities], ["Saves", p.saves],
        ["Attacks", p.attacks], ["Spells", p.spells], ["Features", p.features]
      ];
      fields.forEach(([label, val]) => {
        if (val) rows.push('<div class="pc-row"><span class="label">' +
          label + ':</span>' + escapeHtml(val) + '</div>');
      });
      div.innerHTML = rows.join('');
      pcRoot.appendChild(div);
    });

    const notesRoot = document.getElementById("notes-section");
    notesRoot.innerHTML = "";
    (ENCOUNTER.notes || []).forEach(n => {
      const div = document.createElement("div");
      div.className = "notes-row";
      div.innerHTML = '<span class="label">' + escapeHtml(n.label || '') + '</span>' +
        escapeHtml(n.text || '');
      notesRoot.appendChild(div);
    });
  }

  // ── Turn order ───────────────────────────────────────────────────────────
  function nextTurn() {
    const list = sortedCombatants().filter(c => c.initiative !== null && c.initiative !== undefined);
    if (list.length === 0) return;
    if (!state.activeId) {
      state.activeId = list[0].id;
    } else {
      const idx = list.findIndex(c => c.id === state.activeId);
      if (idx === -1 || idx === list.length - 1) {
        state.activeId = list[0].id;
        state.round += 1;
      } else {
        state.activeId = list[idx + 1].id;
      }
    }
    saveState(); renderTracker();
    scrollActiveIntoView();
  }
  function prevTurn() {
    const list = sortedCombatants().filter(c => c.initiative !== null && c.initiative !== undefined);
    if (list.length === 0) return;
    if (!state.activeId) {
      state.activeId = list[list.length - 1].id;
    } else {
      const idx = list.findIndex(c => c.id === state.activeId);
      if (idx <= 0) {
        state.activeId = list[list.length - 1].id;
        state.round = Math.max(1, state.round - 1);
      } else {
        state.activeId = list[idx - 1].id;
      }
    }
    saveState(); renderTracker();
    scrollActiveIntoView();
  }
  function scrollActiveIntoView() {
    if (!state.activeId) return;
    const el = document.querySelector('.row[data-id="' + state.activeId + '"]');
    if (el && el.scrollIntoView) el.scrollIntoView({block: "nearest", behavior: "smooth"});
  }

  function reset() {
    if (!window.confirm("Reset encounter? This clears HP, conditions, round, and active turn.")) return;
    state = defaultState();
    saveState();
    renderTracker();
  }

  // ── Wire up ──────────────────────────────────────────────────────────────
  document.getElementById("encounter-name").textContent = ENCOUNTER.name || "Encounter";
  document.title = "Encounter - " + (ENCOUNTER.name || "Worksheet");
  document.getElementById("next-btn").addEventListener("click", nextTurn);
  document.getElementById("prev-btn").addEventListener("click", prevTurn);
  document.getElementById("reset-btn").addEventListener("click", reset);

  renderReference();
  renderTracker();
})();
"""


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")
    return s or "encounter"


def html_escape(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_html(spec):
    name = spec.get("name", "Encounter")
    # Embed JSON directly as a JS literal (JSON is a subset of JS object syntax).
    # Escape `</` so a value containing `</script>` can't break out of the
    # surrounding <script> tag, and escape U+2028/U+2029 which are valid in JSON
    # strings but were illegal as raw chars in JS string literals before ES2019.
    data_json = (
        json.dumps(spec, ensure_ascii=False)
        .replace("</", "<\\/")
        .replace(" ", "\\u2028")
        .replace(" ", "\\u2029")
    )
    return (
        HTML_TEMPLATE
        .replace("__NAME__", html_escape(name))
        .replace("__CSS__", CSS)
        .replace("__JS__", JS)
        .replace("__DATA__", data_json)
    )


def load_spec():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    arg = sys.argv[1]
    if arg == "-":
        return json.load(sys.stdin)
    if arg.lstrip().startswith("{"):
        return json.loads(arg)
    with open(arg) as f:
        return json.load(f)


def main():
    spec = load_spec()
    slug = spec.get("slug") or slugify(spec.get("name", "encounter"))
    out_dir = Path(__file__).resolve().parent.parent / "encounters"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / (slug + ".html")
    out_path.write_text(build_html(spec), encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
