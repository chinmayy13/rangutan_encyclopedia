#!/usr/bin/env python3
"""Install the renderers this audit needs, at the version the CUA VM runs.

Separate from render_files.py on purpose: rendering never installs anything,
so it is safe to run anywhere, and provisioning is an explicit act.

The version is not a preference. cua-applications.csv pins LibreOffice
7.3.7.2, and the Document Foundation keeps every past release, so the pinned
build is installable exactly rather than approximated by "latest" — which
matters because a newer LibreOffice repaginates a DOCX, and pagination is what
the rubric's visual criteria grade.

Everything lands under ~/.cua-renderers, so this never needs root and never
touches an application the operator installed for themselves.

    python3 provision_renderers.py                   # plan: what is missing, and why
    python3 provision_renderers.py --install         # install everything installable
    python3 provision_renderers.py soffice --install # just that one
    python3 provision_renderers.py --for audit/<unit_id> --install
                                                     # only what that unit needs
    python3 provision_renderers.py --uninstall       # remove ~/.cua-renderers
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_common as ac  # noqa: E402
import render_common as rc  # noqa: E402

DOWNLOAD_TIMEOUT = 1800


def arch_key() -> str:
    m = platform.machine().lower()
    if m in ("arm64", "aarch64"):
        return "arm64" if sys.platform == "darwin" else "aarch64"
    return "x86_64"


def acquire_url(tool: str) -> tuple[str | None, str | None]:
    """(url, pinned_version) for this platform, or (None, why-not)."""
    spec = rc.tool_spec(tool)
    acq = spec.get("acquire")
    if not acq:
        return None, "no automated install for this tool — see the hint"

    row = rc.application(spec.get("parity_app") or "") or {}
    version = rc.normalise_version(row.get("version"))
    if not version:
        return None, (f"cua-applications.csv has no usable version for "
                      f"{spec.get('parity_app')!r}, so there is nothing to pin to")

    path = (acq.get(rc.platform_key()) or {}).get(arch_key())
    if not path:
        return None, (f"{rc.platform_key()}/{arch_key()} has no published build of "
                      f"{tool} {version}")
    return (f"{acq['base'].format(version=version)}/{path.format(version=version)}",
            version)


def download(url: str, dest: Path) -> Path:
    """Stream to disk, reporting every 10% — these are hundreds of megabytes.

    Deliberately coarse. A carriage-returned percentage is one tidy line in a
    terminal and two hundred lines of noise in a captured log, and an agent
    reading that log is the main audience here.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp, open(dest, "wb") as out:
        total = int(resp.headers.get("content-length") or 0)
        done = milestone = 0
        while chunk := resp.read(1 << 20):
            out.write(chunk)
            done += len(chunk)
            pct = 100 * done // total if total else 0
            if pct >= milestone + 10:
                milestone = pct - pct % 10
                print(f"    downloading {milestone}% of {total >> 20} MiB",
                      file=sys.stderr, flush=True)
    print(f"    downloaded {dest.stat().st_size >> 20} MiB", file=sys.stderr, flush=True)
    return dest


def install_from_dmg(dmg: Path, app_name: str) -> Path:
    """Mount, copy the .app out, unmount. No installer, no admin prompt."""
    rc.APPS_DIR.mkdir(parents=True, exist_ok=True)
    mount = Path(tempfile.mkdtemp(prefix="cua-dmg-"))
    code, out, err = rc.run(["hdiutil", "attach", "-nobrowse", "-quiet",
                             "-mountpoint", str(mount), str(dmg)], timeout=600)
    if code != 0:
        raise RuntimeError(f"hdiutil attach failed: {(err or out).strip()[:200]}")
    try:
        src = next(iter(mount.glob(f"{app_name}*.app")), None)
        if src is None:
            raise RuntimeError(f"no {app_name}*.app inside {dmg.name}")
        target = rc.APPS_DIR / f"{app_name}.app"
        if target.exists():
            shutil.rmtree(target)
        print(f"    copying {src.name} -> {target}", file=sys.stderr)
        subprocess.run(["cp", "-R", str(src), str(target)], check=True, timeout=1800)
        return target
    finally:
        rc.run(["hdiutil", "detach", "-quiet", str(mount)], timeout=300)
        shutil.rmtree(mount, ignore_errors=True)


