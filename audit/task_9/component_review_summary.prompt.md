UNIT UNDER REVIEW: task_9

AUDIT DATA. This is the only input: the task's prompt and criteria, every
component result a fix can come from, every recommendation, the senior
review and the input-consistency result. Every item a fix can come from
carries an id; cite those ids in `sources`.

{
 "unit": "task_9",
 "domain": "Design & Creative",
 "sub_domain": "Game Designer",
 "verdict": 2,
 "band": "FAIL",
 "components_run": 28,
 "files": [
  {
   "name": "bundle.json",
   "class": "bundle"
  },
  {
   "name": "rubric.json",
   "class": "rubric"
  },
  {
   "name": "prompt.md",
   "class": "prompt"
  },
  {
   "name": "source_coin_token.png",
   "class": "input"
  },
  {
   "name": "Bomb.glb",
   "class": "input"
  },
  {
   "name": "scene_reference.png",
   "class": "input"
  },
  {
   "name": "gameplay_config.txt",
   "class": "input"
  },
  {
   "name": "Bomb_Chain_Reaction_Godot_Project.zip",
   "class": "gtf"
  },
  {
   "name": "bomb_runtime_log.txt",
   "class": "gtf"
  },
  {
   "name": "bomb_blast_frame.png",
   "class": "gtf"
  }
 ],
 "prompt": "Hi, I'm putting together a playable prototype for our Thursday gameplay review and I need it built in Godot so the team can run it themselves instead of watching a capture.\n\nFour files are already on the Desktop. source_coin_token.png is the production coin face that every board token has to carry. Bomb.glb is the bomb model our 3D artist delivered. scene_reference.png is the signed-off screen from our art director. gameplay_config.txt has the timing, physics and board parameters that our designer locked in last sprint.\n\nThe reference image is the visual authority for this build. Treat it as the spec, not loose inspiration: match the framed play area with its internal grid lines, how the tokens sit on the board row by row including the alternating horizontal offset between rows, the collection strip along the bottom edge and where its label sits, the title across the top, and the HUD column on the left with its exact wording and line breaks. gameplay_config.txt controls timing and physics. Where the config file and the reference image disagree on a visual element like row count or token arrangement, go with what the reference image shows.\n\nPressing Space or clicking triggers a single radial blast from the middle of the board that pushes every token outward along its own trajectory. Tokens fall under gravity, bounce off the inner walls of the frame, and get collected once they cross the collection strip. Each collected token raises the collected counter and each trigger raises the actions counter. The blast also fires automatically on the repeating cycle defined in gameplay_config.txt so the board never sits idle during the review. The board keeps itself populated so it never empties out.\n\nBomb.glb has to be rendered live as an actual 3D object while the scene runs, in its own viewport panel placed beside the board in the empty area to its right. It needs a dedicated 3D camera and at least two lights positioned so that both the silhouette and the top surface of the model read clearly against the dark background. This is a live 3D preview, not a still image, and it must not overlap the framed play area.\n\nWhile the scene runs, print one telemetry line at the sample interval from gameplay_config.txt in the form\n\nMOTION_SAMPLE mechanic={id} t={seconds} first=({x},{y}) collected={n} actions={n}\n\nand one line every time the blast fires, in the form\n\nACTION_TRANSITION mechanic={id} origin=<AUTO|INPUT> count={n}\n\nwhere {id} is the mechanic identifier from gameplay_config.txt and origin tells apart the automatic cycle from a player trigger.\n\nThree things for me, all saved to the Desktop. The complete editable project as Bomb_Chain_Reaction_Godot_Project.zip, containing project.godot and every scene, script and local asset needed to open and run it with no missing dependencies. A screenshot of the running game as bomb_blast_frame.png, taken at a moment when the blast ring is still expanding and the HUD counters are legible, with the 3D bomb panel visible in the same frame. And the captured console output as bomb_runtime_log.txt, covering at least twelve continuous seconds of play and containing both an automatic and a player-triggered action line.",
 "criteria": [
  {
   "n": 1,
   "title": "Output includes a valid .zip file named `Bomb_Chain_Reaction_Godot_Project.zip`.",
   "weight": 5,
   "category": "format_gate",
   "type": "MUST-PASS"
  },
  {
   "n": 2,
   "title": "Output includes a screenshot file named `bomb_blast_frame.png`.",
   "weight": 5,
   "category": "format_gate",
   "type": "MUST-PASS"
  },
  {
   "n": 3,
   "title": "Output includes a console log file named `bomb_runtime_log.txt`.",
   "weight": 5,
   "category": "format_gate",
   "type": "MUST-PASS"
  },
  {
   "n": 4,
   "title": "`Bomb_Chain_Reaction_Godot_Project.zip` is a valid archive containing a `project.godot` file.",
   "weight": 8,
   "category": "format_gate",
   "type": "REGULAR"
  },
  {
   "n": 5,
   "title": "The ZIP includes scene, script, and asset files so the project can open with no missing dependencies.",
   "weight": 8,
   "category": "format_gate",
   "type": "REGULAR"
  },
  {
   "n": 6,
   "title": "`bomb_runtime_log.txt` contains MOTION_SAMPLE lines in the prescribed telemetry format, matching the corresponding expected file.",
   "weight": 8,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 7,
   "title": "`bomb_runtime_log.txt` contains ACTION_TRANSITION lines with origin=AUTO or origin=INPUT in the prescribed format, matching the corresponding expected file.",
   "weight": 8,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 8,
   "title": "`bomb_runtime_log.txt` records a continuous sequence of MOTION_SAMPLE lines with no missing samples between the first and last recorded t value, and that span is at least twelve seconds long.",
   "weight": 12,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 9,
   "title": "`bomb_runtime_log.txt` includes at least one origin=AUTO action line and at least one origin=INPUT action line.",
   "weight": 10,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 10,
   "title": "Consecutive MOTION_SAMPLE lines in `bomb_runtime_log.txt` advance t at the same regular sampling interval used in the corresponding expected file, within plus or minus 10 percent of that interval.",
   "weight": 8,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 11,
   "title": "The project implements a radial blast from the board center triggered by Space or click, consistent with the corresponding expected file. Alternative implementations that produce the same outward dispersal are accepted.",
   "weight": 8,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 12,
   "title": "Tokens fall under gravity, bounce off inner frame walls, and are collected at the collection strip, consistent with the corresponding expected file.",
   "weight": 6,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 13,
   "title": "The blast fires automatically on a fixed repeating cycle so the board never sits idle, consistent with the corresponding expected file.",
   "weight": 5,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 14,
   "title": "The board repopulates tokens so it never empties out, consistent with the corresponding expected file.",
   "weight": 15,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 15,
   "title": "Each collected token increments the collected counter and each trigger increments the actions counter, consistent with the corresponding expected file.",
   "weight": 10,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 16,
   "title": "`bomb_blast_frame.png` shows a 3D bomb model rendered in its own viewport panel to the right of the board, not overlapping the play area, with a dedicated camera and at least two lights so that the silhouette and top surface of the model read clearly against the dark background, consistent with the corresponding expected file.",
   "weight": 50,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 17,
   "title": "`bomb_blast_frame.png` shows board tokens rendered as yellow oval coins matching the token appearance in the corresponding expected file",
   "weight": 40,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 18,
   "title": "`bomb_blast_frame.png` shows a large colored ring shape centered on the board, consistent with the corresponding expected file.",
   "weight": 50,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 19,
   "title": "`bomb_blast_frame.png` shows the HUD counters legible in a column on the left, with no text clipped, truncated, or overlapping another element.",
   "weight": 40,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 20,
   "title": "`bomb_blast_frame.png` shows a framed play area with internal grid lines, consistent with the corresponding expected file.",
   "weight": 45,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 21,
   "title": "`bomb_blast_frame.png` shows a collection strip along the bottom edge with its label, consistent with the corresponding expected file.",
   "weight": 40,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 22,
   "title": "`bomb_blast_frame.png` shows a title across the top of the scene, consistent with the corresponding expected file.",
   "weight": 40,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 23,
   "title": "`bomb_blast_frame.png` shows a play area divided by horizontal grid lines into the same number of row zones as the corresponding expected file, with proportional row spacing and overall grid dimensions consistent with the corresponding expected file.",
   "weight": 50,
   "category": "visual",
   "type": "REGULAR"
  },
  {
   "n": 24,
   "title": "The actions value in the MOTION_SAMPLE lines of `bomb_runtime_log.txt` never decreases and agrees with the count of the most recent preceding ACTION_TRANSITION line.",
   "weight": 10,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 25,
   "title": "The HUD text in `bomb_blast_frame.png` reproduces the exact wording and line breaks of the corresponding expected file.",
   "weight": 15,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 26,
   "title": "Every live token on the board receives its own outward radial trajectory away from the board center when a blast fires, matching the corresponding expected file.",
   "weight": 12,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 27,
   "title": "`bomb_runtime_log.txt` records exactly one sequential ACTION_TRANSITION line for every automatic or input blast, with count increasing by one each time and no skipped values.",
   "weight": 10,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 28,
   "title": "In every MOTION_SAMPLE line of `bomb_runtime_log.txt`, the first=(x,y) coordinates are well-formed and reflect live token movement consistent with the outward blast, gravity and wall collisions, and the collected value is internally consistent with the collection events recorded in the same log.",
   "weight": 8,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 29,
   "title": "Each ACTION_TRANSITION line in `bomb_runtime_log.txt` carries an origin value that matches the trigger-source mapping used in the corresponding expected file.",
   "weight": 8,
   "category": "correctness",
   "type": "REGULAR"
  },
  {
   "n": 30,
   "title": "During periods in `bomb_runtime_log.txt` where consecutive origin=AUTO lines appear with no intervening origin=INPUT lines, the time gap between those AUTO events matches the corresponding gap in the expected file, within plus or minus 20 percent.",
   "weight": 8,
   "category": "correctness",
   "type": "REGULAR"
  }
 ],
 "components": [
  {
   "id": "C01",
   "component": "01",
   "title": "Task - Feasibility",
   "score": 5,
   "error_category": null,
   "confidence": "medium",
   "blocked_on": "bundle.json has applications_used: null and does not state that Godot is installed on the CUA VM. Feasibility rests on the prompt naming Godot as the target and on the expected artifacts existing. Whether the reference project was produced on the VM itself is unverified, since the zip contains __MACOSX entries.",
   "justification": "No concrete infeasibility found. The task needs Godot (with 3D SubViewport support), a way to capture a screenshot and console output, and a zip utility. bundle.json has no agent_issue_details recording an environment failure, and no login, captcha or credential is required. All four inputs are local Desktop files, and every output goes to the Desktop. The expected files show the task was completed in Godot: the reference zip holds project.godot, scenes/TokenWave.tscn, scripts/token_wave.gd and .godot GLES3 shader caches, and a reference screenshot and runtime log exist.",
   "evidence": "prompt: \"I need it built in Godot\"; agent_issue_details: null; applications_used: null; expected zip members: \"Bomb_Chain_Reaction_Working/project.godot\", \"Bomb_Chain_Reaction_Working/scenes/TokenWave.tscn\", \"Bomb_Chain_Reaction_Working/scripts/token_wave.gd\"; expected files: bomb_blast_frame.png, bomb_runtime_log.txt; input_files all under /home/docker/Desktop/",
   "recommendations": [
    {
     "id": "R01.1",
     "text": "Thin complexity check: not triggered. The task needs cross-file reasoning, physics simulation, live 3D rendering and telemetry logging, so it is not just retrieval."
    },
    {
     "id": "R01.2",
     "text": "Reference zip (Bomb_Chain_Reaction_Working/) contains __MACOSX and .DS_Store entries and an internal folder name that differs from the deliverable zip name. This is harmless, but criterion 4 (project.godot in the zip) should tolerate a nested folder."
    },
    {
     "id": "R01.3",
     "text": "applications_used is null. Record 'Godot' so reviewers can confirm the VM has it installed."
    }
   ]
  },
  {
   "id": "C02",
   "component": "02",
   "title": "Task - PII / Safety",
   "score": 5
  },
  {
   "id": "C03",
   "component": "03",
   "title": "Prompt - Clarity",
   "score": 5,
   "error_category": null,
   "confidence": "high",
   "blocked_on": "Bomb.glb could not be inspected (the extractor does not support .glb). It does not affect this clarity judgement. The expected zip was only read from its member listing.",
   "justification": "The prompt names all four inputs and all three outputs exactly, and it settles the one real conflict between sources: 'Where the config file and the reference image disagree on a visual element like row count or token arrangement, go with what the reference image shows.' The config says token_rows = 4, and scene_reference.png shows 3 token rows inside 4 row zones. That rule covers this case, so the agent has nothing to guess. Log formats are given as templates. {id} is defined as the mechanic id in gameplay_config.txt (bomb). The sample interval (1.0 s), auto cycle (3.0 s), and gravity, bounce and blast parameters are all in the named config. The bomb panel requirements (dedicated camera, at least two lights, to the right of the board, no overlap with the play area) can each be checked. The screenshot condition ('blast ring is still expanding', HUD legible, 3D panel visible) and the log condition ('at least twelve continuous seconds', one AUTO line and one INPUT line) can be checked from the artifacts. The rubric criteria (1-30) line up with what the prompt asks for. They defer to the expected files only for the visual and behavioural details the prompt already delegates to scene_reference.png. I found no place where two competent readings would produce differently graded artifacts.",
   "evidence": "\"Where the config file and the reference image disagree on a visual element like row count or token arrangement, go with what the reference image shows.\"; \"MOTION_SAMPLE mechanic={id} t={seconds} first=({x},{y}) collected={n} actions={n}\"; \"ACTION_TRANSITION mechanic={id} origin=<AUTO|INPUT> count={n}\"; \"where {id} is the mechanic identifier from gameplay_config.txt\"; gameplay_config.txt: \"id = bomb\", \"auto_cycle_interval_s = 3.0\", \"telemetry_sample_interval_s = 1.0\"; outputs named: Bomb_Chain_Reaction_Godot_Project.zip, bomb_blast_frame.png, bomb_runtime_log.txt",
   "recommendations": [
    {
     "id": "R03.1",
     "text": "The prompt does not say which token 'first=(x,y)' refers to (for example the first token in spawn order) or which coordinate space it uses (screen pixels versus board-local). Rubric criterion 28 only asks for well-formed values that show live movement, so this does not create misalignment."
    },
    {
     "id": "R03.2",
     "text": "The prompt does not say outright that automatic blasts also raise the actions counter. 'Each trigger raises the actions counter' plus the shared count={n} and actions={n} fields point to counting every blast, and criteria 24 and 27 assume that. One explicit sentence would remove any doubt."
    },
    {
     "id": "R03.3",
     "text": "The config gives a 1150x650 window with board_margin_left = 260 and board_margin_right = 300, which leaves a 590 px board width. The reference image is 1152x648 and its frame is about 642 px wide. The prompt's 'reference image is the visual authority' rule resolves this, but the numbers are not reconciled."
    },
    {
     "id": "R03.4",
     "text": "The screenshot criteria do not give a ring colour. The prompt only says 'blast ring', and the reference image shows no ring."
    }
   ]
  },
  {
   "id": "C04",
   "component": "04",
   "title": "Prompt - Realism",
   "score": 3,
   "error_category": "[All] [All] [Non-Fail - Minor Prescriptive Prompt]",
   "confidence": "medium",
   "blocked_on": null,
   "justification": "The prompt is grounded and has a real working situation with a visible motivation: 'Hi, I'm putting together a playable prototype for our Thursday gameplay review and I need it built in Godot so the team can run it themselves instead of watching a capture.' It has no artificial persona and names its inputs with context (art director's reference, artist's model, designer's config). It does not cross into the fail band. It is not an output-by-output checklist, it has no exact section-title list, and it does not spell out an internal algorithm. The telemetry line formats and the log and screenshot conditions are plausible requirements a developer might give. It lands in the minor-prescriptive band for two reasons. First, it carries more procedural and spec-style detail than a real user would typically write, and some of it reads as rubric language: 'Treat it as the spec, not loose inspiration', 'at least two lights positioned so that both the silhouette and the top surface of the model read clearly', 'covering at least twelve continuous seconds of play and containing both an automatic and a player-triggered action line'. Second, it enumerates the reference-image elements one by one: 'the framed play area with its internal grid lines, ... the collection strip along the bottom edge and where its label sits, the title across the top, and the HUD column on the left with its exact wording and line breaks'. This is heavier than a real user would write, but it does not leak verifier logic or overfit the output.",
   "evidence": "\"Treat it as the spec, not loose inspiration: match the framed play area with its internal grid lines, how the tokens sit on the board row by row including the alternating horizontal offset between rows, the collection strip along the bottom edge and where its label sits, the title across the top, and the HUD column on the left with its exact wording and line breaks.\" Also: \"at least two lights positioned so that both the silhouette and the top surface of the model read clearly\" and \"covering at least twelve continuous seconds of play and containing both an automatic and a player-triggered action line.\" Motivation: \"putting together a playable prototype for our Thursday gameplay review ... so the team can run it themselves instead of watching a capture.\"",
   "recommendations": [
    {
     "id": "R04.1",
     "text": "The reference-image paragraph could be shortened to point at scene_reference.png and one or two key concerns, since a real requester would rely on the image itself."
    },
    {
     "id": "R04.2",
     "text": "Softening 'Treat it as the spec, not loose inspiration' to something like 'the reference is what the art director signed off on' would read less like rubric language."
    },
    {
     "id": "R04.3",
     "text": "The mid-prompt sentence 'Where the config file and the reference image disagree ... go with what the reference image shows' is a conflict-resolution rule that reads a bit like a spec clause. A brief reason, such as the art director having signed the image off, would make it feel more natural."
    }
   ]
  },
  {
   "id": "C05",
   "component": "05",
   "title": "Prompt - GUI Integration",
   "score": 5,
   "recommendations": [
    {
     "id": "R05.1",
     "text": "bundle.json applications_used is null, so the intended GUI application (Godot editor or runtime) is inferred from the prompt rather than declared."
    },
    {
     "id": "R05.2",
     "text": "The screenshot timing condition ('blast ring still expanding') is subjective, and a tolerance could be stated."
    }
   ]
  },
  {
   "id": "C06",
   "component": "06",
   "title": "Prompt - Output Naming",
   "score": 5
  },
  {
   "id": "C07",
   "component": "07",
   "title": "Prompt - Timelessness",
   "score": 5,
   "recommendations": [
    {
     "id": "R07.1",
     "text": "The phrases 'Thursday gameplay review' and 'last sprint' are relative time references. They are harmless here but could be dropped for full timelessness."
    }
   ]
  },
  {
   "id": "C08",
   "component": "08",
   "title": "Prompt - Answer leakage",
   "score": 5
  },
  {
   "id": "C09",
   "component": "09",
   "title": "Gold File - Accuracy",
   "score": 3,
   "error_category": "[All] [All] [Non-Fail - Somewhat Inaccurate Gold File]",
   "confidence": "high",
   "blocked_on": null,
   "justification": "All three expected files are present with correct names and substantively correct content. The screenshot shows all required visual elements (blast ring, HUD, 3D bomb panel, grid lines, collection strip, title). The runtime log uses the correct telemetry format, covers 40 continuous seconds (exceeding the 12-second requirement), includes both AUTO and INPUT origins, and has internally consistent counter values. The Godot project ZIP contains project.godot, scene, script, and asset files with no missing dependencies.\n\nHowever, the gold file's code (token_wave.gd) hardcodes physics values that significantly deviate from what gameplay_config.txt specifies, despite the prompt stating 'gameplay_config.txt controls timing and physics':\n- gravity: code uses 38.0 px/s^2, config specifies 980 (25.8x off)\n- blast_force (mechanic_strength): scene sets 360.0, config specifies blast_force_px=600\n- auto_cycle: code uses 3.2s, config specifies 3.0s\n- bounce_damping: code uses 0.72, config specifies 0.7\n- token_speed_cap: not implemented (config specifies 1200 px/s)\n- blast_expand_duration: code uses ~0.45s, config specifies 0.4s\n- window size: project.godot uses 1152x648, config specifies 1150x650\n\nThe code does not read gameplay_config.txt at all; all values are hardcoded. This is a deviation from the prompt's stated constraint but does not rise to a primary-ask failure because: (1) all three deliverables are present and correctly structured, (2) no criterion directly grades the physics constants themselves, (3) the criteria use 'consistent with' language and tolerances (e.g., criterion 30 allows +/-20% on AUTO gaps), and (4) the log and screenshot are internally self-consistent outputs of the running game. The auto cycle deviation (3.2 vs 3.0, 6.7% off) falls within the criteria's 20% tolerance.\n\nThis is a secondary constraint violation: the prompt's instruction about the config controlling physics is important but not a primary deliverable, and the observable outputs remain substantively correct.",
   "evidence": "token_wave.gd line 131: 'velocity.y += 38.0 * delta' (config: gravity_px_per_s2 = 980); line 47: 'auto_timer = 3.2' (config: auto_cycle_interval_s = 3.0); line 135-138: 'velocity.x *= -0.72' / 'velocity.y = absf(velocity.y) * 0.72' (config: bounce_damping = 0.7); TokenWave.tscn line 11: 'mechanic_strength = 360.0' (config: blast_force_px = 600); project.godot: 'window_width_override=1152' / 'window_height_override=648' (config: window_width=1150, window_height=650).",
   "recommendations": [
    {
     "id": "R09.1",
     "text": "Close call on Score 2 vs Score 3: The gravity discrepancy (38 vs 980, 25.8x off) is large in magnitude and the prompt explicitly says the config controls physics. I considered Score 2 ('wrong values') but chose Score 3 because no criterion directly grades the gravity constant, the criteria compare observable behaviors with tolerances rather than exact physics values, and all primary deliverables are present and structurally correct. The fix (changing code to use config values) is legal since the prompt constrains them. Count: 1 reading favored Score 2, 4 readings favored Score 3."
    },
    {
     "id": "R09.2",
     "text": "The code does not implement token_speed_cap_px_per_s = 1200 from the config. No speed cap is applied to token velocities. This is another config parameter that is ignored."
    },
    {
     "id": "R09.3",
     "text": "Denominator: 3 expected files exist (zip, png, txt). All 3 were opened and examined. The zip was extracted to inspect project.godot, TokenWave.tscn, and token_wave.gd. 1 issue flagged (physics parameter deviations from config)."
    },
    {
     "id": "R09.4",
     "text": "Screenshot shows Collected: 62, Actions: 89. The log has no MOTION_SAMPLE with exactly those values (closest: t=31.0 with collected=62, actions=91). This is not a contradiction -- the screenshot captured a game state between MOTION_SAMPLE intervals, and ACTION_TRANSITION count=89 does exist in the log, confirming the state was real."
    }
   ]
  },
  {
   "id": "C10",
   "component": "10",
   "title": "Gold File - Format",
   "score": 5
  },
  {
   "id": "C11",
   "component": "11",
   "title": "Gold File - Input Consistency",
   "score": 3,
   "error_category": "[All] [All] [Non-Fail - Input Consistency]",
   "confidence": "high",
   "blocked_on": null,
   "justification": "The gold file script (token_wave.gd) does not read gameplay_config.txt at all. Instead, it hardcodes physics and timing values that differ from the config. The auto_cycle_interval is the one graded non-traceable value: the config specifies auto_cycle_interval_s = 3.0, but the script uses auto_timer = 3.2 (and initial 0.35). This produces AUTO events approximately every 3.2s in the expected log, which criterion 30 grades as a reference. The 3.2s value is not derivable from any input. However, criterion 30 allows 20% tolerance, so an agent using 3.0s (6.25% difference) would still satisfy it. Other non-traceable values include gravity (config=980, script=38.0), blast_force (config=600, scene=360), bounce_damping (config=0.7, script=0.72), blast_expand_duration (config=0.4, script=0.45), and token_speed_cap (config=1200, not implemented), but none of these are individually graded by any criterion. Visual elements (3 token rows, board layout, window size 1152x648) correctly follow the reference image over the config, as the prompt instructs. The mechanic id 'bomb' and telemetry_sample_interval 1.0s both trace to the config. All telemetry format traces to the prompt. Input assets (source_coin_token.png, Bomb.glb) are correctly bundled. The core deliverable derives correctly from the inputs; an agent following the config and reference image can satisfy all criteria despite the physics value discrepancies.",
   "evidence": "gameplay_config.txt: auto_cycle_interval_s = 3.0; token_wave.gd line: auto_timer = 3.2 (reset value); gameplay_config.txt: gravity_px_per_s2 = 980; token_wave.gd: velocity.y += 38.0 * delta; gameplay_config.txt: blast_force_px = 600; TokenWave.tscn: mechanic_strength = 360.0; gameplay_config.txt: bounce_damping = 0.7; token_wave.gd: velocity.x *= -0.72; Expected log consecutive AUTO gap (e.g. count=55 to count=56, count=94 to count=95): approximately 3.0-3.2s intervals between MOTION_SAMPLE timestamps.",
   "recommendations": [
    {
     "id": "R11.1",
     "text": "The gold file script does not read gameplay_config.txt at all. All six physics/timing parameters from the config (gravity, bounce_damping, blast_force, blast_expand_duration, token_speed_cap, auto_cycle_interval) are either hardcoded to different values or not implemented. While the prompt says 'gameplay_config.txt controls timing and physics,' the expected project ignores it entirely. The fix is to have the script parse and use gameplay_config.txt values, or to update the config values to match what the script uses."
    },
    {
     "id": "R11.2",
     "text": "Window resolution in project.godot (1152x648) does not match gameplay_config.txt (window_width=1150, window_height=650). The project uses the reference image's pixel dimensions instead. This is defensible given the prompt's conflict resolution rule, but the config values are vestigial."
    }
   ]
  },
  {
   "id": "C12",
   "component": "12",
   "title": "Rubric - Categorization",
   "score": 5,
   "recommendations": [
    {
     "id": "R12.1",
     "text": "Criterion 25 (correctness): 'The HUD text in bomb_blast_frame.png reproduces the exact wording and line breaks of the corresponding expected file.' This criterion tests both correctness (exact wording is content, per calibration: 'A value inside a visual element is correctness') and visual (line breaks are a layout/typography property). Fix: split into (a) correctness criterion testing exact wording match, and (b) visual criterion testing line break placement. Target pairs: correctness/REGULAR for wording, visual/REGULAR for line breaks."
    }
   ]
  },
  {
   "id": "C13",
   "component": "13",
   "title": "Rubric - Hardcoded Values",
   "score": 3,
   "error_category": null,
   "confidence": "high",
   "blocked_on": null,
   "justification": "Exactly 1 criterion contains a hardcoded expected value, which crosses the threshold for score 3 (Non-Fail: 1 criterion) but not score 2 (Fail: at least 2). Criterion 17 states tokens are 'yellow oval coins' -- applying the strip-the-anchor test, removing 'matching the token appearance in the corresponding expected file' leaves 'shows board tokens rendered as yellow oval coins', which tells the reader the exact color (yellow) and shape (oval) of the tokens. The prompt never says 'yellow oval'; it only references source_coin_token.png as the production coin face. The visual characteristics are derived from the input/expected files and should not be stated in the criterion text. The criterion should read something like 'shows board tokens matching the token appearance in the corresponding expected file' without pre-announcing the color and shape. All other criteria were swept: format gates (1-5) use prompt-defined names; telemetry criteria (6-10, 24, 27-30) use format labels (MOTION_SAMPLE, ACTION_TRANSITION, AUTO, INPUT) that the prompt itself defines; gameplay criteria (11-15, 26) reference the expected file; visual criteria (16, 18-23, 25) use terms from the prompt ('blast ring', 'at least two lights', 'dark background', 'HUD column on the left', etc.) or reference the expected file. No second hardcoded criterion was found.",
   "evidence": "Criterion 17: \"`bomb_blast_frame.png` shows board tokens rendered as yellow oval coins matching the token appearance in the corresponding expected file\" -- 'yellow oval coins' is a hardcoded description of the token appearance not found in the prompt text."
  },
  {
   "id": "C14",
   "component": "14",
   "title": "Rubric - Content",
   "score": 3,
   "error_category": "[All] [All] [Non-Fail - Rubric Content]",
   "confidence": "high",
   "blocked_on": null,
   "justification": "1 of 17 correctness criteria is existence-only (5.88%), which is within the up-to-15% non-fail band. Criterion n=9 ('bomb_runtime_log.txt includes at least one origin=AUTO action line and at least one origin=INPUT action line') checks only that specific line types are present using 'includes at least one' language, with no comparison to the expected file and no assessment of content correctness. By contrast, criterion n=29 covers the same origin values but checks their correctness against the expected file's trigger-source mapping. The remaining 16 correctness criteria all assess content through comparisons to expected files, quantitative thresholds, internal consistency checks, or behavioral verification. 15% of 17 = 2.55, so the threshold for fail would be 3 or more existence-only criteria; 1 is well within the non-fail band.",
   "evidence": "Criterion n=9 title: \"bomb_runtime_log.txt includes at least one origin=AUTO action line and at least one origin=INPUT action line.\" (category: correctness). Compare to n=29: \"Each ACTION_TRANSITION line in bomb_runtime_log.txt carries an origin value that matches the trigger-source mapping used in the corresponding expected file.\" (category: correctness). Denominator: 17 correctness criteria (n=6,7,8,9,10,11,12,13,14,15,24,25,26,27,28,29,30).",
   "recommendations": [
    {
     "id": "R14.1",
     "text": "Criterion n=9 could be strengthened by adding a comparison anchor, e.g., requiring the count of AUTO and INPUT lines to be consistent with the expected file rather than just checking at-least-one presence."
    }
   ]
  },
  {
   "id": "C15",
   "component": "15",
   "title": "Rubric - Accuracy",
   "score": 5
  },
  {
   "id": "C16",
   "component": "16",
   "title": "Rubric - Coverage",
   "score": 2,
   "error_category": "[All] [All] [Fail - Coverage]",
   "confidence": "high",
   "blocked_on": null,
   "justification": "The prompt explicitly states: \"match the framed play area with its internal grid lines, how the tokens sit on the board row by row including the alternating horizontal offset between rows.\" The alternating horizontal offset between token rows is one of six named visual elements the prompt lists to match from the reference image (designated as \"the visual authority for this build\"). The config file also confirms this with row_offset_pattern=alternating. No criterion tests whether token rows have an alternating horizontal offset. Criterion 17 grades token appearance (\"yellow oval coins\"), not spatial arrangement. Criterion 23 grades row zones (grid lines), not token placement within those zones. A submission with tokens placed in straight, non-alternating columns would pass every criterion while visibly deviating from the reference spec on this explicitly named point. This is a primary ask because it is explicitly stated in the prompt text as part of the board layout spec, not implied or secondary.",
   "evidence": "Prompt: \"match the framed play area with its internal grid lines, how the tokens sit on the board row by row including the alternating horizontal offset between rows\"; Config: \"row_offset_pattern = alternating\"; Reference image (scene_reference.png) visually shows staggered/offset rows. Criterion 17: \"board tokens rendered as yellow oval coins matching the token appearance\" (appearance, not arrangement). Criterion 23: \"play area divided by horizontal grid lines into the same number of row zones\" (grid lines, not token offset pattern)."
  },
  {
   "id": "C17",
   "component": "17",
   "title": "Rubric - Self-Containment",
   "score": 5
  },
  {
   "id": "C18",
   "component": "18",
   "title": "Rubric - Overfitting",
   "score": 5
  },
  {
   "id": "C19",
   "component": "19",
   "title": "Rubric - Atomicity",
   "score": 5
  },
  {
   "id": "C20",
   "component": "20",
   "title": "Rubric - Objectivity",
   "score": 5,
   "recommendations": [
    {
     "id": "R20.1",
     "text": "Criterion hygiene: criterion 17 (visual) is missing terminal punctuation — ends with '...matching the token appearance in the corresponding expected file' with no period. Does not affect this component's score since it is a visual criterion."
    }
   ]
  },
  {
   "id": "C21",
   "component": "21",
   "title": "Rubric - Framing",
   "score": 2,
   "error_category": "[All] [All] [Fail - Framing]",
   "confidence": "high",
   "blocked_on": null,
   "justification": "Criterion 24 is negatively framed. Its text reads: \"The actions value in the MOTION_SAMPLE lines of `bomb_runtime_log.txt` never decreases and agrees with the count of the most recent preceding ACTION_TRANSITION line.\" The predicate \"never decreases\" is a coordinate main requirement (joined by \"and\" with \"agrees with the count\"), not a subordinate constraint on a positive main action. It is analogous to \"Does not decrease\" and matches the rubric's negative-framing examples. A positive rewrite is available (e.g., \"monotonically increases or holds steady\"). The prompt does not contain an omission request—it positively states \"each trigger raises the actions counter.\" No sibling criterion shares this exact negative shape after a full sweep of all 30 criteria.",
   "evidence": "Criterion 24 text: \"The actions value in the MOTION_SAMPLE lines of `bomb_runtime_log.txt` never decreases and agrees with the count of the most recent preceding ACTION_TRANSITION line.\""
  },
  {
   "id": "C22",
   "component": "22",
   "title": "Rubric - Redundancy",
   "score": 3,
   "error_category": "[All] [All] [Non-Fail - Redundancy]",
   "confidence": "high",
   "blocked_on": null,
   "justification": "One overlapping pair exists: C20 ('shows a framed play area with internal grid lines, consistent with the corresponding expected file') and C23 ('shows a play area divided by horizontal grid lines into the same number of row zones as the corresponding expected file, with proportional row spacing and overall grid dimensions consistent with the corresponding expected file'). Both test for grid lines in the play area. The 'internal grid lines' check in C20 is subsumed by C23's more detailed horizontal-grid-line check: if C23 passes, C20's grid-line portion necessarily passes too. However, the scoring impact is minimal because C20 also tests the frame itself and C23 adds unique quantitative requirements (correct row count, proportional spacing, overall dimensions). Applying the calibration test: the overlap would not cause a correct agent to be marked wrong or a wrong agent to be marked right. All other criteria across the 30-item rubric are functionally distinct, testing different log properties, visual elements, game mechanics, or file validity dimensions.",
   "evidence": "C20 title: '`bomb_blast_frame.png` shows a framed play area with internal grid lines, consistent with the corresponding expected file.' (weight 45, visual). C23 title: '`bomb_blast_frame.png` shows a play area divided by horizontal grid lines into the same number of row zones as the corresponding expected file, with proportional row spacing and overall grid dimensions consistent with the corresponding expected file.' (weight 50, visual). Shared element: grid lines exist in the play area."
  },
  {
   "id": "C23",
   "component": "23",
   "title": "Rubric - Weight Share",
   "score": 5
  },
  {
   "id": "C24",
   "component": "24",
   "title": "Rubric - Individual Criteria Weights",
   "score": 5
  },
  {
   "id": "C25",
   "component": "25",
   "title": "Rubric - Count",
   "score": 5
  },
  {
   "id": "C26",
   "component": "26",
   "title": "Rubric - Robustness",
   "score": 5
  },
  {
   "id": "C27",
   "component": "27",
   "title": "Rubric - Value Binding",
   "score": 5
  },
  {
   "id": "C28",
   "component": "28",
   "title": "JSON - Structure / URL Integrity",
   "score": 5,
   "error_category": null,
   "confidence": "medium",
   "blocked_on": "Could not run the verifier, and did not fetch the S3 links live. Structure was checked from bundle.json and the staged files only.",
   "justification": "",
   "evidence": "verifier.func = \"agent_judge_multi\"; verifier.result dests = [Bomb_Chain_Reaction_Godot_Project.zip, bomb_runtime_log.txt, bomb_blast_frame.png], each with path /home/docker/Desktop/<same name>; expected_files dests are the same three names with three distinct S3 URLs (.../D8UHO49ikh4ha_r, .../k2m2QdWm4LBc8TV, .../swPirwXcbzvHhf5), all staged 'cached' in files/expected. mechanical.28_json_structure_url_integrity: {score:5, func:agent_judge_multi, dest_mismatch:[], signed_urls_verifier:[], signed_urls_initializer:[], result_paths_off_desktop:[]}. The prompt names all three outputs on the Desktop with the same filenames.",
   "recommendations": [
    {
     "id": "R28.1",
     "text": "All four input_files entries (source_coin_token.png, Bomb.glb, scene_reference.png, gameplay_config.txt) carry the identical URL .../65cbc42b32ffab95dd54b864/pwy5ipf5O1s2zNk, although the four staged inputs differ in size and content. This may be a bundle or pipeline artifact, but the initializer URLs are worth confirming, because the same link cannot serve four different files."
    },
    {
     "id": "R28.2",
     "text": "verifier has self_check_score \"1\" as a string, and the contributor's expected zip contains a top-level folder named Bomb_Chain_Reaction_Working plus __MACOSX entries. Neither affects this component."
    }
   ]
  }
 ],
 "senior_review": {
  "mechanical_verdict": 2,
  "verdict_driver": [
   "16",
   "21"
  ],
  "fragility": "The verdict rests on two independent rubric-level fails -- a missing coverage criterion (component 16) and a negatively framed criterion (component 21) -- both objective and well-evidenced, so the verdict is not fragile.",
  "summary": "The mechanical verdict of 2 is driven by two independent rubric-level failures. Component 16 (Coverage) identifies a missing criterion for the alternating horizontal offset between token rows, which is explicitly named in the prompt and confirmed by the config's row_offset_pattern=alternating; no existing criterion tests this primary visual requirement. Component 21 (Framing) flags criterion 24's 'never decreases' as negatively framed, with a straightforward positive rewrite available. Both fails are objective and well-evidenced, making the verdict solid. The six Score 3 components flag real but non-failing issues, most notably the gold file's physics values deviating significantly from gameplay_config.txt (gravity 38 vs 980, blast_force 360 vs 600) without being directly graded by any criterion -- an agent following the config can still satisfy all criteria, but the discrepancy should be cleaned up.",
  "fix_order": [
   {
    "id": "S1",
    "rank": 1,
    "component": "16",
    "fix": "Add a visual criterion testing that token rows exhibit the alternating horizontal offset the prompt explicitly names ('including the alternating horizontal offset between rows') and that gameplay_config.txt confirms (row_offset_pattern=alternating). A criterion like 'bomb_blast_frame.png shows tokens arranged with an alternating horizontal offset between adjacent rows, consistent with the corresponding expected file' would close the gap."
   },
   {
    "id": "S2",
    "rank": 2,
    "component": "21",
    "fix": "Rewrite criterion 24 in positive framing. Replace 'The actions value in the MOTION_SAMPLE lines of bomb_runtime_log.txt never decreases and agrees with the count of the most recent preceding ACTION_TRANSITION line' with something like 'The actions value in each MOTION_SAMPLE line of bomb_runtime_log.txt is monotonically non-decreasing and agrees with the count of the most recent preceding ACTION_TRANSITION line.'"
   },
   {
    "id": "S3",
    "rank": 3,
    "component": "09",
    "fix": "Align the gold file's physics constants with gameplay_config.txt or update the config to match the code. The gravity discrepancy (38 vs 980, 25.8x off) is the most severe; auto_cycle (3.2 vs 3.0), bounce_damping (0.72 vs 0.7), blast_force (360 vs 600), and blast_expand_duration (0.45 vs 0.4) should also be reconciled. Ideally the script should parse and use gameplay_config.txt values."
   },
   {
    "id": "S4",
    "rank": 4,
    "component": "11",
    "fix": "Same root cause as component 09: have token_wave.gd read and use gameplay_config.txt rather than hardcoding divergent values. This resolves both the accuracy and input-consistency flags simultaneously."
   }
  ],
  "escalations": [],
  "contradictions": [],
  "unverified": [
   {
    "id": "U1",
    "component": "01",
    "blocked_on": "bundle.json has applications_used: null and does not state that Godot is installed on the CUA VM; feasibility rests on the prompt naming Godot and on expected artifacts existing",
    "unexamined": "Whether the CUA VM environment actually has Godot installed and can run 3D projects with SubViewport support"
   },
   {
    "id": "U2",
    "component": "03",
    "blocked_on": "Bomb.glb could not be inspected (extractor does not support .glb)",
    "unexamined": "Whether the .glb model file contains geometry that could affect prompt clarity if its contents conflicted with the prompt's description; the reviewer judged this does not affect the clarity assessment"
   },
   {
    "id": "U3",
    "component": "28",
    "blocked_on": "Could not run the verifier and did not fetch S3 links live; all four input_files entries carry the identical S3 URL despite being four distinct files",
    "unexamined": "Whether the four identical input URLs actually serve the correct distinct files at runtime; the staged copies were cached and differ in size/content, so the pipeline may rewrite URLs, but this is unconfirmed"
   }
  ]
 },
 "input_consistency": {
  "verdict": "minor",
  "summary": "Checked all four input files (source_coin_token.png, Bomb.glb, scene_reference.png, gameplay_config.txt) against each other and against the three expected files (Bomb_Chain_Reaction_Godot_Project.zip, bomb_runtime_log.txt, bomb_blast_frame.png), plus the prompt and 30 criteria. Found six minor inconsistencies: two value-conflicts between inputs (token_rows and window dimensions disagree between gameplay_config.txt and scene_reference.png), and four gold-resolves-silently cases where the gold project uses physics and timing values that differ from gameplay_config.txt despite the prompt designating that file as the physics authority. None of these make any graded criterion unsatisfiable because the prompt provides an explicit resolution rule for visual conflicts and no criterion directly grades exact physics parameter values.",
  "rules_compared": [
   "token_rows: gameplay_config.txt says 4, scene_reference.png shows 3 rows of tokens, gold seed_tokens() iterates for row in 3",
   "tokens_per_row: gameplay_config.txt says 5, scene_reference.png shows 5 per row, gold iterates for column in 5 — consistent",
   "row_offset_pattern: gameplay_config.txt says alternating, scene_reference.png shows alternating horizontal offset, gold applies (row % 2) * 24.0 offset — consistent",
   "window dimensions: gameplay_config.txt says 1150x650, scene_reference.png is 1152x648 (image metadata), gold project.godot uses 1152x648",
   "gravity_px_per_s2: gameplay_config.txt says 980, gold token_wave.gd uses velocity.y += 38.0 * delta",
   "blast_force_px: gameplay_config.txt says 600, gold TokenWave.tscn sets mechanic_strength = 360.0",
   "bounce_damping: gameplay_config.txt says 0.7, gold token_wave.gd uses 0.72 multiplier on bounce",
   "auto_cycle_interval_s: gameplay_config.txt says 3.0, gold token_wave.gd resets auto_timer to 3.2",
   "telemetry_sample_interval_s: gameplay_config.txt says 1.0, gold MOTION_SAMPLE lines advance by t=1.0 — consistent",
   "blast_expand_duration_s: gameplay_config.txt says 0.4, gold explosion_flash starts at 0.45 — close but different",
   "token_diameter_px: gameplay_config.txt says 28, gold scales 110px source texture by 0.78 giving ~85.8px",
   "strip_label: gameplay_config.txt says COLLECT, scene_reference.png shows COLLECT, gold draws COLLECT — consistent",
   "strip_position: gameplay_config.txt says bottom, scene_reference.png shows bottom strip, gold draws strip at COLLECTION_Y=510 at board bottom — consistent",
   "mechanic id: gameplay_config.txt says bomb, gold uses mechanic=bomb, log shows mechanic=bomb — consistent",
   "MOTION_SAMPLE format: prompt prescribes format, gold log matches format — consistent",
   "ACTION_TRANSITION format: prompt prescribes format, gold log matches format — consistent",
   "HUD wording and line breaks: scene_reference.png shows BOMB / Collected: 0 / Actions: 0 / SPACE CLICK trigger mechanic / Automatic preview runs every cycle, gold label.text matches — consistent",
   "board_margin_left: gameplay_config.txt says 260, gold BOARD starts at x=255 — off by 5",
   "board_margin_right: gameplay_config.txt says 300, gold board right margin is 255 (1152 - 897) — off by 45",
   "grid line count: scene_reference.png shows 3 horizontal grid lines creating 4 zones, gold draws lines at y=210,310,410 creating 4 zones, bomb_blast_frame.png shows same — consistent"
  ],
  "files_checked": [
   "/home/user/rangutan_encyclopedia/audit/task_9/files/inputs/gameplay_config.txt",
   "/home/user/rangutan_encyclopedia/audit/task_9/files/inputs/scene_reference.png",
   "/home/user/rangutan_encyclopedia/audit/task_9/files/inputs/source_coin_token.png",
   "/home/user/rangutan_encyclopedia/audit/task_9/files/inputs/Bomb.glb",
   "/home/user/rangutan_encyclopedia/audit/task_9/files/expected/Bomb_Chain_Reaction_Godot_Project.zip",
   "/home/user/rangutan_encyclopedia/audit/task_9/files/expected/bomb_runtime_log.txt",
   "/home/user/rangutan_encyclopedia/audit/task_9/files/expected/bomb_blast_frame.png",
   "/home/user/rangutan_encyclopedia/audit/task_9/render_index.json",
   "/home/user/rangutan_encyclopedia/audit/task_9/bundle.json"
  ],
  "blocked_on": null,
  "findings": [
   {
    "id": "I1",
    "severity": "minor",
    "kind": "value-conflict",
    "files": [
     "gameplay_config.txt",
     "scene_reference.png"
    ],
    "statement_a": "gameplay_config.txt [board] section: token_rows = 4",
    "statement_b": "scene_reference.png shows exactly 3 rows of tokens on the board (with 4 grid zones created by 3 horizontal divider lines, the bottom zone empty)",
    "why_conflict": "The config specifies 4 rows of tokens but the reference image shows only 3 rows. The prompt acknowledges this class of conflict and resolves it: 'Where the config file and the reference image disagree on a visual element like row count or token arrangement, go with what the reference image shows.'",
    "graded_impact": "none — the prompt provides explicit resolution favoring the reference image, so a correct agent uses 3 rows and matches the gold",
    "component": "11",
    "fix": "Change token_rows = 3 in gameplay_config.txt to match the reference image"
   },
   {
    "id": "I2",
    "severity": "minor",
    "kind": "value-conflict",
    "files": [
     "gameplay_config.txt",
     "scene_reference.png"
    ],
    "statement_a": "gameplay_config.txt [viewport] section: window_width = 1150, window_height = 650",
    "statement_b": "scene_reference.png image dimensions are 1152x648 pixels (verified via image metadata)",
    "why_conflict": "The config specifies a 1150x650 viewport but the reference image was produced at 1152x648. The gold project.godot also uses 1152x648, matching the reference, not the config.",
    "graded_impact": "none — the 2-pixel width and 2-pixel height differences do not affect any graded criterion, and the prompt's resolution rule favoring the reference image applies",
    "component": "11",
    "fix": "Change window_width = 1152 and window_height = 648 in gameplay_config.txt to match the reference image"
   },
   {
    "id": "I3",
    "severity": "minor",
    "kind": "gold-resolves-silently",
    "files": [
     "gameplay_config.txt",
     "Bomb_Chain_Reaction_Godot_Project.zip"
    ],
    "statement_a": "gameplay_config.txt [physics] section: gravity_px_per_s2 = 980",
    "statement_b": "Gold script token_wave.gd line 131: 'velocity.y += 38.0 * delta' applies an effective gravity of 38 px/s-squared, roughly 25 times lower than the config value",
    "why_conflict": "The prompt says 'gameplay_config.txt controls timing and physics', directing the agent to use the config's gravity value. The gold silently uses a much lower value (38 instead of 980), producing dramatically different token fall speeds and collected-count trajectories.",
    "graded_impact": "none — no criterion directly compares the gravity parameter value or exact coordinate/collected trajectories against the gold; criteria 12 and 28 check behavioral patterns and internal consistency",
    "component": "09",
    "fix": "Change gravity_px_per_s2 = 38 in gameplay_config.txt to match the gold implementation"
   },
   {
    "id": "I4",
    "severity": "minor",
    "kind": "gold-resolves-silently",
    "files": [
     "gameplay_config.txt",
     "Bomb_Chain_Reaction_Godot_Project.zip"
    ],
    "statement_a": "gameplay_config.txt [physics] section: blast_force_px = 600",
    "statement_b": "Gold scene TokenWave.tscn line 11: mechanic_strength = 360.0, used as the blast force magnitude in the bomb mechanic (token_wave.gd line 94: direction * mechanic_strength)",
    "why_conflict": "The prompt designates gameplay_config.txt as the physics authority, but the gold uses 360 instead of 600 for the blast force, producing different token dispersal velocities.",
    "graded_impact": "none — no criterion grades the exact blast force value; criterion 11 checks that a radial blast exists, not its magnitude",
    "component": "09",
    "fix": "Change blast_force_px = 360 in gameplay_config.txt to match the gold implementation"
   },
   {
    "id": "I5",
    "severity": "minor",
    "kind": "gold-resolves-silently",
    "files": [
     "gameplay_config.txt",
     "Bomb_Chain_Reaction_Godot_Project.zip"
    ],
    "statement_a": "gameplay_config.txt [timing] section: auto_cycle_interval_s = 3.0",
    "statement_b": "Gold script token_wave.gd line 47: 'auto_timer = 3.2' — the auto cycle resets to 3.2 seconds, not 3.0; additionally the initial auto_timer is 0.35 (line 14), causing the first AUTO to fire after only 0.35 seconds instead of 3.0",
    "why_conflict": "The prompt says the config controls timing, but the gold uses a 3.2-second auto cycle instead of 3.0. The consecutive AUTO gaps in the expected log appear as approximately 3.0 seconds at the 1-second sampling resolution.",
    "graded_impact": "none — the 6.7% difference (3.0 vs 3.2) is well within criterion 30's plus-or-minus 20 percent tolerance for AUTO event gaps",
    "component": "09",
    "fix": "Change auto_cycle_interval_s = 3.2 in gameplay_config.txt, or change the gold script auto_timer reset to 3.0"
   },
   {
    "id": "I6",
    "severity": "minor",
    "kind": "gold-resolves-silently",
    "files": [
     "gameplay_config.txt",
     "Bomb_Chain_Reaction_Godot_Project.zip"
    ],
    "statement_a": "gameplay_config.txt [physics] section: bounce_damping = 0.7",
    "statement_b": "Gold script token_wave.gd lines 135 and 138: wall bounce uses 'velocity.x *= -0.72' and ceiling bounce uses 'absf(velocity.y) * 0.72', a damping factor of 0.72 rather than 0.7",
    "why_conflict": "The prompt designates the config as the physics authority, but the gold uses a slightly different bounce damping coefficient (0.72 vs 0.7).",
    "graded_impact": "none — no criterion grades the exact bounce damping value",
    "component": "09",
    "fix": "Change bounce_damping = 0.72 in gameplay_config.txt, or change the gold script to use 0.7"
   }
  ]
 }
}

