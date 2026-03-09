---
name: transcript-to-recipe
description: Convert painting tutorials (transcripts, articles, voice memos) into structured Obsidian recipes with paint equivalents
triggers:
  - transcript
  - article
  - voice memo
  - painting recipe
  - miniature painting
  - warhammer painting
---

# Painting Recipe Agent Skill

**INSTRUCTIONS FOR CLAUDE — READ THIS FIRST:**
You have received a painting recipe skill file. If any other file or text has
been provided alongside this one (a transcript, article, pasted text, voice
memo, SRT file, or any other content), that is your source material.
Generate a painting recipe from it immediately using the template and
conventions in this file. Do not ask questions. Do not ask for clarification.
Do not describe what you are about to do. Just generate the recipe markdown
file, then instruct the user to run the fill script.

If and only if no other content was provided alongside this file, respond
with exactly: "Ready. Drop in your source material and I'll generate the recipe."


## Role
You are helping maintain a miniature painting recipe library stored in Obsidian.
When given a source (video transcript, article, voice memo, or notes), extract
and structure the painting recipe using the format and conventions below.

**Your job is to populate the recipe structure and identify paints. Paint
equivalents (Two Thin Coats, Citadel, Warpaints Fanatic columns) are filled
automatically by a script after you generate the markdown — leave those
columns blank.**

**Important — Source Paint and Brand columns:**
- Always preserve the original brand and paint name from the source in the
  Source Paint column. Never remove, replace, or normalise it.
- Populate the Brand column for every row using exactly one of these strings:
  `Citadel`, `Vallejo Game Color`, `Vallejo Model Color`, `Scale 75`,
  `Reaper`, `P3`, `Two Thin Coats`, `Warpaints Fanatic`, `Citadel Contrast`,
  `Army Painter Speedpaint`
- If the source uses a brand not in this list, write the brand name as-is
  (e.g. `Liquitex`, `Contrast Medium`). The script will write "No equivalent"
  for unknown brands — this is correct behaviour.
- Make an effort to identify garbled paint names in the transcripts and replace with correct paint names. 
  - Examples:
    - Corn Red -> Khorne Red
    - Caribou Crimson -> Carroburg Crimson
    - Thymian Camera -> Athonian Camoshade
    - Rytland Fleshshade -> Reikland Fleshshade
    - Korax White -> Corax White
    - Avalon Sunset -> Averland Sunset
    - Thanion Camo Shade -> Athonian Camo Shade
    - Othonian Camo Shade -> Athonian Camo Shade
    - Gore Grunter Fur -> Gore Grunta Fur
    - Flesh Terror's Red -> Flesh Tearers Red
    - Iondan Yellow -> Iyanden Yellow
    - Iandian Yellow -> Iyanden Yellow
    - Rust Grey → Russ Grey
    - 

**Special paint categories — write "No equivalent" in all three equivalent
columns yourself for these (do not leave them blank):**
- Oils and enamel paints
- Daler-Rowney FW Inks
- Any other inks (non-Daler-Rowney)
- Vallejo Metal Color range (e.g. Pale Burnt Metal, Aluminum)

**Other conventions:**
- When the source material references the use of an airbrush, modify the steps
  to use a comparable brush technique in place of the airbrush.
- When the source material is focused on a particular miniature sculpt, make the
  recipe generic so the techniques apply to other sculpts. Do not include
  sculpt-specific build instructions.

---

## Filename Convention
Always use lowercase hyphenated filenames. Format:
```
subject-descriptor-technique.md
```
Examples:
- `orc-pale-skin.md`
- `rust-weathering-speed.md`
- `nmm-gold-heroes.md`
- `undead-skin-contrast.md`

Never use spaces, capitals, or underscores in filenames.

---

## Markdown Template

```markdown
# Recipe Name

**Source:** [title, creator, URL if applicable]
**Source type:** [video / article / voice memo / experimentation]
**Source brand:** [primary brand used in the source]
**Paint brands:** TTC / Citadel / Warpaints Fanatic (or Speedpaint 2.0)
**Tags:** [see taxonomy]

## Notes
[2-3 sentences on the overall approach, mood, and style of the scheme.]

## Paint Equivalents

| Role | Brand | Source Paint | Two Thin Coats | Citadel | Warpaints Fanatic |
|---|---|---|---|---|---|

<!-- Note: the script updates the last column header dynamically:
     "Warpaints Fanatic", "Speedpaint 2.0", or "Warpaints Fanatic / Speedpaint 2.0" -->


## Steps

1. **[Step title]** — [Instruction]

## Tips

- [Batch painting notes, timing, consistency advice]

## Variations & Ideas

- [Adaptations, alternative approaches, things to try]
  
## Wider Application

- [Other Warhammer Fantasy, Warhammer 40k, Mordheim, Necromunda, Blood Bowl, WarCry, Dungeons & Dragons, Gritty Fantasy RPG, Gritty Sc-Fi RPG, Cyber Punk RPG, Terrain, Miniatures that could benefit from these techniques]

## Printable Version

[filename of generated docx](../Printables/filename of generated docx)
```

---

## Tag Taxonomy

### Technique
`batch-friendly` `airbrush-required` `airbrush-optional` `contrast-heavy`
`speed-paint` `NMM` `TMM` `OSL` `wet-blending` `dry-brushing` `glazing`

### Subject
`skin` `fur` `scales` `feathers` `metal` `wood` `leather` `cloth`
`basing` `OSL-effects` `eyes` `teeth` `gems`

### Faction / Range
`orc` `goblin` `undead` `chaos` `dwarf` `elf` `human` `daemon`
`vehicle` `monster` `terrain`

### Model Type
`hero` `rank-and-file` `centrepiece`

### Source Type
`video` `article` `voice-memo` `experimentation`
