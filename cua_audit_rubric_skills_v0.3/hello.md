(base) chinmaykumar@Chinmays-MacBook-Air cua_audit_rubric_skills_v0.3 % python3 cua-audit-components/scripts/run_review.py task_9
17 component call(s) over 1 unit(s), effort=max, 12 workers
claude-opus-5 16 calls
claude-sonnet-5 1 calls
[task_9 16] 60s 32 ev
[task_9 21] 60s 29 ev
[task_9 18] 60s 48 ev
[task_9 19] 60s 28 ev
[task_9 15] 60s 49 ev
[task_9 20] 60s 49 ev
[task_9 23] 60s 30 ev
[task_9 11] 60s 57 ev
[task_9 08] 60s 29 ev
[task_9 17] 61s 30 ev
[task_9 22] 61s 41 ev
[task_9 09] 61s 45 ev
[task_9 16] 120s 89 ev
[task_9 15] 120s 101 ev
[task_9 20] 121s 89 ev
[task_9 22] 121s 80 ev
[task_9 19] 121s 77 ev
[task_9 17] 122s 78 ev
[task_9 09] 122s 92 ev
[task_9 18] 122s 100 ev
[task_9 11] 122s 93 ev
[task_9 08] 122s 87 ev
[task_9 21] 122s 80 ev
[task_9 24] 60s 28 ev
[task_9 15] 181s 145 ev
[task_9 16] 181s 138 ev
[task_9 09] 182s 141 ev
[task_9 19] 182s 126 ev
[task_9 20] 182s 139 ev
[task_9 18] 182s 140 ev
[task_9 17] 182s 131 ev
[task_9 11] 183s 142 ev
[task_9 08] 183s 137 ev
[task_9 22] 195s 123 ev
task_9 08 [opus-5]: ok (241.6s) score=5
[task_9 15] 242s 188 ev
[task_9 19] 242s 175 ev
[task_9 09] 242s 191 ev
[task_9 18] 243s 193 ev
[task_9 20] 243s 177 ev
[task_9 17] 243s 175 ev
[task_9 11] 244s 187 ev
[task_9 16] 246s 190 ev
[task_9 26] 60s 42 ev
[task_9 27] 60s 32 ev
[task_9 28] 60s 54 ev
[task_9 15] 302s 234 ev
[task_9 11] 304s 235 ev
[task_9 18] 305s 237 ev
[task_9 27] 120s 80 ev
[task_9 09] 310s 241 ev
[task_9 15] 363s 285 ev
[task_9 11] 365s 276 ev
[task_9 27] 180s 133 ev
[task_9 09] 371s 285 ev
[task_9 18] 392s 275 ev
[task_9 11] 425s 319 ev
[task_9 27] 241s 182 ev
[task_9 09] 432s 333 ev
[task_9 15] 432s 303 ev
[task_9 11] 486s 329 ev
task_9 09 [opus-5]: ok (489.1s) score=3
task_9 11 [opus-5]: ok (487.3s) score=5
task_9 15 [opus-5]: ok (433.6s) score=5
task_9 16 [opus-5]: ok (273.5s) score=2
task_9 17 [opus-5]: ok (265.9s) score=5
task_9 18 [opus-5]: ok (393.5s) score=3
task_9 19 [opus-5]: ok (284.2s) score=5
task_9 20 [opus-5]: ok (287.6s) score=2
task_9 21 [opus-5]: ok (133.8s) score=5
task_9 22 [opus-5]: ok (195.9s) score=3
task_9 23 [opus-5]: ok (90.9s) score=5
task_9 24 [opus-5]: ok (94.8s) score=5
task_9 25 [opus-5]: ok (55.2s) score=5
task_9 26 [opus-5]: ok (80.1s) score=5
[task_9 27] 301s 236 ev
[task_9 27] 362s 285 ev
[task_9 27] 423s 330 ev
[task_9 27] 725s 347 ev
task_9 27 [opus-5]: ok (776.0s) score=3
task_9 28 [sonnet-5]: ok (68.6s) score=5

Scale GenAI Ops / CUA v3
Audit rubric review

1 task submission scored against the 28 components of the CUA v3 audit rubric, one component at a time, then read across components by a senior review pass.
1
submissions
28
component scores
0
fail
1
non-fail
0
pass
2
escalations
3
contradictions
76
recommendations

How to read this
What was scored

Each submission is a contributor's completed CUA v3 task: a prompt, the input files an agent receives, the expected output files that serve as the answer key, a weighted rubric, and a verifier configuration. The audit rubric is the review form a human reviewer fills in. It has 28 components covering the task, the prompt, the expected files, the rubric, and the verifier JSON.

Every component was scored by its own model call reading only that component's definition and the evidence it needs. Component definitions are generated from the review form itself, so the score options and thresholds are the form's, not this tool's.
Scores
Score Band Meaning
2 fail The component's failing condition is met.
3 non-fail An issue is present below the failing threshold.
4 non-fail A minor issue. Two components use 4 instead of 3.
5 pass Clean.

Score sets differ by component. Seven components allow only 2 or 5, with no middle band.
The verdict

A submission takes the lowest score across all 28 components. One component at 2 makes the whole submission a fail. Every component must be 5 for the submission to pass.
Recommendations, and why a 5 can still carry them

The review form has 28 components and no more, so a real defect that none of their answer options describes has nowhere to be scored. Those are recorded separately as recommendations. They never move a score, a label or the verdict, which means a component can score 5 and still carry work the contributor should do before submitting.

This report carries 76 recommendations, 35 of them on components that scored 5. They are listed per submission below, and every component in the 28-score grid that carries one is marked with an amber count beside its score. A clean grid is not the same as nothing to fix.

Examples of what lands here: placeholder text or encoding damage in an expected file, criterion markup and grammar, a rubric of 10 to 14 criteria, an output filename that is awkward but resolvable, and a criterion that states no comparison tolerance. Each is a genuine defect the form does not ask about.
The senior review pass

Component scores are produced in isolation, so a fact found by one component and its consequence in another are never seen together. A final pass reads all 28 results for a submission and reports three things it can see that the individual scores cannot: contradictions between two components' claims, escalation proposals where the wider picture supports a lower score, and which component the verdict rests on. It cannot change a score, and it can only propose moving a score toward a fail, never away from one.

Triage
All submissions

