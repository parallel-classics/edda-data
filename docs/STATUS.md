# Status

Version 0.1.0, 2026-10-24. Table from `python -I scripts/validate.py` (overlays applied; `source` = base
edition text, `auto` = automatic alignment or modernisation, `draft` = unreviewed human or AI text,
`empty` = no text in the cell).

```
part            col     source     auto    draft reviewed disputed    empty    total
------------------------------------------------------------------------------------
Formáli         on          12        0        0        0        0        0       12
Formáli         is           0       12        0        0        0        0       12
Formáli         en           0       12        0        0        0        0       12
Gylfaginning    on         345        0        0        0        0        0      345
Gylfaginning    is           0      344        0        0        0        1      345
Gylfaginning    en           0      340        0        0        0        5      345
Skáldskaparmál  on         854        0        0        0        0        0      854
Skáldskaparmál  is           0      854        0        0        0        0      854
Skáldskaparmál  en           0      843        1        0        0       10      854
Háttatal        on         303        0        0        0        0        0      303
Háttatal        is           0      303        0        0        0        0      303
Háttatal        en           0        0      303        0        0        0      303
```

1,514 rows; 0 reviewed cells; 2 overlay files (304 AI draft records); 40 image records (40 of 42 slots; `p-c5` Sigtún and `g-c54` Gangleri alone have no public-domain depiction). All 40 records carry `checked_by: claude (Commons API metadata check, 2026-10-24); human verification pending` — the licence basis was read from the Wikimedia Commons file pages, not yet confirmed by a person against the institution records.

What the columns contain: Formáli, Skáldskaparmál and Háttatal Icelandic are automatic modernised spelling
(about 94% of tokens right); Gylfaginning Icelandic is Netútgáfan's text, automatically aligned; English is
Brodeur, automatically aligned, except Háttatal (AI draft) and `s-c72-8` (AI draft). The empty cells are the
"included in the previous row" cases (1 Icelandic + 4 English in Gylfaginning, 10 English in Skáldskaparmál)
and rows Brodeur has no sentence for.

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
- Brodeur (sacred-texts transcription): ten scan errors fixed by a list in `parse_en.py`; every lost *œ*
  restored; page-break joins applied. Unknown residual errors are likely; the Wikisource proofread copy is the
  planned replacement base.
- Guðni Jónsson's Gylfaginning ends before the two closing sentences on Öku-Þórr and the Turks that Netútgáfan
  and Brodeur both have (noted at the last row of chapter 54).

Modernised spelling (automatic column)
- Residuals such as *it fyrsta* for *hið fyrsta*, occasional inflection endings, and words never seen in
  Gylfaginning left in Old Norse spelling. Held-out accuracy 94.1% on Gylfaginning; the error rate on
  Skáldskaparmál's kenning lists and Háttatal's verse is probably higher (more rare words).

English draft (Háttatal, `s-c72-8`)
- Unreviewed AI draft; 32 of 304 rows contain `[?]`. Metrical terms are kept in Old Norse with a gloss, as
  the English-stream rules require, but consistency across sections has not been checked.

Images
- 42 briefs, 0 verified records. The public-domain candidates named in `scenes.json` are unverified.
