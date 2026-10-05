"""Write compositions/objects.html from objects.json (positions measured from the artwork)."""
import json

SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"
OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\compositions\objects.html"
m = json.load(open(SCR + r"\objects.json"))

# --- timing (seconds, scene-local); the same rules are used in the page script ---
ENTER = {"cust": 0.3, "rest": 1.6, "agent": 2.9, "food": 5.0}
PILL_AFTER = {"cust": 0.55, "rest": 0.55, "agent": 1.55, "food": 0.55}
# "Unified Modeling Language" -> "UML", after all four objects are in and before the panels.
PHRASE, INITIALS = "Unified Modeling Language", [0, 8, 17]
UML_AT, LETTER_GAP, STRETCH, FLASH_STEP = 6.2, 0.06, 0.6, 0.08
READ_AT = round(UML_AT + (len(PHRASE) - 1) * LETTER_GAP + STRETCH, 2)   # whole phrase is up
COLLAPSE_AT, COLLAPSE_DUR = round(READ_AT + 1.2, 2), 0.9                # others fold away
UML_FLASH_AT = round(COLLAPSE_AT + COLLAPSE_DUR + 0.1, 2)               # U, M, L flash again
UML_OUT_AT, UML_OUT_DUR = round(UML_FLASH_AT + 2.2, 2), 0.5
DETAIL_AT, DETAIL_DUR, HOLD = round(UML_OUT_AT + UML_OUT_DUR + 0.2, 2), 0.8, 3.0
t = DETAIL_AT + DETAIL_DUR
# After the hold the whole slide shrinks to the top row (0.725 x) to make room for the class
# cards underneath; it then stays on screen for the whole class-cards scene (20.9 s).
SHRINK_AT, SHRINK_DUR, CARDS_DUR = round(t + HOLD, 2), 1.0, 20.9
CARDS_AT = round(SHRINK_AT + SHRINK_DUR, 2)
DURATION = round(CARDS_AT + CARDS_DUR, 2)

data = {}
for k, o in m["objects"].items():
    data[k] = {
        "c": [o["char"][q] for q in "xywh"], "p": [o["pill"][q] for q in "xywh"], "a": [o["arrow"][q] for q in "xywh"],
        "panels": [{"id": pk, "box": [p["x"], p["y"], p["w"], p["h"]], "lx": [p["lx0"], p["lx1"]], "lines": p["lines"]}
                   for pk, p in o["panels"].items()],
    }

