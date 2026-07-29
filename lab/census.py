#!/usr/bin/env python3
"""Census of 4-vertex-critical graphs among geng output (graph6 on stdin).
Classify each critical graph by induced-subgraph freeness: P6, P7, P8, 2P4, C3, C4, C5.
A graph is 4-vertex-critical iff chi=4 and chi(G-v)<=3 for all v.
Fast path: contains K4 and n>4 -> cannot be vertex-critical (K4 survives some deletion).
"""
import sys

def parse_graph6(line):
    data = [ord(c) - 63 for c in line.strip()]
    n = data[0]
    bits = []
    for b in data[1:]:
        for k in range(5, -1, -1):
            bits.append((b >> k) & 1)
    adj = [0] * n
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if bits[idx]:
                adj[i] |= (1 << j)
                adj[j] |= (1 << i)
            idx += 1
    return n, adj

def has_K4(n, adj):
    for i in range(n):
        Ai = adj[i]
        for j in range(i + 1, n):
            if not (Ai >> j) & 1:
                continue
            common = Ai & adj[j]
            # need edge inside common
            m = common
            while m:
                k = (m & -m).bit_length() - 1
                m &= m - 1
                if common & adj[k] & ~((1 << (k + 1)) - 1):
                    return True
    return False

def three_colorable(n, adj, removed=0):
    """Backtracking 3-coloring on vertices not in 'removed' bitmask."""
    verts = [v for v in range(n) if not (removed >> v) & 1]
    if not verts:
        return True
    # order by degree (within remaining) descending
    verts.sort(key=lambda v: -bin(adj[v] & ~removed).count('1'))
    color = {}
    order = verts
    N = len(order)

    def bt(i, maxc):
        if i == N:
            return True
        v = order[i]
        used = 0
        av = adj[v]
        for u, cu in color.items():
            if (av >> u) & 1:
                used |= (1 << cu)
        limit = min(2, maxc + 1)
        for c in range(limit + 1):
            if (used >> c) & 1:
                continue
            color[v] = c
            if bt(i + 1, max(maxc, c)):
                return True
            del color[v]
        return False

    return bt(0, -1)

def is_4_vertex_critical(n, adj):
    if n > 4 and has_K4(n, adj):
        return False
    if three_colorable(n, adj):
        return False
    for v in range(n):
        if not three_colorable(n, adj, removed=(1 << v)):
            return False
    return True

def longest_induced_path(n, adj, cap=10):
    """Length in vertices of longest induced path, capped."""
    best = 1
    def extend(path_set, last, length, forbidden):
        nonlocal best
        if length > best:
            best = length
            if best >= cap:
                return True
        cand = adj[last] & ~forbidden
        m = cand
        while m:
            v = (m & -m).bit_length() - 1
            m &= m - 1
            # v adjacent to last, must be non-adjacent to all earlier path vertices
            if adj[v] & (path_set & ~(1 << last)):
                continue
            if extend(path_set | (1 << v), v, length + 1,
                      forbidden | (1 << v) | (adj[last] & ~(1 << v))):
                return True
        return False
    for s in range(n):
        if extend(1 << s, s, 1, (1 << s)):
            break
    return best

def induced_P4s(n, adj):
    """All induced P4s as bitmasks."""
    res = []
    for b in range(n):
        for c in range(b + 1, n):
            if not (adj[b] >> c) & 1:
                continue
            # b-c edge; a adj b not c; d adj c not b; a nonadj d
            As = adj[b] & ~adj[c] & ~(1 << c)
            Ds = adj[c] & ~adj[b] & ~(1 << b)
            ma = As
            while ma:
                a = (ma & -ma).bit_length() - 1
                ma &= ma - 1
                md = Ds & ~adj[a] & ~(1 << a)
                while md:
                    d = (md & -md).bit_length() - 1
                    md &= md - 1
                    res.append((1 << a) | (1 << b) | (1 << c) | (1 << d))
    return res

def has_induced_2P4(n, adj):
    p4s = induced_P4s(n, adj)
    for i in range(len(p4s)):
        Si = p4s[i]
        nbr = 0
        m = Si
        while m:
            v = (m & -m).bit_length() - 1
            m &= m - 1
            nbr |= adj[v]
        block = Si | nbr
        for j in range(i + 1, len(p4s)):
            if not (p4s[j] & block):
                return True
    return False

def has_C3(n, adj):
    for i in range(n):
        for j in range(i + 1, n):
            if (adj[i] >> j) & 1 and (adj[i] & adj[j] & ~((1 << (j + 1)) - 1)):
                return True
    # also check common neighbors with smaller index
    for i in range(n):
        for j in range(i + 1, n):
            if (adj[i] >> j) & 1 and (adj[i] & adj[j]):
                return True
    return False

def has_induced_C4(n, adj):
    for i in range(n):
        for j in range(i + 1, n):
            if (adj[i] >> j) & 1:
                continue
            common = adj[i] & adj[j]
            m = common
            pairs = []
            while m:
                v = (m & -m).bit_length() - 1
                m &= m - 1
                pairs.append(v)
            for x in range(len(pairs)):
                for y in range(x + 1, len(pairs)):
                    if not (adj[pairs[x]] >> pairs[y]) & 1:
                        return True
    return False

def has_induced_C5(n, adj):
    import itertools
    for comb in itertools.combinations(range(n), 5):
        deg = []
        S = 0
        for v in comb:
            S |= (1 << v)
        ok = True
        edges = 0
        for v in comb:
            d = bin(adj[v] & S).count('1')
            if d != 2:
                ok = False
                break
            edges += d
        if ok and edges == 10:
            # 5 vertices all degree 2 in induced subgraph, connected -> C5
            # (could be C3+C2? no, C2 impossible; disjoint C3+2 isolated? deg would differ)
            # check connectivity of induced subgraph
            start = comb[0]
            seen = 1 << start
            stack = [start]
            while stack:
                u = stack.pop()
                mm = adj[u] & S & ~seen
                while mm:
                    w = (mm & -mm).bit_length() - 1
                    mm &= mm - 1
                    seen |= (1 << w)
                    stack.append(w)
            if seen == S:
                return True
    return False

def to_graph6(n, adj):
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append((adj[i] >> j) & 1)
    while len(bits) % 6:
        bits.append(0)
    s = chr(n + 63)
    for k in range(0, len(bits), 6):
        val = 0
        for b in bits[k:k+6]:
            val = (val << 1) | b
        s += chr(val + 63)
    return s

def classify(n, adj):
    lip = longest_induced_path(n, adj, cap=9)
    return {
        'n': n,
        'g6': to_graph6(n, adj),
        'longest_induced_path': lip,
        'P6free': lip <= 5,
        'P7free': lip <= 6,
        'P8free': lip <= 7,
        'twoP4free': not has_induced_2P4(n, adj),
        'C3free': not has_C3(n, adj),
        'C4free': not has_induced_C4(n, adj),
        'C5free': not has_induced_C5(n, adj),
    }

def main():
    import json
    total = 0
    crit = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        total += 1
        n, adj = parse_graph6(line)
        if is_4_vertex_critical(n, adj):
            crit.append(classify(n, adj))
    out = {'graphs_scanned': total, 'critical_found': len(crit), 'critical': crit}
    print(json.dumps(out))

if __name__ == '__main__':
    main()
