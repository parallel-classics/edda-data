# images/worlds/ — background picture for the map of the worlds (task 20c)

`worlds-background-v3.jpg` (2576 x 2576) is Grigory Sapunov's picture of 2026-11-07, downscaled (Lanczos) from his
4096 px "world v8 full res.jpg", which stays with the maintainer and is not in the repository. It carries no text; the
labels are an SVG layer on top (task 20b). Credit line (decision of 2026-11-02): "© 2026 Grigory Sapunov"; licence
CC BY 4.0; the labels and the SVG are CC BY 4.0 like the rest of the edition. Provenance, kept in the records only and
not shown on the page: `made_with` in `anchors-v3.json` and `bg/index.json`.

`anchors-v3.json`: label anchor points in image pixels for the realms and features drawn in v3 (one anchors file per
image version; `realms.json` names the current one in its key `anchors`, and the build, the validator and
`make_worlds.py background` read that one). v3 (2026-11-07, Grigory's redraw following the "World of the Eddas"
structure) supersedes v2: Hel inside Niflheimr with Niflhel below it, Urðarbrunnr in heaven, Mímisbrunnr under the
giants' root, Vanaheimr and Gimlé in heaven; Gjallarbrú, the river Gjöll and Surtr are now drawn; Náströnd (after
Ragnarök) is not drawn and is listed under the map only. v1 and v2 are kept only in the git history. Features not in
the picture (Ginnungagap, Élivágar, Náströnd) are listed or go in the note.

`bg/` holds the resized copies (1600 / 1000 / 600 px, WebP and JPEG, `bg/index.json`), written by
`edda-site/pipeline/make_worlds.py background`; the website serves those, never the original, and works without the
picture (a schematic SVG on parchment colour). Spec: `edda-site/docs/specs/WORLD_MAP.md`.

`realms.json` (by hand, 2026-11-01, for the curator to review): the placements — one entry per realm or feature with
the entity id, the anchor, our short description (EN by the editor, IS a draft), and the rows that place it, with
notes on variants. Labels are the entities' Old Norse names; `label` pins the nominative where needed. `label_en`
(2026-11-07, required by the validator) is the English name shown smaller under every label: the entity's
`names.en` where that is an English form, else the form the edition's English texts use (Brodeur, Bellows) or the
usual anglicised form. Where English keeps the Old Norse name (Hel, Hvergelmir, Glitnir, Bilskirnir) it repeats it.

`diagrams.json` + `diagrams/`: the historic diagrams (Wheaton 1844, Bagge 1847, the Skálholt map), hand keys plus the
Commons licence record from `make_worlds.py diagrams`, which also stores the 1000 px copies. All three are public
domain. The validator checks all three files (`scripts/validate.py`).
