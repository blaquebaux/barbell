# barbell

**Taleb's barbell — safe core + convex sliver, vs the "mediocre middle".**

The barbell, not the caricature: hold the vast majority in **safe** assets (bounded downside) and a tiny
sliver in **convex** bets (unbounded upside), and avoid the mediocre middle (a 60/40). Antifragility =
you can't lose much, and you win in the tails. Does it actually beat the middle on a tail basis? This
tests it — including the honest comparison to deploying the same convexity as an *overlay* on a real
core (the [`contextual_rescue`](https://github.com/blaquebaux/nullbar/blob/main/contextual_rescue.py)
result). Alpaca SIP daily, total-return; daily-rebalanced; cash = `BIL`.

## Verdict

**CONDITIONAL KEEPER — Taleb's thesis survives: convexity done right beats the middle on risk-adjusted
and tail terms, at the cost of absolute return.** The two-wing barbell has the best Sharpe, the best
Calmar, a positive skew, and a −4% drawdown — it dominates the 60/40 on everything except raw CAGR,
which is the trade you're knowingly making.

| book | Sharpe | CAGR | maxDD | worst mo | skew | Calmar |
|---|---|---|---|---|---|---|
| **two-wing 85 BIL / 7.5 UPRO / 7.5 VIXM** | **+1.58** | +4.2% | **−4%** | −1.6% | **+0.63** | **+0.98** |
| offensive 90 BIL / 10 UPRO | +1.12 | +5.9% | −11% | −3.8% | −0.40 | +0.51 |
| defensive 90 BIL / 10 VIXM | +0.35 | +1.1% | −10% | −1.6% | **+1.72** | +0.11 |
| offensive 80 BIL / 20 UPRO | +0.92 | +9.4% | −22% | −8.1% | −0.40 | +0.43 |
| — middle: 60/40 (SPY/IEF) | +0.93 | +9.7% | −21% | −7.4% | −0.24 | +0.46 |
| — SPY | +0.88 | +15.0% | −34% | −12.6% | −0.35 | +0.44 |
| — overlay: 90 SPY / 10 VIXM | +0.98 | +13.1% | −25% | −7.7% | +0.03 | +0.52 |

*2016-01 … 2026-07 (10.5y), daily-rebalanced.*

## What the barbell actually delivers

- **The antifragile signature is real.** The defensive wing (cash + long-vol) has a **+1.72 skew** and is
  *green in every crisis* (COVID +6.0%, rate shock +0.8%, tariffs +1.8%) — it structurally profits from
  disorder. The two-wing version adds a levered-equity sliver for upside and still holds a −4% max
  drawdown and +0.63 skew. You genuinely cannot lose much, and you win in the tails.
- **It beats the middle where Taleb says it should.** Two-wing barbell vs 60/40: Sharpe +1.58 vs +0.93,
  Calmar +0.98 vs +0.46, skew +0.63 vs −0.24 — the "mediocre middle" is dominated on every risk-adjusted
  and tail measure. The barbell's bet (concentrate risk in the extremes, hold nothing in the middle) pays.
- **The cost is honest and large: absolute return.** +4.2%/yr vs the middle's +9.7% and SPY's +15.0%.
  Because 85–90% sits in cash, you need to deploy far more capital — or lever the barbell — to earn
  meaningful dollars, and levering reintroduces the risk you removed.

## The caveat, and the alternative

Cash-heavy books **flatter the Sharpe ratio** (a tiny vol denominator), so read the +1.58 alongside the
+4.2% CAGR — Calmar (+0.98, return per unit of drawdown) is the more honest headline and it's still the
best in the field. And in a bull decade you give up a lot by sitting in cash.

The higher-return cousin is the **overlay, not the barbell**: 90% SPY + 10% VIXM (last row) keeps +13.1%
CAGR *and* flips skew to ~0 at a better Sharpe than SPY — that's `contextual_rescue`/`bulkhead` territory,
convexity bolted onto a growth core instead of a cash core. **Barbell = convexity for a preservation-first
mandate; overlay = convexity for a growth mandate.** Both beat the naked middle; which you pick is the
mandate.

## `barbell_2`

Replace the ETF convex wings with **actual OTM options** (Massive/OPRA) — the true Taleb barbell is
cash + far-OTM calls/puts, whose convexity (and premium cost) the VIXM/UPRO proxies only approximate —
to measure the real net-of-premium antifragility across a severe crash.

## Reproduce

```bash
export ALPACA_KEY_ID=... ALPACA_SECRET_KEY=...
python3 research/barbell_1.py
```

---

*Blaque Baux — a Carter Warrens research initiative. Research only; not investment advice. The verdict
falls where the data puts it — the middle is comfortable and the barbell is correct.*
