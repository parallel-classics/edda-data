"""Validate the edda-data repository and print the status table.

Checks
  aligned/al_*.json   every row has a non-empty Old Norse cell; row ids are unique; chapter numbers unique per part
  aligned/poetic/al_<poem>.json  Poetic Edda: rows carry their own ids <poem>-s<N> / <poem>-p<k>, unique;
                      index.json lists every poem file; links.json: both ends of every link exist
  aligned/titles.json every chapter of Snorri's parts and every poem has a title entry
  aligned/sources.json  the generated origin of every part and cell (task 17): kinds, cells, checks per origin
  overlays/**/*.json  {"records": [...]}; every record: row id exists in aligned/, cell in {on, is, en},
                      either status in {auto, draft, reviewed, disputed} (old form) or origin + check (new form,
                      check allowed for that origin; source with origin published), non-empty text, author,
                      date YYYY-MM-DD, "replaces" null or string
  images/records.json every record: unique id, part known, chapter exists, scene_rows (if given) exist, core keys present,
                      "file" (if given) exists in images/pd/; the optional top-level "unfilled" map names existing slots
  images/scenes.json  every chapter key exists in the part
  entities/           (when present) seed.json, rules.json, notable.json, images.json, entities.json, mentions.json:
                      ids are unique slugs, tags are from the vocabulary, Wikidata ids look like Q123, every mention
                      names an existing entity, row and language, every used image passed the licence check;
                      summaries.json: known entity ids, plain-text en (is optional), author, date, status draft|reviewed

Then prints, per part and column, the effective origin (edition / published / machine / ai / contributor / empty)
and check (aligned-auto / aligned-checked / unreviewed / reviewed / disputed / empty) of the cells after overlays
are applied (an unresolved dispute wins; else the latest reviewed or aligned-checked record; else the generated
cell), and the old one-word summary for comparison with earlier tables.

Usage: python -I scripts/validate.py [repo root]      exit code 1 on any error
Standard library only.
"""
import glob
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PARTS = [  # row-id prefix, aligned file, "part" value inside the file, scenes.json key, display name
    ("p", "al_prol.json", "prologue", "prologue", "Formáli"),
    ("g", "al_gylf.json", "gylfaginning", "gylfaginning", "Gylfaginning"),
    ("s", "al_skald.json", "skaldskaparmal", "skaldskaparmal", "Skáldskaparmál"),
    ("h", "al_hatt.json", "hattatal", "hattatal", "Háttatal"),
] 
# possible columns: a language (its default text), or a further version of one, "<lang>-<version>" (task 26,
# edda-site docs/specs/VERSIONS.md), registered in aligned/texts.json by edda-site/pipeline/fill_versions.py
BASE_CODES = ("on", "is", "en", "ru", "nb", "nn", "da", "sv", "de")


def _versions():
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "aligned", "texts.json")
    try:
        return tuple(sorted(json.load(open(p, encoding="utf-8")).get("texts", {})))
    except (OSError, ValueError):
        return ()


