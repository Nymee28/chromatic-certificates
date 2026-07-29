#!/usr/bin/env python3
"""J2 (dossier 9) : la presentation de G_CH(q,4) en module 4 — etape 1.

Les faits exacts aux petits q, avant tout ansatz :
  - `exact 3`  : a q=3 (n=13), balayage du support par ecart d'arete
    (le systeme restreint aux colonnes d'ecart <= G est-il solvable ?)
    puis solution EXACTE sur Q du plus petit support suffisant
    (2 premiers, CRT, reconstruction rationnelle, verification A.mu = e),
    et histogramme des formes de monomes relatifs a l'arete.
    Question J2 : le vocabulaire (ecarts, eclaireurs, gadgets) est-il
    isomorphe a celui de G(q,3) (ecarts <= 2, eclaireur + gadget local) ?
  - `solve 4 [5 ...]` : solvabilite du systeme reduit complet {1,5}
    par Wiedemann creux (la ou l'ancien pipeline dense capitulait a 30 GB).
"""
import json, sys, time
from fractions import Fraction
from collections import Counter
from pillars import (G_CH, mults_k, canon_mono, canon_pair, mul_red_k,
                     edge_poly_terms)
from certificates import rref_particular, crt, ratrec, P1, P2
from sparse_wiedemann import solvable_sparse


def gap_of(e, n):
    d = (e[1] - e[0]) % n
    return min(d, n - d)


def build_with_cols(n, adj, degrees, k, max_gap=None, order=False):
    """Systeme reduit par rotation, avec la carte colonne -> (arete, monome).
    max_gap : ne garder que les colonnes d'arete d'ecart <= max_gap.
    order   : trier les colonnes (ecart, complexite) croissants avant
              numerotation (le pivot RREF prefere alors le vocabulaire simple).
    """
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)
             if (adj[i] >> j) & 1]
    if max_gap is not None:
        edges = [e for e in edges if gap_of(e, n) <= max_gap]
    mus = mults_k(range(n), set(degrees), k)
    pairs = {}
    for e in edges:
        for m in mus:
            w = canon_pair(e, m, n)
            if w not in pairs:
                pairs[w] = None
    cols = list(pairs)
    if order:
        def complexity(w):
            e, m = w
            return (gap_of(e, n), len(m), max((x for _, x in m), default=0),
                    sum(x for _, x in m))
        cols.sort(key=complexity)
    col_ix = {w: i for i, w in enumerate(cols)}
    row_ix, entries = {}, {}

    def rid(m):
        if m not in row_ix:
            row_ix[m] = len(row_ix)
        return row_ix[m]

    const = rid(())
    seen_pairs = set()
    for e in edges:
        gt = edge_poly_terms(e[0], e[1], k)
        for m in mus:
            w = canon_pair(e, m, n)
            if w in seen_pairs:
                continue
            seen_pairs.add(w)
            c = col_ix[w]
            for t in gt:
                r = rid(canon_mono(mul_red_k(m, t, k), n))
                entries[(r, c)] = entries.get((r, c), 0) + 1
    return entries, const, len(row_ix), cols, col_ix


def mono_shape(w, n):
    """Forme du monome relative a l'arete, normalisee (2 orientations)."""
    (a, b), m = w
    best = None
    for (o, sgn) in ((a, 1), (b, -1)):
        rel = tuple(sorted((((v - o) * sgn) % n if ((v - o) * sgn) % n <= n // 2
                            else ((v - o) * sgn) % n - n, e) for v, e in m))
        cand = rel
        if best is None or cand < best:
            best = cand
    return best


