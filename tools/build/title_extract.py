"""New Has-A title: cut the plaques and bar, paint the lettering out of each plaque, and find each
letter's column band so the words can be typed on by revealing the original letters one at a time."""
import json
import numpy as np
from PIL import Image

SRC = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\images\35.webp"
OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\assets"
SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"
A = np.array(Image.open(SRC).convert("RGBA"))
Image.fromarray(A).save(OUT + r"\tt-title.png")

# piece box, inner (lettering) area, ink threshold, word
PIECES = {
    "has":  dict(box=(88, 162, 1032, 482), inner=(122, 194, 1000, 452), ink=95, word="Has-A"),
    "agg":  dict(box=(1098, 162, 1912, 330), inner=(1126, 188, 1888, 310), ink=150, word="AGGREGATION"),
    "comp": dict(box=(1098, 326, 1912, 482), inner=(1126, 346, 1888, 462), ink=150, word="COMPOSITION"),
    "bar":  dict(box=(1038, 166, 1092, 474)),
}

def fill_rows(img, x0, y0, x1, y1, ml, mr):
    """Fill the lettering area row by row with the plaque colour sampled from the clean margin
    columns left (ml) and right (mr) of the lettering (crop-local x ranges), blended across."""
    for r in range(y0, y1):
        cl = np.median(img[r, ml[0]:ml[1], :3].astype(float), axis=0)
        cr = np.median(img[r, mr[0]:mr[1], :3].astype(float), axis=0)
        t = np.linspace(0, 1, x1 - x0)[:, None]
        img[r, x0:x1, :3] = (cl * (1 - t) + cr * t).astype(np.uint8)

# Letter extents (x) from the ink profiles; the border runs at each plaque's edges are left out.
LETTERS = {
    "has": [(151, 391), (399, 552), (561, 673), (697, 758), (760, 975)],                       # H a s - A
    "agg": [(1153, 1226), (1227, 1299), (1307, 1379), (1389, 1442), (1453, 1497), (1504, 1574),
            (1576, 1640), (1641, 1693), (1702, 1715), (1724, 1799), (1809, 1865)],            # AGGREGATION
    "comp": [(1147, 1218), (1224, 1304), (1314, 1395), (1411, 1463), (1471, 1549), (1554, 1606),
             (1617, 1629), (1637, 1690), (1698, 1710), (1721, 1798), (1808, 1865)],           # COMPOSITION
}
meta = {}
for k, p in PIECES.items():
    bx0, by0, bx1, by1 = p["box"]
    crop = A[by0:by1, bx0:bx1].copy()
    m = {"box": [bx0, by0, bx1 - bx0, by1 - by0]}
    if "inner" in p:
        ix0, iy0, ix1, iy1 = p["inner"]
        runs = [[a - ix0, b - ix0] for a, b in LETTERS[k]]   # measured letter extents (absolute x)
        edges = [0] + [(runs[i][1] + runs[i + 1][0]) // 2 for i in range(len(runs) - 1)] + [ix1 - ix0]
        m["inner"] = [ix0 - bx0, iy0 - by0, ix1 - ix0, iy1 - iy0]
        m["edges"] = [int(e) for e in edges]
        print(k, p["word"], len(runs), edges)
        lx0 = LETTERS[k][0][0] - bx0; lx1 = LETTERS[k][-1][1] - bx0
        fill_rows(crop, lx0 - 4, iy0 - by0, lx1 + 9, iy1 - by0, (ix0 - bx0 + 4, lx0 - 8), (lx1 + 9, ix1 - bx0 - 4))
    Image.fromarray(crop).save(OUT + r"\tt-" + k + ".png")
    meta[k] = m
json.dump(meta, open(SCR + r"\title.json", "w"))

sheet = Image.new("RGBA", (2000, 700), (0, 0, 0, 255))
for k, m in meta.items():
    sheet.alpha_composite(Image.open(OUT + r"\tt-" + k + ".png"), (m["box"][0], m["box"][1]))
sheet.convert("RGB").resize((1000, 350)).save(SCR + r"\title_empty.png")