VERSIONS = _versions()
LANG_CODES = BASE_CODES + VERSIONS
CELLS = BASE_CODES + VERSIONS
STATUSES = ("auto", "draft", "reviewed", "disputed")
ORIGINS = ("edition", "published", "machine", "ai", "contributor")
CHECKS = ("aligned-auto", "aligned-checked", "unreviewed", "reviewed", "disputed")
ROW_ID = re.compile(r"^([pgsh]-c\d+-\d+|[a-z0-9]+-[spv]\d+)[a-z]?$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# images/records.json: these keys must be present; the others in images/README.md are optional
IMAGE_KEYS = ("id", "part", "chapter", "title", "artist", "date", "source_url", "file_url", "width", "height",
              "license_basis", "checked_by", "checked_on", "caption")

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def block_text(b):
    return b.get("s", "") if b.get("t") == "p" else " ".join(b.get("l", []))


def check_aligned():
    """Returns {row_id: {"on": bool, "is": bool, "en": bool, "en_draft": bool}} and {prefix: set(chapter nums)}."""
    rows, chapters = {}, {}
    for prefix, fname, part_name, _, _ in PARTS:
        path = os.path.join(ROOT, "aligned", fname)
        if not os.path.exists(path):
            err(f"missing {path}")
            continue
        al = load(path)
        if al.get("part") != part_name:
            err(f"{fname}: part is {al.get('part')!r}, expected {part_name!r}")
        nums = set()
        for c in al.get("chapters", []):
            num = c.get("num")
            if num in nums:
                err(f"{fname}: duplicate chapter number {num}")
            nums.add(num)
            for i, r in enumerate(c.get("rows", []), start=1):
                rid = f"{prefix}-c{num}-{i}"
                if rid in rows:
                    err(f"{fname}: duplicate row id {rid}")
                on = r.get("on") or []
                if not on or not any(block_text(b).strip() for b in on):
                    err(f"{fname}: row {rid} has an empty Old Norse cell")
                rows[rid] = {c: bool(r.get(c)) for c in LANG_CODES}
                rows[rid]["en_draft"] = bool(r.get("en_draft"))
                rows[rid]["en_from"] = bool(r.get("en_from"))
        chapters[prefix] = nums
    # Poetic Edda
    pdir = os.path.join(ROOT, "aligned", "poetic")
    if os.path.isdir(pdir):
        idx = load(os.path.join(pdir, "index.json"))
        listed = {p["file"] for p in idx["poems"]}
        for f in sorted(glob.glob(os.path.join(pdir, "al_*.json"))):
            if os.path.basename(f) not in listed:
                err(f"aligned/poetic/{os.path.basename(f)} is not listed in index.json")
        for p in idx["poems"]:
            path = os.path.join(pdir, p["file"])
            if not os.path.exists(path):
                err(f"aligned/poetic/index.json names a missing file {p['file']}")
                continue
            d = load(path)
            pfx = d.get("poem")
            if pfx != p["prefix"]:
                err(f"{p['file']}: poem {pfx!r} but index says {p['prefix']!r}")
            for c in d["chapters"]:
                for r in c["rows"]:
                    rid = r.get("id", "")
                    if not re.fullmatch(rf"{re.escape(pfx)}-[spv]\d+b?", rid):
                        err(f"{p['file']}: bad row id {rid!r}")
                    if rid in rows:
                        err(f"{p['file']}: duplicate row id {rid}")
                    if not r.get("on"):
                        err(f"{p['file']}: row {rid} has an empty Old Norse cell")
                    rows[rid] = {c2: bool(r.get(c2)) for c2 in LANG_CODES}
                    rows[rid]["en_draft"] = bool(r.get("en_draft"))
                    rows[rid]["en_from"] = bool(r.get("en_from"))
                    rows[rid]["en_thorpe"] = bool(r.get("en_thorpe"))
                    rows[rid]["is_netutgafan"] = bool(r.get("is_netutgafan"))
                    rows[rid]["poem"] = True
        chapters["poetic"] = {p["prefix"] for p in idx["poems"]}
    return rows, chapters


def check_links(rows, chapters):
    n = 0
    path = os.path.join(ROOT, "aligned", "poetic", "links.json")
    if os.path.exists(path):
        for k, l in enumerate(load(path).get("links", [])):
            n += 1
            if l.get("row") not in rows:
                err(f"aligned/poetic/links.json#{k}: Snorri row {l.get('row')!r} does not exist")
            if l.get("poem_row") not in rows:
                err(f"aligned/poetic/links.json#{k}: poem row {l.get('poem_row')!r} does not exist")
    tpath = os.path.join(ROOT, "aligned", "titles.json")
    if os.path.exists(tpath):
        titles = load(tpath)["titles"]
        want = [f"{p}-ch{c}" for p in "pgsh" for c in sorted(chapters.get(p, set()))] + sorted(chapters.get("poetic", set()))
        miss = [k for k in want if k not in titles]
        if miss:
            err(f"aligned/titles.json: no title for {miss[:10]}")
        for k, t in titles.items():
            if not t.get("on") or not t.get("en"):
                warnings.append(f"titles: {k} lacks an Old Norse or English title")
    return n


def load_sources():
    """aligned/sources.json: {"sources": {id: {kind, label, ...}}, "cells": {part: {cell: id}}, "row_flags", "checks"}."""
    path = os.path.join(ROOT, "aligned", "sources.json")
    if not os.path.exists(path):
        err("aligned/sources.json missing (the generated origin of every column; see docs/DATA_MODEL.md)")
        return {"sources": {}, "cells": {}, "row_flags": {}, "checks": {}}
    src = load(path)
    for sid, rec in src.get("sources", {}).items():
        if rec.get("kind") not in ORIGINS:
            err(f"aligned/sources.json: source {sid!r} has kind {rec.get('kind')!r}")
    for part, cells in src.get("cells", {}).items():
        for cell, sid in cells.items():
            if sid not in src.get("sources", {}):
                err(f"aligned/sources.json: cells[{part}][{cell}] = {sid!r} is not a source")
    for origin, checks in src.get("checks", {}).items():
        if origin not in ORIGINS or any(c not in CHECKS for c in checks):
            err(f"aligned/sources.json: checks[{origin}] = {checks!r}")
    return src


def generated_origin(rid, row, src):
    """(origin, source id, default check) of a generated cell per aligned/sources.json."""
    def one(cell):
        if not row.get(cell):
            return None, None, None
        part = rid.split("-")[0] if re.match(r"^[pgsh]-c", rid) else "poetic"
        sid = src.get("cells", {}).get(part, {}).get(cell)
        for flag, flag_sid in src.get("row_flags", {}).items():
            if cell == flag.split("_")[0] and row.get(flag):
                sid = flag_sid
                break
        kind = src.get("sources", {}).get(sid, {}).get("kind", "machine")
        checks = src.get("checks", {}).get(kind) or ["unreviewed"]
        return kind, sid, checks[0]
    return one


def record_props(rec, src):
    """(origin, source, check) of an overlay record: the new fields, or the old `status` mapped as in DATA_MODEL.md."""
    origin, check, status = rec.get("origin"), rec.get("check"), rec.get("status")
    author = rec.get("author") or ""
    if origin is None:
        origin = "ai" if author.startswith("ai:") else "machine" if author.startswith("bot:") or status == "auto" else "contributor"
    if check is None:
        default = (src.get("checks", {}).get(origin) or ["unreviewed"])[0]
        check = {"reviewed": "aligned-checked" if origin == "published" else "reviewed", "disputed": "disputed",
                 "draft": "unreviewed", "auto": default}.get(status)
    return origin, rec.get("source"), check


def legacy_status(origin, check, default_check):
    if check == "disputed":
        return "disputed"
    if check in ("reviewed", "aligned-checked"):
        return "reviewed"
    if origin == "edition":
        return "source"
    if origin in ("published", "machine"):
        return "auto"
    return "draft"


def check_overlays(rows, src):
    """Returns {(row, cell): (origin, source, check)} after applying overlays in file order (rule in
    docs/DATA_MODEL.md; the site build applies the same rule in edda-site/pipeline/overlays.py)."""
    effective = {}
    decided = {}     # (row, cell) -> True once a reviewed / aligned-checked record exists
    files = sorted(glob.glob(os.path.join(ROOT, "overlays", "**", "*.json"), recursive=True))
    for path in files:
        rel = os.path.relpath(path, ROOT)
        try:
            doc = load(path)
        except ValueError as e:
            err(f"{rel}: invalid JSON ({e})")
            continue
        recs = doc.get("records") if isinstance(doc, dict) else None
        if not isinstance(recs, list):
            err(f"{rel}: expected an object with a \"records\" list")
            continue
        folder_cell = os.path.basename(os.path.dirname(path))
        for k, rec in enumerate(recs):
            where = f"{rel}#{k}"
            rid, cell, status = rec.get("row"), rec.get("cell"), rec.get("status")
            origin, source, check = rec.get("origin"), rec.get("source"), rec.get("check")
            if not isinstance(rid, str) or not ROW_ID.match(rid):
                err(f"{where}: bad row id {rid!r}")
                continue
            base = re.sub(r"(?<=\d)[a-z]$", "", rid)  # a suffixed id (split row) must point at an existing base id
            if rid not in rows and base not in rows:
                err(f"{where}: row {rid} does not exist in aligned/")
            if cell not in CELLS:
                err(f"{where}: cell {cell!r} not in {CELLS}")
            elif folder_cell in CELLS and cell.split("-")[0] != folder_cell:   # overlays/en/ holds en and en-<version>
                err(f"{where}: cell {cell!r} but the file is under overlays/{folder_cell}/")
            if origin is None and check is None:
                if status not in STATUSES:
                    err(f"{where}: status {status!r} not in {STATUSES}")
            else:
                if origin not in ORIGINS:
                    err(f"{where}: origin {origin!r} not in {ORIGINS}")
                elif check not in (src.get("checks", {}).get(origin) or CHECKS):
                    err(f"{where}: check {check!r} is not allowed for origin {origin!r}")
                if origin == "published" and source not in src.get("sources", {}):
                    err(f"{where}: origin published needs a source from aligned/sources.json")
                if status is not None and status not in STATUSES:
                    err(f"{where}: status {status!r} not in {STATUSES}")
            if not isinstance(rec.get("text"), str) or not rec["text"].strip():
                err(f"{where}: empty text")
            if not isinstance(rec.get("author"), str) or not rec["author"]:
                err(f"{where}: missing author")
            if not isinstance(rec.get("date"), str) or not DATE.match(rec["date"]):
                err(f"{where}: date {rec.get('date')!r} is not YYYY-MM-DD")
            if "replaces" in rec and rec["replaces"] is not None and not isinstance(rec["replaces"], str):
                err(f"{where}: replaces must be null or a string")
            if "reason" in rec and not isinstance(rec["reason"], str):
                err(f"{where}: reason must be a string")
            if rec.get("withdrawn"):   # kept as history (e.g. an AI draft replaced by a published translation); not applied
                continue
            if rid in rows and cell in CELLS and (status in STATUSES or (origin in ORIGINS and check in CHECKS)):
                # docs/DATA_MODEL.md: an unresolved dispute wins; else the latest reviewed / aligned-checked record;
                # else unreviewed records on top of the generated cell
                o, sid, ch = record_props(rec, src)
                key = (rid, cell)
                cur = effective.get(key)
                if ch in ("reviewed", "aligned-checked"):
                    effective[key] = (o, sid, ch)          # a later reviewed record resolves a dispute
                    decided[key] = True
                elif ch == "disputed":
                    effective[key] = (cur[0] if cur else o, cur[1] if cur else sid, "disputed")
                elif cur is None or cur[2] not in ("reviewed", "aligned-checked", "disputed"):
                    # an unreviewed record: the reading text stays the generated cell, except that an AI-draft cell
                    # (en_draft) is read from its ai: record; a bot's `auto` record stands for the generated cell
                    gen = generated_origin(rid, rows[rid], src)(cell)
                    if o == "ai" and gen[0] == "ai":
                        effective[key] = ("ai", rec.get("author"), "unreviewed")
                    elif cur is None:
                        effective[key] = (o, sid, ch) if o == "machine" and status == "auto" else gen
    return effective, len(files)


def check_images(rows, chapters):
    part_by_name = {name: prefix for prefix, _, name, _, _ in PARTS}
    path = os.path.join(ROOT, "images", "records.json")
    n = 0
    if os.path.exists(path):
        doc = load(path)
        recs = doc.get("records") if isinstance(doc, dict) else None
        if not isinstance(recs, list):
            err("images/records.json: expected an object with a \"records\" list")
            recs = []
        ids = set()
        for k, rec in enumerate(recs):
            where = f"images/records.json#{k}"
            missing = [key for key in IMAGE_KEYS if key not in rec]
            if missing:
                err(f"{where}: missing keys {missing}")
            if rec.get("id") in ids:
                err(f"{where}: duplicate id {rec.get('id')!r}")
            ids.add(rec.get("id"))
            prefix = part_by_name.get(rec.get("part"))
            if prefix is None:
                err(f"{where}: unknown part {rec.get('part')!r} (use {sorted(part_by_name)})")
            elif rec.get("chapter") not in chapters.get(prefix, set()):
                err(f"{where}: chapter {rec.get('chapter')!r} does not exist in {rec.get('part')}")
            for rid in rec.get("scene_rows") or []:
                if rid not in rows:
                    err(f"{where}: scene row {rid} does not exist")
            if rec.get("file") and not os.path.exists(os.path.join(ROOT, "images", "pd", rec["file"])):
                err(f"{where}: file images/pd/{rec['file']} not found")
            for key in ("width", "height", "file_width", "file_height"):
                if key in rec and not (isinstance(rec[key], int) and rec[key] > 0):
                    err(f"{where}: {key} must be a positive integer")
            if ("file_width" in rec) != ("file_height" in rec):
                err(f"{where}: file_width and file_height go together")
        n = len(recs)
        # density rule (images/README.md): one depiction slot per chapter, at most three documentary images per
        # chapter, about one placed image per twenty rows per part. Warnings only.
        per_ch, per_part = {}, {}
        for rec in recs:
            if not rec.get("placed", True):
                continue
            key = (rec.get("part"), rec.get("chapter"), rec.get("kind", "depiction") == "depiction")
            per_ch[key] = per_ch.get(key, 0) + 1
            per_part[rec.get("part")] = per_part.get(rec.get("part"), 0) + 1
        for (part, ch, is_dep), c in sorted(per_ch.items(), key=str):
            if (is_dep and c > 1) or (not is_dep and c > 3):
                warnings.append(f"images: {part} chapter {ch} has {c} {'depictions' if is_dep else 'documentary images'}")
        for prefix, _, part_name, _, _ in PARTS:
            nrows = sum(1 for r in rows if r.startswith(prefix + "-"))
            if nrows and per_part.get(part_name, 0) > max(3, round(nrows / 20 * 2)):
                warnings.append(f"images: {part_name} has {per_part[part_name]} images for {nrows} rows (at most {round(nrows / 10)})")
        total_rows, total_imgs = len(rows), sum(per_part.values())
        if total_rows and total_imgs > round(total_rows / 20 * 1.1):
            warnings.append(f"images: {total_imgs} placed images for {total_rows} rows (guide: about {round(total_rows / 20)})")
        unfilled = doc.get("unfilled") or {}
        if not isinstance(unfilled, dict):
            err("images/records.json: \"unfilled\" must be an object {slot id: reason}")
        else:
            for slot in unfilled:
                m = re.fullmatch(r"([pgsh])-c(\d+)", slot)
                if not m or int(m.group(2)) not in chapters.get(m.group(1), set()):
                    err(f"images/records.json: unfilled slot {slot!r} is not an existing chapter")
    scenes_path = os.path.join(ROOT, "images", "scenes.json")
    if os.path.exists(scenes_path):
        scenes = load(scenes_path)
        name_to_prefix = {sname: prefix for prefix, _, _, sname, _ in PARTS}
        for sname, chs in scenes.items():
            if sname.startswith("_"):
                continue
            prefix = name_to_prefix.get(sname)
            if prefix is None:
                err(f"images/scenes.json: unknown part key {sname!r}")
                continue
            for ch in chs:
                if int(ch) not in chapters.get(prefix, set()):
                    err(f"images/scenes.json: {sname} chapter {ch} does not exist")
    return n


ENTITY_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ENTITY_TAGS = ("god", "goddess", "giant", "dwarf", "elf", "valkyrie", "norn", "hero", "king", "poet", "animal", "horse",
               "monster", "object", "place_myth", "place_real", "river", "hall", "people", "poem", "event", "person", "other")
SEED_TYPES = ("god", "goddess", "giant", "dwarf", "elf", "valkyrie", "human", "character", "skald", "animal", "monster",
              "object", "place-myth", "place-legend", "place-real", "group", "work", "event", "other")
OK_LICENCE = re.compile(r"^(public domain|pd\b|cc0|cc by(-sa)?(\s|$))", re.I)


def poem_prefixes_for_intros():
    p = os.path.join(ROOT, "aligned", "poetic", "index.json")
    if not os.path.exists(p):
        return []
    idx = load(p)
    poems = idx.get("poems") if isinstance(idx, dict) else idx
    out = []
    for x in poems or []:
        if isinstance(x, dict) and x.get("prefix"):
            out.append(x["prefix"])
    return out


def check_intros(poem_prefixes):
    """intros/intros.json (task 22): one intro per part key (p g s h pm ph po) and one headnote per poem prefix; every
    text has en and is, a status, an author per language (ai:<model>-<yyyy-mm> for drafts) and a date."""
    p = os.path.join(ROOT, "intros", "intros.json")
    if not os.path.exists(p):
        return
    doc = load(p)
    parts, poems = doc.get("parts") or {}, doc.get("poems") or {}
    if set(parts) != {"p", "g", "s", "h", "pm", "ph", "po"}:
        err(f"intros/intros.json: parts must be p g s h pm ph po, got {sorted(parts)}")
    if poem_prefixes and set(poems) != set(poem_prefixes):
        err(f"intros/intros.json: poems differ from the aligned poems: missing {sorted(set(poem_prefixes) - set(poems))}, "
            f"extra {sorted(set(poems) - set(poem_prefixes))}")

    def check_rec(where, rec, keys):
        for k in keys:
            t = rec.get(k) or {}
            for lang in ("en", "is"):
                if not isinstance(t.get(lang), str) or not t[lang].strip():
                    err(f"intros/intros.json {where}: {k}.{lang} missing")
        if rec.get("status") not in ("draft", "reviewed"):
            err(f"intros/intros.json {where}: status must be draft or reviewed")
        for lang in ("en", "is"):
            a = (rec.get("author") or {}).get(lang, "")
            if not re.match(r"^(user:[\w-]+|ai:[\w.-]+-\d{4}-\d{2}|bot:[\w-]+)$", a):
                err(f"intros/intros.json {where}: author.{lang} {a!r} is not user:/ai:/bot:")
            if a.startswith("ai:") and rec.get("status") == "reviewed":
                err(f"intros/intros.json {where}: an AI text cannot be reviewed without a user: reviewer")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", rec.get("date", "")):
            err(f"intros/intros.json {where}: date missing")
    for k, rec in parts.items():
        if not rec.get("title"):
            err(f"intros/intros.json parts.{k}: title missing")
        check_rec(f"parts.{k}", rec, ("intro", "note"))
    for k, rec in poems.items():
        check_rec(f"poems.{k}", rec, ("headnote",))


def check_ravens(rows):
    """images/ravens/ (decision of 2026-11-01): index.json names a public-domain source with a licence check, and every
    listed file exists with the recorded size."""
    p = os.path.join(ROOT, "images", "ravens", "index.json")
    if not os.path.exists(p):
        return
    doc = load(p)
    src = doc.get("source") or {}
    for k in ("commons_file", "page", "artist", "licence", "license_basis", "checked_by"):
        if not src.get(k):
            err(f"images/ravens/index.json: source.{k} missing")
    if src.get("licence") not in ("Public domain", "CC0 1.0", "CC BY 4.0", "CC BY-SA 4.0"):
        err(f"images/ravens/index.json: licence {src.get('licence')!r} is not public domain or CC0/BY/BY-SA")
    for name, rec in (doc.get("files") or {}).items():
        f = os.path.join(ROOT, "images", "ravens", name)
        if not os.path.exists(f):
            err(f"images/ravens/{name}: listed in index.json but missing")
        elif os.path.getsize(f) != rec.get("bytes"):
            err(f"images/ravens/{name}: size differs from index.json")
    if not any(n.startswith("huginn-head-") for n in doc.get("files") or {}) or not any(n.startswith("muninn-") for n in doc.get("files") or {}):
        err("images/ravens/index.json: needs a huginn-head-* badge and a muninn-* file")


def check_worlds(rows):
    """images/worlds/ (task 20): realms.json ids are entities, anchors are keys of the anchors file or in-picture
    coordinates, cited rows exist; diagrams.json files exist and passed the licence check; bg/index.json files exist."""
    wd = os.path.join(ROOT, "images", "worlds")
    if not os.path.isdir(wd):
        return
    ents = set()
    ep = os.path.join(ROOT, "entities", "entities.json")
    if os.path.exists(ep):
        e = load(ep).get("entities", {})
        ents = set(e) if isinstance(e, dict) else {x["id"] for x in e}
    rp = os.path.join(wd, "realms.json")
    if os.path.exists(rp):
        doc = load(rp)
        anchors, size = {}, [1, 1]
        ap = os.path.join(wd, doc.get("anchors") or "anchors-v3.json")   # realms.json names the anchors file of the current picture
        if not os.path.exists(ap):
            err(f"images/worlds/realms.json: anchors file {os.path.basename(ap)!r} missing")
        if os.path.exists(ap):
            a = load(ap)
            anchors, size = a.get("anchors", {}), a.get("size", [1, 1])
        groups = {g["id"] for g in doc.get("groups", [])}
        seen = set()
        for r in doc.get("realms", []):
            rid = r.get("id") or ""
            where = f"images/worlds/realms.json#{rid}"
            if rid in seen:
                err(f"{where}: repeated")
            seen.add(rid)
            if ents and rid not in ents:
                err(f"{where}: not an entity")
            a = r.get("anchor")
            if isinstance(a, str) and a not in anchors:
                err(f"{where}: anchor {a!r} is not in {os.path.basename(ap)}")
            elif isinstance(a, list) and not (len(a) == 2 and 0 <= a[0] <= size[0] and 0 <= a[1] <= size[1]):
                err(f"{where}: anchor {a!r} is outside the picture")
            if r.get("group") and r["group"] not in groups:
                err(f"{where}: unknown group {r['group']!r}")
            if not (r.get("desc") or {}).get("en"):
                err(f"{where}: no English description")
            if not (r.get("label_en") or "").strip():
                err(f"{where}: no English name (label_en)")
            for c in r.get("cites", []):
                if c.get("row") not in rows:
                    err(f"{where}: cited row {c.get('row')!r} does not exist")
    dp = os.path.join(wd, "diagrams.json")
    if os.path.exists(dp):
        for d in load(dp).get("diagrams", []):
            where = f"images/worlds/diagrams.json#{d.get('slug')}"
            c = d.get("check") or {}
            if d.get("file"):
                if not c.get("ok"):
                    err(f"{where}: has a file but the licence check did not pass")
                if not os.path.exists(os.path.join(wd, d["file"])):
                    err(f"{where}: file {d['file']!r} missing")
            if not (d.get("caption") or {}).get("en"):
                err(f"{where}: no English caption")
    bp = os.path.join(wd, "bg", "index.json")
    if os.path.exists(bp):
        b = load(bp)
        # decision 2026-11-02: credited to the maintainer (CC BY 4.0), no AI label on the page; the provenance
        # (how the picture was made) must stay recorded in made_with
        if not b.get("made_with"):
            err("images/worlds/bg/index.json: made_with must record how the background was made")
        if b.get("licence") not in ("CC BY 4.0", "CC0 1.0"):
            err(f"images/worlds/bg/index.json: licence {b.get('licence')!r} is not CC BY 4.0 or CC0 1.0")
        for name in b.get("files", {}):
            if not os.path.exists(os.path.join(wd, "bg", name)):
                err(f"images/worlds/bg/{name}: missing")


def check_paths(rows):
    """paths/paths.json (task 19a): unique ids, every step a chapter, chapter range, poem or row that exists."""
    p = os.path.join(ROOT, "paths", "paths.json")
    if not os.path.exists(p):
        return
    doc = load(p)
    chapters = {re.sub(r"^([pgsh])-c(\d+)-.*$", r"\1-ch\2", r) for r in rows if re.match(r"^[pgsh]-c\d+-", r)}
    poems = {r.split("-")[0] + "-poem" for r, v in rows.items() if v.get("poem")}
    seen = set()
    for path in doc.get("paths", []):
        pid = path.get("id") or ""
        where = f"paths/paths.json#{pid}"
        if not re.match(r"^[a-z][a-z0-9-]*$", pid) or pid in seen:
            err(f"{where}: bad or repeated id")
        seen.add(pid)
        for k in ("title", "time"):
            if not (path.get(k) or {}).get("en"):
                err(f"{where}: no English {k}")
        tp = os.path.join(ROOT, "guide", "paths.json")
        tours = set(load(tp).get("paths", {})) if os.path.exists(tp) else set()
        for x in path.get("tours", []):
            if x not in tours:
                err(f"{where}: tour {x!r} is not a Mímir tour in guide/paths.json")
        for i, st in enumerate(path.get("steps", []), 1):
            ref, to = st.get("ref") or "", st.get("to")
            if not (ref in rows or ref in chapters or ref in poems):
                err(f"{where} step {i}: {ref!r} is not a row, chapter or poem id")
            if to is not None:
                a, b = re.match(r"^([pgsh])-ch(\d+)$", ref), re.match(r"^([pgsh])-ch(\d+)$", to)
                if not (a and b and a.group(1) == b.group(1) and int(b.group(2)) > int(a.group(2))):
                    err(f"{where} step {i}: range {ref!r}..{to!r} must be chapters of one part in rising order")
                elif to not in chapters:
                    err(f"{where} step {i}: {to!r} is not a chapter id")
            if not (st.get("note") or {}).get("en"):
                err(f"{where} step {i}: no English note")


def check_entities(rows):
    """entities/: the curated seed, the hand rules and the generated files (edda-site/pipeline/make_entities.py)."""
    d = os.path.join(ROOT, "entities")
    if not os.path.isdir(d):
        return 0, 0
    ids = set()
    seed_path = os.path.join(d, "seed.json")
    if os.path.exists(seed_path):
        seed = load(seed_path)
        for e in seed.get("entities", []):
            where = f"entities/seed.json#{e.get('id')}"
            if not isinstance(e.get("id"), str) or not ENTITY_ID.match(e["id"]):
                err(f"{where}: id must be a lowercase slug")
            elif e["id"] in ids:
                err(f"{where}: duplicate id")
            ids.add(e.get("id"))
            if e.get("type") not in SEED_TYPES:
                err(f"{where}: type {e.get('type')!r} unknown")
            if e.get("wikidata") is not None and not re.match(r"^Q\d+$", str(e["wikidata"])):
                err(f"{where}: wikidata must be null or Q<number>")
            if not isinstance(e.get("names"), dict) or not e["names"]:
                err(f"{where}: names must be a non-empty object")
            if not isinstance(e.get("forms"), dict):
                err(f"{where}: forms must be an object form -> count")
    rules_path = os.path.join(d, "rules.json")
    if os.path.exists(rules_path):
        rules = load(rules_path)
        for e in rules.get("extra", []):
            where = f"entities/rules.json extra {e.get('id')}"
            if not isinstance(e.get("id"), str) or not ENTITY_ID.match(e["id"]):
                err(f"{where}: id must be a lowercase slug")
            elif e["id"] in ids:
                err(f"{where}: id already in seed.json")
            ids.add(e.get("id"))
            if not e.get("tags") or any(t not in ENTITY_TAGS for t in e["tags"]):
                err(f"{where}: tags must be from the vocabulary")
        for eid, tags in rules.get("tags", {}).items():
            if eid not in ids:
                err(f"entities/rules.json tags: unknown entity {eid!r}")
            if not tags or any(t not in ENTITY_TAGS for t in tags):
                err(f"entities/rules.json tags {eid}: tags must be from the vocabulary")
        for eid, rule in rules.get("resolve", {}).get("entities", {}).items():
            if eid not in ids:
                err(f"entities/rules.json resolve.entities: unknown entity {eid!r}")
            for sc, v in rule.items():
                vals = list(v.values()) if isinstance(v, dict) else [v]
                for x in vals:
                    if x not in ("ok", "check", "skip") and x not in ids:
                        err(f"entities/rules.json resolve.entities {eid} [{sc}]: unknown target {x!r}")
        for form, rule in rules.get("resolve", {}).get("forms", {}).items():
            for sc, v in rule.items():
                vals = list(v.values()) if isinstance(v, dict) else [v]
                for x in vals:
                    if x not in ("ok", "check", "skip") and x not in ids:
                        err(f"entities/rules.json resolve.forms {form} [{sc}]: unknown target {x!r}")
        for eid, near in rules.get("resolve", {}).get("near", {}).items():
            if eid not in ids:
                err(f"entities/rules.json resolve.near: unknown entity {eid!r}")
            for word, x in near.items():
                if x not in ids:
                    err(f"entities/rules.json resolve.near {eid} {word}: unknown target {x!r}")
        for sc in rules.get("lists", []):
            if not (sc in rows or re.match(r"^[pgsh]-c\d+$", sc) or re.match(r"^[a-z0-9]+$", sc)):
                err(f"entities/rules.json lists: {sc!r} is not a row, chapter or poem scope")
    notable_path = os.path.join(d, "notable.json")
    if os.path.exists(notable_path):
        for eid in load(notable_path).get("ids", []):
            if eid not in ids:
                warnings.append(f"entities/notable.json: {eid!r} is not an entity (yet)")
    images = {}
    images_path = os.path.join(d, "images.json")
    if os.path.exists(images_path):
        images = load(images_path).get("images", {})
        for f, rec in images.items():
            if rec.get("ok") and not OK_LICENCE.match(rec.get("licence") or ""):
                err(f"entities/images.json {f}: marked ok but licence {rec.get('licence')!r} is not PD / CC0 / CC BY / CC BY-SA")
    n_ent = n_men = 0
    ent_path = os.path.join(d, "entities.json")
    if os.path.exists(ent_path):
        doc = load(ent_path)
        seen = set()
        for e in doc.get("entities", []):
            n_ent += 1
            where = f"entities/entities.json#{e.get('id')}"
            if e.get("id") in seen:
                err(f"{where}: duplicate id")
            seen.add(e.get("id"))
            if e.get("id") not in ids:
                err(f"{where}: not in seed.json or rules.json (regenerate)")
            if not e.get("tags") or any(t not in ENTITY_TAGS for t in e["tags"]) or e.get("type") != e["tags"][0]:
                err(f"{where}: tags must be from the vocabulary and type = tags[0]")
            if e.get("status") != "auto":
                err(f"{where}: status must be auto (entities are not reviewed yet)")
            if e.get("image") and not images.get(e["image"], {}).get("ok"):
                err(f"{where}: image {e['image']!r} has not passed the licence check in images.json")
            for book, rid in list((e.get("first") or {}).items()) + list((e.get("first_any") or {}).items()):
                if rid not in rows:
                    err(f"{where}: first mention row {rid!r} does not exist")
        ids_out = seen
    else:
        ids_out = ids
    men_path = os.path.join(d, "mentions.json")
    if os.path.exists(men_path):
        for i, m in enumerate(load(men_path).get("mentions", [])):
            n_men += 1
            if m.get("entity") not in ids_out:
                err(f"entities/mentions.json[{i}]: unknown entity {m.get('entity')!r}")
            if m.get("row") not in rows:
                err(f"entities/mentions.json[{i}]: unknown row {m.get('row')!r}")
            if m.get("lang") not in CELLS:
                err(f"entities/mentions.json[{i}]: unknown lang {m.get('lang')!r}")
            if not m.get("form") or m.get("kind") not in ("name", "heiti", "kenning") or m.get("status") != "auto":
                err(f"entities/mentions.json[{i}]: needs form, kind in name/heiti/kenning, status auto")
    co_path = os.path.join(d, "coords.json")
    pl_path = os.path.join(d, "places.json")
    places = load(pl_path).get("places", {}) if os.path.exists(pl_path) else {}
    for eid in places:
        if eid not in ids_out:
            err(f"entities/places.json: {eid!r} is not an entity")
    if os.path.exists(co_path):
        for eid, rec in load(co_path).get("places", {}).items():
            where = f"entities/coords.json#{eid}"
            if eid not in ids_out:
                err(f"{where}: unknown entity")
            if not isinstance(rec.get("lat"), (int, float)) or not -90 <= rec["lat"] <= 90 \
                    or not isinstance(rec.get("lon"), (int, float)) or not -180 <= rec["lon"] <= 180:
                err(f"{where}: bad coordinates {rec.get('lat')!r}, {rec.get('lon')!r}")
            if not re.match(r"^Q\d+$", rec.get("wikidata") or ""):
                err(f"{where}: no Wikidata id")
            pinned = places.get(eid, {}).get("wikidata")
            if pinned and pinned != rec["wikidata"]:
                err(f"{where}: {rec['wikidata']} but places.json pins {pinned}; rerun make_entities.py coords")
    img_idx = os.path.join(d, "img", "index.json")
    if os.path.exists(img_idx):
        for eid, rec in load(img_idx).get("images", {}).items():
            where = f"entities/img/index.json#{eid}"
            if eid not in ids_out:
                err(f"{where}: unknown entity")
            if not rec.get("file") or not os.path.exists(os.path.join(d, "img", rec["file"])):
                err(f"{where}: file {rec.get('file')!r} missing")
            if not images.get(rec.get("source") or "", {}).get("ok"):
                err(f"{where}: source {rec.get('source')!r} has not passed the licence check in images.json")
    check_summaries(d, ids_out)
    return n_ent, n_men


AUTHOR = re.compile(r"^(user:[\w-]+|ai:[\w.-]+-\d{4}-\d{2}|bot:[\w-]+)$")


def check_summaries(d, ids_out):
    """entities/summaries.json: {"summaries": {entity id: {"en": text, "is": text (optional), "by": author or {lang: author},
    "date": YYYY-MM-DD, "status": draft|reviewed, "reviewed_by": user:... (needed to mark an AI text reviewed)}}}.
    Plain text (paragraphs separated by a blank line), no markup."""
    p = os.path.join(d, "summaries.json")
    if not os.path.exists(p):
        return
    for eid, rec in (load(p).get("summaries") or {}).items():
        where = f"entities/summaries.json#{eid}"
        if eid not in ids_out:
            err(f"{where}: unknown entity")
        if not isinstance(rec.get("en"), str) or not rec["en"].strip():
            err(f"{where}: en missing")
        langs = [lang for lang in ("en", "is") if rec.get(lang)]
        for lang in langs:
            t = rec[lang]
            if not isinstance(t, str) or re.search(r"<[a-zA-Z/]|\[\[|\*\*", t):
                err(f"{where}: {lang} must be plain text (no HTML or markdown)")
            elif re.search("[\U0001F000-\U0001FAFF☀-➿]", t):
                err(f"{where}: {lang} contains an emoji")
        set_keys = set(rec) - {"en", "is", "by", "date", "status", "reviewed_by", "note"}
        if set_keys:
            err(f"{where}: unknown keys {sorted(set_keys)}")
        by = rec.get("by")
        for lang in langs:
            a = by.get(lang, "") if isinstance(by, dict) else (by or "")
            if not AUTHOR.match(a):
                err(f"{where}: by ({lang}) {a!r} is not user:/ai:<model>-<yyyy-mm>/bot:")
            if a.startswith("ai:") and rec.get("status") == "reviewed" and not str(rec.get("reviewed_by", "")).startswith("user:"):
                err(f"{where}: an AI text cannot be reviewed without a user: reviewer (reviewed_by)")
        if rec.get("status") not in ("draft", "reviewed"):
            err(f"{where}: status must be draft or reviewed")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", rec.get("date") or ""):
            err(f"{where}: date must be YYYY-MM-DD")


def check_tiles():
    """images/tiles.json (where each Mímir tile looks): every id an entity, one of head [x, y, h] / region [x0, y0, x1, y1]
    / pad, fractions in 0..1; every tile written to images/tiles/ (make_plates.py)."""
    tp = os.path.join(ROOT, "images", "tiles.json")
    if not os.path.exists(tp):
        return
    ents = {e["id"] for e in load(os.path.join(ROOT, "entities", "entities.json")).get("entities", [])}
    ip = os.path.join(ROOT, "images", "tiles", "index.json")
    made = set(load(ip).get("tiles", {})) if os.path.exists(ip) else set()
    for eid, f in load(tp).get("tiles", {}).items():
        if eid not in ents:
            err(f"images/tiles.json: {eid} is not an entity")
        vals = f.get("head") or f.get("region")
        if not vals and not f.get("pad"):
            err(f"images/tiles.json: {eid} has no head, region or pad")
        elif vals and (len(vals) != (3 if "head" in f else 4) or not all(0 <= v <= 1 for v in vals)):
            err(f"images/tiles.json: {eid}: bad focus {vals}")
        if eid not in made:
            err(f"images/tiles.json: {eid} has no tile in images/tiles/ (run edda-site/pipeline/make_plates.py)")


def check_portraits():
    """images/portraits/: every subject of briefs.json an entity with a known kind, pairs named from both sides, every
    reference cut-out there; every portrait <id>.jpg and every pick an entity; every portrait has its web copies."""
    pd = os.path.join(ROOT, "images", "portraits")
    bp = os.path.join(pd, "briefs.json")
    if not os.path.exists(bp):
        return
    ents = {e["id"] for e in load(os.path.join(ROOT, "entities", "entities.json")).get("entities", [])}
    br = load(bp)
    subj = br.get("subjects", {})
    for eid, s in subj.items():
        if eid not in ents:
            err(f"images/portraits/briefs.json: {eid} is not an entity")
        if s.get("kind") not in br.get("format", {}) or not s.get("subject"):
            err(f"images/portraits/briefs.json: {eid} needs a kind ({', '.join(br.get('format', {}))}) and a subject")
        if s.get("ref") and not os.path.exists(os.path.join(pd, "ref", f"{eid}.jpg")):
            err(f"images/portraits/briefs.json: {eid} has no reference ref/{eid}.jpg")
        for a, b in (("pair", "pair_of"), ("pair_of", "pair")):
            if s.get(a) and (subj.get(s[a]) or {}).get(b) != eid:
                err(f"images/portraits/briefs.json: {eid} {a} {s[a]}, which does not name it back")
        if (s.get("pair") or s.get("pair_of")) and not s.get("differs"):
            err(f"images/portraits/briefs.json: {eid} is one of a pair and needs 'differs'")
    for name, members in br.get("sets", {}).items():
        for m in members:
            if (subj.get(m) or {}).get("set") != name or not subj[m].get("differs"):
                err(f"images/portraits/briefs.json: set {name}: {m} must carry set and differs")
    for eid, s in subj.items():
        if s.get("set") and eid not in br.get("sets", {}).get(s["set"], []):
            err(f"images/portraits/briefs.json: {eid} names the set {s['set']}, which does not list it")
    for eid in br.get("test", []):
        if eid not in subj:
            err(f"images/portraits/briefs.json: test subject {eid} has no brief")
    tp = os.path.join(ROOT, "images", "tiles", "index.json")
    made = {k for k, v in (load(tp).get("tiles", {}) if os.path.exists(tp) else {}).items() if v.get("source") == "portrait"}
    lights = set(br.get("lights", {}))
    for f in os.listdir(pd):
        m = re.fullmatch(r"([a-z0-9-]+)(?:@([a-z-]+))?\.(jpg|jpeg|png)", f)
        if not m:
            continue
        if m.group(1) not in ents:
            err(f"images/portraits/{f}: {m.group(1)} is not an entity")
        elif m.group(2) and m.group(2) not in lights:
            err(f"images/portraits/{f}: {m.group(2)} is not a light in briefs.json ({', '.join(sorted(lights))})")
        elif m.group(2) and not os.path.exists(os.path.join(pd, f"{m.group(1)}.jpg")):
            err(f"images/portraits/{f}: there is no day picture {m.group(1)}.jpg")
        elif m.group(1) not in made:
            err(f"images/portraits/{f} has no tiles (run edda-site/pipeline/make_plates.py)")
    kp = os.path.join(pd, "picks.json")
    for eid in (load(kp).get("picks", {}) if os.path.exists(kp) else {}):
        if not any(os.path.exists(os.path.join(pd, f"{eid}.{x}")) for x in ("jpg", "jpeg", "png")):
            err(f"images/portraits/picks.json: {eid} is chosen but images/portraits/{eid}.jpg is not there")


def check_pron():
    """guide/pron.json (Mímir pronunciation hints): every card id is a card, every hint has head, ipa and say, every
    section id is a section."""
    pp = os.path.join(ROOT, "guide", "pron.json")
    if not os.path.exists(pp):
        return
    pron = load(pp)
    cards = set(load(os.path.join(ROOT, "guide", "cards.json")).get("cards", {}))
    secs = {s["id"] for s in load(os.path.join(ROOT, "guide", "sections.json")).get("sections", [])}
    hints = [(f"cards.{k}", v) for k, v in pron.get("cards", {}).items()] + [(f"terms.{k}", v) for k, v in pron.get("terms", {}).items()]
    for k in pron.get("cards", {}):
        if k not in cards:
            err(f"guide/pron.json: cards.{k} is not a card in guide/cards.json")
    for k, vv in pron.get("sections", {}).items():
        if k not in secs:
            err(f"guide/pron.json: sections.{k} is not a section in guide/sections.json")
        hints += [(f"sections.{k}", v) for v in vv]
    for where, v in hints:
        missing = [f for f in ("head", "ipa", "say") if not v.get(f)]
        if missing:
            err(f"guide/pron.json: {where} lacks {', '.join(missing)}")


def check_pictures():
    """images/plates/pN.anchors.json and images/mimir/mimir.anchors.json (Mímir, task 34): the picture is there, every
    entity exists, every box lies inside the picture, part_of names a figure of the same plate, a scene's story is a story."""
    ep = os.path.join(ROOT, "entities", "entities.json")
    ents = {e["id"] for e in load(ep).get("entities", [])} if os.path.exists(ep) else set()
    sp = os.path.join(ROOT, "guide", "stories.json")
    stories = set(load(sp).get("stories", {})) if os.path.exists(sp) else set()
    n = 0
    for sub, key in (("plates", "figures"), ("mimir", "scenes")):
        d = os.path.join(ROOT, "images", sub)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".anchors.json"):
                continue
            where, a = f"images/{sub}/{name}", load(os.path.join(d, name))
            if not os.path.exists(os.path.join(d, a.get("image", ""))):
                err(f"{where}: image {a.get('image')!r} is missing")
            W, H = a.get("size", [0, 0])
            figs = {f["entity"] for f in a.get(key, [])}
            for f in a.get(key, []):
                n += 1
                if f["entity"] not in ents:
                    err(f"{where}: entity {f['entity']!r} does not exist")
                x, y, w, h = f["bbox"]
                if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > W or y + h > H:
                    err(f"{where}: {f['entity']} box {f['bbox']} is outside the picture {W}x{H}")
                if f.get("part_of") and f["part_of"] not in figs:
                    err(f"{where}: {f['entity']} part_of {f['part_of']!r} is not on this plate")
                if f.get("story") and stories and f["story"] not in stories:
                    err(f"{where}: story {f['story']!r} is not in guide/stories.json")
            for x in a.get("stories") or []:
                if stories and x not in stories:
                    err(f"{where}: stories: {x!r} is not in guide/stories.json")
            ap = os.path.join(ROOT, "guide", "ages.json")
            for x in a.get("ages") or []:
                if os.path.exists(ap) and x not in load(ap).get("ages", {}):
                    err(f"{where}: ages: {x!r} is not in guide/ages.json")
    return n


