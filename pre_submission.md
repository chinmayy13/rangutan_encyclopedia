# Pre-Submission Checklist

**THE ONE RULE:** build criteria by walking the prompt, not the gold file. Per requirement, ask "does the prompt allow more than one valid, correct answer?" No → Anchored (fine to match the expected file). Yes → Open (grade the shared property, don't lock to one pick). "Semantically/comparable to the expected file" wording is NOT automatically safe — that's exactly where overfitting hides.

**Most common hard-fails, in order:** Coverage > Overfitting > Categorization > Gold File Accuracy > Atomicity > Redundancy.

## RUBRIC

☐ **Atomicity** — each criterion = one element (section/table/chart/image), one category only (10-row table = 1 criterion, graded as a whole)

☐ **Objectivity** — non-visual criteria avoid "good/nice/appropriate" (visual criteria may use subjective language)

☐ **Overfitting** — would a different competent, prompt-only submission be penalized for a valid alternate answer? (chart type, row count, one selected stat, unstated formula, invented title/wording)

☐ **Framing** — positively framed ("does X"), not negative, unless prompt asks to omit something

☐ **Coverage** — every explicit prompt request has a criterion on the SAME ASPECT, not just same noun (value vs. exists, provenance/tool, full set vs. sibling set)

☐ **Redundancy** — no criteria pairs testing the same thing twice

☐ **Content** — correctness criteria check actual values, not just existence ("includes a revenue section" ≠ checks its content)

☐ **Weight Share** — format_gate ≤20%; correctness >50% (20-30% Design & Creative); visual 20-30% (≥50% Design & Creative) (off by >5pts = major, ≤5pts = minor)

☐ **Categorization** — format_gate=file/name/ext, correctness=content/values, visual=appearance/layout only (which items exist / what order = content, never visual)

☐ **Individual Weights** — every weight is an integer 1-50; MUST-PASS reserved for format-gate only

☐ **Hardcoded Values** — value criteria reference expected file + tolerance, never state the literal answer (2+ = major, 1 = minor)

☐ **Count** — 10-30 criteria total

☐ **Rubric Accuracy** — every criterion is objectively, factually correct (1+ inaccuracy = major)

☐ **Robustness** — no criterion gameable by a degenerate shortcut (e.g. shrinking text to "fit") (pair with a legibility/min-size clause, or anchor to expected file layout)

☐ **Self-Containment** — grader sees ONLY expected file + output, never prompt/inputs — criteria anchor to expected file by name (exception: agent's own output compared to itself)

☐ **Value Binding** — values bound to correct row/column/label, extraneous candidate values ruled out

## PROMPT

☐ **Realism** — reads like a real person, real "why", not templated or overly prescriptive (watch: rubric-style phrasing, artificial personas, excessive must/only/exactly, robotic file refs)

☐ **Timelessness** — all sources historical/static; arXiv pinned to a version (…/abs/v1)

☐ **Clarity** — goal obvious, at most a tiny reasonable assumption needed

☐ **Answer Leakage** — prompt doesn't contain the actual scored answer content (values, conclusion, required sentences)

☐ **GUI Integration** — a meaningful GUI action changes what the agent must observe/do, not GUI-for-its-own-sake

☐ **Feasibility** — task completable in the VM with what's installed

☐ **Output Naming** — exact output filename(s) stated naturally + Desktop save location, matching gold assets

☐ **PII / Safety** — no real, sensitive personal data (real person + contact/financial/sensitive info)

## GOLD FILE

☐ **Accuracy** — satisfies every explicit prompt request, correct data/values/formatting (re-read prompt line by line)

☐ **Input Consistency** — every gold value traces back to the actual provided input files

☐ **Format** — correct Office format; per-OS file if applicable; GT URL points to the gold file, not the starting file

## FINAL PASS

☐ **Cold re-read** — as the LLM grader (never saw the prompt) — could a different valid answer still fail any "matches expected file" criterion?

☐ **JSON / URL** — correct golden links, expected/result filenames match gold files, verifier runs clean, func = agent_judge_multi

☐ **Structure** — 10-30 criteria, weights 1-50, weight-share in band, filenames correctly anchored

*Full explanations, examples, and reasoning for every item above start on the next page.*

---

# Detailed Reference

Full explanations for the checklist on page 1 — use this when you need to double-check a judgment call.

## THE ONE RULE THAT FIXES MOST FAILURES

Build your rubric by walking the prompt, one requirement at a time — never by looking at your gold file and writing criteria to match what you produced. For each requirement ask one question:

**"Does the prompt allow more than one valid, correct way to satisfy this?"**

- **No, there's exactly one right answer** (a number, a fact, a name the prompt gives you) → **Anchored.** Fine to grade as "matches the expected file."
- **Yes, competent people could reasonably do this differently** (which stat to lead with, a formula not stated, a layout choice, how many rows, phrasing) → **Open.** Do NOT lock to the expected file's specific pick — grade the property every valid answer must share instead.

**Warning — the "safe harbor" trap:** phrases like "semantically equivalent to the expected file" or "comparable to the expected file" are NOT automatically safe. They are exactly where overfitting hides, because a criterion can use that correct-sounding phrasing while still locking onto one Open answer. The phrasing never makes a criterion safe — only Anchored-vs-Open does. Every time you see this phrasing, stop and re-ask the one question above.

Historically, the most common hard-fail reasons in this order: **Coverage > Overfitting > Categorization > Gold File Accuracy > Atomicity > Redundancy.** Check those first if you're short on time.

## 1. RUBRIC CHECKLIST

### Atomicity

**R1. Atomicity** — Does each criterion test exactly ONE element, in ONE category?

- **Major issue if:** more than ~15% of criteria test more than one "element" (a section/table/chart/image is one element) OR mix Format Gate + Correctness + Visual in the same criterion.
- *Tip: A table with 10 rows still needs only ONE criterion (grade it as a whole/aggregate) — atomic does not mean "one criterion per data point," it means one criterion per element, and one category per criterion.*

### Overfitting

**R2. Overfitting** — Would a different, competent submission — working only from the prompt and input files, without ever seeing the gold file — get penalized for a valid alternate answer?

- **Major issue if:** this is true for a meaningful share of criteria.
- **Minor issue if:** true for an isolated criterion or two.
- *Tip: Common invisible overfits: mandating a chart type/color scheme/layout the prompt never asked for; requiring a specific row count when the prompt says "a few" or "the main ones"; requiring one selected stat/finding out of several equally valid ones; requiring a formula the prompt never states (verify it isn't stated in an input file first); requiring a wording/title/subtitle the prompt never asked for. The Robustness carve-out below is narrow: legibility/containment/anti-clipping language is NEVER overfitting — but that carve-out does NOT extend to chart type, chart features, layout choice, or item counts.*

### Coverage

**R3. Coverage** — Walk every explicit request in the prompt. Does a criterion actually cover the SAME ASPECT of it — not just the same topic/noun?

- **Major issue if:** at least 1 explicit PRIMARY request has no criterion covering its actual aspect — a clearly wrong answer could still pass.
- **Minor issue if:** at least 1 secondary/implicit request is uncovered.
- *Tip: The #1 hidden failure: a criterion mentions the same noun as the prompt but checks the wrong aspect — e.g. prompt asks for the correct VALUE, criterion only checks the column/section EXISTS; prompt asks for a specific tool/provenance ("screenshot taken in VS Code"), criterion never checks that; prompt gives a whole SET of items, criterion only checks a different sibling set. Matching the noun is not matching the requirement.*

### Content (correctness criteria only)

**R4. Content** — Do your correctness criteria check actual VALUES/content, not just that something exists?

- **Major issue if:** more than ~15% of correctness criteria only check existence (e.g. "Includes a revenue analysis section") rather than its content.
- **Minor issue if:** up to ~15% do this.

### Categorization

**R5. Categorization** — Is every criterion tagged the right category?

- **Major issue if:** a meaningful share of criteria are mis-tagged.
- **Minor issue if:** an isolated slip with no gating impact.
- *Tip: format_gate = file exists/named/extension correct. correctness = content, values, data, which item is shown. visual = pure appearance/layout/legibility ONLY. "Which sections/items exist" or "what order things appear in" is a CONTENT fact, never visual — even inside a rendered document.*

### Hardcoded Values

**R6. Hardcoded Values** — Does every value-comparison criterion reference the expected file with a tolerance, instead of stating the literal answer?

- **Major issue if:** 2 or more criteria state a literal expected value (e.g. "Shows X as 3.89°").
- **Minor issue if:** exactly 1 criterion does this.
- *Tip: Fix: "...matches the corresponding value in the expected file within ±1%" — never restate the number itself, even alongside an expected-file reference.*

### Accuracy

**R7. Rubric Accuracy** — Is every criterion objectively, factually correct (no typos in logic, no impossible asks)?

- **Major issue if:** at least 1 criterion contains an objective inaccuracy.

### Self-Containment

**R8. Self-Containment** — Remember: the LLM grader sees ONLY the expected file + agent output — never your prompt or input files. Does every criterion make sense on its own, anchored to the expected file by name?

- **Major issue if:** a meaningful share of criteria need prompt/external context the grader doesn't have.
- **Minor issue if:** a smaller share need minor external context.
- *Tip: Exception: a criterion comparing two parts of the agent's OWN output to each other doesn't need to anchor to the expected file.*

### Objectivity

**R9. Objectivity** — Can a grader check this without personal opinion?

- **Major issue if:** more than ~10% of (non-visual) criteria are subjective/ungradable ("good," "nice," "appropriate").
- **Minor issue if:** up to ~10% are subjective but still reasonably gradable.
- *Tip: Visual criteria are explicitly allowed subjective phrasing like "professional/appropriate" — this rule is for non-visual criteria only.*

### Framing

**R10. Framing** — Is every criterion positively framed ("the model does X")?

- **Major issue if:** at least 1 criterion is negatively framed ("does not include...") and the prompt never asked to omit anything.
- *Tip: Negative framing is fine ONLY when the prompt explicitly asks to omit/exclude something.*

### Redundancy

**R11. Redundancy** — Is every criterion checking something functionally distinct?

- **Major issue if:** redundant/overlapping criteria are pervasive.
- **Minor issue if:** one or two overlapping pairs exist, minimal scoring impact.

### Weight Share

**R12. Weight Share** — (sum of category weight) / (total rubric weight) — does it land in the band for your domain?

- **Major issue if:** any category is off its band by more than 5 points.
- **Minor issue if:** off by up to 5 points.

| Category | All domains except Design & Creative | Design & Creative |
|---|---|---|
| Format Gates | ≤ 20% | ≤ 20% |
| Correctness | > 50% | 20–30% |
| Visual | 20–30% | ≥ 50% |

### Individual Criteria Weights

**R13. Individual Weights** — Is every weight an integer 1–50, and is MUST-PASS used only for format-gate criteria (the file itself/correct extension)?

- **Major issue if:** at least 1 criterion has a weight outside 1–50.
- **Minor issue if:** weights all in range, but one criterion mistagged MUST-PASS/REGULAR.

### Count

**R14. Count** — Does the rubric have 10–30 criteria total?

- **Major issue if:** fewer than 10 or more than 30 criteria.

### Robustness (anti-hacking)

**R15. Robustness** — Can any formatting/visual criterion be satisfied by a degenerate shortcut that defeats its intent?

- **Major issue if:** a criterion like "no overlap"/"doesn't overflow"/"fits on one page" is passable by shrinking text unreadably, with NO paired legibility/quality guard.
- **Minor issue if:** outcome-based overall, but one criterion is a mechanical negative proxy without an explicit guard, though not trivially gameable.
- *Tip: Fix by pairing with a legibility/min-size condition, or by anchoring to the expected file's layout — either alone is enough. General "must be legible" language already satisfies the minimum.*

### Value Binding

**R16. Value Binding** — Does every value criterion bind the value to its correct row/column/label, and rule out other candidate values also appearing?

- **Major issue if:** a value only needs to appear SOMEWHERE in the file — can't tell a correct answer from a dump of every candidate value.
- **Minor issue if:** value required in labeled context, but doesn't explicitly rule out other candidates also appearing.

## 2. PROMPT CHECKLIST

### Realism — natural, not prescriptive

**P1. Realism** — Does this read like a real person asked for it, with a real reason ("why") behind the ask?

- **Major issue if:** synthetic/templated with no real "why"; reads as a raw test case; OR overly prescriptive (step-by-step / exact section-title checklists that leak verifier logic or overfit the output).
- **Minor issue if:** natural and grounded but somewhat more procedural than a real user would write — not yet leaking verifier logic.
- *Tip: Watch for the 4 anti-patterns: (1) rubric-style language — "treat X as fixed," "do not use outside sources"; (2) artificial personas — "You are a finance manager..."; (3) excessive must/only/exactly; (4) robotic file references — "extract data from file A and file B."*

### Clarity

**P2. Clarity** — Is the goal obvious with no more than a tiny, reasonable assumption needed?

- **Major issue if:** overly vague, goal indeterminable.
- **Minor issue if:** one valid interpretation but could be clearer / needs a tiny reasonable assumption.
- *Tip: Don't force-fix ambiguity that has a predominant interpretation, or that would never actually cause a verifier mismatch. Minor typos are fine if intent is obvious.*

### GUI Integration

**P3. GUI Integration** — Does the deliverable require a meaningful GUI action that changes what the agent must observe or do — not GUI-for-its-own-sake?

- **Major issue if:** no meaningful GUI interaction where the deliverable plainly calls for one (e.g. a layout/visual/animation task solvable entirely by script).
- **Minor issue if:** GUI interaction present but minimal or only loosely tied to the deliverable.

### Output Naming

**P4. Output Naming** — Does the prompt name the EXACT output filename(s) naturally, and state that outputs save to the Desktop?

- **Major issue if:** omits the exact filename(s), or doesn't state the Desktop location such that a verifier can't locate the output.
- *Tip: Filenames must also match what the gold file assets actually use.*

### Timelessness

**P5. Timelessness** — Is every data source historical/static?

- **Major issue if:** the correct solution varies with time (live data), or a time-sensitive claim is framed as trajectory confirmation that could mislead the agent (e.g. "There should be 113 results...").
- **Minor issue if:** time-sensitive statements present but don't affect the correct solution (background noise).
- *Tip: For arXiv sources, pin to a fixed historic version, e.g. .../abs/<id>v1.*

### Answer Leakage

**P6. Answer Leakage** — Could an agent copy content straight out of the prompt into the output and get real credit?

- **Major issue if:** the prompt contains the actual scored answer content (values, the conclusion, required sentences).
- **Minor issue if:** restates 1–2 secondary facts also in the answer, but the graded deliverable still requires real work.

### Feasibility & PII/Safety

**P7. Feasibility** — Can this actually be completed in the VM with what's installed?

- **Major issue if:** cannot be completed in the VM (e.g. needs software that isn't installed).

**P8. PII / Safety** — Any real, sensitive personal data (real non-famous person + contact/financial/sensitive info)?

- **Major issue if:** contains a major PII instance.
- **Minor issue if:** PII present but hard to trace / synthetic.
- *Tip: Standalone names/usernames alone are fine.*

## 3. GOLD FILE CHECKLIST

The gold file is the answer key — it must satisfy everything the prompt actually asked for, exactly, with correct file/naming conventions. The rubric grades against the gold file, not the prompt directly — so if the gold file is wrong, every "Anchored" criterion built on it is wrong too.

**G1. Gold File Accuracy** — Re-read the prompt line by line against the gold file. Does the gold file satisfy every explicit request, with correct data/values/formatting?

- **Major issue if:** wrong/missing data, wrong values, ordinal-vs-cardinal errors, tied-rank errors, missing required formatting.
- **Minor issue if:** content/values substantively correct, but a minor non-scoring format issue exists (cosmetic, resolvable naming deviation).

**G2. Gold File Format** — Correct Office format? Per-OS file where applicable? Ground-truth URL points to the gold file, not the starting file?

- **Major issue if:** wrong format; a single file shared across OSes when it shouldn't be; URL points to the starting file instead.

**G3. Input Consistency** — Does every value in the gold file trace back to the actual input files provided to the agent?

- **Major issue if:** gold file records/values don't derive from the provided inputs (different dataset/IDs/figures) — a correct agent working from the inputs cannot match it.
- **Minor issue if:** 1–2 secondary gold values aren't traceable to inputs, but the core deliverable derives correctly.

## FINAL PASS

- Re-read your rubric cold, as if you are the LLM grader who has never seen the prompt — for every "matches/equivalent to expected file" criterion, could a different valid answer still fail it?
- Count your criteria: 10–30, weights 1–50, categories in band.
- Confirm every criterion cites the correct expected filename it anchors to.
- Confirm JSON structure/URL integrity: correct golden file links, expected/result filenames match the gold files, verifier runs cleanly, "func" is "agent_judge_multi".
