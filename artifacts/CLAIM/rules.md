# CLAIM — Generation & Validation Rules

1. **Exactness.** All numerical data in `Exact Data` MUST be exact rationals (fractions or integers). A single floating-point literal fails review. If the source paper states decimals, convert and cite the exact form.
2. **Explicit quantifiers.** The `Statement` MUST make every quantifier explicit. "p is nonlocal" is not a statement; "no triple of response functions and no product latent distribution reproduces p" is.
3. **Finite reduction stated.** If the excluded model class is a priori infinite-dimensional (unbounded latent alphabets, arbitrary protocols), `Model Class` MUST state the reduction that makes checking finite (cardinality bound with citation, or note that no reduction is known — which constrains what a certificate can mean).
4. **Claim ≠ theorem.** A CLAIM is a single checkable statement. If the natural statement decomposes into parts with different verification routes, split into several CLAIMs (future: group under a THEOREM).
5. **Status discipline.** Frontmatter `status: certified` is allowed ONLY when at least one CERTIFICATE with at least one passing CHECK-RUN references this claim. This is enforced by `scripts/graph_gate.py` (planned), not by trust.
6. **One ID per claim.** The `cpt-{system}-claim-{slug}` ID appears under `Statement` and is the anchor all certificates reference.
