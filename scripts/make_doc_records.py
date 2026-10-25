"""Add documentary image records (manuscripts, monuments, places; PD / CC0 / CC BY / CC BY-SA) to
images/records.json. Metadata comes from the Wikimedia Commons API (images/doc_meta.json, read 2026-10-25).
Usage: python -I make_doc_records.py images/records.json images/doc_meta.json"""
import json
import sys

PARTS = {"p": "prologue", "g": "gylfaginning", "s": "skaldskaparmal", "h": "hattatal"}
CHECKED = "claude (Commons API metadata check, 2026-10-25); human verification pending"

# id, kind, Commons file, title, caption (what it is and why it is here), date of the object/photo
DOC = [
 ("p-c1-d1", "manuscript", "Edda.jpg", "Title page of a Prose Edda manuscript (ÍB 299 4to)",
  "Title page of an 18th-century Icelandic Edda manuscript, ÍB 299 4to, f. 58r (National Library of Iceland): Odin, Heimdallr, Sleipnir and others", "18th century"),
 ("g-c38-d1", "monument", "Bildsten 800 - 1099 i Tjängvide, Gotland.jpg", "Tjängvide picture stone",
  "Tjängvide picture stone, Gotland (Historiska museet): a rider on an eight-legged horse is welcomed with a drinking horn, often read as arrival in Valhöll", "8th–9th century"),
 ("g-c43-d1", "monument", "Oseberg ship - IMG 9186.jpg", "The Oseberg ship",
  "The Oseberg ship (c. 820), Viking Ship Museum, Oslo — the kind of ship Skíðblaðnir is the ideal of", "c. 820; photo 2009"),
 ("g-c48-d1", "monument", "Altunastenen U 1161 (Raä-nr Altuna 42-1) Tors fiskafänge 0445.jpg", "Thor's fishing on the Altuna stone",
  "Thor in the boat with the Midgard Serpent on his line, Altuna runestone (U 1161), Uppland", "11th century; photo 2010"),
 ("g-c50-d1", "monument", "Gosforth Cross.jpg", "The Gosforth Cross",
  "The Gosforth Cross, Cumbria (10th century), whose carvings include a bound figure read as Loki with Sigyn", "10th century; photo 2006"),
 ("g-c51-d1", "monument", "Ledbergsstenen 2.jpg", "The Ledberg stone",
  "Ledberg runestone (Ög 181), Östergötland: a figure whose leg is in a wolf's jaws, often read as Odin and Fenrir at Ragnarök", "11th century; photo 2006"),
 ("s-c5-d1", "monument", "Drinking horns.jpg", "Viking-age drinking horns",
  "Viking-age drinking horns — the vessels of the mead of poetry's kennings", "Viking age; photo 2006"),
 ("s-c9-d1", "monument", "Ardre picture stone VIII.jpg", "Ardre picture stone VIII",
  "Ardre picture stone VIII, Gotland (Historiska museet), with an eight-legged horse among its scenes", "8th century; photo 2008"),
 ("s-c10-d1", "manuscript", "CodexWormianus AM 242 fol, bl. 13r.jpg", "Codex Wormianus, AM 242 fol., f. 13r",
  "Codex Wormianus (AM 242 fol.), one of the four main manuscripts of Snorri's Edda, f. 13r", "14th century"),
 ("s-c11-d1", "monument", "Bronzestatue „Christ or Thor“ aus dem isländischen Nationalmuseum.jpg", "The Eyrarland statue",
  "The Eyrarland bronze (c. 1000), National Museum of Iceland: a seated figure gripping a hammer-like object, usually identified as Thor", "c. 1000; photo 2012"),
 ("s-c31-d1", "place", "Iceland Aurora 2.jpg", "Aurora over Þingvellir",
  "Aurora borealis over Þingvellir, Iceland — for the kennings of the sky", "photo 2019"),
 ("s-c32-d1", "place", "Roca de la Ley, Parque Nacional de Þingvellir, Suðurland, Islandia, 2014-08-16, DD 022.JPG", "Lögberg, Þingvellir",
  "Lögberg and the rift at Þingvellir, Iceland, where the Althing met from 930 — for the kennings of the earth", "photo 2014"),
 ("s-c33-d1", "place", "Reynisfjara02js).jpg", "Surf at Reynisfjara",
  "North Atlantic surf at Reynisfjara, south Iceland — for the kennings of the sea", "photo 2003"),
 ("s-c34-d1", "monument", "Solvognen DO-6865 2000.jpg", "The Trundholm sun chariot",
  "The Trundholm sun chariot (Bronze Age), National Museum of Denmark: a horse drawing the sun, far older than Snorri's Sól and her horses", "c. 1400 BC; photo 2006"),
 ("s-c43-d1", "monument", "Lokistone.jpg", "The Snaptun stone",
  "The Snaptun stone (c. 1000), Moesgård Museum: a face with stitched lips, read as Loki after Brokkr sewed his mouth shut", "c. 1000"),
 ("s-c44-d1", "monument", "Gold bracteate Skonager Nationalmuseet.jpg", "Gold bracteate from Skonager",
  "Gold bracteate from Skonager, Denmark (Migration period), National Museum of Denmark — for the kennings of gold", "5th–6th century; photo 2017"),
 ("s-c46-d1", "monument", "U 1163, Drävle (Andvari).JPG", "Andvari on the Drävle stone",
  "Drävle runestone (U 1163), Uppland: detail read as Andvari, the dwarf whose gold paid the otter's ransom", "11th century; photo 2007"),
 ("s-c47-d1", "monument", "Hylestad - Sigurd Sucking Thumb.jpg", "Sigurðr on the Hylestad portal",
  "Sigurðr tasting Fáfnir's heart's blood, Hylestad stave-church portal (12th century), Museum of Cultural History, Oslo", "late 12th century; photo 2010"),
 ("s-c54-d1", "place", "Royal Mounds of Gamla Uppsala (by Pudelek).JPG", "The royal mounds at Old Uppsala",
  "The royal mounds at Gamla Uppsala, seat of King Aðils in the story of Hrólfr kraki", "6th century mounds; photo 2015"),
 ("s-c56-d1", "monument", "Viking gold jewellery - Hiddensee treasure - VIKING exhibition at the National Museum of Denmark - Photo The National Museum of Denmark (9066249208).jpg", "The Hiddensee gold",
  "The Hiddensee gold hoard (10th century) — for the kennings of gold", "10th century; photo 2013"),
 ("s-c61-d1", "monument", "Gjermundbu helmet.JPG", "The Gjermundbu helmet",
  "The Gjermundbu helmet (10th century), Museum of Cultural History, Oslo — the one near-complete Viking-age helmet, for the kennings of weapons and armour", "10th century; photo 2008"),
 ("s-c64-d1", "monument", "Gokstad Ship Side View.JPG", "The Gokstad ship",
  "The Gokstad ship (c. 890), Viking Ship Museum, Oslo — for the kennings of ships", "c. 890; photo 2010"),
 ("s-c65-d1", "monument", "Jelling Runestone-1 KIF 3558.jpg", "Runestone at Jelling",
  "Runestone at Jelling, Denmark; the larger Jelling stone carries the earliest Christ image in Scandinavia (c. 965)", "10th century; photo 2006"),
 ("s-c66-d1", "monument", "Lewis chessmen 02.JPG", "A Lewis chessman king",
  "A king from the Lewis chessmen (12th century, probably Norwegian), National Museum of Scotland — for the kennings of kings", "12th century; photo 2010"),
 ("s-c72-d1", "place", "IcelandicHorseInWinter.jpg", "An Icelandic horse",
  "An Icelandic horse near Krýsuvík — for the list of horse names", "photo 2003"),
 ("s-c75-d1", "place", "Corvus corax varius upper body.jpg", "A raven in Iceland",
  "A common raven at Stokkseyri, Iceland — Odin's bird, for the names of ravens and eagles", "photo 2011"),
 ("s-c76-d1", "place", "Dyrhólaey Peninsula, Iceland, 20240720 1027 2898.jpg", "Dyrhólaey",
  "Dyrhólaey, south Iceland — for the names of the sea", "photo 2024"),
 ("s-c77-d1", "place", "Bárðarbunga - Holuhraun (14971302084).jpg", "The Holuhraun eruption",
  "The Holuhraun eruption from the air, 2014 — for the names of fire", "photo 2014"),
 ("s-c80-d1", "place", "Borre mound cemetery, Norway. Viking burial mounds, Horten. hoarfrost November 2011.jpg", "Borre mound cemetery",
  "The Borre mound cemetery, Vestfold — burial ground of Norwegian kings, for the chapter on kings' lineages", "Viking age; photo 2011"),
 ("h-c1-d1", "place", "Håkonshallen, Bergen, Noruega, 2019-09-08, DD 05.jpg", "Hákonarhöll, Bergen",
  "Hákonarhöll in Bergen, built by King Hákon Hákonarson, to whom Háttatal is addressed", "c. 1260; photo 2019"),
 ("h-c1-d2", "place", "Hvammur Skeggi Valley.jpg", "Hvammur í Dölum",
  "Hvammur in Dalir, west Iceland, where Snorri was born in 1179", "photo 2011"),
 ("h-c2-d1", "place", "Snorri's Bathhouse at Reykholt.jpg", "Snorralaug, after Collingwood",
  "Snorri's pool at Reykholt, drawn by W. G. Collingwood for A Pilgrimage to the Saga-Steads of Iceland (1899)", "1899"),
 ("h-c3-d1", "place", "Snorralaug2009.JPG", "Snorralaug, Reykholt",
  "Snorralaug, the warm pool at Reykholt where Snorri lived and wrote", "photo 2009"),
]


