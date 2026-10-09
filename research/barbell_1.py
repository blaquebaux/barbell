#!/usr/bin/python3
# =============================================================================
# barbell_1.py — Taleb's barbell: safe core + convex sliver vs the "mediocre middle".
#
# The barbell (not the caricature): hold the vast majority in SAFE assets (bounded downside) + a tiny
# sliver in CONVEX bets (unbounded upside), and avoid the mediocre middle (60/40). Antifragility = you
# can't lose much, and you win big in the tails. Test whether it beats the 60/40 middle on a tail basis.
#   Q1  Defensive barbell (cash + long-vol) vs offensive barbell (cash + 3x equity) vs the 60/40 middle.
#   Q2  Is the downside genuinely bounded, and the skew genuinely positive? (the antifragile signature)
#   Q3  Barbell (cash+convex) vs the same convexity as an OVERLAY on an equity core (contextual_rescue).
#   Q4  Crisis months — does the convex wing pay when the middle bleeds?
# Alpaca SIP daily, total-return; daily-rebalanced; cash = BIL.
# =============================================================================
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from _barbell_common import panel, rets

def metrics(r, months):
    r=np.asarray(r,float); c=np.cumprod(1+r); dd=(c/np.maximum.accumulate(c)-1).min()
    sh=r.mean()/r.std()*math.sqrt(252) if r.std()>0 else float("nan"); z=(r-r.mean())/r.std()
    cagr=c[-1]**(252/len(r))-1
    mo={}
    for m,x in zip(months,r): mo[m]=mo.get(m,1.0)*(1+x)
    return dict(sh=sh,cagr=cagr,dd=float(dd),skew=float(np.mean(z**3)),worst=min(v-1 for v in mo.values()),
                calmar=cagr/abs(dd) if dd<0 else float("nan"))

def main():
    syms=["BIL","VIXM","UPRO","SPY","IEF"]
    P,dates=panel(syms); R={s:rets(P[s]) for s in P}
    L=min(len(R[s]) for s in R); months=[d[:7] for d in dates[1:]][-L:]; r={s:R[s][-L:] for s in R}
    print("="*96); print("BARBELL — Taleb's safe core + convex sliver vs the mediocre middle"); print("="*96)
    print(f"  window {dates[-L]}..{dates[-1]}  ({L/252:.1f}y)   convex wings: VIXM (long-vol), UPRO (3x equity)")

    books = {
        "defensive 90 BIL/10 VIXM":   0.90*r["BIL"]+0.10*r["VIXM"],
        "offensive 90 BIL/10 UPRO":   0.90*r["BIL"]+0.10*r["UPRO"],
        "offensive 80 BIL/20 UPRO":   0.80*r["BIL"]+0.20*r["UPRO"],
        "two-wing 85/7.5/7.5":        0.85*r["BIL"]+0.075*r["UPRO"]+0.075*r["VIXM"],
        "— middle: 60/40 (SPY/IEF)":  0.60*r["SPY"]+0.40*r["IEF"],
        "— SPY":                      r["SPY"],
        "— overlay: 90 SPY/10 VIXM":  0.90*r["SPY"]+0.10*r["VIXM"],
    }
    M={k:metrics(v,months) for k,v in books.items()}
    print(f"\n  {'book':28}{'Sharpe':>8}{'CAGR':>8}{'maxDD':>8}{'worstMo':>9}{'skew':>7}{'Calmar':>8}")
    for k,v in books.items():
        m=M[k]; print(f"  {k:28}{m['sh']:>+8.2f}{m['cagr']*100:>+7.1f}%{m['dd']*100:>+7.0f}%{m['worst']*100:>+8.1f}%{m['skew']:>+7.2f}{m['calmar']:>+8.2f}")

    print("\n  CRISIS MONTHS (does the convex wing pay when the middle bleeds?)")
    tests=[("2020-03","COVID"),("2022-06","inflation"),("2022-09","rate shock"),("2025-04","tariffs")]
    print(f"    {'book':28}"+"".join(f"{lbl:>12}" for _,lbl in tests))
    for k in ("defensive 90 BIL/10 VIXM","offensive 90 BIL/10 UPRO","— middle: 60/40 (SPY/IEF)"):
        v=books[k]; row=""
        for mm,_ in tests:
            idx=[i for i,m in enumerate(months) if m==mm]; row+=f"{(np.prod([1+v[i] for i in idx])-1)*100 if idx else float('nan'):>+11.1f}%"
        print(f"    {k:28}{row}")

    print("\n  READ: the barbell's signature is BOUNDED downside (tiny maxDD — 90% is cash) + POSITIVE skew")
    print("  (the convex wing). But in a bull decade it LAGS the 60/40 middle on return/Sharpe — the cash")
    print("  drag, same lesson as bide. 'Convexity done right' is usually the small convex OVERLAY on a real")
    print("  core (last row ≈ bulkhead/contextual_rescue), which keeps the upside AND flips the skew — not the")
    print("  cash-heavy barbell. Antifragile and crash-proof, yes; but return-dominated out of the tails.")

if __name__ == "__main__":
    main()
