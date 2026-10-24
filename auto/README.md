# auto/ — machine output, versioned

| File | What | Produced by |
| --- | --- | --- |
| `modernizer.json` | the learned Old Norse → modern-spelling tables: `word` (4,116 exact-case mappings), `lower` (3,886 lowercase mappings), `suffix` (1,637 suffix rules, identity rules included), `stats` | `edda-site/pipeline/modernize.py train aligned/al_gylf.json auto/modernizer.json` |
| `is_prol_auto.json`, `is_skald_auto.json`, `is_hatt_auto.json` | automatic modernisation of the Old Norse of Formáli, Skáldskaparmál, Háttatal; same block structure as `sources/on/on_*.json` | `modernize.py apply auto/modernizer.json sources/on/on_<part>.json auto/is_<part>_auto.json` |
| `en_draft.json` | the AI draft English as produced: `{"note", "rows": {row_id: text}}`, 304 rows (303 Háttatal + `s-c72-8`); verse lines separated by `\n`; `[?]` = uncertain rendering (32 rows) | an LLM run in October 2026 (`ai:claude-2026-10`) over `trans/hatt_sec{1,2,3}.json` in the working bundle, merged by `integrate_drafts.py` |

## The moderniser

A word dictionary plus suffix rules learned from the Gylfaginning pair (Guðni Jónsson ↔ Netútgáfan), token
by token after a monotone edit-distance alignment. At apply time a token is looked up exactly, then
lowercased, then by its longest matching suffix (an *identity* suffix rule means "keep the word"); unknown
tokens are left unchanged.

Accuracy, five-fold cross-validation by chapter on Gylfaginning (`modernize.py eval`):
**94.1% of tokens correct**, against **71.6%** if the Old Norse is left unchanged. Typical residuals:
*it fyrsta* for *hið fyrsta*, occasional inflection endings, rare words never seen in Gylfaginning.

Retraining (planned monthly once corrections arrive): every accepted Icelandic overlay is a new training
pair; retrain with `modernize.py train`, re-apply to the three parts, re-run the aligner for those parts,
report the held-out accuracy in `docs/STATUS.md`. A retrain changes `auto/` and `aligned/` but never an
overlay, so reviewed cells survive.

## The AI draft

Status `draft`, never `reviewed`, until a human reviewer changes or explicitly accepts each row. The
canonical form for the build is the overlay files `overlays/en/hattatal-ai-draft.json` and
`overlays/en/skaldskaparmal-ai-draft.json` (generated from this file by `scripts/drafts_to_overlays.py`);
`en_draft.json` is kept here unchanged for traceability.
