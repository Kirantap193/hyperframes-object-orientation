# Object Orientation — design principles (HyperFrames lesson)

A TAP Academy Python lesson video built with [HyperFrames](https://hyperframes.heygen.com):
HTML compositions animated with GSAP, rendered to MP4. 1920 × 1080, 30 fps, 2 m 30 s.

## Run it

```bash
npx hyperframes preview --background --no-open --port 3011
```

Open **http://127.0.0.1:3011/#project/video-11**. The CLI version is pinned in `package.json`.

```bash
npm run check     # lint + runtime + layout + motion + contrast
npm run render    # MP4 into renders/
```

On a machine where Windows blocks HyperFrames' own headless Chrome, point it at an installed
Chrome first:

```bash
export HYPERFRAMES_BROWSER_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## What plays when

| Time | Scene | File |
|---|---|---|
| 0:00 – 0:11 | OOPS temple; the four pillars type on | `compositions/oops-temple.html` |
| 0:11 – 0:24 | Ordering food on the phone (0.8×, last part 0.64×) | `compositions/food-order.html` |
| 0:24 – 0:32 | The delivery agent collects and delivers the order | `compositions/delivery.html` |
| 0:32 – 0:47 | Food Delivery App idea, ANALYSIS PHASE, DESIGN PHASE | `compositions/app-logo.html` |
| 0:47 – 1:05 | The four objects, Unified Modeling Language → UML, State / Behaviour | `compositions/objects.html` |
| 1:05 – 1:26 | Class cards build up under the objects | `compositions/class-cards.html` |
| 1:26 – 2:17 | Layout moves, Has-A (aggregation / composition), the team, PlatinumCustomer | `compositions/class-layout.html` |
| 2:17 – 2:30 | Frustrated developer; repeated code in yellow, new members in pink | `compositions/class-hl.html` |

## Generated scene files

`objects.html`, `class-cards.html`, `class-layout.html` and `class-hl.html` are written by the
Python scripts in `tools/build/` (the `*_build.py` files), from positions measured out of the
artwork by the `*_extract.py` scripts (results in the `*.json` files). Edit the script and re-run
it rather than editing the generated HTML by hand. The scripts carry absolute Windows paths from
the machine they were written on — adjust `SCR`, `OUT` and the asset paths before running them
elsewhere.
