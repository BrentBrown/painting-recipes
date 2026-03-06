# Painting Recipes

A miniature painting recipe library maintained in Obsidian. This project contains tools and templates for converting painting tutorials from various sources into structured, printable recipes.

## Overview

The system takes source material (video transcripts, articles, voice memos, or notes) about miniature painting techniques and generates:
- A markdown recipe file for Obsidian
- A print-ready DOCX file formatted for double-sided printing

## Features

- **Multi-brand paint equivalents**: Converts paints between Two Thin Coats (TTC), Citadel, and Army Painter
- **Automated verification**: Validates paint names against reference tables
- **Standardized format**: Consistent recipe structure with tags, steps, and variations
- **Print-ready output**: US Letter DOCX with green color scheme

## Usage

The `transcript-to-recipe` skill is invoked when source material is provided. It automatically:
1. Extracts painting techniques from the source
2. Looks up paint equivalents using the reference tables
3. Generates markdown and DOCX outputs

## Paint Reference

The project includes comprehensive reference tables for converting between:
- Two Thin Coats (Waves 1-3)
- Citadel
- Army Painter
- Vallejo Game Color
- Vallejo Model Color
- Scale 75
- Reaper Master Series
- Privateer Press P3

## License

MIT
