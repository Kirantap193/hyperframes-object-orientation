"""Lift the pillar lettering out of image 2 as transparent PNGs, one per pillar,
and find each letter's vertical extent so it can be revealed one at a time."""
import json
import numpy as np
from PIL import Image, ImageFilter

IMG = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\images"
OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\assets"
SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"

a_im = Image.open(IMG + r"\1.webp").convert("RGBA")
b_im = Image.open(IMG + r"\2.webp").convert("RGBA")
a = np.array(a_im).astype(int)
b = np.array(b_im).astype(int)
d = np.abs(a[..., :3] - b[..., :3]).max(-1).astype(float)

# Shaft interiors (x range kept inside the column outline, y between capital and base).
PILLARS = {
    "p1": ("ENCAPSULATION", 245, 365),
    "p2": ("INHERITANCE", 545, 665),
    "p3": ("POLYMORPHISM", 850, 970),
    "p4": ("ABSTRACTION", 1155, 1275),
}
Y0, Y1 = 405, 828

meta = {"W": a_im.width, "H": a_im.height, "pillars": {}}
for key, (word, x0, x1) in PILLARS.items():
    sub = d[Y0:Y1, x0:x1]
    bsub = b[Y0:Y1, x0:x1]
    core = (sub > 60) & (bsub[..., 2] - bsub[..., 0] > 40) & (bsub[..., 3] > 200)  # navy letter ink
    ys, xs = np.nonzero(core)
    bx0, bx1 = int(max(xs.min() - 8, 0)), int(min(xs.max() + 9, x1 - x0))
    by0, by1 = int(max(ys.min() - 8, 0)), int(min(ys.max() + 9, Y1 - Y0))
    # Soft alpha: full where the images clearly differ, ramping to 0 where they agree.
    alpha = np.clip((sub - 14) / 36.0, 0, 1)
    keep = np.zeros_like(alpha)
    keep[by0:by1, bx0:bx1] = 1
    alpha *= keep
    al = Image.fromarray((alpha * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.8))
    rgba = b[Y0:Y1, x0:x1].astype("uint8").copy()
    rgba[..., 3] = np.minimum(np.array(al), rgba[..., 3])
    crop = Image.fromarray(rgba).crop((bx0, by0, bx1, by1))
    crop.save(f"{OUT}\\oops-{key}.png")

    # Letter extents along y (text reads bottom -> top). Rows with ink:
    prof = core[by0:by1, :].sum(1)
    ink = prof > 1
    runs, start = [], None
    for i, v in enumerate(ink):
        if v and start is None:
            start = i
        if not v and start is not None:
            runs.append([int(start), int(i)]); start = None
    if start is not None:
        runs.append([int(start), int(len(ink))])
    # Touching letters share a run: split the longest run at its thinnest row until
    # there is one run per letter.
    sm = np.convolve(prof, np.ones(3) / 3, mode="same")
    while len(runs) < len(word):
        r = max(runs, key=lambda q: q[1] - q[0])
        lo, hi = r[0] + int((r[1] - r[0]) * 0.25), r[0] + int((r[1] - r[0]) * 0.75)
        cut = int(lo + np.argmin(sm[lo:hi]))
        i = runs.index(r)
        runs[i:i + 1] = [[r[0], cut], [cut, r[1]]]
    assert len(runs) == len(word), (key, len(runs))
    # Band edges: halfway through each gap, so a band holds its whole letter.
    edges = [0] + [int((runs[i][1] + runs[i + 1][0]) // 2) for i in range(len(runs) - 1)] + [int(by1 - by0)]
    meta["pillars"][key] = {
        "word": word, "x": int(x0 + bx0), "y": int(Y0 + by0),
        "w": int(bx1 - bx0), "h": int(by1 - by0), "edges": edges,
    }
    print(key, word, edges)

json.dump(meta, open(SCR + r"\letters.json", "w"), indent=1)

# Proof: composite all letters over image 1.
proof = a_im.copy()
for key, p in meta["pillars"].items():
    proof.alpha_composite(Image.open(f"{OUT}\\oops-{key}.png"), (p["x"], p["y"]))
bg = Image.new("RGBA", proof.size, (1, 1, 1, 255))
bg.alpha_composite(proof)
bg.convert("RGB").save(SCR + r"\proof.png")
