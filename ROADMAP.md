# ZAR X — ROADMAP & HANDOFF
*The single document a new session (any model) reads to continue the work.
FOR PHASE 2 AND BEYOND: follow EXECUTION_PLAN.md — exact steps, gates, and
if/then orders for every phase. It outranks improvisation.*
State as of 2026-07-26 (PHASE 2 COMPLETE; PHASE 3 OPEN — Steps 3.1 and 3.2
DONE, Gates 3.1 passed 45/45 and 3.2 passed 48/48). Read with README.md
(mission + THE PROMISE), SHIP_LAWS.md
(now SEVEN laws — Law 7, the Leak Law, added 2026-07-26),
EDGE_STACK_RESEARCH.md (why), PROGRESS_LOG.md (history).
**REVIEW_QUEUE.md is the docket of everything this ship could NOT honestly
certify itself** — the first file an independent reviewer (Fable, or any second
AI) should open, kept short on purpose so it is actually read rather than
skimmed. Every session files there before shipping anything it is unsure of,
and **no session may clear its own item.**
**NEXT BUILD SESSION: read SESSION_ORDERS.md — it carries the current step's
exact orders. BUT READ THIS FIRST: the 2026-07-26 audit FAILED Gate 3.2 and
STEP 3.2 IS REOPENED. The 48/48 tally is void; 4 of 6 deliberate sabotages
passed that gate. The printed numbers are correct — the guard is not. Rebuild
Gate 3.2 around what the pilot READS before Step 3.2b is touched.**

