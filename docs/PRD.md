# PRD: winning the Justin Sun Prize

Status: **locked** 2026-09-17. Changes go through `DECISIONS.md`.

## 1. What winning means

A complete Lean 4 proof of a problem in the Justin Sun Prize problem bank, in a
public GitHub repo owned by the founder's account, accepted via PR into
`TheJustinSunPrize/awards` and claimed through an award-claim issue.

Not winning: a formal statement without a proof, a partial proof, a proof of a
special case, or a proof of a different theorem than the one the paper states.
The rules reject all four explicitly.

## 2. Strategy

**Fastest plausible win, then repeat.** Take the cheapest credible problem
first, carry it all the way through submission, and learn the review process
with a small bet. Then reuse the machine on higher tiers.

The reasoning: prize tiers above Contribution are decided by an Academic
Committee on criteria that are not public, so tier is not directly steerable.
What *is* steerable is whether we finish at all, and how fast. Zero awards have
been granted so far, so being early is worth more than being ambitious.

## 3. How the prize actually works

| Step | Where |
| --- | --- |
| Pick a problem | `problems/catalog-XXXX-XXXX.md` in the awards repo |
| Prove it | our own public repo, owned by the claiming account |
| Record it | PR to the awards repo editing that problem's **Lean proof** row |
| Claim it | award-claim issue with problem link, repo URL, public email |

The PR must carry repo URL, branch, a full 40-character commit SHA, the theorem
and file, build instructions, and attribution evidence. Lean source must never
be committed into the awards repo itself.

## 4. The opportunity

Measured from the catalog on 2026-09-17:

| Slice | Count |
| --- | --- |
| Problems in bank | 1,022 |
| Marked Solved | 354 |
| Already have a Lean proof | 66 |
| **Solved, no Lean proof** | **287** |
| Awards granted to date | 0 |

Those 287 are the target: the mathematics is published and settled, and nobody
has formalized it. They cluster in number theory, graph theory, and
combinatorics, which are the areas Mathlib covers best. Most are Erdős problems.

Competition is real. `plby/lean-proofs` holds 53 of the 66 existing proofs and
is clearly running a pipeline. A competitor filename encodes `219usd_38h`,
implying roughly 38 hours and $219 of compute for one Erdős problem. That is our
budget benchmark, and it means problems get taken while we deliberate.

## 5. Selection criteria

Ranked by what actually predicts cost:

1. **Concrete over asymptotic.** A resolution that is an explicit counterexample,
   an exact value, or a finite construction is far cheaper than one stated with
   `o(1)` or "for sufficiently large n", and far harder for a reviewer to dispute.
2. **Short solution paper.** Two to fifteen pages. Length of the human proof is
   the best available proxy for formalization cost.
3. **Prerequisites already in Mathlib.** Every cited theorem we must formalize
   ourselves multiplies the work.
4. **Crisp statement.** Fewer moving parts means less fidelity risk.
5. **Self-contained.** A proof that invokes three other unformalized deep results
   inherits all three.

Explicit anti-criteria: famous names, high historical bounty, and short problem
*titles*. "Catalan conjecture" is one line and would take person-years.

## 6. Pipeline

Full stage contracts in `PIPELINE.md`. The shape:

```
scout → statement → skeleton → proving → verify → submit
         (gate)      (gate)              (gate)
```

The governing principle:

> **Replace LLM judgment with kernel facts wherever possible.** Spend agent
> effort only on the one question the kernel cannot answer: does this Lean
> statement mean what the paper means?

Kernel facts we get for free: does it compile, does the main theorem follow from
the stubs, does anything depend on `sorry`, can `plausible` refute the statement.
Those are incorruptible and nearly instant. The statement-to-English mapping is
the only place a fallible reviewer is worth paying for.

## 7. Budgets and kill switches

Per problem, defaults in every ledger:

| Limit | Value | On breach |
| --- | --- | --- |
| Wall-clock | 40 h | Stop, write a post-mortem, pick another problem |
| Spend | $300 | Same |
| Retries per goal | 8 | Stop retrying, decompose the goal instead |
| Statement stage | 4 h | If the statement cannot be written faithfully, abandon |

A problem that fails a gate is abandoned, not rescued. The pool has 287 entries;
sunk cost is the enemy of the strategy.

## 8. Risks

| Risk | Mitigation |
| --- | --- |
| **Statement is subtly weaker than the paper** | The whole statement stage: `plausible`, vacuity witness, blind back-translation, adversarial read, founder sign-off |
| Someone claims our problem first | Prefer unfashionable problems; keep the repo private until submission; move fast |
| Decomposition does not compose | `bin/skeleton` proves it before any proving compute is spent |
| Sunk cost on an intractable problem | Hard budgets with abandon rules |
| Mathlib version drift breaks the build | Toolchain pinned, `lake-manifest.json` committed, CI builds from clean |
| Reviewer disputes attribution | `PROBLEM.md` records exact source refs; we formalize, we do not claim the mathematics |

## 9. Non-goals

- Proving anything currently **Open**. That is original mathematics, not formalization.
- Contributing upstream to Mathlib.
- Building a general-purpose theorem prover.
- Optimizing for prize tier over completion, until the first win is banked.
