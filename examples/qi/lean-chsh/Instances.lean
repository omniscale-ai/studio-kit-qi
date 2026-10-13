import Chsh
/-!
Instance agreement for the Faithfulness Cross-Check (principle P13): the Lean
definitions evaluated on the same finite instances as `examples/qi/chsh-enumerate.py`.
If these `#eval` lines disagree with the exploration record, the Lean encoding is
not the informal object, whatever the compiler says about the proofs. Run with

    lake build && lake env lean Instances.lean
-/
namespace Chsh

def strategies : List (Bool × Bool × Bool × Bool) :=
  [true, false].flatMap fun a0 => [true, false].flatMap fun a1 =>
    [true, false].flatMap fun b0 => [true, false].map fun b1 => (a0, a1, b0, b1)

def sortedSet (l : List Int) : List Int := (l.eraseDups).mergeSort fun a b => decide (a ≤ b)

def chshValues : List Int := strategies.map fun (a0, a1, b0, b1) => chsh a0 a1 b0 b1

def valueSet (c00 c01 c10 c11 : Int) : List Int :=
  sortedSet (strategies.map fun (a0, a1, b0, b1) => bell c00 c01 c10 c11 a0 a1 b0 b1)

def patterns : List (Int × Int × Int × Int) :=
  [1, -1].flatMap fun c00 => [1, -1].flatMap fun c01 =>
    [1, -1].flatMap fun c10 => [1, -1].map fun c11 => (c00, c01, c10, c11)

#eval strategies.length                                        -- expect 16
#eval sortedSet chshValues                                     -- expect [-2, 2]
#eval chshValues.foldl max (-100)                              -- expect 2
#eval patterns.map fun (c00, c01, c10, c11) =>
  ((c00, c01, c10, c11), valueSet c00 c01 c10 c11)             -- expect the 16 value sets of the record
#eval bell 1 1 1 1 true true true true                         -- expect 4 (the refuting witness)
#eval (patterns.filter fun (c00, c01, c10, c11) => c00 * c01 * c10 * c11 == -1).all
  fun (c00, c01, c10, c11) => (valueSet c00 c01 c10 c11).all fun v => v == 2 || v == -2
                                                               -- expect true (odd-sign patterns)
#eval sortedSet ((patterns.filter fun (c00, c01, c10, c11) => c00 * c01 * c10 * c11 == 1).flatMap
  fun (c00, c01, c10, c11) => valueSet c00 c01 c10 c11)        -- expect [-4, 0, 4] (even-sign patterns)

end Chsh
