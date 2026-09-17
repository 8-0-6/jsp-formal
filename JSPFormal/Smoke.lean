/-
Copyright (c) 2026 Yanbo Wang. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yanbo Wang
-/
import Mathlib.NumberTheory.Divisors
import Mathlib.Data.Nat.Prime.Infinite
import Mathlib.Combinatorics.Pigeonhole
import Mathlib.Tactic.Ring

/-!
# Environment smoke test

Exercises the four things every real formalization needs: a new definition,
an induction proof, a finite decidable check, and reuse of Mathlib.
-/

namespace JSPFormal

/-- A new definition: `n` is *divisor-rich* if it has more than `k` divisors. -/
def DivisorRich (n k : ℕ) : Prop := k < n.divisors.card

instance (n k : ℕ) : Decidable (DivisorRich n k) := Nat.decLt _ _

/-- Induction: the sum of the first `n` odd numbers is `n ^ 2`. -/
theorem sum_odds (n : ℕ) : ∑ i ∈ Finset.range n, (2 * i + 1) = n ^ 2 := by
  induction n with
  | zero => simp
  | succ m ih => rw [Finset.sum_range_succ, ih]; ring

/-- Finite decidable check: 12 has more than 5 divisors. -/
theorem twelve_divisor_rich : DivisorRich 12 5 := by decide

/-- Pigeonhole, reusing `Finset.exists_ne_map_eq_of_card_lt_of_maps_to`. -/
theorem pigeonhole {n : ℕ} (s : Finset ℕ) (hs : n < s.card)
    (f : ℕ → ℕ) (hf : ∀ a ∈ s, f a ∈ Finset.range n) :
    ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ f x = f y := by
  have h : (Finset.range n).card < s.card := by simpa using hs
  exact Finset.exists_ne_map_eq_of_card_lt_of_maps_to h hf

/-- Reuse of a deep Mathlib result: there are infinitely many primes. -/
theorem infinitely_many_primes : ∀ N, ∃ p, N ≤ p ∧ Nat.Prime p :=
  Nat.exists_infinite_primes

end JSPFormal
