#!/usr/bin/env python3
"""Attest a Lean 4 development and emit a PROOF-ATTEMPT artifact (studio-kit-qi).

The compiler is the judge (principle P8). This script runs the project build,
prints the axiom closure and the signature of ONE declaration, compares that
signature with the CONJECTURE's compiled Formal Statement, and writes the
script-owned parts of a PROOF-ATTEMPT: the frontmatter status and the sections
Conjecture, Route, Development, Build Log, Verdict, Attestation. The agent-filled
sections (Assumptions, Deviations, Handoff) are preserved when the output file
already exists, so the script can be re-run after every change to the proof.

Criteria measured (IDs `cpt-<system>-criterion-<slug>`, declared in the
RESEARCH-PLAN's Success Criteria):

  builds                 `lake build` exits 0
  sorry-free             `sorryAx` absent from `#print axioms <decl>`
                         (the build exit code does NOT detect `sorry`)
  axioms-standard        axiom closure is a subset of --allowed-axioms
                         (default: propext, Classical.choice, Quot.sound)
  statement-matches      type printed by `#check @<decl>` equals the type in the
                         CONJECTURE's Formal Statement block (for --refutes: its
                         negation), compared up to whitespace
  dependencies-pinned    `lean-toolchain` present and every package in
                         `lake-manifest.json` carries a pinned `rev`
  statement-confirmed    the CONJECTURE's Faithfulness Cross-Check is complete:
                         an independent reading (`Read by` with a date, element
                         rows all `yes`, a `Discrepancies` line), instance
                         agreement (rows `agree` or `n/a`, none `disagree`) and a
                         dated `**Confirmed faithful by**:` line (the only judged
                         row; its completeness is checked here, its content never
                         filled here — P13)

Status written to the frontmatter:
  pass        every row passes                       (relation: proves)
  refuted     every row passes and --refutes was given (relation: refutes —
              the declaration's type is the negation of the formal statement)
  incomplete  attestation completed, at least one row fails
  error       attestation started but could not complete (lake missing,
              declaration not found after a green build, ...)
A usage error (missing file, CONJECTURE without a ```lean block) exits 2 and
writes no artifact at all.

Owned-sections hash (recomputed by graph_gate G7): SHA-256 over the text
"status: <status>\\n" and "generated-by: <value>\\n" followed, for each owned section in the order Conjecture,
Route, Development, Build Log, Verdict, by "## <name>\\n", the section body with
trailing whitespace stripped from every line, runs of blank lines collapsed to
one, leading and trailing blank lines removed, and a final "\\n".

Usage:
  python3 attest_lean.py --project DIR --file REL.lean --decl Full.Name \\
      --conjecture CONJECTURE.md --slug SLUG --out OUT.md \\
      [--refutes] [--system SYS] [--allowed-axioms a,b,c] [--title TEXT] \\
      [--description TEXT] [--route-note TEXT] [--build-cmd "lake build"] [--timeout SECONDS]

Exit: 0 artifact written (whatever its status); 2 usage error (nothing written).
"""

import argparse
import hashlib
import json
import platform
import re
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path

VERSION = "attest_lean.py v1.0"
OWNED = ["Conjecture", "Route", "Development", "Build Log", "Verdict"]
AGENT = ["Assumptions", "Deviations", "Handoff"]
DEFAULT_AXIOMS = "propext,Classical.choice,Quot.sound"
STATUS_MEANING = {
    "pass": "every criterion row passes; the declaration proves the conjecture's formal statement",
    "refuted": "every criterion row passes; the declaration proves the NEGATION of the formal statement — the conjecture is refuted and stays refuted",
    "incomplete": "the attestation completed and at least one criterion row fails; this is a statement with evidence, not a proof",
    "error": "the attestation could not complete; no verdict about the conjecture",
}
AGENT_PLACEHOLDER = {
    "Assumptions": "{Agent-filled: every lemma or fact the proof relies on, with its licence — see the PROOF-ATTEMPT template.}",
    "Deviations": "{Agent-filled: deviations from the plan, or `None` explicitly.}",
    "Handoff": "{Agent-filled: remaining goals as statements, unused hypotheses, what would refute, which budget limit this attempt counts toward.}",
}


