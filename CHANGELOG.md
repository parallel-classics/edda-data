# Changelog

All notable changes to the dataset. Versions are git tags; releases are archived on Zenodo.

## Unreleased

- Map of the worlds, background v4 (2026-11-08): the grazing stag (Dáinn) redrawn whole; anchors unchanged.
- Names: summaries for the minor entities (`entities/summaries.json`, AI drafts, not reviewed): 321 more, for the
  entities with 1-4 Old Norse mentions (67 with 4, 82 with 3, 120 with 2, 52 with 1), one short paragraph each citing
  this edition's rows; 587 of 598 entities now have one. 11 left out because the index entry mixes different figures
  or is a false match (listed in the pull request for a rules fix).
- English · modern (pilot): Open Edda's AI modernisation of Brodeur's Gylfaginning 1-10, CC BY 4.0, not reviewed
  (sources/en/modern/gylf_1-10.json, placed as the column `em` by edda-site/pipeline/fill_modern.py; source
  oe-modern-brodeur in aligned/sources.json). The validator knows the column `em`.

- First review-mode export (2026-11-07, edda-site/tools/export_reviews.py): Gylfaginning 1.1 checked in all three
  columns (overlays/*/review-grigory.json); the picture of Bragi confirmed (reviews/pictures.json); reviews/marks.json
  keeps every exported mark.
- Map of the worlds: the background's credit is "© 2026 Grigory Sapunov", licence CC BY 4.0 (was CC0 and an
  AI-generated label); the Gemini provenance stays in the records (`made_with`), not on the page.
  scripts/validate.py checks for `made_with` and the licence instead of the old `ai_generated` flag.
- Icelandic of Hávamál, Völuspá, Þrymskviða, Völundarkviða and Helgakviða Hundingsbana II: Netútgáfan's modern-spelling
  text (`sources/is/netutgafan/`, 🟡 until the notification email) placed on Guðni Jónsson's rows as `is_nu` (prepared,
  not shown; 365 of 369 rows, four keep the automatic text); `fill_netutgafan.py --switch` turns it into the column.
- Names (curator's answers of 2026-11-01, mailbox 2320): Old Norse headwords set with `names.on` where the label was
  inflected or modern (Þórr, Bölþorn, Niflheimr, Andvaranautr, Garðrofa, Niðafjöll, Svartálfaheimr, Þrúðheimr, Angrboða,
  Glaðsheimr, Gullveig, Hlóra, Náströnd, Ymir, Surtr, Suttungr, Iðavöllr); Ífingr added (river, Vafþrúðnismál 16);
  `thjodolfr-arnorsson` dropped (no mentions); `curated.txt` marked superseded by seed.json. Entities regenerated.
- English of Sólarljóð and Hrafnagaldr Óðins (Forspjallsljóð): Benjamin Thorpe's translation (1866, public domain)
  replaces the AI drafts (`sources/en/thorpe/`, source `thorpe-1866`, row flag `en_thorpe`; 82 + 26 stanzas paired by
  number; Thorpe's notes as the poems' notes; the 108 AI-draft overlay records marked `withdrawn`). Thorpe did not
  translate Gróttasöngr. Overlay records may carry `withdrawn` (ignored, kept as history).
- Names: the curator's seed patch of 2026-11-01 applied (`entities/seed.json`, `rules.json`, `places.json`): 54 entities
  added or completed for the recall gap (Þrymr, Nótt, Dagr, Fulla, Baugi, Logi, Hugi, Elli, Geri, Gramr, Greip, Vanir,
  Dökkálfar, the Rígsþula family, the sky dwarves, horses, rivers, …), forms added to 20 entities, Högni split into
  Gjúkason / father of Hildr / father of Sigrún, Óttarr merged into `ottar`, Grímnir folded into Óðinn's heiti, Buðla
  and Hjaðningar moved, Þóru/Þóri dropped from Þórr, Wikidata ids for the rule-made entities, tag `person` (persóna)
  replaces the placeholder `character` and `other` is added (46 tag overrides), Sköll's headword fixed. Places:
  Francia and Old Saxony as hand points (approximate), Asia and Gotland without a marker. Regenerated: entities 598
  (was 553), Old Norse mentions 6182 (was 5900), flagged `check` 137 (was 141); recall on the 200-token sample 85% (was
  81%). Wikidata labels lose their disambiguators ("Forseti (norræn goðafræði)") and the nnwiki "Gudinna" prefix.
  Validator: tag vocabulary updated, `skip` allowed as an entity-rule target.

- Automatic Icelandic of Formáli, Skáldskaparmál and Háttatal regenerated with the guarded moderniser (edda-site
  task 12, 2026-11-01): `auto/is_{prol,skald,hatt}_auto.json` and the `is` cells of `aligned/al_{prol,skald,hatt}.json`;
  11 cells change (`konar` no longer becomes `allskonar`, `men` no longer `en`, `byggðir` no longer `ásabyggðir`,
  `gullhjálminn` and `ormarnir` keep their endings), every row id and every other cell unchanged; held-out accuracy
  94.15% (`modernize.py eval`). The AI-draft English cells were re-applied from `auto/en_draft.json` unchanged.

- Poetic Edda, complete: the 45 poems of Guðni Jónsson's *Eddukvæði* (heimskringla.no, fetched 2026-10-25;
  `sources/on/eddukvaedi/`) as 1,966 rows in `aligned/poetic/al_<poem>.json` (ids `<poem>-s<N>`, `<poem>-p<k>`),
  automatic modern Icelandic, Bellows 1923 for the 36 poems he translated (`sources/en/bellows/`, Wikisource),
  his notes and introductions; `aligned/poetic/index.json` (order, groups), `links.json` (91 Snorri quotations).
  Völuspá keeps its ids and hand pairing; `aligned/al_vsp.json` and `links_vsp.json` are replaced by the
  poetic folder.
- English for every Poetic Edda row: Brodeur where Snorri quotes the stanza, otherwise an AI draft (359 rows,
  `overlays/en/poetic-ai-draft.json`, `auto/poetic_drafts/`), for the nine poems Bellows did not translate and the
  stanzas he left out. Verse without a stanza number gets ids `<poem>-v<k>` (Eddubrot, and one passage each in
  Sigrdrífumál and Hlöðskviða).
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
