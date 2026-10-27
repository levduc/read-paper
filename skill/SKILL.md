---
name: read-paper
description: Use when the user invokes /read-paper, or asks to read, explain, present or review a research paper (a PDF) in a folder. Builds an animated slide deck of how the paper works, runs three reviewer subagents (theory, systems, protocol) whose questions appear on the slides, and suggests a score. Invoked as /read-paper [paper folder]; the default is the current directory.
---

# read-paper

This skill is a pointer. The workflow lives in the read-paper repo.

1. Find the repo: this skill folder is a symlink into it. Run
   `readlink -f "<base directory of this skill>"` and take the parent directory.
   Call it `$R`.
2. The paper folder `$P` is the argument, or the current directory.
3. Read `$R/PROMPT.md` in full. Do its "Steps" block for `$P`, in order.
   Follow its language rules, deck mechanics and privacy rules.
