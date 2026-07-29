#!/usr/bin/env python3
"""J2, l'assaut final : le systeme JOINT des etiquettes mod 4.

Les etiquettes (ecart, gadget, exposant d'eclaireur, residu mod 4, pli)
sont independantes de n. On empile les equations-quotient de q = 3, 4, 5, 6
(labels partages identifies par leur tuple), on dedoublonne, et on cherche
UNE solution exacte sur Q.

  SOLVABLE  => la loi des constantes est "une constante par etiquette,
               aucune dependance en n" ; l'objet est LA presentation finie
               de G(q,4) mod 4 sur les quatre ordres — et une prediction
               falsifiable pour q = 7, 8 (les points de l'executant CC).
  INSOLVABLE => la loi a une dependance en n ; on bascule sur l'ajustement
               par etiquette (constant / c0 + c1/n) en repli.
"""
import json, time
from fractions import Fraction
from collections import defaultdict
from math import lcm
from j2_labels import build_label_system, solve_exact
from certificates import rref_particular, crt, ratrec, P1, P2

QS = [3, 4, 5, 6]

lab_ix, labels = {}, []
rows_sig = {}
const_sig = None
per_q_rows = {}

for q in QS:
    t0 = time.time()
    ent, const, nrows, labs, n = build_label_system(q)
    print(f"q={q} (n={n}): {nrows} eqs x {len(labs)} etiquettes "
          f"({time.time()-t0:.0f}s)", flush=True)
    # remapper vers l'espace global d'etiquettes
    gmap = {}
    for j, lb in enumerate(labs):
        if lb not in lab_ix:
            lab_ix[lb] = len(labels)
            labels.append(lb)
        gmap[j] = lab_ix[lb]
    rows = defaultdict(list)
    for (r, c), v in ent.items():
        rows[r].append((gmap[c], v))
    nq = 0
    for r, terms in rows.items():
        s = tuple(sorted(terms))
        if r == const:
            const_sig = s
        if s not in rows_sig:
            rows_sig[s] = len(rows_sig)
            nq += 1
    per_q_rows[q] = len(rows)
    print(f"   -> global : {len(labels)} etiquettes, {len(rows_sig)} "
          f"equations distinctes (+{nq})", flush=True)

ent3, cst3 = {}, None
for s, ri in rows_sig.items():
    if s == const_sig:
        cst3 = ri
    for c, v in s:
        ent3[(ri, c)] = v
print(f"JOINT : {len(rows_sig)} equations x {len(labels)} etiquettes, "
      f"nnz {len(ent3)}", flush=True)

t0 = time.time()
mu, status = solve_exact(ent3, cst3, len(rows_sig), len(labels))
if mu is None:
    print(f"JOINT INSOLVABLE / echec ({status}) — la loi depend de n ; "
          f"repli sur l'ajustement par etiquette.", flush=True)
else:
    dens = 1
    for f in mu.values():
        dens = lcm(dens, f.denominator)
    print(f"JOINT SOLVABLE EXACT ({time.time()-t0:.0f}s) : {len(mu)} "
          f"etiquettes actives, denominateur LCM = {dens}", flush=True)
    json.dump({'qs': QS, 'equations': len(rows_sig), 'etiquettes': len(labels),
               'actives': len(mu), 'dens_lcm': str(dens),
               'solution': [[str(labels[c]), str(f)] for c, f in
                            sorted(mu.items())]},
              open('results/j2_joint4.json', 'w'), indent=1)
print("FIN", flush=True)
