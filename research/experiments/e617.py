"""Erdős #617, r=5 instance: does K_26 admit a 5-edge-coloring in which
every 6-subset of vertices contains all 5 colors?  (Conjecture: no.)
Equivalently: partition E(K_26) into 5 graphs, each with independence
number <= 5.  SAT encoding: x[e][c], exactly-one color per edge; for each
color c and each 6-subset S, at least one edge inside S has color c.
A model = counterexample disproving the conjecture (checkable finitely).
"""
import sys, time
from itertools import combinations
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

R, V = 5, 26
verts = list(range(V))
edges = list(combinations(verts, 2))
eidx = {e: i for i, e in enumerate(edges)}
pool = IDPool()
def x(e, c):
    return pool.id(("x", e, c))

def build():
    cls = []
    for e in edges:
        lits = [x(e, c) for c in range(R)]
        cls.append(lits)                                  # at least one color
        for c1 in range(R):
            for c2 in range(c1 + 1, R):
                cls.append([-x(e, c1), -x(e, c2)])        # at most one
    for c in range(R):
        for S in combinations(verts, 6):
            cls.append([x((a, b), c) for a, b in combinations(S, 2)])
    # mild symmetry breaking: colors of the 5 edges (0,1)..(0,5) fixed distinct
    for c in range(R):
        cls.append([x((0, c + 1), c)])
    return cls

if __name__ == "__main__":
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
    cls = build()
    print(f"vars={pool.top} clauses={len(cls)}", flush=True)
    s = Cadical195(bootstrap_with=cls)
    t0 = time.time()
    # cadical in pysat: no native timeout; rely on external timeout of the process
    res = s.solve()
    dt = time.time() - t0
    print(f"result={res} in {dt:.1f}s", flush=True)
    if res:
        model = set(l for l in s.get_model() if l > 0)
        coloring = {}
        for e in edges:
            for c in range(R):
                if x(e, c) in model:
                    coloring[e] = c
        import json
        json.dump({f"{a},{b}": c for (a, b), c in coloring.items()},
                  open("e617_witness.json", "w"))
        print("WITNESS WRITTEN: e617_witness.json  <-- DISPROOF of Erdos 617")
