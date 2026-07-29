#!/usr/bin/env python3
"""Chantier 2, experience (ii) : la densification — l'import force des
instances dures.

Prendre un graphe epars non-3-coloriable A LONGS CHEMINS INDUITS (le
territoire de Lauria-Nordstrom, la ou vivent les bornes inferieures de
degre), puis tuer ses P8 par ajout de cordes jusqu'a P8-liberte. L'ajout
d'aretes preserve chi >= 4. Mesurer : cordes necessaires, degre maximal
avant/apres, et le verdict du degre 4 complet AVANT et APRES.

Prediction de la Conjecture : apres densification, SOLVABLE. Une
trajectoire qui reste INSOLVABLE une fois P8-free = graine de refutation.
"""
import json, random, sys, time
from census import three_colorable, longest_induced_path, to_graph6
from refute_hunt import degree4_full


def find_induced_pk(n, adj, k):
    """Un chemin induit a k sommets (liste), ou None."""
    def extend(path, path_set, forbidden):
        if len(path) == k:
            return path
        last = path[-1]
        m = adj[last] & ~forbidden
        while m:
            v = (m & -m).bit_length() - 1
            m &= m - 1
            if adj[v] & (path_set & ~(1 << last)):
                continue
            r = extend(path + [v], path_set | (1 << v),
                       forbidden | (1 << v) | (adj[last] & ~(1 << v)))
            if r:
                return r
        return None
    for s in range(n):
        r = extend([s], 1 << s, 1 << s)
        if r:
            return r
    return None


def add_edge(adj, i, j):
    b = list(adj)
    b[i] |= 1 << j
    b[j] |= 1 << i
    return b


def densify(n, adj, rng, strategy):
    """Ajouter des cordes jusqu'a P8-liberte. Renvoie (adj, nb_cordes)."""
    cur = list(adj)
    chords = 0
    while True:
        path = find_induced_pk(n, cur, 8)
        if path is None:
            return cur, chords
        cand = [(path[a], path[b]) for a in range(8) for b in range(a + 2, 8)]
        if strategy == 'random':
            i, j = cand[rng.randrange(len(cand))]
        else:  # 'mindeg' : minimiser la montee du degre maximal
            def cost(e):
                di = bin(cur[e[0]]).count('1')
                dj = bin(cur[e[1]]).count('1')
                return (max(di, dj), di + dj)
            i, j = min(cand, key=cost)
        cur = add_edge(cur, i, j)
        chords += 1


def gen_sparse_hard(n, tries, seed, want):
    """Graphes epars chi>=4 AVEC un P8 induit (les rejets de la chasse)."""
    rng = random.Random(seed)
    found, seen = [], set()
    for _ in range(tries):
        p = rng.uniform(0.20, 0.32)
        adj = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    adj[i] |= 1 << j
                    adj[j] |= 1 << i
        if three_colorable(n, adj):
            continue
        if longest_induced_path(n, adj, cap=8) < 8:
            continue
        degs = tuple(sorted(bin(a).count('1') for a in adj))
        m = sum(bin(a).count('1') for a in adj) // 2
        if (degs, m) in seen:
            continue
        seen.add((degs, m))
        found.append(adj)
        if len(found) >= want:
            break
    found.sort(key=lambda a: sum(bin(x).count('1') for x in a))
    return found


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    want = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260722
    rng = random.Random(seed + 2)
    graphs = gen_sparse_hard(n, 200000, seed + 3, want)
    print(f"n={n}: {len(graphs)} instances eparses chi>=4 a P8 induit", flush=True)
    out = []
    for gi, adj in enumerate(graphs):
        m0 = sum(bin(a).count('1') for a in adj) // 2
        d0 = max(bin(a).count('1') for a in adj)
        t1 = time.time()
        ok0, nr0, nc0, _ = degree4_full(n, adj)
        rec = {'g6_avant': to_graph6(n, adj), 'aretes_avant': m0,
               'maxdeg_avant': d0, 'deg4_avant': ok0,
               'time_avant_s': round(time.time() - t1), 'trajectoires': []}
        print(f"[{gi+1}/{len(graphs)}] avant: {m0} aretes, maxdeg {d0}, "
              f"deg4={ok0} ({rec['time_avant_s']}s)"
              + ('' if ok0 else '   <<< INSOLVABLE EPARS (attendu ?)'), flush=True)
        for strat in ('mindeg', 'random'):
            dens, nch = densify(n, adj, rng, strat)
            m1 = sum(bin(a).count('1') for a in dens) // 2
            d1 = max(bin(a).count('1') for a in dens)
            t1 = time.time()
            ok1, nr1, nc1, primes = degree4_full(n, dens)
            traj = {'strategie': strat, 'cordes': nch, 'aretes_apres': m1,
                    'maxdeg_apres': d1, 'deg4_apres': ok1,
                    'g6_apres': to_graph6(n, dens),
                    'time_s': round(time.time() - t1)}
            rec['trajectoires'].append(traj)
            flag = '' if ok1 else '  <<< INSOLVABLE P8-FREE — GRAINE DE REFUTATION'
            print(f"    {strat}: +{nch} cordes -> {m1} aretes, maxdeg {d1}, "
                  f"deg4={ok1} ({traj['time_s']}s){flag}", flush=True)
        out.append(rec)
        json.dump(out, open(f'results/densify_n{n}.json', 'w'), indent=1)
    flips = sum(1 for r in out if not r['deg4_avant']
                and all(t['deg4_apres'] for t in r['trajectoires']))
    print(f"BILAN densification n={n}: {len(out)} instances ; "
          f"{sum(1 for r in out if not r['deg4_avant'])} insolvables epars ; "
          f"{flips} basculements INSOLVABLE->SOLVABLE par P8-liberte", flush=True)
