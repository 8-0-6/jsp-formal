## Pre-submission Lean verification

Completed the optional self-check described in
[`docs/verification.md`](https://github.com/TheJustinSunPrize/awards/blob/main/docs/verification.md#recommended-lean-pre-submission-check),
using this repository's [`lean-verify` skill](https://github.com/TheJustinSunPrize/awards/blob/main/skills/lean-verify/SKILL.md).

- **Method/tool and version:** `skills/lean-verify` at awards commit `bcf1866ea9a4ae82b32bd95b82ffd812b9ee80d2`; `scripts/audit.py` sha256 `5db45dddcb4d588bc27e7c7161fbca5cedaa3e73e1c40843d21f5a214323cd07`.
- **Checked repository and commit:** `8-0-6/jsp-formal` at `3ece478053a97a80aad5b1628bc3e830cde115d6`, branch `main`. This is the same commit this PR submits; there is no difference between the checked and submitted versions. `git merge-base --is-ancestor` confirms the commit is contained in `main`, and the checkout tree is clean.
- **Verification date and conclusion:** 2026-09-22. **Verification passed.**
- **Limitations:** this is a submitter self-check, not independent verification. `Powerful` is our own wording of the catalog's prose condition, so the prose-to-formal correspondence remains a human judgment (two independent cross-checks are supplied below). The mathematics is Golomb's; [Go70] has not been read directly and this PR claims the Lean formalization role only. No external kernel replay with a second, independently implemented checker was run.

### Summary

**Statement correspondence.** The target

```lean
theorem answer_is_no :
    ¬ ∀ n : ℕ, 0 < n → Powerful n → Powerful (n + 1) → IsSquare n ∨ IsSquare (n + 1)
```

is the exact negation of the catalog question, with the same positivity guard, the same `n`/`n+1` consecutiveness, and "at least one" as a disjunction.

To test that rather than assume it, the audit adds `AuditBridge.lean`, which restates the question using notions written independently of the submission (`PowerfulExp` by factorisation exponent instead of divisibility, and `∃ a, n = a * a` instead of Mathlib's `IsSquare`) and proves `submission_implies_intended : IntendedStatement` from the submitted theorem. It compiles. `powerful_iff_exp` additionally shows the two definitions of "powerful" agree for every `n ≠ 0`, and the submission's own `powerful_iff_primeFactors` shows agreement with `Nat.Full 2` as independently formalized in `google-deepmind/formal-conjectures`.

**Coverage.** Six requirements were enumerated from the catalog wording before reading the Lean formulation (definition of powerful; consecutive and positive; both powerful; neither square; the yes/no question answered; scope limited to this question and not the separate counting question of Erdős #365). All six are covered, with no uncovered requirement. Matrix: [`verification/statement-audit.md`](https://github.com/8-0-6/jsp-formal/blob/audit/lean-verify-3ece478/verification/statement-audit.md).

**Lean checks.** On a single-use GitHub Actions runner, with no build cache of the submitted library restored and a step asserting `.lake/build` is absent beforehand:

| Step | Result |
| --- | --- |
| `lake exe cache get` (mathlib oleans only, pinned `065356127b1dc0016f66b7283ce0ce2c4055aa55`) | exit 0 |
| `lake build` from source | exit 0 |
| `lake build JSPFormal.JSP000301.Statement`, `JSPFormal.Smoke`, `JSPFormal` | exit 0 |
| `#check` + `#print axioms` per target via `lake env lean` | exit 0 |
| `lake env lean AuditBridge.lean` (independent bridge) | exit 0 |
| `./bin/verify` repository gate | exit 0, `18/18 targets depend only on standard axioms` |

`scripts/audit.py preflight` returned `ready_for_target_checks: true`, `issues: []`, exit 0.

**Trust dependencies.** Every claimed target and every bridge theorem depends only on `propext`, `Classical.choice` and `Quot.sound`, or fewer: `isSquare_sq` depends on no axioms, and `isSquare_9` and `powerful_zero` depend on `propext` alone. No `sorryAx`, no placeholder, no custom axiom, no `native_decide` or other native computation, and no `debug.skipKernelTC`, `implemented_by` or `extern` on any dependency path. Raw output is in the report and in the run log.

### Evidence

- Report: [`verification/report.md`](https://github.com/8-0-6/jsp-formal/blob/audit/lean-verify-3ece478/verification/report.md)
- Audit run log: <https://github.com/8-0-6/jsp-formal/actions/runs/35734075085>
- Audit branch `audit/lean-verify-3ece478`: the submitted commit `3ece478` plus exactly two added files, `AuditBridge.lean` and `.github/workflows/audit-verify.yml`. No submitted file is modified. Diff: <https://github.com/8-0-6/jsp-formal/compare/3ece478...audit/lean-verify-3ece478>
- Earlier run on the submitted commit itself, 2026-09-18: <https://github.com/8-0-6/jsp-formal/actions/runs/35296255311>
- Target manifest and preflight output: [`verification/targets.json`](https://github.com/8-0-6/jsp-formal/blob/audit/lean-verify-3ece478/verification/targets.json), [`verification/preflight-result.json`](https://github.com/8-0-6/jsp-formal/blob/audit/lean-verify-3ece478/verification/preflight-result.json)

Reproduce:

```bash
git clone --no-checkout https://github.com/8-0-6/jsp-formal proof
git -C proof checkout --detach 3ece478053a97a80aad5b1628bc3e830cde115d6
cd proof && lake exe cache get && lake build && ./bin/verify
```

### Related PRs

#1197 submits a separate Lean formalization of the same problem. For the commit-date comparison described in the [award process](https://github.com/TheJustinSunPrize/awards/blob/main/docs/award-process.md#lean-formalization-or-both-roles), the commit selected by this PR, `3ece478`, has author and committer date **2026-09-18T01:40:06Z**, and is corroborated by a GitHub Actions run on that exact commit completing at **2026-09-18T01:41:49Z**, a server-recorded timestamp that is not settable by the committer.

---
_Generated by [Claude Code](https://claude.ai/code)_
