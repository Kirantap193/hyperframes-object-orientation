# Code + memory video style (approved on video-5-part2, 26 Sep 2026)

This is the template for every code + Stack / Private Heap lesson video. Every value below was a
correction the user made on video-5-part2. Copy this file into each new project. The working
code for every piece lives in `video-5-part2/compositions/`: `citizen-code.html`,
`citizen-memory*.html` and `citizen-output*.html`.

## Frame

- 1920x1080, 30fps, no audio. Background flat `#010101`, with no texture image and no push-in.

## Code window (`compositions/code-window.html`)

- The Main.py vector window: dashed white border (5.5px, dash 5/19.5, 17px outside), body
  `#101b2c`, 60px title bar `#1b2536` with the `code-titlebar.webp` art, inner panel `#26344b`.
- Code: JetBrains Mono **400**, 36px on a 46px grid (21.6px a column), 20px / 16px inner padding,
  ligatures off. Blank lines are half height (23px).
- Colours: plain `#c8d3f5` · `def` / `class` / `if` `#c099ff` · `print`, class names, `self`,
  `main`, methods `#8fb3ff` · strings `#e0c78b` *italic* · numbers `#f5a97f` · comments `#8c8c8c`.
- Typing: per character, 0.075s, no caret, indentation not typed, 0.25s a line.
  **Assignments type value first:** `10`, then `=`, then `a`.
- Editor edits: select in `rgba(38, 110, 214, 0.85)`, fade the text, and the rest closes up.
  Folded bodies show a band `rgba(255, 255, 255, 0.13)` behind the `def` line. The window
  reshapes to hug the code.
- When the memory is on screen, the code window scales to 0.5556 at x 42, centred vertically.

## Output window

- Vector output window on the right while the memory is away: body `#0c1620`, the
  `output-titlebar.webp` art, JetBrains Mono 500 in white. 36px, or 26-28px for long dict lines.
  A printed line is never split, except a whole `__dict__`, which wraps one entry per line.
- The window pops up, prints at 0.03s a character, then fades out. The memory fades out before it
  and back in after it.

## Stack / Private Heap

- Panels: `mem-stack2.png` (left 998, 450 wide) and `mem-heap2.png` (left 1488, 400 wide), both
  181.6 - 964.3 tall, drawn as a nine-slice `120 fill / 50px`. Labels **Stack** and **Private Heap**
  go **under** the panels (top 978), white, Nunito 700, 38px.
- Frames: SVG rounded rect, `stroke #c8d6ff`, `stroke-opacity 0.45`, width 2.5, dash `7 6`, fill
  `rgba(255, 255, 255, 0.03)`, radius 20, 360 wide at left 1043. `main()` at the bottom, `__new__`
  above it, `__init__` on top. Each frame drops in with `push` (y -360 to 0, back.out(1.4)).
- Frame names sit outside the Stack, right-aligned to 960, in JetBrains Mono 400, 19px, `#8d96ab`.
- Stack text: JetBrains Mono 500, no text shadow. Labels white 24px, with `self` and `*args` pink
  `#ffb0c2`. Values sit in boxes (`#0b1836`, 1.5px `#3b5ea8` border, radius 8) at 22px, or 18px
  for `__init__` fields. Tuple cells use the same boxes at 16px, with index numbers `#c9d2e8` 15px.
- Heap objects are **cards**: 320 wide at left 1528, radius 14, border 1.5px
  `rgba(90, 230, 200, 0.45)`. The teal header runs `#127a68` to `#0c5c50` (40px, or 34px in tight
  layouts) and holds the address in white 26px plus a class tag pill (`::after`, 15px code font).
  The body is `#0e1a28`, with lines `name = 'Rohit'`: key `#9fb4cc`, then `=` and the value in
  white, 19-20px. There are **no Key/Value tables and no "dict" label**. Class variables go in a
  plain dark card (no header) with the title above it.
- Highlight: a red dashed box (`#ff3d5e`, 3px dashed, glow) around a heap line.
- Arrows: solid cyan `#4fd1ff`, width 4, glow `drop-shadow(0 0 6px rgba(79, 209, 255, 0.65))`, a
  cubic curve from the Stack value to the card header, drawn on with a mask reveal (1.0s), with
  the head appearing at the end.
- **No bold** in diagram text (normal weight), and text as large as the space allows with
  little padding.

## Flow

1. The code window pops up, and the code types in (or appears whole, if the user says so).
2. The Stack and Private Heap pop up and their labels type in.
3. `main()` is pushed. For each object: `__new__(cls, *args, **kwargs)` is pushed, `cls` and the
   tuple fill in, the empty card pops in the heap, `__init__` is pushed, `self` gets the address
   (the address **flies from the heap card to the Stack**) and the arrow draws. The parameters
   fill in, then each card line types its key and `=`, and its **value flies from the Stack box
   into the card** (never typed). `__init__` fades, the variable in `main()` gets the address (it
   flies from the heap) with its arrow, and `__new__` fades.
4. For output, the memory fades out, the output window prints, then the memory fades back in
   with all objects.
5. Approved parts are never touched. Prove it by hash-comparing snapshots before and after.

## Delivery

- Render only on request: render in full, trim the first second if asked
  (`ffmpeg -ss 1 -c:v libx264 -crf 16`), verify with ffprobe, then copy to
  `OneDrive\Desktop\kiran` and hash-check it. New versions get `-v2`, `-v3` and so on.
- The split-render PPT uses the bundle's pipeline, then:
  - Merge cuts inside motion and cuts on holds shorter than 6 frames.
  - Split each code edit (a removal or a selection) into its own click.
  - Cut before every heap key, so each card line is its own click.
  - Build it in WPS, run `fix_triggers.py` and `shrink_posters.py`, then open the deck in WPS.
