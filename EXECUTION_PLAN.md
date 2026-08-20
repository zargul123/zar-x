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
   NOTE (2026-07-26): funding history needs NO recording — see the Slot 2
   correction in Phase 6. The dataset that DOES expire is Binance OPEN
   INTEREST (30-day window only), which instrument #5 below needs; it gets
   its own step (3.2b) with a 30-day backfill at birth.
3. News headlines — headlines ONLY, no sentiment score, no invented weights
   (the cut ghost stays cut).
   ~~(CryptoPanic free tier)~~
   **CORRECTED 2026-07-31 (evening) BY THE COMMANDER, ON MEASURED EVIDENCE.
   THE STRUCK WORDS ARE LEFT VISIBLE RATHER THAN DELETED so nobody re-derives
   the same dead plan from a clean page** — the same discipline used on the
   Slot 2 correction above.

   **CRYPTOPANIC NO LONGER HAS A USABLE FREE TIER.** The Commander checked and
   found it is now a paid product. Measured the same day: unauthenticated,
   `/api/v1/posts/?public=true` returns **HTTP 403** and
   `/api/developer/v2/posts/` returns **HTTP 404**. **There is no free tier to
   build against.**

   **THREE REPLACEMENTS WERE PROBED AND ALL THREE FAILED, WITH REASONS:**
   - **`cryptocurrency.cv`** (a free aggregator the Commander found) — **it
     contradicts itself.** Called four times in two minutes on the SAME
     address it answered `totalCount: 0` then `totalCount: 2750`; adding the
     innocuous parameter `lang=en` returned **zero articles under HTTP 200**.
     **A source that answers differently each time cannot be checked at all,
     and every gate on this ship works by rebuilding the printed line from a
     raw fetch and demanding an exact match.** It is also a middleman: its own
     source list is CoinDesk, The Block, Decrypt, Cointelegraph — feeds we can
     read directly.
   - **`newsapi.org`** — free tier delivers articles with a **24-hour delay**
     and its licence says it **"cannot be used in a staging or production
     environment (including internally)."** A morning brief cannot print
     day-old news, and the licence forbids the only use we have. Paid starts
     at **$449/month**.
   - **`newapi.ai`** — **not a news service at all.** It is an AI API gateway.
     Name collision only.

   **THE ADOPTED SOURCE: THE PUBLISHERS' OWN PUBLIC FEEDS, READ DIRECTLY.**
   Measured working 2026-07-31: **CoinDesk 25 items** (newest 3 minutes old),
   **Cointelegraph 30 items**, **Decrypt** and **Bitcoin Magazine** both
   answering. **No account, no key, no signup, no expiry.** Parsed with
   `xml.etree.ElementTree` from the standard library — **NO new dependency.**

   **AND THE STRUCTURAL REASON, WHICH IS WHY THIS IS NOT MERELY "THE FREE
   OPTION":** a news API exists to be sold, so its fresh, usable data will
   always end up behind a payment — that is its business model and CryptoPanic
   is the proof. **A publisher's feed exists to be spread as widely as
   possible, because that is how the publisher gets readers.** The incentive
   points the other way and does not change.

   **DECIDED WITH IT, 2026-07-31 (evening):**
   - **Sources: CoinDesk, Cointelegraph, Decrypt, The Block, Blockworks.**
     Five, different owners. **NOT one hundred.** Beyond a handful, extra
     sources return THE SAME STORY reworded, which adds no information and
     **actively corrupts any future headline COUNT** — one ordinary story
     covered by fifty outlets would read as a storm.
   - **Print three headlines plus the count** of stories in the last N hours.
   - **CRYPTO NEWS ONLY.** Macro is already scheduled elsewhere and better:
     instrument 4 is the event calendar (FOMC, CPI) and the research file
     names macro risk-on/off as **DXY and NASDAQ correlation — NUMBERS.**
     **Numbers for the machine, headlines for the Commander.** Turning a
     sentence into a number is where a system starts inventing things.
   - **UNSCHEDULED SHOCKS — war, an equity crash — ARE ALREADY COVERED AND NOT
     BY NEWS.** The regime vane prints `Weather: Chaotic` from PRICE, and
     price moves in seconds where a headline arrives minutes later. The
     research file already ruled speed-based news trading **"unwinnable for
     retail."**
   - **NEWS IS NEVER A SIGNAL AND CANNOT BECOME ONE.** Phase 6's three slots
     are locked BY NAME — Turtle/Donchian, funding-rate fade, on-chain cycle
     thermometer. **None is news, and changing them after the fact is
     cheating.** The README's "news-storm flag" is **vision, not a scheduled
     step**, and any session that finds itself building a signal out of
     headlines has misread this page.
   - **SUBSCRIBING LATER COSTS NOTHING EXTRA.** Law 2 seals each source inside
     its own compartment, so a paid feed could be swapped in an afternoon if
     the free one ever proves genuinely clumsy in real use. **Start free
     because it is reversible**, not because free is a virtue.
4. Event calendar (manual JSON file the Commander can edit + known recurring
   events: FOMC, CPI dates).
