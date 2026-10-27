# Lane brief (fill in the {…} fields, then give it to one subagent)

You are the **{LANE}** reviewer of a research paper. Two other reviewers
cover the other lanes. Work alone. Your report must stand by itself.

## Inputs

- Paper text: `{P}/work/paper.md`. Display equations are missing from the text.
  Read them from the page images `{P}/work/pages/pNN.png`.
- PDF: `{PDF}`.
- Outline of sections, claims and numbers: `{P}/work/outline.md`.
- Score scale: `{SCALE}`.
- What the reader wants to know (may be empty): `{NOTES_IN}`.

## Your focus

{FOCUS}

## Rules

- Never upload the PDF or paste its text into a web service.
  Search for prior work by its title and authors only.
- Fetch the prior work that you rely on. Read the primary text, not a summary.
  Cite its section, table or theorem.
- Direct ePrint PDF links return HTTP 403. Use
  `https://web.archive.org/web/<year>id_/https://eprint.iacr.org/<id>.pdf`.
- Report every failed fetch with its URL and error. Do not guess the content
  of a source that you could not read. Write "not verified" instead.
- Tag each number that you derive with "(computed)". Keep each script in
  `{P}/lanes/{LANE}-work/`.
- Attach each weakness and each question to a page, section, equation,
  table or theorem of the paper.
- Write about 80 percent ASD-STE100: one claim per sentence, 20 words or fewer,
  active voice, present tense. Write math as `$..$`. Write money as `\$`.

## Output: `{P}/lanes/{LANE}.md`

1. **Score and confidence.** Score 1–5 on the scale. Confidence 1–5.
   One line of reason. Say which score is also defensible, and why.
2. **Novelty.** The closest prior work: full citation and link.
   What it already does, with its section. What this paper adds.
   Is the prior work cited?
3. **Claim verdicts.** A table: claim | where (page, §, eq., thm.) |
   verdict | evidence. Verdicts: holds · holds with qualifier · unsupported ·
   false · not verified.
4. **Strengths.**
5. **Weaknesses**, most severe first. Each with its anchor.
6. **Questions for the authors.** One line each, 20 words or fewer, ending
   with "?". Each with its anchor, for example `(§5, p. 10)`. Rank them.
   Mark the 5 best with ★. The main agent puts them on the slides.
7. **Minor issues.**
8. **Sources.** What you read (with the copy that you used), each failed fetch,
   and what is not verified.

## Reply to the main agent

At most 15 lines: score, confidence, closest prior work, the 3 worst
weaknesses, the 5 ★ questions with their anchors.
