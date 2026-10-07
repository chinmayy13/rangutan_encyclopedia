# GTF build spec (build in the VM, then upload to the Asset section)

Every value below is reproduced by `answer_key/compute_answer_key.py` from the v2 input files. Rebuild the GTFs from the **v2** inputs, not from the old GTFs (guidelines §4.1: a GTF built from stale inputs describes data the agent never receives).

## Fixes carried over from the review (all three GTFs)
| Review finding | What to do |
|---|---|
| Peak labels used trace colours, template font colour is #15295d | Peak labels, axis text, title and legend text in the plot are #15295d. Only the two trace lines (and legend swatches) are c91d1d / 277534. |
| Inconsistent label precision (241.372 vs 236.9691) | Temperatures to 1 decimal everywhere (241.4 °C, 237.0 °C), rates to 3 decimals. |
| docx table at 9.5 pt vs the prompt's 10 pt floor | Table, body, notes all ≥10 pt. Check Format ▸ Character on the table too. |
| docx inconsistent heading styles / number formats | Use Heading 1 for the title, Heading 2 for the four sections, same body style throughout. Fixed decimals per column (below). |
| GTF chart green/red vs "template is blue/amber" | Prompt now says the new colours explicitly; plot uses c91d1d (as made) and 277534 (post-adsorption). |
| docx spilled to a second page in my LibreOffice 24 render of the old GTF | Keep the docx to what fits cleanly; a spill is fine but never split the table. |

## 1. `Thermal_Stability_Assessment.pdf` (one page, Letter, margins ≥2.5 cm, body ≥10 pt)
Draft text. Write it in Writer, insert the plot as an image at text width, export to PDF.

**Thermal stability assessment: CTSAgn composite**
*Primary degradation peaks from the September 2018 TGA campaign, read above the water step. Rates are per cent of the 150 °C mass per °C.*

| Material | Peak temperature (°C) | Peak DTG rate (%/°C) |
|---|---|---|
| Chitosan precursor | 305.2 | 1.120 |
| Alginate precursor | 246.8 | 1.270 |
| CTSAgn as made | 241.4 | 0.129 |
| CTSAgn post-adsorption | 237.0 | 0.130 |

[Plot: only the two composite traces, c91d1d "CTSAgn as made", 277534 "CTSAgn post-adsorption", peaks marked and labelled "241.4 °C" and "237.0 °C", labels in #15295d, y-axis extended past the template's 0.28 because the post-adsorption water step reaches ≈0.32 on this basis, template title/axis titles/legend names kept.]

On the lab's 150 °C basis the as-made composite's peak mass-loss rate is 8.7 times lower than chitosan's and 9.9 times lower than alginate's; after loading the factors are 8.6 and 9.8. The composite's peak rate is essentially unchanged by adsorption (0.129 to 0.130 %/°C, +0.6%). On the instrument's initial-mass column it would appear to fall by 14%, but that is the extra water the loaded sample carries, not a change in how fast the dry material decomposes.

The composite peak at 241.4 °C lies below both precursors, 5.4 °C below alginate and 63.8 °C below chitosan, not between them. Its position and the absence of a chitosan-like event near 305 °C are consistent with an alginate-associated decomposition; the traces alone cannot prove the mechanism.

After loading, the peak moves down 4.4 °C, from 241.4 to 237.0 °C. A lower peak temperature is not by itself evidence of earlier onset. Sorbed phosphate and counter-ions may alter the alginate-rich network, but that is a hypothesis, and with the peak rate unchanged neither observation shows stabilisation or earlier breakdown.

For the recovered material, 5% of the mass held at 150 °C has been lost by about 195 °C under the nitrogen ramp. This is the screening handling/regeneration ceiling, about 42 °C below its peak-rate maximum. It is not a demonstrated safe service limit or a measurement of repeated-cycle capacity retention. Regeneration_Guidance_Bulletin.pdf quotes a higher blanket figure of 220 °C, drawn from other products and never measured on this lot; the 195 °C from this material's own trace is the better-supported basis. *(Last text on the page.)*

## 2. `Adsorbent_Cost_Comparison.docx`
Headings: **Adsorbent cost comparison** (Heading 1); **Notes**, **Manufacturing-loss case**, **Break-even**, **Adoption** (Heading 2). Adoption is last.

| Adsorbent | Cost ($/kg) | Cost ($/g) | Capacity (mg/g) | Cost per mg removed ($/mg) | Efficiency (mg/$) |
|---|---|---|---|---|---|
| Biochar | 10.00 | 0.01000 | 30 | 0.000333 | 3000.0 |
| Chitosan | 200.00 | 0.20000 | 100 | 0.002000 | 500.0 |
| Activated Carbon | 150.00 | 0.15000 | 60 | 0.002500 | 400.0 |
| Iron Oxide | 80.00 | 0.08000 | 50 | 0.001600 | 625.0 |
| CTSAgn | 42.92 | 0.04292 | 150 | 0.000286 | 3494.9 |

**Notes.** CTSAgn is costed on the five released pilot batches (1–5): cash cost of $2,146 over 50 kg, i.e. $42.92/kg at the released-batch capacity of 150 mg/g. Cash cost is every pilot cost line except equipment depreciation (Stage_Gate_Policy.pdf §1). Batches 6 and 7 are rejected and not in this figure. Cost per mg removed is cost per gram divided by capacity in mg/g; Efficiency is its reciprocal, mg of phosphate removed per dollar of adsorbent.

**Closest benchmark.** Biochar (3000 mg/$). CTSAgn is at 3494.9 mg/$, 16.5% better, at $0.000286 per mg against $0.000333.

**Manufacturing-loss case.** Carrying the cash cost of all seven batches ($3,093) on the 50 kg released gives $61.86/kg ($0.06186/g), $0.000412 per mg removed and 2,424.8 mg/$ at 150 mg/g, which is 19.2% below biochar. The efficiency lead reverses. This is a sensitivity and does not replace the table entry.

**Break-even.** CTSAgn matches biochar at $50.00/kg, $2,500 for 50 kg, so the released product can absorb $354 more than the $2,146 already charged. The rejected batches cost $947 in cash, so the headroom covers about 37% and $593 cannot be absorbed.

**Adoption.** Hold for validation. Efficiency passes on the table basis but fails on the manufacturing-loss basis; the 195 °C recovered-material ceiling is 20.4 °C above the 175 °C regeneration temperature the benchmark costing assumes, short of the 25 °C margin the policy requires; the trade group's 220 °C is not counted because it was never measured on this material; and the benchmark's three-cycle regeneration has not been demonstrated on CTSAgn (no cycle data exist). Resolve manufacturing losses and run cycle testing before reconsidering.

## 3. `plot_template_updated.xcf`
`plot_template.xcf` is a flat 800×500 file with one raster layer (`plot_template1.png`), so the two traces are pixels, not objects. In GIMP use Colors ▸ Map ▸ Color Exchange on that layer: from `c9941d` (amber) to `c91d1d`, then from `1da6c9` (blue) to `277534`, with a small threshold so the anti-aliased edge pixels follow. Fonts, grid, title and axes must not change (they are `#15295d`/black/grey). Afterwards pick-check the line and legend swatch pixels, confirm no amber/blue remains, then File ▸ Save as XCF.
Reference: renders of old vs updated template from the previous GTF differ in only 216 pixels (the two trace lines and legend swatches), and the `#15295d` text pixel count is identical (4,432), so that is the target.
