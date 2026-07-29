#!/usr/bin/env python3
"""Combler l'ecart k=9..31 : solvabilite directe (Wiedemann creux, residu
certifie) du systeme ansatz {1,5,8} x W=4 pour chaque membre intermediaire."""
import json, sys, time
from zj_transfer_check import build_labeled
from sparse_wiedemann import solvable_sparse

import os
out = {}
if os.path.exists('results/zj_gap_results.json'):
    out = {int(k): v for k, v in json.load(open('results/zj_gap_results.json')).items()}
    print(f"reprise: {sorted(out)} deja au registre", flush=True)
for k in range(9, 32):
    if k in out:
        continue
    t0 = time.time()
    n, row_mono, col_w, entries = build_labeled(k)
    e2 = {}
    for (r, c), v in entries.items():
        e2[(r, c)] = v
    res = solvable_sparse(e2, 0, len(row_mono), len(col_w), verbose=False)
    print(f"k={k} n={n}: solvable={res['solvable']} primes={res['primes']} "
          f"({time.time()-t0:.0f}s)", flush=True)
    out[k] = {'n': n, 'solvable': res['solvable'], 'primes': res['primes']}
    json.dump(out, open('results/zj_gap_results.json', 'w'), indent=1)
