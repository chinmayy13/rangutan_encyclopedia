#!/usr/bin/env python3
"""Output-hygiene pass: turn a unit's results into the ordered list of fixes.

One tool-free opus call per unit. The prompt carries the results themselves:
the task's prompt and criteria, every component that scored below 5, every
recommendation, every group of value criteria that component 27 found one input
answers in full, the senior review and the input-consistency result, each item
with an id. The model answers in JSON through --json-schema. Python checks
every cited id, file and quoted current text against the audit's own files,
then renders `component_review_summary.html` from a fixed template
(render_summary.py): the fix sections, then every recommendation they do not
cite, as its component wrote it. `component_review.html` keeps the full
reasoning, and the summary links to it.

Runs after the sense check and the input-consistency pass. It reads their JSON,
not `component_review.html`. Its output marks the unit's first audit finished.

    python3 summarize.py <unit_id> [...]
    python3 summarize.py                    # every unit with all 28 results
    python3 summarize.py <unit_id> --redo
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402
import render_summary  # noqa: E402
import rollup  # noqa: E402
from render_summary import and_list, num, strings, title  # noqa: E402
from run_review import AUDIT, SKILL, components  # noqa: E402

PROMPT = SKILL / "components" / "_output_hygiene.md"
MODEL = "claude-opus-5"
EFFORT = "high"  # at max, a large unit reasons past the output limit before answering
TIMEOUT = 1800

OUT = ac.SUMMARY
SIDE = "component_review_summary.json"

S = {"type": "string"}
IDS = {"type": "array", "items": S}


def _obj(props: dict) -> dict:
    return {"type": "object", "additionalProperties": False,
            "required": list(props), "properties": props}


def _list(item: dict) -> dict:
    return {"type": "array", "items": item}


SCHEMA = _obj({
    "next_action": S,
    "next_action_why": S,
    "gate": S,
    "steps": _list(_obj({
        "action": S,
        "pill": {"type": "string", "enum": ["", *render_summary.PILL]},
        "clears_verdict": {"type": "boolean"},
        "components": IDS,
        "scope": S,
        "why": S,
        "fixes": _list(_obj({
            "files": _list(_obj({
                "name": S,
                "class": {"type": "string", "enum": list(render_summary.FILE_CLASS)}})),
            "location": S,
            "weight": S,
            "now": S,
            "now_note": S,
            "highlight": S,
            "delete": S,
            "to": S,
            "to_highlight": S,
            "draft": {"type": "boolean"},
            "note": S})),
        "answer_key_check": S,
        "note": S,
        "sources": IDS})),
    "consistency_coverage": S,
    "wrong_facts": _list(_obj({"component": S, "says": S, "fact": S, "sources": IDS})),
    "one_call": _obj({"question": S, "context": S,
                      "options": _list(_obj({"label": S, "detail": S})),
                      "pick": S}),
    "still_open": _list(_obj({"components": IDS, "line": S})),
    "also_found": _list(S),
    "start_here": _obj({"action": S, "detail": S}),
})


def files_of(b: dict) -> dict[str, str]:
    """Every file a fix can edit, by name, with its class. An expected file
    that shares a name with an input file is labelled GTF."""
    out = {"bundle.json": "bundle", "rubric.json": "rubric", "prompt.md": "prompt"}
    for f in b.get("input_files") or []:
        out[Path(f.get("path") or f.get("dest") or "").name] = "input"
    for f in b.get("expected_files") or []:
        out[Path(f.get("dest") or f.get("path") or "").name] = "gtf"
    out.pop("", None)
    return out


def build(unit: str) -> tuple[dict, dict, dict, dict]:
    """The audit data the model reads, the class of every file, what every
    source id names, and rollup's view of the unit, which the counters use."""
    d = AUDIT / unit
    r = rollup.collect(unit, components(), rollup.justification_map())
    b = json.loads((d / "bundle.json").read_text(encoding="utf-8"))
    files, labels = files_of(b), {}

    def tag(items, prefix, label):
        out = []
        for i, it in enumerate(items or [], 1):
            labels[f"{prefix}{i}"] = label(it, i)
            out.append({"id": f"{prefix}{i}", **it})
        return out

    sc, ic = r["sense"] or {}, r["inputs"] or {}
    senior: dict | str = "not run"
    if sc:
        senior = {k: sc.get(k) for k in
                  ("mechanical_verdict", "verdict_driver", "fragility", "summary")}
        senior["fix_order"] = tag(
            sorted(sc.get("fix_order") or [], key=lambda x: x.get("rank") or 0), "S",
            lambda it, i: f"senior review fix order, rank {it.get('rank', i)}")
        senior["escalations"] = tag(
            sc.get("escalations"), "E",
            lambda it, i: f"senior review escalation of component {num(it.get('component'))}")
        senior["contradictions"] = tag(
            sc.get("contradictions"), "X",
            lambda it, i: "senior review contradiction between components "
            + and_list([num(c) for c in it.get("components") or []]))
        senior["unverified"] = tag(
            sc.get("unverified"), "U",
            lambda it, i: f"senior review, component {num(it.get('component'))} unverified")
    consistency: dict | str = "not run"
    if ic:
        consistency = {k: ic.get(k) for k in
                       ("verdict", "summary", "rules_compared", "files_checked", "blocked_on")}
        consistency["findings"] = tag(
            ic.get("findings"), "I",
            lambda it, i: f"input-consistency finding {i} ({it.get('severity')})")

    # A component that scored 5 contributes its recommendations only, unless the
    # senior review or the consistency check names it. A group of value criteria
    # that one input answers in full is Value Binding's fail case, so it comes
    # along whatever component 27 scored.
    named = {num(c) for x in sc.get("contradictions") or [] for c in x.get("components") or []}
    named |= {num(x.get("component")) for k in ("escalations", "unverified", "fix_order")
              for x in sc.get(k) or []}
    named |= {num(c) for c in sc.get("verdict_driver") or []}
    named |= {num(f["component"]) for f in ic.get("findings") or [] if f.get("component")}
    comps = []
    for row in r["rows"]:
        c, recs = row["num"], row.get("minor_issues") or []
        labels[f"C{c}"] = f"component {c} {title(row['title'])}"
        entry = {"id": f"C{c}", "component": c, "title": title(row["title"]),
                 "score": row["score"]}
        if row["score"] is None:
            entry["result"] = "not run"
        elif row["score"] < 5 or c in named:
            entry.update({k: row.get(k) for k in ("error_category", "confidence",
                                                  "blocked_on", "justification", "evidence")})
        held = [g for g in row.get("whole_answer_inputs") or [] if g.get("input")]
        if held:
            entry["whole_answer_inputs"] = held
        if recs:
            entry["recommendations"] = []
            for k, text in enumerate(recs, 1):
                labels[f"R{c}.{k}"] = f"component {c} recommendation {k}"
                entry["recommendations"].append({"id": f"R{c}.{k}", "text": text})
        comps.append(entry)

    data = {"unit": unit, "domain": b.get("domain"), "sub_domain": b.get("sub_domain"),
            "verdict": r["verdict"], "band": r["band"], "components_run": r["n_run"],
            "files": [{"name": n, "class": c} for n, c in files.items()],
            "prompt": b.get("prompt"),
            "criteria": [{k: c.get(k) for k in ("n", "title", "weight", "category", "type")}
                         for c in b.get("criteria") or []],
            "components": comps,
            "senior_review": senior,
            "input_consistency": consistency}
    return data, files, labels, r


