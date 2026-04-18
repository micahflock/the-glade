# /magic-bug-generator

# Generate magic-enhanced bug creatures for The Glade campaign.
# Searches for real invertebrates and enhances their natural abilities
# with the Bloom's Magic Gradient. Output stays in conversation —
# use /stat-block to convert a creature into a YAML stat block.

## Step 1 — Read Campaign Context

Before generating, read these files for tone, balance, and current state:
- memory/Homebrew_Rules.md — base rules, leveling, LP = HP
- memory/campaign_state.yaml — where the party is, what session we're in
- sessions/session_log.md — what's coming up, recent events

Also check creatures/*.yaml for existing stat blocks to avoid duplicating
concepts and to calibrate power level.

## Step 2 — Search for Real Invertebrates

Use web search to find real-world invertebrates that fit the request.
Search for things like:
- "[environment] insects" or "[environment] invertebrates"
- "ambush predator insects" or "venomous arthropods" or "bioluminescent bugs"
- "[behavior] invertebrates" (e.g., "parasitic", "colonial", "aquatic")
- "[specific taxon] species" when narrowing down a family

Cast a wide net. Use the broad American definition of "bugs" — insects,
arachnids, crustaceans, myriapods, mollusks, worms, etc. Favor creatures
with distinctive real biology that translates well to magic enhancement.
Aim for variety: don't return 4 beetles or 4 spiders unless specifically asked.

## Step 3 — Search for Reference Images

Use web search to find reference images for each creature. Search by
scientific name or common name + "macro photo" for best results.
Present image URLs alongside each creature entry so the DM can view them.

## Step 4 — Present Options

Present at least 4 options (unless the user asks for fewer). For each:

-----

### [Emoji] [Common Name(s)]
*[Scientific name] ([Family])*

**Archetype:** [D&D-style role — Ambusher, Brute, Controller, Artillery,
Skirmisher, Sentinel, Support, Boss, Minion, etc.]

**Reference:** [image URL if found]

**Notable Features & Behaviors:**
- [2-4 bullet points about the REAL creature's biology — what makes it
  interesting, how it hunts/defends/lives. This is what the magic enhances.]

**Magic Gradient Effects:**

**Winter** (party level ~3, baseline enhancement):
- Enhancement: [Subtle amplification of natural ability — flavor text]
- Mechanic: [Minor trait or small bonus, e.g. +2 to a check, advantage
  in a narrow situation]

**Spring** (party level ~6, DC 11-13, 1d6-2d6):
- Enhancement: [Noticeable power — flavor text]
- Mechanic: [A proper ability with DC, damage dice, and/or condition]

**Summer** (party level ~9, DC 13-15, 2d6-4d6):
- Enhancement: [Dramatic, spell-like — flavor text]
- Mechanic: [Strong action or spell-like ability with full 5e formatting]

**Fall** (party level ~12, DC 16-18, 4d6-8d6):
- Enhancement: [Extreme, rivals high-level magic — flavor text]
- Mechanic: [Powerful ability — legendary action tier, multi-target,
  high damage, or devastating condition]

-----

If the user specifies a zone or level range, show only the relevant tier(s).
If the user specifies an archetype, use it. Otherwise, infer the best fit
from the creature's real biology.


## Step 5 — Campaign Connections

After presenting all options, briefly note how any of these creatures could
connect to:
- Upcoming sessions or the party's current location
- Existing campaign threads (ant alliance, cordyceps, the Bloom)
- Open questions from memory/Open_Questions.md
- Existing NPCs or factions

Offer to append any of the generated bugs to creatures/magical-bugs.md

## Key Rules

- The magic enhancement always grows FROM the creature's real biology.
  A spider's silk becomes magical binding. A mantis's ambush instinct
  becomes near-invisibility. A dung beetle's strength becomes supernatural.
  Never assign random magical abilities unrelated to the real animal.
- Mechanics should be simple, balanced homebrew — damage dice, DCs, saving
  throws, conditions. Use 5e 2024 conventions.
- Scale DCs and damage to the zone using the party level benchmarks from
  Homebrew_Rules.md (level 3 in winter, +3 per zone crossing).
- Do not generate full stat blocks — that's what /stat-block is for. Focus
  on the concept, the biology, the archetype, and the signature mechanics
  at each gradient tier.
- Preserve real taxonomic names. The scientific grounding is part of the
  campaign's identity.
- When the user's request maps to an existing NPC in NPC_Registry.yaml
  (e.g., "give me a shieldbug guard" when shield bugs already exist in the
  registry), note the connection.
