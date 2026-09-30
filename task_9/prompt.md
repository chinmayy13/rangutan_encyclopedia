Hi — I'm putting together a playable prototype for our Thursday gameplay review and I need it built in Godot so the team can run it themselves instead of watching a capture.

The art is already approved. source_coin_token.png is the production coin face that every board token has to carry, Bomb.glb is the bomb model our 3D artist delivered, and scene_reference.png is the signed-off screen from our art director. Treat that reference as the spec rather than as loose inspiration: everything visible in it has to come back in the build, including the framed play area with its internal grid lines, how many tokens sit on the board and how they are arranged row by row, the horizontal offset between rows, the collection strip along the bottom edge and where its label sits on it, the title across the top, and the HUD column on the left with its exact wording and line breaks.

Pressing Space or clicking triggers a single radial blast from the middle of the board that pushes every token away from the centre, each along its own trajectory. Tokens then fall under gravity, bounce off the inner walls of the frame, and are collected once they cross the collection strip, with each collected token raising the collected counter and each trigger raising the action counter. The same blast also fires automatically on a three-second cycle so the board never sits idle during the review, and the board keeps itself populated so it never empties out.

Bomb.glb has to be rendered live as an actual 3D object while the scene runs, in its own viewport panel placed beside the board in the empty area to its right, with a dedicated 3D camera and at least two lights positioned so that both the model's silhouette and its top surface read clearly against the dark background. It is a live 3D preview rather than a still image, and it must not overlap the framed play area.

While the scene runs, print one telemetry line per second in the form

MOTION_SAMPLE mechanic=<name> t=<seconds> first=(<x>,<y>) collected=<n> actions=<n>

and one line every time the blast fires, in the form

ACTION_TRANSITION mechanic=<name> origin=<AUTO|INPUT> count=<n>

where origin distinguishes the automatic cycle from a player trigger.

Three things for me, all saved to the Desktop. The complete editable project as Bomb_Chain_Reaction_Godot_Project.zip, containing project.godot and every scene, script and local asset needed to open and run it with no missing dependencies. A screenshot of the running game as bomb_blast_frame.png, taken at a moment when the blast ring is still expanding and the HUD counters are legible, with the 3D bomb panel visible in the same frame. And the captured console output as bomb_runtime_log.txt, covering at least twelve continuous seconds of play and containing both an automatic and a player-triggered action line.