def check_guide(rows):
    """guide/ (Mímir, task 34): every passage ref is a row id, every entity id exists, every fact and story step has
    a passage, relations use the known kinds, and stories, ages, myths, outside entries and paths point at things
    that exist. Collections are objects keyed by id (cards, stories, myths, outside, paths, ages) or lists (sections,
    relations)."""
    gd = os.path.join(ROOT, "guide")
    if not os.path.isdir(gd):
        return 0
    ep = os.path.join(ROOT, "entities", "entities.json")
    ents = {e["id"] for e in load(ep).get("entities", [])} if os.path.exists(ep) else set()

    def g(name, key, default):
        p = os.path.join(gd, name)
        return load(p).get(key, default) if os.path.exists(p) else default

    def refs(where, rr):
        for r in rr or []:
            if r not in rows:
                err(f"guide/{where}: ref {r!r} is not a row id")

    def ent(where, e):
        if e not in ents:
            err(f"guide/{where}: entity {e!r} does not exist")
    cards, stories, ages = g("cards.json", "cards", {}), g("stories.json", "stories", {}), g("ages.json", "ages", {})
    myths, sections, outside = g("myths.json", "myths", {}), g("sections.json", "sections", []), g("outside.json", "outside", {})
    paths, relations = g("paths.json", "paths", {}), g("relations.json", "relations", [])
    pi = os.path.join(ROOT, "images", "plates", "index.json")
    plates = set(load(pi).get("plates", {})) if os.path.exists(pi) else set()
    for sec in sections:
        refs(f"sections.json#{sec['id']}", sec.get("refs"))
        for e in sec.get("entities", []) + sec.get("more", []):
            ent(f"sections.json#{sec['id']}", e)
            if e not in cards:
                err(f"guide/sections.json#{sec['id']}: {e!r} has no card")
    for cid, c in cards.items():
        where = f"cards.json#{cid}"
        ent(where, cid)
        if c.get("status") not in ("draft", "reviewed"):
            err(f"guide/{where}: status must be draft or reviewed")
        if not (c.get("hook") or {}).get("en"):
            err(f"guide/{where}: no English hook")
        for f in c.get("facts", []):
            if not f.get("refs"):
                err(f"guide/{where}: fact {f.get('label', {}).get('en')!r} has no passage")
            refs(where, f.get("refs"))
            for e in f.get("ids", []):
                ent(where, e)
        refs(where, [b["row"] for b in c.get("best", [])])
        for r in c.get("related", []):
            ent(where, r["id"])
            for k in [r.get("rel")] + list(r.get("also", [])):
                if k not in CARD_RELS:
                    err(f"guide/{where}: related kind {k!r} is not known")
        if c.get("plate") and c["plate"] not in plates:   # a group's card shows its section's plate (images/plates/index.json)
            err(f"guide/{where}: plate {c['plate']!r} is not in images/plates/index.json")
        for m in c.get("myths", []):
            if m not in myths:
                err(f"guide/{where}: myth {m!r} not in myths.json")
        for s in c.get("stories", []):
            if s not in stories:
                err(f"guide/{where}: story {s!r} not in stories.json")
    placed = [e for sec in sections for e in sec.get("entities", []) + sec.get("more", [])]
    more = [e for sec in sections for e in sec.get("more", [])]
    for cid in cards:   # a main card may stand in two sections (Sleipnir: Loki's children and the mounts)
        if sections and cid not in placed:
            err(f"guide/sections.json: card {cid!r} is in no section")
        if cid in more and placed.count(cid) > 1:
            err(f"guide/sections.json: short card {cid!r} is listed more than once")
    for cid, c in cards.items():   # a link between two cards is there on both, so a reader can always go back
        for r in c.get("related", []):
            if r["id"] in cards and not any(x["id"] == cid for x in cards[r["id"]].get("related", [])):
                err(f"guide/cards.json#{cid}: related {r['id']!r} has no link back")
    for sid, s in stories.items():
        where = f"stories.json#{sid}"
        if s.get("age") not in ages:
            err(f"guide/{where}: age {s.get('age')!r} not in ages.json")
        for st in s.get("steps", []):
            if not st.get("refs"):
                err(f"guide/{where}: a step without a passage")
            refs(where, st.get("refs"))
        refs(where, [b["row"] for b in s.get("best", [])])
        for e in s.get("participants", []):
            ent(where, e)
        for k in ("before", "after"):
            for x in s.get(k) or []:
                if x not in stories:
                    err(f"guide/{where}: {k} {x!r} is not a story")
    for aid, a in ages.items():
        refs(f"ages.json#{aid}", a.get("refs"))
        for x in a.get("stories", []):
            if x not in stories:
                err(f"guide/ages.json#{aid}: story {x!r} is not a story")
    for mid, m in myths.items():
        refs(f"myths.json#{mid}", m.get("refs"))
        for e in m.get("entities", []):
            ent(f"myths.json#{mid}", e)
        for o in m.get("outside", []):
            if o not in outside:
                err(f"guide/myths.json#{mid}: outside {o!r} not in outside.json")
    for oid, o in outside.items():
        refs(f"outside.json#{oid}", o.get("refs"))
        if o.get("kind") not in ("source", "reception"):
            err(f"guide/outside.json#{oid}: kind must be source or reception")
    for r in relations:
        for e in (r["from"], r["to"]):
            ent("relations.json", e)
        if r.get("rel") not in RELS:
            err(f"guide/relations.json: kind {r.get('rel')!r} is not known")
        refs("relations.json", r.get("refs"))
    for pid, p in paths.items():
        for st in p.get("items", []):
            ok = st["id"] in cards if st["kind"] == "card" else st["id"] in stories
            if not ok:
                err(f"guide/paths.json#{pid}: {st['kind']} {st['id']!r} does not exist")
    return len(cards)


