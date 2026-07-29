#!/usr/bin/env python3
"""Piste (f), jalon machine : structure ultimement periodique du systeme ansatz ZJ.

1. CLASSIFICATION : etiquettes de formes independantes de n pour les lignes
   (monomes canoniques) et colonnes (paires arete-multiplicateur canoniques) du
   systeme ansatz {1,5,8} x W=4. Codage : motifs de clusters exacts (offsets,
   exposants), separations exactes si <= EX, zone coeur ('B', s mod 3) sinon,
   zone antipode ('T', half - s) pres de n/2 ; pliage diedral.
2. COHERENCE intra-k : toutes les lignes d'une classe ont la meme signature
   (multiensemble de (etiquette-colonne, coefficient)).
3. STABILITE inter-k par strate de parite (n = 3k+10 : parite de n alterne
   avec k ; n === 1 mod 3 toujours) : classes et signatures identiques entre
   k et k+2 une fois les fenetres saturees.
4. Si stable : SOLVABILITE DU SYSTEME FINI DES ETIQUETTES (colonnes de meme
   etiquette forcees egales). Une solution etiquette-constante, instanciee a
   n quelconque de la strate, est un certificat : verification exacte sur un
   membre temoin. => reduction "degre 4 pour tout ZJ(k)" a une verification
   finie + argument de transfert [redaction].
"""
import itertools, json, sys, time
from collections import defaultdict
from pillars import G_ZJ
from zj_core import all_edges, gap, canon_pair, canon_mono, mul_red, edge_terms
from zj_ansatz import gadgets, GAPS

W = 4
EX = 15          # colonnes: separation codee exactement si <= EX
AMARGE = 9       # colonnes: zone antipode half - s <= AMARGE
MSEAM = 12       # marge de couture (distribution complete mesuree a k=20: max 12)
EXR = EX + MSEAM         # lignes: exact jusqu'a 18
AMR = AMARGE + MSEAM     # lignes: couture antipodale jusqu'a 12
SPLIT = 4        # coupure de clusters: ecart cyclique > SPLIT


def fast_canon_pair(e, m, n):
    """min sur les n rotations de (arete triee, monome trie) : l'arete minimale
    est (0, g) -- atteinte par l'unique rotation envoyant le bon sommet en 0."""
    a, b = e
    d = (b - a) % n
    if d <= n - d:
        s, g = -a % n, d
    else:
        s, g = -b % n, n - d
    return ((0, g), tuple(sorted(((v + s) % n, x) for v, x in m)))


def fast_canon_mono(m, n):
    """min sur les rotations : un point du support va en 0 (<= |support| candidats)."""
    if not m:
        return m
    best = None
    for v0, _ in m:
        cand = tuple(sorted(((v - v0) % n, x) for v, x in m))
        if best is None or cand < best:
            best = cand
    return best


# ------------------------------------------------------------- etiquettes ----
def _zone(s, n, ex=EX, am=AMARGE):
    half = n // 2
    if s <= ex:
        return ('E', s)
    if 0 <= half - s <= am:
        return ('T', half - s)
    return ('B', s % 3)


def _zone_row(s, n):
    return _zone(s, n, EXR, AMR)


def mono_label(mono, n):
    if not mono:
        return ('CONST',)
    exps = dict(mono)
    pts = sorted(exps)
    # clusters (coupure aux ecarts cycliques > SPLIT)
    gaps_c = [(pts[(i + 1) % len(pts)] - pts[i]) % n for i in range(len(pts))]
    if all(g <= SPLIT for g in gaps_c) and len(pts) > 1:
        # tout le cycle est un seul bloc dense (n petit) — motif global
        base = pts[0]
        pat = tuple(((v - base) % n, exps[v]) for v in pts)
        w = max(o for o, _ in pat)
        refl = tuple(sorted((w - o, e) for o, e in pat))
        return ('FULL', min(tuple(sorted(pat)), refl))
    # rotation pour commencer apres une coupure
    start = max(range(len(pts)), key=lambda i: gaps_c[i])
    order = pts[start + 1:] + pts[:start + 1]
    clusters, cur = [], [order[0]]
    for a, b in zip(order, order[1:]):
        if (b - a) % n > SPLIT:
            clusters.append(cur)
            cur = [b]
        else:
            cur.append(b)
    clusters.append(cur)
    # sequence circulaire (motif, separation->suivant) ; la PLUS GRANDE
    # separation est l'arc complementaire qui absorbe la croissance de n :
    # codee ('R', s mod 3) (phase invariante : n === 1 mod 3), jamais E/T/B.
    raw = []
    for i, cl in enumerate(clusters):
        base = cl[0]
        pat = tuple(sorted(((v - base) % n, exps[v]) for v in cl))
        nxt = clusters[(i + 1) % len(clusters)][0]
        sep = (nxt - cl[-1]) % n
        raw.append((pat, sep))
    smax = max(s for _, s in raw)
    seq = [(pat, ('R', s % 3) if s == smax else _zone_row(s, n)) for pat, s in raw]
    # canonique: rotations et reflexion
    def rots(s):
        return [tuple(s[i:] + s[:i]) for i in range(len(s))]
    refl_seq = []
    for pat, z in reversed(seq):
        w = max(o for o, _ in pat) if pat else 0
        refl_seq.append((tuple(sorted((w - o, e) for o, e in pat)), z))
    # decale les separations pour rester "motif -> sep vers suivant"
    zs = [z for _, z in refl_seq]
    zs = zs[1:] + zs[:1]
    refl_seq = [(p, z2) for (p, _), z2 in zip(refl_seq, zs)]
    cands = rots(seq) + rots(refl_seq)
    return ('S', min(cands))


