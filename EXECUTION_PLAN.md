# ZAR X — EXECUTION PLAN (Phase 2 → Phase 8)
*Written 2026-07-21 for ALL future sessions (Opus, Sonnet, any model).
Follow this like a checklist. Do NOT improvise, do NOT reorder, do NOT skip
a gate. If something here conflicts with reality, STOP and tell the Commander.
Read together with: ROADMAP.md (state), SHIP_LAWS.md (laws), README.md (THE PROMISE).*

## THE GOAL (the Commander's own words, so it is never lost)

A system that uses the world's best proven strategies and tools, checks the
markets, gives signals (possibly on different time intervals), and it is the
COMMANDER'S decision to take a signal or not. The system checks its OWN
signals afterward — grades them, tracks accuracy — so it can be improved
over time. Human decides; machine informs, remembers, and self-examines.

## RULES FOR EVERY WORK SESSION (read before touching anything)

1. `git pull` FIRST. The cloud commits every 4 hours; work on a stale copy
   creates conflicts.
2. Run environment: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with
   `PYTHONUTF8=1`. The Commander is a non-programmer: plain words, gray-box
   commands only, explain then commit (Law 5).
3. One part at a time. Every part gets a smoke test (its gate) run against
   reality BEFORE its commit. Gate fails → fix or revert; NEVER commit a
   failing part. NEVER mark a step done when its gate did not pass.
4. Signals doorway (permanent law): anything that says buy/sell must first
   earn an honest stat card in the Lab. Information (describing the chart)
   may be added to the Brief anytime. No tool skips the Lab — not RSI, not
   Fibonacci, not any legend's favorite.
5. Never delete or rewrite evidence files (snapshots_*.csv, vault/, per-trade
   CSVs). Append or create new; history is sacred.
