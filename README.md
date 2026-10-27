# read-paper

A template for reading a research paper fast with Claude Code.

Put a PDF in a folder and ask Claude to read it. You get:

- **An animated slide deck** of how the paper works: the problem, the claims,
  each technical step as a figure with build steps, the evaluation redrawn as
  charts, the closest prior work and a claims ledger.
- **Three reviewer lanes** (theory, systems, protocol), run as parallel
  subagents. Each lane checks its focus, fetches prior work and proposes a score.
- **Questions on the slides.** Each lane's best questions appear on the slide
  where they arise, tagged with the lane that asked them. A closing slide lists
  them all, by lane, with links back.
- **A score card** and `notes.md`: a TL;DR, the pages to read first, the claim
  verdicts and the suggested score range.

## Use

```sh
mkdir -p papers/my-paper && cp ~/Downloads/paper.pdf papers/my-paper/
cd papers/my-paper && claude
```

Then say `/read-paper` (with the skill installed).
Without the skill, say `Read ../../PROMPT.md and do it for this folder.`
The paper folder can be anywhere. Give Claude the path to `PROMPT.md`.

When the deck is ready, open http://127.0.0.1:8028/deck/
(`tools/serve.sh <paper folder>` serves it). Keys: ← → move,
N notes, Q questions, T light/dark, B builds, `#k` jumps to slide k.

## Install the skill (optional)

```sh
ln -s "$PWD/skill" ~/.claude/skills/read-paper
```

The skill only points Claude at `PROMPT.md` in this repo, so a `git pull`
updates both.

## Layout

| Path | What it is |
|---|---|
| `PROMPT.md` | The workflow that Claude follows. Edit it to change the process. |
| `skill/SKILL.md` | The `/read-paper` skill: a pointer to `PROMPT.md`. |
| `template/deck/` | The deck: one HTML file, its fonts and three example figures. |
| `template/lane-brief.md` | The brief for each reviewer subagent, with the report format. |
| `template/lanes.md` | The focus of each lane. |
| `template/score-scale.md` | The default 1–5 scale. A `score-scale.md` in the paper folder replaces it. |
| `template/notes.md` | The skeleton of the final notes. |
| `tools/extract.py` | PDF to Markdown and page PNGs, with OCR off. |
| `tools/serve.sh` | Serves a paper folder on 127.0.0.1 only (port 8028). |
| `tools/shoot.py` | Screenshots each slide and build step, light and dark, wide and phone; contact sheets. |
| `tools/interact.py` | Deck tests: build steps, keys, reload, reduced motion, console errors. |
| `tools/sentcheck.py` | Flags sentences of more than 20 words. |
| `papers/` | Your papers. Git-ignored. |

What one paper folder looks like after a run:

```
papers/my-paper/
  paper.pdf
  work/      paper.md, pages/pNN.png, outline.md, shots/, scripts
  lanes/     theory.md, systems.md, protocol.md
  deck/      index.html, fonts/
  notes.md
```

## Requirements

- Claude Code, with subagents.
- Python 3 with `playwright` (Firefox: `playwright install firefox`), `Pillow`
  and `pymupdf`.
- `pymupdf4llm`, or `uv` (extract.py then runs it with `uvx`).
- The deck loads KaTeX from jsDelivr and Ubuntu Mono from Google Fonts.

## Privacy

Papers under review are confidential. `papers/` and every PDF are git-ignored.
The deck is served on 127.0.0.1 only. The lanes search for prior work by
title and never upload the paper.

## Credits

The deck uses Computer Modern Unicode Typewriter (Andrey V. Panov; web build by
Christian Perfect) under the SIL Open Font License: `template/deck/fonts/OFL.txt`.