html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Objects: state and behaviour</title>
  </head>
  <body>
    <template id="objects-template">
      <style>
        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
          pointer-events: none;
          background: #000000;
        }}
        /* The user's artwork is 1670 x 942; every piece is placed in those pixels, then the whole
           stage is scaled 1.14 to fill the frame (1904 x 1074, centred). */
        .ob-stage {{ position: absolute; left: 8px; top: 3px; width: 1670px; height: 942px;
          transform-origin: 0 0; }}  /* its scale (1.14, later 0.725) is owned by the timeline */
        .ob-el {{ position: absolute; opacity: 0; }}
        .ob-el > img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; }}
        .ob-char {{ transform-origin: 50% 100%; }}
        .ob-pill {{ transform-origin: 50% 50%; }}
        /* Speed streaks behind the scooter while it glides in. */
        .ob-streak {{ position: absolute; height: 5px; border-radius: 3px; opacity: 0;
          background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.85)); }}
        /* Unified Modeling Language -> UML, centred in the empty space under the objects. */
        .ob-uml {{ position: absolute; left: 0; right: 0; top: 770px; height: 190px;
          display: flex; align-items: center; justify-content: center; white-space: nowrap;
          font-family: "Inter", "Segoe UI", sans-serif; font-weight: 500; font-size: 92px;
          line-height: 1.25; color: #e47de8; transform-origin: 50% 50%; }}
        .ob-ch {{ display: inline-block; vertical-align: top; opacity: 0; max-width: 220px;
          transform-origin: 50% 100%; text-shadow: 0 0 18px rgba(228,125,232,.45); }}
      </style>

      <!-- Customer, Restaurant, the DeliveryAgent (riding in from the right) and FoodItem appear one
           after another with their name pills; then all the arrows and State and Behaviour panels
           fade in together. -->
      <div id="root" data-composition-id="objects" data-width="1920" data-height="1080" data-duration="{DURATION}">
        <div class="ob-stage"></div>
        <div class="ob-uml"></div>
      </div>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        (function () {{
          var D = {json.dumps(data, separators=(",", ":"))};
          var ORDER = ["cust", "rest", "agent", "food"];
          var ENTER = {json.dumps(ENTER)};
          var PILL_AFTER = {json.dumps(PILL_AFTER)};
          var DETAIL_AT = {DETAIL_AT}, DETAIL_DUR = {DETAIL_DUR};  // every State/Behaviour panel fades in at once
          var GLIDE_DX = 820, GLIDE_DUR = 1.5;  // the agent starts fully off the right edge

          var root = document.querySelector('[data-composition-id="objects"]');
          var stage = root.querySelector(".ob-stage");
          var tl = gsap.timeline({{ paused: true }});

          function el(cls, box, src, id) {{
            var d = document.createElement("div");
            d.className = "ob-el " + cls;
            if (id) d.id = id;
            d.style.left = box[0] + "px"; d.style.top = box[1] + "px";
            d.style.width = box[2] + "px"; d.style.height = box[3] + "px";
            if (src) {{ var i = document.createElement("img"); i.src = src; i.alt = ""; d.appendChild(i); }}
            stage.appendChild(d);
            return d;
          }}
          function pop(target, at, from, dur, ease) {{
            tl.fromTo(target, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power1.out" }}, at);
            tl.fromTo(target, {{ scale: from }}, {{ scale: 1, duration: dur, ease: ease, immediateRender: false }}, at);
          }}

          // Panels and arrows first (drawn underneath), then pills, then the characters on top.
          ORDER.forEach(function (k) {{
            D[k].arrowEl = el("ob-arrow", D[k].a, "assets/ob-" + k + "-arrow.png", "ob-" + k + "-arrow");
            D[k].panelEls = D[k].panels.map(function (p) {{
              return el("ob-panel", p.box, "assets/ob-" + k + "-" + p.id + ".png", "ob-" + k + "-" + p.id);
            }});
          }});
          ORDER.forEach(function (k) {{
            D[k].pillEl = el("ob-pill", D[k].p, "assets/ob-" + k + "-pill.png", "ob-" + k + "-pill");
          }});
          ORDER.forEach(function (k) {{
            D[k].charEl = el("ob-char", D[k].c, "assets/ob-" + k + ".png", "ob-" + k);
          }});

          // Streaks ride along with the agent, trailing to his right.
          var ag = D.agent.charEl;
          [[250, 150, 220], [300, 210, 280], [340, 120, 330]].forEach(function (s, i) {{
            var st = document.createElement("div");
            st.className = "ob-streak"; st.id = "ob-streak" + i;
            st.style.left = s[0] + "px"; st.style.width = s[1] + "px"; st.style.top = s[2] + "px";
            ag.appendChild(st);
          }});

          // 1-4. The objects arrive one after another.
          pop(D.cust.charEl, ENTER.cust, 0.6, 0.7, "back.out(1.6)");
          pop(D.rest.charEl, ENTER.rest, 0.6, 0.7, "back.out(1.6)");
          // The agent glides in from the right like a scooter pulling up: fast, then easing to a stop
          // with a small bounce on the suspension and a lean that straightens as he stops.
          var A0 = ENTER.agent;
          tl.fromTo(ag, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, A0);
          tl.fromTo(ag, {{ x: GLIDE_DX, rotation: -3 }},
            {{ x: 0, rotation: 0, duration: GLIDE_DUR, ease: "power3.out", immediateRender: false }}, A0);
          tl.fromTo(ag, {{ y: 0 }}, {{ y: -5, duration: 0.14, ease: "sine.inOut", yoyo: true, repeat: 7,
            immediateRender: false }}, A0);
          tl.fromTo(ag, {{ scaleY: 1 }}, {{ scaleY: 0.97, duration: 0.12, ease: "power1.out", yoyo: true, repeat: 1,
            immediateRender: false }}, A0 + GLIDE_DUR - 0.15);
          tl.fromTo(ag.querySelectorAll(".ob-streak"), {{ opacity: 0 }},
            {{ opacity: 0.9, duration: 0.2, stagger: 0.05 }}, A0 + 0.05);
          tl.to(ag.querySelectorAll(".ob-streak"), {{ opacity: 0, duration: 0.5, ease: "power1.in" }}, A0 + 0.9);
          tl.fromTo(D.food.charEl, {{ rotation: -25 }}, {{ rotation: 0, duration: 0.8, ease: "back.out(1.4)",
            immediateRender: false }}, ENTER.food);
          pop(D.food.charEl, ENTER.food, 0.4, 0.8, "back.out(1.6)");
          ORDER.forEach(function (k) {{ pop(D[k].pillEl, ENTER[k] + PILL_AFTER[k], 0.5, 0.45, "back.out(2)"); }});

          // Unified Modeling Language: each letter stretches in through a rainbow flash; then every
          // letter but U, M and L folds away, the three draw together into "UML" and flash again.
          var PHRASE = {json.dumps(PHRASE)}, INITIALS = {json.dumps(INITIALS)};
          var RAINBOW = ["#ff4d4d", "#ffa53b", "#ffe83b", "#4dff7a", "#3bd1ff", "#7a6bff", "#e47de8"];
          var FLASH = "0 0 26px rgba(255,255,255,1), 0 0 54px rgba(255,255,255,.75)";
          var GLOW = "0 0 18px rgba(228,125,232,.45)";
          var uml = root.querySelector(".ob-uml"), chars = [], keep = [], fold = [];
          PHRASE.split("").forEach(function (ch, i) {{
            var sp = document.createElement("span");
            sp.className = "ob-ch"; sp.id = "ob-ch" + i;
            sp.textContent = ch === " " ? "\u00a0" : ch;
            uml.appendChild(sp); chars.push(sp);
            (INITIALS.indexOf(i) >= 0 ? keep : fold).push(sp);
          }});
          function rainbow(sp, at) {{
            tl.fromTo(sp, {{ color: RAINBOW[0], textShadow: FLASH }},
              {{ color: RAINBOW[1], duration: {FLASH_STEP}, ease: "none", immediateRender: false }}, at);
            for (var r = 2; r < RAINBOW.length; r++) {{
              tl.to(sp, {{ color: RAINBOW[r], duration: {FLASH_STEP}, ease: "none" }}, at + (r - 1) * {FLASH_STEP});
            }}
            tl.to(sp, {{ textShadow: GLOW, duration: (RAINBOW.length - 1) * {FLASH_STEP}, ease: "power1.out" }}, at);
          }}
          chars.forEach(function (sp, i) {{
            var at = {UML_AT} + i * {LETTER_GAP};
            tl.fromTo(sp, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12, ease: "power1.out" }}, at);
            tl.fromTo(sp, {{ scaleX: 0.4, scaleY: 2.4 }},
              {{ scaleX: 1, scaleY: 1, duration: {STRETCH}, ease: "elastic.out(1, 0.5)", immediateRender: false }}, at);
            rainbow(sp, at);
          }});
          tl.set(fold, {{ overflow: "hidden" }}, {COLLAPSE_AT});
          tl.to(fold, {{ opacity: 0, duration: 0.35, ease: "power1.in" }}, {COLLAPSE_AT});
          tl.fromTo(fold, {{ maxWidth: 220 }}, {{ maxWidth: 0, duration: {COLLAPSE_DUR}, ease: "power2.inOut" }}, {COLLAPSE_AT} + 0.1);
          // Grow from 92 px to about 150 px (a transform, not a font-size change) and space U, M, L apart.
          tl.fromTo(uml, {{ scale: 1 }}, {{ scale: 1.63, duration: {COLLAPSE_DUR}, ease: "power2.inOut" }}, {COLLAPSE_AT} + 0.1);
          tl.fromTo(keep[0], {{ x: 0 }}, {{ x: -12, duration: {COLLAPSE_DUR}, ease: "power2.inOut", immediateRender: false }}, {COLLAPSE_AT} + 0.1);
          tl.fromTo(keep[2], {{ x: 0 }}, {{ x: 12, duration: {COLLAPSE_DUR}, ease: "power2.inOut", immediateRender: false }}, {COLLAPSE_AT} + 0.1);
          keep.forEach(function (sp, i) {{
            var at = {UML_FLASH_AT} + i * 0.12;
            tl.fromTo(sp, {{ scaleX: 0.6, scaleY: 1.8 }},
              {{ scaleX: 1, scaleY: 1, duration: {STRETCH}, ease: "elastic.out(1, 0.5)", immediateRender: false }}, at);
            rainbow(sp, at);
          }});
          tl.to(uml, {{ opacity: 0, duration: {UML_OUT_DUR}, ease: "power1.inOut" }}, {UML_OUT_AT});

          // Then every arrow and every State and Behaviour panel fades in together.
          var details = [];
          ORDER.forEach(function (k) {{ details.push(D[k].arrowEl); details = details.concat(D[k].panelEls); }});
          tl.fromTo(details, {{ opacity: 0 }}, {{ opacity: 1, duration: DETAIL_DUR, ease: "power1.inOut" }}, DETAIL_AT);

          // The slide shrinks to the top row (each object's column lands over its class card).
          // Final: left 8 + 330.3 = 338.3, top 3 - 18 = -15, scale 0.725 (art y 40 -> frame 14).
          tl.fromTo(stage, {{ x: 0, y: 0, scale: 1.14 }},
            {{ x: 330.3, y: -18, scale: 0.725, duration: {SHRINK_DUR}, ease: "power2.inOut" }}, {SHRINK_AT});

          window.__timelines["objects"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(html)
print("uml", UML_AT, READ_AT, COLLAPSE_AT, UML_FLASH_AT, UML_OUT_AT, "detail", DETAIL_AT, "duration", DURATION, "cards at", CARDS_AT)
