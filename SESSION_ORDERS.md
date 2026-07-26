# ZAR X PHASE 3 — THE SEVENTH SABOTAGE, THEN THE FEAR & GREED KNIFE, THEN STEP 3.2b (a gate is strongest where it has already been attacked; find where it has not)

*Written 2026-07-26 by the session that audited Gate 3.2, failed it, rebuilt it,
and then filed R-009 against its own repair. **Stated before anything else: the
same mind found the fault, wrote the fix, and graded the fix.** PART 1 exists
because that is not certification, and you are the first pair of eyes that did
not build any of it.*

Read these files in `C:\Users\hp\Downloads\zargul trader\zar-x` before doing
anything:

1. `SHIP_LAWS.md` — all seven laws. Law 4 (gates before tests) especially.
2. `EXECUTION_PLAN.md` — the PHASE 3 block and the CURRENT POSITION MARKER.
3. The last THREE entries of `PROGRESS_LOG.md` — the audit that voided a 48/48,
   the Gate 3.2-R declaration (committed with **no `.py` file in it**), and the
   rebuild. **Read the rebuild as a CLAIM, not a result. It is what you are
   auditing.**
4. `cockpit/funding.py` — read every line, production path and `__main__` both.
5. `cockpit/fear_greed.py` — ~155 lines. **This is the one nobody has ever
   attacked.** Read it looking for the same shape as funding's hole.
6. `REVIEW_QUEUE.md` — **R-009 and R-008 are your PART 1 worklist.** R-001 may
   also be settled by you (you did not build the repair). **R-006 may NEVER be
   cleared by you or any in-house session.**

Then: `git pull` FIRST. This session has TWO parts and **PART 2 IS
CONDITIONAL.** If PART 1 finds a real problem, fix that and stop — Step 3.2b
does not happen in the same breath. **If tokens run short, do PART 1 properly
and leave PART 2 entirely.** A half-built recorder on the one dataset that
expires is worse than no recorder. Use `git commit -F <file>` for multi-line
messages; PowerShell here-strings mangle quotes.

Run env: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with `PYTHONUTF8=1`.
The Commander is a non-programmer — plain words, gray-box commands, explain
before you change, commit after.

---

# PART 1 — THE TWO REVIEWS (you are the outside eye; act like one)

**LOCK THE DEFINITION OF "PART 1 CLEARS" BEFORE YOU RUN ANYTHING** — write
these four bars into your working notes first so they cannot soften as you go:
(1) a SEVENTH sabotage, invented by you, is thrown at Gate 3.2-R and its result
recorded either way; (2) `cockpit/fear_greed.py` is put under the same knife and
its verdict recorded either way; (3) any weakness found in Fear & Greed is
REPAIRED under a gate declared before the code exists; (4) `lab/` byte-identical,
vault INTACT 6/6, the Brief still 3/3. **Four of four or it has not cleared, and
"three of four with a good explanation" is the phrasing this ship exists to
refuse.**

## 1.1 — EXHIBIT A: THE SEVENTH SABOTAGE (R-009)

`python cockpit\funding.py` breaks itself six ways every run and catches all
six. **That is the claim under review, not the verdict.** The six were chosen by
the session that had already found them, so the gate is strongest exactly where
it has already been attacked. **Your job is to attack where it has not.**

**Invent at least one NEW sabotage the previous session did not think of, and
report the result either way.** Candidates to get you started — **do not stop at
these, and do not treat the list as the assignment**:

    - break the "no data:" partial-failure path so a missing asset vanishes
      SILENTLY instead of being named
    - make `section_text` swallow a genuine error and return a stale or empty
      block that still looks well-formed
    - corrupt the wording itself — flip "positive = longs pay shorts" to its
      opposite while every NUMBER stays correct
    - break `MAX_PLAUSIBLE_RATE` so an absurd rate prints instead of degrading
    - make the offline path print a plausible-looking number instead of the
      offline line

