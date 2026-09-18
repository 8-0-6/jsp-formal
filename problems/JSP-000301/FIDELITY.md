# JSP-000301 fidelity review

Statement fidelity is the one thing Lean's kernel cannot check for us. This is
the record of the five checks from `docs/PIPELINE.md`.

## 1. Counterexample hunt

`plausible` was not usable here: `Powerful n` quantifies over all primes and is
not decidable as stated, so there is nothing for it to sample. The equivalent
falsification was done two other ways instead.

**Kernel-level.** The definition is checked for degeneracy by theorems that would
fail if it were wrong: `not_powerful_12` (12 = 2²·3 is not powerful, even though
4 does divide it), `not_powerful_2`, `powerful_sq`, `isSquare_sq`, `isSquare_9`.

**Independent arithmetic.** The witness was verified outside Lean twice, once with
`sympy` and once with a from-scratch trial-division factoriser and a binary-search
square test:

```
12167 = {23: 3}          powerful=True  square=False
12168 = {2: 3, 3: 2, 13: 2}  powerful=True  square=False
12168 - 12167 = 1
110² = 12100 < 12167 < 12168 < 12321 = 111²
```

## 2. Vacuity witness

`exists_consecutive_powerful` proves consecutive powerful pairs exist at all
(8 = 2³, 9 = 3²), so the question the catalog asks is not empty.

Note this is belt-and-braces rather than strictly necessary: an unsatisfiable
hypothesis would make the universal statement vacuously **true** and
`answer_is_no` **false**, so vacuity cannot inflate our result here. It is kept
because it documents that the subject matter is real.

## 3. Blind back-translation

An agent was given only the Lean declarations, with every comment, docstring and
reference stripped, and no access to the paper, the catalog, or the web. It was
asked what the statements mean.

It independently identified `Powerful` as "the textbook notion of a powerful
number (also called squarefull), equivalently the numbers of the form a²b³",
rendered `answer_is_no` as:

> "It is not the case that: for every positive integer `n`, if `n` is powerful and
> `n+1` is powerful, then `n` is a perfect square or `n+1` is a perfect square."

and confirmed the derivation of `answer_is_no` from the explicit witness is
intuitionistically valid.

**Divergences from the catalog statement: none.** The back-translation matches
"If two consecutive positive integers are powerful, must at least one be a
perfect square?", answered no.

**Three findings, all acted on:**

1. *Nothing exhibited a positive instance of `IsSquare`.* Under a degenerate
   `IsSquare`, every `¬ IsSquare` conjunct would be free and the counterexample
   would claim much less than it appears to. **Fixed:** added `isSquare_sq` and
   `isSquare_9`.
2. *`Powerful 0` is true* under this definition, since every prime divides 0 and
   `p² ∣ 0`. So the `0 < n` guard is load-bearing in `exists_consecutive_powerful`,
   not decoration. **Documented** and pinned with `powerful_zero`.
3. *`answer_is_no` is the weakest theorem in the file*, since it refutes without
   exhibiting. This is why `exists_consecutive_powerful_neither_square` is proved
   directly and listed first among the targets.

It also brute-forced the range below 300,000 and reported that 12167/12168 is the
smallest consecutive powerful pair with neither member a square. **We do not
claim minimality**, because we have not proved it.

## 4. Adversarial read

An agent was given the catalog question, the Lean, and the repository, and told to
build the strongest possible case for **rejection**. It returned REJECT with three
substantive findings. Adjudicated against primary sources:

### 4.1 "The Golomb attribution is false" — REFUTED, but it forced the check

The reviewer argued from chronology (Erdős poses the question in 1976 and
Erdős-Graham in 1980, *after* Golomb 1970) and from the fact that Golomb's Pell
construction `x² - 8y² = 1` yields only pairs containing a square (8/9, 288/289,
675/676, 9800/9801), which 12167/12168 is not.

The inference is reasonable and wrong. The source the catalog cites,
<https://www.erdosproblems.com/latex/365>, states: *"The answer to the first
question is no: Golomb [Go70] observed that both 12167 = 23³ and 12168 = 2³3²13²
are powerful."* Golomb both gave the Pell family **and** observed this separate
pair; Walker [Wa76] later proved infinitely many counterexamples exist.

The attack failed, but it was the right attack: the attribution had been copied
from the catalog without checking. It is now verified, and the limits of that
verification are written down in `PROBLEM.md`. It also surfaced a real citation
error, the page range is 848-855, not 848-852.

### 4.2 "The scope defense against the OPEN #365 is asserted, not established" — PARTLY UPHELD

The claim was correct but the evidence was missing; `PROBLEM.md` said
erdosproblems.com marks #365 OPEN "for that reason", which was our inference.
The source text now quoted in `PROBLEM.md` shows #365 bundles a settled clause
and an open counting clause. **Fixed:** inference replaced with the quotation.

### 4.3 "`powerful_zero`'s docstring overreaches" — UPHELD

We claimed the `0 < n` guard is load-bearing for the main theorem. It is not.
The reviewer supplied a counter-proof, which we compiled and confirmed:

```lean
theorem answer_is_no_unguarded :
    ¬ ∀ n : ℕ, Powerful n → Powerful (n + 1) → IsSquare n ∨ IsSquare (n + 1)
```

It holds because `IsSquare 0`, so `n = 0` satisfies the conclusion regardless.
The guard is load-bearing only in `exists_consecutive_powerful`. **Fixed:**
docstring corrected to say exactly where the guard matters and why it is kept.

### 4.4 Process gaps — UPHELD, and closed

The reviewer noted no prior-art check was recorded, which `PROGRESS.md` had
itself flagged as an open question. Done now:

- `google-deepmind/formal-conjectures` has **no** `365.lean`. No prior Lean
  statement of this problem exists there.
- Mathlib has no `Powerful` predicate and no occurrence of 12167.
- erdosproblems.com marks #365 `OPEN`, not `(LEAN)`, so no verified Lean proof is
  recorded upstream.

It also produced an unexpected benefit. formal-conjectures *does* define powerful
numbers, as `Nat.Full 2` = `∀ p ∈ n.primeFactors, p ^ 2 ∣ n`, for the neighbouring
problem #364. That is an independently written, publicly reviewed formalization of
the same notion, so `powerful_iff_primeFactors` now proves our definition
equivalent to theirs for every `n`. This is much stronger evidence than any
argument about wording.

### 4.5 Remaining weakest point

The reviewer's own "if you would accept, what is weakest" standard: **we have not
read [Go70] directly**, it is paywalled, so the attribution rests on
erdosproblems.com rather than the primary source. This is disclosed in
`PROBLEM.md`. Since we claim only the formalization role and not the mathematics,
we judge it acceptable, but a reviewer may disagree.

## 5. Sign-off

- [x] Authorised for submission by the repository owner on 2026-09-17.

**Recorded honestly:** the owner authorised submission without reviewing the
statement line by line, after being shown the plain-English rendering of the
result, told that the expected prize tier is low, and told that the Golomb
attribution rests on erdosproblems.com rather than on the primary source.

The pipeline's design intent is that a human reads the back-translation in
section 3 before submission. That did not happen here. The substitutes actually
performed were:

1. `powerful_iff_primeFactors`, machine-checked agreement with the independent
   formalization of powerful numbers in `google-deepmind/formal-conjectures`.
2. The blind back-translation in section 3, which matched the catalog wording
   with no divergences.
3. The adversarial review in section 4, whose one upheld finding was fixed.
4. Arithmetic verified three independent ways.

That is stronger evidence than a human skim would have produced, but it is not
the same thing, and the record should say so.
