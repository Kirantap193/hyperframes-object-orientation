"""Write compositions/class-layout.html: starts on the exact last frame of the objects + class-cards
slide, then moves the cards (with their object pictures) to the corner layout of the lecture,
then Restaurant to the centre, then Customer down to the middle of the left side."""
import json

SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"
OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\compositions\class-layout.html"
ob = json.load(open(SCR + r"\objects.json"))["objects"]
cd = json.load(open(SCR + r"\cards.json"))

# Where things are on the last frame of the previous scenes (frame pixels).
def ob_frame(x, y, w, h):          # objects stage: left 8 + 330.3, top 3 - 18, scale 0.725
    return [338.3 + 0.725 * x, -15 + 0.725 * y, 0.725 * w, 0.725 * h]
def cd_frame(x, y, w, h):          # class-cards stage: left 329.4, top 645.5, scale 0.63
    return [329.4 + 0.63 * x, 645.5 + 0.63 * y, 0.63 * w, 0.63 * h]

ORDER = ["cust", "rest", "agent", "food"]
start = {}
for k in ORDER:
    o = ob[k]
    start[k] = {
        "char": ob_frame(*[o["char"][q] for q in "xywh"]),
        "pill": ob_frame(*[o["pill"][q] for q in "xywh"]),
        "arrow": ob_frame(*[o["arrow"][q] for q in "xywh"]),
        "panels": {pk: ob_frame(p["x"], p["y"], p["w"], p["h"]) for pk, p in o["panels"].items()},
        "card": cd_frame(*cd[k]["box"]),
    }

# Target layouts (frame pixels), read off the lecture screenshots and sized for our cards.
CARD_S = 0.62                     # cards keep (almost) their current size
def card_at(k, cx, cy):
    w, h = cd[k]["box"][2] * CARD_S, cd[k]["box"][3] * CARD_S
    return [cx - w / 2, cy - h / 2, w, h]
def char_beside(k, card, side, height, dy=0):
    a = ob[k]["char"]; s = height / a["h"]; w = a["w"] * s
    x = card[0] - 14 - w if side == "left" else card[0] + card[2] + 14
    return [x, card[1] + card[3] / 2 - height / 2 + dy, w, height]
def char_above(k, card, height):
    a = ob[k]["char"]; s = height / a["h"]; w = a["w"] * s
    return [card[0] + card[2] / 2 - w / 2, card[1] - 12 - height, w, height]

L1 = {}   # 1. corners
L1["cust"] = {"card": card_at("cust", 367, 262)};   L1["cust"]["char"] = char_beside("cust", L1["cust"]["card"], "left", 240)
L1["agent"] = {"card": card_at("agent", 1538, 262)}; L1["agent"]["char"] = char_beside("agent", L1["agent"]["card"], "right", 190)
L1["rest"] = {"card": card_at("rest", 376, 821)};   L1["rest"]["char"] = char_beside("rest", L1["rest"]["card"], "left", 180, -40)
L1["food"] = {"card": card_at("food", 1535, 821)};  L1["food"]["char"] = char_beside("food", L1["food"]["card"], "right", 165, -30)
L2 = {"card": card_at("rest", 938, 540)}            # 2. Restaurant to the centre, its building above
L2["card"][1] += 60
L2["char"] = char_above("rest", L2["card"], 170)
L3 = {"card": card_at("cust", 372, 540)}            # 3. Customer down to the middle of the left side
L3["char"] = char_beside("cust", L3["card"], "left", 240)

def move(frm, to):
    """GSAP x / y / scale (transform-origin 0 0) that take box `frm` onto box `to`."""
    return {"x": round(to[0] - frm[0], 1), "y": round(to[1] - frm[1], 1), "scale": round(to[2] / frm[2], 4)}

plan = {k: {"start": start[k],
            "card1": move(start[k]["card"], L1[k]["card"]), "char1": move(start[k]["char"], L1[k]["char"])}
        for k in ORDER}
plan["rest"]["card2"] = move(start["rest"]["card"], L2["card"])
plan["rest"]["char2"] = move(start["rest"]["char"], L2["char"])
plan["cust"]["card3"] = move(start["cust"]["card"], L3["card"])
plan["cust"]["char3"] = move(start["cust"]["char"], L3["char"])

