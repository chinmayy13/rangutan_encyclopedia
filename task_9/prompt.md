Hi, I'm putting together a playable prototype for our Thursday gameplay review and I need it built in Godot so the team can run it themselves instead of watching a capture.

Four files are already on the Desktop. source_coin_token.png is the production coin face that every board token has to carry. Bomb.glb is the bomb model our 3D artist delivered. scene_reference.png is the signed-off screen from our art director. gameplay_config.txt has the timing, physics and board parameters that our designer locked in last sprint.

The reference image is the visual authority for this build. Treat it as the spec, not loose inspiration: match the framed play area with its internal grid lines, how the tokens sit on the board row by row including the alternating horizontal offset between rows, the collection strip along the bottom edge and where its label sits, the title across the top, and the HUD column on the left with its exact wording and line breaks. gameplay_config.txt controls timing and physics. Where the config file and the reference image disagree on a visual element like row count or token arrangement, go with what the reference image shows.

Pressing Space or clicking triggers a single radial blast from the middle of the board that pushes every token outward along its own trajectory. Tokens fall under gravity, bounce off the inner walls of the frame, and get collected once they cross the collection strip. Each collected token raises the collected counter and each trigger raises the actions counter. The blast also fires automatically on the repeating cycle defined in gameplay_config.txt so the board never sits idle during the review. The board keeps itself populated so it never empties out.

Bomb.glb has to be rendered live as an actual 3D object while the scene runs, in its own viewport panel placed beside the board in the empty area to its right. It needs a dedicated 3D camera and at least two lights positioned so that both the silhouette and the top surface of the model read clearly against the dark background. This is a live 3D preview, not a still image, and it must not overlap the framed play area.

While the scene runs, print one telemetry line at the sample interval from gameplay_config.txt in the form

MOTION_SAMPLE mechanic=<id> t=<seconds> first=(<x>,<y>) collected=<n> actions=<n>

and one line every time the blast fires, in the form

ACTION_TRANSITION mechanic=<id> origin=<AUTO|INPUT> count=<n>

where <id> is the mechanic identifier from gameplay_config.txt and origin tells apart the automatic cycle from a player trigger.

Three things for me, all saved to the Desktop. The complete editable project as Bomb_Chain_Reaction_Godot_Project.zip, containing project.godot and every scene, script and local asset needed to open and run it with no missing dependencies. A screenshot of the running game as bomb_blast_frame.png, taken at a moment when the blast ring is still expanding and the HUD counters are legible, with the 3D bomb panel visible in the same frame. And the captured console output as bomb_runtime_log.txt, covering at least twelve continuous seconds of play and containing both an automatic and a player-triggered action line.
