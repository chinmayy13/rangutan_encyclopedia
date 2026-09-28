#!/usr/bin/env python3
"""Carry a component's result over from an earlier audit of the same task
when nothing it is scored on has changed.

A component definition names its evidence in backticks: the bundle.json keys
it reads (`prompt`, `criteria[]`, `mechanical.23_rubric_weight_share`, ...)
and the files (`inputs_extracted.md`, `render/expected/<filename>/page-NN.png`,
`files/inputs/`, ...). Two audits give a component the same evidence when all
of these are equal:

    prompt       what run_review.py sends it: the definition, the preamble and
                 the rendered-pages list, the unit's name and folder aside
    model        the one the earlier result records
    bundle keys  every top-level key the definition names. For `mechanical`,
                 the entries owned by components of its own evidence class,
                 plus any entry it names (each entry is precomputed for the
                 component whose number it carries); the whole block when
                 that leaves none
    files        every file it names: the extracts, render_index.json (machine
                 paths and timestamps aside), the rendered pages, the staged
                 originals

The earlier audits are the task's first run and every version folder not
edited since it was prepared, newest first. A reused result goes to
components/NN.json with its folder paths moved to this one and
"_reused_from" naming the audit whose call produced it; _components.jsonl
logs it with status "reused". Components are told to read bundle.json whole,
so this trusts each definition to name what its score depends on.
"""
from __future__ import annotations

import functools
import hashlib
import json
import re
from pathlib import Path

import rerun_common as rr
from rerun_common import ac
import rerun_prepare as rp
import run_review

AUDIT = rr.AUDIT
FILES = (("inputs_extracted.md", "extract", "inputs"),
         ("expected_extracted.md", "extract", "expected"),
         ("render_index.json", "index", None),
         ("files/inputs/", "files", "inputs"),
         ("files/expected/", "files", "expected"),
         ("render/inputs/", "render", "inputs"),
         ("render/expected/", "render", "expected"))
PAGES = re.compile(r"RENDERED PAGES — .*?\n\n(?=Read `bundle\.json` first\.)", re.S)
# render_index.json fields that say where, when and on which machine it was
# made, rather than what the files look like.
INDEX_RUN = ("unit", "generated_at", "applications_csv", "tools")
INDEX_PATHS = ("source", "page_dir", "read_directly")
# LibreOffice's intermediate PDF stamps its creation time and a random id, and
# the pages rendered from it are compared already.
RENDER_SKIP = ("converted.pdf",)


def _sha(*parts) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(str(p).encode() + b"\0")
    return h.hexdigest()


def folder(unit: str) -> re.Pattern:
    """An absolute path to a folder named unit, wherever the workspace sits."""
    return re.compile(r"(?:/[^\s/`'\"()<>]+)*/" + re.escape(unit) + r"(?![\w-])")


def neutral(text: str, unit: str) -> str:
    text = folder(unit).sub("<unit folder>", text)
    return text.replace(f"rerun-local://{unit}/", "rerun-local://<unit>/")


@functools.lru_cache(maxsize=None)
def definitions() -> dict:
    """{number: (evidence class, definition text)} for the 28 components."""
    return {c["num"]: (c["cls"], c["path"].read_text(encoding="utf-8"))
            for c in run_review.components()}


def named(text: str, key: str) -> bool:
    return re.search("`" + re.escape(key) + r"(?:\[\])?[.`\[]", text) is not None


