#!/usr/bin/env python3
"""
fill_equivalents.py

Fills paint equivalents in a painting recipe markdown file and generates a
print-ready DOCX. Looks up each Source Paint by brand using paints.json,
strips common paint name suffixes before matching, and writes the results
back to the markdown file in-place.

Usage:
    python fill_equivalents.py <recipe.md>
    python fill_equivalents.py <recipe.md> --force
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUFFIX_PATTERN = re.compile(
    r"\s+(Gloss|Contrast|Shade|Wash|Matte|Matt|Layer|Base|Dry|Technical)$",
    re.IGNORECASE,
)

NO_EQ = "No equivalent"

# ---------------------------------------------------------------------------
# Paint name normalisation
# ---------------------------------------------------------------------------


def strip_suffixes(name: str) -> str:
    """Repeatedly strip trailing paint-name suffixes until stable."""
    stripped = name.strip()
    while True:
        new = SUFFIX_PATTERN.sub("", stripped)
        if new == stripped:
            break
        stripped = new
    return stripped


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_paints(script_dir: Path) -> dict:
    paints_path = script_dir / "paints.json"
    if not paints_path.exists():
        print(
            f"Error: paints.json not found at {paints_path}\n"
            f"Expected it alongside this script in: {script_dir}",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        with open(paints_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: paints.json is malformed: {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Lookup logic
# ---------------------------------------------------------------------------


def build_wf_reverse_lookup(paints: dict) -> dict:
    """
    Build a reverse map from Citadel paint name → Warpaints Fanatic paint name.

    Where multiple WF paints share the same Citadel equivalent the names are
    joined with ' / '.  The 'No equivalent' key is ignored.
    """
    wf_table = paints.get("Warpaints Fanatic", {})
    reverse: dict[str, list[str]] = {}
    for wf_name, entry in wf_table.items():
        cit = entry.get("citadel")
        if cit and cit != NO_EQ:
            reverse.setdefault(cit, []).append(wf_name)
    return {cit: " / ".join(names) for cit, names in reverse.items()}


def lookup_equivalents(
    brand: str, source_paint: str, paints: dict, wf_reverse: dict
) -> tuple:
    """
    Return (ttc_col, citadel_col, warpaints_fanatic_col) for a source paint.

    For brand "Two Thin Coats" the TTC column contains the source paint name
    (with wave); for all other brands the TTC column contains the looked-up
    TTC equivalent.

    The Warpaints Fanatic column is resolved via a reverse lookup from the
    Citadel equivalent; for a Warpaints Fanatic source paint the column
    contains the source paint itself.

    For Citadel Contrast and Army Painter Speedpaint, the Warpaints Fanatic
    column shows the cross-brand equivalent (Speedpaint or Citadel Contrast).
    """
    stripped = strip_suffixes(source_paint)

    brand_table = paints.get(brand)
    if brand_table is None:
        print(
            f"  Warning: Unknown brand '{brand}' — writing '{NO_EQ}' for all columns.",
            file=sys.stderr,
        )
        return NO_EQ, NO_EQ, NO_EQ

    # Try stripped name first, then original as fallback
    entry = brand_table.get(stripped) or brand_table.get(source_paint.strip())

    if entry is None:
        return NO_EQ, NO_EQ, NO_EQ

    # --- Special handling for Citadel Contrast ---
    if brand == "Citadel Contrast":
        speedpaint = entry.get("speedpaint", NO_EQ)
        return NO_EQ, NO_EQ, speedpaint

    # --- Special handling for Army Painter Speedpaint ---
    if brand == "Army Painter Speedpaint":
        contrast = entry.get("citadel_contrast", NO_EQ)
        return NO_EQ, NO_EQ, contrast

    # --- TTC column ---
    if brand == "Two Thin Coats":
        wave = entry.get("wave", "")
        ttc_col = f"{stripped} ({wave})" if wave else stripped
    else:
        ttc_name = entry.get("ttc") or NO_EQ
        if ttc_name == NO_EQ:
            ttc_col = NO_EQ
        else:
            wave = entry.get("wave", "")
            ttc_col = f"{ttc_name} ({wave})" if wave else ttc_name

    # --- Citadel column ---
    if brand == "Citadel":
        citadel_col = source_paint.strip()
    else:
        citadel_col = entry.get("citadel") or NO_EQ

    # --- Warpaints Fanatic column ---
    if brand == "Warpaints Fanatic":
        wf_col = source_paint.strip()
    else:
        wf_col = wf_reverse.get(citadel_col, NO_EQ)

    return ttc_col, citadel_col, wf_col


# ---------------------------------------------------------------------------
# Markdown table helpers
# ---------------------------------------------------------------------------


def parse_table_row(line: str) -> list | None:
    """Parse a markdown table row into a list of stripped cell strings."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    cells = [c.strip() for c in stripped.split("|")]
    # Remove empty strings from leading/trailing '|'
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def is_separator_row(cells: list) -> bool:
    """Return True if every cell looks like a markdown separator (----)."""
    return bool(cells) and all(re.match(r"^:?-+:?$", c) for c in cells)


