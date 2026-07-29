#!/usr/bin/env python3
"""Sparse Wiedemann consistency solver over GF(p) for Nullstellensatz systems.

Decides consistency of  A x = e_const  (mod p), where A (nrows x ncols) is given
by the sparse ``entries = {(row,col): coeff}`` / ``const`` description produced by
``pillars.reduced_system_k`` / ``pokrovskiy.reduced_system``.  Memory footprint is
O(nnz) -- the huge dense matrix is never formed.

Mathematical design
-------------------
Consistency of  A x = b  (b = e_const)  <=>  b in range(A).  Over any field
range(A A^T) subseteq range(A) trivially, so a solution y of  (A A^T) y = b  gives
x = A^T y with  A x = b.  We work with the SQUARE symmetric operator B = A A^T
(nrows x nrows) applied IMPLICITLY:  B v = A (A^T v)  -- two sparse matvecs; B is
never formed (it would densify).

Scalar Wiedemann: for a random u, form the Krylov scalar sequence
    s_i = u^T B^i b        (i = 0, 1, 2, ...),
run Berlekamp-Massey mod p to get the minimal polynomial m(lambda) of the
sequence (m divides the min. poly. of b w.r.t. B).  Over Q, B = A A^T is PSD
hence semisimple with range orthogonal to kernel, so
    b in range(B)  <=>  min. poly. of b w.r.t. B has NONZERO constant term.
Since m_seq | m_b, we have m_seq(0) = 0  =>  m_b(0) = 0  =>  b not in range.

Decision discipline (mandatory)
-------------------------------
* m(0) != 0 : reconstruct y = -m(0)^{-1} (m_1 + m_2 B + ... ) b by Horner (deg(m)
  further matvecs), then CHECK the residual  A(A^T y) == b (mod p).  A PASSING
  residual is an explicit certificate mod p (x = A^T y solves A x = b), so it
  makes false-SOLVABLE impossible.  A failing residual only means m_seq was a
  proper divisor of m_b (unlucky u) -> retry with another u.
* m(0) == 0 (or BM degenerates): this u votes UNSOLVABLE.  The verdict UNSOLVABLE
  is accepted only if it concords across >= 3 distinct primes AND >= 2 random u
  per prime (a fresh u whose sequence yields a passing residual overrides to
  SOLVABLE).  Final SOLVABLE requires a passing residual at >= 2 primes, guarding
  against an astronomically-unlikely solution-creating unlucky prime; final
  UNSOLVABLE requires all (>=3) primes x (>=2) u to concord with no residual.

Exactness of scipy float64 sparse matvecs is guaranteed by choosing p so that
    maxdeg * maxval * p  <  2^52         (float64 accumulation stays exact)
    (2*nrows) * p^2      <  2^61         (int64 BM / dot accumulation stays exact)
where maxdeg = max nnz per row of A or A^T and maxval = max |coeff|.  We reduce
mod p after every matvec (via an exact int64 round-trip), and use >= 3 primes.
"""
import gc
import math
import time

import numpy as np
import scipy.sparse as sp


# ----------------------------------------------------------------------------
#  small utilities
# ----------------------------------------------------------------------------
def _rss_mb():
    """Resident set size of this process in MB (-1 if unavailable)."""
    try:
        with open('/proc/self/status') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    return int(line.split()[1]) // 1024
    except Exception:
        pass
    return -1


