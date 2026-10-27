# Read a paper

The goal is to understand a paper fast and, if needed, give it a score.
You get an animated slide deck of how the paper works. Three reviewer
subagents (theory, systems, protocol) put their questions on the slides
where the questions arise. Each lane proposes a score.

## How to start

1. Make a folder for the paper. Put the PDF in it. For example `papers/my-paper/paper.pdf`.
   The folder can be anywhere. Inside this repo, `papers/` is git-ignored.
2. Start Claude Code in that folder. Then say one of these:
   - `/read-paper` (if the skill is installed, see README.md);
   - `Read <repo>/PROMPT.md and do it for this folder.`
3. Optional: put `score-scale.md` in the folder for the scale of the venue.
   Put `notes-in.md` there for what you want to know.

In the steps below, `$R` is this repo and `$P` is the paper folder.

## Steps

```
Do the steps below in sequence. $R is the read-paper repo. $P is the paper folder.

0. Set up.
   - Find the PDF in $P. If there is more than one, ask which one.
   - Make $P/work/ and $P/lanes/.
   - Read $P/notes-in.md and $P/score-scale.md if they exist.
     Otherwise use $R/template/score-scale.md.
   - Keep the paper private. See "Privacy" below.

1. Read the paper.
   - Extract the text with the PyMuPDF4LLM MCP into $P/work/paper.md.
     If the MCP fails, run: python3 -I $R/tools/extract.py <pdf> $P/work
   - Make a PNG of each page: python3 -I $R/tools/extract.py <pdf> $P/work --pages-only
     (extract.py without the flag makes them too). Read display equations from the PNGs.
   - Read the full paper, with the appendices.
   - Write $P/work/outline.md:
     - one line per section, with its pages;
     - each claim, quoted, with its page. Mark each "first", "only" or "new" claim;
     - each headline number, with its table, figure or equation;
     - the notation that the paper uses.

2. Start the 3 lanes now, in parallel, in the background.
   - Lanes: theory, systems (evaluation) and protocol (design).
     $R/template/lanes.md gives the focus of each lane.
   - Build each brief from $R/template/lane-brief.md. Fill in the lane,
     the focus, the paths and the score scale.
   - Each lane writes $P/lanes/<lane>.md. It keys each question to a place
     in the paper (section, page, theorem), not to a slide.
   - Do not wait for the lanes. Go to step 3.

3. Build the deck while the lanes run.
   - Copy $R/template/deck/ to $P/deck/. Edit $P/deck/index.html.
   - Make 12 to 18 slides. data-sec names the section of each slide.
   - The deck must show:
     - the title, the problem and the claims;
     - a notation slide;
     - each technical section: how the scheme works, step by step;
     - the security argument, if there is one;
     - the evaluation, with the paper's numbers redrawn as charts;
     - the closest prior work, and what is new;
     - the claims ledger: each "first" claim with its qualifier;
     - all questions by lane (the #allq slide builds itself);
     - the score card;
     - a backup slide with sources, failed fetches and what is not verified.
   - Make it visual, not a wall of bullets:
     - Give each technical slide one figure: a message flow, a party diagram,
       a data layout or a chart. Draw it in SVG with the helpers.
     - Animate each figure with build steps, so that a flow appears in order.
     - Put the formal statement in a box next to the figure.
     - Put the detail that the figure leaves out in the speaker notes.
     - Cite the page, table or equation for each number. Tag each number
       that you derive with <span class="tag calc">computed</span>.
       Keep the scripts that compute them in $P/work/.
   - "Deck mechanics" below gives the rules for the code.
   - Check the deck:
     - $R/tools/serve.sh $P 8028   (run it in the background)
     - python3 -I $R/tools/shoot.py http://127.0.0.1:8028/deck/ $P/work/shots
     - python3 -I $R/tools/shoot.py http://127.0.0.1:8028/deck/ $P/work/shots-narrow --narrow
     - python3 -I $R/tools/interact.py http://127.0.0.1:8028/deck/
     - Look at each contact sheet (sheet-*.png). Fix overlaps, clipped boxes
       and every console error. interact.py must end with FAILURES: 0.

4. Fold the lanes into the deck when all three are back.
   - Put each strong question on the slide that covers its place in the paper:
     <p class="q" data-lane="theory">Question? <span class="at">§5, p. 10</span></p>
     Lanes: theory, systems, protocol. Use reader for the reader's own questions.
   - Use at most 3 questions on one slide. Keep the rest in the lane files.
   - Fill the prior-work slide, the claims ledger, the score card and the
     backup slide from the lane reports.
   - If lanes disagree, show both views, and say who holds which.
   - Run the checks of step 3 again.

5. Write $P/notes.md from $R/template/notes.md.

6. Stop and report:
   - the deck URL: http://127.0.0.1:8028/deck/ ;
   - one screen of digest for each lane: score, confidence, closest prior work,
     top 3 weaknesses, top 3 questions;
   - the suggested score range, and what would move it.
   Then wait. The reader reads the deck and may send notes.

7. Only if the reader sends notes: merge them.
   - The reader's verdict sets the score.
   - Add the lane findings that the reader does not mention as supporting points.
   - Add the reader's questions to the deck as data-lane="reader" chips.
   - Write $P/review.md. Ask before you fill any submission form.
```

