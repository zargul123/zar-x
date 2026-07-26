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

### INDEPENDENT REVIEW OF GATE 2.5 (Fable, same day) — THE FINDING STANDS

Verified without trusting the session that built it, same discipline as the
Gate 2.4 review:

1. **The commit touched only what it was allowed to touch.** `git diff` of
   commit 0d633c5 against its parent for engine.py, validator.py, dummies.py,
   gate_2_3.py, gate_2_4.py, walk_forward.py, monte_carlo.py,
   regime_report.py, trade_stats.py, lab/vault/, config.py, risk/, regime/
   and data/: EMPTY. Zero lines. The commit contains exactly gate_2_5.py, the
   evidence CSVs, the log entry and the marker.
2. **The vault verifies INTACT**, all 6 files, checksums matching MANIFEST.
3. **Every headline number recomputed from raw evidence, using NO lab code.**
   An independent script (pandas/numpy only) reloaded the vault CSV and the
   committed per-trade CSVs and recomputed all of it: the MA-cross hold-out
   card (37 trades, 14/23, 37.8%, PF 0.63, -4.88%, dd 7.98% — Gate 2.3 intact
   for the third gate running); the con artist's train card (378 trades,
   77.2%, PF 4.26, +361.67%, dd 1.95%) and hold-out card (195 trades, 41.0%,
   PF 0.69, -19.59%, dd 21.55%); the leak's hold-out card (203 trades, 57.6%,
   PF 1.39, +21.61%); the walk-forward window tables for both exhibits
   (con artist profitable in 1 of 6 with trade counts 40/29/35/25/34/32 and
   SUM -21.40%; leak profitable in 6 of 6, biggest share 36.7%); the battery
   verdicts (con artist NOT CERTIFIED on the PF and walk-forward bars; leak
   passing every bar the review can recompute); and the alarm arithmetic
   (con train 4.26 > 2 and 77.2 > 70 -> must fire, did; leak hold-out
   1.39 < 2 and 57.6 < 70 -> cannot fire, did not). 17 of 17 checks match
   the log. The silent alarm is arithmetic, not a bug.
4. **The train-only claim exercised, not just read.** The review REBUILT the
   con artist's lookup table from the vault's train slice alone, following
   the documented recipe in its own code (no lab imports): the rebuild
   produced exactly **1,687 memorised cells**, and **all 573 of the con
   artist's committed trades (train + hold-out) trace back to a memorised
   cell whose direction matches the trade**. The strategy is what the log
   says it is: a train-only phone book.
