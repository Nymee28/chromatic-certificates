# Main results — English statements

*Status tags: [T-ℚ] exact over the rationals, machine-verified · [C-p] computational modulo ≥ 2 concordant large primes, residual-certified · [L] written lemma with explicit remaining-verification list [R] · [CONJ] conjecture. Full documents (proofs, tables, logs) are in `docs/fr/`; this file states the results.*

## Setting

Non-k-colorability of a graph G is encoded à la Bayer: one variable per vertex in R = ℚ[x]/(x_v^k − 1), one generator g_e per edge (for k = 3: g_e = x_u² + x_u x_v + x_v²), and G is non-k-colorable iff 1 belongs to the ideal — witnessed by a **Nullstellensatz certificate** Σ λ_{e,m} · m · g_e = 1. The *degree* of the certificate is the maximal degree of the multipliers m·g_e after reduction; degrees live in the residue 1 mod k (levels 1, k+1, …). A certificate is an exact rational object; its existence at a given degree is a linear-algebra statement (solvability of an explicit system over ℚ).

## Theorem 1 — the Pokrovskiy family G(q,3) [T-ℚ small q; C-p for the law]

For the 4-vertex-critical circulant family G(q,3) (n = 3q+1, offsets {1} ∪ {2+3j}), every member admits a degree-4 certificate. The certificates follow a finite closed law: 77 rational constants indexed by zone keys (position windows relative to the edge, antipodal fold), with denominators dividing 18 = 2·3².

## Theorem 2 — the triangle-free family ZJ(k) [T-ℚ + C-p]

For the triangle-free 4-vertex-critical family ZJ(k) (n = 3k+10, offsets {±1} ∪ {5+3j}), every member admits a degree-4 certificate, captured by an n-independent label system with orbit normalization ν = n·μ: all quotient entries are exact rationals with denominators dividing 216 = 2³·3³, in two parity strata, stable across all tested orders (exact for k = 3…8, two-prime certified through k = 35, law verified by full re-expansion on witnesses).

## Theorem 3 — the finite presentation of G_CH(q,4), modulus 4 [T-ℚ for q ≤ 12; L for all q]

For the 5-vertex-critical Cameron–Hoàng family G_CH(q,4) (n = 4q+1), every member admits a **degree-5** certificate (quartic-roots encoding, levels {1,5}), supported on edges of gap ≤ 3 = k−1, of scout × gadget form (local gadget of radius 3 plus one free scout variable). The family is captured by a finite presentation:

- an alphabet of **6,487 labels**, independent of n (gap, gadget pattern, scout exponent, scout position mod 4, sign) — closed from q = 5 on;
- an equation set of **6,186 equations**, closed from q = 10 on (increment series: 1299, 1384, 947, 317, 63, 12, 2, 0, 0);
- **two rational vectors** V_even (411 active labels) and V_odd (401), denominators dividing 16 = 2⁴, such that the exact solution of the label system at order q equals V_{q mod 2} **bit-for-bit** for q = 6…12 — seven consecutive orders, reproduced identically on two independent machines;
- three **blind predictions** verified: at q = 10, 11, 12 the predicted vector satisfies all 6,186 equations (zero violations), and the independent exact solve returns it exactly. The prediction test was calibrated to discriminate (a single perturbed coefficient is detected).

The two strata have a proven arithmetic cause: ⌊n/2⌋ = 2q ≡ 0 or 2 (mod 4) — the antipodal boundary catalogue depends on the parity of q alone. The closure lemma (windows of width ≤ 10, saturation of window types, step-4 invariance of scout signatures in the generic zone, parity-only antipodal boundary; threshold q₀ = 10) reduces "all q" to the finitely verified data; its remaining verification list [R] is explicit in the source document. The rank of the label system is constant (3,587; solution-space dimension 2,900) from q = 7 on — three steps before the equation list closes: all late equations are linearly dependent.

**Cross-modulus laws observed** (facts at both moduli; generality [CONJ]): minimal sufficient edge-gap = k−1 (2 at modulus 3, 3 at modulus 4 — both halves, insufficiency and sufficiency, established at two orders each); parity strata present at both moduli; presentation denominators 2·3² (mod 3) and 2⁴ (mod 4).

## The Collapse Conjecture [CONJ] and the adversarial campaign [C-p]

**Conjecture.** Every P₈-free non-3-colorable graph admits a degree-4 certificate (cube-roots encoding).

Structural context: a connected P₈-free graph has diameter ≤ 6, hence max degree Ω(n^{1/6}) (Moore); the known degree-lower-bound machinery for coloring axioms (sparse bounded-degree expanders, long-path gadgets) is therefore structurally inapplicable to the class — any refutation must be native.

Adversarial campaign (all full-support degree-{1,4} systems, two concordant primes): 110 random P₈-free non-3-colorable graphs at orders n = 14–17, far beyond any census, sampled without structural bias; 30 edge-critical cores (minimal within the class — edges removable neither for χ nor for P₈-freeness); 30 densified long-path instances. **170/170 solvable at degree 4. Zero refutation seeds.** Every insolvability alert would trigger a fixed verification protocol (≥ 5 primes, exact rational verification) before any claim — in either direction.

## Conditional NC² corollary

If the Collapse Conjecture holds, then deciding 3-colorability of P₈-free graphs is in **NC²**: the P₈-free promise is testable in AC⁰; building the degree-{1,4} system is local (uniform NC¹); solvability over ℚ reduces to two integer-matrix ranks, computable in NC² (Berkowitz division-free characteristic polynomial on AᵀA; in general Mulmuley 1987). Unconditionally, the degree-4 test itself is in NC². The mechanism is the historically attested route from P to NC: replace the search procedure by an algebraic invariant.
