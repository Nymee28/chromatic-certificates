#!/usr/bin/env python3
"""Explicit symmetric Nullstellensatz certificates for the Pokrovskiy family
G(q,3), with EXACT rational reconstruction and EXACT verification over Q.

Pipeline per q:
 1. Build the symmetry-reduced degree-{1,4} system with labeled orbits.
 2. Canonical particular solution: RREF over GF(p1) and GF(p2) with a fixed
    column order and free variables set to 0. Pivot sets must coincide.
 3. CRT-combine the two solutions mod p1*p2, then rational reconstruction
    (continued fractions) -> exact rational orbit coefficients.
 4. EXACT verification over Q: expand sum mu_e g_e in Q[x]/(x_i^3-1) with
    Fraction arithmetic and check it equals the constant 1. This removes the
    GF(p)-proxy caveat: the certificate becomes a THEOREM for that instance.
 5. Dihedral symmetrization (average with the reflection image; re-verify).
 6. Shape analysis: orbits normalized to (edge gap, relative offsets+exponents)
    for cross-q pattern comparison.
"""
import itertools, json, math, sys, time
from fractions import Fraction
import numpy as np
from pokrovskiy import G, mults, rot_mono, canon_mono, canon_pair, mul_red

P1, P2 = 1000003, 999999937


# ---------------- system with labels ----------------

def reduced_system_labeled(q, degrees):
    n, adj = G(q)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if (adj[i] >> j) & 1]
    mus = mults(n, degrees)
    col_ix, row_ix = {}, {}
    entries = {}

    def rid(m):
        if m not in row_ix:
            row_ix[m] = len(row_ix)
        return row_ix[m]

    const = rid(())
    for e in edges:
        i, j = e
        g_terms = [((i, 2),), tuple(sorted([(i, 1), (j, 1)])), ((j, 2),)]
        for m in mus:
            w = canon_pair(e, m, n)
            if w not in col_ix:
                col_ix[w] = len(col_ix)
            c = col_ix[w]
            for gt in g_terms:
                r = rid(canon_mono(mul_red(m, gt), n))
                entries[(r, c)] = entries.get((r, c), 0) + 1
    col_labels = [None] * len(col_ix)
    for w, c in col_ix.items():
        col_labels[c] = w
    return entries, const, len(row_ix), col_labels, n


# ---------------- canonical RREF solution mod p ----------------

