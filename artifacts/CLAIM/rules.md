# CLAIM — Generation & Validation Rules

**Dependencies**:
- `{principles}` — cross-cutting invariants P1–P13; load before these rules
- `{claim_template}` — structural reference

---

1. **Exactness.** All data in `Exact Data` MUST be exact — integers, rationals (fractions) or finite symbolic data. A single floating-point literal fails review. If the source states decimals, convert and cite the exact form.
2. **Explicit quantifiers.** The `Statement` MUST make every quantifier explicit. "p is nonlocal" is not a statement; "no triple of response functions and no product latent distribution reproduces p" is.
3. **Finite reduction stated.** If the class in `Model Class` is a priori infinite (unbounded latent alphabets, arbitrary protocols, an infinite family of instances), the section MUST state the reduction that makes checking finite (a cardinality bound with citation, a symmetry argument, a blocklength), or note that no reduction is known — which constrains what a certificate can mean.
4. **Claim ≠ theorem.** A CLAIM is a single checkable statement. If the natural statement decomposes into parts with different verification routes, split into several CLAIMs and group them under a THEOREM (published) or a CONJECTURE (new).
5. **Status discipline.** Frontmatter `status: certified` is allowed ONLY when at least one CERTIFICATE with at least one passing CHECK-RUN references this claim. This is enforced by `scripts/graph_gate.py` G4, not by trust.
6. **One ID per claim.** The `cpt-{system}-claim-{slug}` ID appears under `Statement` and is the anchor all certificates reference.

## Where the principles land in a CLAIM

| Section | Principles |
|---------|------------|
| Statement | P6 one checkable statement at the strength the data supports; P1 the evidence kind is exact |
| Model Class | P2 the decomposition matches the cited literature's convention |
| Exact Data | P1 exact rationals only, no floating point |
| Provenance | P11 informational only |
| Verification | P8 `certified` is derived from a passing CHECK-RUN (`graph_gate` G4), never asserted |