5. **A third fresh gate run, in a new process, after the commit:** exit 1,
   66 OK lines, the SAME single failing check ("the too-good alarm fires on
   the leak's hold-out card", PF 1.39 / win 57.6%). Diffed line by line
   against the committed runs: every differing line is the git commit stamp
   (ee09663 -> 0d633c5) — the provenance stamp doing its job, same
   explanation as the Gate 2.4 checksum note. Every number identical. The
   run wrote three more evidence CSVs, committed here — evidence is never
   deleted.

One honesty note from the review itself: the review script's final summary
line printed a hardcoded "15/15" while actually running 17 checks — a typo in
the reviewer's own scratch script, caught by counting the printed lines. The
17 individual checks and their OK verdicts are what count.

**Conclusion: Gate 2.5's record is accurate as written.** The Lab catches the
overfit con artist decisively; the leak clears every numeric bar with no
alarm; the failing check is real, reproducible, and correctly NOT tuned away.
The blocker stands and the decision remains the Commander's: (1) mandatory
code-review-before-testing as law in SHIP_LAWS.md (recommended minimum),
(2) additionally a structural leak check in the Lab, or (3) rework Exhibit 2.
Phase 3 stays shut until the Commander decides.

## 2026-07-26 — THE GATE 2.5 DECISION: LAW 7 ADOPTED, GATE PASSED 37/37 —
## **PHASE 2 COMPLETE**

The Commander delegated the blocker decision in his own words: *"you know the
system spirit and what we want to achieve... do what is better for system."*
Recorded here so the provenance of this decision is never in doubt: the
Commander chose to delegate; the session chose the option; both facts are on
the record.

### THE DECISION: options 1 AND 2 — accept the limit and armour it

Option 3 (rework Exhibit 2 until it flatters us) was REJECTED: reshaping an
exam until the answer looks better is goalpost-moving, and Law 4 forbids it.
The limit Exhibit 2 exposed is true; the system's spirit says a true limit
gets written into law and defended, not painted over. So:

**1. LAW 7 — THE LEAK LAW — added to SHIP_LAWS.md.** In short: the Lab's
numbers catch overfitting and can NEVER catch a leak — measured, not assumed
(the leak cleared all 4 locked bars with the alarm silent). Therefore no
strategy enters Lab certification or a gauntlet slot until its code has been
READ line by line for leaks and the reading RECORDED in this log; the leak
check instrument runs as the reading's aid, never its substitute; and the
too-good alarm stays a flare, not a fence — its silence proves nothing, and
it is never to be lowered until some exhibit trips it (a detector tuned to
catch one known cheat flags honest strategies too).

**2. `lab/leak_check.py` — a new instrument, Law 7's aid.** It walks a
strategy OBJECT — attributes, closures, function defaults, referenced module
globals, nested containers — and reports every piece of candle-shaped data
(DataFrame, Series, datetime index, large numeric array) the strategy carries
AROUND the engine's feed. That is precisely how `PerfectForesight` cheats: the
engine's feed is clean, but the author handed the object the whole file.

Its own smoke test (Law 3), PASSED: three honest shapes clean (MACross,
always_flat, peek_or_guess — whose cheat needs the feed and therefore
carries nothing); four smugglers flagged (PerfectForesight via
`strategy.full`; an array hidden in a default argument; a module-global
DataFrame reached through the function's referenced names; a DataFrame buried
two containers deep inside an attribute dict); reports deterministic — no
memory addresses, types and shapes only, two scans print identical text.

**Its stated limit, printed in every clean report:** a clean scan is NOT
innocence. The scan only sees what the object carries at scan time; a
strategy can still open a file when called, call an API, or hide data in a
form the walk does not recognise. The scan narrows the hunt; the READING is
the verdict. Any session treating a clean scan as a substitute for Law 7's
reading is breaking the law the instrument was built to serve.

### THE ONE AMENDMENT TO GATE 2.5, AND WHY IT IS NOT GOALPOST-MOVING

The gate's single failing check — "the too-good alarm fires on the leak's
hold-out card" — was an ASSERTION WRITTEN ON A WRONG ASSUMPTION, the same
assumption Gate 2.3's log already recorded failing once before (that session
demanded a >70% win rate from this same exhibit and measured 57.6%). Asked a
second time, the number gave the same answer. The world was measured twice;
the expectation was wrong twice.

