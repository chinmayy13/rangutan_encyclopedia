#!/usr/bin/env python3
"""Shared helpers for cua-audit-rerun.

A rerun is cua-audit-components' own pipeline pointed at a version folder, so
this module finds that sibling skill and imports its audit_common. The rest is
about version folders: how they are named, what they must hold, and which
first run they belong to.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
COMPONENTS_SKILL = Path(os.environ.get("CUA_AUDIT_COMPONENTS")
                        or SKILL.parent / "cua-audit-components").expanduser().resolve()
PIPELINE = COMPONENTS_SKILL / "scripts"
if not (PIPELINE / "audit_common.py").is_file():
    raise SystemExit(
        f"cua-audit-rerun runs the cua-audit-components scripts, and they are "
        f"not at {PIPELINE}.\nKeep the two skills side by side, or set "
        f"CUA_AUDIT_COMPONENTS to the cua-audit-components folder.")
sys.path.insert(0, str(PIPELINE))
import audit_common as ac  # noqa: E402

AUDIT = ac.AUDIT
VIEWS = ("prompt.md", "rubric.json", "task.md")
SIDES = ("inputs", "expected")
MANIFEST = "_rerun.json"
REPORT = ac.REPORT
SUMMARY = ac.SUMMARY
VERSION = re.compile(r"v(\d+)")

# Rebuilt by rerun_prepare.py on every prepare.
EVIDENCE = ("bundle.json", "inputs_extracted.md", "expected_extracted.md",
            "render", "render_index.json", MANIFEST)
# Written by the review passes. A folder holding any of them has been audited,
# at least in part, against whatever evidence it held at the time.
REVIEW = ("components", "_components.jsonl",
          "input_consistency.json", "input_consistency.prompt.md",
          "input_consistency.stream.jsonl",
          "sense_check.json", "sense_check.prompt.md", "sense_check.stream.jsonl",
          "component_scores.csv", REPORT,
          SUMMARY, "component_review_summary.json",
          "component_review_summary.prompt.md",
          "component_review_summary.stream.jsonl")


def visible(root: Path) -> list[Path]:
    """The files under root that count as staged. Dotfiles and dot-folders
    (.DS_Store, .git/) ride along with a copied folder but are not part of a
    submission, and the renderer already skips them."""
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*")
                  if p.is_file() and not any(part.startswith(".")
                                             for part in p.relative_to(root).parts))


def rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


_SHA: dict = {}


def sha256(path: Path) -> str:
    st = path.stat()
    key = (str(path.resolve()), st.st_size, st.st_mtime_ns)
    if key not in _SHA:
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        _SHA[key] = h.hexdigest()
    return _SHA[key]


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def is_first_run(d: Path) -> bool:
    """An audit folder cua-audit-components built: a bundle.json, and no
    manifest saying a rerun built it."""
    return (d / "bundle.json").is_file() and not (d / MANIFEST).exists()


def split_unit(name: str) -> tuple[str, str] | None:
    """'<first run>-<suffix>' -> (first run, suffix). The shortest prefix that
    names a first run wins, so '<task>-v2' always belongs to '<task>'."""
    for i, ch in enumerate(name):
        if ch == "-" and 0 < i < len(name) - 1 and is_first_run(AUDIT / name[:i]):
            return name[:i], name[i + 1:]
    return None


def version_of(suffix: str) -> int | None:
    m = VERSION.fullmatch(suffix or "")
    return int(m.group(1)) if m else None


def own_manifest(d: Path) -> dict | None:
    """This folder's manifest, or None when there is none or it was copied in
    from another folder along with that folder's files."""
    m = read_json(d / MANIFEST)
    return m if isinstance(m, dict) and m.get("unit") == d.name else None


def versions(base: str) -> list[Path]:
    """Every version folder of one first run: -v2, -v3, ... in number order,
    then any other suffix alphabetically."""
    if not AUDIT.is_dir():
        return []
    found = []
    for p in AUDIT.iterdir():
        if p.is_dir() and p.name.startswith(base + "-"):
            s = split_unit(p.name)
            if s and s[0] == base:
                found.append((version_of(s[1]), p))
    found.sort(key=lambda t: (t[0] is None, t[0] or 0, t[1].name))
    return [p for _, p in found]


def next_version(base: str) -> int:
    nums = [version_of(p.name[len(base) + 1:]) for p in versions(base)]
    return max([1] + [n for n in nums if n]) + 1


def present(d: Path, names) -> list[str]:
    return [n for n in names if (d / n).exists()]


def remove(d: Path, names) -> None:
    for n in names:
        p = d / n
        if p.is_dir() and not p.is_symlink():
            shutil.rmtree(p)
        elif p.exists() or p.is_symlink():
            p.unlink()


def done_components(d: Path) -> list[str]:
    cd = d / "components"
    return sorted(p.stem for p in cd.glob("[0-9][0-9].json")) if cd.is_dir() else []


def verdict(d: Path) -> tuple[int | None, int]:
    """(lowest component score, components scored) — the roll-up rule."""
    scores = []
    for n in done_components(d):
        s = (read_json(d / "components" / f"{n}.json") or {}).get("score")
        if isinstance(s, int):
            scores.append(s)
    return (min(scores) if scores else None), len(scores)


def summary_ok(d: Path) -> bool:
    """The summary exists and is at least as new as every result it is built
    from. Its existence is what marks an audit finished."""
    return ac.current(d, SUMMARY)


def reported(d: Path) -> bool:
    """The audit got as far as its report or its summary."""
    return (d / REPORT).is_file() or (d / SUMMARY).is_file()


def unfinished(d: Path) -> list[str]:
    """The passes a reported version still lacks, in run order. rollup.py runs
    before the summary and whether or not the unscored passes left a result, so
    a run can stop with its report written and the audit incomplete. The audit
    is finished once its summary describes the current results."""
    passes = ["review"] if len(done_components(d)) < 28 else []
    passes += [step for step, out in (("consistency", "input_consistency.json"),
                                      ("sense", "sense_check.json"))
               if not (d / out).is_file()]
    rest = list(passes)
    if passes or not ac.current(d, REPORT):
        rest.append("report")
    if passes or not summary_ok(d):
        rest.append("summary")
    return rest


def band(v: int | None) -> str:
    return ("FAIL" if v is not None and v <= 2 else "NON-FAIL" if v in (3, 4)
            else "PASS" if v == 5 else "INCOMPLETE")


def resolve_dir(target: str) -> Path:
    """A unit name, audit/<unit> or an absolute path -> AUDIT/<unit>."""
    for c in (AUDIT / target, Path(target).expanduser(), AUDIT / Path(target).name):
        if c.is_dir():
            d = c.resolve()
            if d.parent != AUDIT.resolve():
                raise SystemExit(
                    f"{d}: a version folder must sit directly in {AUDIT}, beside "
                    f"the first run — the review scripts only look there.")
            return AUDIT / d.name
    raise SystemExit(f"{target}: no such folder (looked for {AUDIT / target})")