def install_from_deb_tarball(tarball: Path) -> Path:
    """Unpack the .deb payloads into $HOME — dpkg-deb -x needs no root."""
    import tarfile

    target = rc.APPS_DIR / "libreoffice"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tarball) as tf:
            try:
                tf.extractall(tmp, filter="data")
            except TypeError:                   # filter= arrived in 3.12
                tf.extractall(tmp)              # noqa: S202
        debs = sorted(Path(tmp).rglob("*.deb"))
        if not debs:
            raise RuntimeError("no .deb payloads inside the tarball")
        extractor = shutil.which("dpkg-deb")
        print(f"    unpacking {len(debs)} packages", file=sys.stderr)
        for deb in debs:
            if extractor:
                code, _, err = rc.run([extractor, "-x", str(deb), str(target)],
                                      timeout=600)
            else:                     # no dpkg: a .deb is an ar archive
                code, _, err = rc.run(["sh", "-c",
                                       f"cd {target} && ar p {deb!s} data.tar.xz "
                                       f"| tar xJ"], timeout=600)
            if code != 0:
                raise RuntimeError(f"{deb.name}: {err.strip()[:160]}")
    return target


def provision_pip(tool: str, acq: dict) -> dict:
    """A Python wheel into the workspace venv, creating that venv if need be.

    Skipping here for want of a venv was the one provisioning outcome nobody
    could act on from inside the run, so it is not an outcome any more.
    """
    python, _ = ac.reader_python(log=lambda m: print(m, file=sys.stderr))
    package = acq.get("package") or tool
    print(f"  {tool}: pip install {package} into {python}", file=sys.stderr)
    code, out, err = rc.run([str(python), "-m", "pip", "install", "--quiet", package],
                            timeout=900)
    rc.forget_tools()
    if code != 0:
        return {"tool": tool, "ok": False, "error": (err or out).strip()[:300]}
    return {"tool": tool, "ok": rc.probe(tool)["present"], "package": package,
            "installed_at": str(python), "found_version": rc.tool_version(tool),
            "parity": "n/a",
            "when": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def provision(tool: str) -> dict:
    """Install one tool at its pinned version. Returns a record for the log."""
    acq = rc.tool_spec(tool).get("acquire") or {}
    if acq.get("kind") == "pip":
        return provision_pip(tool, acq)

    url, why = acquire_url(tool)
    if not url:
        return {"tool": tool, "ok": False, "skipped": why,
                "hint": rc.install_hint(tool)}
    version = why
    print(f"  {tool} {version}\n    {url}", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmp:
        archive = download(url, Path(tmp) / url.rsplit("/", 1)[-1])
        try:
            if archive.suffix == ".dmg":
                where = install_from_dmg(archive, "LibreOffice")
            else:
                where = install_from_deb_tarball(archive)
        except Exception as exc:                                # noqa: BLE001
            return {"tool": tool, "ok": False, "error": str(exc)[:300], "url": url}

    rc.forget_tools()                     # the binary is new; discovery was cached
    found = rc.tool_version(tool)
    return {"tool": tool, "ok": rc.which(tool) is not None, "url": url,
            "pinned_version": version, "installed_at": str(where),
            "found_version": found, "parity": rc.compare_versions(version, found),
            "when": datetime.now(timezone.utc).isoformat(timespec="seconds")}


def record(results: list[dict]) -> None:
    rc.PROVISION_FILE.parent.mkdir(parents=True, exist_ok=True)
    log = []
    if rc.PROVISION_FILE.exists():
        try:
            log = json.loads(rc.PROVISION_FILE.read_text(encoding="utf-8"))
        except Exception:                                       # noqa: BLE001
            log = []
    log = [r for r in log if r.get("tool") not in {x["tool"] for x in results}]
    rc.PROVISION_FILE.write_text(
        ac.dumps(log + results, indent=2) + "\n", encoding="utf-8")


def plan(tools: list[str], scope: str = "") -> int:
    """What is missing or off-version, what it costs, and what it unlocks."""
    print(f"applications: {rc.APPLICATIONS_CSV}")
    print(f"install root: {rc.TOOLS_ROOT}")
    print(f"scope:        {scope or 'every tool with an automated install'}\n")
    todo = []
    for tool in tools:
        p = rc.probe(tool)
        if p["present"] and p.get("parity") in ("exact", "compatible", "n/a", None):
            continue
        todo.append(tool)
        state = ("not installed" if not p["present"]
                 else f"version {rc.normalise_version(p.get('found_version'))} "
                      f"!= pinned {rc.normalise_version(p.get('pinned_version'))}")
        acq = rc.tool_spec(tool).get("acquire") or {}
        print(f"  {tool}: {state}")
        print(f"    unlocks: {p.get('unlocks')}")
        if acq.get("kind") == "pip":
            print(f"    installable: pip install {acq.get('package') or tool}")
            continue
        url, why = acquire_url(tool)
        if url:
            print(f"    installable at the pinned version: {url}")
        else:
            print(f"    no automated install: {why}")
            print(f"    hint: {p['hint']}")
    if not todo:
        print("  every renderer in scope is present at the pinned version.")
        return 0
    args = " ".join(todo)
    print(f"\n  python3 {Path(__file__).name} {args} --install")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tools", nargs="*", help="tools to act on (default: all)")
    ap.add_argument("--for", dest="unit", metavar="AUDIT_UNIT_DIR",
                    help="only what this unit's staged files actually need")
    ap.add_argument("--install", action="store_true", help="actually install")
    ap.add_argument("--uninstall", action="store_true",
                    help=f"delete {rc.TOOLS_ROOT}")
    a = ap.parse_args()

    if a.uninstall:
        if rc.TOOLS_ROOT.exists():
            shutil.rmtree(rc.TOOLS_ROOT)
            print(f"removed {rc.TOOLS_ROOT}")
        else:
            print(f"{rc.TOOLS_ROOT} does not exist")
        return 0

    known = list((rc.registry().get("tools") or {}))
    unknown = [t for t in a.tools if t not in known]
    if unknown:
        ap.error(f"unknown tool(s) {unknown}; known: {', '.join(known)}")

    scope = ""
    if a.unit:
        import render_files as rf
        unit = Path(a.unit).resolve()
        if not (unit / "files").is_dir():
            ap.error(f"{unit} has no files/ — run audit_prepare.py first")
        need = rf.unit_needs(unit)
        tools = a.tools or need["install"] + need["off_version"]
        scope = (f"{unit.name}, file kinds {', '.join(need['kinds']) or 'none'}")
        if not tools:
            print(f"{unit.name}: every renderer its files need is present at the "
                  f"pinned version — nothing to install.")
            return 0
    else:
        tools = a.tools or [t for t in known if rc.tool_spec(t).get("acquire")]

    if not a.install:
        return plan(tools, scope)

    results = [provision(t) for t in tools]
    record(results)
    for r in results:
        if r.get("ok"):
            print(f"  ok       {r['tool']} {r.get('found_version')} "
                  f"[parity {r.get('parity')}] -> {r['installed_at']}")
        elif r.get("skipped"):
            print(f"  skipped  {r['tool']}: {r['skipped']}")
        else:
            print(f"  FAILED   {r['tool']}: {r.get('error')}")
    print(f"\nrecorded in {rc.PROVISION_FILE}")
    return 0 if all(r.get("ok") or r.get("skipped") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
