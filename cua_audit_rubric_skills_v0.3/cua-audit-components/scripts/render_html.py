#!/usr/bin/env python3
"""Render the audit-rubric review as a self-contained HTML report.

Follows the Scale GenAI Ops feedback-review style documented in
`mcpadv-lh-benchmark-audit/references/report-design.md`: light editorial
layout, thin rules, monospace for identifiers and numbers, sentence-case
headings, no em dashes, count before interpretation.

The page has to stand alone as an attachment. The reader has none of the
working context, so every term is defined on the page and no internal
shorthand appears.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

# raw: the CSS carries its own backslash escapes (\2212 is the minus sign that
# marks an open fold). In a cooked string Python reads that as octal \221.
CSS = r"""
:root{
  --ink:#0b0b0c; --paper:#ffffff; --body:#3a3a3d; --muted:#87878c;
  --faint:#bcbcc0; --line:#e7e7e3; --panel:#f6f6f3; --maxw:760px;
  --fail:#c62d1f; --fail-bg:#fdeae7; --fail-fg:#b32718;
  --warn:#8a5a00; --warn-bg:#fdf3e2;
  --pass:#0e7a4a; --pass-bg:#e5f4ea; --pass-fg:#0b6640;
  --pend:#6e6e74; --pend-bg:#f1f1ee;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--body);
  font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased}
