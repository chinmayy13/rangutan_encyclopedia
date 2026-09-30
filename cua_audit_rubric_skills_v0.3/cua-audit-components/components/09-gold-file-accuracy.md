# 09. Gold File - Accuracy

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `4d2d498a-cd03-4e60-9367-1dc61a3e4de9` |
| title | Gold File - Accuracy |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `files` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Accuracy of the Gold File dimension.

## Description (verbatim from the CSV)

```
The expected (gold) file is the answer key—it must exactly match what the prompt asks and follow file/naming standards.

If the prompt specifies file names, it's a fail if the gold files don't follow them.
The expected file (not the prompt) is the rubric's scoring anchor.
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Enumerate the prompt's discrete asks before opening anything.** An ask is one thing the contributor was told to do: produce a named file, include a named section, apply a stated constraint, order something a stated way. Split compound sentences — "add a scorecard and a grounding note" is two asks. Mark each MET (name the exact location), MISSING (quote the prompt text and say what is there instead) or UNVERIFIABLE (say why), and report the totals.
- **A universal ask is not met by a sample.** Where the prompt says *every / all / each*, build the set, check every member and report the count — "12 of 19 figures carry a trace entry; the 7 without are …". Derived values are where this breaks: a register cites the figures lifted straight off a page and silently omits the ratios and aggregates the author computed. Partial satisfaction is MISSING.
- **Recompute; do not eyeball.** Totals against their own components, percentages against a consistent base, derived columns against their stated formula, ranks and ordinals. State both numbers: what the file says and what you get.
- **Values the package cannot produce.** Where the expected set contains a generating artifact — a script, notebook or macro — enumerate the literal values it can emit, then check every generated file against that set. A cell holding a value outside it is a defect however sensible the word reads in isolation, and the fix must be a value the artifact can actually emit; prescribing a fourth status a three-status script cannot write relocates the defect instead of resolving it.
- **Hold the answer key's own method statements to what it actually did.** A "methodology", "assumptions", "thresholds used here" or "limitations" note is a claim about the file it sits in, and it is checkable: read the stated rule, apply it yourself, and compare with the numbers the file carries. Two shapes recur. The stated rule **drives nothing** — the note quotes a `> 200` diagnostic cutoff while every figure in the file comes from age-band prevalence. And the stated rule **contradicts the file's own results** — applying it would yield a different answer, sometimes an empty one, than the file reports. Both are wrong statements inside the answer key, independent of whether the figures themselves are right, and they mislead every agent that reads the note as instruction. Quote the note, state the result under the stated rule, state the result the file reports, and name the method actually used. A note that honestly records a limitation is not this — the defect is claiming a rule was applied when it was not.
- **Size is not severity.** A one-word defect can be a fail and a whole-chart defect a non-fail. The question is whether the graded value is reachable.
- **Write out the fix before reporting the finding.** If the only available fix is a font, colour, spacing, layout, extra-sheet, rounding, grammar or methodology change the prompt never constrained, the fix is illegal — so the finding is wrong. Drop it.
- Before marking anything MISSING, search the whole expected set: content asked for in one file is often legitimately delivered in another. An ask the prompt leaves open is MET if the file satisfies any reasonable reading.

### Score 2  — **justification REQUIRED**

```
[Fail - Inaccurate Gold File]
The gold file doesn't match the prompt, e.g., wrong/missing data, wrong values, ordinal vs. cardinal, tied-rank errors, missing required formatting, etc.
```

**Applies to this score.**

- A **primary** ask MISSING — a required deliverable, a core piece of the requested work, or a stated hard constraint — or a graded value that is wrong or unreachable.
- **The wrong-file case.** An expected file that is the genuinely untouched starter is not an answer key at all, so it is "wrong/missing data" in this option's own terms. Establish direction first: `manifest`/`bundle` marking a shared checksum says the bytes match, not which way the copy went. If the file is a completed deliverable that was *also* staged onto the VM as a starter, the defect is in the initializer and this does not fire.
- **Cross-file contradiction**, where the figure is graded. The same value quoted in two deliverables cannot disagree and both be right, so at least one holds wrong data and no correct agent can match both.

### Score 3  — justification not required

```
[Non Fail - Somewhat Inaccurate Gold File] 
Content and values are substantively correct and match the prompt, but a minor, non-scoring-impacting format issue exists (e.g., a cosmetic inconsistency, a resolvable naming deviation) that doesn't alter verifier outcome.
```

**Applies to this score.**

- A **secondary** ask MISSING, or content substantively correct carrying a minor non-scoring format deviation.
- **Cross-file contradiction**, where the figure is incidental prose rather than a graded value. Report it with both locations and say which one you believe is wrong.

### Score 5  — justification not required

```
The gold file is correct and aligns with the prompt.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Inaccurate Gold File]`
- `[All] [All] [Non-Fail - Somewhat Inaccurate Gold File]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Evidence to read

