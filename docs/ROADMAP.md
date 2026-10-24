# Roadmap (data repository view)

Phases from the project plan, trimmed to what concerns edda-data. The gates, not the dates, decide when a
phase is over. Phases 2, 3 and 4 run side by side. Site and edit-service work is tracked in edda-site.

| Phase | What changes in edda-data | Gate |
| --- | --- | --- |
| 0 Foundation (2 weeks) | Repository public; `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md` (IS + EN); validator in CI on every PR; issue template for row problems; tag `v0.1.0`; Zenodo archive and DOI; `README.md` cites it | v0.1 tagged with DOI; site live |
| 1 Edit service (4 weeks) | First bot pull requests from the edit service (one PR per day per language, reviewer named in the commit); overlay files for Formáli from dogfooding (12 rows); the Háttatal AI draft published as *draft — AI* (already in `overlays/en/`); CI validates status transitions | 3 reviewers active; 100 edits merged through the bot |
| 2 Icelandic outreach (12 weeks) | Icelandic overlays arrive for Formáli, then Skáldskaparmál; monthly moderniser retraining from accepted fixes, `auto/` and `aligned/` regenerated, accuracy reported in `docs/STATUS.md`; a tagged release per month | Formáli 100% reviewed; Skáldskaparmál Icelandic 50% reviewed |
| 3 Images (11 weeks) | `images/records.json` filled: the 42 briefs' public-domain candidates verified against institution records; community-track schema added when the track opens | 30 slots with a verified public-domain image |
| 4 English (19 weeks) | Háttatal draft reviewed row by row (overlays → `reviewed`); Brodeur base swapped to the Wikisource proofread copy (new `sources/en/`, re-aligned rows, ids preserved or suffixed); new-translation overlays start on Gylfaginning; glossary file added | Háttatal English reviewed on every row |
| 5 Scholarly release | `v1.0.0` frozen, tagged, DOI; contributors listed in the release; description paper; scope the next phase (Uppsala Edda variants, þulur) | v1.0 published and cited |

## Rules that hold through every phase

- Sources immutable; corrections are overlays; row ids never change (suffix on split).
- Every release: `CHANGELOG.md`, `CITATION.cff` version and date, `docs/STATUS.md` refreshed from the
  validator, tag, Zenodo.
- A regenerated `aligned/` (re-alignment, retrained moderniser, new Brodeur base) is a pull request from
  edda-site with the row-id diff stated in its description; reviewed overlays must still resolve.

## Open decisions affecting this repository

- Licence for contributions: CC BY 4.0 (current) or CC0.
- Whether a free modern-spelling Skáldskaparmál exists anywhere (it would replace the automatic column).
- How to treat Brodeur's bracketed "spurious" passages in a new translation.
- Whether to add the Uppsala Edda as a fourth text after v1.0.
