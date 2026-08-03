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
**NEXT SESSION: TWO JOBS, IN THIS ORDER. (1) R-020 — a FIFTEENTH sabotage
against the open-interest recorder, invented by someone who built none of it.
(2) THEN CLOSE THE BRIEF'S TWO DOORS — THE COMMANDER RULED ON 2026-07-29
(evening) THAT THEY ARE TO BE CLOSED, AND IT IS HIS ORDER, NOT A SESSION'S
IDEA.** A session deferred that order because B14 graded SERIOUS the same
evening and his own rule says SERIOUS means build nothing — **recorded plainly so
he can overrule it in one word.**
**CONTEXT: EIGHT independent reviews in a row have each failed the repair before
them.** The newest, 2026-07-29 (evening), asked *every check finds the recorder's
work by asking the recorder where it put it — what if it puts it somewhere
else?* — and found that R-014's lesson had been applied to five VALUES the gate
compares and **never once to the ADDRESS the gate walks to.** All twenty-three
places that located a CSV asked the module's `csv_path()`, and no line anywhere
on this ship named `<SYMBOL>_4h.csv`. **B14 escaped: an ordinary filename
tidy-up that breaks no logic, writes no wrong number and whose report is TRUE —
it just moves the archive, and check (m), built the day before to prove the
archive survives, followed it to the new name and certified it.** Repaired as
Gate 3.2b-R6, FOURTEEN sabotages. **R-018 FAILED. R-019 CLEARED by the Commander
himself — he refused the session's wording for THE FINDING REPORT's Step 2.2 and
wrote his own, and `THE_PATTERN.md` now carries his words verbatim. R-001 has now
outlived SEVEN FAILED generations of fix and the eighth is untested — it moves
only when one SURVIVES an independent attack, and none ever has.**
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
| **Open-interest recorder (Phase 3, Step 3.2b) — Binance 30-day window, `period=4h`, append-only CSV per asset, idempotent, never rewrites history. GATE 3.2b-R3 PASSED 2026-07-28 (night): eleven bars and TEN sabotages caught; the drill judges THE CSV ON DISK against a raw fetch for every asset, and the asset list is **the gate's own (`GATE_SYMBOLS`), not the module's**. New check (k) builds **MONTH TWO** — a partial window seeded by the test, then appended to — because every other row-level check wrote into an EMPTY directory, so the gate had only ever tested month one and month one happens once. **B10** transposed the OI column on the append path alone: 80 of 180 rows landed 64,763x wrong and all nine sabotages were scored CAUGHT, B4 (that exact lie) among them. Two independent sabotages walked through the previous gate the same day: **B9** cut `SYMBOLS` to two assets and SOLUSDT vanished from the recorder *and from its own detector*, permanently, all green; **B8** made `--record` — the branch the monthly task actually runs, which no test had ever executed — always exit 0, so a failed job reported success. New check (j) now runs `--record` for real as a subprocess in BOTH outcomes, against a copy in scratch. 540 rows recorded. SCHEDULED 2026-07-27: task `ZarX Open Interest`, day 1 monthly, 09:00, on the laptop only (Binance geo-blocks US cloud runners), catches up if the laptop was off. **GATE 3.2b-R4 PASSED 2026-07-29: ELEVEN sabotages, new check (l) — THE PRINTED REPORT MUST MATCH THE DISK.** Every detector here read the CSV back off disk and **nothing had ever asserted that the line this recorder PRINTS is true** — yet that line is its only human-readable output, it goes to `journal/daily_runs.log`, and the Commander's standing order is to judge the recorder BY IT. **B11** wrote `'appended': len(fresh)` for `len(new_rows)`: the disk stayed byte-perfect, ten of ten sabotages were scored CAUGHT, and the report claimed 180 appended rows on a run that appended none (the healthy control printed 0). The gate now counts the rows ITSELF before and after, and runs the recorder TWICE — the lie is invisible on run one and plain on run two. **R-017 FAILED 2026-07-29 (afternoon): TWO OF TWO new sabotages walked through.** **B12** proved R-017's own filed doubt — the window timestamps were guarded by nothing, and a window derived from the CLOCK passed 11/11. **B13 is the worse one and it DESTROYS DATA:** an ordinary 'keep the file in step with the source' tidy-up, *whose printed report is TRUE*, deleted **34 rows** of the real archive (11 BTC, 12 ETH, 11 SOL) while eleven checks stayed green — because **every scenario the gate could build has stored ⊆ fresh, and in real life that is false from the very next run.** **GATE 3.2b-R5 (hardened 2026-07-29 afternoon): both ends of the printed window are now measured against a fetch the gate makes itself on BOTH sides of the run, and new check (m) seeds rows the source NO LONGER SERVES — proving first that they really are outside the window — and requires every one to survive the run byte for byte. THIRTEEN sabotages, all caught.** **R-018 FAILED 2026-07-29 (evening): a FOURTEENTH sabotage walked through.** **B14** — `csv_path` returning `f"{symbol}.csv"` instead of `f"{symbol}_{PERIOD}.csv"` — breaks no logic, writes no wrong number, loses no row from the file it writes, and its report is TRUE. **All twenty-three places in the file that located a CSV asked the module's own `csv_path()`, and no line anywhere on this ship named `<SYMBOL>_4h.csv`.** R-014's lesson had been applied to five VALUES the gate compares (`GATE_SYMBOLS`, `GATE_OFFLINE_WORDS`, `GATE_LIMIT`, `GATE_PERIOD_HOURS`, `GATE_REPORT_RE`) and **never once to the ADDRESS the gate walks to**; `_record_does_the_job` pins the FOLDER and that pin held, but nobody went the one level down. Against a copy of the REAL archive it left `<SYMBOL>_4h.csv` frozen at 180 rows and started a second file, printing `180 new row(s) appended, 180 stored` where the honest run prints 192 — and check (m), built the day before to prove the archive survives, seeded into the new filename and certified it. Graded SERIOUS (by accident; invisible on its face), **with the qualification recorded that B14 DESTROYS NOTHING — the two files together still hold every row.** **GATE 3.2b-R6 (hardened 2026-07-29 evening): the gate holds its own `GATE_CSV_SUFFIX`, fifteen calls across fourteen check sites now use `_gate_csv_path`, the six inside `_sab_*` deliberately do not, a named check prints both filename lists, and a failed name check REFUSES TO RUN rather than dying in a traceback. FOURTEEN sabotages, all caught.** **R-020 open against this repair.** Still known-weak: check (e) is BTCUSDT-only, B1 is a no-op on a UTC machine, `_raw_truth` still reads its fetch coordinates from the module it judges, **and no sweep was done for other ADDRESSES of the same kind in the two Context Deck instruments.** **MEASURED 2026-07-29: the recorder has run exactly ONCE ever (by hand, 2026-07-27, 0 rows appended); the commit-and-push branch has still never fired against real new rows; next scheduled run 1 Aug 09:00. THE ORDERS OF 2026-07-29 MORNING WRONGLY CALLED THAT ERRAND 'NOW DUE' — it is not, and the measurement wins. MEASURED THE SAME DAY against the real archive: a healthy run today appends 11 rows for BTCUSDT, 12 for ETHUSDT, 11 for SOLUSDT, so the honest expectation on 1 Aug is roughly THIRTY per asset and a stored figure near 210 — NOT 180.** **GATE 3.2b-R7 (hardened 2026-07-30, after an independent session found that SABOTAGE B9 HAD NEVER TESTED ANYTHING): the drill installs every sabotage with `globals()[attr] = repl`, which reaches a name only if the name is looked up AT CALL TIME — and `def run(symbols=SYMBOLS, ...)` freezes the tuple when the `def` runs, with `SYMBOLS` read nowhere else in the module. So B9 changed a name nothing reads, the recorder went on collecting all three assets (`mod.SYMBOLS` two, `run.__defaults__[0]` three, `SOLUSDT_4h.csv` 180 rows), and it was scored CAUGHT by the FIRST LINE of its judge — a name comparison that returns before `run()` is ever called. The half of `_covers_every_asset` its own docstring calls the only way to catch an asset going missing had NEVER been shown able to fail, and FOUR generations of this gate printed fourteen of fourteen over it. **THE REAL ONE-LINE DEFECT WAS AND IS CAUGHT — proved by running the whole gate against a scratch tree carrying it: exit 1, two red lines, SOLUSDT visibly absent. The EVIDENCE was broken, not the protection.** B9 is now a REAL TEXT EDIT in `_FILE_SABOTAGES`, judged by `_record_does_the_job` — the same function the healthy check uses, never a second copy of it — and proved to RETURN False rather than raise. New check (n) proves THE DRILL'S INSTALLER IS ABLE TO INSTALL: no globals-swap sabotage may target a name this module has frozen as a default argument, and it carries a positive control that must first find the frozen `SYMBOLS` in `run` before its silence is believed. PASSED, exit 0, ZERO red ticks, FOURTEEN sabotages caught. Production half (lines 1-242) sha256 `5347bfec…` IDENTICAL before and after, every diff hunk at line 359 or later. **R-024 is open against this repair and its author may never clear it. R-023 (CATEGORY B) is open too: on the real defect this gate exits 1 correctly but ends in a bare `FileNotFoundError` traceback instead of printing FAILED, because `symbols_ok` has no REFUSES-TO-RUN branch while `name_ok` does.** MEASURED 2026-07-30: a full 3.2b run takes **~4 minutes** on this machine — **CORRECTED 2026-07-30 (evening) BY THE TWELFTH GENERATION, FIVE CONSECUTIVE TIMED RUNS: 73, 80, 77, 73 and 74 SECONDS. ~75 s is the honest figure; '~4 minutes' was one unrepresentative reading and '55 seconds' in the orders was another. The funding gate, measured the same evening, takes 128 s, not the ~85 s the orders quote; fear_greed takes 40 s, which nobody had ever measured. THE FIGURE ON RECORD HAS NOW BEEN WRONG FOR THREE CONSECUTIVE SESSIONS IN TWO DIFFERENT FILES (R-026 doubt 8, R-027 doubt 10)** — R-020's fifth doubt, unmeasured for two sessions — and R-7 adds two further `--record` subprocess runs to that.** **GATE 3.2b-R8 (hardened 2026-07-30 afternoon, after the ELEVENTH generation attacked check (n) itself and found it BLIND): `_frozen_as_default` read `__defaults__` and nothing else, so three of the four places Python freezes a name were invisible — a KEYWORD-ONLY default (`__kwdefaults__`), a `functools.partial` binding, and a class body. Proved by a probe with the function copied verbatim (control valid: it sees the ship's own shape and the swap cannot reach it) AND by a real two-line binary-mode edit freezing `_utc_iso` as `*, _iso=_utc_iso` on `fetch_history`: the gate scored B1 and B2 `ESCAPED — THE GATE IS DECORATIVE` at line 149 and then certified at line 176 that "the swap reaches the module". **THE SHIPPED FILE HAD NO SUCH FREEZE — no `*,`, no `functools`, no classes, measured — and when one was written the drill went RED LOUDLY, so the blindness hid nothing by itself: it needs a SECOND flaw, a judge failing for a spurious reason, which is what actually made B9 silent.** The detector now reads all four places, and each is proved by a PLANTED EXAMPLE it must FIND before it may speak, plus TWO NEGATIVE controls: the correct call-time pattern must NOT be reported, and neither must a mere module-level alias. **THE SECOND NEGATIVE CONTROL EXISTS BECAUSE THE FIRST DRAFT OF THIS REPAIR FAILED ITS OWN GATE — it counted an alias as a freeze and a healthy file went red FOURTEEN TIMES, because `_RECORD_ORIGINAL = record` is the drill's own saved original. The distinction: what matters is not that another name holds the old object, it is that the module USES the old object without a fresh name lookup.** PASSED, exit 0, ZERO red ticks, FOURTEEN sabotages caught; the original attack re-run against the repaired file is now CAUGHT BY NAME (`FROZEN as a default argument in ['fetch_history']`) and the gate exits 1. Production half (lines 1-242) sha256 `5347bfec…` IDENTICAL before and after — **and the RECIPE, which nobody had recorded and which had to be found by experiment: the first 242 lines joined by CRLF with NO trailing separator.** **R-026 is open against this repair with NINE doubts and its author may never clear it; the most dangerous is doubt 9 — the alias negative control encodes one session's judgement about which freezes matter, and if that judgement is wrong the control will actively stop the next session finding what it hides.** **MEASURED 2026-07-30 afternoon, and it CORRECTS the figure in the line above: a full 3.2b run is 55 SECONDS, timed twice by wall clock (09:07:09→09:08:04 and 09:08:51→09:09:46), not ~4 minutes. Same file, same machine, same revision, same morning. Binance latency dominates and moves by a factor of four; the honest statement is that nobody has measured this gate often enough to quote a figure at all.** **GATE 3.2b-R9 (hardened 2026-07-30 evening, after the TWELFTH generation asked WHOSE CODE A SWAP REACHES — the part under test, or the test itself): check (n) printed of every globals-swap sabotage that 'the swap reaches the module' while measuring only that the name was not frozen as a default. THOSE ARE DIFFERENT CLAIMS. One added sabotage rebinding `_rows` — the GATE'S OWN CSV reader, defined inside `__main__`, which the production half cannot name — was scored CAUGHT, certified as reaching the module, printed zero red ticks and exited 0, while the recorder wrote 180 perfect rows spanning a full 30-day window, entirely untouched. THAT IS B9's SHAPE WITH THE FREEZE TAKEN OUT. And the detector, which names 'a class body' as one of the four places Python freezes a name, was proved blind to `@staticmethod`, `@classmethod` and `property` — in Python 3.10 none of the three exposes `__defaults__` through `vars(cls)`. Both SERIOUS on Steps 2.1 and 2.2; both LATENT, because all twelve real sabotages target production names and this module has one class with no methods. THE REPAIR: a second rule — every globals-swap target must appear as a WHOLE WORD in the production half, split at the `__main__` line — with SIX new permanent controls, including one that reports `_rows` ABSENT while stating out loud that a naive substring search finds it 6 times inside `new_rows`; plus `_holds` unwrapping staticmethod/classmethod/property, taking the detector's proved shapes from five to eight. PASSED, exit 0, ZERO red ticks, FOURTEEN caught, 18 controls, 74 s. Production half sha256 `5347bfec…` IDENTICAL before and after, every diff hunk at line 359 or later. The original attack re-run against the repaired file is CAUGHT BY NAME AND REASON and the gate exits 1. **R-027 is open against this repair with TEN doubts and its author may never clear it — the strongest being that `_named_in_production` is a TEXT search, so a name appearing only in a COMMENT still counts as code.**** | data/open_interest.py + data/oi_history/ | ✅ |
| Context Deck — instrument 1 of 5: Fear & Greed (alternative.me, free, keyless; injectable URL, fails to one offline line). **GATE 3.1-R5 (hardened 2026-07-28 night): the self-test rebuilds the WHOLE printed block and requires EXACT equality on BOTH paths the pilot can see — live AND offline — every constant it judges by is typed out in the gate and compared to the module's by name (the disclaimer, the history limit, the offline wording), and (new) it proves the doorway writes NOTHING to stdout or stderr of its own, on both paths, because the Brief is assembled only from what it RETURNS. It breaks itself FOURTEEN ways every run, all fourteen caught. **F14** printed 'historically a buying opportunity' straight to stdout with the returned block byte-identical, and walked through — in the same run that scored F7, 'the disclaimer turned into ADVICE', as CAUGHT. The offline bar was itself built from the MODULE'S `OFFLINE_WORDS` until 2026-07-28 evening, when F13 reworded that one constant so the lie and the bar moved together — the pilot's offline line read 'last known reading 72 — Extreme Greed' on a day the index read 29 — Fear, and the gate ticked it. **GATE 3.1-R6 (hardened 2026-07-29 night — R-016, THE COMMANDER'S OWN ORDER, carried out after two sessions deferred it): BOTH DOORS ARE CLOSED. PASSED, exit 0, SEVENTEEN sabotages caught.** The ear used to listen with `redirect_stdout`/`redirect_stderr`, which rebind a NAME — measured against the R5 ear itself, `os.write(1, …)` and a `logging` handler bound to the real stderr at import time BOTH returned `''` while printing trade instructions on the terminal. `_capture` now listens at the FILE DESCRIPTOR and compares against empty BYTES; `sys.stdout`/`sys.stderr` are proved still identical to `sys.__stdout__`/`sys.__stderr__`; the descriptors are proved given back; and **THE EAR IS MADE TO PROVE IT CAN HEAR DOWN ALL THREE ROUTES BEFORE ITS SILENCE IS BELIEVED** — three ticks reading 'wrote NOTHING' is exactly what a deaf listener prints. **DOOR 2: nothing anywhere watched what this module writes at IMPORT time**, and `brief.py` line 23 imports it, so one module-level `print` landed F14's advice ABOVE the Morning Brief's own header. A named check now imports the module in a FRESH INTERPRETER and requires return code 0 with both streams empty; **F17 drives it by a real binary-mode edit of a copy outside the repo — the only way to sabotage an import that has already happened — and REFUSES TO RUN if its anchor is not unique.** New permanent sabotages F15 (raw descriptor), F16 (handler bound before us) and F17 (advice at import time). **R-022 is open against this repair and its author filed seven doubts against his own work — the sharpest being that `brief.py`'s OWN import surface is still unwatched, and a `pandas_ta` UserWarning is already printing on the real Brief's first line.** **GATE 3.1-R7 (2026-07-31): DOOR 3 IS BUILT, and F10 was repaired on the Commander's ruling.** A fresh interpreter imports the module, calls `section_text()` on BOTH paths the pilot can see, discards what it returns and **then SHUTS DOWN** — the child's TOTAL output must be empty. Shutdown joins non-daemon threads, flushes every buffer and runs every atexit handler, so all three deferred shapes are caught DETERMINISTICALLY. **A1 thread / A2 kept-alive buffer over fd 1 / A3 atexit all CAUGHT, each planted ALONE and each matched BY ITS OWN MARKER** so a patch that merely crashed could not be scored a success; **A4, a thread that NEVER returns, is required to make the door report FAILURE — R-025 named the timeout as the single most likely way to build a door 3 that guards nothing, and that branch is PROVED to fire, every run.** **F10 WAS THE REASON THIS GATE WAS RED ON ARRIVAL:** it transposes yesterday and a week ago, both were 28, the swap changed not one byte and the drill called that an ESCAPE — **measured at 187 of 3,092 days, 6.05%, one day in 16.5.** The pair is now made distinct by the GATE'S OWN number, and **both branches plus the OLD BROKEN FORM (required to stay SILENT) are proved every run on synthetic readings**, so no future session can quietly regress it. PASSED, exit 0, 0 red, **62 s** (was 34 s before Door 3). Production half sha256 `bb31626c…` identical, every diff hunk at 742+. **R-032 is open against Door 3 with TEN doubts and its author may never clear it; R-029 (the F10 repair) and R-030 (this file says 'broken FOURTEEN ways' while running SIXTEEN) are CATEGORY B.** | cockpit/fear_greed.py | ✅ |
| Context Deck — instrument 2 of 5: funding rates (Binance USDⓈ-M public, free, keyless; USDT perpetuals, partial failure names the missing asset). **GATE 3.2-R5 (hardened 2026-07-28 night): the self-test rebuilds the WHOLE printed block from Binance raw using its own arithmetic and requires EXACT equality on EVERY path the pilot can see — healthy, degraded and offline — holds its OWN copy of the "positive = longs pay shorts" wording, of the tickers and of the offline wording, each compared to the module's by name; rotates the partial-failure drill through all three assets; (new) proves the doorway writes NOTHING to stdout or stderr of its own on all three paths, because `brief.py` runs the function before it prints what the function returns; and breaks itself FIFTEEN ways every run, all fifteen caught. **S15** printed 'close longs before the 16:00 settlement' to stdout with the returned block byte-identical, thirty times on the gate's own screen, and walked through. The offline bar was itself built from the MODULE'S `OFFLINE_WORDS` until 2026-07-28 evening, when S14 reworded that one constant and a fabricated "last reading BTC +0.0100%, longs paying" walked through with a tick mark reading "NOTHING appended". **GATE 3.2-R6 (hardened 2026-07-29 night — R-016, THE COMMANDER'S OWN ORDER, carried out after two sessions deferred it): BOTH DOORS ARE CLOSED. PASSED, exit 0, 55 checks green and 0 red, EIGHTEEN sabotages caught.** `_capture` now listens at the FILE DESCRIPTOR and compares against empty BYTES, so S16 (`os.write(1, …)`) and S17 (a `logging` handler bound to the real stderr before the gate exists) are both caught; the process's own streams are proved untampered and the descriptors proved given back; and **THE EAR IS MADE TO PROVE IT CAN HEAR DOWN ALL THREE ROUTES BEFORE ITS SILENCE IS BELIEVED.** **DOOR 2: a named check imports the module in a FRESH INTERPRETER and requires both streams empty**, because every check in every previous version ran in a process where the import was already over — one injected module-level line put '>> … the crowd is short, go long' ABOVE the Morning Brief's own header. S18 drives it by a real binary-mode edit of a copy outside the repo. **The refusal-on-ambiguous-anchor guard earned its place within sixty seconds: on its first run the anchor matched TWICE, because writing it into the file created the second match.** **R-021 IS OPEN AND CATEGORY B: this gate GOES RED NEAR A FUNDING SETTLEMENT and is green the rest of the time — a live-rate race in `_core_checks`/`_partial_checks`, whose before/after bookends cannot bracket a rate that moves twice, and near a settlement it does. **Binance settles at 00:00, 08:00 and 16:00 UTC.** PROVED BY CONTROLLED COMPARISON rather than asserted: the untouched `3.2-R5` bytes from commit `74ec950`, run in a scratch tree, FAIL x4 inside the window and PASS x2 outside it, while `3.2-R6` FAILS 3 of 4 inside and PASSES x3 outside — **so it is not the R-016 repair and the gate is not newly broken.** ~130 seconds per run. **The repair must tighten the BRACKET, never the BAR — and OUTSIDE A SETTLEMENT WINDOW A RED FUNDING GATE IS A REAL FAILURE.** An earlier version of this row said 'red about three runs in four' flat: measured in one 45-minute window and corrected the same night after the Commander asked why it had passed in previous sessions.** **R-022 is open against the R-016 repair itself.** Still unguarded: the block printed when TWO of three assets fail is built by no check anywhere. Still unguarded: the block printed when TWO of three assets fail is built by no check anywhere. **GATE 3.2-R7 (2026-07-31): DOOR 3 IS BUILT — R-025, the Commander's standing order, deferred SEVEN times, is shut.** A fresh interpreter imports the module, calls `section_text()` on all THREE paths, discards what it returns and **then SHUTS DOWN**, with the child's TOTAL output required to be empty. **A1/A2/A3 all CAUGHT, each planted ALONE and matched BY ITS OWN MARKER; A4 hangs the child on purpose and the door must call it a FAILURE.** The real module: 3 of 3 paths, exit 0 in 2.61 s, output EMPTY. PASSED, exit 0, 0 red, **122 s** (was 88 s before Door 3 — and 88 s, not the 128 s on record). Production half sha256 `95069d1b…` identical, every diff hunk at 874+. **R-032 is open against Door 3 and its author may never clear it.** **AND THE CONFINEMENT RECIPE ON RECORD WAS WRONG FOR BOTH COCKPIT FILES:** their hashes reproduce only from the raw byte prefix up to `__main__` (i.e. WITH the trailing CRLF); the 'no trailing separator' recipe is correct for `open_interest.py` alone. | cockpit/funding.py | ✅ |
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
   audit** · then news headlines
   (~~CryptoPanic free tier~~ **DEAD 2026-07-31 — now a PAID product, HTTP 403.
   REPLACED BY THE PUBLISHERS’ OWN PUBLIC FEEDS: CoinDesk, Cointelegraph,
   Decrypt, The Block, Blockworks. No account, no key, no new dependency.
   Full correction in EXECUTION_PLAN.md Phase 3 step 3**), event calendar, whale watch. Information ONLY, never signals. This closes the user's known blind spot: the system
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