Per the Gate 2.3 precedent ("the check was corrected to what the exhibit
actually proves"), the check now asserts the MEASURED truth and guards it:

    MEASURED LIMIT: the too-good alarm stays SILENT on the leak
    (PF 1.39 < 2 and win 57.6% < 70 — the founding evidence of Law 7; if
     this ever starts firing, the ground has moved and Law 7 must be
     re-examined)

What was NOT changed, listed so nobody wonders: the locked battery bars (all
four, untouched); the alarm thresholds (NOT lowered); every number of both
exhibits (identical to the failing run — only the git commit stamp differs,
which is the provenance stamp working); engine.py, validator.py, dummies.py,
walk_forward.py, monte_carlo.py, regime_report.py, trade_stats.py, gate_2_3.py,
gate_2_4.py (zero lines); the vault (read-only, verified INTACT in the
independent review the same day). And Step 6 gained three checks that did not
exist before: leak_check must FLAG the leak (naming `strategy.full`, the
5,624-candle DataFrame it smuggles), must CLEAR the honest strategies
(MA-cross and the con artist — whose sin is memorising, which is the numbers'
job, and they did it), and must state in words that a clean scan is not
innocence.

### GATE 2.5 FINAL RESULT

**PASSED, 37 of 37 checks. Run twice in separate processes: byte-identical
output apart from the evidence filenames, exit 0 both times.** The full
sequence the gate now proves, end to end: Gate 2.3 reproduced exactly (third
gate running) -> the con artist built train-only with the capacity dial
turned in the open -> train card spectacular, alarm FIRED -> hold-out
collapsed -> walk-forward INCONSISTENT (1 of 6) -> Monte Carlo and regime
report clean -> locked battery REFUSES certification (2 of 4 bars failed) ->
the leak clears all 4 bars, alarm SILENT (the measured limit) -> leak_check
flags the leak and clears the honest strategies -> Law 7 stated in the
output in plain words.

Evidence CSVs of both passing runs committed (Law 5); within-run checksums
identical to the failing run's — the amendment changed no number.

### PHASE 2 IS COMPLETE

The Lab now stands on: a frozen, checksummed vault (2.1); a data inspector at
the only door (2.2); an engine built so flattery is impossible (2.3); three
lie detectors that each caught a planted disease (2.4); an exit exam that
watched the whole pipeline reject a con artist, and an honest, law-backed
answer for the one lie the numbers cannot see (2.5 + Law 7 + leak_check).

Marker updated: **Phase 3, Step 3.1 (Fear & Greed index) READY TO START.**
Phase 3 was NOT started in this session, per the standing order. Open items
carried forward, still on the Commander's desk: TwelveData key rotation; the
risk-doctrine item (25% cap -> actual risk ~0.486% not 1%) to be decided
BEFORE Phase 6; vault CSVs carry no volume column.

## 2026-07-26 — PHASE 3, STEP 3.1: THE FEAR & GREED INSTRUMENT —
## GATE 3.1 PASSED (45/45 checks, first run)

The Context Deck is open. The Morning Brief now carries one instrument of
wider-market context beneath the three asset briefings: the crowd-mood gauge.
It is INFORMATION. It does not say what to do, and no word in its output
proposes a trade.

### WHAT WAS BUILT — exactly two code files, as ordered

- **`cockpit/fear_greed.py` (new, 156 lines).** One doorway, `section_text()`,
  returning the Context Deck block the Brief prints. One network call, no
  retries, 10s timeout. Every failure becomes one honest offline line.
- **`cockpit/brief.py` (wiring, 4 added lines + 1 docstring line).** The full
  diff: one import, two print lines placed after the per-asset briefings and
  before the closing footer, and one sentence added to the module docstring.
  Nothing else in the Brief was touched.

**Scope, verified with `git diff` before committing:** `lab/` byte-identical
(empty diff, zero lines), the vault verified **INTACT — all 6 files match
their checksums**, and `data/ indicators/ regime/ risk/ signals/ config.py`
untouched. No new dependency, no `.env` change, no key: alternative.me's index
is free and keyless.

### THE REAL API SCHEMA RECEIVED (verified at build time, not assumed)

`GET https://api.alternative.me/fng/?limit=8` -> HTTP 200, `application/json`.
The shape the orders predicted was correct, and carried **two extras the
orders did not mention**, both recorded here because the next builder should
not be surprised by them:

    {
      "name": "Fear and Greed Index",            <- extra, ignored
      "data": [
        { "value": "26",                          <- STRING, not a number
          "value_classification": "Fear",
          "timestamp": "1785024000",              <- STRING unix seconds, UTC midnight
          "time_until_update": "39860" },         <- extra, NEWEST ITEM ONLY
        { "value": "27", "value_classification": "Fear",
          "timestamp": "1784937600" },            <- older items: 3 keys, no countdown
        ... 8 items total, NEWEST FIRST ...
      ],
      "metadata": { "error": null }               <- extra, and USED (see below)
    }

What the parser does with the reality it found:

- `value` and `timestamp` arrive as **strings** and are converted, never
  trusted as numbers. A value outside 0-100 is refused, not printed.
- **`metadata.error` is checked.** If the source ever reports its own error
  while still answering HTTP 200, the instrument goes offline rather than
  printing a number it cannot vouch for.
- `time_until_update` and `name` are ignored — reading fields we do not need
  is how a parser breaks when they move.
- The 8 items are **re-sorted newest-first by timestamp** rather than trusting
  the arrival order.
- **The source's own `value_classification` is printed, never a label of our
  own invention.** Observed live this day: 25 = "Extreme Fear" but 26 = "Fear",
  so the boundary sits between them. Inventing our own thresholds would put a
  different word on the Brief than the source publishes on its own page — that
  is exactly the kind of quiet drift this ship refuses.
- **Context values are labelled by their REAL age in days**, computed from the
  timestamps: 1 day -> "yesterday", 7 days -> "a week ago", anything else ->
  "N days ago". If the source ever skips a day, the Brief will say "8 days ago"
  rather than printing a wrong word over a right number.

### WHAT IT PRINTS

    CONTEXT DECK
    Fear & Greed : 26 — Fear   (yesterday 27 · a week ago 28)   [reading of 2026-07-26 UTC]
    (crowd-mood gauge from alternative.me — information, not a signal)

And when it cannot reach the source, the whole of its output is:

    CONTEXT DECK
    🔌 Fear & Greed instrument offline (ConnectionError)

The failure's TYPE is named — a dead network and a changed schema are
different problems, and the pilot should be able to tell them apart without
opening a log.

### GATE 3.1 — DECLARED BEFORE THE BUILD (Law 4), RUN AGAINST THE LIVE
### MARKET, **PASSED 45 of 45 CHECKS ON THE FIRST RUN**

**(a) Standalone run — live value, classification, week of context. PASS
(6 checks).** Exit 0. Fetched 8 daily readings, 2026-07-19 -> 2026-07-26 UTC.
Value **26**, inside 0-100; classification **"Fear"**; yesterday **27**; a
week ago **28**.

**(b) The value matches what alternative.me itself publishes. PASS (4
checks).** Cross-checked not against the API a second time — that would only
ask the same machine the same question — but against the **web page a human
would open**, `https://alternative.me/crypto/fear-and-greed-index/`, scraped
independently of the instrument:

    what the web page published        what the instrument printed
    Now:        26  Fear               26 — Fear
    Yesterday:  27  Fear               yesterday 27
    Last week:  28  Fear               a week ago 28
    Last month: 13  Extreme Fear       (not shown on the Brief)

Four for four, value AND wording. The page's own "Last week" framing is the
same comparison the Brief prints, which is why the instrument shows it.

**(c) THE OFFLINE DRILL — internet never disconnected. PASS (10 checks).**
The instrument's base URL is injectable, so the drill points it at
`https://zar-x-offline-drill.invalid/` — the `.invalid` top-level domain is
reserved by the RFCs and can never resolve, so the failure is genuine and the
Commander's connection is never touched. Result: the two-line offline block
above, **no traceback, nothing else printed**. Then a FULL BRIEF was run with
the instrument pointed at that dead address: **3/3 assets reporting**, exit
code unchanged, and all six per-asset lines (Price, Trend, Momentum,
Volatility, Weather, Example) present three times each. The dead instrument
cost the Brief one line and nothing else.

**(d) Full live Brief — new section present, every old section intact. PASS
(20 checks across the two runs).** 3/3 assets, CONTEXT DECK present, the six
pre-existing per-asset lines present x3, header and footer unchanged. Live
numbers from run 1: BTC $64,684.01 (+0.78%), ETH $1,894.45 (+1.42%), SOL
$74.99 (+1.09%), all three Ranging.

**(e) Two runs back to back, both completed. PASS (2 checks + 1 baseline
check).** Both exit 0, 6.4s and 7.5s. **Both printed index 26 — and the same
prices, to the cent.** The gate ALLOWED the value to differ; it did not, and
that is worth stating plainly so nobody reads it as proof of determinism:
seven seconds apart, TwelveData returned the same last 4h candle and
alternative.me's daily index had not turned over. Run the two an hour apart
and the prices will move. This is live data being live, not a fixture.

### DELIBERATELY NOT BUILT — AND THE 3.2 REMINDER THAT MATTERS MORE

**NO CSV recording of the Fear & Greed index, on purpose.** alternative.me
serves its FULL history on demand (`limit=0` returns every day back to 2018),
so there is nothing here that can be lost by not collecting it. A recorder
would be a second copy of a public archive, and a second copy is a second
thing that can rot.

**STEP 3.2 IS THE OPPOSITE CASE AND MUST NOT BE CONFUSED WITH THIS ONE.**
Binance's free endpoint does NOT serve deep funding history. **Funding
recording to CSV starts THE DAY 3.2 SHIPS** — every day it does not run is a
day of history that cannot be bought back later, and Phase 6's Slot 2
(funding-rate extreme fade) cannot be tested without it. This is the single
most time-sensitive obligation on the ship right now.

### WHAT WENT WRONG, AND THE SMALL THINGS WORTH KNOWING (Law 1)

Honestly: **the gate passed on its first run and nothing failed.** That is
recorded exactly as plainly as a failure would have been — an unbroken run of
green is a fact about a small step, not evidence of a good session. What the
build did meet on the way:

1. **The orders' expected schema was slightly incomplete** (the three extras
   above). Adapted and recorded, as the IF/THEN table required.
