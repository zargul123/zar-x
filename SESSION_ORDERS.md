# ZAR X — SESSION ORDERS: NEXT SESSION

*Written 2026-07-26 by Opus, again wearing Fable's hat, at the Commander's
instruction. **The independence weakness is now two sessions deep and is stated
at the top, not buried:** the same mind wrote the Step 3.2 orders, amended the
Step 3.2 gate, built Step 3.2, graded it 48/48, and is now writing both the
review of its own work and the next step's gate. A tally cannot fix that. Only
PART 1 below can.*

*Step 3.2's orders are not reproduced here — they are in git at `c301f54` and
`2a73645`. Seven laws get read; twelve get skimmed, and the same is true of
orders.*

---

# THIS SESSION HAS TWO PARTS, IN THIS ORDER, AND PART 2 IS CONDITIONAL

**PART 1 — Sit in Fable's chair. Audit Step 3.2 from raw evidence.**
**PART 2 — ONLY IF PART 1 CLEARS: build Step 3.2b, the open-interest recorder.**

If Part 1 finds a real problem, **Part 2 does not happen.** Write the finding
up, tell the Commander, stop. A session that reviews its predecessor and then
rushes into building has not reviewed anything — it has performed a review.

## READ FIRST, IN THIS ORDER

1. `SHIP_LAWS.md` — all seven laws.
2. `EXECUTION_PLAN.md` — the PHASE 3 block and the CURRENT POSITION MARKER.
3. The last THREE entries of `PROGRESS_LOG.md` — the false-premise correction,
   the unpassable-gate correction, and the Step 3.2 build entry.
4. `ROADMAP.md` — the MEASURED data-source facts table.
5. `cockpit/funding.py` and `cockpit/brief.py` — the code under audit.

## SESSION RULES (standing, restated so they cannot be missed)

1. `git pull` FIRST. The cloud watchman commits every 4 hours.
2. Run environment: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with
   `PYTHONUTF8=1`. The Commander is a non-programmer: plain words, gray-box
   commands, explain then commit (Law 5).
3. Use `git commit -F <file>` for multi-line messages. PowerShell here-strings
   mangle quotes when passed to git; two commits were lost to this last time.
4. One part, one gate, one commit. Do NOT start Step 3.3 (news headlines).
5. INFORMATION, never a signal. The signals doorway stands.

---

# PART 1 — THE INDEPENDENT REVIEW OF STEP 3.2 (do this first, cold)

This is the review that Fable used to perform, and it is the review that once
caught a reviewer's own hardcoded "15/15" in Gate 2.5. **Recompute from raw
evidence. Do not trust the printed tally in the log — that is precisely the
thing being audited.**

## 1.1 — SCOPE AND INTEGRITY

- `git diff 2a73645..c301f54 --stat`: ONLY `cockpit/funding.py` (new),
  `cockpit/brief.py`, `PROGRESS_LOG.md`, `EXECUTION_PLAN.md`, `ROADMAP.md`,
  `SESSION_ORDERS.md` may have changed. **All of `lab/` byte-identical.**
- `python lab\verify_vault.py` → VAULT INTACT, 6/6 checksums.
- Read every line of `cockpit/funding.py`. It is ~200 lines. Read them.

## 1.2 — RE-RUN EVERYTHING, FROM SCRATCH

- `python cockpit\funding.py` → all three assets with signs, settlement time,
  exact-identity check, partial-failure drill, offline drill, exit 0.
- `python cockpit\brief.py` → ONE "CONTEXT DECK" header carrying BOTH
  instruments, Fear & Greed above funding, 3/3 assets, every pre-existing
  section intact.
- Kill each instrument separately and both together. Brief stays 3/3 in all
  three cases, no traceback.

## 1.3 — RE-VERIFY THE SIGN AND MAGNITUDE YOURSELF

Fetch Binance raw, by hand, in your own code. Confirm the printed percentage
and **its sign** against `premiumIndex.lastFundingRate`. Confirm the settled
rate matches `/fapi/v1/fundingRate` digit for digit. Confirm from Binance's own
published documentation that **positive = longs pay shorts**, and that the
Brief's wording says that and not its opposite.

## 1.4 — **AUDIT THE AMENDMENT ITSELF. THIS IS THE POINT OF PART 1.**

The previous session **rewrote Gate 3.2's most important check and then
declared itself to have passed the rewritten version.** That is exactly the
move a dishonest session would make, and it must not be taken on trust
regardless of how good the reasoning looks. Test the claim that made the
rewrite legitimate:

1. **Was the original check really unpassable?** Call both endpoints. Is
   `premiumIndex.lastFundingRate` genuinely a different quantity from the
   newest settled `fundingRate`, or did the previous session misread it to
   justify an easier gate? Check `nextFundingTime` against the newest
   `fundingTime`.
2. **Was the sign-agreement fallback really invalid?** Pull the last ~20
   settled rates for ETH and SOL. Do the signs genuinely flip between
   consecutive periods? The previous session claimed `+ − +` and `− + +`.
