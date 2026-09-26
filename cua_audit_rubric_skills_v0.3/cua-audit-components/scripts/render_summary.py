#!/usr/bin/env python3
"""Render component_review_summary.html from the summary pass's JSON.

The page carries the fix sections: what to do, in order. Its last section,
folded, lists word for word every recommendation those sections do not cite.
The scores, reasoning, senior review and evidence stay in
component_review.html, which the page links to and never repeats.

Layout, section order, numbering, counters, file badges and empty lines are
fixed here, so every summary has the same shape and the model writes only the
words.
"""
from __future__ import annotations

import re

from render_html import BAND, CSS, e, is_hard_gate, md

SUMMARY_CSS = r"""
.donow{border-left:3px solid var(--ink);padding:.15rem 0 .15rem 1.05rem;
  margin:1.4rem 0 0}
.donow h1{font-size:clamp(1.45rem,3vw,2.15rem);line-height:1.16;
  margin:.1rem 0 .5rem;letter-spacing:-.015em}
.donow h1 code{font-size:.92em}
.donow .blurb{margin:0}
.statebar{display:flex;gap:2.4rem;flex-wrap:wrap;margin:1.8rem 0 1.3rem;
  padding:.95rem 0;border-top:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.statebar div{min-width:96px}
.statebar b{display:block;color:var(--ink);font-size:1.55rem;line-height:1.12;
  font-variant-numeric:tabular-nums}
.statebar span{font-size:.71rem;text-transform:uppercase;letter-spacing:.09em;
  color:var(--muted);display:block;max-width:15ch}
.gate{font-size:.92rem;background:var(--panel);border:1px solid var(--line);
  padding:.75rem .85rem;margin:0 0 1rem}
.live{display:inline-block;font-weight:700;color:var(--ink)}
.legend{font-size:.78rem;color:var(--muted);margin:0;line-height:1.9}
.strikelegend{text-decoration:line-through}
.prog{display:flex;align-items:center;gap:.8rem;margin:0 0 1.5rem;max-width:var(--maxw)}
.progtrack{flex:1;height:7px;background:var(--panel);border:1px solid var(--line);
  border-radius:4px;overflow:hidden}
.progfill{display:block;height:100%;width:0;background:var(--ink);
  transition:width .18s ease}
.progtext{font-size:.76rem;color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
ul.steps{list-style:none;padding:0;margin:0}
li.step{display:flex;gap:.85rem;align-items:flex-start;
  border-top:1px solid var(--line);padding:1.15rem 0}
li.step>input{margin:.5rem 0 0;width:16px;height:16px;flex:none;
  accent-color:var(--ink);cursor:pointer}
li.step.done .stepbody{opacity:.42}
.stepbody{flex:1;min-width:0;max-width:var(--maxw)}
.stepact{font-size:1.02rem;color:var(--ink);font-weight:640;margin:0 0 .35rem;
  line-height:1.4}
.stepnum{display:inline-block;min-width:1.7rem;color:var(--muted);font-weight:700;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.84rem}
.stepact .pill{margin-left:.45rem;vertical-align:.1rem}
.where{font-size:.79rem;color:var(--muted);margin:0 0 .5rem 1.7rem}
.where code{font-size:.95em;color:var(--ink)}
.why{font-size:.92rem;margin:0 0 .7rem 1.7rem}
.check{font-size:.85rem;margin:.7rem 0 0 1.7rem;padding:.55rem .7rem;
  background:var(--pass-bg);border-left:3px solid var(--pass)}
.check b{color:var(--pass-fg)}
.stepnote{font-size:.82rem;color:var(--muted);margin:.7rem 0 0 1.7rem}
details.more{border:0;margin:1.2rem 0 0}
details.more>summary{background:var(--panel);border:1px solid var(--line);
  padding:.55rem .75rem}
details.more>.in{padding:0}
.fix{border:1px solid var(--line);margin:.55rem 0 .55rem 1.7rem;
  background:var(--paper)}
.fixh{font-size:.76rem;color:var(--muted);margin:0;padding:.42rem .6rem;
  background:var(--panel);border-bottom:1px solid var(--line);
  display:flex;flex-wrap:wrap;gap:.35rem;align-items:baseline}
.fixh code{font-size:.95em;color:var(--ink)}
.w{margin-left:auto;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.92em;white-space:nowrap}
.d{display:flex;gap:.6rem;padding:.5rem .6rem;font-size:.88rem;
  border-top:1px solid var(--line);align-items:flex-start}
.fixh+.d{border-top:0}
.dl{flex:none;width:3.6rem;font-size:.66rem;text-transform:uppercase;
  letter-spacing:.07em;font-weight:700;padding-top:.22rem;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.d .tx{flex:1;min-width:0;white-space:pre-wrap}
.d.was{background:#fbfbf9}
.d.was .dl{color:var(--muted)}
.d.del{background:var(--fail-bg)}
.d.del .dl{color:var(--fail-fg)}
.d.del .tx{text-decoration:line-through;color:var(--fail-fg)}
.d.to{background:var(--pass-bg)}
.d.to .dl{color:var(--pass-fg)}
.d.to .tx{color:var(--ink)}
.draft{display:inline-block;margin-left:.3rem;font-size:.58rem;font-weight:700;
  letter-spacing:.06em;padding:.08rem .28rem;border-radius:3px;
  background:var(--warn-bg);color:var(--warn);border:1px solid #e8d5ad;
  text-transform:uppercase;vertical-align:.05rem}
.fixnote{font-size:.79rem;color:var(--muted);margin:0;padding:.45rem .6rem;
  border-top:1px solid var(--line);background:#fbfbf9}
mark{background:#fdf3c2;color:var(--ink);padding:0 .1em}
.fc{display:inline-block;font-size:.6rem;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;padding:.08rem .3rem;border-radius:3px;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  vertical-align:.05rem}
.fc-gtf{background:var(--fail-bg);color:var(--fail-fg);border:1px solid #f2c3bb}
.fc-input{background:#e7eff8;color:#1f4e79;border:1px solid #c3d6ea}
.fc-plain{background:var(--pend-bg);color:var(--pend);border:1px solid #dcdcd7}
ul.opts{list-style:none;padding:0;margin:0 0 1rem}
ul.opts li{border-top:1px solid var(--line);padding:.7rem 0 .7rem 1.1rem;
  position:relative;font-size:.92rem}
ul.opts li:before{content:"";position:absolute;left:0;top:1.15rem;width:6px;
  height:6px;background:var(--faint);border-radius:50%}
ul.opts li:first-child:before{background:var(--ink)}
ul.opts li b{color:var(--ink)}
ul.also{list-style:none;padding:0;margin:0}
ul.also li{border-top:1px solid var(--line);padding:.62rem 0 .62rem 1.1rem;
  position:relative;font-size:.9rem}
ul.also li:before{content:"";position:absolute;left:0;top:1.05rem;width:6px;
  height:6px;background:var(--faint);border-radius:50%}
.startnow{border:2px solid var(--ink);padding:1.2rem 1.3rem;margin:.6rem 0 0;
  max-width:var(--maxw)}
.startnow h2{margin:0 0 .5rem;font-size:1.28rem}
.startnow p{margin:0;font-size:.95rem}
.startnow code{background:var(--panel);padding:.05rem .25rem;border-radius:3px}
.unmatched{font-size:.82rem;background:var(--warn-bg);color:var(--warn);
  border:1px solid #e8d5ad;padding:.6rem .8rem;margin:1rem 0 0}
.unmatched ul{margin:.3rem 0 0;padding-left:1.1rem}
.fixnote.unmatched,.stepnote.unmatched{border:0;border-top:1px solid #e8d5ad;margin:0}
.stepnote.unmatched{margin:.7rem 0 0 1.7rem;border:1px solid #e8d5ad}
.recs h3{font-size:.92rem;margin:1.4rem 0 .2rem}
.recs h3 .dim{font-weight:400}
@media print{li.step,.fix{break-inside:avoid}}
"""

