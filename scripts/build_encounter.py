#!/usr/bin/env python3
"""Build an interactive HTML encounter worksheet from a JSON spec.

Loads the static template at scripts/encounter_template.html (which contains
the entire <style> and <script> blocks from the design handoff verbatim) and
substitutes three values: <title>, the <h1 id="encounter-name"> content, and
the inline ENCOUNTER JSON literal.

Usage:
    python3 scripts/build_encounter.py spec.json
    python3 scripts/build_encounter.py - < spec.json
    python3 scripts/build_encounter.py '{"name": "...", ...}'

Spec shape: see design_handoff_encounter_worksheet/README.md and
design_handoff_encounter_worksheet/reference/original-slash-command.md.

Output: encounters/<slug>.html (path printed to stdout)
"""

import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR / "encounter_template.html"


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
        .replace("'", "&#39;")
    )


def build_html(spec):
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    name = spec.get("name", "Encounter")

    # Embed JSON as a JS literal. Escape `</` so a string value containing
    # `</script>` can't break out of the surrounding <script> tag, and escape
    # U+2028/U+2029 which are valid JSON but were illegal as raw chars in JS
    # string literals before ES2019.
    data_json = (
        json.dumps(spec, ensure_ascii=False)
        .replace("</", "<\\/")
        .replace(" ", "\\u2028")
        .replace(" ", "\\u2029")
    )

    return (
        template
        .replace("__ENCOUNTER_NAME__", html_escape(name))
        .replace("__ENCOUNTER_JSON__", data_json)
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
    out_dir = SCRIPT_DIR.parent / "encounters"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / (slug + ".html")
    out_path.write_text(build_html(spec), encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
