# ZAR X — ROADMAP & HANDOFF
*The single document a new session (any model) reads to continue the work.
FOR PHASE 2 AND BEYOND: follow EXECUTION_PLAN.md — exact steps, gates, and
if/then orders for every phase. It outranks improvisation.*
State as of 2026-07-26 (PHASE 2 COMPLETE; PHASE 3 OPEN — Steps 3.1 and 3.2
DONE, Gates 3.1 passed 45/45 and 3.2 passed 48/48). Read with README.md
(mission + THE PROMISE), SHIP_LAWS.md
(now SEVEN laws — Law 7, the Leak Law, added 2026-07-26),
EDGE_STACK_RESEARCH.md (why), PROGRESS_LOG.md (history).
**THE_PATTERN.md is how a session runs** — the three layers (the gate declared
first · the sabotage drill that lives in the code forever · the independent
attack only a non-builder can perform), and the rhythm every session follows:
**ATTACK what the last session built, THEN build the next thing.** It is the
substitute for Fable and it says plainly where it is weaker.

**REVIEW_QUEUE.md is the docket of everything this ship could NOT honestly
certify itself** — the first file an independent reviewer (Fable, or any second
AI) should open, kept short on purpose so it is actually read rather than
skimmed. Every session files there before shipping anything it is unsure of,
and **no session may clear its own item.**
**NEXT SESSION: R-017 — a TWELFTH sabotage against the open-interest recorder,
invented by someone who built none of it. AND ON THE COMMANDER'S DESK FIRST:
R-016, two doors into the Brief that were found, graded BORDERLINE, and
DELIBERATELY LEFT OPEN pending his ruling.**
**CONTEXT: SEVEN independent reviews in a row have each failed the repair before
them.** The newest, 2026-07-29, asked *what is the gate's own EAR deaf to?* —
and found that `redirect_stdout` rebinds a NAME, so a logging handler bound at
import time or a write to file descriptor 1 walks straight past the silence
check; that nothing anywhere watches what a module writes at IMPORT time; and
that **no check had ever asserted the recorder's printed REPORT is true**, on
the one line the Commander has been ordered to judge the recorder by. **Three of
three attacks escaped. R-015 FAILED. Only the recorder was repaired (Gate
3.2b-R4, ELEVEN sabotages) because only it graded SERIOUS; R-016 holds the other
two open for the Commander. R-001 has now outlived SIX FAILED generations of fix
and the seventh is untested — it moves only when one SURVIVES an independent
attack, and none ever has.**
**AND THE LARGER HOLE THE NEWEST FINDING SITS INSIDE, STILL OPEN:
`cockpit/brief.py` — the pilot's actual daily tool — HAS NO GATE AT ALL.**