2. **The smoke test fetches the API twice** — once to assert on the parsed
   readings, once for the section it prints. Two requests, no retries, on an
   endpoint with no key and no published rate limit. Chosen so the assertions
   test real parsed values instead of pattern-matching the printed line; the
   cost is that the printed block is a second, separate reading. Same number
   both times today, and the index only turns over daily.
3. **The rate-limit trap that did NOT bite, and the one deliberate pause.**
   Three Brief runs = 9 TwelveData requests against a free tier of 8/minute.
   Runs 1 and 2 went back to back (6 requests) with no 429. Before the third
   (the offline-drill Brief) the gate waited 70 seconds for the window to
   reset, so that a rate-limit retry could never be mistaken for a failure
   caused by the new instrument.
4. **One rewrite before any gate ran:** the smoke test's final verdict line
   was first written as a conditional expression tangled inside an f-string —
   it worked, but it was unreadable. Replaced with a plain if/else.
5. **`journal/snapshots_local.csv` carries 3 uncommitted rows** from the
   automated 12:05 snapshot run, which were already there when this session
   opened. They were **not touched, not deleted, and deliberately NOT included
   in this commit** so the commit's diff is exactly the four files the orders
   allow. The evidence stays on disk for the automation's own commit (Law 5:
   history is sacred, and this session did not write it).