3. **Is the replacement genuinely STRICTER, or is it theatre?** "Exact
   identity" is only stricter if the settled reader and the printed estimate
   truly share `_parse_rate` and `_fmt_pct`. **Read the code and confirm the
   sharing is real.** If a bug were introduced into `_fmt_pct`, would the
   exact-identity check actually catch it? Try it: break the helper on purpose
   in a scratch copy and confirm the smoke test FAILS. A check that cannot
   fail is not a check.
4. **Did the amendment land before the code?** `git show cbfcff4 --stat` must
   contain no `.py` files, and `git log` must show it strictly before
   `c301f54`.

**If any of these four does not hold, say so plainly and stop.** The finding
outranks the tally, the commit, and this document.

## 1.5 — HUNT FOR WHAT THE GATE DID NOT COVER

The Step 3.2 gate checked what it was told to check. Ask what it was not told
to check. Some candidates, not exhaustive — find your own:

- What happens at the settlement boundary, when `nextFundingTime` passes
  mid-run? Is the printed time ever stale or in the past?
- `min(settlements)` is used when assets disagree on settlement time. Is that
  right, or should disagreement be surfaced rather than silently minimised?
- The `MAX_PLAUSIBLE_RATE = 0.05` sanity bound: is it above Binance's real
  cap for these three contracts, or could an honest extreme reading be
  refused as implausible? **Measure Binance's actual funding cap.**
- Does a slow-but-alive Binance (partial timeout) degrade as honestly as a
  dead one?

## 1.6 — WRITE THE REVIEW UP

A `PROGRESS_LOG.md` entry either way, **including if everything is clean.**
Record what was recomputed, the numbers you got yourself, and the verdict.
"Reviewed, found nothing" is a result worth recording; a review that only
appears in the log when it finds something teaches the next session that
silence means safety.

---

# PART 2 — STEP 3.2b: THE OPEN-INTEREST RECORDER

*Only if Part 1 cleared. This is the one dataset on this ship that expires.*

## WHY THIS EXISTS

Every other free source we use serves deep history on demand. **Open interest
does not: Binance serves a 30-day window and refuses anything older.** Phase 3
instrument #5 (Whale Watch) names funding + open interest as its honest free
footprint, and Phase 6 may want it. Whatever falls out of the window is gone
permanently — it cannot be bought back later at any price.

**But there is no emergency, only a deadline.** Because every read reaches back
30 days, a recorder that runs even monthly loses nothing.

## MEASURED FACTS — ALL PROBED 2026-07-26, NONE ASSUMED

*The Step 3.2 lesson was that gates get written from assumption too. So every
claim below was called before this gate was written. Verify them anyway.*

    /fapi/v1/openInterest?symbol=BTCUSDT              HTTP 200
      {"symbol","openInterest","time"}          ← live snapshot, one number

    /futures/data/openInterestHist?symbol=BTCUSDT&period=4h&limit=500
      HTTP 200, 180 rows, 2026-06-26 20:00 → 2026-07-26 16:00 (29.8 days)
      {"symbol","sumOpenInterest","sumOpenInterestValue",
       "CMCCirculatingSupply","timestamp"}

    startTime 60 days back  → HTTP 400 {"code":-1130,
                                        "msg":"parameter 'startTime' is invalid."}
    startTime 20 days back  → HTTP 200, 120 rows (inside the window, fine)

    Rows per period at limit=500:
      period=5m  500 rows   1.7 days
      period=1h  500 rows  20.8 days   ← does NOT cover the window
      period=4h  180 rows  29.8 days   ← BEST: the whole window in ONE call
      period=1d   30 rows  29.0 days

**USE period=4h.** It is the only setting that captures the entire 30-day
window in a single request per asset.

### THREE TRAPS, MEASURED — THE GATE EXISTS FOR THESE

1. **A BOGUS SYMBOL RETURNS `HTTP 200` AND AN EMPTY LIST `[]`, NOT AN ERROR.**
   This is the opposite of the funding endpoint, which returns HTTP 400
   `code -1121` for a bad symbol. **A recorder written the obvious way would
   read `[]`, append nothing, print "0 new rows", exit 0, and report success
   every month while the window silently rolled past.** By the time anyone
   noticed, the data would be gone forever. **An empty result MUST be treated
   as a LOUD FAILURE, never as "no new data".**
2. **The field is named `sumOpenInterest` in the history endpoint but
   `openInterest` in the live snapshot endpoint.** Two names, two endpoints,
   same idea. Do not assume one from the other.
3. **`CMCCirculatingSupply` is in the payload** and was in nobody's plan.
   Record it in the log. Decide deliberately whether to store it; do not
   store it by accident.

## WHAT TO BUILD

**One new file: `data/open_interest.py`. One new data directory:
`data/oi_history/`.** Those are the only paths this session may create.
**`cockpit/` is NOT touched** — 3.2b is a recorder, not a display. The Whale
Watch instrument that reads this is Phase 3 #5 and has its own step.
`lab/` stays byte-for-byte untouched and the vault stays read-only.

- **Append-only CSV per asset**, `data/oi_history/BTCUSDT_4h.csv` and the same
  for ETH and SOL. Columns at minimum: `timestamp` (UTC ISO), `symbol`,
  `sumOpenInterest`, `sumOpenInterestValue`.
