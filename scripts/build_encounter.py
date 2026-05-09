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
  --bg: #f7f6f0;
  --panel: #ffffff;
  --ink: #1c1c1c;
  --muted: #5b5b5b;
  --accent: #4472c4;
  --accent-light: #d6e4f0;
  --shade: #f2f2f2;
  --border: #d0d0d0;
  --good: #2e7d32;
  --bad: #c62828;
  --warn: #ef6c00;
  --active: #fff3a3;
  --active-border: #ef6c00;
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
  background: var(--accent); color: white;
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px;
  gap: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.18);
}
.topbar-left { display: flex; align-items: baseline; gap: 12px; min-width: 0; }
.topbar h1 {
  font-size: 18px; font-weight: 600;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.topbar .round-pill {
  background: rgba(255,255,255,0.18); padding: 4px 10px;
  border-radius: 12px; font-size: 14px; white-space: nowrap;
}
.topbar-right { display: flex; gap: 6px; align-items: center; }
.topbar button {
  min-height: 44px; min-width: 44px;
  padding: 0 12px;
  border: 1px solid rgba(255,255,255,0.35);
  background: rgba(255,255,255,0.10);
  color: white; border-radius: 8px;
  font-weight: 600;
  font-size: 15px;
}
.topbar button.primary {
  background: white; color: var(--accent); border-color: white;
}
.topbar button.danger { background: rgba(0,0,0,0.18); }
.topbar button:active { opacity: 0.65; }

main { padding: 0; max-width: 1200px; margin: 0 auto; }

/* Tracker */
.tracker {
  background: var(--panel);
  padding: 12px 12px 8px;
  border-bottom: 2px solid var(--border);
  position: sticky;
  top: 64px;
  z-index: 40;
  max-height: 65vh;
  overflow-y: auto;
}
.tracker-header {
  display: flex; justify-content: space-between; align-items: baseline;
  margin-bottom: 8px;
  gap: 10px;
}
.tracker h2 {
  font-size: 13px; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.06em;
}
.tracker .hint { font-size: 12px; color: var(--muted); }

#tracker-rows { display: grid; gap: 6px; }

.row {
  display: grid;
  grid-template-columns: 56px 1fr auto;
  gap: 10px;
  padding: 8px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  align-items: center;
}
.row.npc { border-left: 4px solid var(--accent); }
.row.pc  { border-left: 4px solid var(--good); }
.row.active {
  background: var(--active);
  box-shadow: 0 0 0 2px var(--active-border);
}
.row.dead { opacity: 0.5; background: var(--shade); }
.row.dead .name { text-decoration: line-through; }

.row .init {
  font-size: 22px; font-weight: 700; text-align: center;
  background: var(--accent-light);
  border-radius: 6px;
  padding: 8px 0;
  min-width: 56px; min-height: 44px;
  cursor: pointer;
  user-select: none;
}
.row .init.empty { background: var(--shade); color: var(--muted); }

.row .info { min-width: 0; }
.row .name {
  font-weight: 600; font-size: 17px; line-height: 1.2;
  word-wrap: break-word;
}
.row .name .group-tag {
  color: var(--muted); font-weight: 500; font-size: 13px;
  margin-left: 4px;
}
.row .meta { color: var(--muted); font-size: 13px; margin-top: 2px; }
.row .meta .ac { font-weight: 600; color: var(--ink); }
.row .meta .pc-init-mod {
  display: inline-block;
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 600;
  padding: 1px 6px; border-radius: 4px;
  margin-left: 4px;
}
.row .conditions-pills {
  display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px;
}
.row .conditions-pills .pill {
  background: var(--bad); color: white;
  border-radius: 12px; padding: 2px 8px; font-size: 12px;
  font-weight: 600;
}

.row .hp {
  display: flex; flex-direction: column; align-items: flex-end;
  gap: 4px; min-width: 200px;
}
.row .hp-display {
  font-size: 20px; font-weight: 700;
  min-width: 90px; text-align: right;
}
.row .hp-display .sep { color: var(--muted); font-weight: 400; }
.row .hp-display.low { color: var(--warn); }
.row .hp-display.bloodied { color: var(--bad); }

.row .hp-bar {
  width: 100%; height: 4px; background: var(--shade);
  border-radius: 2px; overflow: hidden;
}
.row .hp-bar-fill {
  height: 100%; background: var(--good);
  transition: width 0.2s;
}
.row .hp-bar-fill.low { background: var(--warn); }
.row .hp-bar-fill.bloodied { background: var(--bad); }

.row .hp-controls { display: flex; gap: 4px; align-items: center; }
.row .hp-controls input {
  width: 64px; height: 40px;
  font-size: 16px; text-align: center;
  border: 1px solid var(--border); border-radius: 6px;
  font-family: inherit;
}
.row .hp-controls button {
  min-height: 40px; min-width: 40px;
  padding: 0 12px;
  border: 1px solid var(--border); border-radius: 6px;
  background: var(--shade); font-weight: 700;
  font-size: 18px;
}
.row .hp-controls .dmg { background: #ffe4e4; color: var(--bad); border-color: #f4b3b3; }
.row .hp-controls .heal { background: #e4f5e4; color: var(--good); border-color: #b3d8b3; }

.row .controls {
  display: flex; gap: 4px; justify-content: flex-end;
}
.row .controls button {
  min-height: 36px; min-width: 36px;
  padding: 0 10px;
  border: 1px solid var(--border); border-radius: 6px;
  background: var(--shade);
  font-size: 14px;
}
.row .controls button.active {
  background: var(--accent); color: white; border-color: var(--accent);
}

.row .conditions-panel {
  grid-column: 1 / -1;
  margin-top: 4px; padding: 10px;
  background: var(--shade); border-radius: 6px;
  display: none;
}
.row .conditions-panel.open { display: block; }
.row .conditions-panel .pills {
  display: flex; flex-wrap: wrap; gap: 6px;
}
.row .conditions-panel .pill-toggle {
  min-height: 38px; padding: 0 12px;
  background: var(--panel);
  border: 1px solid var(--border); border-radius: 19px;
  font-size: 14px; font-weight: 500;
}
.row .conditions-panel .pill-toggle.active {
  background: var(--bad); color: white; border-color: var(--bad);
}
.row .conditions-panel .pill-toggle:active { opacity: 0.7; }

/* Reference */
.reference { padding: 16px; }
.reference details {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-bottom: 12px;
  overflow: hidden;
}
.reference summary {
  padding: 12px 16px;
  background: var(--accent); color: white;
  cursor: pointer;
  list-style: none;
  user-select: none;
  display: flex; align-items: center; justify-content: space-between;
}
.reference summary::-webkit-details-marker { display: none; }
.reference summary .section-title { font-size: 16px; font-weight: 700; }
.reference summary::after { content: "\25be"; font-size: 14px; }
.reference details[open] summary::after { content: "\25b4"; }
.reference details > div { padding: 12px 16px; }

.npc-block, .pc-block {
  margin-bottom: 14px; padding: 12px;
  border: 1px solid var(--border); border-radius: 8px;
  background: var(--shade);
}
.npc-block:last-child, .pc-block:last-child { margin-bottom: 0; }
.npc-title { font-size: 16px; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }
.npc-stats, .npc-defenses {
  font-size: 14px; color: var(--ink);
  margin-bottom: 6px; line-height: 1.45;
}
.npc-section-label {
  font-size: 12px; font-weight: 700; color: var(--accent);
  text-transform: uppercase; letter-spacing: 0.06em;
  margin: 10px 0 4px;
  padding-bottom: 2px;
  border-bottom: 1px solid var(--border);
}
.npc-entry { margin-bottom: 6px; line-height: 1.45; font-size: 14px; }
.npc-entry .entry-name { font-weight: 700; }
.npc-entry .entry-name::after { content: ". "; }

.pc-row { margin-bottom: 4px; line-height: 1.45; font-size: 14px; }
.pc-row .label {
  font-weight: 700; color: var(--accent);
  margin-right: 6px;
}

.notes-row { margin-bottom: 10px; line-height: 1.5; font-size: 14px; }
.notes-row .label {
  font-weight: 700; color: var(--accent);
  display: block; margin-bottom: 2px;
}

/* Narrow / portrait iPad */
@media (max-width: 820px) {
  .row { grid-template-columns: 56px 1fr; }
  .row .hp { grid-column: 1 / -1; align-items: stretch; }
  .row .hp-display { text-align: left; }
  .tracker { max-height: 55vh; }
}

@media (max-width: 540px) {
  .topbar h1 { font-size: 15px; }
  .topbar .round-pill { font-size: 12px; }
  .topbar button { padding: 0 8px; font-size: 13px; }
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

      // Init
      const init = document.createElement("div");
      init.className = "init" + (c.initiative === null ? " empty" : "");
      init.textContent = c.initiative === null ? "—" : c.initiative;
      init.title = "Tap to edit initiative";
      init.addEventListener("click", (ev) => {
        ev.stopPropagation();
        const cur = c.initiative === null ? "" : String(c.initiative);
        const label = "Initiative for " + c.name + (c.init_mod ? "  (mod " + c.init_mod + ")" : "");
        const v = window.prompt(label + ":", cur);
        if (v === null) return;
        const t = v.trim();
        if (t === "") {
          c.initiative = null;
        } else {
          const n = parseInt(t, 10);
          if (Number.isNaN(n)) return;
          c.initiative = n;
        }
        saveState(); renderTracker();
      });
      row.appendChild(init);

      // Info
      const info = document.createElement("div");
      info.className = "info";
      const groupTag = c.group ? ' <span class="group-tag">[Group ' + escapeHtml(c.group) + ']</span>' : '';
      const initModBadge = (c.kind === "pc" && c.init_mod)
        ? '<span class="pc-init-mod">Init ' + escapeHtml(c.init_mod) + '</span>' : '';
      const speedBit = c.speed ? ' &middot; ' + escapeHtml(c.speed) : '';
      info.innerHTML =
        '<div class="name">' + escapeHtml(c.name) + groupTag + '</div>' +
        '<div class="meta">' +
          '<span class="ac">AC ' + escapeHtml(c.ac) + '</span>' +
          speedBit +
          (initModBadge ? ' ' + initModBadge : '') +
        '</div>' +
        '<div class="conditions-pills">' +
          c.conditions.map(cn => '<span class="pill">' + escapeHtml(cn) + '</span>').join('') +
        '</div>';
      info.addEventListener("click", () => {
        state.activeId = (state.activeId === c.id) ? null : c.id;
        saveState(); renderTracker();
      });
      row.appendChild(info);

      // HP
      const hp = document.createElement("div");
      hp.className = "hp";
      const cls = hpClass(c.hp_current, c.hp_max);
      const pct = Math.max(0, Math.min(100, (c.hp_current / Math.max(1, c.hp_max)) * 100));
      hp.innerHTML =
        '<div class="hp-display ' + cls + '">' +
          escapeHtml(c.hp_current) + '<span class="sep">/</span>' + escapeHtml(c.hp_max) +
        '</div>' +
        '<div class="hp-bar"><div class="hp-bar-fill ' + cls + '" style="width: ' + pct + '%"></div></div>' +
        '<div class="hp-controls">' +
          '<input type="number" inputmode="numeric" placeholder="amt" min="0">' +
          '<button class="dmg" title="Apply damage">&minus;</button>' +
          '<button class="heal" title="Apply healing">+</button>' +
        '</div>' +
        '<div class="controls">' +
          '<button class="cond-btn" title="Toggle conditions">Conditions ' +
            (c.conditions.length ? '(' + c.conditions.length + ')' : '') +
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