def col_label(colw, n):
    (a, b), mono = colw
    d = (b - a) % n
    g = min(d, n - d)
    anchor = a if d == g else b
    exps = dict(mono)
    near, far = [], []
    for v, e in mono:
        off = (v - anchor) % n
        offm = off if off <= n - off else off - n     # signe: [-n/2, n/2]
        if -EX <= offm <= g + EX:
            near.append((offm, e))
        else:
            # distance a la fenetre (cote le plus proche), zonee
            dl = (anchor - v) % n                      # avant la fenetre
            dr = (v - (anchor + g)) % n                # apres la fenetre
            if dl == dr:                               # antipode exacte: symetrique
                far.append(('S', _zone(dr, n), e))
            elif dr < dl:
                far.append(('R', _zone(dr, n), e))
            else:
                far.append(('L', _zone(dl, n), e))
    near = tuple(sorted(near))
    far_t = tuple(sorted(far))
    # pliage diedral autour de l'arete: o -> g - o ; L <-> R
    near_r = tuple(sorted((g - o, e) for o, e in near))
    far_r = tuple(sorted(
        (('S' if s == 'S' else ('L' if s == 'R' else 'R')), z, e)
        for s, z, e in far))
    return ('C', g, min((near, far_t), (near_r, far_r)))


# ------------------------------------------------------- systeme + classes ----
def build_labeled(k):
    import pickle, os
    cache = f'results/zj_sys_cache_k{k}.pkl'
    if os.path.exists(cache):
        with open(cache, 'rb') as f:
            n, row_mono, col_w, entries = pickle.load(f)
        print(f"  k={k} n={n}: cache ({len(row_mono)}x{len(col_w)})", flush=True)
        return n, row_mono, col_w, entries
    n, adj = G_ZJ(k)
    t0 = time.time()
    edges = [e for e in all_edges(n, adj) if gap(e, n) in GAPS]
    gad_by_g = {g: gadgets(g, W) for g in GAPS}
    col_ix, row_mono, row_ix, entries = {}, [], {}, {}

    def rid(m):
        if m not in row_ix:
            row_ix[m] = len(row_ix)
            row_mono.append(m)
        return row_ix[m]

    rid(())
    col_w = []
    for e in edges:
        a, b = e
        d = (b - a) % n
        g = min(d, n - d)
        anchor = a if d == g else b
        monos = set()
        for j in range(n):
            monos.add(((j, 1),))
        for gad in gad_by_g[g]:
            base = {}
            for off, kk in gad:
                v = (anchor + off) % n
                base[v] = base.get(v, 0) + kk
            for j in range(n):
                m = dict(base)
                m[j] = m.get(j, 0) + 1
                mono = tuple(sorted((v, x % 3) for v, x in m.items() if x % 3))
                deg = sum(x for _, x in mono)
                if mono and deg % 3 == 1 and deg <= 4:
                    monos.add(mono)
        for m in monos:
            w = fast_canon_pair(e, m, n)
            if w not in col_ix:
                col_ix[w] = len(col_ix)
                col_w.append(w)
            c = col_ix[w]
            i, j = e
            for gt in edge_terms(i, j):
                r = rid(fast_canon_mono(mul_red(m, gt), n))
                entries[(r, c)] = entries.get((r, c), 0) + 1
    print(f"  k={k} n={n}: {len(row_mono)}x{len(col_w)} nnz={len(entries)} "
          f"build={time.time()-t0:.0f}s", flush=True)
    with open(cache, 'wb') as f:
        pickle.dump((n, row_mono, col_w, entries), f)
    return n, row_mono, col_w, entries


