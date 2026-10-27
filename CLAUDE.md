# read-paper

This repo is a template for reading research papers. `PROMPT.md` is the workflow.

- To read a paper, follow the "Steps" block of `PROMPT.md` for the paper folder.
- `papers/` is git-ignored. Never commit a paper, its text, its deck, its lane
  reports or its notes. Never force-add them.
- Serve decks on 127.0.0.1 only (`tools/serve.sh`).
- Changes to the template go in `template/`, `tools/` and `PROMPT.md`, never in a
  paper folder. Test a template change with `tools/shoot.py` and `tools/interact.py`
  on `template/deck/` (`tools/serve.sh template 8028`).
