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

Usage:  python3 graph_gate.py <artifacts-root> [--json]
Exit:   0 all gates pass, 1 violations found, 2 usage/parse error.
"""

import json
import re
import sys
from pathlib import Path

STATUS_ORDER = ["open", "cited", "expert-verified", "machine-checked", "formalized"]
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
    for kind in ["CLAIM", "CERTIFICATE", "CHECK-RUN", "THEOREM", "PROOF-MAP", "LEMMA", "VERIFICATION-PLAN"]:
        for p in sorted((root / kind).rglob("*.md")):
            if p.name in ("template.md", "rules.md", "checklist.md"):
                continue
            text = p.read_text(encoding="utf-8")
            own_kind = {"CLAIM": "claim", "CERTIFICATE": "cert", "CHECK-RUN": "run",
                        "THEOREM": "thm", "PROOF-MAP": "pm", "LEMMA": "lem",
                        "VERIFICATION-PLAN": "vplan"}[kind]
            own_ids = ids_in(text, own_kind)
            docs[p] = {"kind": kind, "text": text, "fm": frontmatter(text),
                       "id": own_ids[0] if own_ids else None}
    return docs


def rank(status: str) -> int:
    return STATUS_ORDER.index(status) if status in STATUS_ORDER else -1


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