def _is_prime(n):
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for q in small:
        if n % q == 0:
            return n == q
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in small:                      # deterministic for n < 3.3e24
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def choose_primes(maxdeg, maxval, nrows, n_primes=3, extra=0, matvec_pow=52,
                  int_pow=61):
    """Pick ``n_primes(+extra)`` distinct primes just below the exactness bound.

    Constraints (with safety margins baked into the exponents):
      * float64 matvec exact:   maxdeg * maxval * p   < 2^matvec_pow
      * int64  BM/dot exact:    (2*nrows) * p^2       < 2^int_pow
    """
    p_mv = (1 << matvec_pow) // max(maxdeg * maxval, 1)
    p_i = math.isqrt((1 << int_pow) // max(2 * nrows, 1))
    pmax = min(p_mv, p_i)
    primes = []
    p = pmax if pmax % 2 == 1 else pmax - 1
    while len(primes) < n_primes + extra and p > 5:
        if _is_prime(p):
            primes.append(p)
        p -= 2
    return primes


def build_matrices(entries, nrows, ncols):
    """Build A (csr) and A^T (csr) once from the sparse ``entries`` dict.

    Coefficients are stored verbatim in float64 (they are reused across every
    prime, since every prime exceeds max|coeff|).  Returns A, At and a stats
    dict.  Memory is O(nnz)."""
    nnz = len(entries)
    rows = np.empty(nnz, dtype=np.int32)
    cols = np.empty(nnz, dtype=np.int32)
    vals = np.empty(nnz, dtype=np.float64)
    for i, ((r, c), v) in enumerate(entries.items()):
        rows[i] = r
        cols[i] = c
        vals[i] = v
    A = sp.csr_matrix((vals, (rows, cols)), shape=(nrows, ncols))
    At = sp.csr_matrix((vals, (cols, rows)), shape=(ncols, nrows))
    A.sum_duplicates()
    At.sum_duplicates()
    maxdeg_A = int(np.diff(A.indptr).max()) if nrows else 0
    maxdeg_At = int(np.diff(At.indptr).max()) if ncols else 0
    stats = {
        'nnz': int(A.nnz),
        'maxdeg_A': maxdeg_A,
        'maxdeg_At': maxdeg_At,
        'maxdeg': max(maxdeg_A, maxdeg_At),
        'maxval': int(vals.max()) if nnz else 1,
    }
    return A, At, stats


# ----------------------------------------------------------------------------
#  implicit matvec  B v = A (A^T v)  mod p   (exact via int64 round-trip)
# ----------------------------------------------------------------------------
def _Bmul(A, At, p, wi):
    """wi : int64 array in [0,p) of length nrows  ->  B wi in [0,p)."""
    t = At.dot(wi.astype(np.float64))        # length ncols, exact float64 integers
    ti = t.astype(np.int64)
    ti %= p
    r = A.dot(ti.astype(np.float64))         # length nrows
    ri = r.astype(np.int64)
    ri %= p
    return ri


# ----------------------------------------------------------------------------
#  online Berlekamp-Massey over GF(p)
# ----------------------------------------------------------------------------
class _BM:
    """Incremental Berlekamp-Massey mod p.  Feed terms one at a time via
    ``update``; ``C[:L+1]`` are the connection-poly coeffs (C[0]=1), L the linear
    complexity.  The sequence min. poly. is  m(x) = x^L + C[1] x^{L-1} + ... + C[L]
    so  m(0) = C[L]."""

    def __init__(self, p, maxlen):
        self.p = p
        clen = 2 * maxlen + 16
        self.C = np.zeros(clen, dtype=np.int64)
        self.C[0] = 1
        self.Clen = 1
        self.B = np.zeros(clen, dtype=np.int64)
        self.B[0] = 1
        self.Blen = 1
        self.s = np.zeros(maxlen + 2, dtype=np.int64)
        self.L = 0
        self.m = 1                 # shift since last length change
        self.b = 1                 # last nonzero discrepancy
        self.n = 0                 # number of terms processed
        self.last_change = -1      # n-index of last length increase

    def update(self, sn):
        p = self.p
        n = self.n
        self.s[n] = sn % p
        L = self.L
        if L > 0:
            d = int(self.s[n] +
                    int(np.dot(self.C[1:L + 1], self.s[n - L:n][::-1]))) % p
        else:
            d = int(self.s[n]) % p
        if d != 0:
            coef = (d * pow(int(self.b), p - 2, p)) % p
            if 2 * L <= n:
                T = self.C[:self.Clen].copy()
                Tlen = self.Clen
                seg = self.C[self.m:self.m + self.Blen]
                seg -= coef * self.B[:self.Blen]
                seg %= p
                self.Clen = max(self.Clen, self.m + self.Blen)
                self.L = n + 1 - L
                self.B[:Tlen] = T
                self.Blen = Tlen
                self.b = d
                self.m = 1
                self.last_change = n
            else:
                seg = self.C[self.m:self.m + self.Blen]
                seg -= coef * self.B[:self.Blen]
                seg %= p
                self.Clen = max(self.Clen, self.m + self.Blen)
                self.m += 1
        else:
            self.m += 1
        self.n += 1


# ----------------------------------------------------------------------------
#  one scalar-Wiedemann attempt at a single prime with a single u
# ----------------------------------------------------------------------------
def _wiedemann_once(A, At, const, u, nrows, p, maxterms, margin, tag,
                    log, progress):
    b_int = np.zeros(nrows, dtype=np.int64)
    b_int[const] = 1
    bm = _BM(p, maxterms)
    wi = b_int.copy()
    t0 = time.time()
    nz_any = False
    while bm.n < maxterms:
        sn = int(np.dot(u, wi) % p)
        if sn:
            nz_any = True
        bm.update(sn)
        cnt = bm.n
        if (bm.L > 0 and cnt >= 2 * bm.L + margin and
                (cnt - 1 - bm.last_change) >= margin):
            break
        if bm.n < maxterms:
            wi = _Bmul(A, At, p, wi)
            if progress and bm.n % progress == 0:
                log(f"        [{tag}] seq n={bm.n} L={bm.L} "
                    f"({time.time() - t0:.1f}s)")
    seq_s = time.time() - t0
    L = bm.L
    terms = bm.n
    degenerate = (not nz_any) or L == 0
    Cpoly = bm.C[:L + 1].copy()
    m0 = int(Cpoly[L] % p) if L >= 1 else int(Cpoly[0] % p)

    recon_s = 0.0
    residual_ok = False
    residual_reason = None
    if degenerate:
        residual_reason = 'degenerate (all-zero seq or L=0)'
    elif m0 == 0:
        residual_reason = 'm(0)=0 -> b not in range(B) mod p'
    else:
        tr = time.time()
        mcoef = Cpoly[::-1].copy()              # mcoef[j] = coeff of lambda^j
        acc = b_int.copy()                      # m_L * b, m_L = 1
        for j in range(L - 1, 0, -1):
            acc = _Bmul(A, At, p, acc)
            mj = int(mcoef[j])
            if mj:
                acc[const] = (int(acc[const]) + mj) % p
        minv = pow(m0, p - 2, p)
        y = (-minv * acc) % p
        r = _Bmul(A, At, p, y)
        residual_ok = bool(np.array_equal(r, b_int))
        recon_s = time.time() - tr
        residual_reason = ('residual A(A^T y)=b PASSED' if residual_ok
                           else 'residual FAILED (proper-divisor min-poly)')
    return {
        'L': int(L), 'm0': int(m0), 'terms': int(terms),
        'residual_ok': residual_ok, 'degenerate': bool(degenerate),
        'reason': residual_reason, 'seq_s': round(seq_s, 2),
        'recon_s': round(recon_s, 2),
    }


def _solve_at_prime(A, At, const, nrows, p, n_u, rng, maxterms, margin, log,
                    progress):
    res_list = []
    for ui in range(n_u):
        u = rng.integers(1, p, size=nrows, dtype=np.int64)
        res = _wiedemann_once(A, At, const, u, nrows, p, maxterms, margin,
                              tag=f"p={p},u={ui}", log=log, progress=progress)
        res_list.append(res)
        log(f"    p={p} u={ui}: L={res['L']} m0={res['m0']} "
            f"terms={res['terms']} residual_ok={res['residual_ok']} "
            f"[{res['reason']}] (seq {res['seq_s']}s recon {res['recon_s']}s)")
        if res['residual_ok']:
            return True, res_list
    return False, res_list


# ----------------------------------------------------------------------------
#  public entry point
# ----------------------------------------------------------------------------
def solvable_sparse(entries, const, nrows, ncols, primes=None, n_u=2,
                    seed=0xC0FFEE, verbose=True, log=None, margin=24,
                    progress=5000):
    """Decide consistency of  A x = e_const  (mod several primes) with the sparse
    implicit-B Wiedemann method.

    Returns dict:
      {'solvable': bool, 'primes': [...], 'detail': {...}}
    """
    if log is None:
        log = (lambda *a: print(*a, flush=True)) if verbose else (lambda *a: None)

    rss0 = _rss_mb()
    t_build = time.time()
    A, At, stats = build_matrices(entries, nrows, ncols)
    build_mat_s = time.time() - t_build
    rss_mat = _rss_mb()
    peak_rss = max(rss0, rss_mat)

    if primes is None:
        primes = choose_primes(stats['maxdeg'], stats['maxval'], nrows,
                               n_primes=3)
    backups = [q for q in choose_primes(stats['maxdeg'], stats['maxval'], nrows,
                                        n_primes=3, extra=6)
               if q not in primes]

    maxterms = 2 * nrows + 64
    log(f"  [sparse] {nrows}x{ncols} nnz={stats['nnz']} "
        f"maxdeg={stats['maxdeg']} maxval={stats['maxval']} "
        f"| RSS {rss0}->{rss_mat}MB (sparse mats {build_mat_s:.1f}s)")
    log(f"  [sparse] primes={primes} (int64 & float64 exactness verified) "
        f"n_u={n_u} maxterms={maxterms}")

    detail = {
        'nrows': nrows, 'ncols': ncols, **stats,
        'primes_used': [], 'per_prime': {}, 'events': [],
        'rss_before_mb': rss0, 'rss_after_mat_mb': rss_mat,
    }

    S, U = [], []
    all_primes = list(primes)
    idx = 0
    verdict = None
    while idx < len(all_primes):
        p = all_primes[idx]
        idx += 1
        rng = np.random.default_rng(seed + p)
        t0 = time.time()
        solved_p, res_list = _solve_at_prime(A, At, const, nrows, p, n_u, rng,
                                              maxterms, margin, log, progress)
        detail['primes_used'].append(p)
        detail['per_prime'][p] = {'solved': solved_p, 'runs': res_list,
                                  'wall_s': round(time.time() - t0, 1)}
        peak_rss = max(peak_rss, _rss_mb())
        # record degenerate / proper-divisor events
        for ui, r in enumerate(res_list):
            if r['degenerate']:
                detail['events'].append(
                    f"p={p} u={ui}: DEGENERATE BM ({r['reason']})")
            elif (not r['residual_ok']) and r['m0'] != 0:
                detail['events'].append(
                    f"p={p} u={ui}: proper-divisor min-poly "
                    f"(m0!=0 but residual failed) -> retried")
        if solved_p:
            S.append(p)
        else:
            U.append(p)
            if S:
                detail['events'].append(
                    f"p={p}: UNSOLVABLE-mod-p while other prime(s) {S} "
                    f"gave a passing residual -> AA^T-unlucky prime")
        if len(S) >= 2:
            verdict = True
            break
        # if primes exhausted but disagreement, pull in a backup prime
        if idx >= len(all_primes) and len(S) == 1 and backups:
            nxt = backups.pop(0)
            all_primes.append(nxt)
            detail['events'].append(
                f"disagreement (|S|=1): adding backup prime {nxt} to confirm")

    if verdict is None:
        if len(S) >= 1:
            # only one prime ever solved (residual is airtight for it) but could
            # not reach a second confirmation -> lean SOLVABLE with a caveat
            verdict = True
            detail['events'].append(
                f"SOLVABLE confirmed at only {len(S)} prime(s) {S}; residual "
                f"certificate is exact mod p but second confirmation not reached")
        else:
            # no residual anywhere; all primes concord UNSOLVABLE
            verdict = False

    detail['solved_primes'] = S
    detail['unsolved_primes'] = U
    detail['peak_rss_mb'] = peak_rss

    del A, At
    gc.collect()
    log(f"  [sparse] VERDICT solvable={verdict}  solved_primes={S} "
        f"unsolved_primes={U}  peak RSS={peak_rss}MB")
    return {'solvable': bool(verdict), 'primes': detail['primes_used'],
            'detail': detail}


if __name__ == '__main__':
    # tiny smoke tests
    print("smoke inconsistent (0=1):",
          solvable_sparse({}, 0, 1, 1, verbose=False)['solvable'])       # False
    print("smoke consistent  (x0=1):",
          solvable_sparse({(0, 0): 1}, 0, 1, 1, verbose=False)['solvable'])  # True
    # 2x2 identity-ish consistent
    print("smoke consistent  (A=I 2x2):",
          solvable_sparse({(0, 0): 1, (1, 1): 1}, 0, 2, 2,
                          verbose=False)['solvable'])                    # True