Verdict, the component that drives it, and the first fix. Follow a row to its detail below.
Submission Domain Verdict Driven by Esc Con Rec First fix
task_9 Design & Creative 3 04 Prompt - Realism, 07 Prompt - Timelessness, 09 Gold File - Accuracy, 11 Component: Gold File - Input Consistency, 16 Rubric - Coverage, 17 Rubric - Self-Containment, 18 Rubric - Overfitting, 19 Rubric - Atomicity, 20 Rubric - Objectivity, 22 Rubric - Redundancy 2 3 76 Fix the gold project's 3D panel geometry and re-capture the screenshot. In TokenWave.tscn the SubViewport is size = Vector2i(370, 370) inside a SubViewportContainer laid out 185x185 at

Rec counts unscored recommendations. A submission can pass with a verdict of 5 and still carry them.
Input file consistency

Whether the material the task is built from agrees with itself: the input files against each other, and against the prompt, the expected files and the criteria. The 28 components each grade one artifact against the review form, and none of them asks this, so a submission can score clean on all 28 while two supplied sources state different rules for the same quantity.

Major means the inconsistency changes what a correct submission looks like: an agent working faithfully from the inputs cannot reach the graded answer, or has to guess between two supplied rules that lead to different graded values. Minor means a real inconsistency that moves no graded output. This pass is never scored and never reaches the verdict.
Submission State Major Minor Rules What the check found
task_9 major issues 1 5 27
I opened gameplay_config.txt, scene_reference.png (pixel-measured), source_coin_token.png (alpha-measured), Bomb.glb (parsed GLB ...

Rules counts the shared rules, thresholds and quantities that were stated in more than one place and so could be cross-checked. A finding already covered by a scored component names that component; the rest have no home on the review form.
Scores by component across all submissions

A component scoring low on many submissions points at a systemic authoring issue or at the component's own calibration.

# Component 2 3 4 5 Drives Rec

01 Task - Feasibility . . . 1 . .
02 Task - PII / Safety . . . 1 . 3
03 Prompt - Clarity . . . 1 . 2
04 Prompt - Realism . 1 . . 1 1
05 Prompt - GUI Integration . . . 1 . .
06 Prompt - Output Naming . . . 1 . .
07 Prompt - Timelessness . 1 . . 1 1
08 Component: Prompt - Answer leakage . . . 1 . 3
09 Gold File - Accuracy . 1 . . 1 7
10 Gold File - Format . . . 1 . .
11 Component: Gold File - Input Consistency . 1 . . 1 6
12 Rubric - Categorization . . . 1 . 2
13 Rubric - Hardcoded Values . . . 1 . 4
14 Rubric - Content . . . 1 . 3
15 Rubric - Accuracy . . . 1 . 7
16 Rubric - Coverage . 1 . . 1 4
17 Rubric - Self-Containment . 1 . . 1 4
18 Rubric - Overfitting . 1 . . 1 7
19 Rubric - Atomicity . 1 . . 1 3
20 Rubric - Objectivity . 1 . . 1 5
21 Rubric - Framing . . . 1 . 2
22 Rubric - Redundancy . 1 . . 1 3
23 Rubric - Weight Share . . . 1 . 2
24 Rubric - Individual Criteria Weights . . . 1 . .
25 Rubric - Count . . . 1 . 1
26 Component: Rubric - Robustness . . . 1 . 1
27 Component: Rubric - Value Binding . . . 1 . 4
28 JSON - Structure / URL Integrity . . . 1 . 1

Detail
By submission
task_9
3 non-fail

Design & Creative · 28 of 28 components scored
Output contract issues

    02 sets blocked_on but claims high confidence
    08 sets blocked_on but claims high confidence
    09 sets blocked_on but claims high confidence
    11 sets blocked_on but claims high confidence

What the verdict rests on
The 3 rests on ten independent components, several of them near-objective (07 on literal "Thursday"/"last sprint" text, 22 on two named redundant pairs, 19 on three non-atomic criteria), so the verdict is not a single judgement call — but the 3-vs-2 boundary is thin in three places: 09's Score-3 rationale depends on a clipping check I have confirmed was measured wrong, 17 sits at 16.67% and hits its stated 20% fail threshold exactly if borderline criterion 11 counts, and 20 reports "4 of 22 = 18.2% if all three borderlines were counted" against its own 10% ceiling.

The mechanical verdict is 3 and, unusually, it is not fragile as a 3: ten of the 28 sit at the minimum, several on near-objective grounds (07 on literal "Thursday"/"last sprint" text, 22 on two named redundant pairs, 19 on three non-atomic criteria). The live question is whether this is really a 2, and it turns on one fact three components got wrong — the gold screenshot's 3D bomb IS clipped at the right edge of the game viewport, as component 10 reported and 09, 11 and 15 each denied. I confirmed it directly: bomb-body pixels run at full height to the game area's last column (png x=1320) and stop dead at the window chrome, with the sphere's right side and fuse sliced flat; the cause is arithmetic that both 09 and 10 recorded independently (a 370x370 SubViewport drawn unstretched from offset_left=930 in a ~1150px frame), which 09 wrote down before concluding "No finding." That leaves criterion 16 — weight 50, joint-heaviest of 30, inside the 64.9% visual block — anchored to a gold that does not show what it grades, hence the proposed re-runs of 09 (3 to 2) and 15 (5 to 3). Three further defect classes were each found by three or four components and routed to minor_issues by every one of them because no form option covers them: the four identical input_files URLs (09, 11, 28 — confirmed, all four are .../pwy5ipf5O1s2zNk with no dest field), criterion 30's ±0.64s tolerance against a log whose action lines carry no t= field (15, 18, 20, 27), and criteria 9 and 25's dependence on run-specific gold values (08, 15, 18, 27) — only 18 found an option that fit, and only for criterion 9. Finally, a coordination trap for whoever applies the fixes: 13, 19, 20 and 22 all prescribe splitting criteria, while 25 reports the rubric sits at exactly the 30-criterion ceiling with zero headroom — 19's proposed C11/C26 merge and 22's independent identification of C11/C26 as redundant solve each other, but only if the edits ship as one batch.
Fix order

    09 Gold File - Accuracy. Fix the gold project's 3D panel geometry and re-capture the screenshot. In TokenWave.tscn the SubViewport is size = Vector2i(370, 370) inside a SubViewportContainer laid out 185x185 at offset_left 930.0 / offset_right 1115.0, unstretched — so the rendered content reaches x=1300 in a ~1150px game area and the bomb is sliced flat at the frame edge. Set the SubViewport to 185x185 (or enable stretch on the container) and re-shoot bomb_blast_frame.png so the model sits whole inside a visible panel with clearance from the window edge. This is first because it is the live 3→2 escalation risk and it repairs criterion 16 (weight 50) for components 09, 15 and 26 in one edit.
    18 Rubric - Overfitting. Rewrite criterion 9 to drop the gold-run-specific quantity, using 18's own replacement: "`bomb_runtime_log.txt` contains at least one ACTION_TRANSITION line with origin=AUTO and at least one ACTION_TRANSITION line with origin=INPUT." The gold's 83 INPUT / 13 AUTO split comes from how the capture operator held the mouse, not from any input file. Second because this is the one unreachable graded value that a component could actually score, and clearing it also discharges the concerns 15, 27 and 08 each recorded with nowhere to put them.
    11 Component: Gold File - Input Consistency. Make the gold honour the locked timing value: change explosion_flash = 0.45 to 0.4 at both use sites in Bomb_Chain_Reaction_Working/scripts/token_wave.gd (line 90 and the radius term at line 177), so the project matches gameplay_config.txt's blast_expand_duration_s = 0.4. This single constant is the sole defect driving both 11's and 09's Score 3, so it must be fixed for either to reach 5. While there, either implement token_speed_cap_px_per_s = 1200 (a one-line velocity.limit_length) or drop the key from the config — 09, 10, 11 and 15 all flagged it as an unconsumed parameter.
    17 Rubric - Self-Containment. Move the artifact into the subject of criteria 12, 13, 14, 15 and 26, which currently read "Tokens...", "The blast...", "The board...", "Each collected token...", "Every live token..." against a bare "the corresponding expected file" anchor. 17's own suggested form: "`Bomb_Chain_Reaction_Godot_Project.zip` contains token-spawning logic that keeps the board populated, consistent with the expected `Bomb_Chain_Reaction_Godot_Project.zip`." Fourth because 17 is at 16.67% against a 20% fail bar and reaches exactly 20.00% if borderline criterion 11 is counted — the thinnest margin in the set. Rewriting criterion 11 and criterion 5 the same way (20's minor_issues groups "The ZIP"/"The project" with the same oblique-reference set) removes the knife-edge entirely.
    19 Rubric - Atomicity. Do the atomicity, redundancy and objectivity edits as ONE batch, because 25 reports the rubric sits at exactly 30 criteria with zero headroom and any naive split yields 31 = fail band. The batch that nets to 30: (a) merge criterion 11 into criterion 26 — this simultaneously clears 22's redundant Pair 2, which 22 identified independently, and frees the one slot needed; (b) split criterion 28's two unrelated clauses, fixing 19 and 20's single counted defect at once; (c) split the collection clause out of criterion 12, fixing 19's third finding; (d) delete criterion 16's "with a dedicated camera and at least two lights" clause — a deletion, needing no slot — since 12, 15, 17, 18 and 19 all separately note a PNG cannot evidence scene-graph node counts.
    22 Rubric - Redundancy. Clear redundant Pair 1 by narrowing criterion 8 to the span alone ("the span between the first and last t values is at least twelve seconds") and leaving sample-gap continuity and cadence to criterion 10, which already carries the ±10% band. This frees a second slot for rank 7.
    16 Rubric - Coverage. Add a criterion grading a physics VALUE, using the slot freed at rank 6 — e.g. "Token fall acceleration in the project in `Bomb_Chain_Reaction_Godot_Project.zip` matches the gravity value used in the corresponding expected file, within plus or minus 5 percent." The prompt states "gameplay_config.txt controls timing and physics" and both timing values are graded numerically (criteria 10 and 30), but no criterion grades gravity 38, damping 0.72 or blast force 360; a submission using gravity 300 and damping 0.2 passes every existing criterion. While in this area, fix criterion 30 as 15, 18, 20 and 27 each independently asked: its ±20% band is ±0.64s against a log whose ACTION_TRANSITION lines carry no t= field, so the gap is only readable at 1.0s granularity — the gold's own inferred gaps read [3,3,3,4,3,3,3,4,3,3,3,3], meaning the gold produces both pass and fail verdicts under its own criterion.
    04 Prompt - Realism. Reduce prescriptiveness: replace the literal template strings "MOTION_SAMPLE mechanic={id} t={seconds} first=({x},{y}) collected={n} actions={n}" and "ACTION_TRANSITION mechanic={id} origin=<AUTO|INPUT> count={n}" with prose naming the required fields. Note the tension 08 raised — criteria 6 and 7 grade "the prescribed telemetry format", so the format must stay specified somewhere or those criteria become unsatisfiable; prose that names every field and its order preserves both.
    07 Prompt - Timelessness. Remove the time anchors: "our Thursday gameplay review" (twice) and "our designer locked in last sprint" — e.g. "our upcoming gameplay review" and "that our designer locked in." Last because it is a two-word edit with no interaction with anything else, and 07 confirms neither reference affects the correct solution.

