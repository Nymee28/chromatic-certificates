#!/usr/bin/env python3
"""Verification independante de la presentation jointe, SOUS le quotient.

La solution jointe (309 constantes par etiquette) a ete verifiee sur les
systemes-quotients. Ici on redescend a l'etage des COLONNES : pour chaque q,
reconstruire le systeme restreint (ecart<=3, gadget L=3, <=1 eclaireur),
etendre mu[colonne] = nu*[etiquette(colonne)], et verifier A.mu = e_const
sur Q, ligne par ligne — cela teste aussi le code de quotientage lui-meme.
"""
import json, time
from fractions import Fraction
from collections import defaultdict
from pillars import G_CH
from j2_ch4 import build_with_cols
from j2_scout import keep_scout_gadget
from j2_labels import label_of

sol = json.load(open('results/j2_joint4.json'))
nu = {}
for lbs, fs in sol['solution']:
    nu[eval(lbs)] = Fraction(fs)
print(f"presentation chargee : {len(nu)} constantes, qs={sol['qs']}",
      flush=True)

for q in (3, 4, 5, 6):
    t0 = time.time()
    n, adj = G_CH(q, 4)
    entries, const, nrows, cols, col_ix = build_with_cols(
        n, adj, {1, 5}, 4, max_gap=3, order=True)
    keep = {i for i, w in enumerate(cols) if keep_scout_gadget(w, n, 3, 1)}
    mu = {}
    for i in keep:
        lb = label_of(cols[i], n, 3)
        f = nu.get(lb)
        if f:
            mu[i] = f
    rowsum = defaultdict(Fraction)
    for (r, c), v in entries.items():
        if c in mu:
            rowsum[r] += v * mu[c]
    bad = sum(1 for r, s in rowsum.items()
              if (s != 1 if r == const else s != 0))
    okc = rowsum.get(const, Fraction(0)) == 1
    verdict = 'OK' if (bad == 0 and okc) else f'ECHEC ({bad} lignes, const={okc})'
    print(f"q={q} (n={n}) : {nrows} lignes, {len(mu)} colonnes actives "
          f"-> VERIFICATION {verdict} ({time.time()-t0:.0f}s)", flush=True)
print("FIN", flush=True)
