"""Class cards: for each card write the original (cd-<k>.png), a split-but-empty copy with the text
painted out (cd-<k>-s.png) and an undivided empty copy (cd-<k>-e.png, the divider covered by a
clean stretch of panel). Positions go to cards.json."""
import json
import numpy as np
from PIL import Image

SRC = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\images\14.webp"
OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\assets"
SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"
A = np.array(Image.open(SRC).convert("RGBA"))

# card box; recess (dark well inside the frame); State and Behaviour interiors (inside the thin borders)
CARDS = {
    "cust":  dict(box=(26, 42, 522, 642), recess=(56, 167, 494, 618),
                  s=(67, 188, 484, 382), b=(67, 394, 484, 612)),
    "rest":  dict(box=(538, 54, 1012, 630), recess=(568, 171, 988, 608),
                  s=(580, 191, 976, 390), b=(580, 406, 976, 604)),
    "agent": dict(box=(1030, 55, 1525, 625), recess=(1063, 176, 1501, 601),
                  s=(1075, 205, 1488, 405), b=(1075, 414, 1488, 597)),
    "food":  dict(box=(1541, 73, 1976, 496), recess=(1569, 183, 1955, 490),
                  s=(1580, 201, 1945, 474), b=None),
}

def paint_out(img, rect, ox, oy):
    """Fill rect (absolute coords) of img (crop at ox, oy) with its own background, row by row."""
    x0, y0, x1, y1 = rect[0] - ox, rect[1] - oy, rect[2] - ox, rect[3] - oy
    rgb = img[y0:y1, x0:x1, :3].astype(float)
    lum = rgb.mean(-1)
    cols = []
    for r in range(rgb.shape[0]):
        l = lum[r]; cols.append(np.median(rgb[r][l <= np.percentile(l, 50)], axis=0))
    cols = np.array(cols); k = 15
    pad = np.pad(cols, ((k // 2, k // 2), (0, 0)), mode="edge")
    cols = np.array([pad[i:i + k].mean(0) for i in range(len(cols))])
    for r in range(rgb.shape[0]):
        img[y0 + r, x0:x1, :3] = cols[r].astype(np.uint8)

# FoodItem gets a taller body: n rows (copies of one clean row just inside its panel) are
# inserted at `at` (card-local), making room for "< Enumeration >" inside the card.
GROW = {"food": dict(at=146, src=145, n=64)}
def grow(img, g):
    if not g:
        return img
    # row `src` sits below the badge's shadow and above the first field: plain panel
    band = np.repeat(img[g["src"]:g["src"] + 1], g["n"], axis=0)
    return np.concatenate([img[:g["at"]], band, img[g["at"]:]], axis=0)

meta = {}
for k, c in CARDS.items():
    bx0, by0, bx1, by1 = c["box"]
    g = GROW.get(k)
    orig = A[by0:by1, bx0:bx1].copy()
    Image.fromarray(grow(orig, g)).save(f"{OUT}\\cd-{k}.png")
    split = orig.copy()
    paint_out(split, c["s"], bx0, by0)
    if c["b"]:
        paint_out(split, c["b"], bx0, by0)
    Image.fromarray(grow(split, g)).save(f"{OUT}\\cd-{k}-s.png")
    dh = g["n"] if g else 0
    m = {"box": [bx0, by0, bx1 - bx0, by1 - by0 + dh],
         "s": [c["s"][0] - bx0, c["s"][1] - by0, c["s"][2] - c["s"][0], c["s"][3] - c["s"][1] + dh]}
    if g:
        m["enum"] = [g["at"], g["n"]]
    if c["b"]:
        # Undivided: every row from just above the State panel's bottom edge to just below the
        # Behaviour panel's top edge becomes a copy of one clean mid-panel row of the split image.
        empty = split.copy()
        rx0, rx1 = c["recess"][0] - bx0, c["recess"][2] - bx0
        tmpl_y = (c["s"][1] + c["s"][3]) // 2 - by0
        tmpl = split[tmpl_y, rx0:rx1].copy()
        ya, yb = c["s"][3] - by0 - 14, c["b"][1] - by0 + 14
        for yy in range(ya, yb):
            empty[yy, rx0:rx1] = tmpl
        Image.fromarray(empty).save(f"{OUT}\\cd-{k}-e.png")
        m["b"] = [c["b"][0] - bx0, c["b"][1] - by0, c["b"][2] - c["b"][0], c["b"][3] - c["b"][1]]
        m["split"] = [ya, yb]
    meta[k] = m
    print(k, m)

json.dump(meta, open(SCR + r"\cards.json", "w"), indent=1)
sheet = Image.new("RGBA", (2000, 1900), (0, 0, 0, 255))
x = 0
for k in CARDS:
    o = Image.open(f"{OUT}\\cd-{k}.png"); s = Image.open(f"{OUT}\\cd-{k}-s.png")
    e = Image.open(f"{OUT}\\cd-{k}-e.png") if CARDS[k]["b"] else s
    sheet.alpha_composite(e, (x, 0)); sheet.alpha_composite(s, (x, 640)); sheet.alpha_composite(o, (x, 1280)); x += o.width + 5
sheet.convert("RGB").resize((1000, 950)).save(SCR + r"\cards_proof.png")
