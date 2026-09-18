import Mathlib.Tactic
import Mathlib.Data.Nat.Prime.Basic

-- Non-squareness from tight bounds: a^2 < n < (a+1)^2  =>  n is not a square.
example {n a : ℕ} (h1 : a * a < n) (h2 : n < (a + 1) * (a + 1)) : ¬ IsSquare n := by
  rintro ⟨r, rfl⟩
  have hlt : a < r := by
    by_contra h
    exact absurd h1 (not_lt.2 (Nat.mul_le_mul (not_lt.1 h) (not_lt.1 h)))
  have hgt : r < a + 1 := by
    by_contra h
    exact absurd h2 (not_lt.2 (Nat.mul_le_mul (not_lt.1 h) (not_lt.1 h)))
  omega

-- Powerful for a prime power: p ∣ 23^3 → p = 23
example (p : ℕ) (hp : p.Prime) (h : p ∣ 23 ^ 3) : p = 23 :=
  (Nat.prime_dvd_prime_iff_eq hp (by norm_num)).mp (hp.dvd_of_dvd_pow h)
