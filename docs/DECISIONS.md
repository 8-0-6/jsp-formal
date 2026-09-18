# Decision log

Append-only. Newest last. Each entry: what we decided, why, and what would make
us reverse it. If a decision is reversed, add a new entry, do not edit history.

---

### D1 · Separate repo from Argus
**2026-09-17.** This lives at `~/Desktop/Startup/Active/LeanProver/JSPFormal`, not
inside the Argus Next.js product repo.
**Why:** unrelated toolchains, unrelated dependency trees, and this repo becomes
a public submission artifact that reviewers will read. Mixing would harm both.
**Reverse if:** never.

### D2 · Target the Solved-with-no-Lean-proof pool
**2026-09-17.** We only consider the 287 problems marked **Solved** whose **Lean
proof** field is **No**.
**Why:** the mathematics is already published, so our work is formalization, not
discovery. Open problems would mean doing original mathematics. The 66 that
already have Lean proofs cannot be claimed by us, since a Lean claim requires
the repo be owned by the claiming account.
**Reverse if:** the pool is exhausted or the rules change.

### D3 · Optimize for fastest plausible win, not prize tier
**2026-09-17.** Founder's call.
**Why:** tier is decided by a committee on undisclosed criteria, so it is not
directly steerable. Completion speed is. Zero awards have been granted, so being
early beats being ambitious. Bank one win, learn the review process, then aim higher.
**Reverse if:** the first submission is accepted smoothly and the machine is proven.

### D4 · Persistent REPL daemon instead of `lake build`
**2026-09-17.** `bin/check` talks to a long-lived `repl` process over a unix socket.
**Why:** measured on this machine, `lake env lean` costs 8 to 13 s per check
because it reloads Mathlib every time. The daemon keeps environments cached per
import set: about 25 s once, then ~25 ms per check. Roughly 400x on the inner
loop, which is where nearly all iterations happen.
**Reverse if:** the REPL proves unstable under load. Fallback is `lake env lean`.

### D5 · Gate the decomposition before proving anything
**2026-09-17.** `bin/skeleton` must print `DECOMPOSITION VALID` before Stage 3.
**Why:** the most expensive failure is farming out lemmas that do not actually
imply the theorem. Stubbing every lemma with `sorry` and compiling the main
theorem from the stubs turns that into a kernel fact obtainable in seconds.
**Reverse if:** never. This is the cheapest high-value check we have.

### D6 · The critic reviews the statement, not the proof
**2026-09-17.** Rejected the common design of an "independent critic" that reviews
a finished proof.
**Why:** once Lean compiles, the proof is correct; the kernel already said so, and
a reviewer adds nothing. The uncheckable step is the mapping from the paper's
English to the Lean statement. That is where criticism belongs, and it belongs
at the start, before a month is spent proving the wrong theorem.
**Reverse if:** never.

### D7 · Blind back-translation over side-by-side comparison
**2026-09-17.** The fidelity reviewer renders the Lean statement into English
*without access to the paper*, and we diff afterwards.
**Why:** an agent shown both and asked "do these match?" will rationalize a
match. One that has never seen the original cannot. Same cost, much better signal.
**Reverse if:** it produces too many false positives to be useful.

### D8 · Repo stays private until submission
**2026-09-17.** Develop private, flip public at claim time.
**Why:** the prize needs a public repo at claim time, not before. `plby` and
others are actively working this pool; telegraphing our target invites a race we
would lose.
**Reverse if:** we want collaborators, or the rules require earlier publication.

### D9 · Toolchain pinned to Mathlib's own
**2026-09-17.** Lean v4.35.0-rc2, matching `leanprover-community/mathlib4`'s
`lean-toolchain`. `lake-manifest.json` is committed.
**Why:** reviewers must be able to rebuild from a clean machine at a pinned
commit. Version drift is the most common reason a submitted proof fails to build.
**Reverse if:** we need a Mathlib feature only on a newer toolchain. Re-pin
deliberately and re-run `bin/verify`.

### D10 · Hard budgets with abandon rules, not rescue
**2026-09-17.** 40 h and $300 per problem, 8 retries per goal, 4 h for the
statement stage. Breach means abandon and write a post-mortem.
**Why:** a competitor's filename implies roughly 38 h and $219 for one Erdős
problem, so that is the realistic scale. With 287 candidates available, sunk cost
is the main threat to the strategy.
**Reverse if:** measured data from our own first problem says the benchmark is wrong.

### D11 · Remote repo created private under the claiming account
**2026-09-17.** `github.com/8-0-6/jsp-formal`, private.
**Why:** local-only git meant no backup. The prize requires the repo be owned by
the account that files the claim, so it is created under `8-0-6` from the start
rather than transferred later, since transfers complicate the ownership check.
Private for now per D8; flip to public at submission.
**Reverse if:** never private-vs-public is revisited at submission time only.