6. IF a session finds this plan impossible at some step (API dead, library
   gone, laptop can't handle it) → do NOT silently substitute something else.
   Write the blocker into PROGRESS_LOG.md, tell the Commander, stop that step.

---

# PHASE 2 — THE LAB (build in THIS exact order)

The Lab is the courtroom. Nothing becomes a signal without surviving it.
Est. 3–5 short sessions. Each step below = one commit with a gate.

## Step 2.1 — The Frozen Vault (do FIRST — everything else depends on it)

WHAT: a one-time download of deep history, saved to disk, checksummed,
never modified again. Without it, "hold-out testing" is rhetoric because a
live API always returns fresh data.

BUILD:
- `lab/build_vault.py` — uses data/market_data.py `get_history()`:
  BTC-USD, ETH-USD, SOL-USD × timeframes 4h and 1d × as far back as
  TwelveData allows (target ≥ 3 years; accept what the API gives, record it).
- Save to `lab/vault/{asset}_{timeframe}.csv`. Write `lab/vault/MANIFEST.json`:
  rows, first/last candle time, SHA-256 checksum per file, download date.
- `lab/verify_vault.py` — recomputes checksums vs MANIFEST; prints
  VAULT INTACT or VAULT CORRUPTED per file.

GATE 2.1: (a) all 6 files exist with plausible row counts (4h ≥ ~4,000 rows
per asset for 2y+); (b) verify_vault.py prints INTACT for all; (c) run
verify twice — identical output.
- IF TwelveData free tier refuses deep history → take the maximum it gives,
  record the actual depth in MANIFEST and PROGRESS_LOG, continue. 2 years is
  enough to start; 1 year is the minimum acceptable — below that, STOP and
  ask the Commander whether to pay/wait/proceed thin.
- IF download interrupted midway → delete partial files, rerun; the vault is
  only born complete.
- Commit vault CSVs + MANIFEST to git (they are evidence). If GitHub rejects
  size (>100 MB/file — unlikely for candles), keep vault local, commit only
  MANIFEST, and note it in PROGRESS_LOG.

## Step 2.2 — The Data Validator (the quality inspector at the door)

BUILD: `lab/validator.py` — takes any candle DataFrame and reports:
missing candles (gaps vs the timeframe grid), duplicate timestamps,
zero/negative/NaN prices, high < low rows, absurd single-candle moves
(>25% — flag, don't delete). Output: a plain-words report + PASS/WARN/FAIL.

GATE 2.2: feed it (a) a clean vault file → PASS; (b) a COPY deliberately
corrupted (drop 5 candles, duplicate 2, one negative price) → it must name
all three diseases. IF it misses any → fix before commit.
- Wire it into build_vault (vault files must PASS at birth) and run it inside
  the Lab before any backtest (garbage in = lies out).

## Step 2.3 — The honest backtest engine (the heart)

BUILD: `lab/engine.py` around ONE simple contract:
    signal(df) -> 'long' | 'short' | 'flat'   (for each candle, in order)
- Chronological walk, candle by candle. The strategy sees ONLY candles up to
  "now" (pass df.iloc[:i+1], never the future).
- Entry at NEXT candle's open after a signal (no same-candle magic).
- Exits: ATR stop-loss / take-profit from risk/calculator.py logic (the
  Discipline Engine sets exits, same as live) — checked against each candle's
  high/low; if both hit in one candle, count the LOSS (pessimistic rule).
- COSTS on every simulated trade: fee 0.1% per side + slippage 0.05% per side
  (defaults in config.py, adjustable). The 1h-scar law: costs killed a "real"
  edge once; they are never optional.
- Position sizing: the same stop-distance formula as live (1% risk).
- Output: (a) stat card — trades, win%, profit factor, avg win/avg loss,
  max drawdown, net return, time in market; (b) per-trade CSV X-ray to
  `lab/results/{strategy}_{asset}_{tf}_{run-date}.csv` with entry/exit
  times+prices, P&L, regime at entry.
- Hold-out discipline: engine takes `train_end` date; the strategy's
  parameters may only be chosen looking at data BEFORE train_end; the stat
  card that counts is computed ONLY on data AFTER it. Vault data only —
  never live API inside the Lab.
- Strategy versioning (architect #6): every result row and stat card is
  stamped with strategy name + parameter fingerprint (hash of its params) +
  git commit. A survivor's record dies the moment its parameters change.

GATE 2.3 (three dummies, all must behave):
1. always-flat strategy → exactly 0 trades, 0 P&L.
2. MA-cross (20/50) → produces a full stat card on the hold-out window with
   plausible numbers (trades > 0, costs visibly subtracted).
3. THE CHEAT: a planted look-ahead strategy (peeks at tomorrow's close).
   Run it TWO ways: (a) fed the future → absurdly profitable; (b) through the
   engine's proper candle-by-candle feed → the cheat must be IMPOSSIBLE
   (engine never exposes future candles). Document in the smoke test HOW the
   engine structurally prevents look-ahead.
- IF any dummy misbehaves → the Lab is lying; fix before ANY real strategy
  is tested. This gate is the whole point of Phase 2.

## Step 2.4 — The Lie Detectors (bolt onto the engine)

BUILD, each with its own small gate:
- `lab/walk_forward.py`: split hold-out into rolling windows (e.g. 6 windows);
  stat card per window. RULE: a strategy is only "consistent" if profitable
  in ≥ 60% of windows AND no single window contributes > 50% of total profit
  (the lucky-month detector — the +20% Feb that flipped sign taught us this).
- `lab/monte_carlo.py`: reshuffle the per-trade P&L sequence 10,000×; report
  the 5th-percentile equity path and max-drawdown distribution. RULE: if the
  5th percentile is ruinous (> 30% drawdown), the strategy is a coin with
  good luck, regardless of its average.
- `lab/regime_report.py`: per-trade CSV already carries regime-at-entry;
  break the stat card down by regime (Trending/Ranging/Chaotic). Information
  for the verdict, not an auto-filter.

GATE 2.4: run all three on the MA-cross dummy from 2.3 — they must produce
readable reports without error, and walk-forward must correctly flag it if
one window carries the profit.

## Step 2.5 — Phase 2 exit gate (before anything else is built)

The Lab must catch a deliberately-bad strategy end to end: take the
look-ahead cheat's RESULTS faked as a "great strategy" (or an overfit
1000-parameter curve-fit on train data) and show the pipeline exposes it
(hold-out collapse, walk-forward inconsistency, Monte Carlo ruin).
Write the demonstration into PROGRESS_LOG.md.
- IF the Lab certifies the bad strategy as good → Phase 2 is NOT done,
  no matter how nice the code looks. Fix and repeat.

---

# PHASE 3 — CONTEXT DECK (information, never signals)

Order: one instrument per commit, each fail-safe ("instrument offline"),
each appearing as a new section on the Morning Brief.
1. Fear & Greed index (alternative.me, free, no key).
2. Funding rates display (Binance public API) — raw numbers + plain-words
   line ("longs are paying shorts 0.05%/8h — crowd is leaning long").
3. News headlines (CryptoPanic free tier) — headlines ONLY, no sentiment
   score, no invented weights (the cut ghost stays cut).
4. Event calendar (manual JSON file the Commander can edit + known recurring
   events: FOMC, CPI dates).
GATE per instrument: appears on the Brief with live data; unplugging the
internet (or a bad key) degrades to "offline" without breaking the Brief.
- IF a free API dies or paywalls → mark instrument offline, log it, move on.
  NEVER substitute a paid API without the Commander's yes.

# PHASE 4 — CARRY MONITOR (Layer 7, structural income instrument)

- `cockpit/carry.py`: reads funding rates for BTC/ETH/SOL perps (Binance
  public), computes the annualized delta-neutral carry (long spot + short
  perp), prints it with the risk caveats VERBATIM: exchange counterparty
  risk, funding can flip negative, needs capital on both legs.
- It is an instrument (a readout), NOT a signal; no Lab gate needed, but it
  NEVER says "do it" — it says "the carry currently pays X%/yr IF you run it".
GATE: readout matches the exchange's own displayed funding within rounding.

# PHASE 5 — TRADE LOGGER & MIRROR (grades the pilot, closes the loop)

1. `journal/log_trade.py` — one command, questions in plain words:
   asset, direction, entry, exit, size, WHY (one line), feeling (one word).
   Appends to `journal/my_trades.csv`. Never judges at entry time.
2. `journal/mirror.py` — monthly: the Commander's logged trades vs what the
   system's instruments said at those moments (from snapshots) vs what a
   disciplined 1%-risk version of the same trades would have done.
   Output: plain-words report. No shaming, arithmetic only.
GATE: log 2 fake trades, run mirror, numbers check out by hand.

# PHASE 6 — THE GAUNTLET (THE PROMISE: exactly 3 slots, then it closes)

*Only enter Phase 6 when Phases 2–5 are done and at least 4 weeks of
snapshots+grades exist. The gauntlet uses the Lab; the Lab must be trusted.*

THE THREE SEALED SLOTS (from README/THE PROMISE — no substitutions):
- Slot 1: Turtle/Donchian breakout, daily(+weekly filter), regime-filtered.
- Slot 2: Funding-rate extreme fade (needs funding history collected since
  Phase 3/4 — start recording funding to CSV the day Phase 3.2 ships).
- Slot 3: On-chain cycle thermometer (MVRV or similar free source; if no
  free source exists at build time, the slot may be re-specified ONCE by the
  Commander BEFORE testing begins, never after seeing any results).

GATES — LOCKED NOW, BEFORE ANY TEST (changing them after seeing results =
cheating, forbidden):
- Hold-out (vault, after train_end): Profit Factor ≥ 1.15 AFTER costs
- ≥ 30 hold-out trades (fewer = sample too small = FAIL, not "promising")
- Walk-forward: profitable in ≥ 60% of windows, no window > 50% of profit
- Monte Carlo 5th percentile: max drawdown < 30%
- Must beat buy-and-hold-with-1%-risk-sizing on the same window (the
  parrot's big brother) — otherwise the strategy adds nothing over sitting
  in the market.
- Kimi (or any second AI) reviews the test setup BEFORE running and the
  verdict AFTER; the review text goes into PROGRESS_LOG.md.

PROCEDURE per slot: implement signal() → Lab full pipeline → verdict.
- IF PASS → the strategy earns a place in Phase 7 proving. Freeze its
  parameters (fingerprint stamped); any change = back to the gauntlet
  (costs nothing, it's code — but the track record resets).
- IF FAIL → write the honest obituary in PROGRESS_LOG.md, move to next slot.
  No parameter-tweaking resurrection ("just try 25 instead of 20" = the
  overfitting death spiral; the answer is NO, the slot is spent).
- IF ALL THREE FAIL → THE PROMISE executes: the signals chapter closes
  PERMANENTLY. Zar X remains a cockpit: Brief, Planner, Context Deck, Carry
  Monitor, Journal, Mirror. That is still a complete, valuable system. No
  fourth slot, no "one more idea". This sentence is the whole reason the
  promise exists.

# PHASE 7 — PROVING VOYAGE (only with gauntlet survivors)

- 8 weeks minimum, ZERO real money.
- Survivor strategies run daily (scheduled, like snapshots): every signal
  is written to `journal/signals_{strategy}.csv` at candle close — asset,
  direction, entry, SL, TP, size for a nominal $1,000, strategy fingerprint.
- The Commander sees signals on the Brief. Taking them (on paper or at all)
  is HIS choice; the system never nags (no trade-count caps — his decision,
  recorded 2026-07-20).
- The grader (extended) scores every signal like it scores trend claims:
  did it hit SL or TP first? Running honest P&L per strategy.
- WEEKLY: one-line report on the Brief ("Turtle: 3 signals, 2 wins, paper
  P&L +1.8% after costs").
- EXIT GATE after 8 weeks: live-proving Profit Factor within 70% of its
  hold-out PF AND ≥ 10 signals. IF worse → 4-week extension, once. Still
  worse → the survivor dies with honors (obituary in the log); if no
  survivors remain → Phase 6 all-fail clause applies.
- IF the Commander wants real money after a survivor passes proving: his
  capital, his exchange, his hands on the keys. Zar X gives numbers
  (entry/SL/TP/size), never touches funds. Start at 1% risk with money he
  can lose entirely. (The AI never executes trades and never handles
  credentials — permanent law.)

# PHASE 8 — THE PERMANENT LOOP (years, not weeks)

Daily: Brief (+signals if survivors exist) → Commander decides → journal
records → grader scores. Monthly: Mirror review + "review the journal"
session (Opus recommended). Quarterly: re-verify vault checksums, re-run
survivors through the Lab on the newest frozen data (edge decay check —
IF a survivor's rolling 6-month PF < 1.0, it is retired with honors;
retirement is announced on the Brief, not hidden).
Learning stays HUMAN-IN-THE-LOOP: the system proposes nothing by itself;
improvements come from review sessions, and every change to anything that
signals goes back through the Lab. Self-tuning autopilot remains a cut
ghost forever (50 trades/year cannot teach a machine; it can only overfit).

---

# STANDING IF/THEN TABLE (for any session, any phase)

| IF this happens | THEN do this |
|---|---|
| A gate fails | Fix or revert. Never commit. Never "mostly passed". |
| Git conflict on evidence CSVs | Should be impossible now (writer-split). If one appears anyway: union-merge (keep ALL rows), never delete evidence. |
| TwelveData quota/key dies | Brief/snapshots degrade to "offline" honestly. Commander rotates/upgrades key. Never hardcode a key. |
| A library breaks (the pandas-ta lesson) | Vendor the exact working version; never upgrade-and-pray on a working ship. |
| An AI (any model) proposes a shortcut around a gate | The gate wins. Gates outrank models. |
| Commander asks "can we add tool X?" | As Brief information: yes, small session. As a signal: Lab first, stat card first. |
| Results look TOO good (>2 PF, >70% win) | Assume a bug or leak first. Hunt the leak (look-ahead, survivorship, costs off). Celebrate only after the lie detectors pass. |
| A session is unsure what state the ship is in | `git pull`, read ROADMAP.md + last 3 PROGRESS_LOG entries + this file. Never guess. |
| Anything contradicts THE PROMISE | THE PROMISE wins. 3 slots. Then the chapter closes. |

# CURRENT POSITION MARKER (update this line each session)

→ We are at: **Phase 2, Step 2.1 not yet started.** Before it: Commander
rotates the TwelveData key. Friday 2026-07-26: week-1 review on honest
grader-v2 numbers. Then Step 2.1, the Frozen Vault.
