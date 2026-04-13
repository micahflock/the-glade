# /import-character

# Import a handwritten D&D 5e character sheet from photos into a YAML file.

# One character at a time. Paste photos into chat alongside this command.

## Phase 1 — Extract and Flag (stop after this and wait for confirmation)

Read every visible field across all provided photos. Produce this report:

-----

EXTRACTION REPORT — [Character Name]

CONFIRMED READS:
[every field read with confidence, listed as field: value]

FLAGGED:

- [field]: read as [value] — [reason: illegible / arithmetic inconsistency /
  conflicts with another field]
  Options: [plausible interpretations if applicable]

BLANK ON SHEET:

- [fields the player left empty]

NOT ON SHEET:

- [standard 5e fields absent entirely]

-----

Stop. Wait for DM to resolve flagged items before writing anything.

## Phase 2 — Write YAML (only after DM confirms all flags)

Write to party/[name_slug].yaml using the structure below.
Preserve exact wording of all features and traits — do not paraphrase.
Mark any remaining unresolved items with [UNCLEAR: description].

-----

# party/[name_slug].yaml

character:
name:
callsign:
player:
species:
class:
subclass:
background:
level:
xp:

core:
proficiency_bonus:
inspiration:
ac:
initiative:
speed:
hp_max:
hp_current:       # Set to hp_max on fresh import
hit_dice:
hit_dice_remaining:

ability_scores:
strength:     { score: , modifier: }
dexterity:    { score: , modifier: }
constitution: { score: , modifier: }
intelligence: { score: , modifier: }
wisdom:       { score: , modifier: }
charisma:     { score: , modifier: }

saving_throws:
strength:     { bonus: , proficient: }
dexterity:    { bonus: , proficient: }
constitution: { bonus: , proficient: }
intelligence: { bonus: , proficient: }
wisdom:       { bonus: , proficient: }
charisma:     { bonus: , proficient: }

skills:
acrobatics:      { bonus: , proficient: , ability: dexterity }
animal_handling: { bonus: , proficient: , ability: wisdom }
arcana:          { bonus: , proficient: , ability: intelligence }
athletics:       { bonus: , proficient: , ability: strength }
deception:       { bonus: , proficient: , ability: charisma }
history:         { bonus: , proficient: , ability: intelligence }
insight:         { bonus: , proficient: , ability: wisdom }
intimidation:    { bonus: , proficient: , ability: charisma }
investigation:   { bonus: , proficient: , ability: intelligence }
medicine:        { bonus: , proficient: , ability: wisdom }
nature:          { bonus: , proficient: , ability: intelligence }
perception:      { bonus: , proficient: , ability: wisdom }
performance:     { bonus: , proficient: , ability: charisma }
persuasion:      { bonus: , proficient: , ability: charisma }
religion:        { bonus: , proficient: , ability: intelligence }
sleight_of_hand: { bonus: , proficient: , ability: dexterity }
stealth:         { bonus: , proficient: , ability: dexterity }
survival:        { bonus: , proficient: , ability: wisdom }

passive_perception:

attacks:

- name:
  attack_bonus:
  damage:
  damage_type:
  range:         # omit if melee only
  notes:

spell_slots:       # null if no spellcasting
1st: { max: , current: }
2nd: { max: , current: }

proficiencies:
armor: []
weapons: []
tools: []
languages: []

equipment: []

features_and_traits:

- name:
  source:        # e.g. Ranger 1, Outlander background, Level feat
  description: >
  [exact text as written on sheet]

## notes: []          # anything on the sheet that doesn't fit a standard field

## Key Rules

- Never silently resolve an inconsistency — always flag in Phase 1
- Arithmetic errors: record the corrected value, note the sheet value in a comment
- hp_current always equals hp_max on a fresh import
- null for fields that are genuinely absent; do not omit the field entirely
- Blank spell_slots: null if class has no spellcasting at this level
