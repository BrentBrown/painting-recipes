#!/usr/bin/env python3
"""
migrate_fanatic.py

One-time migration script to parse warpaints_fanatic_conversion.md and merge
a "Warpaints Fanatic" brand block into paints.json.

For each Fanatic paint:
  - citadel      = Citadel (GW) column (first value if compound, e.g. "A / B")
  - army_painter = Original Warpaints (WP) column
  - ttc + wave   = derived by looking up the Citadel value in paints.json["Citadel"]
                   Tries each compound option in order until one matches.
  "—" entries become "No equivalent".

Safe to re-run: overwrites only the "Warpaints Fanatic" key in paints.json.

Usage:
    python migrate_fanatic.py
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PAINTS_JSON = SCRIPT_DIR / 'paints.json'
SOURCE_MD   = SCRIPT_DIR / 'warpaints_fanatic_conversion.md'

NO_EQ = "No equivalent"


def load_paints() -> dict:
    if not PAINTS_JSON.exists():
        print(f"Error: {PAINTS_JSON} not found", file=sys.stderr)
        sys.exit(1)
    with open(PAINTS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_table_row(line: str) -> list | None:
    """Return stripped cells for a markdown table row, or None."""
    s = line.strip()
    if not s.startswith('|'):
        return None
    cells = [c.strip() for c in s.split('|')]
    if cells and cells[0] == '':
        cells = cells[1:]
    if cells and cells[-1] == '':
        cells = cells[:-1]
    return cells


def is_separator(cells: list) -> bool:
    return bool(cells) and all(re.match(r'^:?-+:?$', c) for c in cells)


def normalise(val: str) -> str:
    """Convert '—' or empty to 'No equivalent', else strip whitespace."""
    v = val.strip()
    return NO_EQ if v in ('—', '', '-') else v


def first_option(val: str) -> list[str]:
    """Split a compound cell like 'Hoeth Blue / Lothern Blue' into candidates."""
    if val == NO_EQ:
        return []
    return [v.strip() for v in val.split('/') if v.strip()]


def parse_fanatic_md(path: Path) -> list[dict]:
    """Parse all table rows from the conversion markdown."""
    rows = []
    in_table = False
    header_seen = False

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            cells = parse_table_row(line)
            if cells is None:
                in_table = False
                header_seen = False
                continue
            if is_separator(cells):
                continue
            # Header row
            if not header_seen:
                if len(cells) >= 3 and 'warpaints' in cells[0].lower():
                    in_table = True
                    header_seen = True
                continue
            if not in_table or len(cells) < 3:
                continue

            fanatic_name   = normalise(cells[0])
            wp_name        = normalise(cells[1])
            citadel_name   = normalise(cells[2])

            if fanatic_name == NO_EQ:
                continue

            rows.append({
                'fanatic':   fanatic_name,
                'wp':        wp_name,
                'citadel':   citadel_name,
            })

    return rows


def build_fanatic_block(rows: list[dict], citadel_table: dict) -> dict:
    """
    Build the "Warpaints Fanatic" JSON block.
    TTC + wave derived from the Citadel table; tries each compound option in order.
    """
    block = {}
    unmatched = []

    for row in rows:
        fanatic   = row['fanatic']
        wp        = row['wp']        # → army_painter
        citadel   = row['citadel']   # → citadel col

        # Derive TTC by looking up Citadel candidates
        ttc, wave = NO_EQ, None
        citadel_resolved = citadel  # what we'll store

        if citadel != NO_EQ:
            candidates = first_option(citadel)
            for candidate in candidates:
                entry = citadel_table.get(candidate)
                if entry:
                    ttc  = entry.get('ttc', NO_EQ) or NO_EQ
                    wave = entry.get('wave') if ttc != NO_EQ else None
                    citadel_resolved = candidate  # store the matched name
                    break
            else:
                unmatched.append(f"  {fanatic!r} → Citadel candidates {candidates} not in table")

        block[fanatic] = {
            'ttc':          ttc,
            'wave':         wave,
            'citadel':      citadel_resolved,
            'army_painter': wp,
        }

    if unmatched:
        print(f"\n{len(unmatched)} Citadel name(s) not found in paints.json — TTC set to '{NO_EQ}':")
        for m in unmatched:
            print(m)

    return block


def main():
    if not SOURCE_MD.exists():
        print(f"Error: {SOURCE_MD} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {PAINTS_JSON} ...")
    paints = load_paints()
    citadel_table = paints.get('Citadel', {})
    print(f"  Citadel table: {len(citadel_table)} entries")

    print(f"Parsing {SOURCE_MD} ...")
    rows = parse_fanatic_md(SOURCE_MD)
    print(f"  Parsed {len(rows)} Warpaints Fanatic paints")

    print("Building Warpaints Fanatic block ...")
    fanatic_block = build_fanatic_block(rows, citadel_table)

    ttc_found    = sum(1 for v in fanatic_block.values() if v['ttc'] != NO_EQ)
    ttc_missing  = sum(1 for v in fanatic_block.values() if v['ttc'] == NO_EQ)
    print(f"  TTC resolved: {ttc_found}, unresolved: {ttc_missing}")

    # Merge into paints.json
    paints['Warpaints Fanatic'] = fanatic_block

    with open(PAINTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(paints, f, indent=2, ensure_ascii=False)

    print(f"\nDone. 'Warpaints Fanatic' ({len(fanatic_block)} paints) written to {PAINTS_JSON}")


if __name__ == '__main__':
    main()
