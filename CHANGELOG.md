# Changelog

All notable changes to the dataset. Versions are git tags; releases are archived on Zenodo.

## Unreleased

- Poetic Edda, complete: the 45 poems of Guðni Jónsson's *Eddukvæði* (heimskringla.no, fetched 2026-10-25;
  `sources/on/eddukvaedi/`) as 1,966 rows in `aligned/poetic/al_<poem>.json` (ids `<poem>-s<N>`, `<poem>-p<k>`),
  automatic modern Icelandic, Bellows 1923 for the 36 poems he translated (`sources/en/bellows/`, Wikisource),
  his notes and introductions; `aligned/poetic/index.json` (order, groups), `links.json` (91 Snorri quotations).
  Völuspá keeps its ids and hand pairing; `aligned/al_vsp.json` and `links_vsp.json` are replaced by the
  poetic folder.
- `aligned/titles.json`: chapter and poem titles in Old Norse, automatic Icelandic and AI-draft English
  (`auto/titles_en.json`).
- Columns generalised to a list of languages (data model, validator); `ru`, `nb`, `nn`, `da`, `sv`, `de`
  reserved.
- Licence wording corrected: Guðni Jónsson's normalised editions and Netútgáfan's text are no longer described
  as public domain; their status is being confirmed (`LICENSE` §1).
- Validator: poem files, links, titles, any language column.

## 0.1.0 — 2026-10-24 — initial import

- Sources fetched 2026-10-23: Guðni Jónsson 1954 Old Norse (heimskringla.no via the CLTK mirror), Netútgáfan
  1997 Gylfaginning, Brodeur 1916 (sacred-texts transcription, scan errors fixed by hand, *œ* restored).
- Aligned rows for all four parts: Formáli 5 chapters / 12 rows; Gylfaginning 54 / 345; Skáldskaparmál 89 / 854
  (Brodeur's 74 chapters mapped onto 89); Háttatal 3 sections, 102 stanzas / 303 rows. Total 1,514 rows.
- Automatic modernised spelling for Formáli, Skáldskaparmál and Háttatal (`auto/is_*_auto.json`) from the
  learned tables in `auto/modernizer.json` (5-fold held-out token accuracy on Gylfaginning 94.1%).
- AI draft English for Háttatal (303 rows) and Skáldskaparmál row `s-c72-8`, as overlays with status `draft`
  (`overlays/en/hattatal-ai-draft.json`, `overlays/en/skaldskaparmal-ai-draft.json`); the draft as produced
  is kept in `auto/en_draft.json`.
- 42 illustration briefs in `images/scenes.json`; 40 public-domain images mapped in `images/records.json` (Wikimedia Commons provenance, licence basis, alternatives; human check pending; 38 placed, 2 kept as candidates only) with 1280 px copies in `images/pd/` (re-encoded JPEG, quality 0.78; originals via `file_url`).
- Twelve image-generation briefs (track 2) in `images/generation-briefs.{json,md}`: style prefix, scene prompt, avoid list, must-show checklist.
- Validator `scripts/validate.py`; documentation in `docs/`.
- Status: 0 reviewed cells; everything is `source` (Old Norse), `auto` or `draft`.