**The wording sabotage is the one this session would bet on.** Every check
guards digits; the sentence beside the digits is what tells the pilot what the
digits MEAN, and a reversed meaning with correct numbers is exactly the failure
Gate 3.2's whole existence was justified by.

**EDGE CASE, DEFINED BEFORE YOU RUN: do the sabotage in a scratch copy OUTSIDE
the repo**, confirm `git status` is clean afterwards, and **run the control
(untouched) copy too** — if the control does not pass, your rig is broken and
nothing you conclude means anything.

**A clean verdict on R-009 looks like:** you invented a seventh, it was CAUGHT,
and you say what it was. **Failed looks like:** it escaped — in which case Gate
3.2-R is still shaped around its author's imagination, you say so plainly, and
the repair is extended to cover the class you found.

## 1.2 — THE FEAR & GREED KNIFE (R-008)

**`cockpit/fear_greed.py` has never been attacked, and it is built the same way
as the instrument that failed this morning:** a `_get`, a `_parse`, a formatter,
and a smoke test that checks the PARSE rather than the printed sentence. **This
session did not look. That omission is filed as R-008 and it is now yours.**

Run the same exercise. Scratch copy outside the repo, control first, then
break it on purpose. Candidates — again, find your own:

    - flip the value (print 100 - value, so Extreme Fear reads as Extreme Greed)
    - mismatch the number and its label (26 printed beside "Greed")
    - break `_age_words` so "a week ago" is attached to yesterday's reading
    - break the date so a stale reading prints as today's
    - break `_context_words` index selection so the comparison points are wrong

**EDGE CASE, DEFINED BEFORE CODING:** alternative.me serves ONE reading per day.
Unlike funding, **the value will NOT drift between two fetches within a run**,
so the before/after tolerance funding needed is unnecessary here — **do not copy
it in by reflex.** A tolerance that exists for no reason is a hole with a
comment on it. If you find the value CAN change mid-run, that is a measurement
that beats this paragraph and you write the correction down.

**IF THE SMOKE TEST CATCHES EVERYTHING YOU THROW: say so and clear R-008.**
"Reviewed, found nothing" is a real result. **Do not manufacture a defect to
justify the session.**

## 1.3 — IF FEAR & GREED IS WEAK: STEP 3.1-R, UNDER A GATE DECLARED FIRST

Only if 1.2 finds a real hole. **Copy the shape of Gate 3.2-R exactly — it is
committed and it works:**

**DECLARE GATE 3.1-R IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves
the bar preceded the work. This is the third time this pattern is used and it
has survived an audit each time.

**GATE 3.1-R — the bar, if you need it:**

(a) **NOTHING THE PILOT READS CHANGES.** All edits confined to the `__main__`
    block — **prove it with the diff hunk line numbers, do not assert it.**
    `python cockpit\brief.py` still 3/3, both instruments, ONE deck header.
(b) **THE PRINTED SENTENCE IS VERIFIED**, using the test's own arithmetic
    against a raw fetch. **The helper under test is never called to judge
    itself.** The value, its label, and the age words are each checked.
(c) **THE SABOTAGE DRILL IS PERMANENT** — every break you found in 1.2 is baked
    into the smoke test, caught on every run, originals restored and the
    restoration verified.
(d) Everything the old smoke test did, it still does — live section, offline
    drill degrading to two lines with the header intact, exit 0.
(e) **NO new file, NO new dependency, NO extra call from the Brief's path.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL and is not committed as a pass.**

## 1.4 — WRITE IT UP EITHER WAY, AND MIND WHAT YOU MAY NOT CLEAR

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the
actual output, and the verdict — **including if it is all clean.** A review that
only appears in the log when it finds something teaches the next session that
silence means safety.