# ── shared text helpers (graph_gate.py imports owned_sections_hash) ──────────

def die(msg: str) -> None:
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()
    return fm


def section(text: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", text, re.DOTALL | re.MULTILINE)
    return m.group(1) if m else ""


def norm_block(body: str) -> str:
    out, blank = [], False
    for line in body.splitlines():
        line = line.rstrip()
        if line == "":
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(line)
            blank = False
    while out and out[0] == "":
        out.pop(0)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def owned_sections_hash(text: str) -> str:
    h = hashlib.sha256()
    fm = frontmatter(text)
    h.update(("status: %s\n" % fm.get("status", "")).encode("utf-8"))
    h.update(("generated-by: %s\n" % fm.get("generated-by", "")).encode("utf-8"))
    for name in OWNED:
        h.update(("## %s\n" % name).encode("utf-8"))
        h.update(norm_block(section(text, name)).encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def status_line(sec: str, label: str) -> str:
    m = re.search(r"\*\*%s\*\*:\s*(.*)" % re.escape(label), sec)
    return m.group(1).strip() if m else ""


def is_placeholder(s: str) -> bool:
    s = s.strip()
    return not s or s.startswith("{") or s.lower() in ("none", "n/a", "tbd")


def parse_cross_check(text: str) -> dict:
    """Completeness of a CONJECTURE's Faithfulness Cross-Check (P13); shared with graph_gate G6."""
    cc = section(text, "Faithfulness Cross-Check")
    fs = section(text, "Formal Statement")
    read_by = status_line(cc, "Read by")
    disc = status_line(cc, "Discrepancies")
    conf = status_line(cc, "Confirmed faithful by") or status_line(fs, "Confirmed faithful by")
    element, instance = [], []
    for line in cc.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        last = cells[-1].lower() if cells else ""
        if last in ("yes", "no"):
            element.append(last)
        elif last in ("agree", "disagree", "n/a"):
            instance.append(last)
    problems = []
    if not cc.strip():
        problems.append("no Faithfulness Cross-Check section")
    if is_placeholder(read_by) or not re.search(r"\d{4}-\d{2}-\d{2}", read_by):
        problems.append("no independent reading (`Read by` with a date)")
    if not element:
        problems.append("no element rows marked yes/no")
    if "no" in element:
        problems.append("%d element row(s) marked no" % element.count("no"))
    if not disc.strip() or disc.strip().startswith("{"):
        problems.append("no `Discrepancies` line")
    if not instance:
        problems.append("no instance-agreement rows marked agree/disagree/n/a")
    if "disagree" in instance:
        problems.append("%d instance row(s) marked disagree" % instance.count("disagree"))
    if is_placeholder(conf) or not re.search(r"\d{4}-\d{2}-\d{2}", conf):
        problems.append("no dated `Confirmed faithful by`")
    return {"ok": not problems, "problems": problems, "read_by": read_by, "discrepancies": disc,
            "confirmed": conf or "missing", "elements": element, "instances": instance}


def short(s: str, n: int) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n].rstrip() + "…"


def norm_type(s: str) -> str:
    s = " ".join(s.split())
    return re.sub(r"¬\s+", "¬", s)


def split_signature(sig: str):
    """'Full.Name : type' -> ('Full.Name', 'type'); the name carries no spaces."""
    sig = sig.strip()
    m = re.match(r"^(\S+)\s*:\s*(.*)$", sig, re.DOTALL)
    return (m.group(1), m.group(2)) if m else ("", sig)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd, cwd, timeout):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out, time.time() - t0, None
    except FileNotFoundError as e:
        return None, "", time.time() - t0, "command not found: %s" % e
    except subprocess.TimeoutExpired:
        return None, "", time.time() - t0, "timeout after %ss" % timeout


# ── inputs ───────────────────────────────────────────────────────────────────

