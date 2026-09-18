/-
Copyright (c) 2026 Yanbo Wang. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yanbo Wang
-/
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Algebra.Group.Even
import Mathlib.Tactic

/-!
# JSP-000301

*If two consecutive positive integers are powerful, must at least one be a
perfect square?*

The answer is **no**, by the counterexample `12167 = 23³` and
`12168 = 2³ · 3² · 13²`: both are powerful and neither is a perfect square.

Attribution, verified against <https://www.erdosproblems.com/latex/365>, which
states: "The answer to the first question is no: Golomb [Go70] observed that both
12167 = 23³ and 12168 = 2³3²13² are powerful." We have not independently read
[Go70]; we record the attribution as that source gives it. We claim only the Lean
formalization, not the mathematics.

This file formalizes only that yes/no question. It says nothing about the
separate counting question of Erdős problem #365, which remains open.

## References
* [Go70] S. W. Golomb, *Powerful numbers*, Amer. Math. Monthly 77 (1970), 848-855.
* Attribution source: <https://www.erdosproblems.com/latex/365>
-/

namespace JSPFormal.JSP000301

/-- A natural number is **powerful** when every prime dividing it divides it at
least twice. This is Golomb's definition. -/
def Powerful (n : ℕ) : Prop := ∀ p : ℕ, p.Prime → p ∣ n → p ^ 2 ∣ n

/-- A number strictly between two consecutive squares is not a square. -/
theorem not_isSquare_of_between {n a : ℕ} (h₁ : a * a < n) (h₂ : n < (a + 1) * (a + 1)) :
    ¬ IsSquare n := by
  rintro ⟨r, rfl⟩
  have hlt : a < r := by
    by_contra h
    exact absurd h₁ (not_lt.2 (Nat.mul_le_mul (not_lt.1 h) (not_lt.1 h)))
  have hgt : r < a + 1 := by
    by_contra h
    exact absurd h₂ (not_lt.2 (Nat.mul_le_mul (not_lt.1 h) (not_lt.1 h)))
  omega

theorem powerful_12167 : Powerful 12167 := by
  intro p hp hdvd
  have h : (12167 : ℕ) = 23 ^ 3 := by norm_num
  rw [h] at hdvd ⊢
  have hp23 : p = 23 :=
    (Nat.prime_dvd_prime_iff_eq hp (by norm_num)).mp (hp.dvd_of_dvd_pow hdvd)
  subst hp23
  exact pow_dvd_pow 23 (by norm_num)

theorem powerful_12168 : Powerful 12168 := by
  intro p hp hdvd
  have h : (12168 : ℕ) = 2 ^ 3 * (3 ^ 2 * 13 ^ 2) := by norm_num
  rw [h] at hdvd ⊢
  rcases (Nat.Prime.dvd_mul hp).mp hdvd with h2 | hrest
  · have : p = 2 := (Nat.prime_dvd_prime_iff_eq hp Nat.prime_two).mp (hp.dvd_of_dvd_pow h2)
    subst this; norm_num
  · rcases (Nat.Prime.dvd_mul hp).mp hrest with h3 | h13
    · have : p = 3 := (Nat.prime_dvd_prime_iff_eq hp Nat.prime_three).mp (hp.dvd_of_dvd_pow h3)
      subst this; norm_num
    · have : p = 13 := (Nat.prime_dvd_prime_iff_eq hp (by norm_num)).mp (hp.dvd_of_dvd_pow h13)
      subst this; norm_num

theorem not_isSquare_12167 : ¬ IsSquare (12167 : ℕ) :=
  not_isSquare_of_between (a := 110) (by norm_num) (by norm_num)

theorem not_isSquare_12168 : ¬ IsSquare (12168 : ℕ) :=
  not_isSquare_of_between (a := 110) (by norm_num) (by norm_num)

/-! ### Sanity checks on the definition

`Powerful` is the one piece of this formalization that is our own wording rather
than the catalog's, so it is the place a silent error would hide. A definition
that were accidentally trivial (always true) would make `answer_is_no` provable
and meaningless. These checks show it genuinely discriminates. -/

/-- **Independent cross-validation of the definition.**

`google-deepmind/formal-conjectures` formalizes powerful numbers as
`Nat.Full 2`, namely `∀ p ∈ n.primeFactors, p ^ 2 ∣ n`
(`FormalConjecturesForMathlib/Data/Nat/Full.lean`). That is a separately written,
publicly reviewed formalization of the same notion, so agreeing with it is real
evidence that our wording is right rather than merely self-consistent.