- `bundle.json` -> `prompt`, `criteria[]`, `input_files[]`, `expected_files[]`
- `inputs_extracted.md` — every input file dumped to text
- `expected_extracted.md` — every expected (answer-key) file dumped to text
- `render/inputs/<filename>/page-NN.png` and `render/expected/<filename>/page-NN.png` — each non-image file rasterised page by page: what it LOOKS like, as opposed to what the extraction says it contains
- `render_index.json` — per file: `status`, `visual_verifiable`, `parity`, `pages`, `unverifiable_reason`. Consult it before making any claim about appearance
- `files/inputs/` and `files/expected/` — the originals, for images
- `bundle.json` -> `staged_files` — any value starting `FAILED` did not download; say so rather than guessing

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Looking at the artifacts

You can read images directly. Use the Read tool on any `.png`, `.jpg`, `.gif` or `.webp` under `files/inputs/` or `files/expected/` and judge what it actually shows: axis labels, series, legends, value labels, what the picture depicts, whether it matches its filename and what the prompt says about it. The text extraction lists these files as `IMAGE` with dimensions only; that is a limit of the extraction, not of you. Never score a component clean on an artifact you did not look at. If a file genuinely will not open, set `blocked_on` and lower `confidence`.

Everything else that has a visual form — `.docx`, `.xlsx`, `.pptx`, `.pdf`, `.html`, and the rest — has already been rasterised for you, one PNG per page, under `render/<side>/<filename>/page-NN.png`. The prompt lists the exact page files.

**Open them with the Read tool before you score, and do it first.** Not `cat`, not `head`, not a Python one-liner: a PNG carries no text for Bash to print, and the `text.txt` beside the pages is text, not appearance. Reading the chart XML out of an `.xlsx`, or the slide XML out of a `.pptx`, tells you a chart was declared — it cannot tell you the axis labels are legible, the series fit, the columns are not clipped or the table did not spill onto a second page.

The pages are the only evidence that shows pagination, clipping, column overflow, overlapping shapes, blank pages, chart legibility and whether something fits on one page. So: any statement you make about appearance must name the page file you opened to see it. An appearance claim you did not look at is not a finding, and it is not a clean pass either.

Never render anything yourself and never attempt a `pip install` or an application install. Extraction and rendering are both already done. Open an original only when it is an image.

### What the render is worth — check `render_index.json` first

The entry for a file states how far its appearance can honestly be judged. Respect it literally.

