# AGENTS.md

Working rules for any agent or human in this repository. Strategy is in
`docs/PRD.md`; stage mechanics are in `docs/PIPELINE.md`.

## The one rule that matters most

Lean's kernel guarantees your **proof** is correct. Nothing guarantees your
**statement** is. A fully verified, `sorry`-free file can prove something
vacuous, or weaker than the paper claims, and it will compile beautifully.

So: **never weaken a locked statement to make a proof go through.** If the proof
will not close, either the proof is wrong or the problem was a bad pick. Abandon
the problem. Do not quietly shrink the theorem. That is the only way we lose in a
way we cannot recover from.

## Hard prohibitions

Banned anywhere under `JSPFormal/`:

`sorry` · `admit` · `native_decide` · custom `axiom` · `unsafe` · `partial def` ·
`@[implemented_by]` · `Lean.ofReduceBool`

`sorry` is permitted only inside a skeleton under construction, and only until
Stage 3 closes. `bin/verify` enforces every one of these.

Only three axioms are allowed: `propext`, `Classical.choice`, `Quot.sound`.
Anything else fails the audit.

## Method

1. **Replace judgment with kernel facts.** Before asking an agent to assess
   something, ask whether Lean can answer it. It can tell you whether something
   compiles, whether the main theorem follows from the stubs, what a declaration
   depends on, and often whether a statement is refutable (`plausible`). Those
   answers are free and incorruptible. Save agent effort for the one question the
   kernel cannot answer: does this statement mean what the paper means?
2. **Skeleton before proving.** State every lemma with `sorry`, derive the main
   theorem from the stubs, and run `bin/skeleton`. Only then start proving.
3. **Search Mathlib before proving anything.** `exact?`, `apply?`, `rw?`, `hint`,
   and `LeanSearchClient` (`#leansearch`, `#loogle`). Re-proving an existing lemma
   wastes time and adds review surface.
4. **Targeted imports, never `import Mathlib`.** Measured here: 159 s versus
   4.9 s to build the same file. Keep the import block stable within a session so
   the REPL environment cache keeps hitting.
5. **Do not retry harder, decompose.** After 8 failed attempts on a goal, stop.
   Emit sub-lemmas and recurse. More attempts at the same altitude do not work.
6. **Prose and Lean stay separate.** Plans live in `research/`. Nothing under
   `JSPFormal/` may depend on a claim that is only argued in prose.
7. **One logical step per commit** so a regression can be bisected.

## Statement fidelity

Every problem needs `FIDELITY.md` complete before proving starts:

1. `plausible` counterexample hunt
2. Vacuity witness: an instance satisfying every hypothesis, verified in Lean
3. Blind back-translation: an agent that has not seen the paper renders the Lean
   statement into English, and we diff it against the verbatim statement
4. Adversarial read: an agent argues the Lean statement is weaker than the paper's
5. Founder sign-off on the English

## Layout

| Path | Contents |
| --- | --- |
| `JSPFormal/` | Verified Lean source. Built and audited. |
| `targets.txt` | Theorems `bin/verify` must certify. Not listed means not verified. |
| `problems/<ID>/` | `PROBLEM.md`, `FIDELITY.md`, `ledger.json` |
| `research/` | Natural-language proof plans |
| `attempts/` | Scratch Lean. Not built, never cited as evidence. |
| `harness/` | REPL daemon and ledger library |
| `bin/` | `check`, `skeleton`, `verify`, `status`, `new-problem` |
| `docs/` | PRD, PIPELINE, PROGRESS, DECISIONS, SUBMISSION |

## Budgets

40 h and $300 per problem, 8 retries per goal, 4 h for the statement stage. On
breach, abandon and write a post-mortem. There are 287 candidates; sunk cost is
the main threat to the strategy.
