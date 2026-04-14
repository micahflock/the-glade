# /encounter-worksheet

# Generate a D&D 5e combat encounter worksheet as an .xlsx spreadsheet
# ready to upload to Google Sheets. Reads NPC stat blocks from creatures/
# and PC sheets from party/, rolls initiative and HP, and builds a
# formatted single-tab worksheet with initiative tracker, stat references,
# and encounter notes.

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

### Step 2: Build the .xlsx

Write and execute a Python script using openpyxl that creates a single-tab
worksheet. Follow the formatting spec exactly.

**Section 1: INITIATIVE TRACKER** (starts row 1)

Header row (bold, background #D6E4F0):
  Init | Name | AC | HP Max | HP Current | Speed | Status/Conditions | Notes

- One row per combatant
- NPCs: fill rolled initiative, rolled HP as both Max and Current
- PCs: leave Initiative and HP Current blank (DM fills during play),
  fill HP Max from sheet
- Sort all rows by initiative descending; PCs without init go at bottom
- Grouped creatures sort together by their shared initiative, with
  group members listed consecutively (Ant 1 [A], Ant 2 [A], ... then
  Ant 7 [B], Ant 8 [B], ...)
- Alternating row shading: white / #F2F2F2
- Thin borders around the entire tracker
- FREEZE PANES on the row after the last tracker entry — the tracker
  stays pinned at the top while scrolling through reference material

**Section 2: NPC STAT BLOCK REFERENCE** (after 2-row gap)

Section header: "NPC REFERENCE" — bold white text, #4472C4 background,
merged across columns A–H.

For each unique NPC type (not each numbered instance):
- Labels in column B (bold), content merged across C–H (wrap text)
- Row: Name → "[Name] — [size] [type], [alignment]"
- Row: Stats → "AC [X] ([type]) | HP [X] ([dice]) | Speed [X] |
  STR [X](+[X]) DEX [X](+[X]) CON [X](+[X]) INT [X](+[X])
  WIS [X](+[X]) CHA [X](+[X])"
- Row: Defenses → saves, resistances, immunities, senses, languages, PB
  (omit row if none apply)
- Row(s): Each trait, action, bonus action, reaction — name in B (bold),
  full text in C–H (merged, wrapped). Include section labels
  ("ACTIONS", "REACTIONS", etc.) as sub-headers when switching categories.
- Blank row between NPC types

**Section 3: PC COMBAT REFERENCE** (after 2-row gap)

Section header: "PC REFERENCE" — same style as NPC header.

For each PC:
- Row: Name → "[Name] — [Class] [Level] | [Species] | AC [X] | HP [X] |
  Speed [X] | Passive Perception [X]"
- Row: Abilities → all six scores with mods on one line
- Row: Saves → proficient saves with values
- Row: Attacks → weapon name, to-hit, damage; spell attack/DC if caster
- Row: Spells → spell list by level (only if caster)
- Row: Features → notable combat features
- Blank row between PCs

**Section 4: ENCOUNTER DETAILS** (after 2-row gap, bottom of sheet)

Section header: "ENCOUNTER DETAILS" — same style.

- Encounter name (bold, 14pt)
- Terrain/setting notes, tactical reminders, DM notes (merged, wrapped)
- At the bottom so it doesn't waste screen real estate during combat

### Formatting spec

- Font: Arial 10pt for data, 12pt bold for section headers,
  14pt bold for encounter title
- Column widths: A/Init (8), B/Name (28), C/AC (6), D/HP Max (9),
  E/HP Current (11), F/Speed (8), G/Status (22), H/Notes (28)
- Colors: #D6E4F0 (tracker header), #4472C4 + white text (section
  headers), alternating white / #F2F2F2 (data rows)
- Wrap text on all description/content cells
- Row heights: 15px for data rows, 30-50px for wrapped description rows
- Avoid Excel-only features — the file must work in Google Sheets

### Step 3: Save and present

Save to encounters/[encounter_name_slug].xlsx
Tell the DM the file path and that it's ready to upload to Google Sheets.

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
  Encounter Details section.
- If the user provides creature names that don't match any creatures/*.yaml
  file, accept direct input and flag with [SLOP CHECK] any values you
  had to invent.