FADE_AT, FADE_DUR = 0.3, 0.6
MOVE1_AT, MOVE_DUR, STAGGER = 0.6, 1.4, 0.1
MOVE2_AT, MOVE2_DUR = 3.8, 1.2
MOVE3_AT, MOVE3_DUR = 6.4, 1.1
# --- Has-A (lecture 9:27 - 11:57) ---
AGENT_DOWN = 60                                   # DeliveryAgent slides down to meet its line
cu, re_, fo = L3["card"], L2["card"], L1["food"]["card"]
ag = [L1["agent"]["card"][0], L1["agent"]["card"][1] + AGENT_DOWN] + L1["agent"]["card"][2:]
LINE_Y = {"cust": 575, "agent": ag[1] + 325, "food": fo[1] + 60}
DIA = 22                                          # half-width of a diamond's box (its tip is 21.2 px out)
HASA = {
    # line from x0 to x1 at y; the diamond sits at the Restaurant end (x of its centre)
    "cust":  dict(x0=cu[0] + cu[2] - 4, x1=re_[0] - DIA + 2, y=LINE_Y["cust"], dia=re_[0] - DIA + 2, end="right"),
    "agent": dict(x0=re_[0] + re_[2] + DIA - 2, x1=ag[0] + 4, y=LINE_Y["agent"], dia=re_[0] + re_[2] + DIA - 2, end="left"),
    "food":  dict(x0=re_[0] + re_[2] + DIA - 2, x1=fo[0] + 4, y=LINE_Y["food"], dia=re_[0] + re_[2] + DIA - 2, end="left"),
}
CHAR = 0.06                                       # type-on: one character every 0.06 s
B1 = 8.0                                          # Customer -> Restaurant rod, diamond, "Has-A"
B2 = 10.0                                         # DeliveryAgent slides down
B3A, B3B = 11.4, 13.2                             # diamond + rod to DeliveryAgent, then to FoodItem
B4A, B4B = 15.0, 16.0                             # "Has-A" over each
B5 = 17.0                                         # title: Has-A | AGGREGATION / COMPOSITION (pauses inside)
B6 = 22.7                                         # FoodItem diamond fills, "Composition"
B7A, B7B = 24.9, 26.7                             # "Aggregation" under Customer's rod, then DeliveryAgent's
# --- Dev team at work (lecture 12:43) ---
B8, LIFT = 28.7, 130                              # title fades, the whole diagram moves up 130 px
B9 = 30.3                                         # the team clip's frame pops in
TEAM_AT, TEAM_DUR = 30.3, 3.0                     # source 39.5 - 42.5 s ("team.mp4"), then its last frame
TEAM = [700, 688, 640, 360]                       # under the Restaurant, clear of every card once lifted
# --- PlatinumCustomer (lecture 13:34): girl, then empty card + typed title, split, State, Behaviour ---
PL = json.load(open(SCR + r"\plat.json"))
PK = 0.62                                         # same scale as the other cards
PL_CARD = [cu[0], 650, PL["box_w"] * PK, PL["box_h"] * PK]     # frame px, under the Customer card
PL_GIRL = [cu[0] - 14 - 173, PL_CARD[1] + PL_CARD[3] / 2 - 120, 173, 240]
P1 = round(TEAM_AT + TEAM_DUR + 0.8, 2)           # girl pops in
P2 = round(P1 + 1.0, 2)                           # empty card, then its title types on
P3 = round(P2 + 2.4, 2)                           # body splits
P4 = round(P3 + 1.4, 2)                           # State
P5 = round(P4 + 1.4, 2)                           # Behaviour
# PlatinumCustomer grows: platinum_id, credits | free_delivery(), exclusive_offers()
X1 = round(P5 + 2.0, 2)                           # card + girl move up to make room
X2 = round(X1 + 0.9, 2)                           # State panel opens; its two rows type on (pause between)
X3 = round(X2 + 3.4, 2)                           # Behaviour panel opens; its two rows type on
F1 = round(X3 + 4.0, 2)                           # class-hl.html starts here: frustration, then yellow
PINK = round(F1 + 10.8, 2)                        # the four new PlatinumCustomer names turn pink
DURATION = round(F1 + 13.6, 2)
TT = json.load(open(SCR + r"\title.json"))
print("agent card", [round(v) for v in ag], "lines", {k: (round(v["x0"]), round(v["x1"]), v["y"]) for k, v in HASA.items()})

for k in ORDER:
    print(k, "card", [round(v) for v in L1[k]["card"]], "char", [round(v) for v in L1[k]["char"]])
print("rest centre", [round(v) for v in L2["card"]], [round(v) for v in L2["char"]])
print("cust middle", [round(v) for v in L3["card"]], [round(v) for v in L3["char"]])