**`REVIEW_QUEUE.md`: you MAY clear R-008 and R-009 (you did not build them), and
R-001 too if R-009 clears — the repair's independent review is exactly what
R-001 has been waiting for.** Items you cannot settle stay OPEN with a note on
what is missing; **leaving something open is a legitimate recorded outcome.**
**R-006 is not yours, ever. Never delete an item. Never edit a cleared verdict.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.** If you change a rule you
are about to be measured by, file it in bold. Filing costs one paragraph. Not
filing costs whatever the mistake costs, discovered later by someone who
trusted you.

---

# PART 2 — STEP 3.2b: THE OPEN-INTEREST RECORDER (only if Part 1 cleared, and only if you have room to do it properly)

Build ONLY Step 3.2b: **one new file, `data/open_interest.py`, and one new
directory, `data/oi_history/`.** No new instruments, no display. `cockpit/` is
NOT touched — this is a recorder, and the Whale Watch instrument that will read
it is Phase 3 #5 with its own step and its own gate. Do not smuggle it in.

**WHY THIS ONE IS DIFFERENT FROM EVERY OTHER SOURCE ON THE SHIP.** Every other
free source we use serves deep history on demand — measured, not assumed.
**Open interest does not: Binance serves a 30-day window and refuses anything
older.** Whatever falls out of that window is gone permanently and cannot be
bought back later at any price. There is no emergency — because every read
reaches back 30 days, a recorder that runs even monthly loses nothing — but
there is a real deadline measured in weeks.

