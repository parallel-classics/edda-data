# sources/ — the base texts as fetched

Immutable. Nothing in this folder is edited by hand; corrections go to `overlays/`. The medieval texts are in
the public domain and so are Brodeur's and Bellows' translations; the rights in Guðni Jónsson's normalised
editions and in Netútgáfan's text are not yet confirmed (`LICENSE`, section 1). Fetch date: **2026-10-23**
for Snorri's Edda, **2026-10-25** for the Poetic Edda.

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

### on/eddukvaedi/ — the Poetic Edda (Guðni Jónsson 1949)

| File | What | Produced by |
| --- | --- | --- |
| `gj_eddukvaedi.json` | `{page title: page text}` for the 45 poems of *Eddukvæði* on heimskringla.no, in the edition's order (Völuspá … Forspjallsljóð) | fetched 2026-10-25 through a browser (rendered text of each page) |
| `voluspa_cltk.txt` | Völuspá from the CLTK mirror, the first source used (same edition, kept for provenance) | fetched |

- Edition: *Eddukvæði (Sæmundar-Edda)*, normalised text by Guðni Jónsson, Íslendingasagnaútgáfan, Reykjavík
  1949, as published on heimskringla.no (https://heimskringla.no/wiki/Eddukvæði). The CLTK mirror has only 25
  of the poems (and a truncated Hávamál, 145 of 164 stanzas), so heimskringla.no is the source.
- Contents: the Codex Regius poems, Baldrs draumar, Rígsþula, Hyndluljóð, Völuspá in skamma, Gróttasöngr,
  Grógaldr, Fjölsvinnsmál, and the Eddic poems preserved in sagas and elsewhere (Hjálmarskviða, Hervararkviða,
  Hlöðskviða, Hálfsrekkaljóð, Heiðreksgátur, Eddubrot, Sólarljóð, Forspjallsljóð). Guðni Jónsson prints *Frá
  dauða Sinfjötla* as the prose opening of Grípisspá, and gives Völuspá in skamma separately from Hyndluljóð.
- Page text format: stanza number on its own line ("12."), the lines, a blank line; prose paragraphs with
  three-space indents; speaker lines ("Loki kvað:"); unnumbered verse after a speaker line is the rest of the
  stanza; editorial gaps as dots. `make_poems.py` parses this.
- heimskringla.no also carries Norwegian, Danish and Swedish translations of each poem (linked from the
  language table at the top of every page) — a source for future columns once their status is checked.

## is/ — Modern Icelandic (Netútgáfan 1997), Gylfaginning only

| File | What | Produced by |
| --- | --- | --- |
| `gylf_is.html` | Netútgáfan's page as fetched (stored as UTF-8) | fetched |
| `is_gylf.json` | 54 chapters → blocks, same shape as `on_*.json` | `edda-site/pipeline/parse_is.py gylf_is.html is_gylf.json` |

- Source: https://netutgafan.snerpa.is/snorri/gylf.htm — "Netútgáfan — júní 1997", modern spelling and
  light modernised morphology (*hefir* → *hefur*).
- `netutgafan/`: five Eddic poems in modern spelling from the same site (Hávamál, Völuspá, Þrymskviða, Völundarkviða,
  Helgakviða Hundingsbana II), fetched 2026-11-01; prepared on the rows as `is_nu`, switched on after the notification
  email (`netutgafan/README.md`).
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

### en/bellows/ — the Poetic Edda in English (Bellows 1923)

| File | What | Produced by |
| --- | --- | --- |
| `bellows_poetic_edda.json` | `{page: {intro: [...], blocks: [...], notes: {...}}}` for the 35 poem pages of *The Poetic Edda (tr. Bellows)* on English Wikisource | fetched 2026-10-25 (MediaWiki `action=parse`, structured in the browser) |
| `bellows_voluspo.txt` | Völuspá as plain text, the first fetch | fetched |

- Edition: Henry Adams Bellows, *The Poetic Edda*, The American-Scandinavian Foundation, New York 1923.
  Public domain (Bellows died in 1939).
- Blocks: `{"t": "p", "s": …}` for prose (the manuscript prose and speaker lines) and `{"t": "v", "n": "12",
  "l": [...], "ref": "⟦cite_note-…⟧"}` for stanzas, in page order after the introductory note; a gap inside a
  line (Wikisource *cesura*) is written ` | `; note references are kept as `⟦cite_note-id⟧` and resolved
  against `notes`.
- Bellows did not translate Gróttasöngr or the saga poems, Sólarljóð and Forspjallsljóð. His Svipdagsmol is
  Guðni Jónsson's Grógaldr + Fjölsvinnsmál; his Hyndluljoth includes Völuspá in skamma; his Fra Dautha
  Sinfjotla is the prose that opens Guðni Jónsson's Grípisspá. His stanza numbering and order differ from
  Guðni Jónsson's in many poems; the pairing is automatic (see edda-site `pipeline/README.md`).

### en/thorpe/ — Sólarljóð and Hrafnagaldr Óðins in English (Thorpe 1866)

| File | What | Produced by |
| --- | --- | --- |
| `thorpe04.html`, `thorpe18.html` | the germanicmythology.com transcription of *Edda Sæmundar hinns Fróða* Part I (Odin's Ravens' Song; The Song of the Sun), as fetched 2026-11-01 | fetched |
| `thorpe_fsl.json`, `thorpe_sol.json` | `{title, source, intro: [...], stanzas: [{n, l: [lines]}], notes: {k: text}}`; footnote references as `⟦k⟧` | `edda-site/pipeline/parse_thorpe.py <html> <json> "<heading>" "<title>"` |

- Edition: Benjamin Thorpe, *Edda Sæmundar hinns Fróða: The Edda of Sæmund the Learned*, Part I, London (Trübner)
  1866. Public domain (Thorpe died in 1870). Wikisource carries only the Norrœna Society reprint of 1907 (one
  paragraph per stanza, without Hrafnagaldr), so the line-by-line transcription on germanicmythology.com is the
  source; The Song of the Sun was checked against the Wikisource text (same wording, Thorpe's 83 stanzas).
- Thorpe did not translate Gróttasöngr (his Part I has the mythological poems listed on the page, Part II the
  heroic poems); its English stays Brodeur's stanzas from Skáldskaparmál where Snorri quotes it, else the AI draft.
- Pairing with Guðni Jónsson's stanzas: by number, one to one (Hrafnagaldr 26 = 26; Sólarljóð 82 = 82, Thorpe's
  closing stanza 83 has no counterpart and is given as a note). `edda-site/pipeline/fill_thorpe.py` writes the rows
  (`en_thorpe: true`, source `thorpe-1866` in `aligned/sources.json`); the earlier AI drafts stay in
  `overlays/en/poetic-ai-draft.json` marked `withdrawn`.
