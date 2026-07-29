#!/usr/bin/env python3
"""Piste (e) — laboratoire topologique : le test de Lovász sur le corpus.

Pour chaque graphe G, on construit le COMPLEXE DE VOISINAGE N(G) (sommets =
sommets de G ; simplexes = ensembles S ayant un voisin commun : S <= N(w)) et
l'on calcule son homologie réduite entière H~_0, H_1, H_2 (rangs de Betti +
torsion) par forme normale de Smith exacte.

Cadre théorique (Lovász 1978, cité de mémoire — à collationner avant usage
théorème) : si N(G) est topologiquement k-connexe alors chi(G) >= k+3. Pour
chi >= 4 il faut la 1-connexité. CAVEATS encodés dans le verdict :
  - H~0 = H1 = 0 (sur Z) est NÉCESSAIRE pour la 1-connexité mais pas
    suffisant (pi_1 pourrait être parfait) — verdict 'ACTIVE?' = cohérent
    avec 1-connexité, pas une preuve ;
  - H1 != 0 ou déconnecté => PAS 1-connexe => la borne de Lovász ne peut pas
    certifier chi >= 4 par la connexité : verdict 'INACTIVE' (négatif sûr).
La comptabilité exacte des variantes (complexe boîte, indice Z2, ±1) sera
collationnée sur sources primaires avant toute conclusion théorique.

Question expérimentale du jour : la topologie sépare-t-elle les 36
obstructions sans-triangle (qui trompent le SDP) des graphes 3-coloriables ?
"""
import itertools, json, sys, time


# ---------------------------------------------------------------- graph6 ----
def parse_g6(s):
    data = [ord(c) - 63 for c in s.strip()]
    n = data[0]
    bits = []
    for byte in data[1:]:
        bits.extend((byte >> (5 - i)) & 1 for i in range(6))
    adj = [0] * n
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            idx += 1
    return n, adj


def mycielski(n, adj):
    """Mycielskian: vertices 0..n-1 (copy u_i), n..2n-1 (shadows w_i), 2n (hub)."""
    N = 2 * n + 1
    out = [0] * N
    for i in range(n):
        for j in range(i + 1, n):
            if (adj[i] >> j) & 1:
                for a, b in [(i, j), (i, n + j), (n + i, j)]:
                    out[a] |= 1 << b
                    out[b] |= 1 << a
    for i in range(n):
        out[n + i] |= 1 << (2 * n)
        out[2 * n] |= 1 << (n + i)
    return N, out


def cycle(n):
    adj = [0] * n
    for i in range(n):
        j = (i + 1) % n
        adj[i] |= 1 << j
        adj[j] |= 1 << i
    return n, adj


def complete(n):
    return n, [((1 << n) - 1) ^ (1 << i) for i in range(n)]


