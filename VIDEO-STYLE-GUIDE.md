# Video Style Guide — TAP Academy "premium PPT remake" lessons

**Context name:** `tap-premium-ppt-video`
**Reference build:** this repository (`video-11`, *Object Orientation — design principles*, 2 m 30 s)
**Last updated:** 2026-10-05

This file is the whole spec for how these videos are made. Give it to a new chat, attach a
screenshot of the sir's lecture slide, and the next part can be built in exactly the same style.
Everything below has already been approved — do not redesign it, do not ask to re-choose colours,
fonts or layouts. Only ask about the teaching content if it is genuinely unclear.

---

## 0. How to continue on another laptop

```bash
git clone https://github.com/Kirantap193/hyperframes-object-orientation.git
cd hyperframes-object-orientation
npx hyperframes preview --background --no-open --port 3011
```

Open **http://127.0.0.1:3011/#project/video-11** (use `127.0.0.1`, not `localhost`).

### Prompt to paste into a new Claude chat

```text
Read VIDEO-STYLE-GUIDE.md in C:\<path>\hyperframes-object-orientation - that is my approved
video style (context name: tap-premium-ppt-video). Follow it exactly. Do not redesign anything.

Start the Studio preview and give me the link. Then wait.
From now on I will only attach screenshots of my sir's lecture (and sometimes my own artwork).
Take them one by one, continue the video from its current end, and after each part run
npm run check, look at snapshots yourself, and send me the Studio link with timestamps.
Don't render until I tell you to.
```

---

## 1. What these videos are

- **Who:** a Python trainer at TAP Academy. Students watch on a classroom monitor.
- **What:** the sir's existing lecture (a PPT-style video with a presenter) is **re-made as a
  premium animated video** — same content, same slide layout, same teaching order, but with rich
  3-D artwork, cards and motion. The presenter is **not** included.
- **Input each turn:** one or more screenshots of the sir's lecture (with a timestamp), and often
  the user's own artwork (PNG/WebP with a transparent background) or a source video clip.
- **Tool:** HyperFrames (HTML + GSAP), CLI pinned in `package.json` (`hyperframes@0.8.58`).
- **Frame:** 1920 × 1080, 30 fps. Sound only when a supplied clip has it.

## 2. The golden rules (the user's own corrections — never break these)

1. **Follow the screenshot.** Reproduce the sir's slide layout and content exactly (positions,
   which object sits where, every label, every line of a card), then make it look premium.
2. **Use the user's artwork as-is.** Cut pieces out of the supplied images; never re-draw or
   re-typeset what the artwork already contains. If two images are "before / after" (e.g. empty
   pillars vs. pillars with words), reveal the difference from the second image.
3. **3-D and aesthetic, NO glow.** Depth comes from stacked text-shadows (a hard edge in 3–6
   layered offsets) and drop shadows below — never `0 0 Npx` glow halos or neon.
4. **Type-on text.** New text appears one character at a time (no caret).
5. **Pause before every step.** Each new animation waits ~0.8–1.0 s after the previous one has
   finished. One thing happens at a time (one rod, then one label, then the next…).
6. **Show the movement.** When something changes place, it glides from where it currently is to
   where it goes — never cut or re-appear somewhere else. Build each new part on top of the
   previous slide's last frame (the hand-over must be pixel-identical).
7. **Not bold** for labels and annotation text (Has-A / Aggregation / Composition…). Headings
   and card titles may be bold.
8. **Readable.** Every text must pass contrast ≥ 3 : 1 (`npm run check` tests it). If a brand
   colour fails, darken the background or lighten the text a shade — keep the hue.
9. **Fill the frame**, nothing cut off at the edges, nothing overlapping.
10. **Don't render until asked.** Render → `renders/` → copy to
    `C:\Users\kiran\OneDrive\Desktop\kiran\` → SHA-256 both copies → report the path.

## 3. Design style

### 3.1 Stage
Flat black background (`#000000` / `#010101`). Slides fade to black between major scenes
(0.6–0.8 s), or — preferably — the previous slide **transforms** into the next (shrinks, slides up,
cards glide to new positions).