code,.mono,td.n,.pill,.cite{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.wrap{max-width:1060px;margin:0 auto;padding:0 6vw}
.narrow{max-width:var(--maxw)}
section{padding:72px 0;border-bottom:1px solid var(--line)}
section:last-child{border-bottom:0}
h1,h2,h3{color:var(--ink);font-weight:620;letter-spacing:-.01em}
h1.headline{font-size:clamp(2rem,4.6vw,3.2rem);line-height:1.08;margin:.2em 0 .5em}
h2{font-size:1.5rem;margin:0 0 1rem}
h3{font-size:1.02rem;margin:2rem 0 .6rem}
.brand{text-transform:uppercase;font-size:.72rem;letter-spacing:.16em;
  color:var(--muted);margin:0}
.kicker{text-transform:uppercase;font-size:.74rem;letter-spacing:.18em;
  color:var(--muted);margin:0 0 .8rem}
.blurb{font-size:clamp(1.02rem,1.6vw,1.22rem);color:var(--body);max-width:52ch}
p{margin:0 0 1rem}
.dim{color:var(--muted)}
table{border-collapse:collapse;width:100%;margin:1rem 0;
  font-variant-numeric:tabular-nums}
th,td{border:1px solid var(--line);padding:.5rem .65rem;text-align:left;
  font-size:.88rem;vertical-align:top}
th{background:var(--panel);color:var(--ink);font-weight:600;
  font-size:.78rem;text-transform:uppercase;letter-spacing:.06em}
td.n{text-align:right;white-space:nowrap}
td.nw{white-space:nowrap}
tr.tot td{border-top:2px solid var(--ink);font-weight:600}
.pill{display:inline-block;font-size:.64rem;text-transform:uppercase;
  letter-spacing:.06em;padding:.16rem .42rem;border-radius:4px;font-weight:600}
.p2{background:var(--fail-bg);color:var(--fail-fg)}
.p3{background:var(--warn-bg);color:var(--warn)}
.p4{background:var(--pend-bg);color:var(--pend)}
.p5{background:var(--pass-bg);color:var(--pass-fg)}
.s{display:inline-block;min-width:1.5rem;text-align:center;font-weight:600;
  border-radius:3px;padding:.05rem .3rem;font-size:.82rem}
.cite{font-size:.7rem;background:var(--panel);border:1px solid var(--line);
  border-radius:4px;padding:.05rem .3rem;color:var(--ink);text-decoration:none}
.stat{display:flex;gap:2.6rem;flex-wrap:wrap;margin:1.6rem 0 0}
.stat div{min-width:88px}
.stat b{display:block;color:var(--ink);font-size:2rem;line-height:1.1;
  font-variant-numeric:tabular-nums}
.stat span{font-size:.76rem;text-transform:uppercase;letter-spacing:.09em;
  color:var(--muted)}
.unit{padding:56px 0;border-bottom:1px solid var(--line)}
.unit h2{display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap}
.unit h2 code{font-size:1.05rem}
.reasons{list-style:none;padding:0;margin:0}
.reasons li{border-top:1px solid var(--line);padding:.7rem 0 .7rem 1.1rem;
  position:relative;font-size:.92rem}
.reasons li:before{content:"";position:absolute;left:0;top:1.15rem;width:6px;
  height:6px;background:var(--ink);border-radius:50%}
.panel{border:1px solid var(--line);margin:1rem 0}
.panel>.head{background:var(--panel);padding:.45rem .7rem;font-size:.74rem;
  text-transform:uppercase;letter-spacing:.08em;color:var(--muted);
  border-bottom:1px solid var(--line)}
.panel>.body{padding:.85rem .7rem;font-size:.92rem}
.grid28{display:grid;grid-template-columns:repeat(auto-fill,minmax(172px,1fr));
  gap:1px;background:var(--line);border:1px solid var(--line)}
.c{background:var(--paper);padding:.45rem .55rem;font-size:.78rem;
  display:flex;justify-content:space-between;gap:.4rem;align-items:baseline}
.c .t{color:var(--body);line-height:1.3}
.cs{display:flex;gap:.28rem;align-items:baseline;white-space:nowrap}
.rdot{display:inline-block;min-width:1.15rem;text-align:center;font-weight:700;
  font-size:.66rem;padding:.09rem .26rem;border-radius:3px;
  background:var(--warn-bg);color:var(--warn);border:1px solid #e8d5ad;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.recbox{border:1px solid #e8d5ad;background:#fffdf7;margin:1rem 0}
.recbox>.head{background:var(--warn-bg);color:var(--warn);padding:.45rem .7rem;
  font-size:.74rem;text-transform:uppercase;letter-spacing:.08em;
  border-bottom:1px solid #e8d5ad;font-weight:600}
.recbox>.body{padding:.85rem .7rem}
.recbox table{margin:0}
.recbox ul.reasons li:first-child{border-top:0;padding-top:0}
.recbox ul.reasons li:first-child:before{top:.45rem}
ul.reasons li.hg,ul.reasons li.hg code{font-weight:700;color:var(--ink)}
ul.reasons li.hg:before{background:var(--warn)}
a{color:var(--ink)}
footer{padding:48px 0;color:var(--faint);font-size:.8rem}
details{border:1px solid var(--line);margin:.55rem 0}
details>summary{background:var(--panel);padding:.45rem .7rem;cursor:pointer;
  font-size:.76rem;text-transform:uppercase;letter-spacing:.07em;
  color:var(--muted);list-style:none}
details>summary::-webkit-details-marker{display:none}
details>summary:before{content:"+ ";color:var(--ink);font-weight:700}
details[open]>summary:before{content:"\2212 "}
details>summary:hover{color:var(--ink)}
details .in{padding:.7rem}
/* A table row that folds. The columns stay scannable and the prose is one
   click away, so it no longer has to be truncated to keep the table readable.
   Marker and colours are inherited from the appendix folds above, so the
   gesture a reader learns there is the same one here. */
details.row{border:0;margin:0;background:none}
details.row>summary{background:none;border:0;padding:0;font-size:.88rem;
  text-transform:none;letter-spacing:0;color:var(--body)}
details.row>summary:hover{color:var(--ink)}
details.row[open]>summary{color:var(--muted);margin-bottom:.5rem}
details.row>.in{padding:0}
.fold{white-space:pre-wrap;font-size:.88rem}
.fold+.fold{margin-top:.6rem;padding-top:.6rem;border-top:1px solid var(--line)}
.fold b{color:var(--ink)}
pre{margin:0;white-space:pre-wrap;word-break:break-word;font-size:.76rem;
  line-height:1.5;max-height:460px;overflow:auto;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color:var(--body)}
.evhead{display:flex;gap:1.2rem;flex-wrap:wrap;font-size:.8rem;
  color:var(--muted);margin:.2rem 0 .8rem}
.evhead b{color:var(--ink);font-weight:600}
@media print{section,.unit{break-inside:avoid}details{break-inside:avoid}
  details>.in{display:block}}
"""

BAND = {2: ("p2", "fail"), 3: ("p3", "non-fail"), 4: ("p4", "non-fail"),
        5: ("p5", "pass")}

CAP = 220_000          # per embedded text block


def _det(label: str, body: str, mono: bool = True) -> str:
    inner = f"<pre>{body}</pre>" if mono else body
    return (f"<details><summary>{html.escape(label)}</summary>"
            f"<div class=in>{inner}</div></details>")


def _fold(summary: str, body: str) -> str:
    """One row's prose, folded behind the same toggle as the appendix.

    Both arguments arrive already escaped or rendered: a summary is built from
    a teaser and a body often carries markup of its own.
    """
    return (f"<details class=row><summary>{summary}</summary>"
            f"<div class=in>{body}</div></details>")


def _teaser(text: str, n: int = 130) -> str:
    """A one-line opening for a fold's summary, cut at a word boundary.

    Markdown markers are stripped rather than rendered: a cut that lands
    inside `**bold**` would leak the asterisks into the summary.
    """
    s = re.sub(r"[*`]", "", " ".join((text or "").split()))
    if len(s) <= n:
        return e(s)
    cut = s.rfind(" ", 0, n)
    return e(s[:cut if cut > 40 else n].rstrip(" ,;:.")) + " ..."


def _read(p: Path) -> str:
    if not p.exists():
        return "(not present)"
    s = p.read_text(encoding="utf-8", errors="replace")
    return (s[:CAP] + f"\n\n[truncated at {CAP:,} characters]"
            if len(s) > CAP else s)


def _renders(d: Path) -> list[str]:
    """The page images the review looked at, linked rather than embedded.

    A reader checking a visual finding needs to see the same page the reviewer
    saw. Links keep this report small — they are relative to the unit directory
    the report is written into, so they resolve as long as it stays beside
    `render/`.
    """
    try:
        idx = json.loads((d / "render_index.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    body = []
    for side in ("inputs", "expected"):
        for ent in idx.get(side) or []:
            pages = ent.get("pages") or []
            if not pages or ent.get("mode") == "native":
                continue
            rel = f"render/{side}/{ent['path']}"
            links = " ".join(f"<a href='{html.escape(f'{rel}/{p}')}'>{p[5:-4]}</a>"
                             for p in pages)
            ok = ent.get("visual_verifiable")
            state = (f"parity {e(ent.get('parity'))}" if ok
                     else f"<b>{e(ent.get('status'))}</b>")
            note = ent.get("unverifiable_reason") or ent.get("parity_gap") or ""
            body.append(
                f"<tr><td>{e(side)}</td><td>{e(ent['path'])}</td>"
                f"<td>{len(pages)}</td><td>{state}</td>"
                f"<td class=mono style='font-size:.7rem'>{links}</td>"
                f"<td class=dim>{e(ent.get('renderer'))}"
                + (f"<br>{e(note)}" if note else "") + "</td></tr>")

    if not body:
        return []
    s = idx.get("summary") or {}
    head = (f"Rendered pages — {s.get('pages_rendered', 0)} page(s), "
            f"{s.get('visual_verifiable', 0)} file(s) visually verifiable"
            + ("" if s.get("parity_ok") else ", renderer parity gap"))
    return [_det(head,
                 "<table><tr><th>Side</th><th>File</th><th class=n>Pages</th>"
                 "<th>State</th><th>Pages</th><th>Renderer</th></tr>"
                 + "".join(body) + "</table>", mono=False)]


def evidence(unit: str, audit_dir: Path, rows: list[dict]) -> str:
    """Everything a reader needs to check a score, embedded in the page."""
    d = audit_dir / unit
    bp = d / "bundle.json"
    if not bp.exists():
        return ""
    b = json.loads(bp.read_text(encoding="utf-8"))
    out = ["<h3>Evidence</h3>",
           "<p class=dim>The submission as the review saw it. Everything below "
           "is embedded in this file.</p>"]

    ins = b.get("input_files") or []
    exp = b.get("expected_files") or []
    ver = b.get("verifier") or {}
    out.append(
        f"<div class=evhead>"
        f"<span><b>{len(b.get('criteria') or [])}</b> criteria</span>"
        f"<span><b>{len(ins)}</b> input files</span>"
        f"<span><b>{len(exp)}</b> expected files</span>"
        f"<span>verifier <b>{e(ver.get('func'))}</b></span>"
        f"<span>domain <b>{e(b.get('domain'))}</b></span></div>")

    out.append(_det("Prompt given to the agent", e(b.get("prompt"))))

    if b.get("seed_prompt"):
        out.append(_det("Seed prompt the contributor started from",
                        e(b["seed_prompt"])))

    crits = b.get("criteria") or []
    if crits:
        tot = sum(c.get("weight") or 0 for c in crits)
        rowsh = "".join(
            f"<tr><td class=mono>{c.get('n')}</td>"
            f"<td class=n>{c.get('weight')}</td>"
            f"<td>{e(c.get('category'))}</td><td>{e(c.get('type'))}</td>"
            f"<td>{e(c.get('title'))}</td></tr>" for c in crits)
        out.append(_det(
            f"Rubric, {len(crits)} criteria, total weight {tot}",
            "<table><tr><th>#</th><th class=n>Weight</th><th>Category</th>"
            f"<th>Tag</th><th>Criterion</th></tr>{rowsh}</table>", mono=False))

    files = "".join(
        f"<tr><td>{e(f.get('path') or f.get('dest'))}</td>"
        f"<td class=mono style='font-size:.7rem'>{e(f.get('url'))}</td></tr>"
        for f in ins + exp)
    if files:
        out.append(_det("Input and expected file locations",
                        "<table><tr><th>Path</th><th>Source</th></tr>"
                        f"{files}</table>", mono=False))

    out.append(_det("Input files, extracted to text",
                    e(_read(d / "inputs_extracted.md"))))
    out.append(_det("Expected files, extracted to text",
                    e(_read(d / "expected_extracted.md"))))
    out += _renders(d)

    mech = b.get("mechanical") or {}
    if mech:
        out.append(_det("Precomputed checks",
                        e(json.dumps(mech, indent=1, ensure_ascii=False))))

    ar = b.get("agent_runs") or {}
    if ar.get("present"):
        out.append(_det(
            f"Agent runs, {ar.get('n_scored')} scored of "
            f"{ar.get('n_instances')}", e(json.dumps(
                {k: v for k, v in ar.items() if k != "runs"}, indent=1,
                ensure_ascii=False))))

    per = []
    for x in rows:
        p = d / "components" / f"{x['num']}.json"
        if p.exists():
            per.append(f"// {x['num']} {x['title']}\n" + p.read_text(encoding="utf-8"))
    if per:
        out.append(_det("Raw result for each of the 28 components",
                        e("\n\n".join(per))[:CAP]))

    scp = d / "sense_check.json"
    if scp.exists():
        out.append(_det("Raw senior review result", e(_read(scp))))

    icp = d / "input_consistency.json"
    if icp.exists():
        out.append(_det("Raw input-consistency result", e(_read(icp))))
    return "".join(out)


def e(x) -> str:
    return html.escape("" if x is None else str(x))


# Recommendations that are unscored on this form yet are a hard FAIL in the
# reference eval. Both halves are required, which is why format/extension and
# archive integrity are absent: component 10 can already score those at 2.
# The whole bullet prints in bold so a reader scanning a component that scored 5
# does not skim past one. Mirrors HARD_GATE in `_generate.py`, matched on the
# entry's opening phrase.
HARD_GATE = (
    "domain fit and expertise level",
    "thin complexity",
    "spreadsheet-only deliverables",
    "criterion that tests both correctness and visual",
    "prompt-constrained style not followed",
)


def is_hard_gate(entry: str) -> bool:
    head = re.sub(r"[*`_]", "", entry or "")[:140].lower()
    return any(p in head for p in HARD_GATE)


def md(x) -> str:
    """Escape, then honour the inline markdown the component definitions use.

    Recommendations are written with `**emphasis**` and `` `identifiers` ``
    because that is how the component files ask for them; rendered raw they
    read as noise.
    """
    s = e(x)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s, flags=re.S)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def _score(s) -> str:
    if not isinstance(s, int):
        return '<span class="dim">not run</span>'
    return f'<span class="s {BAND[s][0]}">{s}</span>'


# The input-consistency pass reports a word, not a score, so it borrows the
# score palette rather than introducing a second one: red for a finding that
# changes what a correct submission looks like, amber for one that does not,
# green for a clean comparison.
IC_BAND = {"major": ("p2", "major issues"),
           "minor": ("p3", "minor issues"),
           "none": ("p5", "no issues")}


def _ic_pill(verdict, short: bool = False) -> str:
    """`short` labels one finding; the long form labels a whole submission."""
    cls, label = IC_BAND.get(verdict or "", ("p4", "unknown"))
    return f'<span class="pill {cls}">{verdict if short else label}</span>'


def _ic_cell(ic: dict, findings: list[dict]) -> str:
    """The summary, with every finding folded behind it."""
    summary = ic.get("summary") or ""
    if not findings:
        body = [f"<div class=fold>{e(summary)}</div>"]
        if ic.get("files_checked"):
            body.append("<div class=fold><b>Files compared.</b> "
                        + e(", ".join(ic["files_checked"])) + "</div>")
        if ic.get("blocked_on"):
            body.append(f"<div class=fold><b>Blocked on.</b> "
                        f"{e(ic['blocked_on'])}</div>")
        return _fold(_teaser(summary), "".join(body))

    body = [f"<div class=fold>{e(summary)}</div>"]
    for f in sorted(findings, key=lambda x: x.get("severity") != "major"):
        owner = (f"owned by component <code>{e(f['component'])}</code>"
                 if f.get("component") else "no component covers this")
        body.append(
            "<div class=fold>"
            f"{_ic_pill(f.get('severity'), short=True)} "
            f"<code>{e(f.get('kind'))}</code> "
            f"<span class=dim>{e(' / '.join(f.get('files') or []))}</span><br>"
            f"<b>A.</b> {e(f.get('statement_a'))}<br>"
            f"<b>B.</b> {e(f.get('statement_b'))}<br>"
            f"<b>Why they conflict.</b> {e(f.get('why_conflict'))}<br>"
            f"<b>Graded impact.</b> {e(f.get('graded_impact'))} "
            f"<span class=dim>({owner})</span><br>"
            f"<b>Fix.</b> {e(f.get('fix'))}</div>")
    if ic.get("blocked_on"):
        body.append(f"<div class=fold><b>Blocked on.</b> "
                    f"{e(ic['blocked_on'])}</div>")
    return _fold(_teaser(summary), "".join(body))


def render(rows: list[dict], audit_dir: Path | None = None) -> str:
    n = len(rows)
    fail = sum(1 for r in rows if r["verdict"] is not None and r["verdict"] <= 2)
    nonfail = sum(1 for r in rows if r["verdict"] in (3, 4))
    npass = sum(1 for r in rows if r["verdict"] == 5)
    esc = sum(len((r.get("sense") or {}).get("escalations") or []) for r in rows)
    con = sum(len((r.get("sense") or {}).get("contradictions") or []) for r in rows)
    rec = sum(len(x.get("minor_issues") or []) for r in rows for x in r["rows"])
    rec5 = sum(len(x.get("minor_issues") or []) for r in rows for x in r["rows"]
               if x.get("score") == 5)

    h = [f"<!doctype html><meta charset=utf-8>",
         "<meta name=viewport content='width=device-width,initial-scale=1'>",
         "<title>CUA audit rubric review</title>", f"<style>{CSS}</style>",
         "<div class=wrap>"]

    # ---- hero
    h += ["<section>",
          "<p class=brand>Scale GenAI Ops / CUA v3</p>",
          "<h1 class=headline>Audit rubric review</h1>",
          f"<p class=blurb>{n} task submission{'' if n == 1 else 's'} scored "
          "against the 28 components "
          "of the CUA v3 audit rubric, one component at a time, then read across "
          "components by a senior review pass.</p>",
          f"""<div class=stat>
            <div><b>{n}</b><span>submissions</span></div>
            <div><b>{n * 28}</b><span>component scores</span></div>
            <div><b>{fail}</b><span>fail</span></div>
            <div><b>{nonfail}</b><span>non-fail</span></div>
            <div><b>{npass}</b><span>pass</span></div>
            <div><b>{esc}</b><span>escalations</span></div>
            <div><b>{con}</b><span>contradictions</span></div>
            <div><b>{rec}</b><span>recommendations</span></div>
          </div>""",
          "</section>"]

    # ---- how to read
    h += ["<section class=narrow>",
          "<p class=kicker>How to read this</p>",
          "<h2>What was scored</h2>",
          "<p>Each submission is a contributor's completed CUA v3 task: a prompt, "
          "the input files an agent receives, the expected output files that serve "
          "as the answer key, a weighted rubric, and a verifier configuration. The "
          "audit rubric is the review form a human reviewer fills in. It has 28 "
          "components covering the task, the prompt, the expected files, the "
          "rubric, and the verifier JSON.</p>",
          "<p>Every component was scored by its own model call reading only that "
          "component's definition and the evidence it needs. Component definitions "
          "are generated from the review form itself, so the score options and "
          "thresholds are the form's, not this tool's.</p>",
          "<h3>Scores</h3>",
          "<table><tr><th>Score</th><th>Band</th><th>Meaning</th></tr>"
          "<tr><td class=n>" + _score(2) + "</td><td>fail</td>"
          "<td>The component's failing condition is met.</td></tr>"
          "<tr><td class=n>" + _score(3) + "</td><td>non-fail</td>"
          "<td>An issue is present below the failing threshold.</td></tr>"
          "<tr><td class=n>" + _score(4) + "</td><td>non-fail</td>"
          "<td>A minor issue. Two components use 4 instead of 3.</td></tr>"
          "<tr><td class=n>" + _score(5) + "</td><td>pass</td>"
          "<td>Clean.</td></tr></table>",
          "<p>Score sets differ by component. Seven components allow only 2 or 5, "
          "with no middle band.</p>",
          "<h3>The verdict</h3>",
          "<p>A submission takes the lowest score across all 28 components. One "
          "component at 2 makes the whole submission a fail. Every component must "
          "be 5 for the submission to pass.</p>",
          "<h3>Recommendations, and why a 5 can still carry them</h3>",
          "<p>The review form has 28 components and no more, so a real defect "
          "that none of their answer options describes has nowhere to be scored. "
          "Those are recorded separately as <b>recommendations</b>. They never "
          "move a score, a label or the verdict, which means a component can "
          "score 5 and still carry work the contributor should do before "
          "submitting.</p>",
          f"<p>This report carries <b>{rec}</b> "
          f"{'recommendation' if rec == 1 else 'recommendations'}, "
          f"<b>{rec5}</b> of them on components that scored 5. They are listed "
          "per submission below, and every component in the 28-score grid that "
          "carries one is marked with an amber count beside its score. A clean "
          "grid is not the same as nothing to fix.</p>",
          "<p class=dim>Examples of what lands here: placeholder text or encoding "
          "damage in an expected file, criterion markup and grammar, a rubric of "
          "10 to 14 criteria, an output filename that is awkward but resolvable, "
          "and a criterion that states no comparison tolerance. Each is a genuine "
          "defect the form does not ask about.</p>",
          "<h3>The senior review pass</h3>",
          "<p>Component scores are produced in isolation, so a fact found by one "
          "component and its consequence in another are never seen together. A "
          "final pass reads all 28 results for a submission and reports three "
          "things it can see that the individual scores cannot: contradictions "
          "between two components' claims, escalation proposals where the wider "
          "picture supports a lower score, and which component the verdict rests "
          "on. It cannot change a score, and it can only propose moving a score "
          "toward a fail, never away from one.</p>",
          "</section>"]

    # ---- triage
    h += ["<section>", "<p class=kicker>Triage</p>",
          "<h2>All submissions</h2>",
          "<p class=dim>Verdict, the component that drives it, and the first fix. "
          "Follow a row to its detail below.</p>",
          "<table><tr><th>Submission</th><th>Domain</th><th class=n>Verdict</th>"
          "<th>Driven by</th><th class=n>Esc</th><th class=n>Con</th>"
          "<th class=n>Rec</th><th>First fix</th></tr>"]
    for r in rows:
        sc = r.get("sense") or {}
        drv = sc.get("verdict_driver") or []
        names = ", ".join(
            f"{d} {next((x['title'] for x in r['rows'] if x['num'] == d), '')}"
            for d in drv) or '<span class=dim>not reviewed</span>'
        fx = sorted(sc.get("fix_order") or [], key=lambda x: x["rank"])
        first = fx[0]["fix"] if fx else ""
        nrec = sum(len(x.get("minor_issues") or []) for x in r["rows"])
        h.append(
            f"<tr><td><a href='#u{e(r['unit'])}'><code>{e(r['unit'][:12])}</code></a></td>"
            f"<td>{e(r['domain'])}</td>"
            f"<td class=n>{_score(r['verdict'])}</td>"
            f"<td>{names}</td>"
            f"<td class=n>{len(sc.get('escalations') or [])}</td>"
            f"<td class=n>{len(sc.get('contradictions') or [])}</td>"
            f"<td class=n>{f'<b>{nrec}</b>' if nrec else '<span class=dim>.</span>'}</td>"
            f"<td>{e(first)[:190]}</td></tr>")
    h.append("</table>")
    h.append("<p class=dim>Rec counts unscored recommendations. A submission can "
             "pass with a verdict of 5 and still carry them.</p>")

    # ---- input file consistency
    h += ["<h3>Input file consistency</h3>",
          "<p class=dim>Whether the material the task is built from agrees with "
          "itself: the input files against each other, and against the prompt, "
          "the expected files and the criteria. The 28 components each grade one "
          "artifact against the review form, and none of them asks this, so a "
          "submission can score clean on all 28 while two supplied sources state "
          "different rules for the same quantity.</p>",
          "<p class=dim><b>Major</b> means the inconsistency changes what a "
          "correct submission looks like: an agent working faithfully from the "
          "inputs cannot reach the graded answer, or has to guess between two "
          "supplied rules that lead to different graded values. <b>Minor</b> "
          "means a real inconsistency that moves no graded output. This pass is "
          "never scored and never reaches the verdict.</p>",
          "<table><tr><th>Submission</th><th>State</th><th class=n>Major</th>"
          "<th class=n>Minor</th><th class=n>Rules</th>"
          "<th>What the check found</th></tr>"]
    for r in rows:
        ic = r.get("inputs") or {}
        if not ic:
            h.append(
                f"<tr><td><a href='#u{e(r['unit'])}'>"
                f"<code>{e(r['unit'][:12])}</code></a></td>"
                f"<td class=nw><span class='pill p4'>not run</span></td>"
                f"<td class=n><span class=dim>.</span></td>"
                f"<td class=n><span class=dim>.</span></td>"
                f"<td class=n><span class=dim>.</span></td>"
                f"<td class=dim>No <code>input_consistency.json</code>. The "
                f"supplied files were never compared against each other.</td>"
                f"</tr>")
            continue
        fnd = ic.get("findings") or []
        nmaj = sum(1 for x in fnd if x.get("severity") == "major")
        nmin = len(fnd) - nmaj
        rc = ic.get("rules_compared") or 0
        h.append(
            f"<tr><td><a href='#u{e(r['unit'])}'>"
            f"<code>{e(r['unit'][:12])}</code></a></td>"
            f"<td class=nw>{_ic_pill(ic.get('verdict'))}</td>"
            f"<td class=n>{f'<b>{nmaj}</b>' if nmaj else '<span class=dim>.</span>'}</td>"
            f"<td class=n>{nmin or '<span class=dim>.</span>'}</td>"
            f"<td class=n>{len(rc) if isinstance(rc, list) else rc}</td>"
            f"<td>{_ic_cell(ic, fnd)}</td></tr>")
    h.append("</table>")
    h.append("<p class=dim>Rules counts the shared rules, thresholds and "
             "quantities that were stated in more than one place and so could be "
             "cross-checked. A finding already covered by a scored component "
             "names that component; the rest have no home on the review "
             "form.</p>")

    # ---- component pattern across submissions
    h += ["<h3>Scores by component across all submissions</h3>",
          "<p class=dim>A component scoring low on many submissions points at a "
          "systemic authoring issue or at the component's own calibration.</p>",
          "<table><tr><th>#</th><th>Component</th><th class=n>2</th>"
          "<th class=n>3</th><th class=n>4</th><th class=n>5</th>"
          "<th class=n>Drives</th><th class=n>Rec</th></tr>"]
    order = [x["num"] for x in rows[0]["rows"]] if rows else []
    for num in order:
        title = next(x["title"] for x in rows[0]["rows"] if x["num"] == num)
        cnt = {2: 0, 3: 0, 4: 0, 5: 0}
        nrec = 0
        for r in rows:
            x = next((y for y in r["rows"] if y["num"] == num), None)
            s = x["score"] if x else None
            if isinstance(s, int):
                cnt[s] = cnt.get(s, 0) + 1
            nrec += len((x or {}).get("minor_issues") or [])
        drives = sum(1 for r in rows
                     if num in ((r.get("sense") or {}).get("verdict_driver") or []))
        cells = "".join(
            f"<td class=n>{cnt[k] or '<span class=dim>.</span>'}</td>"
            for k in (2, 3, 4, 5))
        h.append(f"<tr><td class=mono>{num}</td><td>{e(title)}</td>{cells}"
                 f"<td class=n>{drives or '<span class=dim>.</span>'}</td>"
                 f"<td class=n>{nrec or '<span class=dim>.</span>'}</td></tr>")
    h += ["</table>", "</section>"]

    # ---- per unit
    h.append("<section><p class=kicker>Detail</p><h2>By submission</h2></section>")
    for r in rows:
        sc = r.get("sense") or {}
        band = BAND[r["verdict"]][1] if isinstance(r["verdict"], int) else "incomplete"
        h += [f"<div class=unit id='u{e(r['unit'])}'>",
              f"<h2><code>{e(r['unit'])}</code> {_score(r['verdict'])} "
              f"<span class=dim>{e(band)}</span></h2>",
              f"<p class=dim>{e(r['domain'])} · {r['n_run']} of 28 components "
              f"scored</p>"]

        if r["problems"]:
            h += ["<div class=panel><div class=head>Output contract issues</div>"
                  "<div class=body><ul class=reasons>"
                  + "".join(f"<li>{e(p)}</li>" for p in r["problems"])
                  + "</ul></div></div>"]

        if sc:
            h += [f"<div class=panel><div class=head>What the verdict rests on</div>"
                  f"<div class=body>{e(sc.get('fragility'))}</div></div>",
                  f"<p>{e(sc.get('summary'))}</p>"]

            if sc.get("fix_order"):
                h += ["<h3>Fix order</h3><ul class=reasons>"]
                for f in sorted(sc["fix_order"], key=lambda x: x["rank"]):
                    t = next((x["title"] for x in r["rows"]
                              if x["num"] == f["component"]), "")
                    h.append(f"<li><code>{e(f['component'])}</code> {e(t)}. "
                             f"{e(f['fix'])}</li>")
                h.append("</ul>")

            if sc.get("escalations"):
                h += ["<h3>Escalation proposals</h3>",
                      "<p class=dim>Proposed by the senior review pass and not "
                      "applied. The verdict above uses the component scores as "
                      "returned.</p>",
                      "<table><tr><th>#</th><th>Component</th><th class=n>Now</th>"
                      "<th class=n>Proposed</th><th>Reasoning</th></tr>"]
                for x in sc["escalations"]:
                    t = next((y["title"] for y in r["rows"]
                              if y["num"] == x["component"]), "")
                    h.append(f"<tr><td class=mono>{e(x['component'])}</td>"
                             f"<td>{e(t)}</td>"
                             f"<td class=n>{_score(x['current_score'])}</td>"
                             f"<td class=n>{_score(x['proposed_score'])}</td>"
                             f"<td>{e(x['reasoning'])[:900]}</td></tr>")
                h.append("</table>")

            if sc.get("contradictions"):
                h += ["<h3>Contradictions between components</h3>",
                      "<table><tr><th>Components</th><th>Conflict</th></tr>"]
                for c in sc["contradictions"]:
                    h.append(f"<tr><td class=mono>{e(', '.join(c['components']))}</td>"
                             f"<td>{e(c['why_conflict'])[:700]}</td></tr>")
                h.append("</table>")

            if sc.get("unverified"):
                h += ["<h3>Not verified</h3>",
                      "<p class=dim>These components could not be settled from the "
                      "available evidence. The defect classes they cover are "
                      "unexamined.</p><ul class=reasons>"]
                for u in sc["unverified"]:
                    h.append(f"<li><code>{e(u['component'])}</code> "
                             f"{e(u['unexamined'])}</li>")
                h.append("</ul>")

        if audit_dir is not None:
            h.append(evidence(r["unit"], audit_dir, r["rows"]))

        urec = [(x, x.get("minor_issues") or []) for x in r["rows"]
                if x.get("minor_issues")]
        n_urec = sum(len(m) for _, m in urec)

        h += ["<h3>All 28 component scores</h3>"]
        if n_urec:
            h.append(f"<p class=dim>An amber count beside a score means that "
                     f"component recorded unscored recommendations. "
                     f"{n_urec} in total, listed below.</p>")
        h.append("<div class=grid28>")
        for x in r["rows"]:
            mi = x.get("minor_issues") or []
            tag = (f"<span class=rdot title='{len(mi)} unscored "
                   f"recommendation{'' if len(mi) == 1 else 's'}'>{len(mi)}</span>"
                   if mi else "")
            h.append(f"<div class=c><span class=t>"
                     f"<span class=mono>{x['num']}</span> {e(x['title'])}</span>"
                     f"<span class=cs>{tag}{_score(x['score'])}</span></div>")
        h.append("</div>")

        low = [x for x in r["rows"] if isinstance(x["score"], int) and x["score"] < 5]
        if low:
            h += ["<h3>Findings</h3>",
                  "<p class=dim>One row per component that scored below 5. Open a "
                  "row for the reviewer's full reasoning.</p>",
                  "<table><tr><th>#</th><th>Component</th><th class=n>Score</th>"
                  "<th>Label on the review form</th><th>Finding</th></tr>"]
            for x in sorted(low, key=lambda y: (y["score"], y["num"])):
                why = x.get("justification") or x.get("evidence") or ""
                # Folded, so the reasoning is given whole. The old flat cell had
                # to stop at 800 characters, which cut most findings mid-argument.
                body = [f"<div class=fold>{e(why)}</div>"]
                ev = x.get("evidence")
                if ev and ev != why:
                    body.append(f"<div class=fold><b>Evidence.</b> {e(ev)}</div>")
                if x.get("blocked_on"):
                    body.append(f"<div class=fold><b>Blocked on.</b> "
                                f"{e(x['blocked_on'])}</div>")
                if x.get("confidence"):
                    body.append(f"<div class=fold><b>Confidence.</b> "
                                f"{e(x['confidence'])}</div>")
                h.append(f"<tr><td class=mono>{x['num']}</td><td>{e(x['title'])}</td>"
                         f"<td class=n>{_score(x['score'])}</td>"
                         f"<td class=mono style='font-size:.74rem'>"
                         f"{e(x.get('error_category'))}</td>"
                         f"<td>{_fold(_teaser(why), ''.join(body))}</td></tr>")
            h.append("</table>")

        wai = next((x["whole_answer_inputs"] for x in r["rows"]
                    if x.get("whole_answer_inputs") is not None), None)
        if wai is not None:
            h.append("<h3>Value criteria that one input answers in full</h3>")
            if not wai:
                h.append("<p class=dim>Component 27, Value Binding, found no value "
                         "criteria in this rubric.</p>")
            else:
                held = sum(1 for g in wai if g.get("input"))
                h += [f"<p class=dim>{held} of {len(wai)} groups of value criteria "
                      "have one supplied input that prints every value they grade, "
                      "text values such as material names included. A response "
                      "that copies that input passes the whole group without doing "
                      "the task. Recorded by component 27, Value Binding.</p>",
                      "<table><tr><th>Criteria</th>"
                      "<th>Input that prints all their values</th></tr>"]
                for g in wai:
                    crit = ", ".join(str(n) for n in g.get("criteria") or [])
                    src = (e(g["input"]) if g.get("input")
                           else "<span class=dim>none</span>")
                    h.append(f"<tr><td class=mono>{e(crit)}</td><td>{src}</td></tr>")
                h.append("</table>")

        # Unscored recommendations. Rendered for every submission, including a
        # clean one, and for components that scored 5 -- the whole point is that
        # the score does not reveal them.
        h.append("<h3>Recommendations, not scored</h3>")
        if urec:
            at5 = sum(len(m) for x, m in urec if x.get("score") == 5)
            h += ["<div class=recbox>"
                  f"<div class=head>{n_urec} to fix, "
                  f"{at5} on components that scored 5</div><div class=body>",
                  "<p class=dim>None of these changes a score, a label or the "
                  "verdict. The review form has no answer option that describes "
                  "them, so the component passes and the work is still "
                  "outstanding. Treat this as the pre-submission list. Open a "
                  "row for the full text of its recommendations. "
                  "<b>An entry printed in bold is a hard gate elsewhere in the "
                  "project</b> — still unscored here, and the first thing to "
                  "fix.</p>",
                  "<table><tr><th>#</th><th>Component</th><th class=n>Score</th>"
                  "<th>What to fix</th></tr>"]
            for x, mi in sorted(urec, key=lambda y: y[0]["num"]):
                body = ("<ul class=reasons>" + "".join(
                    f"<li class=hg>{md(m)}</li>" if is_hard_gate(m)
                    else f"<li>{md(m)}</li>" for m in mi) + "</ul>")
                head = _teaser(mi[0], 120)
                if is_hard_gate(mi[0]):
                    head = f"<b>{head}</b>"
                if len(mi) > 1:
                    head = f"<b>{len(mi)} items.</b> {head}"
                h.append(f"<tr><td class=mono>{x['num']}</td>"
                         f"<td>{e(x['title'])}</td>"
                         f"<td class=n>{_score(x['score'])}</td>"
                         f"<td>{_fold(head, body)}</td></tr>")
            h += ["</table>", "</div></div>"]
        else:
            h.append("<p class=dim>None recorded. Every component either scored "
                     "its finding or had nothing to add beyond it.</p>")
        h.append("</div>")

    # ---- glossary
    defs_html = ""
    if audit_dir is not None:
        cdir = Path(__file__).resolve().parents[1] / "components"
        parts = []
        for f in sorted(cdir.glob("[0-9][0-9]-*.md")):
            parts.append(_det(f.stem.replace("-", " "), e(f.read_text(encoding="utf-8"))))
        for extra, label in ((cdir / "_sense_check.md", "senior review pass"),
                             (cdir / "_input_consistency.md",
                              "input file consistency pass")):
            if extra.exists():
                parts.append(_det(label, e(extra.read_text(encoding="utf-8"))))
        defs_html = "".join(parts)

    h += ["<section class=narrow>", "<p class=kicker>Glossary</p>",
          "<h2>Terms used above</h2>",
          "<table><tr><th>Term</th><th>Meaning</th></tr>",
          "<tr><td>Expected file</td><td>The answer key a contributor builds. The "
          "grading model compares an agent's output to it. The review form calls "
          "it the gold file.</td></tr>",
          "<tr><td>Criterion</td><td>One scored line in the contributor's rubric. "
          "A submission's rubric holds 10 to 30 of them, each with a weight.</td></tr>",
          "<tr><td>Format gate, correctness, visual</td><td>The three categories a "
          "criterion can carry. Weight is expected to sit in a set share per "
          "category.</td></tr>",
          "<tr><td>Must-pass</td><td>A criterion tag reserved for file existence "
          "and file extension.</td></tr>",
          "<tr><td>Verifier</td><td>The JSON that maps the expected files and the "
          "agent's output paths for grading.</td></tr>",
          "<tr><td>Unreachable value</td><td>A value in an expected file that "
          "cannot be produced from the inputs the agent receives. Any criterion "
          "graded against it cannot be satisfied.</td></tr>",
          "<tr><td>Escalation</td><td>A proposal from the senior review pass to "
          "lower a component score. Not applied to the verdict.</td></tr>",
          "<tr><td>Recommendation</td><td>A real defect that no component's "
          "answer options describe, so it cannot be scored. It never changes a "
          "score, a label or the verdict, and it appears even where the "
          "component scored 5.</td></tr>",
          "</table>", "</section>",
          "<section><p class=kicker>Appendix</p>",
          "<h2>The 28 component definitions</h2>",
          "<p class=dim>Each is generated from the audit rubric and is what the "
          "review for that component was given. Included so a score can be "
          "checked against the form it was scored on.</p>",
          (defs_html if audit_dir is not None else ""),
          "</section>",
          "<footer>Component definitions generated from the CUA v3 audit rubric. "
          "Scores as returned by the per-component review; the verdict is the "
          "lowest of the 28.</footer>",
          "</div>"]
    return "\n".join(h)
