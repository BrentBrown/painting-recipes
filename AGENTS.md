# Agent Instructions

## Goal

Maintain and extend a miniature painting recipe library stored in Obsidian. The core workflow converts painting tutorials (video transcripts, articles, voice memos) into structured markdown recipe files with cross-brand paint equivalents, plus a printable DOCX.

---

## Instructions

- The skill runs inside **opencode**. The skill file `skill.md` is loaded into context when working on recipes.
- Paint lookups must be **deterministic** — the LLM identifies and normalises paint names, a Python script does all table lookups. The LLM never invents TTC paint names.
- Brand names in the recipe `Brand` column must use **exact canonical strings** so the script can look them up in `paints.json`.
- For **Warpaints Fanatic** source recipes, the `Army Painter` column shows the **Original Warpaints (classic line) equivalent**, not the Fanatic paint itself.
- **Citadel Contrast** and **Army Painter Speedpaint 2.0** map only to each other — never to TTC, Citadel base/layer, or Warpaints Fanatic.
- The WF column header is dynamic: "Warpaints Fanatic" (only WF), "Speedpaint 2.0" (only SP), or "Warpaints Fanatic / Speedpaint 2.0" (both). Append **(F)** / **(SP)** suffixes only when both types appear in the same column.
- Special categories (oils, enamels, Daler-Rowney FW Inks, other inks, Vallejo Metal Color) must have `"No equivalent"` written by the LLM directly — not left blank.
- Airbrush steps must be converted to brush technique equivalents.
- Recipes must be generic (not sculpt-specific).
- Filenames: lowercase hyphenated, e.g. `orc-pale-skin.md`.

---

## Relevant Files / Directories

```
painting-recipes/
├── AGENTS.md                           # this file — agent instructions
├── SESSION_NOTES.md                    # human-facing project history
├── README.md
└── .opencode/
    └── skills/
        └── transcript-to-recipe/
            ├── skill.md                # LLM skill prompt
            └── scripts/
                ├── paints.json         # paints across 10 brands (incl. Citadel Contrast + Speedpaint 2.0)
                ├── fill_equivalents.py # fills MD table + generates DOCX (single-file and batch modes)
                ├── migrate_fanatic.py  # one-time migration script (keep for reference)
                └── docs/
                    ├── warpaints_fanatic_conversion.md
                    └── contrast_to_speedpaint_conversion_chart.csv
```

---

## Key Script Invocations

```bash
# Fill equivalents and generate DOCX for a recipe
python scripts/fill_equivalents.py path/to/recipe.md
python scripts/fill_equivalents.py path/to/recipe.md --force

# Re-run Fanatic migration (e.g. after adding new paints to the conversion doc)
python scripts/migrate_fanatic.py
```

---

## Canonical Brand Strings

Must match exactly in the recipe `Brand` column:

`Citadel`, `Vallejo Game Color`, `Vallejo Model Color`, `Scale 75`, `Reaper`, `P3`, `Two Thin Coats`, `Warpaints Fanatic`, `Citadel Contrast`, `Army Painter Speedpaint`