---

# MEASURED FACTS ADDED 2026-07-31 (afternoon) — THE FOURTEENTH GENERATION

**Nothing shipped this session.** Three facts were MEASURED and one door was
attacked. Recorded here because the measurement always wins over any planning
document, including this one.

| What was measured | The number | How |
|---|---|---|
| **CryptoPanic free tier is UNREACHABLE from this repo** | `/api/v1/posts/?public=true` → **HTTP 403**; `/api/developer/v2/posts/` → **HTTP 404** | live request, 2026-07-31. `.env` holds one key, `TWELVEDATA_API_KEY`. **There is no CryptoPanic token. Phase 3 step 3 cannot be built or verified without one, and a session cannot create one.** |
| **S6 (`funding.py`, tickers miswired) is a COMPLETE NO-OP** | **15.84% of settlements — 1020 of 6441, one in 6.3** | Binance settled funding history, BTCUSDT 7549 / ETHUSDT 7315 / SOLUSDT 6516 settlements, 2019→2026. Most recent 2026-06-02 00:00 UTC, all three +0.0100%. **UPPER BOUND — the Brief prints the ESTIMATE, not the settled rate.** |
| **S2 and S4 (`funding.py`) are never inert** | **0 of 6441 settlements** | same series. They require every rate to round to zero at four decimals of a percent, which has not happened once. |
| **Door 3's child stops watching sooner than the pilot is exposed** | child **0.5-1.0 s** after the doorway · Brief **1.5-2.0 s** | one daemon thread per delay, planted once, markers counted in both the child's output and the real Brief. |
| **Door 3 is blind to a DAEMON thread** | shape A5 → **ESCAPED**, by Door 3's own judge | A1 with `daemon=False` → `daemon=True`, planted alone in a whole-repo copy; control silent first; A1-A4 all CAUGHT. |
| **Door 1 is Door 3's accidental backstop, and it holds today** | red at **1.25 s** and **1.75 s** | the same shape planted in the production path and run against the FULL gate: `GATE 3.1-R7 FAILED` both times. Nothing slower than that reaches the Brief at all. |
| Gate runtimes, re-measured | funding **122 s** · fear_greed **62 s** · open_interest **56 s** | unchanged from the figures the thirteenth generation put on record. **First session in five where the runtimes on record were right.** |
| `data/oi_history/` | 3 files, correct names, **181 lines each**, sha256 `e3258e82` / `1549a8a1` / `e0f91a87` | byte-identical since 2026-07-30. The 1 August errand was **not yet due** — `date -u` read 2026-07-31 11:11 UTC. |