RELS = {"child_of", "spouse", "sibling", "foster_child_of", "killed", "owns", "rides", "fights", "bound", "swallows",
        "chases", "lives_in", "servant_of", "made", "lover", "same_as"}
CARD_RELS = RELS | {"parent_of", "foster_parent_of", "killed_by", "owned_by", "ridden_by", "bound_by", "swallowed_by",
                    "chased_by", "home_of", "master_of", "made_by", "companion"}


def cell_props(rid, r, cell, effective, src):
    """(origin, source, check) of a cell: the overlay result or the generated default; (None, None, None) when empty."""
    if (rid, cell) in effective:
        return effective[(rid, cell)]
    return generated_origin(rid, r, src)(cell)


def status_table(rows, effective, src):
    """Three tables per part and column: origin, check, and the old one-word summary."""
    tables = {"origin": ORIGINS + ("empty",), "check": CHECKS + ("empty",),
              "status (old one-word form)": ("source", "auto", "draft", "reviewed", "disputed", "empty")}
    groups = [(prefix, display, lambda rid, p=prefix: rid.split("-")[0] == p) for prefix, _, _, _, display in PARTS]
    groups.append(("poetic", "Poetic Edda", lambda rid: rows[rid].get("poem", False)))
    out = {}
    for title, cols in tables.items():
        table = []
        for prefix, display, member in groups:
            present = [c for c in CELLS if any(rows[r][c] for r in rows if member(r))]
            for cell in present:
                counts = dict.fromkeys(cols, 0)
                for rid, r in rows.items():
                    if not member(rid):
                        continue
                    o, sid, ch = cell_props(rid, r, cell, effective, src)
                    if o is None:
                        k = "empty"
                    elif title == "origin":
                        k = o
                    elif title == "check":
                        k = ch
                    else:
                        k = legacy_status(o, ch, None)
                    counts[k] += 1
                table.append((display, cell, counts))
        w = max(len(d) for d, _, _ in table)
        cw = max(9, max(len(c) for c in cols) + 2)
        head = f"{'part':<{w}}  col  " + "".join(f"{c:>{cw}}" for c in cols) + "    total"
        print(f"[{title}]")
        print(head)
        print("-" * len(head))
        for display, cell, counts in table:
            total = sum(counts.values())
            print(f"{display:<{w}}  {cell:<4} " + "".join(f"{counts[c]:>{cw}}" for c in cols) + f"  {total:>7}")
        print()
        out[title] = table
    return out


