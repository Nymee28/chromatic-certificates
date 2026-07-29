#!/usr/bin/env python3
"""The crucial test: Nullstellensatz certificate degree along the Pokrovskiy
family G(q,3) of 4-vertex-critical P7-free circulants (Cameron-Hoang Def 2.1:
vertices v_0..v_{3q}, v_i ~ v_{i+1} and v_i ~ v_{i+2+3j}, j=0..q-1, mod 3q+1).
q=1 gives K4.

Symmetry reduction: the certificate equation sum mu_e g_e = 1 is linear and
Z_n-equivariant; averaging any solution over the cyclic group (valid since
p does not divide n) yields an invariant one. So we may search invariant
certificates only: variables = orbits of (edge, multiplier-monomial) pairs,
equations = orbits of product monomials. Accumulating all pair contributions
into orbit buckets yields the reduced matrix up to a per-row positive scaling
(the row-orbit size), which does not affect solvability since p > n.
"""
import itertools, json, sys, time
import numpy as np
from census import three_colorable, longest_induced_path

P1, P2 = 1000003, 999999937


def G(q):
    n = 3 * q + 1
    adj = [0] * n
    S = [1] + [2 + 3 * j for j in range(q)]
    for i in range(n):
        for s in S:
            j = (i + s) % n
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    return n, adj


def check_properties(q):
    n, adj = G(q)
    edges = sum(bin(a).count('1') for a in adj) // 2
    col3 = three_colorable(n, adj)
    crit = all(three_colorable(n, adj, removed=(1 << v)) for v in range(n))
    lip = longest_induced_path(n, adj, cap=8)
    return {'q': q, 'n': n, 'edges': edges, 'three_colorable': col3,
            'vertex_critical_if_not3col': crit, 'LIP': lip, 'P7free': lip <= 6,
            'P8free': lip <= 7}


# ---------- monomials & orbits ----------

def mults(n, degrees):
    out = []
    maxd = max(degrees)
    verts = list(range(n))
    for a in range(0, maxd // 2 + 1):
        for A in itertools.combinations(verts, a):
            rem = [v for v in verts if v not in A]
            for b in range(0, maxd - 2 * a + 1):
                if 2 * a + b in degrees and b <= len(rem):
                    for B in itertools.combinations(rem, b):
                        m = tuple(sorted([(v, 2) for v in A] + [(v, 1) for v in B]))
                        out.append(m)
    return out


def rot_mono(m, k, n):
    return tuple(sorted(((v + k) % n, e) for v, e in m))


def canon_mono(m, n):
    return min(rot_mono(m, k, n) for k in range(n))


def canon_pair(edge, m, n):
    best = None
    for k in range(n):
        e2 = tuple(sorted(((edge[0] + k) % n, (edge[1] + k) % n)))
        m2 = rot_mono(m, k, n)
        cand = (e2, m2)
        if best is None or cand < best:
            best = cand
    return best


def mul_red(m1, m2):
    d = dict(m1)
    for v, e in m2:
        d[v] = d.get(v, 0) + e
    return tuple(sorted((v, e % 3) for v, e in d.items() if e % 3))


def reduced_system(q, degrees):
    n, adj = G(q)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if (adj[i] >> j) & 1]
    mus = mults(n, degrees)
    col_ix, row_ix = {}, {}
    entries = {}   # (row, col) -> count

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
                t = mul_red(m, gt)
                r = rid(canon_mono(t, n))
                entries[(r, c)] = entries.get((r, c), 0) + 1
    return entries, const, len(row_ix), len(col_ix)


def gauss_solvable(entries, const, nrows, ncols, p):
    M = np.zeros((nrows, ncols + 1), dtype=np.int64)
    for (r, c), v in entries.items():
        M[r, c] = v % p
    M[const, ncols] = 1
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
        r += 1
    zeroA = (M[:, :-1] == 0).all(axis=1)
    return not bool((zeroA & (M[:, -1] != 0)).any())


def level_reduced(q, degrees):
    t0 = time.time()
    entries, const, nrows, ncols = reduced_system(q, degrees)
    tb = time.time() - t0
    ok1 = gauss_solvable(entries, const, nrows, ncols, P1)
    ok2 = gauss_solvable(entries, const, nrows, ncols, P2)
    return {'degrees': sorted(degrees), 'rows': nrows, 'cols': ncols,
            'sat_p1': ok1, 'sat_p2': ok2, 'build_s': round(tb, 1),
            'total_s': round(time.time() - t0, 1)}


if __name__ == '__main__':
    qs = [int(a) for a in sys.argv[1:]] or [2, 3, 4, 5]
    results = []
    for q in qs:
        props = check_properties(q)
        print(f"G({q},3): n={props['n']} m={props['edges']} "
              f"3col={props['three_colorable']} crit={props['vertex_critical_if_not3col']} "
              f"LIP={props['LIP']} P7free={props['P7free']}", flush=True)
        r1 = level_reduced(q, {1})
        print(f"  L1: sat={r1['sat_p1']}/{r1['sat_p2']} ({r1['rows']}x{r1['cols']}, {r1['total_s']}s)", flush=True)
        r4 = level_reduced(q, {1, 4})
        print(f"  L4: sat={r4['sat_p1']}/{r4['sat_p2']} ({r4['rows']}x{r4['cols']}, {r4['total_s']}s)", flush=True)
        results.append({'props': props, 'L1': r1, 'L4': r4})
        json.dump(results, open(f'pokrovskiy_results.json', 'w'))
