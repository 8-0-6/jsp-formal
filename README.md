# JSPFormal

Lean 4 formalizations targeting the [Justin Sun Prize](https://www.hejustinsun.com)
problem bank.

## Verify

```bash
./bin/verify
```

Builds the project, rejects `sorry`/`admit`/`native_decide`/custom axioms, and
audits every theorem in `targets.txt` with `#print axioms`. Exit code 0 means
every listed theorem is complete and depends only on `propext`,
`Classical.choice`, and `Quot.sound`.

## Setup

Requires [elan](https://github.com/leanprover/elan). Then:

```bash
lake exe cache get && lake build
```

See [AGENTS.md](AGENTS.md) for working rules.
