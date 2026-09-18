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

See below.

## 5. Sign-off

- [ ] Founder has read the back-translation in section 3 and agrees it says what
      the catalog asks.
- Signed: pending
