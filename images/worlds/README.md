# images/worlds/ — background picture for the map of the worlds (task 20c)

`worlds-background-v2.jpg` (2576 x 2576) is Grigory Sapunov's picture of 2026-11-01. It carries no text; the labels
are an SVG layer on top (task 20b). Credit line (decision of 2026-11-02): "© 2026 Grigory Sapunov"; licence CC BY 4.0
(replacing the CC0 of 2026-11-01); the labels and the SVG are CC BY 4.0 like the rest of the edition. Provenance, kept
in the records only and not shown on the page: made with Google Gemini image generation from the prompt in
edda-site/docs/specs/WORLD_MAP.md (`made_with` in `anchors-v2.json` and `bg/index.json`). The 2576 px file here is the
working master the anchors refer to; the maintainer keeps the 4096 px original.

`anchors-v2.json`: label anchor points in image pixels for the realms and features drawn in v2 (one anchors file
per image version). v2 (same day) supersedes v1: Gimlé is a gold-roofed hall (Gylfaginning 17), four stags, Náströnd
a hall woven of serpents (Völuspá 38); v1 is kept only in the git history. Features not in the picture (Ginnungagap,
Gjallarbrú, Élivágar, Veðrfölnir) are label-only or go in the note.

`bg/` holds the resized copies (1600 / 1000 / 600 px, WebP and JPEG, `bg/index.json`), written by
`edda-site/pipeline/make_worlds.py background`; the website serves those, never the original, and works without the
picture (a schematic SVG on parchment colour). Spec: `edda-site/docs/specs/WORLD_MAP.md`.

`realms.json` (by hand, 2026-11-01, for the curator to review): the placements — one entry per realm or feature with
the entity id, the anchor, our short description (EN by the editor, IS a draft), and the rows that place it, with
notes on variants. Labels are the entities' Old Norse names; `label` pins the nominative where needed.

`diagrams.json` + `diagrams/`: the historic diagrams (Wheaton 1844, Bagge 1847, the Skálholt map), hand keys plus the
Commons licence record from `make_worlds.py diagrams`, which also stores the 1000 px copies. All three are public
domain. The validator checks all three files (`scripts/validate.py`).
