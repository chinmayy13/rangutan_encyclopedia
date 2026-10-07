# 11. Component: Gold File - Input Consistency

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `456787e8-cb89-4fd7-a6bd-9d0760318f5e` |
| title | Component: Gold File - Input Consistency |
| allowed scores | 2, 3, 5 |
| required | true |
| evidence class | `files` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Input Consistency of the Gold File dimension.

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Four conditions must all hold** before taking the fail option: the value is *graded* (part of what the deliverable is scored on, not incidental prose); it is absent from the prompt; no input file contains it or makes it derivable; and no defensible derivation from the inputs reaches it. A value reachable from a stable external source the prompt explicitly points to is traceable.
- **Name each place you looked and what you found there** — "checked `field_profile_raw.csv` (no `settlement_date` column), `fund_db_schema.sql` (column exists, no values), and the prompt (silent)". *"I could not immediately find it"* is not that.
- Where to look hardest: **joins and merges** whose record count does not match what the inputs actually produce; **looked-up constants** present in no supplied input; and **swapped inputs** — IDs, date ranges, record counts or entity names that do not correspond to the supplied set, which usually means the file was built against an earlier input set and never rebuilt, and usually breaks more than one thing.
- **Quotation fidelity.** Text presented as a quotation — in quote marks, as a block quote, or introduced as what a source says — must appear in the named source character-for-character. A reworded paraphrase presented as a quotation is a defect, as are two non-adjacent spans joined as continuous with no ellipsis. Normalisation that does not change wording is fine: line wrapping, whitespace, smart vs straight quotes, a marked ellipsis, bracketed editorial insertions. Unquoted prose that summarises a source is **not** this defect.
- **Locators.** A page, section or clause reference must resolve to that material in the named source. A three-page source cannot carry a citation to page 5.
- **Collect every statement of the same rule before checking any value.** A threshold, cutoff, eligibility rule, formula, mapping or definition is routinely stated in more than one place: a methodology or briefing PDF, a `Reference`, `Notes` or `Glossary` sheet inside a supplied workbook, the prompt itself, and the answer key's own method note. Find all of them and write each out verbatim with its location before deciding anything. Three failure shapes, each of which stops a correct agent reproducing the answer key. **(i) Two inputs state different rules for the same quantity** — a PDF selecting on `BMI > 29.9 and glucose > 127.5` while the dataset's own reference sheet defines diabetic as `> 200` and obese as `> 30`. **(ii) The answer key applies neither** — it takes the whole population, or a third rule it never names, so no agent following any supplied rule lands on the gold. **(iii) A supplied rule cannot be applied to the supplied data** — it selects an empty set, or contradicts a label the data already carries. Test it: sort the column and compare against the cutoff. A `> 200` diabetic threshold on a glucose column whose maximum is `199`, in a file whose outcome column already marks 268 positive rows, is unusable and self-contradictory at once. Report which rule the gold actually used and whether any supplied input states it. An agent cannot pick the intended rule by luck, so this is an input consistency defect even when every individual figure is arithmetically sound.
- A different-but-defensible method reaching a different valid answer is never an input-consistency defect, and a quotation whose source file could not be fetched is unverifiable rather than wrong. Two supplied rules that genuinely conflict are the opposite case: there the agent's choice is not defensible-either-way, because only one of them reproduces the answer key.

### Score 2  — **justification REQUIRED**

```
[Fail - Input Consistency]
The gold file's records or values do not derive from the provided input files (a different dataset, IDs, or figures than the agent receives), so a correct agent working from the inputs cannot match it.
```

**Applies to this score.**

- **Input sufficiency is this option.** Where a datum the prompt quotes, a criterion grades, or an expected file contains is carried by **no** input file — absent, truncated, illegible, corrupt or empty — a correct agent working from the inputs cannot match the answer key, which is exactly what this option describes. Name the input file, the absence mode (`absent` / `truncated` / `illegible` / `corrupt` / `empty`), the datum, and what relies on it. **The fix is to the input file**, not to the rubric or the expected file — say so, because the natural repair is to infer the value, and that silently ships a broken task.
- Three things are **not** this, and a false positive here stops a healthy task: a datum stated in full **elsewhere** in the inputs is present, even where the place the task points at is damaged; a datum the task asks the agent to **compute** from the inputs is present; and a file you merely could not open is a tooling gap for `blocked_on`, not a missing input.
- **A rule conflict the answer key resolves silently is this option.** Where the inputs state two different rules for the same selection or calculation and the gold follows neither — or follows one without saying which — the gold's figures do not derive from the inputs an agent can act on, which is this option in its own words. Quote all the competing rules with their locations, state the rule the gold actually used, and say the fix is to make the inputs agree, not to loosen the rubric.

### Score 3  — **justification REQUIRED**

```
[Non-Fail - Input Consistency]
One or two secondary gold values are not directly traceable to the inputs, but the core deliverable derives correctly from them.
```

**Applies to this score.**

- One or two secondary values not directly traceable while the core deliverable derives correctly. This band exists — use it rather than escalating.
- An input-sufficiency gap on a **secondary** datum lands here too. Still name the input file and the fix.
- A rule conflict that moves only an incidental figure, where the graded deliverable derives correctly under every supplied reading, lands here rather than on the fail option.

### Score 5  — justification not required

```
Every graded gold value traces to the provided inputs; an agent following the inputs can reproduce it.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Non-Fail - Input Consistency]`
- `[All] [All] [Fail - Input Consistency]`

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
  "component_id": "456787e8-cb89-4fd7-a6bd-9d0760318f5e",
  "title": "Component: Gold File - Input Consistency",
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
  - **A cited filename that does not match a supplied input, character for character.** Answer keys drift in both directions: a browser artifact the input does not carry (`Airline Dataset(1).csv` cited for `Airline Dataset.csv`), and a silently *corrected* misspelling (`Diabetes Dataset.xlsx` cited for an input actually named `Daibetes Dataset.xlsx`). The correction is the more misleading of the two because it reads as right while naming a file that is not in the task. Compare every cited name against `input_files[]` byte for byte. This does not make a value untraceable, so it stays here unless a graded criterion depends on the cited string.
