#!/usr/bin/env python3
"""J2, test (c) : l'axe eclaireur x gadget — le bon axe d'etiquetage.

Verdict des balayages (a)-(b) : le diametre minimal suffisant est MAXIMAL
(6 = max a n=13, 8 = max a n=17) — le support doit atteindre l'antipode,
comme pour le pilier k=3 (zones a l'antipode). L'axe par-diametre-borne est
mort ; l'axe du pilier 1 est : gadget LOCAL pres de l'arete + UN eclaireur
libre (position quotientee par la loi de zone). Test : le systeme restreint
aux colonnes de cette forme est-il solvable, a q=3 et q=4, a L fixe ?

  forme retenue : au plus `scouts` variables a distance > L de l'arete,
  le reste (gadget) a distance <= L. Variantes L = 2, 3 ; scout deg <= 3.
"""
import json, sys, time
from pillars import G_CH
from j2_ch4 import build_with_cols, mono_shape
from sparse_wiedemann import solvable_sparse


def keep_scout_gadget(w, n, L, max_scouts):
    sh = mono_shape(w, n)
    far = [t for t in sh if abs(t[0]) > L]
    return len(far) <= max_scouts


if __name__ == '__main__':
    qs = [int(a) for a in sys.argv[1:]] or [3, 4]
    out = []
    for q in qs:
        n, adj = G_CH(q, 4)
        print(f"G_CH({q},4): n={n} — axe eclaireur x gadget (ecart <= 3)",
              flush=True)
        base = build_with_cols(n, adj, {1, 5}, 4, max_gap=3)
        entries, const, nrows, cols, col_ix = base
        for L in (2, 3):
            for ns in (1, 2):
                kept = [i for i, w in enumerate(cols)
                        if keep_scout_gadget(w, n, L, ns)]
                remap = {c: j for j, c in enumerate(kept)}
                ent2 = {}
                for (r, c), v in entries.items():
                    j = remap.get(c)
                    if j is not None:
                        ent2[(r, j)] = v
                t0 = time.time()
                res = solvable_sparse(ent2, const, nrows, len(kept),
                                      verbose=False)
                rec = {'q': q, 'n': n, 'L': L, 'scouts': ns,
                       'rows': nrows, 'cols': len(kept),
                       'solvable': res['solvable'], 'primes': res['primes'],
                       'solve_s': round(time.time() - t0)}
                out.append(rec)
                print(f"  L={L}, eclaireurs<={ns}: {nrows}x{len(kept)} "
                      f"solvable={res['solvable']} ({rec['solve_s']}s)",
                      flush=True)
                json.dump(out, open('results/j2_scout.json', 'w'),
                          indent=1)
                if res['solvable']:
                    break
    print("FIN", flush=True)