5. WHALE WATCH (the Commander's requested gap-closer): what the big money is
   doing, from FREE sources only — pick at build time from: exchange
   netflow/large-transaction data (free tiers of blockchain explorer APIs),
   Bitcoin exchange reserve trends, and the funding+open-interest combination
   (crowd positioning) already collected in #2. Plain-words line on the Brief
   ("large holders moved ~X BTC to exchanges this week — historically
   selling-side behavior"). INFORMATION ONLY. True wallet-by-wallet whale
   tracking is paid/unreliable; we show the honest free footprint, not a
   fake x-ray. IF no free source proves reliable at build time → the
   instrument reports "whale watch: no honest free source available" rather
   than showing garbage — and the Commander decides if it's worth paying for.
GATE per instrument: appears on the Brief with live data; unplugging the
internet (or a bad key) degrades to "offline" without breaking the Brief.
- IF a free API dies or paywalls → mark instrument offline, log it, move on.
  NEVER substitute a paid API without the Commander's yes.

## STANDING REQUIREMENT — **`cockpit/brief.py` MUST HAVE ITS OWN GATE BEFORE THE SHIP IS USED FOR REAL**

**Commander's decision, 2026-07-28 (night): NOT NOW. Before going live.**

Every instrument the Brief prints is guarded to the byte. **The file that
assembles them onto the screen is checked by nothing.** That is a real gap and it
is recorded here so it cannot be forgotten.

**It is deliberately NOT built yet**, and the reason is written down so waiting is
never mistaken for forgetting: **`brief.py` changes shape every time an instrument
is added.** A gate written today would be rewritten after Steps 3.3, 3.4 and 3.5,
and every rewrite is a chance to quietly weaken it — which is the one mistake this
ship has already been convicted of (R-001).

**THE DEADLINE: it must exist before the Brief is relied on for real decisions,
and in any case before Phase 6 seals the signal slots.** No session may mark this
done by reading the file and declaring it fine.

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
- Slot 2: Funding-rate extreme fade. ~~(needs funding history collected since
  Phase 3/4 — start recording funding to CSV the day Phase 3.2 ships)~~
  **CORRECTED 2026-07-26 — the struck text was never true and was written from
  assumption:** Binance serves settled funding history back to contract
  inception, free and keyless (BTC 2019-09-10, ETH 2019-11-27, SOL 2020-09-13;
  paginate `startTime` + `limit=1000`). **No collection is required and this
  slot can be tested whenever we choose.** The struck words are left visible
  rather than deleted so nobody re-derives the same wrong plan from a clean
  page. Measured probe and full account in PROGRESS_LOG.md, 2026-07-26.
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
- SELF-JUDGMENT (the Commander's requirement — the system must say "I was
  wrong, and HERE is where"): extend the grader into
  `journal/signal_report.py`, run automatically every week:
  1. Every closed signal graded WIN (hit TP) / LOSS (hit SL) / EXPIRED, with
     honest P&L after costs.
  2. The CONFESSION section — automatic, no mercy: worst 3 signals of the
     period listed with date, what it said, what happened, money lost;
     accuracy broken down by asset, by regime at signal time, and by
     day-of-week. This is where patterns of failure become visible.
  3. PROMISE vs REALITY line: live profit factor vs the profit factor this
     strategy showed in the gauntlet ("promised PF 1.3, delivering 0.9").
  All of it lands on the Brief and in the log; nothing is hidden when the
  news is bad — bad weeks are printed exactly like good weeks.
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
## THE LEARNING LOOP (how the system teaches itself — the safe way)

The Commander asked: "can it teach itself by the results?" The honest
answer, built into this plan:

- WHAT IS AUTOMATIC (the system does alone, forever): grading every claim
  and every signal, the weekly CONFESSION report, the promise-vs-reality
  line, accuracy broken down by regime/asset/time. The system DIAGNOSES
  itself completely without help — it always knows and says where it was
  wrong. That evidence pile IS the teacher.
- WHAT NEEDS THE COMMANDER (one review session, monthly/quarterly): reading
  the diagnosis and approving any change. The session proposes ("Turtle
  loses every Chaotic-regime signal — add the regime filter?"), the
  Commander decides, and the changed strategy goes BACK THROUGH THE LAB as
  a new fingerprint with a fresh track record.
- WHY IT NEVER SILENTLY RE-TUNES ITSELF: with ~50 signals a year, a machine
  that adjusts itself on results learns the noise, not the market — the
  LSTM had 26,000 examples and still memorized instead of learning; 50
  would fool itself faster. Silent self-tuning is how a system starts lying
  to its pilot. So: self-DIAGNOSIS automatic and total; self-MODIFICATION
  never without the Lab and the Commander. This is the cut-ghost law
  (recorded 2026-07-20) and it protects the one thing Zar X is built on:
  that its numbers can be trusted.

## KNOWN GAPS (honest list — so nobody pretends they don't exist)

1. Whale wallet-by-wallet tracking: only the free footprint is shown
   (Phase 3 #5); the full x-ray is paid and often unreliable anyway.
2. The human chart-eye (patterns, "feel", experience from the books):
   cannot be honestly backtested — that is the PILOT's contribution by
   design. The system gives instruments; the Commander gives judgment.
3. Black swans (war, exchange collapse, hack): no system predicts them.
   Our defenses are the 1% risk law, the event calendar, war-warnings on
   the Context Deck, and the regime vane noticing chaos AFTER it starts —
   damage control, not prophecy.
4. Signals live only in the 3 gauntlet slots (THE PROMISE). If the market
   changes so much that a retired survivor's family of ideas stops working,
   the answer is the cockpit + pilot, not a fourth slot.

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
## **>>> 2026-08-20 (afternoon): PHASE 5 IS STILL HALF BUILT AND THE MIRROR WAS NOT STARTED. R-072 WAS ATTACKED AND DID NOT SURVIVE — THREE OF SIX REAL FAULTS WALKED THROUGH GATE 5.1 WHILE IT PRINTED `PASSED — 64 checks, 0 red`. GRADED BORDERLINE. NOTHING REPAIRED, NOTHING BUILT, AWAITING THE COMMANDER'S RULING.**

**WHERE THE SHIP IS.** Every gate green, proved before anything was touched.
**Fourteen invocations, 1,013 green, ZERO cross ticks, no nonzero exit.**

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0   58 green   63 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0   71 green  122 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0   88 green   59 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0   88 green   56 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0   OK/FAIL     5 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0   54 green    6 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0   69 green    1 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0   69 green    1 s
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  107 green    8 s
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  107 green    7 s
    cockpit/carry.py            GATE 4.1      PASSED  exit 0   87 green    5 s
      the same file at TZ=UTC0  GATE 4.1      PASSED  exit 0   87 green    3 s
    journal/log_trade.py        GATE 5.1      PASSED  exit 0   64 green    2 s
      the same file at TZ=UTC0  GATE 5.1      PASSED  exit 0   64 green    1 s
    vault INTACT 6 of 6 · Brief 3/3 · lab/ untouched
    journal/my_trades.csv DOES NOT EXIST — his first real trade creates it

**>>> WHAT IS BROKEN, STATED AS THE MARKER MUST STATE IT.**

**1. GATE 5.1 NEVER ONCE DRIVES THE DOORWAY THE WAY THE SHELL DRIVES IT.** The
only real caller is `log_trade(*answers)` — **no `path`, no `now`.** Every one
of the 64 checks injects both, or inspects only the first eight characters of
the return. **So `TRADES_FILE` and `datetime.now(timezone.utc)` — the two
values the production path resolves from the module's own constants — are
judged by nothing.** Proved by three text-edit faults that each left the gate
printing `PASSED — 64 checks, 0 red`: the real clock relabelled UTC instead of
converted (**every row five hours wrong, wearing a `+00:00` that says it is
not**), the archive moved to another filename (B14's shape), and the real clock
frozen at 2020. **The drill owns T10, a sabotage for precisely this fault,
reports it CAUGHT, and still cannot see it — T10 replaces `_stamp` wholesale
and never reaches the edited branch.**

**THE SHIPPED FILE IS CORRECT TODAY AND THAT WAS MEASURED, NOT ASSUMED:** the
control's stamp offset from true UTC is **+0.00 hours** and `TRADES_FILE` is
`my_trades.csv`. **This is a hole in the gate, not a fault in the file — it is
ONE mistake away from being a fault in the file, and R-074 is a session with
its hands on that exact line.** Graded **BORDERLINE**; not repaired; his ruling.

**2. `cockpit/whales.py`'s `_get` HANGS FOREVER IF ITS TIMEOUT IS EVER LOST,
AND GATE 3.5-R1 CANNOT SEE THAT EITHER.** R-077. Against a server that accepts
and never replies: the control returns `ReadTimeout` in 4.03 s, the broken one
never returns; **both gates print `PASSED — 107 checks, 0 red`.** **MEASURED:
all seventeen `requests.get` calls on the ship outside `lab/` and `vendor/`
carry a timeout today**, so this too is a gate hole and not a live fault.

**3. `journal/mirror.py` DOES NOT EXIST.** Phase 5's second half is unstarted.
The plan's own sentence for Phase 5 — *"log 2 fake trades, RUN MIRROR, numbers
check out by hand"* — is still half unmet, and GATE 5.1 says so in its own pass
text rather than in a footnote.

**4. R-066 IS OPEN WITH FOUR OF ITS FIVE DOUBTS UNTESTED.** It is **no longer
un-attacked** — doubt 2 was attacked this session and was right. Doubts 1, 3, 4
and 5 are untouched by anybody.

**5. THE CATEGORY B PILE IS FORTY-FOUR**, cleared before the ship is used for
real, at the same moment `cockpit/brief.py` gets its gate.

**A NOTE ON THE TIMINGS ABOVE:** `cockpit/carry.py --gate` took 5 s against
~35 s on record, and `fear_greed` took 63 s against ~40 s. **A gate timing is a
weather report, not a check. Never conclude a check was skipped because a gate
was fast — read its output.**

## **>>> 2026-08-20 (morning): PHASE 5 IS HALF BUILT. `journal/log_trade.py` SHIPPED UNDER GATE 5.1 — 64 CHECKS, 0 RED, TWICE, AND CERTIFIED BY ATTACK. R-067 IS CLEARED BY A SESSION THAT DID NOT BUILD `cockpit/carry.py`.**

**WHERE THE SHIP IS.** Every gate green, proved before anything was touched.

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red   ~66 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~125 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red   ~55 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red   ~57 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red    ~7 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red    ~6 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red   ~0.6 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red   ~1.3 s
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red    ~8 s
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red    ~7 s
    cockpit/carry.py            GATE 4.1      PASSED  exit 0  0 red    ~4 s
      the same file at TZ=UTC0  GATE 4.1      PASSED  exit 0  0 red    ~3 s
    journal/log_trade.py        GATE 5.1      PASSED  exit 0  0 red    ~2 s
      the same file at TZ=UTC0  GATE 5.1      PASSED  exit 0  0 red    ~2 s
                                64 checks, TWELVE sabotages, none INERT,
                                tick sequences identical BY MACHINE
    885 green across the twelve arrival invocations · vault INTACT 6 of 6
    Brief 3/3 · lab/ untouched · journal/my_trades.csv DOES NOT YET EXIST

**THE GATE TIMINGS ABOVE ARE TODAY'S AND THEY ARE NOT THE ORDERS' FIGURES.**
`cockpit/carry.py --gate` took 4 s, not the ~35 s on record — the live
cross-check ran with today's real money in it. **A gate timing is a weather
report, not a check. Never conclude anything from one.**

**Production half of `journal/log_trade.py`: lines 1-286, sha256
`652378043e01b8e4`** (prefix before `__main__`, CRLF, NO trailing separator).

**WHAT IS BROKEN OR UNPROVEN, STATED AS THE MARKER MUST STATE IT:**

- **R-072: NOBODY BUT ITS AUTHOR HAS LOOKED AT `journal/log_trade.py`.** The
  next session's Job 1 is to attack it. **No exemption was held or granted.**
- **R-066 IS STILL OPEN AND STILL UN-ATTACKED, NOW FOR THREE GENERATIONS.**
  One mind found R-060, graded it and repaired it. **A deferral is not a
  resolution and it must not fade.**
- **R-070: NO GATE ON THIS SHIP KNOWS HOW MANY CHECKS IT SHOULD RUN.** Proved
  today by deleting five checks from GATE 4.1 and watching it print
  `PASSED — 82 checks, 0 red` while its banner claimed all twenty-one had run.
  **`journal/log_trade.py` shipped with the one-line repair; the other seven
  gates do not have it.**
- **R-071: `cockpit/carry.py`'s `_window_end` promise is unreachable by any
  check** in GATE 4.1's 87. The production file is right; the gate is blind.
- **THE SEVEN INTERACTIVE QUESTIONS IN `journal/log_trade.py` ARE TESTED BY
  NOBODY.** D1 says a prompt is beyond a gate's reach, which is true and which
  means **the ORDER of the seven `input()` calls is checked by nothing.** It
  was driven once by hand and its output read. That is all the evidence there
  is.
- **`journal/mirror.py` DOES NOT EXIST.** Phase 5 is half built, and condition
  10 of GATE 5.1 could only be half met because of it — said out loud in the
  check's own text, not softened.
- **THE CATEGORY B PILE IS FORTY-TWO**, cleared before the ship is used for
  real, at the same moment `cockpit/brief.py` finally gets its gate.
- **THE PREFIX-HASH RECIPE IN THE ORDERS WAS WRONG FOR SIX OF THE SEVEN FILES
  IT LISTED.** Measured and corrected today. **A hash whose recipe nobody can
  reproduce is a number, not a proof** — `git status` and a content comparison
  against HEAD are what the confinement actually stands on.

---

### THE MARKER THIS REPLACED, KEPT FOR THE RECORD

## **>>> 2026-08-19 (morning): PHASE 4 IS COMPLETE. `cockpit/carry.py` SHIPPED UNDER GATE 4.1 — 87 CHECKS, 0 RED, TWICE, AND CERTIFIED BY ATTACK. THE EXEMPTION IS SPENT.**

**WHERE THE SHIP IS.** Every gate green. The Morning Brief now carries the five
Context Deck instruments **and, below them, the Carry Monitor** — its own
instrument, not a sixth context line.

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red   ~68 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~122 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red   ~51 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red   ~50 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red    ~5 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red    ~4 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red   ~0.4 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red   ~0.2 s
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red    ~7 s
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red    ~7 s
    cockpit/carry.py            GATE 4.1      PASSED  exit 0  0 red   ~35 s
      the same file at TZ=UTC0  GATE 4.1      PASSED  exit 0  0 red   ~35 s
                                87 checks, TWENTY-ONE sabotages, all CAUGHT,
                                none INERT, tick sequences identical
    vault INTACT 6 of 6 · Brief 3/3 · lab/ untouched

**Production half of `cockpit/carry.py`: lines 1-415, sha256 `ec5455596007b590`.**

**WHAT IS BROKEN OR UNPROVEN, STATED AS THE MARKER MUST STATE IT:**

- **R-067: NOBODY BUT THE AUTHOR HAS LOOKED AT `cockpit/carry.py`.** The
  Commander's exemption removed the LAST session's check, not this one's. **The
  next session's Job 1 is to attack it, and the exemption is spent** — *"and so
  on"* are his words.
- **R-066 IS STILL OPEN AND STILL UN-ATTACKED.** One mind found R-060, graded it
  and repaired it. Two generations have now passed without a second pair of eyes
  on it. **A deferral is not a resolution and it must not fade.**
- **R-069: THE LIVE CHECK IN GATE 4.1 CAN GO RED THROUGH NO FAULT OF THE FILE**
  if a funding settlement (00:00, 08:00, 16:00 UTC) lands between the module's
  fetch and the gate's own. It is R-021's shape and it was a deliberate choice:
  the alternative was weakening the only exact, no-tolerance live check on this
  ship.
- **THE BRIEF WENT 2/3 FOR THE SECOND TIME**, on the first run after wiring, and
  3/3 on the two runs after it. **It is not the Carry Monitor** — the four added
  lines run after the asset count is computed. **Item 11 on his desk, the
  TwelveData key rotation, is the first suspect and it is now twice.**
- **THE CATEGORY B PILE IS THIRTY-SEVEN.** Nothing was cleared this session, by
  anybody.

**WHAT PHASE 4 DELIBERATELY DID NOT DO.** No Lab gate, no recorder, no CSV, no
archive — `EXECUTION_PLAN.md` is explicit that this is a readout. **It can never
occupy one of Phase 6's three slots, which are locked BY NAME: Turtle/Donchian,
funding-rate fade, on-chain cycle thermometer.**

**AND THE ONE THAT DOES NOT EXPIRE:** at Phase 6 the "separation in time"
substitute for Fable EXPIRES. A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. It is R-006, no
in-house session may clear it, **and it is certainly not waived by an exemption
granted for one build session.**

**NEXT: PHASE 5 — THE TRADE LOGGER & MIRROR** (`journal/log_trade.py`), after
the next session has attacked what this one built.

---

## **>>> 2026-08-18 (night): PHASE 3 IS CLOSED. THE SHIP MOVES TO PHASE 4 — THE CARRY MONITOR. GATE 4.1 IS DECLARED AND COMMITTED WITH NO CODE, AND THE COMMANDER HAS GRANTED HIS SECOND EXEMPTION EVER.**

**WHERE THE SHIP IS.** Unchanged since the repair earlier today. Every gate
green; `cockpit/whales.py` carries GATE 3.5-R1 at 107 checks, 0 red, twice.
**Nothing was built in this part of the session and nothing was measured.**

**THE RULING, VERBATIM, BECAUSE ONLY HE CAN GRANT ONE AND ONLY IN WORDS:**

> *"OK SO WRITE NEXT SESSION ORDER AND ITS THE ONY EXEMPTION FOR NEXT SESSION IT
> WILL NOT ATTACK YOUR FIX AND IT BUILDS THE NEXT SESSION AND IN NEXT SESSION
> ORDER AFTER BUILD IT WOULD BE SAME THAT NEXT SESSION WILL ATTACK THE BUILD AND
> SO ON"*

**THE TWENTY-THIRD GENERATION DOES NOT DO PART 1. IT BUILDS
`cockpit/carry.py`.** The exemption is one session, one thing, and **it dies
with that session** — *"and so on"* are his words, and the rhythm resumes with
the generation after it.

**GATE 4.1 IS DECLARED** in `PROGRESS_LOG.md` under 2026-08-18 (night):
**five design decisions and fourteen conditions, committed with no `.py` file**,
by a session that will not build the thing. That is the shape GATE 3.5 had, and
GATE 3.5 is the bar that survived attack best.

**THE PLAN'S OWN ONE-LINE GATE FOR PHASE 4 HAS BEEN SUPERSEDED, AND IT IS SAID
OUT LOUD RATHER THAN DONE QUIETLY.** `EXECUTION_PLAN.md` line 279 says only
*"readout matches the exchange's own displayed funding within rounding"*. That
is far below what the last four instruments were held to, so it now lives inside
condition 3 of a fourteen-condition bar. **The plan's sentence was not deleted
and was not weakened — it was absorbed.**

**WHAT IS BROKEN OR UNPROVEN, STATED AS THE MARKER MUST STATE IT:**

- **R-066 IS OPEN AND UN-ATTACKED, BY HIS RULING.** One mind found R-060, graded
  it and repaired it. **A deferral is not a resolution**, and the sentence
  "R-066 is still un-attacked" is carried in the orders so it cannot fade.
- **THE CARRY MONITOR IS THE MOST DANGEROUS LINE THIS SHIP HAS EVER PRINTED, AND
  NOT FOR A TECHNICAL REASON.** Everything on the Brief so far describes: a
  price, a mood, a headline. This one prints a percent-a-year figure that reads
  like an opportunity. **The caveats are mandatory and verbatim in the gate, the
  three assets may never be sorted by which pays most, and whether the whole
  line still reads as information is the COMMANDER'S judgement, not a
  session's.**
- **THE SIGN IS THE TECHNICAL RISK.** Positive funding means longs pay shorts,
  and the carry is short the perp, so positive funding EARNS. **Printing "pays
  11%" when it costs 11% is the worst thing this instrument can do**, which is
  why condition 4 requires the sign proved against an independent Binance
  surface.
- **A SINGLE FUNDING PRINT MAY NOT BE ANNUALISED** — one 8-hour reading of 0.05%
  becomes 54% a year on paper. **The readout averages settled rates over a
  stated window and names the window on the line.**
- **THE CATEGORY B PILE IS THIRTY-FIVE.**

---

## **>>> 2026-08-18 (later): THE COMMANDER RULED ON R-060 AND THE REPAIR IS BUILT. GATE 3.5-R1 PASSED — 107 CHECKS, 0 RED, TWICE. THE ATTACK THAT BEAT THE OLD GATE THIS MORNING NOW TURNS IT RED.**

**WHERE THE SHIP IS.** Every gate green. `cockpit/whales.py` is the only file
that changed, and **only below its `__main__` line**:

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~63 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~124 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  (x2, TZ=UTC0)
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~7 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~6 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  (x2, TZ=UTC0)
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red  107 checks
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red  107 checks
                                17 sabotages, all CAUGHT · 6.9 s / 8.4 s
    vault INTACT 6 of 6 · lab/ untouched
    Brief 3/3, FIVE Context Deck lines — but 2/3 on the run before it,
    a TwelveData read timeout on BTC that cleared on a re-run. Recorded.

**WHAT WAS DONE.** The gate now stands up an HTTP server of its own on
`127.0.0.1` and makes the REAL `_get` — the four lines that are the only code on
this ship that actually speaks to Binance — walk to it over a real socket. It
judges **both halves**: what was asked for, read off the wire and compared to six
tuples typed out in the gate, and what came back, held to the same block the fake
transport must produce. **No Binance request is made by the new check.** Three
permanent sabotages ride on it forever — W15, W16 and the one that was INERT this
morning, W17, now provable because the gate's own server answers an unrecognised
request with HTTP 500.

**WHAT CERTIFIES IT.** Not the drill it ships with — **the attack that beat the
old gate.** X15, X16 and X17 were re-applied as REAL TEXT EDITS to a copy outside
the repo, after the repaired control passed first: **exit 1 with 4, 3 and 2 red.
This morning all three walked through `100 checks, 0 red`.**

**WHAT IS STILL BROKEN OR UNPROVEN, STATED AS THE MARKER MUST STATE IT:**

- **R-060 IS REPAIRED BUT NOT CLOSED, AND ITS AUTHOR MAY NOT CLOSE IT.** One
  session found it, graded it and fixed it. **R-066 is filed against the repair
  and stays OPEN.**
- **THE NEW CHECK PROVES THE TRIP TO A SERVER THAT IS NOT BINANCE.** Redirects,
  gzip, a 429 with `Retry-After`, a reset mid-body — none of that is tested. The
  live check still verifies one number of six.
- **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED.** Nobody has timed Binance's
  bucket updates or sampled how far the BTC figure moves between two calls.
- **THE CATEGORY B PILE IS THIRTY-FIVE** — R-061 to R-065, none repaired, none
  cleared.
- **THIS GATE NOW BINDS A PORT.** Nobody has run it behind a firewall, with a
  proxy really configured, or twice at the same moment.
- **A REAL FAIL-SAFE EVENT HAPPENED BY ACCIDENT AND IS RECORDED.** On the first
  Brief run after the repair, BTC's price data went offline — TwelveData timed
  out, the Yahoo fallback returned a `JSONDecodeError` — and the Brief printed
  **2/3** with the dead asset NAMED while ETH, SOL and all five deck lines
  carried on. **An immediate re-run was 3/3.** A transient, not this repair
  (the production half was never touched, and the whale watch read `6 of 6` on
  the failing run too). **Written down rather than quietly re-run away.**

**WHERE THE NEXT SESSION STANDS.** Phase 3's five instruments are complete and
there is no sixth. **Its Job 1 is to attack this repair** — a fresh pair of eyes
on `__main__` of `cockpit/whales.py`, and the fourth fault in `_get` that its
author was blind to.

---

## **>>> 2026-08-18: THE WHALE WATCH WAS ATTACKED BY A SESSION THAT DID NOT BUILD IT, AND IT DID NOT SURVIVE CLEAN. ONE BORDERLINE FINDING IS ON THE COMMANDER'S DESK. NOTHING WAS REPAIRED AND NOTHING WAS BUILT.**

**WHERE THE SHIP IS.** Unchanged in code — **not one byte of any `.py` file was
altered.** Every gate still green, all ten invocations run before anything was
touched:

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  (x2, TZ=UTC0)
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  (x2, TZ=UTC0)
    cockpit/whales.py           GATE 3.5      PASSED  exit 0  0 red  100 checks (x2)
    vault INTACT 6 of 6 · Brief 3/3, FIVE Context Deck lines · lab/ untouched

**WHAT IS BROKEN, STATED AS THE MARKER MUST STATE IT.** Nothing in the shipped
code is producing a wrong number today. **What is broken is a gate's reach:**
GATE 3.5 cannot see a fault in `_get`, the four-line function that is the only
code on this ship that actually speaks to Binance. Two sabotages inside it —
hardcoding the symbol, and asking the top endpoint for both populations — each
put wrong numbers on the Commander's Brief while the gate reported
**`100 checks, 0 red`**. That is **R-060, BORDERLINE, awaiting his ruling.**
It is NOT repaired: THE_PATTERN says a BORDERLINE finding is reported and the
Commander decides.

**FOUR SMALLER THINGS were measured and filed CATEGORY B** — the header built
outside the per-reading guard (R-061), a timestamp tie broken by position while
the docstring denies it (R-062), the one-way staleness guard (R-063), and
R-058's doubt 2 settled against its author: the no-shorts case CAN misreport
(R-064). **One item is filed against this session's own work (R-065).**

**R-058 IS ANSWERED, NOT CLEARED.** The independent attack happened; its doubts
3, 4 and 6 are untouched and doubt 6 is the Commander's alone.

**THE CATEGORY B PILE IS THIRTY-FIVE.**

**WHERE THE NEXT SESSION STANDS.** Phase 3's five instruments are complete and
there is no sixth to build. **The next session's Job 1 is R-060's ruling if the
Commander has given one**, and its Job 2 is what has been on his desk for three
generations. **The plan has not advanced a step and should not pretend it has.**

---

## **>>> 2026-08-11 (night): PHASE 3'S CONTEXT DECK IS COMPLETE. FIVE INSTRUMENTS OF FIVE. GATE 3.5 PASSED 100/100 TWICE.**

**WHERE THE SHIP IS — CHANGED, FOR THE FIRST TIME TODAY.** `cockpit/whales.py`
exists and is on the Morning Brief. Every gate on this ship is green:

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  (x2, TZ=UTC0)
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  (x2, TZ=UTC0)
    cockpit/whales.py           GATE 3.5      PASSED  exit 0  0 red  100 checks (x2)
    vault INTACT 6 of 6 · Brief 3/3, FIVE Context Deck lines · lab/ untouched

**WHAT IS DONE:** Phase 3 Step 3.5, the whale watch, instrument 5 of 5. Two
Binance endpoints side by side for BTC/ETH/SOL — its largest accounts by
position size, beside every account on the venue. **Exchange reserve and netflow
data is PAID and therefore out, and the line on the Brief says so in the
Commander's sight: NOT exchange flows, NOT wallet tracking, NOT the world's
whales.**

**WHAT IS NOT DONE, AND IT IS THE IMPORTANT ONE. NOBODY BUT ITS AUTHOR HAS EVER
LOOKED AT `cockpit/whales.py`.** One hundred checks and fourteen sabotages, all
written by the session that wrote the code. **That is R-058, and the next
session's JOB 1 is to attack it.** The Commander exempted the twenty-first
generation from Part 1 and closed the hole himself in the same breath: *"in next
session when he write session orders and well after others too every time new
session has to attack the build of previous session."* **The exemption died with
that session and no session may renew one.**

**WHAT WENT WRONG, RECORDED HERE AND NOT ONLY IN THE LOG:**

1. **A FALSE CLAIM ABOUT FLOATING-POINT ARITHMETIC** was written into the file's
   docstring, its gate's prose and a COMMITTED log entry. The gate caught it on
   its first run — 1 red of 100 — **only because it had been written as a check
   rather than as a sentence.** Corrected by enumeration: 501 of 10,001
   four-decimal shares really do disagree between the two rounding routes, and
   `0.6085` is not one of them while `0.5525` is. **R-059 is the residue: the
   rest of the prose in that file has never been run.**
2. **THE SHIP-ALIVE COUNTER WOULD HAVE SCORED A REAL FAILURE AS ZERO RED**
   (R-057) because `data/collection_guard.py` prints `OK`/`FAIL` rather than
   tick marks. Found by noticing a suspicious timing, not by any check.
3. **TWO CORRECTIONS TO THE RECORDED HASH RECIPE**, both measured: the orders'
   label *"with the trailing CRLF"* is wrong — the recorded numbers come from
   the prefix WITHOUT the anchor — and `data/open_interest.py` cannot be hashed
   that way at all, because the anchor string appears TWICE in it.

**THE CATEGORY B PILE IS THIRTY.** Nothing was cleared this session and the
reason is written into the queue: the only item within reach, R-056, is one the
builder benefits from clearing.

**WHERE THE SHIP GOES NEXT.** Phase 3's five instruments are built. **The next
session attacks the whale watch — that is its whole first job — and only then
looks at what Phase 3 has left**, which is the Commander's decisions rather than
new code: R-049 (deferred three times), the `data/events.json` timezone, the two
publisher names, and the Category B pile that is cleared when `cockpit/brief.py`
finally gets its own gate before the ship is used for real.

**THE MARKERS BEFORE THIS ONE ARE KEPT BELOW FOR THE RECORD.**


## **>>> 2026-08-11 (evening, second ruling): THE NEXT SESSION HAS ONE JOB — BUILD INSTRUMENT 5 OF 5. PART 1 IS EXEMPTED BY THE COMMANDER HIMSELF.**

**HIS WORDS, VERBATIM:** *"we are only making exemption for next session to not
attack your check and i think there is nothing to attack for next session what
have you done."*

**WHERE THE SHIP IS: unchanged. Every gate green, vault INTACT, Brief 3/3 with
four Context Deck lines, and no `.py` file modified on 2026-08-11 at all.** This
marker records a second DECISION, not a change to the ship.

**WHAT IS DECIDED:**

1. **THE NEXT SESSION DOES NOT ATTACK ANYTHING.** He was right about the half he
   observed — **the twentieth generation shipped no code, so there is nothing of
   its to break.** He judged the other half, R-049, and set it aside.
2. **R-049 IS DEFERRED FOR THE THIRD TIME.** He was told the cost first: a
   self-marked repair, touching all six fields of every story, running on every
   headline he reads. **The measurement that supports him is real — 136 real
   headlines, not one carrying markup, so the bug has never once fired.**
3. **THE NEXT SESSION'S WHOLE JOB IS THE WHALE WATCH UNDER GATE 3.5.** Finishing
   it makes the Context Deck five of five and closes Phase 3's instruments.

**THE EXEMPTION'S EDGES, BECAUSE AN EXEMPTION NOBODY BOUNDED IS AN EXEMPTION
SOMEBODY WILL WIDEN:** it covers attacking the last session's work and R-049.
**It does NOT cover proving the ship alive first, it does NOT cover the sabotage
drill inside what gets built, and it does NOT loosen one condition of GATE
3.5** — conditions 11 and 12 were written because of R-054 and stand exactly as
written. **IT DIES WITH THAT SESSION.**

**AND THE NUMBER, SAID OUT LOUD AS THE STANDING DUTY REQUIRES: THIS IS THE FIFTH
REDUCTION OF PART 1** — 2026-07-31, 2026-08-03 twice, 2026-08-05, now. **The
streak was broken in between: the twentieth generation ran Part 1 in full and
found three sabotages walking through a green gate in a morning. That is what
the outside check is for, and it is the only thing on this ship that has ever
caught what a builder could not see.**

**THE MARKERS BEFORE THIS ONE ARE KEPT BELOW FOR THE RECORD.**

## **>>> 2026-08-11 (evening): THE COMMANDER RULED R-054 SMALL. NOTHING IS BLOCKING THE BUILD. THE NEXT SESSION MAKES THE CONTEXT DECK FIVE OF FIVE.**

**HIS WORDS, VERBATIM:** *"OK MAKE IT IN SMALL CATEGORY AND I THINK SESSION WILL
BUILT THE NEXT STEP. UPDATE ALL THE MAIN FILES LIKE EXECUTION , PROGRESS, ETC."*

**WHERE THE SHIP IS: exactly where the marker below it says.** Every gate green,
vault INTACT, Brief 3/3 with four Context Deck lines, **no `.py` file modified
on 2026-08-11 at all.** This marker records a DECISION, not a change to the
ship.

**WHAT IS DECIDED THAT WAS OPEN THIS MORNING:**

1. **R-054 IS SMALL.** The three sabotages that walked through GATE 3.4 are a
   known, recorded, **unrepaired** weakness in the test. **Filed as CATEGORY B,
   not cleared, and no session may clear it.** He was shown the argument for
   SERIOUS as well and chose SMALL knowing both.
2. **NOTHING IS ON HIS DESK THAT BLOCKS ANYTHING.** The only item that did is
   this one, and it is ruled.
3. **THE NEXT SESSION IS EXPECTED TO BUILD INSTRUMENT 5 OF 5 — THE WHALE
   WATCH — UNDER GATE 3.5**, which was declared and committed alone this
   morning by a session that will never build it.

**AND THE ONE THING THAT MUST NOT BE READ INTO IT: THIS IS NOT AN EXEMPTION FROM
PART 1.** When the Commander exempts a session he says so in words — *"i exempt
only this for next session"* was the last one, on 2026-08-05. **He did not use
those words here.** Part 1 stands, uncapped: attack `cockpit/news.py`'s X1
repair (R-049), then build. **What changed is the priority, not the duty.**

**THE PRECEDENT HIS RULING SETS:** a gap in a TEST, where the shipped output is
proved correct, is SMALL and does not stop a build. **It says nothing about a
fault that makes the Brief wrong today — that is still SERIOUS and still stops
everything.** And it does not loosen GATE 3.5: conditions 11 and 12 were written
because of R-054 and stand exactly as written.

**THE MORNING'S MARKER, AND EVERY MARKER BEFORE IT, IS KEPT BELOW FOR THE
RECORD.**

## **>>> 2026-08-11: THE EVENT CALENDAR WAS ATTACKED BY A SESSION THAT DID NOT BUILD IT. ITS OUTPUT IS RIGHT — PROVED THREE WAYS. ITS GATE HAS THREE BLIND SPOTS AND THREE SABOTAGES WALKED THROUGH THEM.**

**WHERE THE SHIP IS:**

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  65.6 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  124.7 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  65.5 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red  62.1 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  7.6 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  4.7 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  1.5 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red  1.3 s
    vault INTACT 6 of 6 · Brief 3/3, FOUR Context Deck lines · lab/ untouched
    data/oi_history/  the weekly laptop task ran 10-Aug and pushed.

**EVERY GATE ON THIS SHIP IS GREEN AND ALL SIX INSTRUMENTS ARE CORRECT. NOT ONE
`.py` FILE WAS MODIFIED THIS SESSION.**

**AND A CORRECTION, BECAUSE THE MEASUREMENT WINS:** the orders on record quote
the news gate at ~25 s and the events gate at ~5 s. **Measured today: 4.7 s and
1.5 s.** Both faster, so nothing is wrong — but the figures were wrong and a
session seeing a 1.5 s run should not go looking for a fault that is not there.

**WHAT IS TRUE THAT WAS NOT TRUE YESTERDAY:**

1. **THE CALENDAR'S ARITHMETIC IS PROVED, NOT ASSERTED (R-050 CLEARED).** Every
   daylight-saving-dependent string in GATE 3.4 was reproduced by hand from US
   DST law and a day-of-year weekday count, **without `zoneinfo` and without
   running this ship's code.** All of it matches. The gate and the module are
   not agreeing about something false; they are both right.
2. **SOMEBODY ASKED A SOURCE WHETHER IT WAS STILL SAYING THE SAME THING — FOR
   THE FIRST TIME ON THIS SHIP.** All sixteen dates re-read off
   `federalreserve.gov` and `bls.gov` on 2026-08-11. **Not one has moved**, the
   Fed's tentative note is unchanged, and the BLS schedule still stops dead at
   10 Dec 2026. `bls.gov` still answers HTTP 403 to a non-browser fetch.
3. **GATE 3.4 WAS RUN AND ATTACKED BY SOMEONE OTHER THAN ITS AUTHOR (R-052
   CLEARED).** Four new sabotages, in a copy of the whole repo outside the repo.
4. **THE WHALE WATCH'S SOURCES ARE MEASURED RATHER THAN GUESSED.** Nine
   endpoints probed, numbers in `ROADMAP.md`. **The exchange-flow data the plan
   asks for most directly is paid; the free honest footprint is Binance's own
   top-trader positioning, keyless, 5 minutes fresh.**
5. **GATE 3.5 IS DECLARED — BY A SESSION THAT WILL NOT BUILD IT.** Committed
   alone with no `.py`. **The builder cannot lower a bar set by somebody with
   nothing to gain from where it sits**, which is what Layer 1 was always
   supposed to mean.

**WHAT IS BROKEN OR UNPROVEN, STATED HERE RATHER THAN IN THE QUEUE ALONE:**

- **>>> GATE 3.4 CANNOT SAY NO AT ITS OWN BOUNDARY (R-054).** Twenty days of
  slack in the staleness guard, and an off-by-one in it, **both walked through a
  green gate** — because checks (b) and (c) only ever test 26 days and a year
  past the horizon, never the day it fires. And the `DEFAULT_TIME` behaviour the
  Commander is invited to rely on is **pinned as a constant and exercised by no
  check**: an event of his own moved a whole day with the gate still green.
  **Recommended SMALL; the argument for SERIOUS is written out too. HE RULES.**
- **R-051 IS MEASURED BUT NOT CLEARED.** Nothing still guards a tentative date
  MOVING. One hand check on one day is not a guard.
- **R-049 IS STILL UNVERIFIED, NOW FOR THE SECOND GENERATION RUNNING** — this
  time for want of room, not by anybody's ruling.
- **THE FIVE PLACES R-052 NAMES ARE STILL ONLY EVER LOOKED AT BY THEIR AUTHOR
  (R-055).** This session's attack deliberately went elsewhere.
- **`cockpit/brief.py` STILL HAS NO GATE**, by his own ruling: not now, before
  going live.

**WHAT THIS SESSION DID NOT DO: IT DID NOT BUILD INSTRUMENT 5.** Not because
Part 1 forbade it — Part 1 graded SMALL and allowed it — but because an
instrument to this ship's current standard would not fit honestly in what was
left, **and a half-built part is worse than no part.** What it did instead is
the step the orders put BEFORE the build: measure the sources, write the numbers
down, and declare the gate.

**THE PREVIOUS MARKER IS KEPT BELOW FOR THE RECORD.**

## **>>> 2026-08-07: THE EVENT CALENDAR IS BUILT AND GATED. THE CONTEXT DECK IS FOUR OF FIVE.**

**WHERE THE SHIP IS:**

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  54 checks
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  <- NEW
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red
                                69 checks, 12 sabotages, all CAUGHT and all
                                PROVED to change the output. None INERT.
    vault INTACT · Brief 3/3, four Context Deck lines · lab/ untouched
    data/oi_history/  3 files, 222 lines each — untouched; the recorder was
                      NOT run. Next scheduled run 10-Aug-2026 09:00.

**EVERY GATE ON THIS SHIP IS GREEN AND ALL SIX INSTRUMENTS ARE CORRECT.**

**WHAT IS TRUE THAT WAS NOT TRUE YESTERDAY:**

1. **THE BRIEF NOW SAYS WHAT IS COMING.** Sixteen scheduled events ahead, the
   next three named with the days until each and **the time on HIS clock, not
   New York's**. `data/events.json` is his own file and anything he puts in it
   joins the same line.
2. **NO DATE WAS REMEMBERED BY A MODEL.** Every one was read off the issuing
   authority's own page on 2026-08-07 — the Fed's FOMC calendar and the BLS's
   CPI schedule. **`bls.gov` answers HTTP 403 to a non-browser fetch**, the same
   edge block that killed The Block, so it was read in a real browser.
3. **THE STALENESS TRAP IS GUARDED AND IT IS NOT HYPOTHETICAL.** The BLS
   publishes about a year ahead and its schedule **stops dead at 10 Dec 2026**,
   so the built-in CPI list runs out in roughly four months. Past a list's
   published horizon the deck names THAT LIST as ENDED; nothing ahead at all is
   a loud line judged by exact equality; and **both horizons print on the Brief
   every day, so the trap is visible before it fires.**
4. **THIS IS THE THIRD FILE BUILT WITH THE SABOTAGE-PROOF RULE FROM BIRTH**, and
   it carries the FILE-DESCRIPTOR door 3 plus a fresh-interpreter check that
   `cockpit/news.py` still lacks (R-046).

**WHAT IS BROKEN OR UNPROVEN, STATED HERE RATHER THAN IN THE QUEUE ALONE:**

- **EVERY EXPECTED STRING IN GATE 3.4 WAS COMPUTED BY HAND AND ALL 69 CHECKS
  WENT GREEN ON THE FIRST RUN (R-050).** Four of them turn on United States
  daylight saving. That is either right arithmetic or a gate and a module
  agreeing about something false, and only a fresh session can tell which.
- **THE HORIZON GUARDS THE LIST RUNNING OUT, NOT A DATE CHANGING INSIDE IT
  (R-051).** Eight of the sixteen dates are marked TENTATIVE by the Fed itself.
  If one moves, the deck prints the old date with a confident countdown and
  nothing says a word. It is a hardcoded list, so it cannot even be re-read.
- **NOBODY BUT ITS AUTHOR HAS RUN GATE 3.4 OR INVENTED AN ATTACK ON IT
  (R-052).** Five specific places to start are named in the queue.
- **R-049 IS STILL UNVERIFIED** — the price of the exemption, and he was told
  before he ruled.
- **`cockpit/brief.py` STILL HAS NO GATE**, by his own ruling: not now, before
  going live. It now imports four instruments and prints four deck lines.

**WHAT THIS SESSION DID NOT DO:** **it attacked nothing.** The Commander
exempted it from PART 1 in words on 2026-08-05, for one session. **THAT
EXEMPTION DIES HERE. THE ORDERS WRITTEN BELOW IT RESTORE PART 1 IN FULL, WITH NO
CAP** — and they say out loud that PART 1 has now been reduced four times
running, which is his to know about.

**SO THE NEXT BUILD IS PHASE 3 INSTRUMENT 5 OF 5 — THE WHALE WATCH** — but
**only after the event calendar has been attacked by a session that did not
build it.**

**THE PREVIOUS MARKER IS KEPT BELOW FOR THE RECORD.**

## **>>> 2026-08-05: THE NEWS INSTRUMENT WAS ATTACKED BY A SESSION THAT DID NOT BUILD IT. IT LEAKED. THE LEAK IS REPAIRED AND THE GATE NOW BREAKS ITSELF TWELVE WAYS.**

**WHERE THE SHIP IS:**

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  (12:10 UTC)
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  first time
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  <- REPAIRED
                                54 checks (was 50), 12 sabotages (was 11),
                                all CAUGHT and all PROVED to change the output
    vault INTACT · Brief 3/3 · lab/ untouched
    data/oi_history/  3 files, 222 lines each — untouched; the recorder was
                      NOT run. Next scheduled run 10-Aug-2026 09:00.

**EVERY GATE ON THIS SHIP IS GREEN AND ALL FIVE INSTRUMENTS ARE CORRECT.**

**WHAT IS TRUE THAT WAS NOT TRUE YESTERDAY:**

1. **THE NEWS INSTRUMENT SILENTLY REWROTE PUBLISHERS' HEADLINES, AND NOW IT
   DOES NOT.** `ElementTree.findtext` returns the text before an element's
   first child and nothing after it, so a headline written
   `Bitcoin <b>crashes</b> 20% as ETF outflows accelerate` reached the Brief as
   the single word **`Bitcoin`** — no clip mark, nothing anywhere saying so,
   fifty green checks while it happened. **Repaired in `_parse` with a helper
   that reads every scrap of text in the element, applied to ALL SIX fields
   rather than only the one that was caught.**
2. **IT WAS NOT FIRING, AND THAT WAS MEASURED RATHER THAN HOPED.** 136 real
   titles read across all five shipped publishers on 2026-08-05: **none carried
   markup.** The finding was reported with the measurement that weakens it.
3. **THE BUILDER'S OWN LIST OF FIVE WEAK SPOTS DID NOT CONTAIN THE FINDING.**
   That is Layer 3 earning its place: a builder cannot invent the attack they
   are blind to, however honest their list.
4. **THE LAST INCH WAS ATTACKED FOR THE FIRST TIME AND IS CLEAN.** Nobody had
   ever checked that `brief.py` prints what `news.py` returns. It does —
   verbatim, exactly once. **"Attacked hard, found nothing" is a real result.**

**WHAT IS BROKEN OR UNPROVEN, STATED HERE RATHER THAN IN THE QUEUE ALONE:**

- **THE DEAD-FEED GUARD HAS A GAP AND IT IS FILED, NOT FIXED (R-047).** One
  story stamped in the FUTURE sorts to the front of the feed, makes the
  computed age NEGATIVE, and walks the abandoned-feed check straight past.
  Proved against its own control. **It costs the publisher COUNT and the
  `[no data:]` naming — no stale headline reaches the Brief, which is why it
  graded SMALL and was left for the Commander to rule on.**
- **`news.py`'s DOOR 3 IS STILL THE WEAKEST ON THIS SHIP (R-046), AND IT IS NOW
  PROVEN RATHER THAN SUSPECTED.** An `os.write(1, ...)` from inside the doorway
  was completely inaudible to it, while the same words through `print` were
  heard. **Graded SMALL — a deaf ear cannot itself put anything on his screen —
  and deliberately NOT cleared, because the session that would be excused by
  clearing it is the one that verified it.**
- **THE DAILY NEWS COUNT ARCHIVE IS STILL NOT BUILT.** Deferred twice now: once
  as a half-built writer, once under the stop rule. **Phase 3 step 3b.**
- **`cockpit/brief.py` STILL HAS NO GATE**, by the Commander's own ruling: not
  now, before going live. It now imports three instruments and prints three
  sections, and the inch between them and the screen is checked only by hand.

**WHAT THE COMMANDER RULED THE SAME DAY, WHICH DECIDES WHAT HAPPENS NEXT:**

1. **R-047 AND R-048 ARE SMALL.** Filed, not fixed, **not cleared.**
2. **THE NEXT SESSION IS EXEMPT FROM PART 1** and does not attack the X1
   repair. **His exemption, granted in words, for ONE session. It dies with
   that session and no session may extend it.** **The price is that R-049 goes
   unverified, and he was told so before he ruled.**
3. **STEP 3b, THE DAILY NEWS COUNT ARCHIVE, WAITS UNTIL THE WHOLE PROGRAMME IS
   COMPLETE.** His words: *"we will build news section after when all the
   programme will be completed."* **He was told once that this is the only
   deferral on the ship whose cost is permanent — the past cannot be bought
   back. He ruled. It waits.**

**SO THE NEXT BUILD IS PHASE 3 INSTRUMENT 4 OF 5 — THE EVENT CALENDAR**
(`cockpit/events.py`, NOT `calendar.py`, which would shadow a standard library
module). **The Context Deck goes to four of five.**

**THE PREVIOUS MARKER IS KEPT BELOW FOR THE RECORD.**

## **>>> 2026-08-04: THE NEWS INSTRUMENT IS BUILT AND ON THE BRIEF. THE CONTEXT DECK IS THREE OF FIVE. R-038 IS CLEAN.**

**WHERE THE SHIP IS:**

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red
    cockpit/news.py             GATE 3.3      PASSED  exit 0  0 red  <- NEW
                                50 checks, 11 sabotages, all CAUGHT and
                                all PROVED to change the output
    vault INTACT · Brief 3/3 · lab/ untouched
    data/oi_history/  3 files, 222 lines each — byte for byte what this
                      session inherited; the recorder was NOT run

**EVERY GATE ON THIS SHIP IS GREEN AND ALL FIVE INSTRUMENTS ARE CORRECT.**

**WHAT IS TRUE THAT WAS NOT TRUE YESTERDAY:**

1. **R-038 IS CLEARED AND ITS DEADLINE IS BEATEN.** 123 of 123 recovered rows,
   and 537 of 537 in-window rows, are digit for digit what Binance serves. The
   audit did not import the recorder. **This could only ever have been done
   before about 2026-09-02.**
2. **R-034 (S6) AND R-031 (B1) ARE CLEARED** by a session that did not build
   either repair. Both defects are reproduced on every run rather than
   remembered.
3. **`cockpit/news.py` EXISTS, IS GATED, AND IS ON THE COMMANDER'S BRIEF.**
   Phase 3 step 3, deferred eight times, is done.
4. **`cockpit/brief.py` GAINED EXACTLY TWO LINES** — one import, one print.
   Nothing else the pilot reads changed.

**WHAT IS BROKEN OR UNPROVEN, STATED HERE RATHER THAN IN THE QUEUE ALONE:**

- **`news.py`'s DOOR 3 IS THE WEAKEST ON THIS SHIP.** It listens at
  `sys.stdout`/`sys.stderr`, **not at the file descriptor**, and does not test a
  write deferred to a thread or an atexit handler. The other two cockpit
  instruments catch all three. **R-046, and it is the first thing in the next
  orders.**
- **THE FIVE PUBLISHERS ARE FIVE NAMES MEASURED ON ONE AFTERNOON** (R-044). Two
  of the five ORDERED sources were found unusable and replaced; one of the
  replacements I chose was itself found rate-limiting within the hour.
- **THE DAILY COUNT ARCHIVE WAS NOT BUILT** — deliberately, and said out loud.
  It is step 3b with its own gate.
- **R-035 IS LARGER THAN IT WAS.** Five more sources nobody cross-checks.

---

## **>>> PREVIOUS MARKER, KEPT FOR THE RECORD — 2026-08-03 (third): S6 AND B1 ARE REPAIRED. EVERY GATE ON THE SHIP IS GREEN, AND THE RECORDER'S IS GREEN ON TWO DIFFERENT CLOCKS.**

**WHERE THE SHIP IS:**

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  <- REPAIRED
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  <- REPAIRED
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red  <- AND HERE
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red
    vault INTACT · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 222 lines each, a1ed6729 / a077cf03 / c8d97f71
                      — byte for byte what this session inherited

**THE THIRD AND LAST OF THE INERT-SABOTAGE FAULTS IS GONE.** F10 (2026-07-31),
then S6 and B1 together (today). **All three were the same fault in three
different files: a deliberate break that could not change the output, scored
ESCAPED, turning a gate red about a lie it had never managed to tell.**

**NEITHER FAULT WAS EVER IN A NUMBER THE COMMANDER READS.** Both were faults in
an alarm, and all four instruments were proved green before either was touched.

    S6 was costing him red screens — up to one settlement in six, on his own
       laptop. That is the one he could see.
    B1 was costing him nothing on his machine, because it runs at UTC+5.
       It was blind on the CLOUD, where nobody was watching. Measured, and
       said plainly rather than dressed up as urgent.

**BOTH DEFECTS WERE REPRODUCED BEFORE THEY WERE CALLED FIXED.** S6: Binance
stubbed to answer the same rate for all three contracts — the shipped form
ESCAPED, the repaired form was CAUGHT. B1: the whole repo copied outside itself
with B1 alone reverted and run at `TZ=UTC0` — ESCAPED, gate FAILED, exit 1,
**while the reachability check printed its green tick in the same run.** Both
statements were true at once, and that is the whole of R-031.

**NOTHING THE PILOT READS CHANGED**, proved two ways: every diff hunk sits
inside `__main__` (earliest at line 1172 and 1182, against `__main__` starting
at 160 and 243), and the production half of each file hashes to what it hashed
to before — `95069d1b…` and `5347bfec…`, both recipes reproduced from the
inherited digests before any edit was made.

**GATE 3.2-R8 AND GATE 3.2b-R10 WERE DECLARED TOGETHER AND COMMITTED ALONE**,
no `.py` in the commit. **The declaration also carries a DEVIATION, written
before the code existed:** S6 could not be made to speak "using a number the
gate holds", because nothing a `CONTRACTS` payload contains decides a rate.
**The gate holds an ORDER instead.** Two alternatives were named and rejected in
writing so the Commander can overrule either.

**WHAT IS OPEN, PLAINLY.** R-042 and R-043 are filed against these two repairs
and **their author may not clear them.** R-034 and R-031 are repaired but **NOT
cleared** — that verdict belongs to the next session. **R-038's deadline is
about 2026-09-02 and this session's exception spent the run before it, so
checking those 123 rows against Binance is the next session's FIRST job.** The
Category B pile stands at **eighteen** and has never once shrunk.

**THE EXCEPTION DIED WITH THIS SESSION.** The orders written for the next one
restore PART 1 — ATTACK — then PART 2 — BUILD. **No session may grant an
exemption, including to its successor. Only the Commander can.**

---

## **>>> 2026-08-03 (second): R-037 IS REPAIRED UNDER GATE 3.2c-R1, AND THE COMMANDER HAS GRANTED THE EXCEPTION AGAIN.**

**WHERE THE SHIP IS:**

    cockpit/fear_greed.py       GATE 3.1-R7  PASSED  exit 0  0 red
    cockpit/funding.py          GATE 3.2-R7  PASSED  exit 0  0 red
    data/open_interest.py       GATE 3.2b-R9 PASSED  exit 0  0 red
    data/collection_guard.py    GATE 3.2c-R1 PASSED  exit 0  0 red   <- NEW
    vault INTACT · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 222 lines each, a1ed6729 / a077cf03 / c8d97f71

**HIS TWO RULINGS OF 2026-08-03, RECORDED THE HOUR HE MADE THEM:**

1. **R-037 IS SORTED FIRST.** Done this session, under a gate declared and
   committed alone as `3dc11e6` before any code existed.
2. **THE ONE-SESSION EXCEPTION IS GRANTED AGAIN, FOR THE NEXT SESSION ONLY:**
   **no attack, repair S6 (R-034) and B1 (R-031).** `THE_PATTERN.md` is NOT
   edited — a rule suspended twice is still a rule suspended, not a rule changed.

**WHAT THE REPAIR ACTUALLY IS, AND WHY IT IS SHAPED THIS WAY.** `CHECK_STATUS.bat`
read Windows' `LastTaskResult` and printed **`OK`** when it was 0 — **so on
3 August the one screen the Commander checks would have confirmed the failure as
a success.** The cause of Windows' `0` is unproven and now unprovable, because
the Task Scheduler event log was switched off. **Only an outcome check survives a
cause nobody has proved. So the repair stops asking the job and asks the data.**

    the recorder .......... MONTHLY -> WEEKLY (Mondays 09:00, catch-up kept).
                            One silent failure now costs NOTHING, because the
                            next run still reaches back a full 30 days.
    its log ............... its OWN file. Nothing else writes there, and the
                            gate proves that every run with both controls.
    its exit code ......... HONEST. The old batch ended on `copy` and reported
                            the copy's success; reproduced, and proved fixed.
    the status screen ..... shows the ARCHIVE's newest row and its age. The
                            word OK against a task is gone; it says `exit 0`
                            and says underneath what that is worth.

**NOTHING THE PILOT READS CHANGED** — `brief.py`, `funding.py`, `fear_greed.py`
and `open_interest.py` are byte-identical, sha256 printed before and after.

**WHAT IS STILL OPEN, PLAINLY:** the Task Scheduler event log is **still off**
(needs Administrator — one command, on his desk); the five sibling jobs **still
share one log** (R-040, their data is re-fetchable); **the contention fault could
not be reproduced on demand, so the gate asserts the SHAPE and not the race**
(R-039, and the gate says so in its own pass line); and **R-038's deadline of
about 2026-09-02 has not moved.**

---

## **>>> 2026-08-03: THE COLLECTING FAILED SILENTLY. THE INSTRUMENTS ARE CORRECT AND ALWAYS WERE.**

**WHERE THE SHIP ACTUALLY IS, INCLUDING WHAT IS BROKEN:**

    cockpit/fear_greed.py    GATE 3.1-R7  PASSED  exit 0  0 red
    cockpit/funding.py       GATE 3.2-R7  PASSED  exit 0  0 red
    data/open_interest.py    GATE 3.2b-R9 PASSED  exit 0  0 red
    vault INTACT · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 222 lines each (221 rows), sha256
                      a1ed6729bef45be6 / a077cf034bf66c26 / c8d97f7122544f70
                      window 2026-06-27T16:00:00Z → 2026-08-03T08:00:00Z

**THE 1 AUGUST ERRAND FIRED AND DID NOTHING.** Six scheduled tasks were released
together at 11:47:41 on 3 August after two days with the laptop off. **Windows
records all six as `Last Result: 0`. The log holds exactly ONE entry for that
second.** The recorder wrote no header, ran no Python, appended no rows and
committed nothing — **and reported success.** Filed as **R-037, SERIOUS, on the
Commander's desk.**

**THE DATA WAS RECOVERED IN TIME AND THAT PART IS FINISHED.** The real batch was
run by hand: **41 rows per asset appended, 221 stored, committed `5c7c54a` and
pushed.** The pre-existing rows were proved byte-identical by hashing each file's
old-length prefix. **Had nothing run before the next scheduled date of
1 September, 33 rows per asset — 99 rows — would have been gone permanently.**

**>>> THE COMMIT-AND-PUSH BRANCH HAS NOW FIRED FOR REAL, AGAINST REAL NEW ROWS,
FOR THE FIRST TIME IN THIS SHIP'S HISTORY.** It committed only
`data/oi_history`; the pathspec held.

**WHAT IS STILL BROKEN, PLAINLY:** **the mechanism is NOT repaired.** Nothing
stops this recurring at the next boot after a gap, and the next scheduled run is
1 September. **Contention is reproduced and explains the SILENCE; it does not
explain the reported SUCCESS, and the Task Scheduler operational log is disabled
so the record of 11:47:41 does not exist.** Recorded as partly unproven.

**AND WHAT WAS ORDERED AND NOT DONE: S6 (R-034) AND B1 (R-031) WERE NOT
REPAIRED.** The Commander's one-session exception was spent on a session that
did not use it. **Whether it carries forward is his ruling alone.**

---

## **>>> 2026-07-31 (evening, second): CRYPTOPANIC IS DEAD AND THE COMMANDER RULED THE REPLACEMENT.**

**He went to get the token this ship had asked him for eight times and found it
is now a PAID product. Nobody had checked.** Three replacements were probed and
rejected with reasons; **the publishers' own public feeds were adopted — no
account, no key, no signup, no expiry, no new dependency.** **Phase 3 step 3 now
carries the correction with the wrong plan STRUCK AND LEFT VISIBLE**, following
the Slot 2 precedent of 2026-07-26.

**THERE IS NOTHING LEFT ON HIS DESK TO SIGN UP FOR.** The news instrument is
unblocked and needs nothing from him.

**AND ONE THING THE NEXT SESSION MUST MEASURE BEFORE IT BUILDS: a news gate may
not be able to verify anything at all.** Funding rates sit still for eight hours;
headlines land every few minutes, so the gate's fetch and the module's fetch can
legitimately disagree and **the gate would go red with nothing wrong — R-021 and
R-034 by design, in a part nobody has written.** **R-036, filed unmeasured by the
session that recommended the source.**

---

## **>>> 2026-07-31 (evening): THE COMMANDER SUSPENDED PART 1 FOR ONE SESSION.**

**The next session does NOT attack. It repairs S6 (R-034) and B1 (R-031),
proves both, and explains both in plain words. HIS RULING, ONE SESSION ONLY —
the usual rhythm stands for every build after it, and `THE_PATTERN.md` was
deliberately NOT edited, because a rule suspended once is not a rule changed.**

    NOT SUSPENDED: a session may never clear its own repair · the gate is
    declared first and committed alone · re-running the original fault against
    your own fix is not attacking, it is what "fixed" means.

**MEASURED THE SAME HOUR, AND IT REORDERED THE JOB:** the Commander's laptop
runs **UTC+5** (12:20 UTC / 17:20 local). **B1 is therefore NOT blind on his
machine and never cost him a red screen** — it goes inert only where local time
IS UTC, which is the cloud watchman. **S6 is the one costing him time: one
settlement in six, on his own laptop, in every timezone.**

**AND THE LARGEST UNGUARDED THING ON THIS SHIP, FOUND WHILE ANSWERING HIS
QUESTION ABOUT FAKE DATA IN REAL TIME — MEASURED, NOT SUSPECTED: no file here
talks to more than one source.** Fear & Greed from alternative.me alone, funding
from Binance alone, prices from TwelveData alone. **Every gate proves the printed
line matches what the source SENT; nothing asks whether the source was RIGHT.**
A wrong number from a source would be printed in perfect confidence with every
alarm green. **R-035, P2 — the only route to a wrong number on his screen with
no guard on it at all.** Recommended as the next real attack, after the news
build. **Nothing was built or repaired this session; only documents changed.**

---

## **>>> DOOR 3 SURVIVED ITS FIRST INDEPENDENT ATTACK — WITH ONE BLIND SPOT NAMED. AND PHASE 3 STEP 3 IS BLOCKED ON A FREE SIGNUP.**

→ We are at: **PHASE 3 — THE FOURTEENTH GENERATION. NOTHING WAS BUILT AND
NOTHING WAS REPAIRED, AND FOR THE FIRST TIME THAT IS NOT BECAUSE OF A FINDING.**

    cockpit/funding.py      GATE 3.2-R7  PASSED  exit 0  0 red  (first run,
                                         11:12-11:14 UTC, +3h12m past settlement)
    cockpit/fear_greed.py   GATE 3.1-R7  PASSED  exit 0  0 red
    data/open_interest.py   GATE 3.2b-R9 PASSED  exit 0  0 red
    lab/verify_vault.py     VAULT INTACT 6/6
    cockpit/brief.py        3/3 instruments reporting
    data/oi_history/        3 files, correctly named, 181 lines each, sha256
                            e3258e82 / 1549a8a1 / e0f91a87 — UNCHANGED. No B14.
    git status              clean before and after. No .py file was edited.

**F10 DID NOT COME BACK.** The thirteenth generation's repair is not regressed.

**WHAT IS BROKEN OR UNPROVEN, WHICH IS THE POINT OF THIS MARKER.**

- **>>> PHASE 3 STEP 3 IS BLOCKED AND ONLY THE COMMANDER CAN UNBLOCK IT.**
  `.env` holds exactly one key, `TWELVEDATA_API_KEY`. **There is no CryptoPanic
  token anywhere in this repo.** Unauthenticated: `/api/v1/posts/` → **HTTP 403**,
  `/api/developer/v2/posts/` → **HTTP 404**. Every gate on this ship measures a
  printed line against a raw fetch; **with no fetch there is nothing to measure
  against, and a gate whose expectations were invented is the one thing this ship
  exists to refuse.** **THIS IS THE EIGHTH TIME STEP 3 HAS NOT BEEN BUILT AND THE
  FIRST TIME THE REASON IS NOT A FINDING.**
- **DOOR 3 IS BLIND TO A DAEMON THREAD — proved by Door 3's own judge.** Shape A5
  is A1 with `daemon=False` → `daemon=True`; the control ran first and was silent;
  A1-A4 CAUGHT; **A5 ESCAPED.** The printed pass line says *"nothing was deferred
  to a thread"* when only NON-DAEMON threads are tested. **R-033, CATEGORY B.**
- **MEASURED, AND IT IS THE DURABLE PART: Door 3's child stops watching between
  0.5 s and 1.0 s after the doorway; the Commander's Brief is still on screen
  until between 1.5 s and 2.0 s.** The judge is deliberately the smallest possible
  process, so **it watches for less time than the pilot is exposed.**
- **THAT GAP DOES NOT REACH HIM TODAY, AND ONLY BY ACCIDENT.** A write in that
  band is caught by **DOOR 1**, because the gate calls the doorway dozens of times
  in 62 s and the write lands in a later listening window (measured red at 1.25 s
  and 1.75 s). **Nobody designed that backstop and nothing records that it is
  load-bearing.** The funding instrument's equivalent protection is **the order of
  two lines in `brief.py`** — 90 then 91 — **and nothing tests that order.**
- **THE THIRD FILE'S INERTNESS SWEEP FOUND THE F10/B1 DISEASE AGAIN, WORSE.**
  `S6` (tickers miswired) is a **complete no-op on 15.84% of settlements — one in
  6.3**, measured over 6,441 settlements of real Binance history; most recently
  2026-06-02, all three at +0.0100%. **Two and a half times more common than the
  F10 defect that turned this ship red yesterday morning. R-034, CATEGORY B.**
  **HONEST LIMIT: measured on SETTLED rates; the Brief prints the ESTIMATE, so
  15.84% is an UPPER BOUND and the live figure is unknown.**
- **THE OTHER SEVENTEEN SABOTAGES IN `funding.py` SWEPT CLEAN** — S2 and S4 are
  inert on 0 of 6,441 settlements, S1/S3 never (the sign character always moves),
  S11's hole is already covered on purpose by the rotating partial drill.
- **NINE OF R-032'S TEN DOUBTS ARE STILL UNTESTED**, including doubt 2 — a write
  to the real console device, to descriptor 3, or through a re-opened `CONOUT$`.
  **Nobody knows the answer to that one.**
- **DOUBT 10 IS CONFIRMED BY OBSERVATION:** both cockpit gates print `…-R6` as
  their title and `…-R7 PASSED` as their verdict. **Nothing checks that a gate's
  printed name matches the bar it was declared under.**
- **THE CATEGORY B PILE IS ELEVEN DEEP.** Cleared before the ship is used for
  real, at the same moment `cockpit/brief.py` gets its gate.
- **R-021 has a THIRD clean data point (+3h12m) and its edges are still
  unmeasured.** **R-006 is untouched and no in-house session may clear it.**

---

## PREVIOUS MARKER, KEPT FOR THE RECORD — 2026-07-31 (morning), the thirteenth generation

## **>>> DOOR 3 IS BUILT. THE ORDER THAT SLIPPED SEVEN TIMES IS CARRIED OUT.**

→ We are at: **PHASE 3 — THE THIRTEENTH GENERATION. R-025 IS SHUT.** A fresh
interpreter now imports each cockpit module, calls its doorway on every path the
pilot can see, and **then shuts down** — and the child's TOTAL output must be
empty. Interpreter shutdown joins non-daemon threads, flushes every buffer and
runs every atexit handler, **so the three deferred shapes that put 162 lines of
trading advice past the gate on 2026-07-30 are now caught deterministically
instead of raced.**

    cockpit/funding.py      GATE 3.2-R7  PASSED  exit 0  0 red  122 s
    cockpit/fear_greed.py   GATE 3.1-R7  PASSED  exit 0  0 red   62 s
    data/open_interest.py   GATE 3.2b-R9 PASSED  exit 0  0 red   56 s
    lab/verify_vault.py     VAULT INTACT 6/6
    cockpit/brief.py        3/3 instruments reporting
    data/oi_history/        3 files, 181 lines each, sha256 e3258e82 /
                            1549a8a1 / e0f91a87 — byte-identical to 2026-07-30

**ALL THREE RUNTIMES ON RECORD WERE WRONG AGAIN** (128 / 40 / 74). Measured before
Door 3: **88 / 34 / 56.** Door 3 then cost funding +34 s and fear_greed +28 s.
**R-027 doubt 10 has now been right for FOUR consecutive sessions.**

**WHAT IS BROKEN OR UNPROVEN, WHICH IS THE POINT OF THIS MARKER.**

- **THE SHIP WAS RED WHEN THIS SESSION ARRIVED, AND NOT FOR A REASON ANYONE HAD
  BUILT.** `GATE 3.1-R6` exited 1 because sabotage F10 transposed two numbers that
  were both 28 that day. **The instrument and the Brief were correct throughout.**
  Graded SMALL; repaired only because **the Commander ruled** it should be, since
  Door 3 could not be certified into a file whose gate exits 1.
- **THE SAME DISEASE WAS THEN FOUND IN A SECOND FILE.** `B1` in the recorder is a
  **no-op on any machine whose clock is UTC** — reproduced deterministically with
  no file edited, the sabotage being the ENVIRONMENT. R-013 doubt 4 predicted it on
  2026-07-28 and it sat three sessions as a suspicion. **R-031, CATEGORY B.**
- **AND THE THING UNDERNEATH BOTH, WHICH NOTHING ON THIS SHIP MEASURES:** a
  sabotage can satisfy the gate's reachability check completely and still change
  nothing. In the same failing run the gate printed `✓ B1 rebinds '_utc_iso' → the
  swap reaches the code the pilot runs` **and** `✗ B1 → ESCAPED`. **Both true.
  REACH and EFFECT are different things and only the first has ever been checked.**
- **DOOR 3 IS UNATTACKED.** R-032, ten doubts, filed by its author against his own
  work. **Twelve of the previous twelve generations were failed by the next pair of
  eyes.** The sharpest doubt: Door 3 runs the paths the GATE names, inheriting
  R-022 doubt 6 whole.
- **R-025 IS NOT CLEARED and this session REFUSED the permission the orders gave
  it to clear it** — those orders were written before it was known the same session
  would be ordered to build the repair. **A session may never clear its own work.**
- **CONTEXT DECK INSTRUMENT 3 OF 5 (news headlines) IS NOW THE NEXT BUILD.** It has
  been deferred SEVEN times. **Nothing is ahead of it any more.**
- **THE CATEGORY B PILE IS NINE DEEP**, up from six in one session.
- **THE 1 AUGUST ERRAND IS DUE TOMORROW.** The recorder's commit-and-push branch
  has still never fired against real new rows.

---

# PREVIOUS MARKER — 2026-07-30 (evening), kept for the record rather than erased

## **>>> THE COLLISION BELOW IS ANSWERED. THE COMMANDER RULED THE SAME EVENING.**

**HE CHANGED HOW FINDINGS ARE JUDGED, AND `THE_PATTERN.md` WAS EDITED ON HIS
RULING — 98 insertions, ZERO deletions, nothing renumbered, his own Step 2.2
wording untouched.** Three questions now sit in front of Step 0: **what information
is this code for · can this fault make it WRONG, MISSING or DELETED, today or after
how many further mistakes each named · say it in real business terms.**

**HE ALSO SAID, AND IT IS RECORDED IN `PROGRESS_LOG.md` IN HIS OWN WORDS:** *"I'm
not saying loosen the checks. Show the real faults which can affect when the system
will run. For those actual faults I'm willing to do 50 sessions."* **THE FOURTEEN
SABOTAGES STILL RUN EVERY TIME. THE LOOP IS UNCHANGED. Only WHICH findings may stop
the building has changed.**

**UNDER THE NEW FORM, THIS SESSION'S OWN FINDING SCORES SMALL** — the recorder
wrote 180 perfect rows, the fault was in the scoreboard, and two further mistakes
are needed before any number goes wrong. **DOOR 3 IS THE NEXT SESSION'S FIRST JOB
AND IT IS NOT CONDITIONAL.**

→ We are at: **PHASE 3 — THE TWELFTH GENERATION. TWO MORE FINDINGS AGAINST THE
SAME CHECK, ONE DAY AFTER THE LAST TWO, BOTH REPAIRED UNDER GATE 3.2b-R9. A SABOTAGE
THAT REBOUND A NAME THE RECORDER CANNOT EVEN SEE WAS SCORED **CAUGHT** AND CERTIFIED
AS REACHING THE MODULE, WHILE THE RECORDER WROTE 180 PERFECT ROWS AND THE GATE
EXITED 0. **DOOR 3 (R-025) IS STILL NOT BUILT — THE SERIOUS RULE STOPPED THE BUILD,
AND THAT COLLISION IS ON THE COMMANDER'S DESK.**

    data/open_interest.py   GATE 3.2b-R9 PASSED  exit 0  0 red, 14/14 CAUGHT, 74 s
    cockpit/fear_greed.py   GATE 3.1-R6  PASSED  exit 0  0 red   40 s
    cockpit/funding.py      GATE 3.2-R6  PASSED  exit 0  0 red  128 s — SEE R-025
    lab/verify_vault.py     VAULT INTACT 6/6
    cockpit/brief.py        3/3 instruments reporting
    data/oi_history/        3 files, correctly named, 181 lines each, sha256
                            e3258e82 / 1549a8a1 / e0f91a87 — unchanged all session

**WHAT IS BROKEN OR UNPROVEN, WHICH IS THE POINT OF THIS MARKER.**

- **DOOR 3 IS AN ORDER AND IT IS NOT BUILT.** The Commander ruled R-025 SERIOUS on
  2026-07-30 (afternoon) and accepted that Context Deck instrument 3 slips a sixth
  time. **It has now slipped a SEVENTH**, because this session's own findings graded
  SERIOUS and the rule for SERIOUS is fix-and-stop. **The session that wrote that
  grade is the session the grade excused from building. He can overrule it in one
  word and the orders say so.**
- **R-027 IS OPEN AGAINST GATE 3.2b-R9 AND ITS AUTHOR MAY NOT CLEAR IT.** Ten
  doubts filed. The strongest: `_named_in_production` is a TEXT search, so a name
  appearing only in a COMMENT counts as code — the same disease, untested.
- **THE PROPERTY FIX IS A SHAPE, NOT A FORM.** A getter with a frozen default is
  now seen; a getter that closes over the value is not, proved in the same run.
- **R-026 DOUBT 1 IS UNTOUCHED** — the controls still mutate the module's own
  `globals()` and nothing compares the namespace before and after.
- **R-022 DOUBT 6 IS UNTOUCHED**, nine sessions now.
- **THE CATEGORY B PILE IS SIX DEEP** (R-028 joined it tonight).
- **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED FOR REAL.** The
  errand is due **1 August**; on 2026-07-30 it was NOT due and the scheduled task
  reads Status Ready, Next Run 01-Aug-2026 09:00.

**THE PREVIOUS MARKER, KEPT FOR THE RECORD RATHER THAN ERASED:**

→ We are at: **PHASE 3 — THE ELEVENTH GENERATION. TWO FINDINGS, BOTH PROVED, ONE
REPAIRED. THE CHECK BUILT THAT MORNING TO STOP B9's CLASS WAS ITSELF BLIND TO
THREE OF THE FOUR WAYS IT HAPPENS (repaired under GATE 3.2b-R8), AND R-022 DOUBT 1
WAS RIGHT: 162 LINES OF ADVICE REACHED THE PILOT'S SCREEN UNDER A GATE THAT
PASSED (R-025 — **RULED SERIOUS BY THE COMMANDER 2026-07-30 (afternoon); DOOR 3 IS
THE NEXT SESSION'S ORDER**).**

    data/open_interest.py   GATE 3.2b-R8 PASSED  exit 0  0 red ticks, 14/14 CAUGHT
    cockpit/fear_greed.py   GATE 3.1-R6  PASSED  exit 0  0 red
    cockpit/funding.py      GATE 3.2-R6  PASSED  exit 0  0 red  — BUT SEE R-025
    lab/verify_vault.py     VAULT INTACT 6/6
    cockpit/brief.py        3/3 instruments reporting
    data/oi_history/        3 files, correctly named, 181 lines each, sha256
                            unchanged across every run of this session

**FINDING 1, REPAIRED.** `_frozen_as_default` read `__defaults__` and nothing
else. A KEYWORD-ONLY default, a `functools.partial` and a class body were
invisible to it. A real two-line edit made B1 and B2 no-ops while check (n)
printed a green tick over both, **in the same run that scored them ESCAPED**.
Graded SERIOUS on Step 2.1 — `*,` is ordinary Python — and repaired under GATE
3.2b-R8, declared and committed alone first (`3434ed6`). **The shipped file had no
such freeze, and when one was written the drill went red loudly: the CLAIM was
broken, not the protection.**

**AND THE PART THAT MATTERS MOST ABOUT THE REPAIR: ITS FIRST DRAFT FAILED ITS OWN
GATE.** It counted a module-level alias as a freeze and a healthy file went red
fourteen times, because `_RECORD_ORIGINAL = record` is the drill's own saved
original. The rule was removed and turned into a permanent negative control.
**The drill caught its author, which is the whole argument for building the
controls before the verdict.**

**FINDING 2, NOT REPAIRED — R-025, ON THE COMMANDER'S DESK.** The ear shuts the
instant the doorway returns. A thread, a kept-alive buffer over descriptor 1 and
an atexit handler put **162 lines of trading advice** on the pilot's screen while
GATE 3.2-R6 printed *"the doorway wrote NOTHING"* three times, passed its ear
control 3/3, and **exited 0**. Graded **SERIOUS** on Step 2.2 in the Commander's
own wording. **NOTHING ON THIS SHIP DEFERS A WRITE TODAY** — measured across both
production halves — **so it is SERIOUS and NOT LIVE, which is the distinction he
needs in order to rule.** The repair (DOOR 3: a fresh interpreter that imports,
calls, and SHUTS DOWN, with a timeout counting as failure) is designed and written
down in `REVIEW_QUEUE.md` so the next session need not invent it.

**R-022 DOUBT 4 TESTED AND HELD.** `os.fstat(fd)[:4]` returns a real 17-digit
`st_ino` on this machine and detects both a leak onto the capture file and a leak
onto another regular file. The doubt's premise — "on Windows st_ino is often 0" —
is false here. Measured with stdout redirected to a file; a console handle was not
tested, and that limit is written down rather than counted as cleared.

**WHAT IS NOT DONE.** Context Deck instrument 3 was not built — two findings
graded SERIOUS is not a building session. **R-007 is untouched for the eighth
session.** R-022 doubt 6 untouched. **R-026 is open against the repair and its
author may never clear it.** **Six generations have now fixed the instance and
left the pattern:** `def run(symbols=SYMBOLS, ...)` and `fetch_history` still
freeze their globals, and the one-line change that ends the class touches what the
pilot reads, so only the Commander can order it.

**THE PREVIOUS MARKER, KEPT FOR THE RECORD:**

→ We are at: **PHASE 3 — THE TENTH GENERATION. R-020 WAS ATTACKED AT LAST AND A
REAL LEAK WAS FOUND: SABOTAGE B9 HAD NEVER TESTED ANYTHING. REPAIRED UNDER GATE
3.2b-R7. R-022 WAS ATTACKED IN TWO DIRECTIONS AND HELD — THE SHIP'S FIRST CLEAN
REVIEW RESULT.**

    data/open_interest.py   GATE 3.2b-R7 PASSED  exit 0  0 red ticks, 14/14 CAUGHT
    cockpit/fear_greed.py   GATE 3.1-R6  PASSED  exit 0  0 red
    cockpit/funding.py      GATE 3.2-R6  — see item 3 below for when and why
    lab/verify_vault.py     VAULT INTACT 6/6
    cockpit/brief.py        3/3 instruments reporting
    data/oi_history/        3 files, correctly named, 181 lines each,
                            sha256 unchanged across every run of this session

**WHAT WAS FOUND.** Every sabotage in the recorder's drill is installed with
`globals()[attr] = repl`, which reaches a name only if the name is looked up **at
call time.** `def run(symbols=SYMBOLS, ...)` captures the tuple once, when the
`def` runs, and `SYMBOLS` is read nowhere else in the module — **so B9 changed a
name nothing reads, and the recorder went on collecting all three assets.** It was
scored CAUGHT by the first line of its judge, a name comparison that returns
before `run()` is ever called. **The half of `_covers_every_asset` its own
docstring calls the only way to catch an asset going missing had never been shown
able to fail.** Four generations of this gate printed `✓ B9 → CAUGHT` under a
headline announcing fourteen of fourteen.

**WHAT WAS NOT WRONG, STATED AS LOUDLY.** The real one-line defect **is** caught
— proved by running the whole gate against a scratch tree carrying it: exit 1,
two red lines, SOLUSDT visibly absent. **The evidence was broken, not the
protection.** No asset could ever have silently stopped being collected.

**WHAT WAS BUILT.** GATE 3.2b-R7, declared in `PROGRESS_LOG.md` and committed
alone with no `.py` file in that commit. B9 is now a **REAL TEXT EDIT** in
`_FILE_SABOTAGES`, judged by `_record_does_the_job` — the same function the
healthy check uses — and proved to RETURN False rather than raise. And a new
permanent check `(n)` proves **the drill's installer is able to install**: no
globals-swap sabotage may target a name this module has frozen as a default
argument, and the check carries a positive control that must first find the
frozen `SYMBOLS` in `run` before its silence is believed.

## **THE TRUTH INCLUDING WHAT IS BROKEN OR UNPROVEN**

1. **GATE 3.2b-R7 HAS NOT BEEN INDEPENDENTLY ATTACKED — R-024.** Written by the
   session that found the fault it repairs, which may never clear it. **Seven
   doubts filed against it by its own author**, the sharpest being that its
   positive control is hardcoded to one name, so **fixing `run`'s signature — the
   right change in itself — would turn the gate red**, and that the new check
   guards `_SABOTAGES` only, not `_FILE_SABOTAGES`, and does not exist in the two
   cockpit files at all.

2. **THE PATTERN WAS FIXED IN THE TEST AND LEFT IN THE MODULE.**
   `def run(symbols=SYMBOLS, ...)` is still there. It is **not** a production
   defect — a real source edit works correctly — and the repair rules forbade
   touching anything the pilot reads. **But it is the fifth time a session has
   repaired the one instance it attacked**, and `funding.py`'s `contracts=None`
   pattern shows what the alternative looks like.

3. **THE FUNDING GATE WAS NOT RUN ON ARRIVAL, DELIBERATELY, AND THE REASON IS
   RECORDED RATHER THAN GLOSSED.** Arrival was 07:53 UTC — seven minutes before
   the 08:00 settlement, inside R-021's window. Running it there would have
   proved nothing either way. **It was run after the window cleared and the
   result is in `PROGRESS_LOG.md`.** R-021 stands: SMALL, CATEGORY B, unrepaired.
   **OUTSIDE A SETTLEMENT WINDOW A RED FUNDING GATE IS A REAL FAILURE.**

4. **R-023, NEW, CATEGORY B: ON THE REAL B9 DEFECT THE GATE ENDS IN A STACK
   TRACE.** It exits 1 with two red lines above it, so the alarm is correct and
   loud — but it never prints `GATE FAILED`, never reaches the drill, and dies on
   a bare `FileNotFoundError`. `name_ok` has a REFUSES-TO-RUN branch for exactly
   this reason; `symbols_ok` has the identical consequence and no such branch.
   **Filed, not fixed — the rules say a SMALL finding is filed.**

5. **R-022 HELD ON TWO AXES AND IS STILL OPEN ON THREE DOUBTS.** The constant
   swaps all reach; both import doors are caught for the reason they claim,
   `quiet` being the only component that flips. **NOT tested: doubt 1's thread
   that writes after `_capture` has restored the descriptors — its author's own
   strongest lead — nor doubt 4's `os.fstat` on Windows, nor doubt 6.** R-016 is
   therefore still not settled.

6. **`cockpit/brief.py` STILL HAS NO GATE.** He has ruled: **NOT NOW, BEFORE
   GOING LIVE.** A standing requirement, not a deferral to re-argue.

7. **THE CATEGORY B PILE IS NOW FIVE DEEP** and is cleared before the ship is
   used for real, at the same moment `brief.py` finally gets its own gate.

8. **AT PHASE 6 THE "SEPARATION IN TIME" SUBSTITUTE FOR FABLE EXPIRES — R-006,
   which no in-house session may ever clear.** Unchanged and not waived.

---

# PREVIOUS POSITION MARKER — 2026-07-29 (night), superseded by the above, kept for the record

→ We are at: **PHASE 3 — THE BRIEF'S TWO DOORS ARE CLOSED. THE COMMANDER'S
ORDER, DEFERRED BY TWO SESSIONS, WAS CARRIED OUT ON 2026-07-29 (night).**

**HE REVERSED THE RHYTHM TO GET IT DONE, IN WRITING, AND ONLY HE COULD.**
ATTACK-then-BUILD became BUILD-then-ATTACK for that session alone: *"Part 1 is
closing the two doors — that is my order and it has waited two sessions… Do not
defer my order a third time."* **`THE_PATTERN.md` was NOT edited; the rhythm
stands for everyone else.**

    cockpit/fear_greed.py   GATE 3.1-R6 PASSED  exit 0  17 sabotages caught
    cockpit/funding.py      GATE 3.2-R6 PASSED  exit 0  18 sabotages caught
                                                55 checks green, 0 red
    data/open_interest.py   GATE 3.2b-R6 PASSED (2026-07-29 evening, 14)
    vault INTACT 6/6 · Brief 3/3 · lab/ and data/oi_history/ untouched

**WHAT WAS CLOSED.** The ear listened to the NAMES `sys.stdout`/`sys.stderr`, so
a raw `os.write` to the descriptor and a `logging` handler bound at import time
both walked past it — **measured, with both escaped lines printing trade
instructions on the terminal.** And **nothing anywhere watched what these modules
write at IMPORT time**, where one line put ">> … go long" ABOVE the Morning
Brief's own header. `_capture` now listens at the FILE DESCRIPTOR, the ear is
**made to prove it can hear before its silence is believed**, and a fresh
interpreter imports each module and requires silence.

## **THE TRUTH INCLUDING WHAT IS BROKEN OR UNPROVEN**

1. **NOTHING OF THE NINTH REPAIR (R-020) WAS ATTACKED. NOT PARTIALLY — NOT AT
   ALL.** The session ran short and the Commander had authorised exactly that
   in advance. **R-020 is untouched, uncleared, and it is the next session's
   Part 1.** Its five recorded doubts have never been tested.

2. **THE FUNDING GATE GOES RED NEAR A FUNDING SETTLEMENT — R-021, CATEGORY B.**
   A live-rate race in `_core_checks`/`_partial_checks`: the bookend snapshots
   cannot bracket a rate that moves twice, and near a settlement it does.
   **PROVED by controlled comparison, not asserted:** the untouched `3.2-R5`
   bytes from commit `74ec950` FAIL x4 in the window and PASS x2 outside it,
   while `3.2-R6` FAILS 3 of 4 inside and PASSES x3 outside. **Binance settles
   at 00:00, 08:00 and 16:00 UTC.** ~130 seconds per run. It fails LOUD and the
   Brief is correct throughout, so it was graded SMALL at the Step 1 veto and
   filed rather than repaired. **The repair must tighten the BRACKET, never the
   BAR. AND: OUTSIDE A SETTLEMENT WINDOW A RED FUNDING GATE IS A REAL FAILURE.**
   The first version of this marker called it "red three runs in four" flat —
   measured in one 45-minute window and corrected the same night.

3. **THE R-016 REPAIR HAS NOT BEEN INDEPENDENTLY ATTACKED — R-022.** Its author
   filed **seven doubts against his own work**, the sharpest being that
   `brief.py`'s own import surface is still unwatched: **a `pandas_ta`
   `UserWarning` is already printing on the real Brief's first line.**

4. **`cockpit/brief.py` STILL HAS NO GATE.** The Commander has ruled: **NOT
   NOW, BEFORE GOING LIVE.** Standing requirement, not to be re-argued.

5. **AND THE ONE THAT DOES NOT EXPIRE:** at Phase 6 the "separation in time"
   substitute for Fable EXPIRES. A second, genuinely independent AI reviews the
   gauntlet's test setup before it runs and its verdict after. **R-006, and no
   in-house session may ever clear it.**

---

## THE PREVIOUS MARKER, KEPT FOR THE RECORD RATHER THAN ERASED

→ We are at: **PHASE 3 — THE GATE NOW HOLDS ITS OWN ADDRESS, NOT JUST ITS OWN
EXPECTATIONS. THE COMMANDER HAS RULED THAT THE BRIEF'S TWO DOORS ARE TO BE
CLOSED, AND THEY ARE STILL OPEN — A SESSION DEFERRED HIS ORDER AND SAID SO.**
Gate 3.2b-R6 (the open-interest recorder, **FOURTEEN** sabotages) PASSED
2026-07-29 evening, exit 0, zero failure marks. Gate 3.2-R5 (funding, fifteen)
and Gate 3.1-R5 (Fear & Greed, fourteen) still PASS — **and are both still known
to be defeatable. They have still not been repaired.**

**WHAT THE NINTH INDEPENDENT REVIEW FOUND.** A session that built none of it
invented one new attack and **it escaped, predicted correctly in writing
beforehand.** The new question — the five previous ones being spent — was
***every check finds the recorder's work by asking the recorder where it put it;
what if it puts it somewhere else?***

    B14  `csv_path` returns `f"{symbol}.csv"` instead of
         `f"{symbol}_{PERIOD}.csv"`. An ordinary filename tidy-up. It
         breaks no logic, writes no wrong number, loses no row from the
         file it writes, and its report is TRUE about that file.
         GATE 3.2b-R5 PASSED, exit 0, 13/13 CAUGHT ................... ESCAPED

**THE CLASS, in one sentence: R-014's lesson had been applied to five VALUES THE
GATE COMPARES and never once to the ADDRESS THE GATE WALKS TO.**
`GATE_SYMBOLS`, `GATE_OFFLINE_WORDS`, `GATE_LIMIT`, `GATE_PERIOD_HOURS`,
`GATE_REPORT_RE` — every one a value. All twenty-three places that located a CSV
asked the module's `csv_path()`, and **no line anywhere on this ship named
`<SYMBOL>_4h.csv`.** `_record_does_the_job` pins the FOLDER, that pin was
attacked the day before and HELD — **nobody went the one level down.**

**THE MOST DAMNING LINE WAS CHECK (m), BUILT THE DAY BEFORE TO PROVE THE ARCHIVE
SURVIVES.** It seeded archive rows into the new filename, watched the recorder
append to the new filename, read them back from the new filename, and certified
them. Against a copy of the REAL archive, B14 left `<SYMBOL>_4h.csv` frozen at
180 rows and started a second file, printing `180 new row(s) appended, 180
stored` where the honest run prints 192.

Graded **SERIOUS** on **two of three** Step 2 questions — by accident, and
invisible on its face under the Commander's own new 2.2. **AND THE
QUALIFICATION, RECORDED AGAINST THE FINDING'S OWN INTEREST: B14 DESTROYS
NOTHING.** B13 deleted 34 irreplaceable rows; B14 deletes none — the two files
together still hold every row. **It is SERIOUS because it is invisible and
happens by accident, not because anything is lost.** **Repaired under Gate
3.2b-R6, declared in `e4fdb7c` with no `.py` in it.** The attack, re-run as a
real text edit, now fails with exit 1 and a named first line
(*"the module's csv_path ['BTCUSDT.csv', …] equals the gate's own
['BTCUSDT_4h.csv', …]"*), then **REFUSES TO RUN** rather than dying in a
traceback. Production half byte-identical by sha256; **zero** diff hunks touch
lines 1-242, `__main__` at 243.

**STEP 3.3 WAS NOT BUILT — DEFERRED A SEVENTH TIME**, because a SERIOUS finding
means fix it and stop. **The Context Deck has sat at two instruments of five for
seven consecutive sessions**, and the reason each time was a real defect found in
the session before.

**THE COMMANDER'S TWO RULINGS OF 2026-07-29 (evening), both put to him in plain
words before any code was read, and both recorded:**
- **R-016: CLOSE THE TWO DOORS.** The condition he set — *attack first, then
  decide* — had been met. **HE RULED. THE WORK IS NOT DONE.** B14 graded SERIOUS
  the same session, his own rule says SERIOUS means build nothing, and closing
  the doors is a build. **It is the next session's Part 2, marked as HIS
  instruction. A session made that call about his order and it is recorded here
  so he can overrule it in one word.**
- **R-019: HE REFUSED THE SESSION'S WORDING FOR STEP 2.2 AND WROTE HIS OWN.**
  **`THE_PATTERN.md` IS NOW EDITED**, verbatim, under a heading saying the words
  are his. His version is stricter than the draft in a way nobody proposed: **his
  knowledge of this ship's own rules counts as a prediction about him.** R-019 is
  CLEARED — by him, the only authority who could.

**WHAT IS BROKEN OR UNPROVEN RIGHT NOW, stated because this marker must carry
the truth and not the good news:**
- **Gate 3.2b-R6 has been failed by nobody, which is not the same as having
  survived somebody.** Filed as R-020 with five doubts its own author could not
  settle. **Nine generations; the condition on R-001 has never once been met.**
- **I FIXED ONE ADDRESS AND SWEPT FOR NO OTHERS.** The two Context Deck
  instruments were not examined for the same class at all. **That is R-020's
  first and strongest doubt.**
- **THE BRIEF'S TWO DOORS ARE OPEN AND THE COMMANDER HAS ORDERED THEM SHUT.**
  Until they are, one line in either instrument can put a trade instruction on
  his Morning Brief with every gate green.
- **`cockpit/brief.py` STILL HAS NO GATE.** His standing ruling: NOT NOW, BEFORE
  GOING LIVE.
- **The recorder's commit-and-push branch has still never fired against real new
  rows.** It cannot until 1 August.
- **The Category B pile must be cleared before the ship is used for real.**

**THE PREVIOUS MARKER, kept for the record rather than erased:**

→ We are at: **PHASE 3 — THE GATE CAN NOW BUILD THE SHAPE THE REAL WORLD HAS.
THE BRIEF'S TWO UNWATCHED DOORS ARE STILL OPEN AND THE COMMANDER HAS DEFERRED
HIS RULING UNTIL AFTER THIS REVIEW — WHICH IS NOW DONE, SO THE RULING IS DUE.**
Gate 3.2b-R5 (the open-interest recorder, **THIRTEEN** sabotages) PASSED
2026-07-29 afternoon, exit 0, zero failure marks. Gate 3.2-R5 (funding, fifteen)
and Gate 3.1-R5 (Fear & Greed, fourteen) still PASS — **and are both still known
to be defeatable. They have still not been repaired.**

**WHAT THE EIGHTH INDEPENDENT REVIEW FOUND.** A session that built none of it
invented two new attacks and **both escaped, both predicted correctly in writing
beforehand.** The new question — the four previous ones being spent — was
***the gate builds the world it tests in; what shape does the REAL world have
that the gate's world can never have?***

    B12  the report's `window X → Y` derived from THE CLOCK. The parser
         stopped matching at the word `window ` and nothing compared
         those timestamps to anything. Counts stayed honest, so the
         brand-new check (l) had nothing to say ...................... ESCAPED
    B13  the archive "kept in step with the window the source serves" —
         an ordinary rolling-window tidy-up WHOSE PRINTED REPORT IS
         TRUE. In every scenario the gate could build, stored ⊆ fresh,
         so the branch never fired and eleven checks stayed green .... ESCAPED

**THE CLASS, in one sentence: A GATE CAN ONLY EVER JUDGE THE WORLD IT IS ABLE TO
BUILD.** Seven generations hardened *what the gate looks at*; none had asked
*what the gate is able to put in front of itself.*

**B13 IS THE WORST FINDING THIS SHIP HAS RECORDED AGAINST THE RECORDER.** Every
gate scenario seeds an empty directory or one filled from the gate's own fetch,
so the stored rows are always a SUBSET of what Binance still serves. **In real
life that is false from the very next run:** the archive starts 2026-06-27,
Binance serves a rolling thirty days, and its window already begins 2026-06-29.
Run against a copy of the REAL archive, B13 **destroyed 34 rows** — 11 BTC,
12 ETH, 11 SOL — that exist nowhere else on earth, while printing
`11 new row(s) appended, 180 stored` where the honest run prints 191.

Graded **SERIOUS** on **three of three** Step 2 questions — by accident,
invisible to him, **and not undoable at any price.** B12 graded SERIOUS, the
lesser. **Repaired under Gate 3.2b-R5, declared in `dac6db4` with no `.py` in
it.** Both attacks, re-run as real text edits, now fail with named diagnostics
(*"the report claims the window STARTS at … the gate's own fetch says …"* and
*"ARCHIVE ROW … WAS DESTROYED"*). Production half byte-identical by sha256;
every diff hunk at or after line 309 with `__main__` at 243.

**STEP 3.3 WAS NOT BUILT — DEFERRED A SIXTH TIME**, because a SERIOUS finding
means fix it and stop. Said plainly rather than buried: **the Context Deck has
sat at two instruments of five for six consecutive sessions**, and the reason
each time was a real defect found in the session before.

**THE COMMANDER'S TWO RULINGS OF 2026-07-29, both recorded:**
- **R-016: ATTACK FIRST, THEN DECIDE.** He deferred deciding whether to close
  the Brief's two doors until this review reported. **It has now reported, and
  it found the newest gate leaking too. The ruling is due.**
- **STEP 2.2 OF THE FINDING REPORT: DO NOT ASSUME EITHER WAY.** A claim about a
  person may not carry a technical grade. **This changes the grading form
  itself.** Both of this session's findings were graded under it. **`THE_PATTERN.md`
  has NOT been edited** — the wording is on his desk in `SESSION_ORDERS.md`,
  filed as R-019.

**WHAT IS BROKEN OR UNPROVEN RIGHT NOW, stated because this marker must carry
the truth and not the good news:**
- **Gate 3.2b-R5 has been failed by nobody, which is not the same as having
  survived somebody.** Filed as R-018 with five doubts its own author could not
  settle. **Eight generations; the condition on R-001 has never once been met.**
- **`cockpit/funding.py` and `cockpit/fear_greed.py` were not attacked at all
  this session.** R-016's two doors are open and untested.
- **`cockpit/brief.py` STILL HAS NO GATE.** His standing ruling: NOT NOW, BEFORE
  GOING LIVE.
- **The recorder's commit-and-push branch has still never fired against real new
  rows.** It cannot until 1 August.
- **The Category B pile must be cleared before the ship is used for real.**

**THE PREVIOUS MARKER, kept for the record rather than erased:**

→ We are at: **PHASE 3 — THE RECORDER'S REPORT IS NOW GUARDED. THE BRIEF'S TWO
UNWATCHED DOORS ARE STILL OPEN, ON PURPOSE, AND THE COMMANDER MUST RULE ON
THEM.** Gate 3.2b-R4 (the open-interest recorder, **ELEVEN** sabotages) PASSED
2026-07-29, exit 0, zero failure marks. Gate 3.2-R5 (funding, fifteen) and Gate
3.1-R5 (Fear & Greed, fourteen) still PASS — **and are both known to be
defeatable. They were not repaired.**

**WHAT THE SEVENTH INDEPENDENT REVIEW FOUND.** A session that built none of it
invented three new attacks and **all three escaped, all three predicted
correctly in writing beforehand.** The new question — the three previous ones
being spent — was ***the gate has an ear now; what is the ear itself deaf to?***

    S16  a logging handler bound to the real stderr at IMPORT time, or
         os.write(1, ...), walks straight past redirect_stdout, which only
         rebinds a NAME. 35 advice lines on the gate's own screen, three
         ticks underneath saying it wrote nothing ..................... ESCAPED
    F15  nothing anywhere watches what a module writes at IMPORT time,
         and brief.py imports both instruments. The advice is the FIRST
         line the gate prints, and the gate then passes itself ........ ESCAPED
    B11  'appended': len(fresh) for len(new_rows). The disk stays
         byte-perfect, so every detector is happy — only the printed
         REPORT lies, and that line is the one the Commander reads .... ESCAPED

**THE CLASS, in one sentence: THE GATE'S DETECTOR IS ITSELF CODE, AND IT HAS
BLIND SPOTS.** The check is present, green, correctly aimed — and deaf.

**B11 IS THE ONE THAT MATTERS MOST, AND IT WAS THE ONLY ONE REPAIRED.** Graded
**SERIOUS** on all three Step 2 questions: it happens by an ordinary typo, the
Commander cannot see it (180 looks exactly like a healthy month), and the weeks
of open interest lost while he believes it is being collected cannot be bought
back at any price. **The standing order on his desk is to judge the recorder by
that very line on 1 August.** Repaired under Gate 3.2b-R4, declared in `29ac18b`
with no `.py` in it; the attack re-run as a real text edit now fails with the
named diagnostic *"the report claims 180 row(s) appended — the gate counted 0
arriving on disk"*. Production half byte-identical by sha256, every diff hunk
inside `__main__`.

**S16 AND F15 WERE GRADED BORDERLINE AND DELIBERATELY NOT REPAIRED.** Under the
Commander's rule of 2026-07-28 a BORDERLINE finding is reported and stopped at;
the session recommends and he rules. **Filed as R-016, with the conflict of
interest stated: the session that graded them BORDERLINE is the session that was
thereby excused from fixing them.** Until he rules, **it remains true that a
single line of code in either instrument can put a trade instruction on the
Morning Brief with every gate green.**

**STEP 3.3 WAS NOT BUILT — deferred a fifth time**, because a SERIOUS finding
means fix it and stop. The Context Deck still stands at two instruments.

**R-001's condition has now never been met in SEVEN attempts.** Six generations
of gate have each been failed by the next pair of eyes; the seventh, 3.2b-R4,
was written today by the session that found the fault and is filed as R-017.

## The previous marker, kept for the record rather than erased

→ We were at: **PHASE 3 — THE GATES NOW WATCH THE CHANNEL THE BRIEF ACTUALLY
READS FROM, AND THE MONTH THE RECORDER ONLY EVER SEES ONCE.** Gate 3.2-R5
(funding, FIFTEEN sabotages), Gate 3.1-R5 (Fear & Greed, FOURTEEN) and Gate
3.2b-R3 (the open-interest recorder, TEN) all PASSED, 2026-07-28 night.
**Thirty-nine sabotages, thirty-nine caught — and THREE of the thirty-nine were
walking through green gates a few hours earlier.**

**WHAT THE SIXTH INDEPENDENT REVIEW FOUND.** A session that built none of it
invented three new attacks and **all three escaped, all three predicted correctly
in writing beforehand.**

**THE CLASS, in one sentence: A GATE CAN BE PERFECTLY HONEST ABOUT THE WRONG
OBJECT.** The previous five holes were all *the gate is looking at the right
thing and believing the wrong source*. This one is *the gate is looking somewhere
else entirely.*

    S15  funding's doorway PRINTS a trade instruction to stdout and returns
         the honest block unchanged. brief.py runs the function BEFORE it
         prints what the function returns, so it reached the pilot .... ESCAPED
    F14  the same in Fear & Greed — green in the same run that scored F7,
         "the disclaimer turned into ADVICE", as CAUGHT ............... ESCAPED
    B10  record() transposes the OI column ONLY when the file already
         exists. Every row-level check writes into an EMPTY directory,
         so the gate had only ever tested MONTH ONE ................... ESCAPED

**B10 IS THE ONE THAT MATTERS MOST.** Month one happens once; from month two
onward the monthly task takes the append path every single time, and **no check
had ever read a row back off it.** Built by hand: 80 of 180 rows landed 64,763x
wrong — the dollar value in the coin column — with all NINE sabotages scored
CAUGHT, **including B4, which is that exact lie.** B10 is B4 with one `if` in
front of it, on the one dataset Binance will not sell back at any price.

**THE REPAIR, SHIPPED THE SAME NIGHT**, declared in `46f95e5` with no `.py` in
it. Both instruments prove the doorway writes NOTHING to stdout or stderr on
EVERY path the pilot can see; the recorder builds month two for every asset the
gate names, reads every appended row back against its own raw fetch, **and must
prove it appended rather than passing on an already-complete window.** All three
original attacks, re-run as real file edits, now FAIL with named diagnostics.
Production halves byte-identical by sha256; every diff hunk inside `__main__`.
Brief 3/3, vault INTACT 6/6, `data/oi_history/` byte-identical.

**THE LARGER HOLE THIS FINDING SITS INSIDE IS STILL OPEN: `cockpit/brief.py`
HAS NO GATE AT ALL.** The instruments are now proved silent; nothing proves the
Brief itself prints only what they return. Filed as R-015 doubt 2.

**R-014 FAILED. R-015 is open against tonight's repair. R-001 has now outlived
FIVE FAILED generations of fix, and the sixth is untested** — it moves only when
a generation SURVIVES an independent attack, and none ever has. **Untested is not
the same as survived, and this ship counts it that way on purpose.**

---

## PREVIOUS MARKER, kept for the record rather than erased

→ We were at: **PHASE 3 — THE GATES NO LONGER TAKE THE MODULE'S WORD FOR WHAT
THEY ARE CHECKING.** Gate 3.2-R4 (funding, FOURTEEN sabotages), Gate 3.1-R4
(Fear & Greed, THIRTEEN) and Gate 3.2b-R2 (the open-interest recorder, NINE) all
PASSED, 2026-07-28 evening. **Thirty-six sabotages, thirty-six caught — and FOUR
of the thirty-six were walking through green gates earlier the same day.**

**WHAT THE FIFTH INDEPENDENT REVIEW FOUND.** A session that built none of it
invented four new attacks and **all four escaped, all four predicted correctly in
writing beforehand.**

**THE CLASS, in one sentence: A GATE THAT ASKS THE THING IT IS JUDGING WHAT THE
ANSWER SHOULD BE IS NOT A GATE.** Three constants that decided what each gate
expected were read straight out of the module under test, so corrupting one moved
the lie and the bar together.

    S14  funding's OFFLINE_WORDS reworded to carry a fabricated rate .. ESCAPED
    F13  the same in Fear & Greed: "72 - Extreme Greed" on a 29 - Fear day
                                                                       ESCAPED
    B9   SYMBOLS cut to two assets; SOL vanished from the recorder AND
         from its own detector .......................................  ESCAPED
    B8   `--record`, the branch the monthly task runs, is exercised by
         nothing; its exit code was made always-0 .....................  ESCAPED

**B9 IS THE ONE THAT MATTERS MOST.** Every loop in Gate 3.2b said
`for symbol in SYMBOLS`. Deleting one asset from the module deleted it from the
gate too: SOLUSDT stopped being recorded entirely, permanently, **on the one
dataset Binance will not sell back at any price**, and the gate printed PASSED
while announcing in its own words that it checks "ALL THREE assets". That is
B7's lesson one level up — B7 was *two of three assets guarded by a row count*;
B9 is *all three guarded by a list the module hands over.*

**THE REPAIR, SHIPPED THE SAME DAY**, declared in `f2be611` with no `.py` in it.
Both instruments hold `GATE_OFFLINE_WORDS` and the recorder holds `GATE_SYMBOLS`,
each compared to the module's constant by a **named** check; every loop in the
recorder gate runs over the gate's own list; and new check (j) runs `--record`
for real as a subprocess in **both** outcomes, against a copy in scratch so the
real history cannot be touched. **All four original attacks, re-run as real file
edits, now FAIL the gates with named diagnostics — each caught twice over.**
Production halves byte-identical by sha256; all 45 diff hunks inside `__main__`.
Verified after: Brief 3/3, vault INTACT 6/6, `lab/` and `data/oi_history/`
untouched.

**R-014 IS FILED AGAINST THIS REPAIR.** Fifth generation of the same structure:
the session that found the fault wrote the fix and graded it. **R-013 is FAILED,
not cleared. R-001 has now seen four generations of repair and still does not
move** — it moves when a generation SURVIVES an independent attack, and none has.

**WHAT IS STILL KNOWN-WEAK AND WAS NOT FIXED:** funding's **two-assets-fail**
block (`[no data: ETH, SOL]`) is built by no check anywhere; the recorder's check
(e) is still BTCUSDT-only; the 4h-boundary exposure is unwatched; B1 is a no-op
on a UTC machine.

**THE QUESTION THIS PHASE LEAVES FOR THE NEXT SESSION: the last two sessions
asked "which paths has nobody attacked?" and "where does the gate take the
module's word?" — both are now the directions these gates are STRONGEST in.
Bring a third question.**

---

**PREVIOUS MARKER, kept for the record:**

→ We were at: **PHASE 3 — EVERY PATH THE PILOT CAN SEE IS NOW HELD TO EXACT
EQUALITY, NOT JUST THE HEALTHY ONE.** Gate 3.2-R3 (funding, THIRTEEN sabotages),
Gate 3.1-R3 (Fear & Greed, TWELVE) and Gate 3.2b-R (the open-interest recorder,
SEVEN) all PASSED, 2026-07-28. **Thirty-two sabotages, thirty-two caught — and
FOUR of the thirty-two were walking through green gates that same morning.**

**WHAT THE FOURTH INDEPENDENT REVIEW FOUND.** A session that built none of it
did the ordered audit first — **it confirmed all six of the recorder's existing
sabotages fail for the reason their labels claim, so there is no second B5, and
that half of R-012 is genuinely clean.** Then it invented four new attacks and
**all four escaped, all four predicted correctly in writing beforehand.**

**THE CLASS, and it is one sentence: the gates rebuilt the whole output and
demanded exact equality ON THE HEALTHY PATH ONLY. Every degraded, offline or
secondary path was still guarded by asking whether an expected substring was
PRESENT, and by counting.** That is the exact question the 2026-07-27 rebuild
was written to abolish — **applied where the lesson was learned and nowhere
else.**

    S12  the funding meaning REVERSES when an asset is missing ... ESCAPED
    S13  the funding OFFLINE line carries a fabricated rate ...... ESCAPED
    F12  the Fear & Greed OFFLINE line fabricates a mood ......... ESCAPED
    B7   ETH and SOL recorded with BITCOIN's open interest ....... ESCAPED

**B7 IS THE ONE THAT MATTERS MOST.** `_disk_matches_source()` — the only check
in Gate 3.2b that compared what was WRITTEN to what Binance SERVED — was
hardcoded to BTCUSDT, as were checks (e) and (g). **For two of three assets the
gate only ever COUNTED rows.** A memo cache keyed on the timestamp instead of on
(symbol, timestamp) left BTC perfect while ETH went 22x wrong and SOL 80x wrong
for thirty days, **on the one dataset Binance will not sell back at any price**,
and the gate printed PASSED and exited 0.

**THE REPAIR, SHIPPED THE SAME DAY**, declared in `a8eddab` with no `.py` in it.
Funding's degraded block and both instruments' offline blocks are rebuilt from
the gates' own verbatim wording and compared for EXACT equality; F6 lost its
private weaker judge and now shares the real one; the recorder's detector and
plausibility check run for **all three symbols** and name which failed. **All
four original attacks, re-run as real file edits, now FAIL the gates with named
diagnostics — B7 twice over, by two checks not designed together.** Production
halves byte-identical by sha256 (funding 1-159, fear_greed 1-112,
open_interest 1-242); all 63 diff hunks inside `__main__`. Verified after:
Brief 3/3, vault INTACT 6/6, `lab/` and `data/oi_history/` untouched.

**R-013 IS FILED AGAINST THIS REPAIR.** Fourth generation of the same structure:
the session that found the fault wrote the fix and graded it. **R-011 and R-012
are FAILED, not cleared. R-001 has now seen three generations of repair and
still does not move** — it moves when a generation SURVIVES an independent
attack, and none has.

**THE QUESTION THIS PHASE LEAVES FOR THE NEXT SESSION, in one line: every gate
here should now be read with "WHICH PATHS HAS NOBODY ATTACKED?"**

---

**PREVIOUS MARKER, kept for the record:**

→ We were at: **PHASE 3 — THE GATES NOW CHECK THE WORDS, NOT JUST THE DIGITS.**
Gate 3.2-R2 (funding) PASSED and Gate 3.1-R2 (Fear & Greed) PASSED, 2026-07-27.
**Twenty-two sabotages, twenty-two caught — and SEVEN of the twenty-two were
walking through green gates that same morning.**

**WHAT THE THIRD INDEPENDENT REVIEW FOUND.** A session that built neither
instrument, neither gate, nor either repair threw ten new sabotages and **seven
escaped.** The worst printed `positive = shorts pay longs` — **the exact
opposite of how the market works** — beside three perfectly correct numbers,
while the gate reported PASSED. Another printed `>> strong buy signal` on the
Context Deck of a ship whose first rule is INFORMATION, NEVER A SIGNAL. **THE
CLASS: every check asked whether an expected string was PRESENT; none asked
whether anything ELSE was present, and none checked the fixed words at all.**
The previous rebuild closed the hole for DIGITS and left it open for WORDS.

**THE REPAIR, SHIPPED THE SAME DAY.** Both gates now rebuild the WHOLE printed
block from the source and require EXACT equality, holding their own verbatim
copy of every fixed sentence; the partial-failure drill rotates through all
three assets; the Fear & Greed gate holds its own `HISTORY_LIMIT` (reading the
module's had silently disarmed one of its own detectors). **All ten original
attacks, re-run as real file edits, are now CAUGHT.** Production halves
byte-identical by sha256 — funding lines 1-159, fear_greed lines 1-112, so what
the Brief prints cannot have changed. Verified: Brief 3/3, both instruments, one
deck header, vault INTACT 6/6, `lab/` untouched.

**THE KNOWN GAP RECORDED HERE YESTERDAY — the unguarded disclaimer text — IS
NOW CLOSED on both instruments.**

**R-011 IS FILED AGAINST THIS REPAIR.** Third generation of the same structure:
the session that found the fault wrote the fix and graded it.

**AND THE SAME DAY, ON THE COMMANDER'S EXPLICIT DIRECTION, STEP 3.2b WAS BUILT:
GATE 3.2b PASSED, all nine bars, all six sabotages caught, and 540 rows of the
open-interest window are recorded and pushed.** One new file
(`data/open_interest.py`) and one new directory (`data/oi_history/`); **no
existing file was modified at all.** `THE_PATTERN.md` says Part 2 is conditional
and a session that finds a real problem stops — **the Commander directed
otherwise and that is recorded as his call, not a session's drift.** It was a
safe call: the recorder touches no cockpit file and does not build on the repair
under review.

**THE 30-DAY WINDOW IS NO LONGER EXPIRING UNRECORDED.** BTC/ETH/SOL,
2026-06-27T16:00Z → 2026-07-27T12:00Z, 180 rows each, idempotent on re-run.
**AND IT IS NOW SCHEDULED**, on the Commander's instruction: task
`ZarX Open Interest`, day 1 of every month, 09:00, on his laptop — never the
cloud watchman, whose US-hosted runners Binance geo-blocks. It catches up if the
laptop was off, runs on battery, and preserves the rows to GitHub and OneDrive.
**`schtasks` reported SUCCESS while creating a BROKEN task** (it split the path
at the space in "zargul trader"); caught by running it and reading the log, not
by trusting the report. **The commit-and-push branch has still never fired
against real new rows — the first run after 1 August is its test.**

**NOTHING IS CERTIFIED. R-001, R-002, R-004, R-008, R-009 and R-010 are FAILED;
R-006, R-007, R-011 and R-012 are OPEN.** Both of today's deliverables were
built and graded by the same session that wrote them.

**NEXT SESSION, IN ORDER, AND IT IS ALL ATTACK: (1) a TWELFTH sabotage against
each Context Deck instrument — R-011; (2) a SEVENTH against the open-interest
recorder, plus a check that each of its six existing sabotages fails for the
reason its label claims — R-012, and this matters because one of them was found
being scored CAUGHT while never reaching the check it was meant to prove.**
**No new part is built until both are attacked.**

---

**YESTERDAY'S POSITION, KEPT FOR THE RECORD:** Gate 3.2-R (funding) PASSED,
Gate 3.1-R (Fear & Greed) PASSED. R-008 confirmed the defect is a CLASS, measured on two
independently built instruments: every check interrogated the parse, none
compared the printed sentence to the source. Fear & Greed leaked **5 of 6** —
`70 — Fear` printed as a contradiction on its own face while every check passed.
**Both repairs touched ONLY the `__main__` block of their file** (funding: every
diff hunk ≥ line 160; Fear & Greed: ≥ line 113), so both production paths are
byte-identical and what the Brief prints cannot have changed. Verified: Brief
3/3, both instruments, one deck header, vault INTACT 6/6.

**NOTHING IS CERTIFIED. R-001, R-002, R-004 and R-008 are FAILED; R-009 and
R-010 are OPEN.** Every one of the twelve sabotages was invented by the session
that then defended against it. **NEXT SESSION, IN ORDER: (1) a SEVENTH sabotage
against each instrument, by someone who built neither — that is R-009 and R-010,
and it is what unblocks R-001; (2) Step 3.2b, the open-interest recorder, whose
orders and Gate 3.2b are written and measured in SESSION_ORDERS.md and whose
30-day window is still expiring.**

**KNOWN GAP, NEITHER INSTRUMENT COVERS IT:** nothing checks the fixed
disclaimer text — *"information, not a signal"*, *"positive = longs pay
shorts"*. Both could be edited or deleted and no gate would notice. Filed in
R-010. **— CLOSED 2026-07-27 by Gates 3.2-R2 / 3.1-R2, after it was
demonstrated rather than merely suspected: the reversed sentence printed and
the gate passed. Left here unedited because a gap that was known for a day and
not closed is part of the record.**

---

**EARLIER TODAY, KEPT FOR THE RECORD:** **THE INSPECTOR WAS FIXED. GATE 3.2-R
PASSED 2026-07-26
(21 checks in the program + 4 verified in the shell), and ALL SIX deliberate
sabotages are now CAUGHT — including the four that walked through the old gate
the same morning. The repair touched ONLY the `__main__` block of
`cockpit/funding.py`: every diff hunk begins at line 160 or later, so the
production path is byte-identical and what the Brief prints cannot have
changed. Verified: Brief still 3/3, both Context Deck instruments, one header.**

**BUT R-001 IS NOT CLEARED, AND STEP 3.2 IS NOT CERTIFIED.** The session that
found the fault wrote the repair and graded it. **R-009 is filed** so someone
who did not build it invents a SEVENTH sabotage — because a gate built from a
known list of attacks is strongest exactly where it has already been attacked.

**NEXT SESSION, IN ORDER: (1) R-008 — run the same sabotage exercise against
`cockpit/fear_greed.py`, which is built the same way and has never been checked
for this class of hole; (2) Step 3.2b, the open-interest recorder, whose orders
and Gate 3.2b are already written and measured in SESSION_ORDERS.md and whose
30-day window is still expiring.**

**ON THE COMMANDER'S DESK, UNDECIDED, NOT TAKEN BY DEFAULT:** tighten
`MAX_PLAUSIBLE_RATE` from 0.05 to ~0.01 (measured: the real cap is 0.003–0.00375)
· print the last settled rate on the Brief as a checkable anchor (R-004) · three
law candidates, the newest being *"a check is not proven until it has been
deliberately broken."*

---

**THE MORNING'S POSITION, KEPT FOR THE RECORD:** **STEP 3.2 WAS REOPENED. THE
AUDIT RAN 2026-07-26 AND
DID NOT CLEAR: 3 of 5 bars passed, 1 partial, and BAR 5 (Exhibit A, the
sabotage test) FAILED — 4 of 6 deliberate breakages walked through Gate 3.2
while it reported 48/48. THE 48/48 TALLY IS VOID. Step 3.2b (the open-interest
recorder) was NOT started, exactly as the orders required.**

**WHAT IS AND IS NOT BROKEN.** The funding numbers on the Brief are CORRECT —
re-derived independently against Binance the same day, sign and magnitude
matching digit for digit. **The defect is in the GUARD, not the output:** every
check verified what happens before the printed string is assembled, and nothing
verified the string itself. A sign-flipped `_fmt_pct`, a dropped ×100, a
timezone-less `_utc_hhmm` and a miswired contract map all passed. **The funding
line was deliberately NOT removed from the Brief** — that is on the Commander's
desk, because removing a line proven correct on the authority of a clause
written by the session under audit would be obedience to wording over meaning.

**NEXT SESSION: rebuild Gate 3.2 around what the pilot READS, not what the
parser returns — a check that compares the printed STRING to an independently
derived string, plus the sabotage exercise made PERMANENT rather than a one-off
audit. Then, and only then, Step 3.2b.** Full verdicts in `REVIEW_QUEUE.md`
(R-001 FAILED, R-002 FAILED, R-003 CLEARED, R-004 FAILED, R-005 CLEARED, R-007
and R-008 newly filed) and in the `PROGRESS_LOG.md` audit entry.

**Gate 3.2b and its orders remain written and valid in SESSION_ORDERS.md, with
every claim about the OI endpoints MEASURED first. The 30-day open-interest
window is still expiring; that deadline did not pause for this audit.**

**Gate 3.2b's endpoints were probed BEFORE the gate was written** — applying
the same morning's lesson that gates get written from assumption too. The find
that shaped the gate: **a bogus symbol on `/futures/data/openInterestHist`
returns `HTTP 200` with an empty list `[]`, not an error** (the funding
endpoint returns a clean HTTP 400 for the same mistake). A recorder written the
obvious way would report success while collecting nothing, every month, until
the 30-day window had silently rolled past — on the one dataset that cannot be
recovered later at any price. Gate 3.2b check (c) exists solely for that.

**Step 3.2 (Funding rates) DONE 2026-07-26, GATE 3.2 PASSED 48/48** (10 in the
instrument's own smoke test, 38 in the gate runner). `cockpit/funding.py` (new)
+ 5 wiring lines in `cockpit/brief.py` were the only code touched; `lab/`
byte-identical, vault INTACT (6/6 checksums). The Context Deck now carries TWO
instruments under ONE header, independently killable in every combination.
Live that day: BTC +0.0059% · ETH +0.0018% · SOL +0.0014% per 8h, next
settlement 16:00 UTC. Source: Binance USDⓈ-M public API, free, keyless, no new
dependency — **an open-source funding library was offered twice and declined
both times**, because Binance answered HTTP 200 throughout and a wrapper would
add a breakable dependency (the pandas-ta lesson) while hiding the schema the
orders require us to record.

**THE THING THIS STEP WILL BE REMEMBERED FOR: Gate 3.2's check (b) — the one
check standing between this ship and printing the opposite of the truth every
morning — was UNPASSABLE AS WRITTEN, and was corrected before any code
existed.** The orders assumed `premiumIndex.lastFundingRate` IS the last
settled rate; measured, it is not — it is the running estimate for the NEXT
settlement, a different quantity, so "same number within rounding" could never
have passed for any correct implementation. The weaker fallback of "at least
the signs agree" was measured too and is also invalid: settled signs ran
`+ − +` for ETH and `− + +` for SOL, so that check would have failed at RANDOM
on correct code. Check (b) was replaced with three stricter checks (b1 exact
identity digit-for-digit, b2 hand re-derivation of every printed number, b3
the meaning proven from Binance's published documentation, since no endpoint
can prove a naming convention) — **written and committed alone, in commit
cbfcff4, before `cockpit/funding.py` existed.**

**The lesson generalises the previous session's, one step further: gates get
written from assumption too.** Last time an untested claim about a FUTURE
step's data rode through a passing gate. This time the untested claim was
inside THIS step's own gate, in its single most important check, and every
other check would have passed around it — (a) (c) (d) (e) (f) all verify that
a number appeared and that failure degrades honestly, never that the number
means what the line beside it claims.

**Independence note, carried forward and now WEAKER, not stronger:** last
session the planner and builder were the same mind. This session that same
mind also amended the gate it would be judged by, at the Commander's explicit
delegation. The surviving protections are that the amendment landed first with
its evidence attached, and that **a THIRD fresh session must review by
recomputing from raw evidence — and must audit the amended check (b) itself
rather than assume it.** The Phase 6 second-AI requirement remains NOT waived.

Previously:

**CORRECTION, same day, before 3.2 was built:** this marker previously ended
"funding recording to CSV starts the day 3.2 ships." **That was false** —
inherited from the Slot 2 line above, repeated into the Step 3.1 log and
commit message, and never tested by anyone until the 3.2 planning session
probed the API. Binance serves ~7 years of settled funding on demand, so
**funding needs no recording at all.** The instrument that genuinely expires
is **open interest — a 30-day window, nothing older is served** — and it gets
its own step, 3.2b. Because each read reaches back 30 days, a recorder running
even monthly loses nothing: a deadline in weeks, not an emergency. Left here
in full, mistake included, because a plan that quietly edits its own errors
teaches the next session nothing.

**Step 3.1 (Fear & Greed) DONE 2026-07-26, GATE 3.1 PASSED 45/45 on the first
run.** `cockpit/fear_greed.py` (new) + 4 wiring lines in `cockpit/brief.py`
were the only code touched; lab/ byte-identical, vault INTACT. The Brief's
CONTEXT DECK now prints the crowd-mood gauge (live that day: 26 — Fear,
yesterday 27, a week ago 28, cross-checked against alternative.me's own web
page, 4 of 4 matching). The offline drill points an injectable base URL at an
unresolvable `.invalid` host: the instrument degrades to one line and the
Brief still reports 3/3 assets. **No CSV recording was built and none is
needed** — alternative.me serves its whole history on demand (`limit=0`).
**Step 3.2 is the opposite case: Binance does NOT serve deep funding history,
so funding recording to CSV must start the day 3.2 ships, or Phase 6's Slot 2
cannot be tested.** Full entry in PROGRESS_LOG.md.

Phase 2, for the record:
Step 2.5 (`lab/gate_2_5.py`) PASSED 37/37, run twice byte-identical, after
the Commander's decision resolved its one honest blocker. The full story is
in PROGRESS_LOG.md (three entries: the finding, the independent review, the
decision); the short version every future session must know:
- **The Lab catches overfitting, proven end to end.** The synthetic con
  artist (1,687-cell lookup memorised from train candles only, no RNG):
  train card PF 4.26 / win 77.2% / +361.67% (too-good alarm FIRED), hold-out
  PF 0.69 / -19.59%, walk-forward INCONSISTENT (1 of 6 windows), locked
  battery verdict **NOT CERTIFIED** (2 of 4 bars failed).
- **The Lab's numbers can NEVER catch a leak, and the alarm may stay silent
  too — MEASURED, not assumed.** `PerfectForesight` (reads tomorrow's candle)
  cleared all 4 locked bars (PF 1.39, 203 trades, walk-forward CONSISTENT
  6/6, MC 8.01%) and the too-good alarm stayed SILENT (1.39 < 2, 57.6% < 70).
- **LAW 7 — THE LEAK LAW — now stands in SHIP_LAWS.md:** mandatory recorded
  code-reading before any certification; `lab/leak_check.py` (new instrument,
  own smoke test; flags the leak's smuggled `strategy.full` DataFrame, clears
  the honest strategies) runs as the reading's aid, never its substitute; the
  alarm was NOT lowered. Gate 2.5's Step 6 now asserts the measured silence —
  if that check ever fails, the ground moved and Law 7 must be re-examined.
Phase 3 was not started by the Phase 2 sessions (per the standing order not
to, even on a quick pass); it opened with Step 3.1 above.
Step 2.1 (Frozen Vault) DONE 2026-07-26, GATE 2.1 PASSED.
Step 2.2 (Data Validator) DONE 2026-07-26, GATE 2.2 PASSED first run.
Step 2.3 (Backtest Engine) DONE 2026-07-26, GATE 2.3 PASSED.
Step 2.4 (Lie Detectors) DONE 2026-07-26, GATE 2.4 PASSED first run, 35/35
checks. The MA-cross dummy's hold-out card reproduced Gate 2.3 exactly.

**What Step 2.5 must bolt onto (the three instruments, all built on the
engine's output and all using `return_pct`, never dollars):**
- `lab/walk_forward.py` — `walk_forward(result, window='holdout')` for an
  engine result, `walk_forward_trades(df, index=None)` for any trade table.
  Returns a report with `.text()`, `.verdict` (CONSISTENT/INCONSISTENT),
  `.consistency_ok`, `.lucky_window_flag`, `.windows`. Non-overlapping
  windows (each trade counted once, or shares of profit are fiction). If the
  total is <= 0 the concentration test is REFUSED in words, never divided.
- `lab/monte_carlo.py` — `monte_carlo_result(result)` / `monte_carlo(returns)`.
  **RECORDED SEED: 20260726**, printed in every report; identical across
  processes. Judge on `dd_p95` (the 5th-percentile-worst drawdown) vs the
  30% ruin line; `ruin_flag` carries the verdict.
- `lab/regime_report.py` — `regime_report(result)`. Information only.
- `lab/trade_stats.py` — the one shared `summarise(trades)`; the Lab has a
  single definition of profit factor and drawdown so they cannot drift.

**What Step 2.4 bolted onto:** `lab/engine.py`, contract
`signal(df) -> long|short|flat`, entered via `load_vault(asset, timeframe)`
(the ONLY door — it refuses any path outside lab/vault/ and any file the
validator FAILs). `run_backtest(...)` returns a BacktestResult with
`.card('holdout'|'train'|'full')`, `.window_trades(window)` and
`.save_csv()`. The MA-cross dummy for Gate 2.4 is `lab/dummies.MACross(20,50)`;
run it with `train_end='2025-10-01'` to reproduce the Step 2.3 card exactly.
Per-trade CSVs already carry `regime_at_entry` (for regime_report.py) and
`return_pct` — each trade's net result as a fraction of the equity it
started with, so any subset of trades (a walk-forward window, a Monte Carlo
reshuffle) can be compounded honestly on its own. Use `return_pct`, never
raw dollars, when slicing trades into windows.

**HOLD-OUT LINE, RECORDED: train_end = 2025-10-01** (~10 months / 1,789
4h candles of untouched hold-out). Every Step 2.3 gate number is on that
line; Step 2.4 must use the same one or say loudly that it changed.

**OPEN ITEM FOR THE COMMANDER (found by Gate 2.3's hand-check, not yet
acted on — it is doctrine, not a bug):** on BTC 4h the 1.5-ATR stop is
~1.9% wide, so risking 1% of the account implies a position worth ~80% of
it. `RISK_CONFIG['max_position_fraction']` caps that at 25%, and the cap —
not the 1% rule — set the size on 116 of 119 trades. Actual risk taken:
**~0.49% per trade, not 1%.** The engine is faithfully running the LIVE
formula, so live behaves the same way. Nothing was changed. But it means
every return AND every drawdown in the Lab is on roughly half the intended
risk, and the Phase 6 gate "must beat buy-and-hold-with-1%-risk-sizing"
needs to know which number it is comparing. Decide before Phase 6, not
after seeing results.
Vault v2 healthy at birth: 4h from 2024-01-01 (~2.6y, source glitch zone
excluded, see log), 1d full 3y.
Vault v2 born 2026-07-26 (commit below), all four gates passed: 6 files
(4h 5,624 rows each from 2024-01-01; 1d 1,094 each from 2023-07-28),
verify INTACT twice identically, validator reports ZERO FAIL verdicts,
gate_2_2 still passes. `validated_at_birth: true` is in the MANIFEST.

**The 4h window starts at 2024-01-01 and that is permanent.** TwelveData's
stored 4h history before then carries 48 decimal-point-glitch candles
(last one 2023-12-20), proven reproducible — re-downloading is DEAD as a
fix, do not attempt it again. The MANIFEST carries the reason in its own
`vault_4h_start_reason` field. The 1d files were healthy and kept the
full 3 years; asymmetric depth is intentional, not an oversight.
Open items carried forward: (1) Commander still to rotate the TwelveData
key (.env + GitHub secret); (2) vault CSVs carry NO volume column —
TwelveData returns none for these crypto pairs; OHLC only. Any future
tool that needs volume must be told this first.
