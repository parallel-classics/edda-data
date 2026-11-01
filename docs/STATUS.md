# Status

Version 0.1.0, 2026-10-24; tables refreshed 2026-11-01 (task 17). Tables from `python -I scripts/validate.py`
(overlays applied). Two properties per cell: the **origin** of the text (`edition` = Guðni Jónsson's base text,
`published` = a published human text placed in the row automatically — Brodeur, Bellows, Netútgáfan —, `machine` =
automatic spelling modernisation, `ai` = AI draft, `contributor` = written through the edit flow) and the **check**
state (for published text the placement: `aligned-auto` / `aligned-checked`; for the rest the words: `unreviewed` /
`reviewed`; `disputed` when reviewers disagree). `empty` = no text in the cell. The third table is the old one-word
form kept for comparison (`auto` there means "placed automatically" for published text).

```
[origin]
part            col        edition    published      machine           ai  contributor        empty    total
------------------------------------------------------------------------------------------------------------
Formáli         on              12            0            0            0            0            0       12
Formáli         is               0            0           12            0            0            0       12
Formáli         en               0           12            0            0            0            0       12
Gylfaginning    on             345            0            0            0            0            0      345
Gylfaginning    is               0          344            0            0            0            1      345
Gylfaginning    en               0          340            0            0            0            5      345
Skáldskaparmál  on             854            0            0            0            0            0      854
Skáldskaparmál  is               0            0          854            0            0            0      854
Skáldskaparmál  en               0          843            0            1            0           10      854
Háttatal        on             303            0            0            0            0            0      303
Háttatal        is               0            0          303            0            0            0      303
Háttatal        en               0            0            0          303            0            0      303
Poetic Edda     on            1952            0            0            0            0            0     1952
Poetic Edda     is               0            0         1952            0            0            0     1952
Poetic Edda     en               0         1587            0          359            0            6     1952

[check]
part            col       aligned-auto  aligned-checked       unreviewed         reviewed         disputed            empty    total
------------------------------------------------------------------------------------------------------------------------------------
Formáli         on                   0                0               12                0                0                0       12
Formáli         is                   0                0               12                0                0                0       12
Formáli         en                  12                0                0                0                0                0       12
Gylfaginning    on                   0                0              345                0                0                0      345
Gylfaginning    is                 344                0                0                0                0                1      345
Gylfaginning    en                 340                0                0                0                0                5      345
Skáldskaparmál  on                   0                0              854                0                0                0      854
Skáldskaparmál  is                   0                0              854                0                0                0      854
Skáldskaparmál  en                 843                0                1                0                0               10      854
Háttatal        on                   0                0              303                0                0                0      303
Háttatal        is                   0                0              303                0                0                0      303
Háttatal        en                   0                0              303                0                0                0      303
Poetic Edda     on                   0                0             1952                0                0                0     1952
Poetic Edda     is                   0                0             1952                0                0                0     1952
Poetic Edda     en                1587                0              359                0                0                6     1952

[status (old one-word form)]
part            col      source      auto     draft  reviewed  disputed     empty    total
------------------------------------------------------------------------------------------
Formáli         on           12         0         0         0         0         0       12
Formáli         is            0        12         0         0         0         0       12
Formáli         en            0        12         0         0         0         0       12
Gylfaginning    on          345         0         0         0         0         0      345
Gylfaginning    is            0       344         0         0         0         1      345
Gylfaginning    en            0       340         0         0         0         5      345
Skáldskaparmál  on          854         0         0         0         0         0      854
Skáldskaparmál  is            0       854         0         0         0         0      854
Skáldskaparmál  en            0       843         1         0         0        10      854
Háttatal        on          303         0         0         0         0         0      303
Háttatal        is            0       303         0         0         0         0      303
Háttatal        en            0         0       303         0         0         0      303
Poetic Edda     on         1952         0         0         0         0         0     1952
Poetic Edda     is            0      1952         0         0         0         0     1952
Poetic Edda     en            0      1587       359         0         0         6     1952
```

Poetic Edda (added 2026-10-25): 45 poems, 1,952 rows (stanzas, prose passages, unnumbered verse); Icelandic
automatic; English for every row: Bellows 1923 for 36 poems (1,587 rows, matched automatically — `published` /
`aligned-auto`), Brodeur where Snorri quotes a stanza Bellows does not cover (2 rows), and an unreviewed AI draft for the
rest (359 rows: the nine poems Bellows did not translate and the stanzas he left out; records in
`overlays/en/poetic-ai-draft.json`, 135 lines marked [?]). The 6 empty cells are stanzas whose English sits in the
previous row. 91 links from Snorri's rows. Titles: 196 in Old Norse, automatic Icelandic and AI-draft English.

3,480 rows (Snorri 1,514, Poetic Edda 1,966); 0 reviewed cells; 2 overlay files (304 AI draft records); 73 image records (40 depictions, 38 placed; 33 documentary: 2 manuscripts, 18 monuments, 13 places), 71 placed in all (`placed: false` on `s-c3` and `s-c46`, whose pictures turned out not to show the scene; `p-c5` Sigtún and `g-c54` Gangleri alone have no public-domain depiction at all). Generation briefs for those four slots and eight optional ones: `images/generation-briefs.md`. All 40 records carry `checked_by: claude (Commons API metadata check, 2026-10-24); human verification pending` — the licence basis was read from the Wikimedia Commons file pages, not yet confirmed by a person against the institution records.