SCRIPT = """
(function(){
  var boxes = [].slice.call(document.querySelectorAll('ul.steps li.step > input[type=checkbox]'));
  var fill = document.getElementById('progfill'), text = document.getElementById('progtext'),
      gate = document.getElementById('gatestate');
  var total = boxes.length, gateTotal = 0;
  boxes.forEach(function(b){ if (b.parentNode.hasAttribute('data-gate')) gateTotal++; });
  function sync(){
    var done = 0, gateDone = 0;
    boxes.forEach(function(b){
      var li = b.parentNode;
      if (b.checked){ done++; if (li.hasAttribute('data-gate')) gateDone++; li.classList.add('done'); }
      else { li.classList.remove('done'); }
    });
    if (fill) fill.style.width = total ? (done / total * 100) + '%' : '0%';
    if (text) text.textContent = done + ' of ' + total + ' done';
    if (gate && gateTotal)
      gate.textContent = (gateTotal - gateDone) + ' of ' + gateTotal + ' verdict-clearing fixes left.';
  }
  boxes.forEach(function(b){ b.addEventListener('change', sync); });
  sync();
})();
"""

FILE_CLASS = {"gtf": ("fc-gtf", "GTF"), "input": ("fc-input", "input"),
              "prompt": ("fc-plain", "prompt"), "rubric": ("fc-plain", "rubric"),
              "bundle": ("fc-plain", "bundle")}
