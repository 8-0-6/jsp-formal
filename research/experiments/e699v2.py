"""e699 v2: n to 1e7, i<=8, smooth-triple corner deep-dive, skip sampling."""
import e699, time, random, json
import numpy as np

LIM = 10_000_000
CH = 500_000
rng = random.Random(1)
small_primes = [p for p in range(2, 500) if all(p % q for q in range(2, int(p**0.5) + 1))]

def largest_pf_under(x, bound=500):
    for p in small_primes:
        while x % p == 0:
            x //= p
        if x == 1: return True
    return x == 1

t0 = time.time()
spf = e699.build_spf(min(LIM + 2, 10_000_002))
print(f"spf built t={time.time()-t0:.0f}s", flush=True)
hits, smooth_hits, near_total, skips = [], [], 0, 0
for lo in range(1_000_001, LIM + 1, CH):
    hi = min(lo + CH - 1, LIM)
    for n in range(lo, hi + 1):
        half = n // 2
        facs = [e699.factor(n - k, spf) for k in range(8)]
        smooth = largest_pf_under(n * (n - 1) * (n - 2))
        for i in range(1, 9):
            if i >= half: continue
            Q = set()
            for k in range(i):
                for p in facs[k]:
                    if p >= max(i, 2) and not e699.no_carry(i, n, p):
                        Q.add(p)
            if not Q:
                hits.append((n, i, None, "Q empty")); continue
            q0 = min(Q, key=lambda p: e699.box_size(n, p, half))
            cap = 5_000_000 if (smooth and i <= 3) else 300_000
            if e699.box_size(n, q0, half) > cap:
                skips += 1
                continue
            cand = e699.enum_box(n, q0, half, cap)
            if cand is None:
                skips += 1; continue
            rest = [p for p in Q if p != q0]
            for j in cand:
                if j <= i: continue
                if all(e699.no_carry(j, n, p) for p in rest):
                    rec = (n, i, j, sorted(Q))
                    (smooth_hits if smooth else hits).append(rec)
                    print("HIT:", rec, flush=True)
    print(f"[{lo},{hi}] t={time.time()-t0:.0f}s hits={len(hits)+len(smooth_hits)} skips={skips}", flush=True)
print(f"FINAL hits={hits} smooth_hits={smooth_hits} skips={skips}", flush=True)
json.dump({"hits": hits, "smooth": smooth_hits}, open("e699v2_hits.json", "w"))
