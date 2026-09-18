# Screen of computation-adjacent open problems (2026-09-18)

Founder-approved 4-hour screen. Question: among open Erdős problems that a
finite computation could settle, is there any whose witness our compute could
plausibly find and our pipeline could certify in Lean? A hit would be a
"mathematical solution + Lean" claim, the strongest role, on a problem nobody
can snipe (because the mathematics itself would be ours).

## Frame, before the list

These problems are open BECAUSE the computation has not settled them. For a
falsifiable problem we only win if the conjecture is actually false and the
counterexample sits beyond everyone's past searches but within ours. For a
verifiable problem we only win if it is true and the witness is findable. That
window is narrow by construction. Everything below is a lottery ticket, and
the recommendation caps total spend accordingly.

The pool: erdosproblems.com marks 41 open problems as decidable (9),
falsifiable (25) or verifiable (7). Our 09-17 crawl stored `status: null` for
all 41 (the crawler did not know these labels), which is why the scout run
never saw this band. Statements were recovered from formal-conjectures
docstrings and the llm-hunter attack archive; page-level status via search
snippets (site blocked from this environment).

## Kills, with reasons

Killed on prior search depth (counterexample effectively ruled out to large
bounds, or believed true with heavy evidence): #242 Erdős-Straus (searched
past 10^14), #398 Brocard (searched past 10^9), #375 Grimm, #364 consecutive
powerful triples, #64 Erdős-Gyárfás power-of-2 cycles ($1000), #107
Erdős-Szekeres ($500, SAT-searched by the community), #167 Tuza, #583
Gallai path partitions, #743 tree packing, #779 Deaconescu (verified to
n=1000, heuristic failure probability vanishing), #723 projective plane of
order 12 (a decades-scale search), #982 and #1082 distance geometry
(regular-polygon extremals believed tight), #23, #628, #1020 (Erdős matching
conjecture), #672 (perfect powers in APs, Győry et al. closed the small
cases), #7 odd covering systems (existence doubted, structured searches
exhausted), #366 (heuristic count of solutions converges; easy range empty).

Killed on certificate cost, independent of findability (our rules ban
native_decide, so the witness check must run in the kernel): #128 (checking
a witness needs all C(n, n/2) induced subgraphs), #647 (witness n likely
at least 10^9 and the claim quantifies over every m < n, meaning ~n
factorizations verified in kernel), #114 lemniscate lengths (certifying arc
length inequalities needs verified numerics we do not have; Tao settled the
large-degree case anyway), #1041 (same arc-length problem), #506 (real
geometry enumeration).

Killed on category signals without a page read (budget call): #19 ($500
chromatic), #556, #580, #547, #551 (Ramsey values: certifying an upper bound
means checking all colorings, and Mathlib has no Ramsey theory), #742
Murty-Simon (known for n above an astronomical bound; the finite gap is not
reachable), #475 (believed-true ordering conjecture, per-instance cost
factorial), #848, #993, #287 (blocked by a Bertrand-type obstruction:
near-consecutive denominator chains cannot avoid a lone large prime), #458
(violation needs two prime squares inside one prime gap of size ~2 sqrt(p):
far beyond every known gap), #488 note below, #617 note below, #699 note
below.

## The three tickets worth anything

### 1. Erdős #488. Density of a set of multiples cannot double after max(A)

For finite A, B = multiples of A, F(x) = |B ∩ [1,x]|. Conjecture: for all
m > n >= max(A), F(m)/m < 2 F(n)/n. Open; direction genuinely unclear; not a
famous believed-true target. The adjacent literature (Ahlswede-Khachatrian)
disproved other Erdős conjectures about sets of multiples with clever
constructions, so this genre yields.

- Witness if false: a finite A plus one pair (n, m). Pure arithmetic.
- Certificate: F via inclusion-exclusion over subsets of A, exact rationals,
  kernel-friendly (2^|A| floor terms; |A| <= 20 keeps it around 10^6 terms).
  JSP-000301-grade.
- Search: structured design (prime powers, uneven residues mod lcm(A)),
  maximize d(m)/d(n) numerically, then exact-check. Bounded, ours to run.
- Risk: the ratio may provably cap below 2 for reasons nobody wrote down.
  One GPT attack file exists; no evidence of a systematic search.

### 2. Erdős #699. gcd of two binomial coefficients has a prime factor >= i

Erdős-Szekeres: for 1 <= i < j <= n/2, some prime p >= i divides
gcd(C(n,i), C(n,j)). Open.

- Witness if false: (n, i, j). For small i the check is tiny: factor
  C(n,i) (polynomial in n), then show each prime >= i fails Kummer's
  carry criterion for C(n,j). Kernel-perfect digit arithmetic.
- Precedent: #387, the same genre, fell in 2026 to exactly this kind of
  hunt (explicit n = 99215 sub-case, then the BNPZ paper).
- Risk: this genre is being actively mined right now (three arXiv papers in
  two months on binomial divisor problems). If a cheap counterexample
  existed, that crowd may find it first. Direction unknown.

### 3. Erdős #617, the r = 5 instance. Balanced coloring of K_26

The conjecture (proved r = 3, 4; open r >= 5) says every 5-coloring of
K_26 has 6 vertices missing a color. A counterexample is a partition of the
325 edges into 5 graphs, each with independence number <= 5. One SAT run.

- Witness if SAT: one explicit coloring; check = 230,230 six-subsets per
  color, bitmask decidable, JSP-000301 playbook.
- Risk: r = 3 and 4 were proved impossible, so the believed answer is
  UNSAT, and UNSAT gives us nothing claimable. This is the purest lottery
  of the three: a few CPU-hours for a full disproof of a named conjecture
  if the pattern breaks.

Rejected from the shortlist at the last step: #307 (Barbeau product of
prime reciprocal sums). Perfect certificate shape, but a 2026 paper with its
own Lean repo (Bonfioli, ElVec1o/erdos307) already proves any witness needs
at least 60 disjoint primes satisfying exact divisor-sum identities, which
puts it outside brute reach, and that author is already formalizing around
the problem.

## Recommendation

1. Cap the whole adventure at 15 hours of compute experiments and zero Lean
   until a witness is in hand. The #969 gate from the deep-dive still rules
   all real spend.
2. Order: #488 first (best ratio of unknown-direction to search cost, least
   crowd), #699 second (best certificate, worst crowd), #617 as background
   SAT whenever a machine is idle.
3. Any hit converts immediately: witness, then statement, then the standard
   pipeline. A hit is a solver-plus-Lean claim on a problem that cannot be
   sniped, which is the only claim shape left with real upside.
4. If all three come back empty inside the cap, stop. Empty is the expected
   outcome and does not merit a second budget.