def main():
    rows, chapters = check_aligned()
    src = load_sources()
    effective, n_overlay_files = check_overlays(rows, src)
    n_images = check_images(rows, chapters)
    n_links = check_links(rows, chapters)
    n_ent, n_men = check_entities(rows)
    check_paths(rows)
    check_worlds(rows)
    check_guide(rows)
    check_pictures()
    check_pron()
    check_tiles()
    check_portraits()
    check_ravens(rows)
    check_intros(poem_prefixes_for_intros())
    print(f"aligned rows: {len(rows)} in {len(chapters)} parts; overlay files: {n_overlay_files}, "
          f"overlay cells: {len(effective)}; image records: {n_images}; quotation links: {n_links}; "
          f"entities: {n_ent}, mentions: {n_men}\n")
    status_table(rows, effective, src)
    print("origin: edition = base text, published = a published human text (aligned automatically unless checked), "
          "machine = automatic spelling, ai = AI draft, contributor = written through the edit flow. "
          "check: aligned-auto / aligned-checked for published text (the placement), unreviewed / reviewed for the "
          "rest (the words), disputed = reviewers disagree. empty = no text in this cell.")
    for w in warnings:
        print("warning: " + w)
    if errors:
        print(f"\n{len(errors)} error(s):", file=sys.stderr)
        for e in errors[:200]:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    print("\nOK")


if __name__ == "__main__":
    main()
