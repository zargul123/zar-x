# New System Research — The Edge Stack (founding notes)
*Written 2026-07-19, last Fable session. These notes carry the full design intent to any future model/session. Read together with PROGRESS_LOG.md (master plan + verdict matrix) and the memory files.*

## User's goal
Personal signals cockpit (no auto-execution). User decides and clicks. ~40% wrong acceptable IF sizing math makes it survivable. Wants an edge over at least ~60% of market participants. Accepts losing as part of the game; refuses wrong *direction*.

## Core research finding
Most retail traders lose to overtrading, oversizing, leverage, fees, and trading during chaos — NOT to lack of signals. Therefore a large fraction of the target edge is **engineerable with certainty** (discipline mechanics), and only the remainder must be *found* (probabilistic, gauntlet-tested).

## THE EDGE STACK (build order = certainty order)

### Layer 1 — Discipline Engine (certain edge; beats ~40-50% of traders)
- Position sizing from expectancy math; risk per trade capped 1-2%
- Hard SL/TP on every signal (risk engine — ported from Zargul 2.0)
- Expectancy & drawdown tracking; monthly journal audit of the USER's decisions
- Guru wisdom that survives decades = risk frameworks, not entries: Wilder (ATR sizing), Turtles (systematic discipline), Van Tharp (position sizing/expectancy), Mark Douglas (psychology/journaling), Bollinger (volatility cycles), Minervini (risk-first)

### Layer 2 — Chaos Avoidance (edge proven in our own data)
- Recalibrated regime vane (per-timeframe entropy percentiles — method in analyze_regime_4h.py; 1h-tuned thresholds saturate on 4h)
- Scheduled-event calendar: FOMC, ETF decisions, halvings, major unlocks
- News-storm flag (headline velocity/sentiment via free CryptoPanic-tier API)
- Evidence: war-March 2026 cost -32.6% in one month in our tests; skipping deadly weeks is a validated defensive edge

### Layer 3 — Slow Trend Core (GAUNTLET SLOT 1)
- Time-series momentum / Donchian-channel breakouts, DAILY-WEEKLY horizon, regime-filtered
- Rationale: only anomaly with decades of broad evidence incl. crypto; survives because it requires patience capital can't scale; slow clock = cost-tolerant (our 1h autopsy: fees killed everything fast)
- Honest prior: modest (~5-10%)

### Layer 4 — Positioning Fade (GAUNTLET SLOT 2, crypto-native)
- Funding rates + open interest extremes → fade crowded leverage (liquidation-hunt structure)
- Data: Binance/Bybit public APIs, free; younger + less strip-mined than chart math
- Honest prior: ~10%

### Layer 5 — Cycle Thermometer (GAUNTLET SLOT 3 — the "modern" slot, researched pick)
- On-chain valuation/behavior: exchange netflows, MVRV-style bands, long-term-holder supply
- Slow, cycle-positioning signals — matches the winning clock speed
- Free-tier sources exist (e.g., blockchain.com metrics; some premium data paywalled — start free)
- Honest prior: ~10-15%

### Layer 6 — Context Deck (information, never signals; no gauntlet needed)
- Fear & Greed (alternative.me, free), macro risk-on/off (DXY, NASDAQ corr), news headlines, cycle calendar

## Deliberately EXCLUDED (wrong directions, with reasons)
- Speed-based news trading (bots win in ms — unwinnable for retail)
- Anything high-frequency / sub-4h signals (fees + competition; proven dead in our lab)
- Leverage (the #1 account killer; cockpit computes spot-equivalent sizes only)
- Paid signal-sellers / "guru calls" (if it's sold, it's arbed)
- LSTM/NN price prediction (chapter formally closed — tag prediction-chapter-closed; verdict matrix in PROGRESS_LOG)

## The sealed gauntlet contract (THE PROMISE — carved here)
- Exactly 3 slots (Layers 3, 4, 5). Gates DECLARED BEFORE each test (default: OOS PF ≥ 1.15, ≥ 30 trades, not carried by one lucky month; Kimi adviser reviews gates).
- 2 days per slot. One fails → next well. ALL THREE FAIL → signals chapter closes permanently:
  no 4th slot, no re-tests, no paper trading of failed rules, cockpit = information-only;
  no new signal ideas for ≥ 3 months, and any future idea must come from a genuinely NEW
  data source and face the same gauntlet.
- Survivors → 8-week live proving (zero money) with journal review of system AND user.
- If zero survivors: no "proving voyage" (Kimi amendment accepted) — only optional
  instrument-assisted manual trading with monthly honest review of the user.

## Build plan (agreed, all advisers aligned)
1. Stage 1 Hull (1-2 wks): new folder + NEW git repo; 7 sealed compartments (data/ indicators/ regime/ signals/ risk/ lab/ cockpit/), each with smoke test + error isolation ("instrument offline" pattern — one module's failure never stops the rest). Port from Zargul 2.0: data engine, indicators, regime filter, risk engine, backtest lab (incl. ZARGUL_TRAIN_CUTOFF-style hold-out discipline, per-trade CSV X-rays), journal. Deliverable: Morning Brief + trade calculator.
2. Stage 2: gauntlet slots in order 1→2→3.
3. Stage 3 (parallel): Context Deck.
4. Stage 4: only with survivors.

## Expectation calibration (agreed with user)
- Target clock speed: a FEW well-sized trades per MONTH, not 2/day (market is an adversarial game, not physics; high frequency = maximum competition + fee drag)
- Beating ~60% of participants: Layers 1-2 achieve most of this near-certainly; Layers 3-5 are the probabilistic reach (~27% at least one survives per Kimi's math — good pot odds for 6 days of testing)

## Process laws (carried from the prediction chapter)
Explain before change · commit after change · gates before tests · budget sealed · every result to PROGRESS_LOG · Kimi consulted at phase gates · new repo per user's rule (strategy change = new program; port only proven organs)

## AMENDMENT 1 (2026-07-19, adopted from Kimi adviser) — Layer 7 + build order

**Layer 7 — Carry Monitor (structural, adopted from Kimi's "honest map"):** delta-neutral
funding-rate carry (hold spot, short perpetual, collect funding) monitored across
exchanges; cockpit reports current annualized carry and flags attractive/thin/negative.
NOT a prediction — needs no gauntlet win-rate, only risk math. Carved caveats: requires
real capital on a derivatives exchange; yield modest and variable; funding can flip
negative; exchange counterparty risk is real (FTX lesson). Small, boring, real.

**Reading law for all stat cards:** win rate alone is meaningless —
win% × payoff ratio − costs is the only equation. (Our own 1h data: 50.2% wins at
0.70/1.04 payoff = negative.)

**BUILD ORDER A (final):** Hull → Layer 7 Carry Monitor → behavioral context instruments
(Layers 4-6 as information) → the 3 sealed gauntlet slots last. THE PROMISE unchanged.
Concessions recorded: Layers 1-2 = survival precondition, not profit; "60%" target
retired — the market sets bars.