class Evidence:
    """What one audit folder shows its components, each part hashed once.

    With plan (rerun_prepare.build), the folder is taken as prepare would
    leave it. With proxy, each extract and render stands for the staged files
    it is made from: a plan made before prepare runs cannot hash outputs that
    do not exist yet, and both sides of a comparison must be taken alike."""

    def __init__(self, d: Path, plan: dict | None = None, proxy: bool = False):
        self.d, self.unit, self.proxy, self._memo = d, d.name, proxy or plan is not None, {}
        if plan is None:
            self.bundle = rr.read_json(d / "bundle.json") or {}
            self.files = {s: {rr.rel(d / "files" / s, p): p
                              for p in rr.visible(d / "files" / s)} for s in rr.SIDES}
        else:
            self.files = {s: plan["sides"][s]["files"] for s in rr.SIDES}
            self.bundle = {**plan["core"],
                           "staged_files": rp.staged(plan["core"], d, self.files)}

    def _once(self, key, fn):
        if key not in self._memo:
            self._memo[key] = fn()
        return self._memo[key]

    def _value(self, v) -> str:
        return _sha(neutral(json.dumps(v, sort_keys=True, default=str), self.unit))

    def key(self, k: str) -> str:
        v = self.bundle.get(k)
        if k == "staged_files" and isinstance(v, dict):
            # Components read these only for a FAILED download; a first run
            # says "ok" where a version folder says "cached".
            v = {s: {n: x if str(x).startswith("FAILED") else "ok"
                     for n, x in (v[s] or {}).items()} for s in v}
        return self._value(v)

    def mechanical(self, entry: str) -> str:
        return self._value((self.bundle.get("mechanical") or {}).get(entry))

    def staged(self, side: str) -> str:
        return self._once(("files", side), lambda: _sha(*(
            f"{n}:{rr.sha256(p)}" for n, p in sorted(self.files[side].items()))))

    def tree(self, rel: str) -> str:
        root = self.d / rel
        if not root.is_dir():
            return "absent"
        return _sha(*(f"{rr.rel(root, p)}:{rr.sha256(p)}" for p in sorted(root.rglob("*"))
                      if p.is_file() and p.name not in RENDER_SKIP))

    def index(self) -> str:
        idx = rr.read_json(self.d / "render_index.json")
        if not isinstance(idx, dict):
            return "absent"
        idx = {k: v for k, v in idx.items() if k not in INDEX_RUN}
        for side in rr.SIDES:
            idx[side] = [{k: v for k, v in e.items() if k not in INDEX_PATHS}
                         for e in idx.get(side) or [] if isinstance(e, dict)]
        if isinstance(idx.get("needs"), dict):
            idx["needs"] = {k: v for k, v in idx["needs"].items() if not k.endswith("_command")}
        return self._value(idx)

    def part(self, kind: str, side: str | None) -> str:
        if kind == "files":
            return self.staged(side)
        if self.proxy:
            return self.staged(side) if side else _sha(self.staged("inputs"),
                                                       self.staged("expected"))
        if kind == "extract":
            p = self.d / f"{side}_extracted.md"
            return self._once(p.name, lambda: rr.sha256(p) if p.is_file() else "absent")
        if kind == "render":
            return self._once(("render", side), lambda: self.tree(f"render/{side}"))
        return self._once("index", self.index)

    def prompt(self, comp: dict, sent: bool) -> str | None:
        """sent: the prompt this folder's own result was produced from;
        otherwise the one run_review.py would send now."""
        if sent:
            p = self.d / "components" / f"{comp['num']}.prompt.md"
            if not p.is_file():
                return None
            text = p.read_text(encoding="utf-8")
        else:
            text = run_review.render_prompt(self.unit, comp)
        text = neutral(text.replace(f"UNIT UNDER REVIEW: {self.unit}\n",
                                    "UNIT UNDER REVIEW: <unit>\n"), self.unit)
        return _sha(PAGES.sub("", text) if self.proxy else text)


