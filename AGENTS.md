# AGENTS.md

Rules for any agent or human working in this repository.

## Goal

Produce complete, machine-verified Lean 4 proofs of problems from the Justin Sun
Prize problem bank, in a form a hostile reviewer cannot fault.

## Non-negotiable rules

1. **Never change or weaken the original theorem.** The Lean statement must mean
   exactly what the catalog entry and the source paper mean. Not a special case,
   not a bounded version, not an extra hypothesis that makes it easier.
2. **Never use `sorry`, `admit`, or a custom `axiom`.** Also banned:
   `native_decide`, `unsafe`, `partial def`, `@[implemented_by]`,
   `Lean.ofReduceBool`. `bin/verify` enforces all of these.
3. **Every target theorem goes in `targets.txt`.** If it is not listed, it is not
   verified. An empty manifest is treated as a failure.
4. **Only the three standard axioms are allowed:** `propext`, `Classical.choice`,
   `Quot.sound`. Anything else fails the audit.
5. **Prefer Mathlib.** Search before you prove: `exact?`, `apply?`, `rw?`, `hint`,
   and `loogle`. Re-proving an existing lemma is wasted work and adds review risk.
6. **Break hard proofs into small lemmas.** State the whole skeleton first, prove
   the main theorem from the stubs, then fill each stub independently.
7. **Compile constantly.** Use targeted imports, not `import Mathlib`. In this
   project that is the difference between a 5 second and a 159 second loop.
8. **Keep natural language separate from Lean.** Prose plans live in `research/`.
   Nothing in `JSPFormal/` may depend on a claim that is only argued in prose.

## Statement fidelity

Lean's kernel proves your *proof* is right. Nothing proves your *statement* is
right. That is where submissions fail, so:

- For every theorem, record in `problems/` the exact source (paper, theorem
  number, page) the Lean statement is meant to capture.
- **Prove a satisfiability witness.** If the hypotheses can never hold, the
  theorem is vacuously true and worthless. Construct an instance that satisfies
  them and verify it.
- Before submitting, do an adversarial pass whose only goal is to find a reading
  under which the Lean statement is weaker than the paper's.

## Layout

| Path | Contents |
| --- | --- |
| `JSPFormal/` | Verified Lean source. Everything here is built and audited. |
| `targets.txt` | The theorems `bin/verify` must certify. |
| `problems/` | Problem statements, catalog entries, source references. |
| `research/` | Natural-language proof plans and blueprints. |
| `attempts/` | Scratch Lean. Not built, not audited, never cited as evidence. |
| `bin/verify` | The gate. |

## Workflow

1. Write the plan in `research/`.
2. Write the statement in `JSPFormal/`, with every lemma stubbed.
3. Add the main theorem to `targets.txt`.
4. Fill stubs one at a time, compiling after each.
5. Run `./bin/verify`. It must print `VERIFIED`.
6. Commit one logical step at a time so a regression can be bisected.

## Submitting

The prize requires a Lean proof in a public repo **owned by the submitting
GitHub account**, referenced from a PR against `TheJustinSunPrize/awards` that
edits the relevant `problems/catalog-XXXX-XXXX.md` row, plus an award-claim
issue. The PR needs repo URL, branch, a full 40-character commit SHA, the
theorem and file, build instructions, and attribution. Never commit Lean source
into the awards repo itself.
