# Roadmap (data repository view)

Phases from the project plan, trimmed to what concerns edda-data. The gates, not the dates, decide when a
phase is over. Phases 2, 3 and 4 run side by side. Site and edit-service work is tracked in edda-site.

| Phase | What changes in edda-data | Gate |
| --- | --- | --- |
| 0 Foundation (2 weeks) | Repository public; `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md` (IS + EN); validator in CI on every PR; issue template for row problems; tag `0.1.0`; Zenodo archive and DOI; `README.md` cites it | v0.1 tagged with DOI; site live |
| 1 Edit service (4 weeks) | First bot pull requests from the edit service (one PR per day per language, reviewer named in the commit); overlay files for Formáli from dogfooding (12 rows); the Háttatal AI draft published as *draft — AI* (already in `overlays/en/`); CI validates status transitions | 3 reviewers active; 100 edits merged through the bot |
| 2 Icelandic outreach (12 weeks) | Icelandic overlays arrive for Formáli, then Skáldskaparmál; monthly moderniser retraining from accepted fixes, `auto/` and `aligned/` regenerated, accuracy reported in `docs/STATUS.md`; a tagged release per month | Formáli 100% reviewed; Skáldskaparmál Icelandic 50% reviewed |
| 3 Images (11 weeks) | `images/records.json`: the 40 Commons records verified by a person against institution records; documentary images (manuscript pages, monuments, places; PD / CC0 / CC BY / CC BY-SA, see `images/README.md`) added within the density rule; community-track schema added when the track opens | 30 slots with a verified depiction; documentary strip on every part |
| 4 English (19 weeks) | Nafnaþulur added as a fifth part (`sources/on/`, `aligned/al_thul.json`; Old Norse, automatic Icelandic, English glosses); Háttatal draft reviewed row by row (overlays → `reviewed`); Brodeur base swapped to the Wikisource proofread copy (new `sources/en/`, re-aligned rows, ids preserved or suffixed); new-translation overlays start on Gylfaginning; glossary file added | Háttatal English reviewed on every row |
| Poetic Edda (alongside 2–4) | All 45 poems added 2026-10-25 (`aligned/poetic/`). Next: review the automatic stanza alignment poem by poem (worst first), English for the 9 poems Bellows left out (Thorpe 1866 where possible), image slots for the poems | the `?` rows of every poem checked; Völuspá read through by one reviewer |
| Languages (after the Icelandic and English streams are running) | A column per language: Norwegian Nynorsk (Mortensson-Egnund, poems), Russian (Sviridenko 1917, mythological poems; the rest a new CC BY-SA translation), German (Simrock), Swedish (Brate), Danish (Olaf Hansen, Thøger Larsen); each with its licence basis recorded | one new language live with its status counts in `docs/STATUS.md` |
| 5 Scholarly release | `v1.0.0` frozen, tagged, DOI; contributors listed in the release; description paper; scope the next phase (Uppsala Edda variants, þulur) | v1.0 published and cited |

## Rules that hold through every phase

- Sources immutable; corrections are overlays; row ids never change (suffix on split).
- Every release: `CHANGELOG.md`, `CITATION.cff` version and date, `docs/STATUS.md` refreshed from the
  validator, tag, Zenodo.
- A regenerated `aligned/` (re-alignment, retrained moderniser, new Brodeur base) is a pull request from
  edda-site with the row-id diff stated in its description; reviewed overlays must still resolve.

## Open decisions affecting this repository

- Rights in Guðni Jónsson's normalised editions (and Netútgáfan's text): permission from heimskringla.no, or a
  re-based Old Norse column (19th-century editions, or our own normalisation from handrit.is transcriptions).
  This blocks calling the dataset public domain, and should be settled before the DOI release.
- Whether the Poetic Edda becomes its own dataset repository or stays here (current: here, same model).

- Licence for contributions: CC BY 4.0 (current) or CC0.
- Whether a free modern-spelling Skáldskaparmál exists anywhere (it would replace the automatic column).
- How to treat Brodeur's bracketed "spurious" passages in a new translation.
- Whether to add the Uppsala Edda as a fourth text after v1.0.
- The interactive book (MCP server, cast bible, reader-side AI) is a separate project after v1.0; the only data-model addition it needs is a cast record. See the project plan.
