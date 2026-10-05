"""Cut the object-slide artwork into its pieces: characters, name pills, arrows, and for each
State/Behaviour panel an empty copy (text painted out) plus the original, whose lines are shown
one at a time through windows. Writes assets/ob-*.png and scratchpad/objects.json."""
import json
import numpy as np
from PIL import Image

SRC = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\images\11.webp"
OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\assets"
SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"

im = Image.open(SRC).convert("RGBA")
A = np.array(im)

def cut(name, box, minus=None, keep=None, keep_rects=(), kill_rects=(), clean=None):
    """Crop `box`. Pixels inside `minus` (the neighbour's area) are cleared unless `keep(r,g,b)`
    says they are ours or they sit in one of `keep_rects`. `kill_rects` are cleared outright.
    `clean` = (rows, test) clears neighbour pixels from this crop's first rows."""
    x0, y0, x1, y1 = box
    sub = A[y0:y1, x0:x1].copy()
    def local(r):
        rx0, ry0, rx1, ry1 = r
        return max(rx0 - x0, 0), max(ry0 - y0, 0), min(rx1 - x0, x1 - x0), min(ry1 - y0, y1 - y0)
    if minus:
        sx0, sy0, sx1, sy1 = local(minus)
        if sx1 > sx0 and sy1 > sy0:
            reg = sub[sy0:sy1, sx0:sx1]
            clear = np.ones(reg.shape[:2], bool)
            if keep:
                t = reg.astype(int); clear &= ~keep(t[..., 0], t[..., 1], t[..., 2])
            for kr in keep_rects:
                kx0, ky0, kx1, ky1 = local(kr)
                clear[max(ky0 - sy0, 0):max(ky1 - sy0, 0), max(kx0 - sx0, 0):max(kx1 - sx0, 0)] = False
            reg[clear, 3] = 0
    for kr in kill_rects:
        kx0, ky0, kx1, ky1 = local(kr)
        if kx1 > kx0 and ky1 > ky0: sub[ky0:ky1, kx0:kx1, 3] = 0
    if clean:
        rows, test = clean
        top = sub[:rows].astype(int)
        kill = test(top[..., 0], top[..., 1], top[..., 2])
        sub[:rows][kill, 3] = 0
    Image.fromarray(sub).save(OUT + "\ob-" + name + ".png")
    return {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}

lowsat = lambda r, g, b: (np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)) < 28
heel = lambda r, g, b: (r > 190) & (g < 90)
HEELS = [(108, 528, 159, 540), (209, 528, 279, 540)]   # where her shoes stand on the pill
OBJ = {
    "cust": dict(char=dict(box=(40, 40, 400, 540), minus=(56, 529, 368, 600), keep_rects=HEELS),
                 pill=dict(box=(56, 529, 368, 598), kill_rects=HEELS),
                 arrow=(120, 598, 325, 653), panels={"s": (40, 652, 216, 870), "b": (216, 652, 456, 922)}),
    "rest": dict(char=dict(box=(400, 70, 892, 552), minus=(508, 533, 838, 600), keep=lowsat),
                 pill=dict(box=(510, 533, 836, 598), clean=(16, lowsat)),
                 arrow=(575, 598, 775, 653), panels={"s": (488, 652, 668, 870), "b": (672, 652, 904, 870)}),
    "agent": dict(char=dict(box=(915, 115, 1310, 550), minus=(944, 533, 1294, 600), keep=lowsat),
                  pill=dict(box=(946, 533, 1292, 598), clean=(10, lowsat)),
                  arrow=(1010, 598, 1215, 653), panels={"s": (930, 652, 1113, 872), "b": (1115, 652, 1373, 872)}),
    "food": dict(char=dict(box=(1315, 205, 1660, 528)),
                 pill=dict(box=(1366, 526, 1627, 596)),
                 arrow=(1480, 596, 1530, 653), panels={"s": (1425, 652, 1608, 872)}),
}
HEADER_BOTTOM = 707   # panel header strip ends here; the list starts below

meta = {"W": im.width, "H": im.height, "objects": {}}
for key, o in OBJ.items():
    m = {"char": cut(key, **o["char"]),
         "pill": cut(key + "-pill", **o["pill"]),
         "arrow": cut(key + "-arrow", o["arrow"]),
         "panels": {}}
    for pk, box in o["panels"].items():
        x0, y0, x1, y1 = box
        full = A[y0:y1, x0:x1].copy()
        Image.fromarray(full).save(f"{OUT}\\ob-{key}-{pk}.png")
        rgb = full[..., :3].astype(float)
        lum = rgb.mean(-1)
        alpha = full[..., 3]
        # The list area: under the header, inside the rim.
        ly0, ly1 = HEADER_BOTTOM - y0, (y1 - y0) - 14
        lx0, lx1 = 12, (x1 - x0) - 12
        # Text = bright pixels (white words, orange/cyan chevrons) in the list area.
        bright = lum > 95
        area = np.zeros_like(bright); area[ly0:ly1, lx0:lx1] = True
        ink = bright & area
        # Empty panel: every list row filled with the median of its dark (background) pixels.
        empty = full.copy()
        cols = []
        for yy in range(ly0, ly1):
            row = rgb[yy, lx0:lx1]
            l = lum[yy, lx0:lx1]
            bgpix = row[l <= np.percentile(l, 55)]
            cols.append(np.median(bgpix, axis=0))
        cols = np.array(cols)
        # smooth down the panel so the fill has no row-to-row banding
        k = 15; pad = np.pad(cols, ((k // 2, k // 2), (0, 0)), mode="edge")
        cols = np.array([pad[i:i + k].mean(0) for i in range(len(cols))])
        for i, yy in enumerate(range(ly0, ly1)):
            empty[yy, lx0:lx1, :3] = cols[i].astype(np.uint8)
        Image.fromarray(empty).save(f"{OUT}\\ob-{key}-{pk}-empty.png")
        # Lines: runs of rows that hold ink.
        prof = ink.sum(1) > 2
        runs, s = [], None
        for yy, v in enumerate(prof):
            if v and s is None: s = yy
            if not v and s is not None: runs.append([s, yy]); s = None
        if s is not None: runs.append([s, len(prof)])
        # merge runs split by descenders/gaps under 4 px
        merged = []
        for r in runs:
            if merged and r[0] - merged[-1][1] < 4: merged[-1][1] = r[1]
            else: merged.append(r)
        merged = [r for r in merged if r[1] - r[0] >= 8]
        # Windows: halfway between lines, so each window carries its whole line.
        edges = [ly0] + [(merged[i][1] + merged[i + 1][0]) // 2 for i in range(len(merged) - 1)] + [ly1]
        lines = [[int(edges[i]), int(edges[i + 1])] for i in range(len(merged))]
        m["panels"][pk] = {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0,
                           "lx0": lx0, "lx1": lx1, "lines": lines}
        print(key, pk, "lines", len(lines), lines)
    meta["objects"][key] = m

json.dump(meta, open(SCR + r"\objects.json", "w"), indent=1)

# Proof sheet: empty panels next to the originals.
sheet = Image.new("RGBA", (1700, 560), (0, 0, 0, 255))
x = 5
for key, o in OBJ.items():
    for pk in o["panels"]:
        e = Image.open(f"{OUT}\\ob-{key}-{pk}-empty.png"); f = Image.open(f"{OUT}\\ob-{key}-{pk}.png")
        sheet.alpha_composite(f, (x, 5)); sheet.alpha_composite(e, (x, 285)); x += f.width + 8
sheet.convert("RGB").save(SCR + r"\panels_proof.png")
