# sources/ — the base texts as fetched

Immutable. Nothing in this folder is edited by hand; corrections go to `overlays/`. The medieval texts are in
the public domain and so are Brodeur's and Bellows' translations; the rights in Guðni Jónsson's normalised
editions and in Netútgáfan's text are not yet confirmed (`LICENSE`, section 1). Fetch date: **2026-10-23**
for Snorri's Edda, **2026-10-25** for Völuspá.

## on/ — Old Norse (Guðni Jónsson 1954)

| File | What | Produced by |
| --- | --- | --- |
| `prologus.txt` | Formáli (Prologus), 5 chapters | fetched |
| `gylfaginning.txt` | Gylfaginning, 54 chapters | fetched |
| `skaaldskaparmaal.txt` | Skáldskaparmál, 89 chapters | fetched |
| `haattatal.txtl` | Háttatal, 3 sections, 102 stanzas (the odd extension is the mirror's) | fetched |
| `on_prol.json`, `on_gylf.json`, `on_skald.json` | chapters → blocks | `edda-site/pipeline/parse_on.py <txt> <json>` |
| `on_hatt.json` | sections → blocks (stanzas numbered) | `edda-site/pipeline/parse_hatt.py haattatal.txtl on_hatt.json` |

- Edition: *Edda Snorra Sturlusonar*, normalised text by Guðni Jónsson, Íslendingasagnaútgáfan, Reykjavík
  1954, as published on heimskringla.no (Norrøne Tekster og Kvad). Chapter numbers and titles follow it.
- Fetched from the GitHub mirror `cltk/old_norse_texts_heimskringla`, folder `Snorra-Edda/txt_files/`.
  The mirror's README asks that Heimskringla and the editors be credited; we do, in `README.md` and on the site.
- Known issue: Guðni Jónsson's Gylfaginning ends before the two closing sentences on Öku-Þórr and the Turks
  that Netútgáfan and Brodeur both have. The page notes this at the last row of chapter 54.

Block shape (`on_*.json`): `{"title", "chapters": [{"num", "title", "blocks": [...]}]}` with blocks
`{"t": "p", "s": "<paragraph>"}` or `{"t": "v", "n": <stanza number or null>, "l": ["line", ...]}`.

### Völuspá (Poetic Edda)

| File | What | Produced by |
| --- | --- | --- |
| `voluspa.txt` | Völuspá, 66 stanzas, Guðni Jónsson's numbering | fetched |

- Edition: *Eddukvæði (Sæmundar-Edda)*, normalised text by Guðni Jónsson, Íslendingasagnaútgáfan, Reykjavík
  1949, as published on heimskringla.no. Fetched from the same CLTK mirror, folder
  `Sæmundar-Edda/Völuspá/txt_files/complete.txt`. The folder has 25 poems in all (Völuspá to Hamðismál).
- Guðni Jónsson's text mixes the Codex Regius and Hauksbók versions: 66 stanzas, with the refrain
  (*Geyr nú Garmr mjök …*) four times (44, 49, 54, 58) and the Hauksbók stanza on Váli (34).

## is/ — Modern Icelandic (Netútgáfan 1997), Gylfaginning only

| File | What | Produced by |
| --- | --- | --- |
| `gylf_is.html` | Netútgáfan's page as fetched (stored as UTF-8) | fetched |
| `is_gylf.json` | 54 chapters → blocks, same shape as `on_*.json` | `edda-site/pipeline/parse_is.py gylf_is.html is_gylf.json` |

- Source: https://netutgafan.snerpa.is/snorri/gylf.htm — "Netútgáfan — júní 1997", modern spelling and
  light modernised morphology (*hefir* → *hefur*).
- No free modern-spelling text of the other three parts is known; their Icelandic column is automatic
  (`auto/is_*_auto.json`). If one turns up it replaces the automatic column (see `docs/ROADMAP.md`).

## en/ — English (Brodeur 1916)

| File | What | Produced by |
| --- | --- | --- |
| `brodeur_prologue.html`, `brodeur_gylf.html`, `brodeur_skald.html` | the sacred-texts.com transcription, HTML of the article element as captured through a reader view (not the raw page) | fetched |
| `en_prol.json` | 5 sections | `edda-site/pipeline/parse_en.py --prologue brodeur_prologue.html en_prol.json` |
| `en_gylf.json` | 54 chapters with bottom-of-page notes | `edda-site/pipeline/parse_en.py brodeur_gylf.html en_gylf.json` |
| `en_skald.json` | 74 chapters (Brodeur's division) with notes | `edda-site/pipeline/parse_en.py brodeur_skald.html en_skald.json` |

- Edition: Arthur Gilchrist Brodeur, *The Prose Edda by Snorri Sturluson*, The American-Scandinavian
  Foundation, New York 1916. Public domain. Brodeur translated the Prologue, Gylfaginning and Skáldskaparmál
  and omitted Háttatal; his chapter divisions in Skáldskaparmál differ from Guðni Jónsson's (74 vs 89) and are
  mapped in `aligned/al_skald.json` (`chapter_beads`, `en_chapters`).
- Known issues: the transcription had ten scanning errors (e.g. "Then. spake", "be knew",
  "The third is Fir:") which `parse_en.py` fixes by a fixed list (`OCR_FIXES`), and it had lost every *œ*
  (Hœnir, Hœfir), which the parser restores. Page-break markers `{p. N}` are removed and paragraphs cut
  mid-sentence by a page break are joined. Footnote references are kept as `⟦n⟧` in the text with the notes
  in `chapters[].notes`. Brodeur's editorial brackets are kept. ` | ` inside a verse line is his half-line
  division.
- The proofread Wikisource copy of Brodeur is cleaner and is the planned replacement base (roadmap phase 4).
  Brodeur's text stays as a separate, unchanged layer when a new translation is added as overlays.

### Völuspá — Bellows 1923

| File | What | Produced by |
| --- | --- | --- |
| `bellows_voluspo.txt` | Bellows' introductory note, 66 stanzas and his notes, as plain text | fetched |

- Edition: Henry Adams Bellows, *The Poetic Edda*, The American-Scandinavian Foundation, New York 1923.
  Public domain (Bellows died in 1939). Fetched 2026-10-25 from English Wikisource,
  *The Poetic Edda (tr. Bellows)/Voluspo*, rendered page text through the MediaWiki API.
- Bellows follows the Codex Regius order with changes of his own (he swaps 23 and 24, has two stanzas where Guðni Jónsson
  has one (28 and 56), prints the refrain three times and leaves out the Hauksbók stanza on Váli). The pairing
  is in `edda-site/pipeline/make_voluspa.py` (`GJ2B`) and in each row's `en_stanzas`.
- In the text file a gap inside a line is his half-line division (Wikisource *cesura*); the build shows it as
  ` | `. Two lines lost their gap in the transcription (stanzas 13 and 15) and are fixed in the script. His
  notes are numbered by his stanzas; stanzas 11, 13, 16 and 24 have none.
