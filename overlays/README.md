# overlays/ — human changes on top of the generated rows

The sources and the aligned rows are never edited. Every change a person (or a labelled AI run) makes to a
cell is a record here, keyed by row id and cell. The build applies these records on top of `aligned/`,
so re-running the aligner or retraining the moderniser never loses human work.

```
overlays/
  on/   changes to the Old Norse column (typographical fixes to the base edition only; two reviewers)
  is/   changes to the modern Icelandic column
  en/   changes to the English column (hattatal-ai-draft.json and skaldskaparmal-ai-draft.json are here)
```

Files are grouped per part and origin (`<part>.json`, `<part>-ai-draft.json`, `<part>-<campaign>.json`); the
folder name must equal the `cell` of every record inside. Any number of files per folder is allowed.

## File shape

```json
{
 "_note": "free text about this file",
 "records": [
  {
   "row": "g-c35-5",
   "cell": "is",
   "text": "Fimmta er Fulla. Hún er enn mær …",
   "origin": "contributor",
   "check": "reviewed",
   "status": "reviewed",
   "author": "user:123",
   "date": "2026-11-02",
   "reason": "inflection",
   "replaces": "auto:v3"
  }
 ]
}
```

| Field | Required | Meaning |
| --- | --- | --- |
| `row` | yes | row id `<p>-c<chapter>-<row>[suffix]`; must exist in `aligned/` (a suffixed id must exist or its base id must) |
| `cell` | yes | `on`, `is` or `en`; equals the folder name |
| `text` | yes | the full new text of the cell. Prose: one paragraph. Verse: lines separated by `\n`. Non-empty. |
| `origin` | new records | `edition`, `published`, `machine`, `ai` or `contributor` — where the text comes from (docs/DATA_MODEL.md) |
| `source` | with `origin: published` | the source id from `aligned/sources.json` (`brodeur-1916`, `bellows-1923`, `netutgafan-1997`) |
| `check` | new records | for `published`: `aligned-auto`, `aligned-checked`, `disputed`; for `machine`, `ai`, `contributor`: `unreviewed`, `reviewed`, `disputed`; for `edition`: `unreviewed`, `reviewed` |
| `status` | old records (optional when `origin` and `check` are given) | the one-word form: `auto`, `draft`, `reviewed` or `disputed`; mapped to origin and check as in DATA_MODEL.md |
| `author` | yes | `user:<handle>`, `ai:<model>-<yyyy-mm>` or `bot:<name>` |
| `date` | yes | `YYYY-MM-DD` |
| `reason` | recommended | one line: what was wrong |
| `replaces` | recommended | what this record supersedes: `null` for the generated text, or an identifier of the earlier record/version (e.g. `auto:v3`, or the earlier record's `author`+`date`) |

Optional extra fields are allowed (`source`, `discussion` URL for disputes, `reviewer`), the validator
ignores them.

## Status rules

Since task 17 (2026-11-01) a record states two things: `origin` (where the text comes from) and `check` (what a
person confirmed). An alignment fix on a published translation — the sentence belongs to another row — is a record
with `origin: published`, `source`, `check: aligned-checked` and the text as it should stand in this row; a new
wording by a person is `origin: contributor`. The one-word `status` below is the old form, still accepted and
derived for every record:

- `auto` — machine output. Overlays with status `auto` exist only when a tool writes a cell on purpose
  (for example a retrained moderniser recording a per-row result); people never write `auto`.
- `draft` — an unreviewed edit by a person, or an AI translation (author `ai:…`). Visible to the author and
  to reviewers; not shown to the public as the reading text.
- `reviewed` — accepted by a reviewer with the right role for that language. Only reviewers set it.
  The Old Norse column needs two reviewers.
- `disputed` — two reviewers disagree. The page shows both readings and the discussion link.

Transitions: `auto → draft → reviewed`, `reviewed → disputed → reviewed`, `draft → disputed`. A record never
goes back to `auto`.

## Resolution: which record wins

For each (row, cell), in file order then record order: the latest `reviewed` record is the reading text; if
there is no reviewed record the generated cell from `aligned/` is shown (with the `auto`/`draft` label and
the drafts available to reviewers); if the latest record is `disputed` the cell is marked disputed and both
readings are shown. Records are never edited or deleted — add a newer one with `replaces` set.

## Validation

`python -I scripts/validate.py` checks every record (row exists, cell matches the folder, status allowed,
text non-empty, author, date format) and counts the effective status per part and column.