PILL = {"clears the fail": "p2", "major": "p2", "pre-empts an escalation": "p3"}
VISIBLE_STEPS = 5

LEGEND = ("Key: <span class=draft>draft</span> replacement composed here rather "
          "than quoted from the review &mdash; verify the wording before committing. "
          "<span class=strikelegend>Struck through</span> text is deleted. "
          "<mark>Highlighted</mark> text is the part that changes. File class: "
          "<span class='fc fc-gtf'>GTF</span> answer key, editing it changes what "
          "every submission is graded against &middot; "
          "<span class='fc fc-input'>input</span> a file the agent receives, editing "
          "it changes what is solvable &middot; <span class='fc fc-plain'>rubric</span> "
          "<span class='fc fc-plain'>bundle</span> <span class='fc fc-plain'>prompt</span> "
          "the task's own artifacts.")


def num(c) -> str:
    """A component reference as its two-digit number: 7, "7", "C07" -> "07"."""
    m = re.search(r"\d+", str(c or ""))
    return m.group().zfill(2) if m else str(c or "")


def title(t: str) -> str:
    """A component's heading without the "Component: " some of them open with."""
    return re.sub(r"^Component:\s*", "", t or "")


def strings(x) -> list[str]:
    """Every string in a JSON value, at any depth."""
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [s for v in x.values() for s in strings(v)]
    if isinstance(x, list):
        return [s for v in x for s in strings(v)]
    return []


def _plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def and_list(parts: list[str]) -> str:
    if len(parts) < 2:
        return "".join(parts)
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def _mark(text: str, part: str) -> str:
    """The text escaped, with the first occurrence of `part` highlighted."""
    i = text.find(part) if part else -1
    if i < 0:
        return e(text)
    return (e(text[:i]) + "<mark>" + e(part) + "</mark>"
            + e(text[i + len(part):]))


def _files(entries: list[dict], files: dict[str, str]) -> str:
    """Each file once, with its badge. The class the task's own file list gives
    wins over the one the summary states."""
    out = []
    for name in dict.fromkeys(f.get("name") or "" for f in entries):
        stated = next((f.get("class") for f in entries if f.get("name") == name), "")
        cls, label = FILE_CLASS.get(files.get(name) or stated or "", ("fc-plain", "unlisted"))
        out.append(f"<code>{e(name)}</code> <span class='fc {cls}'>{label}</span>")
    return and_list(out)


