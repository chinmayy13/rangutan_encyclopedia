UNIT UNDER REVIEW: task_9
EVIDENCE DIRECTORY: /home/user/rangutan_encyclopedia/audit/task_9
  bundle.json            /home/user/rangutan_encyclopedia/audit/task_9/bundle.json
  inputs_extracted.md    /home/user/rangutan_encyclopedia/audit/task_9/inputs_extracted.md
  expected_extracted.md  /home/user/rangutan_encyclopedia/audit/task_9/expected_extracted.md
  files/inputs/          /home/user/rangutan_encyclopedia/audit/task_9/files/inputs
  files/expected/        /home/user/rangutan_encyclopedia/audit/task_9/files/expected
  render_index.json      /home/user/rangutan_encyclopedia/audit/task_9/render_index.json

THE SUPPLIED SET — every one of these must be opened:
  input    /home/docker/Desktop/source_coin_token.png
  input    /home/docker/Desktop/Bomb.glb
  input    /home/docker/Desktop/scene_reference.png
  input    /home/docker/Desktop/gameplay_config.txt
  expected Bomb_Chain_Reaction_Godot_Project.zip
  expected bomb_runtime_log.txt
  expected bomb_blast_frame.png

==============================================================================

# Input file consistency — cross-artifact review

You are checking ONE CUA v3 task submission for a defect class the 28-component
audit rubric never asks about directly: whether the material the task is built
from agrees with itself.

The 28 components each grade one artifact against the form. None of them grades
the **input files** in their own right, and none asks whether two supplied
sources contradict each other. That is your entire job here.

## Hard limits

- **This is not scored.** It cannot change a component score, a label or the
  verdict. Nothing you write here moves the roll-up.
- **Do not re-audit the rubric, the prompt or the gold.** Where a finding is
  already owned by a scored component — 09 gold accuracy, 11 input
  consistency, 15 rubric accuracy, 16 coverage — record it and name the
  component in `component`. Duplication is expected and useful; silence is not.
- **Affirmative evidence only.** Every finding quotes both sides with its
  location. "These might disagree" is not a finding.
- **A file you could not open is `blocked_on`, never a finding.** A missing
  renderer is a limit of this host, not a defect in the submission.

## What consistency means here

Two directions, both required.

**A. Input against input.** The supplied files must describe one world.

- **Rule conflict.** The same threshold, cutoff, eligibility rule, formula,
  mapping or definition stated differently in two places — a methodology PDF
  selecting on `BMI > 29.9 and glucose > 127.5` while the dataset's own
  `Reference` sheet defines diabetic as `> 200`. Collect every statement of a
  rule before judging it; they hide in reference sheets, notes tabs, footnotes
  and briefing documents.
- **Rule unusable against the data it governs.** Apply each supplied rule to
  the supplied data and see what it selects. A cutoff that returns an empty set
  (`> 200` on a column whose maximum is `199`), or that contradicts a label the
  data already carries (that same column beside an outcome field marking 268
  positive rows), is broken whichever way the agent reads it.
- **Value conflict.** One quantity, two different figures across files, or a
  total that disagrees with the rows that feed it.
- **Scope, unit and vocabulary conflict.** Date ranges, currencies, units,
  entity names, IDs or category vocabularies that do not line up between files
  that have to be joined.
- **Self-contradiction inside one input.** A reference sheet that disagrees
  with the data sheet beside it; a summary page that disagrees with its own
  detail table.
- **Missing referent.** An input naming a sheet, column, page, appendix or
  companion file that the supplied set does not contain.

**B. Input against everything else** — the prompt, the expected files and the
rubric criteria.

- The **prompt** names a file, sheet, column, page or figure the inputs do not
  have, or states a value or rule the inputs contradict.
- The **expected files** apply a rule that no input states, or resolve a
  conflict between two inputs silently, so an agent following either supplied
  rule misses the answer key. Say which rule the gold actually used.
- The **expected files** cite an input by a name that is not the input's name,
  character for character — a browser artifact (`Airline Dataset(1).csv`), or a
  silently corrected misspelling (`Diabetes Dataset.xlsx` for an input actually
  named `Daibetes Dataset.xlsx`).
- A **criterion** grades a value, threshold or artifact that conflicts with
  what the inputs say.

## Severity

Exactly two levels, and the test is what a correct agent would produce.

- **major** — the inconsistency changes what a correct submission looks like.
  An agent working faithfully from the inputs cannot reach the graded answer,
  or must guess between two supplied rules that lead to different graded
  values. Anything that makes a graded criterion unsatisfiable is major.
- **minor** — a real inconsistency that moves no graded output: naming drift, a
  stale note, an unused definition that contradicts a used one, a cosmetic
  disagreement in incidental prose.

The unit's `verdict` is mechanical: `major` if any finding is major, else
`minor` if any finding is minor, else `none`. Do not soften a major finding
because the task is otherwise good, and do not inflate a cosmetic one.

`none` is a real and useful result. Report it plainly, and say in `summary`
what you checked to reach it.

## Method

1. Inventory every input file and every expected file, with its role.
2. Open each one. Text extraction is enough for values; for a scanned page or
   an image, open the rendered page or the original with the Read tool. What a
   dataset holds must be checked against the data, not against its own
   description of itself.
3. List every rule, threshold, definition and shared quantity, with the file
   and location where each is stated. A quantity stated once cannot conflict;
   spend your effort on the ones stated twice.
4. For each, compare every statement of it and apply it to the data it governs.
5. Then check the prompt, the expected files and the criteria against that
   list.
6. Report what you covered: files opened, every shared rule and quantity
   compared (listed one by one in `rules_compared`, not counted), findings.

## Evidence

- `bundle.json` — `prompt`, `criteria[]`, `input_files[]`, `expected_files[]`,
  `verifier`, `mechanical`.
- `inputs_extracted.md` — every input file dumped to text.
- `expected_extracted.md` — every expected file dumped to text.
- `render/inputs/<filename>/page-NN.png`, `render/expected/<filename>/page-NN.png`
  — the pages, for anything whose content is only legible as an image. Open
  them with the **Read** tool; `cat` and Bash are blind to a PNG.
- `files/inputs/`, `files/expected/` — the originals, for images.
- `render_index.json` — consult before any claim that rests on appearance.

## Output contract

```json
{
  "unit": "<id>",
  "verdict": "major" | "minor" | "none",
  "summary": "<2-5 sentences: what you compared and what you found>",
  "files_checked": ["<path>", "..."],
  "rules_compared": ["<each shared rule / quantity you cross-checked, and the files you compared it across>", "..."],
  "findings": [
    {
      "severity": "major",
      "kind": "rule-conflict",
      "files": ["<file a>", "<file b>"],
      "statement_a": "<verbatim, with file and location>",
      "statement_b": "<verbatim, with file and location>",
      "why_conflict": "<why both cannot hold>",
      "graded_impact": "<which criterion or value moves, or 'none'>",
      "component": "<NN of the scored component that owns it, or null>",
      "fix": "<the change that makes the sources agree>"
    }
  ],
  "blocked_on": "<what you could not open, or null>"
}
```

`kind` is one of `rule-conflict`, `rule-unusable`, `value-conflict`,
`scope-conflict`, `missing-referent`, `self-contradiction`, `naming-drift`,
`gold-resolves-silently`, `prompt-conflict`, `criterion-conflict`.

Leave `findings` empty rather than filling it. The fix must make the **sources
agree**; loosening the rubric to accommodate a contradiction is not a fix.
