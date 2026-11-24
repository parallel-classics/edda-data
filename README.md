# edda-data — Open Edda, the dataset

Read it at **https://openedda.is**.

An open, community-corrected parallel edition of both Eddas: Snorri Sturluson's *Edda* (c. 1220) and the
*Poetic Edda*. The normalised Old Norse is the pivot; beside it stand the text in modern Icelandic spelling and
an English translation, and further languages can be added as columns. All four parts of Snorri's Edda
(Formáli/Prologue, Gylfaginning, Skáldskaparmál, Háttatal) are aligned paragraph by paragraph into 1,514
rows; the 45 poems of Guðni Jónsson's *Eddukvæði* are aligned stanza by stanza into 1,952 rows, and 91 places
where Snorri quotes a poem are linked both ways.

This repository is the thing to cite: the sources as fetched, the aligned rows, the human corrections
(overlays), further English versions, the names index, the Mímir guide, the pictures and the licences. It
contains no code beyond a validator. The pipeline that
produces the aligned rows and the website live in a second repository, edda-site, which is not public yet.

## Sources and provenance

The medieval texts are in the public domain. Two of the modern editions used are not yet cleared: Guðni
Jónsson's normalised Old Norse and Netútgáfan's modern-spelling Gylfaginning (see `LICENSE`, section 1).
The English translations (Brodeur 1916, Bellows 1923, Thorpe 1866, Anderson 1880) are in the public domain.

