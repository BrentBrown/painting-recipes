# Session Notes

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
