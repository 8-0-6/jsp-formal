# JSPFormal

Lean 4 formalizations targeting the [Justin Sun Prize](https://www.hejustinsun.com)
problem bank.

Every theorem listed in `targets.txt` is machine-verified: it compiles, contains
no `sorry`, `admit`, `native_decide`, or custom axioms, and depends only on
Lean's three standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

## Verify

```bash
./bin/verify
```

Exit code 0 means every listed theorem is complete and clean. This is the same
command CI runs on a clean machine.

## Build from scratch

Requires [elan](https://github.com/leanprover/elan).

```bash
lake exe cache get   # download prebuilt Mathlib, do not compile it
lake build
./bin/verify
```

Toolchain and Mathlib revision are pinned in `lean-toolchain` and
`lake-manifest.json`.

## Development

```bash
bin/check <file.lean>      # fast incremental check (~25 ms warm)
bin/skeleton <file> <Thm>  # verify a proof decomposition actually composes
bin/status                 # progress across problems
```

Working rules are in [AGENTS.md](AGENTS.md). Strategy, pipeline, decisions, and
progress are in [docs/](docs/).