## What exists and works (all gated live, all pushed)
| Part | File | Status |
|---|---|---|
| Data (candles, 429-proof, paginated, hold-out capable) | data/market_data.py | ✅ |
| Indicators (Elite set + EMA 20/50/200, cores=0) | indicators/technical.py | ✅ |
| Risk — Discipline Engine (ATR SL/TP, stop-distance sizing, 25% cap) | risk/calculator.py | ✅ |
| Regime vane (per-TF dials: 4h=1.96 calibrated; fail-honest) | regime/vane.py | ✅ |
| Morning Brief (the user's daily tool) | cockpit/brief.py | ✅ |
| Journal snapshots (the black box, split by writer: laptop → snapshots_local.csv, cloud → snapshots_cloud.csv, legacy snapshots.csv frozen) | journal/snapshot.py | ✅ |
| Grader v2 (merges all notebooks, candle-identity de-dup, always-UP parrot baseline) | journal/grader.py | ✅ |
| Automation (Task Scheduler: brief 09:05 PKT; snapshots at every 4h close) | run_daily.bat / run_snapshot.bat | ✅ |
| Context Deck — instrument 1 of 5: Fear & Greed (alternative.me, free, keyless; injectable URL, fails to one offline line) | cockpit/fear_greed.py | ✅ |
| Context Deck — instrument 2 of 5: funding rates (Binance USDⓈ-M public, free, keyless; USDT perpetuals, partial failure names the missing asset). **PRINTS CORRECTLY — sign and magnitude re-verified against Binance raw 2026-07-26 — but GATE 3.2 IS VOID and the step is REOPENED: the gate could not catch a sign-flipped formatter.** | cockpit/funding.py | ⚠️ |
| THE LAB, complete (Phase 2, Gates 2.1–2.5 all passed 2026-07-26): frozen checksummed vault · data validator at the only door · honest backtest engine (look-ahead impossible, costs always on, hold-out line train_end=2025-10-01) · walk-forward + Monte Carlo (seed 20260726) + regime breakdown · exit gate that caught a 1,687-parameter con artist · leak_check (Law 7's aid) | lab/ | ✅ |

Run environment: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with `PYTHONUTF8=1`.
User is a non-programmer; explain in plain words; he runs commands from gray boxes only.

## Build queue (order now governed by EXECUTION_PLAN.md Phases 3–8; the list
## below is kept for history — EXECUTION_PLAN outranks it where they differ,
## e.g. the Context Deck (Phase 3) now comes BEFORE the trade logger (Phase 5))
1. **lab/** — ✅ DONE 2026-07-26 as EXECUTION_PLAN Phase 2 (five steps, five
   gates, all passed; see the Gate 2.1–2.5 entries in PROGRESS_LOG.md). The
   exit exam proved the pipeline rejects an overfit con artist end to end, and
   its honest limit — numbers cannot catch a leak — became Law 7.
2. **journal/ part 2** — trade logger (user records real/paper trades) + **the grader**
   (scores past snapshots against what prices did next; also monthly review of user's
   logged trades). Gate: grader correctly scores ≥2 weeks of accumulated snapshots.
3. **Context Deck** (cockpit) — 🔨 IN PROGRESS (EXECUTION_PLAN Phase 3, 2 of 5 done):
   ✅ Fear & Greed (alternative.me, free) 2026-07-26 — **not yet audited for the
   class of hole found in funding (R-008)** · ⚠️ funding rates display (Binance
   USDⓈ-M public, free) 2026-07-26 — **REOPENED by the 2026-07-26 audit; prints
   correctly, gate void** · ⏭️ **Gate 3.2 rebuilt FIRST, then Step 3.2b — the
   open-interest recorder (30-day window, backfill at birth), still the only
   dataset on this ship that expires and its deadline did not pause for the
   audit** · then news headlines (CryptoPanic free
   tier), event calendar, whale watch. Information ONLY, never signals. This closes the user's known blind spot: the system
   is math-only today; news/whales knowledge comes from the pilot until this ships.
4. **Layer 7 — Carry Monitor** (Kimi's structural edge): delta-neutral funding carry
   monitor with annualized-rate readout + risk caveats (exchange counterparty, funding
   flips). Instrument, not prediction — no gauntlet needed.
5. **THE GAUNTLET (sealed at 3 slots — THE PROMISE, see README):**
   Slot 1 Turtle/Donchian (daily/weekly, regime-filtered) · Slot 2 funding-rate extreme
   fade · Slot 3 on-chain cycle thermometer. Gates BEFORE each test (default: OOS PF ≥
   1.15, ≥30 trades, no lucky-month carry; Kimi adviser reviews). All fail → signals
   chapter closes permanently; cockpit stays information-only.
6. **Only with gauntlet survivors:** 8-week live proving, zero money, journal judging
   system AND pilot.

## MEASURED data-source facts (probed 2026-07-26 — never plan on a guess again)

Which sources serve deep history on demand decides what must be RECORDED and
what merely has to be READ. Every line below was measured, not assumed:

| Source | Depth actually served, free | Must we record it? |
|---|---|---|
| alternative.me Fear & Greed | FULL history (`limit=0`, back to 2018) | **No** |
| Binance funding rates `/fapi/v1/fundingRate` | **To contract inception** — BTC 2019-09-10, ETH 2019-11-27, SOL 2020-09-13; paginate `startTime` + `limit=1000` | **No** |
| Binance open interest `/futures/data/openInterestHist` | **30 DAYS ONLY** — re-measured 2026-07-26: 180 rows at `period=4h` spanning 29.8 days, identical for all 3 assets; `startTime` 60 days back refused (code -1130). `period=1h` covers only 20.8 days at limit=500, so **4h is the only period that captures the whole window in one call** | **YES — the only one** |
| TwelveData candles (our vault) | ~3y 1d / 4h from 2024-01-01 (glitch zone excluded) | Already frozen in lab/vault/ |

**THE CORRECTION THAT MATTERS (2026-07-26):** earlier planning documents stated
that funding history is NOT served deep and that funding recording must begin
the day Step 3.2 ships, or Phase 6's Slot 2 could never be tested. **That was
wrong** — it was written from assumption and repeated into the Step 3.1 log,
marker and commit before anyone tested it. Binance serves ~7 years of settled
funding on demand. Slot 2 can be tested whenever we choose.

**The urgency was real but attached to the wrong instrument: it belongs to OPEN
INTEREST**, which Phase 3.5's Whale Watch needs and which vanishes after 30
days. And because every read can reach back 30 days, an OI recorder that runs
even monthly loses nothing — so the laptop is a sufficient recorder and there
is no emergency, only a deadline measured in weeks.

Also measured the same day: **OKX does not resolve from the Commander's
connection at all** (DNS failure); Binance and Bybit both answer normally.

**THE SILENT-FAILURE TRAP (measured 2026-07-26, before Gate 3.2b was written):
a bogus symbol on `/futures/data/openInterestHist` returns `HTTP 200` with an
empty list `[]` — it does NOT error.** The funding endpoint returns a clean
HTTP 400 (`code -1121`) for the same mistake, so the two behave oppositely. A
recorder written the obvious way would read `[]`, append nothing, print "0 new
rows", exit 0 and report success every month while the 30-day window silently
rolled past — on the ONE dataset that cannot be bought back later at any price.
**An empty result must be treated as a loud failure, never as "no new data".**
Two smaller traps beside it: the field is `sumOpenInterest` in the history
endpoint but `openInterest` in the live snapshot endpoint, and the payload
carries an unplanned `CMCCirculatingSupply`.

**MEASURED 2026-07-26 by the audit session — the guess was safe, and now it is
a fact.** Binance publishes real funding caps at `/fapi/v1/fundingInfo` (HTTP
200, 736 symbols), an endpoint no earlier session had called:

| Contract | Published cap / floor | Funding interval | Largest actually seen (500 settled periods, from 2026-02-10) |
|---|---|---|---|
| BTCUSDT | ±0.00300 (0.300% / 8h) | 8h | 0.0123% |
| ETHUSDT | ±0.00300 (0.300% / 8h) | 8h | 0.0365% |
| SOLUSDT | ±0.00375 (0.375% / 8h) | 8h | 0.0535% |

`cockpit/funding.py`'s `MAX_PLAUSIBLE_RATE = 0.05` (5%) is **13–16× looser than
the real cap**, so it can never refuse an honest extreme — the failure R-003
feared does not exist. It is also too loose to be a useful fence (it would pass
a rate 80× too large); tightening it to ~0.01 is **recommended and left on the
Commander's desk, not done.**

**The 8h interval on all three is why `min(settlements)` is safe** (R-005
CLEARED) — across all 848 Binance perpetuals there are 5 distinct settlement
times, but the disagreement comes from 4h-interval contracts, which ours are
not.

## Standing answers to the Commander's questions (so they're never re-litigated)
- **"How does it know what will happen?"** It doesn't. It's a weather station + cockpit:
  describes what IS (trend/momentum/volatility/regime) and sizes risk IF the pilot acts.
- **"News/wars/whales?"** Today: pilot's job (human-in-the-loop is the design). The vane
  sees news *footprints* (chaos in price) but not causes. Context Deck (queue #3) adds
  headlines/sentiment as information. Never as signals without the gauntlet.
- **"Can the AI analyze reports to improve the system?"** Yes, in-session: the Commander
  opens a session and says "review the journal" → read snapshots.csv + daily_runs.log,
  report findings, propose improvements (Laws apply). The grader (queue #2) automates
  the scoring half.
- **"Is the code working?"** Every part has a smoke test (its gate) run against the live
  market before commit; failures self-report as "instrument offline"; git reverts anything.

## The Commander's daily ritual (Pakistan time)
Automatic if laptop is awake. Manual any time:
```
cd "C:\Users\hp\Downloads\zargul trader\zar-x"
set PYTHONUTF8=1
C:\Users\hp\miniconda3\envs\tfdml\python.exe cockpit\brief.py
C:\Users\hp\miniconda3\envs\tfdml\python.exe journal\snapshot.py
```

## History and provenance
Born from Zargul Trader 2.0 (github.com/zargul123/zargul-trader-2.0 — the museum):
a year of LSTM prediction work, honestly concluded 2026-07-19 with a complete negative
verdict (tag `prediction-chapter-closed`; full story in its PROGRESS_LOG.md). Zar X
keeps the proven organs and the honesty discipline; it does not predict.
