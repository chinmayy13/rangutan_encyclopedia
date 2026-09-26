#!/usr/bin/env python3
"""Generate one component file per row of this skill's audit-rubric.csv.

The CSV is the only authority for WHAT each component scores. Everything
verbatim from it — id, question text, description, the exact score options,
which options require a justification, and the errorCategories label set — is
copied, never paraphrased. Re-run this whenever the CSV changes:

    python3 _generate.py            # writes components/NN-slug.md
    python3 _generate.py --check    # exit 1 if any file is stale
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# The skill's own copy wins. A `project_docs/` copy outside the skill is only a
# fallback for a checkout that keeps the form elsewhere -- preferring it would
# mean edits to the bundled CSV silently did nothing, and this folder is meant
# to run on its own.
_c = [HERE.parent / "audit-rubric.csv",
      HERE.parents[1] / "project_docs" / "audit-rubric.csv"]
CSV = next((c for c in _c if c.exists()), _c[0])
OUT = HERE / "components"

# --- the one piece of judgement in this file, kept visible and editable ---
# evidence class -> which subagent model runs the component.
#   files  : must open the input / expected files to decide
#   rubric : decided by reading the rubric criteria against the prompt
#   other  : decided by reading the prompt or the verifier JSON
MODEL = {"files": "claude-opus-5",
         "coverage": "claude-opus-5",   # needs the gold + input files
         "rubric": "claude-opus-5",
         "other": "claude-sonnet-5"}

# Components whose fail threshold is a share of the criteria. On a 19-30
# criterion rubric one criterion moves the share by 3-5 points, so a single
# permissive call flips the verdict. These must enumerate every candidate.
PERCENT = {
    "Rubric - Categorization", "Rubric - Content", "Rubric - Self-Containment",
    "Rubric - Overfitting", "Rubric - Atomicity", "Rubric - Objectivity",
}

CLASS = {
    "Task - Feasibility": "other",
    "Task - PII / Safety": "files",
    "Prompt - Clarity": "other",
    "Prompt - Realism": "other",
    "Prompt - GUI Integration": "other",
    "Prompt - Output Naming": "other",
    "Prompt - Timelessness": "other",
    "Component: Prompt - Answer leakage": "files",
    "Gold File - Accuracy": "files",
    "Gold File - Format": "files",
    "Component: Gold File - Input Consistency": "files",
    "Rubric - Categorization": "rubric",
    "Rubric - Hardcoded Values": "rubric",
    "Rubric - Content": "rubric",
    "Rubric - Accuracy": "files",        # claims must be checked against the answer key
    "Rubric - Coverage": "coverage",
    "Rubric - Self-Containment": "rubric",
    "Rubric - Overfitting": "rubric",
    "Rubric - Atomicity": "rubric",
    "Rubric - Objectivity": "rubric",
    "Rubric - Framing": "rubric",
    "Rubric - Redundancy": "rubric",
    "Rubric - Weight Share": "rubric",
    "Rubric - Individual Criteria Weights": "rubric",
    "Rubric - Count": "rubric",
    "Component: Rubric - Robustness": "rubric",
    "Component: Rubric - Value Binding": "rubric",
    "JSON - Structure / URL Integrity": "other",
}

# Which bundle fields / staged paths each evidence class should be pointed at.
EVIDENCE = {
    "files": [
        "`bundle.json` -> `prompt`, `criteria[]`, `input_files[]`, `expected_files[]`",
        "`inputs_extracted.md` — every input file dumped to text",
        "`expected_extracted.md` — every expected (answer-key) file dumped to text",
        "`render/inputs/<filename>/page-NN.png` and "
        "`render/expected/<filename>/page-NN.png` — each non-image file "
        "rasterised page by page: what it LOOKS like, as opposed to what the "
        "extraction says it contains",
        "`render_index.json` — per file: `status`, `visual_verifiable`, "
        "`parity`, `pages`, `unverifiable_reason`. Consult it before making "
        "any claim about appearance",
        "`files/inputs/` and `files/expected/` — the originals, for images",
        "`bundle.json` -> `staged_files` — any value starting `FAILED` did not "
        "download; say so rather than guessing",
    ],
    "coverage": [
        "`bundle.json` -> `prompt`, `criteria[]`",
        "`expected_extracted.md` — the answer key, to see what a criterion "
        "anchored to the expected file actually forces",
        "`inputs_extracted.md` — to expand the prompt's plurals into their "
        "named members",
        "`bundle.json` -> `mechanical` — precomputed; do not recompute",
    ],
    "rubric": [
        "`bundle.json` -> `criteria[]` — each `{n, id, title, weight, category, type}`",
        "`bundle.json` -> `prompt` — for coverage and framing only",
        "`bundle.json` -> `mechanical` — precomputed counts and weight shares; "
        "trust them, do not recompute",
    ],
    "other": [
        "`bundle.json` -> `prompt`, `seed_prompt`, `applications_used`",
        "`bundle.json` -> `input_files[]`, `verifier`, `mechanical`",
        "`bundle.json` -> `agent_issue_details` — often records a real "
        "environment failure",
    ],
}

# --------------------------------------------------------------------- v0.1
# Calibration ported from the deployed reference evals, per the "Improvements"
# and "Other" sections of the merge analysis that produced this skill.
#
# The CSV remains the only authority for WHAT is scored. Nothing here adds an
# answer option, moves a threshold, or invents a band — every entry is guidance
# on how to apply an option the CSV already lists.
#
#   before   -> governs the choice between this component's existing options
#   scores   -> pinned to one existing option, rendered under it
#   minor    -> NEVER scored; rendered into the `minor_issues` output field
#   evidence -> extra sources this component alone may read, appended to the
#               ones its evidence class already carries
#   output   -> extra fields this component alone must return, added to its
#               output contract; scripts/run_review.py requires every one the
#               component file names
#
# Where the reference eval and the CSV genuinely conflict, the CSV wins and the
# rule is omitted here rather than quietly overriding the form.
# Minor entries that satisfy both halves of the bold rule: they are **unscored
# here** — audit-rubric.csv has no answer option for them, so they can only ever
# be a recommendation — and the reference eval treats the same defect as a hard
# FAIL. The only difference is presentation: the report prints the whole bullet
# in bold so a reader scanning a component that scored 5 does not skim past one.
#
# Both halves are required. An entry the reference eval fails but that this form
# *can* score is deliberately absent: format/extension integrity and archive
# integrity already escalate to score 2 on component 10 when the file will not
# open, so bolding the leftover recommendation would double-signal.
#
# Keyed by the entry's lead phrase; `scripts/render_html.py` holds the same set
# and does the bolding.
HARD_GATE = {
    # task- and prompt-level gates the reference eval fails outright
    "Domain fit and expertise level",
    "Thin complexity",
    "Spreadsheet-only deliverables",
    # artifact- and rubric-level, same bar
    "A criterion that tests both correctness and visual properties",
    "Prompt-constrained style not followed",
}


def lead_phrase(entry: str) -> str:
    """The `**...**` phrase a minor entry opens with, or ''."""
    m = re.match(r"\s*\*\*(.+?)\*\*", entry)
    return m.group(1).strip() if m else ""


CALIB: dict[str, dict] = {

    "Task - Feasibility": {
        "before": [
            "Infeasibility is concrete and nameable: software that is not "
            "installed on the VM, a login or credential the agent cannot hold, "
            "a captcha, or a step the VM physically cannot perform. Name which "
            "one, and name the application the task would have needed.",
            "A browser lookup to a **stable public authority** for a historical "
            "fact is ordinary CUA work and is feasible. Do not read it as an "
            "infeasible external dependency.",
        ],
        "scores": {"2": [
            "Quote the step you say cannot run and the capability it needs. "
            "`agent_issue_details` recording a real environment failure is "
            "evidence; your own doubt about difficulty is not.",
        ]},
        "minor": [
            "**Domain fit and expertise level** — the task really tests a "
            "different profession than its `domain` / `sub_domain` claims, or "
            "someone with only basic subdomain knowledge could complete it. Fit "
            "is carried by who is asking and the work context, not by the "
            "deliverable's genre, so do not record this merely because the "
            "output format is unexpected.",
            "**Thin complexity** — the task is retrieval or reorganisation "
            "rather than professional judgment, multi-step execution, cross-file "
            "reasoning, calculation or transformation.",
        ],
    },

    "Task - PII / Safety": {
        "before": [
            "A name is PII only when **paired with sensitive data** — a name "
            "beside a phone number, an address, an SSN, an account or a medical "
            "detail. A standalone name, author or username is not PII, including "
            "in the task's own metadata.",
            "PII can sit in the input and expected files, not only the prompt. "
            "Check `inputs_extracted.md` and `expected_extracted.md` as well.",
            "**Minor PII is score 4 — one band, one value.** The CSV describes "
            "this band three ways: the description says \"a score of 3 "
            "`[Fail - Minor PII Violation]`\", the option is score **4** labelled "
            "`[Non-Fail - Minor PII Violation]`, and `errorCategories` lists "
            "`[All] [All] [Fail - Minor PII Violation]`. "
            "`references/source-conflicts.md` §7 resolves it: the option text "
            "wins, minor PII is **Non-Fail at 4**. There is no score 3 on this "
            "component. Emit the only minor label the form lists — "
            "`[All] [All] [Fail - Minor PII Violation]` — verbatim despite its "
            "wording, and say in `justification` that the band is Non-Fail.",
        ],
        "scores": {
            "2": ["Name the field, the file and the location, and state the "
                  "redaction or synthetic substitute that would remove it."],
            "4": ["Synthetic names, or data that is hard to trace back or "
                  "verify, belong here. Synthetic data is permitted, so say what "
                  "would remove it rather than escalating. This is a **non-fail** "
                  "band despite the label's wording."],
        },
        "minor": [],
    },

    "Prompt - Clarity": {
        "before": [
            "A typo in a **key identifier** — a column name, a filename, a "
            "setting value — changes the interpretation and is a clarity defect. "
            "An ordinary typo whose intent is obvious is not.",
            "A pointer must resolve to exactly one thing. \"page 5 of the "
            "baseline package\" is ambiguous when the printed pagination and the "
            "file's own page index disagree; a trailing \"etc.\" is not a "
            "specification; \"title it `waste_report.docx`\" conflates the "
            "document title with the filename.",
            "Do not score down for ambiguity where a predominant reasonable "
            "reading exists, or where the ambiguous element would not show up as "
            "verifier misalignment.",
        ],
        "scores": {
            "2": ["Reserve for a goal that is genuinely indeterminable. Quote "
                  "the text and state the two readings that would produce "
                  "differently graded artifacts.",
                  "**Solution space**, in its severe form. The CSV opens this "
                  "component with \"the task must be verifiable and objective; "
                  "avoid open-ended queries\", so a prompt establishing a "
                  "solution space for which **no objective rubric of a correct "
                  "answer could be written** takes this option — the goal is "
                  "indeterminable in the sense that matters. Asking for reasoned "
                  "professional opinion is *not* this: an opinion deliverable "
                  "bounded by an explicit decision rule is gradable and scores "
                  "5."],
            "3": ["Solvable with one valid interpretation, but the agent has to "
                  "make a small, reasonable assumption. This is the band for "
                  "genuine but minor ambiguity.",
                  "**Solution space**, in its milder form: the solution space is "
                  "loose enough that two competent submissions would be graded "
                  "differently, but a defensible rubric could still be written. "
                  "Score it here and say what decision rule would bound it.",
                  "**Unnamed input files.** The prompt refers to its inputs only "
                  "obliquely (\"the attached data\"), so the agent must work out "
                  "which file feeds which requirement and a reviewer cannot "
                  "confirm it did. That is a small, reasonable assumption forced "
                  "on the agent, so it lands in this band. The fix is to name "
                  "each input file in the prompt — naming them is correct "
                  "practice and is never a defect under component 04."],
        },
        "minor": [],
    },

    "Prompt - Realism": {
        "before": [
            "**Naming input files is correct practice and is never a defect on "
            "this component.** A prompt that refers to its inputs by name — "
            "\"work from `Q3_returns.xlsx` and the field notes in "
            "`site_survey.pdf`\" — is doing what the project requires: named "
            "inputs are what make a task verifiable and what let a reviewer "
            "confirm the prompt, the files and the rubric describe the same "
            "task. Never read that as robotic, unnatural or templated, and "
            "never count it toward this component at any band.",
            "**The \"robotic file references\" anti-pattern is narrowed to its "
            "mechanical form**: a bare \"extract data from file A and file B\" "
            "instruction carrying no context, no motivation and no working "
            "situation. Filenames *plus* context are not it. The reverse is the "
            "real concern, and it belongs to component 03: a prompt that never "
            "names any input, describing them only as \"the attached data\".",
            "Prescriptiveness is overwhelmingly the middle band. In the observed "
            "defect distribution it carries five warnings and **zero** failures, "
            "so detail alone is score 3 and the fail option stays rare.",
            "Domain fit is carried by who is asking and the work context they "
            "are in, not by the deliverable's genre. An unexpected output genre "
            "is not an unnatural prompt.",
        ],
        "scores": {
            "2": ["Before taking this option, confirm the prompt is genuinely "
                  "rubric-shaped in one of these specific ways: output-by-output "
                  "enumeration, an exact section-title checklist, a step-by-step "
                  "statement of the internal algorithm, or leaked verifier "
                  "logic. Quote the enumeration or checklist you object to."],
            "3": ["More procedural detail than a real user would write, without "
                  "leaking the verifier or overfitting the output. A prompt that "
                  "is merely detailed, or that states necessary constraints, "
                  "lands here."],
        },
        "minor": [],
    },

    "Prompt - GUI Integration": {
        "before": [
            "**Apply the GUI evidence test before scoring.** Do not judge GUI by "
            "vibes or by the presence of a verb like \"open\", \"review\" or "
            "\"check\". Write down two things: **(1) the action** — the specific "
            "thing the agent must do in the interface, quoted from the prompt; "
            "and **(2) the artifact change** — what would look different in the "
            "deliverable if the agent skipped it. Both must be nameable from the "
            "prompt's own words.",
            "Worked contrasts. \"adjust the translated German text so it fits "
            "the text box without overlapping the chart, then preview the "
            "slide\" → action and artifact change both nameable, **meaningful**. "
            "\"use print-preview to make sure the sheet prints on one page\" → "
            "**meaningful**. \"open the workbook and review the data before "
            "summarising\" → no artifact change; the summary is identical either "
            "way. \"keep the existing template's formatting\" → nothing the "
            "agent must observe.",
            "Restraint — a supplied visual reference is **not** minimal GUI. "
            "Where the agent must read a layout out of an image to know what to "
            "produce, and a readability requirement lands on the rendered "
            "output, both are real GUI work with nameable artifact changes.",
        ],
        "scores": {
            "2": ["Take this option only when you **cannot name the artifact "
                  "change** — skipping the interface work would leave the graded "
                  "output identical. State the action you found and the artifact "
                  "change you could not."],
            "3": ["You can name both the action and the artifact change, but the "
                  "change is cosmetic or only loosely tied to the deliverable. "
                  "Report it rather than escalating: the observed problem on this "
                  "component is this band going **unreported**, not the fail "
                  "option being too loose."],
        },
        "minor": [],
    },

    "Prompt - Output Naming": {
        "before": [
            "Trust `mechanical.06_prompt_output_naming`: `unnamed_outputs` and "
            "`states_desktop` are computed from the verifier's `result[].dest` "
            "against the prompt text. Do not re-derive them.",
            "Match by evident correspondence, not string equality. A difference "
            "in naming style between the prompt and the recorded path — spaces "
            "vs underscores, a dropped extension, a truncated or "
            "system-generated name — is not a missing filename.",
        ],
        "scores": {"2": [
            "Quote the output the prompt fails to name, or show that the Desktop "
            "save location is absent.",
        ]},
        "minor": [
            "**Filename present but awkward** — phrased oddly, or slightly "
            "inconsistent with the expected-file name, but still resolvable. The "
            "prompt names the output and states the Desktop location, so the CSV "
            "scores this a clean 5; record it as a warning with the suggested "
            "rewording. It **does not affect the score**.",
            "**Off-list deliverable extension** — e.g. `.jpg` where `.png` is "
            "the norm for a diagram export. Blender work delivering a `.blend` "
            "is correct, not off-list.",
            "**Spreadsheet-only deliverables** — the prompt requires only "
            "`.xlsx` / `.csv` outputs.",
        ],
    },

    "Prompt - Timelessness": {
        "before": [
            "Mild time framing over static inputs is the middle band, not the "
            "fail option. \"It is March 2026 … the current cycle\" does not "
            "change the correct answer when that answer derives from the "
            "attached files.",
        ],
        "scores": {"2": [
            "Reserve for a correct solution that genuinely varies with time — "
            "live prices, real-time scores, current weather, live inventory, an "
            "\"as of today\" page — or a time-sensitive count framed as "
            "trajectory confirmation. An unpinned arXiv reference is "
            "time-dependent because the paper it resolves to can change; a "
            "version-pinned one is not.",
        ]},
        "minor": [],
    },

    "Component: Prompt - Answer leakage": {
        "before": [
            "Check this on every prompt. Leakage is among the most common prompt "
            "defects and the one most often missed — ask directly whether the "
            "agent could lift a graded value, the conclusion, or a required "
            "sentence straight out of the prompt and earn credit without doing "
            "the work.",
            "Decide against what is actually graded. Read `expected_extracted.md` "
            "and `criteria[]` first: leakage is defined by what the scored "
            "criteria look for, not by whatever the prompt happens to restate.",
        ],
        "scores": {"3": [
            "One or two secondary facts restated, with the core graded "
            "deliverable still requiring work the prompt does not contain.",
        ]},
        "minor": [],
    },

    "Gold File - Accuracy": {
        "before": [
            "**Enumerate the prompt's discrete asks before opening anything.** "
            "An ask is one thing the contributor was told to do: produce a named "
            "file, include a named section, apply a stated constraint, order "
            "something a stated way. Split compound sentences — \"add a "
            "scorecard and a grounding note\" is two asks. Mark each MET (name "
            "the exact location), MISSING (quote the prompt text and say what is "
            "there instead) or UNVERIFIABLE (say why), and report the totals.",
            "**A universal ask is not met by a sample.** Where the prompt says "
            "*every / all / each*, build the set, check every member and report "
            "the count — \"12 of 19 figures carry a trace entry; the 7 without "
            "are …\". Derived values are where this breaks: a register cites the "
            "figures lifted straight off a page and silently omits the ratios "
            "and aggregates the author computed. Partial satisfaction is MISSING.",
            "**Recompute; do not eyeball.** Totals against their own components, "
            "percentages against a consistent base, derived columns against their "
            "stated formula, ranks and ordinals. State both numbers: what the "
            "file says and what you get.",
            "**Values the package cannot produce.** Where the expected set "
            "contains a generating artifact — a script, notebook or macro — "
            "enumerate the literal values it can emit, then check every generated "
            "file against that set. A cell holding a value outside it is a defect "
            "however sensible the word reads in isolation, and the fix must be a "
            "value the artifact can actually emit; prescribing a fourth status a "
            "three-status script cannot write relocates the defect instead of "
            "resolving it.",
            "**Hold the answer key's own method statements to what it actually "
            "did.** A \"methodology\", \"assumptions\", \"thresholds used here\" "
            "or \"limitations\" note is a claim about the file it sits in, and it "
            "is checkable: read the stated rule, apply it yourself, and compare "
            "with the numbers the file carries. Two shapes recur. The stated rule "
            "**drives nothing** — the note quotes a `> 200` diagnostic cutoff "
            "while every figure in the file comes from age-band prevalence. And "
            "the stated rule **contradicts the file's own results** — applying it "
            "would yield a different answer, sometimes an empty one, than the "
            "file reports. Both are wrong statements inside the answer key, "
            "independent of whether the figures themselves are right, and they "
            "mislead every agent that reads the note as instruction. Quote the "
            "note, state the result under the stated rule, state the result the "
            "file reports, and name the method actually used. A note that "
            "honestly records a limitation is not this — the defect is claiming a "
            "rule was applied when it was not.",
            "**Size is not severity.** A one-word defect can be a fail and a "
            "whole-chart defect a non-fail. The question is whether the graded "
            "value is reachable.",
            "**Write out the fix before reporting the finding.** If the only "
            "available fix is a font, colour, spacing, layout, extra-sheet, "
            "rounding, grammar or methodology change the prompt never "
            "constrained, the fix is illegal — so the finding is wrong. Drop it.",
            "Before marking anything MISSING, search the whole expected set: "
            "content asked for in one file is often legitimately delivered in "
            "another. An ask the prompt leaves open is MET if the file satisfies "
            "any reasonable reading.",
        ],
        "scores": {
            "2": ["A **primary** ask MISSING — a required deliverable, a core "
                  "piece of the requested work, or a stated hard constraint — or "
                  "a graded value that is wrong or unreachable.",
                  "**The wrong-file case.** An expected file that is the "
                  "genuinely untouched starter is not an answer key at all, so "
                  "it is \"wrong/missing data\" in this option's own terms. "
                  "Establish direction first: `manifest`/`bundle` marking a "
                  "shared checksum says the bytes match, not which way the copy "
                  "went. If the file is a completed deliverable that was *also* "
                  "staged onto the VM as a starter, the defect is in the "
                  "initializer and this does not fire.",
                  "**Cross-file contradiction**, where the figure is graded. The "
                  "same value quoted in two deliverables cannot disagree and "
                  "both be right, so at least one holds wrong data and no "
                  "correct agent can match both."],
            "3": ["A **secondary** ask MISSING, or content substantively correct "
                  "carrying a minor non-scoring format deviation.",
                  "**Cross-file contradiction**, where the figure is incidental "
                  "prose rather than a graded value. Report it with both "
                  "locations and say which one you believe is wrong."],
        },
        "minor": [
            "**Close calls.** If you seriously considered reporting something and "
            "talked yourself out of it, record it here: state both readings, "
            "which you applied, and the count on each side. Deciding not to flag "
            "is a decision worth recording.",
            "**Your denominator** — how many expected files exist, how many you "
            "opened, how many you flagged.",
        ],
    },

    "Gold File - Format": {
        "before": [
            "This component's fail option names exactly three conditions: a "
            "format outside the 24-application list, a single expected file "
            "shared across operating systems where a per-OS file is required, "
            "and a ground-truth URL pointing at the starting file instead of the "
            "answer key. Score against those and nothing else — failing here for "
            "a reason the option does not name is a tool defect this component "
            "has already been corrected for once.",
            "Trust `mechanical.10_gold_file_format`: `gt_url_points_at_input`, "
            "`expected_exts` and `os_enabled` are precomputed. Treat Ubuntu-only "
            "as correct unless the task metadata enables another OS.",
            "Never fail a format the upload widget blocked — the contributor had "
            "no compliant path. See `references/source-conflicts.md`.",
            "**Structural damage scores only when it stops the task.** The "
            "suggestions listed under `minor_issues` are not scored — except "
            "where the damage leaves the expected file **unopenable**: a corrupt "
            "archive, or bytes that are not the declared format at all. Such a "
            "file is not one the 24 permitted applications can generate or open, "
            "which is this component's fail option read literally, so take score "
            "2 and say which application cannot open it. Everything short of "
            "that — residue, mojibake, inconsistent typography, an unfollowed "
            "style instruction — is a suggestion and leaves the score at 5.",
        ],
        "minor": [
            "**Format / extension integrity** — bytes that do not match the "
            "extension: an `.xlsx` that is not a zip, a `.pdf` that is not a PDF.",
            "**Archive integrity** — a corrupt or unopenable archive. "
            "`__MACOSX/` and `.DS_Store` are macOS metadata and never a defect.",
            "**Placeholder or draft residue** — `TODO`, `TBD`, `FIXME`, "
            "`Lorem ipsum`, `XXX`, `<placeholder>`, template instruction text "
            "left in place, an obviously unfilled field.",
            "**Mojibake and encoding damage** — `â€™`, `Ã©`, replacement "
            "characters.",
            "**Self-inconsistent typography** — a mid-document typeface or size "
            "change with no structural reason, heading levels that skip or "
            "invert, mixed number formats in one column (`1,000` beside `1000`), "
            "mixed date formats in one table, inconsistent currency or unit "
            "symbols for the same quantity, straight and curly quotes mixed in "
            "one run of prose. The test is whether you can point at **two places "
            "in the same deliverable that contradict each other**. An "
            "unconstrained *choice* applied consistently is never a defect.",
            "**Prompt-constrained style not followed** — a stated language "
            "variant (\"write everything in British English\"), a named font or "
            "template, a stated date / number / currency format, or a stated "
            "capitalisation convention. Quote the prompt text and check it "
            "across every deliverable, not just the first.",
            "Appearance claims come from the rendered pages under `render/`, "
            "never from extracted text — look at them before calling anything "
            "here a defect. A file `render_index.json` reports as not visually "
            "verifiable is **not** a defect: set `blocked_on` and lower "
            "`confidence`.",
        ],
    },

    "Component: Gold File - Input Consistency": {
        "before": [
            "**Four conditions must all hold** before taking the fail option: "
            "the value is *graded* (part of what the deliverable is scored on, "
            "not incidental prose); it is absent from the prompt; no input file "
            "contains it or makes it derivable; and no defensible derivation "
            "from the inputs reaches it. A value reachable from a stable "
            "external source the prompt explicitly points to is traceable.",
            "**Name each place you looked and what you found there** — \"checked "
            "`field_profile_raw.csv` (no `settlement_date` column), "
            "`fund_db_schema.sql` (column exists, no values), and the prompt "
            "(silent)\". *\"I could not immediately find it\"* is not that.",
            "Where to look hardest: **joins and merges** whose record count does "
            "not match what the inputs actually produce; **looked-up constants** "
            "present in no supplied input; and **swapped inputs** — IDs, date "
            "ranges, record counts or entity names that do not correspond to the "
            "supplied set, which usually means the file was built against an "
            "earlier input set and never rebuilt, and usually breaks more than "
            "one thing.",
            "**Quotation fidelity.** Text presented as a quotation — in quote "
            "marks, as a block quote, or introduced as what a source says — must "
            "appear in the named source character-for-character. A reworded "
            "paraphrase presented as a quotation is a defect, as are two "
            "non-adjacent spans joined as continuous with no ellipsis. "
            "Normalisation that does not change wording is fine: line wrapping, "
            "whitespace, smart vs straight quotes, a marked ellipsis, bracketed "
            "editorial insertions. Unquoted prose that summarises a source is "
            "**not** this defect.",
            "**Locators.** A page, section or clause reference must resolve to "
            "that material in the named source. A three-page source cannot carry "
            "a citation to page 5.",
            "**Collect every statement of the same rule before checking any "
            "value.** A threshold, cutoff, eligibility rule, formula, mapping or "
            "definition is routinely stated in more than one place: a "
            "methodology or briefing PDF, a `Reference`, `Notes` or `Glossary` "
            "sheet inside a supplied workbook, the prompt itself, and the answer "
            "key's own method note. Find all of them and write each out verbatim "
            "with its location before deciding anything. Three failure shapes, "
            "each of which stops a correct agent reproducing the answer key. "
            "**(i) Two inputs state different rules for the same quantity** — a "
            "PDF selecting on `BMI > 29.9 and glucose > 127.5` while the "
            "dataset's own reference sheet defines diabetic as `> 200` and obese "
            "as `> 30`. **(ii) The answer key applies neither** — it takes the "
            "whole population, or a third rule it never names, so no agent "
            "following any supplied rule lands on the gold. **(iii) A supplied "
            "rule cannot be applied to the supplied data** — it selects an empty "
            "set, or contradicts a label the data already carries. Test it: sort "
            "the column and compare against the cutoff. A `> 200` diabetic "
            "threshold on a glucose column whose maximum is `199`, in a file "
            "whose outcome column already marks 268 positive rows, is "
            "unusable and self-contradictory at once. Report which rule the gold "
            "actually used and whether any supplied input states it. An agent "
            "cannot pick the intended rule by luck, so this is an input "
            "consistency defect even when every individual figure is arithmetically "
            "sound.",
            "A different-but-defensible method reaching a different valid answer "
            "is never an input-consistency defect, and a quotation whose source "
            "file could not be fetched is unverifiable rather than wrong. Two "
            "supplied rules that genuinely conflict are the opposite case: there "
            "the agent's choice is not defensible-either-way, because only one "
            "of them reproduces the answer key.",
        ],
        "scores": {
            "2": ["**Input sufficiency is this option.** Where a datum the "
                  "prompt quotes, a criterion grades, or an expected file "
                  "contains is carried by **no** input file — absent, truncated, "
                  "illegible, corrupt or empty — a correct agent working from "
                  "the inputs cannot match the answer key, which is exactly what "
                  "this option describes. Name the input file, the absence mode "
                  "(`absent` / `truncated` / `illegible` / `corrupt` / `empty`), "
                  "the datum, and what relies on it. **The fix is to the input "
                  "file**, not to the rubric or the expected file — say so, "
                  "because the natural repair is to infer the value, and that "
                  "silently ships a broken task.",
                  "Three things are **not** this, and a false positive here "
                  "stops a healthy task: a datum stated in full **elsewhere** in "
                  "the inputs is present, even where the place the task points "
                  "at is damaged; a datum the task asks the agent to **compute** "
                  "from the inputs is present; and a file you merely could not "
                  "open is a tooling gap for `blocked_on`, not a missing input.",
                  "**A rule conflict the answer key resolves silently is this "
                  "option.** Where the inputs state two different rules for the "
                  "same selection or calculation and the gold follows neither — "
                  "or follows one without saying which — the gold's figures do "
                  "not derive from the inputs an agent can act on, which is this "
                  "option in its own words. Quote all the competing rules with "
                  "their locations, state the rule the gold actually used, and "
                  "say the fix is to make the inputs agree, not to loosen the "
                  "rubric."],
            "3": ["One or two secondary values not directly traceable while the "
                  "core deliverable derives correctly. This band exists — use it "
                  "rather than escalating.",
                  "An input-sufficiency gap on a **secondary** datum lands here "
                  "too. Still name the input file and the fix.",
                  "A rule conflict that moves only an incidental figure, where "
                  "the graded deliverable derives correctly under every supplied "
                  "reading, lands here rather than on the fail option."],
        },
        "minor": [
            "**A cited filename that does not match a supplied input, "
            "character for character.** Answer keys drift in both directions: a "
            "browser artifact the input does not carry (`Airline Dataset(1).csv` "
            "cited for `Airline Dataset.csv`), and a silently *corrected* "
            "misspelling (`Diabetes Dataset.xlsx` cited for an input actually "
            "named `Daibetes Dataset.xlsx`). The correction is the more "
            "misleading of the two because it reads as right while naming a file "
            "that is not in the task. Compare every cited name against "
            "`input_files[]` byte for byte. This does not make a value "
            "untraceable, so it stays here unless a graded criterion depends on "
            "the cited string.",
        ],
    },

    "Rubric - Categorization": {
        "before": [
            "**Category definitions.** `format_gate`: the required file was "
            "produced, or has the required file / organisational shape — "
            "filenames, file types and extensions, page count, slide count, word "
            "count, document length, folder and ZIP structure, and which "
            "worksheets a workbook contains. `correctness`: the agent got the "
            "content right — computed values, transformations, reasoning, "
            "classifications, recommendations, conclusions, heading names, "
            "column names, chart data values. `visual`: the output looks right — "
            "chart rendering, axes, scales, legibility, layout, typography, "
            "style, slide presentation, document section / page / template "
            "structure, and ordering where reasoning is not involved.",
            "**Disambiguation, most-missed first.** A *value* inside a visual "
            "element is `correctness` — the axis label text, the KPI number on a "
            "tile, the figure in a callout, the total in a rendered table; only "
            "its rendering, spacing and legibility are `visual`. Display rounding "
            "is `visual`, computational precision is `correctness`. Chart "
            "rendering is `visual`, chart plotted values are `correctness`. "
            "Folder, ZIP and worksheet arrangement is `format_gate`; document "
            "layout *within* a file is `visual`. Named column headers and "
            "heading names are `correctness` — the names are content even though "
            "they sit in a layout. A conclusion the agent drew by inspecting a "
            "supplied image is `correctness`; the word \"visual\" appearing in "
            "the criterion text is not the signal.",
            "**Ordering** is `visual` by default and `correctness` only when the "
            "order is itself the output of a reasoning step. The test: could the "
            "agent produce the required order without doing any of the task's "
            "analysis? \"in the order China, USA, India\" → handed down, "
            "`visual`. \"in ascending order of 2025 GDP per capita\" → derived, "
            "`correctness`.",
            "**Being mandated by the prompt does not decide the category.** A "
            "property the prompt required is still `visual` if what it tests is "
            "a rendering property.",
            "**Group same-shape criteria and judge them as a unit.** "
            "Miscategorisations come in pairs and triples, because a contributor "
            "writes one criterion and copies it to its siblings and the copies "
            "inherit the category. Catching one of a pair and leaving its twin "
            "makes the survivor read as a deliberate choice.",
            "**Your own uncertainty is not a miscategorisation.** Where the rules "
            "above do not settle a call, leave the criterion as filed and do not "
            "count it toward the share.",
            "**Not defects, all three confirmed over-flags.** Page, slide and "
            "word counts **are** `format_gate` and **are** `REGULAR`. An "
            "unordered set of required topic areas is `correctness` — \"numbered "
            "sections\" is not automatically document structure; an *ordered* "
            "section skeleton is `visual`. Which worksheets a workbook contains "
            "is `format_gate`, not `visual`.",
        ],
        "scores": {
            "2": ["**Gating impact takes this option on its own, whatever the "
                  "share.** `MUST-PASS` assigned to a criterion that is not a "
                  "file-existence or file-type/extension gate — including one "
                  "that bundles such a check in alongside the gate — silently "
                  "gates the whole task on formatting, so it fails here even "
                  "when the misfiled share is under the threshold. The mirror "
                  "case, a genuine file gate left `REGULAR`, has no gating "
                  "impact and belongs in the band below. Component 24 scores the "
                  "same tag under the weighting protocol; both readings stand, "
                  "and each scores its own question."],
            "3": ["Under the threshold and with no gating impact — an isolated "
                  "category or type slip. Every criterion in this band must "
                  "still be named, with the pair it currently carries and the "
                  "pair it should."],
        },
        "minor": [
            "**A criterion that tests both correctness and visual properties**, "
            "so that no single filing is correct for it — a presentation wrapper "
            "carrying a required content list, for example. The fix is a split, "
            "not a refiling: name **both** target `criteria_category` / "
            "`criteria_type` pairs.",
        ],
    },

    "Rubric - Hardcoded Values": {
        "before": [
            "**The strip-the-anchor test.** Delete the expected-file anchor from "
            "the criterion and read what remains. If the remaining text still "
            "tells a reader the answer, it is a hardcoded value. This is the "
            "operational form of the rule and the fastest way to settle a "
            "disputed criterion.",
            "**An expected-file clause does not cure a restated literal.** \"The "
            "Status value for every scenario **is PASS**, consistent with the "
            "expected file\" is still hardcoded — strip the anchor and the answer "
            "is still there.",
            "Two further shapes that fail the same test: a criterion that "
            "supplies the two issues the prompt asked the agent to *find*, and "
            "one that pre-announces the mechanism the agent had to extract from "
            "the source.",
            "The count is **absolute, not a share**, and it decides the band — so "
            "having found one, sweep the rubric for the same construction before "
            "you score. The difference between the two bands is whether its twin "
            "exists, not how badly this one reads.",
        ],
        "minor": [
            "**Comparison mode not stated.** A criterion should say how the "
            "comparison is made: a numeric tolerance (±1 / 3 / 5%), semantic "
            "equivalence for prose, structural comparability for visuals, or "
            "defensible alternatives for open-ended methods. Omitting one where "
            "a comparison clearly needs it is a warning with the suggested "
            "wording, and **does not affect the score**. The one exception is "
            "already scored: where the criterion omits a comparison mode "
            "*because* it states the literal answer instead, that is a hardcoded "
            "value and it counts toward this component's bands.",
        ],
    },

    "Rubric - Content": {
        "before": [
            "**Count the denominator before the numerator.** This threshold is a "
            "share of the **correctness criteria only** — an existence-only "
            "*visual* criterion or format gate belongs in neither the numerator "
            "nor the denominator. Worked count: with 12 correctness criteria, "
            "15% is 1.8, so 2 or more takes the fail option.",
            "**Existence-only** means the criterion checks that something is "
            "merely present — a header, page numbers, a section, a title — "
            "without checking that its content is correct.",
            "A correctness criterion must cover all enumerable entries in the "
            "answer key, not a spot-check: \"all 44 classifications\", not 7 of "
            "44.",
            "\"Similar to / semantically comparable to the expected file\" is an "
            "acceptable content anchor. It is neither existence-only nor "
            "subjective.",
        ],
        "minor": [],
    },

    "Rubric - Accuracy": {
        "before": [
            "The question is narrow: is what **the criterion itself** asserts "
            "objectively false? A false statement that lives in the expected "
            "file, with the criterion merely anchored to it, is not this "
            "component's finding.",
            "Flag only on affirmative evidence. The recognised shapes are: naming "
            "a file or artifact that is not present when the criterion requires "
            "it; stating a numeric value, formula, section, relationship or "
            "source claim that the prompt or the inspected files contradict; "
            "asserting a condition the prompt or source expressly contradicts; "
            "claiming a cited source confirms a conclusion it does not establish; "
            "and **combining requirements in a logically inconsistent way** — two "
            "tolerances derived from the same quantity that cannot both be "
            "satisfied, so the rubric cannot be met as written.",
            "**Explicitly not judged here:** incomplete, overfit, redundant, "
            "subjective, existence-only, poorly categorised, or merely difficult "
            "to verify. Other components own each of those.",
            "**Unverifiable is not inaccurate.** If a file could not be opened, "
            "or the prompt does not establish the fact, set `blocked_on` — never "
            "convert an inaccessible file into an accuracy failure.",
            "**When artifacts disagree, find the outlier before prescribing the "
            "fix.** Where the criteria, the verifier paths and both expected "
            "files use one filename and the prompt uses another, the prompt is "
            "the outlier; a criterion is not inaccurate for agreeing with the "
            "majority, and a fix that breaks five artifacts to accommodate one is "
            "the wrong fix.",
            "**The correction must be a true statement about the actual "
            "material.** If you cannot state the corrected claim, you have not "
            "established that the original is false.",
            "Having found one, sweep the rest: a criterion's defect is usually "
            "copied — a mirrored criterion, the same check repeated per artifact, "
            "the same tolerance reused.",
        ],
        "minor": [],
    },

    "Rubric - Coverage": {
        "before": [
            "**Archetypes that repeatedly go uncovered.** A schema or header "
            "criterion never covers the **values** under it — a table of "
            "correctly named columns full of zeros passes it. A compound "
            "deliverable needs one criterion per named member (\"the fluid **and "
            "temperature** profiles\"). A count hard-coded where a cutoff or "
            "tie-break rule makes the answer size a property of the *data* leaves "
            "the tie rule untested. For a GUI, HTML or application deliverable, a "
            "criterion on a control's *appearance* plus criteria on each view's "
            "*contents* still leaves the control's **effect** untested. An "
            "aggregate-under-tolerance criterion (`within ±1%`) does not cover "
            "the **completeness** of the enumeration feeding it — ask whether a "
            "whole category, subtype or line item could be dropped and still land "
            "inside the band. And a named opening or closing element (\"open with "
            "the headline numbers\") states a *position*, not just a topic.",
            "**Expand a shared requirement into its full entity x element "
            "grid.** One sentence naming two entities and several elements — "
            "\"for fund A and fund B, show how much came from own revenue versus "
            "bond proceeds and transfers\" — is one ask per cell, not one ask. "
            "Write the grid out and tick each cell against a criterion. The "
            "usual shape of the gap is a rubric that grades the grid in full for "
            "the entity the author found interesting and grades one bundled "
            "criterion for its neighbour, so a whole row goes untested. A "
            "criterion that names the neighbour is not coverage of the "
            "neighbour's elements; read what it actually lists.",
            "**A chart criterion on contents leaves how the chart is drawn "
            "ungraded.** Title, axis labels, series names, categories and value "
            "labels are the chart's *contents*. Its *construction* — a baseline "
            "that does not start at zero, a truncated or clipped axis range, a "
            "distorted aspect ratio, a scale that misstates the comparison the "
            "prompt asked the chart to make — is a separate ask, and \"legible "
            "and clearly labeled\" does not reach it. A chart whose bars "
            "misrepresent the comparison while every label is correct passes "
            "every contents criterion, so ask explicitly whether a misleading "
            "but correctly labelled chart would be caught.",
            "**A purpose clause is an ask.** \"...so the figures can be checked "
            "directly\", \"...so a reader can follow the calculation\", "
            "\"...so the committee can see where each number came from\" state a "
            "property the deliverable must have — live formulas rather than "
            "pasted constants, intermediate steps shown, each figure carrying "
            "its source — and a rubric that grades only the final values leaves "
            "it untested. Treat the clause as its own ask, name the observable "
            "property it demands, and check whether a deliverable holding the "
            "right numbers as opaque hard-coded constants would pass.",
            "**Never a coverage gap, however the prompt phrases it:** where "
            "output files are saved (enforced by the verifier's `result.path`, "
            "not by the rubric); output filenames and extensions beyond the one "
            "format gate the rubric already carries; and which application or "
            "method the agent used, unless the tool itself is the deliverable.",
            "**Restraint.** A clearly aggregated criterion covers every instance "
            "— \"each slide …\", \"every classification …\" — so do not demand "
            "one criterion per artifact where an aggregate already reads clearly. "
            "Sweep the whole rubric before calling a schema gap: a values "
            "criterion several rows away, worded differently, still covers the "
            "request. Redundancy is not a coverage gap — two criteria testing the "
            "same request means it is covered, twice.",
            "**The criterion you would add must itself be legal:** one element, "
            "one category, no restated answer, no conditional wording, and not "
            "already present elsewhere under different words. A proposed criterion that hands the "
            "contributor the finding the agent was meant to reach is not a fix.",
        ],
        "scores": {"3": [
            "An uncovered **secondary or implicit** request. Name the request and "
            "the artifact and say explicitly that it is secondary.",
        ]},
        "minor": [],
    },

    "Rubric - Self-Containment": {
        "before": [
            "**Self-containment is an observability test:** can the grader see "
            "**both sides** of the comparison? Any criterion grading the **prior "
            "state** of supplied material — \"the already existing X\", \"the "
            "existing Y\", \"the original Z\", \"unchanged from the starter\", "
            "\"reuses the provided …\" — fails, because the grader never sees the "
            "starting files and so cannot distinguish *reused* from "
            "*re-created*. An expected-file anchor does not cure this.",
            "**The second archetype: verifying accuracy against a source the "
            "grader does not have.** \"Each figure carries a citation naming a "
            "statement or clause, **and that figure comes from the named "
            "statement**\" — presence and specificity of the citation are "
            "gradable; accuracy against the unavailable source filing is not. The "
            "fix is to keep the observable half and drop the other.",
            "**Cross-file consistency criteria are exempt and must not be "
            "counted.** \"The total in the summary table matches the total in the "
            "detail table\", \"`Report.pptx` uses the same background colour as "
            "`Metrics.pptx`\", \"each complaint shown on a theme slide is "
            "assigned to that same theme in `complaints.csv`\" — both sides are "
            "already in front of the grader, so an expected-file anchor would add "
            "nothing.",
        ],
        "minor": [],
    },

    "Rubric - Overfitting": {
        "before": [
            "**Check the requirement's source before flagging.** A detail is "
            "overfit only when it is left open by the prompt **and** prescribed "
            "by no input file. The prompt plus the input files together are the "
            "decisive input, and every finding must be checked against both.",
            "A detail is an explicit requirement — and the criterion is **not** "
            "overfit — when it is: a section, heading, field or bracketed "
            "placeholder instruction contained in a supplied **template**; a "
            "calculation, formula, methodology or convention prescribed by a "
            "supplied **methodology, specification or runbook**; a column name, "
            "key, unit or structure fixed by a supplied **schema, data file or "
            "code file**; a visual convention fixed by a supplied **style "
            "reference**; or a specific value, date, rounding rule or prescribed "
            "field value stated in a supplied **SLA or briefing**. Each of these "
            "has been flagged as overfit and each flag was overturned.",
            "**Archetypes, once the source check comes back empty.** The "
            "*mirrored criterion* — the same constraint correctly grounded on one "
            "entity and invented on its neighbour, the single most reliable "
            "signal. *Placement is not cardinality* — apply the negation test to "
            "every \"exactly N\", \"only\", \"no additional\" and \"and nothing "
            "else\": does the prompt or an input actually forbid the extra thing? "
            "*A display form mandated where any form works* — the prompt named "
            "the content, not whether it is a table. *Semantic equivalence "
            "demanded on an element the prompt left open.* *A visual anchor "
            "governing a stylistic choice* rather than a legibility judgment.",
            "**Rounding imported from the answer key.** Open the expected file "
            "and read what a graded cell **stores**, not what it displays. Where "
            "the answer key stores a rounded derived value — a coverage share "
            "held as `0.303`, a rate held as `0.9031` — and the criterion says "
            "only \"matches the corresponding expected file\", the gold's "
            "rounding becomes the requirement: a response holding the exact "
            "quotient is marked wrong, and the exact quotient is usually the "
            "number the gold itself carried forward into its own downstream "
            "figures. That is a display artifact promoted to a graded "
            "constraint, and it is overfitting whether or not the author "
            "intended it. Quote the stored value and the exact value, and "
            "prescribe either a tolerance or an explicit rounding instruction. "
            "Screen every criterion whose graded value is *computed* rather than "
            "copied; a bare \"match\" is safe only on a value with one exact "
            "representation.",
            "**An anchor on an absence.** A criterion phrased as an exclusion — "
            "\"excludes the transfer in and lapsed encumbrances\", \"omits the "
            "prior-year column\", \"does not count X\" — that is then anchored "
            "with \"matching the corresponding expected file\" stops grading the "
            "exclusion and starts grading the gold's **depiction** of it: a "
            "reconciliation line, a struck row, a footnote naming what was left "
            "out. A response that simply never counted the excluded items, which "
            "is the behaviour the prompt asked for, has nothing to match and "
            "fails. Grade the consequence — the resulting figure, computed "
            "without the excluded items — not the display of the omission. "
            "Beware of reading such a criterion as a *guard*: an exclusion "
            "anchored to a file is a form requirement wearing a guard's clothes.",
            "**Restraint.** Anchoring a legibility or containment judgment to the "
            "expected file is sound construction, not overfitting. An inherited "
            "public API in a supplied codebase is a preserved interface, not a "
            "mandated construct. Grading a *function* without prescribing a "
            "heading, wording or position is not dictating a form. And a "
            "requirement the supplied **data** makes unavoidable is not overfit — "
            "ask whether a *correct* answer could omit it; if it could not, the "
            "criterion stands.",
            "Count criteria, not phrases: a criterion with several overfitting "
            "issues counts once. When uncertain, leave it unflagged. Whether a "
            "criterion restates a literal answer is a hardcoded-values question "
            "and belongs to component 13, not here.",
        ],
        "minor": [
            "**A loosening must be bounded by the observable outcome.** A "
            "permission clause that shelters genuinely wrong answers is a worse "
            "defect than the overfitting it cures. Write the clause you would "
            "prescribe, then ask what a wrong answer could now slip past it — "
            "\"any implementation that renders as a constant line at the same "
            "value across the full date range\" is bounded; \"citing other "
            "provisions does not detract\" is not.",
            "**Never recommend spreading an existing tolerance band across the "
            "rubric.** Uneven bands are not in themselves a defect, and \"these "
            "six criteria carry `±1%` and those six do not\" is not a finding. "
            "Before proposing a band anywhere, classify the value: *transcribed* "
            "(copied off a supplied page, cell or table, so exactly one answer "
            "is right) or *derived* (computed, so rounding and step order "
            "legitimately move the last digits). A band belongs only on a "
            "derived value. On a transcribed one it admits a wrong number and is "
            "itself the defect — which component 27 scores, not this one. If you "
            "record a tolerance observation here at all, state the "
            "classification and what the band is worth in the value's own units.",
        ],
        "evidence": [
            "`expected_extracted.md` — required for the rounding check: a "
            "criterion that says \"matches the corresponding expected file\" "
            "inherits whatever the answer key stores, so you cannot judge it "
            "without reading the stored values",
            "`inputs_extracted.md` — required for the source check: a detail is "
            "overfit only when no supplied template, schema, methodology or data "
            "file already prescribes it",
        ],
    },

    "Rubric - Atomicity": {
        "before": [
            "**The surface rule.** A legibility, containment or no-clipping "
            "criterion scoped to **one surface** — a slide, a page, a sheet, an "
            "image — is atomic, even when that surface holds several content "
            "blocks. \"The field mapping table and ingestion rules in "
            "`deck.pptx` are fully legible and well-spaced\" is one judgment "
            "about one slide.",
            "Do **not** count a criterion for bundling several correctness "
            "requirements about **one** element — one table, one column, one "
            "chart. A table containing many items is correctly covered by a "
            "single criterion assessing the whole table by aggregation.",
            "A formatting attribute the prompt explicitly requires **of the same "
            "element** stays atomic: \"the memo closes with a **bolded** "
            "one-sentence recommendation matching the expected file\" is one "
            "element and one requirement, expressed with its required "
            "presentation.",
            "Non-atomic is: a criterion **mixing categories** (a correctness "
            "check bundled with a visual one), or one spanning **different "
            "files**.",
            "**Count each criterion once.** A single disputed criterion is one "
            "defect — never charge it toward this share and another component's "
            "bar off the same observation.",
            "**State the fix and check it does not break something else.** If "
            "splitting a criterion would push the rubric past 30 criteria and "
            "trip component 25, the split is not the required remedy and the "
            "original is not the defect you thought it was.",
        ],
        "minor": [],
    },

    "Rubric - Objectivity": {
        "before": [
            "The denominator is the **non-visual criteria only**, since visual "
            "criteria are expressly permitted subjective phrasing. Worked count: "
            "with 20 non-visual criteria, 10% is exactly 2, so 3 or more takes "
            "the fail option.",
            "Permitted and **not** subjective: \"professionally comparable / "
            "appropriate\" on a visual criterion, and \"similar to / semantically "
            "comparable to the expected file\" on a correctness criterion.",
        ],
        "minor": [
            "**Criterion hygiene** — malformed markup (a filename with a missing "
            "opening backtick, a mismatched delimiter, a rubric where no filename "
            "is backticked at all), missing terminal punctuation, a doubled space, "
            "a stray character left from an edit, or ungrammatical wording that "
            "survived a rewrite. These cost nothing to fix and distort no "
            "grading, so they **do not affect the score**. Record them as **one "
            "grouped entry** naming the criteria affected, not one entry per "
            "criterion. The exception is already scored: where the wording is so "
            "broken that the criterion cannot be graded as written, it is no "
            "longer hygiene — it is not objectively evaluable, and it counts "
            "toward this component's bands.",
            "**Conditional wording** — a criterion whose requirement holds only "
            "in some case: \"if …\", \"unless …\", \"where applicable\", \"when "
            "present\", \"if any\", \"depending on …\". The grader must settle the "
            "condition before it can grade, often from input files it never "
            "sees, and a response that avoids the case passes without doing the "
            "work. The task's inputs and expected file already fix which case "
            "holds, so the fix grades that case's outcome against the expected "
            "file: \"If the starting total includes the transfers, it subtracts "
            "them\" becomes \"The adjusted total in `report.xlsx` matches the "
            "corresponding value in the expected file within ±1%\". A condition "
            "copied from the prompt resolves the same way. Record every "
            "conditional criterion in **one grouped entry**, quoting each "
            "condition; this **does not affect the score**.",
        ],
    },

    "Rubric - Framing": {
        "before": [
            "**Judge the criterion's main requirement**, not incidental wording, "
            "and count each offending criterion once. A criterion is positively "
            "framed when it states what the output does, includes, provides, "
            "displays or contains; negatively framed when its main requirement is "
            "what the output does *not* do.",
            "**Do not flag** a legitimate constraint, comparison, tolerance or "
            "condition merely because a \"no\" or a \"without\" appears inside "
            "it. \"…fits within the page margins **without overflow**, and "
            "remains legible at normal zoom\" is positive — and it is also the "
            "construction component 26 asks for, so flagging it would leave the "
            "author no compliant wording. \"…reports the variance **without "
            "exceeding 10%**\" states the acceptable result.",
            "**Genuinely negative**, both with positive rewrites available: "
            "\"Body text and list items are **free of** formatting artifacts — no "
            "overlapping text, no truncation, no mixed list markers\", where the "
            "only concrete content is a set of things that must not appear; and "
            "\"**No slide** covers material outside the operations review\".",
            "**Sweep the siblings.** This defect is copied more often than any "
            "other — one audited rubric had a negatively framed criterion caught "
            "and its structurally identical twin two rows down missed; another "
            "had three legibility criteria sharing one absence-framed "
            "construction, of which one was reported. Having found one, search "
            "for the same shape before you score.",
        ],
        "minor": [],
    },

    "Rubric - Redundancy": {
        "before": [
            "Settle \"pervasive\" with this test: **would the overlap cause a "
            "correct agent to be marked wrong, or a wrong agent to be marked "
            "right?** If yes it is the fail option; if no it is the non-fail "
            "band.",
            "Redundancy is **not** a coverage gap. Two criteria testing the same "
            "request means the request is covered — twice. Do not let a coverage "
            "observation drive this score.",
        ],
        "minor": [],
    },

    "Rubric - Weight Share": {
        "before": [
            "**Only `Design & Creative` inverts.** Every other domain — "
            "**including Multimedia & A/V** — takes the default bands, and the "
            "mechanical pre-pass is built that way. Where a Multimedia & A/V "
            "task sits outside the default bands, **flag rather than fail**: "
            "take the non-fail band and say in `justification` that the domain "
            "may warrant the inverted set, so the call is visible. See "
            "`references/source-conflicts.md` §4.",
            "**Take each criterion's declared `criteria_category` as given.** A "
            "share verdict that only holds after you re-categorise something is "
            "not a weighting finding — miscategorisation belongs to component 12.",
            "**Measure the miss from the nearest edge of the band** and state it "
            "in percentage points. A visual share of 18.9% against a 20–30% band "
            "is off by 1.1pp — the non-fail band. A correctness share of 62% "
            "against a 20–30% band is off by 32pp — the fail option. Never "
            "escalate a boundary case.",
            "**Show the arithmetic as `sum / total = xx%` for all three "
            "categories**, not only the one you are scoring against, and **name "
            "the band set you applied** so the choice is visible and can be "
            "challenged.",
            "Trust `mechanical.23_rubric_weight_share`: the three shares, the "
            "band set and `off_by` are precomputed. Do not recompute them.",
            "**The fix is to move weight**, never to refile a criterion into "
            "another category, and never to add or delete criteria in a way that "
            "would take the rubric outside 10–30.",
        ],
        "minor": [],
    },

    "Rubric - Individual Criteria Weights": {
        "before": [
            "**You do not assess whether a weight value suits its criterion's "
            "importance.** A supporting detail weighted 50 and a core result "
            "weighted 3 are both in range and neither is a finding. Never "
            "prescribe a weight on the grounds that it fits the criterion's "
            "importance better — that judgment is not made on this project.",
            "Everything other than a file-existence or file-type/extension gate "
            "is `REGULAR`: page count, slide count, word count, document length, "
            "folder or ZIP structure, every correctness criterion however "
            "important, and every visual criterion.",
            "Trust `mechanical.24_rubric_individual_criteria_weights` for "
            "`weights_out_of_range` and `type_mistags`. MUST-PASS legitimacy "
            "still needs a read of each gate's own title.",
            "**Absent fields are a bundle defect, not a contributor defect.** A "
            "criterion arriving with no `criteria_category` / `criteria_type`, "
            "or a rubric where **no** criterion carries a `weight`, means that "
            "evidence was never handed to you — the band did not run. "
            "`mechanical` reports both under `bundle_defects` and "
            "`bands_not_run` and excludes them from its score. Put them in "
            "`blocked_on`, lower `confidence`, score only the bands that did "
            "run, and never read absence as the contributor omitting the field. "
            "A weight that is *present* and outside [1, 50] is a real defect and "
            "still takes the fail option.",
            "A `MUST-PASS` on anything that is not a file gate is the tagging "
            "error that matters, because it silently gates the whole task on "
            "formatting. The mirror case — a genuine file gate left `REGULAR` — "
            "is the same band, not a worse one.",
        ],
        "minor": [],
    },

    "Rubric - Count": {
        "before": [
            "Trust `mechanical.25_rubric_count` for `n_criteria`.",
            "Check any fix another component prescribes against this band: a "
            "split that would push the rubric past 30, or a merge or deletion "
            "that would drop it below 10, is not a legal remedy.",
            "An over-30 rubric is usually a tooling defect — the generator's "
            "`criteriaCount` is 50 — and a sub-10 rubric submits cleanly because "
            "`minCriteria` is 0. See `references/source-conflicts.md`.",
        ],
        "minor": [
            "**A rubric of 10–14 criteria** is allowed — the CSV's range is "
            "10–30 and this scores a clean 5 — but it sits below the 15–30 "
            "target the project aims for. Record it as a warning with the "
            "suggestion to add criteria up to 15; it **does not affect the "
            "score**.",
        ],
    },

    "Component: Rubric - Robustness": {
        "before": [
            "A criterion is adequately guarded if **either** guard is present, "
            "and either one alone is sufficient: **(a)** an explicit legibility "
            "or quality condition — \"fits without overflow\" paired with "
            "\"remains legible at normal zoom\"; or **(b)** an anchor to the "
            "expected file's layout — \"comparable to the corresponding expected "
            "file\" — which rules out the degenerate shortcut on its own, because "
            "a 4pt table is not comparable to the expected file.",
            "**Never score a formatting or visual criterion down for lacking "
            "guard (a) when it carries guard (b).** This has been a confirmed "
            "over-flag: a criterion was failed as \"a mechanical fit/no-overflow "
            "proxy without a legibility guard\" while the evidence block quoted "
            "its anchoring clause.",
            "**Before taking the fail option, confirm a compliant construction "
            "exists.** It must satisfy this component, atomicity and value "
            "binding *simultaneously*. If your finding leaves the author no "
            "compliant wording, the finding is wrong, not the rubric.",
        ],
        "scores": {"3": [
            "Where the **prompt itself** explicitly asks for the fit, overflow "
            "or pagination behaviour, the criterion is a requested check: "
            "mechanical phrasing there is this band, not the fail option.",
        ]},
        "minor": [],
    },

    "Component: Rubric - Value Binding": {
        "before": [
            "**Anchoring to a whole file instead of the element inside it is the "
            "same defect in another costume.** \"The basket language quoted in "
            "`leverage_memo.docx` is semantically equivalent to the corresponding "
            "expected file\" compares a quotation to an entire document. Where "
            "the comparison target is a section, a table row, a slide, a cell or "
            "a quoted passage, the anchor must name it.",
            "This is **distinct from atomicity**: a criterion can test exactly "
            "one value (atomic) and still fail to bind it to a location. Score it "
            "here, not there, and do not charge the same criterion to both.",
            "**A tolerance band on a transcribed figure unbinds the value.** "
            "Classify every numeric criterion's value first: *transcribed* — "
            "copied off a supplied page, cell or table, so exactly one answer is "
            "right and no method variance exists — or *derived*, computed from "
            "the inputs, where rounding and step order legitimately move the "
            "last digits. A band on a derived value is sound construction and is "
            "never a finding. A band on a transcribed one turns a single correct "
            "answer into a range of accepted ones, which is the score-5 "
            "conjunct \"guard against extraneous candidate values appearing as "
            "correct\" failing: the extraneous candidates are every number "
            "inside the band. Do the arithmetic and put it in evidence — "
            "\"`±1%` of the `$15,481,203` income tax line is `±$154,812`, so a "
            "figure off by six figures passes\" — because the band reads "
            "harmless until it is priced. Uneven bands across the rubric are "
            "not the issue and must not be reported as one.",
            "**Look for one supplied artifact that already contains the whole "
            "answer.** Before clearing a group of value criteria, open the "
            "inputs and ask whether a single page, column, table or cell block "
            "prints every figure that group grades. Where it does, a response "
            "that reproduces that artifact verbatim and unlabelled carries every "
            "graded value and passes them all without performing the task — "
            "which is this component's fail option in its own words, \"cannot "
            "tell a correctly placed answer from a dump of every candidate\". "
            "Name the source artifact and list the criteria it satisfies at "
            "once. Derived values are the defence: a group is safe when at least "
            "one of its figures must be computed and so appears in no input. "
            "Check that fund by fund, entity by entity — a rubric is often safe "
            "on the entity whose figures are computed and wide open on the one "
            "whose figures are transcribed.",
        ],
        "minor": [],
        "evidence": [
            "`inputs_extracted.md` and `render/inputs/<filename>/page-NN.png` — "
            "needed to see whether one supplied artifact already prints every "
            "figure a group of criteria grades",
            "`expected_extracted.md` — the labels, rows and columns a criterion "
            "would have to name to bind its value",
        ],
        "output": {
            "whole_answer_inputs": (
                '[{"criteria": [<one group\'s value criteria>], "input": "<file '
                'and page, column, table or cell block that prints all their '
                'values, or null>"}, "..."]',
                "**`whole_answer_inputs` is required.** It records the check "
                "above for one supplied artifact that already contains the "
                "whole answer: one entry per group of value criteria, giving "
                "the group's criterion numbers and the input that prints every "
                "value the group grades — the file plus the page, column, table "
                "or cell block — or `null` when no single input does. Text "
                "values such as material names count, not only numbers: a "
                "column that lists every material name a group grades prints "
                "that group's whole answer. Use `[]` only when the rubric has "
                "no value criteria."),
        },
    },

    "JSON - Structure / URL Integrity": {
        "before": [
            "Trust `mechanical.28_json_structure_url_integrity`: `func`, "
            "`dest_mismatch`, signed URLs in **both** JSONs and result paths off "
            "the Desktop are precomputed.",
            "An expiring link may have been added by the pipeline rather than the "
            "contributor. Say which JSON carries it; see "
            "`references/source-conflicts.md` before attributing it.",
        ],
        "minor": [],
    },
}


def slug(t: str) -> str:
    t = re.sub(r"^Component:\s*", "", t)
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t.lower())).strip("-")


def parse() -> list[dict]:
    dims, cur = [], None
    for r in csv.DictReader(CSV.open(encoding="utf-8")):
        if r["id"]:
            cur = {k: r[k] for k in ("id", "title", "questionText",
                                     "questionDescription", "required",
                                     "useAllSteps", "errorCategories",
                                     "rubricFailureType")}
            cur["options"] = []
            dims.append(cur)
        if r["answerOptionText"]:
            cur["options"].append({
                "score": r["answerOptionScore"],
                "requires_justification": r["answerOptionRequiresJustification"],
                "text": r["answerOptionText"],
            })
    return dims


def render(i: int, d: dict) -> str:
    cls = CLASS[d["title"]]
    scores = [o["score"] for o in d["options"]]
    cats = [c.strip() for c in (d["errorCategories"] or "").split(";") if c.strip()]

    L = [f"# {i:02d}. {d['title']}", "",
         "> Generated from this skill's `audit-rubric.csv` by `_generate.py`. "
         "Do not hand-edit; edit the CSV and regenerate.", "",
         "| | |", "|---|---|",
         f"| audit-rubric id | `{d['id']}` |",
         f"| title | {d['title']} |",
         f"| allowed scores | {', '.join(scores)} |",
         f"| required | {d['required']} |",
         f"| evidence class | `{cls}` |",
         f"| subagent model | `{MODEL[cls]}` at `--effort max` |", ""]

    L += ["## Question", "", d["questionText"] or "_(none)_", ""]

    if (d["questionDescription"] or "").strip():
        L += ["## Description (verbatim from the CSV)", "",
              "```", d["questionDescription"].strip(), "```", ""]

    cal = CALIB.get(d["title"], {})
    # Either the evidence class carries the rendered pages, or the component
    # asked for them itself. Both need the instructions on how to open one.
    wants_pages = cls == "files" or any(
        "page-NN.png" in e for e in cal.get("evidence") or [])

    L += ["## Score options", "",
          "Only these scores exist for this component. There is no other value; "
          "in particular do not invent a score the CSV does not list.", ""]

    if cal.get("before"):
        L += ["**Before you score.** The notes below are calibration carried "
              "over from the deployed reference evals. They say how the options "
              "that follow are applied — they never add an option, move a "
              "threshold, or create a band the CSV does not list. Where the two "
              "sources genuinely conflict, the CSV wins and the rule is left "
              "out, so everything below is safe to apply as written.", ""]
        L += [f"- {b}" for b in cal["before"]]
        L += [""]

    for o in d["options"]:
        req = str(o["requires_justification"]).lower() == "true"
        L += [f"### Score {o['score']}"
              + ("  — **justification REQUIRED**" if req else "  — justification not required"),
              "", "```", o["text"].strip(), "```", ""]
        notes = (cal.get("scores") or {}).get(str(o["score"]))
        if notes:
            L += ["**Applies to this score.**", ""]
            L += [f"- {n}" for n in notes]
            L += [""]

    L += ["## errorCategories", "",
          "The label a reviewer selects. Emit one of these verbatim in "
          "`error_category` when the score is not the clean pass, else `null`.", ""]
    L += ([f"- `{c}`" for c in cats] if cats
          else ["_(none listed in the CSV for this component)_"])
    L += ["",
          "**One band, one value.** Where the score you chose has no matching "
          "label — several components define a non-fail score but list only a "
          "`Fail` entry — emit `null` and name the band in `justification`. "
          "Never emit a `Fail` label on a non-fail score: the label is what "
          "reaches the reviewer's CSV, and a mislabelled non-fail reads there as "
          "a failure.", ""]

    if d["title"] in ("Prompt - Clarity", "Component: Prompt - Answer leakage",
                      "Rubric - Overfitting", "Rubric - Coverage"):
        L += ["## Multiple valid interpretations", "",
              "An ambiguity matters when it changes the graded output. For each "
              "element of the request that could be read more than one way, list "
              "the defensible readings, then decide whether they produce "
              "*different* artifacts that `criteria[]` would score differently. "
              "If two competent submissions following different valid readings "
              "would be graded differently, the ambiguity is consequential and "
              "belongs in your score; if every valid reading converges on the "
              "same graded content, it does not. Where a method, statistic or "
              "convention is left unspecified and several standard choices give "
              "different numbers, that is consequential by definition.", "",
              "Judge the request as the agent receives it. A supplied template "
              "or example file may narrow a reading, but only if it is "
              "unambiguous on the point in question; do not treat an attachment "
              "as curing an ambiguity it does not actually settle.", ""]

    if d["title"] == "Rubric - Self-Containment":
        L += ["## Anchoring is by filename", "",
              "The CSV requires value and content criteria to anchor to the "
              "expected file **by name** (\"matches the value in "
              "expected_file.docx\"). Read `expected_files[]` first and state "
              "how many there are, then apply the rule below.", "",
              "A generic phrase — \"the expected file\", \"the corresponding "
              "expected file\" — is not self-contained when **both** of these "
              "hold:", "",
              "1. the task ships **more than one** expected file, **and**",
              "2. the criterion's own subject does not already identify the "
              "element being compared.", "",
              "Where the task ships a **single** expected file, the phrase "
              "resolves to it and there is nothing for the grader to guess. "
              "Where the criterion's subject already names the element — \"the "
              "Q3 net revenue figure in the summary table of `summary.xlsx` is "
              "semantically equivalent to the corresponding expected file\" — the "
              "comparison target is unambiguous even across several expected "
              "files. Neither case is a finding; do not flag it.", "",
              "Both conditions together are what make the phrase ungradable: "
              "several candidate artifacts, and nothing in the criterion saying "
              "which one to open. Name the count and the criterion's subject in "
              "your evidence so the call can be checked.", ""]

    if d["title"] == "Component: Rubric - Value Binding":
        L += ["## Binding is a pairing, not co-occurrence", "",
              "A criterion naming a value and a label in one sentence does not "
              "bind them. Ask the CSV's own question: could a submission carry "
              "every correct label and every correct value, paired wrongly, and "
              "still pass? If yes, the value is unbound. Binding needs an "
              "explicit pairing (each value associated with its own row, column "
              "or label) plus a guard against extra candidate values.", ""]

    if d["title"] == "Component: Rubric - Robustness":
        L += ["## The guard lives in the same criterion", "",
              "A legibility or quality guard discharges this component only when "
              "it sits in the **same criterion** as the mechanical check. A "
              "guard in a different criterion does not help: that criterion can "
              "fail independently while the gameable one still passes. Nor does "
              "an argument that other criteria create an incentive against the "
              "shortcut. Name the element at risk, then quote the guard from "
              "that criterion's own text, or record that there is none.", ""]

    if d["title"] == "Prompt - Realism":
        L += ["## Overlap with the rubric is not evidence", "",
              "The rubric is written from the prompt, so prompt wording matching "
              "criterion wording is the expected direction of causation, not "
              "proof the prompt was reverse-engineered from the verifier. Do not "
              "compare prompt text against the criteria for this component. "
              "Score the prompt's own register only: artificial personas, "
              "rubric vocabulary, stacked must/only/exactly, robotic file "
              "references, and whether a real person's motivation is visible. "
              "`prompt_changes_made` is authoring history and says nothing about "
              "the prompt an agent receives.", ""]

    if d["title"] == "Rubric - Coverage":
        L += ["## Decompose before matching", "",
              "Do not match prompt sentences to criteria. A single sentence "
              "routinely carries several atomic asks, and a criterion covering "
              "one of them reads as coverage while the others go ungraded. "
              "Conjunctions, lists and plurals are the tell: \"X and Y\", "
              "\"the options considered\", \"each of the alternatives\", "
              "\"the drivers\".", "",
              "1. Walk the prompt and write out every atomic ask: one verifiable "
              "thing the deliverable must contain or do. Split every conjunction "
              "and expand every plural into its named members. If the prompt "
              "names three items, that is three asks, not one.",
              "2. For each atomic ask, write the specific wrong submission that "
              "satisfies every criterion while omitting or falsifying that ask. "
              "Name which criteria it passes and why none of them fails it. If "
              "you cannot construct such a submission, the ask is covered. A "
              "criterion is not coverage because it names the ask\'s noun — "
              "passing it must **entail** satisfying the ask.",
              "3. State the totals: how many atomic asks, how many covered, "
              "which are not.", "",
              "The test for an uncovered ask: could a submission omit it "
              "entirely and still pass every criterion? If yes, it is "
              "uncovered, however well the rest of the rubric maps.", "",
              "## Primary or secondary", "",
              "The two bands turn on this, so decide it explicitly for each "
              "uncovered ask rather than defaulting to the lower severity.", "",
              "An ask is **primary** when it is essential to the core intent: "
              "the prompt states it as something the deliverable must contain or "
              "decide, a reader would judge the deliverable incomplete without "
              "it, or omitting it would leave a clearly wrong answer passing the "
              "rubric. An ask is **secondary** when it supports or refines a "
              "primary ask, or is implied rather than stated.", "",
              "State the classification and the reason for every uncovered ask. "
              "One uncovered primary ask takes the fail option, whatever the "
              "proportion of the rubric that maps cleanly. Do not describe an "
              "explicitly stated request as implicit.", ""]

    if d["title"] in PERCENT:
        L += ["## Counting instances", "",
              "This component's threshold is a share of the criteria, so the "
              "verdict turns on the count. Walk **every** criterion in "
              "`criteria[]` and record a verdict for each: does it exhibit the "
              "defect, yes or no. Report the count, the denominator and the "
              "resulting percentage, and list the criterion numbers on both "
              "sides of the line. Do not report only the ones you decided "
              "count.", "",
              "One criterion moves the share by three to five points on a "
              "typical rubric, which is enough to cross the threshold on its "
              "own. When a criterion is borderline, say so explicitly and say "
              "which way you resolved it. If including the borderline cases "
              "would cross the threshold, report both figures and take the "
              "stricter band; a defect the form names is not excused by being "
              "one instance short.", ""]

    if d["title"] in ("Component: Rubric - Robustness", "Rubric - Categorization"):
        L += ["## Scope, not just presence", "",
              "A guard or a label is not enough on its own; it has to cover the "
              "thing at risk. For each criterion in scope, name the specific "
              "element that could be degraded or mis-handled, then check whether "
              "the guard or category actually covers **that element**. A guard "
              "scoped to one element leaves every other element unprotected, "
              "and a criterion that spans two categories is mis-categorised even "
              "when the category it carries is defensible for part of it. Report "
              "the element and the coverage, not the existence of the clause.", ""]

    L += ["## Evidence to read", ""]
    # A few components need one source their evidence class does not carry --
    # a rubric component that has to read what the answer key actually stores,
    # for instance. `evidence` widens that component alone.
    L += [f"- {e}" for e in EVIDENCE[cls] + (cal.get("evidence") or [])]
    L += ["",
          "Every path above is relative to the evidence directory named in the "
          "prompt. Read nothing outside it.", ""]

    if wants_pages:
        L += ["## Looking at the artifacts", "",
              "You can read images directly. Use the Read tool on any `.png`, "
              "`.jpg`, `.gif` or `.webp` under `files/inputs/` or "
              "`files/expected/` and judge what it actually shows: axis labels, "
              "series, legends, value labels, what the picture depicts, whether "
              "it matches its filename and what the prompt says about it. The "
              "text extraction lists these files as `IMAGE` with dimensions "
              "only; that is a limit of the extraction, not of you. Never score "
              "a component clean on an artifact you did not look at. If a file "
              "genuinely will not open, set `blocked_on` and lower "
              "`confidence`.", "",
              "Everything else that has a visual form — `.docx`, `.xlsx`, "
              "`.pptx`, `.pdf`, `.html`, and the rest — has already been "
              "rasterised for you, one PNG per page, under "
              "`render/<side>/<filename>/page-NN.png`. The prompt lists the "
              "exact page files.", "",
              "**Open them with the Read tool before you score, and do it "
              "first.** Not `cat`, not `head`, not a Python one-liner: a PNG "
              "carries no text for Bash to print, and the `text.txt` beside "
              "the pages is text, not appearance. Reading the chart XML out of "
              "an `.xlsx`, or the slide XML out of a `.pptx`, tells you a "
              "chart was declared — it cannot tell you the axis labels are "
              "legible, the series fit, the columns are not clipped or the "
              "table did not spill onto a second page.", "",
              "The pages are the only evidence that shows pagination, "
              "clipping, column overflow, overlapping shapes, blank pages, "
              "chart legibility and whether something fits on one page. So: "
              "any statement you make about appearance must name the page file "
              "you opened to see it. An appearance claim you did not look at "
              "is not a finding, and it is not a clean pass either.", "",
              "Never render anything yourself and never attempt a `pip "
              "install` or an application install. Extraction and rendering "
              "are both already done. Open an original only when it is an "
              "image.", "",
              "### What the render is worth — check `render_index.json` first",
              "",
              "The entry for a file states how far its appearance can honestly "
              "be judged. Respect it literally.", "",
              "- `visual_verifiable: true` — the pages are a faithful render. "
              "Judge appearance from them.",
              "- `visual_verifiable: false` (`status` `degraded` or "
              "`unavailable`) — the renderer for that format is missing or "
              "only a first-page preview was produced. Its `unverifiable_reason` "
              "says which. Every ask about that file's layout goes in "
              "`blocked_on` with that reason. A renderer this audit host lacks "
              "is never evidence of a defect in the submission.",
              "- `truncated: true` — pages beyond the ones listed were not "
              "rendered. Say nothing about them.",
              "- `parity` — whether the application that laid these pages out "
              "is the version the CUA VM runs (`cua-applications.csv`). "
              "`exact` or `compatible`: pagination claims are sound. "
              "`mismatch` or `unknown`: what you see may be this host's "
              "LibreOffice rather than the VM's, so claims that depend on "
              "exact reflow — total page count, a table fitting on one page, a "
              "specific line break — go in `blocked_on`. What is visible on "
              "the page regardless of reflow (a missing chart, an empty "
              "section, a wrong label, overlapping shapes) stands as a "
              "finding.", ""]
        L += [
              "## Required method — reproducibility of the expected artifact",
              "",
              "Do this before you score. The question is not whether the "
              "expected files agree with one another; it is whether a competent "
              "agent could arrive at them from what it is actually given.", "",
              "1. Inventory what the agent has. List the input files. For every "
              "input that is a script, template, schema or config, state the "
              "outputs it can generate and the vocabulary, labels and ranges it "
              "can emit.",
              "2. For each graded value in the expected files, name the specific "
              "input it derives from and the operation that produces it. "
              "Recompute it where it is computable.",
              "3. Mark every value you cannot reach, and say why — absent from "
              "all inputs; requires a label, constant or category the provided "
              "code cannot emit; requires data the agent never receives; "
              "requires a step the inputs do not support.",
              "4. Report both halves in `justification`: what you reconstructed, "
              "and what you could not reach.", "",
              "**Reachable is not the same as correct.** Step 3 establishes only "
              "that a value can be derived from the inputs. It says nothing "
              "about whether the value is right. Both must hold, and "
              "correctness is the more important of the two. Separately check: "
              "is the arithmetic right; does the artifact satisfy every request "
              "the prompt and any supplied template make, including sections or "
              "fields left blank; do the inputs actually contain what their "
              "filenames and the prompt claim they contain; and is the content "
              "true against the domain rather than merely internally "
              "consistent. A traceable value that is wrong, and an artifact "
              "that is accurate but incomplete against the template, are both "
              "defects. State the correctness check you ran, not only the "
              "derivation.", "",
              "A label or wording is a presentation choice **only if no "
              "criterion grades it**. Check `criteria[]`: once a criterion "
              "compares that cell, field or label to the expected file, it is a "
              "graded value, and \"the agent could have phrased it differently\" "
              "is not available as a defence — the criterion demands the "
              "expected file's version specifically.", "",
              "A graded value the agent cannot reach is **not** cosmetic and "
              "**not** a disagreement between expected files. It is "
              "unreachable, every criterion anchored to it is unsatisfiable. "
              "Report it. But score **only** against this component's own "
              "answer options: if none of them describes unreachability, this "
              "finding does not change your score, and it belongs in "
              "`justification` as context. Never stretch an option's wording to "
              "fit a defect it does not name.", ""]

    L += ["## Output contract", "",
          "Return exactly one JSON object:", "",
          "```json", "{", '  "component_id": "%s",' % d["id"],
          '  "title": "%s",' % d["title"].replace('"', '\\"'),
          '  "score": <one of: %s>,' % ", ".join(scores),
          '  "error_category": "<verbatim from the list above, or null>",',
          '  "justification": "<required when the chosen score says so>",',
          '  "evidence": "<quote the exact text, value, cell or filename>",',
          '  "criteria": [<rubric criterion numbers, if applicable>],',
          '  "confidence": "high|medium|low",',
          '  "blocked_on": "<what you could not verify, or null>",']
    extra = cal.get("output") or {}
    L += [f'  "{k}": {example},' for k, (example, _) in extra.items()]
    L += ['  "minor_issues": ["<non-scoring suggestion>", "..."]', "}", "```", "",
          "Rules:", "",
          "- Score **only** from the options above. The clean-pass score is "
          f"`{scores[-1]}`.",
          "- A score whose option is marked **justification REQUIRED** must carry "
          "a non-empty `justification` naming the threshold it crosses and the "
          "evidence it rests on.",
          "- Quote evidence. A finding with no quoted text, value or filename is "
          "not a finding — score the clean pass instead.",
          "- If you could not verify something (a file would not open, an "
          "artifact is unavailable), set `blocked_on` and lower `confidence`; do "
          "not guess.",
          "- Judge **this** submission only. Any reviewer score or feedback in "
          "the task response was written about the PREVIOUS attempt and does not "
          "apply here — ignore it."]
    L += [f"- {rule}" for _, rule in extra.values()]
    if "Rubric - " in d["title"]:
        L += ["- **A criterion you propose must pass the rubric itself.** Replacement "
              "or new criterion text you write, in `justification` or "
              "`minor_issues`, is judged by the rubric components the way the "
              "task's own criteria are. It never states the value, name, date, "
              "count or conclusion the agent has to produce: it names the expected "
              "file and a comparison — a tolerance on a derived number, semantic "
              "equivalence on prose — and only a value the prompt itself gives may "
              "appear. It has no conditional wording (\"if …\", \"unless …\", "
              "\"where applicable\", \"when present\", \"if any\", \"any X it "
              "reports\"): the task's inputs already fix which case holds, so it "
              "grades that case's outcome. It tests one element. A criterion that "
              "grades what the prompt never asks for is removed, folded into "
              "another, or backed by a prompt change, never made conditional."]
    L += ["- `minor_issues` is **never scored**. It carries suggestions that "
          "would improve the task but that this component's answer options do "
          "not name, so nothing you put there may change `score`, "
          "`error_category` or the verdict — and a clean pass stays a clean pass "
          "with entries in it. Use `[]` when there is nothing to record."]
    if cal.get("minor"):
        L += ["- Record in `minor_issues` any of the following you find. Each "
              "entry quotes its evidence, names the file or criterion, and "
              "states the fix:"]
        for m in cal["minor"]:
            hard = (" Keep the opening phrase as written: this defect is a hard "
                    "gate elsewhere in the project, so the report prints the "
                    "whole entry in bold. It still does not affect your score."
                    if lead_phrase(m) in HARD_GATE else "")
            L += [f"  - {m}{hard}"]
    L += [""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    dims = parse()
    assert len(dims) == 28, f"expected 28 components, CSV has {len(dims)}"
    missing = [d["title"] for d in dims if d["title"] not in CLASS]
    assert not missing, f"CLASS has no entry for: {missing}"

    OUT.mkdir(parents=True, exist_ok=True)
    stale, written = [], []
    for i, d in enumerate(dims, 1):
        p = OUT / f"{i:02d}-{slug(d['title'])}.md"
        body = render(i, d)
        if a.check:
            if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != \
                    hashlib.sha256(body.encode()).hexdigest():
                stale.append(p.name)
            continue
        p.write_text(body, encoding="utf-8")
        written.append((p.name, CLASS[d["title"]], [o["score"] for o in d["options"]]))

    if a.check:
        print(f"stale: {stale}" if stale else "all 28 component files up to date")
        return 1 if stale else 0

    by = {}
    for n, c, _ in written:
        by.setdefault(c, []).append(n)
    print(f"wrote {len(written)} component files to {OUT}")
    for c in ("files", "rubric", "other"):
        print(f"  {MODEL[c]:22} {c:7} {len(by.get(c, []))} components")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
