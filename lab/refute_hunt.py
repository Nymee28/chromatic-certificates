#!/usr/bin/env python3
"""Chantier 2 (refutation), experience (iii) : la chasse aux contre-exemples.

Generer des graphes P8-free NON-3-coloriables a n = 14..16 (au-dela du census,
qui s'arrete a 10 en general / 13 sans-triangle) et tester le degre 4 en
SYSTEME COMPLET (niveau {1,4}, tout le support) par Wiedemann creux, deux
premiers concordants.

  - chaque instance solvable = un point de plus pour la Conjecture, dans une
    zone jamais exploree ;
  - toute instance INSOLVABLE au degre 4 = graine de refutation (a verifier
    exactement, puis pousser aux niveaux superieurs).

Generation : G(n, p) aleatoire, filtre chi >= 4 (backtracking exact), filtre
P8-free (longest_induced_path < 8), dedoublonnage grossier par invariant.
"""
import itertools, json, random, sys, time
from collections import defaultdict
from census import three_colorable, longest_induced_path, to_graph6
from sparse_wiedemann import solvable_sparse


def mul_red(m, t):
    d = dict(m)
    for v, e in t:
        d[v] = d.get(v, 0) + e
    return tuple(sorted((v, e % 3) for v, e in d.items() if e % 3))


def edge_terms(i, j):
    return [((i, 2),), tuple(sorted([(i, 1), (j, 1)])), ((j, 2),)]


def mults_full(n):
    out = [((v, 1),) for v in range(n)]
    for a, b in itertools.combinations(range(n), 2):
        out.append(((a, 2), (b, 2)))
    for a in range(n):
        for b, c in itertools.combinations([v for v in range(n) if v != a], 2):
            out.append(tuple(sorted([(a, 2), (b, 1), (c, 1)])))
    for quad in itertools.combinations(range(n), 4):
        out.append(tuple((v, 1) for v in quad))
    return out


def degree4_full(n, adj):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if (adj[i] >> j) & 1]
    mults = mults_full(n)
    row_ix, entries = {}, defaultdict(int)

    def rid(mono):
        if mono not in row_ix:
            row_ix[mono] = len(row_ix)
        return row_ix[mono]

    rid(())
    ncols = 0
    for e in edges:
        for m in mults:
            c = ncols
            ncols += 1
            for t in edge_terms(*e):
                entries[(rid(mul_red(m, t)), c)] += 1
    res = solvable_sparse(dict(entries), 0, len(row_ix), ncols, verbose=False)
    return res['solvable'], len(row_ix), ncols, res['primes']


def gen_candidates(n, tries, seed):
    rng = random.Random(seed)
    found = []
    seen = set()
    for t in range(tries):
        p = rng.uniform(0.30, 0.50)
        adj = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    adj[i] |= 1 << j
                    adj[j] |= 1 << i
        if three_colorable(n, adj):
            continue
        if longest_induced_path(n, adj, cap=8) >= 8:
            continue
        # invariant grossier de dedoublonnage
        degs = tuple(sorted(bin(a).count('1') for a in adj))
        m = sum(bin(a).count('1') for a in adj) // 2
        key = (degs, m)
        if key in seen:
            continue
        seen.add(key)
        found.append((adj, p))
    return found


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    tries = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260722
    n_sparse = int(sys.argv[4]) if len(sys.argv) > 4 else 25
    n_spread = int(sys.argv[5]) if len(sys.argv) > 5 else 15
    t0 = time.time()
    cands = gen_candidates(n, tries, seed)
    print(f"n={n}: {len(cands)} candidats P8-free non-3-coloriables "
          f"(sur {tries} tirages, {time.time()-t0:.0f}s)", flush=True)
    # curation : les plus epars (proches de la criticite) + un etale en densite
    def edge_count(adj):
        return sum(bin(a).count('1') for a in adj) // 2
    cands.sort(key=lambda cp: edge_count(cp[0]))
    step = max(1, (len(cands) - n_sparse) // n_spread) \
        if len(cands) > n_sparse else 1
    cands = cands[:n_sparse] + cands[n_sparse::step][:n_spread]
    print(f"curation: {len(cands)} instances retenues, aretes "
          f"{edge_count(cands[0][0])} a {edge_count(cands[-1][0])}", flush=True)
    # reprise : ne pas refaire les instances deja au JSON (meme g6)
    try:
        prev = {r['g6']: r for r in
                json.load(open(f'results/refute_hunt_n{n}.json'))}
    except Exception:
        prev = {}
    out = []
    for i, (adj, p) in enumerate(cands):
        g6 = to_graph6(n, adj)
        if g6 in prev:
            out.append(prev[g6])
            print(f"  [{i+1}/{len(cands)}] repris du JSON "
                  f"(solvable={prev[g6]['deg4_solvable']})", flush=True)
            json.dump(out, open(f'results/refute_hunt_n{n}.json', 'w'),
                      indent=1)
            continue
        t1 = time.time()
        ok, nr, nc, primes = degree4_full(n, adj)
        rec = {'g6': to_graph6(n, adj), 'p': round(p, 3),
               'rows': nr, 'cols': nc, 'deg4_solvable': ok, 'primes': primes,
               'time_s': round(time.time() - t1)}
        out.append(rec)
        flag = '' if ok else '  <<< INSOLVABLE AU DEGRE 4 — GRAINE DE REFUTATION'
        print(f"  [{i+1}/{len(cands)}] {nr}x{nc} solvable={ok} "
              f"({rec['time_s']}s){flag}", flush=True)
        json.dump(out, open(f'results/refute_hunt_n{n}.json', 'w'), indent=1)
    solv = sum(1 for r in out if r['deg4_solvable'])
    print(f"BILAN n={n}: {solv}/{len(out)} solvables au degre 4 (systeme complet)", flush=True)
