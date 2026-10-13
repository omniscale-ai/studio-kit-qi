import Euler
/-!
Instance agreement for the Faithfulness Cross-Check (principle P13): the Lean
definitions evaluated on the same finite instances as `examples/euler-polynomial/enumerate.py`.
Run with

    lake build && lake env lean Instances.lean
-/
namespace Euler

#eval (List.range 100).filter fun n => !isPrime (f n)       -- n < 100 with n² + n + 41 composite
#eval (List.range 40).all fun n => isPrime (f n)            -- expect true: prime for every n < 40
#eval f 40                                                  -- expect 1681
#eval 41 * 41                                               -- expect 1681 — the witness factors
#eval (List.range 41).filter isPrime                        -- the primes below 41
#eval ((List.range 41).filter isPrime).all fun p =>
  (List.range 10000).all fun n => f n % p != 0              -- expect true: no prime below 41 divides f n (n < 10000)
#eval (List.range 100).filter fun n => isPrime n && n != 41 && f 40 % n == 0   -- expect []: 1681's only prime factor is 41

end Euler
