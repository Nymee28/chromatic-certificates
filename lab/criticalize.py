#!/usr/bin/env python3
"""Chantier 2, raffinement (iv) : la criticalisation dans la classe.

Retirer des aretes tant que chi >= 4 ET que le graphe reste P8-free
(le retrait peut creer des chemins induits : double condition obligatoire).
Le point fixe est un coeur "arete-critique dans P8-free" : le noyau dur
minimal, la ou une montee de degre se verrait en premier.

Pipeline : regenerer les candidats (meme graine que la chasse), criticaliser,
dedoublonner (invariant grossier enrichi), tester au degre 4 complet les
coeurs les plus epars non deja couverts par la chasse.
"""
import json, random, sys, time
from census import three_colorable, longest_induced_path, to_graph6
from refute_hunt import gen_candidates, degree4_full


def edge_list(n, adj):
    return [(i, j) for i in range(n) for j in range(i + 1, n) if (adj[i] >> j) & 1]


def remove_edge(adj, i, j):
    b = list(adj)
    b[i] &= ~(1 << j)
    b[j] &= ~(1 << i)
    return b


def criticalize(n, adj, rng):
    """Point fixe du retrait d'aretes sous (chi>=4) ET (P8-free)."""
    cur = list(adj)
    changed = True
    while changed:
        changed = False
        es = edge_list(n, cur)
        rng.shuffle(es)
        for (i, j) in es:
            cand = remove_edge(cur, i, j)
            if three_colorable(n, cand):
                continue
            if longest_induced_path(n, cand, cap=8) >= 8:
                continue
            cur = cand
            changed = True
            break
    return cur


def coarse_key(n, adj):
    tri = []
    for v in range(n):
        t = 0
        m = adj[v]
        while m:
            u = (m & -m).bit_length() - 1
            m &= m - 1
            t += bin(adj[v] & adj[u]).count('1')
        tri.append(t // 2)
    degs = [bin(a).count('1') for a in adj]
    return (sum(degs) // 2, tuple(sorted(degs)), tuple(sorted(zip(degs, tri))))


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    tries = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260722
    cap_tests = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    rng = random.Random(seed + 1)
    t0 = time.time()
    cands = gen_candidates(n, tries, seed)
    print(f"n={n}: {len(cands)} candidats regeneres ({time.time()-t0:.0f}s)", flush=True)
    t0 = time.time()
    cores, seen = [], {}
    shave = []
    for adj, p in cands:
        core = criticalize(n, adj, rng)
        m0 = sum(bin(a).count('1') for a in adj) // 2
        m1 = sum(bin(a).count('1') for a in core) // 2
        shave.append(m0 - m1)
        k = coarse_key(n, core)
        if k not in seen:
            seen[k] = core
    cores = sorted(seen.values(), key=lambda a: sum(bin(x).count('1') for x in a))
    print(f"criticalisation: {len(cores)} coeurs distincts (invariant grossier), "
          f"aretes rasees en moyenne {sum(shave)/len(shave):.1f}, "
          f"coeurs de {sum(bin(x).count('1') for x in cores[0])//2} a "
          f"{sum(bin(x).count('1') for x in cores[-1])//2} aretes ({time.time()-t0:.0f}s)",
          flush=True)
    # ordre effectif = sommets non isoles ; eff <= 10 est deja couvert par
    # le census exhaustif -> seuls les coeurs eff >= 11 valent un test
    def eff_order(a):
        return sum(1 for x in a if x)
    small = sum(1 for c in cores if eff_order(c) <= 10)
    print(f"coeurs d'ordre effectif <= 10 (deja couverts par le census) : "
          f"{small}/{len(cores)}", flush=True)
    # ne pas retester ce que la chasse a deja couvert
    try:
        done = {r['g6'] for r in json.load(open(f'results/refute_hunt_n{n}.json'))}
    except Exception:
        done = set()
    out = []
    todo = [c for c in cores if eff_order(c) >= 11
            and to_graph6(n, c) not in done][:cap_tests]
    print(f"tests: {len(todo)} coeurs eff>=11 (cap {cap_tests})", flush=True)
    for i, core in enumerate(todo):
        t1 = time.time()
        ok, nr, nc, primes = degree4_full(n, core)
        rec = {'g6': to_graph6(n, core), 'eff': eff_order(core),
               'edges': sum(bin(a).count('1') for a in core) // 2,
               'rows': nr, 'cols': nc, 'deg4_solvable': ok, 'primes': primes,
               'time_s': round(time.time() - t1)}
        out.append(rec)
        flag = '' if ok else '  <<< INSOLVABLE AU DEGRE 4 — GRAINE DE REFUTATION'
        print(f"  [{i+1}/{len(todo)}] {rec['edges']} aretes {nr}x{nc} "
              f"solvable={ok} ({rec['time_s']}s){flag}", flush=True)
        json.dump(out, open(f'results/critical_cores_n{n}.json', 'w'), indent=1)
    solv = sum(1 for r in out if r['deg4_solvable'])
    print(f"BILAN coeurs n={n}: {solv}/{len(out)} solvables au degre 4", flush=True)
