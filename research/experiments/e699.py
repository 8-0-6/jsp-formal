"""Erdős #699 counterexample search.

Conjecture (Erdős-Szekeres): for all 1 <= i < j <= n/2 there is a prime
p >= i with p | gcd(C(n,i), C(n,j)).

Counterexample: (n, i, j) such that NO prime p >= i divides both binomials.
Method: primes p >= i dividing C(n,i) all divide n-k for some k < i (since
p >= i > k rules out denominator primes); p | C(n,r) iff adding r and n-r in
base p carries (Kummer). A j-counterexample = j in (i, n/2] passing the
no-carry test for every p in Q_i(n) = {p >= i : p | C(n,i)}.
No-carry(j, n, p)  <=>  every base-p digit of j is <= the digit of n.
"""
import sys
import numpy as np

def build_spf(M):
    spf = np.zeros(M + 1, dtype=np.int64)
    spf[1] = 1
    for p in range(2, M + 1):
        if spf[p] == 0:
            spf[p::p][spf[p::p] == 0] = p
    return spf

def factor(x, spf):
    out = set()
    while x > 1:
        p = int(spf[x]); out.add(p)
        while x % p == 0:
            x //= p
    return out

def digits(x, p):
    d = []
    while x:
        d.append(x % p); x //= p
    return d

def no_carry(j, n, p):
    dn, dj = digits(n, p), digits(j, p)
    if len(dj) > len(dn):
        return False
    return all(dj[t] <= dn[t] for t in range(len(dj)))

def box_size(n, p, half):
    # |{ j in [0, n/2] : digitwise j <= n base p }| upper bound: prod(d+1)
    prod = 1
    for d in digits(n, p):
        prod *= d + 1
        if prod > 10**7:
            return prod
    return prod

def enum_box(n, p, half, cap):
    """Enumerate j with digitwise j <= n base p, j <= half. Odometer."""
    dn = digits(n, p)
    L = len(dn)
    out = []
    cur = [0] * L
    while True:
        j = 0
        for t in range(L - 1, -1, -1):
            j = j * p + cur[t]
        if j <= half:
            out.append(j)
            if len(out) > cap:
                return None
        # increment odometer (digit t bounded by dn[t])
        t = 0
        while t < L and cur[t] == dn[t]:
            cur[t] = 0; t += 1
        if t == L:
            return out
        cur[t] += 1

def search(n_lo, n_hi, i_max=5, box_cap=300_000):
    spf = build_spf(n_hi + 2)
    hits = []
    near = []   # j failing all but one prime, for diagnostics
    for n in range(n_lo, n_hi + 1):
        half = n // 2
        # prime pool per i: primes p >= i dividing some n-k, k < i, with carry at (i, n-i)
        facs = [factor(n - k, spf) for k in range(0, i_max)]
        for i in range(1, i_max + 1):
            if i >= half:
                continue
            Q = set()
            for k in range(i):
                for p in facs[k]:
                    if p >= max(i, 2) and not no_carry(i, n, p):
                        Q.add(p)
            if not Q:
                # C(n,i) itself has no prime >= i -> (n, i, any j) is already
                # a counterexample if some j exists; gcd has no prime >= i.
                hits.append((n, i, None, "Q empty"))
                continue
            # enumerate the smallest box among Q, test against the rest
            q0 = min(Q, key=lambda p: box_size(n, p, half))
            if box_size(n, q0, half) > box_cap:
                continue   # too expensive; skip (record nothing)
            cand = enum_box(n, q0, half, box_cap)
            if cand is None:
                continue
            rest = [p for p in Q if p != q0]
            for j in cand:
                if j <= i:
                    continue
                bad = [p for p in rest if not no_carry(j, n, p)]
                # j is a counterexample iff no p in Q divides C(n,j):
                # q0 already fails by construction? NO: cand = box of q0 =
                # no-carry j's, i.e. q0 does NOT divide C(n,j). Good.
                if not bad:
                    hits.append((n, i, j, sorted(Q)))
                elif len(bad) == 1 and len(Q) > 2:
                    near.append((n, i, j, bad[0], len(Q)))
    return hits, near

if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    hits, near = search(lo, hi)
    print(f"range [{lo},{hi}]  hits={len(hits)}  near={len(near)}")
    for h in hits[:20]:
        print("HIT:", h)
    for t in near[:10]:
        print("near:", t)