def petersen():
    n = 10
    adj = [0] * n
    edges = [(i, (i + 1) % 5) for i in range(5)] + \
            [(i, i + 5) for i in range(5)] + \
            [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return n, adj


# ------------------------------------------------- neighborhood complex ----
def neighborhood_faces(n, adj, maxdim=3):
    """All faces of N(G) up to dimension maxdim (subsets of size maxdim+1),
    as sorted tuples. A set S is a face iff S subset of N(w) for some w."""
    nbhds = [adj[w] for w in range(n) if adj[w]]
    faces = [set() for _ in range(maxdim + 1)]
    for mask in nbhds:
        verts = [v for v in range(n) if (mask >> v) & 1]
        for k in range(1, min(maxdim + 2, len(verts) + 1)):
            for comb in itertools.combinations(verts, k):
                faces[k - 1].add(comb)
    return [sorted(f) for f in faces]


def boundary_matrix(k_faces, km1_faces):
    """Integer boundary matrix d_k: C_k -> C_{k-1} as dict-of-cols."""
    ix = {f: i for i, f in enumerate(km1_faces)}
    cols = []
    for f in k_faces:
        col = {}
        for j in range(len(f)):
            sub = f[:j] + f[j + 1:]
            col[ix[sub]] = (-1) ** j
        cols.append(col)
    return cols, len(km1_faces)


def smith_rank_torsion(cols, nrows):
    """Exact Smith normal form (fraction-free Gauss over Z with pivoting on
    smallest |entry|). Returns (rank, torsion list = diagonal entries > 1).
    Sizes here are small (<= few thousand); growth controlled by gcd steps."""
    from math import gcd
    M = {}
    for c, col in enumerate(cols):
        for r, v in col.items():
            M[(r, c)] = v
    rows_live = set(r for r, _ in M)
    cols_live = set(c for _, c in M)
    rank, tors = 0, []
    while M:
        (r0, c0), v0 = min(M.items(), key=lambda kv: abs(kv[1]))
        # clear column c0 and row r0
        rowr0 = {c: v for (r, c), v in M.items() if r == r0}
        colc0 = {r: v for (r, c), v in M.items() if c == c0}
        clean = True
        for r, v in list(colc0.items()):
            if r == r0:
                continue
            q = v // v0
            if q:
                for c, w in rowr0.items():
                    key = (r, c)
                    nv = M.get(key, 0) - q * w
                    if nv:
                        M[key] = nv
                    else:
                        M.pop(key, None)
            if M.get((r, c0), 0):
                clean = False
        rowr0 = {c: v for (r, c), v in M.items() if r == r0}
        for c, v in list(rowr0.items()):
            if c == c0:
                continue
            q = v // v0
            if q:
                colc0b = {r: w for (r, cc), w in M.items() if cc == c0}
                for r, w in colc0b.items():
                    key = (r, c)
                    nv = M.get(key, 0) - q * w
                    if nv:
                        M[key] = nv
                    else:
                        M.pop(key, None)
            if M.get((r0, c), 0):
                clean = False
        if not clean:
            continue
        piv = M.pop((r0, c0))
        # row r0 and col c0 now clean elsewhere?
        rest_r = [c for (r, c) in M if r == r0]
        rest_c = [r for (r, c) in M if c == c0]
        if rest_r or rest_c:
            M[(r0, c0)] = piv
            continue
        rank += 1
        if abs(piv) > 1:
            tors.append(abs(piv))
    return rank, sorted(tors)


def homology(n, adj):
    t0 = time.time()
    faces = neighborhood_faces(n, adj, maxdim=3)
    dims = [len(f) for f in faces]
    d1, _ = boundary_matrix(faces[1], faces[0])
    d2, _ = boundary_matrix(faces[2], faces[1])
    d3, _ = boundary_matrix(faces[3], faces[2])
    r1, t1 = smith_rank_torsion(d1, dims[0])
    r2, t2 = smith_rank_torsion(d2, dims[1])
    r3, t3 = smith_rank_torsion(d3, dims[2])
    b0t = dims[0] - r1          # b0 (unreduced)
    b1 = dims[1] - r1 - r2
    b2 = dims[2] - r2 - r3
    return {'faces': dims, 'b0_reduced': b0t - 1, 'b1': b1, 'b2': b2,
            'torsion_H1': t2, 'torsion_H2': t3,
            'time_s': round(time.time() - t0, 2)}


def verdict(h):
    if h['b0_reduced'] == 0 and h['b1'] == 0 and not h['torsion_H1']:
        return 'ACTIVE? (H~0=H1=0 : coherent avec 1-connexite -> chi>=4 plausible par Lovasz)'
    return 'INACTIVE (pas 1-connexe : la borne ne certifie pas chi>=4)'


def run_corpus():
    out = []

    def add(name, n, adj, chi_note):
        h = homology(n, adj)
        v = verdict(h)
        rec = {'name': name, 'n': n, 'chi': chi_note, **h, 'verdict': v}
        out.append(rec)
        print(f"{name:28s} n={n:3d} chi={chi_note:9s} faces={h['faces']} "
              f"b~0={h['b0_reduced']} b1={h['b1']} b2={h['b2']} "
              f"tors={h['torsion_H1']}/{h['torsion_H2']} -> {v}", flush=True)

    # --- controls ---
    add('K4 (controle+)', *complete(4), '4')
    add('C5 (controle-)', *cycle(5), '3')
    add('C7 (controle-)', *cycle(7), '3')
    add('Petersen (controle-)', *petersen(), '3')
    n5, a5 = cycle(5)
    add('Grotzsch (controle+)', *mycielski(n5, a5), '4')

    # --- the 36 triangle-free obstructions that fool the SDP ---
    sdp = json.load(open('results/lab_sdp.json'))
    tf = [r for r in sdp if r.get('C3free')]
    print(f"\n36 attendues, trouvees: {len(tf)}", flush=True)
    for r in tf:
        n, adj = parse_g6(r['g6'])
        add(f"tf[{r['src']}] {r['g6']}", n, adj, '4 (crit)')

    json.dump(out, open('results/topo_results.json', 'w'), indent=1)
    act = sum(1 for r in out[5:] if r['verdict'].startswith('ACTIVE'))
    print(f"\nBILAN obstructions sans-triangle : {act}/{len(out)-5} ACTIVE?, "
          f"{len(out)-5-act} INACTIVE", flush=True)
    print("controles attendus : K4 ACTIVE?, Grotzsch ACTIVE? (Stiebitz), "
          "C5/C7/Petersen INACTIVE", flush=True)


if __name__ == '__main__':
    run_corpus()
