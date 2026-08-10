# CERTIFICATE — Review Checklist

- [ ] SHA-256 present and matches the referenced file (recompute, don't copy)?
- [ ] Could you implement the checker from `Semantics` alone, without the producer's code?
- [ ] Checking predicate strict where it must be (strict inequality vs ≥ — the difference between a proof and nothing)?
- [ ] Every auxiliary input listed, hashed, and honestly labeled (verified / re-derivable / trusted)?
- [ ] The weakest trust link identified explicitly?
- [ ] Exactness: no tolerance, no epsilon, no floats anywhere in the predicate?
- [ ] Certified claim ID resolves to an existing CLAIM whose Exact Data matches what the certificate actually separates?
- [ ] Status consistent with Check Runs section?
