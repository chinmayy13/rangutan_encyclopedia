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
bomb_runtime_log.txt records a continuous sequence of MOTION_SAMPLE lines spanning at least twelve seconds, with consecutive entries advancing t at the same regular sampling interval used in the corresponding expected file, within plus or minus 10 percent of that interval.
12 points · REGULAR · correctness

9
bomb_runtime_log.txt contains both origin=AUTO and origin=INPUT ACTION_TRANSITION lines, with at least two origin=AUTO lines, confirming that the log captures both automatic-cycle and player-triggered blast events.
10 points · REGULAR · correctness

10
The project in Bomb_Chain_Reaction_Godot_Project.zip implements a radial blast from the board center, triggered by Space or click, that pushes every live token outward along its own trajectory, consistent with the corresponding expected file.
8 points · REGULAR · correctness

11
The project in Bomb_Chain_Reaction_Godot_Project.zip instances Bomb.glb as a 3D node inside a SubViewport with a dedicated Camera3D and at least two light nodes, so the bomb model renders live during play, consistent with the corresponding expected file.
5 points · REGULAR · correctness

12
In the project from Bomb_Chain_Reaction_Godot_Project.zip, tokens that cross the collection strip are removed from play and increment the collected counter, consistent with the corresponding expected file.
4 points · REGULAR · correctness

13
The project in Bomb_Chain_Reaction_Godot_Project.zip repopulates board tokens before the board empties, keeping the board populated during play, consistent with the corresponding expected file.
15 points · REGULAR · correctness

14
In the project from Bomb_Chain_Reaction_Godot_Project.zip, tokens fall under gravity, bounce off inner frame walls, and follow fall-and-bounce trajectories consistent with those in the corresponding expected file.
10 points · REGULAR · correctness

15
The project scripts in Bomb_Chain_Reaction_Godot_Project.zip set the blast-ring expansion duration to a value within plus or minus 20 percent of the duration used in the corresponding expected file.
5 points · REGULAR · correctness

16
bomb_blast_frame.png shows a 3D bomb model rendered in its own viewport panel to the right of the board, not overlapping the play area, with both the silhouette and top surface of the model reading clearly against the dark background, consistent with the corresponding expected file.
50 points · REGULAR · visual

17
bomb_blast_frame.png shows board tokens matching the token appearance in the corresponding expected file.
40 points · REGULAR · visual

18
bomb_blast_frame.png shows a large colored ring shape centered on the board, consistent with the corresponding expected file.
50 points · REGULAR · visual

19
bomb_blast_frame.png shows the HUD counters legible in a column on the left, with no text clipped, truncated, or overlapping another element.
40 points · REGULAR · visual

20
bomb_blast_frame.png shows a framed play area with internal grid lines, divided by horizontal grid lines into the same number of row zones as the corresponding expected file, with proportional row spacing and overall grid dimensions consistent with the corresponding expected file.
50 points · REGULAR · visual

21
bomb_blast_frame.png shows a collection strip along the bottom edge with its label, consistent with the corresponding expected file.
40 points · REGULAR · visual

22
bomb_blast_frame.png shows a title across the top of the scene, consistent with the corresponding expected file.
40 points · REGULAR · visual

23
Bomb_Chain_Reaction_Godot_Project.zip contains a project that arranges initial board tokens with an alternating horizontal offset between adjacent rows, consistent with the corresponding expected file.
45 points · REGULAR · visual

24
The actions value in each MOTION_SAMPLE line of bomb_runtime_log.txt is monotonically non-decreasing and agrees with the count of the most recent preceding ACTION_TRANSITION line.
10 points · REGULAR · correctness

25
The HUD text in bomb_blast_frame.png reproduces the exact wording and line breaks of the corresponding expected file.
15 points · REGULAR · correctness

26
bomb_runtime_log.txt records exactly one sequential ACTION_TRANSITION line for every automatic or input blast, with count increasing by one each time and no skipped values.
10 points · REGULAR · correctness

27
In every MOTION_SAMPLE line of bomb_runtime_log.txt, the first=(x,y) field contains a well-formed numeric coordinate pair within the board-area bounds shown in the corresponding expected file.
5 points · REGULAR · correctness

28
In bomb_runtime_log.txt, the collected value in each MOTION_SAMPLE line is monotonically non-decreasing across consecutive samples.
5 points · REGULAR · correctness

29
The number of origin=AUTO ACTION_TRANSITION lines in bomb_runtime_log.txt is within plus or minus one of the count of origin=AUTO lines in the corresponding expected file.
8 points · REGULAR · correctness

30
In bomb_runtime_log.txt, between consecutive origin=AUTO ACTION_TRANSITION lines with no intervening origin=INPUT line, the number of intervening MOTION_SAMPLE lines is within plus or minus one of the corresponding count in the expected file.
8 points · REGULAR · correctness