html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Class cards: layout moves</title>
  </head>
  <body>
    <template id="class-layout-template">
      <style>
        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
          pointer-events: none;
          background: #000000;
        }}
        /* Every piece is placed at its frame position on the last frame of the objects + class-cards
           slide, then moved with x / y / scale about its top-left corner. */
        .cl-el {{ position: absolute; transform-origin: 0 0; }}
        .cl-el > img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; }}
        /* "< Enumeration >" inside the FoodItem card, in the band added above its fields. */
        .cl-enum {{
          position: absolute; display: flex; align-items: center; justify-content: center; gap: 0.45em;
          white-space: nowrap; font-family: "Poppins", "Inter", "Segoe UI", sans-serif; font-weight: 500;
          color: #efe2ff; letter-spacing: 0.03em;
          text-shadow: 0 0 12px rgba(200,120,255,.55), 0 2px 3px rgba(0,0,0,.7);
        }}
        .cl-enum b {{ font-weight: 600; color: #ff86de; }}
        /* Has-A: 3-D cyan rods with diamonds at the Restaurant end; raised lettering, no glow. */
        .cl-rod {{ position: absolute; height: 10px; margin-top: -5px;
          background: linear-gradient(180deg, #d4f6ff 0%, #5fd3f5 38%, #1e95c2 72%, #0d5f80 100%);
          box-shadow: inset 0 1px 0 rgba(255,255,255,.7), 0 5px 6px rgba(0,0,0,.75); transform: scaleX(0); }}
        .cl-dia-pos {{ position: absolute; width: 44px; height: 44px; margin: -22px 0 0 -22px; opacity: 0; }}
        .cl-dia {{ position: absolute; left: 7px; top: 7px; width: 30px; height: 30px;
          transform: rotate(45deg);
          background: linear-gradient(135deg, #d4f6ff 0%, #5fd3f5 40%, #1e95c2 75%, #0d5f80 100%);
          box-shadow: 3px 3px 5px rgba(0,0,0,.75); }}
        .cl-dia-hole {{ position: absolute; inset: 6px; background: #000;
          box-shadow: inset 2px 2px 3px rgba(0,0,0,.9), inset -1px -1px 2px rgba(120,220,255,.35); }}
        .cl-lbl {{ position: absolute; width: 400px; margin-left: -200px; text-align: center; white-space: nowrap;
          font-family: "Poppins", "Inter", sans-serif; font-weight: 400; font-size: 34px; line-height: 1;
          color: #fbe7a1;
          text-shadow: 0 1px 0 #e0c779, 0 2px 0 #c4a95a, 0 3px 0 #a68b3f, 0 4px 0 #866d28, 0 8px 8px rgba(0,0,0,.8); }}
        .cl-title {{ position: absolute; left: 40px; top: 34px; height: 170px; display: flex; align-items: center; gap: 34px; }}
        .cl-hasa {{ font-family: "Playfair Display", Georgia, serif; font-weight: 900; font-size: 116px; line-height: 1;
          color: #ffffff; letter-spacing: 1px;
          text-shadow: 0 1px 0 #dcdcdc, 0 2px 0 #c4c4c4, 0 3px 0 #acacac, 0 4px 0 #949494, 0 5px 0 #7c7c7c,
                       0 6px 0 #646464, 0 12px 12px rgba(0,0,0,.8); }}
        .cl-bar {{ width: 14px; height: 150px; border-radius: 4px; transform-origin: 50% 0; transform: scaleY(0);
          background: linear-gradient(90deg, #ff7a9c 0%, #ff3d6e 45%, #c2184a 100%);
          box-shadow: 4px 5px 6px rgba(0,0,0,.7); }}
        .cl-kinds {{ font-family: "Bebas Neue", "Oswald", sans-serif; font-size: 82px; line-height: 0.95; letter-spacing: 1px;
          color: #d4e157;
          text-shadow: 0 1px 0 #b9c541, 0 2px 0 #9daa2f, 0 3px 0 #818d20, 0 4px 0 #667014, 0 9px 9px rgba(0,0,0,.8); }}
        .cl-tc {{ opacity: 0; }}
        .cl-all {{ position: absolute; inset: 0; }}
        /* The clip in a raised, bevelled frame with a drop shadow (no glow). */
        .cl-team {{ position: absolute; left: {TEAM[0] - 14}px; top: {TEAM[1] - 14}px; width: {TEAM[2] + 28}px;
          height: {TEAM[3] + 28}px; border-radius: 26px; opacity: 0; transform-origin: 50% 100%;
          background: linear-gradient(160deg, #5b6474 0%, #2c323d 45%, #161a21 100%);
          box-shadow: inset 0 2px 0 rgba(255,255,255,.35), inset 0 -3px 0 rgba(0,0,0,.6),
                      0 8px 0 #0b0d11, 0 22px 30px rgba(0,0,0,.85); }}
        .cl-team-in {{ position: absolute; left: 14px; top: 14px; width: {TEAM[2]}px; height: {TEAM[3]}px;
          border-radius: 14px; overflow: hidden; background: #000;
          box-shadow: inset 0 3px 8px rgba(0,0,0,.8); }}
        .cl-pl-title {{ position: absolute; display: flex; align-items: center; white-space: nowrap;
          font-family: "Poppins", "Inter", sans-serif; font-weight: 700; letter-spacing: 0.2px; color: #1d222a;
          text-shadow: 0 1px 0 rgba(255,255,255,.65), 0 -1px 0 rgba(0,0,0,.25); }}
        .cl-pl-split {{ clip-path: inset(0 50% 0 50%); }}
        .cl-pl-block {{ position: absolute; opacity: 0; background-repeat: no-repeat; }}
        .cl-tt {{ position: absolute; left: -0.5px; top: -38.5px; width: 2000px; height: 668px;
          transform: scale(0.46); transform-origin: 0 0; }}
        .cl-tt-el {{ position: absolute; opacity: 0; }}
        .cl-tt-ch {{ position: absolute; opacity: 0; background: url(assets/tt-title.png) no-repeat; }}
        .cl-px {{ position: absolute; left: 0; top: 0; width: 100%; opacity: 0; }}
        .cl-px img, .cl-px .cl-px-sl {{ position: absolute; left: 0; display: block; width: 100%; }}
        .cl-px-sl {{ background: url(assets/cd-plat.png) no-repeat; background-size: 100% auto; }}
        .cl-px-row {{ position: absolute; display: flex; align-items: center; white-space: nowrap;
          font-family: "Segoe UI", "Inter", sans-serif; color: #ebeef4; }}
        .cl-px-type {{ position: absolute; color: #3de2c1; font-weight: 700; }}
        .cl-px-id {{ border-radius: 5px; font-family: "Inter", sans-serif; font-weight: 800; color: #24303d;
          display: flex; align-items: center; justify-content: center;
          background: linear-gradient(160deg, #ffffff 0%, #cfd6df 55%, #8d97a3 100%);
          box-shadow: inset 0 1px 0 #fff, 0 2px 3px rgba(0,0,0,.6); }}
        .cl-px-coin {{ border-radius: 50%; font-family: "Inter", sans-serif; font-weight: 800; color: #7a4a00;
          display: flex; align-items: center; justify-content: center;
          background: radial-gradient(circle at 35% 30%, #fff3b0 0%, #ffd23f 45%, #d98e00 100%);
          box-shadow: inset 0 -2px 2px rgba(120,60,0,.5), 0 2px 3px rgba(0,0,0,.6); }}
        .cl-team-in video, .cl-team-in img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      </style>

      <!-- 1. The pills, arrows and State / Behaviour lists fade away and each class card glides to its
           corner with its object beside it (Customer top-left, DeliveryAgent top-right, Restaurant
           bottom-left, FoodItem bottom-right). 2. Restaurant moves to the centre, its building above it.
           3. Customer moves down to the middle of the left side. -->
      <div id="root" data-composition-id="class-layout" data-width="1920" data-height="1080" data-duration="{DURATION}">
        <div class="cl-all"></div>
        <div class="cl-team">
          <div class="cl-team-in">
            <video id="cl-team-video" class="clip" src="assets/team.mp4" data-start="{TEAM_AT}" data-duration="{TEAM_DUR}"
              data-media-start="0" data-track-index="0" muted playsinline></video>
            <img id="cl-team-still" class="clip" src="assets/team-last.jpg" data-start="{round(TEAM_AT + TEAM_DUR, 2)}"
              data-duration="{round(DURATION - TEAM_AT - TEAM_DUR, 2)}" data-track-index="1" alt="The development team at their desk">
          </div>
        </div>
      </div>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        (function () {{
          var P = {json.dumps(plan, separators=(",", ":"))};
          var ORDER = ["cust", "rest", "agent", "food"];
          var FADE_AT = {FADE_AT}, FADE_DUR = {FADE_DUR};
          var MOVE1_AT = {MOVE1_AT}, MOVE_DUR = {MOVE_DUR}, STAGGER = {STAGGER};
          var MOVE2_AT = {MOVE2_AT}, MOVE2_DUR = {MOVE2_DUR}, MOVE3_AT = {MOVE3_AT}, MOVE3_DUR = {MOVE3_DUR};
          var root = document.querySelector('[data-composition-id="class-layout"]');
          var tl = gsap.timeline({{ paused: true }});
          var all = root.querySelector(".cl-all");   // everything except the team clip lives in here

          function el(id, box, src) {{
            var d = document.createElement("div");
            d.className = "cl-el"; d.id = id;
            d.style.left = box[0] + "px"; d.style.top = box[1] + "px";
            d.style.width = box[2] + "px"; d.style.height = box[3] + "px";
            var i = document.createElement("img"); i.src = src; i.alt = ""; d.appendChild(i);
            all.appendChild(d);
            return d;
          }}

          // The previous slide, rebuilt piece for piece: lists and arrows first, then pills,
          // characters and the class cards.
          var leaving = [], els = {{}};
          ORDER.forEach(function (k) {{
            var s = P[k].start;
            leaving.push(el("cl-" + k + "-arrow", s.arrow, "assets/ob-" + k + "-arrow.png"));
            Object.keys(s.panels).forEach(function (pk) {{
              leaving.push(el("cl-" + k + "-" + pk, s.panels[pk], "assets/ob-" + k + "-" + pk + ".png"));
            }});
          }});
          ORDER.forEach(function (k) {{ leaving.push(el("cl-" + k + "-pill", P[k].start.pill, "assets/ob-" + k + "-pill.png")); }});
          ORDER.forEach(function (k) {{
            els[k] = {{ char: el("cl-" + k + "-char", P[k].start.char, "assets/ob-" + k + ".png"),
                        card: el("cl-" + k + "-card", P[k].start.card, "assets/cd-" + k + ".png") }};
          }});

          // FoodItem's "< Enumeration >" tag, inside its card (card sized at 0.63 of the artwork).
          var E = {json.dumps(cd["food"]["enum"])}, FH = {cd["food"]["box"][3]}, FW = {cd["food"]["box"][2]};
          var en = document.createElement("div");
          en.className = "cl-enum"; en.id = "cl-food-enum";
          en.style.left = (39 / FW * 100) + "%"; en.style.width = (365 / FW * 100) + "%";
          en.style.top = (128 / FH * 100) + "%"; en.style.height = ((E[0] + E[1] - 128) / FH * 100) + "%";
          en.style.fontSize = (40 * 0.63) + "px";
          en.innerHTML = "<b>&lt;</b>Enumeration<b>&gt;</b>";
          els.food.card.appendChild(en);

          // 1. Lists, arrows and pills fade; cards and objects glide to the corners.
          tl.to(leaving, {{ opacity: 0, duration: FADE_DUR, ease: "power1.inOut" }}, FADE_AT);
          ORDER.forEach(function (k, i) {{
            var at = MOVE1_AT + i * STAGGER;
            tl.to(els[k].card, Object.assign({{ duration: MOVE_DUR, ease: "power2.inOut" }}, P[k].card1), at);
            tl.to(els[k].char, Object.assign({{ duration: MOVE_DUR, ease: "power2.inOut" }}, P[k].char1), at);
          }});

          // 2. Restaurant moves to the centre, its building settling above the card.
          tl.to(els.rest.card, Object.assign({{ duration: MOVE2_DUR, ease: "power2.inOut" }}, P.rest.card2), MOVE2_AT);
          tl.to(els.rest.char, Object.assign({{ duration: MOVE2_DUR, ease: "power2.inOut" }}, P.rest.char2), MOVE2_AT);

          // 3. Customer moves down to the middle of the left side.
          tl.to(els.cust.card, Object.assign({{ duration: MOVE3_DUR, ease: "power2.inOut" }}, P.cust.card3), MOVE3_AT);
          tl.to(els.cust.char, Object.assign({{ duration: MOVE3_DUR, ease: "power2.inOut" }}, P.cust.char3), MOVE3_AT);

          // ---------------- Has-A ----------------
          var H = {json.dumps(HASA)};
          var CHAR = {CHAR};
          function div(cls, css, html) {{
            var d = document.createElement("div"); d.className = cls;
            Object.keys(css).forEach(function (k) {{ d.style[k] = css[k]; }});
            if (html) d.innerHTML = html;
            all.appendChild(d); return d;
          }}
          // Type text into el one character at a time (no caret); returns the time it finishes.
          function typeOn(el, text, at) {{
            el.textContent = "";
            text.split("").forEach(function (ch, i) {{
              var sp = document.createElement("span"); sp.className = "cl-tc";
              sp.textContent = ch === " " ? "\u00a0" : ch; el.appendChild(sp);
              tl.set(sp, {{ opacity: 1 }}, at + i * CHAR);
            }});
            return at + text.length * CHAR;
          }}
          var rods = {{}}, dias = {{}};
          Object.keys(H).forEach(function (k) {{
            var h = H[k];
            rods[k] = div("cl-rod", {{ left: h.x0 + "px", top: h.y + "px", width: (h.x1 - h.x0) + "px",
              transformOrigin: "0 50%",            // Customer's rod runs out of its card; the others out of their diamonds
              borderRadius: h.end === "right" ? "5px 0 0 5px" : "0 5px 5px 0" }});  // square where it meets the diamond
            dias[k] = div("cl-dia-pos", {{ left: h.dia + "px", top: h.y + "px" }},
              '<div class="cl-dia"><div class="cl-dia-hole"></div></div>');
          }});
          function rod(k, at) {{ tl.fromTo(rods[k], {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power2.inOut" }}, at); }}
          function dia(k, at) {{
            tl.fromTo(dias[k], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, at);
            tl.fromTo(dias[k], {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.5, ease: "back.out(2.2)",
              immediateRender: false }}, at);
          }}
          function label(k, text, above, at) {{
            var h = H[k];   // centre over the rod's visible part (between the card and the diamond's tip)
            var cx = h.end === "right" ? (h.x0 + h.dia - 21) / 2 : (h.dia + 21 + h.x1) / 2;
            var el = div("cl-lbl", {{ left: cx + "px", top: (above ? h.y - 58 : h.y + 22) + "px" }});
            return typeOn(el, text, at);
          }}
          var DIA_HALF = {DIA};

          // 1. Customer -> Restaurant: the rod runs out of the Customer card, the diamond pops at the Restaurant.
          rod("cust", {B1});
          dia("cust", {B1} + 0.65);
          label("cust", "Has-A", true, {B1} + 1.1);

          // 2. DeliveryAgent slides down to meet its line.
          tl.to(els.agent.card, {{ y: P.agent.card1.y + {AGENT_DOWN}, duration: 0.8, ease: "power2.inOut" }}, {B2});
          tl.to(els.agent.char, {{ y: P.agent.char1.y + {AGENT_DOWN}, duration: 0.8, ease: "power2.inOut" }}, {B2});

          // 3. Diamonds at the Restaurant, rods out to DeliveryAgent and FoodItem.
          dia("agent", {B3A}); rod("agent", {B3A} + 0.3);
          dia("food", {B3B}); rod("food", {B3B} + 0.3);

          // 4. "Has-A" on both.
          label("agent", "Has-A", true, {B4A});
          label("food", "Has-A", true, {B4B});

          // 5. Title: the user's Has-A | AGGREGATION / COMPOSITION plaques (scaled 0.46). Each plaque
          //    pops in empty, then its own lettering is revealed one letter at a time.
          var TT = {json.dumps(TT)};
          var title = div("cl-tt", {{}});
          function plaque(k, src) {{
            var b = TT[k].box, d = document.createElement("div");
            d.className = "cl-tt-el"; d.id = "cl-tt-" + k;
            d.style.left = b[0] + "px"; d.style.top = b[1] + "px"; d.style.width = b[2] + "px"; d.style.height = b[3] + "px";
            d.innerHTML = '<img src="assets/tt-' + k + '.png" alt="" style="width:100%;height:100%;display:block">';
            title.appendChild(d); return d;
          }}
          function letters(k, at, gap) {{
            var b = TT[k].box, n = TT[k].inner, e = TT[k].edges;
            for (var i = 0; i < e.length - 1; i++) {{
              var c = document.createElement("div"), x = b[0] + n[0] + e[i], y = b[1] + n[1];
              c.className = "cl-tt-ch"; c.id = "cl-tt-" + k + i;
              c.style.left = x + "px"; c.style.top = y + "px";
              c.style.width = (e[i + 1] - e[i]) + "px"; c.style.height = n[3] + "px";
              c.style.backgroundPosition = (-x) + "px " + (-y) + "px";
              title.appendChild(c);
              tl.set(c, {{ opacity: 1 }}, at + i * gap);
            }}
            return at + (e.length - 1) * gap;
          }}
          function pop(el, at) {{
            tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power1.out" }}, at);
            tl.fromTo(el, {{ scale: 0.85 }}, {{ scale: 1, duration: 0.5, ease: "back.out(1.6)", immediateRender: false }}, at);
          }}
          var ttHas = plaque("has"), ttBar = plaque("bar"), ttAgg = plaque("agg"), ttComp = plaque("comp");
          ttBar.style.transformOrigin = "50% 0";
          pop(ttHas, {B5});
          var t5 = letters("has", {B5} + 0.5, 0.1);
          tl.fromTo(ttBar, {{ opacity: 0, scaleY: 0 }}, {{ opacity: 1, scaleY: 1, duration: 0.45, ease: "power2.out" }}, t5 + 0.5);
          pop(ttAgg, t5 + 1.2);
          t5 = letters("agg", t5 + 1.6, 0.06);
          pop(ttComp, t5 + 0.6);
          letters("comp", t5 + 1.0, 0.06);

          // 6. Restaurant - FoodItem is composition: its diamond fills solid.
          tl.to(dias.food.querySelector(".cl-dia-hole"), {{ opacity: 0, duration: 0.35, ease: "power1.inOut" }}, {B6});
          tl.fromTo(dias.food, {{ scale: 1 }}, {{ scale: 1.35, duration: 0.18, ease: "power1.out", yoyo: true, repeat: 1,
            immediateRender: false }}, {B6});
          label("food", "Composition", false, {B6} + 0.4);

          // 7. The other two are aggregation.
          label("cust", "Aggregation", false, {B7A});
          label("agent", "Aggregation", false, {B7B});

          // ---------------- The development team at work ----------------
          tl.to(title, {{ opacity: 0, duration: 0.5, ease: "power1.inOut" }}, {B8});
          tl.fromTo(all, {{ y: 0 }}, {{ y: -{LIFT}, duration: 1.0, ease: "power2.inOut" }}, {B8} + 0.3);
          var team = root.querySelector(".cl-team");
          tl.fromTo(team, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, {B9});
          tl.fromTo(team, {{ y: 60, scale: 0.85 }}, {{ y: 0, scale: 1, duration: 0.6, ease: "back.out(1.6)",
            immediateRender: false }}, {B9});

          // ---------------- PlatinumCustomer ----------------
          // Placed inside the lifted layer, so add the lift back to land on frame positions.
          var PL = {json.dumps(PL)}, PK = {PK}, LIFT = {LIFT};
          var pc = {json.dumps(PL_CARD)}, pg = {json.dumps(PL_GIRL)};
          var plGirl = el("cl-plat-girl", [pg[0], pg[1] + LIFT, pg[2], pg[3]], "assets/ob-plat.png");
          var plCard = el("cl-plat-card", [pc[0], pc[1] + LIFT, pc[2], pc[3]], "assets/cd-plat-e.png");
          plGirl.style.opacity = "0"; plCard.style.opacity = "0";
          plGirl.style.transformOrigin = "50% 100%"; plCard.style.transformOrigin = "50% 30%";
          var plSplit = document.createElement("img");
          plSplit.src = "assets/cd-plat-s.png"; plSplit.alt = ""; plSplit.className = "cl-pl-split";
          plCard.appendChild(plSplit);
          function plBlock(r, id) {{
            var b = document.createElement("div"); b.className = "cl-pl-block"; b.id = id;
            b.style.left = r[0] * PK + "px"; b.style.top = r[1] * PK + "px";
            b.style.width = r[2] * PK + "px"; b.style.height = r[3] * PK + "px";
            b.style.backgroundImage = "url(assets/cd-plat.png)";
            b.style.backgroundSize = PL.box_w * PK + "px " + PL.box_h * PK + "px";
            b.style.backgroundPosition = (-r[0] * PK) + "px " + (-r[1] * PK) + "px";
            plCard.appendChild(b); return b;
          }}
          var plState = plBlock(PL.s, "cl-plat-state"), plBeh = plBlock(PL.b, "cl-plat-beh");
          var plTitle = document.createElement("div"); plTitle.className = "cl-pl-title"; plTitle.id = "cl-plat-title";
          plTitle.style.left = PL.title[0] * PK + "px"; plTitle.style.top = PL.title[1] * PK + "px";
          plTitle.style.width = PL.title[2] * PK + "px"; plTitle.style.height = PL.title[3] * PK + "px";
          plTitle.style.fontSize = "27px";
          plCard.appendChild(plTitle);

          tl.fromTo(plGirl, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {P1});
          tl.fromTo(plGirl, {{ scale: 0.6 }}, {{ scale: 1, duration: 0.6, ease: "back.out(1.6)", immediateRender: false }}, {P1});
          tl.fromTo(plCard, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, {P2});
          tl.fromTo(plCard, {{ scale: 0.85 }}, {{ scale: 1, duration: 0.6, ease: "back.out(1.5)", immediateRender: false }}, {P2});
          typeOn(plTitle, "PlatinumCustomer", {P2} + 0.7);
          tl.fromTo(plSplit, {{ clipPath: "inset(0% 50% 0% 50%)" }},
            {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.6, ease: "power2.inOut" }}, {P3});
          tl.fromTo(plState, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power1.inOut" }}, {P4});
          tl.fromTo(plBeh, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power1.inOut" }}, {P5});

          // ---------------- PlatinumCustomer grows ----------------
          // The finished card is re-laid as slices (identical at first); then a clean band opens inside the
          // State panel and later inside the Behaviour panel, pushing the rest down, and the new rows type on.
          var H1 = 82, H2 = 62, CW = PL.box_w * PK;          // band heights in artwork px (2 rows each)
          var px = document.createElement("div"); px.className = "cl-px"; px.id = "cl-px";
          px.style.height = PL.box_h * PK + "px";
          plCard.insertBefore(px, plTitle);
          function slice(parent, y0, y1, id) {{
            var d = document.createElement("div"); d.className = "cl-px-sl"; d.id = id;
            d.style.top = y0 * PK + "px"; d.style.height = (y1 - y0) * PK + "px";
            d.style.backgroundPosition = "0 " + (-y0 * PK) + "px";
            parent.appendChild(d); return d;
          }}
          function band(parent, y0, h, src, id) {{
            var b = document.createElement("img"); b.src = src; b.alt = ""; b.id = id;
            b.style.top = y0 * PK + "px"; b.style.height = h * PK + "px"; b.style.transformOrigin = "50% 0";
            b.style.transform = "scaleY(0)";
            parent.appendChild(b); return b;
          }}
          function wrap(parent, id) {{
            var w = document.createElement("div"); w.id = id;
            w.style.position = "absolute"; w.style.left = "0"; w.style.top = "0"; w.style.width = "100%";
            parent.appendChild(w); return w;
          }}
          slice(px, 0, 330, "cl-px-top");
          var b1 = band(px, 330, H1, "assets/cd-plat-band1.png", "cl-px-b1");
          var low1 = wrap(px, "cl-px-low1");
          slice(low1, 330, 568, "cl-px-mid");
          var b2 = band(low1, 568, H2, "assets/cd-plat-band2.png", "cl-px-b2");
          var low2 = wrap(low1, "cl-px-low2");
          slice(low2, 568, PL.box_h, "cl-px-bot");

          var newNames = [];
          // One new row: icon, then name, " : ", type typed on. Positions in artwork px of the card.
          function newRow(parent, cy, icon, name, type, at, fs) {{
            var r = document.createElement("div"); r.className = "cl-px-row";
            r.style.left = "0"; r.style.top = (cy - 20) * PK + "px"; r.style.height = 40 * PK + "px";
            r.style.width = CW + "px"; r.style.fontSize = fs * PK + "px";
            parent.appendChild(r);
            var ic = document.createElement("div"); ic.style.position = "absolute";
            var cube = icon === "cube";      // the cube is cropped 46 x 36 from the card itself
            ic.style.left = (cube ? 68 : 74) * PK + "px"; ic.style.top = (cube ? 2 : 3) * PK + "px";
            ic.style.width = (cube ? 46 : 34) * PK + "px"; ic.style.height = (cube ? 36 : 34) * PK + "px";
            if (icon === "cube") ic.innerHTML = '<img src="assets/cd-plat-cube.png" alt="" style="width:100%;height:100%">';
            else {{ ic.className = icon === "id" ? "cl-px-id" : "cl-px-coin"; ic.textContent = icon === "id" ? "ID" : "C";
                    ic.style.fontSize = 15 * PK + "px"; ic.style.position = "absolute"; }}
            r.appendChild(ic);
            tl.fromTo(ic, {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }}, at);
            var nm = document.createElement("div"); nm.style.position = "absolute"; nm.style.left = 145 * PK + "px";
            r.appendChild(nm);
            newNames.push(nm);
            var t = typeOn(nm, name, at + 0.3);
            if (type) {{
              var co = document.createElement("div"); co.style.position = "absolute"; co.style.left = 289 * PK + "px";
              r.appendChild(co); t = typeOn(co, ":", t + 0.1);
              var ty = document.createElement("div"); ty.className = "cl-px-type"; ty.style.left = 327 * PK + "px";
              r.appendChild(ty); t = typeOn(ty, type, t + 0.1);
            }}
            return t;
          }}

          // Make room: the card and its girl rise 47 px; the slices take over from the card underneath.
          tl.to([plCard, plGirl], {{ y: -47, duration: 0.6, ease: "power2.inOut" }}, {X1});
          tl.set(px, {{ opacity: 1 }}, {X1});
          // State panel opens, then platinum_id ... pause ... credits
          tl.to(b1, {{ scaleY: 1, duration: 0.5, ease: "power2.inOut" }}, {X2});
          tl.fromTo(low1, {{ y: 0 }}, {{ y: H1 * PK, duration: 0.5, ease: "power2.inOut" }}, {X2});
          var t6 = newRow(px, 344, "id", "platinum_id", "int", {X2} + 0.7, 28);
          newRow(px, 385, "coin", "credits", "int", t6 + 0.8, 28);
          // Behaviour panel opens, then free_delivery() ... pause ... exclusive_offers()
          tl.to(b2, {{ scaleY: 1, duration: 0.5, ease: "power2.inOut" }}, {X3});
          tl.fromTo(low2, {{ y: 0 }}, {{ y: H2 * PK, duration: 0.5, ease: "power2.inOut" }}, {X3});
          var t7 = newRow(low1, 583, "cube", "free_delivery()", null, {X3} + 0.7, 25);
          newRow(low1, 614, "cube", "exclusive_offers()", null, t7 + 0.8, 25);
          // After the repeated lines turn yellow (class-hl.html), what PlatinumCustomer adds turns pink.
          tl.to(newNames, {{ color: "#ff7ad9", duration: 0.4, ease: "power1.inOut", stagger: 0.25 }}, {PINK});

          window.__timelines["class-layout"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(html)
print("duration", DURATION)
