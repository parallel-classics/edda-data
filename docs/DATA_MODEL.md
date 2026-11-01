# Data model

The row is the unit of everything: reading, editing, reviewing, citing.

## Parts and ids

| Prefix | Part | Aligned file | Chapters |
| --- | --- | --- | --- |
| `p` | Formáli (Prologue) | `aligned/al_prol.json` | 1–5 |
| `g` | Gylfaginning | `aligned/al_gylf.json` | 1–54 |
| `s` | Skáldskaparmál | `aligned/al_skald.json` | 1–89 (Guðni Jónsson's division; Brodeur's 74 mapped onto them) |
| `h` | Háttatal | `aligned/al_hatt.json` | sections 1–3 (stanzas 1–30, 31–67, 68–102) |
| `<poem>` | the 45 poems of the Poetic Edda (`vsp`, `hav`, `vm`, `grm`, …; list in `aligned/poetic/index.json`) | `aligned/poetic/al_<poem>.json` | one chapter per poem |

Row id: `<prefix>-c<chapter>-<row>`, row 1-based within the chapter, e.g. `s-c11-4`. Chapter id on the page:
`<prefix>-ch<chapter>`. Ids are the stable reference for citing, reporting and editing.

Poems of the Poetic Edda are a second book on the same model. A poem row is one stanza, id
`<poem>-s<N>` with Guðni Jónsson's stanza number (`vsp-s19`, *Ask veit ek standa*), one prose passage,
`<poem>-p<k>` (the k-th in the poem), or one verse passage without a stanza number, `<poem>-v<k>`. Poem prefixes are short, lowercase, unique and never single letters
(those are Snorri's): `vsp hav vm grm skm hrbl hym ls thrk alv bdr rth hdl vsk grt grg fjm vkv hhv hh1 hh2
grp rm fm sd br gdr1 sg hlr drn gdr2 gdr3 od akv am ghv hm hjk hvk hlk hrl heid ebr sol fsl`.

Cross-references: `aligned/poetic/links.json` lists `{"row": <Snorri row id>, "poem_row": <poem row id>,
"lines": <k>}` for every verse block in Snorri's Edda that quotes a stanza (line matching, at least two lines
and one line unique to that stanza). The build links both rows to each other; the validator checks both ends.

## Languages (columns)

A row's cells are keyed by language code: `on` Old Norse (the pivot, never empty), `is` modern Icelandic,
`en` English, and in future `ru`, `nb`, `nn`, `da`, `sv`, `de` (the list is `LANGS` in edda-site
`pipeline/build2.py` and `LANG_CODES` in `scripts/validate.py`; add a code to both). Every cell is a list of
blocks; `<code>_cont` marks "included in the previous row"; overlays address a cell by the same code
(`overlays/<code>/…`). A part shows the columns that have text in it. Titles of chapters and poems per
language are in `aligned/titles.json`, with a status per language (`auto`, `draft`, `reviewed`).

## Blocks

A block is the smallest text unit: a prose paragraph `{"t": "p", "s": "…"}` or a stanza
`{"t": "v", "n": <number or null>, "l": ["line", …]}`. Sources (`sources/*/*.json`, `auto/is_*_auto.json`)
are `{"title", "chapters": [{"num", "title", "blocks": [...]}]}`.

## Rows

A row is one Old Norse block with its counterparts. `aligned/README.md` gives the exact shape; in short:

- `on` — one block, never empty (the pivot).
- `is` — Netútgáfan's sentences aligned to the block (Gylfaginning), or the automatic modernisation of the
  block (other parts). May be empty with `is_cont` true ("included in the previous row").
- `en` — Brodeur's sentences aligned to the block; empty with `en_cont` true, or empty when Brodeur has no
  counterpart; an AI draft when `en_draft` is true.
- `s_en`, `s_is` — alignment confidence per column (bead score; `null` when unaligned).

## Overlays

A record is one change to one cell of one row (schema and rules in `overlays/README.md`):

```json
{"row": "g-c35-5", "cell": "is", "text": "Fimmta er Fulla. Hún er enn mær …", "status": "reviewed",
 "author": "user:123", "date": "2026-11-02", "reason": "inflection", "replaces": "auto:v3"}
```

Records are append-only. Files live in `overlays/<cell>/`. Author forms: `user:<handle>`,
`ai:<model>-<yyyy-mm>`, `bot:<name>`.

## Statuses

Every cell has exactly one effective status:

| Status | Set by | Meaning |
| --- | --- | --- |
| `auto` | the pipeline (implicit for generated cells) | machine output: automatic alignment of a published text, or automatic modernised spelling |
| `draft` | contributors, AI runs | an unreviewed edit, or an AI translation (always labelled as AI on the page) |
| `reviewed` | reviewers with the role for that language | accepted; the reading text |
| `disputed` | reviewers | two reviewers disagree; both readings shown with a discussion link |

The Old Norse column is the base edition and is counted as `source` in status tables (it is not machine
output and not under review except for typographical overlays, which need two reviewers). Status is shown on
the page, in the data and in exports; nothing automatic is ever presented as reviewed.

Base status of a generated cell when no overlay exists: `on` → `source`; `is`/`en` with text → `auto`;
`en` with `en_draft` → `draft`; no text → `empty`.

## How the build applies overlays

For each (row, cell), records are read in file order, then record order within a file:

1. If any record is `disputed` and no later `reviewed` record resolves it, the cell is **disputed**: the page
   shows the generated/previous reading and the disputed reading side by side with the discussion link.
2. Otherwise the **latest `reviewed` record wins** and is the reading text; the cell shows the reviewed
   badge and the author on hover.
3. Otherwise the generated cell from `aligned/` is shown with its `auto` label (or `draft`/AI label when the
   only records are drafts or the generated cell is an AI draft); drafts are listed for reviewers.

The build never writes into `aligned/`; re-running the aligner or the moderniser replaces `aligned/` and
`auto/` but leaves `overlays/` untouched, so reviewed text survives every rebuild. The site build applies the
rule in `edda-site/pipeline/overlays.py` (since 2026-11-01); the AI-draft cells are read from their overlay
records (`overlays/en/*-ai-draft.json`), the `en_draft` copies in `aligned/` only mark the cell as a draft.
Overlay text: blocks separated by a blank line, verse lines by `\n`; a one-line segment facing an Old Norse
verse block is a one-line verse.

## Id stability

- A row id never changes once published.
- If a base text is re-parsed and a block splits, the new rows get letter suffixes (`s-c11-4a`, `s-c11-4b`);
  the old id `s-c11-4` keeps resolving (to the first piece, with a note). Overlays on the old id stay valid.
- If two blocks merge, the merged row keeps the first id; the second id resolves to it.
- Chapter numbers follow Guðni Jónsson and do not change; a new base edition with a different division would
  be a new part key, not a renumbering.
- Overlays for a suffixed id are accepted by the validator when either the suffixed id or its base exists.

## Images

`images/scenes.json` (briefs per chapter) and `images/records.json` (verified public-domain images with
`part`, `chapter`, `scene_rows`, credit and licence fields) — schema in `images/README.md`.

## Entities (names)

`entities/` holds the names of the Eddas keyed to Wikidata: a curated `seed.json`, hand `rules.json` and
`notable.json`, and the generated `entities.json` (one record per entity, with `tags`, names per language,
image, first mentions per book) and `mentions.json` (one record per mention: entity, row id, `lang`, the form as
written, kind `name` / `heiti` / `kenning`, `check` when ambiguous). Shapes and the tag vocabulary in
`entities/README.md`; the feature in `edda-site/docs/specs/ENTITIES.md`. Everything there is status `auto`.
Entity ids are stable like row ids; corrections will be overlay records (shape to be defined with task 16b).

## Validation

`python -I scripts/validate.py` enforces: every row has Old Norse; ids unique; every overlay record points at
an existing row and a known cell with an allowed status, non-empty text, author and date; image records point
at existing chapters and rows; scene briefs point at existing chapters. It prints the status table used in
`docs/STATUS.md`.