def main(records_path, meta_path):
    data = json.load(open(records_path, encoding="utf-8"))
    meta = json.load(open(meta_path, encoding="utf-8"))
    recs = [r for r in data["records"] if r.get("kind", "depiction") == "depiction"]
    for r in recs:
        r.setdefault("kind", "depiction")
        r["file"] = r["id"] + ".jpg"
    for rid, kind, f, title, caption, date in DOC:
        m = meta[f]
        slot, _ = rid.rsplit("-d", 1)
        lic = m["lic"]
        basis = {"Public domain": "public domain (per Commons file page)",
                 "No restrictions": "no known copyright restrictions (Flickr Commons, British Library)"}.get(lic, f"{lic} — attribution required: {m['artist']}")
        recs.append({
            "id": rid, "part": PARTS[rid[0]], "chapter": int(slot.split("-c")[1]), "kind": kind,
            "title": title, "artist": m["artist"], "artist_dates": "", "date": date, "medium": kind,
            "source": m.get("credit", ""), "commons_file": f, "source_url": m["page"],
            "file_url": m["url"].split("?")[0], "file": rid + ".jpg",
            "width": m["w"], "height": m["h"], "license": lic, "license_url": m.get("licurl", ""),
            "license_basis": basis, "checked_by": CHECKED, "checked_on": "2026-10-25",
            "caption": caption, "note": "", "alternatives": [], "placed": True})
    data["records"] = recs
    data["_note"] = (data["_note"].split(" Documentary")[0] +
                     " Documentary records (kind manuscript / monument / place) are shown in a strip under the chapter's "
                     "illustration; their licences may be CC0 / CC BY / CC BY-SA and are shown in the credit line.")
    json.dump(data, open(records_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    kinds = {}
    for r in recs:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(len(recs), "records", kinds)


if __name__ == "__main__":
    main(*sys.argv[1:])
