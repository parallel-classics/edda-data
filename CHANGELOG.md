# Changelog

All notable changes to the dataset. Versions are git tags; releases are archived on Zenodo.

## 0.1.0 — 2026-11-18 — first public release

Tag `0.1.0`. The repository was made public on this date. Everything below, down to the initial import, is part
of this release.

- After the tag (2026-11-18): README, `sources/README.md`, `aligned/README.md`, `docs/STATUS.md`, `LICENSE` §1 and
  the other documents brought up to date with the data (versions, Netútgáfan's poems, names and guide counts);
  `scripts/validate.py` now reads the row flags `is_netutgafan` and `en_thorpe`, so the status table counts the 359
  Netútgáfan poem rows as published text, not as automatic spelling.
- Versions of a language (2026-11-07): `aligned/texts.json`; `en-anderson` (Anderson 1880, Gylfaginning, 335 rows) and
  `en-thorpe` (Thorpe 1866, 33 poems, 1,464 rows), both from the proofread Wikisource transcriptions and placed
  automatically; `en-modern` replaces the pilot column `em`.

- Icelandic for Mímir and the Names summaries (2026-11-14): every English string in `guide/` (cards, stories,
  myths, outside, sections, paths, ages, relation notes; 4,876 values) and the 587 summaries in `entities/summaries.json` now has an
  `is` value beside `en`: an AI translation by Claude, a draft, not reviewed by a person. Names are in their modern
  Icelandic forms. Where the English quotes a line of the Eddas the Icelandic is a translation of the sense or a
  wording recalled by the translator, not yet checked against the Icelandic text of this edition.
- English · modern, complete where a public-domain English exists (task 31, 2026-11-14): Open Edda's AI modernisation
  now covers the Formáli (12 rows), Gylfaginning (340), Skáldskaparmál (843) and the poems (1,695), 2,890 rows in
  `sources/versions/en-modern/` (gylf_1-10, gylf_11-54, prol, skald, poems), placed as the version `en-modern`.
  From Brodeur 1916 for Snorri, Bellows 1923 and Thorpe 1866 for the poems; the translators' readings and name
  spellings are kept, footnote markers dropped, evident transcription errors in the sources corrected; CC BY 4.0,
  AI draft, not reviewed. Háttatal and the rows whose English is only an AI draft are not included. The source
  `oe-modern-brodeur` keeps its id; its label now names all three translators.

- Mímir pictures (task 34): Grigory Sapunov's plates P1-P4 and the Mímir picture (© 2026, CC BY 4.0) with their
  anchors; web sizes, a crop per figure and the social card from edda-site `pipeline/make_plates.py`. The validator
  checks the anchors (picture present, entities exist, boxes inside, part_of, stories).
- Mímir (task 34), content pass 3: 331 cards (115 short ones), every link between two cards both ways, one entry per
  neighbour (`also` for further kinds), sections with `more`. Old Norse names (`names.on`) for 34 entities whose
  title fell back to an inflected form (Vé, Miðgarðr, Jörð, Ullr …). The validator checks `also`, sections and link-backs.
- Mímir (task 34), content pass 2: 40 stories (16 new, age 3 now has its own), 5 paths, cards list every story they
  take part in.
- Mímir (task 34), content: `guide/` now holds the cloud session's first full pass — 216 cards, 18 sections, 24 stories,
  8 ages and the heroes' line, 344 relations, 2 paths, 18 misconceptions, 14 outside entries. AI draft, fact-checked
  by AI against the rows, not reviewed by a person. The validator follows its format (objects keyed by id) and checks
  fact chips, story and myth links, outside kinds and the relation kinds.

- Mímir (task 34), pilot: `guide/` with a small sample (Óðinn and Þórr, two stories, the eight ages, a path, two
  outside sources, two myths) for the pages until the cloud session's content replaces it; AI draft, not reviewed.
  The validator checks `guide/`: refs are row ids, entities exist, every story step has a passage, symmetric relations.

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
  Switched on 2026-11-16: 359 rows show Netútgáfan's text (`is_netutgafan`), ten keep the automatic text.
- Names (curator's answers of 2026-11-01): Old Norse headwords set with `names.on` where the label was
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

## Initial import — 2026-10-24 (before the first tag)

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