def rref_particular(entries, const, nrows, ncols, p):
    M = np.zeros((nrows, ncols + 1), dtype=np.int64)
    for (r, c), v in entries.items():
        M[r, c] = v % p
    M[const, ncols] = 1
    pivots = []
    r = 0
    for c in range(ncols):
        if r == nrows:
            break
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0:
            continue
        pr = r + int(nz[0])
        if pr != r:
            M[[r, pr]] = M[[pr, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        colv = M[:, c].copy()
        colv[r] = 0
        mask = colv != 0
        if mask.any():
            M[mask] = (M[mask] - np.outer(colv[mask], M[r])) % p
        pivots.append(c)
        r += 1
    zeroA = (M[:, :-1] == 0).all(axis=1)
    if bool((zeroA & (M[:, -1] != 0)).any()):
        return None, pivots
    x = {}
    for rr, c in enumerate(pivots):
        v = int(M[rr, ncols])
        if v:
            x[c] = v
    return x, pivots


# ---------------- CRT + rational reconstruction ----------------

def crt(a1, a2):
    # x = a1 mod P1, x = a2 mod P2
    M = P1 * P2
    inv = pow(P1, -1, P2)
    t = ((a2 - a1) * inv) % P2
    return (a1 + P1 * t) % M


def ratrec(u, M):
    """Rational reconstruction: a/b = u mod M with |a|, b <= sqrt(M/2)."""
    bound = math.isqrt(M // 2)
    r0, r1 = M, u % M
    s0, s1 = 0, 1
    while r1 > bound:
        qq = r0 // r1
        r0, r1 = r1, r0 - qq * r1
        s0, s1 = s1, s0 - qq * s1
    a, b = r1, s1
    if b < 0:
        a, b = -a, -b
    if b == 0 or math.gcd(a, b) != 1 or b > bound:
        return None
    if (a - b * u) % M != 0:
        return None
    return Fraction(a, b)


# ---------------- exact verification over Q ----------------

def orbit_pairs(w, n):
    (e0, m0) = w
    seen = set()
    for k in range(n):
        e = tuple(sorted(((e0[0] + k) % n, (e0[1] + k) % n)))
        m = rot_mono(m0, k, n)
        if (e, m) not in seen:
            seen.add((e, m))
    return seen


def verify_exact(q, sol):
    """sol: dict orbit-label -> Fraction. Check sum mu*g == 1 in Q[x]/(x^3-1)."""
    n, adj = G(q)
    total = {}
    for w, coef in sol.items():
        if coef == 0:
            continue
        for (e, m) in orbit_pairs(w, n):
            i, j = e
            for gt in [((i, 2),), tuple(sorted([(i, 1), (j, 1)])), ((j, 2),)]:
                t = mul_red(m, gt)
                total[t] = total.get(t, Fraction(0)) + coef
    total = {t: v for t, v in total.items() if v != 0}
    return total == {(): Fraction(1)}


# ---------------- dihedral symmetrization ----------------

def reflect_orbit(w, n):
    (e, m) = w
    e2 = ((-e[0]) % n, (-e[1]) % n)
    m2 = tuple(sorted(((-v) % n, k) for v, k in m))
    return canon_pair(tuple(sorted(e2)), m2, n)


def symmetrize(sol, n):
    out = {}
    for w, c in sol.items():
        wr = reflect_orbit(w, n)
        out[w] = out.get(w, Fraction(0)) + c / 2
        out[wr] = out.get(wr, Fraction(0)) + c / 2
    return {w: c for w, c in out.items() if c != 0}


# ---------------- shapes ----------------

def gap(e, n):
    d = (e[1] - e[0]) % n
    return min(d, n - d)


def shape(w, n):
    """Normalize the orbit to (edge gap, monomial offsets relative to edge),
    minimizing over the <=4 symmetries fixing the edge {0,g}."""
    (e, m) = w
    g = gap(e, n)
    cands = []
    for (a, b) in [(e[0], e[1]), (e[1], e[0])]:
        for refl in (False, True):
            offs = []
            for v, k in m:
                d = (v - a) % n if not refl else (a - v) % n
                offs.append((d, k))
            # need edge to map to (0, +g) direction: check partner
            d_b = (b - a) % n if not refl else (a - b) % n
            if d_b == g % n or d_b == g:
                cands.append(tuple(sorted(offs)))
    return (g, min(cands)) if cands else (g, tuple(sorted(m)))


# ---------------- main ----------------

def run(q, save=True):
    t0 = time.time()
    entries, const, nrows, col_labels, n = reduced_system_labeled(q, {1, 4})
    ncols = len(col_labels)
    x1, piv1 = rref_particular(entries, const, nrows, ncols, P1)
    x2, piv2 = rref_particular(entries, const, nrows, ncols, P2)
    assert x1 is not None and x2 is not None, 'inconsistent system?!'
    assert piv1 == piv2, 'pivot mismatch between primes - add a third prime'
    rank = len(piv1)
    sol = {}
    M = P1 * P2
    for c in set(x1) | set(x2):
        u = crt(x1.get(c, 0), x2.get(c, 0))
        f = ratrec(u, M)
        assert f is not None, f'rational reconstruction failed on column {c}'
        sol[col_labels[c]] = f
    ok = verify_exact(q, sol)
    sol_sym = symmetrize(sol, n)
    ok_sym = verify_exact(q, sol_sym)
    dens = sorted({f.denominator for f in sol.values()})
    res = {
        'q': q, 'n': n, 'rows': nrows, 'cols': ncols, 'rank': rank,
        'solution_space_dim': ncols - rank,
        'nonzero_orbit_coeffs': len(sol),
        'nonzero_after_dihedral_sym': len(sol_sym),
        'denominators': dens[:20],
        'EXACT_VERIFIED_OVER_Q': ok,
        'EXACT_VERIFIED_SYMMETRIZED': ok_sym,
        'time_s': round(time.time() - t0, 1),
    }
    if save:
        cert = [{'edge': list(w[0]), 'monomial': [list(t) for t in w[1]],
                 'num': f.numerator, 'den': f.denominator}
                for w, f in sorted(sol_sym.items())]
        json.dump({'meta': res, 'certificate_dihedral_symmetric': cert},
                  open(f'certificate_q{q}.json', 'w'))
    return res, sol, sol_sym


if __name__ == '__main__':
    qs = [int(a) for a in sys.argv[1:]] or [1, 2, 3]
    for q in qs:
        res, sol, sol_sym = run(q)
        print(json.dumps(res), flush=True)