The two agree for every `n`, including `n = 0`, where both hold: ours because
`p ^ 2 ∣ 0`, theirs because `(0 : ℕ).primeFactors = ∅`. -/
theorem powerful_iff_primeFactors (n : ℕ) :
    Powerful n ↔ ∀ p ∈ n.primeFactors, p ^ 2 ∣ n := by
  constructor
  · intro h p hp
    rw [Nat.mem_primeFactors] at hp
    exact h p hp.1 hp.2.1
  · intro h p hp hdvd
    rcases eq_or_ne n 0 with rfl | hn
    · exact dvd_zero _
    · exact h p (Nat.mem_primeFactors.mpr ⟨hp, hdvd, hn⟩)

/-- 12 = 2² · 3 is **not** powerful: 3 divides it but 9 does not. -/
theorem not_powerful_12 : ¬ Powerful 12 := by
  intro h
  have := h 3 (by norm_num) (by norm_num)
  norm_num at this

/-- 2 is not powerful. -/
theorem not_powerful_2 : ¬ Powerful 2 := by
  intro h
  have := h 2 Nat.prime_two (by norm_num)
  norm_num at this

/-- Sanity: `IsSquare` is actually satisfiable. Without this, a degenerate
`IsSquare` would make every `¬ IsSquare` conjunct free and the counterexample
would say far less than it appears to. -/
theorem isSquare_sq (a : ℕ) : IsSquare (a * a) := ⟨a, rfl⟩

/-- Sanity: a concrete square, and one adjacent to a powerful number. -/
theorem isSquare_9 : IsSquare (9 : ℕ) := ⟨3, by norm_num⟩

/-- Sanity: `Powerful 0` holds under this definition, because `p ^ 2 ∣ 0` for
every `p`.

The `0 < n` hypothesis is load-bearing in `exists_consecutive_powerful`: without
it, `n = 0` would be a free witness there. It is **not** needed for
`answer_is_no`, since `IsSquare 0` holds and so `n = 0` satisfies that
conclusion anyway. The guard is kept on both for faithfulness to the catalog's
wording ("two consecutive **positive** integers"), not because the main theorem
requires it. -/
theorem powerful_zero : Powerful 0 := fun p _ _ => dvd_zero (p ^ 2)

/-- A perfect square is powerful, so the two notions are not accidentally disjoint. -/
theorem powerful_sq (a : ℕ) : Powerful (a * a) := by
  intro p hp hdvd
  have h : p ∣ a := ((Nat.Prime.dvd_mul hp).mp hdvd).elim id id
  rw [pow_two]
  exact mul_dvd_mul h h

/-- **Vacuity witness.** Consecutive powerful pairs exist at all, so the question
is not vacuous: `8 = 2³` and `9 = 3²` are both powerful. -/
theorem exists_consecutive_powerful : ∃ n : ℕ, 0 < n ∧ Powerful n ∧ Powerful (n + 1) := by
  refine ⟨8, by norm_num, ?_, ?_⟩
  · intro p hp hdvd
    have h : (8 : ℕ) = 2 ^ 3 := by norm_num
    rw [h] at hdvd ⊢
    have : p = 2 := (Nat.prime_dvd_prime_iff_eq hp Nat.prime_two).mp (hp.dvd_of_dvd_pow hdvd)
    subst this; norm_num
  · intro p hp hdvd
    have h : (8 + 1 : ℕ) = 3 ^ 2 := by norm_num
    rw [h] at hdvd ⊢
    have : p = 3 := (Nat.prime_dvd_prime_iff_eq hp Nat.prime_three).mp (hp.dvd_of_dvd_pow hdvd)
    subst this; norm_num

/-- **Golomb's counterexample.** There are consecutive positive powerful integers
of which neither is a perfect square. -/
theorem exists_consecutive_powerful_neither_square :
    ∃ n : ℕ, 0 < n ∧ Powerful n ∧ Powerful (n + 1) ∧ ¬ IsSquare n ∧ ¬ IsSquare (n + 1) :=
  ⟨12167, by norm_num, powerful_12167, powerful_12168, not_isSquare_12167, not_isSquare_12168⟩

/-- **Main result.** The answer to JSP-000301 is *no*: it is not the case that
whenever two consecutive positive integers are powerful, at least one of them is
a perfect square. -/
theorem answer_is_no :
    ¬ ∀ n : ℕ, 0 < n → Powerful n → Powerful (n + 1) → IsSquare n ∨ IsSquare (n + 1) := by
  intro h
  obtain ⟨n, hn, hp, hp', hs, hs'⟩ := exists_consecutive_powerful_neither_square
  rcases h n hn hp hp' with hsq | hsq
  · exact hs hsq
  · exact hs' hsq

end JSPFormal.JSP000301
