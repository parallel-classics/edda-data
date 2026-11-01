# entities/ — names in the Eddas (task 16)

Who, what and where: every being, place, object, people and event named in the texts, keyed to Wikidata where
an item exists, with every mention located by row id. Spec: `edda-site/docs/specs/ENTITIES.md`. Generator:
`edda-site/pipeline/make_entities.py` (standard library; `images` needs the network, `detect` is offline).
Everything here is status `auto` (automatic identification, not reviewed) until a review process exists.

## Files

| file | written by | what |
|---|---|---|
| `seed.json` | the curator (cloud session, 2026-11-01) | the curated entity list: id, type, Wikidata id or null, labels per language, description, image candidates (Wikidata P18), coordinates, sitelinks, attested Old Norse `forms` with counts, `heiti` (other names and kennings pointing at the entity), curation notes (`amb: ...` marks a name shared by several people), first rows and counts as the curator found them |
| `curated.txt` | the curator | the lemma → entity table behind `seed.json` (so it can be regenerated) |
| `unresolved.json` | the curator | capitalised Old Norse forms the seed does not cover (rare names, mostly from the þulur) |
| `rules.json` | by hand (Claude Code) | tag overrides; extra entities that ambiguity rules point at; ambiguity rules per entity or form scoped by poem, part, chapter or row (`ok`, `check`, an entity id, `skip` for a form, or `{prose, verse}`); bynames in the same row (`near`); the name-list sections (`lists`); translator spellings |
| `notable.json` | by hand (Grigory's list, 2026-11-01) | ids that get a first-appearance card even with fewer than three narrative mentions |
| `images.json` | `make_entities.py images` | Commons `extmetadata` for every image candidate: licence, author, credit, date, size, page URL, 480 px thumbnail URL, `ok` when the licence is PD / CC0 / CC BY / CC BY-SA (never NC or ND) |
| `entities.json` | `make_entities.py detect` | one record per entity (below) plus the tag vocabulary with English and Icelandic labels |
| `mentions.json` | `make_entities.py detect` | one record per mention (below) |
| `report.md` | `make_entities.py detect` | numbers, `check` counts, derived forms, the gap list for the curator, rejected images, cards |

Generated files are regenerated, never edited (COORDINATION rule 5: rerun, do not merge).

## Entity record (`entities.json`)

```json
{"id": "thjazi", "tags": ["giant"], "type": "giant", "wikidata": "Q1346913",
 "names": {"on": "Þjazi", "is": "Þjassi", "en": "Þjazi", "de": "Thiazi", "sv": "Tjatse", "ru": "Тьяцци"},
 "desc": {"en": "Norse mythical character"},
 "image": "He flapped away with her, magic apples and all by Elmer Boyd Smith.jpg",
 "image_candidates": ["He flapped away with her, magic apples and all by Elmer Boyd Smith.jpg"],
 "coords": null, "wiki": {"enwiki": "Þjazi", "iswiki": "Þjassi"},
 "forms": {"on": ["Þjaza", "Þjazi"], "is": ["Þjassa", "Þjassi"], "en": ["Thjazi", "Thjazi's"]},
 "heiti": {}, "first": {"snorri": "g-c23-1", "poetic": "grm-s11"}, "first_any": {"snorri": "g-c23-1", "poetic": "grm-s11"},
 "mentions": 19, "narrative": 19, "check": 0, "card": true, "status": "auto", "notes": []}
```

- `id`: ASCII slug, stable forever (same rule as row ids). The seed's ids are the permanent ids.
- `tags`: from the vocabulary (first = main; `type` = `tags[0]`): god, goddess, giant, dwarf, elf, valkyrie, norn,
  hero, king, poet, animal, horse, monster, object, place_myth, place_real, river, hall, people, poem, event;
  `character` is a placeholder for seed entries whose description gives no better tag (listed in `report.md`).
- `names`: Wikidata labels (CC0) plus `on` where the curator set it. `desc`: the Wikidata description (CC0).
- `image`: the first candidate whose Commons licence passed (`images.json`); null otherwise. Local resized copies
  come with task 16d.
- `forms`: the spellings met per language, most frequent first (English and Icelandic as the translations spell
  them: Othin, Thor, Guthrun, Sigurth, Hárbarður ...). `heiti`: form → `heiti` or `kenning`.
- `mentions` / `narrative` / `check`: Old Norse mentions in all, outside the name-list sections, and flagged
  uncertain. `first`: first narrative mention per book (the card row); `first_any`: first of any kind.
- `card`: has a free image and (in `notable.json` or at least three narrative mentions).

## Mention record (`mentions.json`)

```json
{"entity": "thjazi", "row": "s-c3-1", "lang": "on", "form": "Þjaza", "kind": "name", "status": "auto"}
```

- `lang` is `on`, `is` or `en`; `kind` is `name`, `heiti` or `kenning`.
- `check: true`: ambiguous and not resolved by `rules.json` (several people share the name, or the curator
  marked it `amb:`); the page must not link it without an "uncertain" label.
- `list: true`: inside a name-list section (Skáldskaparmál chapters 67–89, Grímnismál's river and name lists):
  not narrative, never a card.
- `derived: true`: matched through a case form derived from the nominative, not an attested form of the seed.
- Old Norse mentions are canonical; Icelandic and English mentions exist only in rows whose Old Norse cell has
  the entity, found by a spelling-blind comparison with the entity's names.
- Corrections (wrong entity, missed mention) will go through overlays like any cell edit; the overlay shape for
  mentions is not defined yet (task 16b or later).

## How to regenerate

```
cd ../edda-site
python -I pipeline/make_entities.py images     # only when seed.json gained image candidates (network)
python -I pipeline/make_entities.py detect
python -I pipeline/make_entities.py sample --n 200 --seed 7   # review sample for STATUS.md
cd ../edda-data && python -I scripts/validate.py
```