def parse_conjecture(path: Path):
    text = path.read_text(encoding="utf-8")
    ids = re.findall(r"cpt-([a-z0-9]+)-conj-[a-z0-9-]+", text)
    full = re.findall(r"cpt-[a-z0-9]+-conj-[a-z0-9-]+", text)
    if not full:
        die("no `cpt-<system>-conj-<slug>` ID found in %s" % path)
    fs = section(text, "Formal Statement")
    block = re.search(r"```lean\n(.*?)```", fs, re.DOTALL)
    if not block:
        die("%s has no ```lean block in its Formal Statement section "
            "(compile a stub and paste its `#check` output; tier A routes do not use this script)" % path)
    cc = parse_cross_check(text)
    return {"id": full[0], "system": ids[0], "block": block.group(1).strip(),
            "confirmed": cc["confirmed"], "confirmed_ok": cc["ok"], "cross_check": cc}


def module_of(rel_file: str) -> str:
    p = Path(rel_file)
    if p.suffix != ".lean":
        die("--file must be a .lean file relative to --project")
    return ".".join(p.with_suffix("").parts)


def read_manifest(project: Path):
    mf = project / "lake-manifest.json"
    if not mf.exists():
        return None
    try:
        return json.loads(mf.read_text(encoding="utf-8"))
    except Exception:
        return None


