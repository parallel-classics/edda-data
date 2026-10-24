# Changelog

All notable changes to the dataset. Versions are git tags; releases are archived on Zenodo.

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
- 42 illustration briefs in `images/scenes.json`; 40 public-domain images mapped in `images/records.json` (Wikimedia Commons provenance, licence basis, alternatives; human check pending) with 1280 px copies in `images/pd/` (re-encoded JPEG, quality 0.78; originals via `file_url`).
- Validator `scripts/validate.py`; documentation in `docs/`.
- Status: 0 reviewed cells; everything is `source` (Old Norse), `auto` or `draft`.
