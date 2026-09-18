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
| Complete solution (counterexample) | [Go70] S. W. Golomb, *Powerful numbers*, Amer. Math. Monthly 77 (1970), **848-855**. <https://doi.org/10.2307/2317020> |
| Attribution source (verified) | <https://www.erdosproblems.com/latex/365> |
| Related | [Wa76] Walker, *Consecutive integer pairs of powerful numbers...*, Fibonacci Quart. (1976), 111-116 |
| Related | [Gu04] Guy, *Unsolved problems in number theory* (2004) |

## Attribution, and what we have actually verified

The prize catalog credits Golomb. We checked the source it cites,
<https://www.erdosproblems.com/latex/365>, which states verbatim:

> "The answer to the first question is no: Golomb [Go70] observed that both
> 12167 = 23³ and 12168 = 2³3²13² are powerful. Walker [Wa76] proved that the
> equation 7³x² = 3³y² + 1 has infinitely many solutions, giving infinitely many
> counterexamples."

Two honest limits on this:

1. **We have not read [Go70] itself.** It is paywalled. We record the attribution
   as the cited source gives it, and we do not assert a page or theorem number
   inside that paper. If a reviewer requires the primary source, that is the gap.
2. Note the page range differs between sources: the prize catalog says 848-852,
   erdosproblems.com says 848-855. We follow the latter and flag the discrepancy.

**We claim the Lean formalization role only.** The mathematics is Golomb's, and
nothing in our submission should be read as claiming otherwise.

## Scope

This record covers **only** the yes/no question above.

It does **not** cover the separate counting question in
[Erdős problem #365](https://www.erdosproblems.com/365).

Erdős #365 bundles two questions, and the distinction matters, so here is the
evidence rather than an inference. Its source text reads:

> "Do all pairs of consecutive powerful numbers `n` and `n+1` come from solutions
> to Pell equations? In other words, must either `n` or `n+1` be a square?
> **Is the number of such `n ≤ x` bounded by `(log x)^{O(1)}`?**"

and then: "**The answer to the first question is no**: Golomb [Go70] observed
that both 12167 = 23³ and 12168 = 2³3²13² are powerful."

So the first clause is settled and the counting clause is not. The site marks
#365 OPEN on account of the counting clause; the prize catalog splits the two and
marks this half Solved. Our formalization covers the settled clause only and says
nothing about counting, density, or asymptotics anywhere.

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
