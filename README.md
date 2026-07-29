# Exact Nullstellensatz Certificates and Finite Presentations for Critical Graph Families

[![DOI](https://zenodo.org/badge/1316275748.svg)](https://zenodo.org/badge/latestdoi/1316275748)

We construct **exact rational Nullstellensatz certificates** of non-k-colorability for infinite families of vertex-critical graphs, and we compress entire infinite families into **finite presentations** — finite label alphabets and finite systems of equations whose single exact solution instantiates a certificate for every member of the family. We complement these constructions with **adversarial campaigns** designed to kill our own conjectures, and we publish both the confirmations and the failures.

**The long-term object of this program is the complexity of 3-colorability on P₈-free graphs** — the open frontier of the Pₜ-free hierarchy (polynomial for P₇-free; NP-completeness known for no t). We conjecture a *degree-4 collapse*: every P₈-free non-3-colorable graph admits a Nullstellensatz certificate of degree ≤ 4 in the cube-roots encoding. If true, this places the class not only in P but in **NC²**. We treat this as a concrete, falsifiable laboratory for the wider P vs NP landscape, and we are not shy about that ambition — we simply let the statements carry it: every claim below can be killed by a computation, and we say by which one.

## Claims and their status

Status convention (used throughout): **[T-ℚ]** proved by exact rational computation, verified over ℚ · **[C-p]** computational, concordant over ≥ 2 large primes (residual-certified) · **[L]** written lemma with an explicit list of remaining verifications · **[CONJ]** conjecture.

| # | Statement | Status | Where |
|---|---|---|---|
| 1 | **Theorem 1.** The Pokrovskiy family G(q,3) (4-critical circulants, n = 3q+1) admits degree-4 certificates for all q, governed by a finite law of 77 rational constants. | [T-ℚ] small q, [C-p] law | `docs/fr/recueil-theoremes.md` |
| 2 | **Theorem 2.** The triangle-free 4-critical family ZJ(k) (n = 3k+10) admits degree-4 certificates for all k, via an orbit-normalized label system (ν-law, parity strata). | [T-ℚ]+[C-p] | `docs/fr/recueil-theoremes.md` |
| 3 | **Theorem 3.** The Cameron–Hoàng family G_CH(q,4) (5-critical, n = 4q+1, modulus 4) admits degree-5 certificates for all q, captured by a **finite presentation**: 6,487 n-independent labels, 6,186 equations (closed from q = 10), and two rational vectors V_even, V_odd (denominators dividing 2⁴) — solutions are exactly 2-periodic in q, with a proven arithmetic cause (⌊n/2⌋ = 2q mod 4). Verified bit-for-bit on twelve consecutive orders, q = 3…12, including three blind predictions. | [T-ℚ] for q ≤ 12; [L] for all q | `docs/fr/theoreme-1bis.md`, `docs/fr/lemme-C-mod4.md`, `docs/fr/additif-v2.md` |
| 4 | **Collapse Conjecture** (P₈-free degree-4 collapse). | [CONJ] | `docs/fr/plan-refutation.md` |
| 5 | Adversarial campaign on the wild class: 170 instances (random hunts n = 14–17 beyond any census, edge-critical cores, densified long-path instances) — **170/170 conform**, zero refutation seeds. | [C-p] | `docs/fr/plan-refutation.md`, `results/refute_hunt_n*.json` |
| 6 | **NC² corollary.** If the Collapse Conjecture holds, 3-colorability of P₈-free graphs is in NC² (the degree-4 test itself is unconditionally in NC²; the P₈-free promise is testable in AC⁰). | conditional | `docs/fr/additif-v2.md` |

## Try to kill these results

We consider a day well spent when it renders something impossible. The fastest routes to refuting us:

```bash
# Kill Theorem 3: find a q where the label system rejects the predicted vector.
# (Any FAILURE verdict, or an exact solve differing from V_{q mod 2}, refutes the closure.)
cd lab && cp ../results/j2_labels_q7.json ../results/j2_labels_q8.json results/ 2>/dev/null || mkdir -p results && cp ../results/j2_labels_q*.json results/
python j2_predict.py 13        # warning: the system build is heavy (~32 h, ~27 GB at q = 13)

# Kill the Collapse Conjecture: exhibit one P₈-free non-3-colorable graph
# whose FULL degree-{1,4} system is insolvable (two concordant primes flag it).
python refute_hunt.py 18 4000 12345 8 4     # any "INSOLVABLE" line is a refutation seed

# Reproduce Theorem 3 from nothing (no cached data, exact over Q, ~minutes for small q):
python j2_labels.py 3 4        # expected: SOLVABLE EXACT, LCM 48 / 48, then compare with results/
```

Any insolvability finding is subject to the verification protocol of `docs/fr/plan-refutation.md` § (iii) (multi-prime concordance, exact rational verification) — we commit to applying it to refutations of our own claims with the same rigor as to confirmations.

## Repository layout

- `docs/fr/` — the research documents (currently in French; English translations in progress). `docs/en/results.md` states the main results in English.
- `lab/` — the complete toolchain: system builders, exact solvers (dense RREF over ℚ via CRT + rational reconstruction; sparse residual-certified Wiedemann), label-quotient machinery, adversarial hunts. Pure Python + numpy. Run from inside `lab/`; outputs go to `lab/results/` and never overwrite the frozen registries at the repository root.
- `results/` — frozen JSON registries backing every numerical claim above (label-system solutions q = 3…12, blind-prediction verdicts, the 170-verdict adversarial campaign, the census registry). These files are the evidence; the scripts regenerate them.

## Reproducibility

Everything is exact arithmetic (ℚ) or two-prime certified. The full q = 3…12 chain of Theorem 3 has been reproduced **bit-for-bit on two independent machines and operating systems**. No floating point enters any claim.

## Licensing

Code (`lab/`): [MIT](LICENSE). Documents and data (`docs/`, `results/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cite via `CITATION.cff`.

## Contact

Open an issue — especially to report a refutation. We will consign it with the same ink as our successes.