def format_table_row(cells: list) -> str:
    return "| " + " | ".join(cells) + " |\n"


# ---------------------------------------------------------------------------
# Core fill logic
# ---------------------------------------------------------------------------


def fill_equivalents(lines: list, paints: dict, force: bool) -> tuple:
    """
    Process markdown lines, filling blank (or all-"No equivalent") paint
    equivalent cells using paints.json lookups.

    Returns (updated_lines, rows_filled, rows_skipped).
    Idempotent: rows with all three equivalent columns already populated are
    skipped unless --force is given.
    """
    result = []
    in_equiv_section = False
    header_seen = False
    rows_filled = 0
    rows_skipped = 0
    warned_no_table = True  # flipped to False when section heading found
    wf_reverse = build_wf_reverse_lookup(paints)

    for i, line in enumerate(lines):
        # Detect Paint Equivalents section
        if re.match(r"^##\s+Paint Equivalents", line.strip()):
            in_equiv_section = True
            header_seen = False
            warned_no_table = False
            result.append(line)
            continue

        # Leaving the section when another ## heading appears
        if in_equiv_section and re.match(r"^##\s+", line.strip()):
            in_equiv_section = False

        if not in_equiv_section:
            result.append(line)
            continue

        # --- Inside the Paint Equivalents section ---
        cells = parse_table_row(line)

        # Non-table content (blank lines, etc.)
        if cells is None:
            result.append(line)
            continue

        # Separator row — pass through unchanged
        if is_separator_row(cells):
            result.append(line)
            continue

        # Header row: Role | Brand | Source Paint | Two Thin Coats | Citadel | Warpaints Fanatic
        if not header_seen:
            if len(cells) >= 6 and cells[0].lower() == "role":
                header_seen = True
            result.append(line)
            continue

        # Data rows require exactly 6 columns
        if len(cells) != 6:
            print(
                f"  Warning: Line {i + 1} has {len(cells)} column(s) (expected 6), "
                f"skipping: {line.rstrip()}",
                file=sys.stderr,
            )
            result.append(line)
            rows_skipped += 1
            continue

        role, brand, source_paint, ttc_val, citadel_val, wf_val = cells

        # Skip rows with no source paint or brand
        if not source_paint or not brand:
            result.append(line)
            continue

        all_filled = bool(ttc_val and citadel_val and wf_val)

        if all_filled and not force:
            rows_skipped += 1
            result.append(line)
            continue

        ttc_new, citadel_new, wf_new = lookup_equivalents(
            brand, source_paint, paints, wf_reverse
        )
        new_cells = [role, brand, source_paint, ttc_new, citadel_new, wf_new]
        result.append(format_table_row(new_cells))
        rows_filled += 1

    if not warned_no_table:
        pass  # section was found — no warning needed
    else:
        print(
            "  Warning: No '## Paint Equivalents' section found in the markdown file.",
            file=sys.stderr,
        )

    return result, rows_filled, rows_skipped


# ---------------------------------------------------------------------------
# Recipe parser (for DOCX generation)
# ---------------------------------------------------------------------------


