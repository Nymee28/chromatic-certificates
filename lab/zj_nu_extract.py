#!/usr/bin/env python3
"""Extraction EXACTE de nu : la loi par etiquettes de ZJ, sur Q, avec temoin.

Pour une strate (representee par son dump sature k=34 paire / k=35 impaire) :
  1. construit le systeme fini des etiquettes (zj_label_solve.build_label_system),
     colonnes triees par etiquette (ordre canonique reproductible) ;
  2. RREF uint8 multi-premiers (zj_bigrref via zj_bigcert.run_primes), variables
     libres = 0, rangs/pivots concordants ; CRT + reconstruction rationnelle ;
  3. verification EXACTE sur Q du systeme des etiquettes (Fractions, creux) ;
  4. TEMOIN : instancie mu = nu(etiquette)/n sur le membre sature jumeau
     (k=32 pour la strate paire, k=33 pour l'impaire), et verification exacte
     complete par re-expansion polynomiale (zj_core.verify_exact) — le meme
     etalon-or que tous les certificats du dossier.
Sortie : zj_nu_k{K}.json (la table nu + statuts) ; log incremental.
"""
import json, sys, time
from fractions import Fraction
from collections import defaultdict

from zj_label_solve import build_label_system
from zj_bigcert import run_primes, reconstruct
from zj_bigrref import PRIMES_8BIT
import zj_transfer_check as T
from zj_core import verify_exact


def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)


def extract_nu(k_dump, k_witness):
    rows, target, col_ix = build_label_system(k_dump)
    ncols = len(col_ix)
    # ordre canonique des colonnes : tri par etiquette
    order = sorted(range(ncols), key=lambda c: str(next(
        lab for lab, i in col_ix.items() if i == c)))
    # plus efficace : inverser d'abord
    inv = [None] * ncols
    for lab, i in col_ix.items():
        inv[i] = lab
    order = sorted(range(ncols), key=lambda c: str(inv[c]))
    pos = {c: j for j, c in enumerate(order)}
    labels_sorted = [inv[c] for c in order]
    entries = {}
    for r, row in enumerate(rows):
        for c, v in row.items():
            entries[(r, pos[c])] = v
    const_row = len(rows) - 1
    assert target[const_row] == 1 and all(t == 0 for t in target[:-1])
    log(f"strate k={k_dump}: systeme etiquettes {len(rows)}x{ncols} "
        f"nnz={len(entries)}")

    import pickle, os
    nprimes = 6
    res = []
    while True:
        for p in PRIMES_8BIT[:nprimes]:
            if any(r[0] == p for r in res):
                continue
            ck = f'results/zj_nu_ckpt_k{k_dump}_p{p}.pkl'
            if os.path.exists(ck):
                with open(ck, 'rb') as f:
                    res.append(pickle.load(f))
                log(f"p={p}: checkpoint charge")
                continue
            one = run_primes(entries, const_row, len(rows), ncols, [p],
                             log=log, trail_chunk=4096)
            if not one:
                log(f"p={p}: INCONSISTANT -- inattendu (solvabilite certifiee)")
                continue
            with open(ck, 'wb') as f:
                pickle.dump(one[0], f)
            res.append(one[0])
        if not res:
            log("aucun premier concluant : abandon")
            return None
        sol, maxden = reconstruct(res, labels_sorted)
        if sol is not None:
            break
        nprimes += 2
        if nprimes > 14:
            log("ratrec echoue a 14 premiers, abandon")
            return None
        log(f"ratrec incomplet, extension a {nprimes} premiers")
    nz = sum(1 for v in sol.values() if v)
    log(f"nu reconstruit : {nz} etiquettes non nulles / {ncols}, "
        f"maxden={maxden}, {len(res)} premiers")

    # 3. verification exacte du systeme des etiquettes sur Q
    t0 = time.time()
    lab_val = {lab: Fraction(v) for lab, v in sol.items()}
    ok_labels = True
    for r, row in enumerate(rows):
        s = sum(v * lab_val.get(inv[c], Fraction(0)) for c, v in row.items())
        want = 1 if r == const_row else 0
        if s != want:
            ok_labels = False
            log(f"ECHEC exact ligne {r}: {s} != {want}")
            break
    log(f"verification exacte du systeme des etiquettes : {ok_labels} "
        f"({time.time()-t0:.0f}s)")

    # 4. temoin : instanciation exacte
    n, row_mono, col_w, entries_w, = T.build_labeled(k_witness)
    mu = {}
    missing = 0
    for w in col_w:
        lab = T.col_label(w, n)
        if lab in lab_val:
            v = lab_val[lab]
            if v:
                mu[w] = v / n
        else:
            missing += 1
    log(f"temoin k={k_witness} (n={n}): {len(mu)} paires non nulles, "
        f"etiquettes absentes de la table: {missing}")
    t0 = time.time()
    ok_witness = verify_exact(n, mu)
    log(f"VERIFICATION EXACTE TEMOIN k={k_witness}: {ok_witness} "
        f"({time.time()-t0:.0f}s)")

    out = {'k_dump': k_dump, 'k_witness': k_witness, 'n_witness': n,
           'ncols': ncols, 'nrows': len(rows), 'nz': nz,
           'maxden': int(maxden), 'primes': [r[0] for r in res],
           'label_system_exact_ok': ok_labels,
           'witness_exact_ok': bool(ok_witness),
           'nu_table': {str(lab): [v.numerator, v.denominator]
                        for lab, v in lab_val.items() if v}}
    json.dump(out, open(f'results/zj_nu_k{k_dump}.json', 'w'), indent=1)
    log(f"ecrit zj_nu_k{k_dump}.json")
    return out


if __name__ == '__main__':
    for kd, kw in [(int(sys.argv[1]), int(sys.argv[2]))] if len(sys.argv) > 2 \
            else [(34, 32), (35, 33)]:
        extract_nu(kd, kw)