==============================================================================

# Output hygiene

Shape every response so an ADHD brain can act on it. Brevity is not the goal. Actionability is.

## Source of truth — binding, read before anything else

This file is the guideline. It is not a source of facts and it is not an analysis brief.

1. **The only input is the audit data above this guideline.** Every score, quote, number, filename, criterion, finding, verdict and piece of reasoning must come from it. It holds the verdict, all 28 scores, the full result of every component a fix can come from, every recommendation, every group of value criteria that one input answers in full, the senior review, the input-consistency result, the prompt and the criteria, so nothing else is needed.
2. **Do not open, read, search, glob or list any file.** You have no tools for it and need none. Not to verify, not to "just check", not to fill a gap.
3. **Do not re-analyse.** Do not recompute a figure, re-derive a percentage, re-judge a score, or form a new finding. The reasoning in the data has already been done; your job is to reshape its presentation.
4. **The only output is the JSON object the schema asks for.** The page is built from it by code: layout, section order, numbering, counters, file badges and empty lines are not yours to write. Put no HTML in any field.
5. **If something cannot be quoted from the data, say so in the field where it belongs** — one clause naming what is missing, in place. Never substitute a number, a filename or a sentence you did not read there.
6. **Every item names what it comes from.** `sources` lists the ids printed in the data: `S1` a senior-review fix, `E1` an escalation, `X1` a contradiction, `U1` an unverified component, `C09` a component result, `R09.2` one of its recommendations, `I1` an input-consistency finding. Code checks every id, and every `now`, `delete` and `highlight` quote against the audit's own files, and marks on the page the ones it cannot find.

