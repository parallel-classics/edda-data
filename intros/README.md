# intros/ — an introduction per part and a headnote per poem (task 22)

`intros.json`: `parts` keyed by part key (`p g s h pm ph po`), each with `title`, `intro` and `note` ("how to read
it") in `en` and `is`; `poems` keyed by poem prefix (the 45 of `aligned/poetic/`), each with a one-sentence
`headnote` in `en` and `is`. Every record carries `status` (`draft` until a person reviews it), `author` per
language (`ai:<model>-<yyyy-mm>` for drafts) and `date`. The English drafts are by the cloud session, the
Icelandic by Claude Code, both 2026-11-01; the page shows them with the AI-draft mark until reviewed.
Corrections are overlay records keyed `intro:<key>` / `headnote:<prefix>` (cells `intro`, `note`, `headnote`),
never edits of this file. The validator checks keys, languages, status, authors and dates.
