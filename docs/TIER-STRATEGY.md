# Tier strategy

Written 2026-09-18, after JSP-000301 was submitted and the prize rules were read
properly for the first time.

## The rule that reframes everything

From <https://www.hejustinsun.com/prize/rules>, section 4.1:

> "**Lean verification serves strictly as a pass/fail entry threshold and is not
> factored into the final evaluation dimensions.**"

The Lean proof is the ticket through the door. It is not what is being scored.
Tier is decided by three dimensions, all of which are properties of the
**problem**, not of our work:

1. **Problem longevity.** How long it stood open in the public scientific domain.
2. **Publication venue.** The standing of the journal where the *mathematical*
   proof was vetted.
3. **Academic recognition.** How widely the result is recognised.

Then a completion adjustment: fully resolved, substantially resolved, partial
progress, or no progress.

## What follows from it

**To move up tiers we do not need to change the kind of work we do. We need a
bigger problem.** The same Lean formalization skill, pointed at an older and more
famous target, scores higher. We never need to do original mathematics.

This also explains why JSP-000301 will score low, and why no amount of polish
would have changed that. It was posed and answered in roughly the same era, the
venue is the Monthly, and recognition is modest. Our verification is unusually
careful, and that is worth nothing to the tier, because Lean is pass/fail.

## Two axes people confuse

| Axis | Values |
| --- | --- |
| **Claim role** (what you contributed) | Mathematical solution · Lean formalization · Both |
| **Prize tier** (what it is worth) | Pinnacle ($1M) · Breakthrough · Landmark · Advance · Contribution |

These are independent. A Lean-only claim on a famous problem can reach a high
tier. Claiming the solver role means solving something still open, which is
original research and not an engineering plan.

## The target band

Longevity is the dimension we can actually shop for. Measured across the 287
solved-with-no-Lean-proof catalog entries:

- 69 stood open 50 years or more
- 33 cite a premier venue (Annals, Inventiones, JAMS, Acta)

**The ceiling: JSP-000035, the Catalan conjecture.** Posed 1844, solved by
Mihăilescu in 2002. **158 years**, the longest-standing solved problem in the
catalog with no Lean proof. Rejected as a target: the proof needs cyclotomic
fields, Stickelberger, and Thaine's theorem, and is realistically person-years.
A Coq formalization exists, which the rules explicitly say does **not** satisfy
entry, so the opportunity is real but far beyond our budget.

**The band worth working: long open, short proof.** Where high longevity meets a
published proof we can actually finish. Candidates, all Solved with Lean proof
"No", every cited paper short, no arXiv preprints of unknown length:

| Problem | Open for | Longest paper | Area |
| --- | --- | --- | --- |
| JSP-001020 | 71 years | 5pg | Analysis, polynomials on the unit circle |
| JSP-000402 | 65 years | 5pg | Combinatorics / set theory |
| JSP-000216 | 65 years | 7pg | Additive combinatorics |
| JSP-000625 | 61 years | 8pg | Number theory / additive combinatorics |
| JSP-000813 | 61 years | 8pg | Number theory |
| JSP-000711 | 56 years | 8pg | Number theory / primitive sets |
| JSP-000628 | 62 years | 9pg | Graph theory / Turán numbers |

Compare against what we submitted: JSP-000301 scores near zero on longevity.
**A 65-year-old problem with a 5-page proof costs us roughly the same as a
6-year-old one with a 6-page proof, and is worth far more.** That is the whole
insight. Longevity is free to shop for; proof length is what we pay.

## Recommended approach

1. Deep-dive three from the band above. The deep-dive has already saved us twice
   by killing candidates that looked cheap and were not, so budget 4 hours and
   expect most to fail.
2. Commit to one we can finish in two to four weeks.
3. Do **not** attempt Catalan. Revisit only if this becomes a funded, multi-person
   effort.
4. Do not claim the solver role. That is original research, not a plan.

## The risk that should size this bet

As of 2026-09-18 the awards repository has **about 700 open pull requests**,
almost all Lean submissions opened within a single day, **zero external proof PRs
ever merged**, and both `data/awards.json` and `data/candidates.json` still empty.

Nobody has been paid. Nobody has even been recorded as a candidate. Until one
submission is accepted, the probability that any of this converts is unknown.

**Therefore: do not spend months before the first evidence of payout.** Size the
next bet at weeks, not months, and treat the result of PR #969 as the signal that
unlocks larger investment.
