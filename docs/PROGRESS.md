# Progress

Current state and the next concrete step. Update this at the end of every
working session. Detailed per-problem state lives in `problems/<ID>/ledger.json`
and renders with `bin/status`.

**Last updated:** 2026-09-17

---

## Where we are

**Stage: triage complete, shortlist of 3, no problem committed yet.**

The environment and the verification spine are complete and tested. No
formalization work has started, because the problem is not chosen. Choosing it
is the next step and is worth doing carefully: per `PRD.md`, selection is more
than half the outcome.

## Done

- [x] Lean v4.35.0-rc2 + Mathlib v4.35.0-rc2, toolchain pinned, cache prebuilt
- [x] `bin/verify`: build + forbidden-construct scan + `#print axioms` audit
- [x] `bin/verify` negative-tested: catches a raw `sorry`, and a `sorry`
      laundered through a custom `axiom`, each by two independent layers
- [x] `bin/check`: REPL daemon, ~25 ms warm vs 8 to 13 s for `lake env lean`
- [x] `bin/check` guards against silently-broken imports, which the raw REPL
      reports as a valid empty environment with no error
- [x] `bin/skeleton`: decomposition gate, tested against valid and invalid decompositions
- [x] `bin/status`, `bin/new-problem`, ledger schema
- [x] `PRD.md`, `PIPELINE.md`, `DECISIONS.md`, `SUBMISSION.md`
- [x] Prize mechanism understood and documented: 287 Solved problems have no
      Lean proof; zero awards granted so far
- [x] `plausible` verified working: refuted a false statement in seconds
      (found n=6 as a counterexample), which is the Stage 1 falsification tool
- [x] Remote repo `github.com/8-0-6/jsp-formal`, **private**, owned by the
      claiming account. Flip to public at submission (see `SUBMISSION.md`)
- [x] `/scout` skill written; Stage 0 run end to end
- [x] Crawled all 1,249 erdosproblems.com pages into
      `research/triage/erdos-status.json` (reusable; regenerate with
      `research/triage/crawl-erdos.py`)
- [x] `docs/TRIAGE.md`: shortlist of 3, with rejections and reasons
- [x] CI green on a clean Ubuntu machine. First run failed on a real portability
      bug (module name taken from the directory basename), now fixed (D14)

## Next step

**Deep-dive the top two candidates in `docs/TRIAGE.md`.** Read Heath-Brown 1984
(JSP-000787) and BNPZ 2026 (JSP-000320), and produce a real blueprint estimate for
each, including which Mathlib pieces already exist. Budget 4 hours. Only then commit.

The headline from triage: 298 of 577 solved Erdős problems are already
Lean-verified, so the easy wins are gone. A realistic first target is weeks of
work on a 5 to 15 page paper.

## Open questions

| Question | Blocks | Notes |
| --- | --- | --- |
| Which problem? | everything | Stage 0 answers it |
| Is our top candidate already formalized upstream? | selection | Check Mathlib, its Archive, `google-deepmind/formal-conjectures` before committing |
| Does 40 h / $300 hold? | budgets | Benchmark is a competitor's `219usd_38h` filename. Recalibrate after problem one |

## Known constraints

- **Disk.** Mathlib alone is 7.4 GB and the machine runs close to full. Do not
  add a second toolchain without checking free space first.
- **Cold start.** The first `bin/check` after a reboot, or with a new import set,
  costs about 25 seconds. Every check after that is milliseconds. Keep import
  blocks stable across a working session.
- **Web tools.** `WebSearch` and `WebFetch` were failing in-session on
  2026-09-17 with a model configuration error. `curl` works, and the awards repo
  can be cloned directly.

## Log

| Date | Entry |
| --- | --- |
| 2026-09-17 | Prize researched, mechanism documented, 287-problem opportunity identified |
| 2026-09-17 | Lean + Mathlib installed; `bin/verify` built and negative-tested |
| 2026-09-17 | REPL daemon built; inner loop ~400x faster |
| 2026-09-17 | Pipeline designed; PRD, decisions, and submission checklist written |
| 2026-09-17 | Private repo created under 8-0-6 and pushed |
| 2026-09-17 | Stage 0 triage: 1,249 problems crawled, 279 solved-not-formalized found, shortlist of 3 |
| 2026-09-17 | CI caught a directory-name portability bug in bin/verify; fixed, CI green |
