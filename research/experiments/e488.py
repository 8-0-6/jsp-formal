"""Erdős #488 counterexample search.

Conjecture: for finite A, B = multiples of A, F(x)=|B∩[1,x]|:
  for all m > n >= max(A):  F(m)/m < 2 F(n)/n.
Witness = (A, n, m) with n*F(m) >= 2*m*F(n)   (>= because inequality is strict).

r(A) = max_{m>n>=N} [F(m)/m] / [F(n)/n], N=max(A), estimated on a sieve window.
"""
import numpy as np
from itertools import combinations
from math import gcd

def dens_array(A, M):
    isB = np.zeros(M + 1, dtype=bool)
    for a in A:
        isB[a::a] = True
    F = np.cumsum(isB)
    return F  # F[x] = F(x), F[0]=0

def max_ratio(A, M=None, mult=64, cap=4_000_000):
    A = sorted(set(A)); N = A[-1]
    if M is None:
        M = min(max(mult * N, 20000), cap)
    F = dens_array(A, M)
    x = np.arange(M + 1, dtype=np.float64)
    d = F[N:] / x[N:]                       # densities for n = N..M
    runmin = np.minimum.accumulate(d)
    r = d[1:] / runmin[:-1]                 # ratio at m = N+1..M vs best n<m
    i = int(np.argmax(r))
    m = N + 1 + i
    # recover the n achieving the running min before m
    j = int(np.argmin(d[:i + 1]))           # first index of min among n<=m-1
    n = N + j
    return float(r[i]), n, m, F

def exact_check(A, n, m):
    A = sorted(set(A))
    F = dens_array(A, m)
    lhs, rhs = n * int(F[m]), 2 * m * int(F[n])
    return lhs - rhs, int(F[n]), int(F[m])   # >= 0 means counterexample

# ---------- Stage 1: exhaustive tiny ----------
def stage1(maxN=13, M=6000):
    best = (0.0, None)
    hits = []
    pool = list(range(2, maxN + 1))          # exclude 1: A∋1 -> B=all, ratio 1
    for k in range(1, 6):
        for A in combinations(pool, k):
            r, n, m, _ = max_ratio(list(A), M=M)
            if r > best[0]:
                best = (r, (A, n, m))
            if r > 1.999:
                diff, Fn, Fm = exact_check(list(A), n, m)
                hits.append((A, n, m, diff, Fn, Fm))
    return best, hits

# ---------- Stage 2: window family ----------
def stage2():
    out = []
    for N in (50, 100, 200, 500, 1000, 2000, 4000):
        A = list(range(N // 2 + 1, N + 1))
        r, n, m, _ = max_ratio(A, mult=40, cap=2_000_000)
        out.append((N, r, n, m))
    return out

# ---------- Stage 3: annealing over divisors of a smooth L ----------
def divisors(L):
    ds = [1]
    t, out = L, {}
    f = 2
    while f * f <= t:
        while t % f == 0:
            out[f] = out.get(f, 0) + 1; t //= f
        f += 1
    if t > 1: out[t] = out.get(t, 0) + 1
    for p, e in out.items():
        ds = [d * p**i for d in ds for i in range(e + 1)]
    return sorted(ds)

def stage3(L, lo_frac=0.05, time_s=60, seed=0):
    import time, random
    rng = random.Random(seed)
    cand = [d for d in divisors(L) if d >= max(2, int(lo_frac * L)) and d <= L]
    if len(cand) < 3: return None
    cur = set(rng.sample(cand, min(len(cand), rng.randint(3, max(4, len(cand) // 2)))))
    def score(S):
        if not S: return 0.0, 0, 0
        r, n, m, _ = max_ratio(sorted(S), mult=24, cap=1_500_000)
        return r, n, m
    cur_r, *_ = score(cur)
    best = (cur_r, frozenset(cur), None, None)
    t0 = time.time(); T = 0.05
    while time.time() - t0 < time_s:
        d = rng.choice(cand)
        nxt = set(cur); (nxt.remove if d in nxt else nxt.add)(d)
        if not nxt: continue
        r, n, m = score(nxt)
        if r > cur_r or rng.random() < pow(2.718, (r - cur_r) / T):
            cur, cur_r = nxt, r
            if r > best[0]:
                best = (r, frozenset(nxt), n, m)
        T = max(0.005, T * 0.999)
    return best

if __name__ == "__main__":
    import sys
    stage = sys.argv[1] if len(sys.argv) > 1 else "1"
    if stage == "1":
        best, hits = stage1()
        r, w = best
        print(f"stage1 best ratio {r:.6f} at A={w[0]} n={w[1]} m={w[2]}")
        print(f"exact hits (diff>=0 means counterexample): {hits if hits else 'none'}")
    elif stage == "2":
        for N, r, n, m in stage2():
            print(f"window N={N:5d}  ratio={r:.6f}  (n={n}, m={m})")
    elif stage == "3":
        import sys
        L = int(sys.argv[2]); t = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        for seed in range(int(sys.argv[4]) if len(sys.argv) > 4 else 3):
            b = stage3(L, time_s=t, seed=seed)
            if b:
                r, S, n, m = b
                print(f"L={L} seed={seed} best={r:.6f} |A|={len(S)} n={n} m={m} A={sorted(S)[:12]}{'...' if len(S)>12 else ''}")
                if r > 1.999 and n and m:
                    print("   exact:", exact_check(sorted(S), n, m))

# ---------- Stage 4: systematic small-|A| sweep ----------
def stage4():
    from itertools import combinations
    best = (0.0, None)
    hits = []
    def consider(A):
        nonlocal best
        r, n, m, _ = max_ratio(list(A), mult=30, cap=200_000)
        if r > best[0]:
            best = (r, (tuple(A), n, m))
        if r > 1.9999:
            hits.append((tuple(A), n, m, exact_check(list(A), n, m)))
    # pairs up to 600
    for A in combinations(range(2, 601), 2):
        consider(A)
    print(f"after pairs: best={best[0]:.7f} at {best[1]}")
    # triples up to 130
    for A in combinations(range(2, 131), 3):
        consider(A)
    print(f"after triples: best={best[0]:.7f} at {best[1]}")
    # structured quadruples: multiples of 6 up to 240, plus divisors of smooth numbers
    pool6 = [x for x in range(6, 241, 6)]
    for A in combinations(pool6, 4):
        consider(A)
    print(f"after 6-multiples quads: best={best[0]:.7f} at {best[1]}")
    print("hits:", hits if hits else "none")
