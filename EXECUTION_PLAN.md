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
3. News headlines (CryptoPanic free tier) — headlines ONLY, no sentiment
   score, no invented weights (the cut ghost stays cut).
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

→ We are at: **PHASE 3 — THE INSPECTOR IS FIXED. GATE 3.2-R PASSED 2026-07-26
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
