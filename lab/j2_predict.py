#!/usr/bin/env python3
"""CC-02, mission A' : le test de la prediction 2-periodique.

Fait etabli (CC-01 + analyse) : les solutions canoniques par q sont
EXACTEMENT 2-periodiques des q = 6 — solution(q) = V_pair (q pair,
= j2_labels_q8.json) ou V_impair (q impair, = j2_labels_q7.json),
verifie bit-a-bit sur q = 6, 7, 8, 9.

Prediction falsifiable : V_{q mod 2} satisfait le systeme d'etiquettes de
TOUT q >= 6. Ce script la teste a un q donne : build du systeme, evaluation
de V (pas de solve — bien moins cher), verdict.

Usage : python j2_predict.py <q> [chemin_V_pair.json] [chemin_V_impair.json]
Sortie : resultats/j2_predict_q<q>.json ; tout ECHEC = alerte tete de bilan.
"""
import json, os, sys, time
from fractions import Fraction
from collections import defaultdict
from j2_labels import build_label_system

q = int(sys.argv[1])
here = os.path.dirname(os.path.abspath(__file__))
res = os.path.join(here, 'resultats')
vp = sys.argv[2] if len(sys.argv) > 2 else os.path.join(res, 'j2_labels_q8.json')
vi = sys.argv[3] if len(sys.argv) > 3 else os.path.join(res, 'j2_labels_q7.json')
src = vp if q % 2 == 0 else vi
d = json.load(open(src))
V = {lb: Fraction(f) for lb, f in d['sol']}
print(f"q={q} : V_{'pair' if q % 2 == 0 else 'impair'} chargee depuis "
      f"{os.path.basename(src)} ({len(V)} constantes)", flush=True)

t0 = time.time()
ent, cst, nrows, labs, n = build_label_system(q)
print(f"systeme q={q} (n={n}) : {nrows} equations x {len(labs)} etiquettes "
      f"(build {time.time()-t0:.0f}s)", flush=True)

rowsum = defaultdict(Fraction)
for (r, c), v in ent.items():
    f = V.get(labs[c])
    if f:
        rowsum[r] += v * f
bad = sum(1 for r in range(nrows)
          if (rowsum.get(r, Fraction(0)) != (1 if r == cst else 0)))
verdict = 'PREDICTION OK' if bad == 0 else \
    f'ECHEC — {bad}/{nrows} equations violees  <<< ALERTE TETE DE BILAN'
print(f"q={q} : {verdict}", flush=True)
json.dump({'q': q, 'n': n, 'equations': nrows, 'etiquettes': len(labs),
           'source_V': os.path.basename(src), 'constantes': len(V),
           'violees': bad, 'ok': bad == 0},
          open(os.path.join(res, f'j2_predict_q{q}.json'), 'w'), indent=1)
print("FIN", flush=True)