def git_info(project: Path):
    rc, out, _, err = run(["git", "-C", str(project), "rev-parse", "HEAD"], project, 60)
    if rc != 0 or err:
        return "not a git repository", "n/a"
    commit = out.strip()
    rc2, st, _, _ = run(["git", "-C", str(project), "status", "--porcelain", "--", "."], project, 60)
    changed = [l for l in (st or "").splitlines() if l.strip()]
    tree = "clean" if rc2 == 0 and not changed else "%d path(s) modified or untracked under the project" % len(changed)
    return commit, tree


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Attest a Lean 4 declaration and emit a PROOF-ATTEMPT artifact.")
    ap.add_argument("--project", required=True, help="Lake project directory (contains lakefile + lean-toolchain)")
    ap.add_argument("--file", required=True, help="file containing the declaration, relative to --project")
    ap.add_argument("--decl", required=True, help="fully qualified declaration name, e.g. Chsh.chsh_det_le_two")
    ap.add_argument("--conjecture", required=True, help="path to the CONJECTURE artifact (.md)")
    ap.add_argument("--slug", required=True, help="slug of the attempt ID: cpt-<system>-attempt-<slug>")
    ap.add_argument("--out", required=True, help="PROOF-ATTEMPT artifact to write (.md); a .build.log sibling is written too")
    ap.add_argument("--refutes", action="store_true", help="the declaration proves the NEGATION of the formal statement")
    ap.add_argument("--system", default=None, help="ID system prefix; default: taken from the CONJECTURE ID")
    ap.add_argument("--allowed-axioms", default=DEFAULT_AXIOMS, help="comma-separated allowed axiom set")
    ap.add_argument("--title", default=None, help="H1 of the artifact")
    ap.add_argument("--description", default=None, help="one-sentence frontmatter description (default: route, conjecture, status)")
    ap.add_argument("--route-note", default=None, help="how the proof was found (informational)")
    ap.add_argument("--build-cmd", default="lake build", help="build command run inside --project")
    ap.add_argument("--timeout", type=int, default=None, help="seconds for the build and for the query")
    args = ap.parse_args()

    project = Path(args.project).resolve()
    if not project.is_dir():
        die("%s is not a directory" % project)
    src = project / args.file
    if not src.is_file():
        die("%s not found" % src)
    conj_path = Path(args.conjecture)
    if not conj_path.is_file():
        die("%s not found" % conj_path)
    conj = parse_conjecture(conj_path)
    system = args.system or conj["system"]
    allowed = [a.strip() for a in args.allowed_axioms.split(",") if a.strip()]
    out_path = Path(args.out)
    log_path = out_path.with_name(out_path.stem + ".build.log")
    today = time.strftime("%Y-%m-%d")
    relation = "refutes" if args.refutes else "proves"
    module = module_of(args.file)
    log = ["# %s — %s" % (VERSION, time.strftime("%Y-%m-%d %H:%M:%S %z")),
           "# invocation: python3 " + " ".join(shlex.quote(a) for a in sys.argv), ""]
    fatal = None

    # 1. build
    build_cmd = shlex.split(args.build_cmd)
    rc, build_out, build_s, err = run(build_cmd, project, args.timeout)
    log += ["## %s (cwd %s)" % (args.build_cmd, args.project), build_out.rstrip(), "## exit: %s%s" % (rc, (" — " + err) if err else ""), ""]
    if err:
        fatal = "build could not run: " + err
    error_lines = [l for l in build_out.splitlines() if re.match(r"^(error:|✖)", l.strip())]
    builds_ok = rc == 0 and not error_lines
    sorry_warns = [l for l in build_out.splitlines()
                   if "declaration uses `sorry`" in l or "declaration uses 'sorry'" in l]
    sorry_in_file = [l for l in sorry_warns if args.file in l]

    # 2. query: axioms + signature
    axioms, signature, query_out = None, None, ""
    if fatal is None:
        q = "import %s\n#print axioms %s\n#check @%s\n" % (module, args.decl, args.decl)
        with tempfile.NamedTemporaryFile("w", suffix=".lean", prefix="attest_", delete=False, encoding="utf-8") as tf:
            tf.write(q)
            qpath = tf.name
        qrc, query_out, _, qerr = run(["lake", "env", "lean", qpath], project, args.timeout)
        Path(qpath).unlink(missing_ok=True)
        log += ["## query file", q.rstrip(), "", "## lake env lean <query>", query_out.rstrip(),
                "## exit: %s%s" % (qrc, (" — " + qerr) if qerr else ""), ""]
        m = re.search(r"'%s' depends on axioms: \[(.*?)\]" % re.escape(args.decl), query_out, re.DOTALL)
        if m:
            axioms = [a.strip() for a in m.group(1).split(",") if a.strip()]
        elif re.search(r"'%s' does not depend on any axioms" % re.escape(args.decl), query_out):
            axioms = []
        lines = query_out.splitlines()
        for i, l in enumerate(lines):
            if l.startswith(args.decl + " :"):
                signature = "\n".join(lines[i:]).strip()
                break
        if qerr or (builds_ok and (axioms is None or signature is None)):
            fatal = "query failed: " + (qerr or "declaration `%s` not found in module `%s` after a green build" % (args.decl, module))

    # 3. toolchain, packages, git, hashes
    tc_file = project / "lean-toolchain"
    toolchain = tc_file.read_text(encoding="utf-8").strip() if tc_file.exists() else None
    _, lv, _, _ = run(["lake", "env", "lean", "--version"], project, 120)
    lean_version = (lv or "").strip().splitlines()[0] if lv else "unknown"
    manifest = read_manifest(project)
    packages = manifest.get("packages", []) if isinstance(manifest, dict) else []
    unpinned = [p.get("name", "?") for p in packages if not re.fullmatch(r"[0-9a-f]{7,40}", str(p.get("rev", "")))]
    commit, tree = git_info(project)
    file_hash = sha256_file(src)

    # 4. verdict rows
    exp_name, exp_type = split_signature(conj["block"])
    got_name, got_type = split_signature(signature or "")
    if signature is None:
        stmt_ok, stmt_measured = False, "not measured (no signature)"
    elif args.refutes:
        cands = {norm_type("¬" + exp_type), norm_type("¬(" + exp_type + ")")}
        stmt_ok = norm_type(got_type) in cands
        stmt_measured = "type equals the NEGATION of the Formal Statement" if stmt_ok else "type differs from the negation of the Formal Statement"
    else:
        stmt_ok = norm_type(got_type) == norm_type(exp_type)
        stmt_measured = "type equals the Formal Statement" if stmt_ok else "type differs from the Formal Statement"
    sorry_ok = axioms is not None and "sorryAx" not in axioms
    extra = [a for a in (axioms or []) if a not in allowed and a != "sorryAx"]
    axioms_ok = axioms is not None and not extra
    deps_ok = toolchain is not None and manifest is not None and not unpinned
    cid = "cpt-%s-criterion-" % system
    rows = [
        (cid + "builds", "exit %s, %d error line(s), %.1f s" % (rc, len(error_lines), build_s), "exit 0, 0 errors", "mechanical: `%s`" % args.build_cmd, builds_ok),
        (cid + "sorry-free", ("sorryAx absent from closure" if sorry_ok else ("sorryAx IN closure" if axioms is not None else "not measured"))
         + ("; %d `sorry` warning(s) in %s" % (len(sorry_in_file), args.file) if sorry_in_file else ""), "absent", "mechanical: `#print axioms`", sorry_ok),
        (cid + "axioms-standard", ("[%s]" % ", ".join(axioms) if axioms is not None else "not measured") + ("; extra: [%s]" % ", ".join(extra) if extra else ""),
         "⊆ {%s}" % ", ".join(allowed), "mechanical: `#print axioms`", axioms_ok),
        (cid + "statement-matches", stmt_measured, "equal up to whitespace", "mechanical: `#check` vs CONJECTURE Formal Statement", stmt_ok),
        (cid + "dependencies-pinned", "%s; %d package(s)%s" % (toolchain or "lean-toolchain MISSING", len(packages), ("; unpinned: " + ", ".join(unpinned)) if unpinned else ""),
         "toolchain present, 0 unpinned", "mechanical: `lean-toolchain` + `lake-manifest.json`", deps_ok),
        (cid + "statement-confirmed",
         ("cross-check complete: independent reading by %s; %d element row(s) yes; discrepancies: %s; instances: %s; confirmed by %s" % (
             short(conj["cross_check"]["read_by"], 60), len(conj["cross_check"]["elements"]),
             short(conj["cross_check"]["discrepancies"], 40), "/".join(sorted(set(conj["cross_check"]["instances"]))),
             short(conj["confirmed"], 40)))
         if conj["confirmed_ok"] else "incomplete: " + "; ".join(conj["cross_check"]["problems"]),
         "complete, no open discrepancy",
         "judged by: %s (CONJECTURE Faithfulness Cross-Check; completeness checked by attest_lean.py)" % (
             ("reader %s, confirmer %s" % (short(conj["cross_check"]["read_by"], 40), short(conj["confirmed"], 30))) if conj["confirmed_ok"] else "nobody yet"),
         conj["confirmed_ok"]),
    ]
    if fatal:
        status = "error"
    elif all(r[4] for r in rows):
        status = "refuted" if args.refutes else "pass"
    else:
        status = "incomplete"

    # 5. preserve agent sections
    agent = dict(AGENT_PLACEHOLDER)
    if out_path.exists():
        old = out_path.read_text(encoding="utf-8")
        for name in AGENT:
            body = section(old, name).strip()
            if body:
                agent[name] = body

    # 6. assemble
    attempt_id = "cpt-%s-attempt-%s" % (system, args.slug)
    title = args.title or "%s — %s attempt, tier C (Lean 4), %s" % (conj["id"], "refutation" if args.refutes else "proof", today)
    tail = build_out.rstrip().splitlines()[-40:]
    pkg_lines = ["none (core Lean only)"] if not packages else [
        "`%s` @ `%s` (%s)" % (p.get("name"), p.get("rev", "UNPINNED"), p.get("url") or p.get("scope") or "local") for p in packages]
    doc = []
    description = args.description or "Tier C (Lean 4) %s attempt at %s — status %s, attested by %s." % (
        "refutation" if args.refutes else "proof", conj["id"], status, VERSION.split()[0])
    doc += ["---", "description: %s" % description, "status: %s" % status, "date: %s" % today, "generated-by: %s" % VERSION, "---", "",
            "# %s" % title, "", "**ID**: `%s`" % attempt_id, "", "## Table of Contents", "", "<!-- generated by `cfs toc` -->", ""]
    doc += ["## Conjecture", "",
            "- **Conjecture**: `%s` (%s)" % (conj["id"], conj_path),
            "- **Relation**: %s — the attested declaration %s" % (relation, "proves the negation of the formal statement" if args.refutes else "proves the formal statement"),
            "- **Expected formal statement** (CONJECTURE Formal Statement block, compiled stub `%s`):" % (exp_name or "?"), "",
            "```lean", conj["block"], "```", ""]
    doc += ["## Route", "",
            "- **Tier**: C — Lean 4 proof-assistant development (formal evidence, P1)",
            "- **Toolchain**: `%s` — %s" % (toolchain or "MISSING", lean_version),
            "- **Packages** (`lake-manifest.json`): " + "; ".join(pkg_lines),
            "- **Environment**: %s %s (%s)" % (platform.system(), platform.release(), platform.machine()),
            "- **Tools used to find the proof** (informational, P11): %s" % (args.route_note or "not stated"), ""]
    doc += ["## Development", "",
            "- **Project**: `%s` — git commit `%s`, working tree %s" % (args.project, commit, tree),
            "- **File**: `%s` — SHA-256 `%s`" % (args.file, file_hash),
            "- **Module**: `%s`" % module,
            "- **Declaration**: `%s`" % args.decl,
            "- **Signature** (`#check @%s`):" % args.decl, "",
            "```lean", signature or "(not available: %s)" % (fatal or "query failed"), "```", "",
            "- **Build command**: `%s` in the project directory (%.1f s, exit %s)" % (args.build_cmd, build_s, rc), ""]
    doc += ["## Assumptions", "", agent["Assumptions"], ""]
    doc += ["## Build Log", "", "`%s` (last %d line(s)):" % (args.build_cmd, len(tail)), "", "```"] + tail + ["```", "",
            "`#print axioms` and `#check`:", "", "```", query_out.rstrip() or "(no output)", "```", ""]
    doc += ["## Deviations", "", agent["Deviations"], ""]
    doc += ["## Verdict", "",
            "| Criterion ID | Measured | Threshold | Measured by | Result |",
            "|--------------|----------|-----------|-------------|--------|"]
    for rid, measured, thr, by, ok in rows:
        doc.append("| `%s` | %s | %s | %s | %s |" % (rid, measured.replace("|", "\\|"), thr, by, "pass" if ok else "fail"))
    doc += ["", "Status: **%s** — %s." % (status, STATUS_MEANING[status] + (" Cause: " + fatal if fatal else "")), ""]
    doc += ["## Handoff", "", agent["Handoff"], ""]
    doc += ["## Attestation", "",
            "- **Generated by**: %s on %s — `python3 %s`" % (VERSION, today, " ".join(shlex.quote(a) for a in sys.argv)),
            "- **Full log**: `%s` — SHA-256 `%s`" % (log_path.name, "@@LOGHASH@@"),
            "- **Owned-sections SHA-256**: `%s` (over the `status:` and `generated-by:` lines and the sections %s; recomputed by graph_gate G7)" % ("@@OWNED@@", ", ".join(OWNED)),
            ""]
    text = "\n".join(doc)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(log) + "\n", encoding="utf-8")
    text = text.replace("@@LOGHASH@@", sha256_file(log_path))
    text = text.replace("@@OWNED@@", owned_sections_hash(text))
    out_path.write_text(text, encoding="utf-8")

    # 7. stdout summary
    print("attest_lean: %s" % attempt_id)
    for rid, measured, _, _, ok in rows:
        print("  %-5s %-45s %s" % ("pass" if ok else "FAIL", rid.replace(cid, "criterion-"), measured))
    print("STATUS           : %s — %s" % (status.upper(), STATUS_MEANING[status]))
    if fatal:
        print("ERROR            : %s" % fatal)
    print("artifact         : %s" % out_path)
    print("log              : %s" % log_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
