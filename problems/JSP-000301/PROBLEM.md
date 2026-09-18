# JSP-000301 · If two consecutive positive integers are powerful, must at least one be a perfect square?

## Catalog entry

- Prize catalog: `problems/catalog-0301-0400.md#JSP-000301` in `TheJustinSunPrize/awards`
- **Current status:** Solved. Proof contributors: Solomon W. Golomb (counterexample in [Go70], 1970).
- **Lean proof:** No
- **Mathematical area:** Number theory / Powerful numbers

## Original statement (verbatim from the catalog)

> If two consecutive positive integers are powerful, must at least one be a
> perfect square?

The answer is **no**. The catalog's own review note (Source review 2026-09-13)
records the resolution:

> Disproved: 12167 = 23³ and 12168 = 2³ × 3² × 13² are consecutive powerful
> numbers, and neither is a perfect square. A powerful number has exponent at
> least two in every prime factor. The displayed factorizations verify this
> property for 12167 and 12168. Both lie strictly between 110² = 12100 and
> 111² = 12321, so neither is a square.

## Definition

An integer `n` is **powerful** when every prime dividing `n` divides it at least
twice: `∀ p, p.Prime → p ∣ n → p ^ 2 ∣ n`.

Mathlib has no `Powerful` predicate, so we define it. This is Golomb's original
definition from [Go70] and the one the catalog's review note uses.

## Sources

| Role | Reference |
| --- | --- |
| Original problem | Erdős, see [Er76d, p.31], [ErGr80, p.68] |
| Complete solution (counterexample) | [Go70] S. W. Golomb, *Powerful numbers*, Amer. Math. Monthly 77(8) (1970), 848-852. <https://doi.org/10.2307/2317020> |
| Related | [Wa76] Walker, *Consecutive integer pairs of powerful numbers...*, Fibonacci Quart. (1976), 111-116 |
| Related | [Gu04] Guy, *Unsolved problems in number theory* (2004) |

## Scope

This record covers **only** the yes/no question above.

It does **not** cover the separate counting question in
[Erdős problem #365](https://www.erdosproblems.com/365) ("is the number of such
`n ≤ x` bounded by `(log x)^{O(1)}`?"), which remains **open**. erdosproblems.com
marks #365 as OPEN for that reason; the prize catalog deliberately splits the two
and marks this half Solved. Our formalization must not claim anything about the
counting question.

## Lean statement (English back-translation)

Filled during Stage 1, then compared against the verbatim statement above.

## Scope notes

- `Powerful 1` holds vacuously. This is standard and harmless here, since our
  witness is 12167.
- The question says "two consecutive **positive** integers", so the statement
  must carry `0 < n`.
- "At least one is a perfect square" is a disjunction, so disproving it requires
  showing **both** 12167 and 12168 are non-squares. Showing only one is not enough.
- We claim the **Lean formalization** role only. The mathematics is Golomb's.
