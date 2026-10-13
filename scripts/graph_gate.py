#!/usr/bin/env python3
"""Cross-artifact semantic gate for studio-kit-qi claim graphs.

Deterministic checks that exceed what `cfs validate` (static structure) can express:

  G1  THEOREM frontmatter status is computed, not asserted:
        verified        <=> every load-bearing node status >= machine-checked
        in-verification <=> a proof map exists
  G2  LEMMA status never exceeds what its Verification section can establish
        (heuristic v0: `formalized`/`machine-checked` require an artifact reference
         keyword in the Verification section; see STRONG_EVIDENCE).
  G3  Every load-bearing node ID in a PROOF-MAP resolves to a LEMMA/CLAIM artifact.
  G4  CLAIM status `certified` requires a CERTIFICATE referencing it with a passing CHECK-RUN.
  G5  VERIFICATION-PLAN status `approved` requires a filled Approval section.
  G6  CONJECTURE status is derived from attempts and claims, never asserted:
        proved    <=> Proved by names a PROOF-ATTEMPT with status pass whose
                      Conjecture section references this conjecture, or a CLAIM
                      with status certified (CLAIMs do not reference conjectures;
                      the conjecture names the claim)
        refuted   <=> Refuted by names a PROOF-ATTEMPT with status refuted or a
                      certified CLAIM; and ANY refuting attempt forces `refuted`
                      (P10: refuted stays refuted)
        supported <=> Evidence has an exact instance check
        withdrawn <=> Withdrawn by is filled and carries a date
        a passing attempt that references a conjecture not marked proved is stale;
        every CONJECTURE references a RESEARCH-PLAN that resolves;
        a CONJECTURE with a Lean block that has attempts or is proved/refuted has a
        complete Faithfulness Cross-Check (P13: independent reading, instance
        agreement, dated confirmation — parsed by attest_lean.parse_cross_check)
  G7  PROOF-ATTEMPT is script-generated: `generated-by` present, status in the
        closed vocabulary, every Verdict row `pass` when status is pass/refuted,
        the Verdict rows are exactly the criterion IDs declared in the conjecture's
        RESEARCH-PLAN (P7), Conjecture section resolves, and the owned-sections
        SHA-256 in Attestation equals the recomputation (import from
        attest_lean.py) — hand-edited script-owned sections fail here.
  G8  RESEARCH-PLAN status `approved` requires a filled Approval section; every
        Conjecture Register row's status equals the CONJECTURE's frontmatter and
        every register ID resolves.

Usage:  python3 graph_gate.py <artifacts-root> [--json]
Exit:   0 all gates pass, 1 violations found, 2 usage/parse error.
"""

import json
import re
import sys
from pathlib import Path

STATUS_ORDER = ["open", "cited", "expert-verified", "machine-checked", "formalized"]
CONJ_STATUS = ["open", "supported", "proved", "refuted", "withdrawn"]
ATTEMPT_STATUS = ["pass", "incomplete", "refuted", "error"]
try:  # the attestation script ships next to this gate; its hash spec is the reference
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from attest_lean import owned_sections_hash, parse_cross_check
except Exception:  # pragma: no cover
    owned_sections_hash = parse_cross_check = None
STRONG_EVIDENCE = re.compile(
    r"cpt-[a-z0-9-]+-run-[a-z0-9-]+"  # a CHECK-RUN id
    r"|build.*(pass|ok|green)|lake build|leanprover", re.IGNORECASE)


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


def ids_in(text: str, kind: str) -> list:
    return re.findall(rf"cpt-[a-z0-9]+-{kind}-[a-z0-9-]+", text)


def collect(root: Path) -> dict:
    docs = {}
    for kind in ["CLAIM", "CERTIFICATE", "CHECK-RUN", "THEOREM", "PROOF-MAP", "LEMMA", "VERIFICATION-PLAN",
                 "RESEARCH-PLAN", "CONJECTURE", "PROOF-ATTEMPT"]:
        for p in sorted((root / kind).rglob("*.md")):
            if p.name in ("template.md", "rules.md", "checklist.md"):
                continue
            text = p.read_text(encoding="utf-8")
            own_kind = {"CLAIM": "claim", "CERTIFICATE": "cert", "CHECK-RUN": "run",
                        "THEOREM": "thm", "PROOF-MAP": "pm", "LEMMA": "lem",
                        "VERIFICATION-PLAN": "vplan", "RESEARCH-PLAN": "rplan",
                        "CONJECTURE": "conj", "PROOF-ATTEMPT": "attempt"}[kind]
            own_ids = ids_in(text, own_kind)
            docs[p] = {"kind": kind, "text": text, "fm": frontmatter(text),
                       "id": own_ids[0] if own_ids else None}
    return docs