def parse_recipe(lines: list) -> dict:
    """Parse recipe markdown into a structured dict for DOCX generation."""
    recipe = {
        "title": "",
        "source": "",
        "source_type": "",
        "paint_brands": "",
        "source_brand": "",
        "tags": "",
        "notes": [],
        "equivalents": [],
        "steps": [],
        "tips": [],
        "variations": [],
        "wider_application": [],
    }

    meta_map = {
        "**Source:**": "source",
        "**Source type:**": "source_type",
        "**Paint brands:**": "paint_brands",
        "**Source brand:**": "source_brand",
        "**Tags:**": "tags",
    }

    current_section = None

    for line in lines:
        s = line.rstrip("\n")

        # Title (# but not ##)
        if re.match(r"^#\s+", s) and not re.match(r"^##\s+", s):
            recipe["title"] = s[2:].strip()
            continue

        # Metadata fields
        matched_meta = False
        for prefix, key in meta_map.items():
            if s.startswith(prefix):
                recipe[key] = s[len(prefix) :].strip()
                matched_meta = True
                break
        if matched_meta:
            continue

        # Section headings
        if re.match(r"^##\s+", s):
            heading = s[3:].strip().lower()
            if "note" in heading:
                current_section = "notes"
            elif "paint equiv" in heading:
                current_section = "equivalents"
            elif "step" in heading:
                current_section = "steps"
            elif "tip" in heading:
                current_section = "tips"
            elif "variation" in heading:
                current_section = "variations"
            elif "wider" in heading or "application" in heading:
                current_section = "wider_application"
            elif "printable" in heading:
                current_section = None
            else:
                current_section = None
            continue

        # Accumulate content per section
        if current_section == "equivalents":
            cells = parse_table_row(s)
            if (
                cells
                and len(cells) >= 6
                and not is_separator_row(cells)
                and cells[0].lower() != "role"
            ):
                recipe["equivalents"].append(
                    {
                        "role": cells[0],
                        "brand": cells[1],
                        "source_paint": cells[2],
                        "ttc": cells[3],
                        "citadel": cells[4],
                        "warpaints_fanatic": cells[5],
                    }
                )
        elif current_section and current_section != "equivalents":
            if s and not s.startswith("|") and not s.startswith("#"):
                recipe[current_section].append(s)

    return recipe


# ---------------------------------------------------------------------------
# DOCX generation
# ---------------------------------------------------------------------------