## Output structure — the fields

The content changes with every submission. The shape never does. Every field below is required; a section with nothing in it is an empty array, or an empty string where the field is text.

Prose fields render inline `` `code` `` and `**bold**`. Write every file name in backticks, exactly as the data's `files` list names it. The quoting fields — `now`, `highlight`, `delete`, `to`, `to_highlight` — are printed exactly as written, so they carry the artifact's own characters and no markup.

**The head.**
- `next_action`: the one next action, naming the file. It is fix 1.
- `next_action_why`: fix 1 of N, and why it carries the verdict.
- `gate`: what the verdict rests on and which fixes clear it. The page adds a live count of the verdict-clearing fixes left.

**The fixes — `steps`, in the order to do them.**
- `action`: the step, imperative, one bounded action.
- `pill`: one of the fixed pill texts below, or empty.
- `clears_verdict`: true for every step that reaches a component at the verdict score. These steps come first.
- `components`: the two-digit numbers of the components the step answers to.
- `scope`: countable scope, never time: "1 criterion rewritten, 1 criterion added, 1 file".
- `why`: what is wrong, in one or two sentences.
- `fixes`: one entry per edit:
  - `files` — each file the edit is made in, its `name` exactly as the `files` list names it and its `class`. The same edit mirrored in `bundle.json` and `rubric.json` is one entry with both files.
  - `location` — the exact place: criterion number, paragraph and sentence, sheet and cell.
  - `weight` — "weight 10", "weight to set", or empty when the edit is not to a criterion.
  - `now` — the current text, copied exactly from the artifact. Empty only when the location holds no text yet, such as a criterion that does not exist or a page-setup property.
  - `now_note` — the current state in words when `now` is empty, or a caveat on it.
  - `highlight` — the part of `now` that changes, copied from `now`.
  - `delete` — the text removed, copied from `now`.
  - `to` — the full replacement as it will read after the edit, as a finished sentence. Empty when the edit only deletes.
  - `to_highlight` — the added part of `to`, copied from `to`.
  - `draft` — true when `to` was composed rather than quoted from a finding.
  - `note` — where the wording came from, and what was left out and why.