QUOTES = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
                        "\u00a0": " "})


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").translate(QUOTES)).strip()


QUOTED = re.compile(r'"([^"]+)"')


def artifacts(d: Path) -> str:
    """The text a quoted current text must be found in: the task's own text, and
    every quote the results took from the files. The extracted files stop at 200
    rows per sheet and 20,000 characters per file, and carry no hyperlink
    targets; the passes that open the files quote past all three."""
    parts = []
    for name in ("bundle.json", "rubric.json"):
        try:
            parts += strings(json.loads((d / name).read_text(encoding="utf-8")))
        except (OSError, ValueError):
            pass
    for name in ("prompt.md", "inputs_extracted.md", "expected_extracted.md"):
        if (d / name).is_file():
            parts.append((d / name).read_text(encoding="utf-8", errors="replace"))
    for p in [*sorted((d / "components").glob("[0-9][0-9].json")),
              d / "input_consistency.json", d / "sense_check.json"]:
        try:
            said = strings(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
        parts += [q for s in said for q in QUOTED.findall(norm(s))]
    return "\n".join(norm(s) for s in parts)


def canon(i: str) -> str:
    """A source id as build() spells it: "c7" -> "C07", "R7.2" -> "R07.2"."""
    i = (i or "").strip().upper()
    m = re.fullmatch(r"([CR])(\d+)(\.\d+)?", i)
    return f"{m[1]}{m[2].zfill(2)}{m[3] or ''}" if m else i


# "IF" stays out: in a criterion it is a spreadsheet function, not a condition.
COND = re.compile(
    r"\b(?:[Ii]f|(?i:unless|otherwise|whenever|provided that|in case|in the event"
    r"|depending on|as long as|only (?:when|where)|(?:where|when|as) (?:applicable|relevant|present)"
    r"|(?:passes|fails|is met|counts|applies) (?:only )?(?:when|where)"
    r"|any \w+(?: \w+)? it (?:reports|shows|includes|contains|gives|states)))\b")
MONTH = (r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?"
         r"|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)")
DATE = re.compile(rf"\b{MONTH}\.? \d{{1,2}}(?:, \d{{4}})?\b|\b\d{{4}}-\d{{2}}-\d{{2}}\b")
TOLERANCE = re.compile(r"(?i)(?:±|\+/-|\bwithin\b|\btolerance of\b)\s*±?\s*[$€£]?\d[\d,.]*\s*"
                       r"(?:%|pp\b|percentage points?\b|bps\b|basis points?\b)?")
TOKEN = re.compile(r"(?<![\w.$€£])[$€£]?\d[\w.,%-]*")
VALUE = re.compile(r"[$€£]?\d[\d,]*(?:\.\d+)?(?:%|x|bps|pp|mt|[KMB])?")
PLACE = re.compile(r"(?i)(?:§|\b(?:slides?|pages?|p\.|sections?|sheets?|rows?|columns?|cols?"
                   r"|tables?|figures?|fig\.|steps?|criteri(?:on|a)|items?|paragraphs?|lines?"
                   r"|cells?|tabs?|appendix|notes?|footnotes?|parts?|chapters?|exhibits?"
                   r"|schedules?|questions?))\s*(?:\d+\s*[–-]\s*)?$")
SETTING = re.compile(r"(?i)\s*(?:decimal|dp\b|significant|sig\.? ?figs?|digits?|zoom\b|pt\b"
                     r"|px\b|dpi\b|point (?:font|type)\b)")
NUMBER_WORDS = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def _values(text: str):
    """(value, digits, start, end) for every number the text states as a value,
    unit kept; a name such as 10-K or 5-mile is not one."""
    for m in TOKEN.finditer(text):
        tok = m.group().rstrip(".,-")
        if VALUE.fullmatch(tok):
            yield tok, re.sub(r"[^\d.]", "", tok).strip("."), m.start(), m.start() + len(tok)


def _date(d: str) -> str:
    return re.sub(r"[.,]", "", d).lower()


def given(text: str) -> set[str]:
    """Every date and number the text states, in the form stated() compares."""
    t = norm(text)
    keys = {_date(m.group()) for m in DATE.finditer(t)} | {v[1] for v in _values(t)}
    return keys | {NUMBER_WORDS[w] for w in re.findall(r"[a-z]+", t.lower())
                   if w in NUMBER_WORDS}


def stated(to: str, known: set[str]) -> list[str]:
    """The dates and numbers `to` states that `known` lacks. A tolerance, a place
    (slide 4, row 12), a precision or display setting (2 decimal places, 100%
    zoom), 0 and 1 are not answers."""
    t = TOLERANCE.sub(" ", re.sub(r"`[^`]*`", " ", norm(to)))
    out = [m.group() for m in DATE.finditer(t) if _date(m.group()) not in known]
    t = DATE.sub(" ", t)
    out += [v for v, core, a, b in _values(t)
            if core not in ("0", "1") and core not in known
            and not PLACE.search(t[:a]) and not SETTING.match(t[b:])]
    return list(dict.fromkeys(out))


def check(out: dict, files: dict[str, str], labels: dict[str, str], corpus: str,
          r: dict, prompt: str) -> list[str]:
    """Every failed check, one line each. Each fix or step a check concerns gets
    the message in `_flags` too, or in `_rules` when a criterion it writes breaks
    a rubric rule, so the page marks it in place."""
    problems: list[str] = []
    known = {x["num"] for x in r["rows"]}
    in_prompt = given(prompt)

    def ids(where: str, xs: list[str]) -> None:
        bad = [i for i in xs if i not in labels]
        if bad:
            problems.append(f"{where} cites {', '.join(bad)}, which the audit data "
                            f"does not contain.")

    def comps(where: str, xs: list) -> None:
        bad = [str(c) for c in xs if num(c) not in known]
        if bad:
            problems.append(f"{where} names component {', '.join(bad)}, which does "
                            f"not exist.")

    steps = out.get("steps") or []
    for n, st in enumerate(steps, 1):
        where = f"Fix {n}"
        st["sources"] = [canon(i) for i in st.get("sources") or []]
        ids(where, st["sources"])
        comps(where, st.get("components") or [])
        flags, gtf = [], False
        if not st["sources"]:
            flags.append("It cites no source.")
        for fx in st.get("fixes") or []:
            fl = []
            for f in fx.get("files") or []:
                name, cls = f.get("name") or "", files.get(f.get("name") or "")
                if cls is None:
                    fl.append(f"`{name}` is not one of the task's files.")
                elif cls != f.get("class"):
                    fl.append(f"`{name}` is classed {cls} in the task's files, "
                              f"not {f.get('class')}.")
                gtf |= (cls or f.get("class")) == "gtf"
            now, to = fx.get("now") or "", fx.get("to") or ""
            if now and norm(now) not in corpus:
                fl.append("The current text was not found word for word in the "
                          "task's files, nor in a quote the results took from them.")
            for key, whole, what in (("highlight", now, "highlighted"),
                                     ("delete", now, "deleted"),
                                     ("to_highlight", to, "highlighted replacement")):
                part = fx.get(key) or ""
                if part and part not in whole:
                    fl.append(f"The {what} text is not part of the text it marks.")
            if fl:
                fx["_flags"] = fl
                problems += [f"{where}: {m}" for m in fl]
            if to and (fx.get("weight") or "").strip():
                rules = []
                cond = list(dict.fromkeys(
                    m.group() for m in COND.finditer(re.sub(r"`[^`]*`", " ", to))))
                if cond:
                    rules.append("The criterion is conditional ("
                                 + ", ".join(f'"{c}"' for c in cond) + "): state the one "
                                 "requirement that always applies, graded against the "
                                 "expected file.")
                vals = stated(to, in_prompt | given(now))
                if vals:
                    rules.append(f"The criterion states {and_list(vals)}, which the prompt "
                                 f"does not give. If {'that is' if len(vals) == 1 else 'those are'}"
                                 " what the agent must produce, compare to the expected file "
                                 "instead (component 13).")
                if rules:
                    fx["_rules"] = rules
                    problems += [f"{where}: {m}" for m in rules]
        if gtf and not (st.get("answer_key_check") or "").strip():
            flags.append("It edits a GTF file but carries no answer-key check.")
        if flags:
            st["_flags"] = flags
            problems += [f"{where}: {m}" for m in flags]

    for n, w in enumerate(out.get("wrong_facts") or [], 1):
        w["sources"] = [canon(i) for i in w.get("sources") or []]
        ids(f"Wrong fact {n}", w["sources"])
        comps(f"Wrong fact {n}", [w.get("component")])
    for n, s in enumerate(out.get("still_open") or [], 1):
        comps(f"Still-open item {n}", s.get("components") or [])

    cited = {i for st in steps for i in st["sources"]}
    left = [i for i in labels if i.startswith("I") and i not in cited]
    if left:
        many = len(left) > 1
        problems.append(f"Input-consistency finding{'s' if many else ''} "
                        f"{', '.join(left)} {'are' if many else 'is'} carried by no fix.")
    if not steps and (r["n_minor"] or (r["inputs"] or {}).get("findings")
                      or any(isinstance(x.get("score"), int) and x["score"] < 5
                             for x in r["rows"])):
        problems.append("The fix list is empty, but the results hold things to fix.")
    call = out.get("one_call") or {}
    n_opts = len(call.get("options") or [])
    if (call.get("question") or "").strip() and not 2 <= n_opts <= 4:
        problems.append(f"The open call has {n_opts} options; it needs 2 to 4.")
    if len(out.get("also_found") or []) > 3:
        problems.append(f"Also found has {len(out['also_found'])} items; the "
                        f"guideline allows 3.")
    return problems


def watchdog(p: subprocess.Popen, t0: float, label: str,
             done: threading.Event, fired: threading.Event) -> None:
    """Kill the call at TIMEOUT. A tool-free call is silent until it answers,
    so the limit cannot wait for the next stream event."""
    while True:
        left = TIMEOUT - (time.time() - t0)
        if left <= 0:
            fired.set()
            p.kill()
            return
        if done.wait(min(60.0, left)):
            return
        print(f"    [{label}] {int(time.time() - t0)}s", flush=True)


def ready(unit: str) -> bool:
    d = AUDIT / unit
    return ((d / "bundle.json").is_file()
            and len(list((d / "components").glob("[0-9][0-9].json"))) == 28)


def run_one(unit: str) -> dict:
    d = AUDIT / unit
    t0 = time.time()
    data, files, labels, r = build(unit)
    prompt = (
        f"UNIT UNDER REVIEW: {unit}\n\n"
        "AUDIT DATA. This is the only input: the task's prompt and criteria, every\n"
        "component result a fix can come from, every recommendation, the senior\n"
        "review and the input-consistency result. Every item a fix can come from\n"
        "carries an id; cite those ids in `sources`.\n\n"
        + ac.dumps(data)
        + "\n\n" + "=" * 78 + "\n\n" + PROMPT.read_text(encoding="utf-8")
    )
    (d / "component_review_summary.prompt.md").write_text(prompt, encoding="utf-8")

    cmd = ["claude", "--print", "--model", MODEL, "--effort", EFFORT,
           "--tools", "", "--permission-mode", "bypassPermissions",
           "--session-id", str(uuid.uuid4()),
           "--output-format", "stream-json", "--verbose",
           "--json-schema", json.dumps(SCHEMA)]
    final, n_ev = None, 0
    child_env = {**os.environ, "IS_SANDBOX": "1"}
    done, fired = threading.Event(), threading.Event()
    try:
        with subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
                              bufsize=1, cwd=str(d), env=child_env) as p, \
                (d / "component_review_summary.stream.jsonl").open("w", encoding="utf-8") as sf:
            threading.Thread(target=watchdog, daemon=True,
                             args=(p, t0, f"{unit[:8]} summary", done, fired)).start()
            p.stdin.write(prompt)
            p.stdin.close()
            for line in p.stdout:
                sf.write(line)
                sf.flush()
                n_ev += 1
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if ev.get("type") == "result":
                    final = ev
            p.wait()
    except FileNotFoundError:
        return {"unit": unit, "status": "claude_not_found"}
    finally:
        done.set()

    rec = {"unit": unit, "elapsed_s": round(time.time() - t0, 1), "events": n_ev}
    if fired.is_set():
        rec["status"] = "timeout"
        return rec
    if final is None:
        rec["status"] = "no_result_event"
        return rec
    try:
        obj = final.get("structured_output")
        if not isinstance(obj, dict):
            txt = final.get("result")
            obj = txt if isinstance(txt, dict) else json.loads(txt)
        assert isinstance(obj.get("steps"), list), "no steps"
    except Exception as e:                                   # noqa: BLE001
        rec.update(status="invalid_output", error=f"{type(e).__name__}: {e}")
        return rec

    answer = json.loads(json.dumps(obj))
    problems = check(obj, files, labels, artifacts(d), r, data.get("prompt") or "")
    (d / SIDE).write_text(ac.dumps(
        {"unit": unit, "output": OUT,
         "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
         "model": MODEL, "effort": EFFORT, "elapsed_s": rec["elapsed_s"],
         "problems": problems, "answer": answer}), encoding="utf-8")
    (d / OUT).write_text(render_summary.render(r, files, labels, obj, problems),
                         encoding="utf-8")
    rec.update(status="ok", fixes=len(obj["steps"]), problems=len(problems))
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("units", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()

    have = [p.name for p in (sorted(AUDIT.iterdir()) if AUDIT.exists() else [])
            if ready(p.name)]
    units = [u for u in (a.units or have) if u in have]
    for u in (a.units or []):
        if u not in have:
            print(f"  {u}: fewer than 28 component results — run run_review.py first")

    units = ac.admit(units, "summarize.py", named=bool(a.units),
                     replaces=lambda u: a.redo and ac.current(AUDIT / u, OUT))
    if units is None:
        return 3
    if not a.redo:
        units = [u for u in units if not ac.current(AUDIT / u, OUT)]
    if not units:
        print("nothing to do")
        return 0

    for u in units:
        missing = [n for n in ("sense_check.json", "input_consistency.json")
                   if not (AUDIT / u / n).is_file()]
        if missing:
            print(f"  {u[:12]}: no {' or '.join(missing)}; the summary carries "
                  f"nothing from {'them' if len(missing) > 1 else 'it'}")
    print(f"output hygiene on {len(units)} unit(s), {MODEL} effort={EFFORT}, no tools")
    rc = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for rec in ex.map(run_one, units):
            if rec.get("status") == "ok":
                note = (f"{rec['fixes']} fixes"
                        + (f", {rec['problems']} check(s) failed, marked on the page"
                           if rec["problems"] else ""))
            else:
                note = rec.get("error") or ""
                rc = 1
            print(f"  {rec['unit'][:12]}: {rec.get('status')} "
                  f"({rec.get('elapsed_s')}s)  {note}".rstrip(), flush=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
