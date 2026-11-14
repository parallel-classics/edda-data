# Portraits for the Mímir cards: brief

One picture per figure, made for the card, so that no tile has to be cut out of a group plate.
Where a portrait exists the site uses it for the Who is who tile, the card and the small round picture;
where it does not, the present picture stays.

Status: style not chosen yet. Step 1 is the test set below (five styles, the same five subjects).
Step 2, after the choice: the full set, in the order of the list at the end.

The same briefs in machine-readable form are in `briefs.json` (styles, poses, one entry per subject); the
generator reads that file, so a change of wording is made there and this page explains it. How it runs is
in section 9.

## 1. Format (every picture, every style)

- 4:3 landscape, at least 1600 x 1200 px. JPEG or PNG.
- One subject only. No second person, no crowd, no hands or shoulders of neighbours at the edges.
- A person: half-figure (head to about the waist), body turned three-quarters, the same way in every
  picture: facing slightly to the viewer's left. Eye level, no view from below or above.
- The head is in the middle of the width; the top of the head is about one eighth down from the top edge;
  the eyes are about one third down. The site also cuts a square from the middle of the picture, so the
  face and the main attribute must both be inside the central square.
- The thing that tells the figure apart is large and in front, never hidden: in the hands, on the shoulder,
  at the chest. If a reader covers the name, the attribute should still say who it is.
- An animal: the whole animal in its most telling outline (side view for horses, wolves, goats, the hart;
  a coil for the serpent), filling most of the frame.
- A place or thing: the whole of it, one clear shape, no small figures needed to understand it.
- Background: quiet and plain, one tone with at most a hint of setting (a wave line, a branch, a hall post).
  The same background treatment in every picture of the set.
- No text, no runes that spell anything, no labels, no frame, no border, no signature, no watermark.
- No horned or winged helmets. Clothing and gear of the Viking Age and earlier: tunics, cloaks with
  brooches, mail only where the story needs it.

## 2. Keeping the character

For the 28 figures of plates P1-P4 there is a reference cut-out in `ref/<id>.jpg` (the figure as it stands on
the plate, with its own things). Give it to the model as the input image with each prompt:

> Use the attached picture only as the character reference: the same person, face, hair, clothing colours
> and objects. Redraw the figure alone in the format and style described below. Do not copy the neighbours
> or the background.

In style A the reference also carries the style. In styles B-E the reference carries only who the figure is.

## 2a. Sheets: four options in one picture

One request makes one sheet at 4K: a 2 x 2 grid of four separate 4:3 panels on a pure white ground with wide
white gutters, so each panel is about 2K, more than a card needs. The generator cuts the sheet into its
panels by finding the white gutters (it falls back to an even cut and says so), so no panel carries a
neighbour.

- One subject: the same figure in four poses (three-quarter view facing left; facing the viewer; in the
  act the figure is known for; at rest, further back). Animals, places and things have their own four.
- A pair: two rows, each row the two of them facing each other across the gutter (section 6).

Every panel becomes a candidate; one is chosen per figure in the picker (section 9). The first pose is the
common one, so a set chosen all from "top left" has everyone at the same angle; the others are there for
the figures whose attribute shows better another way.

## 3. Styles to try

Each block is the style paragraph of the prompt. A full prompt is: reference line (section 2) + subject
line (sections 5-7) + format line (below) + style paragraph.

Format line for every prompt:

> 4:3 landscape. A single figure, half-length, three-quarter view facing slightly left, head centred, eyes
> one third down from the top, the attribute held in front and fully visible. Plain quiet background. No
> text, no letters, no border, no frame, no other people.

### A. The plates' own style

> The same hand as the attached plate: painted illustration with fine ink outline, muted earth colours
> (ochre, rust red, slate blue, moss green) on warm parchment, soft flat light, small touches of gold.
> Background: bare warm parchment with a faint wash behind the figure.

For: one look across plates and cards, the least risk. Against: the least new; the goddesses stay close to
each other unless the attributes are pushed.

### B. Woodcut / linocut

> Hand-printed linocut: bold black outline and carved hatching, three flat colours only (black, one rust
> red, one muted blue-green) on cream paper, slight unevenness of ink as in a real print. Strong simple
> shapes, large attribute, almost no background: a few carved lines for ground or sky.