| Column | Text | Edition | Where fetched from | Parts |
| --- | --- | --- | --- | --- |
| Old Norse (`on`) | *Edda Snorra Sturlusonar* | Guðni Jónsson's normalised edition (Íslendingasagnaútgáfan, 1954) as published by heimskringla.no | GitHub mirror `cltk/old_norse_texts_heimskringla` (CLTK Old Norse corpus) | all four |
| Modern Icelandic (`is`) | *Gylfaginning* | Netútgáfan, June 1997 | https://netutgafan.snerpa.is/snorri/gylf.htm | Gylfaginning only; the other parts carry an automatic modernisation |
| English (`en`) | *The Prose Edda* | Arthur Gilchrist Brodeur (American-Scandinavian Foundation, 1916) | sacred-texts.com transcription | Prologue, Gylfaginning, Skáldskaparmál (Brodeur omitted Háttatal) |
| Old Norse (`on`), poems | *Eddukvæði* | Guðni Jónsson's normalised edition (Íslendingasagnaútgáfan, 1949) as published by heimskringla.no | heimskringla.no pages, fetched 2026-10-25 | all 45 poems |
| English (`en`), poems | *The Poetic Edda* | Henry Adams Bellows (American-Scandinavian Foundation, 1923) | English Wikisource, *The Poetic Edda (tr. Bellows)*, MediaWiki API | 36 of the 45 poems (his 35 pages; Svipdagsmol and Hyndluljoth each cover two of Guðni Jónsson's poems, Fra Dautha Sinfjotla joins Grípisspá) |

| Modern Icelandic (`is`), poems | Hávamál, Völuspá, Þrymskviða, Völundarkviða, Helgakviða Hundingsbana II | Netútgáfan, 1996–1997 | https://netutgafan.snerpa.is/kvaedi/, fetched 2026-11-01 | 359 rows of these five poems; the other poems carry an automatic modernisation |
| English (`en`), poems | *Edda Sæmundar hinns Fróða* | Benjamin Thorpe (Trübner, 1866) | germanicmythology.com transcription | Sólarljóð and Hrafnagaldr Óðins (108 rows), which Bellows did not translate |

Further English versions stand beside the default English column (`aligned/texts.json`, `sources/versions/`):

| Version | Text | Where from | Rows |
| --- | --- | --- | --- |
| `en-anderson` | Rasmus B. Anderson, *The Younger Edda* (1880), public domain | English Wikisource, proofread transcription | 335, Gylfaginning |
| `en-thorpe` | Benjamin Thorpe, *The Edda of Sæmund the Learned* (1866; the Norrœna reprint of 1907), public domain | English Wikisource, proofread transcription | 1,474, 33 poems |
| `en-modern` | Open Edda's modernisation of the public-domain English (Brodeur, Bellows, Thorpe): an AI draft, not reviewed, CC BY 4.0 | made for this edition | 2,890, everything except Háttatal and the rows whose English is only an AI draft |

Details per file, fetch dates and known defects: `sources/README.md`. The Wikisource proofread copy of
Brodeur is the planned cleaner base for the English column (see `docs/ROADMAP.md`).

## What is in the rows

| Part | Chapters | Rows | Old Norse | Icelandic | English |
| --- | --- | --- | --- | --- | --- |
| Formáli (Prologue) | 5 | 12 | Guðni Jónsson 1954 | automatic modernisation | Brodeur 1916 |
| Gylfaginning | 54 | 345 | Guðni Jónsson 1954 | Netútgáfan 1997 | Brodeur 1916 |
| Skáldskaparmál | 89 | 854 | Guðni Jónsson 1954 | automatic modernisation | Brodeur 1916 (his 74 chapters mapped onto 89) |
| Háttatal | 3 sections, 102 stanzas | 303 | Guðni Jónsson 1954 | automatic modernisation | AI draft, unreviewed |
| *Poetic Edda* | 45 poems in 3 groups (17 mythological, 20 heroic, 8 other) | 1,952 (stanzas, prose passages, unnumbered verse) | Guðni Jónsson 1949 | Netútgáfan 1996–1997 for five poems (359 rows); automatic modernisation elsewhere | Bellows 1923 for 36 poems (1,586 rows); Thorpe 1866 for two (108); Brodeur for 2 stanzas Snorri quotes; AI draft (marked) for 248 rows: the seven poems neither translated and the stanzas Bellows left out |

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

- **English for the poems** without a public-domain translation (248 rows) is an AI draft of the same kind.
- **English · modern** (`en-modern`, 2,891 rows) is an AI modernisation of the public-domain translations; it keeps
  the translators' readings, gives the names in their original form (Mímisbrunnr, not "Mímir's Well") and has not
  been reviewed.
- **The names index** (`entities/`: 686 names, 29,124 mentions in all columns, 6,840 of them in the Old Norse) is
  detected automatically from a curated list; 108 name marks have been checked by a person (`reviews/mentions.json`);
  the summaries are AI drafts. **The Mímir guide** (`guide/`: 426 cards, 40 stories) is an AI draft checked by AI
  against the rows; its Icelandic is an AI translation; it has not been reviewed by a person yet.

Nothing automatic is presented as settled: every cell has an origin (`edition`, `published`, `machine`, `ai`,
`contributor`) and a check state (`aligned-auto`, `aligned-checked`, `unreviewed`, `reviewed`, `disputed`), see
`docs/DATA_MODEL.md` and the current counts in `docs/STATUS.md`.

## Layout

```
sources/      the base texts as fetched (txt/html) and their parsed JSON — immutable
  on/         Guðni Jónsson: prologus.txt, gylfaginning.txt, skaaldskaparmaal.txt, haattatal.txtl; on_{prol,gylf,skald,hatt}.json
  on/eddukvaedi/  gj_eddukvaedi.json — the 45 poems as fetched from heimskringla.no (page text per poem)
  is/         Netútgáfan: gylf_is.html, is_gylf.json; netutgafan/ — the five poems
  en/         Brodeur: brodeur_{prologue,gylf,skald}.html, en_{prol,gylf,skald}.json; bellows/, thorpe/ (the two poems),
              anderson/ and thorpe-ws/ (the Wikisource pages behind the versions)
  versions/   the further versions as placed on the rows: en-anderson/, en-thorpe/, en-modern/
aligned/      al_{prol,gylf,skald,hatt}.json — Snorri's rows; poetic/al_<poem>.json, index.json, links.json — the poems
              and Snorri's quotations of them; titles.json, sources.json (where each column comes from), texts.json
              (the versions). GENERATED by edda-site, never hand-edited
auto/         modernizer.json (learned tables), is_{prol,skald,hatt}_auto.json, en_draft.json and poetic_drafts/
              (AI drafts, as produced), titles_en.json (AI draft English titles)
overlays/     human (and labelled AI) changes keyed by row id and cell: overlays/{on,is,en}/*.json
reviews/      review-mode marks exported from the site: marks.json and the verdicts on names, mentions, pictures, titles
entities/     the names index: entities.json, mentions.json, summaries.json, places, img/ (pictures at 480 px)
guide/        the Mímir guide: cards, sections, stories, ages, relations, misconceptions, tours, pronunciation
intros/       an introduction per part and a headnote per poem
paths/        the reading paths of the Start here page
images/       records.json and pd/ (public-domain illustrations per chapter), scenes.json (briefs); plates/, tiles/,
              portraits/, mimir/, ravens/, worlds/ — Open Edda's own pictures (images/README.md)
scripts/      validate.py (checks everything, prints the status table) and small generators
docs/         DATA_MODEL.md, STATUS.md, ROADMAP.md
```

## Validate

```
python -I scripts/validate.py
```

Standard library only, Python 3.11+. Exits non-zero on any structural error and prints the status table
(rows per part and column by status).

## How to cite

Releases are tagged (`0.1.0`, 2026-11-18, is the first public release). A DOI will follow; until then cite the
version tag and the repository address.

> Sapunov, G. (2026). *Open Edda: a parallel Old Norse – Icelandic – English dataset of Snorri's Edda and the Poetic Edda* (0.1.0).
> https://github.com/parallel-classics/edda-data

Machine-readable citation: `CITATION.cff`. Please also credit the source editions named above
(heimskringla.no asks to be credited for the Guðni Jónsson text).

## Licences

- The medieval texts and the four English translations are in the public domain; the rights in Guðni
  Jónsson's normalised editions and in Netútgáfan's text are being confirmed (`LICENSE`, section 1).
- Everything Open Edda adds (the alignment, the automatic modern spelling, the AI-draft and modern English, the
  names index, the Mímir guide, introductions, review and overlay records, the plates, portraits and map) is
  licensed **CC BY 4.0** (`LICENSE`, section 2; decision 2026-11-16). Credit "Open Edda, openedda.is" and the
  contributor where a record names one. The licence covers only what Open Edda added.
- Contributors are credited per row (the `author` field of each overlay record) and on a contributors page.
- Code in this repository (`scripts/`) is MIT, like edda-site.

## How to contribute

The main route is the website: sign in on [openedda.is](https://openedda.is/help/), switch on Suggest, click a
cell, fix it and give a reason. Reviewers look at each suggestion, and the accepted ones come into this
repository as overlay records with the next release of the data. No git is needed.

If you prefer git: open a pull request that adds overlay records, or open an issue with the `row-problem`
template (`.github/ISSUE_TEMPLATE/row-problem.md`). Rules, roles and statuses, and what must never be committed
to this public repository: `CONTRIBUTING.md`.

## Status summary

As of 2026-11-24: 3,466 rows (Snorri 1,514, poems 1,952). 167 cells have been checked by a person, all in
Gylfaginning: in 166 the placement of a published translation was confirmed, 1 text was reviewed. Everything else is
automatic or draft. `docs/STATUS.md` has the tables of release 0.1.0.

## Contact

Maintainer: Grigory Sapunov (see the GitHub profile of the repository owner). Takedown or licence questions
go to the same address or to an issue.
