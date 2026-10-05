"""Write compositions/class-hl.html: drawn over the class-layout slide.
1. The white-shirt developer in the team clip gets frustrated (punch-in, storm cloud, anger mark,
   sweat drops, shake).  2. Every repeated line of Customer and PlatinumCustomer turns yellow."""
import json

OUT = r"C:\Users\kiran\Documents\hyperframes\video-11\compositions\class-hl.html"

# Frame geometry of the pieces underneath (see layout_build.py).
TEAM = [700, 688, 640, 360]                 # team clip inner box (frame px), its still is showing
FACE = [500, 145]                           # developer's face in the 640 x 360 clip box
CUST = [218, 224, 0.6210]                   # Customer card: frame x, y, scale of its artwork
PLAT = [218, 603, 0.62, 82 * 0.62]          # PlatinumCustomer: x, y, scale, Behaviour shift after it grew
STATE_ROWS = [[155, 199], [199, 236], [236, 277], [277, 327]]
BEH_ROWS = [[347 + i * 31.3, 347 + (i + 1) * 31.3] for i in range(7)]
TEXT_X = [138, 600]

F_IN, F_OUT = 0.0, 4.4                      # frustration
H_CUST, H_PLAT, ROW_GAP = 5.6, 8.2, 0.12    # yellow: Customer rows, then (pause) PlatinumCustomer rows
DURATION = 13.6