For: reads best at the small sizes (tile, round chip); attributes become emblems; very consistent across
300 pictures. Against: faces are simple, less warmth.

### C. Icelandic paper manuscript

> In the manner of the illustrated Icelandic Edda manuscripts of the 17th and 18th centuries: naive pen
> drawing in brown-black ink with flat watercolour washes (red, yellow ochre, blue, green), stiff frontal
> charm, simple faces, plain laid paper with slight foxing. No lettering.

For: belongs to the tradition of the text itself; friendly, a little humorous. Against: naive drawing may
look unintended next to the polished plates; the model tends to add handwriting (ask twice for no text).

### D. Viking Age ornament

> Flat stylised figure in the manner of Viking Age picture stones and metalwork: clear silhouette, interlace
> and ribbon ornament inside the shapes, limited palette of stone grey, iron black, red ochre and a little
> gold, on a rough pale stone or vellum ground. Figure still readable as a person or animal at a glance.

For: the animals and monsters look their best; unmistakably Norse. Against: human faces are weak, so the
gods differ only by attribute; the hardest to keep readable.

### E. Book illustration, about 1900

> Ink-and-watercolour book illustration in the Nordic manner of about 1900: confident pen line, large calm
> areas of muted colour, a low horizon or a single tree or wave as setting, art-nouveau sense of design
> without ornament borders. Dignified, a little melancholy.

For: the most "portrait" of the five, real faces and mood. Against: closest to pictures people already
know; the most variation from picture to picture.

## 4. Test set (five subjects in each of five styles: 25 sheets, 100 candidates)

Chosen to show the hard cases: a god full of attributes, a goddess who must not look like the others,
a pair, a monster, a place.

1. Óðinn (`ref/odin.jpg`) - see 5.
2. Freyja (`ref/freyja.jpg`) - see 5.
3. Huginn and Muninn, one sheet for the pair - see 6.
4. Fenrir - see 7.
5. Yggdrasill - see 7.

The picker shows the five styles one under another for each subject, every candidate at tile size with the
small round picture beside it, next to the picture the site uses now.

## 5. The plate figures (28)

Subject line for each. "As on the plate" means: take it from the reference, do not invent.

Æsir (P1, P2)

- `odin` Óðinn: an old man with one eye; the other an empty, closed, scarred socket, never a patch; grey beard, dark blue cloak and
  wide hat or hood; the spear Gungnir upright in his hand; a gold arm-ring. No ravens or wolves in this
  picture (they have their own).
- `thor` Þórr: red beard, broad; the hammer Mjöllnir with its short handle raised to the chest in an iron
  glove; the belt of strength.
- `baldur` Baldr: young, fair, light coming from him (a pale glow on hair and skin, not a halo disc);
  empty hands or a sprig of mistletoe.
- `tyr` Týr: a warrior whose right arm ends at the wrist, shown plainly and in front; sword on the left.
- `heimdall` Heimdallr: the watchman with the great horn Gjallarhorn held across the chest; golden teeth
  showing in a slight smile.
- `bragi` Bragi: an old poet with a very long beard; a harp or lyre as on the plate.
- `loki` Loki: slight, sharp-faced, a sideways look; old stitch scars across the lips; a fishing net over
  his arm.
- `hodr` Höðr: blind, eyes closed or bound; one hand out before him; the mistletoe shaft in the other.
- `vidarr` Víðarr: silent and strong, mouth firmly shut; one foot forward with the thick shoe, which must
  be in the picture (this one may be three-quarter length).
- `vali` Váli: a very young archer, bow drawn or held ready.
- `ull` Ullr: skis on his shoulder, a bow, a shield.
- `forseti` Forseti: the judge, seated, calm, open hand; a pillar of gold and a roof of silver hinted
  behind (Glitnir).
- `h-nir` Hœnir: tall, long-legged, handsome, hesitant; as on the plate (may be three-quarter length).
- `mimir` Mímir: an old head and shoulders by a well, drinking from a horn.

Ásynjur (P3)

