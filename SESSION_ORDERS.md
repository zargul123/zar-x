# ZAR X PHASE 3 — THE AUDIT, THEN STEP 3.2b (the reviewer must be able to fail the builder; the recorder must be unable to lose data quietly)

*Written 2026-07-26 by Opus wearing Fable's hat, at the Commander's
instruction. **Stated before anything else: the same mind wrote the Step 3.2
orders, amended the Step 3.2 gate mid-flight, built Step 3.2, graded it 48/48,
and wrote these orders including the audit of its own work.** That is two
sessions deep now. A tally cannot repair it. PART 1 is the only thing that can,
and only if you run it as a real audit rather than a formality.*

Read these files in `C:\Users\hp\Downloads\zargul trader\zar-x` before doing
anything:

1. `SHIP_LAWS.md` — all seven laws, Law 4 (gates before tests) especially.
2. `EXECUTION_PLAN.md` — the PHASE 3 block and the CURRENT POSITION MARKER
   (which records what Step 3.2 did to its own gate — read that part twice).
3. The last THREE entries of `PROGRESS_LOG.md` — the false-premise correction,
   the unpassable-gate correction, and the Step 3.2 build entry with its 48/48
   tally. **That tally is the thing you are auditing. Do not read it as a
   result; read it as a claim.**
4. `cockpit/funding.py` and `cockpit/brief.py` — the code under audit, ~200
   lines. Read every line of both.
5. `ROADMAP.md` — the MEASURED data-source facts table.

Then: `git pull` FIRST. This session has TWO parts and **PART 2 IS
CONDITIONAL.** If PART 1 finds a real problem, PART 2 does not happen — write
it up, tell the Commander, stop. A session that reviews its predecessor and
then hurries into building has not reviewed anything, it has performed a
review. Use `git commit -F <file>` for multi-line messages; PowerShell
here-strings mangle quotes and cost the last session two commits.

---

# PART 1 — THE AUDIT (Fable's chair; recompute everything, trust nothing)

**LOCK THE DEFINITION OF "THE AUDIT CLEARS" BEFORE YOU RUN ANYTHING** — write
these five bars into your working notes first so they cannot soften as you go:
(1) diff scope is clean and `lab/` is byte-identical and the vault verifies
INTACT; (2) both programs re-run live and behave as the log claims; (3) the
printed funding sign and magnitude re-derived independently by you agree with
Binance; (4) all four claims that justified the mid-flight gate amendment hold
under test; (5) the exact-identity check demonstrably CAN fail. Anything less
than five of five is NOT a clear, and "four of five with a good explanation" is
the phrasing this ship exists to refuse.

**1.1 SCOPE AND INTEGRITY.** `git diff 2a73645..c301f54 --stat` must show only
`cockpit/funding.py` (new), `cockpit/brief.py`, and the four planning
documents. All of `lab/` byte-identical. Run `python lab\verify_vault.py` →
VAULT INTACT 6/6. Confirm `git show cbfcff4 --stat` contains **no `.py` files
at all** and that `git log` places it strictly before `c301f54` — the previous
session's central defence is that it amended the gate before writing code, and
that claim is checkable in one command.

**1.2 RE-RUN EVERYTHING COLD.** `python cockpit\funding.py` → three assets each
with an explicit sign, settlement time as HH:MM UTC, exact-identity check,
partial-failure drill, offline drill, exit 0. `python cockpit\brief.py` → ONE
"CONTEXT DECK" header carrying BOTH instruments, Fear & Greed above funding,
3/3 assets, every pre-existing section intact. Then kill each instrument
separately and both together (inject the `.invalid` URL) — the Brief stays 3/3
in all three cases with no traceback. **EDGE CASE, DEFINED BEFORE YOU RUN: the
funding numbers WILL differ from the ones in the log, and may differ between
your own two runs.** Funding is quoted continuously. That is live data being
live, not evidence of tampering. What must NOT differ is the sign, the shape of
the output, or the 3/3.

**1.3 RE-VERIFY THE SIGN YOURSELF, IN YOUR OWN CODE.** Fetch Binance raw. Do
not import the instrument to check the instrument. Confirm the printed
percentage and its sign against `premiumIndex.lastFundingRate`; confirm the
settled rate matches `/fapi/v1/fundingRate` digit for digit; confirm from
Binance's own published documentation that **positive = longs pay shorts** and
that the Brief's wording says that and not its opposite. A backwards sign here
would print the exact opposite of the truth every morning and no "a number
appeared" check would ever catch it.

**1.4 AUDIT THE AMENDMENT ITSELF — THIS IS THE POINT OF PART 1.** The previous
session rewrote Gate 3.2's most important check and then declared itself to
have passed the rewritten version. **That is precisely the move a dishonest
session would make, and the quality of its reasoning is not evidence.** Test
the four claims that made the rewrite legitimate, in code, yourself:
(a) is `premiumIndex.lastFundingRate` genuinely a different quantity from the
newest settled `fundingRate` — compare `nextFundingTime` against the newest
`fundingTime` — or was it misread to justify an easier gate? (b) pull the last
~20 settled rates for ETH and SOL: do the signs genuinely flip between
consecutive periods, as claimed (`+ − +` and `− + +`), making the
sign-agreement fallback truly invalid? (c) read the code and confirm the
settled reader and the printed estimate REALLY share `_parse_rate` and
`_fmt_pct` — the entire claim that the new check is "stricter" rests on that
sharing being real rather than asserted; (d) the ordering check from 1.1.

