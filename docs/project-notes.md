# How Indonesia Uses ChatGPT Differently

A scrollytelling data story about how Indonesians use ChatGPT, built as a portfolio piece by Akbar Saputra. It is one self-contained HTML page: prose, ten D3 charts, and data all inline.

The story's claim: between mid-2024 and mid-2026 the world's share of work-related ChatGPT messages fell from 48.9% to 30.7%, while Indonesia's held near 40%. What kept it up is writing, done by a young user base that is mostly women by first-name inference, and whose "work" looks a lot like campus work.

## Commands

```bash
pip install -r requirements.txt         # pandas, numpy, pycountry, playwright
python scripts/build_data.py            # CSVs -> data/story_data.json (prints headline figures)
python scripts/assemble.py              # src/template.html + vendor + data -> dist/index.html
start dist/index.html                   # Windows (macOS: open). Plain file, no server needed

# visual checks: point CHROME at an installed Chrome, or run `playwright install chromium` once
export CHROME="C:/Program Files/Google/Chrome/Application/chrome.exe"
python scripts/shot.py 1440 900 d top drift:0 drift:3 '[data-fig="iwa"]'
python scripts/shot.py 390 844 m hundred:2 '[data-fig="percap"]'
```

The author works on Windows 11. `python` is Anaconda's Python 3.12, and there is no `python3` on the PATH. In PowerShell, set the browser with `$env:CHROME = "C:\Program Files\Google\Chrome\Application\chrome.exe"`.

The scripts read and write UTF-8 with LF endings explicitly, and `.gitattributes` pins LF in the repo, so the outputs are byte-identical on Windows, macOS, and Linux. Running `build_data.py` on unchanged data should leave `git status` clean. If it doesn't, something in the data logic or the library versions changed. The log's last line prints the output path relative to the repo, so it is the same on every machine. Regenerate the log with `python scripts/build_data.py | tr -d '\r' > docs/data_build_log.txt`.

Edit `src/template.html`, never `dist/index.html`. Run `assemble.py` after every template change. Run `build_data.py` only when the data logic changes.

## Layout

```
src/template.html        the whole page: CSS, prose, chart code. Has two placeholders:
                         /*__D3__*/  /*__DATA__*/
data/raw/public_release_csv/   OpenAI Signals v3.0: 24 CSVs + README.pdf (CC BY 4.0)
data/story_data.json     pre-aggregated data the page reads (about 43 KB)
scripts/build_data.py    builds story_data.json
scripts/assemble.py      inlines everything into dist/index.html
scripts/shot.py          screenshots sections at any viewport
vendor/                  d3.min.js (v7)
dist/index.html          the built page (about 420 KB)
docs/findings.md         the findings and the numbers behind each section
docs/data_build_log.txt  output of the last build_data.py run
```

## How the page is put together

Twelve sections in `<main>`, in this order. Section ids are what `shot.py` targets.

| id | Heading | Layout | Figure id(s) |
| --- | --- | --- | --- |
| (header) | title screen | fills the window: title, subtitle in a composer pill, credit, and a "Keep scrolling" cue at the bottom | |
| `opening` | lede | column, chart after the second paragraph | `hero` |
| `hundred` | Imagine these 100 boxes are 100 messages sent from Indonesia to ChatGPT | pinned chart right, panels split 50:50, 6 text blocks: the first (with the heading) starts low beside the chart, and the last carries its own heading, "Let's dissect these numbers" | `grid` |
| `crowd` | Where does Indonesia rank in the use of ChatGPT? | two equal panels, not pinned: ranking line on the left, heading and text in half of the right panel | `percap` |
| `drift` | Is work fading from ChatGPT in Indonesia too? | pinned chart right, 4 text blocks, one per chart state, the first starting low beside the chart | `work` |
| `desk` | What do Indonesians use ChatGPT for? | prose in column, small multiples full width | `topics` |
| `tell` | Do Indonesians ask ChatGPT, or tell it what to do? | chart left, heading and text right, not pinned | `ade` |
| `campus` | What kind of work do Indonesians bring to ChatGPT? | prose in column, chart full width | `iwa` |
| `young` | How old are Indonesia's ChatGPT users? | pinned chart right, 3 steps, the first starting low beside the chart, the last a table of bars by age group and country | `age` |
| `women` | Are Indonesia's ChatGPT users mostly women? | pinned chart left (`.flip`), 2 steps, the first starting low beside the chart | `gender` |
| `pictures` | What is changing in how Indonesians use ChatGPT? | prose in column, three panels full width | `pics` |
| `closing` | So how does Indonesia use ChatGPT differently? | column: a conclusion that recaps the findings with the data's limits woven in, then method and sources | |