- **Backfill at birth:** the first run writes the full 30-day window.
- **Idempotent:** running it twice must NOT duplicate rows. De-duplicate on
  `(symbol, timestamp)`. This is the whole reason it can run on any schedule.
- **Never rewrites history.** An existing row is never modified, only new
  timestamps appended. If a re-read disagrees with a stored row, that is a
  finding to report loudly, not a value to overwrite.
- **Injectable base URL** (the `.invalid` trick) so the offline drill needs no
  disconnection. **Fail-safe (Law 3): on failure it reports honestly and
  writes NOTHING** — a truncated or partial CSV is worse than no write.
- **Standalone smoke test in `__main__`**, as every part on this ship has.

## GATE 3.2b — DECLARED HERE, BEFORE THE BUILD (Law 4)

(a) **BACKFILL:** from empty, one run writes ≥ 175 rows per asset for all
    three assets, spanning ≥ 29 days, `period=4h`. Report the real span.
(b) **IDEMPOTENCE — the check that lets it run on any schedule.** Run it a
    second time immediately. Row counts must be **identical**, no duplicates.
    Prove it by counting distinct `(symbol, timestamp)` pairs against total
    rows: the two numbers must be equal.
(c) **THE EMPTY-RESULT TRAP.** Point it at a bogus symbol. It must **FAIL
    LOUDLY** — non-zero exit or an explicit error line — and must **NOT**
    write an empty file, append nothing silently, or report success. **A
    session that cannot demonstrate this has not passed this gate**, because
    this is the exact failure that would lose the data without anyone noticing.
(d) **OFFLINE DRILL:** injected unreachable URL → honest offline line, no
    traceback, **and the CSVs on disk are byte-identical afterwards**
    (checksum before and after).
(e) **HISTORY IS NEVER REWRITTEN:** hand-edit one stored value in a scratch
    copy, re-run, and confirm the tool reports the disagreement rather than
    silently overwriting it.
(f) **THE BRIEF IS UNAFFECTED:** `python cockpit\brief.py` still prints 3/3
    with both Context Deck instruments. 3.2b touches no cockpit file, so this
    should be trivially true — verify it anyway.
(g) **THE DATA IS PLAUSIBLE:** spot-check that BTC open interest is in a sane
    range against Binance's own displayed figure. A recorder that faithfully
    stores nonsense is not a working recorder.

## IF / THEN

| IF | THEN |
|---|---|
| Binance answers HTTP 451 / restricted location | STOP. Do NOT swap exchanges. Write it up, tell the Commander. **One source, chosen once, never switched mid-history.** |
| The 30-day window has moved or the schema differs from the measured facts above | **The new measurement wins.** Record the real shape, adapt, write the correction down. |
| A bogus symbol no longer returns `200 []` | Record it. Keep check (c) anyway — the recorder must refuse empty results regardless of how Binance signals them. |
| The gate fails | Do not commit. Fix, or write it up and stop. **A failing gate is never "mostly passed".** |
| Any planning document contradicts a measurement you just took | The measurement wins, and you write the correction down. **Twice now.** |

## IF EVERYTHING PASSES

1. `PROGRESS_LOG.md`: the review verdict (Part 1) AND the build (Part 2) —
   what was built, the gate tally with real numbers, the real schema received,
   and every mistake as plainly as every success (Law 1).
2. `EXECUTION_PLAN.md` marker → "Step 3.2b DONE <date>, GATE 3.2b PASSED."
3. `ROADMAP.md`: tick the recorder; update the MEASURED facts table.
4. Commit with full notes (`git commit -F`), push.
5. **RAISE THE SCHEDULING DECISION WITH THE COMMANDER — do not silently skip
   it.** A recorder that is never run collects nothing. Because each read
   reaches back 30 days, running it monthly suffices; folding it into the
   existing daily batch is simplest. **It must run on the Commander's laptop,
   NOT the cloud watchman** — GitHub's runners are US-hosted and Binance
   geo-blocks US addresses, so a cloud recorder might collect nothing,
   silently, for weeks. Changing his Task Scheduler is his call: present the
   one-line command and let him decide.

---

# STILL ON THE COMMANDER'S DESK (do not let these drop)

1. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
2. **The risk-doctrine decision**: the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Must be settled BEFORE Phase 6,
   never after seeing results.**
3. **The Law 8 candidate** — *"a claim about what a data source will or will
   not give us is not a fact until it has been called; planning documents must
   mark which claims are measured and which are assumed."* **It now has TWO
   earned examples in two sessions**, the second being a false claim inside a
   gate's own most important check. Adopt, reject, or reshape — his call, and
   no session promotes its own idea to law.
4. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

# AND THE ONE THAT DOES NOT EXPIRE

**At Phase 6 the "separation in time" substitute EXPIRES.** A second,
genuinely independent AI must review the gauntlet's test setup before and its
verdict after. That is a locked requirement of EXECUTION_PLAN Phase 6 and is
**NOT waived by Fable's absence.** Information instruments can carry a lighter
guard. The gauntlet cannot.