def exact_mode(q, known_gap=None):
    import pickle, os
    n, adj = G_CH(q, 4)
    dists = sorted({gap_of((0, s % n), n)
                    for s in [1] + [4 * j + mm for j in range(q)
                                    for mm in (2, 3)]})
    print(f"G_CH({q},4): n={n}, ecarts presents {dists}", flush=True)
    verdicts = {}
    best_gap = known_gap
    if best_gap is None:
        for G in dists:
            t0 = time.time()
            entries, const, nrows, cols, col_ix = build_with_cols(
                n, adj, {1, 5}, 4, max_gap=G)
            x, piv = rref_particular(entries, const, nrows, len(cols), P1)
            verdicts[G] = x is not None
            print(f"  ecart <= {G}: {nrows}x{len(cols)}, solvable mod P1 = "
                  f"{x is not None} ({time.time()-t0:.0f}s)", flush=True)
            if x is not None:
                best_gap = G
                break
        if best_gap is None:
            print("AUCUN ecart ne suffit ?! (contradiction avec le complet)",
                  flush=True)
            return
    else:
        print(f"  ecart minimal suffisant connu (repris) : {best_gap}",
              flush=True)
    # solution exacte sur le support minimal, colonnes triees simples d'abord
    entries, const, nrows, cols, col_ix = build_with_cols(
        n, adj, {1, 5}, 4, max_gap=best_gap, order=True)
    sols = {}
    for p in (P1, P2):
        ck = f'results/j2_ckpt_q{q}_p{p}.pkl'
        if os.path.exists(ck):
            sols[p] = pickle.load(open(ck, 'rb'))
            print(f"  RREF mod {p}: repris du point de controle "
                  f"(|support| = {len(sols[p])})", flush=True)
            continue
        t0 = time.time()
        x, piv = rref_particular(entries, const, nrows, len(cols), p)
        assert x is not None
        sols[p] = x
        pickle.dump(x, open(ck, 'wb'))
        print(f"  RREF mod {p}: |support| = {len(x)} ({time.time()-t0:.0f}s)",
              flush=True)
    keys = sorted(set(sols[P1]) | set(sols[P2]))
    M = P1 * P2
    mu, fails = {}, 0
    for c in keys:
        f = ratrec(crt(sols[P1].get(c, 0) % P1, sols[P2].get(c, 0) % P2), M)
        if f is None:
            fails += 1
        elif f:
            mu[c] = f
    print(f"  reconstruction: {len(mu)} coefficients rationnels, "
          f"{fails} echecs", flush=True)
    # verification exacte A.mu = e_const sur Q
    rowsum = {}
    for (r, c), v in entries.items():
        if c in mu:
            rowsum[r] = rowsum.get(r, Fraction(0)) + v * mu[c]
    ok = all((s == 1 if r == const else s == 0) for r, s in rowsum.items()) \
        and rowsum.get(const, Fraction(0)) == 1
    print(f"  VERIFICATION EXACTE sur Q : {'OK' if ok else 'ECHEC'}",
          flush=True)
    # analyse du support
    from math import lcm
    dens = 1
    for f in mu.values():
        dens = lcm(dens, f.denominator)
    gaps = Counter(gap_of(cols[c][0], n) for c in mu)
    shapes = Counter()
    scouts = Counter()
    for c in mu:
        w = cols[c]
        sh = mono_shape(w, n)
        shapes[sh] += 1
        if len(sh) == 1:
            scouts['eclaireur seul (deg 1)'] += 1
        else:
            # eclaireur = variable de degre 1 la plus lointaine, gadget = reste
            far = max(abs(o) for o, _ in sh)
            near = [t for t in sh if abs(t[0]) != far]
            scouts[f'diam {far}, gadget {len(near)} vars'] += 1
    if not verdicts:  # repris : le balayage etabli precedemment (journal)
        verdicts = {g: (g >= best_gap) for g in dists if g <= best_gap}
    res = {'q': q, 'n': n, 'ecarts_presents': dists,
           'balayage_ecart': {str(g): bool(v) for g, v in verdicts.items()},
           'ecart_minimal_suffisant': best_gap,
           'support': len(mu), 'denominateur_lcm': str(dens),
           'verification_exacte': bool(ok),
           'gaps_du_support': {str(g): c for g, c in sorted(gaps.items())},
           'formes_distinctes': len(shapes),
           'formes_top': [[str(s), c] for s, c in shapes.most_common(25)],
           'familles_eclaireur': {k2: v for k2, v in scouts.most_common()}}
    json.dump(res, open(f'results/j2_ch4_exact_q{q}.json', 'w'), indent=1)
    print(f"  ecart minimal suffisant : {best_gap} (k=3 donnait 2)\n"
          f"  denominateur LCM : {dens}\n"
          f"  formes distinctes : {len(shapes)} ; familles : "
          f"{dict(scouts.most_common(6))}", flush=True)


def solve_mode(qs, max_gap=None):
    tag = '' if max_gap is None else f'_gap{max_gap}'
    out = []
    for q in qs:
        n, adj = G_CH(q, 4)
        t0 = time.time()
        entries, const, nrows, cols, col_ix = build_with_cols(
            n, adj, {1, 5}, 4, max_gap=max_gap)
        tb = time.time() - t0
        print(f"G_CH({q},4){' ecart<=' + str(max_gap) if max_gap else ''}: "
              f"n={n}, reduit {nrows}x{len(cols)} "
              f"(nnz {len(entries)}, build {tb:.0f}s)", flush=True)
        t0 = time.time()
        res = solvable_sparse(entries, const, nrows, len(cols), verbose=False)
        rec = {'q': q, 'n': n, 'max_gap': max_gap, 'rows': nrows,
               'cols': len(cols), 'nnz': len(entries),
               'solvable': res['solvable'],
               'primes': res['primes'], 'build_s': round(tb),
               'solve_s': round(time.time() - t0)}
        out.append(rec)
        print(f"  niveaux {{1,5}} mod 4 : solvable={res['solvable']} "
              f"({rec['solve_s']}s)", flush=True)
        json.dump(out, open(f'results/j2_ch4_solve{tag}.json', 'w'),
                  indent=1)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'exact':
        exact_mode(int(sys.argv[2]) if len(sys.argv) > 2 else 3,
                   known_gap=int(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif mode == 'solve':
        solve_mode([int(a) for a in sys.argv[2:]] or [4])
    elif mode == 'solvegap':
        solve_mode([int(sys.argv[2])], max_gap=int(sys.argv[3]))
