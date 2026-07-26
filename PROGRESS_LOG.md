# ZAR X — Progress Log

Every build step, every test, every result — wins and losses alike.

---

## 2026-07-19 — THE KEEL IS LAID

Zar X founded. Name chosen by the Commander. Repository initialized, seven compartments
created (`data/ indicators/ regime/ signals/ risk/ lab/ cockpit/`), founding documents
written: README.md (mission + THE PROMISE) and EDGE_STACK_RESEARCH.md (full design
research from the final Fable session).

**Inheritance from Zargul Trader 2.0** (museum repo, tag `prediction-chapter-closed`):
- The verdict that founded this ship: LSTM price prediction has no extractable edge
  (BTC 1h -3.17, BTC 4h -2.25, ETH 4h -0.72, SOL 4h -0.66 — all full-year hidden exams)
- The honest-lab methodology: chronological validation, hold-out cutoffs, per-trade
  CSV X-rays, regime recalibration by calibration-period percentiles
- Proven organs to port in Stage 1: data engine (paginated, 429-proof), indicators,
  regime filter, risk engine, backtest lab, journal

**Next:** Stage 1 Phase 0 — port `data/` module + smoke test. Deliverable gate:
one command prints live BTC/ETH/SOL candles.

## 2026-07-19 — GitHub home + Ship Laws

Repo connected and pushed: github.com/zargul123/zar-x (branch main). SHIP_LAWS.md added —
the Commander's six laws: everything recorded with results and reasons; code in isolated
parts; fail-safe parts with smoke tests; gates before tests; explain-then-commit; THE PROMISE.

## 2026-07-19 — Amendment 1: Layer 7 Carry Monitor, Build Order A

Kimi's structural-edge contribution adopted (funding carry monitor as instrument, not
prediction). Build order fixed: Hull → Carry Monitor → context instruments → gauntlet
slots last. Win%×payoff−costs reading law recorded. Phase 0 (data compartment port)
begins now. Gate: one command prints live BTC/ETH/SOL candles.

## 2026-07-19 — PHASE 0 COMPLETE: data compartment alive (GATE PASSED)

Ported from museum: TwelveData fetch (429-retry, 65s wait), pagination with 8s pacing,
Yahoo fallback, hold-out end_date cutoff — into `data/market_data.py` (clean candles ONLY;
indicators deliberately left for their own compartment per Law 2). `config.py` created as
single source of settings; `.env` key installed (gitignored). Fail-safe pattern in place:
"DATA INSTRUMENT OFFLINE" instead of crashes.

**Gate result:** `python data/smoke_test.py` → live candles for all three assets
(BTC $64,510.71 / ETH $1,869.61 / SOL $76.12 at 2026-07-19 12:00). PASSED.

**Next:** indicators/ compartment port + smoke test.

## 2026-07-19 — Part 2: indicators/ compartment (GATE PASSED)

Ported the proven Elite indicator set (rsi, macd, bbands, adx, mfi, atr + cores=0 memory
fix) from the museum, added ema_20/50/200 for Brief trend state, kept time features and
cleanup order. Fail-safe: returns candles untouched + "INDICATORS INSTRUMENT OFFLINE" on
error. CORE_COLUMNS contract published for consumers.
**Gate:** live BTC 300 candles → all 12 core columns, RSI 54.8 in range, ATR $497 positive,
trend check works (price ABOVE EMA-200). PASSED.
**Next:** risk/ compartment (SL/TP/size calculator) port.

## 2026-07-19 — Part 3: risk/ compartment — the Discipline Engine (GATE PASSED)

Ported from museum RiskManager: ATR calc + ATR-based SL/TP levels (faithful). Sizing
UPGRADED to the stop-distance formula (size = risk money / stop distance — the math that
makes ~40%-wrong survivable), with a 25% max-position cap. Deliberately NOT ported, with
reasons: trailing stop (2026 data showed it cut winners/kept losers), should_execute
(dead AI-prediction pipeline). RISK_CONFIG added to config.py (1% risk default).
**Gate:** live BTC long plan on $1000 → SL<entry<TP, R:R 1.33 as configured, cap engaged
correctly ($250 position, $2.49 risk). PASSED.
**Next:** regime/ compartment (vane with per-timeframe calibration).

## 2026-07-19 — Part 4: regime/ compartment — the weather vane (GATE PASSED)

Ported with three lessons applied: per-timeframe entropy dials (4h = calibrated 1.96;
1h = 1.5), fail-honest "Uncalibrated" for undialed timeframes, stateless per-reading
replay (fixes the museum's shared-EMA cross-asset contamination bug). HONEST STATUS in
docstring: context instrument, NOT proven alpha (failed fresh-year P&L rescue test).
**Gate:** live BTC 4h → "Ranging" (entropy 1.952 vs dial 1.96, ADX 23.3); 1d correctly
answers "Uncalibrated". PASSED.
**Next:** lab/ (honest backtester redesigned around rule-signals) OR cockpit Morning Brief.

## 2026-07-19 — Part 5: THE MORNING BRIEF IS ALIVE (Stage 1 core deliverable)

`python cockpit/brief.py` → full live briefing, 3/3 assets: price + 24h change, trend
state (EMA50/200), RSI momentum, ATR volatility, weather reading (calibrated vane), and
a disciplined example risk plan per asset. Assembled purely through compartment doorways;
offline instruments self-report without stopping the Brief.
**First-ever live Brief (2026-07-19 20:41):** BTC $64,580 UP-trend Ranging; ETH $1,874
UP-trend Chaotic; SOL $76.24 MIXED Chaotic. All instruments reporting.
**Stage 1 status:** data ✅ indicators ✅ risk ✅ regime ✅ Brief ✅ — remaining: lab/ port
(honest backtester redesigned around rule-signals) + journal, then Layer 7 Carry Monitor.

## 2026-07-19 — Part 6: journal/ snapshots — the black box (GATE PASSED)

`python journal/snapshot.py` appends one row per asset to journal/snapshots.csv:
UTC time, price, trend state, RSI, ATR(%), regime reading. Purpose: score the
instruments against reality later ("said UP on the 15th — what happened?"). First
entries recorded live (BTC UP/Ranging, ETH UP/Chaotic, SOL MIXED/Chaotic).
User's daily ritual (Pakistan time): run Brief + snapshot ~09:05 PKT (after the
09:00 candle close; timestamps inside are UTC = PKT-5).
**Next:** lab/ (honest backtester around rule-signals), then trade-logging half of the
journal, then Carry Monitor.

## 2026-07-19 — Part 7: Automation — Zar X runs itself (GATE PASSED)

Windows Task Scheduler registered: "ZarX Morning Brief" daily 09:05 PKT (full ritual:
Brief + snapshot -> journal/daily_runs.log) and "ZarX Evening Snapshot" daily 21:05 PKT
(extra evidence row). run_daily.bat / run_snapshot.bat added (ASCII/CRLF endings — cmd
chokes on LF-only bats, fixed and re-gated: zero errors). Limitation recorded: laptop
must be on and awake at run time; missed runs are skipped (manual run any time is valid).
Reading the log: use UTF-8 (e.g. `Get-Content journal\daily_runs.log -Encoding UTF8`).

## 2026-07-19 — Snapshots at every 4h close + ROADMAP.md handoff

Commander's request: snapshot cadence raised from 2x to 6x daily — Task Scheduler now
fires run_snapshot.bat at every 4h candle close (01:05/05:05/13:05/17:05/21:05 PKT,
morning 09:05 covered by the full ritual). API cost ~18/800 daily credits. ROADMAP.md
written: complete state, build queue (lab → grader → Context Deck → Carry Monitor →
sealed gauntlet), standing answers, daily ritual, provenance — the single handoff
document for any future session/model.

## 2026-07-19 — Automation incident & fix: the missing-quotes trap (RESOLVED, verified by fire)

The first scheduled run (21:05) failed with 0x80070002 "file not found": schtasks stored
the bat path WITHOUT quotes, so Windows read it only to the first space ("...\zargul").
Fix: all six tasks recreated via native PowerShell cmdlets (Register-ScheduledTask) with
Execute=cmd.exe, Arguments=/c "quoted path" — immune to spaces. Verified by test-firing
through the real scheduler: snapshot wrote 3 rows autonomously at 21:10 PKT
(BTC $64,522 UP/Ranging; ETH $1,869 UP/Chaotic; SOL $76.05 MIXED/Chaotic) — Zar X's
first fully autonomous action.

## 2026-07-19 — Part 8: the Trade Planner (GATE PASSED)

Commander's feedback: "trend UP alone is nothing — where is my stop loss?" → built
cockpit/plan.py: the pilot states asset/direction/capital (+optional risk% and entry),
Zar X answers the full disciplined plan from live data: SL, TP, exact size, money lost
if wrong, gained if right, weather context. Clarified the two outputs: snapshots = the
science notebook (for the future grader), the Brief + Planner = the pilot's tools.
**Gate:** live plan for long BTC on $500 → SL/TP correct sides, 25% cap engaged,
loss-if-wrong $1.41 (0.28% of capital). PASSED.

## 2026-07-19 — Part 9: THE GRADER — the system now checks itself (GATE PASSED)

ROADMAP queue item #2 (first half) built on Commander's request: run the existing system
7 days and have it verify its own basic readings automatically. journal/grader.py scores
every snapshot trend claim (UP/DOWN) against what price actually did 6 candles (24h)
later; MIXED rows carry no claim; young rows honestly reported as "not yet gradable".
Wired into the 09:05 daily ritual — every morning: Brief → snapshot → self-exam, all in
daily_runs.log. **Gate:** first run correctly reports 12 claims / 0 gradable / "come back
after 24h" — fail-honest behavior verified. First real grades appear 2026-07-20+.
**7-day observation plan:** system self-grades daily; Commander may ask "zar x, review
the journal" any day; full week-1 review ~2026-07-26. Build queue continues unchanged
(lab next) in parallel sessions.