def _components(nums: list[str], titles: dict[str, str]) -> str:
    nums = [num(c) for c in nums if num(c)]
    if not nums:
        return ""
    word = "component" if len(nums) == 1 else "components"
    return word + " " + and_list([f"<code>{e(c)}</code> {e(titles.get(c, ''))}".rstrip()
                                  for c in nums])


def _sources(ids: list[str], labels: dict[str, str]) -> str:
    out = [e(labels[i]) if i in labels
           else f"<code>{e(i)}</code> (not in the audit data)" for i in ids]
    return ("Source: " + "; ".join(out) + ".") if out else ""


def _flags(flags: list[str], cls: str, head: str = "Not matched to the audit data.") -> str:
    if not flags:
        return ""
    return (f"<p class='{cls} unmatched'><b>{head}</b> "
            + " ".join(md(f) for f in flags) + "</p>")


def _fix(fx: dict, files: dict[str, str]) -> str:
    head = [x for x in (_files(fx.get("files") or [], files), md(fx.get("location")))
            if x]
    weight = (f"<span class=w>{e(fx['weight'])}</span>"
              if (fx.get("weight") or "").strip() else "")
    h = ["<div class=fix>", f"<p class=fixh>{' &middot; '.join(head)}{weight}</p>"]
    now, note = fx.get("now") or "", (fx.get("now_note") or "").strip()
    if now:
        tail = f" <span class=dim>({md(note)})</span>" if note else ""
        h.append(f"<div class='d was'><span class=dl>now</span><span class=tx>"
                 f"{_mark(now, fx.get('highlight') or '')}{tail}</span></div>")
    else:
        h.append(f"<div class='d was'><span class=dl>now</span><span class=tx>"
                 f"{md(note) or 'Nothing at this location yet.'}</span></div>")
    if fx.get("delete"):
        h.append(f"<div class='d del'><span class=dl>delete</span><span class=tx>"
                 f"{e(fx['delete'])}</span></div>")
    if fx.get("to"):
        draft = "<span class=draft>draft</span>" if fx.get("draft") else ""
        h.append(f"<div class='d to'><span class=dl>to{draft}</span><span class=tx>"
                 f"{_mark(fx['to'], fx.get('to_highlight') or '')}</span></div>")
    if (fx.get("note") or "").strip():
        h.append(f"<p class=fixnote>{md(fx['note'])}</p>")
    h.append(_flags(fx.get("_flags") or [], "fixnote"))
    h.append(_flags(fx.get("_rules") or [], "fixnote", "Breaks a rubric rule."))
    h.append("</div>")
    return "\n".join(x for x in h if x)


def _step(n: int, st: dict, files: dict[str, str], titles: dict[str, str],
          labels: dict[str, str]) -> str:
    pill = st.get("pill") or ""
    pill = f' <span class="pill {PILL[pill]}">{e(pill)}</span>' if pill in PILL else ""
    entries = [f for fx in st.get("fixes") or [] for f in fx.get("files") or []]
    where = [x for x in (_files(entries, files), md(st.get("scope")),
                         _components(st.get("components") or [], titles)) if x]
    gate = " data-gate" if st.get("clears_verdict") else ""
    h = [f"<li class=step id=step{n}{gate}>",
         f"<input type=checkbox aria-label='mark fix {n} done'>",
         "<div class=stepbody>",
         f"<p class=stepact><span class=stepnum>{n}</span>{md(st.get('action'))}{pill}</p>"]
    if where:
        h.append(f"<p class=where>{' &middot; '.join(where)}</p>")
    if (st.get("why") or "").strip():
        h.append(f"<p class=why>{md(st['why'])}</p>")
    h += [_fix(fx, files) for fx in st.get("fixes") or []]
    if (st.get("answer_key_check") or "").strip():
        h.append(f"<p class=check><b>Answer-key check.</b> {md(st['answer_key_check'])}</p>")
    note = " ".join(x for x in (md(st.get("note")),
                                _sources(st.get("sources") or [], labels)) if x)
    if note:
        h.append(f"<p class=stepnote>{note}</p>")
    h.append(_flags(st.get("_flags") or [], "stepnote"))
    h += ["</div>", "</li>"]
    return "\n".join(x for x in h if x)