- `visual_verifiable: true` — the pages are a faithful render. Judge appearance from them.
- `visual_verifiable: false` (`status` `degraded` or `unavailable`) — the renderer for that format is missing or only a first-page preview was produced. Its `unverifiable_reason` says which. Every ask about that file's layout goes in `blocked_on` with that reason. A renderer this audit host lacks is never evidence of a defect in the submission.
- `truncated: true` — pages beyond the ones listed were not rendered. Say nothing about them.
- `parity` — whether the application that laid these pages out is the version the CUA VM runs (`cua-applications.csv`). `exact` or `compatible`: pagination claims are sound. `mismatch` or `unknown`: what you see may be this host's LibreOffice rather than the VM's, so claims that depend on exact reflow — total page count, a table fitting on one page, a specific line break — go in `blocked_on`. What is visible on the page regardless of reflow (a missing chart, an empty section, a wrong label, overlapping shapes) stands as a finding.

## Required method — reproducibility of the expected artifact

Do this before you score. The question is not whether the expected files agree with one another; it is whether a competent agent could arrive at them from what it is actually given.

1. Inventory what the agent has. List the input files. For every input that is a script, template, schema or config, state the outputs it can generate and the vocabulary, labels and ranges it can emit.
2. For each graded value in the expected files, name the specific input it derives from and the operation that produces it. Recompute it where it is computable.
3. Mark every value you cannot reach, and say why — absent from all inputs; requires a label, constant or category the provided code cannot emit; requires data the agent never receives; requires a step the inputs do not support.
4. Report both halves in `justification`: what you reconstructed, and what you could not reach.

**Reachable is not the same as correct.** Step 3 establishes only that a value can be derived from the inputs. It says nothing about whether the value is right. Both must hold, and correctness is the more important of the two. Separately check: is the arithmetic right; does the artifact satisfy every request the prompt and any supplied template make, including sections or fields left blank; do the inputs actually contain what their filenames and the prompt claim they contain; and is the content true against the domain rather than merely internally consistent. A traceable value that is wrong, and an artifact that is accurate but incomplete against the template, are both defects. State the correctness check you ran, not only the derivation.

A label or wording is a presentation choice **only if no criterion grades it**. Check `criteria[]`: once a criterion compares that cell, field or label to the expected file, it is a graded value, and "the agent could have phrased it differently" is not available as a defence — the criterion demands the expected file's version specifically.

A graded value the agent cannot reach is **not** cosmetic and **not** a disagreement between expected files. It is unreachable, every criterion anchored to it is unsatisfiable. Report it. But score **only** against this component's own answer options: if none of them describes unreachability, this finding does not change your score, and it belongs in `justification` as context. Never stretch an option's wording to fit a defect it does not name.

## Output contract

Return exactly one JSON object:

```json
{
  "component_id": "4d2d498a-cd03-4e60-9367-1dc61a3e4de9",
  "title": "Gold File - Accuracy",
  "score": <one of: 2, 3, 5>,
  "error_category": "<verbatim from the list above, or null>",
  "justification": "<required when the chosen score says so>",
  "evidence": "<quote the exact text, value, cell or filename>",
  "criteria": [<rubric criterion numbers, if applicable>],
  "confidence": "high|medium|low",
  "blocked_on": "<what you could not verify, or null>",
  "minor_issues": ["<non-scoring suggestion>", "..."]
}
```

Rules:

- Score **only** from the options above. The clean-pass score is `5`.
- A score whose option is marked **justification REQUIRED** must carry a non-empty `justification` naming the threshold it crosses and the evidence it rests on.
- Quote evidence. A finding with no quoted text, value or filename is not a finding — score the clean pass instead.
- If you could not verify something (a file would not open, an artifact is unavailable), set `blocked_on` and lower `confidence`; do not guess.
- Judge **this** submission only. Any reviewer score or feedback in the task response was written about the PREVIOUS attempt and does not apply here — ignore it.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.
- Record in `minor_issues` any of the following you find. Each entry quotes its evidence, names the file or criterion, and states the fix:
  - **Close calls.** If you seriously considered reporting something and talked yourself out of it, record it here: state both readings, which you applied, and the count on each side. Deciding not to flag is a decision worth recording.
  - **Your denominator** — how many expected files exist, how many you opened, how many you flagged.
