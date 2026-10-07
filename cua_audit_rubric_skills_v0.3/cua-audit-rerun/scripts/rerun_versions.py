#!/usr/bin/env python3
"""The version folders of one audited task: what exists, what is pending, and
a fresh one to edit.

    python3 rerun_versions.py status <task_id>
    python3 rerun_versions.py new <task_id>                   # copy the latest version to -v<N+1>
    python3 rerun_versions.py new <task_id> --from <unit>     # copy that folder instead
    python3 rerun_versions.py new <task_id> --from-response   # the views and files of tasks/<task_id>/response.json

`status` exits 1 when the task has no finished first audit: that audit is
cua-audit-components' job, and a rerun starts only after it.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rerun_common as rr  # noqa: E402
from rerun_common import ac  # noqa: E402
import rerun_prepare as rp  # noqa: E402

RERUN = Path(__file__).resolve().with_name("rerun.py")


def first_run_of(target: str) -> str:
    """A task id, its first-run unit or any of its version folders -> the first run."""
    name = Path(target).name
    s = rr.split_unit(name)
    return s[0] if s else name


def latest(base: str) -> Path:
    """The newest numbered version holding all three views, else the first run."""
    numbered = [d for d in rr.versions(base)
                if rr.version_of(d.name[len(base) + 1:]) is not None]
    for d in reversed(numbered):
        if all((d / v).is_file() for v in rr.VIEWS):
            return d
    return rr.AUDIT / base


def state(d: Path, base: str) -> dict:
    missing = [v for v in rr.VIEWS if not (d / v).is_file()]
    if missing:
        return {"state": "incomplete", "pending": False,
                "detail": f"missing {', '.join(missing)}"}
    man = rr.own_manifest(d)
    v, n = rr.verdict(d)
    plan = rp.build(d, base)
    edited = bool(man) and plan.get("fingerprint") != man.get("fingerprint")
    reported = bool(man) and rr.reported(d)
    if plan["errors"] and not reported:
        return {"state": "invalid", "pending": False, "detail": plan["errors"][0]}
    if reported:
        st = "summarized" if (d / rr.SUMMARY).exists() else "reported"
        rest = [] if edited else rr.unfinished(d)
        if rest:
            return {"state": st, "pending": True, "verdict": v,
                    "detail": f"stopped before {', '.join(rest)} finished; "
                              f"running it again finishes it"}
        return {"state": st, "pending": False, "verdict": v,
                "detail": ("edited after its audit, so its report describes the "
                           "earlier content") if edited else ""}
    if not man:
        foreign = rr.present(d, rr.EVIDENCE + rr.REVIEW)
        shown = ", ".join(foreign[:3]) + (f" and {len(foreign) - 3} more" if len(foreign) > 3 else "")
        return {"state": "staged", "pending": True,
                "detail": "not prepared yet" + (
                    f"; holds {shown} from a copied run, which prepare clears"
                    if foreign else "")}
    if n:
        return {"state": f"reviewing {n}/28", "pending": True,
                "detail": ("edited since its review started: resuming needs --reset"
                           if edited else "resumes where it stopped")}
    return {"state": "prepared", "pending": True,
            "detail": "edited since prepared; prepare rebuilds it" if edited
            else "ready to review"}


def first_run_ready(base: str) -> bool:
    """Say why not, when the task has no finished first audit."""
    bd = rr.AUDIT / base
    if not rr.is_first_run(bd):
        src = [r / base for r in (ac.TASKS, ac.ATTEMPTS) if (r / base / "response.json").exists()]
        print(f"{base}: no first audit in {rr.AUDIT}"
              + (f" (its task files are in {src[0]})" if src else "") + ".\n"
              f"  The first audit belongs to cua-audit-components; reruns start after it.")
        return False
    if not (bd / rr.SUMMARY).exists():
        _, n = rr.verdict(bd)
        print(f"{base}: its first audit has not finished ({n}/28 components, no "
              f"{rr.SUMMARY}).\n  Finish it with cua-audit-components; reruns start after it.")
        return False
    return True


def pending(base: str) -> list[Path]:
    return [d for d in rr.versions(base) if state(d, base)["pending"]]


def status(target: str) -> int:
    base = first_run_of(target)
    if not first_run_ready(base):
        return 1
    bd = rr.AUDIT / base
    v, _ = rr.verdict(bd)
    rows = [("first run", base, "summarized" if (bd / rr.SUMMARY).exists() else "reported",
             f"verdict {v} {rr.band(v)}")]
    waiting = []
    for d in rr.versions(base):
        s = state(d, base)
        ver = f"verdict {s['verdict']} {rr.band(s['verdict'])}" if "verdict" in s else ""
        rows.append((d.name[len(base) + 1:], d.name, s["state"],
                     "  ".join(x for x in (ver, s["detail"]) if x)))
        if s["pending"]:
            waiting.append(d)
    w = max(len(r[1]) for r in rows)
    print(f"task {base}")
    for label, name, st, detail in rows:
        print(f"  {label:<10} {name:<{w}}  {st:<14} {detail}".rstrip())
    if len(waiting) == 1:
        print(f"next: python3 {RERUN} {waiting[0].name}")
    elif waiting:
        print(f"next: {len(waiting)} versions are pending "
              f"({', '.join(d.name for d in waiting)}); audit the one meant: "
              f"python3 {RERUN} <unit>")
    else:
        print(f"next: python3 {RERUN} {base} --new    (copies {latest(base).name} "
              f"to {base}-v{rr.next_version(base)} and audits it)")
    return 0


def copy_view(src: Path, dest: Path) -> None:
    """shutil.copy2, except that a rubric.json spelling characters as \\uXXXX
    escapes is written with each one as itself: the copy is what someone
    edits, and an escape left in it is carried into every later version."""
    shutil.copy2(src, dest)
    if dest.name != "rubric.json":
        return
    try:
        text = dest.read_text(encoding="utf-8")
        rub = json.loads(text) if "\\u" in text else None
    except ValueError:
        return
    if rub is not None:
        dest.write_text(ac.dumps(rub, indent=2) + "\n", encoding="utf-8")


def new(base: str, src: str | None = None, from_response: bool = False) -> Path | None:
    if not first_run_ready(base):
        return None
    dest = rr.AUDIT / f"{base}-v{rr.next_version(base)}"
    if dest.exists():
        print(f"{dest} already exists")
        return None

    if from_response:
        try:
            origin = ac.unit_dir(base) / "response.json"
        except FileNotFoundError as e:
            print(f"  {e}")
            return None
        dest.mkdir(parents=True)
        rp.ap.write_views(base, dest)
        got = rp.ap.stage_files(ac.bundle_for(base), dest)
        bad = [f"{side}/{n}: {s}" for side, x in got.items() for n, s in x.items()
               if s.startswith("FAILED")]
        if bad:
            print("  could not download: " + "; ".join(bad))
        what = str(origin)
    else:
        sd = rr.resolve_dir(src) if src else latest(base)
        missing = [v for v in rr.VIEWS if not (sd / v).is_file()]
        if missing:
            print(f"{sd.name} has no {', '.join(missing)} to copy")
            return None
        dest.mkdir(parents=True)
        for v in rr.VIEWS:
            copy_view(sd / v, dest / v)
        for side in rr.SIDES:
            root = sd / "files" / side
            for f in rr.visible(root):
                t = dest / "files" / side / rr.rel(root, f)
                t.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, t)
        what = sd.name

    for side in rr.SIDES:
        (dest / "files" / side).mkdir(parents=True, exist_ok=True)
    nin, nexp = (len(rr.visible(dest / "files" / s)) for s in rr.SIDES)
    print(f"created {dest}\n"
          f"  from {what}: prompt.md, rubric.json, task.md, {nin} input and "
          f"{nexp} expected file(s)\n"
          f"  edit it, then audit it: python3 {RERUN} {dest.name}")
    return dest


def main() -> int:
    p = argparse.ArgumentParser(description="Version folders of an audited task.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status", help="the first run and every version, with what to run next")
    s.add_argument("task_id", help="task id, or any of its version folders")
    n = sub.add_parser("new", help="create the next version folder")
    n.add_argument("task_id")
    src = n.add_mutually_exclusive_group()
    src.add_argument("--from", dest="src", metavar="UNIT",
                     help="copy this folder (default: the latest version, else the first run)")
    src.add_argument("--from-response", action="store_true",
                     help="write the views and download the files from the task's "
                          "response.json, for a task re-downloaded since the first run")
    a = p.parse_args()
    if a.cmd == "status":
        return status(a.task_id)
    return 0 if new(first_run_of(a.task_id), a.src, a.from_response) else 1


if __name__ == "__main__":
    raise SystemExit(main())
