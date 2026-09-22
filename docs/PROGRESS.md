# Progress

Current state and the next concrete step. Update this at the end of every
working session. Detailed per-problem state lives in `problems/<ID>/ledger.json`
and renders with `bin/status`.

**Last updated:** 2026-09-22

---

## Where we are

**Stage: JSP-000301 SUBMITTED. Awaiting maintainer review.**

The environment and the verification spine are complete and tested, and problem
one is proved, verified and filed. PR #969 has been open and unreviewed for five
days. As of the 2026-09-22 upstream check, no external Lean submission has been
accepted from anyone, so the wait is a review-capacity problem rather than a
signal about our work.

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

**Still waiting on maintainer review of PR #969. Nothing is blocked on us.** Do
not force-push the submitted branch: PR #969 pins commit `3ece478`, and reviewers
check that the named branch still contains it.

Two things are worth doing while waiting, in this order:

1. **Gather public evidence that our proof commit is ours and is dated.** Under
   the new v4 rules (see below), priority is decided by the earliest verified
   proof commit, not by who opened a PR first. Our advantage over the duplicate
   submission is now an evidence question, not a timestamp question.
2. **Run the upstream `lean-verify` skill against commit `3ece478`** and attach
   the report to PR #969. It is optional, not a requirement, but it is the
   maintainers' own checklist and no reviewer has reached our PR yet.

Screening the next candidate from `research/triage/next-candidates.md` is lower
priority than it was: see the acceptance evidence below.

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
| Will maintainers review external Lean PRs at all? | everything downstream | Zero accepted in the first five days across ~2,600 PRs. Recheck weekly |
| Can we prove our commit date to a challenger? | priority on JSP-000301 | v4 decides priority on earliest verified commit, not PR time. Git dates alone are explicitly not enough |
| Should claim issue #971 be updated now or after #969 merges? | our claim | The form now requires a merged PR. Upstream says update the existing issue, do not open a duplicate |
| Has the identity-verification email been sent? | award delivery | Now mandatory for every applicant, including Lean-only. Not yet sent |
| Is a second problem worth starting? | budgets | Pipeline is proven and cheap, but a second unreviewed PR adds no value while acceptance is zero |
| Does 40 h / $300 hold? | budgets | Problem one cost 3.5 h and $0, far under budget. Benchmark was a competitor's `219usd_38h` filename |

## Upstream check, measured 2026-09-22

Read directly from a clone of `TheJustinSunPrize/awards` at commit `bcf1866`
(2026-09-21). GitHub API access is scoped to our own repo in this environment, so
PR bodies, review comments and merge state were inferred from repository content
and refs, not from the PR API.

### Our submission

- **PR #969 is still open and still mergeable.** `refs/pull/969/merge` exists
  upstream, which GitHub only publishes for open, conflict-free PRs. No review
  has landed and no maintainer commit references it.
- The duplicate #1197 is **also still open**. Neither has been accepted.
- The JSP-000301 catalog entry is materially unchanged: **Lean proof: No**,
  **Eligible to claim: No**. The only edit was a repo-wide field rename,
  `Public review` to `Scholarly recognition`, which does not collide with our diff.

### Nobody's Lean submission has been accepted

Problems flagged **Lean proof: Yes** in the catalog: **66 on 2026-09-17, 66 now.**
Identical. Roughly 1,800 further PRs were opened in those four days and not one
moved a problem from No to Yes. The bottleneck is maintainer review capacity,
not the queue position we measured on 2026-09-18.

### First candidates published, zero awards

Six contributions entered the public register on 2026-09-19, starting 14-day
review clocks that end **2026-10-03**:

| Problem | Solver | Lean formalizer |
| --- | --- | --- |
| JSP-000305 | | Wouter van Doorn |
| JSP-000371 | | Wouter van Doorn |
| JSP-000381 | | Wouter van Doorn |
| JSP-000526 | Wouter van Doorn; Yanyang Li; Quanyu Tang | Wouter van Doorn |
| JSP-000866 | Quanyu Tang | |
| JSP-001001 | Yanyang Li; Quanyu Tang | |

**All six were already Eligible to claim on 2026-09-17**, before the submission
rush. They are people claiming credit for solutions and formalizations the
project had already recorded, not new formalization work being accepted.
`awards/` still holds no award records.

### The rules changed after we submitted (v4 process)

Merged 2026-09-19 to 2026-09-21, in PRs #1642, #1710, #1728, #1759, #1782, #2052,
#2123, #2190, #2542 and #2606. What affects us:

- **Priority is the earliest verified proof commit, not PR opening time.**
  Stated outright: "PR opening time does not determine priority." The docs also
  warn that git dates can be set by hand and require independently checkable
  public history tying a proof version to its claimed date. See D15.
- **A claim issue now requires a *merged* contribution PR.** "A pending PR or a
  proof repository URL does not satisfy the merged-PR requirement." Our claim
  #971 was filed when a pending PR was acceptable, so it cannot be accepted until
  #969 merges. Upstream guidance is to update the existing issue rather than open
  a new one.
- **The claim form gained required fields and declarations**, including a
  "Merged submission PR" field and four new checkboxes.
- **Every applicant must now send an identity-verification email** from their
  public follow-up address to `thejustinsunprize@hejustinsun.com`. This used to
  be waivable for Lean-only claims where source attribution was clear. It is not
  any more, and existing attribution explicitly does not waive it.
- **Mathematical review must pass before a Lean proof is accepted.** Harmless for
  us: JSP-000301 is already Solved with Golomb credited.
- **A `lean-verify` skill now ships in the upstream repo** (`skills/lean-verify/`),
  a recommended pre-submission self-check with an audit script. Optional, and not
  using it is explicitly not a defect.
- **The PR template roughly doubled.** New fields include statement origin,
  mathematical solution and review reference, related PRs, an axiom audit command
  with its output, and an optional self-check section.
- **Before closing a 14-day review, maintainers check pending PRs on the same
  problem and contribution type.** The duplicate #1197 will be looked at
  alongside ours rather than ignored.
- Upstream deleted its JSON schema machinery, `scripts/manage.py`, its test suite
  and its CI workflows. Records are now plain Markdown.

### What this means

The queue-position worry from 2026-09-18 was the wrong worry. Being 672nd costs
nothing when the acceptance rate for everyone is zero. The real risks now are
the merged-PR precondition on our claim, the identity email we have not sent,
and priority being decided on commit evidence we have not published.

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
| 2026-09-18 | Competitive position measured: 672nd of 832 PRs by submission time |
| 2026-09-22 | Upstream check: #969 still open, zero Lean submissions accepted repo-wide, first six candidates published, v4 rules changed priority to earliest commit |