6. **The gate harness is NOT in the repository.** Only two code files could be
   touched, and a `gate_3_1.py` would have been a third. The harness ran from
   outside the ship; its 45 checks are itemised above in enough detail to be
   rebuilt exactly. If a future session wants Phase 3 gates kept as code, that
   is a decision for the Commander, not something to smuggle in under a step
   that forbade it.
7. **Law 7 does not bite here** and was not invoked: nothing entered the Lab,
   no strategy was certified, no vault file was read. The signals doorway
   stands untouched — the Context Deck describes the crowd, it never proposes
   a position.

**Step 3.2 was NOT started**, per the standing order, even though 3.1 finished
early. One part, one gate, one commit.

## 2026-07-26 — PLANNING SESSION FOR STEP 3.2 (Opus wearing Fable's hat) —
## **A FALSE PREMISE FOUND AND KILLED BEFORE IT COST US ANYTHING**

No code was built in this session. Orders for Step 3.2 were written, the
ROADMAP was refreshed, and one belief this ship had been carrying since the
execution plan was drafted was tested for the first time — and turned out to
be wrong.

### WHY THIS SESSION EXISTS

Fable, who normally writes the orders and independently verifies the work,
was unavailable. The Commander asked the Step 3.1 build session to fill the
planning chair. **The builder and the planner are therefore the same mind,
which is precisely the independence this ship normally relies on**, and that
is recorded plainly rather than glossed over. What was done about it is in
SESSION_ORDERS.md under "WHO CHECKS THE CHECKER": the gate is declared and
committed BEFORE any code exists, a FRESH session builds to it, a THIRD fresh
session reviews by recomputing from raw evidence, and **the Phase 6
second-AI requirement is explicitly NOT waived.**

### THE MISTAKE — MINE, MADE THE SAME MORNING, IN BOLD, THREE TIMES

The Step 3.1 entry above, the EXECUTION_PLAN marker, and the Step 3.1 commit
message all state — with emphasis — that Binance does not serve deep funding
history, that funding recording to CSV must therefore begin the day Step 3.2
ships, and that this was *"the single most time-sensitive obligation on the
ship right now."*

**Every word of that is false.**

It came from EXECUTION_PLAN's Phase 6 Slot 2 line, which had carried the same
claim since the plan was drafted. The Step 3.1 session read it, believed it,
amplified it, and wrote it into three permanent records without once calling
the endpoint. It cost nothing this time only because the next session happened
to test it before building on it.

**The structural lesson, which is worth more than the correction itself: a
step's gate only tests the step's OWN data source.** Step 3.1's gate was
thorough — 45 checks — and it verified alternative.me's schema against reality
exactly as ordered. It had no reason to touch Binance, so a false claim about
Binance rode through a passing gate untouched and picked up the authority of a
"GATE PASSED" commit on the way. **Claims about a FUTURE step's data are the
blind spot of a per-step gate**, and this ship now has one documented example.

