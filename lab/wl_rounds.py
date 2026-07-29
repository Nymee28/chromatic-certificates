#!/usr/bin/env python3
"""K4, contre-test machine : la profondeur de la DECOUVERTE sur notre classe.

Le raffinement de couleurs (1-WL) est le squelette P-complet de la phase de
decouverte (A.6.6, A.7.14 du compendium ; pire cas Theta(n) rondes — les
graphes "long-refinement" sont construits sur de longs chemins). Question :
combien de rondes la classe P8-free demande-t-elle ?

Hypothese (la promesse aplatit les deux etages) : diametre <= 6 => tres peu
de rondes ; les temoins a longs chemins induits (controles) en demandent
beaucoup plus, lineairement pour les chemins purs.
"""
import json
from collections import Counter
from topo_lab import parse_g6
from pillars import G_ZJ
from pokrovskiy import G as G_pok


def wl_rounds(n, adj):
    col = {v: bin(adj[v]).count('1') for v in range(n)}
    rounds = 0
    while True:
        sig = {}
        for v in range(n):
            nb = []
            m = adj[v]
            while m:
                u = (m & -m).bit_length() - 1
                m &= m - 1
                nb.append(col[u])
            sig[v] = (col[v], tuple(sorted(nb)))
        # renumeroter
        ids = {}
        new = {}
        for v in range(n):
            if sig[v] not in ids:
                ids[sig[v]] = len(ids)
            new[v] = ids[sig[v]]
        if len(set(new.values())) == len(set(col.values())):
            # meme nombre de classes : verifier partition identique
            part_old = {}
            for v in range(n):
                part_old.setdefault(col[v], set()).add(v)
            part_new = {}
            for v in range(n):
                part_new.setdefault(new[v], set()).add(v)
            if sorted(map(sorted, part_old.values())) == \
               sorted(map(sorted, part_new.values())):
                return rounds, len(set(col.values()))
        col = new
        rounds += 1


def path(n):
    adj = [0] * n
    for i in range(n - 1):
        adj[i] |= 1 << (i + 1)
        adj[i + 1] |= 1 << i
    return n, adj


def stats(name, graphs):
    rs = []
    for n, adj in graphs:
        r, ncls = wl_rounds(n, adj)
        rs.append((r, n, ncls))
    mx = max(rs)
    print(f"{name:34s} | {len(rs):4d} graphes | rondes max {mx[0]:3d} "
          f"(n={mx[1]}, {mx[2]} classes) | moy {sum(r for r,_,_ in rs)/len(rs):.2f}",
          flush=True)
    return {'groupe': name, 'k': len(rs), 'max_rondes': mx[0],
            'n_du_max': mx[1], 'moyenne': round(sum(r for r,_,_ in rs)/len(rs), 2)}


if __name__ == '__main__':
    out = []
    # 1. les 477 obstructions du census (P8-free, n <= 10)
    cens = [parse_g6(r['g6']) for r in json.load(open('lab_sdp.json'))]
    out.append(stats('census P8-free chi>=4 (n<=10)', cens))
    # 2. les chasses n=14..17 (P8-free, hors echantillon)
    hunt = []
    for nn in (14, 15, 16, 17):
        try:
            hunt += [parse_g6(r['g6'])
                     for r in json.load(open(f'refute_hunt_n{nn}.json'))]
        except Exception:
            pass
    out.append(stats('chasses n=14..17 (P8-free)', hunt))
    # 3. coeurs critiques n=14
    cores = [parse_g6(r['g6']) for r in json.load(open('critical_cores_n14.json'))]
    out.append(stats('coeurs critiques n=14 (P8-free)', cores))
    # 4. CONTROLE en taille : les instances eparses A LONGS CHEMINS (densify avant)
    dens = [parse_g6(r['g6_avant']) for r in json.load(open('densify_n14.json'))]
    out.append(stats('CONTROLE longs chemins n=14', dens))
    # 5. et leurs versions densifiees P8-free (apres)
    densap = [parse_g6(t['g6_apres'])
              for r in json.load(open('densify_n14.json'))
              for t in r['trajectoires']]
    out.append(stats('memes instances P8-free-isees', densap))
    # 6. CONTROLE pur : les chemins P_n
    out.append(stats('CONTROLE chemins P_n (n=8..64)',
                     [path(n) for n in range(8, 65, 4)]))
    # 7. les familles transitives (degenerescence attendue : 0 ronde utile)
    out.append(stats('G(q,3) q=2..15 (transitifs)',
                     [G_pok(q) for q in range(2, 16)]))
    out.append(stats('G_ZJ(k) k=3..25 (transitifs)',
                     [G_ZJ(k) for k in range(3, 26)]))
    json.dump(out, open('wl_rounds.json', 'w'), indent=1)
    print("FIN", flush=True)
