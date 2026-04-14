#!/usr/bin/env python3
"""Roll initiative and HP for encounter NPCs.

Usage:
    python3 scripts/roll_dice.py '{"npcs": [...]}'

Input JSON — npcs array, each entry:
    name      — creature name (required)
    hp_dice   — dice expression "2d8+4" or flat number "32" (required)
    dex_mod   — DEX modifier for initiative (default 0)
    count     — number of this creature type (default 1)
    groups    — number of initiative groups (default: same as count,
                i.e. individual rolls). All members of a group share
                one initiative roll.

Examples:
    Individual rolls (default):
        {"name": "Ant", "hp_dice": "2d8+2", "dex_mod": 1, "count": 4}
        → Ant 1 (init 14), Ant 2 (init 8), Ant 3 (init 19), Ant 4 (init 11)

    Grouped initiative:
        {"name": "Ant", "hp_dice": "2d8+2", "dex_mod": 1, "count": 12, "groups": 2}
        → Ant 1-6 [A] (init 15), Ant 7-12 [B] (init 9)

    Single group (all share one roll):
        {"name": "Ant", "hp_dice": "2d8+2", "dex_mod": 1, "count": 6, "groups": 1}
        → Ant 1-6 [A] (init 12)

Output JSON:
    npcs[] — one entry per individual:
        name             — display name with group tag if grouped
        hp_rolled        — rolled or flat HP
        initiative_rolled — rolled initiative (shared within group)
        group            — group label if grouped, null otherwise
"""

import json
import math
import random
import re
import sys


def roll_dice_expr(expr):
    """Parse and roll a dice expression like '2d8+4', '3d6-1', or '32'."""
    expr = str(expr).strip()
    if re.match(r"^-?\d+$", expr):
        return max(1, int(expr))
    match = re.match(r"^(\d+)d(\d+)([+-]\d+)?$", expr, re.IGNORECASE)
    if not match:
        raise ValueError(f"Cannot parse dice expression: {expr}")
    num = int(match.group(1))
    sides = int(match.group(2))
    bonus = int(match.group(3)) if match.group(3) else 0
    return max(1, sum(random.randint(1, sides) for _ in range(num)) + bonus)


def group_label(index):
    """Convert 0-based index to letter label: 0→A, 1→B, ..., 25→Z."""
    return chr(ord("A") + index)


def main():
    data = json.loads(sys.argv[1])
    results = []

    for npc in data["npcs"]:
        name = npc["name"]
        hp_dice = npc.get("hp_dice", "1")
        dex_mod = npc.get("dex_mod", 0)
        count = npc.get("count", 1)
        groups = npc.get("groups", None)

        # No grouping: each creature gets its own initiative roll
        if groups is None or groups >= count:
            for i in range(count):
                label = f"{name} {i + 1}" if count > 1 else name
                results.append({
                    "name": label,
                    "hp_rolled": roll_dice_expr(hp_dice),
                    "initiative_rolled": random.randint(1, 20) + dex_mod,
                    "group": None,
                })
        else:
            # Grouped: split count into N groups, each sharing one init roll
            base_size = count // groups
            remainder = count % groups
            creature_num = 1

            for g in range(groups):
                size = base_size + (1 if g < remainder else 0)
                shared_init = random.randint(1, 20) + dex_mod
                tag = group_label(g)

                for _ in range(size):
                    label = (
                        f"{name} {creature_num} [{tag}]"
                        if count > 1
                        else f"{name} [{tag}]"
                    )
                    results.append({
                        "name": label,
                        "hp_rolled": roll_dice_expr(hp_dice),
                        "initiative_rolled": shared_init,
                        "group": tag,
                    })
                    creature_num += 1

    print(json.dumps({"npcs": results}, indent=2))


if __name__ == "__main__":
    main()
