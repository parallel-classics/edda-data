"""Image-generation briefs for slots that have no usable public-domain depiction (or a weak one).
Writes images/generation-briefs.json and images/generation-briefs.md. Usage: python -I make_briefs.py <outdir>"""
import json
import sys

STYLE = ("Illustration for a scholarly reading edition of Snorri Sturluson's Prose Edda. Style: 19th-century "
         "Scandinavian national-romantic book illustration — pen-and-ink with grey or sepia wash, fine hatching, "
         "muted earth tones, a single clear focal action, calm composition with some empty space. Period-accurate "
         "Viking-Age / medieval Norse dress: wool tunics, cloaks pinned with round brooches, simple leather shoes, "
         "plain conical or rounded helmets only where armed; longhouse interiors of timber with a central hearth. "
         "Landscape format 3:2.")
AVOID = ("No horned or winged helmets, no runes or lettering used as decoration, no text, captions, signatures or "
         "watermarks anywhere in the image, no modern or fantasy-film armour, no glowing magic effects, no "
         "photorealistic faces of real actors, no anachronistic objects.")

B = [
    dict(slot="s-c3", anchor="#s-ch3", part="Skáldskaparmál", chapter=3, rows="s-c3-1 to s-c3-3",
         title="Loki náði Iðunni ok dráp Þjaza", priority=1, reason="slot empty after review (Penrose painting is a different scene)",
         short="Loki as a falcon carrying Iðunn (as a nut) home; Þjazi as an eagle pursuing; the Æsir's fire at the wall of Ásgarðr catching the eagle",
         must=["Loki in falcon shape, small and fast, clutching a single nut in his claws", "a huge eagle (Þjazi) close behind, wings spread",
               "the wall of Ásgarðr below with the Æsir piling plane-shavings and the flames just lit, smoke rising", "the eagle's wing-feathers beginning to catch fire"],
         prompt="A small falcon, flying low and hard with a single hazelnut gripped in its talons, is about to clear a high timber-and-stone wall; a few paces behind it an enormous eagle with ragged feathers dives after it, beak open. Inside the wall, a group of bearded men and women in wool tunics and cloaks (the Æsir) are heaping wood shavings into a long fire at the foot of the wall; the flames leap up just as the falcon passes over, and the eagle's wing-feathers catch alight. Low evening light, long shadows, a few spears and a round shield leaning on the wall."),
    dict(slot="s-c46", anchor="#s-ch46", part="Skáldskaparmál", chapter=46, rows="s-c46-1 to s-c46-6",
         title="Af otrgjöldum", priority=1, reason="slot empty after review (Stassen's Andvari shows the dwarf alone)",
         short="Otter's ransom: in Hreiðmarr's hall the gods fill and cover the otter skin with Andvari's gold; Loki holds back the ring",
         must=["an otter skin spread on the floor, stuffed with gold and being covered with gold coins and rings", "three gods: Odin (one eye, wide hat, spear), Loki, Hœnir, bound or guarded",
               "Hreiðmarr, an old farmer-sorcerer, inspecting the pile with his two sons Fáfnir and Reginn", "one whisker still showing; Loki holding a small ring (Andvaranaut)"],
         prompt="Inside a dim timber longhouse lit by a central hearth, an otter's pelt lies stretched on the earthen floor, stuffed full of gold and almost buried under a heap of coins, arm-rings and brooches. An old, hard-faced farmer (Hreiðmarr) bends over it, pointing at one whisker still uncovered, while his two grown sons, one heavy and brooding, the other a wiry smith with a leather apron, stand behind him. Opposite them three travellers under guard: a tall one-eyed man with a wide-brimmed hat and spear (Odin), a lean sharp-featured man with a sly expression holding a small gold ring half-hidden in his hand (Loki), and a quiet long-legged companion (Hœnir). Smoke in the rafters, tools and nets hanging from the posts."),
    dict(slot="g-c54", anchor="#g-ch54", part="Gylfaginning", chapter=54, rows="g-c54-1 to g-c54-2",
         title="Frá Ganglera", priority=1, reason="no public-domain depiction",
         short="Gangleri alone on an open plain: the hall and the city have vanished; he turns home to tell what he heard",
         must=["a lone traveller in a grey hooded cloak with a staff, seen from behind or three-quarters", "a wide, empty plain under a big sky, grass bending in wind",
               "faint trace of where a great hall stood — perhaps a last shimmer or nothing at all", "no buildings, no other people"],
         prompt="A single traveller in a grey hooded cloak, staff in hand and a bundle on his back, stands on a vast open plain of wind-flattened grass under a huge pale sky, looking around in bewilderment: a moment ago a great hall and a city stood here, and now there is only the plain to the horizon, a few stones and a thin morning mist where the hall was. Seen from slightly behind so his face is half turned; far off, one line of low hills and the beginning of a path leading home. Quiet, spare, slightly uncanny."),
    dict(slot="p-c5", anchor="#p-ch5", part="Formáli", chapter=5, rows="p-c5-1 to p-c5-3",
         title="Óðinn stofnar Sigtún", priority=2, reason="no public-domain depiction",
         short="Odin founding Sigtún by the lake and seating twelve chieftains as judges, after the manner of Troy",
         must=["Odin as a mortal chieftain-king: tall, grey-bearded, one eye, wide hat or circlet, spear as staff", "twelve seated chieftains in a ring on a slope above a lake (Mälaren), each on a stone or bench",
               "surveyors marking out a settlement: posts, cords, men raising the first timber frames", "pine forest and water; northern light"],
         prompt="On a grassy slope above a wide northern lake fringed with pine forest, a tall grey-bearded chieftain with one eye and a spear held like a staff stands at the centre of a ring of twelve seated men — chieftains in cloaks and brooches, each on a stone seat — and addresses them as judges. Behind them, men with cords and wooden posts are marking out streets and the first timber frames of a town are going up; boats are drawn up on the shore. Clear cool northern daylight, long morning shadows, a sense of a new order being founded."),
    dict(slot="g-c2", anchor="#g-ch2", part="Gylfaginning", chapter=2, rows="g-c2-1 to g-c2-4",
         title="Hér hefr Gylfaginning", priority=2, reason="the NKS 1867 drawing is schematic; a fuller scene would help first-time readers",
         short="Gylfi as Gangleri entering the hall roofed with golden shields; a juggler keeping seven knives in the air; three high-seats one above another",
         must=["a hall whose roof is tiled with overlapping golden shields, seen from the entrance", "a man in the doorway juggling seven short knives",
               "three high-seats stacked one above the other at the far end, each with an enthroned figure (Hár, Jafnhár, Þriði)", "the visitor Gangleri in a grey cloak at the threshold"],
         prompt="A traveller in a plain grey cloak (Gangleri) pauses at the open doors of an immense timber hall whose roof is covered, like scales, with overlapping round golden shields that glow in the light. In the doorway a lithe entertainer keeps seven short knives spinning in the air at once. Beyond him, down the length of the hall between carved posts and benches of warriors, three high-seats stand one above another against the far wall, each holding a bearded figure in rich dress, the highest in shadow. Low golden light, smoke from the long hearth, scale emphasised by the small figure at the threshold."),
    dict(slot="s-c5", anchor="#s-ch5", part="Skáldskaparmál", chapter=5, rows="s-c5-1 to s-c5-4",
         title="Frá Kvasi ok mjöðinum", priority=2, reason="Huard's engraving shows Suttungr and the dwarfs on the skerry, not the making of the mead",
         short="The dwarfs Fjalar and Galar brewing the mead of poetry from Kvasir's blood in the two vats Són and Boðn and the kettle Óðrerir",
         must=["two dwarfs — short, broad, bearded, in leather and wool — at work in a rock-cut smithy-kitchen", "a large kettle (Óðrerir) and two vats (Són, Boðn) with honey being stirred in",
               "Kvasir's body laid aside on a bench, treated plainly and without gore", "jars of honey, a fire, dripping stone walls"],
         prompt="In a low cave-like chamber hewn from rock, two squat bearded dwarfs in leather aprons work by firelight: one pours honey from a clay jar into a great iron kettle, the other stirs a wooden vat with a long paddle, a second vat waiting beside it. On a stone bench in the background lies the still body of a wise-looking man in a simple tunic, covered to the chest with a cloth. Steam rises from the kettle; the dwarfs exchange a conspiratorial look. Warm fire-glow against cold wet stone; no visible wounds or blood."),
    dict(slot="s-c47", anchor="#s-ch47", part="Skáldskaparmál", chapter=47, rows="s-c47-1 to s-c47-5",
         title="Sigurðr drap Fáfni", priority=2, reason="the Ramsund photograph is a document of the carving; a drawn scene would show the story",
         short="Sigurðr roasting Fáfnir's heart on a spit, burning his thumb and tasting the blood; the birds in the tree telling him Reginn's treachery; Grani loaded with gold",
         must=["a young warrior (Sigurðr) crouched at a small fire, a heart on a spit, thumb to his mouth", "the great dead serpent-dragon Fáfnir lying along the heath behind",
               "a smith (Reginn) asleep or sharpening a sword nearby", "nuthatches or small birds in a bare tree above; a grey horse (Grani) with saddlebags"],
         prompt="On a bleak heath, a young long-haired warrior in a mail-shirt crouches over a small fire turning a heart on a wooden spit; he has just touched it and raises his burned thumb to his lips, eyes lifting to a bare tree where several small birds sit in a row as if speaking. Behind him the vast coils of a dead serpent-like dragon stretch across the heath, and a short, grey old smith dozes against a rock with a sword across his knees. To one side a grey horse stands loaded with heavy saddlebags. Cold overcast light, heather and stones."),
    dict(slot="s-c62", anchor="#s-ch62", part="Skáldskaparmál", chapter=62, rows="s-c62-1 to s-c62-3",
         title="Hjaðningavíg", priority=2, reason="the Stora Hammars photograph is a document of the stone; a drawn scene would show the everlasting battle",
         short="Hildr waking the fallen every night so that Högni's and Heðinn's hosts fight on until Ragnarök",
         must=["a battlefield at night on a shore (Háey in Orkney): fallen warriors, broken shields, beached ships", "a tall woman (Hildr) walking among the dead, touching or calling them, and the dead rising stiffly to their feet",
               "two opposing kings' hosts regrouping under their banners at the edges", "moonlight or a cold dawn"],
         prompt="Night on a rocky island shore: the aftermath of a battle, with fallen warriors, split shields and dropped spears lying in the grass, longships beached in the surf behind. A tall woman in a dark cloak walks among the dead, one hand raised, and where she passes the fallen men are rising stiffly to their feet, picking up their weapons again. At the two far edges of the picture, two hosts under banners form up once more to face each other. Pale moonlight, silver sea, a sense of weary endless repetition rather than glory."),
    dict(slot="g-c13", anchor="#g-ch13", part="Gylfaginning", chapter=13, rows="g-c13-1 to g-c13-2",
         title="Frá Bifröst", priority=3, reason="Doepler's scan is cropped irregularly; an alternative could replace it",
         short="Bifröst, the three-coloured burning bridge from earth to heaven, seen from the earth",
         must=["a bridge of three bands of colour (red, blue, green or red, yellow, blue) arching from a meadow up into cloud", "the red band visibly burning like flame along its edge",
               "a tiny guardian figure with a horn at the top (Heimdallr) or none", "earth below: fields, a river, a farm"],
         prompt="From a summer meadow with a river and a small farm, a vast bridge of three bands of colour — red, green and blue — springs into the sky and vanishes into high cloud; the outermost red band burns with a soft living flame along its whole length. Two farm children and a dog stand in the grass looking up. Far up where the bridge meets the cloud a minute figure with a curved horn stands watch. Clear air, high cumulus, strong but not garish colour; the bridge solid like glass and fire rather than a rainbow of light."),
    dict(slot="s-c43", anchor="#s-ch43", part="Skáldskaparmál", chapter=43, rows="s-c43-1 to s-c43-6",
         title="Frá smíðum dverganna", priority=3, reason="Boyd Smith's illustration is only 446 px wide",
         short="Sindri's forge: Brokkr at the bellows, the fly (Loki) stinging his eyelid, Sindri drawing Mjöllnir with its too-short handle from the fire; Gullinbursti and Draupnir finished beside",
         must=["two dwarfs: one working the bellows with a fly on his eyelid and blood on his cheek, one lifting a hammer from the forge with tongs", "a golden boar and a gold ring already made, set on the bench",
               "the hammer's handle noticeably short", "a dark forge with sparks"],
         prompt="In a cramped stone forge lit by the white glare of the furnace, a broad dwarf works a huge bellows with both hands, grimacing as a fly bites his eyelid and a thread of blood runs down his cheek; a second dwarf in a scorched apron draws a hammer from the coals with tongs — a heavy square head on a handle a little too short. On the bench behind them lie the morning's work: a boar figure of gold with bristles like rays, and a plain heavy gold ring. Sparks, soot, tools on the walls, deep shadow at the edges."),
    dict(slot="p-c4", anchor="#p-ch4", part="Formáli", chapter=4, rows="p-c4-1 to p-c4-3",
         title="Óðinn ferr norðr", priority=3, reason="the NKS drawing of Odin on Sleipnir is a stand-in; the chapter is about the migration",
         short="Odin leading his household and a great following north out of Turkey through Saxland and into the Danish lands",
         must=["a long column of people, horses, carts and herds crossing hill country, seen from a height", "Odin at the head on horseback: grey-bearded, one eye, broad hat, spear",
               "women, children and household goods in the train; no army look", "distant sea or northern forests ahead"],
         prompt="Seen from a hillside, a long winding train of travellers crosses a broad river valley heading north: horsemen, ox-carts loaded with chests and tent cloth, herds of cattle, women and children on foot, dogs. At the head, on a tall horse, rides a grey-bearded chieftain with a wide hat shading one eye and a spear held upright. Ahead the country opens into dark pine forest and a glimpse of grey sea; behind, dusty southern hills. Early morning, long light; the mood of a migration, not a campaign."),
    dict(slot="g-c42", anchor="#g-ch42", part="Gylfaginning", chapter=42, rows="g-c42-1 to g-c42-9",
         title="Frá smiðnum ok Svaðilfara", priority=3, reason="Hardy (1909) has an unverified death date; a generated image would remove the doubt",
         short="The giant master-builder and the stallion Svaðilfari hauling stones for the wall of Ásgarðr by night; Loki as a mare luring the horse away",
         must=["a half-built massive stone wall, enormous blocks, winter night", "a powerful stallion in harness dragging a sled of stones, driven by a huge grim builder",
               "a mare at the forest edge, neighing, the stallion turning towards her", "the builder's dismay"],
         prompt="A winter night under a cold moon: a towering half-built wall of enormous stone blocks runs across the picture. A huge, grim builder in rough furs drives a magnificent stallion in harness that drags a sledge piled with boulders — but the stallion has stopped and turned its head, ears pricked, towards a pale mare that stands whinnying at the edge of a dark birch wood. The builder's shoulders slump as he realises. Snow, blue shadows, breath steaming."),
]