def _statebar(r: dict, steps: list[dict]) -> str:
    v = r.get("verdict")
    band = ("incomplete" if v is None else "fail" if v <= 2 else BAND[v][1])
    below = sum(1 for x in r["rows"] if isinstance(x.get("score"), int) and x["score"] < 5)
    clears = sum(1 for s in steps if s.get("pill") == "clears the fail")
    cells = [("&ndash;" if v is None else str(v), f"verdict &middot; {band}"),
             (str(len(steps)), "fix queued" if len(steps) == 1 else "fixes queued"),
             (str(clears), "fix clears a fail" if clears == 1 else "fixes clear a fail"),
             (str(below), "component below 5" if below == 1 else "components below 5")]
    ic = r.get("inputs") or {}
    if ic:
        major = sum(1 for f in ic.get("findings") or [] if f.get("severity") == "major")
        cells.append((str(major),
                      "major inconsistency" if major == 1 else "major inconsistencies"))
    else:
        cells.append(("&ndash;", "consistency check not run"))
    return ("<div class=statebar>\n"
            + "\n".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in cells)
            + "\n</div>")


RID = re.compile(r"\bR(\d+)\.(\d+)\b")


def _recommendations(r: dict, out: dict, titles: dict[str, str]) -> list[str]:
    """Every recommendation the answer does not cite, in a source list or in its
    text, word for word and grouped by component."""
    cited = {f"R{num(c)}.{int(k)}" for s in strings(out) for c, k in RID.findall(s)}
    groups, total = [], 0
    for x in sorted(r["rows"], key=lambda y: y["num"]):
        recs = x.get("minor_issues") or []
        total += len(recs)
        left = [m for k, m in enumerate(recs, 1) if f"R{x['num']}.{k}" not in cited]
        if left:
            groups.append((x, left))
    n = sum(len(left) for _, left in groups)
    h = ["<section class=narrow>", "<p class=kicker>Minor improvements</p>"]
    if not n:
        h.append("<h2>Every recommendation is cited in the sections above.</h2>" if total
                 else "<h2>No component made a recommendation.</h2>")
        return h + ["</section>", ""]
    hard = sum(1 for _, left in groups for m in left if is_hard_gate(m))
    intro = ("None changes a score. Each is quoted as its component wrote it, grouped "
             "by component, so two components can make the same point.")
    if total > n:
        intro += f" {_plural(total - n, 'other is', 'others are')} cited in the sections above."
    if hard:
        intro += (" <b>An entry in bold is a hard gate elsewhere in the project</b>: "
                  "unscored here, and the first of these to fix.")
    shown = _plural(n, "recommendation", "recommendations")
    h += [f"<h2>{shown} not cited above</h2>", f"<p class=dim>{intro}</p>",
          f"<details class=more><summary>Show the {shown}"
          f"{f', {hard} in bold' if hard else ''}</summary>",
          "<div class='in recs'>"]
    for x, left in groups:
        s = x.get("score")
        score = f" <span class=dim>&middot; scored {s}</span>" if isinstance(s, int) else ""
        h += [f"<h3><code>{e(x['num'])}</code> {e(titles.get(x['num'], ''))}{score}</h3>",
              "<ul class=reasons>",
              *[f"<li class=hg>{md(m)}</li>" if is_hard_gate(m) else f"<li>{md(m)}</li>"
                for m in left],
              "</ul>"]
    return h + ["</div>", "</details>", "</section>", ""]


