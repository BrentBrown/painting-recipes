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
reference tables in this file. Do not ask questions. Do not ask for
clarification. Do not describe what you are about to do. Just generate
the recipe and the docx file.

If and only if no other content was provided alongside this file, respond
with exactly: "Ready. Drop in your source material and I'll generate the recipe."


## Role
You are helping maintain a miniature painting recipe library stored in Obsidian.
When given a source (video transcript, article, voice memo, or notes), extract
and structure the painting recipe using the format and conventions below.

**Important — Paint Equivalents:**
- Always preserve the original brand and paint name from the source in the
  Source Paint column. Never remove or replace it.
- Always populate TTC, Citadel, and Army Painter columns by looking up the
  reference tables at the bottom of this file. Use the correct table for the
  source brand:
  - Source is Citadel → use the "Citadel → TTC Quick Reference" table
  - Source is Vallejo → use the "Vallejo Game Color" or "Vallejo Model Color" table
  - Source is Army Painter → use the TTC table, search the Army Painter column
  - Source is TTC → use the TTC table directly
- In the recipe Paint Equivalents table, include the wave number in
  parentheses after the TTC paint name, e.g. "Oblivion Black Wash (W1)".
  Do NOT use a separate Wave column in the recipe table.
- **CRITICAL: Never invent or guess TTC paint names. TTC names are exact
  product names — they must be found in the reference tables below, verbatim.
  Common ones to get right:**
  - Nuln Oil → **Oblivion Black Wash (W1)**
  - Agrax Earthshade → **Battle Mud Wash (W1)**
  - Seraphim Sepia → **Archaic Sepia Wash (W1)**
  - Reikland Fleshshade → **Flesh Wash (W1)**
  - Carroburg Crimson → **Hellion Red Wash (W2)**
  - Drakenhof Nightshade → **Tempest Blue Wash (W2)**
  - Druchii Violet → **Magi Purple Wash (W2)**
  - Athonian Camoshade → **Necrosis Green Wash (W1)**
  - Biel-Tan Green → **Orc Flesh Wash (W1)**
  - **If a paint is not in the tables, write "No equivalent". Never invent
    a plausible-sounding name.**
- Only write "No equivalent" if the paint genuinely does not appear anywhere
  in the reference tables.
- Vallejo Metal Color paints (e.g. Pale Burnt Metal, Aluminum) are a specialist
  metallic range with no direct equivalents — note this clearly.
- Daler-Rowney FW Inks have properties which are difficult to achieve with paints. When these inks are used, do not attempt to find equivalents. Only write "No equivalent"
- When the source material uses other inks than Daler-Rowney do not attempt to 
  look up equivalents. Only write "No equivalent"
- When the source material uses oil and/or enamel paints, do not look up equivalents. Only write "No equivalent"
- When the source material references the use of an airbrush, modify the steps to use 
  comparable brush technique in place of the airbrush.
- When the source material is focused on a particular miniature sculpt, make the recipe
  generic so that the techniques can be applied to a other sculpts. The recipe should
  be widely applicable to a variety of miniature sculpts. Do not include sculpt specific build instructions in the recipe.


---

## MANDATORY VERIFICATION STEP

**Before finalising the Paint Equivalents table, you MUST perform the following
audit on every single row. Do not skip this step. Do not assume your first-pass
lookups were correct — re-check each entry against the tables explicitly.**

For every row in your Paint Equivalents table, work through this checklist:

### Check 1 — No invented TTC names
Locate the exact TTC paint name you wrote in the table reference tables below.
Search the "Two Thin Coats" column (or TTC column) and confirm it appears
verbatim. If you cannot find it, the name is wrong — replace it with the
correct name from the table, or write "No equivalent" if it genuinely
does not appear anywhere.

### Check 2 — No false "No equivalent" entries
If you wrote "No equivalent" in any cell, re-search all relevant tables for
the source paint before accepting it. Specifically:
- For Citadel source paints: search the "Citadel → TTC Quick Reference" table
- For TTC equivalents: search the TTC column of the main TTC table
- For Army Painter equivalents: search the Army Painter column of the main TTC table
Only leave "No equivalent" if the paint is genuinely absent after this re-check.

### Check 3 — Citadel column contains the correct Citadel paint
The Citadel column must contain the correct Citadel equivalent — not a
substitute from another brand. A common failure mode is writing a
Citadel-sounding name that is actually a different brand's paint, or confusing
two paints that serve similar roles (e.g. writing Steel Legion Drab instead of
Zandri Dust). Re-confirm each Citadel entry maps correctly.

### Check 4 — Wave number is present on all TTC entries
Every TTC paint name that has an equivalent must include its wave number in
parentheses, e.g. "Sanguine Scarlet (W1)". If you wrote a TTC name without
a wave number, look it up and add it.

### Check 5 — Special paint categories are excluded from lookup
Confirm that any of the following paint types are listed as "No equivalent"
across all columns and have NOT been looked up:
- Oils and enamels
- Daler-Rowney FW Inks
- Any other inks (non-Daler-Rowney)
- Vallejo Metal Color range

### Verification output format
Before writing the final recipe, produce a silent internal audit block
(you do not need to show this to the user) structured as follows. Work through
every row and confirm pass or fail for each check. If any check fails, correct
the table before proceeding:

  Row: [Source Paint]
  Check 1 (TTC name found verbatim): PASS / FAIL → [corrected value if needed]
  Check 2 (No false No equivalent): PASS / FAIL → [corrected value if needed]
  Check 3 (Citadel column correct): PASS / FAIL → [corrected value if needed]
  Check 4 (Wave number present): PASS / FAIL → [corrected value if needed]
  Check 5 (Special category excluded): PASS / N/A

Only proceed to generate the markdown and docx once all rows pass all checks.

---

