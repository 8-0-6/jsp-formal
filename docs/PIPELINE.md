# Pipeline

Six stages. Each has a **gate** that must pass before the next stage's compute is
spent, and a **kill rule** that ends the problem rather than rescuing it.

```
   287 candidates
        │
  ┌─────▼─────────────────────────────────────────┐
  │ 0  SCOUT        parallel · read-only · cheap  │──► kill: too costly
  └─────┬─────────────────────────────────────────┘
   shortlist 3-5
        │
  ┌─────▼─────────────────────────────────────────┐
  │ 1  STATEMENT    the gate that decides the win │──► kill: cannot state
  │    plausible · witness · back-translate ·     │       it faithfully
  │    adversarial read · founder sign-off        │
  └─────┬─────────────────────────────────────────┘
   statement LOCKED
        │
  ┌─────▼─────────────────────────────────────────┐
  │ 2  SKELETON     bin/skeleton                  │──► fail: replan (minutes)
  └─────┬─────────────────────────────────────────┘
   decomposition PROVEN valid
        │
  ┌─────▼─────────────────────────────────────────┐
  │ 3  PROVING      recursive descent · parallel  │──► budget breach: abandon
  └─────┬─────────────────────────────────────────┘
        │ every stub filled
  ┌─────▼─────────────────────────────────────────┐
  │ 4  VERIFY       bin/verify + CI               │
  └─────┬─────────────────────────────────────────┘
  ┌─────▼─────────────────────────────────────────┐
  │ 5  SUBMIT       SHA · PR · claim issue        │
  └───────────────────────────────────────────────┘
```

---

## Stage 0 · Scout

**In:** catalog entry, source papers.
**Out:** a row in `docs/TRIAGE.md` scoring feasibility.
**Agents:** many, parallel, read-only. Cheap model.

Each scout answers only these, and is required to say "unknown" rather than guess:

| Field | Why it matters |
| --- | --- |
| Resolution shape | concrete / exact value / construction / asymptotic |
| Solution paper length | best proxy for cost |
| Prerequisites | which cited results are already in Mathlib |
| Statement risk | how easy is it to state this wrongly |
| Already formalized? | check Mathlib, its Archive, `google-deepmind/formal-conjectures` |
| Estimated hours | with a confidence label |

**Gate:** estimated cost under budget, and not already formalized elsewhere.
**Kill:** anything asymptotic, or over 15 pages, or depending on unformalized deep results.

## Stage 1 · Statement

The stage that decides whether we win. No proving happens here.

**In:** the chosen problem, its source paper.
**Out:** a Lean statement, `FIDELITY.md` complete, `statement.locked = true`.

Five checks, in order. The first two are kernel facts; the rest are judgment:

1. **`plausible` counterexample hunt.** If the statement is false as written,
   this finds a small counterexample in seconds. Free falsification.
2. **Vacuity witness.** Construct and verify an instance satisfying every
   hypothesis. Without this, unsatisfiable hypotheses make the theorem
   vacuously true and worthless.
3. **Blind back-translation.** An agent that has *not seen the paper* renders the
   Lean statement into English. Diff that against the verbatim statement. An
   agent told "check these match" will rationalize a match; one that never saw
   the original cannot. This is the highest-yield check in the pipeline.
4. **Adversarial read.** An agent is asked to argue the Lean statement is
   *weaker* than the paper's, and to produce the strongest such case it can.
5. **Founder sign-off.** The founder reads the back-translation in English and
   confirms it says what the paper says. Cheap, and the last line of defence.

**Gate:** all five done, `fidelity_signed_off = true`.
**Kill:** 4 hours without a faithful statement. The problem is harder to state
than it looked, which usually means it is harder to prove than it looked.

Once locked, the statement is frozen and git-tagged. Weakening it later to make
a proof go through is the one unforgivable failure mode.

## Stage 2 · Skeleton

**In:** locked statement, a natural-language proof plan in `research/`.
**Out:** a Lean file where every lemma is `sorry`-stubbed and the main theorem is
*derived from those stubs*; goals written into the ledger.

```bash
bin/skeleton JSPFormal/JSP000XXX/Main.lean JSPFormal.JSP000XXX.main
```

**Gate:** `DECOMPOSITION VALID`. This is a kernel fact, not an opinion: Lean
confirms the lemmas actually imply the theorem.
**Kill:** three failed replans. The proof plan is not understood well enough yet;
go back and read the paper again.

This stage is cheap and catches the most expensive class of mistake. Never skip it.

## Stage 3 · Proving

**In:** a validated skeleton with N open stubs.
**Out:** zero open stubs.

Stubs are independent by construction, so workers run in parallel over the DAG.
Each worker on one goal:

1. **Premise search first.** `exact?`, `apply?`, `rw?`, `hint`, and
   `LeanSearchClient` (`#leansearch`, `#loogle`). Re-proving something Mathlib
   already has is wasted work and extra review surface.
2. **Tactic ladder.** `simp` / `norm_num` / `omega` / `decide` → `linarith` /
   `nlinarith` / `positivity` → `field_simp` / `ring` → `aesop` → manual.
3. **Feed errors back.** `bin/check` returns the error and the open goal in
   milliseconds. Retry with that context.
4. **On budget exhaustion, do not retry harder.** Escalate: the worker becomes a
   decomposer for its own goal, emitting sub-lemmas and recursing. That recursion
   is what cracks hard goals; more retries at the same altitude do not.

**Gate:** `bin/verify` passes.
**Kill:** problem budget breached. Write the post-mortem, pick another problem.

## Stage 4 · Verify

```bash
bin/verify
```

Build, then a forbidden-construct scan (`sorry`, `admit`, `native_decide`,
custom `axiom`, `unsafe`, `partial def`, `@[implemented_by]`,
`Lean.ofReduceBool`), then a `#print axioms` audit of every theorem in
`targets.txt`. Only `propext`, `Classical.choice`, `Quot.sound` are permitted.

CI runs the same command on a clean machine, which is also our public evidence
that the proof builds from scratch.

## Stage 5 · Submit

See `SUBMISSION.md`.

---

## Where each tool fits

| Tool | Stage | Latency |
| --- | --- | --- |
| `bin/check` | 1, 2, 3 | ~25 ms warm, ~25 s per new import set |
| `bin/skeleton` | 2 | seconds |
| `bin/verify` | 4 | minutes |
| `bin/status` | all | instant |
| `bin/new-problem` | 0 → 1 | instant |

`bin/check` is the reason the loop is viable. `lake build` takes 8 to 13 seconds
per iteration; the REPL daemon takes about 25 milliseconds, roughly 400x faster,
because Mathlib stays loaded in memory between checks.