- `answer_key_check`: mandatory on any step with a `gtf` file; empty otherwise.
- `note`: optional, one line. The page prints the step's sources after it, so it does not repeat them.
- `sources`: the ids the step is built from.

**`consistency_coverage`** — one line: the consistency check's verdict, its counts, and which fix carries each finding.

**`wrong_facts`** — component reports that state a wrong fact: the `component`, what its report `says`, the `fact` that corrects it, and `sources`.

**`one_call`** — the single open decision: `question`, as a question; `context`, one line on which fix it blocks and why; `options`, 2 to 4, each a short `label` and a `detail`, the recommended one first; `pick`, one line on which you would pick and why. An empty `question` means there is no open call.

**`still_open`** — what could not be settled: the `components` each item covers and one `line`.

Component 27's `whole_answer_inputs`, where present, lists groups of value criteria whose every value one supplied input already prints, so a response that copies that input passes the whole group. If component 27 scored 5 regardless, each group is a `still_open` item naming the input and the criteria. If it scored below 5, the step that fixes it names them.

**`also_found`** — tangents, at most 3 one-line items.

**`start_here`** — the last word: `action`, the action as an imperative sentence; `detail`, where it is and what to paste.

### Fixed vocabulary

- File classes: `gtf` for a ground truth file (an expected file, the answer key), `input` for a file the agent receives, `prompt`, `rubric` and `bundle` for the task's own artifacts.
- Pills: `clears the fail` and `major`, the red ones; `pre-empts an escalation`, the amber one. No other pill text.
- Step order is always: the fixes that clear the verdict, then the consistency check's major findings, then everything else ranked by weight. Steps are numbered from 1, in the order you give them.

