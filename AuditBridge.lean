/-
Audit bridge for the `lean-verify` pre-submission self-check of JSP-000301.

This file is NOT part of the submission. It exists only on the audit branch
`audit/lean-verify-3ece478`, which is the submitted commit
`3ece478053a97a80aad5b1628bc3e830cde115d6` plus this file and one extra CI
workflow. No submitted file is modified.

Purpose: restate the JSP-000301 question from the catalog wording using notions
written independently of the submission, then check that the submitted theorem
implies that independent statement. This tests the one thing a build cannot
test, namely whether the Lean statement means what the catalog asks.
-/
import JSPFormal.JSP000301.Statement

namespace JSP000301Audit

/-- "Powerful", restated by prime-factorisation exponent rather than by the
submission's divisibility wording. -/
def PowerfulExp (n : ℕ) : Prop := ∀ p : ℕ, p.Prime → p ∣ n → 2 ≤ n.factorization p

/-- "Perfect square", restated without Mathlib's `IsSquare`. -/
def IsSquareE (n : ℕ) : Prop := ∃ a : ℕ, n = a * a

/-- The intended reading of the catalog question: "If two consecutive positive
integers are powerful, must at least one be a perfect square?", answered no. -/
def IntendedStatement : Prop :=
  ¬ ∀ n : ℕ, 0 < n → PowerfulExp n → PowerfulExp (n + 1) →
      IsSquareE n ∨ IsSquareE (n + 1)

theorem powerful_to_exp {n : ℕ} (hn : n ≠ 0) (h : JSPFormal.JSP000301.Powerful n) :
    PowerfulExp n := fun p hp hdvd =>
  (Nat.Prime.pow_dvd_iff_le_factorization hp hn).mp (h p hp hdvd)

theorem exp_to_powerful {n : ℕ} (hn : n ≠ 0) (h : PowerfulExp n) :
    JSPFormal.JSP000301.Powerful n := fun p hp hdvd =>
  (Nat.Prime.pow_dvd_iff_le_factorization hp hn).mpr (h p hp hdvd)

/-- The submission's `Powerful` and this file's independent `PowerfulExp` agree
on every positive `n`. -/
theorem powerful_iff_exp {n : ℕ} (hn : n ≠ 0) :
    JSPFormal.JSP000301.Powerful n ↔ PowerfulExp n :=
  ⟨powerful_to_exp hn, exp_to_powerful hn⟩

theorem isSquareE_to_isSquare {n : ℕ} (h : IsSquareE n) : IsSquare n :=
  h.elim fun a ha => ⟨a, ha⟩

theorem isSquare_to_isSquareE {n : ℕ} (h : IsSquare n) : IsSquareE n :=
  h.elim fun a ha => ⟨a, ha⟩

/-- Arithmetic of the counterexample, rechecked here rather than trusted. -/
theorem counterexample_arithmetic :
    (12167 : ℕ) = 23 ^ 3 ∧ (12168 : ℕ) = 2 ^ 3 * 3 ^ 2 * 13 ^ 2 ∧
      110 * 110 < 12167 ∧ (12168 : ℕ) < 111 * 111 ∧ 12168 = 12167 + 1 := by
  norm_num

theorem primes_used : Nat.Prime 2 ∧ Nat.Prime 3 ∧ Nat.Prime 13 ∧ Nat.Prime 23 := by
  norm_num

/-- **The bridge.** The submitted theorem `answer_is_no` implies the
independently written `IntendedStatement`. -/
theorem submission_implies_intended : IntendedStatement := by
  intro h
  apply JSPFormal.JSP000301.answer_is_no
  intro n hn hp hp'
  rcases h n hn (powerful_to_exp hn.ne' hp) (powerful_to_exp (by omega) hp') with hs | hs
  · exact Or.inl (isSquareE_to_isSquare hs)
  · exact Or.inr (isSquareE_to_isSquare hs)

example : IntendedStatement := submission_implies_intended

end JSP000301Audit

#check @JSPFormal.JSP000301.answer_is_no
#print JSPFormal.JSP000301.Powerful
#print axioms JSP000301Audit.submission_implies_intended
#print axioms JSP000301Audit.powerful_iff_exp
#print axioms JSP000301Audit.counterexample_arithmetic
#print axioms JSP000301Audit.primes_used