### 3.2 Colours

| Use | Colour |
|---|---|
| Heading card (ANALYSIS PHASE / DESIGN PHASE) | Burnt Orange `#FC6C26` top → `#D04C16` bottom, white text |
| Card / label lettering on black ("Has-A", "Aggregation") | cream `#FBE7A1` with gold edge stack `#E0C779 → #866D28` |
| Connector rods and diamonds | cyan tube gradient `#D4F6FF → #5FD3F5 → #1E95C2 → #0D5F80` |
| "Repeated code" highlight | yellow `rgb(255,226,96)` |
| "New members" highlight | pink `#FF7AD9` |
| Card body text (from the artwork) | names `#EBEEF4`, types teal `#3DE2C1` |
| UML / rainbow flash letters | settle on pink `#E47DE8` |
| Platinum card | the Customer card recoloured: silver frame, graphite panels |

### 3.3 Typography
- Headings / labels: **Poppins** (700 for card titles, 400 for annotation labels).
- Card body text: **Segoe UI** (matches the card artwork).
- Big serif titles: come from the user's artwork (e.g. the Has-A plaque) — revealed, not re-typed.
- UML phrase: Inter 500.

### 3.4 Recurring elements
- **Heading card:** rounded card that hugs its text (no inner padding), 80 px Poppins 400 white,
  10 px stacked 3-D edge, swings down from the top (hinged, `rotationX -95 → 0`, back.out),
  a faint glint crosses it, then a slight 3-D rock. Centred at the top of the slide.
- **Class cards:** the user's coloured cards (Customer blue, Restaurant orange, DeliveryAgent
  green, FoodItem purple with `‹ Enumeration ›` inside the card, PlatinumCustomer platinum).
  Build-up: empty card pops → body splits in two (divider opens from the middle) → State fades
  in → Behaviour fades in, with a pause before each.
- **Objects:** character art + name pill; the delivery agent always **rides in from the right**
  like a scooter (fast, eases to a stop, small bounce, speed streaks).
- **Relations (Has-A):** 3-D cyan rod runs out of the source card; a diamond spins in at the
  Restaurant end — hollow = aggregation, filled = composition. The rod runs *square* into the
  diamond's point (sharp joint, no gap, no rounded end there).
- **Video clips:** inside a bevelled grey frame with a drop shadow, or full frame between slides.
  Trim exactly to the requested seconds (move the cut to the nearest shot change if the requested
  edge shows the wrong shot — and say so). Slow-motion with `data-playback-rate`.
- **Highlights:** recolour the existing text in place (yellow = repeated, pink = new) row by row.

## 4. Motion rules

| Thing | Motion |
|---|---|
| Type-on | `CHAR = 0.06 s` per character (0.1 s for big title letters), no caret |
| Pop-in | opacity 0→1 (0.25 s) + scale 0.85→1 `back.out(1.5)` |
| Pause between steps | 0.8–1.0 s after the previous step ends |
| Moves | `power2.inOut`, 0.6–1.4 s, from the current position |
| Fade between scenes | 0.6–0.8 s `power1.inOut` |
| "Stretch and flash rainbow" | letters enter `scaleX 0.4 / scaleY 2.4 → 1` (elastic) while cycling red → orange → yellow → green → cyan → violet → pink |
| Frustration | punch-in on the face, storm cloud + lightning, red anger mark, sweat drops, short shake |

## 5. Workflow per part

1. Read the screenshot(s); say in one line what the part will do (and any assumption).
2. Cut the needed pieces from the artwork (`tools/build/*_extract.py` patterns: transparent
   crops, painted-out "empty" versions, per-letter / per-line windows, recolours).
