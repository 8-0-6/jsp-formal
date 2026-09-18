---
name: scout
description: Stage 0 of the pipeline. Triage the Justin Sun Prize problem bank to find the cheapest problem we can completely formalize in Lean. Mechanical prefilter, then a parallel agent fan-out over survivors, producing a ranked shortlist in docs/TRIAGE.md. Use when choosing which problem to work on.
---

# Scout

Stage 0. Find the cheapest credible problem. Per `docs/PRD.md`, this decision is
more than half the outcome, so it gets real effort and it is done before any
Lean is written.

## Eligible pool

Only problems where **Current status = Solved** and **Lean proof = No**. Open
problems would require original mathematics. Problems with an existing Lean
proof cannot be claimed by us, since a Lean claim requires the repo be owned by
the claiming account.

## Phase A: mechanical prefilter

No agents. Score every candidate from catalog fields alone, then keep the top
band. Signals, in rough order of usefulness:

1. **Erdős bounty size.** Erdős priced his problems by difficulty, so this is
   the single best cheap proxy. Under $100 is promising, $500 and up is not.
2. **Question form.** "Can / Must / Is / Does there exist" are decision
   questions, often settled by an explicit construction or a counterexample,
   which is the cheapest thing to formalize. "How many / What is the maximum /
   What threshold" are quantitative and usually asymptotic.
3. **Anti-keywords.** asymptotic, density, threshold, growth, infinitely many,
   almost all, sufficiently large, o(1). Each of these is expensive.
4. **Area.** Elementary and finite combinatorics and number theory are well
   covered by Mathlib. Analysis, geometry, and topology are thinner.
5. **Reference count.** Fewer cited works means more self-contained.

## Phase B: agent fan-out

Parallel, read-only agents over the survivors, batched so each agent handles a
few problems rather than one. Each must report, and must answer "unknown"
rather than guess:

| Field | Meaning |
| --- | --- |
| Resolution shape | counterexample / explicit construction / exact value / asymptotic |
| Solution paper | length in pages, and whether the proof is self-contained |
| Mathlib coverage | which prerequisites already exist, which we would build |
| Statement risk | how easy is it to state this wrongly |
| Already formalized | check Mathlib, its Archive, `google-deepmind/formal-conjectures`, and the repos already credited in the catalog |
| Estimated hours | with a confidence label |
| Verdict | pursue / reject, with one sentence of reasoning |

## Output

`docs/TRIAGE.md`: a ranked table plus a short dossier for the top 3 to 5, each
naming the source paper and the specific theorem to formalize.

## Kill rules

Reject anything asymptotic, over roughly 15 pages of proof, depending on
unformalized deep results, or already formalized elsewhere.

## After

The founder and Claude pick one together. Then `bin/new-problem <ID> <slug>
"<title>"` and move to Stage 1.
