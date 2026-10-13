import Euler
/-!
Statement stubs for the CONJECTURE artifacts of the number-theory example pack.
A CONJECTURE's Formal Statement is the `#check` output of its stub, compiled here —
never typed by hand (CONJECTURE rules, rule 2). Build `Euler` first, then:

    lake env lean Stubs.lean
-/
namespace Euler

/-- stub for `cpt-nt-conj-euler-all-prime` -/
theorem conj_euler_all_prime : ∀ n : Nat, isPrime (f n) = true := sorry

/-- stub for `cpt-nt-conj-euler-prime-below-40` -/
theorem conj_euler_prime_below_40 : ∀ n : Nat, n < 40 → isPrime (f n) = true := sorry

/-- stub for `cpt-nt-conj-euler-no-small-prime-factor` -/
theorem conj_euler_no_small_prime_factor :
    ∀ n p : Nat, p < 41 → isPrime p = true → f n % p ≠ 0 := sorry

end Euler

#check @Euler.conj_euler_all_prime
#check @Euler.conj_euler_prime_below_40
#check @Euler.conj_euler_no_small_prime_factor
