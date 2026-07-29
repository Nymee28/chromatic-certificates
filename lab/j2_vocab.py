#!/usr/bin/env python3
"""J2, la mesure decisive — reformulee en test de solvabilite restreinte.

Question de presentabilite mod 4 : existe-t-il un vocabulaire de formes
INDEPENDANT DE n qui porte des certificats a tous les q ? Plutot que
d'extraire la solution exacte de q=4 (hors de portee dense), on teste :

  (a) q=4 restreint au VOCABULAIRE DE q=3 (les 1 299 formes du certificat
      exact, transferees telles quelles — offsets |o| <= 6 < n/2) ;
  (b) balayage en DIAMETRE : q=4 restreint aux colonnes de diametre <= D,
      D = 3, 4, 5, 6, 7, 8 (a n=17 le diametre max est 8 ; a n=13 il etait
      censure a 6). Le D minimal suffisant, compare entre q=3 et q=4,
      dit si le vocabulaire grandit avec n.

Verdicts par Wiedemann creux certifie residu, deux premiers concordants.
"""
import json, sys, time
from pillars import G_CH
from j2_ch4 import build_with_cols, mono_shape, gap_of
from sparse_wiedemann import solvable_sparse


def restrict(n, adj, max_gap, keep):
    """Systeme gap<=max_gap dont on ne garde que les colonnes keep(w)."""
    entries, const, nrows, cols, col_ix = build_with_cols(
        n, adj, {1, 5}, 4, max_gap=max_gap)
    kept = [i for i, w in enumerate(cols) if keep(w)]
    remap = {c: j for j, c in enumerate(kept)}
    ent2 = {}
    for (r, c), v in entries.items():
        j = remap.get(c)
        if j is not None:
            ent2[(r, j)] = v
    return ent2, const, nrows, len(kept)


def diam_of(w, n):
    sh = mono_shape(w, n)
    if not sh:
        return 0
    return max(abs(o) for o, _ in sh)


if __name__ == '__main__':
    q = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    n, adj = G_CH(q, 4)
    vocab = None
    try:
        r3 = json.load(open('results/j2_ch4_exact_q3.json'))
        vocab = {eval(s) for s, _ in r3['formes_top']}  # top 25 seulement
    except Exception:
        pass
    # le vocabulaire COMPLET de q=3 : re-derive du support exact sauvegarde ?
    # formes_top ne garde que 25 ; on recharge les formes via les checkpoints
    import pickle
    from certificates import P1
    sols = pickle.load(open('results/j2_ckpt_q3_p1000003.pkl', 'rb'))
    n3, adj3 = G_CH(3, 4)
    e3, c3, nr3, cols3, ci3 = build_with_cols(n3, adj3, {1, 5}, 4,
                                              max_gap=3, order=True)
    vocab = {mono_shape(cols3[c], n3) for c in sols}
    print(f"vocabulaire q=3 recharge : {len(vocab)} formes "
          f"(support {len(sols)})", flush=True)
    out = []

    def test(nom, keep):
        t0 = time.time()
        ent, const, nrows, ncols = restrict(n, adj, 3, keep)
        tb = time.time() - t0
        t0 = time.time()
        res = solvable_sparse(ent, const, nrows, ncols, verbose=False)
        rec = {'q': q, 'n': n, 'test': nom, 'rows': nrows, 'cols': ncols,
               'nnz': len(ent), 'solvable': res['solvable'],
               'primes': res['primes'], 'build_s': round(tb),
               'solve_s': round(time.time() - t0)}
        out.append(rec)
        print(f"  {nom}: {nrows}x{ncols} solvable={res['solvable']} "
              f"(build {rec['build_s']}s, solve {rec['solve_s']}s)",
              flush=True)
        json.dump(out, open(f'results/j2_vocab_q{q}.json', 'w'), indent=1)
        return res['solvable']

    print(f"G_CH({q},4): n={n} — tests de vocabulaire (ecart <= 3 partout)",
          flush=True)
    # (a) le test central : le vocabulaire de q=3 porte-t-il q=4 ?
    ok_vocab = test('vocab_q3', lambda w: mono_shape(w, n) in vocab)
    # (b) balayage en diametre, du plus petit au plus grand
    for D in (3, 4, 5, 6, 7, 8):
        ok = test(f'diam<={D}', lambda w, D=D: diam_of(w, n) <= D)
        if ok:
            break
    print("FIN", flush=True)