"Column" is the centered reading column (`--col`, 45rem, about half of a 1440px screen). All prose sits in it. So does the `hero` figure (`class="inset"`), which gains nothing from more width. Left-right panels (sections with `class="split"`) and the three `class="wide"` figures (`topics`, `iwa`, `pics`) use the full page width, set in from the window edge by `--pad` plus `--edge`. Below 860px everything is one column.

Chart code lives in the last `<script>`:

- `reg(id, build)` registers a figure. `build(el)` draws into `.plot` and may return `{ set(state, animate) }`.
- Pinned sections are `.scrolly[data-for="<figure id>"]` holding `.sticky` (the figure) and `.steps > .step[data-step="n"]`. An IntersectionObserver calls `setState(id, n)` when a step crosses the middle of the viewport.
- Charts size themselves from `el.clientWidth` and redraw on resize. Each has a small-screen branch (`sm`). Below 860px the pinned figure sticks to the top and steps scroll under it.
- Helpers: `txt()` (text, `note: true` for an annotation, `halo: true` for a page-colored outline), `lab2()` (the label form used everywhere: name in bold, value in brackets at regular weight), `fit()` (keeps a label inside the chart), `hover()` (lights up the point nearest the pointer), `arrow()`, `ring()` (circle around a point), `wrap()` (line breaks to fit a width), `brk()` (axis-break mark), `axisLine()` (y-axis line and baseline, with the break mark when the axis is cut), `dodge()` (label collision), `lineSeries()`, `endLabels()`.
- `grid` has six states: one large grid of 100 gray boxes (state 0, shown beside the heading and the opening paragraph), a row of boxes per topic (1), three small grids side by side for Indonesia, Southeast Asia, and the world (2 to 4: work, feminine names, under 25), and last Indonesia three times over, one grid per count, each under its own number and short caption (5). In states 2 to 4 Indonesia's grid stands apart, with a wide gap before the other two, and only it carries the large caption, which wraps to stay over its own column. The others carry a one-line label such as "Southeast Asia (33)". It has no title and no `<figcaption>`: the small caption is drawn inside the chart, directly under the boxes in every state. The heading used to be drawn above the state 0 grid and now sits in the text beside it.
- Paced sections (`class="paced"`: `hundred`, `drift`, `young`, and `women`, which is every pinned section) share one scroll mechanism. Each opens with a `.step.low` block (see below) instead of an empty lead-in step. Each later step is a full screen tall, so one paragraph leaves before the next arrives. Step text sits in `.say` blocks, and a scroll handler changes the chart when the top of a block has risen 25% of the window height from the bottom (the author moved this from 50% to 40% to 25%). On desktop the pinned area fills the window and the chart is centered in it. There is no space after the last step, so the chart never outlasts the text: on desktop the last block rises until its top is level with the top of the chart (`--ft` and `--lp`, also set by `lowStep()`), and then the two leave the screen together. The author asked for this after an earlier version let the last paragraph leave first. On phones the chart sticks to the top and a little space still follows the last step. The IntersectionObserver path remains in the code for any pinned section without `.say` blocks, but no section uses it now.
- `hundred` differs in two ways. Its panels split 50:50. And its last block leaves with the chart while still centered in the window, not level with the chart's top. That block is the connecting one: a heading ("Let's dissect these numbers") and one paragraph that restates the three counts and lays out the rest of the story, beside the three Indonesia grids. The author first had this block in the centered column under the pinned chart, then moved it into the scroll. The caution that traits cannot be cross-tabulated sits in the block before it.
- `percap` is one vertical line with rank 1 at the top, and position along it is proportional to rank, so distances can be compared (the author asked for this after an evenly spaced list hid them). The dataset publishes only the per-person rank, never a count, so it is a scale of rank and not of usage. Every country gets a faint tick. Labels sit left of the line for the first and last country, Indonesia, its ten neighbors, and the United States and India. They move apart where they would collide. Two small arrows between the line and the text say which way is more. The line is 5px a rank, long enough that the dots of neighboring ranks do not touch. On desktop the heading and text stay together as one block, and the chart code centers that block vertically on the line. The section is not pinned.
- `drift` has one text block per chart state, because the author found the earlier text out of step with the chart. State 0 is the world line over every country (the low first block, with the heading). State 1 adds the Southeast Asia average, and its text describes how unevenly the nine neighbors fell. State 2 adds Indonesia's line together with the note "Indonesia stops following here". State 3 turns the chart into the change view: every country as a dot, placed by how many points of work share it lost between its first six months and its last six. That view used to be a separate figure (`change`) in the column below. The `work` chart shows the regional average only. The author tried thin lines for the nine neighbors and reverted it, and removed a "9 points above the world" note, so the text does not lean on that gap either.
- Every section starts with the same gap (about a quarter of the window), except `opening` and `hundred`, which sit closer to what comes before. A section that follows a pinned one has a smaller gap of its own, because the pinned area ends with empty space under its chart: `crowd` makes up only the difference to 1.4 times the standard gap (through `--tail`; the author found the old gap too large and the standard one too small), and `desk`, `women`, and `pictures` have reduced padding.
- Every numeric y-axis has an axis line and a baseline (`axisLine()`), at the author's request: `hero`, `work`, `topics`, `ade`, `age`, `gender`, and `pics`. Cut axes also carry a break mark. `hero`, `work`, `ade`, `age`, and `gender` do not start at zero (the author tried zero for `hero` and `ade` and reverted it), so each cut axis is labeled 0 at its origin and shows a break mark (`brk()`) before the first value. `ade` axes also end in arrows.
- Hovering works the same way in `ade` and in the change view of `work`, through `hover()`: one listener on the whole chart finds the nearest dot, lights it up, and names the country with its values. Per-dot listeners were dropped because a fast exit could leave a dot lit. In `ade` every dot responds, including the world, the region, Indonesia, and Japan, and a dot that already carries a name hides it while the fuller label shows.
- `iwa` is a strip per activity on a log scale of "times the median country", ruled like a table with no gaps between rows, and sorted from Indonesia's highest multiple to its lowest. Every country is a small mark: gray for the other 83, blue for the Southeast Asia average, and red for Indonesia, which carries its multiple as a label (such as "4.9x"). The chart uses multiples only, written with a plain "x", with no percentages, rank lines, or direction arrows, at the author's request. One note above the chart spells out the first row in words, with a little room between it and the caption. Moving the pointer along a strip lights up the nearest country, names it, and lights the same country in the other strips. The author tried two simpler versions (plain percentage bars, then lines from the median for Indonesia and the region only) and came back to this one because it shows the other countries. A second note under the table restates a multiple below 1 as "less" for the goods-and-services row: 0.6x reads "0.4 times less than the median country". That is the author's wording, chosen after "0.6 times as much" and a version in whole messages ("for every 10, Indonesia spends 6"). Axis ticks are decimals (0.25x, 0.5x), not fractions, to match the labels.
- `age` has three views. All three under-25 lines. Then a close-up for the September step: the y-axis tightens to 36 to 70%, the world and Southeast Asia lines fade out, Indonesia's quarterly line turns thin and dashed, and its monthly points appear with each August-to-September segment drawn heavy. Then a table of bars: one row per country, one column per age group, bar length the share of that country's messages, with the value printed beside each bar. Bars in a column share a baseline, so an age group can be compared down its column and a country's profile read across its row. Indonesia, the region, and the world sit among eight large countries (India, Nigeria, Mexico, Brazil, Japan, Germany, the United States, South Korea; the list is `PICK` in `build_data.py`), ordered by the share from ages 18 to 24. A phone drops two rows and shows four age groups, with everyone aged 45 and over as one column (the author asked for this; the sums are `mix45` and `o` in the data, added before rounding). The author rejected, in turn, stacked bars, a dot plot of Indonesia, the region, and the world, and a ridgeline, and ruled out a dumbbell chart and grouped bars. The y-axis of the line views is cut above zero and carries the break mark.
- `pics` is three panels side by side on one scale, at page width: Indonesia, the Southeast Asia average, and the median country, which stands in for the world because work activities have no world series. Each panel holds only two lines, visual design in the panel's own color and programming in light ink, both labeled at their last point. In every panel a dashed vertical line marks where design passes programming, and a label under the axis names the two quarters it falls between (the data is quarterly, so the crossing is only known to that interval). One note in Indonesia's panel, "Creating pictures now passes coding", points at it. The author asked for this after a single chart mixed Indonesia's two lines with the region's. Below 760px the panels stack.
- `closing` has no chart. It recaps the findings in paragraphs and states each limit of the data where it applies. A dot chart of topics in 2024 and 2026 (`thennow`) and a separate list headed "What this data cannot say" were both removed at the author's request.
- In `hundred`, `drift`, `young`, and `women` the heading opens the first block of step text, and the paragraph after it answers or sets up the heading directly ("Young, for the most part."). The author tried the heading above the pinned chart and moved it here. These sections have no empty lead-in step: the first block is a `.step.low`, which ends level with the bottom of the plot (the chart code sets `--fb` through `lowStep()`), so the heading is on screen beside the chart from the start instead of arriving from below. In `hundred` it ends level with the small caption under the first grid, since that chart does not fill its box. `lowStep()` also sets `--lg`, the space under that block, to what a block centered in a full-screen step would leave, so the gap to the second block matches the gap between later blocks.
- Phone layout (below 860px), as the author set it in November 2026. A pinned chart hangs at the top of the screen with padding above and below it and no rule under it. In `crowd` and `tell` the chart sits between paragraphs, after the second in `crowd` and after the first in `tell`: the text wrappers get `display:contents` and `order` places the figure. Sections start closer together (about an eighth of the window), and the last block of a pinned section is followed by only a little space, so the next heading can come into view while the old chart is still pinned. The `grid` caption moves left in the topic view so it stays on screen.
- Text inside the charts is laid out with measured widths, but margins for line-end labels are fixed. Phones use fonts a little wider than Segoe UI, so `endLabels()` shrinks a label that would pass the right edge, and the `grid` caption and the `iwa` row names and second note are kept inside the chart the same way.
- Data is the global `D`. Its shape is whatever `build_data.py` writes.

