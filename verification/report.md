# Pre-submission Lean verification report, JSP-000301

**Overall verdict: Verification passed.**

For JSP-000301 ("If two consecutive positive integers are powerful, must at
least one be a perfect square?"), the submission at
`8-0-6/jsp-formal@3ece478053a97a80aad5b1628bc3e830cde115d6` fully resolves the
original question. Decisive reason: `JSPFormal.JSP000301.answer_is_no` is the
exact negation of the catalog's universally quantified question, it builds from
source under the pinned toolchain with no `sorry` or `admit`, every target
depends only on `propext`, `Classical.choice` and `Quot.sound`, and an
independently written restatement of the question is derivable from it.

| Required question | Judgment | Decisive evidence |
| --- | --- | --- |
| Does the proof address the specified original problem? | **Yes** | `answer_is_no` negates exactly the catalog's quantified claim, with the same positivity guard, the same `n`/`n+1` consecutiveness and "at least one" as a disjunction. Confirmed by the bridge `JSP000301Audit.submission_implies_intended`, which derives an independently worded statement of the same question from it. |
| Did the specified commit actually pass verification? | **Yes** | Clean source build and per-target checks on the pinned commit, GitHub Actions run 35734075085, all steps exit 0. |
| Does it fully solve the original problem? | **Yes** | It is a complete disproof. All five enumerated requirements are covered; the axiom audit shows no placeholder or custom axiom on any target. |
| Does it meet the Lean completeness requirements for this verification? | **Meets** | No proof gaps, no added assumptions, full coverage, standard axioms only. |

**Verification levels completed:** static review; actual Lean checks (clean
build from source, explicit module builds, `#print axioms` on every target); an
independent semantic bridge compiled against the pinned commit.
**Not completed:** kernel replay with an external checker, and independent
third-party review. This is a submitter self-check, which the upstream guide
treats as supporting evidence only.

## Pinned evidence

| Item | Value |
| --- | --- |
| Retrieval time | 2026-09-22, times below in UTC |
| Awards PR | <https://github.com/TheJustinSunPrize/awards/pull/969> |
| Awards repository state read | `bcf1866ea9a4ae82b32bd95b82ffd812b9ee80d2` (2026-09-21) |
| Catalog entry | `problems/catalog-0301-0400.md#JSP-000301` |
| Original problem source | Golomb, *Powerful numbers*, Amer. Math. Monthly 77 (1970); attribution via <https://www.erdosproblems.com/latex/365> |
| Proof repository | <https://github.com/8-0-6/jsp-formal> |
| Claimed branch | `main` |
| Selected commit | `3ece478053a97a80aad5b1628bc3e830cde115d6` |
| Ancestry | `git merge-base --is-ancestor` exit 0 against `refs/heads/main`; branch tip at check time `433e1af074209624f044c32862403348fcf49bb4` |
| Working tree at checkout | clean, `git status --porcelain` empty |
| Submodules / LFS | none |
| Target declarations | 14 under `JSPFormal.JSP000301`, listed in `targets.txt`; 4 further harness targets are audited by the repository gate but are not part of this claim |
| `targets.json` sha256 | `2ce3bb00696a287dfe87e13a4d3bae3209524b1cc39be8fae6e040454c03eafc` |
| `Statement.lean` sha256 | `7fff6e44fee6fae9111f4e484ada1fffc948be5cd7567ef411251e05e6817f99` |
| Audit script sha256 | `5db45dddcb4d588bc27e7c7161fbca5cedaa3e73e1c40843d21f5a214323cd07` (`skills/lean-verify/scripts/audit.py`) |

No revision conflicts were found: the PR body, the catalog edit and the
repository all name the same commit.

## Mathematical statement and coverage

Original question, from the catalog entry:

> If two consecutive positive integers are powerful, must at least one be a
> perfect square?

Submitted target:

```lean
theorem answer_is_no :
    ¬ ∀ n : ℕ, 0 < n → Powerful n → Powerful (n + 1) → IsSquare n ∨ IsSquare (n + 1)
```

where `Powerful (n : ℕ) : Prop := ∀ p : ℕ, p.Prime → p ∣ n → p ^ 2 ∣ n`.

| Req | Original requirement | Lean declaration | Correspondence | Gap |
| --- | --- | --- | --- | --- |
| R1 | "Powerful": every prime dividing n divides it at least twice | `Powerful`, `powerful_iff_primeFactors`, `not_powerful_12`, `not_powerful_2`, `powerful_sq`, `powerful_zero` | Matches. Cross-checked two ways: against the exponent formulation (`JSP000301Audit.powerful_iff_exp`) and against the independently written `Nat.Full 2` of `google-deepmind/formal-conjectures` | none |
| R2 | Consecutive and positive: n, n+1 with 0 < n | `0 < n` guard and `n`/`n + 1` shape throughout | Matches | none |
| R3 | Both members powerful | `powerful_12167`, `powerful_12168` | Matches; proved from 12167 = 23³ and 12168 = 2³·3²·13² | none |
| R4 | Neither a perfect square | `not_isSquare_12167`, `not_isSquare_12168`, via `not_isSquare_of_between`; satisfiability of `IsSquare` pinned by `isSquare_sq`, `isSquare_9` | Matches; uses the catalog's own 110²/111² argument | none |
| R5 | The yes/no question is answered "no" | `answer_is_no` | Exact negation of the quantified claim | none |
| R6 | Scope is this question only, not the counting question of Erdős #365 | file docstring | Matches the catalog review note | none |

### Equivalence and implication bridges

`AuditBridge.lean`, added on the audit branch only, restates the question
without reusing the submission's vocabulary:

```lean
def PowerfulExp (n : ℕ) : Prop := ∀ p : ℕ, p.Prime → p ∣ n → 2 ≤ n.factorization p
def IsSquareE (n : ℕ) : Prop := ∃ a : ℕ, n = a * a
def IntendedStatement : Prop :=
  ¬ ∀ n : ℕ, 0 < n → PowerfulExp n → PowerfulExp (n + 1) → IsSquareE n ∨ IsSquareE (n + 1)
theorem submission_implies_intended : IntendedStatement
```

Result: compiled, standard axioms only. `powerful_iff_exp` further shows the two
definitions of "powerful" agree for every `n ≠ 0`. `counterexample_arithmetic`
and `primes_used` recheck the numerics and the primality of 2, 3, 13, 23
independently of the submission's proofs.

## Environment and execution

| Item | Observed value |
| --- | --- |
| OS / isolation | GitHub Actions `ubuntu-latest`, single-use hosted runner, no reuse of the author's machine state. Run 35734075085, job 106766684541 |
| Toolchain | Pin `leanprover/lean4:v4.35.0-rc2` from `lean-toolchain`, installed via elan from official sources; resolved elan/Lean/Lake versions recorded in step 4 of the run log |
| Dependencies | `lake-manifest.json` sha256 `5d8605e12923ffc5167e75c83be9474722af615c815617d27112574a787ce423`; mathlib pinned at `065356127b1dc0016f66b7283ce0ce2c4055aa55` (`v4.35.0-rc2`). No `lake update` was run |
| Cache provenance | Mathlib oleans fetched by `lake exe cache get` from the official cache. No build cache of the submitted library was restored: the workflow deliberately omits `actions/cache`, and a step asserts `.lake/build` is absent before the build |
| Unmodified build | `lake build`, exit 0, 13:33:50 to 13:33:56 UTC |
| Explicit target checks | `lake build JSPFormal.JSP000301.Statement`, `JSPFormal.Smoke`, `JSPFormal`, exit 0 |
| Axiom audit | Generated `AxiomAudit.lean` with `#check` and `#print axioms` per target, run via `lake env lean`, exit 0 |
| Semantic bridge | `lake env lean AuditBridge.lean`, exit 0 |
| Repository gate | `./bin/verify`, exit 0, prints `18/18 targets depend only on standard axioms` and `VERIFIED` |
| Kernel / external cross-check | Not run. No independent checker was available in the audit environment |
| Post-run state | No submitted file modified. Audit additions are `AuditBridge.lean` and `.github/workflows/audit-verify.yml`, both only on branch `audit/lean-verify-3ece478` |

Automation, reported separately: `scripts/audit.py preflight` returned
`ready_for_target_checks: true`, `issues: []`, exit code 0. That is a mechanical
precondition check, not a mathematical verdict, and
`standard_axioms_only` is not by itself full-problem acceptance.

## Proof dependencies and gaps

Raw `#print axioms` output for the 14 claimed targets:

```
JSPFormal.JSP000301.answer_is_no                                depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.exists_consecutive_powerful_neither_square  depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.exists_consecutive_powerful                 depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.not_powerful_12                             depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.not_powerful_2                              depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.powerful_sq                                 depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.powerful_iff_primeFactors                   depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.isSquare_sq                                 does not depend on any axioms
JSPFormal.JSP000301.isSquare_9                                  depends on axioms: [propext]
JSPFormal.JSP000301.powerful_zero                               depends on axioms: [propext]
JSPFormal.JSP000301.powerful_12167                              depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.powerful_12168                              depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.not_isSquare_12167                          depends on axioms: [propext, Classical.choice, Quot.sound]
JSPFormal.JSP000301.not_isSquare_12168                          depends on axioms: [propext, Classical.choice, Quot.sound]

JSP000301Audit.submission_implies_intended                      depends on axioms: [propext, Classical.choice, Quot.sound]
JSP000301Audit.powerful_iff_exp                                 depends on axioms: [propext, Classical.choice, Quot.sound]
JSP000301Audit.counterexample_arithmetic                        depends on axioms: [propext, Classical.choice, Quot.sound]
JSP000301Audit.primes_used                                      depends on axioms: [propext, Classical.choice, Quot.sound]
```

All are the standard classical Lean foundations. No `sorryAx`, no placeholder,
no custom axiom, no `native_decide` or other native-computation dependency, and
no `debug.skipKernelTC`, `implemented_by` or `extern` on any target's dependency
path. A separate textual gate over `JSPFormal/` scans for `sorry`, `admit`,
`native_decide`, a bare `axiom`, `unsafe def`/`theorem`, `partial def`,
`@[implemented_by]`, `Lean.ofReduceBool` and `sorryAx`, and found none.

## Findings, limitations and next steps

No defects were found. Limitations, ordered by effect on a reader's confidence:

1. **This is a self-check, not independent verification.** It was run by the
   submitting account. Under the upstream process it is supporting evidence;
   maintainers still check the statement and reproduce verification themselves.
2. **`Powerful` is our own wording.** The catalog gives the condition in prose.
   Two independent cross-checks are supplied, but prose-to-formal correspondence
   remains a human judgment that no build establishes.
3. **The mathematics is Golomb's, not ours.** [Go70] has not been read directly;
   attribution follows the catalog and erdosproblems.com. The claim is for the
   Lean formalization role only.
4. **No external kernel replay.** Only Lean's own kernel checked the proof. No
   second, independently implemented checker was run.
5. **Local reproduction was not possible in the audit environment.** The
   environment used for report preparation has an egress policy that blocks the
   Mathlib olean cache hosts, so the executed checks were run on GitHub Actions
   instead of on a local machine. The build is still from source for the
   submitted library, on a single-use runner, at the pinned commit, and its log
   is public.

## Reproducible artifacts

- Audit run: <https://github.com/8-0-6/jsp-formal/actions/runs/35734075085>
- Audit branch: `audit/lean-verify-3ece478` (submitted commit plus
  `AuditBridge.lean` and `.github/workflows/audit-verify.yml`, no submitted file
  changed)
- Earlier run on the submitted commit itself:
  <https://github.com/8-0-6/jsp-formal/actions/runs/35296255311> (2026-09-18)
- `targets.json`, preflight `result.json`, the statement audit matrix and the
  evidence snapshots are retained locally with this report.

Reproduce with:

```bash
git clone --no-checkout https://github.com/8-0-6/jsp-formal proof
git -C proof checkout --detach 3ece478053a97a80aad5b1628bc3e830cde115d6
cd proof && lake exe cache get && lake build && ./bin/verify
```

This report concerns Lean proof verification only. It does not establish
attribution, priority, award eligibility or any payment decision.
