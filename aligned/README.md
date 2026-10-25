# aligned/ — the rows

**GENERATED. Do not hand-edit.** Snorri's four files are produced by the edda-site pipeline
(`pipeline/align2.py`, then `pipeline/integrate_drafts.py` for the draft cells). A correction to any cell is an
overlay record in `overlays/`; the build applies overlays on top of these rows. Re-running the aligner
replaces these files wholesale, so anything typed into them is lost.

| File | Part | `part` value | Row-id prefix | Chapters | Rows |
| --- | --- | --- | --- | --- | --- |
| `al_prol.json` | Formáli (Prologue) | `prologue` | `p` | 5 | 12 |
| `al_gylf.json` | Gylfaginning | `gylfaginning` | `g` | 54 | 345 |
| `al_skald.json` | Skáldskaparmál | `skaldskaparmal` | `s` | 89 | 854 |
| `al_hatt.json` | Háttatal | `hattatal` | `h` | 3 sections | 303 |
| `poetic/al_<poem>.json` | one per poem of the Poetic Edda (45) | `poetic` | the poem prefix (`vsp`, `hav`, `grm`, …) | 1 per file | 1,966 in all |
| `poetic/index.json` | poem order, prefixes, titles, groups (`myth`, `heroic`, `other`), row counts | | | | |
| `poetic/links.json` | Snorri's quotations: `{"row": "g-c4-3", "poem_row": "vsp-s3", "lines": 6}` | | | | 91 links |
| `titles.json` | chapter and poem titles per language: `{"g-ch34": {"on", "is", "en", "status": {…}}, "vsp": {…}}` | | | | 196 |

Poem files hold one chapter (the poem) with `title`, `subtitle`, `group`, `notes` (Bellows'), `intro_en`
(his introductory note), `en_source` or `en_missing_note`. Poem rows differ from Snorri rows: each carries its
own `id` (`<poem>-s<N>`, Guðni Jónsson's stanza number, `<poem>-p<k>` for the k-th prose passage, or `<poem>-v<k>` for unnumbered verse);
`stanza`; `en_stanzas` (Bellows' stanza numbers in the English cell: none, one or two); `quoted_in` (Snorri
rows that quote it); optional `head` (a heading shown above the row: Völuspá's editorial sections, Guðni
Jónsson's subtitles, Hávamál's section numerals); `s_en` only on weak automatic matches; `en_draft: true` where the English is an AI draft; `en_from: <Snorri row>`
where it is Brodeur's translation of the stanza as Snorri quotes it. A speaker line
("Loki kvað:") is a prose block with `"sp": true` inside the stanza's cell. Produced by
`edda-site/pipeline/make_poems.py`; titles by `make_titles.py`.

## File shape

```json
{
 "part": "gylfaginning",
 "title": "Hér hefr Gylfaginning",
 "chapters": [
  {
   "num": 35,
   "title": "Frá ásynjum.",
   "rows": [ { ...row... } ],
   "notes": [ {"n": 1, "s": "Brodeur's footnote text"} ],
   "en_chapters": [35],
   "en_missing": false
  }
 ],
 "chapter_beads": [[[0, 1], [0, 1]], ...]
}
```

- `chapters[].num` / `title` — Guðni Jónsson's chapter number and title (Háttatal: section 1–3, title
  "Erindi a–b" = stanza range).
- `notes` — Brodeur's bottom-of-page notes for the English chapter(s) mapped to this chapter; referenced from
  English text as `⟦n⟧`.
- `en_chapters` — Brodeur's chapter numbers that correspond to this chapter (Skáldskaparmál: 74 of his onto 89).
- `en_missing` — true when no Brodeur chapter maps here.
- `chapter_beads` — the chapter-level alignment as index ranges `[[on_from, on_to], [en_from, en_to]]`
  (0-based, half-open) into the Old Norse and English chapter lists.

## Row shape

```json
{
 "on": [ {"t": "p", "s": "Fimmta er Fulla. Hon er enn mær ..."} ],
 "is": [ {"t": "p", "s": "Fimmta er Fulla. Hún er enn mær ..."} ],
 "en": [ {"t": "p", "s": "The fifth is Fulla: she also is a maid, ..."} ],
 "is_cont": false,
 "en_cont": false,
 "s_en": 3.42,
 "s_is": 6.1
}
```

| Key | Meaning |
| --- | --- |
| `on` | exactly one block: the Old Norse paragraph (`{"t":"p","s"}`) or stanza (`{"t":"v","n","l":[lines]}`). Never empty. |
| `is` | zero or more blocks of modern Icelandic that correspond to the Old Norse block. Gylfaginning: Netútgáfan's sentences, aligned. Other parts: the automatic modernisation of the same block (always exactly one block). |
| `en` | zero or more blocks of English. Brodeur's sentences, aligned; inline `<i>…</i>` kept; `⟦n⟧` footnote references; ` \| ` inside a verse line is Brodeur's half-line division. |
| `is_cont`, `en_cont` | true when the cell is empty because the aligner put this block's counterpart into the previous row ("included in the previous row"). |
| `s_en`, `s_is` | alignment confidence: the mean dynamic-programming bead score for the Old Norse units of this block, or `null` when unaligned. Higher is better; prose rows with `s_en < -0.5` are shown with a "?" on the page. Scores are only comparable within one column. |
| `en_draft` | present and true when `en` is an AI draft merged by `integrate_drafts.py` (Háttatal, and `s-c72-8`). Such cells have status `draft`, the others `auto`. |

Row id = `<prefix>-c<chapter num>-<row index>`; the row index is 1-based within the chapter in file order.
Ids are derived from position, so **never reorder, insert or delete rows in these files**; the id-stability
rules for re-parsed sources are in `docs/DATA_MODEL.md`.
