# 10. Gold File - Format

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

| | |
|---|---|
| audit-rubric id | `5b2a7e9a-4aaf-40d8-8ea5-eec4bf279436` |
| title | Gold File - Format |
| allowed scores | 2, 5 |
| required | true |
| evidence class | `files` |
| subagent model | `claude-opus-5` at `--effort max` |

## Question

Rate the Format of the Gold File dimension.

## Description (verbatim from the CSV)

```
All file types that can be created by the software programs in the following list are acceptable for the Gold Files:
LibreOffice Calc, LibreOffice Writer, LibreOffice Impress, Blender, 3D Slicer, KiCAD, FreeCAD, MuseScore, Chrome, Solvespace, Reaper, MPV, pgAdmin, VSCode, LabPlot, Octave, R Studio, GeoGebra, Zotero, Logism, GIMP, Shotcut, Obsidian, and Openboard
```

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- This component's fail option names exactly three conditions: a format outside the 24-application list, a single expected file shared across operating systems where a per-OS file is required, and a ground-truth URL pointing at the starting file instead of the answer key. Score against those and nothing else — failing here for a reason the option does not name is a tool defect this component has already been corrected for once.
- Trust `mechanical.10_gold_file_format`: `gt_url_points_at_input`, `expected_exts` and `os_enabled` are precomputed. Treat Ubuntu-only as correct unless the task metadata enables another OS.
- Never fail a format the upload widget blocked — the contributor had no compliant path. See `references/source-conflicts.md`.
- **Structural damage scores only when it stops the task.** The suggestions listed under `minor_issues` are not scored — except where the damage leaves the expected file **unopenable**: a corrupt archive, or bytes that are not the declared format at all. Such a file is not one the 24 permitted applications can generate or open, which is this component's fail option read literally, so take score 2 and say which application cannot open it. Everything short of that — residue, mojibake, inconsistent typography, an unfollowed style instruction — is a suggestion and leaves the score at 5.

### Score 2  — **justification REQUIRED**

```
[Fail - Wrong Format]
The gold file is not in a file format that the software programs in the list above can generate. | A single gold file is shared across OS's. | The ground-truth URL points to the starting file instead of the gold file.
```

### Score 5  — justification not required

```
The gold file is in a file format that the software programs in the list above can generate. | There's a separate gold file per OS (when applicable). | The ground-truth URL points to the gold file.
```

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Wrong Format]`

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
  "component_id": "5b2a7e9a-4aaf-40d8-8ea5-eec4bf279436",
  "title": "Gold File - Format",
  "score": <one of: 2, 5>,
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
  - **Format / extension integrity** — bytes that do not match the extension: an `.xlsx` that is not a zip, a `.pdf` that is not a PDF.
  - **Archive integrity** — a corrupt or unopenable archive. `__MACOSX/` and `.DS_Store` are macOS metadata and never a defect.
  - **Placeholder or draft residue** — `TODO`, `TBD`, `FIXME`, `Lorem ipsum`, `XXX`, `<placeholder>`, template instruction text left in place, an obviously unfilled field.
  - **Mojibake and encoding damage** — `â€™`, `Ã©`, replacement characters.
  - **Self-inconsistent typography** — a mid-document typeface or size change with no structural reason, heading levels that skip or invert, mixed number formats in one column (`1,000` beside `1000`), mixed date formats in one table, inconsistent currency or unit symbols for the same quantity, straight and curly quotes mixed in one run of prose. The test is whether you can point at **two places in the same deliverable that contradict each other**. An unconstrained *choice* applied consistently is never a defect.
  - **Prompt-constrained style not followed** — a stated language variant ("write everything in British English"), a named font or template, a stated date / number / currency format, or a stated capitalisation convention. Quote the prompt text and check it across every deliverable, not just the first. Keep the opening phrase as written: this defect is a hard gate elsewhere in the project, so the report prints the whole entry in bold. It still does not affect your score.
  - Appearance claims come from the rendered pages under `render/`, never from extracted text — look at them before calling anything here a defect. A file `render_index.json` reports as not visually verifiable is **not** a defect: set `blocked_on` and lower `confidence`.
