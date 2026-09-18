# Triage (Stage 0 output)

**Run:** 2026-09-17. **Method:** `.claude/skills/scout/SKILL.md`.

## Headline

**The trivially easy wins are gone.** Of 577 solved Erdős problems, 298 already
have a verified Lean proof. The 279 that remain are the hard tail, and the
shortness of a problem's *statement* has almost no relationship to the cost of
its *proof*.

"Fastest plausible win" therefore means weeks on a 5 to 15 page paper, not days.
Anyone promising less has not looked at the actual papers.

## What was measured

Crawled all 1,249 problem pages at erdosproblems.com (1,169 with a parseable
status) and cross-referenced `google-deepmind/formal-conjectures` and the Justin
Sun Prize catalog.

| Slice | Count |
| --- | --- |
| Erdős problems with a status | 1,169 |
| Open | 592 |
| Solved | 577 |
| ...already Lean-verified | 298 |
| **...solved, NOT yet Lean-verified** | **279** |
| ...of those, with a ready-made Lean statement in formal-conjectures | 41 |
| ...of those, not even stated in Lean yet | 238 |

## Three findings that changed the plan

**1. erdosproblems.com is the authority on Lean status, not formal-conjectures.**
formal-conjectures lags it. Problems #175, #250 and #48 still carry `sorry`
there while the site already marks them `PROVED (LEAN)`. Any target must be
checked against the site, not the repo, or we will duplicate finished work.

**2. Short statement does not mean short proof.** Erdős #402 (`gcd(a,b) ≤ a/|A|`
for any finite `A ⊂ ℕ`) has a beautiful one-line statement. The complete proof
is Balasubramanian and Soundararajan, Acta Arith. 1996, **38 pages**. Erdős #109
is one line and is the Erdős sumset conjecture, Annals 2019. The useful signal is
the page span of the solving paper, which the catalogs record.

**3. Mathlib has no Ramsey theory.** `find Mathlib -iname '*amsey*'` returns
nothing. Since the short-paper end of the remaining pool is dominated by Ramsey
and extremal graph theory, those problems carry a hidden cost: we would build the
foundational API before touching the actual proof. This dominates the page count.

## Shortlist

Three candidates, each confirmed **Solved** with **no Lean proof** in the prize
catalog, and confirmed not Lean-verified on erdosproblems.com.

### 1. JSP-000787 · Erdős #946 · consecutive integers with equal divisor counts

> There are infinitely many `n` such that `τ(n) = τ(n+1)`.

- **Solving paper:** Heath-Brown 1984, 15 pages.
- **For:** the statement is honest, self-contained, and purely number-theoretic.
  Mathlib is strongest here, and already has the divisor-counting function as
  `σ 0`. No exotic machinery is needed to *state* it.
- **Against:** an infinitude result proved by analytic methods. Formalizing the
  analytic core is the whole job.
- **Verdict:** best balance of Mathlib coverage and paper length. Deep-dive first.

### 2. JSP-000320 · Erdős #387 · binomial coefficient divisors

> Is there `c > 0` such that for all `1 ≤ k < n`, `C(n,k)` has a divisor in `(cn, n]`?

- **Solving paper:** Bui, Naprienko, Pratt, Zaharescu 2026, 7 pages. Answered **negatively**.
- **For:** short and very recent paper, pure number theory, Mathlib-friendly types.
  Disproofs need a construction rather than a universal argument.
- **Against:** the disproof is an infinite family, not a single counterexample, so
  it is not the cheap kind of disproof. The formal-conjectures file also leans on
  `native_decide`, which our rules ban, so any borrowed reasoning must be redone.
- **Verdict:** worth a deep-dive, second.

### 3. JSP-000657 · Erdős #800 · linear Ramsey numbers for subdivided graphs

> If `G` has no two adjacent vertices of degree `≥ 3` then `R(G) ≪ n`.

- **Solving paper:** Alon 1994, **5 pages**, the shortest in the whole pool.
- **For:** shortest known proof of any remaining candidate. Statement already
  written in formal-conjectures.
- **Against:** Mathlib has no Ramsey number at all, so we build that API first.
  Alon's argument is probabilistic, which is expensive to formalize.
- **Verdict:** the page count is misleading. Third.

## Rejected, with reasons

| Problem | Why |
| --- | --- |
| #402 Graham's gcd conjecture | 38-page complete proof |
| #109 Erdős sumset conjecture | Annals 2019, ergodic theory |
| #4, #45 prime gaps | Maynard-Tao territory, $10,000 Erdős prize |
| #67 Erdős discrepancy | Tao, $500 prize |
| #591 ordinal Ramsey | Mathlib's ordinal support is thin |
| #166, #986 Ramsey lower bounds | 25 pages, heavily asymptotic |
| #399 factorial counterexample | already proved, and taken |
| Anything asymptotic | `o(1)`, density, "sufficiently large" all multiply cost |

## What the scoring got wrong, and what to keep

Three scoring passes, each corrected by evidence:

1. Statement length. Useless. Correlates with fame, not difficulty.
2. Question form and keywords. Weakly useful as a prefilter only.
3. **Solving-paper page span plus Mathlib coverage of the prerequisites.** This is
   the signal that survived. Keep it, and always check Mathlib for the required
   machinery before trusting a page count.

The Erdős bounty is a real signal where present, since Erdős priced by
difficulty, but only 18 of 287 catalog entries carry one.

## Next step

Deep-dive the top two: read Heath-Brown 1984 and BNPZ 2026, and produce a genuine
blueprint estimate for each, including which Mathlib pieces exist. Only then pick.

Budget this at 4 hours. If neither yields a plan under 40 hours, the honest move
is to widen to the non-Erdős part of the prize catalog rather than force one.