def render(r: dict, files: dict[str, str], labels: dict[str, str], out: dict,
           problems: list[str]) -> str:
    """r: rollup.collect() for the unit. files: file name -> class. labels:
    source id -> what it names. out: the model's JSON, with any `_flags` the
    checks attached. problems: every check that failed, for the banner."""
    titles = {x["num"]: title(x["title"]) for x in r["rows"]}
    steps = out.get("steps") or []
    gates = sum(1 for s in steps if s.get("clears_verdict"))
    live = (f"{gates} of {gates} verdict-clearing fixes left." if gates
            else "No fix here moves the verdict.")
    h = ["<!doctype html><meta charset=utf-8>",
         "<meta name=viewport content='width=device-width,initial-scale=1'>",
         f"<title>CUA audit fixes &middot; {e(r['unit'])}</title>",
         f"<style>{CSS}{SUMMARY_CSS}</style>",
         "<div class=wrap>", ""]

    # ---- head
    h += ["<section>",
          f"<p class=brand>Scale GenAI Ops / CUA v3 &middot; {e(r['unit'])}"
          f" &middot; {e(r.get('domain') or 'domain unknown')}</p>",
          f"<div class=donow><h1>{md(out.get('next_action'))}</h1>",
          f"<p class=blurb>{md(out.get('next_action_why'))}</p></div>",
          _statebar(r, steps),
          f"<p class=gate>{md(out.get('gate'))} <span class=live id=gatestate>{live}</span></p>",
          f"<p class=legend>{LEGEND}</p>",
          "<p class=legend>Every score, recommendation and piece of evidence behind "
          "these fixes is in <a href='component_review.html'>"
          "<code>component_review.html</code></a>, beside this file.</p>"]
    if problems:
        h.append("<div class=unmatched><b>"
                 + _plural(len(problems), "check", "checks")
                 + " failed.</b> The items are marked where they appear; confirm "
                 "them before editing.<ul>"
                 + "".join(f"<li>{md(p)}</li>" for p in problems) + "</ul></div>")
    h += ["</section>", ""]

    # ---- the fixes
    n = len(steps)
    h += ["<section>", "<p class=kicker>Do these in order</p>"]
    if n:
        rows = [_step(i, st, files, titles, labels) for i, st in enumerate(steps, 1)]
        h += [f"<h2>{_plural(n, 'fix', 'fixes')}</h2>",
              "<div class=prog><div class=progtrack><span class=progfill id=progfill>"
              "</span></div>",
              f"<span class=progtext id=progtext>0 of {n} done</span></div>",
              "<ul class=steps>", *rows[:VISIBLE_STEPS], "</ul>"]
        if n > VISIBLE_STEPS:
            h += ["<details class=more><summary>Show the remaining "
                  f"{_plural(n - VISIBLE_STEPS, 'fix', 'fixes')}</summary>",
                  "<div class=in>", "<ul class=steps>", *rows[VISIBLE_STEPS:],
                  "</ul>", "</div>", "</details>"]
    else:
        h.append("<h2>Nothing to fix</h2>")
    cov = (out.get("consistency_coverage") or "").strip()
    if cov:
        h.append(f"<p class=dim>Consistency-check coverage: {md(cov)}</p>")
    elif not r.get("inputs"):
        h.append("<p class=dim>Consistency-check coverage: the input-file consistency "
                 "check did not run, so its findings are missing from this list.</p>")
    h += ["</section>", ""]

    # ---- wrong facts in the component reports
    wrong = out.get("wrong_facts") or []
    scores = {x["num"]: x.get("score") for x in r["rows"]}
    h += ["<section class=narrow>", "<p class=kicker>Before acting on the component reports</p>"]
    if wrong:
        verb = "states" if len(wrong) == 1 else "state"
        h += [f"<h2>{len(wrong)} of them {verb} a wrong fact</h2>",
              "<p class=dim>Read these before you trust the report they sit in.</p>"]
        for w in wrong:
            c = num(w.get("component"))
            s = scores.get(c)
            head = f"component <code>{e(c)}</code> {e(titles.get(c, ''))}"
            if isinstance(s, int):
                head += f" &middot; scored {s}"
            src = _sources(w.get("sources") or [], labels)
            h += ["<div class=fix>", f"<p class=fixh>{head}</p>",
                  f"<div class='d was'><span class=dl>says</span><span class=tx>"
                  f"{md(w.get('says'))}</span></div>",
                  f"<div class='d to'><span class=dl>fact</span><span class=tx>"
                  f"{md(w.get('fact'))}</span></div>"]
            if src:
                h.append(f"<p class=fixnote>{src}</p>")
            h.append("</div>")
    else:
        h.append("<h2>No component report states a wrong fact.</h2>")
    h += ["</section>", ""]

    # ---- the single open decision
    call = out.get("one_call") or {}
    h += ["<section class=narrow>", "<p class=kicker>One call to make</p>"]
    if (call.get("question") or "").strip():
        h.append(f"<h2>{md(call['question'])}</h2>")
        if (call.get("context") or "").strip():
            h.append(f"<p>{md(call['context'])}</p>")
        opts = call.get("options") or []
        if opts:
            h.append("<ul class=opts>")
            for i, o in enumerate(opts):
                h.append(f"<li><b>Option {chr(65 + i)} &mdash; {md(o.get('label'))}</b> "
                         f"{md(o.get('detail'))}</li>")
            h.append("</ul>")
        if (call.get("pick") or "").strip():
            h.append(f"<p>{md(call['pick'])}</p>")
    else:
        h.append("<h2>No open call: every fix above is unambiguous.</h2>")
    h += ["</section>", ""]

    # ---- what could not be settled
    still = out.get("still_open") or []
    covered = list(dict.fromkeys(num(c) for s in still for c in s.get("components") or []))
    h += ["<section class=narrow>", "<p class=kicker>Still open</p>"]
    if still:
        verb = "could not be settled"
        h += [f"<h2>{_plural(len(covered), 'component', 'components')} {verb}</h2>"
              if covered else f"<h2>{_plural(len(still), 'item', 'items')} {verb}</h2>",
              "<ul class=also>"]
        for s in still:
            cs = [num(c) for c in s.get("components") or []]
            who = (f"<code>{e(cs[0])}</code> {e(titles.get(cs[0], ''))}" if len(cs) == 1
                   else ", ".join(f"<code>{e(c)}</code>" for c in cs))
            h.append(f"<li>{who + ' &mdash; ' if who else ''}{md(s.get('line'))}</li>")
        h.append("</ul>")
    else:
        h.append("<h2>Every component was settled from the available evidence.</h2>")
    h += ["</section>", ""]

    # ---- tangents
    also = [a for a in out.get("also_found") or [] if (a or "").strip()]
    h += ["<section class=narrow>", "<p class=kicker>Also found</p>"]
    if also:
        h += [f"<h2>{_plural(len(also), 'thing', 'things')} outside the fix list</h2>",
              "<ul class=also>", *[f"<li>{md(a)}</li>" for a in also], "</ul>"]
    else:
        h.append("<h2>Nothing outside the fix list.</h2>")
    h += ["</section>", ""]

    # ---- the first move
    start = out.get("start_here") or {}
    h += ["<section class=narrow>", "<p class=kicker>Start here</p>",
          f"<div class=startnow><h2>{md(start.get('action'))}</h2>",
          f"<p>{md(start.get('detail'))}</p></div>", "</section>", ""]

    # ---- the recommendations no section above cites
    h += _recommendations(r, out, titles)
    h += [f"<script>{SCRIPT}</script>", "</div>", ""]
    return "\n".join(h)