- `frigg` Frigg: the queen, enthroned, as on the plate; distaff or keys if the plate has them.
- `fulla` Fulla: a girl with loose hair and a gold band round her head, carrying Frigg's box.
- `sif` Sif: hair of real gold, long, the main thing in the picture: metallic, not blond.
- `idunn` Iðunn: holding the open box of apples in front of her.
- `gefjon` Gefjun: with the plough and the heads of her oxen beside her.
- `skadi` Skaði: a huntress on skis in snow, bow in hand, mountain line behind.
- `saga` Sága: lifting a gold cup; a second cup beside her; water behind (Søkkvabekkr).
- `gna` Gná: riding through the air on her horse, hair and cloak blown back (whole figure, small horse
  allowed to be cut at the legs).
- `eir` Eir: the healer; herbs and bowl as on the plate.

Vanir and others (P4)

- `njordr` Njörðr: an older man barefoot at the shore, the bare feet in the picture (three-quarter
  length), a ship's prow or gulls hinted.
- `freyr` Freyr: bright, a sheaf of corn; in his hand a stag's antler in place of a sword.
- `freyja` Freyja: the necklace Brísingamen large on her breast; a cloak of falcon feathers on her
  shoulders; a tear of red gold on her cheek; one cat at her side.
- `gullveig` Gullveig: a woman standing unharmed in flames with spear shafts through her, gold on her.
- `kvasir` Kvasir: the wise one, as on the plate.

## 6. Pairs and sets

A pair is drawn as two halves of one picture. Rules:

- The same composition mirrored: the first of the pair faces right, the second faces left, so that side by
  side on the page they face each other. The same size in the frame, the same background.
- One difference in pose and one in appearance, both taken from the name or the story, and nothing else
  different. A reader should be able to say which is which without the label.
- Both are drawn in one sheet, left and right panel of a row, so the model sees them together.