## Filename Convention
Always use lowercase hyphenated filenames. Format:
```
subject-descriptor-technique.md
subject-descriptor-technique.docx
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
**Paint brands:** TTC / Citadel / Army Painter
**Tags:** [see taxonomy]

## Notes
[2-3 sentences on the overall approach, mood, and style of the scheme.]

## Paint Equivalents

| Role | Source Paint | Two Thin Coats | Citadel | Army Painter |
|---|---|---|---|---|


## Steps

1. **[Step title]** — [Instruction]

## Tips

- [Batch painting notes, timing, consistency advice]

## Variations & Ideas

- [Adaptations, alternative approaches, things to try]
  
## Wider Application

- [Other Warhammer Fantasy, Warhammer 40k, Mordheim, Necromunda, Blood Bowl, WarCry, Dungeons & Dragons, Gritty Fantasy RPG, Gritty Sc-Fi RPG, Cyber Punk RPG, Terrain, Miniatures that could benfit from these techniques]

## Printable Version

[filename of generated docx](../Printables/filename of generated docx)
```

---

## Docx Format
Generate a print-ready US Letter docx formatted for double-sided printing (2 pages max).
- 0.4" margins
- Green colour scheme (dark: #2D5A27, mid: #4A7C3F, light: #EAF2E8)
- Tables with dark green headers, alternating light green / white rows
- Step headings in dark green, instruction text in #444444
- Font: Arial throughout
- Compact spacing to fit 2 pages

### Preferred Method: python-docx

`python-docx` is pre-installed in this environment. Use it by default for all new documents — do NOT attempt to use the `docx` npm package, as outbound network access is unavailable and it cannot be installed.
```python
from docx import Document
# ... build document ...
doc.save("output.docx")
```

---

---

### Citadel → TTC Quick Reference
*Use this table when the source calls out a Citadel paint. Look up the Citadel
name here to find the correct TTC name — do not guess or invent TTC names.*

| Citadel | Two Thin Coats | Wave | Army Painter |
|---|---|---|---|
| Abaddon Black | Doom Death Black | W1 | Matt Black |
| Administratum Grey | Carcharodon Grey | W1 | Ash Grey |
| Agrax Earthshade | Battle Mud Wash | W1 | Strong Tone |
| Athonian Camoshade | Necrosis Green Wash | W1 | Military Shade |
| Averland Sunset | Dark Sun Yellow | W1 | Basilisk Brown |
| Baharroth Blue | Ray Gun Glow | W2 | Toxic Mist |
| Balthazar Gold | Spartan Bronze | W1 | True Copper |
| Baneblade Brown | Wasteland Brown | W1 | Monster Brown |
| Barak-Nar Burgundy | Royal Cloak | W1 | Crusted Sore |
| Biel-Tan Green | Orc Flesh Wash | W1 | Green Tone |
| Blue Horror | Celestial Blue | W1 | Electric Blue |
| Bugman's Glow | Barbarian Brawn | W1 | Tanned Flesh |
| Caledor Sky | Witching Hour Blue | W2 | Viking Blue |
| Calgar Blue | Elysium Blue | W1 | Ultramarine Blue |
| Caliban Green | Wyvern Green | W1 | Angel Green |
| Carroburg Crimson | Hellion Red Wash | W2 | Red Tone |
| Castellan Green | Fury Green | W2 | Elf Green |
| Catachan Flesh | Druid Flesh | W2 | Onyx Skin |
| Corvus Black | Death Reaper | W1 | Necromancer Cloak |
| Corax White | Trooper White | W1 | Spaceship Exterior |
| Cadian Fleshtone | Dwarven Skin | W1 | Tanned Skin |
| Daemonette Hide | Incubus Purple | W3 | Hexed Violet |
| Dark Reaper | Faust Blue | W3 | Night Sky |
| Dawnstone | Wizard Grey | W1 | Uniform Grey |
| Deathclaw Brown | Satyr Brown | W2 | Troll Claws |
| Drakenhof Nightshade | Tempest Blue Wash | W2 | Blue Tone |
| Druchii Violet | Magi Purple Wash | W2 | Purple Tone |
| Dryad Bark | Scorched Earth | W1 | Oak Brown |
| Emperor's Children | Hot Pink | W2 | Pixie Pink |
| Eshin Grey | Ashen Grey | W2 | Necromancer Cloak |
| Evil Sunz Scarlet | Demon Red | W1 | Pure Red |
| Fenrisian Grey | Gravestone Blue | W1 | Ice Storm |
| Fire Dragon Bright | Orange Flare | W1 | Magical Orange |
| Flash Gitz Yellow | Yellow Flame | W1 | Babe Blonde |
| Flayed One Flesh | Pale Skin | W3 | Pearl Skin |
| Fulgrim Pink | Neo Pink / Cyber Pink | W2/W3 | Centaur Skin |
| Gal Vorbak Red | Dread Red | W2 | Crusted Sore |
| Genestealer Purple | Sorceror's Cloak | W1 | Oozing Purple |
| Gorthor Brown | Ancient Forest | W1 | Werewolf Fur |
| Hoeth Blue | Leviathan Blue | W2 | Voidshield Blue |
| Incubi Darkness | Hydra Green | W2 | No equivalent |
| Ionrach Skin | Zombie Rot | W3 | Necrotic Flesh |
| Ironbreaker | Plate Armour | W1 | Plate Mail Metal |
| Iron Warriors | Dwarven Iron | W2 | No equivalent |
| Kakophoni Purple | Runic Purple / Spectral Purple | W1/W3 | Toxic Boils |
| Kantor Blue | Abyss Blue | W2 | Deep Blue |
| Karak Stone | Temple Stone | W1 | No equivalent |
| Kabalite Green | Jade Green | W2 | Wizards Orb |
| Khorne Red | Asmodeus Red | W2 | Chaotic Red |
| Kislev Flesh | Elven Skin | W1 | Kobold Skin |
| Leadbelcher | Sir Coates Silver | W1 | Gun Metal |
| Liberator Gold | Glistening Gold | W1 | Bright Gold |
| Loren Forest | Gung-Ho Green | W2 | Army Green |
| Lothern Blue | Seafarer Blue | W3 | Arctic Gem |
| Lugganath Orange | Solar Flare | W3 | Inner Light |
| Macragge Blue | Marine Blue | W1 | Dark Sky |
| Mechanicus Standard Grey | Dungeon Stone Grey | W1 | Dungeon Grey |
| Mephiston Red | Sanguine Scarlet | W1 | Vampire Red |
| Moot Green | Ethereal Green | W1 | Jungle Green |
| Mournfang Brown | Noble Steed Brown | W2 | Dirt Spatter |
| Morghast Bone | Sandstone | W1 | Desert Yellow |
| Naggaroth Night | Von Evile Purple | W3 | Terrestial Titan |
| Nuln Oil | Oblivion Black Wash | W1 | Dark Tone |
| Pallid Wych Flesh | Ivory Tusk | W1 | Brainmatter Beige |
| Pink Horror | Perisher Pink | W2 | Warlock Purple |
| Phoenician Purple | Enchantress Purple | W3 | Diabolic Plumb |
| Rakarth Flesh | Griffon Claw | W1 | Banshee Brown |
| Reikland Fleshshade | Flesh Wash | W1 | Flesh Tone |
| Retributor Armour | Dragon's Gold | W1 | Greedy Gold |
| Rhinox Hide | Cuirass Leather | W1 | Oak Brown |
| Runelord Brass | Battle Axe Brass | W2 | Rough Iron |
| Russ Grey | Wolf Grey | W1 | Wolf Grey |
| Screaming Bell | Steampunk Copper | W2 | Weapon Bronze |
| Squig Orange | Rust Orange | W1 | Dry Rust |
| Tuskgor Fur | Fur Cloak | W1 | Leather Brown |
| Doombull Brown | Boar Hide | W1 | Dirt Splatter |
| Pink Horror | Glistening Gums | W1 | Wasteland Soil |
| Screaming Skull | Vampire Fang | W1 | Skeleton Bone |
| Screamer Pink | Sword Hilt Burgundy | W1 | Wasteland Soil |
| Seraphim Sepia | Archaic Sepia Wash | W1 | Soft Tone |
| Skarsnik Green | Troll Snot Green | W2 | Mouldy Clothes |
| Skavenblight Dinge | Eidolon Grey | W2 | Hardened Carapace |
| Skrag Brown | Dry Rust Brown | W2 | Fur Brown |
| Skullcrusher Brass | Heirloom Gold | W3 | Bright Gold |
| Sotek Green | Antiquity Green | W3 | Pharaoh Guard |
| Sons of Horus Green | Ranger Cloak / Traitor Green | W2/W3 | Venom Worm |
| Steel Legion Drab | Dust Bowl | W1 | Leather Brown |
| Stormhost Silver | Mythril Blade | W1 | Shining Silver |
| Straken Green | Green Beret | W2 | Scaly Hide |
| Sybarite Green | Ghoul Green / Legion Green | W2/W3 | Elemental Bolt |
| Tau Light Ochre | Manticore Ochre | W2 | Troll Claws |
| Teclis Blue | Relic Blue | W3 | Crystal Blue |
| The Fang | Cold Corpse Blue | W1 | Wolf Grey |
| Thousand Sons Blue | Sentient Turquoise | W2 | Hydra Turquoise |
| Thunderhawk Blue | Shadow Blue | W3 | Thunderous Blue |
| Troll Slayer Orange | Fanatic Orange | W1 | Lava Orange |
| Ungor Flesh | Cerberus Brown | W2 | Barbarian Flesh |
| Ushabti Bone | Skeleton Legion | W1 | Skeleton Bone |
| Waaagh! Flesh | Orc Hide | W2 | Greenskin |
| Warboss Green | Goblinoid Green | W2 | Goblin Green |
| Warpstone Glow | Emerald Green | W1 | No equivalent |
| Wazdakka Red | Evil Eye Red | W2 | Abomination Gore |
| White Scar | White Star | W1 | Matt White |
| Wild Rider Red | Centurion Red | W3 | Blood Chalice |
| Word Bearers Red | Berserker Red | W1 | Chaotic Red |
| Warplock Bronze | No equivalent | — | No equivalent |
| Xereus Purple | Amethyst Rayne | W1 | Alien Purple |
| XV-88 | Gyzmo Fur | W2 | Fur Brown |
| Yriel Yellow | Skulker Yellow | W1 | Daemonic Yellow |
| Zandri Dust | Dragon Fang | W1 | Skeleton Bone |


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

---

## Paint Reference Tables

### TTC → Citadel → Army Painter (Waves 1–3)

| Two Thin Coats | Wave | Citadel | Army Painter |
|---|---|---|---|
| Berserker Red | W1 | Word Bearers Red | Chaotic Red |
| Sanguine Scarlet | W1 | Mephiston Red | Vampire Red |
| Demon Red | W1 | Evil Sun Scarlet | Pure Red |
| Dark Sun Yellow | W1 | Averland Sunset | Basilisk Brown |
| Skulker Yellow | W1 | Yriel Yellow | Daemonic Yellow |
| Yellow Flame | W1 | Flash Gitz Yellow | Babe Blonde |
| Marine Blue | W1 | Macragge Blue | Dark Sky |
| Elysium Blue | W1 | Calgar Blue | Ultramarine Blue |
| Celestial Blue | W1 | Blue Horror | Electric Blue |
| Rust Orange | W1 | Squig Orange | Dry Rust |
| Fanatic Orange | W1 | Troll Slayer Orange | Lava Orange |
| Orange Flare | W1 | Fire Dragon Bright | Magical Orange |
| Wyvern Green | W1 | Caliban Green | Angel Green |
| Emerald Green | W1 | Warpstone Glow | Greenskin |
| Ethereal Green | W1 | Moot Green | Jungle Green |
| Amethyst Rayne | W1 | Xereus Purple | Alien Purple |
| Sorceror's Cloak | W1 | Genestealer Purple | Oozing Purple |
| Runic Purple | W1 | Kakophoni Purple | Toxic Boils |
| Doom Death Black | W1 | Abaddon Black | Matt Black |
| Death Reaper | W1 | Corvus Black | Necromancer Cloak |
| Dungeon Stone Grey | W1 | Mechanicus Standard Grey | Dungeon Grey |
| Wizard Grey | W1 | Dawnstone | Uniform Grey |
| Carcharodon Grey | W1 | Administratum Grey | Ash Grey |
| White Star | W1 | White Scar | Matt White |
| Barbarian Brawn | W1 | Bugman's Glow | Fur Brown |
| Dwarven Skin | W1 | Cadian Fleshtone | Tanned Skin |
| Elven Skin | W1 | Kislev Flesh | Kobold Skin |
| Cuirass Leather | W1 | Rhinox Hide | Oak Brown |
| Griffon Claw | W1 | Rakarth Flesh | Banshee Brown |
| Dragon Fang | W1 | Zandri Dust | Skeleton Bone |
| Skeleton Legion | W1 | Ushabti Bone | Skeleton Bone |
| Vampire Fang | W1 | Screaming Skull | Skeleton Bone |
| Ivory Tusk | W1 | Pallid Wych Flesh | Brainmatter Beige |
| Trooper White | W1 | Corax White | Spaceship Exterior |
| Dust Bowl | W1 | Steel Legion Drab | Basilisk Brown |
| Sandstone | W1 | Morghast Bone | Desert Yellow |
| Temple Stone | W1 | Karak Stone | Skeleton Bone |
| Sir Coates Silver | W1 | Leadbelcher | Gun Metal |
| Plate Armour | W1 | Ironbreaker | Plate Mail Metal |
| Mythril Blade | W1 | Stormhost Silver | Shining Silver |
| Spartan Bronze | W1 | Balthazar Gold | True Copper |
| Dragon's Gold | W1 | Retributor Armour | Greedy Gold |
| Glistening Gold | W1 | Liberator Gold | Bright Gold |
| Royal Cloak | W1 | Barak-Nar Burgundy | Crusted Sore |
| Sword Hilt Burgundy | W1 | Screamer Pink | Wasteland Soil |
| Ancient Forest | W1 | Gorthor Brown | Werewolf Fur |
| Wasteland Brown | W1 | Baneblade Brown | Monster Brown |
| Boar Hide | W1 | Doombull Brown | Dirt Splatter |
| Glistening Gums | W1 | Pink Horror | Wasteland Soil |
| Fur Cloak | W1 | Tuskgor Fur | Leather Brown |
| Cold Corpse Blue | W1 | The Fang | Dungeon Grey |
| Wolf Grey | W1 | Russ Grey | Wolf Grey |
| Gravestone Blue | W1 | Fenrisian Grey | Ice Storm |
| Scorched Earth | W1 | Dryad Bark | Oak Brown |
| Oblivion Black Wash | W1 | Nuln Oil | Dark Tone |
| Battle Mud Wash | W1 | Agrax Earthshade | Strong Tone |
| Flesh Wash | W1 | Reikland Fleshshade | Flesh Tone |
| Orc Flesh Wash | W1 | Biel-Tan Green | Green Tone |
| Necrosis Green Wash | W1 | Athonian Camoshade | Military Shade |
| Archaic Sepia Wash | W1 | Seraphim Sepia | Soft Tone |
| Perisher Pink | W2 | Pink Horror | Warlock Purple |
| Hot Pink | W2 | Emperor's Children | Pixie Pink |
| Neo Pink | W2 | Fulgrim Pink | Centaur Skin |
| Dread Red | W2 | Gal Vorbak Red | Crusted Sore |
| Asmodeus Red | W2 | Khorne Red | Chaotic Red |
| Evil Eye Red | W2 | Wazdakka Red | Abomination Gore |
| Sentient Turquoise | W2 | Thousand Sons Blue | Hydra Turquoise |
| Cursed Blue | W2 | Ahriman Blue | Royal Cloak |
| Ray Gun Glow | W2 | Baharroth Blue | Toxic Mist |
| Abyss Blue | W2 | Kantor Blue | Deep Blue |
| Witching Hour Blue | W2 | Caledor Sky | Crystal Blue |
| Leviathan Blue | W2 | Hoeth Blue | Voidshield Blue |
| Jade Green | W2 | Kabalite Green | Wizards Orb |
| Ghoul Green | W2 | Sybarite Green | No equivalent |
| Fury Green | W2 | Castellan Green | Elf Green |
| Gung-Ho Green | W2 | Loren Forest | Army Green |
| Orc Hide | W2 | Waaagh! Flesh | Greenskin |
| Goblinoid Green | W2 | Warboss Green | Goblin Green |
| Troll Snot Green | W2 | Skarsnik Green | Mouldy Clothes |
| Hydra Green | W2 | Incubi Darkness | No equivalent |
| Druid Flesh | W2 | Catachan Flesh | Onyx Skin |
| Satyr Brown | W2 | Deathclaw Brown | Troll Claws |
| Noble Steed Brown | W2 | Mournfang Brown | Dirt Spatter |
| Dry Rust Brown | W2 | Skrag Brown | Fur Brown |
| Manticore Ochre | W2 | Tau Light Ochre | Troll Claws |
| Rodent Grey | W2 | Stormvermin Fur | No equivalent |
| Eidolon Grey | W2 | Skavenblight Dinge | Hardened Carapace |
| Ashen Grey | W2 | Eshin Grey | Necromancer Cloak |
| Dwarven Iron | W2 | Iron Warriors | No equivalent |
| Battle Axe Brass | W2 | Runelord Brass | Rough Iron |
| Steampunk Copper | W2 | Screaming Bell | Weapon Bronze |
| Hellion Red Wash | W2 | Carroburg Crimson | Red Tone |
| Tempest Blue Wash | W2 | Drakenhof Nightshade | Blue Tone |
| Magi Purple Wash | W2 | Druchii Violet | Purple Tone |
| Centurion Red | W3 | Wild Rider Red | Blood Chalice |
| Oxidation Green | W3 | Stegadon Scale Green | Scarab Green |
| Antiquity Green | W3 | Sotek Green | Pharaoh Guard |
| Mythic Turquoise | W3 | Temple Guard Blue | Talisman Teal |
| Eldar Robe | W3 | Caledor Sky | Royal Blue |
| Relic Blue | W3 | Teclis Blue | Crystal Blue |
| Seafarer Blue | W3 | Lothern Blue | Arctic Gem |
| Faust Blue | W3 | Dark Reaper | Night Sky |
| Shadow Blue | W3 | Thunderhawk Blue | Thunderous Blue |
| Frost Blue | W3 | Fenrisian Grey | Frost Blue |
| Von Evile Purple | W3 | Naggaroth Night | Terrestial Titan |
| Enchantress Purple | W3 | Phoenician Purple | Diabolic Plumb |
| Spectral Purple | W3 | Kakophoni Purple | Cultist Purple |
| Incubus Purple | W3 | Daemonette Hide | Hexed Violet |
| Enticing Purple | W3 | Warpfiend Grey | Violet Coven |
| Decadent Purple | W3 | Slaanesh Grey | Kraken Lavender |
| Scabbard Brown | W3 | Thondia Brown | Bootstrap Brown |
| Boot Strap Brown | W3 | Gorthor Brown | Leather Brown |
| Vambrace Brown | W3 | Baneblade Brown | Paratrooper Tan |
| Cyber Pink | W3 | Fulgrim Pink | Impish Rogue |
| Elixir Green | W3 | Gauss Blaster Green | Mossy Green |
| Solar Flare | W3 | Lugganath Orange | Inner Light |
| Ion Blue | W3 | Blue Horror | Frost Blue |
| Septic Green | W3 | No equivalent | Vivid Volt |
| Pale Skin | W3 | Flayed One Flesh | Pearl Skin |
| Scarab Red | W3 | No equivalent | Gemstone Red |
| Omega Blue | W3 | No equivalent | No equivalent |
| Enchantment Blue | W3 | No equivalent | No equivalent |
| Emperor's Purple | W3 | No equivalent | No equivalent |
| Carapace Green | W3 | No equivalent | Glittering Green |
| Fire Opal | W3 | No equivalent | No equivalent |
| Ancient Gold | W3 | No equivalent | No equivalent |
| Doom Metal | W3 | No equivalent | Death Metal |
| Chaos Bronze | W3 | Brass Scorpion | Evil Chrome |
| Blue Steel | W3 | Grey Knights Steel | No equivalent |
| Heirloom Gold | W3 | Skullcrusher Brass | Bright Gold |
| Bits O'Tin | W3 | Runelord Brass | Rough Iron |
| Smoke Grey Wash | W3 | Soulblight Grey | No equivalent |
| Hazard Yellow Wash | W3 | Casandora Yellow | No equivalent |
| Aztec Turquoise Wash | W3 | Coelia Greenshade | No equivalent |
| Bone Wash | W3 | No equivalent | Rust Tone |
| Satin Varnish | W3 | Stormshield | Satin Varnish |
| Gloss Varnish | W3 | No equivalent | Gloss Varnish |

---

### Other Brands → TTC / Citadel / Army Painter

When a source tutorial calls out a paint from another brand, use the table
below to find the TTC, Citadel, and Army Painter equivalents. Note the
original brand and paint in the recipe's Notes section.

#### Vallejo Game Color → Equivalents

| Vallejo Game Color | Two Thin Coats | Wave | Citadel | Army Painter |
|---|---|---|---|---|
| White (001) | White Star | W1 | White Scar | Matt White |
| Pale Flesh (003) | Elven Skin | W1 | Kislev Flesh | Kobold Skin |
| Elf Skintone (004) | No equivalent | — | Bestigor Flesh | No equivalent |
| Sunblast Yellow (006) | Yellow Flame | W1 | Flash Gitz Yellow | Babe Blonde |
| Gold Yellow (007) | Skulker Yellow | W1 | Yriel Yellow | No equivalent |
| Orange Fire (008) | Orange Flare | W1 | Fire Dragon Bright | Magical Orange |
| Hot Orange (009) | Fanatic Orange | W1 | Troll Slayer Orange | Lava Orange |
| Bloody Red (010) | Demon Red | W1 | Evil Sunz Scarlet | Pure Red |
| Gory Red (011) | Evil Eye Red | W2 | Wazdakka Red | Dragon Red |
| Scarlett Red (012) | Asmodeus Red | W2 | Khorne Red | Chaotic Red |
| Squid Pink (013) | Hot Pink | W2 | Emperor's Children | Pixie Pink |
| Warlord Purple (014) | Sword Hilt Burgundy | W1 | Screamer Pink | Wasteland Soil |
| Hexed Lichen (015) | Amethyst Rayne | W1 | Xereus Purple | Alien Purple |
| Royal Purple (016) | No equivalent | — | Naggaroth Night | No equivalent |
| Imperial Blue (020) | Abyss Blue | W2 | Kantor Blue | Deep Blue |
| Magic Blue (021) | Witching Hour Blue | W2 | Caledor Sky | Crystal Blue |
| Ultra Marine Blue (022) | Marine Blue | W1 | Macragge Blue | Ultramarine Blue |
| Electric Blue (023) | No equivalent | — | Teclis Blue | Electric Blue |
| Falcon Turquoise (024) | No equivalent | — | Sotek Green | Hydra Turquoise |
| Foul Green (025) | Ghoul Green | W2 | Sybarite Green | No equivalent |
| Jade Green (026) | Jade Green | W2 | Kabalite Green | Wizards Orb |
| Dark Green (028) | Wyvern Green | W1 | Caliban Green | Angel Green |
| Sick Green (029) | Emerald Green | W1 | Warpstone Glow | No equivalent |
| Goblin Green (030) | Goblinoid Green | W2 | Warboss Green | Goblin Green |
| Scorpy Green (032) | Ethereal Green | W1 | Moot Green | No equivalent |
| Bonewhite (034) | Skeleton Legion | W1 | Ushabti Bone | Skeleton Bone |
| Dead Flesh (035) | No equivalent | — | Nurgling Green | Necrotic Flesh |
| Bronze Flesh (036) | No equivalent | — | No equivalent | Barbarian Flesh |
| Filthy Brown (037) | Manticore Ochre | W2 | Tau Light Ochre | No equivalent |
| Plague Brown (039) | No equivalent | — | Zamesi Desert | No equivalent |
| Cobra Leather (040) | No equivalent | — | Balor Brown | No equivalent |
| Dwarf Skin (041) | No equivalent | — | Ratskin Flesh | Barbarian Flesh |
| Parasite Brown (042) | Dry Rust Brown | W2 | Skrag Brown | No equivalent |
| Beasty Brown (043) | Noble Steed Brown | W2 | Mournfang Brown | No equivalent |
| Dark Fleshtone (044) | No equivalent | — | Doombull Brown | No equivalent |
| Charred Brown (045) | Cuirass Leather | W1 | Rhinox Hide | Oak Brown |
| Ghost Grey (046) | No equivalent | — | Ulthuan Grey | No equivalent |
| Wolf Grey (047) | Gravestone Blue | W1 | Fenrisian Grey | Ice Storm |
| Sombre Grey (048) | Cold Corpse Blue | W1 | The Fang | Wolf Grey |
| Stonewall Grey (049) | Carcharodon Grey | W1 | Administratum Grey | Ash Grey |
| Cold Grey (050) | Wizard Grey | W1 | Dawnstone | Uniform Grey |
| Black (051) | Doom Death Black | W1 | Abaddon Black | Matt Black |
| Silver (052) | No equivalent | — | Runefang Steel | Shining Silver |
| Chain Mail (053) | Plate Armour | W1 | Ironbreaker | Plate Mail Metal |
| Gunmetal Metal (054) | Sir Coates Silver | W1 | Leadbelcher | Gun Metal |
| Polished Gold (055) | Dragon's Gold | W1 | Gehenna's Gold | Greedy Gold |
| Glorious Gold (056) | Glistening Gold | W1 | Auric Armour Gold | Bright Gold |
| Bright Bronze (057) | No equivalent | — | Hashut Copper | Weapon Bronze |
| Brassy Brass (058) | Battle Axe Brass | W2 | Runelord Brass | Rough Iron |
| Hammered Copper (059) | No equivalent | — | Brass Scorpion | No equivalent |
| Tinny Tin (060) | No equivalent | — | Warplock Bronze | No equivalent |
| Khaki (061) | Dragon Fang | W1 | Zandri Dust | No equivalent |
| Earth (062) | Dust Bowl | W1 | Steel Legion Drab | Leather Brown |
| Desert Yellow (063) | No equivalent | — | Tallarn Sand | Desert Yellow |
| Tan (066) | Barbarian Brawn | W1 | Bugman's Glow | Tanned Flesh |
| Heavy Red (141) | Sanguine Scarlet | W1 | Mephiston Red | Vampire Red |
| Heavy Blue (143) | Marine Blue | W1 | Macragge Blue | Dark Sky |
| Heavy Green (146) | Gung-Ho Green | W2 | Loren Forest | Army Green |
| Heavy Blackgreen (147) | Orc Hide | W2 | Waaagh! Flesh | Greenskin |
| Heavy Warmgrey (148) | Griffon Claw | W1 | Rakarth Flesh | Banshee Brown |
| Heavy Khaki (149) | No equivalent | — | Deathworld Forest | No equivalent |
| Heavy Ochre (150) | No equivalent | — | Balor Brown | No equivalent |
| Heavy Goldbrown (151) | Dark Sun Yellow | W1 | Averland Sunset | No equivalent |
| Heavy Grey (155) | Rodent Grey | W2 | Stormvermin Fur | No equivalent |
| Black Wash (73201) | Oblivion Black Wash | W1 | Nuln Oil | Dark Tone |
| Sepia Wash (73200) | Archaic Sepia Wash | W1 | Seraphim Sepia | Soft Tone |
| Red Shade Wash (73206) | Hellion Red Wash | W2 | Carroburg Crimson | Red Tone |
| Blue Shade Wash (73207) | Tempest Blue Wash | W2 | Drakenhof Nightshade | Blue Tone |
| Umber Shade Wash (73203) | Battle Mud Wash | W1 | Agrax Earthshade | Strong Tone |
| Fleshtone Shade Wash (73204) | Flesh Wash | W1 | Reikland Fleshshade | Flesh Tone |

#### Vallejo Model Color → Equivalents

| Vallejo Model Color | Two Thin Coats | Wave | Citadel | Army Painter |
|---|---|---|---|---|
| White (951) | White Star | W1 | White Scar | Matt White |
| Lemon Yellow (952) | No equivalent | — | Dorn Yellow | No equivalent |
| Flat Yellow (953) | Skulker Yellow | W1 | Yriel Yellow | Daemonic Yellow |
| Light Green (942) | Ethereal Green | W1 | Moot Green | No equivalent |
| Intermediate Green (891) | Emerald Green | W1 | Warpstone Glow | No equivalent |
| Pastel Green (885) | Goblinoid Green | W2 | Warboss Green | Goblin Green |
| Olive Green (967) | No equivalent | — | Elysian Green | No equivalent |
| Black Green (980) | Orc Hide | W2 | Waaagh! Flesh | Greenskin |
| Park Green (969) | Ghoul Green | W2 | Sybarite Green | No equivalent |
| Emerald (838) | Jade Green | W2 | Kabalite Green | Wizards Orb |
| Dark Prussian Blue (965) | Marine Blue | W1 | Macragge Blue | Dark Sky |
| Royal Purple (810) | Amethyst Rayne | W1 | Xereus Purple | Alien Purple |
| Violet (960) | Sword Hilt Burgundy | W1 | Screamer Pink | Wasteland Soil |
| Magenta (945) | Sword Hilt Burgundy | W1 | Screamer Pink | Wasteland Soil |
| Pink (958) | Hot Pink | W2 | Emperor's Children | Pixie Pink |
| Vermillion (909) | Demon Red | W1 | Evil Sunz Scarlet | Pure Red |
| Scarlet (817) | Fanatic Orange | W1 | Troll Slayer Orange | No equivalent |
| Red (926) | Sanguine Scarlet | W1 | Mephiston Red | Vampire Red |
| Carmine Red (908) | Asmodeus Red | W2 | Khorne Red | Chaotic Red |
| Cavalry Brown (982) | Evil Eye Red | W2 | Wazdakka Red | No equivalent |
| Orange Brown (981) | Dry Rust Brown | W2 | Skrag Brown | No equivalent |
| Brown Sand (876) | No equivalent | — | Balor Brown | No equivalent |
| Flat Brown (984) | Noble Steed Brown | W2 | Mournfang Brown | No equivalent |
| Burnt Umber (941) | Cuirass Leather | W1 | Rhinox Hide | Oak Brown |
| Mahogany Brown (846) | No equivalent | — | Doombull Brown | No equivalent |
| Yellow Ochre (913) | No equivalent | — | Zamesi Desert | No equivalent |
| Goldbrown (877) | Dark Sun Yellow | W1 | Averland Sunset | No equivalent |
| Gold Brown (877) | Dark Sun Yellow | W1 | Averland Sunset | No equivalent |
| Dark Yellow (978) | No equivalent | — | Tallarn Sand | Desert Yellow |
| Light Flesh (928) | Elven Skin | W1 | Kislev Flesh | Kobold Skin |
| Flat Flesh (955) | No equivalent | — | Bestigor Flesh | No equivalent |
| Brown Rose (no#) | Dwarven Skin | W1 | Cadian Fleshtone | Tanned Skin |
| Dark Flesh (927) | No equivalent | — | Ratskin Flesh | Barbarian Flesh |
| Black (950) | Doom Death Black | W1 | Abaddon Black | Matt Black |
| Basalt Grey (869) | Wizard Grey | W1 | Dawnstone | Uniform Grey |
| German Grey (995) | Rodent Grey | W2 | Stormvermin Fur | No equivalent |
| Pale Grey Blue (907) | Carcharodon Grey | W1 | Administratum Grey | Ash Grey |
| Oxford Blue (807) | Cold Corpse Blue | W1 | The Fang | Wolf Grey |
| Prussian Blue (965) | Marine Blue | W1 | Macragge Blue | Dark Sky |
| Dark Blue (930) | Witching Hour Blue | W2 | Caledor Sky | Crystal Blue |
| Sky Blue (961) | No equivalent | — | Teclis Blue | Electric Blue |
| Azure (902) | Seafarer Blue | W3 | Lothern Blue | Arctic Gem |
| Silver (997) | No equivalent | — | Runefang Steel | Shining Silver |
| Natural Steel (864) | Plate Armour | W1 | Ironbreaker | Plate Mail Metal |
| Gunmetal Grey (863) | Sir Coates Silver | W1 | Leadbelcher | Gun Metal |
| Gold (996) | Glistening Gold | W1 | Auric Armour Gold | Bright Gold |
| Old Gold (878) | Dragon's Gold | W1 | Gehenna's Gold | Greedy Gold |
| Bronze (998) | No equivalent | — | Hashut Copper | Weapon Bronze |
| Brass (801) | Battle Axe Brass | W2 | Runelord Brass | Rough Iron |
| Copper (999) | No equivalent | — | Brass Scorpion | No equivalent |
| Buff (976) | Skeleton Legion | W1 | Ushabti Bone | Skeleton Bone |
| Ivory (918) | Vampire Fang | W1 | Screaming Skull | Skeleton Bone |

#### Scale 75 → Equivalents

| Scale 75 | Two Thin Coats | Wave | Citadel | Army Painter |
|---|---|---|---|---|
| White Matt | White Star | W1 | White Scar | Matt White |
| Pale Skin Matt | Elven Skin | W1 | Kislev Flesh | Kobold Skin |
| Antares Red | Demon Red | W1 | Evil Sunz Scarlet | Pure Red |
| Deep Red Matt | Asmodeus Red | W2 | Khorne Red | Chaotic Red |
| Fuchsia Matt | Sword Hilt Burgundy | W1 | Screamer Pink | Wasteland Soil |
| Irati Green | Emerald Green | W1 | Warpstone Glow | No equivalent |
| Spring Green | Ethereal Green | W1 | Moot Green | No equivalent |
| Sky Blue | No equivalent | — | Teclis Blue | Electric Blue |
| Sol Yellow Matt | Skulker Yellow | W1 | Yriel Yellow | No equivalent |
| Sahara Yellow Matt | No equivalent | — | Tallarn Sand | Desert Yellow |
| Gobi Brown Matt | Dust Bowl | W1 | Steel Legion Drab | Leather Brown |
| Kalahari Orange Matt | Barbarian Brawn | W1 | Bugman's Glow | Tanned Flesh |
| Mars Orange Matt | Dry Rust Brown | W2 | Skrag Brown | No equivalent |
| Black Leather Matt | Cuirass Leather | W1 | Rhinox Hide | Oak Brown |
| Arabic Shadow Matt | Wasteland Brown | W1 | Baneblade Brown | Monster Brown |
| Boreal Green Matt | Fury Green | W2 | Castellan Green | Elf Green |
| Nacar Matt | Carcharodon Grey | W1 | Administratum Grey | Ash Grey |
| Artic Blue Matt | Wizard Grey | W1 | Dawnstone | Uniform Grey |
| Golden Skin Matt | Skeleton Legion | W1 | Ushabti Bone | Skeleton Bone |
| White Sands Matt | Vampire Fang | W1 | Screaming Skull | No equivalent |
| Dwarven Gold | Glistening Gold | W1 | Auric Armour Gold | Bright Gold |
| Elven Gold | Dragon's Gold | W1 | Gehenna's Gold | Greedy Gold |
| Viking Gold | Battle Axe Brass | W2 | Runelord Brass | Rough Iron |
| Necro Gold | No equivalent | — | Warplock Bronze | No equivalent |

#### Reaper Master Series → Equivalents

| Reaper | Two Thin Coats | Wave | Citadel | Army Painter |
|---|---|---|---|---|
| Pure White (9039) | White Star | W1 | White Scar | Matt White |
| Pure Black (9037) | Doom Death Black | W1 | Abaddon Black | Matt Black |
| Sun Yellow (9008) | Yellow Flame | W1 | Flash Gitz Yellow | Babe Blonde |
| Marigold Yellow (9007) | Skulker Yellow | W1 | Yriel Yellow | No equivalent |
| Fire Orange (9006) | Orange Flare | W1 | Fire Dragon Bright | Magical Orange |
| Phoenix Red (9005) | Fanatic Orange | W1 | Troll Slayer Orange | Lava Orange |
| Clotted Red (9134) | Sanguine Scarlet | W1 | Mephiston Red | Vampire Red |
| Deep Red (9002) | Asmodeus Red | W2 | Khorne Red | Chaotic Red |
| Rosy Highlight (9069) | Elven Skin | W1 | Kislev Flesh | Kobold Skin |
| Antique Rose (9139) | Barbarian Brawn | W1 | Bugman's Glow | Tanned Flesh |
| Rosy Skin (9068) | No equivalent | — | Ratskin Flesh | Barbarian Flesh |
| Yellowed Bone (9143) | Skeleton Legion | W1 | Ushabti Bone | Skeleton Bone |
| Intense Brown (9138) | Noble Steed Brown | W2 | Mournfang Brown | No equivalent |
| Muddy Brown (9028) | Cuirass Leather | W1 | Rhinox Hide | Oak Brown |
| Chestnut Brown (9071) | Dry Rust Brown | W2 | Skrag Brown | No equivalent |
| Chestnut Gold (9073) | No equivalent | — | Zamesi Desert | No equivalent |
| Tanned Leather (9031) | Barbarian Brawn | W1 | Bugman's Glow | Tanned Flesh |
| Jungle Moss (9082) | Orc Hide | W2 | Waaagh! Flesh | Greenskin |
| Olive Drab (9158) | Gung-Ho Green | W2 | Loren Forest | Army Green |
| Pine Green (9010) | Wyvern Green | W1 | Caliban Green | Angel Green |
| Clear Green (9096) | Emerald Green | W1 | Warpstone Glow | No equivalent |
| Field Green (9167) | Goblinoid Green | W2 | Warboss Green | Goblin Green |
| Pale Green (9012) | Ethereal Green | W1 | Moot Green | No equivalent |
| Brilliant Blue (9116) | No equivalent | — | Altdorf Guard Blue | Ultramarine Blue |
| Breonne Blue (9055) | Marine Blue | W1 | Macragge Blue | Dark Sky |
| Snow Shadow (9021) | Gravestone Blue | W1 | Fenrisian Grey | Ice Storm |
| Twilight Blue (9020) | Cold Corpse Blue | W1 | The Fang | Wolf Grey |
| Rainy Grey (9038) | Wizard Grey | W1 | Dawnstone | Uniform Grey |
| Weathered Stone (9087) | Carcharodon Grey | W1 | Administratum Grey | Ash Grey |
| Ghost White (9063) | No equivalent | — | Ulthuan Grey | No equivalent |
| Honed Steel (9053) | Plate Armour | W1 | Ironbreaker | Plate Mail Metal |
| Shadowed Steel (9052) | Sir Coates Silver | W1 | Leadbelcher | Gun Metal |
| Polished Silver (9054) | No equivalent | — | Runefang Steel | Shining Silver |
| New Gold (9051) | Dragon's Gold | W1 | Gehenna's Gold | Greedy Gold |
| Antique Gold (9050) | Glistening Gold | W1 | Auric Armour Gold | Bright Gold |
| Ancient Bronze (9049) | No equivalent | — | Hashut Copper | Weapon Bronze |
| Tarnished Brass (9198) | Battle Axe Brass | W2 | Runelord Brass | Rough Iron |
| Coppery Orange (9102) | No equivalent | — | Brass Scorpion | No equivalent |

#### Privateer Press P3 → Equivalents

| P3 | Two Thin Coats | Wave | Citadel | Army Painter |
|---|---|---|---|---|
| Morrow White | White Star | W1 | White Scar | Matt White |
| Thamar Black | Doom Death Black | W1 | Abaddon Black | Matt Black |
| Heartfire | Skulker Yellow | W1 | Yriel Yellow | Daemonic Yellow |
| Ryn Flesh | Elven Skin | W1 | Kislev Flesh | Kobold Skin |
| Khardic Flesh | Barbarian Brawn | W1 | Bugman's Glow | Tanned Flesh |
| Menoth White Base | Skeleton Legion | W1 | Ushabti Bone | Skeleton Bone |
| Menoth White Highlight | Vampire Fang | W1 | Screaming Skull | No equivalent |
| Hammerfall Khaki | Temple Stone | W1 | Karak Stone | No equivalent |
| Gun Corps Brown | Dust Bowl | W1 | Steel Legion Drab | Leather Brown |
| Bloodtracker Brown | Noble Steed Brown | W2 | Mournfang Brown | No equivalent |
| Umbral Umber | Cuirass Leather | W1 | Rhinox Hide | Oak Brown |
| Gnarls Green | Wyvern Green | W1 | Caliban Green | Angel Green |
| Ioson Green | Emerald Green | W1 | Warpstone Glow | No equivalent |
| Eldritch | Jade Green | W2 | Kabalite Green | Wizards Orb |
| Meredius Blue | No equivalent | — | Sotek Green | Hydra Turquoise |
| Cygnar Blue Highlight | Witching Hour Blue | W2 | Caledor Sky | Crystal Blue |
| Frostbite | Gravestone Blue | W1 | Fenrisian Grey | Ice Storm |
| Bad Bruise | No equivalent | — | No equivalent | No equivalent |
| Murderous Magenta | Sword Hilt Burgundy | W1 | Screamer Pink | Wasteland Soil |
| Beaten Purple | Amethyst Rayne | W1 | Xereus Purple | Alien Purple |
| Pig Iron | Sir Coates Silver | W1 | Leadbelcher | Gun Metal |
| Cold Steel | Plate Armour | W1 | Ironbreaker | Plate Mail Metal |
| Quicksilver | No equivalent | — | Runefang Steel | Shining Silver |
| Solid Gold | Glistening Gold | W1 | Auric Armour Gold | Bright Gold |
| Brass Balls | Battle Axe Brass | W2 | Runelord Brass | Rough Iron |
| Molten Bronze | No equivalent | — | Hashut Copper | Weapon Bronze |
| Deathless Metal | No equivalent | — | Warplock Bronze | No equivalent |
| Necrotite Green | Ethereal Green | W1 | Moot Green | No equivalent |
| Great Coat Grey | Dungeon Stone Grey | W1 | Mechanicus Standard Grey | No equivalent |
| Bastion Grey | Rodent Grey | W2 | Stormvermin Fur | No equivalent |
| Jack Bone | No equivalent | — | Nurgling Green | Necrotic Flesh |
| Carnal Pink | Hot Pink | W2 | Emperor's Children | Pixie Pink |
