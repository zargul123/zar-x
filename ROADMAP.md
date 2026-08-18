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
| Context Deck — instrument 3 of 5: **THE NEWS INSTRUMENT** (five publishers' own public feeds, read directly; no account, no key, no new dependency — `xml.etree.ElementTree` from the standard library). Prints three crypto headlines and a 24-hour story count. **INFORMATION ONLY — no sentiment score, no weight, no number derived from a sentence.** A headline that is itself ADVICE is printed in quotes and attributed, and the instrument's own voice never adopts it — **awkward case 1 arrived unprompted on the very first real run** (a price-prediction headline, quoted and attributed to its publisher and to the person by name). **GATE 3.3-R1 PASSED 2026-08-05: 54 checks, 0 red, TWELVE sabotages, every one CAUGHT and — the part that matters — every one PROVED TO CHANGE WHAT SOMEBODY READS before its verdict was counted.** (Shipped 2026-08-04 as GATE 3.3 — 50 checks, eleven sabotages — and **the very next day a session that had not built it found X1. The bar was raised, never lowered.**) **This is the SECOND file on this ship built with that rule from birth rather than retrofitted; F10, S6 and B1 were the same inert-sabotage fault in three files and cost three different generations a session each.** The witness is PER-SABOTAGE: N10 prints advice to stdout while returning a byte-identical block (S15's exact shape), so it is witnessed at STDOUT and not at the block — a drill measuring every sabotage on one channel would have scored it INERT and deleted the only check that catches it. The gate builds its own five feeds from its own constants, hands the SAME BYTES to the doorway (**one fetch, two readers**) and demands the whole block match a copy typed out in the gate CHARACTER FOR CHARACTER — on the healthy path, with a dead feed, with an empty feed, with each of the five publishers taking its turn at failing, and with all five down. Plus **one REAL live fetch judged LOOSELY on purpose**, because a gate that only judges bytes it handed over never tests the trip to the internet and is decorative. **THE DEAD-FEED GUARD IS THE ONE THE ORDERS DID NOT ASK FOR:** Blockworks answers HTTP 200 with fifty perfect, correctly-dated stories whose newest is **209 DAYS OLD**, so a feed staler than 48 h is named as no-data and contributes neither a headline nor one unit of the count. **KNOWN WEAK, said in the gate's own pass line rather than in a footnote: DOOR 3 LISTENS AT `sys.stdout`/`sys.stderr`, NOT AT THE FILE DESCRIPTOR, and nothing in it tests a write deferred to a thread or to an `atexit` handler** — the other two cockpit instruments catch all three, and did this session. **R-046 is open against it, R-044 against the five publishers, R-045 against its author's three judgement constants, and their author may clear none of them.** **>>> X1 — FOUND 2026-08-05 BY A SESSION THAT DID NOT BUILD THIS FILE, AND IN NONE OF THE FIVE PLACES ITS BUILDER NAMED AS WEAKEST. `ElementTree.findtext` returns the text BEFORE an element's first child and nothing after it, so a headline a publisher wrote as `Bitcoin <b>crashes</b> 20% as ETF outflows accelerate` reached the Brief as the single word `Bitcoin` — with NO CLIP MARK, no `[no data:]`, no exception, and all fifty checks green while it happened.** It is `_clip`'s own promise — *"a silent truncation would be this instrument quietly rewriting a publisher"* — broken through a door `_clip` cannot see, because the rewriting happens in `_parse` before `_clip` is reached; and when the markup came FIRST the title was empty and the story was DROPPED from the count in silence. **REPAIRED with a `_text` helper reading every scrap of text in the element, applied to ALL SIX fields (title, guid, link, pubDate and both Atom stamps) rather than only the one that was caught — the class, not the instance.** New permanent checks (r1)-(r4) and sabotage **N12**, which reverts `_parse` to the exact original fault and is PROVED to change the block before its verdict counts. **MEASURED THE SAME MORNING AND REPORTED AGAINST THE FINDING'S OWN INTEREST: 136 real titles across all five shipped publishers, NOT ONE carrying markup — it was never firing.** **R-047 (a future-dated stamp walks past the dead-feed guard, SMALL, filed not fixed), R-048 (an RSS+Atom document loses its Atom half, SMALL and weak) and R-049 (against the repair itself) are open, and their author may clear none of them.** | cockpit/news.py | ✅ |
| Context Deck — instrument 4 of 5: **THE EVENT CALENDAR** (`cockpit/events.py` — **NOT `calendar.py`, which would shadow a standard-library module**). A line on the Brief saying what is COMING — *"in 5 days — US CPI release (Wed 12 Aug 2026, 17:30 local)"* — so the pilot is never surprised by a scheduled event he could have seen. **INFORMATION ONLY: a date is a fact, and a date with a suggestion attached is advice and is forbidden.** Two sources, both sealed in this compartment under Law 2: **`data/events.json`, the Commander's own hand-edited file**, and **built-in FOMC and US CPI lists**. **GATE 3.4 PASSED 2026-08-07: 69 checks, 0 red, TWELVE sabotages, every one CAUGHT and every one PROVED to change what somebody reads before its verdict was counted — none INERT. Run twice, once at `TZ=UTC0`, identical both times.** **This is the THIRD file on this ship built with the sabotage-proof rule from birth, and the first outside the two original cockpit instruments to carry DOOR 3 AT THE FILE DESCRIPTOR plus a fresh-interpreter check that import, three doorway calls and shutdown write nothing — machinery `cockpit/news.py` still lacks (R-046).** **>>> NO DATE WAS REMEMBERED BY A MODEL. Every one was read off the issuing authority's own page on 2026-08-07:** FOMC from `federalreserve.gov` (the decision is the SECOND day of each two-day meeting, 14:00 US Eastern; **the Fed's own page marks the eight 2027 dates TENTATIVE and that word is printed on his screen rather than dropped**), and US CPI from `bls.gov` at 08:30 US Eastern. **`bls.gov` ANSWERS HTTP 403 TO A NON-BROWSER FETCH — the same edge block that killed The Block on 2026-08-04 — so it was read in a real browser. A session that hit that 403 and filled the gap from memory would have produced a calendar indistinguishable from this one and wrong.** **>>> THE TRAP THIS FILE IS SHAPED AROUND: A HARDCODED LIST OF DATES GOES STALE AND A STALE CALENDAR LOOKS EXACTLY LIKE A HEALTHY ONE** — Blockworks a second time, the recorder's empty-list trap a third, and **an empty deck line is indistinguishable from a genuinely quiet month.** So each list carries the last date its authority has PUBLISHED, past it the deck names THAT LIST as ENDED, nothing ahead at all is a LOUD line judged by exact equality, and **both horizons print on the Brief every day so the trap is visible before it fires.** **AND IT IS NOT HYPOTHETICAL: the BLS publishes about a year ahead and its schedule STOPS DEAD AT 10 DEC 2026, so the CPI list runs out in roughly four months — check (b) proves the guard by advancing the clock to January 2027 rather than waiting, and requires the FOMC list to carry on working in the same block.** **THE TIME-ZONE DECISION, which is where this would otherwise have been a day out with nothing saying so: every event is an INSTANT — a date, a time and a zone, never a bare date — the JSON file declares its own zone INSIDE the file, a file declaring none contributes nothing and is NAMED, and "today"/"tomorrow"/"in N days" are counted in the READER'S OWN local date.** Measured: his machine runs UTC+5, so counting in New York's date would have said *"US CPI tomorrow"* on the very morning of every release. Check (i) is the control — the same file rendered for Karachi and for UTC must DISAGREE. Awkward cases all held to exact equality: file missing, malformed, a bare `[]`, empty, no timezone, an unknown timezone, a past event, an impossible date, "next tuesday", a blank name, a 112-character name clipped VISIBLY, two events on one day, and four bad entries **refused AND COUNTED — never silently dropped.** **R-050 (every expected string was computed by hand and all 69 checks went green on the first run — four of them turn on US daylight saving), R-051 (the horizon guards the list running out, NOT a date changing inside it, and eight dates are tentative), R-052 (nobody but its author has run this gate or invented an attack on it) and R-053 are open, and their author may clear none of them.** | cockpit/events.py | ✅ |
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
3. **Context Deck** (cockpit) — 🔨 IN PROGRESS (EXECUTION_PLAN Phase 3, **4 of 5 done — the event calendar shipped 2026-08-07 under GATE 3.4, 69 checks, 12 sabotages, 0 red; the news instrument shipped 2026-08-04 under GATE 3.3, and was attacked, found leaking and repaired the next day: GATE 3.3-R1, 54 checks, 12 sabotages, 0 red**):
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
| **The publishers' own feeds are ADOPTED and MEASURED — and TWO OF THE FIVE ORDERED SOURCES WERE DEAD** | Measured 2026-08-04. **THE BLOCK: HTTP 403** on four addresses and two user-agents, eight attempts — edge-blocked, no path in. **BLOCKWORKS: HTTP 200 with FIFTY real, well-formed, correctly-dated stories whose NEWEST IS 209 DAYS OLD** — an abandoned feed that looks healthier than a healthy one, and would have put a January headline on the Brief under today's date. **That is `open_interest.py`'s empty-list trap wearing its best suit, and it is why `news.py` has a DEAD-FEED guard from birth.** **CRYPTOSLATE: HTTP 429 behind a Cloudflare challenge** — it rate-limits a repeat caller, found by the gate within an hour of my adopting it, exactly as R-036's second doubt warned. **SHIPPED FIVE: CoinDesk (25 items, newest 15 min), Cointelegraph (30, 37 min), Decrypt (39, 41 min), BeInCrypto (12, 25 min), Bitcoin.com (10, 26 min).** **R-036 MEASURED: 0 of 4 feeds changed their top story in 90 s; a publisher lands ~1 story an hour; median gap 33-61 min. The headline collision is REAL BUT RARE.** **R-044 is open: these are five names measured on one afternoon and nobody has watched them over a day.** |
| **THE FIVE PUBLISHERS, READ AGAIN ON A SECOND DAY — AND EVERY TITLE INSPECTED FOR MARKUP** | Measured 2026-08-05, one day after adoption. **All five answered HTTP 200 on all three readings that morning** (a standalone probe, the gate's own live check, and a real Brief run): **CoinDesk 25 items, Cointelegraph 30, Decrypt 59, BeInCrypto 12, Bitcoin.com 10.** **BeInCrypto — the Cloudflare-fronted one that bit the builder when it was CryptoSlate — was clean all three times.** **Story flow: 86 and 87 stories inside 24 h on two independent readings, about 3.6 an hour across five publishers**, which is the number under R-045's reasoning that an empty 24-hour window is a fault rather than quiet news. **AND THE ONE THAT DECIDED X1's SEVERITY: 136 title elements inspected, and NOT ONE carries markup inside `<title>`** — so the silent-truncation fault was real, proven and repaired, but was never firing. **R-044 stays open: three readings in one morning cannot see a weekend, a holiday, or a rate-limiter with a long memory.** |
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

# SHIPPED 2026-08-03 (second) — **THE COLLECTION GUARD, GATE 3.2c-R1**

| What | Where | State |
|---|---|---|
| **The collection guard (Phase 3, Step 3.2c) — reads `data/oi_history/` off disk and reports the newest row and its age. It asks THE DATA, never the job.** Built after R-037: the recorder fired on 2026-08-03, reported `Last Result: 0`, and collected nothing, while `CHECK_STATUS.bat` — the one screen the Commander runs — read that 0 and printed **OK**. **The status screen would have confirmed the failure as a success.** The cause of Windows' 0 is unproven and now unprovable (the Task Scheduler event log was off), **so the repair deliberately does not depend on knowing it.** GATE 3.2c-R1 PASSED, exit 0, zero red: all THREE verdicts — fresh, stale, and past Binance's own 30-day window — are driven every run from timestamps **the gate writes itself**, so no branch waits on the calendar to be seen firing (F10's lesson, applied from birth rather than retrofitted four sessions later). An archive under another filename is reported **MISSING**, not followed (B14). A file that exists but holds no row **fails loudly** (the recorder's empty-result trap). The log-sharing detector must FIND a planted collision — including one hidden behind `set LOG=` — and stay SILENT about a clean pair, before it is believed about the real batch files. The exit-code fault was **reproduced** (old shape reports a reassuring 0 while failing) and **proved fixed** (new shape reports 1), with a healthy run required to still report 0. Check (g) runs the **pilot path in a fresh interpreter** and requires its output to be the five-line block EXACTLY — added because the first draft printed the whole 90-line self-test on the Commander's status screen. **THE GATE WENT RED TWICE ON ITS AUTHOR'S OWN WORK BEFORE IT PASSED**, and its pass line names what it does NOT test (R-030 and R-033 were both gates overstating their scope). **R-039: the log-contention fault could not be reproduced on demand, so the gate asserts the SHAPE — nothing else writes where the recorder writes — and never the race.** **R-041 is open against this repair and its author may never clear it.** | `data/collection_guard.py` | ✅ |
| **The recorder's schedule and alarm, repaired.** MONTHLY → **WEEKLY** (Mondays 09:00, catch-up preserved, next run 10-Aug-2026, verified in `schtasks`). **The old reasoning in the batch header — "a single missed month loses nothing" — was WRONG and is corrected in place rather than deleted:** the task did not miss, it RAN and did nothing, so ONE silent failure was enough to put 99 irreplaceable rows a month from deletion. On a weekly cadence a silent failure costs **nothing**. The recorder now writes **its own log**, and ends with `exit /b %RC%` so Windows is told the recorder's result rather than the `copy`'s. | `run_oi_recorder.bat` | ✅ |
| **The status screen stopped trusting the job.** The word `OK` against a task is gone — it reads `exit 0`, a fact, with the line *"a job that does nothing can still report exit 0 - that is R-037"* underneath, and the archive's real age below that. | `CHECK_STATUS.bat` | ✅ |

## MEASURED FACTS ADDED 2026-08-03 (second)

| What | Measured | Note |
|---|---|---|
| `ZarX Open Interest` schedule | **Weekly, Mondays 09:00**, next run **10-Aug-2026 09:00** | `StartWhenAvailable` preserved; verified in the task XML after the change |
| Task Scheduler operational log | **DISABLED, and enabling it needs Administrator** | `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true` — on the Commander's desk |
| Batch files still sharing one log | **`run_daily.bat` + `run_snapshot.bat` → `journal\daily_runs.log`** | printed by the gate every run rather than hidden. R-040 |
| The four files the pilot reads | `brief.py` `6fa5ff96` · `funding.py` `bc0819ee` · `fear_greed.py` `d0c71344` · `open_interest.py` `98f95133` | **IDENTICAL before and after this session's work**, printed not asserted |
| `data/collection_guard.py` gate | **~10 s**, the fastest gate on the ship | it makes no network call at all |
| A LF-only `.bat` under `cmd` | **no output, exit 1, silently refused** | the 2026-07-19 incident, reproduced by accident 2026-08-03 |

# SHIPPED 2026-08-03 (third) — **S6 AND B1 REPAIRED. GATE 3.2-R8 AND GATE 3.2b-R10.**

| What | Where | State |
|---|---|---|
| **S6 can no longer be silenced by three matching rates (GATE 3.2-R8).** S6 miswires the tickers, but the printed LABEL comes from the dictionary KEY, so only the RATES rotated and the block was byte-identical whenever all three formatted the same — **up to 15.84% of settled funding periods, one in 6.3, and that is an UPPER BOUND measured on settled rates, never the live figure.** On those runs the drill reported ESCAPED about a lie it had never managed to tell, while the instrument and the Brief were correct. The payload now carries **the same three asset-to-contract pairs with the keys written in the GATE's own order**, so the rate-lie is untouched and a label-lie no market can silence is added on top of it. **FOUR branches print every run on rates the gate invents, with no network** — including the OLD form required to speak on differing rates (proving the repair did not weaken the rate-lie) and to stay SILENT on matching ones (proving the defect was real rather than remembered). **THE ORIGINAL FAULT WAS RE-RUN, NOT REMEMBERED:** Binance stubbed to answer +0.0100% for all three contracts, and the drill's own judge said **ESCAPED** for the shipped form and **CAUGHT** for the repaired one. **R-042 is open against this repair and its author may never clear it.** | `cockpit/funding.py` | ✅ |
| **B1 can no longer be silenced by a clock that is already UTC (GATE 3.2b-R10).** B1 writes the stamp as LOCAL time while still printing the `Z`; on a UTC machine local time IS UTC, so it changed nothing. **Measured: green at UTC+5 — the Commander's own laptop — and RED at UTC, same file, same tree, only the clock moved. It has therefore never cost him a red screen; it was blind on the cloud.** The repair is S5's, whose author wrote the reason down in 2026-07-28: when the local stamp comes out equal to the honest UTC one, and only then, B1 falls back to a **fixed seven-hour shift the gate types out** — deliberately not B2's one hour, and not a whole multiple of `PERIOD`. **The test is on the STAMP, not the offset, so the guarantee is structural.** Windows has no `time.tzset()`, so the offset is a PARAMETER: the live sabotage measures the real one and the control proves UTC, UTC+5 and UTC+5:30 in one run on any machine. **THE GATE PRINTS THE OFFSET IT MEASURED, because "I ran it under UTC" is a claim and a measured offset is evidence.** **THE ORIGINAL FAULT WAS RE-RUN:** the whole repo copied outside itself with B1 alone reverted, run at `TZ=UTC0` — ESCAPED, gate FAILED, exit 1, **while the reachability check printed its green tick in the same run.** **R-043 is open against this repair and its author may never clear it.** | `data/open_interest.py` | ✅ |

## MEASURED FACTS ADDED 2026-08-03 (third)

| What | Measured | Note |
|---|---|---|
| Every gate on the ship, after both repairs | `3.1-R7` · `3.2-R8` · `3.2b-R10` · `3.2c-R1` — **all exit 0, all zero red** | five runs, because the recorder's gate was run twice |
| The recorder's gate on a **UTC** clock | **exit 0, zero red, B1 CAUGHT** | the clock R-031 said it was blind on |
| `TZ=UTC0` under Windows Python | **HONOURED — measured, not believed** | the gate itself printed `+5.00 h` then `+0.00 h` |
| The OLD B1 on a UTC clock | **ESCAPED, gate FAILED, exit 1** — and the reachability check went GREEN in the same run | REACH and EFFECT are different questions; nothing here had ever measured the second |
| The OLD S6 on three equal rates | **ESCAPED** — the repaired form **CAUGHT** | judged by `_core_checks`, the drill's own judge, not by a new one |
| Production half of `cockpit/funding.py` | `95069d1b…` **unchanged** | lines 1..159 joined by CRLF, with a trailing CRLF |
| Production half of `data/open_interest.py` | `5347bfec…` **unchanged** | lines 1..242 joined by CRLF, no trailing separator |
| Earliest diff hunk in either file | line **1172** (`funding.py`) and **1182** (`open_interest.py`) | against `__main__` at 160 and 243 — confinement proved, not asserted |
| B1's fallback shift | **25,200 s (7 h)** | not B2's 3,600 s, and not a whole multiple of `PERIOD` ('4h') |
| `data/oi_history/` after five gate runs | 3 files, 222 lines each, `a1ed6729` / `a077cf03` / `c8d97f71` | **byte for byte what the session inherited** |

## **A CORRECTION THIS SESSION OWES THE ROW ABOVE IT**

**The row "The four files the pilot reads" in the 2026-08-03 (second) table
carries a WHOLE-FILE sha256 for each, and two of those four numbers are now
stale — correctly so.** The test halves of two files were edited on purpose:

    cockpit/funding.py       bc0819ee -> 6f30f42b     test half edited
    data/open_interest.py    98f95133 -> 0945a32b     test half edited
    cockpit/brief.py         6fa5ff96 -> 6fa5ff96     unchanged
    cockpit/fear_greed.py    d0c71344 -> d0c71344     unchanged

**A whole-file hash cannot tell "the pilot's code changed" apart from "the test
around it changed" — which is exactly why the bar for these repairs was written
against the PRODUCTION HALF and not the file.** Both production halves are
unchanged and both digests are in the table above.

---

# MEASURED FACTS ADDED 2026-08-07 — THE NINETEENTH GENERATION

**Every line below was measured on 2026-08-07. None is remembered, and the two
that came from outside this ship name the page they were read from.**

| Fact | Measured value | How it was measured |
|---|---|---|
| **FOMC decision dates** | 2026: 16 Sep, 28 Oct, 9 Dec. 2027 (**the Fed's own page marks these TENTATIVE**): 27 Jan, 17 Mar, 28 Apr, 9 Jun, 28 Jul, 15 Sep, 27 Oct, 8 Dec. **The decision is the SECOND day of each two-day meeting, 14:00 US Eastern.** | Read off `federalreserve.gov/monetarypolicy/fomccalendars.htm` |
| **US CPI release dates** | 12 Aug, 11 Sep, 14 Oct, 10 Nov, 10 Dec 2026, all 08:30 US Eastern | Read off `bls.gov/schedule/news_release/cpi.htm` |
| **>>> THE BLS SCHEDULE ENDS AT 10 DEC 2026** | They publish about a year ahead and the table simply stops. **The built-in CPI list therefore runs out in roughly four months and the staleness guard fires for real on 11 Dec 2026.** | The same page — the last row of the table |
| **>>> `bls.gov` ANSWERS HTTP 403 TO A NON-BROWSER FETCH** | 403 Forbidden, twice, on two addresses. **The same edge block that killed The Block on 2026-08-04.** It was read in a real browser instead. | Two fetch attempts, then a browser |
| **The Commander's machine runs UTC+5** | An 08:30 New York release prints as **17:30** on his Brief | The instrument's own live output, before any gate existed |
| **`zoneinfo` works here** | Python 3.10.18, `tzdata` 2025.2 present, 599 zones. **Windows has no system zone database, so this instrument depends on the `tzdata` package; without it every event is refused and the deck says so rather than falling back to UTC.** | `ZoneInfo('America/New_York')` resolved, EDT and EST both correct |
| **`strptime('%Y-%m-%d')` accepts `'2026-8-1'`** | Accepted as 2026-08-01. `'2026-13-45'`, `'2026-02-30'` and `'next tuesday'` are all refused. | Measured directly, before it was filed as R-052 point 1 |
| **>>> THE ORDERS' PRODUCTION-HALF HASH RECIPE WAS AN ARTIFACT** | The orders recorded `open_interest.py` as joining with **NO** trailing separator and the other two **WITH** a trailing CRLF, as though the files differed. **BOTH JOINS ARE BYTE-FOR-BYTE RAW PREFIXES OF ALL FIVE INSTRUMENT FILES.** All three remembered hashes reproduce exactly once the matching variant is used. **The files do not differ; the recipe was only ever which variant each session happened to pick.** R-053. | Both joins computed and compared against the raw bytes of all five files |
| **Production-half sha256, with the trailing CRLF** | fear_greed `bb31626c493a1ac6…` (line 113) · funding `95069d1bef8316d7…` (160) · news `503663762315b2f2…` (272) · open_interest `c68508e881524cf0…` (243) · collection_guard `d6518cd7208eb611…` (156) | The join verified to be the raw prefix before any hash was printed |
| **News, 2026-08-07** | **82 stories from 5 of 5 publishers** at the gate's live check; 80 at the Brief twenty minutes later. All five answered on every reading. | GATE 3.3-R1 check (c), then `cockpit/brief.py` |

## **A CORRECTION THIS SESSION OWES A HABIT, NOT A ROW**

**`git show HEAD:<file>` HANDS BACK THE BLOB, AND THE BLOB IS LF.** Every CRLF
file on this ship looks LF-only in HEAD. A line-ending check written against it
proves nothing, and this session wrote one, believed it for a minute, and nearly
reported `README.md` and `SHIP_LAWS.md` as damaged when they have been LF-only
all along and no session may change either. **Line endings are judged in the
WORKING TREE. Mojibake counts CAN be compared against HEAD, because those come
from decoded text and line endings cannot affect them.**

# MEASURED FACTS ADDED 2026-08-11 — THE TWENTIETH GENERATION

**Nothing shipped this session and no `.py` file was modified.** What follows was
MEASURED, and it is written here because the next session is going to choose a
whale-watch source and must not choose on a guess. **Four sources on this ship
have been found broken by measurement and none by assumption.**

| Measured fact | The measurement |
|---|---|
| **THE WHALE WATCH'S FREE SOURCES, PROBED 2026-08-11 08:44 UTC.** Nine endpoints, each recorded with HTTP status, seconds, bytes, row count and **the age of the newest row** — because Blockworks answered HTTP 200 with fifty perfect stories 209 days old. | **BINANCE, FREE AND KEYLESS, on a host this ship already reaches:** `/futures/data/topLongShortPositionRatio` **HTTP 200, 0.48 s, 3 rows, newest 5 min old**; `/futures/data/topLongShortAccountRatio` **200, 0.33 s, 5 min**; `/futures/data/globalLongShortAccountRatio` **200, 0.33 s, 5 min**; `/futures/data/takerlongshortRatio` **200, 0.30 s, 10 min**; `/futures/data/openInterestHist` **200, 0.30 s, 5 min** (already collected monthly by `data/open_interest.py`). **READINGS AT 08:44 UTC: top traders 61.01% long by POSITION (ratio 1.5649), 63.02% long by ACCOUNT (1.7042); the crowd 62.09% long (1.6378); taker buy/sell 0.7593.** **KEYLESS ON-CHAIN:** `api.blockchain.info/charts/estimated-transaction-volume-usd` **200, 1.05 s**; `.../output-volume` **200, 1.15 s**; `api.blockchair.com/bitcoin/stats` **200, 1.04 s** (961,985 blocks, 613,357 transactions in 24 h); `mempool.space/api/v1/fees/recommended` **200, 0.61 s**. **These give chain-wide totals, NOT exchange flows.** **>>> THE HONEST GAP: exchange RESERVE and NETFLOW series — the thing the plan asks for most directly — are CryptoQuant, Glassnode and Whale Alert, and ALL THREE PUT IT BEHIND A PAID KEY. None was probed because none is free. The whale watch cannot be an exchange-flow instrument and must not be worded as though it were.** **R-056 is open: nine endpoints answering on one morning is not nine endpoints that work, and CryptoSlate was found rate-limiting within an hour of being adopted.** |
| **THE EVENT CALENDAR'S SIXTEEN DATES WERE RE-READ OFF THEIR AUTHORITIES ON 2026-08-11 — the first time anybody on this ship has asked whether a source is still saying the same thing (R-035, R-051).** | **NOT ONE HAS MOVED since 2026-08-07.** `federalreserve.gov/monetarypolicy/fomccalendars.htm`: all eleven meeting dates match, decision on the second day — 2026 15-16 Sep, 27-28 Oct, 8-9 Dec; 2027 26-27 Jan, 16-17 Mar, 27-28 Apr, 8-9 Jun, 27-28 Jul, 14-15 Sep, 26-27 Oct, 7-8 Dec — **and the tentative note is unchanged word for word.** `bls.gov/schedule/news_release/cpi.htm`: 12 Aug, 11 Sep, 14 Oct, 10 Nov, **10 Dec 2026**, all 08:30, **and the schedule still stops dead at 10 Dec 2026**, so the horizon printed on the Brief is still the right horizon and the guard still fires for real on 11 Dec 2026. **`bls.gov` STILL ANSWERS HTTP 403 to a non-browser fetch — reproduced today — so it was read in a real browser again.** **R-051 IS NOT CLEARED BY THIS: one hand check on one day is a demonstration that the guard could exist, not a guard.** |
| **GATE TIMINGS, CORRECTED. THE MEASUREMENT WINS.** | Measured 2026-08-11, all eight invocations from one script: fear_greed **65.6 s**, funding **124.7 s**, open_interest **65.5 s** and **62.1 s** at `TZ=UTC0`, collection_guard **7.6 s**, news **4.7 s**, events **1.5 s** and **1.3 s** at `TZ=UTC0`. **The orders on record quote news at ~25 s and events at ~5 s. Both are wrong and both are wrong in the SAFE direction, which is exactly why nobody would have caught them.** |
| **GATE 3.4's STALENESS GUARD IS NOT TESTED AT ITS BOUNDARY, AND TWO BREAKS PROVED IT (R-054).** | Measured 2026-08-11 in a copy of the whole repo outside the repo, control green FIRST (exit 0, 0 red) and a positive control proved to turn the gate red (exit 1, 3 red). **Twenty days of slack in `_expired` — ESCAPED. An off-by-one in `_expired` — ESCAPED. The `DEFAULT_TIME` path changed while the constant was left alone, moving one of the Commander's own events a whole day — ESCAPED.** Checks (b) and (c) advance the clock 26 days and a year past the horizon and **never once to the day it fires.** All three breaks were PROVED to change what the doorway returns; all originals restored byte-for-byte and verified. |

# **>>> RULED BY THE COMMANDER 2026-08-11 (evening) — R-054 IS SMALL, AND THE NEXT BUILD IS INSTRUMENT 5 OF 5**

**His words, verbatim:** *"OK MAKE IT IN SMALL CATEGORY AND I THINK SESSION WILL
BUILT THE NEXT STEP."*

| What was decided | What it means for the next session |
|---|---|
| **R-054 IS SMALL — CATEGORY B, FILED, NOT REPAIRED, NOT CLEARED.** The three sabotages that walked through GATE 3.4 (twenty days of slack in the staleness guard, an off-by-one in it, and the `DEFAULT_TIME` path changed while the constant stayed pinned) are a recorded, unfixed weakness in the TEST. He was shown the argument for SERIOUS as well and chose SMALL knowing both. | **Nothing is blocking the build.** GATE 3.4 still cannot say no at its own boundary and that is now a known, accepted state until the Category B pile is cleared — which happens before the ship is used for real, at the same moment `cockpit/brief.py` gets its gate. **The pile is still twenty-seven: a ruling of SMALL puts an item INTO the pile, it does not take one out.** |
| **THE NEXT BUILD IS THE WHALE WATCH, INSTRUMENT 5 OF 5, UNDER GATE 3.5** — declared and committed alone on 2026-08-11 by a session that will never build it, so the bar cannot be lowered to match what gets built. | The sources are **already measured** (2026-08-11 08:44 UTC, in the facts above): Binance's own keyless top-trader positioning is the honest free footprint; **exchange reserve and netflow data is PAID and therefore out**, and the wording on the Brief must not imply otherwise. **Re-probe before choosing anyway — R-056.** |
| **THE PRECEDENT, NOW A DECIDED QUESTION RATHER THAN AN ARGUMENT EACH SESSION HAS WITH ITSELF:** a gap in a TEST, where the shipped output is proved correct, is SMALL and does not stop a build. | **It cuts one way only.** It says nothing about a fault that makes the Brief wrong today, which remains SERIOUS and still stops everything. **And it does not loosen GATE 3.5** — conditions 11 and 12 were written because of R-054 and stand exactly as written. |
| **IT IS NOT AN EXEMPTION FROM PART 1.** When he exempts a session he says so in words; *"i exempt only this for next session"* was the last one, 2026-08-05. He did not use those words here. | **Part 1 stands, uncapped: verify R-049, then build.** What changed is the priority, not the duty. **No session may read a reduction into a sentence about building.** |

# **>>> RULED BY THE COMMANDER 2026-08-11 (evening, second ruling) — THE NEXT SESSION IS EXEMPT FROM PART 1 AND BUILDS INSTRUMENT 5 OF 5**

**His words, verbatim:** *"we are only making exemption for next session to not
attack your check and i think there is nothing to attack for next session what
have you done."*

| What was decided | What it means, and what it does NOT mean |
|---|---|
| **THE NEXT SESSION ATTACKS NOTHING.** He was right about the half he observed: **the twentieth generation shipped ZERO LINES OF PROGRAM CODE**, so there is genuinely nothing of its for a fresh session to break in a scratch copy. The only things of its that can be questioned are its two clearances and the bar it set, **and it filed those against itself as R-055.** | **A session that ships no code leaves nothing for Layer 3 to bite on.** That is arithmetic, not a loophole, and he saw it before anybody pointed it out. **The exemption dies with that session and no session may renew it, extend it, or grant one to anybody.** |
| **R-049 IS DEFERRED A THIRD TIME**, and this half was a judgement rather than an observation. He was told the cost before ruling: a self-marked repair — the session that found X1 wrote the fix AND the checks that mark it — touching **all six fields of every story**, running on every headline on his Brief every morning. | **The measurement that supports him is real: 136 real titles across all five publishers, NOT ONE carrying markup**, measured by the repair's own author and reported against his own interest. **The bug it fixes has never once fired in production.** **The measurement that does not: nobody outside has ever shown the repair works.** Both are true. **Offer it to him again when the deck is five of five, and say "third time" out loud.** |
| **PART 1 HAS NOW BEEN REDUCED FIVE TIMES** — 2026-07-31, 2026-08-03 (twice), 2026-08-05, and now. | **THE STREAK WAS BROKEN IN BETWEEN.** The twentieth generation ran Part 1 in full, uncapped and unexempted, **and found three sabotages walking through a green gate in a morning.** That is not "four in a row" any more — **but the outside check is still the only thing on this ship that has ever caught what a builder could not see.** |
| **THE EXEMPTION IS BOUNDED, AND THE BOUNDS ARE WRITTEN DOWN** rather than left to the next session's judgement. | **It does NOT cover proving the ship alive first** (eight invocations, read, red ticks counted by machine). **It does NOT cover the sabotage drill inside what gets built** — that is the thing being built, not an outside check. **It does NOT loosen one condition of GATE 3.5**; conditions 11 and 12 were written because of R-054 and stand exactly as written. |

# **>>> SHIPPED 2026-08-11 (night) — `cockpit/whales.py`, THE WHALE WATCH. PHASE 3'S CONTEXT DECK IS FIVE OF FIVE AND COMPLETE.**

| What now exists and works | The measurement behind it |
|---|---|
| **`cockpit/whales.py` — the Whale Watch, Context Deck instrument 5 of 5.** One doorway (`section_text`), everything injectable, every default resolved from `None` IN THE BODY, never raises, never prints. **GATE 3.5 PASSED, 100 checks, 0 red, run twice — once normally and once at `TZ=UTC0`, ~7 s each.** | Two Binance endpoints side by side for BTC/ETH/SOL: `/futures/data/topLongShortPositionRatio` (its largest accounts, weighted by POSITION SIZE) beside `/futures/data/globalLongShortAccountRatio` (every account on the venue). Live at 12:55 UTC: BTC top 61.0% / all 60.6%, ETH 57.4% / 70.8%, SOL 63.2% / 67.7%. |
| **THE HONEST-NAME RULE IS ON THE BRIEF, NOT IN A DOCSTRING.** | Exchange RESERVE and NETFLOW — what the plan asks for most directly — is PAID at CryptoQuant, Glassnode and Whale Alert. So the line says, every morning, in his sight: **NOT exchange flows, NOT wallet tracking, NOT the world's whales.** It is one venue's own figures about its own customers. |
| **THE SOURCES WERE RE-PROBED BEFORE ANYTHING WAS ADOPTED (R-056), and two questions the first probe never asked were answered.** | 2026-08-11 12:33 UTC, four hours after the first probe: all four positioning endpoints HTTP 200 for all three assets, 0.30–0.51 s, newest row 3.1 min old. **A burst of TWELVE requests in a few seconds returned twelve 200s and no rate-limit.** `period` supports 5m/1h/4h/1d; **`7d` is refused, code -1130.** **R-056 IS NOT CLEARED BY THIS** — two probes four hours apart is two probes, and the session that adopted the source may not certify it. |
| **THE ROUNDING RULE IS MEASURED, NOT ASSERTED — AND THE FIRST ASSERTION WAS FALSE.** | The file claimed `0.6085` is a value where float formatting disagrees with half-up rounding. **IT IS NOT** — both routes give 60.9. The gate caught it on the FIRST RUN (1 red of 100) because the claim had been written as a check rather than a sentence. **Enumerated instead: 501 of the 10,001 four-decimal shares Binance can send DO disagree, and `0.5525` — ETH's own top-account figure — is one of them: 55.3% here, 55.2% by the float route.** The enumeration now runs on every gate run, forever. |
| **THE PRODUCTION-HALF HASHES, RE-MEASURED RATHER THAN REMEMBERED (R-053).** | `fear_greed` `bb31626c493a1ac6` · `funding` `95069d1bef8316d7` · `news` `503663762315b2f2` · `collection_guard` `d6518cd7208eb611` — **all four reproduce the recorded numbers exactly.** First measurements: `events` `6fc5ce7d67aa8f24`, `whales` `d2cd1b58373d2fcb`. |
| **>>> AND TWO CORRECTIONS TO THAT RECIPE. THE MEASUREMENT WINS.** | **(1) The orders' label is wrong.** They say the recorded hashes were taken *"with the trailing CRLF"*. They were not — they come from the prefix **WITHOUT** the anchor line; with the anchor and its CRLF the same untouched `fear_greed.py` hashes `39aa756e…`. The files have not moved (`git log`: last changed at `d78b2e0`). **(2) `data/open_interest.py` CANNOT BE HASHED THIS WAY AT ALL** — the anchor `if __name__ == '__main__':` appears **TWICE** in it, once for real and once quoted inside its own gate at line 1918. The hashing script REFUSED rather than splitting on the first hit, which is the eleven-session anchor rule earning its keep. |
| **A HOLE IN THE SHIP-ALIVE COUNTER, FOUND AND FILED AS R-057.** | It counted `✗` characters. **`data/collection_guard.py` prints `OK  ` and `FAIL `, not tick marks**, so it scored 0 red / 0 green — and a genuine failure there would have scored 0 red too. Found by noticing a suspicious timing, never by a check. **The corrected counter makes three independent passes over the same bytes** — the tick character, the first word of a line, and the phrase "GATE … FAILED" — and the whole 2,300-line capture came back **697 green, 0 red, 13 gates PASSED, vault INTACT, on all three passes.** |
| **GATE TIMINGS, CORRECTED AGAIN.** | Measured 2026-08-11 (night), ten invocations from one script: fear_greed **63.4 s**, funding **122.1 s**, open_interest **50.1 s** and **48.1 s** at `TZ=UTC0`, collection_guard **0.7 s**, news **5.3 s**, events **0.3 s** twice, **whales 7.2 s and 6.4 s**. |

## **>>> WHAT IS NOT PROVED ABOUT THE NEWEST INSTRUMENT, SAID HERE RATHER THAN IN A FOOTNOTE**

**NOBODY BUT ITS AUTHOR HAS EVER LOOKED AT `cockpit/whales.py`.** One hundred
checks and fourteen sabotages, all written by the session that wrote the code.
**That is R-058 and the next session's first job is to attack it.** GATE 3.4 also
reported 69 green, and a fresh session found three sabotages walking through it
in a single morning.

**AND THE GATE ITSELF NAMES WHAT IT CANNOT DO, IN ITS OWN PASS LINE:** it cannot
tell whether Binance's published figures are honest — only that this file reports
them faithfully; it cannot see an endpoint that answers today and rate-limits
next week; and it proves nothing whatever about whether positioning data is
USEFUL. **This is an information instrument. It will never become a signal.
Phase 6's three slots are locked BY NAME.**

---

# MEASURED FACTS ADDED 2026-08-18 — THE TWENTY-SECOND GENERATION

**Nothing shipped this session. Not one byte of any `.py` file changed.** What
follows was measured while attacking `cockpit/whales.py`, which this session did
not build.

| What was measured | The measurement |
|---|---|
| **GATE 3.5 CANNOT SEE A FAULT IN `_get`, THE ONLY CODE ON THIS SHIP THAT ACTUALLY SPEAKS TO BINANCE.** Almost every check injects a fake transport, so the real four-line function never runs; the excellent recording transport proves what the module ASKED FOR, but it REPLACES `_get` and cannot testify about it. The one check that executes `_get` is the live fetch, whose only numeric bar is the BTC top-account figure within 1.0 point. | **Two sabotages inside `_get`, each PROVED to change the live block, each walking through `GATE 3.5 PASSED — 100 checks, 0 red`. X15** (hardcode the symbol `BTCUSDT`): ETH and SOL printed BTC's numbers — all three coins showed `59.9% / 60.3%`. **X16** (ask the TOP endpoint for both populations): every coin printed the same figure under both names — `BTC 59.9/59.9, ETH 58.4/58.4, SOL 61.2/61.2` — **which is precisely what the gate's own check (a2) exists to forbid, proved on fixtures only.** Control X26 (row limit 1 → 500) was CAUGHT, exit 1, 2 red, so the rig was proved able to go red. **R-060, BORDERLINE, on the Commander's desk. NOT REPAIRED.** |
| **THE SHIPPED DOORWAY IS ROBUST — MEASURED, NOT ASSUMED.** Fed NaN, infinities, huge-exponent zeros, non-numeric fields, rows that are not dicts, replies that are not lists, negative timestamps and absurd timestamps. | **It never raised and never printed.** Every hostile payload came back as a named absence inside the block. The `Decimal`/`ROUND_HALF_UP` path, the six-independent-fates design and the named-refusal vocabulary all held. |
| **FOUR SMALLER MEASUREMENTS, ALL DATA CASES, NO CODE CHANGED.** | **(1)** The header is built OUTSIDE the per-reading guard: an unrenderable stamp collapses the block to `🔌 Whale watch offline (OSError)` — **but only when it is the last reading standing**, because `_oldest` takes the minimum (R-061). **(2)** A timestamp tie is broken by POSITION while `_newest`'s docstring says it is not — the same two rows in opposite order printed **60.9%** then **20.0%** (R-062). **(3)** The staleness guard only looks one way: a row six hours in the future printed as healthy; **one year** in the future printed `oldest 12:00 UTC` and looked current, because `_hhmm` carries no date (R-063). **(4)** **R-058's doubt 2 is settled AGAINST its author** — with no shorts in the population the cross-check is skipped and a swap prints `100.0% long` where the truth is 0% (R-064). |
| **THE LIVE WHALE WATCH, 2026-08-18 08:40 UTC** — recorded because a second real reading of this instrument now exists to compare against the first. | **BTC top 59.9% / all 60.3% · ETH top 58.4% / all 71.8% · SOL top 61.2% / all 69.9%.** (First reading, 2026-08-11 12:55 UTC: BTC 61.0/60.6, ETH 57.4/70.8, SOL 63.2/67.7.) |
| **ALL TEN GATE INVOCATIONS, TIMED ON THIS MACHINE THIS MORNING** — because the figures on record have been wrong three times in two files (R-026 doubt 8). | `fear_greed` **63.4 s** · `funding` **124.3 s** · `open_interest` **56.2 s**, and **57.6 s** at `TZ=UTC0` · `collection_guard` **6.7 s** · `news` **5.9 s** · `events` **0.6 s**, and **1.4 s** at `TZ=UTC0` · `whales` **8.4 s**, and **6.9 s** at `TZ=UTC0`. **All exit 0, all 0 red.** |
| **A CRUDE RED-COUNTER INVENTS FAILURES AS WELL AS MISSING THEM (R-057, pointing the other way).** | This session's own machine counter scored the funding gate as **1 red**. It was **the word "escaped" beginning a sentence of the gate's own explanatory prose**, line 137. Cleared by a human reading the line — never by a check. |

---

# MEASURED FACTS ADDED 2026-08-18 (later) — THE REPAIR THE COMMANDER ORDERED

| What shipped | The measurement |
|---|---|
| **GATE 3.5-R1 — `cockpit/whales.py`. THE REAL TRANSPORT IS NO LONGER TAKEN ON TRUST.** The gate stands up an HTTP server of its own on `127.0.0.1`, on a port the OS picks, and calls the doorway with `base_url` pointing at it and **no transport argument**, so the genuine `_get` makes the trip over a real socket. **Both halves are judged:** the path, symbol, period and limit of all six requests, read off the wire and compared to six tuples **typed out in the gate as literal strings**; and the block that came back, held to `GOLD_EXPECTED` byte for byte — the same copy the fake transport must produce. **No Binance request is made by this check.** Three new permanent sabotages: **W15** (`_get` pinned to one symbol), **W16** (`_get` pinned to one endpoint), **W17** (`raise_for_status` dropped). `_get` joined the restoration check. | **PASSED, 107 checks, 0 red, run twice — normally and at `TZ=UTC0` — with an IDENTICAL tick sequence compared by machine. 6.9 s and 8.4 s.** All seventeen sabotages CAUGHT, none INERT. **W17 was INERT this morning and its verdict was thrown away; it is provable now because the gate's own server answers an unrecognised request with HTTP 500 — the first thing on this ship ever to exercise `raise_for_status`.** |
| **WHAT CERTIFIES THE REPAIR IS THE ATTACK, NOT THE DRILL.** The three faults that beat the old gate were re-applied as **REAL TEXT EDITS** to a copy of the repaired repo outside the repo, with the repaired control required to pass first (Step 0.1). | **control exit 0 / 0 red · X15 exit 1 / 4 red · X16 exit 1 / 3 red · X17 exit 1 / 2 red.** This morning all three produced `GATE 3.5 PASSED — 100 checks, 0 red`. **And an undesigned property fell out: with the real fault already in the file the matching sabotage reports INERT, which is itself a FAIL — so each fault reddens the gate for two independent reasons.** |
| **THE PRODUCTION HALF DID NOT MOVE, PROVED TWO WAYS.** | sha256 `d2cd1b58373d2fcb` **before and after** — unchanged. Diff hunks at lines **1222, 1244, 1358, 1396, 1406 and 1439**; the `__main__` line is **363**, so the nearest change is 859 lines below it. The patch script checked all seven anchors before writing a byte, and refused on a non-unique anchor, on a bare newline, or on the hash moving. |
| **THE HASH RECIPE IS CONFIRMED, AND ONE RECORDED LINE NUMBER IS OFF BY ONE.** | The recipe — sha256 of the prefix BEFORE the `__main__` line, without the anchor line — reproduces `events` `6fc5ce7d67aa8f24` and `news` `503663762315b2f2` exactly. **`whales.py`'s `__main__` is at line 363, not the 362 on record.** The hash is identical, so the prefix is identical; only the counting of the anchor line differs. **The measurement wins and is written down rather than left.** |
