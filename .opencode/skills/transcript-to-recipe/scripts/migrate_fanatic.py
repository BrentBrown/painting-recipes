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


def build_reverse_lookup(paints: dict) -> dict:
    """
    Build a comprehensive citadel_name → {ttc, wave} map by scanning all brand
    tables and the TTC table in reverse (via each entry's 'citadel' field).
    """
    reverse = {}

    # Forward scan: any brand table entry that has both citadel + ttc values
    for brand, table in paints.items():
        if brand in ('Warpaints Fanatic', 'Two Thin Coats'):
            continue
        for entry in table.values():
            c = entry.get('citadel', '')
            t = entry.get('ttc', '')
            w = entry.get('wave')
            if c and c != NO_EQ and t and t != NO_EQ and c not in reverse:
                reverse[c] = {'ttc': t, 'wave': w}

    # Reverse scan of the TTC table: TTC name is the ttc value, citadel field is the key
    for ttc_name, entry in paints.get('Two Thin Coats', {}).items():
        c = entry.get('citadel', '')
        if c and c != NO_EQ and c not in reverse:
            reverse[c] = {'ttc': ttc_name, 'wave': entry.get('wave')}

    return reverse


def build_fanatic_block(rows: list[dict], paints: dict) -> dict:
    """
    Build the "Warpaints Fanatic" JSON block.
    TTC + wave derived first from the Citadel table, then via extended reverse
    lookup across all brand tables and the TTC table.
    """
    citadel_table = paints.get('Citadel', {})
    reverse = build_reverse_lookup(paints)

    block = {}
    unmatched = []

    for row in rows:
        fanatic          = row['fanatic']
        wp               = row['wp']        # → army_painter
        citadel          = row['citadel']   # → citadel col

        ttc, wave        = NO_EQ, None
        citadel_resolved = citadel

        if citadel != NO_EQ:
            candidates = first_option(citadel)

            # Pass 1: direct Citadel table lookup
            for candidate in candidates:
                entry = citadel_table.get(candidate)
                if entry:
                    ttc  = entry.get('ttc', NO_EQ) or NO_EQ
                    wave = entry.get('wave') if ttc != NO_EQ else None
                    citadel_resolved = candidate
                    break

            # Pass 2: extended reverse lookup across all tables
            if ttc == NO_EQ:
                for candidate in candidates:
                    hit = reverse.get(candidate)
                    if hit:
                        ttc  = hit['ttc']
                        wave = hit['wave']
                        citadel_resolved = candidate
                        break

            if ttc == NO_EQ:
                unmatched.append(
                    f"  {fanatic!r} → Citadel candidates {candidates} — no TTC equivalent found"
                )

        block[fanatic] = {
            'ttc':          ttc,
            'wave':         wave,
            'citadel':      citadel_resolved,
            'army_painter': wp,
        }

    if unmatched:
        print(f"\n{len(unmatched)} paint(s) with no TTC equivalent (set to '{NO_EQ}'):")
        for m in unmatched:
            print(m)

    return block


def main():
    if not SOURCE_MD.exists():
        print(f"Error: {SOURCE_MD} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {PAINTS_JSON} ...")
    paints = load_paints()
    print(f"  Citadel table: {len(paints.get('Citadel', {}))} entries")

    print(f"Parsing {SOURCE_MD} ...")
    rows = parse_fanatic_md(SOURCE_MD)
    print(f"  Parsed {len(rows)} Warpaints Fanatic paints")

    print("Building Warpaints Fanatic block ...")
    fanatic_block = build_fanatic_block(rows, paints)

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