def classes(k):
    n, row_mono, col_w, entries = build_labeled(k)
    clab = [col_label(w, n) for w in col_w]
    rlab = [mono_label(m, n) for m in row_mono]
    by_row = defaultdict(list)
    for (r, c), v in entries.items():
        by_row[r].append((clab[c], v // n if v % n == 0 else (v, 'NONDIV')))
    sig_of_class = defaultdict(set)
    for r, lab in enumerate(rlab):
        sig = tuple(sorted(by_row.get(r, [])))
        sig_of_class[lab].add(sig)
    sig_of_class.pop(('CONST',), None)   # ligne constante: agregat, traitee a part
    n_col_labels = len(set(clab))
    return n, sig_of_class, n_col_labels


def compare(k1, k2):
    n1, c1, ncl1 = classes(k1)
    n2, c2, ncl2 = classes(k2)
    inc1 = sum(1 for v in c1.values() if len(v) > 1)
    inc2 = sum(1 for v in c2.values() if len(v) > 1)
    shared = set(c1) & set(c2)
    stable = sum(1 for x in shared if c1[x] == c2[x])
    o1, o2 = len(set(c1) - set(c2)), len(set(c2) - set(c1))
    ok = inc1 == inc2 == 0 and stable == len(shared) and o1 == o2 == 0
    print(f"k={k1} (n={n1}) vs k={k2} (n={n2}): classes {len(c1)}/{len(c2)} "
          f"(etiq. colonnes {ncl1}/{ncl2}) | incoherentes {inc1}/{inc2} | "
          f"communes {len(shared)}, stables {stable} | orphelines {o1}/{o2} "
          f"=> {'STABLE' if ok else 'PAS ENCORE STABLE'}", flush=True)
    return {'k': (k1, k2), 'n': (n1, n2), 'classes': (len(c1), len(c2)),
            'col_labels': (ncl1, ncl2), 'incoherent': (inc1, inc2),
            'shared': len(shared), 'stable': stable, 'orphans': (o1, o2), 'ok': ok}


def classes_dump(k):
    import pickle
    n, sig, ncl = classes(k)
    with open(f'results/zj_classes_k{k}.pkl', 'wb') as f:
        pickle.dump((n, dict(sig), ncl), f)
    print(f"dump k={k}: {len(sig)} classes, {ncl} etiquettes colonnes", flush=True)


def compare_dumps(k1, k2):
    import pickle
    with open(f'results/zj_classes_k{k1}.pkl', 'rb') as f:
        n1, c1, ncl1 = pickle.load(f)
    with open(f'results/zj_classes_k{k2}.pkl', 'rb') as f:
        n2, c2, ncl2 = pickle.load(f)
    inc1 = sum(1 for v in c1.values() if len(v) > 1)
    inc2 = sum(1 for v in c2.values() if len(v) > 1)
    shared = set(c1) & set(c2)
    stable = sum(1 for x in shared if c1[x] == c2[x])
    o1, o2 = len(set(c1) - set(c2)), len(set(c2) - set(c1))
    ok = inc1 == inc2 == 0 and stable == len(shared) and o1 == o2 == 0
    print(f"k={k1} (n={n1}) vs k={k2} (n={n2}): classes {len(c1)}/{len(c2)} "
          f"(etiq. colonnes {ncl1}/{ncl2}) | incoherentes {inc1}/{inc2} | "
          f"communes {len(shared)}, stables {stable} | orphelines {o1}/{o2} "
          f"=> {'STABLE' if ok else 'PAS ENCORE STABLE'}", flush=True)
    import json
    json.dump({'k': (k1, k2), 'n': (n1, n2), 'classes': (len(c1), len(c2)),
               'col_labels': (ncl1, ncl2), 'incoherent': (inc1, inc2),
               'shared': len(shared), 'stable': stable, 'orphans': (o1, o2),
               'ok': ok}, open(f'results/zj_transfer_verdict_{k1}_{k2}.json', 'w'))


if __name__ == '__main__':
    if sys.argv[1] == 'dump':
        classes_dump(int(sys.argv[2])); sys.exit(0)
    if sys.argv[1] == 'cmp':
        compare_dumps(int(sys.argv[2]), int(sys.argv[3])); sys.exit(0)
    ks = [int(a) for a in sys.argv[1:]] or [6, 8, 7, 9, 10, 12, 11, 13, 12, 14, 13, 15]
    out = []
    for i in range(0, len(ks) - 1, 2):
        out.append(compare(ks[i], ks[i + 1]))
    json.dump(out, open('results/zj_transfer_results.json', 'w'), indent=1)
    print('written zj_transfer_results.json', flush=True)

