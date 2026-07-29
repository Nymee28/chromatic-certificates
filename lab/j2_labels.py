#!/usr/bin/env python3
"""J2, derniere marche : le systeme d'etiquettes mod 4 — la presentation.

Etiquette de colonne (independante de n) :
    (ecart de l'arete, gadget local (offsets <= 3, normalise), exposant de
     l'eclaireur, residu mod 4 de sa position, signe/pli de sa position)
Ansatz : le coefficient ne depend que de l'etiquette. Le systeme quotient
(equations = lignes du systeme restreint, inconnues = etiquettes) est fini
et le MEME pour tout q sature. S'il est solvable a q=3 ET q=4 avec les
memes valeurs sur les etiquettes partagees, la presentation finie de
G(q,4) mod 4 existe en deux points — le theoreme 1 bis est en vue.
"""
import json, sys, time
from fractions import Fraction
from collections import defaultdict
from math import lcm
from pillars import G_CH
from j2_ch4 import build_with_cols, mono_shape, gap_of
from j2_scout import keep_scout_gadget
from certificates import rref_particular, crt, ratrec, P1, P2


def label_of(w, n, L=3):
    sh = mono_shape(w, n)
    far = [t for t in sh if abs(t[0]) > L]
    near = tuple(t for t in sh if abs(t[0]) <= L)
    g = gap_of(w[0], n)
    if not far:
        return (g, near, None, None, None)
    (o, e), = far
    half = n // 2
    side = 'S' if abs(o) == half else ('+' if o > 0 else '-')
    return (g, near, e, o % 4, side)


def build_label_system(q, L=3):
    n, adj = G_CH(q, 4)
    entries, const, nrows, cols, col_ix = build_with_cols(
        n, adj, {1, 5}, 4, max_gap=3, order=True)
    keep = [i for i, w in enumerate(cols) if keep_scout_gadget(w, n, L, 1)]
    labs, lab_ix = [], {}
    colmap = {}
    for i in keep:
        lb = label_of(cols[i], n, L)
        if lb not in lab_ix:
            lab_ix[lb] = len(labs)
            labs.append(lb)
        colmap[i] = lab_ix[lb]
    ent2 = defaultdict(int)
    for (r, c), v in entries.items():
        j = colmap.get(c)
        if j is not None:
            ent2[(r, j)] += v
    # dedoublonner les equations identiques
    rows = defaultdict(list)
    for (r, c), v in ent2.items():
        rows[r].append((c, v))
    sig = {}
    const_sig = None
    for r, terms in rows.items():
        s = tuple(sorted(terms))
        if r == const:
            const_sig = s
        sig.setdefault(s, r)
    uniq = list(sig)
    ent3 = {}
    cst3 = None
    for ri, s in enumerate(uniq):
        if s == const_sig:
            cst3 = ri
        for c, v in s:
            ent3[(ri, c)] = v
    return ent3, cst3, len(uniq), labs, n


def solve_exact(ent, const, nrows, ncols):
    sols = {}
    for p in (P1, P2):
        x, piv = rref_particular(ent, const, nrows, ncols, p)
        if x is None:
            return None, p
        sols[p] = x
    M = P1 * P2
    mu = {}
    for c in sorted(set(sols[P1]) | set(sols[P2])):
        f = ratrec(crt(sols[P1].get(c, 0) % P1, sols[P2].get(c, 0) % P2), M)
        if f is None:
            return None, 'ratrec'
        if f:
            mu[c] = f
    rowsum = defaultdict(Fraction)
    for (r, c), v in ent.items():
        if c in mu:
            rowsum[r] += v * mu[c]
    ok = all((s == 1 if r == const else s == 0) for r, s in rowsum.items()) \
        and rowsum[const] == 1
    return (mu if ok else None), ('OK' if ok else 'verif')


if __name__ == '__main__':
    qs = [int(a) for a in sys.argv[1:]] or [3, 4]
    per_q = {}
    for q in qs:
        t0 = time.time()
        ent, const, nrows, labs, n = build_label_system(q)
        print(f"q={q} (n={n}): systeme d'etiquettes {nrows} equations x "
              f"{len(labs)} etiquettes (build {time.time()-t0:.0f}s)",
              flush=True)
        t0 = time.time()
        mu, status = solve_exact(ent, const, nrows, len(labs))
        if mu is None:
            print(f"  INSOLVABLE / echec ({status}) — l'ansatz "
                  f"etiquette-constante est trop grossier a q={q}", flush=True)
            per_q[q] = None
            continue
        dens = 1
        for f in mu.values():
            dens = lcm(dens, f.denominator)
        print(f"  SOLVABLE EXACT ({time.time()-t0:.0f}s) : {len(mu)} "
              f"etiquettes non nulles, denominateur LCM = {dens}", flush=True)
        per_q[q] = {labs[c]: f for c, f in mu.items()}
        json.dump({'q': q, 'n': n, 'rows': nrows, 'labels': len(labs),
                   'dens': str(dens),
                   'sol': [[str(lb), str(f)] for lb, f in per_q[q].items()]},
                  open(f'results/j2_labels_q{q}.json', 'w'), indent=1)
    qs_ok = [q for q in qs if per_q.get(q)]
    if len(qs_ok) >= 2:
        a, b = qs_ok[0], qs_ok[1]
        A, B = per_q[a], per_q[b]
        shared = set(A) & set(B)
        eq = sum(1 for lb in shared if A[lb] == B[lb])
        print(f"COMPARAISON q={a} / q={b} : {len(A)} vs {len(B)} etiquettes "
              f"actives, {len(shared)} partagees, {eq} EGALES", flush=True)
        rows = []
        for lb in sorted(shared, key=str)[:2000]:
            rows.append([str(lb), str(A[lb]), str(B[lb]), A[lb] == B[lb]])
        json.dump({'q': qs_ok, 'actives': {str(q): len(per_q[q]) for q in qs_ok},
                   'partagees': len(shared), 'egales': eq,
                   'detail': rows},
                  open('results/j2_labels_cmp.json', 'w'), indent=1)
    print("FIN", flush=True)
