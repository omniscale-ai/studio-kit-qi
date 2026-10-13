namespace Euler

/-- `hasDivisorFrom n d fuel` is `true` iff some `d' ≥ d` with `d' * d' ≤ n` divides `n`
(searched with `fuel` steps; `fuel = n` is always enough). -/
def hasDivisorFrom (n d : Nat) : Nat → Bool
  | 0 => false
  | fuel + 1 =>
    if d * d > n then false
    else if n % d == 0 then true
    else hasDivisorFrom n (d + 1) fuel

/-- Trial-division primality: `n ≥ 2` and no `d` with `2 ≤ d`, `d * d ≤ n` divides `n`. -/
def isPrime (n : Nat) : Bool := n ≥ 2 && !hasDivisorFrom n 2 n

/-- Euler's prime-generating polynomial `n² + n + 41`. -/
def f (n : Nat) : Nat := n * n + n + 41

theorem not_all_prime : ¬ ∀ n : Nat, isPrime (f n) = true := by
  intro h
  have w := h 40
  revert w
  decide

theorem prime_below_40 : ∀ n : Nat, n < 40 → isPrime (f n) = true := by
  decide

end Euler
