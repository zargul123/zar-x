# ZAR X PHASE 3 — TWO TWELFTH SABOTAGES, THEN STEP 3.2b (a gate is strongest where it has already been attacked; your whole job is to attack where it has not)

*Written 2026-07-27 by the session that threw ten new sabotages at both Context
Deck gates, watched SEVEN walk through, repaired both, and then filed R-011
against its own repair. **Stated before anything else: one mind found the fault,
wrote the fix, and graded the fix.** Twenty-two sabotages now live in the two
instruments and **all twenty-two were invented by the sessions that then
defended against them.** PART 1 exists because that is not certification, and
you are the first pair of eyes that built none of it.*

**WHAT HAPPENED THE DAY BEFORE YOU, IN FIVE LINES.** On 2026-07-26 Gate 3.2
reported 48/48 while four deliberate lies walked through it; it was voided and
rebuilt, and the same knife then found five more in `cockpit/fear_greed.py`.
Both were rebuilt and both passed. **On 2026-07-27 a third session failed BOTH
rebuilds: seven of ten new sabotages escaped.** One printed
`positive = shorts pay longs` — **the exact opposite of how the market works** —
beside three perfectly correct numbers, and the gate said PASSED. Another
printed `>> strong buy signal` on the deck of a ship whose first rule is
INFORMATION, NEVER A SIGNAL. **The cause both times: every check asked whether
an expected string was PRESENT; none asked whether anything ELSE was present,
and none checked the fixed words at all.**

**THE PATTERN SO FAR, AND WHY YOUR JOB IS WHAT IT IS: three sessions in a row
have each found real holes in the work of the session before, and every one of
those holes was found by a session ORDERED TO TRY TO BREAK THE CODE — never by
one being careful.** Two generations of repair have each been failed by the next
pair of eyes. **You are generation three's reviewer.**

Read these files in `C:\Users\hp\Downloads\zargul trader\zar-x` before doing
anything:

0a. **`THE_PATTERN.md` — how a session runs, in plain words.** The three layers
   (the gate declared first · the sabotage drill that lives in the code forever
   · the independent attack), the two-job rhythm, and the housekeeping that has
   already bitten this ship. **Not a law; if it and `SHIP_LAWS.md` disagree, the
   laws win.** Read it first if you have never worked on this ship.
0. **`README.md` — it carries THE PROMISE**, which Law 6 points at by name:
   three sealed gauntlet slots and then the signals chapter closes. It is 1.7 KB.
   **A session that has not read it does not know the rule the whole ship is
   built around.**
1. `SHIP_LAWS.md` — all seven laws. Law 4 (gates before tests) especially.
2. `EXECUTION_PLAN.md` — the PHASE 3 block and the CURRENT POSITION MARKER.
   **This is the map: what is built, what is next, what each phase's gate is.**
3. The last THREE entries of `PROGRESS_LOG.md` — the Gate 3.1-R rebuild, the
   2026-07-27 review that failed it, and the Gate 3.2-R2 / 3.1-R2 repair.
   **Read the repair as a CLAIM, not a result. It is what you are auditing.**
4. `cockpit/funding.py` — every line, production path and `__main__` both.
5. `cockpit/fear_greed.py` — production path and `__main__` both.
6. `ROADMAP.md` — what exists and works, and the **MEASURED data-source facts
   table**. Part 2 depends on it. If anything you measure disagrees with it,
   **your measurement wins and you write the correction down.**
7. `REVIEW_QUEUE.md` — **R-011 is your PART 1 worklist.** R-001, R-008, R-009
   and R-010 may also be settled by you, since you built none of it.
   **R-006 may NEVER be cleared by you or any in-house session.**

**A NOTE ON `PROGRESS_LOG.md`: it is ~200 KB and reading all of it will eat the
budget you need for the actual work.** The last three entries are the assignment
and are enough. `EXECUTION_PLAN.md` and `ROADMAP.md` exist precisely so nobody
has to read the whole log — **if you find yourself needing older entries to
understand the current position, that is a defect in those two files and you
should say so and fix it.**

