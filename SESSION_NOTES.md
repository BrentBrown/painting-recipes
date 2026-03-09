# Session Notes

## Session 2

### Discoveries

- Existing recipes use **mixed table formats** (4-, 5-, and 6-column). The 6-column format has a Brand column; older formats do not.
- Some older recipes use parenthetical hints like `Black Templar (contrast)` — the `(contrast)` suffix needs to be stripped before lookup and the brand inferred as "Citadel Contrast".
- Citadel Contrast paints are stored in `paints.json` under `"Citadel Contrast"` with a `speedpaint` field; Speedpaints are stored under `"Army Painter Speedpaint"` with a `citadel_contrast` field. These two brands map only to each other.
- Warpaints Fanatic entries have an `army_painter` field pointing to the **original Warpaints (classic line)** equivalent — distinct from Speedpaint.
- When scanning result rows to classify the WF column header, separator rows (e.g. `|---|---|`) must be skipped to avoid false positives.
- `convert_all_recipes.py` was a separate batch script; its functionality has been merged into `fill_equivalents.py`.

### Accomplished

1. Added `Citadel Contrast` (47 paints) and `Army Painter Speedpaint` (43 paints) brand blocks to `paints.json`, sourced from `contrast_to_speedpaint_conversion_chart.csv`.
2. Cleaned `contrast_to_speedpaint_conversion_chart.csv`: snake_case headers, replaced "No Match" with "No equivalent", removed comments.
3. Updated `fill_equivalents.py` to:
   - Look up Citadel Contrast when brand is "Citadel" and the paint matches a Contrast entry.
   - Infer brand from `(contrast)` suffix in brandless tables.
   - Strip parenthetical suffixes before lookup.
   - Support 4-, 5-, and 6-column table formats.
   - Dynamically set the WF column header based on column contents.
   - Annotate paint names with **(F)** / **(SP)** when both Fanatic and Speedpaint entries appear in the same column.
   - Skip separator rows during header classification.
4. Merged batch-mode functionality from `convert_all_recipes.py` into `fill_equivalents.py`; deleted `convert_all_recipes.py`.
5. Ran `fill_equivalents.py --force` on all 138 recipes successfully (0 errors).

---

## Session 1

### Discoveries

- The original `skill.md` was 748 lines, ~500 of which were paint reference tables loaded into LLM context on every invocation — expensive and prone to hallucination. These were moved to a deterministic Python script.
- LLMs correct garbled paint names from transcripts (e.g. "Norn Oil" → "Nuln Oil") via training knowledge, not from the reference tables. Removing the tables does not affect this capability.
- A `Brand` column was added to the Paint Equivalents table (per-row, not a header field) to future-proof against paint name collisions across brands, since some brands use generic names like "pale yellow".
- Suffix stripping (Gloss, Contrast, Shade, Wash, Matte, etc.) before exact matching handles the majority of real-world paint name variations without fuzzy matching risk.
- The Warpaints Fanatic conversion chart (`warpaints_fanatic_conversion.md`) had some entries where AP paint names appeared in the Citadel column (e.g. "Ice Storm", "Voidshield Blue", "Shining Silver") — these are chart errors and correctly resolve to `"No equivalent"`.
- 49 Warpaints Fanatic paints genuinely have no TTC equivalent (Contrast paints, technical paints, newer Citadel releases). The `"No equivalent"` result for these is correct.
- A two-pass reverse lookup (direct Citadel table, then cross-brand reverse scan) was needed to resolve 7 additional Fanatic entries whose Citadel equivalents were values in other brand tables but not keys in the Citadel table.

### Accomplished

1. Added YAML frontmatter to `skill.md` with triggers for when the skill should be invoked.
2. Created `README.md` with project overview.
3. **Major refactor** — moved all paint reference tables out of `skill.md` into `scripts/paints.json` (462 paints across 7 brands), reducing `skill.md` from 748 lines to 113 lines (~85% smaller).
4. Created `scripts/fill_equivalents.py` — the lookup + DOCX generation script:
   - Parses the `## Paint Equivalents` table in a recipe `.md` file
   - Looks up by `Brand` + `Source Paint` in `paints.json`
   - Strips suffixes before matching
   - Writes TTC (with wave), Citadel, Army Painter back to the MD in-place
   - Idempotent — skips populated rows unless `--force`
   - Generates print-ready DOCX (US Letter, green scheme, Arial, 0.4" margins) to `../Printables/<stem>.docx`
   - Solid error handling with per-row warnings and hard exits on missing files
5. Updated `skill.md` to remove the MANDATORY VERIFICATION STEP, all reference tables, DOCX generation instructions, and updated the template to include the `Brand` column.
6. Created `.gitignore` (root and `.opencode/`).
7. Published to GitHub: `https://github.com/BrentBrown/painting-recipes` (private).
8. Added **Warpaints Fanatic** brand support:
   - Created `scripts/migrate_fanatic.py` — parses `warpaints_fanatic_conversion.md`, derives TTC via two-pass reverse lookup (direct Citadel table + cross-brand reverse scan), merges `"Warpaints Fanatic"` block into `paints.json`.
   - Result: 205 Fanatic paints, 84 TTC resolved, 121 correctly `"No equivalent"`.
   - Moved `warpaints_fanatic_conversion.md` to `scripts/docs/` for future reference.
   - Added `Warpaints Fanatic` to the canonical brand list in `skill.md`.