html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>Frustrated developer, repeated code in yellow</title>
  </head>
  <body>
    <template id="class-hl-template">
      <style>
        #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
        .hl-team {{ position: absolute; left: {TEAM[0]}px; top: {TEAM[1]}px; width: {TEAM[2]}px; height: {TEAM[3]}px;
          border-radius: 14px; overflow: hidden; }}
        .hl-zoom {{ position: absolute; inset: 0; transform-origin: {FACE[0]}px {FACE[1]}px; }}
        .hl-zoom img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
        .hl-tint {{ position: absolute; inset: 0; background: #ff2a1a; opacity: 0; mix-blend-mode: multiply; }}
        .hl-fx {{ position: absolute; opacity: 0; }}
        .hl-row {{ position: absolute; opacity: 0; background-repeat: no-repeat; }}
      </style>

      <div id="root" data-composition-id="class-hl" data-width="1920" data-height="1080" data-duration="{DURATION}">
        <div class="hl-team" id="hl-team">
          <div class="hl-zoom" id="hl-zoom"><img src="assets/team-last.jpg" alt="The team; the developer on the right is frustrated"></div>
          <div class="hl-tint" id="hl-tint"></div>
          <!-- storm cloud with a lightning bolt over his head -->
          <svg class="hl-fx" id="hl-cloud" style="left:{FACE[0] - 78}px; top:2px" width="156" height="92" viewBox="0 0 156 92">
            <path d="M30 60 C8 60 6 34 26 30 C24 12 50 4 62 18 C70 2 100 4 104 22 C122 14 146 28 136 46 C152 52 146 72 128 70 L34 70 Z"
              fill="#4b5160" stroke="#1d2027" stroke-width="4" stroke-linejoin="round"/>
            <path d="M44 40 q10 -10 20 0 t20 0 t20 0 t20 0" fill="none" stroke="#2a2e37" stroke-width="3" stroke-linecap="round"/>
            <path d="M80 66 L68 84 L80 82 L72 92 L94 74 L82 76 L90 66 Z" fill="#ffd43b" stroke="#7a5200" stroke-width="2" stroke-linejoin="round"/>
          </svg>
          <!-- anger mark -->
          <svg class="hl-fx" id="hl-anger" style="left:{FACE[0] + 52}px; top:{FACE[1] - 92}px" width="54" height="54" viewBox="0 0 54 54">
            <g fill="none" stroke="#e8202a" stroke-width="7" stroke-linecap="round">
              <path d="M6 20 Q20 20 20 6"/><path d="M34 6 Q34 20 48 20"/><path d="M48 34 Q34 34 34 48"/><path d="M20 48 Q20 34 6 34"/>
            </g>
          </svg>
          <!-- sweat drops -->
          <svg class="hl-fx" id="hl-drop1" style="left:{FACE[0] - 66}px; top:{FACE[1] - 60}px" width="22" height="32" viewBox="0 0 22 32">
            <path d="M11 2 C11 2 2 16 2 22 a9 9 0 0 0 18 0 C20 16 11 2 11 2 Z" fill="#8fd8ff" stroke="#1f6f9e" stroke-width="2"/>
            <ellipse cx="8" cy="21" rx="2.5" ry="4" fill="#ffffff"/>
          </svg>
          <svg class="hl-fx" id="hl-drop2" style="left:{FACE[0] + 50}px; top:{FACE[1] - 20}px" width="18" height="26" viewBox="0 0 22 32">
            <path d="M11 2 C11 2 2 16 2 22 a9 9 0 0 0 18 0 C20 16 11 2 11 2 Z" fill="#8fd8ff" stroke="#1f6f9e" stroke-width="2"/>
            <ellipse cx="8" cy="21" rx="2.5" ry="4" fill="#ffffff"/>
          </svg>
        </div>
      </div>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        (function () {{
          var root = document.querySelector('[data-composition-id="class-hl"]');
          var q = function (s) {{ return root.querySelector(s); }};
          var tl = gsap.timeline({{ paused: true }});
          var F_IN = {F_IN}, F_OUT = {F_OUT};

          // ---- 1. Frustrated developer ----
          tl.fromTo("#hl-zoom", {{ scale: 1 }}, {{ scale: 2.1, duration: 0.7, ease: "power2.inOut" }}, F_IN);
          tl.fromTo("#hl-cloud", {{ opacity: 0, y: -30, scale: 0.6 }},
            {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.8)" }}, F_IN + 0.8);
          tl.fromTo("#hl-cloud", {{ x: 0 }}, {{ x: 6, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 9,
            immediateRender: false }}, F_IN + 1.3);
          tl.fromTo("#hl-anger", {{ opacity: 0, scale: 0 }},
            {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }}, F_IN + 1.2);
          tl.fromTo("#hl-anger", {{ scale: 1 }}, {{ scale: 1.25, duration: 0.22, ease: "power1.inOut", yoyo: true, repeat: 7,
            immediateRender: false }}, F_IN + 1.5);
          ["#hl-drop1", "#hl-drop2"].forEach(function (d, i) {{
            var at = F_IN + 1.5 + i * 0.35;
            tl.fromTo(d, {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: 6, duration: 0.25, ease: "power1.out" }}, at);
            tl.to(d, {{ y: 34, duration: 1.4, ease: "power1.in" }}, at + 0.25);
            tl.to(d, {{ opacity: 0, duration: 0.3 }}, at + 1.4);
          }});
          tl.fromTo("#hl-tint", {{ opacity: 0 }}, {{ opacity: 0.22, duration: 0.3, yoyo: true, repeat: 3 }}, F_IN + 1.2);
          tl.fromTo("#hl-team", {{ x: 0 }}, {{ x: 5, duration: 0.05, ease: "none", yoyo: true, repeat: 9 }}, F_IN + 1.25);
          // ... then he calms down: effects go, the camera pulls back out
          tl.to(["#hl-cloud", "#hl-anger"], {{ opacity: 0, duration: 0.35 }}, F_OUT - 0.4);
          tl.to("#hl-zoom", {{ scale: 1, duration: 0.6, ease: "power2.inOut" }}, F_OUT);

          // ---- 2. Repeated code turns yellow ----
          var C = {json.dumps(CUST)}, P = {json.dumps(PLAT)}, TX = {json.dumps(TEXT_X)};
          var SR = {json.dumps(STATE_ROWS)}, BR = {json.dumps(BEH_ROWS)};
          function rowWin(x0, y0, s, img, w, h, r, dy, id) {{
            var d = document.createElement("div"); d.className = "hl-row"; d.id = id;
            d.style.left = x0 + TX[0] * s + "px"; d.style.top = y0 + dy + r[0] * s + "px";
            d.style.width = (TX[1] - TX[0]) * s + "px"; d.style.height = (r[1] - r[0]) * s + "px";
            d.style.backgroundImage = "url(" + img + ")";
            d.style.backgroundSize = w * s + "px " + h * s + "px";
            d.style.backgroundPosition = (-TX[0] * s) + "px " + (-r[0] * s) + "px";
            root.appendChild(d); return d;
          }}
          function card(geo, img, w, h, behDy, at, pfx) {{
            var rows = [];
            SR.forEach(function (r, i) {{ rows.push(rowWin(geo[0], geo[1], geo[2], img, w, h, r, 0, pfx + "s" + i)); }});
            BR.forEach(function (r, i) {{ rows.push(rowWin(geo[0], geo[1], geo[2], img, w, h, r, behDy, pfx + "b" + i)); }});
            rows.forEach(function (d, i) {{
              tl.fromTo(d, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power1.inOut" }}, at + i * {ROW_GAP});
            }});
          }}
          card(C, "assets/cd-cust-y.png", 496, 600, 0, {H_CUST}, "hl-c");
          card(P, "assets/cd-plat-y.png", 646, 600, P[3], {H_PLAT}, "hl-p");

          window.__timelines["class-hl"] = tl;
        }})();
      </script>
    </template>
  </body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(html)
print("duration", DURATION)