out = {"_note": "Briefs for generated or commissioned images (track 2). One brief per slot; 'prompt' is the scene prose for an image model, "
                "prefix it with 'style' and suffix it with 'avoid'. 'must' is the reviewer's checklist. Priority 1 = the slot is empty; "
                "2 = the current public-domain image shows a related but different scene or is a document rather than a depiction; "
                "3 = optional replacement.",
       "style": STYLE, "avoid": AVOID, "briefs": B}
json.dump(out, open(f"{sys.argv[1]}/generation-briefs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

md = ["# Image generation briefs (track 2)", "",
      "Slots with no usable public-domain depiction, or where a drawn scene would add what the historical image lacks. "
      "Each full prompt = the style paragraph + the scene + the avoid list; the *must* items are the reviewer's checklist before voting.", "",
      "**Style (prefix every prompt):** " + STYLE, "", "**Avoid (suffix every prompt):** " + AVOID, "",
      "| Pri. | Where (anchor · rows) | Short description | Must show |", "| --- | --- | --- | --- |"]
for b in B:
    md.append(f"| {b['priority']} | `{b['anchor']}` · {b['part']} {b['chapter']} *{b['title']}* · rows {b['rows']} | {b['short']} | " + "; ".join(b["must"]) + " |")
md += ["", "## Full prompts", ""]
for b in B:
    md += [f"### {b['slot']} — {b['part']} {b['chapter']}, *{b['title']}* (priority {b['priority']})", "",
           f"Why: {b['reason']}.", "", "```", STYLE + " " + b["prompt"] + " " + AVOID, "```", ""]
open(f"{sys.argv[1]}/generation-briefs.md", "w", encoding="utf-8").write("\n".join(md))
print(len(B), "briefs")
