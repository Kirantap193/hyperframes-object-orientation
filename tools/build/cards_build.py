"""Write compositions/class-cards.html from cards.json."""
import json

SCR = r"C:\Users\kiran\AppData\Local\Temp\claude\C--Users-kiran-Documents-hyperframes\526ee048-95c2-4a95-af18-3d33de25148c\scratchpad"
OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\compositions\class-cards.html"
m = json.load(open(SCR + r"\cards.json"))

LEAD, STEP, CARD_GAP, POP, WIPE, FADE, HOLD = 0.4, 1.3, 1.3, 0.6, 0.6, 0.6, 3.0
# per card: empty at T, split at T+STEP, State at T+2*STEP, Behaviour at T+3*STEP; FoodItem: empty, State
t = LEAD
starts = {}
for k, c in m.items():
    starts[k] = round(t, 2)
    steps = 4 if "b" in c else 2
    t += (steps - 1) * STEP + CARD_GAP
DURATION = round(t - CARD_GAP + FADE + HOLD, 2)

html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Class cards</title>
  </head>
  <body>
    <template id="class-cards-template">
      <style>
        #root {{
          position: absolute;
          inset: 0;
          overflow: hidden;
          pointer-events: none;
        }}
        /* The user's artwork is 2000 x 669 with the cards spanning x 26 - 1976, y 42 - 642. Scaled
           0.63 the row is 1229 x 378, centred, sitting under the shrunken objects row (y 672 - 1050);
           each card lands under its own object. */
        .cc-stage {{ position: absolute; left: 329.4px; top: 645.5px; width: 2000px; height: 669px;
          transform: scale(0.63); transform-origin: 0 0; }}
        .cc-card {{ position: absolute; opacity: 0; transform-origin: 50% 30%; }}
        .cc-card > img {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; }}
        .cc-split {{ clip-path: inset(0 50% 0 50%); }}
        /* State / Behaviour text: windows onto the original card, over the painted-out panels. */
        .cc-block {{ position: absolute; opacity: 0; background-repeat: no-repeat; }}
        /* "< Enumeration >" inside the FoodItem card, in the band added above its fields. */
        .cc-enum {{
          position: absolute; display: flex; align-items: center; justify-content: center; gap: 0.45em;
          white-space: nowrap; font-family: "Poppins", "Inter", "Segoe UI", sans-serif; font-weight: 500;
          color: #efe2ff; letter-spacing: 0.03em;
          text-shadow: 0 0 12px rgba(200,120,255,.55), 0 2px 3px rgba(0,0,0,.7);
        }}
        .cc-enum b {{ font-weight: 600; color: #ff86de; }}
      </style>

      <!-- Drawn over the objects scene, which has shrunk to the top row. Each class card in turn: 1. the empty card, 2. its body splits into two, 3. State,
           4. Behaviour - with a pause before each step. FoodItem has State only. -->
      <div id="root" data-composition-id="class-cards" data-width="1920" data-height="1080" data-duration="{DURATION}">
        <div class="cc-stage"></div>
      </div>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        (function () {{
          var C = {json.dumps(m, separators=(",", ":"))};
          var START = {json.dumps(starts)};
          var STEP = {STEP}, POP = {POP}, WIPE = {WIPE}, FADE = {FADE};
          var root = document.querySelector('[data-composition-id="class-cards"]');
          var stage = root.querySelector(".cc-stage");
          var tl = gsap.timeline({{ paused: true }});

          function box(parent, cls, r, id) {{
            var d = document.createElement("div");
            d.className = cls; d.id = id;
            d.style.left = r[0] + "px"; d.style.top = r[1] + "px";
            d.style.width = r[2] + "px"; d.style.height = r[3] + "px";
            parent.appendChild(d);
            return d;
          }}
          function img(parent, src, cls) {{
            var i = document.createElement("img"); i.src = src; i.alt = ""; if (cls) i.className = cls;
            parent.appendChild(i); return i;
          }}
          function block(card, k, r, id) {{
            var b = box(card, "cc-block", r, id);
            b.style.backgroundImage = "url(assets/cd-" + k + ".png)";
            b.style.backgroundPosition = (-r[0]) + "px " + (-r[1]) + "px";
            return b;
          }}

          Object.keys(C).forEach(function (k) {{
            var c = C[k], T = START[k];
            var card = box(stage, "cc-card", c.box, "cc-" + k);
            var hasB = !!c.b;
            img(card, "assets/cd-" + k + (hasB ? "-e" : "-s") + ".png");
            var split = hasB ? img(card, "assets/cd-" + k + "-s.png", "cc-split") : null;
            var sBlock = block(card, k, c.s, "cc-" + k + "-state");
            var bBlock = hasB ? block(card, k, c.b, "cc-" + k + "-beh") : null;
            var en = null;
            if (c.enum) {{
              // FoodItem is an enumeration: its tag sits inside the card, above the fields.
              en = document.createElement("div");
              en.className = "cc-enum"; en.id = "cc-" + k + "-enum";
              en.style.left = "39px"; en.style.width = "365px";
              en.style.top = "128px"; en.style.height = (c.enum[0] + c.enum[1] - 128) + "px";
              en.style.fontSize = "40px"; en.style.opacity = "0";
              en.innerHTML = "<b>&lt;</b>Enumeration<b>&gt;</b>";
              card.appendChild(en);
            }}

            // 1. The empty card pops up.
            tl.fromTo(card, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, T);
            tl.fromTo(card, {{ scale: 0.85 }}, {{ scale: 1, duration: POP, ease: "back.out(1.5)",
              immediateRender: false }}, T);
            var t = T + STEP;
            if (en) {{
              tl.fromTo(en, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power1.out" }}, T + 0.4);
              tl.fromTo(en, {{ scale: 0.5 }}, {{ scale: 1, duration: 0.5, ease: "back.out(2)", immediateRender: false }}, T + 0.4);
            }}
            // 2. Its body splits in two: the divider opens from the middle outwards.
            if (split) {{
              tl.fromTo(split, {{ clipPath: "inset(0% 50% 0% 50%)" }},
                {{ clipPath: "inset(0% 0% 0% 0%)", duration: WIPE, ease: "power2.inOut" }}, t);
              t += STEP;
            }}
            // 3. State, then 4. Behaviour.
            tl.fromTo(sBlock, {{ opacity: 0 }}, {{ opacity: 1, duration: FADE, ease: "power1.inOut" }}, t);
            if (bBlock) {{
              tl.fromTo(bBlock, {{ opacity: 0 }}, {{ opacity: 1, duration: FADE, ease: "power1.inOut" }}, t + STEP);
            }}
          }});

          window.__timelines["class-cards"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(html)
print("starts", starts, "duration", DURATION)