### WHAT WAS ACTUALLY MEASURED (2026-07-26, from the Commander's connection)

Four endpoints probed directly, results recorded verbatim:

    BINANCE /fapi/v1/premiumIndex   HTTP 200  lastFundingRate, nextFundingTime, markPrice
    BINANCE /fapi/v1/fundingRate    HTTP 200  settled 8-hourly history, paginated
    BYBIT   /v5/market/tickers      HTTP 200  reachable, funding present
    OKX     /api/v5/public/funding-rate  DNS FAILURE — www.okx.com does not
                                    resolve at all from this connection

**Funding history depth — the claim that was wrong:**

    limit=1000, no window          500 rows   2026-02-10 -> 2026-07-26
    startTime=2020-01-01           1000 rows  2020-01-01 -> 2020-11-29
    BTCUSDT earliest available     2019-09-10 08:00   (contract inception)
    ETHUSDT earliest available     2019-11-27 08:00
    SOLUSDT earliest available     2020-09-13 16:00

Roughly **seven years of settled funding, free, keyless, paginated with
`startTime` + `limit=1000`.** Nothing needs collecting. **Phase 6 Slot 2
(funding-rate extreme fade) can be tested whenever we choose** — a real
de-risking of Phase 6, arrived at by accident while checking a different
thing.

**Open interest depth — where the urgency actually lives:**

    /futures/data/openInterestHist  period=4h limit=500
      -> 180 rows only: 2026-06-26 16:00 -> 2026-07-26 12:00  (exactly 30 days)
      -> startTime older than the window is REFUSED: code -1130,
         "parameter 'startTime' is invalid"

**Open interest is the one dataset that genuinely evaporates**, and Phase 3's
instrument #5 (Whale Watch) names the funding+open-interest combination as its
honest free footprint. The instinct behind the old instruction was sound; it
was pointed at the wrong instrument.

**And the detail that removes the panic:** because every read reaches back 30
days, a recorder that runs even once a month loses nothing. This is a deadline
measured in weeks, not an emergency — and it means the Commander's laptop is a
sufficient recorder. The cloud watchman is not required, which conveniently
sidesteps an unresolved risk: GitHub's runners are US-hosted and Binance
geo-blocks US addresses, so a cloud-side funding/OI recorder might have
collected nothing at all, silently, for weeks.

### THE COMMANDER'S QUESTION: "WHAT SHOULD WE DO ABOUT THE FUNDING THING?"

Answered as follows, and written into SESSION_ORDERS.md:

1. **The source stays Binance.** It is reachable, it is free, it is what the
   plan names, and it serves everything we need. No swap, no Bybit, no OKX
   (which this connection cannot even resolve). Bybit is recorded as the
   standing candidate ONLY if Binance ever refuses us, and switching is the
   Commander's call, never a session's.
2. **Step 3.2 builds the funding DISPLAY only. No recorder.** The reason is
   now measured rather than assumed.
3. **The open-interest recorder becomes its own step, 3.2b**, with a 30-day
   backfill at birth and its own gate. It is NOT to be smuggled into 3.2.
4. **One source, chosen once, never switched mid-history.** Funding rates
   differ between exchanges; a dataset stitched from two of them is a dataset
   that cannot be trusted. This matters more than which exchange wins.
5. **The sign is the whole instrument.** Gate 3.2 check (b) exists solely to
   prove that a positive rate is printed as longs paying shorts and not the
   reverse. Getting it backwards would print the opposite of the truth every
   morning, and no "a number appeared" check would ever catch it.

### WHAT WAS CORRECTED, AND WHERE (nothing deleted, everything visible)

- `EXECUTION_PLAN.md` Phase 6 Slot 2: the false clause **struck through, left
  legible**, with the measured facts beside it. A plan that quietly edits its
  own errors teaches the next session nothing.
- `EXECUTION_PLAN.md` Phase 3 #2: note added redirecting the recording
  obligation to open interest.
- `EXECUTION_PLAN.md` marker: the false sentence from this morning quoted and
  corrected in place.
- `ROADMAP.md`: refreshed to Phase 3 state, Step 3.1 added to the parts table,
  and a new **MEASURED data-source facts table** — every free source with the
  depth it ACTUALLY serves and whether it must be recorded, so no future
  session plans on a guess again.