**STILL TRUE AND STILL KNOWN-WEAK:** `cockpit/brief.py` has no gate · the
Category B pile is **eleven** deep · nine of R-032's ten doubts are untested ·
R-006 may never be cleared in-house.

---

# MEASURED FACTS ADDED 2026-07-31 (evening) — **THE NEWS SOURCE CHANGED**

**The Commander found that CryptoPanic is no longer free. The plan named a dead
source and nobody had checked.** Full correction, with the wrong plan struck and
left visible, in `EXECUTION_PLAN.md` Phase 3 step 3.

| Source probed | Result | Verdict |
|---|---|---|
| **CryptoPanic** `/api/v1/posts/?public=true` | **HTTP 403** | **DEAD — paid product now** |
| **CryptoPanic** `/api/developer/v2/posts/` | **HTTP 404** | **DEAD** |
| **cryptocurrency.cv** `/api/news` | HTTP 200, **`totalCount` 0 then 2750 on the same address inside two minutes**; `?lang=en` → **0 articles under HTTP 200**; declared `perPage: 10`, returned 3 | **REJECTED — cannot be checked. Also a middleman for the feeds below** |
| **newsapi.org** | free tier = **24-hour delay** + licence bars production use "including internally"; paid from **$449/month** | **REJECTED — day-old news, and forbidden** |
| **newapi.ai** | an AI API gateway | **NOT A NEWS SERVICE** |
| **CoinGecko** `/api/v3/news` | **HTTP 401** | **REJECTED — needs a key now** |
| **CoinDesk RSS** | **25 items, newest 3 minutes old at fetch** | **ADOPTED** |
| **Cointelegraph RSS** | **30 items, newest 11:35 UTC** | **ADOPTED** |
| **Decrypt RSS** · **Bitcoin Magazine RSS** | both answering | **ADOPTED / reserve** |