Then: **`git pull` FIRST** — a scheduled task pushes snapshots from elsewhere.
This session has TWO parts and **PART 2 IS CONDITIONAL.** If PART 1 finds a real
problem, fix that and stop — Step 3.2b does not happen in the same breath. **If
tokens run short, do PART 1 properly and leave PART 2 entirely.** A half-built
recorder on the one dataset that expires is worse than no recorder. Use
`git commit -F <file>` for multi-line messages; PowerShell here-strings mangle
quotes.

**NEVER use PowerShell `Get-Content` / `Add-Content` / `Set-Content` on this
repo's UTF-8 files.** PowerShell 5.1 reads BOM-less UTF-8 as ANSI and silently
eats every em-dash, mid-dot, arrow and tick mark. It corrupted four commits on
2026-07-26. Use Python (`open(p, encoding='utf-8')`) or the editor tools.

Run env: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with `PYTHONUTF8=1`.
The Commander is a non-programmer — plain words, gray-box commands, explain
before you change, commit after.

---

# PART 1 — THE TWO REVIEWS (you are the outside eye; act like one)

**LOCK THE DEFINITION OF "PART 1 CLEARS" BEFORE YOU RUN ANYTHING** — write these
four bars into your working notes first so they cannot soften as you go:
(1) a TWELFTH sabotage, invented by you, is thrown at Gate 3.2-R2 (funding) and
its result recorded either way; (2) the same against Gate 3.1-R2 (Fear & Greed);
(3) any leak found is REPAIRED under a gate declared before the code exists;
(4) `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3. **Four of four
or it has not cleared, and "three of four with a good explanation" is the
phrasing this ship exists to refuse.**

**AND ONE PRACTICE WORTH COPYING, EARNED 2026-07-27: write your prediction for
each sabotage BEFORE you run it.** That session predicted ten of ten correctly,
which is what showed the holes were structural rather than lucky — and it makes
it impossible to reinterpret a result after seeing it.

## 1.1 — THE TWELFTH SABOTAGE ON FUNDING (R-011)

`python cockpit\funding.py` breaks itself eleven ways every run and catches all
eleven. **That is the claim under review, not the verdict.**

**What the gate now does** — read it as a list of things it has ALREADY been
attacked on, which is exactly where it is strongest and where you should NOT
spend your time:

- rebuilds the WHOLE printed block from a raw Binance fetch, using its own
  arithmetic, and requires **exact equality** — so nothing can be appended
- holds its **own verbatim copy** of `positive = longs pay shorts` and the
  `— crowd positioning, information, not a signal` line, checked by name
- **rotates** the partial-failure drill: each asset in turn is the bogus one and
  must be named by its own name
- keeps the before/after drift allowance (rates move continuously), the exact
  identity check on settled rates, and the offline drill

**Ideas to get you started — do not stop at these, and do not treat the list as
the assignment:**

    - the drift allowance: the block is accepted if it matches the BEFORE or
      the AFTER snapshot. Can a lie be made to live in that gap?
    - the offline path: make it print something plausible instead of the
      offline line, without touching section_text's happy path
    - MAX_PLAUSIBLE_RATE: still 0.05, still 13-16x looser than Binance's real
      cap. Does anything notice if it is removed entirely?
    - the exact-identity check in section 4: it calls read_settled AND fetches
      raw. Is the comparison real, or does something shared make it agree
      with itself?
    - the gate's own copy of the wording: what happens if someone edits the
      PRODUCTION sentence and the GATE'S COPY to match, in one commit? Nothing
      on this ship would notice. Is that a defect or accepted? Say which.

## 1.2 — THE TWELFTH SABOTAGE ON FEAR & GREED (R-011)

Identical exercise, one instrument over. `python cockpit\fear_greed.py` breaks
itself eleven ways and catches all eleven. **Same author, same blind spot, same
review.** The gate now also holds its own `GATE_LIMIT` and compares the module's
`HISTORY_LIMIT` against it — because reading that constant from the module had
silently disarmed one of its own detectors.

**Ideas — again, find your own:**

    - the UTC day-rollover allowance: the raw is re-fetched ONCE on mismatch
      and only a genuinely CHANGED date excuses it. Can that door be widened?
    - `_parse`'s 0-100 range guard, and the `metadata.error` field: neither is
      reachable from a live fetch. Are they ever actually exercised?
    - the offline drill judges "two lines, header first". What passes that bar
      while still being a lie?
    - the context points are taken from indexes 1 and 7. What if the source
      serves a gap, or duplicates a day?

## 1.3 — THE THREE DOUBTS THE 2026-07-27 SESSION COULD NOT SETTLE ABOUT ITS OWN REPAIR

Handed to you as starting points, **NOT as the assignment** — the whole point is
that its author cannot see past them:

1. **THE GATE NOW CONTAINS A COPY OF THE EXACT WORDS THE BRIEF PRINTS.** The next
   time anyone legitimately improves that wording, the gate FAILS — and the
   obvious move is to edit the gate to match. **That is how a gate gets fitted to
   the code instead of the code to the gate, which is what R-001 was convicted
   of.** Nothing enforces that such an edit is deliberate and recorded.
2. **THE PERMANENT SABOTAGES CORRUPT OUTPUT, NOT THE FILE.** S7-S11 and F7-F11
   wrap `section_text` and rewrite what it returns. That proves the checks can
   say no to a corrupted SENTENCE. **It does not prove they would say no to
   every corrupted CODE PATH that could produce one.** The scratch rig that
   edited the real files ran once, on 2026-07-27, and is not part of the gate.
3. **NOTHING CHECKS THAT A GATE'S OWN DESCRIPTION MATCHES WHAT IT DOES.** That
   session's first working version announced "six ways" while running eleven.
   Caught by reading, not by a check.

## 1.4 — THE RIG (defined before you run, because a broken rig proves nothing)

**Do the sabotage in a scratch copy OUTSIDE the repo.** Confirm `git status` is
clean afterwards. **Run the untouched control too** — if the control does not
pass, your rig is broken and nothing you conclude means anything.

**AND CHECK YOUR OWN HARNESS: a sabotage that CRASHES is scored as "caught".**
So a sabotage that never really ran is recorded as a pass. **Print the block
your sabotage produces and confirm it is visibly wrong before you trust the
verdict.** This ship has had two near-misses of exactly that shape.

**If your text-replacement anchor matches more than once, REFUSE TO RUN rather
than editing the first match.** The gates now hold their own copies of the
production wording, so several obvious anchors appear twice.

## 1.5 — IF EITHER GATE LEAKS: REPAIR UNDER A GATE DECLARED FIRST

Only if 1.1 or 1.2 finds a real hole. **The pattern is committed five times over
and has survived audit each time — copy it exactly:**

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves
the bar preceded the work. Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits confined to the `__main__`
    block — **prove it two ways, do not assert it:** every diff hunk at or after
    the `__main__` line (`funding.py` line 160, `fear_greed.py` line 113), AND a
    sha256 of the production half before and after, printed side by side.
    `python cockpit\brief.py` still 3/3, both instruments, ONE deck header.
(b) **THE PRINTED BLOCK IS VERIFIED** using the test's own arithmetic against a
    raw fetch. **The helper under test is never called to judge itself.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the eleven,
    caught on every run, originals restored and the restoration verified.
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT. **That is the evidence; the
    in-run drill is not.**
(e) Everything the old gates did, they still do.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL and is not committed as a pass.**

## 1.6 — WRITE IT UP EITHER WAY, AND MIND WHAT YOU MAY NOT CLEAR

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the
actual output, and the verdict — **including if it is all clean.** A review that
only appears in the log when it finds something teaches the next session that
silence means safety.

**`REVIEW_QUEUE.md`: you MAY clear R-011 (you built none of it), and R-001,
R-008, R-009 and R-010 too if those clear — R-001 has now been waiting through
two failed generations of repair and moves only when a generation survives an
independent attack.** Items you cannot settle stay OPEN with a note on what is
missing; **leaving something open is a legitimate recorded outcome.**
**R-006 is not yours, ever. Never delete an item. Never edit a cleared verdict.**

**IF BOTH GATES CATCH EVERYTHING YOU THROW: say so, and clear R-011.**
"Reviewed, found nothing" is a real result. **DO NOT MANUFACTURE A DEFECT TO
JUSTIFY THE SESSION.** The pressure after three sessions that each found
something big is to also find something. **A clean review is a legitimate
outcome and this ship needs to see one eventually.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.** If you change a rule you
are about to be measured by, file it in bold.

---

# PART 2 — STEP 3.2b: THE OPEN-INTEREST RECORDER (only if Part 1 cleared, and only if you have room to do it properly)

**This step has now been deferred TWICE — on 2026-07-26 and again on
2026-07-27 — both times because Part 1 found a real problem, which is correct.
The 30-day window keeps expiring. It is still not an emergency (see below), but
it is no longer theoretical.**

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

**USE `period=4h`. It is the ONLY setting that captures the entire window in one
request per asset** — `1h` reaches back just 20.8 days at limit 500, so a
recorder using it would silently lose nine days it believed it had.

**THE TRAP, MEASURED, AND THE REASON CHECK (c) EXISTS. A bogus symbol returns
`HTTP 200` with an empty list `[]` — it does NOT error.** This is the opposite
of the funding endpoint, which returns a clean HTTP 400 `code -1121` for the
same mistake. **A recorder written the obvious way would read `[]`, append
nothing, print "0 new rows", exit 0 and report success — every month, while the
30-day window silently rolled past.** On the one dataset that cannot be
recovered. **An empty result is a LOUD FAILURE, never "no new data".**
Two smaller traps beside it, both measured: the field is `sumOpenInterest` in
the history endpoint but `openInterest` in the live snapshot endpoint — two
names for one idea, and assuming one from the other silently yields `None`; and
the payload carries an unplanned `CMCCirculatingSupply`, which you store
deliberately or not at all, never by accident.

**WHAT TO BUILD.** Append-only CSV per asset — `data/oi_history/BTCUSDT_4h.csv`
and the same for ETH and SOL — columns at minimum `timestamp` (UTC ISO),
`symbol`, `sumOpenInterest`, `sumOpenInterestValue`. The first run backfills the
full 30-day window. **Idempotent: running it twice must not duplicate a single
row** — de-duplicate on `(symbol, timestamp)`; this is the whole reason it can
run on any schedule. **It never rewrites history** — existing rows are never
modified, only new timestamps appended, and if a re-read disagrees with a stored
row that is a finding to report loudly, not a value to overwrite. Injectable base
URL (the `.invalid` trick) so the offline drill needs no disconnection.
**Fail-safe (Law 3): on failure it reports honestly and writes NOTHING** — a
truncated CSV is worse than no write. Its own standalone smoke test in
`__main__`, as every part on this ship has.

**EDGE CASE, DEFINED BEFORE CODING — do not discover this mid-build and
improvise:** the newest row Binance returns is for a period that may not have
closed yet. **Decide before you write the loop whether the current, possibly
incomplete period is stored or held back, state the decision in the output and
the log, and make it consistent between runs** — otherwise check (b),
idempotence, will fail intermittently and you will be tempted to blame the
network. Either choice is defensible; silently doing both is not.

## GATE 3.2b — DECLARED 2026-07-26, BEFORE THE BUILD, AND UNCHANGED SINCE (Law 4)

**This gate was written before the recorder existed and has not been touched by
the two sessions that deferred the step. Do not soften it.**

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
    copy, re-run, confirm the tool REPORTS the disagreement rather than silently
    overwriting it.
(f) **THE BRIEF IS UNAFFECTED:** `python cockpit\brief.py` still 3/3 with both
    instruments. 3.2b touches no cockpit file so this should be trivially true —
    verify it anyway, at the end as well as the start.
(g) **THE DATA IS PLAUSIBLE:** spot-check BTC open interest against Binance's
    own displayed figure. **A recorder that faithfully stores nonsense is not a
    working recorder.**
(h) **THE SABOTAGE DRILL IS BUILT IN FROM BIRTH.** This recorder's smoke test
    breaks itself on purpose and requires each break to be CAUGHT, exactly as
    both Context Deck instruments now do. **At minimum: a de-dup key that
    silently drops rows, a column written into the wrong field, and a timestamp
    converted with the wrong timezone.** **A gate that has never been attacked
    is a gate that has never been tested, and this ship learned that at the cost
    of a voided 48/48 — no new part ships without it.**
(i) **ADDED 2026-07-27, EARNED TWICE OVER — THE DRILL CHECKS WHAT IS WRITTEN,
    NOT WHAT THE PARSER RETURNED.** Both Context Deck gates failed because every
    check interrogated the parse and none compared the OUTPUT to the source.
    **The recorder's equivalent of "the printed sentence" is THE CSV ROW.** At
    least one check must read a written row back off disk and compare it,
    field by field, to a raw fetch the test made itself. **The helper under test
    is never called to judge itself.**

**STANDING LAWS.** `lab/vault/` read-only and `lab/` byte-identical — nothing in
`lab/` is touched, at all. Do NOT modify `cockpit/funding.py`,
`cockpit/fear_greed.py` (except under Part 1 above, and then only their
`__main__` blocks), `cockpit/brief.py`, `data/market_data.py`, `config.py` or
anything in `indicators/ regime/ risk/ signals/ journal/`. Nothing outside
`data/open_interest.py`, `data/oi_history/`, `PROGRESS_LOG.md`,
`EXECUTION_PLAN.md`, `ROADMAP.md`, `REVIEW_QUEUE.md` and this file. **The
risk-doctrine item (25% cap / ~0.49%) stays parked.** Do NOT start Step 3.3
(news headlines) even if everything passes quickly. INFORMATION, never a signal
— the signals doorway stands. One source, chosen once, never switched
mid-history.

## IF / THEN

| IF | THEN |
|---|---|
| Your twelfth sabotage ESCAPES either gate | Say so plainly, extend the drill to cover that class, and **R-001 and R-011 both stay open.** This is a success of the process, not a failure of the session. |
| BOTH gates catch everything you throw | **Clear R-011 and say "reviewed, found nothing".** Do not invent a defect to justify the session. |
| Binance answers HTTP 451 / restricted location | STOP. Do NOT swap exchanges. Write it up, tell the Commander — that swap is his call, never a session's. |
| The schema or the 30-day window differs from the measured facts above | **The new measurement wins.** Record the real shape, adapt, write the correction down. |
| A bogus symbol no longer returns `200 []` | Record it — and keep check (c) anyway. The recorder must refuse empty results however Binance signals them. |
| Backfill returns fewer than 175 rows | That is a FAILED bar, reported honestly — **not a number to tune until it passes.** |
| Any planning document contradicts a measurement you just took | The measurement wins and you write the correction down. **Fifth time this has been needed.** |
| A sabotage cannot be caught without changing production code | **STOP and report.** Changing the instrument to make a test pass is how a ship gets a gate that fits the code instead of code that fits the gate. |

**IF EVERYTHING PASSES:** write both halves into `PROGRESS_LOG.md` — the review
verdicts with the sabotages you invented and their actual output, then the build
with the gate tally, the real schema received, and every mistake as plainly as
every success (Law 1). **Update `REVIEW_QUEUE.md`: verdicts on R-011 and (if
earned) R-001, R-008, R-009, R-010, plus any new item this session could not
certify itself.** Update the marker, tick the recorder in `ROADMAP.md`, refresh
the MEASURED facts table. Commit, push. **Then raise the scheduling decision
with the Commander and do not silently skip it — a recorder that is never run
collects nothing. It must run on his LAPTOP, not the cloud watchman: GitHub's
runners are US-hosted and Binance geo-blocks US addresses, so a cloud recorder
might collect nothing, silently, for weeks. Present the one-line command and let
him decide.**

**IF PART 1 FINDS A REAL PROBLEM, or Gate 3.2b fails twice, or anything here is
unclear to you — STOP and tell the Commander.** If something in these orders is
unclear to a session that has no memory of writing them, that is a defect in the
orders and you should say so rather than guess.

---

# THE CLOSING RITUAL — no session ends without this

Before the final commit, in this order: **1.** `PROGRESS_LOG.md` (what happened,
mistakes as plainly as successes) · **2.** `REVIEW_QUEUE.md` (what could not be
certified, verdicts + new doubts) · **3.** `EXECUTION_PLAN.md` (where the ship is
now, including what is unproven) · **4.** `ROADMAP.md` (what exists and works) ·
**5.** `SESSION_ORDERS.md` (the next session's job, written for someone with NO
memory of you) · **6.** Commit. Push. **`THE_PATTERN.md` is the exception — do
not rewrite it unless a session earned a genuinely new lesson.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
2. **The risk-doctrine decision** — the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never after
   seeing results.**
3. **`MAX_PLAUSIBLE_RATE`** — measured 2026-07-26 at 13–16× looser than
   Binance's published cap (real: BTC/ETH ±0.300%, SOL ±0.375% per 8h; the code
   refuses only beyond ±5%). Safe, but too loose to be a real fence.
   **Recommendation: tighten to ~0.01. STILL NOT DONE — a session does not
   decide it by default.**
4. **The settled-rate anchor (R-004)** — returned to him on correct facts: the
   Step 3.2 orders explicitly permitted the extra call the previous session
   claimed they forbade. Printing it would put a number on the Brief the pilot
   can check with his own eyes.
5. **THE FUNDING LINE STAYED ON THE BRIEF, 2026-07-27, and he was told.** R-001's
   own wording said the line comes off "until the sign is proven". The sign HAS
   been proven, repeatedly, against Binance raw — most recently this session.
   **A session decided not to remove a line it had just verified as true. He can
   reverse that in one word.**
6. **FOUR law candidates, none adopted, all his call — no session promotes its
   own idea to law:**
   - *"A session may not certify its own work; anything it cannot certify is
     filed in `REVIEW_QUEUE.md` before the commit that ships it, and only an
     independent reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."* **Three earned examples.**
   - *"A check is not proven until it has been deliberately broken. Any gate
     guarding what the pilot reads ships with a sabotage exercise demonstrating
     it can FAIL."* **Now four working implementations and still not law.**
   - **NEWEST, earned 2026-07-27:** *"A gate must verify what the pilot READS —
     the whole line, words included — not what the parser returned."* **Two
     independently built instruments failed the same way twice each: the first
     rebuild fixed the digits and left the words unguarded, and a reversed
     sentence with correct numbers walked through a gate reporting PASSED.**
7. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.**
Information instruments can carry a lighter guard. The gauntlet cannot.
**Three sessions in a row have now failed their predecessor's work — the
substitute is working, and every hole was found by a session ORDERED to break
things rather than one being careful. Whatever reviews Phase 6 must be ordered
to break it too.**