## Language rules

Use these rules in every text file and on the slides.

- Write approximately 80 percent ASD-STE100.
- Write one claim in each sentence.
- Use 20 words or fewer in each sentence.
- Use the active voice and the present tense.
- Attach each weakness to a page, section, equation, table or theorem.
- Write math as `$..$` in text files and in the HTML text.
- Write each dollar amount as `\$`.
- Check: `python3 -I $R/tools/sentcheck.py $P/notes.md $P/lanes/*.md`

## Deck mechanics

- Keep the CSS, the engine, the helpers and the registry block of the template.
  Replace the slides and the example figures (`fclaims`, `fflow`, `fbars`).
- A figure is `<svg id="fxxx">` inside `<div class="fig">`. Register it in `FIGS`.
  Set `BUILDS.fxxx` to its highest build step. Set `FMIN.fxxx` (about 720–900),
  the narrowest design width in deck mode.
- A figure function draws its final state at width `W`. `bg(svg, k, fn, kind)`
  tags what `fn` draws with build step `k`. Kinds: `fade`, `land`, `growx`,
  `growy`, `draw`. Use step 0 when `W < 640`: phones show the final state.
- A formal box is `<div class="formal" data-bstep="K">` inside `<div class="row">`,
  next to the figure. It appears at build step `K`.
- Helpers: `T` (text), `rt` (text with `_x` or `_{xy}` subscripts), `rect`, `path`,
  `arrow` + `arrowDef`, `pill`, `rpill`, `plate` (a label on a plate, so that it
  never touches a line), `tbox`, `disc`, `tick`, `mark`, `verdict`, `brace`, `sector`.
- Colours come from CSS tokens: `css('--s1')` … `css('--s4')`, `--good`,
  `--critical`, `--accent`, `--ink-muted`. Never hard-code a colour.
  Light and dark both work then.
- KaTeX renders `$..$` and `$$..$$` in HTML text. SVG text cannot hold KaTeX:
  use Unicode and `rt()` subscripts there.
- Write `c_{\mathrm{max}}`, not `c_{\max}`. `\max` inside a subscript gives a
  malformed `<msub>` in Firefox.
- A `$` inside an SVG label or a JS string is literal text, not math.
- The deck checks itself on load. It logs a console error when `BUILDS` does not
  match the steps of a figure. It also logs one for a question with an unknown lane.
  It logs a warning when a question has no anchor. shoot.py and interact.py
  report these.
- Keys: ← → space PgUp PgDn Home End move. N notes. Q questions. T theme.
  B builds. `#k` in the URL jumps to slide k.

## Privacy

Papers under review are confidential.

- Never commit a paper, its text, its deck or its notes to this repo.
  `papers/` is git-ignored. Do not change that.
- Serve the deck on 127.0.0.1 only. serve.sh refuses 0.0.0.0.
- Never upload the PDF or paste its text into a web service.
  Search for prior work by its title and authors only.
- Do not publish the deck as an artifact or on a website.

## Known problems

- The PyMuPDF4LLM MCP can fail with "Tesseract language initialisation failed".
  tools/extract.py turns OCR off and works without tessdata.
- Direct ePrint PDF links return HTTP 403 to scripts. Use
  `https://web.archive.org/web/<year>id_/https://eprint.iacr.org/<id>.pdf`.
- shoot.py can flag KaTeX square-root SVG paths as overflow at the right edge.
  That is a false positive.
- In --narrow shots, the fixed control bar can cover the bottom of a tall slide.
  The page itself is fine.
