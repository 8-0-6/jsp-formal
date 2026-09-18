# CLAUDE.md

Entry point for Claude Code in this repo. Keep this file small: it loads on every
request. `AGENTS.md` is the source of truth for working rules.

## What this repo is

Lean 4 formalizations targeting the Justin Sun Prize problem bank. The goal is a
complete, machine-verified proof of a already-solved problem, submitted as a PR
to `TheJustinSunPrize/awards`. Strategy and reasoning live in `docs/PRD.md`.

## Always-true rules

- Respond in English. Be concise and precise. Plain language a non-technical
  reader can follow.
- No em dashes in docs, commit messages, or chat replies. Use a period, comma,
  or colon.
- The user is a non-technical founder. Explain by user-visible effect and risk
  before implementation detail. Do not hand back commands you can run yourself.
- **Never weaken a locked statement to make a proof go through.** This is the one
  unforgivable failure mode. If the proof will not close, the proof is wrong, or
  the problem was a bad pick. Abandon it rather than quietly shrink the theorem.
- **Never use `sorry`, `admit`, `native_decide`, a custom `axiom`, `unsafe`,
  `partial def`, `@[implemented_by]`, or `Lean.ofReduceBool`** in anything under
  `JSPFormal/`. `sorry` is allowed only in a skeleton under construction, and
  only until Stage 3 closes.

## Before non-trivial work

1. Read `docs/PROGRESS.md` for current state and the next step.
2. Read `AGENTS.md` for the working rules.
3. Read `docs/PIPELINE.md` for the stage you are in.
4. Consult `docs/PRD.md` only when the *strategy* is in question, not routine work.

For a narrow fix, read only what is relevant.

## Commands

```bash
bin/check <file.lean>     # fast check, ~25 ms warm
bin/skeleton <file> <Thm> # is the decomposition valid?
bin/verify                # the full gate; must print VERIFIED
bin/status                # progress across all problems
bin/new-problem <ID> <slug> "<title>"
```

`bin/check` is 400x faster than `lake build`. Use it for every iteration and save
`bin/verify` for checkpoints.

## Recording work

- Per-problem state goes in `problems/<ID>/ledger.json`, not in prose.
- Update `docs/PROGRESS.md` at the end of a session.
- Any decision that future-you would otherwise re-litigate goes in
  `docs/DECISIONS.md`, with the reason and what would reverse it.