- The Step 3.1 log entry and its commit message are **left exactly as written,
  wrong bits included.** They are history. This entry is the correction, and
  the two are meant to be read together.

### A CANDIDATE FOR LAW 8 — PROPOSED, **NOT ADOPTED**, THE COMMANDER DECIDES

*"A claim about what a data source will or will not give us is not a fact
until it has been called. Planning documents must mark which of their claims
are measured and which are assumed, and no session may build on an assumed
one without measuring it first."*

That law would have caught this today. It is deliberately **not** written into
SHIP_LAWS.md by this session: the law book has seven laws and each one was
adopted by the Commander after a failure that earned it, not by a session that
liked its own idea. Seven laws get read; twelve get skimmed. Recorded here as
a candidate so the decision is his and the reasoning is not lost.

### WHAT WAS DELIBERATELY NOT DONE

- **No code was written.** Step 3.2 was not started; the orders exist so a
  FRESH session builds to a gate it did not write.
- **The open-interest recorder was not built**, despite being the genuinely
  time-sensitive item. It is a step with a gate, not a footnote on another
  step.
- **SHIP_LAWS.md was not touched.** No session promotes its own idea to law.
- **No file outside the four planning documents was changed.** No code, no
  evidence, no vault.

### STILL ON THE COMMANDER'S DESK (carried forward, unchanged)

1. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
2. **The risk-doctrine decision**: the 25% position cap means actual risk is
   ~0.49% per trade, not the intended 1%. Must be settled BEFORE Phase 6,
   never after seeing results.
3. **Law 8 candidate** above — adopt, reject, or reshape.
4. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

**Next: a fresh session builds Step 3.2 to the committed gate.**

---

## 2026-07-26 — STEP 3.2 BUILD SESSION, PART 1 OF 2: **GATE 3.2 CHECK (b)
## WAS UNPASSABLE AS WRITTEN — CORRECTED BEFORE ANY CODE EXISTED**

**No code was written in this part.** This entry is committed on its own,
BEFORE `cockpit/funding.py` exists, so that the corrected bar is on the record
before anything can be built to fit it. Law 4 is the reason for the split
commit: a gate amended by the same session that later reports passing it is
worth nothing unless the amendment lands first, in public, with its evidence.

### WHAT HAPPENED

The fresh build session read the orders, then probed the two Binance endpoints
to record the real schema as ordered. The probe showed that **check (b) rests
on a false assumption and could never have passed** — not for a bad
implementation, but for any implementation.

The orders assume `premiumIndex.lastFundingRate` **is** the last settled
funding rate, and therefore that it can be cross-checked against the
`fundingRate` history endpoint expecting the *same number*. Measured:

    ASSET   premiumIndex.lastFundingRate   newest settled fundingRate   equal?
    BTC     0.00006211                     0.00005884                   NO
    ETH     0.00001104                     0.00002358                   NO
    SOL     0.00001776                     0.00006371                   NO

    premiumIndex.nextFundingTime = 2026-07-26 16:00:00 UTC
    newest settled fundingTime   = 2026-07-26 08:00:00 UTC

They are **different quantities**. `lastFundingRate` is the running *estimate*
for the NEXT settlement; the history endpoint reports payments that already
happened. Binance's own documentation confirms it: the pre-settlement figure
*"represents an estimation of the last 8 hours of the premium index."*

**And the obvious weaker fallback is also invalid.** Before assuming "well, at
least the signs should agree", that was measured too:

    BTCUSDT: predicted +  | last 3 settled ['+', '+', '+']
    ETHUSDT: predicted +  | last 3 settled ['+', '-', '+']
    SOLUSDT: predicted +  | last 3 settled ['-', '+', '+']

The settled sign flips between consecutive 8-hour periods. A sign-agreement
check between the two surfaces would have failed **at random**, on correct
code — the worst possible kind of check, because a session that saw it fail
would be tempted to wave it through, and the ship would learn to distrust its
own gates.

### WHY THIS ONE MATTERS MORE THAN THE USUAL TYPO

Check (b) is not a routine check. It is the ONLY check standing between this
ship and printing *the exact opposite of the truth* on the Brief every single
morning, and the orders say so in bold. **The single most important check in
Gate 3.2 was unpassable, and every other check in the gate would have passed
around it** — (a), (c), (d), (e) and (f) all verify that a number appeared and
that failure degrades honestly. None of them looks at whether the number means
what the line next to it claims.