**ADOPTED DESIGN, ruled by the Commander 2026-07-31 (evening):** five publishers
(CoinDesk, Cointelegraph, Decrypt, The Block, Blockworks) — **NOT one hundred,
because beyond a handful the extra outlets return the same story reworded and
would corrupt any future count** · three headlines printed plus a count · **crypto
only** · a daily count archived from day one as **cheap insurance, not a
requirement** · **no new dependency** (`xml.etree.ElementTree` is standard
library) · **news is NEVER a signal — Phase 6's three slots are locked by name
and none is news.**

**UNMEASURED AND FILED AS R-036:** whether a news gate can verify anything at
all, given headlines land between two fetches. **The design rests on an
expectation nobody has tested.**

# MEASURED FACTS ADDED 2026-08-03 — THE FIFTEENTH GENERATION

**Nothing was built and neither ordered repair landed.** What shipped is **data**:
the open-interest archive was collected and pushed after the scheduled task
failed to do it. Every fact below was measured this session.

| What | Measured 2026-08-03 | Note |
|---|---|---|
| `data/oi_history/` | 3 files, correct names, **222 lines each (221 rows)**, sha256 `a1ed6729` / `a077cf03` / `c8d97f71` | window `2026-06-27T16:00:00Z → 2026-08-03T08:00:00Z`. Was 181 lines / `e3258e82` / `1549a8a1` / `e0f91a87`. **41 rows appended per asset, 123 total.** |
| Archive integrity across the write | **The old byte prefix of every file still hashes to its old value** — `e3258e82` / `1549a8a1` / `e0f91a87` at 11927 / 12115 / 11985 bytes | nothing rewritten, nothing pruned, first data row still `2026-06-27T16:00:00Z` |
| Binance's live 30-day window | `2026-07-03T12:00:00Z → 2026-08-03T08:00:00Z`, **186 rows** at `period=4h` | measured by the recorder's own gate, not assumed |
| Rows we hold that Binance NO LONGER serves | **35 per asset** | the archive is already irreplaceable; this is the number that proves it |
| Rows that would have been lost by 1 Sep | **33 per asset — 99 total** | had nothing run before the next scheduled date |
| The recorder's commit-and-push branch | **FIRED FOR REAL, FIRST TIME EVER** — `5c7c54a`, 3 files, 123 insertions, pushed | scoped to `data/oi_history` only; the pathspec held |
| `ZarX Open Interest` scheduled task | `Last Run Time 03-Aug-2026 11:47:41`, `Last Result: 0` — **and it did nothing** | no header, no Python, no rows, no commit |
| The other five ZarX tasks | **all six report `11:47:41, result 0`; the log holds ONE entry for that second** | five produced no evidence of any kind |
| Reproduced outside the repo | six identical batches appending to one log with `>>`: **one wrote, five wrote nothing — not even their header** | control first: one batch alone writes and exits 0 |
| Task Scheduler operational log | **DISABLED on this machine** | the record of 11:47:41 does not exist and cannot be recovered |
| Gate run times, this session | fear_greed **~60 s** · open_interest **~55 s** · funding **~125 s** | consistent with the figures of 2026-07-30 evening |

**THE CORRECTION THIS SESSION OWES THE RECORD.** The line in the recorder's
roadmap row saying *"the honest expectation on 1 Aug is roughly THIRTY per asset
and a stored figure near 210"* was **never tested, because the task never ran.**
The real figure, measured on 3 August, is **41 per asset and 221 stored.**

**AND THE ONE THAT MATTERS MORE:** the same row records the recorder as
`SCHEDULED 2026-07-27 … catches up if the laptop was off.` **It does catch up —
it caught up at 11:47:41 on 3 August and collected nothing while reporting
success.** *"Catches up"* is now known to be a claim about the trigger, not about
the work. **R-037.**
