# Progress

Current state and the next concrete step. Update this at the end of every
working session. Detailed per-problem state lives in `problems/<ID>/ledger.json`
and renders with `bin/status`.

**Last updated:** 2026-09-17

---

## Where we are

**Stage: JSP-000301 SUBMITTED. Awaiting maintainer review.**

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

**Wait for maintainer review**, then act on whatever they say. Do not force-push
the submitted branch: PR #969 pins commit `3ece478`, and reviewers check that the
named branch still contains it.

While waiting, screen the next candidate from
`research/triage/next-candidates.md` using the rule recorded there. The pipeline
is proven now, so a second problem of the same shape is cheap.

**Submitted 2026-09-17:**
- Proof repo (now public): <https://github.com/8-0-6/jsp-formal>
- PR: <https://github.com/TheJustinSunPrize/awards/pull/969>
- Claim: <https://github.com/TheJustinSunPrize/awards/issues/971>
- Role claimed: Lean formalization only

Both shortlisted candidates died on deep-dive (#387 is 62 pages using sieve
methods and exponential sums, not the 7 the heuristic reported; #946 is
Heath-Brown's sieve argument). Fixing the heuristic to exclude arXiv-cited
entries and require every cited paper to be short surfaced JSP-000301, which the
earlier passes had missed.

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
| 2026-09-17 | Deep-dive killed both shortlist candidates; corrected heuristic found JSP-000301 |
| 2026-09-17 | JSP-000301 proved end to end, 18/18 targets axiom-clean, CI green |
| 2026-09-17 | Blind back-translation found a missing IsSquare witness; fixed |
| 2026-09-17 | Adversarial review returned REJECT; 1 of 3 findings upheld and fixed, 2 refuted against primary sources |
| 2026-09-17 | Repo made public; PR #969 and claim issue #971 filed. First submission complete |