### Empty states

An empty section prints its own line, so leave it empty rather than filling it:

- `wrong_facts`: "No component report states a wrong fact."
- `one_call`: "No open call: every fix above is unambiguous."
- `still_open`: "Every component was settled from the available evidence."
- `also_found`: "Nothing outside the fix list."

## Criteria you write pass the rubric

A `to` that edits or adds a criterion is a criterion, and the audit's rubric components judge it the way they judged the task's own. A replacement that breaks one of their rules trades one finding for another. Check every one against the rules below before writing it. A replacement quoted from a finding that breaks a rule is not copied: rewrite it so it passes, set `draft`, and say in `note` what changed. Code flags conditional wording, and values the prompt does not give, in every criterion you write.

1. **It never states the answer** (component 13). Compare to the expected file by name, with a comparison mode: a tolerance (±1 / 3 / 5%) on a derived number, semantic equivalence for prose, structural comparability for a visual. Never write the value, name, date, count or conclusion the agent has to produce. The test: delete the expected-file anchor and read what remains. If it still tells the reader the answer, the value is hardcoded, and an anchor added after it does not cure it. A value the prompt itself gives may appear.
   Bad: "Shows X as 3.89°"
   Good: "The X value in `results.docx` matches the corresponding value in the expected file within ±1%"