## Design system

The look follows the ChatGPT app in dark mode: a black page, one centered column like a chat thread, and the system font. The author chose it in November 2026 to replace the first design, a sheet of ruled exam paper with serif type and handwritten notes. Do not bring back the paper background, the red margin line, Alegreya, or any handwriting font.

- The title screen is the app's home screen and fills the window: the title sits where the greeting would, and the subtitle sits inside a composer pill whose round button scrolls to the story. The credit links to akbarsaputra.com. A quiet "Keep scrolling" cue sits at the bottom in a soft gray (`#757575`). It fades out once the reader scrolls and fades back in at the top of the page. No chart on this screen. It borrows the layout only. Do not add the OpenAI logo or wordmark as page decoration.
- Page `#000000`, pill `#1b1b1b`, text `#ededed`, headings `#ffffff`, secondary text and captions `#afafaf`, grid lines `#262626`. These were sampled from the author's own ChatGPT screenshot. The page is dark only.
- Three colors carry all the data, the same in every chart: red `#f0554a` is Indonesia, blue `#3f8cf0` is the Southeast Asia average, gray `#939393` is the world. Other countries are dark gray `#4a4a4a`. The three were checked for colorblind separation and for 3:1 contrast on black, so re-check if any of them changes. Light ink appears as a data color only for the programming line in each `pics` panel, where two series of the same place share a chart, and a softer `#b9b9b9` marks the non-writing dots in `grid`.
- Type: the system font stack that ChatGPT uses (Segoe UI on Windows, San Francisco on Apple devices). No fonts are embedded. Headings are medium or semibold, never heavy.
- Annotations are short semibold notes in the color of the thing they point at, one or two per chart, with a thin curved arrow.
- Every chart opens with a small title and an info line, both in the `<figcaption>` above the plot. The title (`.ct`) says what is plotted, such as "Rank by messages per capita", in medium weight at body size, well below a heading. The info line (`.ci`) carries the rest in caption type: period, country count, how to read the marks. The author asked for this in November 2026, after having removed an earlier set of titles (`.ft`) that stated findings and were confusing. So a title names the measure and never states the finding, which stays in the prose. Figures with more than one view (`work`, `age`, `gender`) hold one title and info pair per view, and the chart code switches them through `data-view`. In `percap` the caption sits at the top of the panel, a short gap left of the first labels. The chart code places it, after the author found the far left corner too distant from the chart. Pinned charts on phones show the title only. `grid` has no title. Series are labeled directly at the line end. No legends, except the small key in `topics`.
- Labels that pair a name with a number read "Name (number)", with the name in bold and the bracketed number at regular weight, in every chart (`lab2()`).
- Titles and info lines do not repeat the source. Every chart uses OpenAI Signals, which the lede, Method, and Sources already say.
- Motion only where the reader caused it: scroll steps, the pill's button, and the `hero` lines, which draw once when that chart first scrolls into view. The one exception, which the author asked for, is the subtitle in the composer pill: every few seconds it is edited into another line from the `SUBTITLES` list, the way a person edits a sentence (the cursor moves between words, words are selected or backspaced, new ones are typed, with an occasional corrected typo), and it pauses when off screen. A word-level diff picks what changes. Nothing else loops or bobs. `prefers-reduced-motion` turns transitions into cuts and leaves the subtitle static.
- Every section ends the way a reply does in the ChatGPT app: a row of four small icons (copy, read aloud, share, more) under its last paragraph or figure, then a soft horizontal rule (`.acts`). The author asked for this in November 2026. The icons are decoration only: inline SVG symbols defined once at the top of `<body>`, `aria-hidden`, not buttons. In `young` and `women` the row sits under the last step's text, and in `closing` it comes before the method and sources, which sit lower and in smaller type (0.875rem).
- Keep it plain. No cards, drop shadows, gradient washes, all-caps eyebrow labels, monospace data labels, or fade-up entrances. The composer pill is the only rounded surface.

