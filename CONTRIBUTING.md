# Contributing to Open Edda

The goal is a free, citable, continually improving edition of both Eddas that anyone can read in three texts and that
Icelanders can correct without learning git. Most of the people who can fix the Icelandic have never opened a
pull request, so the web page is the primary editor and GitHub is the back office.

## The unit of work: one row, one cell

Every row has a stable id (`g-c35-5` = Gylfaginning, chapter 35, row 5) and three cells: `on` (Old Norse),
`is` (modern Icelandic spelling), `en` (English). One edit changes one cell of one row and gives a one-line
reason. This keeps reviews small and conflicts rare.

## Two routes

**On the page (everyone).** Click a cell, change the text, add a reason, submit. Sign-in is an email magic
link or a Google/GitHub login. Your edit becomes a *draft* overlay, visible to you and to reviewers, until a
reviewer accepts it. You see a list of your edits and their status. (The editor is being built; until it
exists, use the issue template `row-problem` or the pull-request route below.)

**Pull requests (power users and maintainers).** Add overlay records to `overlays/<cell>/<file>.json`
(schema in `overlays/README.md`), run `python -I scripts/validate.py`, open a PR. CI runs the same validator.
Issues are for anything bigger than a row: a chapter whose alignment is systematically off, a term to render
consistently, a policy question.

## Statuses

| Status | Meaning |
| --- | --- |
| `auto` | machine output: the automatic alignment or the automatic modernised spelling |
| `draft` | a person's unreviewed edit, or an AI draft translation (always labelled as AI) |
| `reviewed` | accepted by a reviewer with the right role |
| `disputed` | two reviewers disagree; both readings are shown with a link to the discussion |

Nothing automatic is ever presented as reviewed. A rebuild of the aligned rows never overwrites a reviewed
cell; overlays are applied on top of the generated rows.

## Roles

- **Contributor** (anyone signed in): propose edits, vote on images, comment.
- **Reviewer** (invited by a maintainer, per language): accept, request a change, or mark disputed.
  Icelandic reviewers should be native speakers; English reviewers need Old Norse. Changes to the Old Norse
  column itself need two reviewers and are limited to typographical fixes to the base edition.
- **Maintainer**: merge, run the pipeline, manage roles, decide disputes.

## Rules per column

- **Icelandic.** Modern spelling only. No modernised morphology beyond what Netútgáfan did in Gylfaginning
  (for example *hefir* → *hefur*), so the three columns stay word-for-word parallel. Accepted corrections
  become training data for the moderniser.
- **English.** Brodeur's 1916 text stays as an unchanged layer; a new translation is an overlay with its own
  status. AI drafts are a starting point only, always marked as AI, and a reviewer must change or explicitly
  accept each row before the mark goes. Names keep their normalised Old Norse forms (Óðinn, Þórr, Freyja);
  kennings are translated literally with a bracketed gloss where opaque; metrical terms in Háttatal stay in
  Old Norse with a gloss at first use in a section.
- **Old Norse.** Typographical fixes to the base edition only, two reviewers.
- **Alignment.** Moving a sentence up or down one row is an edit to both rows' cells; say so in the reason.

## Credit and licence

Every accepted edit is attributed on the row and on the contributors page; each data release lists everyone.
Contributions are licensed CC BY 4.0 (see `LICENSE`); by contributing you agree to that.

## Checklist for a pull request

1. Records added, none changed or deleted (supersede with a new record and `replaces`).
2. `python -I scripts/validate.py` prints `OK`.
3. Status is `draft` unless you are a reviewer for that language.
4. The reason field says what was wrong in a few words.

---

## Íslenska

*(drög — þýðing eftir gervigreind, þarf yfirlestur)*

### Markmið

Markmiðið er ókeypis, tilvitnanleg og sífellt betri Snorra-Edda sem hver sem er getur lesið í þremur textum
og Íslendingar geta leiðrétt án þess að læra á git. Vefsíðan sjálf er aðalritillinn; GitHub er bakvinnslan.

### Eining vinnunnar: ein lína, einn reitur

Hver lína hefur fast auðkenni (`g-c35-5` = Gylfaginning, 35. kafli, 5. lína) og þrjá reiti: `on` (forníslenska),
`is` (nútímastafsetning), `en` (enska). Ein breyting nær til eins reits í einni línu og fylgir stutt ástæða.

### Tvær leiðir

**Á síðunni (allir).** Smelltu á reit, breyttu textanum, skrifaðu ástæðu, sendu inn. Innskráning er með
tölvupósti (töfratengli) eða Google/GitHub. Breytingin verður *drög* sem þú og yfirlesarar sjá þar til
yfirlesari samþykkir hana. (Ritillinn er í smíðum; þangað til má nota „row-problem“ sniðmátið fyrir mál
eða senda pull request.)

**Pull request (vanir notendur).** Bættu færslum við `overlays/<reitur>/<skrá>.json`, keyrðu
`python -I scripts/validate.py` og opnaðu pull request.

### Staða reita

- `auto` — sjálfvirk útkoma (sjálfvirk samröðun eða sjálfvirk nútímastafsetning)
- `draft` — óyfirlesin breyting frá manneskju, eða þýðingardrög frá gervigreind (alltaf merkt sem slík)
- `reviewed` — samþykkt af yfirlesara með rétt hlutverk
- `disputed` — tveir yfirlesarar eru ósammála; báðar útgáfur sýndar

Ekkert sjálfvirkt er nokkurn tíma sýnt sem yfirlesið.

### Hlutverk

- **Þátttakandi**: leggur til breytingar, kýs um myndir, skrifar athugasemdir.
- **Yfirlesari** (boðið af umsjónarmanni, fyrir hvert tungumál): samþykkir, biður um breytingu eða merkir
  sem umdeilt. Yfirlesarar íslensku ættu að hafa íslensku að móðurmáli.
- **Umsjónarmaður**: sameinar breytingar, keyrir vinnsluna, stýrir hlutverkum, sker úr ágreiningi.

### Reglur fyrir íslenska dálkinn

Aðeins nútímastafsetning. Engar beygingarbreytingar umfram það sem Netútgáfan gerði í Gylfaginningu
(t.d. *hefir* → *hefur*), svo dálkarnir þrír haldist orð fyrir orð samhliða. Samþykktar leiðréttingar verða
þjálfunargögn fyrir stafsetningarbreytinn.

### Heiður og leyfi

Hver samþykkt breyting er eignuð höfundi á línunni og á síðu þátttakenda. Framlög eru gefin út með
CC BY 4.0 leyfi (sjá `LICENSE`).