Escalation proposals

Proposed by the senior review pass and not applied. The verdict above uses the component scores as returned.

# Component Now Proposed Reasoning

09 Gold File - Accuracy 3 2 09's Score-3 band requires that "no graded value is wrong or unreachable" — its own stated Score-2 trigger. Criterion 16 (weight 50, joint-heaviest of 30, 9.1% of the 547 total and inside the 64.9% visual block that dominates this Design & Creative task) grades that bomb_blast_frame.png "shows a 3D bomb model rendered in its own viewport panel ... so that the silhouette and top surface of the model read clearly against the dark background, consistent with the corresponding expected file." The expected file shows a sphere sliced flat by the viewport boundary and no panel border. This is categorically different from the blast_expand_duration_s defect 09 correctly scored as 3: that one is an invisible constant no artifact reveals, whereas this one is visible in the delivered screenshot and sits on the rubric's heaviest criterion. The cause is arithmetic, no
15 Rubric - Accuracy 5 3 15 verified the camera/lights clause and the non-overlap clause, but not the clipping — it measured the bomb's extent and stopped at the board's right edge rather than checking the viewport's. Two of C16's clauses ("in its own viewport panel" and "the silhouette ... read[s] clearly") are not true of the expected file the criterion anchors to, which is exactly the assertion 15's Score-5 band excludes. I propose 3 conservatively because only one criterion is affected and I cannot see 15's percentage thresholds; the re-run should determine whether an inaccuracy on a weight-50 criterion crosses into its fail band.
Contradictions between components
Components Conflict
10, 09, 11, 15 Same artifact, same pixels, incompatible readings. I resolved it directly against files/expected/bomb_blast_frame.png: bomb-body pixels (RGB ~14-20 grey, distinct from the 16,25,34 navy background) number 37 at png x=1314, 25 at x=1318, 25 at x=1319 and 27 at x=1320 — the last column of the game viewport — then window chrome (27,27,27) begins at x=1321. There is no taper to zero; a rendered crop shows the sphere's right side and the fuse sliced flat against the boundary. 10 is correct. The layout arithmetic both 09 and 10 recorded independently predicts exactly this (930 + 370 = 1300 in a ~1150px-wide game area, ~150px off-screen), so this is not a close call — 09 wrote down the cause a
15, 27, 18, 08 This is the unreachable-graded-value pattern. 15 concedes the same facts inside its own text ("the log's 83 INPUT presses are run-dependent and fixed by no input") but records them as context because its two options do not name unreachability; 27 does the same; only 18 found an option that fit, and it fit only criterion 9 (1/30 = 3.3%, well under its 15% fail bar). Four components saw the defect and it moved one score by one band. Criterion 25 carries weight 15 and criterion 9 weight 10, so the exposure is real but not verdict-moving on its own.
09, 10, 15 The count matters because 09's Score-3-not-2 argument is explicitly that only one secondary value deviates and that it is "invisible in every delivered artifact." Two of 10's four extras (token_diameter_px, board_margin_right) are governed by the prompt's tie-break — "go with what the reference image shows" — and 11 verified the gold matches scene_reference.png to 0.1px, so those resolve in the gold's favour and 09's substantive conclusion survives. But 09's literal claim is false, and the residue is a genuine input-side inconsistency: the shipped gameplay_config.txt contains at least two values (token_speed_cap_px_per_s, token_diameter_px) t
Not verified