## 2026-07-19 — Automation upgrade: catch-up on wake

All six scheduled tasks set to StartWhenAvailable=true: if the laptop was closed/asleep
at an alarm time, the run fires automatically the moment the laptop wakes. Missed-hour
gaps remain harmless (grader scores whatever rows exist); no user action ever needed.

## 2026-07-20 — Part 10: the Cloud Watchman (deployed; gate pending secret)

Commander's request: snapshots must not depend on the laptop. GitHub Actions workflow
(.github/workflows/cloud_snapshot.yml) runs journal/snapshot.py on GitHub's own runner
at every 4h candle close (+5min, UTC cron) and commits new evidence rows back to the
repo — viewable from the phone anywhere via the GitHub app/site. requirements.txt added
for the cloud runner. Laptop ritual continues in parallel (double coverage; snapshot
timestamps make duplicates harmless).
**Gate (pending):** requires TWELVEDATA_API_KEY added by the Commander as a GitHub
Actions secret, then one manual workflow run must commit rows. Mobile OneDrive sync of
local reports also added to both runner bats (OneDrive\ZarX).

## 2026-07-20 — Incident: 01:05 snapshot skipped on battery (RESOLVED, verified)

The 01:05 PKT alarm did not fire despite the laptop being awake: Windows' default task
condition "do not start if on batteries" blocked it (laptop was unplugged). Fix:
DisallowStartIfOnBatteries and StopIfGoingOnBatteries set to false on all six tasks.
Missed shot fired as catch-up: success (result 0), rows landed 01:32 PKT (BTC $64,501
UP/Ranging; ETH $1,864 UP/Chaotic; SOL $75.96 MIXED/Chaotic). Also this session:
OneDrive mobile sync in both bats (OneDrive\ZarX) and the Cloud Watchman workflow
(pending user's GitHub secret + test run).

## 2026-07-20 — Cloud fix: vendored pandas_ta (zero-behavior-change option)

Cloud install failed because pandas-ta 0.3.14b0 is no longer served by PyPI (only 0.4.x
for Python >=3.12 exists). Chosen fix per Commander's "no morning surprises" rule:
vendor the EXACT library copy from the laptop's environment into vendor/pandas_ta
(0.86 MB, verified importable and version 0.3.14b0). Cloud workflow points PYTHONPATH at
vendor/; requirements slimmed. Local system untouched — indicators smoke gate re-run to
confirm: PASSED unchanged.

## 2026-07-20 — THE CLOUD WATCHMAN IS ALIVE (GATE PASSED)

After four honest onion layers (dirty-worktree ordering bug → PyPI no longer serves
pandas-ta 0.3.14b0 → vendored the laptop's exact library copy → patched its non-fatal
version lookup), the workflow ran green: commits 22f9b35/661a6cb authored by
zarx-cloud-watchman — GitHub's runner fetched live data and committed snapshot rows
autonomously (21:03/21:04 UTC). Zar X now has a redundant watch: laptop Task Scheduler
(6× daily + Brief + grader at 09:05) AND cloud every 4h independent of the laptop.
Evidence viewable from mobile: GitHub app → zar-x → journal/snapshots.csv. Known
cosmetic: Node.js deprecation annotation from GitHub's own actions — harmless, bump
checkout/setup-python versions in a calm session.

## 2026-07-20 — CHECK_STATUS.bat: one-click health check

Double-click shows: each laptop alarm's last run time with OK/never/error-code verdict,
the six newest black-box rows, and the reminder that the cloud guard is checked at the
repo's latest-commit line on GitHub. Window stays open until a key is pressed.

## 2026-07-20 — Cloud self-grading (Commander's design insight)

Commander spotted the gap: the cloud gathers the most complete diary (laptop sleeps;
cloud doesn't) but only the laptop graded. Cloud workflow now runs the Grader after
every snapshot and commits journal/cloud_grader_report.txt — an always-fresh graded
report card on the GitHub page, phone-readable. Laptop keeps grading its own diary at
09:05; Friday's review merges both. Two watchmen, both now self-examining.

## 2026-07-20 — MASTER PLAN v1 (brainstorm, agreed)

Visual artifact: claude.ai/code/artifact/edd0e5a4-34c4-493e-9f0f-4c87db3fc204
Synthesized from our roadmap + Kimi's detailed build manual + user's decisions.

**Nine phases:**
0. Foundation — DONE (the 7 live compartments + automation)
1. Honesty Check — NOW. + Data Validator; + old LSTM as a silent GRADED observer.
   (Regime v2 complexity — Hurst/fractal/voting — HELD until this evidence speaks.)
2. The Lab — sealed-vault data split, walk-forward, cost simulator, Monte Carlo,
   regime breakdown, lie detector. Gate: must catch a deliberately-bad dummy strategy.
3. Context Deck — fear&greed, funding, news headlines, event calendar, war-warnings.
   Shown as RAW pieces, NOT a fake-precise blended score. (Fixes the war blind spot.)
4. Carry Monitor — delta-neutral funding carry; structural income, no gauntlet needed.
5. Trade Logger & Mirror — one-command log, psychology tracking, monthly you-vs-system.
6. The Gauntlet — 3 sealed trials (Turtle / Funding-fade / Cycle), gates locked BEFORE
   testing (Kimi reviews). Only survivors give real buy/sell signals.
7. Proving Voyage — paper trading at the pilot's pace. USER DECISION: NO 4-trades/month
   cap (system informs, never blocks). 1% risk shown, not forced. Learning = human review
   only, never silent auto-tuning.
8. Permanent Loop — daily brief → decision → track → monthly review, for years.

**Three-Voice Courtroom:** ZarX instruments + old LSTM observer + gauntlet survivors,
all graded side by side, all silent until proven.

**Two ghosts CUT (with reasons):** (a) self-tuning autopilot — with ~50 paper trades/yr
you fit noise; the LSTM had 26,000 examples and still failed, so 50 fails faster; learning
stays human-in-the-loop at review time. (b) fake-precise blended "context score" mixing
unproven signals with invented weights — show raw pieces, let the pilot judge.

**Creed:** part-time, not competing with institutions; test everything; 2-year horizon;
50% of earnings → schools & hospitals.

## 2026-07-20 — ARCHITECT CRITIQUE (senior-architect review of the plan)

Cold review found the plan's philosophy/gates/sequencing sound, but the unglamorous
plumbing layer missing and one live security wound. Fix these BEFORE new features:

**Critical missing architecture:**
1. Two-writers problem: laptop + cloud both append the SAME snapshots.csv → recurring
   merge conflicts (hit again during THIS very session). Fix: split by writer
   (snapshots_cloud.csv / snapshots_local.csv), grader merges + de-duplicates.
2. Grader has NO duplicate protection → weekend manual test-fires (rows at 21:03 AND
   21:04, etc.) will pollute the week-1 report card. Fix: candle-identity rule
   (asset + timeframe + candle-open-time = ONE claim; extras discarded).
3. Phase-1 gate "beat a coin flip" is the WRONG baseline in an up-drifting market (a
   parrot that always says UP scores 55-60% with zero skill). Fix: grader also scores an
   "always-UP parrot" column; gate becomes "beats the parrot," not "beats the coin."
4. No frozen historical data store → the Sealed Vault is rhetorical (a live API returns
   today's data, not a fixed past). Fix: one-time checksummed backfill, stored, immutable.
5. LSTM observer (Voice 2) lives in a different repo/env — needs a bridge/adapter spec
   (predict-only harness writing into ZarX journal, keyed by candle identity).
6. No strategy versioning — a survivor's track record must not carry across a parameter
   change. Fix: stamp name + parameter-fingerprint + code-version on every signal.

**Security / scaling blind spots:**
- 🔴 API KEY LEAK: TwelveData error messages print the full request URL including
  apikey=...; daily_runs.log is git-TRACKED + pushed + OneDrive-synced, and the museum
  archive logs also contain it. Both repos private (moderate, not critical). Fix: redact
  key from error prints, untrack daily_runs.log, ROTATE the key (free, 2 min).
- GitHub Actions pinned by floating tag (@v4/@v5) with write access → pin to commit SHAs
  (soft, low urgency).
- Phase-2 compute (walk-forward × Monte Carlo 10k × strategies on laptop CPU) only viable
  with the frozen local store (#4) + vectorized simulation.
- Evidence file grows ~2,200 commits/yr; the writer-split (#1) also relieves this.

**Immediate order:** (1) security hygiene ~30min → (2) BEFORE Friday: grader dedup +
parrot baseline → (3) split black box by writer → (4) frozen backfill → (5) spec LSTM
adapter → (6) defer the rest. Plan's ordering otherwise correct.

## 2026-07-21 — Brainstorm clarifications recorded (the tool doorway + the five adopted tools)

**The Tool Doorway Rule (Commander asked when price-action math tools join):**
- As INFORMATION on the Brief (describe the chart, no buy/sell): may be added almost
  anytime, cheaply, a few per session — including any tool the Commander names.
- As SIGNALS (anything that says buy/sell): must pass through the Lab first and earn an
  honest stat card. No tool skips this — not RSI, not Fibonacci, not any guru's favorite.
- Therefore: small instrument additions can trickle in from next week; the BIG toolbox
  expansion happens right after the Lab exists, so every tool arrives with proof attached.

**Five adopted tools confirmed, each with its phase:**
1. Data Validator — Phase 1 (quality inspector at the data door)
2. Cost Simulator — Phase 2, in the Lab (our 1h-scar made into a tool: every simulated
   trade pays real fees/slippage)
3. Monte Carlo Stress Test — Phase 2, in the Lab (reshuffle trades 10,000× — luck detector)
4. Walk-Forward Testing — Phase 2, in the Lab (many windows; the +3.53/-0.87 lesson
   made into a machine)
5. Human-vs-Machine + Psychology — Phase 5, Trade Logger & Mirror (grades the pilot)

**Cloud status:** ran fully autonomous 24h+ (7+ consecutive watches, zero errors). First
real grades: 24/24 correct (100%) — read with the parrot warning: up-drifting market, no
baseline yet, duplicates not yet filtered. Exactly why the repairs come first.

**NEXT WORK SESSION (start here):** the three repairs, in order —
1. Security hygiene: redact API key from error prints, untrack daily_runs.log, rotate key
2. Grader honesty: candle-identity de-dup + always-UP parrot baseline (BEFORE Friday)
3. Split the black box by writer (snapshots_cloud.csv / snapshots_local.csv, grader merges)
Then: Friday week-1 review → Phase 2 the Lab (frozen vault backfill first).

## 2026-07-21 — THE THREE REPAIRS (architect critique items 1-3) — ALL GATES PASSED

**Repair 1 — security hygiene (committed 08a64ef):** every error print in
data/market_data.py now passes through _redact() (the API key becomes
***REDACTED*** before it can reach any log); journal/daily_runs.log untracked
+ gitignored. History audit ran first: the key had NEVER actually landed in
this repo's commits — the door is sealed before the leak, not after. Gate:
forced request failure printed no key; live smoke test unchanged (3/3 assets).
STILL OPEN (Commander's 2 minutes): rotate the TwelveData key (the museum
repo's old logs may hold it), update .env + the GitHub Actions secret.

**Repair 2 — grader honesty (v2):** candle-identity rule (asset + timeframe +
candle-open-time = ONE claim, earliest row wins) + always-UP parrot baseline.
Gate (synthetic): 4 rows across 2 writers → 2 unique claims. Gate (live): the
weekend's "24/24 = 100%" collapsed to 69 rows → 36 unique claims → 13 graded,
and the parrot ALSO scored 100% (18/18) → verdict: "system does NOT beat the
parrot." The inflated report card is dead; this is the honest bar for Friday.

**Repair 3 — black box split by writer:** laptop now writes
snapshots_local.csv, cloud writes snapshots_cloud.csv (writer identity =
GITHUB_ACTIONS env var); legacy snapshots.csv frozen as evidence; grader v2
merges all three notebooks at reading time. The recurring merge-conflict
disease is structurally cured (no two writers share a file). Bats + workflow +
CHECK_STATUS.bat updated to the new filenames. Gate: live local snapshot wrote
3 rows to snapshots_local.csv; cloud-identity check picks snapshots_cloud.csv.

**Next:** Commander rotates the key → Friday week-1 review (2026-07-26, on
honest numbers) → Phase 2 the Lab, starting with the frozen vault backfill.

## 2026-07-26 — WEEK-1 REVIEW (the 7-day observation verdict)

**Machinery grade: A.** Seven days, two watchmen (laptop + cloud), 189 evidence
rows, zero data losses. Every incident of the week (quoted-path scheduler bug,
battery block, LF bat endings, two-writers conflicts, PyPI dropping pandas-ta)
was found, fixed, and verified by fire. Catch-up-on-wake proven repeatedly.
The ship runs itself.

**Instruments verdict (80 graded claims, full week):** system 40.0% vs
always-UP parrot 49.5% — the system did NOT beat the parrot in week 1.
Market context: a round trip (BTC $64.5k → $66.3k → $64.4k). The EMA trend
claims said UP near the top as lagging instruments must, and the falling
half of the week graded them down (SOL worst at 29%, ETH best at 52%).
MIXED honesty rose late-week (25 claims) as the instruments caught up.

**The Commander's catch:** on Saturday ~10:00–14:00 UTC the system briefly
BEAT the parrot (42.1% vs 41.1% — preserved in cloud_grader_report.txt
history). The lead lasted hours and flipped back — recorded as the textbook
demonstration of why a 1-point lead on a small sample is noise, not skill.

**The learning (the founding lesson, now proven on our own fresh evidence):**
trend DESCRIPTION is not trend PREDICTION. The weather station describes;
it does not forecast. This is exactly why the Brief is a cockpit and not a
signal source, and why signals must earn their place through the Lab and
the sealed gauntlet. No instrument tuning done or permitted on this sample —
"fixing" lagging EMAs to match one round-trip week is the overfitting trap.

**Decisions:** observation period CLOSED. Snapshots + grading continue
forever as background heartbeat. Next: TwelveData key rotation (still on
the Commander's desk) → Phase 2 Step 2.1, the Frozen Vault, per
EXECUTION_PLAN.md.

## 2026-07-21 — EXECUTION_PLAN.md: the step-by-step orders for Phases 2-8

Commander's request: a plan so exact that any model (Opus, Sonnet) can follow
it to the point, with if/then branches for everything that can go wrong.
Written and committed as EXECUTION_PLAN.md: Phase 2 Lab in 5 gated steps
(Frozen Vault → Data Validator → honest engine with the three-dummies gate
including a planted look-ahead cheat → lie detectors → end-to-end exit gate),
then Context Deck / Carry Monitor / Trade Logger & Mirror / sealed Gauntlet
(gates locked in writing BEFORE any test) / Proving Voyage / Permanent Loop.
Includes the standing IF/THEN table (gates outrank models; too-good results =
hunt the leak first; THE PROMISE wins every argument) and a CURRENT POSITION
MARKER line each session must update. ROADMAP.md now points to it.

## 2026-07-26 — PHASE 2, STEP 2.1: THE FROZEN VAULT — GATE 2.1 PASSED

**What was built (nothing outside lab/):**
- `lab/build_vault.py` — one-time deep download through data/market_data.py
  `get_history()`. All six downloads happen in memory FIRST; not one byte is
  written unless all six arrived (the vault is only born complete). Refuses to
  run at all if a MANIFEST already exists — a born vault is never re-born
  (Law 5, evidence is never rewritten).
- `lab/vault/` — 6 CSVs, 22,986 candles total, plus MANIFEST.json (rows,
  first/last candle, days covered, byte size, SHA-256 per file, build date,
  the git commit it was built from).
- `lab/verify_vault.py` — recomputes every checksum, prints VAULT INTACT /
  VAULT CORRUPTED / VAULT MISSING per file, and names any stranger file
  sitting in the vault that the manifest does not know about. Read-only,
  clock-free output by design.
- `lab/vault/.gitattributes` (`* -text`) — the laptop runs
  core.autocrlf=true; without this, git would rewrite line endings on
  checkout and every checksum would "fail" for a reason that has nothing to
  do with the data. The vault's bytes are now frozen on every machine.

**Depth actually granted (recorded, as the plan orders): the full ask.**
TwelveData gave 3 years on all six — 4h: 6,568 candles per asset
(2023-07-27 → 2026-07-26); 1d: 1,094 per asset (2023-07-28 → 2026-07-25).
Well above the 1-year floor, above the ~4,000-row 4h expectation. No thin-data
decision needed from the Commander.

**GATE 2.1 — all three conditions, run before the commit:**
(a) all 6 files exist with plausible counts (4h 6,568 ≥ ~4,000) ✅
(b) verify_vault.py printed INTACT for all six, exit code 0 ✅
(c) run twice → byte-identical output (diff clean) ✅
Extra proof, no file touched: one price digit changed in memory
(29292.0 → 29292.1) moves the fingerprint from 9d0cd7d5... to cf96cad2... —
the guard can actually tell, it is not just printing a nice word.

**Two honest notes, neither hidden:**
1. NO VOLUME COLUMN. TwelveData returns none for BTC/ETH/SOL-USD, so the
   vault is OHLC only. Every future tool that wants volume must be told this
   before it is designed, not after.
2. The still-forming last candle was dropped from each file (its high/low/
   close are not final). A frozen vault holds only finished candles;
   recorded in MANIFEST as `unclosed_last_candle_dropped: true`.

**Next:** Step 2.2 — the Data Validator (gaps, duplicates, impossible prices,
absurd single-candle moves), with its two-part gate: clean vault file → PASS,
a deliberately corrupted COPY → must name all three diseases.

## 2026-07-26 — PHASE 2, STEP 2.2: THE DATA VALIDATOR — GATE 2.2 PASSED
## …and the inspector immediately caught the vault it was built to guard

**What was built (nothing outside lab/):**
- `lab/validator.py` — the quality inspector at the door. Takes any candle
  DataFrame and reports in plain words: missing candles (holes vs the
  timeframe's own grid), off-grid candle times, duplicate timestamps,
  blank/zero/negative prices, high-below-low, impossible candle shapes
  (high not the highest, low not the lowest), impossible intra-candle moves,
  and big-but-real swings. Verdict: PASS / WARN / FAIL. It reads only — it
  never cleans, never deletes, never decides.
- `lab/gate_2_2.py` — the exam, re-runnable by anyone forever.
- `lab/build_vault.py` — wired: every downloaded file must pass the inspector
  BEFORE a single byte is written. A vault is frozen forever, so it may not be
  born sick. Future manifests carry `validated_at_birth: true`; the current
  MANIFEST does NOT have that key, which is the honest record that it predates
  the inspector.

**GATE 2.2 — passed on the first run, before the commit:**
(a) clean vault file (BTC-USD_1d.csv) → PASS ✅
(b) a COPY of it poisoned in memory — 5 candles dropped, 2 duplicated, one
    negative price — → all three diseases named BY NAME, verdict FAIL ✅
    Plus a fourth check the plan did not ask for: the gate re-reads the real
    vault file afterwards and proves it was never touched (the poison lived
    only in memory). ✅

**ONE HONEST DEPARTURE FROM THE LETTER OF THE PLAN (Commander told, not
hidden):** the plan lists ">25% single-candle move — flag, don't delete",
which is WARN behaviour. Real crypto does 28-33% days, so >25% alone cannot
mean FAIL or the inspector cries wolf at the truth. But a candle that moves
1,000,000% is not volatility, it is a broken number. So the check has two
tiers: >25% = WARN (flagged, kept, exactly as the plan orders) and >100%
inside one candle = FAIL ("impossible price"), which belongs to the same
family as the plan's "zero/negative prices" — data that contradicts reality.
Threshold is a named constant, changeable in one line.

**THE FINDING — THE VAULT IS PARTLY DISEASED (Step 2.3 is blocked):**
Run against the frozen vault, the inspector's verdicts were:
    PASS  BTC-USD_1d.csv     — clean
    WARN  ETH-USD_1d.csv     — 2 real volatile days (28.4%, 26.6%)
    WARN  SOL-USD_1d.csv     — 9 real volatile days + 1 big jump
    FAIL  BTC-USD_4h.csv     — 42 impossible candles
    FAIL  ETH-USD_4h.csv     — 2 impossible candles
    FAIL  SOL-USD_4h.csv     — 4 impossible candles
48 candles arrived from TwelveData with a decimal point in the wrong place —
the `low` divided by ~10,000. Examples: BTC 2023-07-28 12:00 shows a low of
$2.93 inside a $29,206 candle; SOL 2023-12-12 16:00 shows a low of
$0.00000224 inside a $68 candle. TWO BTC candles have a broken CLOSE as well
(2023-08-01 12:00 closes at $2.8954). All 48 sit in 2023-07 → 2023-12; the
1d files of the same period are clean, so the glitch is in the source's 4h
series, not in our download code.

**Why this matters more than it looks:** a backtest cannot tell a broken
candle from a real crash. Any stop-loss placed above $2.93 would have been
"hit" 42 times in BTC alone — the engine would report losses that never
happened, or "buy the dip" at prices that never existed. This is precisely
the "garbage in = lies out" that Step 2.2 exists to prevent. The inspector
justified its existence within an hour of being born, against our own data.

**Nothing was repaired, cleaned or deleted.** The vault is evidence and it
still verifies INTACT (checksums unchanged, verify_vault.py re-run after all
of today's changes). The decision — re-download the three 4h files with the
inspector standing at the door, or run Phase 2 on daily candles only — is the
Commander's, and it is recorded here as an open blocker on Step 2.3.

**Next:** the Commander's decision on the diseased 4h files, THEN Step 2.3
(the honest backtest engine with the three-dummies gate).

## 2026-07-26 — VAULT RE-BIRTH ATTEMPTED — REFUSED BY THE DOOR (blocker stands)

**The Commander's written order:** delete lab/vault/ and rebuild it through the
now-guarded builder; legal ONCE because the diseased original is committed and
pushed (aa6de2d, e63a9ca) — git history keeps the evidence, so Law 5 is
satisfied, not violated.

**Executed in the ordered sequence:**
1. `git pull` — fast-forwarded to 8a17fe3 (cloud snapshots).
2. `verify_vault.py` BEFORE touching anything → INTACT for all six. We only
   re-birth from a known state.
3. Proof of reversibility taken first: the committed blob of BTC-USD_4h.csv in
   aa6de2d hashes to 9d0cd7d5…, byte-identical to the file on disk. The old
   vault is genuinely recoverable, not "probably" recoverable.
4. lab/vault/ deleted (plus an off-repo scratch copy as belt-and-braces).
5. `build_vault.py` run.

**THE DOOR REFUSED AT FILE 1 OF 6.** BTC-USD 4h came back from TwelveData with
the SAME 42 impossible candles. The builder printed the inspector's report,
wrote nothing, and exited 1 — exactly the behaviour Step 2.2 was built to
produce. Nothing was ever written to disk.

**Then the vault was restored to its committed state** (`git checkout -- lab/vault`)
and re-verified: INTACT for all six, and `git status lab/` shows zero changes.
The failed re-birth left no scar. The repo is exactly as it was.

**RECONNAISSANCE (read-only, run from the scratchpad — nothing added to lab/):**
all three 4h series were downloaded fresh and compared, candle by candle,
against the vault's copies. The result is the decisive fact:

    BTC-USD 4h : 42 diseased fresh, 42 in vault — SAME candles: TRUE
    ETH-USD 4h :  2 diseased fresh,  2 in vault — SAME candles: TRUE
    SOL-USD 4h :  4 diseased fresh,  4 in vault — SAME candles: TRUE

**THE GLITCH IS PERMANENT IN TWELVEDATA'S STORED HISTORY.** It is not a
transient download error. Re-downloading will never fix it, today or in a year.
That option is now closed by evidence, not by opinion.

**Exactly which candles came back diseased (all 48):**
BTC-USD 4h — the `low` is the true price divided by ~10,000:
    2023-07-28 12:00 low 2.927   | 2023-07-31 08:00 low 2.9398
    2023-08-01 12:00 low 2.8936  | 2023-08-01 20:00 low 2.9204
    2023-08-02 16:00 low 2.9265  | 2023-08-03 00:00 low 2.9197
    2023-08-03 04:00 low 2.905   | 2023-08-04 12:00 low 2.9218
    2023-08-06 08:00 low 2.9096  | 2023-08-06 12:00 low 2.902
    2023-08-07 04:00 low 2.9066  | 2023-08-07 16:00 low 2.9176
    2023-08-08 00:00 low 2.92    | 2023-08-08 08:00 low 2.935
    2023-08-08 12:00 low 2.957   | 2023-08-08 16:00 low 2.9636
    2023-08-09 20:00 low 2.9568  | 2023-08-10 12:00 low 2.9458
    2023-08-15 08:00 low 2.9376  | 2023-08-15 20:00 low 2.9204
    2023-08-16 04:00 low 2.917   | 2023-08-16 16:00 low 2.9194
    2023-08-16 20:00 low 2.8944  | 2023-08-17 08:00 low 2.8533
    2023-08-17 12:00 low 2.8428  | 2023-08-18 12:00 low 2.6211
    2023-08-18 16:00 low 2.6044  | 2023-08-18 20:00 low 2.6068
    2023-08-19 04:00 low 2.5876  | 2023-08-20 12:00 low 2.5998
    2023-08-20 20:00 low 2.6152  | 2023-08-21 00:00 low 2.614
    2023-08-21 12:00 low 2.6062  | 2023-08-21 20:00 low 2.6124
    2023-08-25 00:00 low 2.6092  | 2023-08-25 16:00 low 2.5972
    2023-08-26 12:00 low 2.6076  | 2023-09-02 16:00 low 2.58
    2023-09-03 16:00 low 2.5865  | 2023-09-05 16:00 low 2.5735
    2023-09-07 04:00 low 2.581   | 2023-09-14 12:00 low 2.6455
ETH-USD 4h:
    2023-11-13 16:00 open 2105.23 high 2118.00 low 1.795    close 2100.00
    2023-12-19 12:00 open 2236.13 high 2241.27 low 0.74859  close 2191.38
SOL-USD 4h:
    2023-11-27 00:00 open 57.57 high 58.09 low 0.2698     close 56.60
    2023-12-12 16:00 open 68.45 high 68.78 low 0.00000224 close 67.62
    2023-12-16 08:00 open 74.39 high 75.15 low 0.01652     close 75.15
    2023-12-20 12:00 open 77.06 high 81.13 low 0.45911     close 80.52

**Two facts that shape the decision (stated, not acted on):**
1. 47 of the 48 have ONLY the `low` broken — open, high and close are sane.
   The single exception is BTC 2023-08-01 12:00, whose CLOSE is also broken
   ($2.8954 instead of ~$28,954).
2. Every diseased candle sits between 2023-07-28 and 2023-12-20 — the first
   five months of the three-year window. The last one in each asset:
   BTC 2023-09-14, ETH 2023-12-19, SOL 2023-12-20. From 2023-12-21 onward all
   three 4h series are free of impossible candles, and the 1d files covering
   the diseased period are clean throughout.

**RECORD CORRECTION (we correct forward, we do not rewrite the past):** the
Step 2.2 entry above says TWO BTC candles have a broken close. The true count
is ONE — 2023-08-01 12:00, close $2.8954. One broken close produces TWO
candle-to-candle jumps (into it and out of it), which is what caused the
miscount. The Step 2.2 entry stands as written; this line is the correction.

**Nothing was repaired, no candle was hand-edited, no low was multiplied by
10,000, no second data source was touched, and the validator's standards were
not lowered.** All four were explicitly forbidden by the order, and all four
remain undone.

**Step 2.3 stays BLOCKED.** The re-download option is dead on evidence. The
decision — and it belongs to the Commander, not to a session — is now between
the honest remaining routes: run the Lab on 1d only; start the 4h window at
2024-01-01 and record the shortened depth; or bring in a second data source
with the Commander's explicit yes. No session may choose this alone.

## 2026-07-26 — VAULT v2 BORN HEALTHY — ALL GATES PASSED — STEP 2.3 UNBLOCKED

**The Commander's decision (Route 2, on Fable's recommendation):** the 4h
window starts at 2024-01-01 — clean data only; the 1d files keep the full
3 years because they were never sick. Asymmetric depth by choice, not by
accident. Forbidden throughout and never done: hand-repairing candles,
multiplying lows by 10,000, any second data source, lowering the validator.

**What changed in the ship (lab/build_vault.py only):** a named constant
`VAULT_4H_START = '2024-01-01'` with a comment pointing at the evidence entry
above, plus `VAULT_4H_START_REASON` — one honest sentence that is written INTO
the MANIFEST, so the shortened window can never be mistaken for laziness by a
future session. 4h asks from that date; 1d keeps the 1,095-day ask; the request
carries a small day-margin and the builder then trims exactly to the line
(26 candles trimmed per asset, reported out loud).

**The sequence, as ordered:** git pull → verify_vault INTACT (known state) →
delete lab/vault/ → rebuild. The old vault stays in git history at aa6de2d.

**THE DOOR SAID YES THIS TIME. Zero FAIL verdicts at birth:**
    BTC-USD_4h  5,624 candles  2024-01-01 → 2026-07-26   PASS
    BTC-USD_1d  1,094 candles  2023-07-28 → 2026-07-25   PASS
    ETH-USD_4h  5,624 candles  2024-01-01 → 2026-07-26   WARN (2 real 25%+ days)
    ETH-USD_1d  1,094 candles  2023-07-28 → 2026-07-25   WARN (2 real 25%+ days)
    SOL-USD_4h  5,624 candles  2024-01-01 → 2026-07-26   WARN (1 real 25%+ day)
    SOL-USD_1d  1,094 candles  2023-07-28 → 2026-07-25   WARN (9 real 25%+ days)
20,154 candles total. Every WARN is genuine market violence (Feb 2025, Oct 2025,
Mar 2024) — flagged for human eyes, never deleted, exactly as the plan orders.

**ALL FOUR GATES, run before the commit:**
(a) 6 files; 4h 5,624 rows each (≥ ~4,000) starting on 2024-01-01; 1d 1,094
    each still starting 2023-07-28 ✅
(b) verify_vault.py INTACT for all six, run twice → byte-identical output ✅
(c) validator.py over the whole vault → ZERO FAIL ✅
(d) gate_2_2.py → still PASSED (clean file PASS; poisoned copy caught) ✅

**AN UNPLANNED INTEGRITY PROOF (worth keeping):** the three 1d files came back
from TwelveData with SHA-256 checksums IDENTICAL to the old vault's — byte for
byte, a download made two hours apart. That proves two things at once: the
source's daily history is stable, and our download-and-write pipeline is
perfectly deterministic. The 4h checksums changed, as they must (different
window). A vault that reproduces itself exactly is a vault whose checksums mean
something.

**Housekeeping done (the fix flagged last session):** the position marker no
longer offers "repair/re-download the 4h files" — that option is closed by
evidence, and the marker now says so explicitly so no future session wastes a
run rediscovering it. `lab/vault/.gitattributes` (`* -text`, the byte-freeze
against autocrlf) was restored from git after the rebuild — the builder does
not create it, and without it every checksum would break on the next clone.

**Old vault:** remains in git history at aa6de2d (and e63a9ca) — the diseased
original is evidence and is not lost, merely retired.

**Next:** Step 2.3 — the honest backtest engine, with the three-dummies gate
(always-flat → 0 trades; MA-cross → full stat card; the planted look-ahead
cheat → structurally impossible through the engine's own feed).

## 2026-07-26 — STEP 2.3: THE HONEST BACKTEST ENGINE — GATE 2.3 PASSED

The heart is in. `lab/engine.py` walks candles one at a time around one
contract — `signal(df) -> 'long'|'short'|'flat'` — and is built so that
flattering a strategy is not merely difficult but IMPOSSIBLE. Every wall
below exists because of a specific known lie:

- **Look-ahead.** At candle i the strategy is handed `df.iloc[:i+1].copy()`.
  Candle i+1 is not a hidden row, not a NaN row — it is absent, and the
  object has its own memory, so the rest of the file cannot be reached by
  walking back through the buffer the slice was cut from.
- **Same-candle magic.** Entries happen at the NEXT candle's OPEN.
- **The optimistic exit.** Stop and target both touched inside one candle
  -> the LOSS is counted. Always. A gap through the stop fills at the open,
  not at the stop.
- **Costs as a detail.** fee 0.1% + slippage 0.05%, BOTH sides, every trade,
  from the new `LAB_COSTS` block in config.py (the one permitted touch
  outside lab/). The 1h-scar law honoured.
- **Testing where you tuned.** `train_end` splits the run; the card that
  counts is hold-out only.
- **Bad data.** `load_vault()` runs validator.py at load, and a FAIL verdict
  refuses the backtest outright.
- **Live data sneaking in.** `run_backtest` accepts ONLY a `VaultData`, whose
  constructor refuses any path outside lab/vault/. engine.py does not import
  data/market_data.py and never may.
- **"Which version made this number?"** Every card and every CSV row carries
  strategy name + fingerprint (a hash of the params AND the costs, risk and
  ATR settings) + the git commit.

Exits are ATR stop/target from risk/calculator.py — the LIVE Discipline
Engine, not a Lab reinvention. Sizing is the live 1%-risk stop-distance
formula. The strategy is asked for a signal only when flat; an open position
is managed by the rules, exactly like live.

**HOLD-OUT LINE, RECORDED: train_end = 2025-10-01** — 1,789 4h candles
(~10 months) that no parameter ever saw.

### GATE 2.3 — THE THREE DUMMIES (BTC-USD 4h, door verdict PASS)

**DUMMY 1 — always-flat:** 0 trades, 0 P&L, 0% time in market, an empty CSV
with no phantom rows — and the engine still walked all 5,624 candles.

**DUMMY 2 — MA-cross 20/50, HOLD-OUT STAT CARD (2025-10-01 -> 2026-07-26,
1,789 candles):**

    trades        : 37   (19 long / 18 short)
    wins / losses : 14 / 23      win rate 37.8%
    profit factor : 0.63  (after costs)
    avg win       : +0.60% of equity
    avg loss      : -0.58% of equity   (win/loss ratio 1.03)
    max drawdown  : 7.98%
    NET RETURN    : -4.88%   <- after every fee and every slippage
    gross return  : -2.20%   <- the same run with costs switched off
    COST DRAG     : 2.68 percentage points ($265.60 over 37 trades, $7.18
                    per round trip, on a $10,000 account)
    time in market: 16.7%
    exits         : stop 22, target 14, forced close at end of data 1
    regime at entry: Ranging 20, Chaotic 13, Trending 4

A losing strategy, printed exactly as it is. Costs turned a -2.20% fantasy
into a -4.88% truth — that is the whole reason costs are never optional.
Nothing here is claimed as an edge.

**DUMMY 3 — THE CHEAT (peeks at tomorrow's close).**

*(a) Fed the future, outside the engine:* correct on every one of the 1,789
hold-out candles, no costs -> **+11,260,167% (112,602x the account)**, while
buy-and-hold did -43.80% over the same window. That is what a leak is worth.

*(b) Through the engine's proper feed:* the identical peek —
`df['close'].iloc[len(df)]`, one row past the end — raised IndexError on
**5,624 of 5,624 calls. 0 trades, 0 P&L.** An independent witness (`FeedSpy`
in the gate script, which does not trust the engine's own audit and re-checks
every single delivery against the vault file itself) measured: 0 candles from
the future ever delivered, 0 deliveries of the wrong length, 0 out-of-order
deliveries. The engine's own audit logged 0 look-ahead violations. The cheat
did not fail to profit — it never received a number to cheat with.

*(b2) The cheat that refuses to go flat* (falls back to "the last move
continues" when the peek fails): 219 trades, win rate 42.0%, PF 0.83,
**-11.60%**. That is what a look-ahead strategy IS once the look-ahead is
taken away: an ordinary losing guess.

**The leak's fingerprint is the SWING, not the size.** A third exhibit
(beyond the plan, kept because it teaches): the same cheat run THROUGH the
engine but holding its own copy of the whole file, so the future reached it
AROUND the feed — same entry cadence, same ATR exits, same costs as (b2),
only the peek differs:

    win rate     42.0%   ->   57.6%
    profit factor 0.83   ->    1.39
    net return  -11.60%  ->  +21.61%

One candle of future turned a loser into a winner. It is +21.6% rather than
millions because the peek buys only the ENTRY direction: the engine holds a
trade until an ATR stop or target hits — median 6 candles, mean 8.8, max 99 —
so ~5/6 of the exposure is blind, and entry is at the next candle's OPEN
while the peek is about that candle's CLOSE. **Recorded so nobody misreads
it as the engine half-containing a leak: the engine controls what the FEED
delivers, and nothing else. A strategy whose AUTHOR hands it the future will
still cheat.** That is why strategy code gets read, and why Step 2.4 exists.

### GATE RUN HONESTY (both things that went wrong)

1. **The first run FAILED** — on an assertion written in this session, not on
   the engine. I had demanded the leaked-future exhibit show a win rate above
   70%; it showed 57.6%. My expectation was wrong, for the reason explained
   above (one candle of foresight, six candles of holding). The check was
   corrected to what the exhibit actually proves — that the leak turns a loser
   into a winner — and the reasoning was written into the gate script so the
   number can never again be mistaken for containment. No engine code changed.
2. **The second run crashed** — the gate script printed a comparison against a
   stat card that had not been computed yet. Fixed. No engine code changed.

The engine was identical across all three runs, and so were its results: the
per-trade CSVs of runs 1, 2 and 3 carry IDENTICAL SHA-256 checksums. The Lab
is deterministic — a run that reproduces itself exactly is a run whose numbers
mean something.

**Evidence files (Law 5: nothing deleted, so all three runs remain on disk).
THE FINAL PASSING RUN is:** `always-flat_...-3.csv`,
`ma-cross-20-50_...-3.csv`, `cheat-leaked-future_...-3.csv`,
`cheat-through-the-feed_...-2.csv`, `cheat-degraded-to-a-guess_...-2.csv`.
The unsuffixed and other-suffixed files are earlier runs of the same day;
their contents are identical wherever the same strategy ran.

### AN INDEPENDENT HAND-CHECK (run before the commit, using no engine code)

All 119 MA-cross trades recomputed from the vault CSV alone. All 15 checks
clean: entry price is the entry candle's OPEN; slippage always worsens the
fill in the correct direction; every entry was preceded by the matching cross
on the PREVIOUS candle (119/119); stop and target sit exactly 1.5/2.0 ATR
from the fill; the money arithmetic reproduces; net is ALWAYS below gross;
every stop exit landed on a candle that genuinely touched the stop (66/66)
and every target exit on one that genuinely touched the target (52/52); never
two positions open at once; and the ATR at entry recomputes from candles
BEFORE the entry candle only (119/119).

### WHAT THE HAND-CHECK FOUND — AN OPEN ITEM, NOT A BUG

**116 of 119 trades were sized by the 25% concentration cap, not by the 1%
risk rule.** On BTC 4h a 1.5-ATR stop is ~1.9% wide, so risking 1% of the
account implies a position worth ~80% of it;
`RISK_CONFIG['max_position_fraction']` caps that at 25%, and the risk actually
taken was a **median 0.486% per trade (mean 0.509%, range 0.14% - 1.00%)**.

The engine is faithfully running the LIVE formula — so the live ship sizes the
same way. Nothing was changed, because this is doctrine, and doctrine belongs
to the Commander, not to a session. But it must be known: every Lab return and
every Lab drawdown above is on roughly HALF the intended risk, and the Phase 6
gate "must beat buy-and-hold-with-1%-risk-sizing" needs to state which risk it
means. To be decided before Phase 6 — never after seeing results.

**Next:** Step 2.4 — the Lie Detectors (walk_forward.py, monte_carlo.py,
regime_report.py), all three run against this same MA-cross dummy.

## 2026-07-26 — STEP 2.4: THE LIE DETECTORS — GATE 2.4 PASSED (35/35 checks)

Three instruments are bolted onto the honest engine. All three read the
engine's own output — a `BacktestResult` or the per-trade CSV — and all three
compound `return_pct` (each trade's net result as a fraction of the equity IT
started with), never raw dollars. Dollars carry the account history of every
trade before them, so a window's dollar profit secretly reports trades that
are not in the window. Percentages of own equity are the only honest unit for
a subset.

- `lab/walk_forward.py` — cuts the hold-out into 6 consecutive windows, scores
  each alone, and asks two questions: profitable in >= 60% of windows, and did
  any single window supply more than 50% of the profit.
- `lab/monte_carlo.py` — reshuffles the trade sequence 10,000x, compounds every
  path, reports the max-drawdown distribution and the 5th-percentile road.
- `lab/regime_report.py` — breaks the card down by the `regime_at_entry` already
  stamped on every trade. Information for the verdict, never an auto-filter.
- `lab/trade_stats.py` — one small shared file (the only addition beyond the
  three named instruments). All three needed the same profit-factor and
  drawdown arithmetic on arbitrary subsets; writing it three times means three
  places to be quietly wrong. It is written ONCE here, and it imports the
  engine's own drawdown function rather than re-deriving it, so the Lab has a
  single definition of "drawdown" that cannot drift.

**NOTHING MOVED.** Before measuring anything, the gate re-ran the Gate 2.3
dummy — MACross(20,50), BTC-USD 4h, train_end 2025-10-01 — and reproduced the
hold-out card exactly: **37 trades, 14/23, win rate 37.8%, PF 0.63, max
drawdown 7.98%, net -4.88%.**

### THE WALK-FORWARD WINDOW TABLE (MA-cross hold-out, 1,789 candles)

    #  from         to           candles  trades  win%     PF     SUM%     NET%   maxDD%
    1  2025-10-01   2025-11-19      298       5   80.0    5.76    +2.44    +2.46    0.51
    2  2025-11-19   2026-01-08      298       9   22.2    0.18    -3.26    -3.22    3.22
    3  2026-01-08   2026-02-27      298       5   20.0    0.16    -2.01    -2.00    2.00
    4  2026-02-27   2026-04-17      298      10   40.0    0.59    -1.77    -1.78    2.98
    5  2026-04-17   2026-06-06      298       4   25.0    0.24    -1.02    -1.02    1.02
    6  2026-06-06   2026-07-26      299       4   50.0    1.96    +0.68    +0.68    0.64
    TOTAL (arithmetic sum of every trade's percent result): -4.94%

37 trades in, 37 trades counted — the instrument refuses to report at all if a
single trade fails to land in exactly one window. TEST 1: profitable in 2 of 6
windows (33%, needs 60%) -> FAIL. **VERDICT: INCONSISTENT.**

Two totals are printed per window on purpose. SUM is the arithmetic sum of the
trades' percentages (-4.94%); NET is the same trades compounded (-4.88%). Only
the SUM can answer "what share of the profit came from this window?", because
the parts of a sum add up to the whole and the parts of a product do not.

### THE EDGE CASE, DEFINED BEFORE THE CODE WAS WRITTEN, AND WALKED BY THE GATE

The ">50% of profit" rule only means something when there IS profit. The
MA-cross dummy lost money, so the instrument printed this instead of a number:

    TEST 2 — CONCENTRATION: DOES NOT APPLY. The strategy finished the hold-out
             at -4.94% — there is no profit to divide into shares, so asking
             "which window carried the profit?" would be arithmetic on nothing.
             No number is printed here because any number printed here would be
             misleading. The verdict does not need it: a losing strategy is
             already INCONSISTENT.

Nothing was divided by a zero or negative total; no share-of-profit figure was
invented for a loser (the gate checks that the share column is literally empty
and that no lucky-window flag was raised); and the consistency test still ran
and still failed honestly. A losing strategy is INCONSISTENT by definition —
it is not consistent at anything except losing.

**A window with no trades is printed as "no trades" and still counted in the
denominator.** Silently dropping quiet windows would quietly improve the
consistency score of every strategy that sits out a bad stretch.

**The windows do not overlap.** "Rolling" means the window rolls forward
through time, not that windows share trades. If a trade were counted twice the
windows' shares of the profit would add to more than the profit, and the 50%
rule would be meaningless.

### THE DETECTOR MUST DETECT — THE PLANTED LUCKY WINDOW

A detector that has never caught anything is decoration. So the gate builds
SYNTHETIC trade sequences in memory (labelled as such in the output, never
written to the vault or to results, no number from them is a market result) —
the same technique as the poisoned vault copy in Gate 2.2.

**EXHIBIT A — the disease.** 60 fabricated trades: five windows make an
unremarkable +1.2% each, window 4 makes +40% alone. A single stat card would
show +46% and look like an edge.

    4  2025-12-24   2026-01-21       10   80.0   26.00   +40.00   +47.62    1.59   87.0% of profit
    -> FAIL — LUCKY-WINDOW FLAG RAISED.  VERDICT: INCONSISTENT.
    "Remove that window and the rest of the hold-out made +6.00%. That is the
     strategy without its lucky month — treat THAT as the honest expectation."

It named the right window, and — the part that matters — this sequence PASSES
the consistency test (profitable in 6 of 6 windows). It is caught by the
concentration test and nothing else. That is the +20% February, detected.

**EXHIBIT B — the control.** A detector that flags everything is as useless as
one that flags nothing. The same kind of fabricated sequence, profitable in all
six windows with the profit spread evenly (biggest window 25.7%): **NOT
flagged, verdict CONSISTENT.** The detector discriminates.

**EXHIBIT C — the quiet window.** The control with window 3 emptied: the table
printed `no trades in this window (counted, never skipped)` and the denominator
stayed 6 windows, not 5.

### MONTE CARLO — SEED 20260726 (RECORDED)

The 37 hold-out trades dealt in 10,000 different orders:

    the gentlest ride (best of all)    :  4.88%
    typical ride (median)              :  6.21%
    a rough ride  (75th percentile)    :  6.91%
    a bad ride    (90th percentile)    :  7.58%
    THE 5th-PERCENTILE RIDE            :  8.02%   <- the number the rule judges
    the worst shuffle of all           : 10.46%
    the ride history actually dealt    :  7.98%

**8.02% is well under the 30% ruin line -> passes the reshuffle test.** Said
plainly in the report: this means the ride is survivable, NOT that the strategy
makes money. A losing strategy can pass this test comfortably by losing
smoothly — and this one does.

The 5th-percentile equity path (100 units): 100.71 -> 99.74 -> 99.79 -> 98.49
-> 95.71 -> 94.47 -> 93.62 -> 93.44 -> 94.25 -> 95.12, deepest point 8.02%
below its own peak. It is a real path out of the 10,000, not an interpolation.

**A TRUTH THE INSTRUMENT IS NOT ALLOWED TO HIDE:** every reshuffle finishes in
exactly the same place — measured spread between the best and worst of 10,000
final returns: **0.000000 percentage points**. The same numbers multiplied in a
different order give the same product. There is no "distribution of final
returns" from a pure reshuffle; a tool that prints one is printing rounding
dust and calling it risk. What a reshuffle changes is the ROAD, and the road is
what this instrument measures. To answer the different question — what if the
same edge had dealt a different HAND — a clearly separated second exhibit
resamples WITH replacement: 5th percentile -10.49%, median -4.97%, 95th
percentile +1.20%, and **91.3% of hands lost money**. That exhibit is
information; the RULE is judged on the reshuffle, as the plan specifies.

"5th percentile" is stated unambiguously in the report: the 5th-percentile-
WORST outcome, i.e. the 95th percentile of the drawdown distribution — only 5
shuffles in 100 were rougher.

**REPRODUCIBILITY, PROVEN TWICE OVER.** Run twice inside the gate: identical
numbers AND character-identical report text. Run in two separate processes: the
entire 365-line gate output was byte-identical except the evidence filename
(which never overwrites, by Law 5).

### REGIME BREAKDOWN (hold-out, weather stamped at entry from closed candles)

    regime      trades  share   win%     PF    avg win  avg loss    SUM%     NET%  maxDD%
    Ranging         20   54.1%   30.0   0.32    +0.44     -0.59    -5.59    -5.46   6.76
    Chaotic         13   35.1%   53.8   1.58    +0.76     -0.57    +1.96    +1.95   2.22
    Trending         4   10.8%   25.0   0.22    +0.37     -0.56    -1.31    -1.31   1.31
    ALL             37  100.0%   37.8   0.63    +0.60     -0.58    -4.94    -4.88   7.98

The buckets add back up to the engine's own stat card exactly — the check that
proves no trade was lost on the way into a bucket. Thin samples are marked in
words: 4 Trending trades is "an anecdote, not a statistic".

The tempting reading is "it only works in Chaotic — filter for that". The
report refuses it in print: with three buckets one of them always looks good,
and 13 trades is not evidence. Keeping only the flattering regime is the oldest
form of curve-fitting there is. If a regime filter is ever added it becomes a
NEW strategy with a NEW fingerprint and starts the Lab again from the door.

### WHAT THE THREE INSTRUMENTS SAY ABOUT THE DUMMY, IN PLAIN WORDS

Nothing good, which is correct — it is an unremarkable losing strategy and
nobody claimed otherwise. It lost in 4 of 6 windows; it survives the reshuffle
test only because it loses smoothly; the one regime where it made money holds
13 trades. Three instruments, one honest verdict: no edge here.

### GATE RUN HONESTY

**The first run had one FAIL, and it was my assertion, not an instrument.** The
gate demanded the reproduced win rate equal 37.8; the engine returned 37.84,
which IS 37.8 to the precision the log recorded it at. The fix was to compare
each Gate 2.3 number to the number of decimals the log actually wrote down,
not to invent precision the record never had. No instrument code changed, and
no engine code was touched at any point in this session.

**A checksum difference, explained rather than waved away.** The per-trade CSVs
written this session do NOT match the Gate 2.3 ones byte for byte. Cause,
verified column by column: the `commit` stamp only — Gate 2.3's CSVs were
written before the Gate 2.3 commit existed (3fd443c), this session's carry
c4215bb. **All 119 trades are identical row for row in all 34 other columns.**
That is the provenance stamp working exactly as designed. Within this session
all four gate runs produced byte-identical CSVs.

**Untouched, deliberately:** engine.py, validator.py, dummies.py, gate_2_3.py —
not one line. Nothing outside `lab/` except this log and the plan's marker. The
risk-doctrine open item (the 25% cap making actual risk ~0.486% instead of 1%)
was NOT acted on — it is the Commander's decision and stays parked until before
Phase 6.

**Next:** Step 2.5 — the Phase 2 exit gate: run a deliberately-bad strategy
through the whole pipeline end to end and show the Lab exposes it (hold-out
collapse, walk-forward inconsistency, Monte Carlo ruin). If the Lab certifies
the bad strategy as good, Phase 2 is not done.

### INDEPENDENT REVIEW OF GATE 2.4 (Fable, same day, before Step 2.5)

Verified without trusting the session that built it: (1) the 2.4 commit
touched ONLY the five new lab files, evidence CSVs, the log and the marker —
zero lines changed in engine.py, validator.py, dummies.py, gate_2_3.py,
config.py, risk/, regime/, data/, and the vault verifies INTACT; (2) the gate
re-run fresh in a new process: 35/35, exit 0; (3) an independent script using
NO lab code recomputed the whole walk-forward table from the raw per-trade CSV
and the vault file alone — all six windows match the log to the cent, as do
PF 0.63, net -4.88%, sum -4.94%, 14/23; (4) the reshuffle-invariance claim
re-tested with different shuffles under a DIFFERENT seed: spread exactly 0.
Step 2.4 stands. The review run wrote one more evidence CSV (-8), committed
here — evidence is never deleted.

## 2026-07-26 — STEP 2.5: THE PHASE 2 EXIT GATE — GATE 2.5 **FAILED** (33/34)
## The con artist was caught. The LEAK walked straight through. Phase 2 is NOT
## declared complete. A decision is waiting for the Commander.

`lab/gate_2_5.py` is built and run. It is the only new file; engine.py,
validator.py, dummies.py, gate_2_3.py, gate_2_4.py, walk_forward.py,
monte_carlo.py, regime_report.py and trade_stats.py were not touched by one
line, and lab/vault/ was only read. The gate ran TWICE and produced
byte-identical output both times apart from the evidence filenames, exit code
1 both times, failing on the SAME single check.

**Why this entry exists even though the gate failed.** The Commander's
standing instruction, and Rule 6 of EXECUTION_PLAN.md: a blocker gets written
into this log, not just spoken. A history that records only the runs that
passed is a flattering history, and a flattering record is the exact disease
this whole ship was built to refuse. What follows is the complete result —
what was demonstrated, what failed, and what is now open.

### THE DEFINITION OF "CERTIFIED AS GOOD", LOCKED BEFORE ANY RUN

Written into the file as constants before a single number was measured — a
copy of the Phase 6 gauntlet bars, so they cannot drift later:

    hold-out profit factor after costs        >= 1.15
    hold-out trades                           >= 30
    walk-forward verdict                      == CONSISTENT
      (>= 60% of windows profitable AND no window > 50% of the profit)
    Monte Carlo 5th-percentile drawdown       <  30%

CERTIFIED means all four. Phase 6 carries two FURTHER requirements this gate
does not evaluate — "must beat buy-and-hold-with-1%-risk-sizing" and a second
AI's review. Leaving them out makes the battery EASIER than the real gauntlet,
which is the safe direction for an exam of this kind.

### STEP 0 — NOTHING MOVED

MACross(20,50), BTC-USD 4h, train_end 2025-10-01, re-run before anything else:
**37 trades, 14/23, win rate 37.8%, PF 0.63, max drawdown 7.98%, net -4.88%.**
Gate 2.3 reproduced exactly, for the second gate running. 0 look-ahead
violations.

### EXHIBIT 1 — THE CON ARTIST (SYNTHETIC, and labelled so everywhere)

A strategy that breaks NO rule. It never sees a candle past train_end, never
peeks at the future, obeys the signal contract exactly — and is still garbage,
because it MEMORISED the training data. The table is keyed on candle FEATURES:
hour-of-day (6 values on 4h) x day-of-week (7) x the up/down shape of the last
6 candles (64) = **2,688 possible cells, 1,687 of them memorised as signals**.
1,687 free parameters, every one fitted to the training data, not one of them
justified by any idea about how a market works.

**Train-only, enforced in code and printed.** The table is built from
`df[df.index <= train_end]` and nothing else, and the forward walk that scores
each training candle is bounded by the END of that slice — a trade unfinished
at train_end is DROPPED, never followed one candle into the hold-out. Training
slice 3,835 candles (3,815 scored, 20 dropped for having no ATR yet or no
resolution before the training data ran out); hold-out 1,789 candles; not one
candle shared.

**The edge case, decided before coding.** It memorises RECURRING features,
never TIMESTAMPS. A table keyed on "2024-03-15 08:00" would match nothing
after train_end — zero hold-out trades and an exhibit proving nothing. Hours,
weekdays and candle shapes come round again: **1,139 of the 1,789 hold-out
candles (63.7%) matched a memorised cell**, so the collapse is visible in
numbers rather than hidden behind an empty table. Had the hold-out still come
in under 30 trades, that IS one of the locked bars and would have been
reported as a failure, not tuned away.

**No randomness at all.** No RNG, no seed, no sampling; ties broken by a fixed
rule, never a coin. The table was built twice inside the gate and compared key
by key — identical. The only randomness anywhere in this gate is the Monte
Carlo's, seed **20260726**, printed in its own report.

#### THE MEMORISATION DIAL, TURNED IN FRONT OF THE READER

The con artist is allowed unlimited parameters ON TRAIN — that is its whole
character. What it is never allowed is one candle past train_end. The stopping
rule was written down first and is TRAIN-ONLY: *use the smallest pattern
length whose TRAIN card trips BOTH halves of the standing too-good law.* The
gate's code applies that rule itself, reading train PF and train win rate; the
hold-out column is printed for the reader but never consulted by the code.

     pattern   cells  memorised  samples  TRAIN PF  TRAIN win%  HOLDOUT PF  HOLDOUT net%
           3     336        237     11.0      1.72        59.0        0.86         -9.09
           4     672        499      6.0      1.87        61.4        0.76        -15.62
           5    1344       1012      3.0      2.73        69.0        0.82        -12.88
           6    2688       1687      2.0      4.26        77.2        0.69        -19.59

Read that table slowly, because it is overfitting drawn as a picture: every
turn of the dial makes TRAIN better and HOLD-OUT worse, in lockstep, all the
way down. A median of TWO training candles behind one cell is not a discovery
about markets. It is a phone book.

#### (a) and (b) — THE TWO CARDS, SIDE BY SIDE

                             TRAIN (memorised)    HOLD-OUT (never seen)
    trades                                 378                      195
    wins / losses                     292 / 86                 80 / 115
    win rate %                            77.2                     41.0
    PROFIT FACTOR                         4.26                     0.69
    avg win %                            +0.69                    +0.61
    avg loss %                           -0.55                    -0.61
    max drawdown %                        1.95                    21.55
    NET RETURN %                       +361.67                   -19.59
    gross return %                      510.66                    -6.98
    cost drag (pts)                     148.99                    12.61
    time in market                       97.1%                    91.3%
    window              2024-01-01 -> 2025-10-01   2025-10-01 -> 2026-07-26

The train card is spectacular, and **the standing too-good law fired on it**,
on both halves at once:

    !! TOO-GOOD ALARM — the con artist's TRAIN card
    !! profit factor 4.26 > 2.0 and win rate 77.2% > 70.0%.
    !! STANDING LAW: results this good are a bug or a leak until proven
    !! otherwise. Do not celebrate. Go and hunt the leak ... and READ THE
    !! STRATEGY'S CODE. This alarm is not a verdict, it is an order to go look.

Then ten months it had never seen: PF 4.26 -> 0.69, +361.67% -> -19.59%,
drawdown 1.95% -> 21.55%. Nothing was broken and no rule was bent. The
strategy wrote down what had already happened and bet it would happen again in
the same hour of the same weekday after the same shape of candles. On the data
it copied from, that is a perfect prophecy. On ten months it had never seen,
it is a phone book. **This is the entire disease, and it is why a train card
is never evidence of anything.**

#### (c) WALK-FORWARD ON THE CON ARTIST'S HOLD-OUT

    #  from         to           candles  trades  win%     PF     SUM%     NET%   maxDD%
    1  2025-10-01   2025-11-19      298      40   42.5    0.67    -4.70    -4.66    6.49
    2  2025-11-19   2026-01-08      298      29   44.8    0.77    -2.57    -2.60    4.85
    3  2026-01-08   2026-02-27      298      35   37.1    0.54    -7.08    -6.92    6.93
    4  2026-02-27   2026-04-17      298      25   60.0    1.51    +3.49    +3.49    1.99
    5  2026-04-17   2026-06-06      298      34   38.2    0.72    -2.94    -2.95    5.35
    6  2026-06-06   2026-07-26      299      32   28.1    0.38    -7.61    -7.37    8.98
    TOTAL (arithmetic sum of every trade's percent result): -21.40%

Profitable in **1 of 6** windows (17%, needs 60%) -> FAIL. The concentration
test correctly refused to run on a negative total, in the same words as Gate
2.4. **VERDICT: INCONSISTENT.** All 195 trades landed in exactly one window.

#### (d) MONTE CARLO (seed 20260726) AND THE REGIME REPORT

195 trades reshuffled 10,000 times: gentlest ride 19.59%, median 21.43%, 90th
percentile 23.76%, **5th-percentile ride 24.54%**, worst shuffle of all
30.21%. Spread between the best and worst FINAL return: 0.000000 percentage
points, as it must be. Run twice on the same seed — identical numbers.

    regime      trades  share   win%     PF    avg win  avg loss    SUM%     NET%  maxDD%
    Trending        76   39.0%   42.1   0.75    +0.64     -0.63    -6.93    -6.86    9.99
    Chaotic         68   34.9%   29.4   0.42    +0.60     -0.59   -16.53   -15.34   15.94
    Ranging         51   26.2%   54.9   1.15    +0.57     -0.60    +2.06    +1.98    4.70
    ALL            195  100.0%   41.0   0.69    +0.61     -0.61   -21.40   -19.59   21.55

The buckets add back up to the engine's own card. Both instruments ran without
error, as the gate required.

#### (e) THE LOCKED BATTERY — THE LAB'S ANSWER

    bar                                       measured           required   verdict
    hold-out profit factor after costs            0.69            >= 1.15   FAIL
    hold-out trade count                           195               >= 30   PASS
    walk-forward verdict                  INCONSISTENT  must be CONSISTENT   FAIL
    Monte Carlo 5th-percentile drawdown         24.54%              < 30%   PASS
    bars passed: 2 of 4

**VERDICT: NOT CERTIFIED — REJECTED BY THE LAB.** The exam Phase 2 exists to
pass, passed. A strategy must clear EVERY bar; clearing some is not a partial
pass, it is a fail — "promising" is the word that kills accounts.

The two bars it DID clear are recorded so that clearing them is never mistaken
for a compliment: a big trade count only means it traded a lot, and a
survivable Monte Carlo only means it lost SMOOTHLY. Losing smoothly is still
losing. The battery is an AND, not a score.

### EXHIBIT 2 — THE LEAK. **THIS IS THE BLOCKER.**

`PerfectForesight` from lab/dummies.py — the Gate 2.3 leak whose author handed
it the whole file, so it reads tomorrow's candle around the side of the
engine's feed. Run through the same pipeline, on the same hold-out line.

Its hold-out does not collapse, which was expected — a cheat cheats on the
hold-out too. **What was NOT expected is everything else.**

    bar                                       measured           required   verdict
    hold-out profit factor after costs            1.39            >= 1.15   PASS
    hold-out trade count                           203               >= 30   PASS
    walk-forward verdict                    CONSISTENT  must be CONSISTENT   PASS
    Monte Carlo 5th-percentile drawdown          8.01%              < 30%   PASS
    bars passed: 4 of 4      VERDICT: CERTIFIED AS GOOD.

Its walk-forward is not merely acceptable, it is exemplary: profitable in
**6 of 6** windows (+7.53, +4.09, +1.46, +1.12, +5.21, +0.66), biggest single
window 36.7% of the profit, comfortably under the 50% limit. Every lie
detector we built looked at a strategy that reads the future and reported a
well-behaved, consistent, survivable edge.

**AND THE TOO-GOOD ALARM STAYED SILENT.**

    .. too-good alarm SILENT — the leak's HOLD-OUT card
    .. profit factor 1.39 (limit 2.0) and win rate 57.6% (limit 70.0%).
    .. Nothing here is spectacular enough to trip the standing law.

This is the one failing check in the gate, and it is the finding of Step 2.5.
We expected to write down the limit as: *"the numbers miss a leak, but the
too-good alarm catches it."* **That is not what was measured.** A strategy
that reads tomorrow's candle walked this entire pipeline, cleared every locked
Phase 6 bar, and set off no alarm anywhere.

**Why it looks so ordinary** (recorded in Gate 2.3, confirmed again here): the
cheat sees exactly ONE candle ahead, but the engine holds a trade until an ATR
stop or target is hit, many candles later. So the peek buys the entry
direction and nothing else; most of the exposure is blind and rule-based exits
decide the outcome. A modest leak produces modest numbers. **That is precisely
what makes it dangerous** — the too-good alarm is tuned for spectacular
cheating, and a leak does not have to be spectacular to be a lie. It only has
to be good enough to win a Phase 6 slot, and this one is.

For the record: this same expectation was already proven wrong once, in Gate
2.3, whose entry states that session's first run failed because it demanded a
>70% win rate from this exhibit and got 57.6%. It has now failed twice. The
number is not going to change by asking it again.

### THE LIMIT, STATED IN PLAIN WORDS AND NEVER TO BE OVERSTATED

**The Lab's NUMBERS catch OVERFITTING.** Exhibit 1 proved it end to end, and
it is a real and valuable power: a strategy that memorised the past falls
apart on candles it has not seen, and the hold-out, the walk-forward and the
Monte Carlo all said so, in that order.

**The Lab's NUMBERS CANNOT CATCH A LEAK.** A strategy fed the answers answers
correctly everywhere — on train, on the hold-out, in every window. There is no
arithmetic that separates "knew the future" from "was right".

**And on the evidence of Exhibit 2, the too-good alarm does not catch this one
either.** So what stands between a leaking strategy and a Phase 6 certificate
is ONE thing: **a human reading the strategy's code.** Not a formality, not a
nice-to-have — the single point of failure, because neither the battery nor
the alarm objected to this leak at any point. Nothing beyond that is claimed.

### WHAT WAS DELIBERATELY *NOT* DONE

- **The failing check was not "fixed".** Lowering the alarm until this exhibit
  trips it would flag honest strategies too — a detector that fires on
  everything catches nothing. Tuning a gate until it passes is the shortcut
  the standing IF/THEN table forbids: gates outrank models.
- **Phase 2 is NOT marked complete** and the marker does not say it is.
- **Nothing was certified.** No strategy, real or synthetic, carries a pass.
- **Phase 3 was not started.** The risk-doctrine open item (the 25% cap making
  actual risk ~0.486% instead of 1%) stays parked for the Commander.
- **No protected file was touched.** engine.py, validator.py, dummies.py,
  gate_2_3.py, gate_2_4.py, walk_forward.py, monte_carlo.py, regime_report.py
  and trade_stats.py — zero lines changed. Vault read-only.

### REPRODUCIBILITY

Gate run twice, back to back, in separate processes: output byte-identical
except the evidence filenames (which never overwrite, Law 5), exit code 1 both
times, the same single failing check. The per-trade CSVs of the two runs carry
IDENTICAL SHA-256 checksums — con artist `a70a4560...`, leak `f361f91d...`.

### THE DECISION THAT IS THE COMMANDER'S, NOT A SESSION'S

By EXECUTION_PLAN's own wording, Step 2.5 asks whether the Lab catches a
deliberately-bad strategy, and it does. What failed is the stricter condition
the Commander set for this session: that the leak exhibit trip the alarm. The
options, none of them taken here:

1. **Accept the limit and make it law.** Write mandatory code-review-before-
   testing into SHIP_LAWS.md as a hard gate before Phase 6, since on this
   evidence it is the only defence against a leak. (Recommended minimum.)
2. **Accept the limit and add a structural check** to the Lab — something that
   inspects whether a strategy holds a reference to data outside the feed it
   was handed, rather than trying to detect a leak from its results.
3. **Treat Gate 2.5 as failed and rework Exhibit 2.**

Fable is to be asked. Nothing further is built until the Commander decides.

**Next:** blocked on that decision. Phase 3 does not start.