**THE MEASURED FACTS, PROBED 2026-07-26, NONE ASSUMED. Verify them anyway — if
any has moved, the new measurement wins and you write the correction down.**

    /fapi/v1/openInterest?symbol=BTCUSDT     HTTP 200
      {"symbol","openInterest","time"}                      live snapshot
    /futures/data/openInterestHist?symbol=BTCUSDT&period=4h&limit=500
      HTTP 200, 180 rows, 2026-06-26 20:00 → 2026-07-26 16:00 (29.8 days)
      {"symbol","sumOpenInterest","sumOpenInterestValue",
       "CMCCirculatingSupply","timestamp"}
    startTime 60 days back → HTTP 400 {"code":-1130,"msg":"parameter
                                       'startTime' is invalid."}
    Rows per period at limit=500:  5m→500 rows/1.7d · 1h→500 rows/20.8d ·
                                   4h→180 rows/29.8d · 1d→30 rows/29.0d

**USE `period=4h`. It is the ONLY setting that captures the entire window in
one request per asset** — `1h` reaches back just 20.8 days at limit 500, so a
recorder using it would silently lose nine days it believed it had.

**THE TRAP, MEASURED, AND THE REASON CHECK (c) EXISTS. A bogus symbol returns
`HTTP 200` with an empty list `[]` — it does NOT error.** This is the opposite
of the funding endpoint, which returns a clean HTTP 400 `code -1121` for the
same mistake. **A recorder written the obvious way would read `[]`, append
nothing, print "0 new rows", exit 0 and report success — every month, while the
30-day window silently rolled past.** On the one dataset that cannot be
recovered. Nobody would find out until they went looking for history that no
longer existed. **An empty result is a LOUD FAILURE, never "no new data".**
Two smaller traps beside it, both measured: the field is `sumOpenInterest` in
the history endpoint but `openInterest` in the live snapshot endpoint — two
names for one idea, and assuming one from the other silently yields `None`; and
the payload carries an unplanned `CMCCirculatingSupply`, which you store
deliberately or not at all, never by accident.

**WHAT TO BUILD.** Append-only CSV per asset — `data/oi_history/BTCUSDT_4h.csv`
and the same for ETH and SOL — columns at minimum `timestamp` (UTC ISO),
`symbol`, `sumOpenInterest`, `sumOpenInterestValue`. The first run backfills
the full 30-day window. **Idempotent: running it twice must not duplicate a
single row** — de-duplicate on `(symbol, timestamp)`; this is the whole reason
it can run on any schedule. **It never rewrites history** — existing rows are
never modified, only new timestamps appended, and if a re-read disagrees with a
stored row that is a finding to report loudly, not a value to overwrite.
Injectable base URL (the `.invalid` trick) so the offline drill needs no
disconnection. **Fail-safe (Law 3): on failure it reports honestly and writes
NOTHING** — a truncated CSV is worse than no write. Its own standalone smoke
test in `__main__`, as every part on this ship has.

**EDGE CASE, DEFINED BEFORE CODING — do not discover this mid-build and
improvise:** the newest row Binance returns is for a period that may not have
closed yet. **Decide before you write the loop whether the current, possibly
incomplete period is stored or held back, state the decision in the output and
the log, and make it consistent between runs** — otherwise check (b),
idempotence, will fail intermittently and you will be tempted to blame the
network. Either choice is defensible; silently doing both is not.

## GATE 3.2b — DECLARED HERE, BEFORE THE BUILD (Law 4)

Run the **regression check FIRST, at the top, so we know nothing moved**:
`python cockpit\brief.py` prints 3/3 with BOTH Context Deck instruments before
you write a line. Then:

(a) **BACKFILL:** from empty, one run writes ≥ 175 rows per asset for all three
    assets spanning ≥ 29 days at `period=4h`. Print the real span.
(b) **IDEMPOTENCE:** run again immediately — row counts identical, zero
    duplicates. Prove it by counting distinct `(symbol, timestamp)` pairs
    against total rows; **the two numbers must be equal**, printed side by side.
(c) **THE EMPTY-RESULT TRAP:** point it at a bogus symbol. It must **FAIL
    LOUDLY** — non-zero exit or an explicit error line — and must NOT write an
    empty file, append nothing silently, or report success. **A session that
    cannot demonstrate this has not passed this gate.**
(d) **OFFLINE DRILL:** injected unreachable URL → honest offline line, no
    traceback, **and the CSVs are byte-identical afterwards** (checksum before
    and after, both printed).
(e) **HISTORY IS NEVER REWRITTEN:** hand-edit one stored value in a scratch
    copy, re-run, confirm the tool REPORTS the disagreement rather than
    silently overwriting it.
(f) **THE BRIEF IS UNAFFECTED:** `python cockpit\brief.py` still 3/3 with both
    instruments. 3.2b touches no cockpit file so this should be trivially true
    — verify it anyway, at the end as well as the start.
(g) **THE DATA IS PLAUSIBLE:** spot-check BTC open interest against Binance's
    own displayed figure. **A recorder that faithfully stores nonsense is not a
    working recorder.**
(h) **NEW, AND EARNED TODAY — THE SABOTAGE DRILL IS BUILT IN FROM BIRTH.** This
    recorder's smoke test breaks itself on purpose and requires each break to be
    CAUGHT, exactly as `cockpit/funding.py` now does. **At minimum: a de-dup
    key that silently drops rows, a column written into the wrong field, and a
    timestamp converted with the wrong timezone.** **A gate that has never been
    attacked is a gate that has never been tested, and this ship learned that at
    the cost of a voided 48/48 — no new part ships without it.**

**STANDING LAWS.** `lab/vault/` read-only and `lab/` byte-identical — nothing
in `lab/` is touched, at all. Do NOT modify `cockpit/funding.py`,
`cockpit/fear_greed.py` (except under Step 3.1-R above, and then only its
`__main__` block), `cockpit/brief.py`, `data/market_data.py`, `config.py` or
anything in `indicators/ regime/ risk/ signals/ journal/`. Nothing outside
`data/open_interest.py`, `data/oi_history/`, `PROGRESS_LOG.md`,
`EXECUTION_PLAN.md`, `ROADMAP.md`, `REVIEW_QUEUE.md` and this file. **The
risk-doctrine item (25% cap / ~0.49%) stays parked.** Do NOT start Step 3.3
(news headlines) even if everything passes quickly. INFORMATION, never a
signal — the signals doorway stands. One source, chosen once, never switched
mid-history.

## IF / THEN

| IF | THEN |
|---|---|
| Your seventh sabotage ESCAPES Gate 3.2-R | Say so plainly, extend the drill to cover that class, and **R-001 and R-009 both stay open.** This is a success of the process, not a failure of the session. |
| Fear & Greed catches everything you throw | **Clear R-008 and say "reviewed, found nothing".** Do not invent a defect to justify the session. |
| Binance answers HTTP 451 / restricted location | STOP. Do NOT swap exchanges. Write it up, tell the Commander — that swap is his call, never a session's. |
| The schema or the 30-day window differs from the measured facts above | **The new measurement wins.** Record the real shape, adapt, write the correction down. |
| A bogus symbol no longer returns `200 []` | Record it — and keep check (c) anyway. The recorder must refuse empty results however Binance signals them. |
| Backfill returns fewer than 175 rows | That is a FAILED bar, reported honestly — **not a number to tune until it passes.** |
| Any planning document contradicts a measurement you just took | The measurement wins and you write the correction down. **Fourth time this has been needed.** |
| A sabotage cannot be caught without changing production code | **STOP and report.** Changing the instrument to make a test pass is how a ship gets a gate that fits the code instead of code that fits the gate. |

**IF EVERYTHING PASSES:** write both halves into `PROGRESS_LOG.md` — the review
verdicts with the sabotages you invented and their actual output, then the build
with the gate tally, the real schema received, and every mistake as plainly as
every success (Law 1). **Update `REVIEW_QUEUE.md`: verdicts on R-008, R-009 and
(if earned) R-001, plus any new item this session could not certify itself.**
Update the marker, tick the recorder in `ROADMAP.md`, refresh the MEASURED facts
table. Commit, push. **Then raise the scheduling decision with the Commander and
do not silently skip it — a recorder that is never run collects nothing. It must
run on his LAPTOP, not the cloud watchman: GitHub's runners are US-hosted and
Binance geo-blocks US addresses, so a cloud recorder might collect nothing,
silently, for weeks. Present the one-line command and let him decide.**

**IF PART 1 FINDS A REAL PROBLEM, or Gate 3.2b fails twice, or anything here is
unclear to you — STOP and tell the Commander.** If something in these orders is
unclear to a session that has no memory of writing them, that is a defect in the
orders and you should say so rather than guess.

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
2. **The risk-doctrine decision** — the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never
   after seeing results.**
3. **`MAX_PLAUSIBLE_RATE`** — measured 2026-07-26 at 13–16× looser than
   Binance's published cap (real: BTC/ETH ±0.300%, SOL ±0.375% per 8h; the code
   refuses only beyond ±5%). Safe, but too loose to be a real fence.
   **Recommendation: tighten to ~0.01. NOT done — a session does not decide it
   by default.**
4. **The settled-rate anchor (R-004)** — returned to him on correct facts: the
   Step 3.2 orders explicitly permitted the extra call the previous session
   claimed they forbade. Printing it would put a number on the Brief the pilot
   can check with his own eyes.
5. **THREE law candidates, none adopted, all his call — no session promotes its
   own idea to law:**
   - *"A session may not certify its own work; anything it cannot certify is
     filed in `REVIEW_QUEUE.md` before the commit that ships it, and only an
     independent reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."* **Three earned examples.**
   - **NEWEST, earned 2026-07-26:** *"A check is not proven until it has been
     deliberately broken. Any gate guarding what the pilot reads ships with a
     sabotage exercise demonstrating it can FAIL."* **Four of six lies passed
     Gate 3.2 while it reported 48/48. Every check ran. Every check passed.
     Nobody had tried to break them.**
6. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.**
Information instruments can carry a lighter guard. The gauntlet cannot.
