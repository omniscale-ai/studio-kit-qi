import Chsh
/-!
Statement stubs for the CONJECTURE artifacts of the kit's discovery-layer example.
A CONJECTURE's Formal Statement is the `#check` output of its stub, compiled here —
never typed by hand (CONJECTURE rules, rule 2). Build `Chsh` first, then:

    lake env lean Stubs.lean
-/
namespace Chsh

/-- stub for `cpt-qi-conj-chsh-det-bound` -/
theorem conj_chsh_det_bound (a0 a1 b0 b1 : Bool) : chsh a0 a1 b0 b1 ≤ 2 := sorry

/-- stub for `cpt-qi-conj-bell-pm-coeff-values` -/
theorem conj_bell_pm_coeff_values :
    ∀ c00 c01 c10 c11 : Int,
      (c00 = 1 ∨ c00 = -1) → (c01 = 1 ∨ c01 = -1) →
      (c10 = 1 ∨ c10 = -1) → (c11 = 1 ∨ c11 = -1) →
      ∀ a0 a1 b0 b1 : Bool,
        bell c00 c01 c10 c11 a0 a1 b0 b1 = 2 ∨ bell c00 c01 c10 c11 a0 a1 b0 b1 = -2 := sorry

/-- stub for `cpt-qi-conj-bell-odd-sign-values` -/
theorem conj_bell_odd_sign_values :
    ∀ c00 c01 c10 c11 : Int,
      (c00 = 1 ∨ c00 = -1) → (c01 = 1 ∨ c01 = -1) →
      (c10 = 1 ∨ c10 = -1) → (c11 = 1 ∨ c11 = -1) →
      c00 * c01 * c10 * c11 = -1 →
      ∀ a0 a1 b0 b1 : Bool,
        bell c00 c01 c10 c11 a0 a1 b0 b1 = 2 ∨ bell c00 c01 c10 c11 a0 a1 b0 b1 = -2 := sorry

end Chsh

#check @Chsh.conj_chsh_det_bound
#check @Chsh.conj_bell_pm_coeff_values
#check @Chsh.conj_bell_odd_sign_values