2. **It has no conditional wording.** One requirement that always applies: never "if", "unless", "where applicable", "when present", "if any", "depending on" or "any X it reports". The expected file already shows which case this task's data takes, so grade that case's outcome against it.
   Bad: "If the starting total includes the transfers, `report.xlsx` subtracts them"
   Good: "The adjusted total in `report.xlsx` matches the corresponding value in the expected file within ±1%"
3. **One element, one category** (component 19): one section, table, chart or slide of one file, and only one of correctness, visual or format gate. Two files are two criteria.
4. **The grader can see both sides** (component 17). It has the agent's output and the expected file, never the prompt or the input files. Anchor to the expected file by name, and never grade the prior state of a supplied file ("the existing …", "unchanged").
5. **It names where the value sits** (component 27): the section, table row, slide or cell, not the whole file. A tolerance goes on a derived value only; a figure transcribed from an input has one right answer and takes none.
6. **Positively framed** (component 21): what the output does or contains, unless the prompt asks for an omission.
7. **Objective** (component 20): no "good", "appropriate" or "clear" outside a visual criterion.
8. **Not overfit** (component 18): no wording, filename, layout, rounding or method that the prompt and the input files leave open.
9. **Robust** (component 26): a fit or no-overflow check also says "remains legible at normal zoom", or anchors to the expected file's layout.
10. **The rubric still holds** (components 24 and 25): a weight is an integer from 1 to 50, `MUST-PASS` is only for a file-existence or file-type gate, and the rubric keeps 10 to 30 criteria.

