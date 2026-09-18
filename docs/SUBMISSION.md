# Submission checklist

Derived from `CONTRIBUTING.md` in `TheJustinSunPrize/awards`. Re-read that file
before submitting; it changes.

## Preconditions

- [ ] `bin/verify` prints `VERIFIED` locally
- [ ] CI is green on a clean machine
- [ ] `FIDELITY.md` complete, including founder sign-off
- [ ] Vacuity witness proved and listed in `targets.txt`
- [ ] `PROBLEM.md` cites the exact paper, theorem number, and page
- [ ] Repo flipped from private to **public**
- [ ] Repo is owned by the **claiming GitHub account** (`8-0-6`). Ownership by
      anyone else disqualifies the Lean claim.

## Pin the commit

```bash
git rev-parse HEAD        # full 40-character SHA, not short
git branch --show-current
```

Both go in the PR. Reviewers check that the named branch actually contains that
commit, so do not force-push afterwards.

## PR to the awards repo

Edit only `problems/catalog-XXXX-XXXX.md`, only the row for our problem. Fields
external PRs may touch: **Current status**, **Lean proof**, **Attribution basis**,
**Publication details**. Status may only be `Open` or `Solved`.

Must include:

- [ ] Public source repository URL
- [ ] Branch name
- [ ] Full 40-character commit SHA
- [ ] Theorem name and file path
- [ ] Build instructions
- [ ] Formalization authors and attribution evidence

Must **not** include:

- [ ] Any Lean source, project files, dependencies, archives, or binaries
- [ ] Proof text pasted into catalog rows
- [ ] Changes to unrelated repository files
- [ ] Intermediate results or partial formalizations

## Award claim issue

Use the award-claim issue form. It must be filed **by the contributor
themselves**; proxy claims are rejected.

- [ ] Problem-bank link
- [ ] Original Lean proof repository URL, owned by the issue author
- [ ] A public follow-up email. It will be published, so use an address intended
      for public correspondence.
- [ ] Contribution role. We are claiming the **Lean formalization** role only,
      not the mathematical solver role.

For a Lean-only claim, the identity-verification field may be left blank *only
if* the repository's own attribution establishes the applicant as a
formalization contributor. So make authorship explicit in the repo: file headers
and README.

## After submitting

- [ ] Do not force-push the submitted branch
- [ ] Record the PR and issue URLs in the ledger
- [ ] Update `PROGRESS.md`