What the columns contain: Formáli, Skáldskaparmál and Háttatal Icelandic are automatic modernised spelling
(about 94% of tokens right); Gylfaginning Icelandic is Netútgáfan's text, automatically aligned; English is
Brodeur, automatically aligned, except Háttatal (AI draft) and `s-c72-8` (AI draft). The empty cells are the
"included in the previous row" cases (1 Icelandic + 4 English in Gylfaginning, 10 English in Skáldskaparmál)
and rows Brodeur has no sentence for.

## Names (entities/, task 16a, 2026-11-01)

Generated by `edda-site/pipeline/make_entities.py detect` from the curated seed; everything is status `auto`.

| | |
|---|---|
| entities | 550 (15 added by rules.json: targets of ambiguity rules and the ones the curator asked for), 548 with a mention |
| mentions | 17223 (Old Norse 5878, Icelandic 5871, English 5474) |
| flagged `check` (ambiguous, unresolved) | 141 Old Norse mentions |
| sentence-initial mentions added beyond the seed | 1424 |
| first-appearance cards | 84 (free image and notable or ≥ 3 narrative mentions) |
| images with a usable licence | 96 of 96 entities with a candidate (63 hand-picked pictures, 33 Wikidata) |

Review sample (`make_entities.py sample --n 200 --seed 7`, checked by hand on 2026-11-01, before the derived
case forms were added; the 45 derived-form mentions were then checked in full, all right):

| | |
|---|---|
| precision | 195 of 197 linked mentions right (99%); 3 of the 200 were `check` and not counted. The two errors came from the seed (Buðla → Buðlungar, Hjaðningar → the battle) and are fixed by a rule / reported |
| recall | 166 of 200 random capitalised mid-sentence Old Norse tokens linked (83%); target 90% |

The recall gap is names the seed lacks, mostly names that also exist as common words (Hel, Skaði, Rán, Freki,
Dagr, Nótt, Sól, Þrymr, Þriði, Gram, Norðri/Suðri/Austri/Vestri ...): `entities/report.md` lists the unlinked
mid-sentence tokens with counts for the curator.

## Known issues

Alignment
- Gylfaginning: 5 rows carry a "see previous row" marker (`is_cont`/`en_cont`), spot-checked as correct. About
  20 rows were flagged as weak English matches during alignment; with the page's current threshold
  (`s_en < -0.5`, prose rows) 3 Gylfaginning rows and 49 Skáldskaparmál rows show the "?" mark. Spot checks
  found the flagged Gylfaginning rows correct; Skáldskaparmál has not been spot-checked systematically.
- Gylfaginning chapter 8, row 6: Brodeur renders the paragraph as the last line of the verse above; the page
  says so instead of "not in Brodeur".
- Skáldskaparmál: Brodeur's 74 chapters are mapped onto Guðni Jónsson's 89 by a chapter-level alignment
  (`chapter_beads`); groups where one Brodeur chapter covers several of ours put his notes with the first.
  Row `s-c72-8` (a list of riders and their horses) has no Brodeur text; an AI draft fills it.
- Skáldskaparmál English has 10 empty cells (`en_cont`) where Brodeur ran two paragraphs into one sentence.

Sources
- Licence: the medieval texts and both English translations are public domain; the rights in Guðni Jónsson's
  normalised editions (1949, 1954) and in Netútgáfan's Gylfaginning are not yet confirmed (`LICENSE` §1).
- Brodeur (sacred-texts transcription): ten scan errors fixed by a list in `parse_en.py`; every lost *œ*
  restored; page-break joins applied. Unknown residual errors are likely; the Wikisource proofread copy is the
  planned replacement base.
- Guðni Jónsson's Gylfaginning ends before the two closing sentences on Öku-Þórr and the Turks that Netútgáfan
  and Brodeur both have (noted at the last row of chapter 54).

Poetic Edda
- Stanza alignment Guðni Jónsson ↔ Bellows is automatic except Völuspá (hand table; the aligner agrees on 64
  of 66). A spot check of 30 random stanzas elsewhere found 27 right; misses cluster where Bellows reorders or
  renumbers (Hávamál 85–90, Atlamál, Fjölsvinnsmál, Sigurðarkviða in skamma near the end, Guðrúnarkviða III,
  Helgakviða Hundingsbana II 17–19). Weak matches carry `s_en` and show "?" on the page.
- Speaker lines are kept inside the stanza (Old Norse "Loki kvað:", Bellows "Loki spake:").
- Quotation links were found automatically; Snorri's paraphrases and strongly variant quotations are not
  linked.
- Völuspá: Guðni Jónsson 34 (Hauksbók, Váli) has no Bellows stanza; 54 (a fourth refrain) shows Bellows'
  refrain. The moderniser rejects learned word pairs that drop the first letter or more than two letters
  (held-out accuracy 94.15%); Formáli/Skáldskaparmál/Háttatal automatic columns are not regenerated with it yet.

Modernised spelling (automatic column)
- Residuals such as *it fyrsta* for *hið fyrsta*, occasional inflection endings, and words never seen in
  Gylfaginning left in Old Norse spelling. Held-out accuracy 94.1% on Gylfaginning; the error rate on
  Skáldskaparmál's kenning lists and Háttatal's verse is probably higher (more rare words).

English draft (Háttatal, `s-c72-8`)
- Unreviewed AI draft; 32 of 304 rows contain `[?]`. Metrical terms are kept in Old Norse with a gloss, as
  the English-stream rules require, but consistency across sections has not been checked.

Images
- 42 briefs, 0 verified records. The public-domain candidates named in `scenes.json` are unverified.
