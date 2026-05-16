# /encounter-worksheet

# Generate a D&D 5e combat encounter worksheet as a self-contained
# interactive .html file, designed for offline use on iPad during a
# session. Reads NPC stat blocks from creatures/ and PC sheets from
# party/, rolls initiative and HP, and produces a single HTML file
# with:
#   - An initiative tracker with editable PC initiative, HP +/- controls,
#     a per-row HP bar gauge, and condition pill toggles
#   - A sticky "active reference" panel pinned above the tracker that
#     shows the stat block for the current turn (or for a row the DM
#     has tapped to pin)
#   - Turn/round counter with Next/Prev buttons (clears any pinned row)
#   - Collapsible full NPC/PC reference and encounter notes below the
#     tracker for browsing
# State (HP, conditions, current turn, round, pinned row) persists in
# the browser's localStorage keyed by encounter slug.

## Input Handling

Accepted inputs (any combination):

1. **NPC stat blocks** — Specify creatures by name from creatures/*.yaml,
   or provide stat blocks directly (text, image, any format).
   Include the count for each type (e.g. "3 leafcutter workers and 1 fire
   ant commander"). Ask for count if not specified.
2. **PC character sheets** — Read from party/*.yaml if available.
   If party/ has no character files, accept photos or text descriptions
   and extract combat essentials. Confirm your reading of handwritten
   sheets with the DM before proceeding.
3. **Terrain/setting notes** — Free-text description of the environment,
   hazards, tactical features, special rules. Optional.
4. **Encounter name** — A short label for the encounter. Ask if not given.

## Phase 1 — Parse and Confirm (stop after this and wait)

Read all inputs. For each NPC stat block (from creatures/*.yaml or direct
input), extract:
- Name, AC (value and type), HP (value and dice expression), Speed
- Full ability scores and modifiers (need DEX mod for initiative)
- Saving throws, skills, senses, passive Perception
- Resistances, immunities, condition immunities
- All traits, actions, bonus actions, reactions, legendary actions
- CR and proficiency bonus

For each PC (from party/*.yaml or direct input), extract combat essentials:
- Name (and player name if available)
- Class/level, species
- AC, HP max, Speed, Initiative modifier
- Ability scores and modifiers
- Saving throw proficiencies and values
- Passive Perception
- Key attacks: weapon name, to-hit, damage
- Spell save DC and spell attack bonus (if caster)
- Notable combat features (Sneak Attack, Extra Attack, Channel Divinity, etc.)
- Spell list (names grouped by level, if caster)

Present this summary:

-----

ENCOUNTER WORKSHEET — [Encounter Name]

NPCs:
- [Name] x[count] — CR [X], AC [X], HP [dice] (~avg [X]), Init DEX +[X]
- [Name] x[count] — ...

PCs:
- [Name] — [Class] [Level], AC [X], HP [X], Init +[X]
- [Name] — ...

TERRAIN: [summary of setting/hazards, or "none provided"]

INITIATIVE GROUPING:
For any NPC type with 4+ copies, ask the DM:
"[Name] x[count] — roll individually, or group into N initiative groups?"
List the confirmed grouping plan here:
- [Name] x[count]: [individual / N groups of ~X]

FLAGGED:
- [missing data, ambiguous readings, stat inconsistencies]

[SLOP CHECK]:
- [anything inferred rather than read from source]

-----

Stop. Wait for DM to confirm, adjust counts/grouping, or provide missing info.

## Phase 2 — Generate Worksheet (only after DM confirms)

### Step 1: Roll dice for NPCs

Use scripts/roll_dice.py to pre-roll initiative and HP:

    python3 scripts/roll_dice.py '{"npcs": [
      {"name": "Ant", "hp_dice": "2d8+2", "dex_mod": 1, "count": 12, "groups": 2},
      {"name": "Commander", "hp_dice": "5d10+10", "dex_mod": 3, "count": 1}
    ]}'

Parameters per NPC type:
- name: creature name
- hp_dice: dice expression from stat block (e.g. "2d8+4") or flat number
- dex_mod: DEX modifier for initiative rolls
- count: total number of this creature type
- groups: number of initiative groups (omit for individual rolls).
  All members of a group share one initiative roll. HP is always
  rolled individually.

The script numbers creatures automatically (Ant 1, Ant 2, etc.) and
tags grouped creatures with a letter (Ant 1 [A], Ant 7 [B], etc.).

### Step 2: Build the encounter spec JSON

Write a JSON file to encounters/[slug].json with the encounter data.
This is the single input to the HTML build script. The shape:

```json
{
  "name": "Winter Farm Encounter",
  "slug": "winter_farm_encounter",
  "combatants": [
    {
      "id": "skull_cracker",
      "kind": "npc",
      "name": "Skull-Cracker",
      "ac": 16,
      "hp_max": 162,
      "hp_current": 162,
      "speed": "30 ft., climb 20 ft.",
      "initiative": 4,
      "group": null,
      "notes": ""
    },
    {
      "id": "tabby",
      "kind": "pc",
      "name": "Tabatha Starr (Heather)",
      "ac": 14,
      "hp_max": 31,
      "hp_current": 31,
      "speed": "30 ft.",
      "initiative": null,
      "init_mod": "+5",
      "notes": "Dread Ambusher rd 1: +10 spd, bonus attack +1d8"
    }
  ],
  "npc_blocks": [
    {
      "title": "Skull-Cracker — Large Monstrosity (ant), Lawful Evil",
      "stats": "AC 16 (natural armor) | HP 162 (16d10+64) | Speed 30 ft., climb 20 ft. | STR 20 (+5) DEX 10 (+0) CON 18 (+4) INT 6 (-2) WIS 12 (+1) CHA 10 (+0)",
      "defenses": "Skills: Athletics +8 | Senses: ... | CR 6 (2300 XP) | PB +3",
      "sections": [
        { "label": "TRAITS",  "entries": [{"name": "Heated Body", "text": "..."}] },
        { "label": "ACTIONS", "entries": [
          {"name": "Multiattack", "text": "..."},
          {"name": "Crusher's Bite", "text": "..."}
        ]}
      ]
    }
  ],
  "pc_blocks": [
    {
      "header": "Tabatha Starr (Heather) — Ranger 3 (Gloomstalker) | ...",
      "abilities": "STR 14 (+2) DEX 16 (+3) ...",
      "saves": "STR +4 (prof), DEX +5 (prof). Others use ability mod.",
      "attacks": "Longbow +7, 1d8+3 piercing (150/600) [Archery] | ...",
      "spells": "...",
      "features": "Favored Enemy: Monstrosities ..."
    }
  ],
  "notes": [
    {"label": "Setup", "text": "..."},
    {"label": "Difficulty note", "text": "..."}
  ]
}
```

Field rules:

- **combatants** — one entry per individual (use the rolled output from
  roll_dice.py: each grouped creature still gets its own row, sharing
  initiative). NPCs get rolled `initiative` and rolled `hp_current = hp_max`.
  PCs get `initiative: null` (DM enters at the table) and `init_mod` as a
  display reminder ("+5"). Use `kind: "npc"` or `kind: "pc"`. Include
  `group: "A"` etc. only when the creature shares an initiative group.

- **npc_blocks** — one block per unique creature TYPE, not per individual.
  `title` is a one-line header. `stats` is the AC/HP/Speed/abilities line.
  `defenses` covers saves/resistances/immunities/senses/languages/CR/PB
  (omit if none apply). `sections` is the list of rule blocks — TRAITS,
  ACTIONS, BONUS ACTIONS, REACTIONS, LEGENDARY ACTIONS — each with a
  label and an entries array of `{name, text}` pairs. Be COMPLETE: every
  trait, action, and ability the DM might need at the table.

- **pc_blocks** — one block per PC. `header` is a one-line summary
  (name/class/species/AC/HP/speed/passive). Other fields are short text
  blocks. Omit `spells` for non-casters.

- **notes** — encounter notes pinned to the bottom of the worksheet.
  Use labels like Setup, Difficulty, Tactics, Recharge tracking, Triggers,
  NPC Registry cross-ref, etc.

#### Reference matching (active-reference panel)

The pinned reference panel looks up each combatant's stat block by
**name prefix**. The lookup strips instance and player suffixes from
the combatant `name` and matches it against the base of a block's
`title` (NPCs) or `header` (PCs). Examples:

| Combatant `name`             | Strips to            | Must match prefix of            |
|------------------------------|----------------------|---------------------------------|
| `Skull-Cracker`              | `Skull-Cracker`      | npc_block `title`               |
| `Leafcutter Worker 3 [A]`    | `Leafcutter Worker`  | npc_block `title`               |
| `Tabatha Starr (Heather)`    | `Tabatha Starr`      | pc_block `header`               |

To make matching work cleanly:

- NPC `title` should lead with the creature's bare name, then a separator
  (em-dash, en-dash, hyphen, or open-paren). Good:
  `"Skull-Cracker — Large Monstrosity (ant), Lawful Evil"` or
  `"Pheromone Crowner (Spring) — Medium Monstrosity (ant), Lawful Evil"`.
- PC `header` should lead with the character's name, then a separator
  (em-dash works best). Good:
  `"Tabatha Starr — Ranger 3 (Gloomstalker) | ..."`.
- Combatant names for grouped/numbered NPCs follow `"Name N [LETTER]"`
  (what roll_dice.py emits) — the lookup handles the suffix stripping.
- Combatant names for PCs may include the player name in parens
  (e.g. `"Tabatha Starr (Heather)"`) — the parens are stripped.

If a combatant can't be matched, the active-reference panel shows
"No reference block matched for …" — that's the signal to fix the
combatant name or the block title.

### Step 3: Build the HTML

    python3 scripts/build_encounter.py encounters/[slug].json

This writes encounters/[slug].html — a single self-contained file. Fonts
load from Google Fonts (the page degrades to system serifs offline), but
all layout, styling, and interactive behavior is inline. You only need
to provide the JSON.

### Step 4: Save and present

Tell the DM the file path. Note that:
- The .html file is portable — drop it in iCloud/Files and open in
  **Safari** on iPhone/iPad (or any browser) to use offline.
- On iPhone/iPad: opening from the Files app uses Quick Look preview,
  which won't run JavaScript and the page will appear empty. Instead,
  tap the share icon in Files → "Open in Safari", or open Safari first
  and use the address bar.
- State (HP, conditions, current turn, round) auto-saves to the browser's
  localStorage keyed by the encounter slug. Reset button at the top
  clears it.
- The .json spec stays alongside as the source of truth — re-running
  build_encounter.py rebuilds the HTML if you tweak the spec.

## Key Rules

- Always confirm inputs in Phase 1 before generating. Errors in encounter
  worksheets surface at the table when it's too late to fix them.
- For any NPC type with 4+ copies, proactively ask about initiative
  grouping in Phase 1. Don't assume individual or grouped — ask.
- NPC reference blocks must be COMPLETE — every trait, action, and ability.
  The DM should never need to look anything else up during combat.
- PC reference should include everything the DM needs to adjudicate effects
  targeting PCs (saves, AC, HP, passive Perception, notable features).
- Do not add creatures or PCs the DM didn't specify.
- When reading from creatures/*.yaml, use the data as-is. Don't modify
  stat block values.
- Cross-reference memory/NPC_Registry.yaml — if any NPCs in the encounter
  are tracked there, note relevant party_history or disposition in the
  notes section.
- If the user provides creature names that don't match any creatures/*.yaml
  file, accept direct input and flag with [SLOP CHECK] any values you
  had to invent.
- Keep the .json spec file alongside the .html. If the DM asks for a
  tweak (extra creature, terrain note, etc.), edit the .json and rerun
  the build script — don't hand-edit the .html.