**This is the SAME failure shape the previous session documented**, one step
later: a claim about a data source, written from assumption, never called. The
previous session caught it about a *future* step's data. This one was about
*this* step's data, sitting inside this step's own gate. The lesson generalises
further than first recorded: **a gate is only as good as the measurements
behind the claims it is built on, and gates get written from assumption too.**

### THE CORRECTION — STRICTER, NOT LOOSER

Recorded in full in SESSION_ORDERS.md with the original struck through and
left legible. Check (b) becomes three checks, all required:

- **b1 — EXACT IDENTITY.** The instrument also reads the last SETTLED rate.
  Settled rates are fixed historical facts, so the parsed value must match a
  fresh raw fetch **exactly, digit for digit, sign included** — an upgrade
  from the struck check's "within rounding". Settled and estimate values must
  pass through the SAME parse/format helpers, or the check proves nothing.
- **b2 — THE PRINTED NUMBER.** Every printed rate re-derived BY HAND from a
  fresh raw response; both numbers recorded in the log.
- **b3 — THE MEANING.** "Positive = longs pay shorts" verified against
  Binance's published documentation, an independent surface from the API,
  because **no endpoint can prove a naming convention.** Verified already:
  positive → *"traders long on a perpetual contract will pay a funding fee to
  traders on the opposing side"*; negative → *"traders short on a perpetual
  contract will pay a funding fee to long traders"*. Interval confirmed:
  *"every 8 hours at 00:00 (UTC), 08:00 (UTC), and 16:00 (UTC)."*

### THE REAL SCHEMA RECEIVED (recorded as ordered)

    GET /fapi/v1/premiumIndex?symbol=BTCUSDT   HTTP 200
    {"symbol","markPrice","indexPrice","estimatedSettlePrice",
     "lastFundingRate","interestRate","nextFundingTime","time"}

    GET /fapi/v1/fundingRate?symbol=BTCUSDT&limit=3   HTTP 200
    [{"symbol","fundingTime","fundingRate","markPrice","rateType"}]

    GET /fapi/v1/premiumIndex?symbol=NOTAREALSYMBOL   HTTP 400
    {"code":-1121,"msg":"Invalid symbol."}

All values arrive as STRINGS except `nextFundingTime`, `fundingTime` and
`time`, which are integer milliseconds. **`rateType` ("Regular") is a field
the orders did not know about** — recorded here, unused, so a future session
does not mistake it for a surprise.

The bogus-symbol result is noted because Gate 3.2 check (f) needs a per-asset
failure: an unmapped symbol yields HTTP 400 for that asset alone, which is
exactly the partial-failure path the check demands.

### DECISIONS TAKEN WEARING FABLE'S HAT (the Commander delegated; recorded so
### they can be overruled)

1. **Source stays Binance. No third-party library, no GitHub funding package.**
   The Commander twice offered an open-source fallback. It is declined because
   Binance is not failing — every endpoint answered HTTP 200 from his
   connection today. A wrapper would add a dependency that can break (the
   pandas-ta lesson, already in the IF/THEN table) and would hide the very
   schema the orders require us to record in Binance's own words.
2. **The Brief prints the ESTIMATE only, one request per asset**, per the
   orders' explicit call budget and output example. The session's own earlier
   suggestion of also printing the last settled rate on the Brief was
   **overruled by the session itself**: it would double the request count
   against an explicit written cap, and the settled rate's real job is exact
   verification, which belongs in the gate. Because both values run through
   the same parse/format helpers, b1 still guards the printed path.
3. **The independence problem is now WORSE than last session, and is not
   glossed.** Last session the planner and builder were the same mind. This
   session the same mind also amended the gate it will be judged by. The only
   protections that survive are (i) this amendment is committed BEFORE any
   code exists, with its measured evidence attached, and (ii) **a THIRD fresh
   session must review by recomputing from raw evidence — it should treat the
   amended (b) itself as a thing to be audited, not assumed.** The Phase 6
   second-AI requirement remains explicitly NOT waived.

### WHAT IS NOT YET DONE

`cockpit/funding.py` does not exist. Gate 3.2 has not been run. The next entry
reports the build and the full tally, pass or fail.
