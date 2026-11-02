# edda-data — Open Edda, the dataset

Read it at **https://openedda.is**.

An open, community-corrected parallel edition of both Eddas: Snorri Sturluson's *Edda* (c. 1220) and the
*Poetic Edda*. The normalised Old Norse is the pivot; beside it stand the text in modern Icelandic spelling and
an English translation, and further languages can be added as columns. All four parts of Snorri's Edda
(Formáli/Prologue, Gylfaginning, Skáldskaparmál, Háttatal) are aligned paragraph by paragraph into 1,514
rows; the 45 poems of Guðni Jónsson's *Eddukvæði* are aligned stanza by stanza into 1,952 rows, and 91 places
where Snorri quotes a poem are linked both ways.

This repository is the thing to cite: the sources as fetched, the aligned rows, the human corrections
(overlays), the image records and the licences. It contains no code beyond a validator. The pipeline that
produces the aligned rows and the website live in the sibling repository **edda-site**.

## Sources and provenance

The medieval texts are in the public domain. Two of the modern editions used are not yet cleared: Guðni
Jónsson's normalised Old Norse and Netútgáfan's modern-spelling Gylfaginning (see `LICENSE`, section 1).
The English translations (Brodeur 1916, Bellows 1923) are in the public domain.

| Column | Text | Edition | Where fetched from | Parts |
| --- | --- | --- | --- | --- |
| Old Norse (`on`) | *Edda Snorra Sturlusonar* | Guðni Jónsson's normalised edition (Íslendingasagnaútgáfan, 1954) as published by heimskringla.no | GitHub mirror `cltk/old_norse_texts_heimskringla` (CLTK Old Norse corpus) | all four |
| Modern Icelandic (`is`) | *Gylfaginning* | Netútgáfan, June 1997 | https://netutgafan.snerpa.is/snorri/gylf.htm | Gylfaginning only; the other parts carry an automatic modernisation |
| English (`en`) | *The Prose Edda* | Arthur Gilchrist Brodeur (American-Scandinavian Foundation, 1916) | sacred-texts.com transcription | Prologue, Gylfaginning, Skáldskaparmál (Brodeur omitted Háttatal) |
| Old Norse (`on`), poems | *Eddukvæði* | Guðni Jónsson's normalised edition (Íslendingasagnaútgáfan, 1949) as published by heimskringla.no | heimskringla.no pages, fetched 2026-10-25 | all 45 poems |
| English (`en`), poems | *The Poetic Edda* | Henry Adams Bellows (American-Scandinavian Foundation, 1923) | English Wikisource, *The Poetic Edda (tr. Bellows)*, MediaWiki API | 36 of the 45 poems (his 35 pages; Svipdagsmol and Hyndluljoth each cover two of Guðni Jónsson's poems, Fra Dautha Sinfjotla joins Grípisspá) |

Details per file, fetch dates and known defects: `sources/README.md`. The Wikisource proofread copy of
Brodeur is the planned cleaner base for the English column (see `docs/ROADMAP.md`).

## What is in the rows

| Part | Chapters | Rows | Old Norse | Icelandic | English |
| --- | --- | --- | --- | --- | --- |
| Formáli (Prologue) | 5 | 12 | Guðni Jónsson 1954 | automatic modernisation | Brodeur 1916 |
| Gylfaginning | 54 | 345 | Guðni Jónsson 1954 | Netútgáfan 1997 | Brodeur 1916 |
| Skáldskaparmál | 89 | 854 | Guðni Jónsson 1954 | automatic modernisation | Brodeur 1916 (his 74 chapters mapped onto 89) |
| Háttatal | 3 sections, 102 stanzas | 303 | Guðni Jónsson 1954 | automatic modernisation | AI draft, unreviewed |
| *Poetic Edda* | 45 poems in 3 groups (17 mythological, 20 heroic, 8 other) | 1,952 (stanzas, prose passages, unnumbered verse) | Guðni Jónsson 1949 | automatic modernisation | Bellows 1923 for 36 poems; AI draft (marked) for the 9 others and the stanzas he left out |

Total: 3,466 rows (Snorri 1,514, poems 1,952). Poem rows have ids `<poem>-s<stanza>` (`vsp-s19`) and
`<poem>-p<k>` for prose passages and `<poem>-v<k>` for verse without a stanza number; Snorri's quotations of the poems are listed in `aligned/poetic/links.json`.
Chapter and poem titles in each language are in `aligned/titles.json` (English titles are an unreviewed AI draft). A row is one Old Norse paragraph or stanza with its Icelandic and English counterparts.
Row ids look like `g-c35-5` (Gylfaginning, chapter 35, row 5) and never change once published.

What is automatic, and how good it is:

- **Alignment** of the Icelandic and English to the Old Norse is by dynamic programming at sentence level,
  regrouped per Old Norse block (features: token-prefix overlap for Icelandic; names, speakers, numbers,
  verse structure, length and position for English). Each row carries confidence scores (`s_en`, `s_is`).
- **Modernised spelling** outside Gylfaginning comes from a word dictionary plus identity-aware suffix rules
  learned from the Gylfaginning pair. Five-fold held-out token accuracy on Gylfaginning: 94.1%
  (71.6% if the Old Norse is left unchanged). Typical residuals: *it fyrsta* for *hið fyrsta*,
  occasional inflection endings.
- **English for Háttatal** (303 rows) and for Skáldskaparmál row `s-c72-8` is an AI draft translation
  (status `draft`, author `ai:claude-2026-10`), unreviewed; `[?]` marks a line the draft was unsure of.

Nothing automatic is presented as settled: every cell has a status (`auto`, `draft`, `reviewed`,
`disputed`), see `docs/DATA_MODEL.md` and the current counts in `docs/STATUS.md`.

## Layout

```
sources/      the base texts as fetched (txt/html) and their parsed JSON — immutable
  on/         Guðni Jónsson: prologus.txt, gylfaginning.txt, skaaldskaparmaal.txt, haattatal.txtl; on_{prol,gylf,skald,hatt}.json
  on/eddukvaedi/  gj_eddukvaedi.json — the 45 poems as fetched from heimskringla.no (page text per poem)
  is/         Netútgáfan: gylf_is.html; is_gylf.json
  en/         Brodeur: brodeur_{prologue,gylf,skald}.html; en_{prol,gylf,skald}.json
  en/bellows/ bellows_poetic_edda.json — Bellows' 35 Wikisource pages (stanzas, prose, notes, introductions)
aligned/      al_{prol,gylf,skald,hatt}.json — Snorri's rows; poetic/al_<poem>.json, index.json, links.json — the poems
              and Snorri's quotations of them; titles.json — titles per language. GENERATED by edda-site, never hand-edited
auto/         modernizer.json (learned tables), is_{prol,skald,hatt}_auto.json, en_draft.json (AI draft, as produced),
              titles_en.json (AI draft English titles)
overlays/     human (and labelled AI) changes keyed by row id and cell: overlays/{on,is,en}/*.json
images/       scenes.json (42 illustration briefs), records.json (verified public-domain images), pd/ (files)
scripts/      validate.py (checks everything, prints the status table), drafts_to_overlays.py
docs/         DATA_MODEL.md, STATUS.md, ROADMAP.md
```

## Validate

```
python -I scripts/validate.py
```

Standard library only, Python 3.11+. Exits non-zero on any structural error and prints the status table
(rows per part and column by status).

## How to cite

Releases are tagged (`v0.1.0` is the initial import) and will be archived on Zenodo with a DOI.

> Sapunov, G. (2026). *Open Edda: a parallel Old Norse – Icelandic – English dataset of Snorri's Edda and the Poetic Edda* (v0.1.0).
> DOI: 10.5281/zenodo.XXXXXXX (placeholder until the first Zenodo release).

Machine-readable citation: `CITATION.cff`. Please also credit the source editions named above
(heimskringla.no asks to be credited for the Guðni Jónsson text).

## Licences

- The medieval texts and the two English translations are in the public domain; the rights in Guðni
  Jónsson's normalised editions and in Netútgáfan's text are being confirmed (`LICENSE`, section 1).
- New contributions (overlays, image records, documentation) are licensed **CC BY 4.0** (`LICENSE`).
  An open decision remains whether to switch to CC0; contributors are asked to accept either.
- Contributors are credited per row (the `author` field of each overlay record) and on a contributors page.
- Code in this repository (`scripts/`) is MIT, like edda-site.

## How to contribute

The intended route is the website's editor (click a cell, fix it, give a reason), which turns accepted edits
into pull requests here. Until the editor exists, open a pull request that adds overlay records, or open an
issue with the `row-problem` template (`.github/ISSUE_TEMPLATE/row-problem.md`). Rules, roles and statuses:
`CONTRIBUTING.md`.

## Status summary

As of v0.1.0 everything is automatic or draft: 1,514 rows, 0 reviewed cells. See `docs/STATUS.md`.

## Contact

Maintainer: Grigory Sapunov (see the GitHub profile of the repository owner). Takedown or licence questions
go to the same address or to an issue.
