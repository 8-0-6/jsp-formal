<h1 align="center">JSPFormal</h1>

<p align="center">
  <em>Machine-verified formalizations of settled results in number theory, in Lean 4.</em>
</p>

<p align="center">
  <a href="https://github.com/8-0-6/jsp-formal/actions/workflows/verify.yml">
    <img alt="verify" src="https://github.com/8-0-6/jsp-formal/actions/workflows/verify.yml/badge.svg">
  </a>
  <img alt="Lean" src="https://img.shields.io/badge/Lean-v4.35.0--rc2-blue">
  <img alt="Mathlib" src="https://img.shields.io/badge/Mathlib-pinned-blue">
  <img alt="sorry-free" src="https://img.shields.io/badge/sorry--free-verified-brightgreen">
  <img alt="axioms" src="https://img.shields.io/badge/axioms-standard%20three%20only-brightgreen">
</p>

---

## What this is

A small, deliberately over-engineered repository for turning published
mathematical results into proofs a machine can check end to end.

The mathematics here is not new. Every result formalized in this repository was
settled in the literature, sometimes decades ago, and is credited to the
mathematician who settled it. What this repository contributes is the
*formalization*: a statement faithful to the original, a complete proof, and a
verification record strong enough that a sceptical reader does not have to take
anything on trust.

## The verification standard

A Lean proof that compiles is not, by itself, evidence of much. A file can be
`sorry`-free, pass CI, and still prove something vacuous, something weaker than
the paper claimed, or something that quietly depends on an axiom nobody agreed
to. Every safeguard below exists because one of those failure modes is real.

**Mechanical gates, enforced by `bin/verify` on every commit:**

| Gate | What it rules out |
| :--- | :--- |
| Build from a clean checkout | Environment drift; a proof only its author can rebuild |
| Forbidden-construct scan | `sorry`, `admit`, `native_decide`, custom `axiom`, `unsafe`, `partial def`, `@[implemented_by]`, `Lean.ofReduceBool` |
| `#print axioms` on every listed theorem | Anything depending on more than `propext`, `Classical.choice`, `Quot.sound` |
| Explicit target manifest | Silent scope loss. A theorem not listed in `targets.txt` is not verified, and an empty manifest is treated as a failure |

The gate is **negative-tested**. It is checked against a planted `sorry`, a
`sorry` laundered through a custom `axiom`, and a target theorem silently
deleted. Each is caught, most by two independent layers. A gate nobody has tried
to break is not evidence.

**Human-level checks, recorded per result in `problems/<ID>/FIDELITY.md`:**

- **Anti-degeneracy theorems.** Every bespoke definition is accompanied by proofs
  that it is discriminating, so that a definition which had drifted to "always
  true" could not silently make the headline result trivial.
- **Cross-validation against independent formalizations.** Where another project
  has formalized the same notion, the two definitions are proved equivalent in
  Lean rather than compared by eye.
- **Blind back-translation.** The Lean statement is rendered back into English by
  a reader with no access to the source paper, and the result is diffed against
  the original wording. A reviewer shown both and asked "do these match?" will
  rationalize a match; one who never saw the original cannot.
- **Adversarial review.** A reviewer is instructed to build the strongest possible
  case for rejection. Findings are recorded with their adjudication, including the
  ones that were upheld.

The intent is that the weakest link is stated in the repository before a reader
has to find it.

## Results

### Consecutive powerful integers

> A positive integer is **powerful** when every prime dividing it divides it at
> least twice. Must two consecutive powerful integers include a perfect square?

**No.** `12167 = 23³` and `12168 = 2³ · 3² · 13²` are consecutive, both powerful,
and both lie strictly between `110² = 12100` and `111² = 12321`, so neither is a
square.

```lean
theorem answer_is_no :
    ¬ ∀ n : ℕ, 0 < n → Powerful n → Powerful (n + 1) → IsSquare n ∨ IsSquare (n + 1)
```

Formalized in [`JSPFormal/JSP000301/Statement.lean`](JSPFormal/JSP000301/Statement.lean),
with 18 audited theorems including a satisfiability witness, anti-degeneracy
checks on both `Powerful` and `IsSquare`, and a proof that this definition of
`Powerful` agrees for every `n` with the independent formulation
`∀ p ∈ n.primeFactors, p ^ 2 ∣ n` used in `google-deepmind/formal-conjectures`.

**Attribution.** The mathematics is **Solomon W. Golomb's**, from *Powerful
numbers*, Amer. Math. Monthly 77 (1970), 848-855. This repository contributes the
Lean formalization only and makes no claim on the mathematical result.

**Stated limitations.** Golomb's paper is paywalled and has not been read
directly; the attribution follows
[erdosproblems.com](https://www.erdosproblems.com/latex/365), and no page or
theorem number inside that paper is asserted. Sources disagree on its page range
(848-852 versus 848-855). The formalization addresses only the question above and
says nothing about counting, density, or asymptotics, so it bears on no part of
the related and still-open counting question.

Full provenance in [`problems/JSP-000301/PROBLEM.md`](problems/JSP-000301/PROBLEM.md),
fidelity record in [`problems/JSP-000301/FIDELITY.md`](problems/JSP-000301/FIDELITY.md).

## Reproducing

Requires [elan](https://github.com/leanprover/elan). Mathlib is downloaded
prebuilt rather than compiled.

```bash
lake exe cache get
lake build
./bin/verify
```

`./bin/verify` exits 0 only if every theorem in `targets.txt` builds, contains no
forbidden construct, and depends on nothing beyond the three standard axioms. CI
runs exactly this command on a clean machine.

## Working environment

Correctness is the point, but iteration speed is what makes thorough checking
affordable, so the harness is built around it.

| Command | Purpose | Latency |
| :--- | :--- | :--- |
| `bin/check <file>` | Incremental check against a persistent Lean REPL | **~25 ms** warm |
| `bin/skeleton <file> <Thm>` | Proves a proof decomposition actually composes, before any effort is spent filling it in | seconds |
| `bin/verify` | The full gate | minutes |
| `bin/status` | Per-result progress, dependency tree, budget | instant |

`bin/check` holds Mathlib resident in memory and caches one environment per
import set. Measured on the reference machine, the same check costs 8 to 13
seconds through `lake env lean` and about 25 milliseconds through the daemon. It
also guards against a trap in the underlying REPL, which answers an unresolvable
import with a valid-looking empty environment and no error, turning every
subsequent message into noise.

`bin/skeleton` exists because the most expensive mistake in a large proof is a
decomposition that does not compose. Stubbing every lemma and asking Lean whether
the main theorem still follows converts that from a judgement call into a fact,
obtainable in seconds rather than after the work is done.

## Repository layout

```
JSPFormal/            Verified Lean source. Everything here is built and audited.
targets.txt           The manifest bin/verify certifies. Not listed means not verified.
problems/<ID>/        Provenance, fidelity record, and per-result state
bin/                  check · skeleton · verify · status · new-problem
harness/              Lean REPL daemon and axiom auditor
docs/                 Method, pipeline, decision log, progress
```

[`AGENTS.md`](AGENTS.md) states the working rules, foremost among them that a
locked statement is never weakened to make a proof close. If a proof will not
close, the proof is wrong or the problem was a bad choice; the theorem does not
quietly shrink to meet it.

[`docs/DECISIONS.md`](docs/DECISIONS.md) records every non-obvious choice with its
reasoning and the evidence that would reverse it.

## License

Code: [Apache 2.0](LICENSE).
