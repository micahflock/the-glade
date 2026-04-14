# /stat-block

# Generate a D&D 5e creature or NPC stat block as a YAML file.

# Accepts flexible input: a brief concept ("CR 4 shieldbug guard"), a pasted
# stat block from another source, or the output of /magic-bug-generator.
# Fills gaps with sensible 5e defaults. Asks for CR if not provided.

## Input Handling

Detect which input format was provided:

1. **Concept prompt** — a brief description like "CR 4 shieldbug guard" or
   "a sneaky earwig rogue, level-appropriate for a party of 3rd-level PCs."
   Generate a full stat block from scratch using 5e 2024 rules.
2. **Pasted stat block** — a full or partial stat block from any source
   (D&D Beyond, homebrew doc, markdown, plain text, image).
   Extract all data, reformat into the YAML structure below.
3. **Magic Bug Generator output** — structured output from /magic-bug-generator.
   Use the creature concept, archetype, notable features, and a single zone's
   mechanics. Ask which zone if not specified.

**If the input does not include a CR** (or enough context to infer one),
ask: "What CR should this creature be?" Do not proceed until you have a CR.

## Phase 1 — Draft and Confirm (stop after this and wait)

Read the input. Generate the stat block using 5e 2024 rules. Present this
summary for review:

-----

STAT BLOCK DRAFT — [Creature Name]

CR [X] | [Size] [Type] | [Alignment]
AC [X] ([type]) | HP [X] ([dice]) | Speed [X]

STR [score](+mod)  DEX [score](+mod)  CON [score](+mod)
INT [score](+mod)  WIS [score](+mod)  CHA [score](+mod)

KEY FEATURES:
- [Trait/action name]: [one-line summary]
- [Trait/action name]: [one-line summary]
- [...]

SECTIONS INCLUDED: [Traits, Actions, Bonus Actions, Reactions, etc.]
SECTIONS OMITTED: [e.g. "Legendary Actions — not a boss creature"]

SOURCE: [concept prompt / pasted stat block / magic-bug-generator ([zone])]
DECISIONS MADE:
- [any gap the DM should know about, e.g. "No speed given; defaulted to 30 ft."]
- [any rebalancing, e.g. "Adjusted damage from 3d10 to 2d8+3 to fit CR 4"]

[SLOP CHECK] flags:
- [anything invented wholesale that the DM should verify]

-----

Stop. Wait for DM to confirm, adjust, or request changes.

## Phase 2 — Write YAML (only after DM confirms)

Write to creatures/[name_slug].yaml using the structure below.
**Only include sections that have content.** Do not include empty sections,
placeholder sections, or sections with null values.

-----

# creatures/[name_slug].yaml

creature:
  name:
  size:               # Tiny / Small / Medium / Large / Huge / Gargantuan
  type:               # Beast, Monstrosity, Humanoid, Aberration, etc.
  alignment:
  source:             # "original", "adapted from [source]", "magic-bug-generator"

combat:
  ac:
    value:
    type:             # "natural armor", "leather armor", etc.
  hp:
    value:
    hit_dice:         # e.g. "8d8+16"
  speed: []           # e.g. ["30 ft.", "fly 60 ft.", "swim 30 ft."]
  cr:
    rating:           # number or fraction: 4, "1/2", "1/4"
    xp:
    proficiency_bonus:

ability_scores:
  strength:     { score: , modifier: }
  dexterity:    { score: , modifier: }
  constitution: { score: , modifier: }
  intelligence: { score: , modifier: }
  wisdom:       { score: , modifier: }
  charisma:     { score: , modifier: }

defenses:                   # omit entire section if nothing applies
  saving_throws: []         # e.g. ["DEX +5", "WIS +3"]
  damage_resistances: []
  damage_immunities: []
  condition_immunities: []

senses: []                  # e.g. ["darkvision 60 ft.", "tremorsense 30 ft."]
passive_perception:
languages: []

skills: []                  # e.g. ["Perception +5", "Stealth +4"]

traits:                     # omit if none
  - name:
    description: >

actions:
  - name:
    description: >

bonus_actions:              # omit if none
  - name:
    description: >

reactions:                  # omit if none
  - name:
    description: >

legendary_actions:          # omit unless specifically warranted — see Key Rules
  budget:                   # actions per round
  actions:
    - name:
      cost:                 # 1, 2, or 3
      description: >

roleplaying:                # include for named NPCs, omit for generic creatures
  personality:
  motivation:
  tactics:                  # how they fight

-----

## CR Reference Table (5e 2024 guidelines)

Use this table to sanity-check generated stats. Creatures can deviate —
a glass cannon might have low HP but high damage — but the overall
offensive + defensive CR should average to the target.

CR  | Prof | AC | HP        | Atk  | Dmg/Rd | Save DC
----|------|----|-----------|------|--------|--------
1/4 | +2   | 13 | 36-49     | +3   | 4-5    | 13
1/2 | +2   | 13 | 50-70     | +3   | 6-8    | 13
1   | +2   | 13 | 71-85     | +3   | 9-14   | 13
2   | +2   | 13 | 86-100    | +3   | 15-20  | 13
3   | +2   | 13 | 101-115   | +4   | 21-26  | 13
4   | +2   | 14 | 116-130   | +5   | 27-32  | 14
5   | +3   | 15 | 131-145   | +6   | 33-38  | 15
6   | +3   | 15 | 146-160   | +6   | 39-44  | 15
7   | +3   | 15 | 161-175   | +6   | 45-50  | 15
8   | +3   | 16 | 176-190   | +7   | 51-56  | 16
9   | +4   | 16 | 191-205   | +7   | 57-62  | 16
10  | +4   | 17 | 206-220   | +7   | 63-68  | 16

## Key Rules

- **Only include sections that apply.** Most creatures need only Traits and
  Actions. Do NOT add Legendary Actions, Bonus Actions, or Reactions unless
  the input specifically calls for them or the creature concept clearly
  warrants them (e.g. an explicit boss encounter, a creature whose identity
  revolves around a reaction). When in doubt, leave them out.
- **Ability score math must be correct:**
  modifier = floor((score - 10) / 2)
- **HP must match hit dice:**
  hp = (number of dice x ceil(average die roll)) + (number of dice x CON mod)
  Use the size-appropriate hit die (Tiny d4, Small d6, Medium d8, Large d10,
  Huge d12, Gargantuan d20).
- **Cross-reference memory/NPC_Registry.yaml** — if the creature matches a
  known NPC, note the connection in Phase 1 but do not modify the registry.
- **[SLOP CHECK]** — flag anything you invented that wasn't in the input
  or directly implied by it. Especially flag: specific damage types, unusual
  senses, languages, and any named abilities you created wholesale.
- **Never silently rebalance.** If the input's numbers don't fit the target CR,
  say what you changed and why in DECISIONS MADE.
- When the source is /magic-bug-generator, preserve the flavor and specific
  mechanical language from the generator output. Do not genericize it.
