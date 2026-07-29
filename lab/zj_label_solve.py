#!/usr/bin/env python3
"""Piste (f), etape 2 : SOLVABILITE DU SYSTEME FINI DES ETIQUETTES.

Le controle de stabilite (zj_transfer_check) a etabli : par strate de parite,
a saturation (n >= 104), les classes d'equations et leurs signatures sur les
etiquettes de colonnes sont IDENTIQUES pour tout n (100 % stables, 0/0).

Avec la normalisation d'orbite (coefficients bruts = n * cnt), en variables
nu(etiquette) = n * mu(etiquette), le systeme des classes est INDEPENDANT DE n:
    classe non-CONST :  sum cnt * nu = 0
    classe CONST     :  sum cnt * nu = 1
Une solution nu sur Q donne mu = nu/n : certificat de degre 4 pour TOUT n de
la strate (>= saturation ; n petits deja verifies directement k=3..8).

Ce script construit le systeme des etiquettes depuis un dump de classes et
teste sa solvabilite par Wiedemann creux mod >= 2 premiers concordants
(SOLVABLE certifie par residu explicite ; UNSOLVABLE par concordance).
"""
import json, pickle, sys, time
from collections import defaultdict


def load_dump(k):
    with open(f'results/zj_classes_k{k}.pkl', 'rb') as f:
        n, cls, ncl = pickle.load(f)
    return n, cls, ncl


def build_label_system(k):
    """Depuis le dump de classes(k) : lignes = classes (signatures uniques),
    colonnes = etiquettes de colonnes ; + la ligne CONST reconstruite depuis
    build_labeled (elle est retiree des dumps)."""
    n, cls, _ = load_dump(k)
    col_ix = {}
    rows = []                      # liste de dict {col: cnt}
    target = []                    # second membre par ligne

    def cix(cl):
        if cl not in col_ix:
            col_ix[cl] = len(col_ix)
        return col_ix[cl]

    seen_sigs = set()
    for lab, sigs in cls.items():
        assert len(sigs) == 1, f"classe incoherente {lab}"
        sig = next(iter(sigs))
        if sig in seen_sigs:
            continue               # equations dupliquees -> une seule fois
        seen_sigs.add(sig)
        rows.append({cix(cl): v for cl, v in _acc(sig).items()})
        target.append(0)

    # ligne CONST : reconstruire depuis le systeme brut de k
    import zj_transfer_check as T
    nn, row_mono, col_w, entries = T.build_labeled(k)
    clab = [T.col_label(w, nn) for w in col_w]
    const_sig = defaultdict(int)
    for (r, c), v in entries.items():
        if r == 0:                                 # ligne du monome constant
            assert v % nn == 0
            const_sig[clab[c]] += v // nn
    rows.append({cix(cl): v for cl, v in const_sig.items()})
    target.append(1)
    return rows, target, col_ix


def _acc(sig):
    d = defaultdict(int)
    for cl, v in sig:
        d[cl] += v
    return d


def main(k):
    t0 = time.time()
    rows, target, col_ix = build_label_system(k)
    nrows, ncols = len(rows), len(col_ix)
    nnz = sum(len(r) for r in rows)
    print(f"systeme des etiquettes (depuis k={k}): {nrows} x {ncols} nnz={nnz} "
          f"({time.time()-t0:.0f}s)", flush=True)
    # format sparse_wiedemann : entries {(r,c): v}, const = index ligne cible
    entries = {}
    for r, row in enumerate(rows):
        for c, v in row.items():
            entries[(r, c)] = v
    const_row = nrows - 1
    from sparse_wiedemann import solvable_sparse
    out = solvable_sparse(entries, const_row, nrows, ncols, verbose=True)
    print(f"VERDICT solvabilite du systeme des etiquettes (strate de k={k}): "
          f"{out}", flush=True)
    json.dump({'k': k, 'rows': nrows, 'cols': ncols, 'nnz': nnz,
               'result': {kk: (vv if isinstance(vv, (int, bool, str, list)) else str(vv))
                          for kk, vv in out.items()}},
              open(f'results/zj_label_solve_k{k}.json', 'w'), indent=1)


if __name__ == '__main__':
    main(int(sys.argv[1]))