3. Add the beats to the right scene file (or a new scene file — see §7), keep timing constants
   at the top so later beats shift together.
4. Update `data-duration` in the scene and in `index.html`; later scenes' `data-start` move too.
5. `npm run check` → 0 errors.
6. Snapshot the new beats (`npx hyperframes snapshot --at … --no-end --describe false -o <dir>`),
   **look at them**, fix anything off, delete the snapshot folder.
7. Reply with the Studio link, a timestamp table of the new beats, and any choice the user
   should confirm.

## 6. Environment notes (Windows, kiran's machines)

- **Headless Chrome blocked:** Windows Application Control blocks HyperFrames' own
  `chrome-headless-shell.exe` (`spawn UNKNOWN`). Always run check / snapshot / render with
  ```bash
  export HYPERFRAMES_BROWSER_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
  ```
- **Python:** `C:\Users\kiran\AppData\Local\Programs\Python\Python312\python.exe` (bare `python`
  is the Store stub). Pillow + numpy + scipy are used by the build scripts.
- **Studio:** `npx hyperframes preview --background --no-open --port 3011`; confirm with
  `--status`. If the page says "preview did not reload (it took too long)", close extra Studio
  tabs, wait for the network to be stable, press F5. Keep heavy assets small (re-encode clips with
  `-crf 19 -g 30 -movflags +faststart`, logos as WebP).
- **Studio rewrites files** (adds `data-hf-id`) — anchor edits on attribute fragments, never on a
  tag start.
- Render of 2 m 30 s takes ~10 min on the RTX 3060.

## 7. Technical rules (HyperFrames)

- One paused GSAP timeline per composition, registered on `window.__timelines["<id>"]`.
- Seek-safe: `fromTo` with `immediateRender: false` for later tweens on the same target; hidden
  initial states go in CSS, not `tl.set` at 0.
- Animate transforms / opacity / colour only — **no `fontSize`, `letterSpacing`, width/height
  tweens** (lint `gsap_non_transform_motion`). Grow things with `scale`, open bands with `scaleY`.
- Don't put a CSS `transform` on an element GSAP also moves (`gsap_css_transform_conflict`) —
  let the timeline own its scale.
- Media inside a scene uses **scene-local** `data-start`. Each `<audio>` needs its own
  `data-track-index`. A slowed clip's "media shorter than slot" warning is a false alarm.
- A scene file over **300 lines** → put the next beats in a **new scene file** drawn on top
  (like `class-hl.html` over `class-layout.html`) using the same frame coordinates.
- Unique ids / class prefixes per scene file (`ot-`, `fo-`, `al-`, `ob-`, `cc-`, `cl-`, `hl-`).
- Only deterministic code — no `Math.random()`, `Date.now()` or fetches.

## 8. This video's scene map

| Time | Scene file | Content |
|---|---|---|
| 0:00 | `oops-temple.html` | OOPS temple fades in, pillar words type on bottom-up |
| 0:11 | `food-order.html` | Ordering food (0.8×, last 4 s 0.64×) |
| 0:24 | `delivery.html` | Agent collects the order and delivers it |
| 0:32 | `app-logo.html` | Logo + man thinking (bubbles) → ANALYSIS PHASE → DESIGN PHASE |
| 0:47 | `objects.html` | 4 objects → Unified Modeling Language → UML → State/Behaviour → shrinks to top |
| 1:05 | `class-cards.html` | Class cards build up under the objects |
| 1:26 | `class-layout.html` | Corner layout → Has-A rods/labels → title plaques → team clip → PlatinumCustomer grows |
| 2:17 | `class-hl.html` | Frustrated developer; repeated code yellow, new members pink |

`objects.html`, `class-cards.html`, `class-layout.html`, `class-hl.html` are **generated** by the
scripts in `tools/build/` — edit the script and re-run it (fix the absolute paths at the top first
when on another machine). `STYLE.md` in this folder is the old code+memory template spec and is
**not** used by this video.