These components could not be settled from the available evidence. The defect classes they cover are unexamined.

    02 Whether the .glb's rendered geometry or embedded textures carry anything PII-relevant. 02 argues this is immaterial (glTF JSON carries no author/copyright field, buffer is geometry not image payload) and I see no reason to doubt that, but the asset was never seen.
    08 Whether the model rendered in the gold screenshot is in fact Bomb.glb. Establishes by reference only (UID resolution + byte-identity), never by sight. 08 is right that this bears on criterion 16 rather than on leakage.
    09 Mesh-level fidelity of the rendered bomb. Note this compounds with the confirmed clipping: the one asset nobody could view is the subject of the rubric's heaviest criterion, and the frame that shows it is cut.
    11 Whether the model's materials/geometry are consistent with the input. Byte-identity (md5 0be332d7…) is established; visual consistency is not.
    16 The only component below high confidence (medium). Its defect class — whether any PRIMARY ask is uncovered — is therefore the least-secured negative finding in the set. 16 concluded only a secondary ask (physics parameter values) is uncovered; if a primary ask were also uncovered this component would be a 2, and nothing else in the 28 independently checks primary-ask coverage.

Evidence

The submission as the review saw it. Everything below is embedded in this file.
30 criteria4 input files3 expected filesverifier agent_judge_multidomain Design & Creative
Prompt given to the agent

Rubric, 30 criteria, total weight 547
Input and expected file locations
Input files, extracted to text

Expected files, extracted to text

Precomputed checks

Raw result for each of the 28 components

Raw senior review result

Raw input-consistency result

All 28 component scores

An amber count beside a score means that component recorded unscored recommendations. 76 in total, listed below.
01 Task - Feasibility5
02 Task - PII / Safety35
03 Prompt - Clarity25
04 Prompt - Realism13
05 Prompt - GUI Integration5
06 Prompt - Output Naming5
07 Prompt - Timelessness13
08 Component: Prompt - Answer leakage35
09 Gold File - Accuracy73
10 Gold File - Format5
11 Component: Gold File - Input Consistency63
12 Rubric - Categorization25
13 Rubric - Hardcoded Values45
14 Rubric - Content35
15 Rubric - Accuracy75
16 Rubric - Coverage43
17 Rubric - Self-Containment43
18 Rubric - Overfitting73
19 Rubric - Atomicity33
20 Rubric - Objectivity53
21 Rubric - Framing25
22 Rubric - Redundancy33
23 Rubric - Weight Share25
24 Rubric - Individual Criteria Weights5
25 Rubric - Count15
26 Component: Rubric - Robustness15
27 Component: Rubric - Value Binding45
28 JSON - Structure / URL Integrity15
Findings

One row per component that scored below 5. Open a row for the reviewer's full reasoning.

# Component Score Label on the review form Finding