## What exists and works (all gated live, all pushed)
| Part | File | Status |
|---|---|---|
| Data (candles, 429-proof, paginated, hold-out capable) | data/market_data.py | ✅ |
| Indicators (Elite set + EMA 20/50/200, cores=0) | indicators/technical.py | ✅ |
| Risk — Discipline Engine (ATR SL/TP, stop-distance sizing, 25% cap) | risk/calculator.py | ✅ |
| Regime vane (per-TF dials: 4h=1.96 calibrated; fail-honest) | regime/vane.py | ✅ |
| Morning Brief (the user's daily tool). **IT HAS NO GATE OF ITS OWN — noted 2026-07-28 night, R-015 doubt 2.** Every instrument it prints is now gated hard, and the file that assembles them is checked by nothing. It was read by eye and does only `print(section())`, which is exactly the kind of "verified by reading" this ship has been wrong about six times. | cockpit/brief.py | ✅ |
| Journal snapshots (the black box, split by writer: laptop → snapshots_local.csv, cloud → snapshots_cloud.csv, legacy snapshots.csv frozen) | journal/snapshot.py | ✅ |
| Grader v2 (merges all notebooks, candle-identity de-dup, always-UP parrot baseline) | journal/grader.py | ✅ |
| Automation (Task Scheduler: brief 09:05 PKT; snapshots at every 4h close) | run_daily.bat / run_snapshot.bat | ✅ |
| **Open-interest recorder (Phase 3, Step 3.2b) — Binance 30-day window, `period=4h`, append-only CSV per asset, idempotent, never rewrites history. GATE 3.2b-R3 PASSED 2026-07-28 (night): eleven bars and TEN sabotages caught; the drill judges THE CSV ON DISK against a raw fetch for every asset, and the asset list is **the gate's own (`GATE_SYMBOLS`), not the module's**. New check (k) builds **MONTH TWO** — a partial window seeded by the test, then appended to — because every other row-level check wrote into an EMPTY directory, so the gate had only ever tested month one and month one happens once. **B10** transposed the OI column on the append path alone: 80 of 180 rows landed 64,763x wrong and all nine sabotages were scored CAUGHT, B4 (that exact lie) among them. Two independent sabotages walked through the previous gate the same day: **B9** cut `SYMBOLS` to two assets and SOLUSDT vanished from the recorder *and from its own detector*, permanently, all green; **B8** made `--record` — the branch the monthly task actually runs, which no test had ever executed — always exit 0, so a failed job reported success. New check (j) now runs `--record` for real as a subprocess in BOTH outcomes, against a copy in scratch. 540 rows recorded. SCHEDULED 2026-07-27: task `ZarX Open Interest`, day 1 monthly, 09:00, on the laptop only (Binance geo-blocks US cloud runners), catches up if the laptop was off. **GATE 3.2b-R4 PASSED 2026-07-29: ELEVEN sabotages, new check (l) — THE PRINTED REPORT MUST MATCH THE DISK.** Every detector here read the CSV back off disk and **nothing had ever asserted that the line this recorder PRINTS is true** — yet that line is its only human-readable output, it goes to `journal/daily_runs.log`, and the Commander's standing order is to judge the recorder BY IT. **B11** wrote `'appended': len(fresh)` for `len(new_rows)`: the disk stayed byte-perfect, ten of ten sabotages were scored CAUGHT, and the report claimed 180 appended rows on a run that appended none (the healthy control printed 0). The gate now counts the rows ITSELF before and after, and runs the recorder TWICE — the lie is invisible on run one and plain on run two. **R-015 FAILED. R-017 open against this repair**, whose own filed doubt is that check (l) guards `appended` and `total` but **not** the `window X → Y` timestamps the same line prints. Still known-weak: check (e) is BTCUSDT-only, B1 is a no-op on a UTC machine. **MEASURED 2026-07-29: the recorder has run exactly ONCE ever (by hand, 2026-07-27, 0 rows appended); the commit-and-push branch has still never fired against real new rows; next scheduled run 1 Aug 09:00, and the honest figure that day is roughly THIRTY rows, not 180.** | data/open_interest.py + data/oi_history/ | ✅ |
| Context Deck — instrument 1 of 5: Fear & Greed (alternative.me, free, keyless; injectable URL, fails to one offline line). **GATE 3.1-R5 (hardened 2026-07-28 night): the self-test rebuilds the WHOLE printed block and requires EXACT equality on BOTH paths the pilot can see — live AND offline — every constant it judges by is typed out in the gate and compared to the module's by name (the disclaimer, the history limit, the offline wording), and (new) it proves the doorway writes NOTHING to stdout or stderr of its own, on both paths, because the Brief is assembled only from what it RETURNS. It breaks itself FOURTEEN ways every run, all fourteen caught. **F14** printed 'historically a buying opportunity' straight to stdout with the returned block byte-identical, and walked through — in the same run that scored F7, 'the disclaimer turned into ADVICE', as CAUGHT. The offline bar was itself built from the MODULE'S `OFFLINE_WORDS` until 2026-07-28 evening, when F13 reworded that one constant so the lie and the bar moved together — the pilot's offline line read 'last known reading 72 — Extreme Greed' on a day the index read 29 — Fear, and the gate ticked it. **R-015 FAILED 2026-07-29 and THIS GATE WAS NOT REPAIRED — the Commander must rule (R-016).** Sabotage **F15** put one advice `print` at MODULE level: nothing anywhere watches what a module writes at IMPORT time, and `brief.py` imports this file, so the advice became the first line of the Brief — and the first line of the gate's own output, which then passed itself. | cockpit/fear_greed.py | ✅ |
| Context Deck — instrument 2 of 5: funding rates (Binance USDⓈ-M public, free, keyless; USDT perpetuals, partial failure names the missing asset). **GATE 3.2-R5 (hardened 2026-07-28 night): the self-test rebuilds the WHOLE printed block from Binance raw using its own arithmetic and requires EXACT equality on EVERY path the pilot can see — healthy, degraded and offline — holds its OWN copy of the "positive = longs pay shorts" wording, of the tickers and of the offline wording, each compared to the module's by name; rotates the partial-failure drill through all three assets; (new) proves the doorway writes NOTHING to stdout or stderr of its own on all three paths, because `brief.py` runs the function before it prints what the function returns; and breaks itself FIFTEEN ways every run, all fifteen caught. **S15** printed 'close longs before the 16:00 settlement' to stdout with the returned block byte-identical, thirty times on the gate's own screen, and walked through. The offline bar was itself built from the MODULE'S `OFFLINE_WORDS` until 2026-07-28 evening, when S14 reworded that one constant and a fabricated "last reading BTC +0.0100%, longs paying" walked through with a tick mark reading "NOTHING appended". **R-015 FAILED 2026-07-29 and THIS GATE WAS NOT REPAIRED — the Commander must rule (R-016).** Sabotage **S16** proved the silence check's ear is deaf: `redirect_stdout`/`redirect_stderr` rebind a NAME, so a `logging` handler bound to the real stderr at import time — or `os.write(1, …)` straight to the file descriptor, on stdout itself — walks past it. 35 advice lines on the gate's own screen, three green ticks underneath reading "the doorway wrote NOTHING to stdout or stderr of its own", PASSED, exit 0; shown landing on the real Brief, and `run_daily.bat` writes it to `journal/daily_runs.log` with `2>&1` and copies it to the Commander's phone. Still unguarded: the block printed when TWO of three assets fail is built by no check anywhere. | cockpit/funding.py | ✅ |
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
   ✅ Fear & Greed (alternative.me, free) — **audited 2026-07-26: leaked 5 of 6
   sabotages; GATE 3.1-R rebuilt, then FAILED 2026-07-27 when 3 of 5 NEW
   sabotages walked through it, including ">> strong buy signal" printed on the
   deck; GATE 3.1-R2 shipped the same day, all ELEVEN now caught every run** ·
   ✅ funding rates display (Binance USDⓈ-M public, free) — **leaked 4 of 6;
   GATE 3.2-R rebuilt, then FAILED 2026-07-27 when 4 of 5 NEW sabotages walked
   through, including the meaning REVERSED with every digit correct; GATE
   3.2-R2 shipped the same day, all ELEVEN caught** · ⏭️ **a TWELFTH sabotage on
   each, by someone who built neither (R-011), and a seventh on the recorder
   (R-012). **Step 3.2b SHIPPED 2026-07-27** — the open-interest recorder — the
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

## MEASURED data-source facts (probed 2026-07-26, ALL RE-PROBED 2026-07-27 and none had moved — never plan on a guess again)

**ADDED 2026-07-27, and it corrected a planning document: a Binance 4h
open-interest row is a POINT SAMPLE taken at the stamped instant, NOT a running
aggregate over the following four hours.** 33 of 33 overlapping rows across
BTC/ETH/SOL matched the 5m reading at the same instant exactly, while the 5m
series kept moving afterwards and the 4h row did not. **So there is no
"incomplete period" to hold back, and the newest row is stored.** The orders
had warned of an incomplete-period trap; the premise was untested and the
measurement won. **Fifth time.**

**ADDED 2026-07-28: the live snapshot endpoint `GET /fapi/v1/openInterest` was
called for ETHUSDT and SOLUSDT for the first time.** It had only ever been
called for BTCUSDT — which is precisely why sabotage B7 could fill two assets
with Bitcoin's figures unseen. It answers for all three, each in its own
contract's units, and the recorder's newest stored point sample sits **0.34% /
0.52% / 0.55%** away from it for BTC / ETH / SOL. **The 10% plausibility bar is
still a guess (R-012 doubt 4) — but it is now a guess measured against three
assets instead of one.**

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
