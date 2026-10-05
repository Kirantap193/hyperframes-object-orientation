"""PlatinumCustomer art from the Customer art: the card's blue becomes platinum (cool silver frame and
header, graphite panels), the header title is cleared (the new title is typed on in HTML), and the card
is widened so "PlatinumCustomer" fits. The girl's red outfit becomes platinum too."""
import colorsys, json
import numpy as np
from PIL import Image

A = r"C:\Users\kiran\Documents\hyperframes\video-11\assets"
SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"

TITLE = (150, 30, 448, 122)     # header area holding "Customer" (card-local)
FILL_X = 452                    # a clean pill column just right of the title
WIDEN_AT, WIDEN_N = 450, 150    # duplicate this column to widen the card
ICONS = (52, 150, 100, 568)     # field icon column (left of the text): keep its colours

def to_hsv(a):
    rgb = a[..., :3].astype(float) / 255
    mx, mn = rgb.max(-1), rgb.min(-1)
    v = mx; d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.zeros_like(v)
    m = d > 1e-6
    hr = ((g - b) / np.maximum(d, 1e-6)) % 6; hg = (b - r) / np.maximum(d, 1e-6) + 2; hb = (r - g) / np.maximum(d, 1e-6) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
    h = np.where(m, h, 0)
    return h, s, v

def platinum_card(img):
    a = img.copy()
    h, s, v = to_hsv(a)
    blue = (h > 175) & (h < 260) & (s > 0.2)
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    icon = (xx >= ICONS[0]) & (xx < ICONS[2]) & (yy >= ICONS[1]) & (yy < ICONS[3])
    icon &= ~((yy >= 336) & (yy < 356))      # not the divider between State and Behaviour
    m = blue & ~(icon & (v > 0.45))          # keep the bright field icons; recolour the panel behind them
    badge = (xx < 150) & (yy < 145)          # the round header badge: darker metal so its white icon reads
    vv = np.where(badge, 0.72 * v ** 1.25, 1.12 * v ** 1.25)   # navy -> graphite, bright blue -> silver
    vv = np.clip(vv, 0, 1)
    base = np.stack([vv * 0.95, vv * 0.97, vv * 1.0], -1)
    a[..., :3] = np.where(m[..., None], (base * 255).astype(np.uint8), a[..., :3])
    return a

def clear_title(a):
    x0, y0, x1, y1 = TITLE
    col = a[y0:y1, FILL_X:FILL_X + 1, :].copy()
    a[y0:y1, x0:x1] = np.repeat(col, x1 - x0, axis=1)
    return a

def widen(a):
    col = a[:, WIDEN_AT:WIDEN_AT + 1]
    return np.concatenate([a[:, :WIDEN_AT], np.repeat(col, WIDEN_N, axis=1), a[:, WIDEN_AT:]], axis=1)

for src, dst in [("cd-cust.png", "cd-plat.png"), ("cd-cust-s.png", "cd-plat-s.png"), ("cd-cust-e.png", "cd-plat-e.png")]:
    a = np.array(Image.open(A + "\\" + src).convert("RGBA"))
    a = widen(platinum_card(clear_title(a)))
    # the top of the first Behaviour cube peeks over the divider in the empty copies: clear it
    if dst != "cd-plat.png":
        reg = a[336:366, 60:110].astype(int)
        purple = (reg[..., 0] - reg[..., 1] > 40) & (reg[..., 2] - reg[..., 1] > 40)
        reg[purple, :3] = a[336:366, 120:121, :3].astype(int).repeat(50, axis=1)[purple]
        a[336:366, 60:110] = reg.astype(np.uint8)
    Image.fromarray(a).save(A + "\\" + dst)

# The girl: red outfit -> platinum silver.
g = np.array(Image.open(A + r"\ob-cust.png").convert("RGBA"))
h, s, v = to_hsv(g)
red = ((h < 8) | (h > 340)) & (s > 0.6) & (v > 0.35)   # jacket, shoes, hair tie - not the brown hair
vv = np.clip(0.22 + 0.95 * v, 0, 1)
base = np.stack([vv * 0.92, vv * 0.94, vv * 1.0], -1)
shade = np.clip(base * (0.75 + 0.25 * (1 - s))[..., None], 0, 1)
g[..., :3] = np.where(red[..., None], (shade * 255).astype(np.uint8), g[..., :3])
Image.fromarray(g).save(A + r"\ob-plat.png")

c = json.load(open(SCR + r"\cards.json"))["cust"]
widen_r = lambda r: [r[0], r[1], r[2] + WIDEN_N, r[3]]   # the text windows span the widened panels too
meta = {"box_w": c["box"][2] + WIDEN_N, "box_h": c["box"][3], "s": widen_r(c["s"]), "b": widen_r(c["b"]), "split": c["split"],
        "title": [TITLE[0], TITLE[1], TITLE[2] - TITLE[0] + WIDEN_N, TITLE[3] - TITLE[1]]}
json.dump(meta, open(SCR + r"\plat.json", "w"))
print(meta)

proof = Image.new("RGBA", (1700, 620), (0, 0, 0, 255))
x = 0
for n in ["cd-plat-e", "cd-plat-s", "cd-plat"]:
    im = Image.open(A + "\\" + n + ".png"); proof.alpha_composite(im, (x, 0)); x += im.width + 10
proof.alpha_composite(Image.open(A + r"\ob-plat.png").resize((185, 250)), (x, 0))
proof.convert("RGB").save(SCR + r"\plat_proof.png")
