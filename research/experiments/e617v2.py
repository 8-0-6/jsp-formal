"""e617 v2: monotone symmetry breaking + per-color cardinality [55,105]."""
import sys, time, json
from itertools import combinations
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

R, V = 5, 26
verts = list(range(V))
edges = list(combinations(verts, 2))
pool = IDPool()
def x(e, c): return pool.id(("x", e, c))

cls = []
for e in edges:
    cls.append([x(e, c) for c in range(R)])
    for c1 in range(R):
        for c2 in range(c1 + 1, R):
            cls.append([-x(e, c1), -x(e, c2)])
for c in range(R):
    for S in combinations(verts, 6):
        cls.append([x((a, b), c) for a, b in combinations(S, 2)])
# monotone colors along vertex 0's edges (kills color + partial vertex symmetry)
for v in range(1, V - 1):
    for c1 in range(R):
        for c2 in range(c1):
            cls.append([-x((0, v), c1), -x((0, v + 1), c2)])
# provable per-color size bounds: 55 <= |H_c| <= 325 - 4*55 = 105
for c in range(R):
    lits = [x(e, c) for e in edges]
    cls += CardEnc.atleast(lits=lits, bound=55, vpool=pool, encoding=EncType.seqcounter).clauses
    cls += CardEnc.atmost(lits=lits, bound=105, vpool=pool, encoding=EncType.seqcounter).clauses

print(f"vars={pool.top} clauses={len(cls)}", flush=True)
s = Cadical195(bootstrap_with=cls)
t0 = time.time()
res = s.solve()
print(f"result={res} in {time.time()-t0:.1f}s", flush=True)
if res:
    model = set(l for l in s.get_model() if l > 0)
    col = {f"{a},{b}": c for (a, b) in edges for c in range(R) if x((a, b), c) in model}
    json.dump(col, open("e617_witness.json", "w"))
    print("WITNESS WRITTEN <-- DISPROOF of Erdos 617", flush=True)
