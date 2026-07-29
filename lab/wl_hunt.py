#!/usr/bin/env python3
"""Chasse adverse K4.2 : existe-t-il des graphes P8-free A LONG RAFFINEMENT ?

La Conjecture K4.2 dit : le raffinement de couleurs (1-WL) stabilise en O(1)
rondes sur tout P8-free connexe (mesure : jamais > 5 sur 617 graphes).
Cette chasse essaie de la TUER : recherche locale maximisant le nombre de
rondes sous contrainte P8-free.

Usage : python wl_hunt.py [n_max=32] [restarts=40] [steps=400] [seed]
Sortie : wl_hunt.json (par n : record de rondes, graph6 du recordman).
Tout record > 8 rondes est une alerte a signaler en tete de bilan.
"""
import json, random, sys
from census import longest_induced_path, to_graph6


def wl_rounds(n, adj):
    col = [bin(a).count('1') for a in adj]
    rounds = 0
    while True:
        sig = []
        for v in range(n):
            nb = []
            m = adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                nb.append(col[u])
            sig.append((col[v], tuple(sorted(nb))))
        ids = {}
        new = [0] * n
        for v in range(n):
            if sig[v] not in ids:
                ids[sig[v]] = len(ids)
            new[v] = ids[sig[v]]
        if len(ids) == len(set(col)):
            old_part = {}
            for v in range(n):
                old_part.setdefault(col[v], []).append(v)
            new_part = {}
            for v in range(n):
                new_part.setdefault(new[v], []).append(v)
            if sorted(old_part.values()) == sorted(new_part.values()):
                return rounds
        col = new
        rounds += 1


def connected(n, adj):
    seen = 1
    stack = [0]
    while stack:
        v = stack.pop()
        m = adj[v] & ~seen
        while m:
            u = (m & -m).bit_length() - 1
            m &= m - 1
            seen |= 1 << u
            stack.append(u)
    return seen == (1 << n) - 1


def p8free(n, adj):
    return longest_induced_path(n, adj, cap=8) < 8


def random_p8free(n, rng):
    """Depart : graphe aleatoire densifie jusqu'a P8-liberte + connexite."""
    adj = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.35:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    guard = 0
    while (not p8free(n, adj) or not connected(n, adj)) and guard < 4000:
        i, j = rng.randrange(n), rng.randrange(n)
        if i != j and not (adj[i] >> j) & 1:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
        guard += 1
    return adj if p8free(n, adj) and connected(n, adj) else None


def hunt(n, restarts, steps, rng):
    best_r, best_g = -1, None
    for _ in range(restarts):
        adj = random_p8free(n, rng)
        if adj is None:
            continue
        cur = wl_rounds(n, adj)
        for _ in range(steps):
            i, j = rng.randrange(n), rng.randrange(n)
            if i == j:
                continue
            b = list(adj)
            if (b[i] >> j) & 1:
                b[i] &= ~(1 << j)
                b[j] &= ~(1 << i)
            else:
                b[i] |= 1 << j
                b[j] |= 1 << i
            if not p8free(n, b) or not connected(n, b):
                continue
            r = wl_rounds(n, b)
            if r >= cur:          # montee + plateaux acceptes
                adj, cur = b, r
        if cur > best_r:
            best_r, best_g = cur, to_graph6(n, adj)
    return best_r, best_g


if __name__ == '__main__':
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 20260724
    rng = random.Random(seed)
    out = []
    for n in range(12, n_max + 1, 4):
        r, g = hunt(n, restarts, steps, rng)
        rec = {'n': n, 'record_rondes': r, 'g6': g,
               'restarts': restarts, 'steps': steps}
        out.append(rec)
        alerte = '   <<< ALERTE : > 8 RONDES, GRAINE CONTRE K4.2' if r > 8 else ''
        print(f"n={n:3d} : record {r} rondes{alerte}", flush=True)
        json.dump(out, open('wl_hunt.json', 'w'), indent=1)
    print("FIN", flush=True)
