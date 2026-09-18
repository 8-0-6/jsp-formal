#!/usr/bin/env python3
"""Parse `#print axioms` output and enforce the standard-axiom whitelist.

Reads Lean's output on stdin. Lean wraps long lines, so the whole text is
normalised to a single whitespace-separated string before matching; a regex
anchored to line ends silently fails on long theorem names.

Exit 0 only if every target reports exactly the three standard axioms (or none),
and the number of reports matches the number of targets.
"""
import re, sys

ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
G, R, C = "\033[32m", "\033[31m", "\033[0m"

expected = int(sys.argv[1]) if len(sys.argv) > 1 else 0
raw = sys.stdin.read()
norm = re.sub(r"\s+", " ", raw)

if re.search(r"\berror\b", norm) or "sorryAx" in norm:
    print(f"{R}AXIOM AUDIT FAILED (error or sorryAx){C}")
    for line in raw.splitlines():
        if "error" in line or "sorryAx" in line:
            print("  " + line.strip()[:200])
    sys.exit(1)

seen, bad = [], []
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", norm):
    name = m.group(1)
    ax = {a.strip() for a in m.group(2).split(",") if a.strip()}
    seen.append(name)
    extra = ax - ALLOWED
    if extra:
        bad.append((name, sorted(extra)))
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", norm):
    seen.append(m.group(1))

for name in seen:
    print(f"  {name}")
if bad:
    print(f"{R}NON-STANDARD AXIOM DEPENDENCY{C}")
    for name, extra in bad:
        print(f"  {R}{name}{C} depends on: {', '.join(extra)}")
    sys.exit(1)
if expected and len(seen) != expected:
    print(f"{R}AUDIT INCOMPLETE: {len(seen)} reports for {expected} targets{C}")
    sys.exit(1)
print(f"{G}{len(seen)}/{expected or len(seen)} targets depend only on standard axioms{C}")
