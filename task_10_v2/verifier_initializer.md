# Initializer and verifier JSON (templates)

Fill every `PASTE_*` from the platform: input URLs from *Initial Files Upload* ("Starting File URLs to be used in Task Initializer"), expected-file URLs from *Asset Upload* (link icon). Both must be `scale-cds://…#s3/scale-cds-public-us-west-2` with **no** `Expires=` parameter. File names in the initializer, verifier and Asset section must match exactly. Last block in each list has **no trailing comma**. The previous submission failed on a missing closing bracket and on stale golden links, so paste the result into a JSON validator before clicking Execute.

## Initial Files Upload section — upload these nine
`CTS.txt`, `Agn.txt` (v2), `CTSAgn.xlsx`, `CTSAgn_After.xlsx`, `CTSAgn_batch_economics.csv` (v2), `Thermal_Screening_Note.pdf` (v2), `Stage_Gate_Policy.pdf` (new), `Regeneration_Guidance_Bulletin.pdf`, `plot_template.xcf`.
Remove from the section anything left over from the seed (`DTG Thermogram.png`, `adsorbent_economic_analysis.csv`, `CTSAgn After.xlsx` with a space, `Composite_DTG_Overlay.png`). Unchanged files are in `../task_10/initial_files/`, changed/new ones in `initial_files/`. Do not upload the GTFs here.

## Initializer
```json
{
  "config": [
    {
      "type": "download",
      "parameters": {
        "files": [
          {"url": "PASTE_CTS_TXT",        "path": "/home/docker/Desktop/CTS.txt"},
          {"url": "PASTE_AGN_TXT",        "path": "/home/docker/Desktop/Agn.txt"},
          {"url": "PASTE_CTSAGN_XLSX",    "path": "/home/docker/Desktop/CTSAgn.xlsx"},
          {"url": "PASTE_CTSAGN_AFTER",   "path": "/home/docker/Desktop/CTSAgn_After.xlsx"},
          {"url": "PASTE_ECON_CSV",       "path": "/home/docker/Desktop/CTSAgn_batch_economics.csv"},
          {"url": "PASTE_SCREENING_NOTE", "path": "/home/docker/Desktop/Thermal_Screening_Note.pdf"},
          {"url": "PASTE_STAGE_GATE",     "path": "/home/docker/Desktop/Stage_Gate_Policy.pdf"},
          {"url": "PASTE_BULLETIN",       "path": "/home/docker/Desktop/Regeneration_Guidance_Bulletin.pdf"},
          {"url": "PASTE_TEMPLATE_XCF",   "path": "/home/docker/Desktop/plot_template.xcf"}
        ]
      }
    }
  ],
  "evaluator": {}
}
```
Nine files, nine paths, braces balanced. No `_output` files in this block.

## Verifier (rubric block is auto-filled by the platform; do not edit it)
```json
{
  "config": [],
  "evaluator": {
    "func": "agent_judge_multi",
    "expected": [
      {"dest": "Thermal_Stability_Assessment.pdf", "path": "PASTE_GTF_PDF",  "type": "cloud_file"},
      {"dest": "Adsorbent_Cost_Comparison.docx",   "path": "PASTE_GTF_DOCX", "type": "cloud_file"},
      {"dest": "plot_template_updated.xcf",        "path": "PASTE_GTF_XCF",  "type": "cloud_file"}
    ],
    "result": [
      {"dest": "Thermal_Stability_Assessment.pdf", "path": "/home/docker/Desktop/Thermal_Stability_Assessment.pdf", "type": "vm_file"},
      {"dest": "Adsorbent_Cost_Comparison.docx",   "path": "/home/docker/Desktop/Adsorbent_Cost_Comparison.docx",   "type": "vm_file"},
      {"dest": "plot_template_updated.xcf",        "path": "/home/docker/Desktop/plot_template_updated.xcf",        "type": "vm_file"}
    ],
    "rubric": { "criteria": [ "…auto-populated…" ] }
  }
}
```
The GTFs must be physically on the VM Desktop for the verifier to return 1. Hand-check the three `dest` names against the Asset section spelling (case-sensitive).
