Write criteria that encompass all requirements needed to fulfill this prompt.
30/30 completed

Edit raw criteria

Show summary

List view
Search criteria...
1
Output includes a valid .zip file named Bomb_Chain_Reaction_Godot_Project.zip.
5 points · MUST-PASS · format_gate

2
Output includes a screenshot file named bomb_blast_frame.png.
5 points · MUST-PASS · format_gate

3
Output includes a console log file named bomb_runtime_log.txt.
5 points · MUST-PASS · format_gate

4
Bomb_Chain_Reaction_Godot_Project.zip is a valid archive containing a project.godot file.
8 points · REGULAR · format_gate

5
The ZIP includes scene, script, and asset files so the project can open with no missing dependencies.
8 points · REGULAR · format_gate

6
bomb_runtime_log.txt contains MOTION_SAMPLE lines in the prescribed telemetry format, matching the corresponding expected file.
8 points · REGULAR · correctness

7
bomb_runtime_log.txt contains ACTION_TRANSITION lines with origin=AUTO or origin=INPUT in the prescribed format, matching the corresponding expected file.
8 points · REGULAR · correctness

8
bomb_runtime_log.txt records a continuous sequence of MOTION_SAMPLE lines with no missing samples between the first and last recorded t value, and that span is at least twelve seconds long.
12 points · REGULAR · correctness

9
bomb_runtime_log.txt includes at least one origin=AUTO action line and at least one origin=INPUT action line.
10 points · REGULAR · correctness

10
Consecutive MOTION_SAMPLE lines in bomb_runtime_log.txt advance t at the same regular sampling interval used in the corresponding expected file, within plus or minus 10 percent of that interval.
8 points · REGULAR · correctness

11
The project implements a radial blast from the board center triggered by Space or click, consistent with the corresponding expected file. Alternative implementations that produce the same outward dispersal are accepted.
8 points · REGULAR · correctness

12
Tokens fall under gravity, bounce off inner frame walls, and are collected at the collection strip, consistent with the corresponding expected file.
6 points · REGULAR · correctness

13
The blast fires automatically on a fixed repeating cycle so the board never sits idle, consistent with the corresponding expected file.
5 points · REGULAR · correctness

14
The board repopulates tokens so it never empties out, consistent with the corresponding expected file.
15 points · REGULAR · correctness

15
Each collected token increments the collected counter and each trigger increments the actions counter, consistent with the corresponding expected file.
10 points · REGULAR · correctness

16
bomb_blast_frame.png shows a 3D bomb model rendered in its own viewport panel to the right of the board, not overlapping the play area, with a dedicated camera and at least two lights so that the silhouette and top surface of the model read clearly against the dark background, consistent with the corresponding expected file.
50 points · REGULAR · visual

17
bomb_blast_frame.png shows board tokens rendered as yellow oval coins matching the token appearance in the corresponding expected file
40 points · REGULAR · visual

18
bomb_blast_frame.png shows a large colored ring shape centered on the board, consistent with the corresponding expected file.
50 points · REGULAR · visual

19
bomb_blast_frame.png shows the HUD counters legible in a column on the left, with no text clipped, truncated, or overlapping another element.
40 points · REGULAR · visual

20
bomb_blast_frame.png shows a framed play area with internal grid lines, consistent with the corresponding expected file.
45 points · REGULAR · visual

21
bomb_blast_frame.png shows a collection strip along the bottom edge with its label, consistent with the corresponding expected file.
40 points · REGULAR · visual

22
bomb_blast_frame.png shows a title across the top of the scene, consistent with the corresponding expected file.
40 points · REGULAR · visual

23
bomb_blast_frame.png shows a play area divided by horizontal grid lines into the same number of row zones as the corresponding expected file, with proportional row spacing and overall grid dimensions consistent with the corresponding expected file.
50 points · REGULAR · visual

24
The actions value in the MOTION_SAMPLE lines of bomb_runtime_log.txt never decreases and agrees with the count of the most recent preceding ACTION_TRANSITION line.
10 points · REGULAR · correctness

25
The HUD text in bomb_blast_frame.png reproduces the exact wording and line breaks of the corresponding expected file.
15 points · REGULAR · correctness

26
Every live token on the board receives its own outward radial trajectory away from the board center when a blast fires, matching the corresponding expected file.
12 points · REGULAR · correctness

27
bomb_runtime_log.txt records exactly one sequential ACTION_TRANSITION line for every automatic or input blast, with count increasing by one each time and no skipped values.
10 points · REGULAR · correctness

28
In every MOTION_SAMPLE line of bomb_runtime_log.txt, the first=(x,y) coordinates are well-formed and reflect live token movement consistent with the outward blast, gravity and wall collisions, and the collected value is internally consistent with the collection events recorded in the same log.
8 points · REGULAR · correctness

29
Each ACTION_TRANSITION line in bomb_runtime_log.txt carries an origin value that matches the trigger-source mapping used in the corresponding expected file.
8 points · REGULAR · correctness

30
During periods in bomb_runtime_log.txt where consecutive origin=AUTO lines appear with no intervening origin=INPUT lines, the time gap between those AUTO events matches the corresponding gap in the expected file, within plus or minus 20 percent.
8 points · REGULAR · correctness
