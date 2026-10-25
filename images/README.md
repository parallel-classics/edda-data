# images/ — illustration briefs and image records

Two tracks with different rules.

**Licence policy (decided 2026-10-25).** Track 1 accepts public-domain works and anything released under CC0, CC BY or CC BY-SA. Nothing NC or ND, and nothing whose licence is only asserted by an uploader without a source. The licence is recorded per image (`license`, `license_basis`) and shown in the page's credit line; a BY-SA photograph keeps its own licence beside the CC BY 4.0 text. Each record carries a `kind`: `depiction` (a picture of the scene), `manuscript` (a page of Codex Regius, Wormianus, the Uppsala Edda, NKS 1867 4to…), `monument` (runestones, picture stones, carvings, church portals), `place` (Reykholt, Þingvellir, landscape). The page shows one depiction per chapter first and up to three documentary images in a strip below it.

**Density rule.** At most one illustration slot per chapter, at most three documentary images per chapter, and about one image per twenty rows overall (roughly one per three printed pages; about 75 for 1,514 rows). The validator warns when a part exceeds it.

**Track 1 — public-domain mapping (open data).** The 42 scene briefs in `scenes.json` become an open dataset
of verified public-domain depictions: each record names the scene (row range), the work, artist and date, the
holding institution, a stable URL, the licence basis and who checked it. One image per scene is shown in the
page's slot; others are listed. Candidates already noted in the briefs (Frølich, Doepler, Eckersberg, Winge,
Bauer, Collingwood, the 1760 manuscript NKS 1867 4to, the Gosforth cross) are **unverified** until a record
exists with `checked_by` filled. A maintainer verifies the licence field before a record goes live.

**Track 2 — community-made images.** Only for scenes with no public-domain depiction, or as a separate
"new interpretations" gallery. The brief is the prompt everyone works from. Submissions need the image, the
tool or technique (hand-drawn, model name, or both), the prompt or process in a sentence, and a CC BY 4.0
grant. Gate before voting (checked against the brief: right characters and attributes, scene from the text,
no text in the image, no watermark, resolution), then voting weighted by account standing, a minimum of ten
votes, jury for close calls, two flags hide an image. A public-domain image always keeps the first position.
Track 2 records are not stored here yet; the schema will be added when the track opens (roadmap phase 3).

## scenes.json

`{"_note": ..., "<part>": {"<chapter>": {"scene": "<brief>", "pd": ["<candidate work>", ...]}}}` with part
keys `prologue`, `gylfaginning`, `skaldskaparmal`, `hattatal` (3 + 26 + 12 + 1 = 42 briefs). `scene` is the
one-line brief for an artist or an image model; `pd` lists public-domain works believed to depict the scene,
to be verified against the institution record. The page renders a dashed "Illustration wanted" slot per brief.

## records.json (track 1)

A record with `"placed": false` is kept for provenance but not shown in its slot (the build skips it); `note` says why. `generation-briefs.json` / `.md` hold the track-2 briefs (prompt + checklist) for slots that need a generated or commissioned image.

`{"_note": ..., "records": [ ... ], "unfilled": {"<slot id>": "<why no image>"}}`. One record per **slot**
(chapter); the slot id is `<p>-c<chapter>` (e.g. `g-c1`), which is also the record `id`, so the build can
look a chapter's image up directly; a second image for the same chapter goes into that record's
`alternatives`. `unfilled` is optional and names slots searched without result.

Optional keys added 2026-10-25: `kind` (depiction | manuscript | monument | place; default depiction), `placed` (default true). Documentary images for a chapter go in `alternatives` of that chapter's record with their own `kind`, or, when the chapter has no depiction record, in a record of their own with `kind` set.

Core keys (required, checked by the validator):

| Key | Meaning |
| --- | --- |
| `id` | the slot id `<p>-c<chapter>`, unique |
| `part` | `prologue`, `gylfaginning`, `skaldskaparmal` or `hattatal` |
| `chapter` | chapter number (integer) in that part |
| `title` | title of the work |
| `artist` | artist's name as commonly written (or "anonymous", a manuscript name, a workshop) |
| `date` | date of the work as a string (`"1895"`, `"c. 1760"`) |
| `source_url` | stable record page (Wikimedia Commons file page, museum or library record) |
| `file_url` | direct URL of the image file at the source |
| `width`, `height` | pixel size of the file at `file_url` (integers) |
| `license_basis` | why it is free: `"artist died 1908 (PD)"`, `"institution CC0 release"`, `"15th-century manuscript; reproduction released by BnF"` |
| `checked_by` | who checked the institution record; say explicitly when a human check is still pending |
| `checked_on` | `YYYY-MM-DD` |
| `caption` | the credit line shown under the image: work, artist, date, holding institution |

Optional keys (validated when present):

| Key | Meaning |
| --- | --- |
| `artist_dates` | `"1820–1908"`, `"active c. 1490–1510"` or `null` |
| `medium` | `"oil on canvas"`, `"pen drawing"`, `"manuscript illumination"`, ... |
| `source` / `institution` | holding institution, collection, shelfmark |
| `commons_file` | the Commons file name when the source is Wikimedia Commons |
| `license` | the licence label at the source (`"Public domain"`, `"CC0"`) |
| `scene_rows` | row ids the image depicts, e.g. `["g-c1-1", "g-c1-2"]`; each must exist |
| `file` | file name in `images/pd/` when a copy is hosted here (must exist); the build looks for `<id>.jpg` there by default |
| `note` | free text shown under the credit (e.g. what the picture shows that the text does not) |
| `alternatives` | list of other candidate records seen (same keys, unverified) |

The validator checks: unique `id`, known `part`, existing `chapter`, existing `scene_rows`, core keys
present, `file` present in `images/pd/` when set, and that every `unfilled` slot is an existing chapter.
The build (`edda-site/pipeline/build2.py --records images/records.json --images local|embed|commons`) uses
`id`, `file_url`, `width`, `height`, `source_url`, `title`, `caption`, `note`.

## pd/

Image files for records that host a copy (only when `license_basis` is documented): a 1280 px JPEG per slot named
`<id>.jpg` (e.g. `g-c1.jpg`), under about 500 KB each. The site build copies them next to the page.
