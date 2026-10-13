/-!
# CHSH in the (2,2,2) Bell scenario — deterministic strategies

A deterministic strategy assigns to each of Alice's two settings an outcome
`a0 a1 : Bool` and to each of Bob's two settings `b0 b1 : Bool`, encoded as ±1.
-/

namespace Chsh

/-- Outcome encoding: `true ↦ 1`, `false ↦ -1`. -/
def pm (b : Bool) : Int := if b then 1 else -1

/-- The CHSH expression `E00 + E01 + E10 − E11` on a deterministic strategy. -/
def chsh (a0 a1 b0 b1 : Bool) : Int :=
  pm a0 * pm b0 + pm a0 * pm b1 + pm a1 * pm b0 - pm a1 * pm b1

/-- A general correlator expression with integer coefficients. -/
def bell (c00 c01 c10 c11 : Int) (a0 a1 b0 b1 : Bool) : Int :=
  c00 * pm a0 * pm b0 + c01 * pm a0 * pm b1 + c10 * pm a1 * pm b0 + c11 * pm a1 * pm b1

/-- **Conjecture C1 (proved).** Every deterministic strategy has CHSH value ≤ 2. -/
theorem chsh_det_le_two (a0 a1 b0 b1 : Bool) : chsh a0 a1 b0 b1 ≤ 2 := by
  cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide

/-- **Conjecture C2 (refuted).** The over-generalisation "every ±1-coefficient
correlator expression takes only the values ±2 on deterministic strategies"
is false: the witness `c = (1,1,1,1)` on the all-`true` strategy evaluates to 4. -/
theorem not_bell_pm_one_in_pm_two :
    ¬ ∀ c00 c01 c10 c11 : Int,
        (c00 = 1 ∨ c00 = -1) → (c01 = 1 ∨ c01 = -1) →
        (c10 = 1 ∨ c10 = -1) → (c11 = 1 ∨ c11 = -1) →
        ∀ a0 a1 b0 b1 : Bool,
          bell c00 c01 c10 c11 a0 a1 b0 b1 = 2 ∨ bell c00 c01 c10 c11 a0 a1 b0 b1 = -2 := by
  intro h
  have w := h 1 1 1 1 (Or.inl rfl) (Or.inl rfl) (Or.inl rfl) (Or.inl rfl) true true true true
  revert w
  decide

end Chsh