def view(ev: Evidence, comp: dict, result: dict | None = None) -> dict | None:
    """Everything comp is scored on in ev's folder. result: that folder's own
    result for comp, when ev is an earlier audit."""
    cls, text = definitions()[comp["num"]]
    prompt = ev.prompt(comp, sent=result is not None)
    if prompt is None:
        return None
    v = {"call prompt": prompt,
         "call model": result.get("_model") if result is not None else comp["model"]}
    for k in sorted(ev.bundle):
        if not named(text, k):
            continue
        if k != "mechanical":
            v[f"bundle {k}"] = ev.key(k)
            continue
        entries = sorted(ev.bundle.get("mechanical") or {})
        mine = [e for e in entries
                if (definitions().get(e[:2]) or ("",))[0] == cls
                or re.search(r"\b" + re.escape(e) + r"\b", text)]
        # A class that owns no entry gives no hint which it reads: all of them.
        for e in mine or entries:
            v[f"bundle mechanical.{e}"] = ev.mechanical(e)
    for token, kind, side in FILES:
        if token in text:
            v[f"file {token}"] = ev.part(kind, side)
    return v


def earlier(d: Path, base: str) -> list[Path]:
    """The audits of base whose results d may take, newest first: version
    folders not edited since they were prepared, then the first run."""
    out = []
    for p in reversed(rr.versions(base)):
        man = rr.own_manifest(p)
        if (p.name != d.name and man and rr.done_components(p)
                and rp.build(p, base).get("fingerprint") == man.get("fingerprint")):
            out.append(p)
    first = AUDIT / base
    return out + ([first] if rr.done_components(first) else [])


def find(d: Path, base: str, comps: list[dict], plan: dict | None = None) -> dict:
    """{component number: (earlier audit, its result)} for each of comps that
    an earlier audit scored on the evidence d now gives it. With plan, d is
    judged as prepare would leave it (see Evidence)."""
    here = Evidence(d, plan)
    mine = {c["num"]: view(here, c) for c in comps}
    found = {}
    for src in earlier(d, base):
        there = Evidence(src, proxy=here.proxy)
        first_run = rr.own_manifest(src) is None
        for c in comps:
            n = c["num"]
            p = src / "components" / f"{n}.json"
            res = None if n in found else rr.read_json(p)
            if not isinstance(res, dict) or "score" not in res:
                continue
            # A first run prepared again after this call scored other evidence.
            if first_run and p.stat().st_mtime < (src / "bundle.json").stat().st_mtime:
                continue
            if view(there, c, res) == mine[n]:
                found[n] = (src, res)
    return found


def move(x, old: str, new: str):
    """x with every path into the folder old pointed at the folder new."""
    if isinstance(x, str):
        x = folder(old).sub(lambda m: str(AUDIT / new), x)
        x = re.sub(r"(?<![\w/.-])audit/" + re.escape(old) + r"(?![\w-])", f"audit/{new}", x)
        return x.replace(f"rerun-local://{old}/", f"rerun-local://{new}/")
    if isinstance(x, list):
        return [move(v, old, new) for v in x]
    if isinstance(x, dict):
        return {k: move(v, old, new) for k, v in x.items()}
    return x


def carry(d: Path, found: dict, comps: list[dict]) -> None:
    """Write each found result into d as its own, and log it."""
    by = {c["num"]: c for c in comps}
    cd = d / "components"
    cd.mkdir(parents=True, exist_ok=True)
    with (d / "_components.jsonl").open("a", encoding="utf-8") as log:
        for n, (src, res) in sorted(found.items()):
            res = move(res, src.name, d.name)
            res["_reused_from"] = res.get("_reused_from") or src.name
            (cd / f"{n}.json").write_text(ac.dumps(res), encoding="utf-8")
            # What a later version compares its own prompt against.
            (cd / f"{n}.prompt.md").write_text(run_review.render_prompt(d.name, by[n]),
                                               encoding="utf-8")
            for leftover in (f"{n}.stream.jsonl", f"{n}.raw.txt"):
                (cd / leftover).unlink(missing_ok=True)
            log.write(ac.dumps({"unit": d.name, "component": n, "title": by[n]["title"],
                                "model": res.get("_model"), "status": "reused",
                                "reused_from": res["_reused_from"],
                                "score": res.get("score")}, indent=None) + "\n")
