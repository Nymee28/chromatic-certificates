#!/usr/bin/env python3
"""Family-ansatz certificate solver for G(q,3).

Observation (from exact certificates q=2..5): nonzero multipliers live ONLY on
gap-1 and gap-2 edges, and every nonzero multiplier monomial is either
  - a single variable ("scout") anywhere on the cycle, or
  - a scout times a fixed LOCAL GADGET (3 vertices near the edge), from a
    small repertoire, with coefficients ~ c/n and period-3 structure in the
    scout position.
This module solves the certificate system RESTRICTED to that ansatz family:
columns = orbits of (edge of gap<=2, scout(+gadget) monomial). The system has
size O(n) x O(n), so exact certificates become computable for large q, and are
then verified EXACTLY over Q with verify_exact (independent of how they were
found). A pass at many q makes the closed-form conjecture precise.
"""
import json, sys, time
from fractions import Fraction
import numpy as np
from pokrovskiy import G, canon_mono, canon_pair, mul_red
from certificates import (rref_particular, crt, ratrec, verify_exact,
                          symmetrize, P1, P2)

# gadget offset patterns relative to oriented edge (a, a+g): (offset, exp)
GADGETS = [
    ((-1, 2), (1, 1)),
    ((-1, 1), (0, 1), (1, 1)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 1), (2, 2)),
]


def mirrored(gad, g):
    # reflection through the edge center: offset d -> g - d
    return tuple(sorted(((g - d), k) for d, k in gad))


def restricted_pairs(q):
    """All (edge, monomial) pairs of the ansatz family."""
    n, adj = G(q)
    pairs = set()
    for g in (1, 2):
        gads = set()
        for gad in GADGETS:
            gads.add(tuple(sorted(gad)))
            gads.add(mirrored(gad, g))
        for i in range(n):
            e = tuple(sorted((i, (i + g) % n)))
            # scouts alone (degree 1)
            for j in range(n):
                pairs.add((e, ((j, 1),)))
            # scout x gadget (degree 4 after reduction, else skip)
            for gad in gads:
                base = {}
                for d, k in gad:
                    v = (i + d) % n
                    base[v] = base.get(v, 0) + k
                for j in range(n):
                    m = dict(base)
                    m[j] = m.get(j, 0) + 1
                    mono = tuple(sorted((v, k % 3) for v, k in m.items() if k % 3))
                    deg = sum(k for _, k in mono)
                    if deg % 3 == 1 and deg <= 4 and mono:
                        pairs.add((e, mono))
    return n, pairs


def build_restricted(q):
    n, pairs = restricted_pairs(q)
    col_ix, row_ix, entries = {}, {}, {}

    def rid(m):
        if m not in row_ix:
            row_ix[m] = len(row_ix)
        return row_ix[m]

    const = rid(())
    for (e, m) in pairs:
        i, j = e
        w = canon_pair(e, m, n)
        if w not in col_ix:
            col_ix[w] = len(col_ix)
        c = col_ix[w]
        for gt in [((i, 2),), tuple(sorted([(i, 1), (j, 1)])), ((j, 2),)]:
            r = rid(canon_mono(mul_red(m, gt), n))
            entries[(r, c)] = entries.get((r, c), 0) + 1
    labels = [None] * len(col_ix)
    for w, c in col_ix.items():
        labels[c] = w
    return entries, const, len(row_ix), labels, n


def run(q, save=True):
    t0 = time.time()
    entries, const, nrows, labels, n = build_restricted(q)
    ncols = len(labels)
    x1, piv1 = rref_particular(entries, const, nrows, ncols, P1)
    if x1 is None:
        return {'q': q, 'n': n, 'rows': nrows, 'cols': ncols,
                'ANSATZ_SOLVABLE': False, 'time_s': round(time.time() - t0, 1)}, None
    x2, piv2 = rref_particular(entries, const, nrows, ncols, P2)
    assert x2 is not None and piv1 == piv2, 'prime mismatch'
    sol = {}
    M = P1 * P2
    for c in set(x1) | set(x2):
        f = ratrec(crt(x1.get(c, 0), x2.get(c, 0)), M)
        assert f is not None, 'ratrec failed'
        sol[labels[c]] = f
    sol = symmetrize(sol, n)
    ok = verify_exact(q, sol)
    res = {'q': q, 'n': n, 'rows': nrows, 'cols': ncols, 'rank': len(piv1),
           'ANSATZ_SOLVABLE': True, 'nonzero': len(sol),
           'EXACT_VERIFIED_OVER_Q': ok, 'time_s': round(time.time() - t0, 1)}
    if save and ok:
        cert = [{'edge': list(w[0]), 'monomial': [list(t) for t in w[1]],
                 'num': f.numerator, 'den': f.denominator}
                for w, f in sorted(sol.items())]
        json.dump({'meta': res, 'certificate': cert},
                  open(f'ansatz_certificate_q{q}.json', 'w'))
    return res, sol


if __name__ == '__main__':
    qs = [int(a) for a in sys.argv[1:]] or [3, 4, 5, 6]
    for q in qs:
        res, sol = run(q)
        print(json.dumps(res), flush=True)