**EXHIBIT A — THE SABOTAGE TEST (the reviewer must be able to fail the
builder).** A check that cannot fail is not a check, and the previous session
never proved its own could. **In a scratch copy outside the repo**, break
`_fmt_pct` on purpose — flip the sign, or drop the ×100 — and run the smoke
test. **It MUST FAIL.** Then break `_parse_rate` and run it again; it must fail
again. If either sabotage passes the gate, the 48/48 tally is worthless and
Step 3.2 reopens regardless of how good everything else looks. Report both
results with the actual output. **Do the sabotage in the scratchpad, never in
the repo, and confirm `git status` is clean afterwards.**

**1.5 HUNT WHAT THE GATE WAS NEVER TOLD TO CHECK.** The Step 3.2 gate checked
what it was told to. Ask what it was not. Candidates, not exhaustive — find
your own and record them: does the printed settlement time ever go stale or
sit in the past when a settlement passes mid-run? `min(settlements)` is used
when assets disagree on settlement time — is silently taking the earliest right,
or should disagreement be surfaced? **`MAX_PLAUSIBLE_RATE = 0.05` is an
ADMITTED GUESS** — the previous session never measured Binance's real funding
cap for these three contracts, so an honest extreme reading might be refused as
implausible and print as offline. **Measure the real cap and report it.** Does a
slow-but-alive Binance degrade as honestly as a dead one?

**1.6 WRITE THE REVIEW UP EITHER WAY — INCLUDING IF IT IS ALL CLEAN.** A
`PROGRESS_LOG.md` entry recording what you recomputed, the numbers YOU got, the
sabotage results, and the verdict. "Reviewed, found nothing" is a result worth
recording. A review that only appears in the log when it finds something
teaches the next session that silence means safety.

---

# PART 2 — STEP 3.2b: THE OPEN-INTEREST RECORDER (only if the audit cleared)

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

**THE MEASURED FACTS, PROBED 2026-07-26, NONE ASSUMED.** Step 3.2's lesson was
that gates get written from assumption too, so every claim here was called
before this gate was written. **Verify them anyway — if any has moved, the new
measurement wins and you write the correction down.**

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

**STANDING LAWS.** `lab/vault/` read-only and `lab/` byte-identical — nothing
in `lab/` is touched, at all. Do NOT modify `cockpit/funding.py`,
`cockpit/fear_greed.py`, `cockpit/brief.py`, `data/market_data.py`, `config.py`
or anything in `indicators/ regime/ risk/ signals/ journal/`. Nothing outside
`data/open_interest.py`, `data/oi_history/`, `PROGRESS_LOG.md`,
`EXECUTION_PLAN.md`, `ROADMAP.md` and this file. **The risk-doctrine item (25%
cap / ~0.49%) stays parked.** Do NOT start Step 3.3 (news headlines) even if
everything passes quickly. INFORMATION, never a signal — the signals doorway
stands. One source, chosen once, never switched mid-history.

## IF / THEN

| IF | THEN |
|---|---|
| Binance answers HTTP 451 / restricted location | STOP. Do NOT swap exchanges. Write it up, tell the Commander — that swap is his call, never a session's. |
| The schema or the 30-day window differs from the measured facts above | **The new measurement wins.** Record the real shape, adapt, write the correction down. |
| A bogus symbol no longer returns `200 []` | Record it — and keep check (c) anyway. The recorder must refuse empty results however Binance signals them. |
| Backfill returns fewer than 175 rows | That is a FAILED bar, reported honestly — **not a number to tune until it passes.** |
| Any planning document contradicts a measurement you just took | The measurement wins and you write the correction down. **Third time this has been needed.** |

**IF EVERYTHING PASSES:** write both halves into `PROGRESS_LOG.md` — the audit
verdict with the numbers you recomputed and the sabotage results, then the
build with the gate tally, the real schema received, and every mistake as
plainly as every success (Law 1). Update the marker to "Step 3.2b DONE <date>,
GATE 3.2b PASSED — Step 3.3 (news headlines, CryptoPanic free tier) READY".
Tick the recorder in `ROADMAP.md` and refresh the MEASURED facts table. Commit,
push. **Then raise the scheduling decision with the Commander and do not
silently skip it — a recorder that is never run collects nothing. It must run
on his LAPTOP, not the cloud watchman: GitHub's runners are US-hosted and
Binance geo-blocks US addresses, so a cloud recorder might collect nothing,
silently, for weeks. Present the one-line command and let him decide.**

**IF PART 1 FINDS A REAL PROBLEM, or Gate 3.2b fails twice, or anything here is
unclear to you — STOP and tell the Commander.** If something in these orders is
unclear to a session that has no memory of writing them, that is a defect in
the orders and you should say so rather than guess.

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
2. **The risk-doctrine decision** — the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never
   after seeing results.**
3. **The Law 8 candidate** — *"a claim about what a data source will or will
   not give us is not a fact until it has been called; planning documents must
   mark which claims are measured and which are assumed."* **Two earned
   examples in two sessions**, the second a false claim inside a gate's own
   most important check. Adopt, reject or reshape — his call. No session
   promotes its own idea to law.
4. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
EXECUTION_PLAN Phase 6 and is **NOT waived by Fable's absence.** Information
instruments can carry a lighter guard. The gauntlet cannot.
