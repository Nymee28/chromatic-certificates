#!/usr/bin/env python3
"""Industrialization: Nullstellensatz certificate pipeline for arbitrary
circulant vertex-critical families, with general modulus.

Families:
  - G_CH(q, k): Cameron-Hoang, n = kq+1, N(v_i) = {v_{i+-1}} u {v_{i+kj+m}:
    m=2..k-1, j=0..q-1}. (k+1)-vertex-critical (their Lemma 2.6). k=3 is the
    Pokrovskiy family. Non-k-colorability certificates: k-th roots encoding,
    exponents mod k, multiplier degrees == 1 (mod k) -> levels {1, k+1}.
  - G_ZJ(k): Zhou-Jooken-Shan-Goedgebeur-Huang, n = 3k+10, offsets
    {+-1} u {5+3j: j=0..k}. 4-vertex-critical TRIANGLE-FREE for k >= 3.
    Same mod-3 machinery as Pokrovskiy.
"""
import itertools, json, sys, time
import numpy as np

P1, P2 = 1000003, 999999937


def circulant(n, offsets):
    adj = [0] * n
    for i in range(n):
        for s in offsets:
            j = (i + s) % n
            if j != i:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    return n, adj


def G_CH(q, k):
    n = k * q + 1
    offs = [1] + [k * j + m for j in range(q) for m in range(2, k)]
    return circulant(n, offs)


def G_ZJ(k):
    n = 3 * k + 10
    offs = [1] + [5 + 3 * j for j in range(k + 1)]
    return circulant(n, offs)


def colorable(n, adj, ncolors, removed=0):
    verts = [v for v in range(n) if not (removed >> v) & 1]
    verts.sort(key=lambda v: -bin(adj[v] & ~removed).count('1'))
    color = {}

    def bt(i, maxc):
        if i == len(verts):
            return True
        v = verts[i]
        used = 0
        for u, cu in color.items():
            if (adj[v] >> u) & 1:
                used |= 1 << cu
        for c in range(min(ncolors - 1, maxc + 1) + 1):
            if (used >> c) & 1:
                continue
            color[v] = c
            if bt(i + 1, max(maxc, c)):
                return True
            del color[v]
        return False
    return bt(0, -1)


def properties(n, adj, chi_target):
    m = sum(bin(a).count('1') for a in adj) // 2
    below = colorable(n, adj, chi_target - 1)
    crit = all(colorable(n, adj, chi_target - 1, removed=(1 << v)) for v in range(n))
    tri = any((adj[i] >> j) & 1 and (adj[i] & adj[j])
              for i in range(n) for j in range(i + 1, n))
    return {'n': n, 'edges': m, f'{chi_target-1}_colorable': below,
            'vertex_critical': crit, 'has_triangle': tri}


# ---- general-modulus symmetry-reduced Nullstellensatz system ----

def mults_k(vars_, degrees, k):
    out = []
    maxd = max(degrees)
    vs = list(vars_)

    def rec(i, cur, deg):
        if deg in degrees and cur:
            out.append(tuple(cur))
        if i == len(vs) or deg >= maxd:
            return
        rec(i + 1, cur, deg)
        for e in range(1, k):
            if deg + e <= maxd:
                rec(i + 1, cur + [(vs[i], e)], deg + e)
    rec(0, [], 0)
    return out


def rot_mono(m, sh, n):
    return tuple(sorted(((v + sh) % n, e) for v, e in m))


def canon_mono(m, n):
    return min(rot_mono(m, sh, n) for sh in range(n))


def canon_pair(edge, m, n):
    best = None
    for sh in range(n):
        e2 = tuple(sorted(((edge[0] + sh) % n, (edge[1] + sh) % n)))
        cand = (e2, rot_mono(m, sh, n))
        if best is None or cand < best:
            best = cand
    return best


def mul_red_k(m1, m2, k):
    d = dict(m1)
    for v, e in m2:
        d[v] = d.get(v, 0) + e
    return tuple(sorted((v, e % k) for v, e in d.items() if e % k))


def edge_poly_terms(i, j, k):
    """g_ij = sum_{l=0}^{k-1} x_i^{k-1-l} x_j^l  (terms as exponent tuples)."""
    terms = []
    for l in range(k):
        t = {}
        if k - 1 - l:
            t[i] = k - 1 - l
        if l:
            t[j] = l
        terms.append(tuple(sorted(t.items())))
    return terms


def reduced_system_k(n, adj, degrees, k):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if (adj[i] >> j) & 1]
    mus = mults_k(range(n), set(degrees), k)
    col_ix, row_ix, entries = {}, {}, {}

    def rid(m):
        if m not in row_ix:
            row_ix[m] = len(row_ix)
        return row_ix[m]

    const = rid(())
    for e in edges:
        gt = edge_poly_terms(e[0], e[1], k)
        for m in mus:
            w = canon_pair(e, m, n)
            if w not in col_ix:
                col_ix[w] = len(col_ix)
            c = col_ix[w]
            for t in gt:
                r = rid(canon_mono(mul_red_k(m, t, k), n))
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


def certificate_level_k(n, adj, k, levels=None):
    levels = levels or [(1,), (1, k + 1)]
    out = []
    for degs in levels:
        t0 = time.time()
        entries, const, nrows, ncols = reduced_system_k(n, adj, set(degs), k)
        ok = all(gauss_solvable(entries, const, nrows, ncols, p) for p in (P1, P2))
        out.append({'degrees': sorted(degs), 'rows': nrows, 'cols': ncols,
                    'sat': ok, 'time_s': round(time.time() - t0, 1)})
        if ok:
            break
    return out


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'zj':          # triangle-free family, mod 3
        for kk in [int(a) for a in sys.argv[2:]] or [3]:
            n, adj = G_ZJ(kk)
            props = properties(n, adj, 4)
            print(f'G_ZJ({kk}): {props}', flush=True)
            res = certificate_level_k(n, adj, 3)
            print(f'  levels: {json.dumps(res)}', flush=True)
    elif mode == 'ch4':       # Cameron-Hoang k=4 (5-critical), mod 4
        for qq in [int(a) for a in sys.argv[2:]] or [2]:
            n, adj = G_CH(qq, 4)
            props = properties(n, adj, 5)
            print(f'G_CH({qq},4): {props}', flush=True)
            res = certificate_level_k(n, adj, 4)
            print(f'  levels: {json.dumps(res)}', flush=True)