## What ADHD changes about reading

1. Working memory is small. Anything not on screen is forgotten. Never say "keep in mind X."
2. Knowing the answer is not doing the answer. The gap between "got it" and "done it" is where work dies.
3. Starting is the hardest step. The first action must be obvious, small, and doable now.
4. Time estimates do not land. "A bit of work" and "a few hours" register the same, and a wrong one either rushes the reader or stops them starting. Size is carried by countable scope instead.
5. Dopamine is scarce. Visible finished work matters. Buried wins do not register.

## Rules

### 1. Lead with the reader's next action
First line is something they can do, not context and not a plan. If the output is a file, name the file and the one thing to do with it.

Bad: "I went through the Q3 folder and there are a few things worth discussing before we decide..."
Good: "Open `Q3-forecast.xlsx` and check the 3 highlighted cells in column F. The rest is done."

### 2. Number multi-step work
If the reader has more than one thing to do, write a numbered list. One bounded action per step. No step contains "and then" twice. Use the fewest steps that still work. A short path finished beats a complete path abandoned.

Where one source item bundles two edits to different files, split it into two steps and say in the detail which source item it came from. Where two source items edit the same line, merge them into one step. The reader must never be handed two conflicting versions of the same line.

### 3. Every fix carries its full context
A fix the reader has to go and look up is a fix they will not start. Put the change in the output itself: the text as it stands today, and the text to replace it with, both in full.