def generate_docx(recipe: dict, output_path: Path) -> None:
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor

    COLOR_DARK = RGBColor(0x2D, 0x5A, 0x27)
    COLOR_TEXT = RGBColor(0x44, 0x44, 0x44)
    COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    HEX_DARK = "2D5A27"
    HEX_LIGHT = "EAF2E8"

    def set_cell_shading(cell, fill_hex: str):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), fill_hex)
        tcPr.append(shd)

    def add_run(para, text, bold=False, color=None, size_pt=None):
        run = para.add_run(text)
        run.font.name = "Arial"
        run.font.bold = bold
        if color:
            run.font.color.rgb = color
        if size_pt:
            run.font.size = Pt(size_pt)
        return run

    def spacing(para, before=0, after=2):
        para.paragraph_format.space_before = Pt(before)
        para.paragraph_format.space_after = Pt(after)

    doc = Document()

    # Page: US Letter, 0.4" margins
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    for attr in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, attr, Inches(0.4))

    doc.styles["Normal"].font.name = "Arial"  # type: ignore[union-attr]
    doc.styles["Normal"].font.size = Pt(9)  # type: ignore[union-attr]

    # Title
    p = doc.add_paragraph()
    spacing(p, before=0, after=4)
    add_run(
        p, recipe["title"] or "Untitled Recipe", bold=True, color=COLOR_DARK, size_pt=14
    )

    # Metadata line
    meta_parts = []
    if recipe["source"]:
        meta_parts.append(f"Source: {recipe['source']}")
    if recipe["source_type"]:
        meta_parts.append(f"Type: {recipe['source_type']}")
    if recipe["paint_brands"]:
        meta_parts.append(f"Brands: {recipe['paint_brands']}")
    if recipe["tags"]:
        meta_parts.append(f"Tags: {recipe['tags']}")
    if meta_parts:
        p = doc.add_paragraph()
        spacing(p, after=4)
        add_run(p, "  ·  ".join(meta_parts), color=COLOR_TEXT, size_pt=8)

    # Notes
    if recipe["notes"]:
        p = doc.add_paragraph()
        spacing(p, before=4, after=2)
        add_run(p, "Notes", bold=True, color=COLOR_DARK, size_pt=10)
        note_text = " ".join(
            ln.lstrip("- ").strip() for ln in recipe["notes"] if ln.strip()
        )
        p = doc.add_paragraph()
        spacing(p, after=4)
        add_run(p, note_text, color=COLOR_TEXT, size_pt=9)

    # Paint Equivalents table
    if recipe["equivalents"]:
        p = doc.add_paragraph()
        spacing(p, before=4, after=2)
        add_run(p, "Paint Equivalents", bold=True, color=COLOR_DARK, size_pt=10)

        headers = [
            "Role",
            "Source Paint",
            "Two Thin Coats",
            "Citadel",
            "Warpaints Fanatic",
        ]
        col_widths = [Inches(0.9), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.3)]

        table = doc.add_table(rows=1, cols=5)
        table.style = "Table Grid"

        # Header row
        hdr_row = table.rows[0]
        for idx, (hdr, width) in enumerate(zip(headers, col_widths)):
            cell = hdr_row.cells[idx]
            cell.width = width
            set_cell_shading(cell, HEX_DARK)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            add_run(p, hdr, bold=True, color=COLOR_WHITE, size_pt=8)

        # Data rows
        for row_idx, eq in enumerate(recipe["equivalents"]):
            row = table.add_row()
            fill = HEX_LIGHT if row_idx % 2 == 0 else "FFFFFF"
            values = [
                eq["role"],
                eq["source_paint"],
                eq["ttc"],
                eq["citadel"],
                eq["warpaints_fanatic"],
            ]
            for idx, (val, width) in enumerate(zip(values, col_widths)):
                cell = row.cells[idx]
                cell.width = width
                set_cell_shading(cell, fill)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                add_run(p, val, color=COLOR_TEXT, size_pt=8)

    # Steps
    if recipe["steps"]:
        p = doc.add_paragraph()
        spacing(p, before=4, after=2)
        add_run(p, "Steps", bold=True, color=COLOR_DARK, size_pt=10)

        step_num = 0
        for step_line in recipe["steps"]:
            s = step_line.strip()
            if not s:
                continue
            m = re.match(r"^\d+\.\s+\*\*(.+?)\*\*\s*[—\-]\s*(.+)$", s)
            if m:
                step_num += 1
                p = doc.add_paragraph()
                spacing(p, after=2)
                add_run(
                    p,
                    f"{step_num}. {m.group(1)} — ",
                    bold=True,
                    color=COLOR_DARK,
                    size_pt=9,
                )
                add_run(p, m.group(2), color=COLOR_TEXT, size_pt=9)
            else:
                p = doc.add_paragraph()
                spacing(p, after=2)
                add_run(p, s, color=COLOR_TEXT, size_pt=9)

    # Tips
    if recipe["tips"]:
        p = doc.add_paragraph()
        spacing(p, before=4, after=2)
        add_run(p, "Tips", bold=True, color=COLOR_DARK, size_pt=10)
        for tip in recipe["tips"]:
            t = tip.strip().lstrip("- ").strip()
            if t:
                p = doc.add_paragraph()
                spacing(p, after=1)
                add_run(p, f"• {t}", color=COLOR_TEXT, size_pt=9)

    # Variations & Ideas
    if recipe["variations"]:
        p = doc.add_paragraph()
        spacing(p, before=4, after=2)
        add_run(p, "Variations & Ideas", bold=True, color=COLOR_DARK, size_pt=10)
        for v in recipe["variations"]:
            t = v.strip().lstrip("- ").strip()
            if t:
                p = doc.add_paragraph()
                spacing(p, after=1)
                add_run(p, f"• {t}", color=COLOR_TEXT, size_pt=9)

    # Wider Application
    if recipe["wider_application"]:
        p = doc.add_paragraph()
        spacing(p, before=4, after=2)
        add_run(p, "Wider Application", bold=True, color=COLOR_DARK, size_pt=10)
        for w in recipe["wider_application"]:
            t = w.strip().lstrip("- ").strip()
            if t:
                p = doc.add_paragraph()
                spacing(p, after=1)
                add_run(p, f"• {t}", color=COLOR_TEXT, size_pt=9)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f"  DOCX saved: {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fill paint equivalents in a recipe markdown file and generate a DOCX."
        )
    )
    parser.add_argument("recipe", help="Path to the recipe .md file")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-fill all rows, overwriting any existing equivalent values",
    )
    args = parser.parse_args()

    recipe_path = Path(args.recipe)
    if not recipe_path.exists():
        print(f"Error: Recipe file not found: {recipe_path}", file=sys.stderr)
        sys.exit(1)
    if recipe_path.suffix.lower() != ".md":
        print(
            f"Warning: Expected a .md file, got: {recipe_path.suffix}",
            file=sys.stderr,
        )

    script_dir = Path(__file__).parent
    paints = load_paints(script_dir)

    print(f"Processing: {recipe_path}")

    with open(recipe_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines, rows_filled, rows_skipped = fill_equivalents(
        lines, paints, args.force
    )

    # Write the updated markdown back in-place
    with open(recipe_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"  Rows filled: {rows_filled}, rows skipped: {rows_skipped}")

    # Derive DOCX path: sibling Printables/ directory relative to the recipe
    printables_dir = recipe_path.parent.parent / "Printables"
    docx_path = printables_dir / (recipe_path.stem + ".docx")

    print(f"Generating DOCX: {docx_path}")
    try:
        recipe_data = parse_recipe(updated_lines)
        generate_docx(recipe_data, docx_path)
    except ImportError:
        print(
            "Error: python-docx is not installed. Install with: pip install python-docx",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error generating DOCX: {e}", file=sys.stderr)
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