## Editorial decisions already made

1. English, for a portfolio.
2. Title "How Indonesia Uses ChatGPT Differently," subtitle "A data story of how Indonesians work more (and chat less) with ChatGPT." The author changed both in November 2026. The first title was "While the World Chats, Indonesia Writes." That subtitle is the first of several the pill types in turn (`SUBTITLES` in the template). Every one of them must stay a true description of the story.
   Section headings are plain questions (the author's preference, after "Where does Indonesia rank in the use of ChatGPT?"). Keep new headings in that style. The one exception is the closing block of `hundred`, "Let's dissect these numbers," which follows the author's own wording.
3. Indonesia is compared with the world and with a Southeast Asia average. Do not single out the Philippines or any other neighbor as a rival. Two places name other countries, both at the author's request: the Southeast Asia block in `drift` describes how each of the nine neighbors fell, and the age table in `young` sets Indonesia beside eight large countries. Japan is labeled once in `ade` as the opposite pole.
4. Layouts are mixed on purpose: not every section pins a chart on the right.
5. Outside reporting comes from published sources, linked inline and listed at the end. There are no interviews, and no quote is invented.
6. Paragraph-led, NYT-style long form. Paragraphs carry the reasoning, and charts change only when the argument does.

## Data rules

- Everything is a share of messages. The only intensity measure is the per-capita rank.
- Default unit is the quarterly average of monthly shares. Six-month averages (April to September 2026) are used for ranks. Indonesia's monthly figures are noisy (work share moves about 4 points month to month).
- "World" is OpenAI's global series. Where none exists (work activities, per-capita rank) the median country stands in, and the text says so.
- "Southeast Asia" is a simple, unweighted average of Indonesia's neighbors with complete data in that file, excluding Indonesia: 9 countries for work and topics, 8 for age, 7 for intent, 6 for gender, 5 for work activities. Gender by topic has too little regional coverage (only the Philippines has every topic in each of the last three months), so that chart compares Indonesia with the world only, and its info line says why.
- Every rank states its denominator, because country counts differ by file and month.
- Limits that must stay visible in the text: the country-level classifier is binary, so "work" may include study. Gender is inferred from first names. Age covers adults who reported one. Consumer accounts only. Traits cannot be cross-tabulated. They are stated in the sections where they arise and again in the closing paragraphs. There is no separate list of limits.

## Writing conventions

- American spelling and the Oxford comma.
- No semicolons joining two sentences. Split the sentence instead.
- No em dashes in prose.
- Every number in the prose must be traceable to `docs/data_build_log.txt` or to a linked source. If the data logic changes, re-check the prose numbers. `docs/findings.md` maps numbers to sections.
- Quote sources sparingly and paraphrase otherwise.

## Checking work

After a change, rebuild and screenshot the affected section at 1440x900 and 390x844 with `scripts/shot.py`, then look at the images. Label collisions are the usual failure, especially on the phone layout. `shot.py` also prints page errors. On a phone, look at every state of the pinned charts: the `grid` caption once ran off the right edge in the topic view only.

## Publishing notes

Live at https://akbsaputra.github.io/chatgpt-use/. `.github/workflows/pages.yml` runs `assemble.py` and deploys `dist/` on every push to `main`, so the live page always matches the template. Still commit the rebuilt `dist/index.html`, so the file in the repo matches too.

The page is static and self-contained, so it can go on any static host.

## Known gaps

- In `iwa` and in the hover labels of `ade` and `work`, country names need a pointer or a tap.
- Tested in headless Chrome at desktop and phone widths, not in Safari or Firefox.
- The campus reading in `campus` rests on surveys and statistics. Two or three real voices (a student, a lecturer, a schoolteacher) would strengthen it.
- No Indonesian-language version.
- The "compare your country" selector from the storyboard was not built.