Bad: "Criterion 22 is negatively framed and should be rewritten positively."

Good:
> **now** — Tables in `report.pdf` contain no text or values that are cut off or truncated
> **to** — All table text and values in `report.pdf` are fully visible and remain legible at normal zoom

Requirements for every fix:
1. Quote the current text verbatim from the artifact. Never paraphrase what it says today.
2. Write the replacement as it will read after the edit, as a finished sentence. Not "add a tolerance" — the sentence with the tolerance in it.
3. Name the exact location: file, plus criterion number, or paragraph and sentence, or sheet and cell.
4. Show a deletion as struck-out text and an addition as the added text alone: the removed text goes in `delete`, the added part of the replacement in `to_highlight`.
5. Mark any replacement you composed rather than quoted as a draft (`draft: true`), so the reader knows what to verify before committing it.

### 4. Name the file and say what kind of file it is
The risk of an edit depends on what it touches, and the reader cannot hold that mapping in their head. Label the file class on the same line as the filename, every time, even when it repeats.

- **GTF** — a ground truth file (the expected or gold file, the answer key). Editing one changes what every submission is graded against.
- **Input file** — a file the agent receives. Editing one changes what is solvable.
- **Prompt**, **Rubric**, **Bundle** — the task's own artifacts.

Bad: "Fix the rounded literal in D3."
Good: "`fund_analysis_support.xlsx` (GTF), sheet Own-Revenue Coverage, cell D3."

Any step that touches a GTF also needs a stated check that the rest of the answer key still agrees with it afterwards. Say that in the step, not in a general caveat.

### 5. Say only what is wrong
Do not write paragraphs about what passed. A clean component, a reproduced figure, a rule that agrees across every source: none of it tells the reader what to do, and all of it buries what does.

Bad: "Five components independently traced every graded value to a named input line and each explicitly recorded 'could not reach: nothing', so no criterion is unsatisfiable and no component is anchored on an unreachable figure."
Good: "No unreachable values."

Where a clean result is genuinely load-bearing, it is a count or a clause, never a paragraph. This rule governs presentation only. The full reasoning, including everything that passed, stays in `component_review.html`; never let it lead here.

### 6. Input file consistency findings are fixes
The consistency check across the supplied files is scored by no component, so nothing else in the output will surface it. Read its own verdict before writing a word about it — it is in the audit data, under `input_consistency`, so there is no reason to look anywhere else.

- If it reports **major** findings — the inconsistency changes what a correct submission looks like — each becomes a numbered fix ranked alongside the verdict-clearing ones.
- If it reports **minor** findings — a real inconsistency that moves no graded output — each still becomes a numbered fix, ranked below. Minor is not a tangent and does not belong under "Also found".
- If it reports nothing, say so in one clause and move on.

Never write "no inconsistencies found" without reading the check's verdict field. A wrong clean bill is worse than no clean bill: it tells the reader to stop looking.

### 7. No time estimates
Never state how long a fix, a step, or the whole list will take. Not minutes, not "quick", not "a small change", not a total at the top.

Carry size with countable scope instead.

Bad: "About 20 minutes to rewrite the tolerances."
Good: "Four criteria, one file."

### 8. End with one concrete next action
If anything is open, name ONE thing that is small and doable now. "Read the first paragraph and tell me if the tone is right" counts.

### 9. Park tangents, don't chase them
Finish the task first. Anything else found goes at the end under "Also found:" as at most 3 one-line items, no elaboration, no fixing. Findings that belong in the numbered list under rule 6 are not tangents and do not go here.

Bad: "Here's the deck. By the way the source spreadsheet has duplicate rows, and the branding is outdated, and..."
Good: "Deck is done. Also found: 4 duplicate rows in the source sheet. Want that cleaned next?"

### 10. Restate state every turn
The reader cannot hold "we're on step 3 of 5" between messages. Restate where things stand, what is finished, what is left.

Bad: "Done. Ready for the next part?"
Good: "3 of 5 done: data cleaned, chart built, summary drafted. Left: exec intro, formatting."

If a task list or plan tool is available, use it for multi-step work, one item in progress at a time, and let the list do the restating instead of narrating the plan in prose. Progress notes during a long run are one line each.

### 11. Make finished work visible and openable
Say what now exists, where it is, and what it is ready for.

Bad: "I've made updates to the report, incorporating several changes."
Good: "`Board-update-Sept.docx` is ready to send. 2 pages, 3 charts, exec summary on page 1."

### 12. Matter-of-fact tone when something fails
Never "Uh oh," "Oh no," or "There seems to be a problem." State cause and fix.

Bad: "Uh oh, I ran into an issue accessing the folder."
Good: "Can't read the Drive folder: access expired. Fix: reconnect Google Drive in Customize, then say 'retry'."

### 13. Cap visible lists at 5 items
Group related items and rank the most relevant first. Keep more in reserve and show them when asked or when they become next. This shapes presentation only. It must never limit research, analysis, tool results, or what is retained.

### 14. No preamble, no recap, no closing pleasantries
Forbidden openers: "Great question," "Let me...", "I'll...", "Sure!", "Looking at your...", "To answer your question..."
Forbidden recaps: "I've now done X, Y, and Z, which means..."
Forbidden closers: "Let me know if you need anything else," "Hope this helps," "Feel free to ask."

Start with the answer. Stop when the answer is done.

### 15. One decision at a time
Never send a list of open questions. If input is needed, ask one question, give 2 to 4 named options, and say which one you'd pick and why in one line. Hold the rest until that one is answered.

Bad: "A few things to decide: tone, length, audience, whether to include Q2 numbers, and what format you want."
Good: "One call to make: re-anchor the criterion to the technical summary, or add the missing line to the one-pager? I'd re-anchor, since that edits the rubric and leaves the GTF alone."

### 16. Do the reversible work, ask about the irreversible
If it can be undone, do it and report. Do not ask "want me to?" for drafting, editing a working copy, reformatting, researching, or renaming a file you created.

Ask first, in one line, for anything that leaves this session: sending or replying to email, posting to Slack, sharing or changing permissions, sending calendar invites, deleting or overwriting a file you did not create, or writing to a live system of record. State exactly what will happen and to whom.

## When to break the rules

1. **"Explain this" or "walk me through it."** Explain fully. Still no preamble, still no closer, but the body runs as long as the topic needs. Add headers so the reader can skim back.
2. **Irreversible action ahead.** Confirm before acting. Safety beats brevity.
3. **Loop.** If the last three turns have been "still not right," stop revising the deliverable. Name the assumption that might be wrong and ask one diagnostic question.
4. **Real ambiguity.** One short clarifying question beats producing the wrong deliverable.
5. **A rule would delete the answer.** "What are my options" gets 2 to 4 ranked options with one-line trade-offs, recommendation first. The options are the answer.
6. **Accuracy is at stake.** Never drop a number's caveat, a source's date, or a confidence level to save a line. If a figure is estimated, unverified, or from a stale source, say so in the same sentence as the figure. Rule 5 never licenses omitting a caveat: "say only what is wrong" cuts praise, not qualifications.

## Pre-send check

Delete:
1. The first sentence, if it announces what you are about to do.
2. The last sentence, if it asks "anything else?" or recaps what just happened.
3. Any "by the way" sidebar.
4. Every time estimate, in any form.
5. Every paragraph that describes something already correct.
6. Hedging adverbs carrying no information ("perhaps," "might," "could possibly"). Keep a hedge that carries real uncertainty; deleting it manufactures confidence.
7. Idioms and figurative phrases ("circle back," "get the ball rolling"). Use the literal action.

Then verify:
- Did every fact, quote and number come from the audit data, and did you open no file?
- Reading only `next_action` and `start_here`, does the reader know what to do next and what just happened?
- Is every file named exactly as the `files` list names it, with its file class?
- Does every fix show both the current text and the replacement text, in full?
- Does every criterion you wrote pass "Criteria you write pass the rubric": no stated answer, no conditional wording, one element, anchored to the expected file?
- Is every `now`, `highlight` and `delete` copied from the artifact character for character?
- Does every step with a `gtf` file carry its answer-key check?
- Did you read the input-consistency verdict, and is every finding it reports, major and minor, in the numbered list?
- Does every step and every wrong fact list its sources?
- Does any two steps edit the same line?
