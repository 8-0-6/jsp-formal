# Next candidates

Second screening round, run 2026-09-17 after JSP-000301 was submitted.

## Conclusion first

**The counterexample-shaped opportunity is close to exhausted.** JSP-000301 was
nearly unique: a yes/no question answered no by a single finite object whose
properties are decidable arithmetic. A strict screen over the whole pool produced
no second instance.

The realistic next target is a **short but genuine theorem**, not another free
witness. That is a 20 to 40 hour project, not a 3 hour one.

## What was screened

**279 Erdős problems** marked solved on erdosproblems.com and not `(LEAN)`.
Strict filter: the resolution must name a concrete finite object, and the question
itself must not be infinitary (no "infinitely many", density, asymptotics, logs).
**8 survived. All 8 failed on inspection:**

| # | Why it failed |
| --- | --- |
| 1140 | "Not infinitely many" needs Epure-Gica plus Mollin-Williams on class-number-one real quadratic fields, and still leaves "at most one exception" |
| 441 | Pure asymptotics, `g(N) ~ (9N/8)^½` |
| 1198 | Counterexample is a 2-colouring of all of ℕ, an infinite object |
| 1006 | Real resolution is Nešetřil-Rödl building a graph for *every* girth; the Grötzsch graph only covers girth 4, and the question asks girth > 4 |
| 387 | The explicit counterexample (n=99215, k=15) settles a *historical sub-question*. The catalog entry JSP-000320 cites BNPZ 2026, the 62-page sieve paper, so that is what "Solved" refers to |
| 1046 | Complex analysis, `{z : |f(z)| < 1}` |
| 587, 816, 133, 518, 894 | Asymptotic or infinitary on inspection |

**186 non-Erdős catalog entries.** Ranked by shortest cited paper. JSP-000301
appears at 6pg, which validates the ranking. Nothing above it is a counterexample.

## The two most tractable real theorems

### JSP-000584 · every 4-regular graph plus an edge contains a 3-regular subgraph

- [AFK84] J. Combin. Theory Ser. B (1984), **92-93**, and [Ta82] Soviet Math. Dokl.
  (1982), **37-38**. Two 2-page papers, the shortest in the entire pool.
- **For:** genuinely short published proofs.
- **Against:** a universal statement, not a witness, so there is a real argument to
  formalize. Mathlib's `SimpleGraph` API for regular subgraphs is thin, so expect
  to build supporting lemmas.
- **Estimate:** 20 to 40 hours. Within the 40-hour budget, but only just.

### JSP-000878 · finitely many `n! + 1` supported on the next two primes

- [Lu01] Luca, Math. Comp. (2001), 893-896. 4 pages.
- **Against:** a finiteness result. Those usually rest on effective methods
  (Baker-type bounds) plus computation, which is expensive to formalize.
- **Estimate:** unknown, likely worse than it looks.

## Screening rule, unchanged and validated

1. Read the erdosproblems.com page and find what the resolution actually *is*.
2. Reject anything whose answer concerns infinitude, density, or asymptotics.
3. Accept a free win only when the resolution is a finite object plus finitely
   many decidable checks.
4. Otherwise treat it as a real project and estimate honestly.
5. Confirm the site does **not** mark it `(LEAN)`, and that a catalog entry exists
   with **Lean proof: No**.
6. **Check what the catalog entry's references actually are.** JSP-000320 looked
   cheap until its reference list showed the 62-page paper.

## Reusable data

- `research/triage/erdos-status.json`: status for all 1,249 problems
- `research/triage/crawl-erdos.py`: regenerates it