04 Prompt - Realism 3 [All] [All] [Non-Fail - Minor Prescriptive Prompt]
The prompt is natural and grounded, so it clears the Score 2 fail bar: it opens in a real first-person working voice ("Hi, I'm ...
07 Prompt - Timelessness 3 [All] [All] [Non-Fail - Minor Time-sensitivity]
The prompt contains mild time-sensitive framing — "our Thursday gameplay review" (used twice: at the opening and in "so the board ...
09 Gold File - Accuracy 3 [All] [All] [Non-Fail - Somewhat Inaccurate Gold File]
RECONSTRUCTED (reachable + correct): Inputs give the agent scene_reference.png (the stated visual authority) ...
11 Component: Gold File - Input Consistency 3 [All] [All] [Non-Fail - Input Consistency]
RECONSTRUCTED (core deliverable derives correctly). I traced every graded gold value to a named input and recomputed it. From ...
16 Rubric - Coverage 3 [All] [All] [Non-Fail - Coverage]
Crosses the score-3 threshold: at least one secondary request is not covered. The uncovered ask is that the physics parameters ...
17 Rubric - Self-Containment 3 [All] [All] [Non-Fail - Self-containment]
The task ships THREE expected files (Bomb_Chain_Reaction_Godot_Project.zip, bomb_runtime_log.txt, bomb_blast_frame.png), so ...
18 Rubric - Overfitting 3 [All] [All] [Non-Fail - Overfitting]
Band: <15% of criteria overfit (Non-Fail). Count: 1 of 30 criteria = 3.3%, under the 15% Fail threshold (15% of 30 = 4.5, so 5 ...
19 Rubric - Atomicity 3 [All] [All] [Non-Fail - Minor Atomicity Issues]
3 of 30 criteria (10.0%) are non-atomic, which is at or below the 15% bar for score 3 and above the zero required for score 5 ...
20 Rubric - Objectivity 3 [All] [All] [Non-Fail - Objectivity]
Band: Non-Fail. 1 of 22 non-visual criteria (4.5%) is loosely worded but still reasonably gradable, which is at or under the 10% ...
22 Rubric - Redundancy 3 [All] [All] [Non-Fail - Redundancy]
Crosses the score-3 threshold ("One or two redundant or overlapping pairs exist; scoring impact is minimal, i.e., there are still ...
Value criteria that one input answers in full

1 of 4 groups of value criteria have one supplied input that prints every value they grade, text values such as material names included. A response that copies that input passes the whole group without doing the task. Recorded by component 27, Value Binding.
Criteria Input that prints all their values
17, 19, 20, 21, 22, 25 files/inputs/scene_reference.png (single 1152x648 frame) — prints every value this subgroup grades: the yellow coin token art, the framed play area divided into four row zones by three internal grid lines, the bottom COLLECT strip with its label right-of-centre, the title "TD 2D • BOMB", and the left HUD column wording and line breaks (BOMB / Collected: N / Actions: N / SPACE / CLICK / trigger mechanic / Automatic preview / runs every cycle.). Renaming this input to bomb_blast_frame.png would carry all six. The output file is defended by criteria 16 and 18 below.
16, 18 none
6, 7, 8, 9, 10, 24, 27, 28, 29, 30 none
11, 12, 13, 14, 15, 23, 26 none
Recommendations, not scored
76 to fix, 35 on components that scored 5

None of these changes a score, a label or the verdict. The review form has no answer option that describes them, so the component passes and the work is still outstanding. Treat this as the pre-submission list. Open a row for the full text of its recommendations. An entry printed in bold is a hard gate elsewhere in the project — still unscored here, and the first thing to fix.

# Component Score What to fix

02 Task - PII / Safety 5
3 items. Not PII and not scored here: bomb_blast_frame.png carries a C2PA content-credentials manifest stating 'Claude provided ...

03 Prompt - Clarity 5
2 items. "Each collected token raises the collected counter and each trigger raises the actions counter" appears in the sentence ...

04 Prompt - Realism 3
The telemetry format section (curly-brace/angle-bracket template syntax) is the single most spec-like portion of the ...

07 Prompt - Timelessness 3
The Thursday/last-sprint framing is harmless flavor text but could be tightened to fully static phrasing (e.g. 'our ...

08 Component: Prompt - Answer leakage 5
3 items. Not leakage, for the criteria-quality component: the expected log's first 11 seconds record 54 origin=INPUT triggers ...

09 Gold File - Accuracy 3
7 items. CLOSE CALL (not flagged) — gameplay_config.txt [physics] sets 'token_speed_cap_px_per_s = 1200' and no clamp exists ...

11 Component: Gold File - Input Consistency 3
6 items. gameplay_config.txt [physics] sets "token_speed_cap_px_per_s = 1200" and the gold project implements no speed cap ...

12 Rubric - Categorization 5
2 items. Not a categorisation defect, non-scoring. Criterion 16 names bomb_blast_frame.png as the artifact but requires "a ...

13 Rubric - Hardcoded Values 5
4 items. Comparison mode not stated — criterion 17, bundle.json criteria[16]: "bomb_blast_frame.png shows board tokens matching ...

14 Rubric - Content 5
3 items. Criteria 6, 7 and 9 would read more cleanly if they led with the content test rather than with 'contains'/'appear'; the ...

15 Rubric - Accuracy 5
7 items. Criterion 28 says the collected value must be "internally consistent with the collection events recorded in the same ...

16 Rubric - Coverage 3
4 items. Criterion 23 grades only the alternating offset sub-element of the initial layout ("arranges initial board tokens with ...

17 Rubric - Self-Containment 3
4 items. Criteria 12, 13, 14, 15 and 26 would become fully self-contained by moving the artifact into the subject and naming the ...

18 Rubric - Overfitting 3
7 items. Criterion 25 wording: "reproduces the exact wording and line breaks of the corresponding expected file" is anchored to ...

19 Rubric - Atomicity 3
3 items. C23 is tagged category visual but is scoped to Bomb_Chain_Reaction_Godot_Project.zip and grades how the project source ...

20 Rubric - Objectivity 3
5 items. Conditional wording (not scored) - criterion 30 is the only conditional criterion: "During periods in ...

21 Rubric - Framing 5
2 items. Criterion 30 scopes its check with a conditional-style clause ("During periods in bomb_runtime_log.txt where ...

22 Rubric - Redundancy 3
3 items. Criterion 28 grades two independent elements in one line (the first=(x,y) field and the collected field). It could be ...

23 Rubric - Weight Share 5
2 items. Correctness sits at 29.43%, only 0.57pp under the 30% ceiling of the Design & Creative band — raising any single ...

25 Rubric - Count 5
The rubric sits exactly on the ceiling of the allowed band (bundle.json -> mechanical.25_rubric_count: "n_criteria" ...

26 Component: Rubric - Robustness 5
Criterion 19 is the only visual criterion with no expected-file anchor; its "legible" clause alone discharges this ...

27 Component: Rubric - Value Binding 5
4 items. Criterion 30 grades a value the graded artifact has no field for: ACTION_TRANSITION lines carry no timestamp ...

28 JSON - Structure / URL Integrity 5
All four input_files entries share the identical S3 URL (pwy5ipf5O1s2zNk) despite being four distinct files ...

Glossary
Terms used above
Term Meaning
Expected file The answer key a contributor builds. The grading model compares an agent's output to it. The review form calls it the gold file.
Criterion One scored line in the contributor's rubric. A submission's rubric holds 10 to 30 of them, each with a weight.
Format gate, correctness, visual The three categories a criterion can carry. Weight is expected to sit in a set share per category.
Must-pass A criterion tag reserved for file existence and file extension.
Verifier The JSON that maps the expected files and the agent's output paths for grading.
Unreachable value A value in an expected file that cannot be produced from the inputs the agent receives. Any criterion graded against it cannot be satisfied.
Escalation A proposal from the senior review pass to lower a component score. Not applied to the verdict.
Recommendation A real defect that no component's answer options describe, so it cannot be scored. It never changes a score, a label or the verdict, and it appears even where the component scored 5.

Appendix
The 28 component definitions

Each is generated from the audit rubric and is what the review for that component was given. Included so a score can be checked against the form it was scored on.
01 task feasibility

# 01. Task - Feasibility

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

|                 |                                        |
| --------------- | -------------------------------------- |
| audit-rubric id | `58db686e-d16d-413e-8e83-e54feb9ca6de` |
| title           | Task - Feasibility                     |
| allowed scores  | 2, 5                                   |
| required        | true                                   |
| evidence class  | `other`                                |
| subagent model  | `claude-sonnet-5` at `--effort max`    |

## Question

Rate the Feasibility of the Task dimension.

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- Infeasibility is concrete and nameable: software that is not installed on the VM, a login or credential the agent cannot hold, a captcha, or a step the VM physically cannot perform. Name which one, and name the application the task would have needed.
- A browser lookup to a **stable public authority** for a historical fact is ordinary CUA work and is feasible. Do not read it as an infeasible external dependency.

### Score 2 — **justification REQUIRED**

[Fail - Infeasible Prompt]
The task cannot be completed in the VM, e.g., needs software that's not installed
**Applies to this score.**

- Quote the step you say cannot run and the capability it needs. `agent_issue_details` recording a real environment failure is evidence; your own doubt about difficulty is not.

### Score 5 — justification not required

The task is fully feasible.

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - Infeasible Prompt]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Evidence to read

- `bundle.json` -> `prompt`, `seed_prompt`, `applications_used`
- `bundle.json` -> `input_files[]`, `verifier`, `mechanical`
- `bundle.json` -> `agent_issue_details` — often records a real environment failure

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:
{
"component_id": "58db686e-d16d-413e-8e83-e54feb9ca6de",
"title": "Task - Feasibility",
"score": <one of: 2, 5>,
"error_category": "<verbatim from the list above, or null>",
"justification": "<required when the chosen score says so>",
"evidence": "<quote the exact text, value, cell or filename>",
"criteria": [<rubric criterion numbers, if applicable>],
"confidence": "high|medium|low",
"blocked_on": "<what you could not verify, or null>",
"minor_issues": ["<non-scoring suggestion>", "..."]
}
Rules:

- Score **only** from the options above. The clean-pass score is `5`.
- A score whose option is marked **justification REQUIRED** must carry a non-empty `justification` naming the threshold it crosses and the evidence it rests on.
- Quote evidence. A finding with no quoted text, value or filename is not a finding — score the clean pass instead.
- If you could not verify something (a file would not open, an artifact is unavailable), set `blocked_on` and lower `confidence`; do not guess.
- Judge **this** submission only. Any reviewer score or feedback in the task response was written about the PREVIOUS attempt and does not apply here — ignore it.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.
- Record in `minor_issues` any of the following you find. Each entry quotes its evidence, names the file or criterion, and states the fix:
  - **Domain fit and expertise level** — the task really tests a different profession than its `domain` / `sub_domain` claims, or someone with only basic subdomain knowledge could complete it. Fit is carried by who is asking and the work context, not by the deliverable's genre, so do not record this merely because the output format is unexpected. Keep the opening phrase as written: this defect is a hard gate elsewhere in the project, so the report prints the whole entry in bold. It still does not affect your score.
  - **Thin complexity** — the task is retrieval or reorganisation rather than professional judgment, multi-step execution, cross-file reasoning, calculation or transformation. Keep the opening phrase as written: this defect is a hard gate elsewhere in the project, so the report prints the whole entry in bold. It still does not affect your score.

02 task pii safety

# 02. Task - PII / Safety

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

|                 |                                        |
| --------------- | -------------------------------------- |
| audit-rubric id | `6da062ea-94f1-4e13-86f5-9763145509aa` |
| title           | Task - PII / Safety                    |
| allowed scores  | 2, 4, 5                                |
| required        | true                                   |
| evidence class  | `files`                                |
| subagent model  | `claude-opus-5` at `--effort max`      |

## Question

Rate the PII / Safety of the Task dimension.

## Description (verbatim from the CSV)

PII types:
Real non-famous people
| - Contact info
| - Financial info
| - Other sensitive personal details.

Flag names as PII only when paired with sensitive data (e.g., names alongside phone numbers or SSNs). If the PII is hard to trace, a score of 3 [Fail - Minor PII Violation] is acceptable since synthetic data is also allowed.

Standalone names, authors, or usernames (even in the task's metadata) are fine.

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- A name is PII only when **paired with sensitive data** — a name beside a phone number, an address, an SSN, an account or a medical detail. A standalone name, author or username is not PII, including in the task's own metadata.
- PII can sit in the input and expected files, not only the prompt. Check `inputs_extracted.md` and `expected_extracted.md` as well.
- **Minor PII is score 4 — one band, one value.** The CSV describes this band three ways: the description says "a score of 3 `[Fail - Minor PII Violation]`", the option is score **4** labelled `[Non-Fail - Minor PII Violation]`, and `errorCategories` lists `[All] [All] [Fail - Minor PII Violation]`. `references/source-conflicts.md` §7 resolves it: the option text wins, minor PII is **Non-Fail at 4**. There is no score 3 on this component. Emit the only minor label the form lists — `[All] [All] [Fail - Minor PII Violation]` — verbatim despite its wording, and say in `justification` that the band is Non-Fail.

### Score 2 — **justification REQUIRED**

[Fail - PII Violation]
The task contains any major instance of PII.
**Applies to this score.**

- Name the field, the file and the location, and state the redaction or synthetic substitute that would remove it.

### Score 4 — justification not required

[Non-Fail - Minor PII Violation]
The task contains any minor instance of PII. For instance, synthetic names or data that is hard to trace back/verify.
**Applies to this score.**

- Synthetic names, or data that is hard to trace back or verify, belong here. Synthetic data is permitted, so say what would remove it rather than escalating. This is a **non-fail** band despite the label's wording.

### Score 5 — justification not required

The task does not contain any instance of PII.

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Fail - PII Violation]`
- `[All] [All] [Fail - Minor PII Violation]`

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
{
"component_id": "6da062ea-94f1-4e13-86f5-9763145509aa",
"title": "Task - PII / Safety",
"score": <one of: 2, 4, 5>,
"error_category": "<verbatim from the list above, or null>",
"justification": "<required when the chosen score says so>",
"evidence": "<quote the exact text, value, cell or filename>",
"criteria": [<rubric criterion numbers, if applicable>],
"confidence": "high|medium|low",
"blocked_on": "<what you could not verify, or null>",
"minor_issues": ["<non-scoring suggestion>", "..."]
}
Rules:

- Score **only** from the options above. The clean-pass score is `5`.
- A score whose option is marked **justification REQUIRED** must carry a non-empty `justification` naming the threshold it crosses and the evidence it rests on.
- Quote evidence. A finding with no quoted text, value or filename is not a finding — score the clean pass instead.
- If you could not verify something (a file would not open, an artifact is unavailable), set `blocked_on` and lower `confidence`; do not guess.
- Judge **this** submission only. Any reviewer score or feedback in the task response was written about the PREVIOUS attempt and does not apply here — ignore it.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.

03 prompt clarity

# 03. Prompt - Clarity

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

|                 |                                        |
| --------------- | -------------------------------------- |
| audit-rubric id | `f42591e3-1f2a-4eee-9089-7a1d785d2e8b` |
| title           | Prompt - Clarity                       |
| allowed scores  | 2, 3, 5                                |
| required        | true                                   |
| evidence class  | `other`                                |
| subagent model  | `claude-sonnet-5` at `--effort max`    |

## Question

Rate the Clarity of the Prompt dimension.

## Description (verbatim from the CSV)

The task must be verifiable and objective; avoid open-ended queries.

The prompt must align with all valid states the paired verifier/rubric will accept—no more, no less.

Do not fail for ambiguity when a predominant interpretation exists, or when an ambiguous element wouldn't manifest as verifier misalignment.

Minor typos are OK, provided that the intention is very obvious.

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- A typo in a **key identifier** — a column name, a filename, a setting value — changes the interpretation and is a clarity defect. An ordinary typo whose intent is obvious is not.
- A pointer must resolve to exactly one thing. "page 5 of the baseline package" is ambiguous when the printed pagination and the file's own page index disagree; a trailing "etc." is not a specification; "title it `waste_report.docx`" conflates the document title with the filename.
- Do not score down for ambiguity where a predominant reasonable reading exists, or where the ambiguous element would not show up as verifier misalignment.

### Score 2 — **justification REQUIRED**

[Fail - Major Clarity / Specificity Issues]
The prompt is overly vague, and the goal is indeterminable.
**Applies to this score.**

- Reserve for a goal that is genuinely indeterminable. Quote the text and state the two readings that would produce differently graded artifacts.
- **Solution space**, in its severe form. The CSV opens this component with "the task must be verifiable and objective; avoid open-ended queries", so a prompt establishing a solution space for which **no objective rubric of a correct answer could be written** takes this option — the goal is indeterminable in the sense that matters. Asking for reasoned professional opinion is _not_ this: an opinion deliverable bounded by an explicit decision rule is gradable and scores 5.

### Score 3 — justification not required

[Non Fail - Minor Clarity / Specificity Issues]
The prompt is solvable with only one valid interpretation but could be clearer; the agent might need to make a very small, reasonable assumption.
**Applies to this score.**

- Solvable with one valid interpretation, but the agent has to make a small, reasonable assumption. This is the band for genuine but minor ambiguity.
- **Solution space**, in its milder form: the solution space is loose enough that two competent submissions would be graded differently, but a defensible rubric could still be written. Score it here and say what decision rule would bound it.
- **Unnamed input files.** The prompt refers to its inputs only obliquely ("the attached data"), so the agent must work out which file feeds which requirement and a reviewer cannot confirm it did. That is a small, reasonable assumption forced on the agent, so it lands in this band. The fix is to name each input file in the prompt — naming them is correct practice and is never a defect under component 04.

### Score 5 — justification not required

The prompt is clear, and the goal is apparent; the agent does not need to make assumptions.

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[Prompt] [Prompt Clarity/ Specificity] [Non-Fail Minor Clarity / Specificity Issues]`
- `[Prompt] [Prompt Clarity/ Specificity] [Fail - Major Clarity / Specificity Issues]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Multiple valid interpretations

An ambiguity matters when it changes the graded output. For each element of the request that could be read more than one way, list the defensible readings, then decide whether they produce _different_ artifacts that `criteria[]` would score differently. If two competent submissions following different valid readings would be graded differently, the ambiguity is consequential and belongs in your score; if every valid reading converges on the same graded content, it does not. Where a method, statistic or convention is left unspecified and several standard choices give different numbers, that is consequential by definition.

Judge the request as the agent receives it. A supplied template or example file may narrow a reading, but only if it is unambiguous on the point in question; do not treat an attachment as curing an ambiguity it does not actually settle.

## Evidence to read

- `bundle.json` -> `prompt`, `seed_prompt`, `applications_used`
- `bundle.json` -> `input_files[]`, `verifier`, `mechanical`
- `bundle.json` -> `agent_issue_details` — often records a real environment failure

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:
{
"component_id": "f42591e3-1f2a-4eee-9089-7a1d785d2e8b",
"title": "Prompt - Clarity",
"score": <one of: 2, 3, 5>,
"error_category": "<verbatim from the list above, or null>",
"justification": "<required when the chosen score says so>",
"evidence": "<quote the exact text, value, cell or filename>",
"criteria": [<rubric criterion numbers, if applicable>],
"confidence": "high|medium|low",
"blocked_on": "<what you could not verify, or null>",
"minor_issues": ["<non-scoring suggestion>", "..."]
}
Rules:

- Score **only** from the options above. The clean-pass score is `5`.
- A score whose option is marked **justification REQUIRED** must carry a non-empty `justification` naming the threshold it crosses and the evidence it rests on.
- Quote evidence. A finding with no quoted text, value or filename is not a finding — score the clean pass instead.
- If you could not verify something (a file would not open, an artifact is unavailable), set `blocked_on` and lower `confidence`; do not guess.
- Judge **this** submission only. Any reviewer score or feedback in the task response was written about the PREVIOUS attempt and does not apply here — ignore it.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.

04 prompt realism

# 04. Prompt - Realism

> Generated from this skill's `audit-rubric.csv` by `_generate.py`. Do not hand-edit; edit the CSV and regenerate.

|                 |                                        |
| --------------- | -------------------------------------- |
| audit-rubric id | `c651259f-9eb4-4a33-98db-0775ac9e56c9` |
| title           | Prompt - Realism                       |
| allowed scores  | 2, 3, 5                                |
| required        | true                                   |
| evidence class  | `other`                                |
| subagent model  | `claude-sonnet-5` at `--effort max`    |

## Question

Rate the Realism of the Prompt dimension.

## Description (verbatim from the CSV)

The prompt should read like something a real person would write—wording, rhythm, minor spelling errors, and detail matching a normal working session.
It should carry a light layer of context—who is asking, their role/stack, the constraint shaping the ask, etc.—and make the motivation for the expected files visible.

Stripped-of-context, templated prompts are the failure mode this dimension catches.

Watch for the V3 anti-patterns:
Rubric-style language ("treat X as fixed," "do not use outside sources")
| - Artificial personas ("You are a finance manager")
| - Excessive "must/only/exactly"
| - Robotic file references ("extract data from file A and file B").

## Score options

Only these scores exist for this component. There is no other value; in particular do not invent a score the CSV does not list.

**Before you score.** The notes below are calibration carried over from the deployed reference evals. They say how the options that follow are applied — they never add an option, move a threshold, or create a band the CSV does not list. Where the two sources genuinely conflict, the CSV wins and the rule is left out, so everything below is safe to apply as written.

- **Naming input files is correct practice and is never a defect on this component.** A prompt that refers to its inputs by name — "work from `Q3_returns.xlsx` and the field notes in `site_survey.pdf`" — is doing what the project requires: named inputs are what make a task verifiable and what let a reviewer confirm the prompt, the files and the rubric describe the same task. Never read that as robotic, unnatural or templated, and never count it toward this component at any band.
- **The "robotic file references" anti-pattern is narrowed to its mechanical form**: a bare "extract data from file A and file B" instruction carrying no context, no motivation and no working situation. Filenames _plus_ context are not it. The reverse is the real concern, and it belongs to component 03: a prompt that never names any input, describing them only as "the attached data".
- Prescriptiveness is overwhelmingly the middle band. In the observed defect distribution it carries five warnings and **zero** failures, so detail alone is score 3 and the fail option stays rare.
- Domain fit is carried by who is asking and the work context they are in, not by the deliverable's genre. An unexpected output genre is not an unnatural prompt.

### Score 2 — **justification REQUIRED**

[Fail - Unnatural Prompt]
The prompt is overly synthetic/templated without a realistic framing, i.e., the "why".
| The prompt reads as a raw test case a real user would never write.
| The prompt is overly prescriptive—excessive step-by-step guidance or exact section-title checklists that overfit the output / reveal verifier logic.
**Applies to this score.**

- Before taking this option, confirm the prompt is genuinely rubric-shaped in one of these specific ways: output-by-output enumeration, an exact section-title checklist, a step-by-step statement of the internal algorithm, or leaked verifier logic. Quote the enumeration or checklist you object to.

### Score 3 — **justification REQUIRED**

[Non-Fail - Minor Prescriptive Prompt]
The prompt is natural and grounded but is somewhat prescriptive—there's more procedural detail than a real user would typically write, but not to the extent of leaking verifiers or overfitting output.
**Applies to this score.**

- More procedural detail than a real user would write, without leaking the verifier or overfitting the output. A prompt that is merely detailed, or that states necessary constraints, lands here.

### Score 5 — justification not required

The prompt is natural, grounded, and conveys a realistic user context.

## errorCategories

The label a reviewer selects. Emit one of these verbatim in `error_category` when the score is not the clean pass, else `null`.

- `[All] [All] [Non-Fail - Minor Prescriptive Prompt]`
- `[All] [All] [Fail - Unnatural Prompt]`

**One band, one value.** Where the score you chose has no matching label — several components define a non-fail score but list only a `Fail` entry — emit `null` and name the band in `justification`. Never emit a `Fail` label on a non-fail score: the label is what reaches the reviewer's CSV, and a mislabelled non-fail reads there as a failure.

## Overlap with the rubric is not evidence

The rubric is written from the prompt, so prompt wording matching criterion wording is the expected direction of causation, not proof the prompt was reverse-engineered from the verifier. Do not compare prompt text against the criteria for this component. Score the prompt's own register only: artificial personas, rubric vocabulary, stacked must/only/exactly, robotic file references, and whether a real person's motivation is visible. `prompt_changes_made` is authoring history and says nothing about the prompt an agent receives.

## Evidence to read

- `bundle.json` -> `prompt`, `seed_prompt`, `applications_used`
- `bundle.json` -> `input_files[]`, `verifier`, `mechanical`
- `bundle.json` -> `agent_issue_details` — often records a real environment failure

Every path above is relative to the evidence directory named in the prompt. Read nothing outside it.

## Output contract

Return exactly one JSON object:
{
"component_id": "c651259f-9eb4-4a33-98db-0775ac9e56c9",
"title": "Prompt - Realism",
"score": <one of: 2, 3, 5>,
"error_category": "<verbatim from the list above, or null>",
"justification": "<required when the chosen score says so>",
"evidence": "<quote the exact text, value, cell or filename>",
"criteria": [<rubric criterion numbers, if applicable>],
"confidence": "high|medium|low",
"blocked_on": "<what you could not verify, or null>",
"minor_issues": ["<non-scoring suggestion>", "..."]
}
Rules:

- Score **only** from the options above. The clean-pass score is `5`.
- A score whose option is marked **justification REQUIRED** must carry a non-empty `justification` naming the threshold it crosses and the evidence it rests on.
- Quote evidence. A finding with no quoted text, value or filename is not a finding — score the clean pass instead.
- If you could not verify something (a file would not open, an artifact is unavailable), set `blocked_on` and lower `confidence`; do not guess.
- Judge **this** submission only. Any reviewer score or feedback in the task response was written about the PREVIOUS attempt and does not apply here — ignore it.
- `minor_issues` is **never scored**. It carries suggestions that would improve the task but that this component's answer options do not name, so nothing you put there may change `score`, `error_category` or the verdict — and a clean pass stays a clean pass with entries in it. Use `[]` when there is nothing to record.

05 prompt gui integration

06 prompt output naming

07 prompt timelessness

08 prompt answer leakage

09 gold file accuracy

10 gold file format

11 gold file input consistency

12 rubric categorization

13 rubric hardcoded values

14 rubric content

15 rubric accuracy

16 rubric coverage

17 rubric self containment

18 rubric overfitting

19 rubric atomicity

20 rubric objectivity

21 rubric framing

22 rubric redundancy

23 rubric weight share

24 rubric individual criteria weights

25 rubric count

26 rubric robustness

27 rubric value binding

28 json structure url integrity

senior review pass

input file consistency pass

Component definitions generated from the CUA v3 audit rubric. Scores as returned by the per-component review; the verdict is the lowest of the 28.

what the heck is acutally going on?

its just keep getting worse/?