def rank(status: str) -> int:
    return STATUS_ORDER.index(status) if status in STATUS_ORDER else -1


def status_line(sec: str, label: str) -> str:
    m = re.search(rf"\*\*{re.escape(label)}\*\*:\s*(.*)", sec)
    return m.group(1).strip() if m else ""


def is_placeholder(s: str) -> bool:
    s = s.strip()
    return not s or s.startswith("{") or s.lower() in ("none", "none yet", "n/a")


def run_gates(root: Path):
    docs = collect(root)
    by_id = {d["id"]: (p, d) for p, d in docs.items() if d["id"]}
    violations = []

    lemma_status = {d["id"]: d["fm"].get("status", "open")
                    for _, d in docs.items() if d["kind"] == "LEMMA" and d["id"]}
    claim_status = {d["id"]: d["fm"].get("status", "open")
                    for _, d in docs.items() if d["kind"] == "CLAIM" and d["id"]}

    # Passing check-runs per certificate id
    cert_passing = set()
    for p, d in docs.items():
        if d["kind"] == "CHECK-RUN" and d["fm"].get("status") == "pass":
            cert_passing.update(ids_in(section(d["text"], "Certificate"), "cert"))

    # Certificates per claim id
    claim_certs = {}
    for p, d in docs.items():
        if d["kind"] == "CERTIFICATE" and d["id"]:
            for cid in ids_in(section(d["text"], "Certified Claim"), "claim"):
                claim_certs.setdefault(cid, []).append(d["id"])

    # Discovery layer indexes
    attempt_status = {d["id"]: d["fm"].get("status", "") for _, d in docs.items()
                      if d["kind"] == "PROOF-ATTEMPT" and d["id"]}
    attempt_conjs = {d["id"]: set(ids_in(section(d["text"], "Conjecture"), "conj"))
                     for _, d in docs.items() if d["kind"] == "PROOF-ATTEMPT" and d["id"]}
    conj_status = {d["id"]: d["fm"].get("status", "open") for _, d in docs.items()
                   if d["kind"] == "CONJECTURE" and d["id"]}
    rplan_criteria = {d["id"]: set(re.findall(r"\*\*ID\*\*:\s*`(cpt-[a-z0-9]+-criterion-[a-z0-9-]+)`",
                                                 section(d["text"], "Success Criteria")))
                      for _, d in docs.items() if d["kind"] == "RESEARCH-PLAN" and d["id"]}
    conj_plans = {d["id"]: set(ids_in(d["text"], "rplan")) for _, d in docs.items()
                  if d["kind"] == "CONJECTURE" and d["id"]}
    refuting = {}   # conj id -> attempt ids with status refuted that reference it
    passing = {}    # conj id -> attempt ids with status pass that reference it
    for aid, conjs in attempt_conjs.items():
        for c in conjs:
            if attempt_status.get(aid) == "refuted":
                refuting.setdefault(c, []).append(aid)
            if attempt_status.get(aid) == "pass":
                passing.setdefault(c, []).append(aid)

    for p, d in docs.items():
        if d["kind"] == "PROOF-MAP":
            lb = section(d["text"], "Load-Bearing Nodes") + section(d["text"], "Dependency Graph")
            nodes = set(ids_in(lb, "lem")) | set(ids_in(lb, "claim"))
            for n in nodes:
                if n not in by_id:                                    # G3
                    violations.append(f"G3 {p.name}: load-bearing node {n} resolves to no artifact")

        if d["kind"] == "THEOREM":                                    # G1
            status = d["fm"].get("status", "open")
            pm_ids = ids_in(section(d["text"], "Proof Map"), "pm")
            if status == "verified":
                for pm_id in pm_ids:
                    pm = next((dd for _, dd in docs.items() if dd["id"] == pm_id), None)
                    if not pm:
                        violations.append(f"G1 {p.name}: verified but proof map {pm_id} missing")
                        continue
                    lb = section(pm["text"], "Load-Bearing Nodes") + section(pm["text"], "Dependency Graph")
                    for n in set(ids_in(lb, "lem")):
                        if rank(lemma_status.get(n, "open")) < rank("machine-checked"):
                            violations.append(
                                f"G1 {p.name}: status verified but load-bearing {n} is "
                                f"{lemma_status.get(n, 'open')}")
            if status in ("verified", "in-verification") and not pm_ids:
                violations.append(f"G1 {p.name}: status {status} but no proof map referenced")

        if d["kind"] == "LEMMA":                                      # G2
            status = d["fm"].get("status", "open")
            ver = section(d["text"], "Verification")
            if rank(status) >= rank("machine-checked") and not STRONG_EVIDENCE.search(ver):
                violations.append(
                    f"G2 {p.name}: status {status} but Verification section shows no "
                    f"check-run/build artifact")

        if d["kind"] == "VERIFICATION-PLAN":                          # G5
            if d["fm"].get("status") == "approved":
                appr = section(d["text"], "Approval").strip()
                if not appr or appr.startswith("{"):
                    violations.append(f"G5 {p.name}: status approved but Approval section empty/placeholder")

        if d["kind"] == "CONJECTURE":                                 # G6
            status = d["fm"].get("status", "open")
            st = section(d["text"], "Status")
            proved_by = status_line(st, "Proved by")
            refuted_by = status_line(st, "Refuted by")
            withdrawn_by = status_line(st, "Withdrawn by")
            if status not in CONJ_STATUS:
                violations.append(f"G6 {p.name}: status `{status}` not in {CONJ_STATUS}")
            proved_ev = [a for a in ids_in(proved_by, "attempt")
                         if attempt_status.get(a) == "pass" and d["id"] in attempt_conjs.get(a, ())]
            proved_ev += [c for c in ids_in(proved_by, "claim") if claim_status.get(c) == "certified"]
            refuted_ev = [a for a in ids_in(refuted_by, "attempt")
                          if attempt_status.get(a) == "refuted" and d["id"] in attempt_conjs.get(a, ())]
            refuted_ev += [c for c in ids_in(refuted_by, "claim") if claim_status.get(c) == "certified"]
            if status == "proved" and not proved_ev:
                violations.append(f"G6 {p.name}: status proved but Proved by names no passing attempt "
                                  f"(referencing {d['id']}) and no certified claim")
            if status == "refuted" and not refuted_ev:
                violations.append(f"G6 {p.name}: status refuted but Refuted by names no refuting attempt "
                                  f"and no certified counterexample claim")
            refuters = sorted(set(refuting.get(d["id"], [])) | set(refuted_ev))
            if status != "refuted" and refuters:
                violations.append(f"G6 {p.name}: status {status} but refuting artifact(s) exist: "
                                  f"{', '.join(refuters)} — refuted stays refuted (P10)")
            if status not in ("proved", "refuted") and passing.get(d["id"]):
                violations.append(f"G6 {p.name}: status {status} but passing attempt(s) reference it: "
                                  f"{', '.join(passing[d['id']])} — status is stale")
            if status == "supported":
                ev = section(d["text"], "Evidence")
                if is_placeholder(ev) or not re.search(r"\bexact\b", ev, re.IGNORECASE):
                    violations.append(f"G6 {p.name}: status supported but Evidence shows no exact instance check")
            if status == "withdrawn" and (is_placeholder(withdrawn_by) or not re.search(r"\d{4}-\d{2}-\d{2}", withdrawn_by)):
                violations.append(f"G6 {p.name}: status withdrawn but Withdrawn by names no person and date")
            has_lean = "```lean" in section(d["text"], "Formal Statement")
            has_attempts = any(d["id"] in cs for cs in attempt_conjs.values())
            if has_lean and (has_attempts or status in ("proved", "refuted")):
                if parse_cross_check is None:
                    violations.append(f"G6 {p.name}: cannot check Faithfulness Cross-Check (attest_lean.py not importable)")
                else:
                    cc = parse_cross_check(d["text"])
                    if not cc["ok"]:
                        violations.append(f"G6 {p.name}: Faithfulness Cross-Check incomplete (P13): "
                                          + "; ".join(cc["problems"]))
            plans = conj_plans.get(d["id"], set())
            if not plans:
                violations.append(f"G6 {p.name}: references no RESEARCH-PLAN (cpt-<system>-rplan-<slug>)")
            for pl in plans:
                if pl not in rplan_criteria:
                    violations.append(f"G6 {p.name}: RESEARCH-PLAN {pl} resolves to no artifact")

        if d["kind"] == "PROOF-ATTEMPT":                              # G7
            status = d["fm"].get("status", "")
            if status not in ATTEMPT_STATUS:
                violations.append(f"G7 {p.name}: status `{status}` not in {ATTEMPT_STATUS}")
            if not d["fm"].get("generated-by"):
                violations.append(f"G7 {p.name}: no `generated-by` in frontmatter — PROOF-ATTEMPTs are script-generated")
            conjs = attempt_conjs.get(d["id"], set())
            if not conjs:
                violations.append(f"G7 {p.name}: Conjecture section references no CONJECTURE ID")
            for c in conjs:
                if c not in conj_status:
                    violations.append(f"G7 {p.name}: conjecture {c} resolves to no artifact")
            rows = [l for l in section(d["text"], "Verdict").splitlines() if l.startswith("| `cpt-")]
            row_ids = set()
            for l in rows:
                row_ids.update(re.findall(r"cpt-[a-z0-9]+-criterion-[a-z0-9-]+", l.split("|")[1]))
            for c in conjs:                                               # exactly the plan's rows (P7)
                for pl in conj_plans.get(c, set()):
                    expected = rplan_criteria.get(pl)
                    if expected and row_ids != expected:
                        missing, extra = sorted(expected - row_ids), sorted(row_ids - expected)
                        violations.append(f"G7 {p.name}: Verdict rows are not exactly the criteria of {pl}"
                                          + (f"; missing {missing}" if missing else "")
                                          + (f"; extra {extra}" if extra else ""))
            if status in ("pass", "refuted"):
                bad = [l.split("|")[1].strip() for l in rows if l.rstrip().split("|")[-2].strip() != "pass"]
                if not rows:
                    violations.append(f"G7 {p.name}: status {status} but Verdict has no criterion rows")
                if bad:
                    violations.append(f"G7 {p.name}: status {status} but row(s) not pass: {', '.join(bad)}")
            att = section(d["text"], "Attestation")
            m = re.search(r"Owned-sections SHA-256\*\*: `([0-9a-f]{64})`", att)
            if not m:
                violations.append(f"G7 {p.name}: no owned-sections SHA-256 in Attestation")
            elif owned_sections_hash is None:
                violations.append(f"G7 {p.name}: cannot verify owned-sections hash (attest_lean.py not importable)")
            elif owned_sections_hash(d["text"]) != m.group(1):
                violations.append(f"G7 {p.name}: owned-sections SHA-256 mismatch — script-owned sections or "
                                  f"status were edited after generation; re-run attest_lean.py")

        if d["kind"] == "RESEARCH-PLAN":                              # G8
            if d["fm"].get("status") == "approved":
                appr = section(d["text"], "Approval").strip()
                if is_placeholder(appr):
                    violations.append(f"G8 {p.name}: status approved but Approval section empty/placeholder")
            for line in section(d["text"], "Conjecture Register").splitlines():
                if not line.startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                cids = ids_in(cells[0], "conj")        # the row's conjecture is the ID in the first cell
                if not cids:
                    continue
                row_status = next((c for c in cells if c in CONJ_STATUS), None)
                for c in cids:
                    if c not in conj_status:
                        violations.append(f"G8 {p.name}: register row {c} resolves to no CONJECTURE artifact")
                    elif row_status is None:
                        violations.append(f"G8 {p.name}: register row {c} has no status cell from {CONJ_STATUS}")
                    elif row_status != conj_status[c]:
                        violations.append(f"G8 {p.name}: register says {c} is {row_status} but the CONJECTURE says "
                                          f"{conj_status[c]}")

        if d["kind"] == "CLAIM":                                      # G4
            if d["fm"].get("status") == "certified":
                certs = claim_certs.get(d["id"], [])
                if not certs:
                    violations.append(f"G4 {p.name}: certified but no CERTIFICATE references it")
                elif not any(c in cert_passing for c in certs):
                    violations.append(f"G4 {p.name}: certified but no passing CHECK-RUN for its certificates")

    return violations, len(docs)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    root = Path(args[0])
    if not root.is_dir():
        print(f"error: {root} is not a directory")
        return 2
    violations, n = run_gates(root)
    if "--json" in sys.argv:
        print(json.dumps({"artifacts": n, "violations": violations}, indent=2))
    else:
        print(f"graph_gate: {n} artifacts scanned")
        for v in violations:
            print(f"  FAIL {v}")
        print("graph_gate: " + ("PASS" if not violations else f"{len(violations)} violation(s)"))
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
