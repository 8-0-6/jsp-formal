# Next candidates

Generated during the JSP-000301 round. The pattern that made JSP-000301 cheap:
**a yes/no question answered NO by a small explicit object**, where the whole
proof is "exhibit it and check finitely many facts".

Candidates below are solved, not Lean-verified on erdosproblems.com, and their
blurbs name concrete numbers. None has been deep-dived yet, and the lesson from
the first triage stands: **a promising blurb is not a cheap proof.** Verify the
actual resolution before committing.

| Erdős # | Site status | Why it looked cheap | Caveat |
| --- | --- | --- | --- |
| 1140 | DISPROVED | "infinitely many n with n - 2x² prime for all 2x² < n"; small witnesses 13, 31, 61, 181, 199 | Disproving *infinitude* is not the same as exhibiting one counterexample. Likely needs covering congruences. |
| 441 | DISPROVED | largest A ⊆ {1..N} with lcm(a,b) ≤ N; numbers 87, 134, 183 | Extremal, may be asymptotic |
| 1198 | DISPROVED | 2-colouring of ℕ, infinite product-sum set | Ramsey-flavoured |
| 549 | DISPROVED | R(T) = 4k-1 is false | Needs Ramsey API, which Mathlib lacks |
| 651 | DISPROVED | convex polyhedra from points in general position | Geometry, Mathlib thin |
| 705 | DISPROVED | finite unit-distance graph in ℝ² | Geometry |

## How to screen the next one

1. Read the erdosproblems.com page and find what the resolution actually *is*.
2. Reject anything whose negative answer is about infinitude, density, or
   asymptotics. Those need a real argument, not a witness.
3. Accept only when the resolution is a finite object plus finitely many checks.
4. Before committing, confirm the site does **not** mark it `(LEAN)`, and that a
   matching prize-catalog entry exists with **Lean proof: No**.

## Reusable data

- `research/triage/erdos-status.json`: status for all 1,249 problems
- `research/triage/crawl-erdos.py`: regenerates it