| Pair | First | Second |
|---|---|---|
| `huginn` / `munin` (Óðinn's ravens; Thought and Memory) | Huginn: leaning forward, wings half open, about to take off, beak open, looking ahead; blue sheen on the black | Muninn: perched still, wings closed, head turned back over the shoulder, looking behind; warm bronze sheen on the black |
| `geri` / `freki` (Óðinn's wolves; both names mean greedy) | Geri: grey, lying over a bone, head low, eyes up | Freki: darker, standing, jaws open, tongue out |
| `skoll` / `hati` (the wolves after sun and moon) | Sköll: running, rust-red lit from in front by warm gold light (the sun just out of frame) | Hati: running, grey-blue lit from in front by cold silver light (the moon just out of frame) |
| `arvakr` / `alsvidr` (the sun's horses) | Árvakr, Early-Wake: head high, ears pricked, pale gold; bellows under the shoulder | Alsviðr, All-Swift: neck stretched in full gallop, deeper red-gold; bellows under the shoulder |
| `skinfaxi` / `hrimfaxi` (horses of Day and Night) | Skinfaxi: bright horse, the mane shining and lighting the sky | Hrímfaxi: dark horse, mane white with frost, foam dropping from the bit as dew |
| `tanngnjostr` / `tanngrisnir` (Þórr's goats) | Tanngnjóstr: head lowered to butt, teeth bared | Tanngrisnir: head up, jaw set sideways as if grinding; a slightly lame hind leg |
| `sol` / `mani` | Sól: a girl driving, reins in hand, gold light, hair flying | Máni: a youth steering, silver light, two small children behind him |
| `dagr` / `nott` | Dagr: fair and bright, riding | Nótt: dark, cloaked in stars, riding |
| `fenja` / `menja` (the giant maids at the mill Grotti) | Fenja: pushing the mill handle | Menja: pulling it, singing |
| `brokkr` / `sindri` (the dwarf smiths) | Brokkr: at the bellows, a fly on his eyelid | Sindri: at the anvil with tongs |
| `fjalar` / `galar` (the dwarves who killed Kvasir) | Fjalar: with the knife | Galar: with the vat |
| `magni` / `modi` (Þórr's sons) | Magni: a child of huge strength | Móði: older, fierce |

The pairs above are in `briefs.json`, with further pairs from the legends (Ægir / Rán, Göndul / Skögul,
Hrist / Mist, Gjálp / Greip, Hamðir / Sörli, Þjálfi / Röskva, Byggvir / Beyla, Afi / Amma, Faðir / Móðir,
Högni / Heðinn and others).

Sets are drawn the same way, a panel for each member in one sheet (`sets` in `briefs.json`):

- The three norns `urdr`, `verdandi`, `skuld`: old, grown, young; the thread passed from one to the next
  (Urðr holds the spun ball, Verðandi the thread running through her hands, Skuld the shears and the loose
  end; a helmet beside Skuld, since she rides as a valkyrie).
- The four dwarves under the sky `austri`, `sudri`, `vestri`, `nordri`: the same dwarf holding up the edge
  of the sky, in dawn, noon, dusk and night light.
- `hugi`, `logi`, `elli` (Útgarða-Loki's three tricks): a runner who is half a blur, an eater who is flame,
  an old woman in a wrestler's stance.
- `svafa`, `sigrun`, `kara`: Helgi's valkyrie born three times, the same face.
- The three vessels of the mead `odrerir`, `bodn`, `son`; the brothers `slagfidr` and `egill`.

## 7. Creatures, places and things in the test set and after

- `fenrir` Fenrir: a huge wolf bound with a thin silk ribbon (Gleipnir), a sword propping the jaws open.
- `jormungandr` the Miðgarðr serpent: one coil ringing the sea, biting its own tail.
- `sleipnir` Sleipnir: a grey horse in side view, the eight legs clearly countable.
- `yggdrasil` Yggdrasill: the whole ash, crown, trunk and three roots; an eagle at the top, a serpent at
  the root, a squirrel on the trunk, all small.
- `bifrost` Bifröst: the whole arc of the bridge from earth to the gods' gate, the red band burning.
- `nidhoggr`, `ratatoskr`, `eikthyrnir`, `heidrun`, `gullinbursti`, `gulltoppr`, `audumbla`, `garmr`,
  `fafnir`: whole animal, the one telling feature large (the gnawed root; the squirrel on the trunk; the
  dripping antlers; the mead from the udder; the gold bristles; the gold forelock; the cow licking a man's
  head out of the ice; the bound hound before a cave; the dragon on its gold).
- Things (`mjolnir`, `gungnir`, `gjallarhorn`, `mead-of-poetry`): the object alone, lying or hanging, no hand.

## 8. Order of work

1. Test set (section 4).
2. Choice of style.
3. The 28 plate figures (section 5): these replace the cut-outs from the plates first.
4. Pairs and sets (section 6), then the creatures, places and things (section 7).
5. Everyone else who has a card. All 333 cards have a subject line in `briefs.json` (the wording of
   sections 5-7 for the first seventy; the rest only there). Pairs and sets share a sheet, so the full set
   in one style is 296 sheets.

## 9. How it runs

Tools in `edda-site/tools/` (Pillow needed, so `/usr/bin/python3 -I`); the key is read from the environment
variable `GEMINI_API_KEY` or the file `~/.config/edda/gemini_key`, never from a repository.

```
python -I tools/gen_portraits.py --dry-run --test      # the prompts and the number of requests, no key needed
python -I tools/gen_portraits.py --check               # one small request: key, model and endpoint work
python -I tools/gen_portraits.py --test                # 25 sheets -> candidates/<id>/<style>-<run>-<k>.jpg
python -I tools/pick_portraits.py                      # http://127.0.0.1:8765/ : choose one per figure
python -I tools/gen_portraits.py --style B --all       # after the choice: every subject in that style
python -I tools/gen_portraits.py --style B --ids sif --runs 2    # more options for one figure
python -I tools/gen_portraits.py --cut sheet.jpg --id sif --style B   # a sheet made by hand in the Gemini app
python -I pipeline/make_plates.py                      # chosen portraits -> tiles and card pictures
```

- `candidates/` is not committed: only chosen pictures are published. The sheet and its prompt are kept
  beside the candidates (`candidates/_sheets/`).
- A choice copies the candidate to `images/portraits/<entity id>.jpg` and notes it in `picks.json` (file,
  style, model, date). A second click takes it back.
- `make_plates.py` writes `portraits/web/<id>-{1200,600}` for the card and replaces that figure's tile and
  small square in `images/tiles/`. A figure without a portrait keeps its present picture.
- Default model `gemini-nano-banana-2.1` at 4K (`--model`, `--size` change it).

Credit as for the plates: (c) 2026 Grigory Sapunov, CC BY 4.0, with the model named in `made_with`.
