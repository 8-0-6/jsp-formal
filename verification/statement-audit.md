# Statement and completeness audit, JSP-000301

Catalog question, quoted from
`problems/catalog-0301-0400.md#JSP-000301` at awards commit `bcf1866`:

> If two consecutive positive integers are powerful, must at least one be a
> perfect square?

Catalog review note, same entry, dated 2026-09-13:

> Disproved: 12167 = 23³ and 12168 = 2³ × 3² × 13² are consecutive powerful
> numbers, and neither is a perfect square. A powerful number has exponent at
> least two in every prime factor. [...] Both lie strictly between 110² = 12100
> and 111² = 12321, so neither is a square. This disproves the stated yes/no
> question. This record covers that question only, not the separate counting
> question in Erdős problem #365.

## Requirement enumeration

Requirements were enumerated from the catalog wording before reading the Lean
formulation. The question is a yes/no question whose recorded answer is "no", so
the obligation is a refutation, not a theorem.

| # | Original requirement | Where it comes from |
| --- | --- | --- |
| R1 | "Powerful" means every prime dividing n divides it at least twice | catalog review note, "exponent at least two in every prime factor" |
| R2 | The integers are consecutive and positive: n and n+1, 0 < n | "two consecutive positive integers" |
| R3 | Both members of the pair are powerful | "if two consecutive positive integers are powerful" |
| R4 | Neither member is a perfect square | "must at least one be a perfect square?" answered no |
| R5 | The yes/no question is answered: the universal claim is refuted | the question form itself |
| R6 | Scope is this question only, not the counting question of Erdős #365 | catalog review note, final sentence |

## Coverage matrix

| Req | Lean declaration | Correspondence | Evidence | Gap |
| --- | --- | --- | --- | --- |
| R1 | `Powerful (n : ℕ) : Prop := ∀ p : ℕ, p.Prime → p ∣ n → p ^ 2 ∣ n` | Divisibility wording of the exponent condition. Checked equivalent to the exponent wording by the audit bridge `powerful_iff_exp` for every n ≠ 0, and to the independently written `google-deepmind/formal-conjectures` definition `Nat.Full 2` by the submission's own `powerful_iff_primeFactors` for every n including 0 | `Statement.lean:36`, `AuditBridge.lean` `powerful_iff_exp` | none |
| R1 | `not_powerful_12`, `not_powerful_2` | Definition is discriminating, not vacuously true | `Statement.lean` | none |
| R1 | `powerful_sq`, `powerful_zero` | Boundary behaviour pinned: squares are powerful, and `Powerful 0` holds | `Statement.lean` | none |
| R2 | `0 < n` guard and the `n`, `n + 1` shape in `exists_consecutive_powerful*` and `answer_is_no` | Positivity and consecutiveness both present | `Statement.lean` | none |
| R3 | `powerful_12167`, `powerful_12168` | Both members proved powerful from the explicit factorisations | `Statement.lean` | none |
| R4 | `not_isSquare_12167`, `not_isSquare_12168` via `not_isSquare_of_between` | Uses the catalog's own 110²/111² argument | `Statement.lean` | none |
| R4 | `isSquare_sq`, `isSquare_9` | `IsSquare` is satisfiable, so the negative conjuncts are real constraints rather than vacuous | `Statement.lean` | none |
| R5 | `answer_is_no : ¬ ∀ n : ℕ, 0 < n → Powerful n → Powerful (n + 1) → IsSquare n ∨ IsSquare (n + 1)` | Exact negation of the catalog question, with "at least one" as a disjunction | `Statement.lean`, bridge `submission_implies_intended` | none |
| R6 | file docstring restricts scope to the yes/no question | Matches the catalog note | `Statement.lean` header | none |

## Independent bridge

`AuditBridge.lean` restates the question without reusing the submission's
vocabulary:

- `PowerfulExp n := ∀ p, p.Prime → p ∣ n → 2 ≤ n.factorization p`, an exponent
  formulation rather than the submission's divisibility formulation.
- `IsSquareE n := ∃ a, n = a * a`, avoiding Mathlib's `IsSquare`.
- `IntendedStatement := ¬ ∀ n, 0 < n → PowerfulExp n → PowerfulExp (n+1) → IsSquareE n ∨ IsSquareE (n+1)`.

`submission_implies_intended : IntendedStatement` is proved from the submitted
`answer_is_no`. The bridge therefore checks that the submitted theorem carries
the intended meaning, rather than only that it compiles.

`counterexample_arithmetic` and `primes_used` recheck 12167 = 23³,
12168 = 2³·3²·13², 12168 = 12167 + 1, 110·110 < 12167, 12168 < 111·111, and the
primality of 2, 3, 13 and 23, independently of the submission's proofs.

## Known limitations of the correspondence

1. `Powerful` is our own wording. The catalog states the exponent condition in
   prose only. Two independent cross-checks are supplied (the bridge, and
   agreement with `formal-conjectures`' `Nat.Full 2`), but prose-to-formal
   correspondence remains a human judgment and is not proved by any build.
2. The Golomb attribution is taken from the catalog and from
   erdosproblems.com/latex/365. [Go70] has not been read directly. The
   submission claims the formalization only, not the mathematics.
3. This self-check is performed by the submitter. It is not independent
   third-party verification.
