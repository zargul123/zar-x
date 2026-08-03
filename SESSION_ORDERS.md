# ZAR X PHASE 3 — **THE NORMAL RHYTHM IS BACK. PART 1 ATTACK, THEN PART 2 BUILD.**

*Written 2026-08-03 by the fifteenth generation. **The Commander's one-session
exception is spent. It applied to me, I did not use it, and I may not extend it
to you** — only he can do that. So you attack first, as every session before the
last one did.*

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The Commander is not a programmer and asked for it in this form. Write your
report to him the same way.*

## Where the ship is

    cockpit/fear_greed.py    GATE 3.1-R7  PASSED  exit 0  0 red  ~60 s
    cockpit/funding.py       GATE 3.2-R7  PASSED  exit 0  0 red  ~125 s
    data/open_interest.py    GATE 3.2b-R9 PASSED  exit 0  0 red  ~55 s
    vault INTACT · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 222 lines each (221 rows), sha256
                      a1ed6729bef45be6 / a077cf034bf66c26 / c8d97f7122544f70
                      window 2026-06-27T16:00:00Z → 2026-08-03T08:00:00Z

**ALL THREE INSTRUMENTS ARE CORRECT AND HAVE NEVER BEEN IN QUESTION.**

## What happened last session, in plain words

**The monthly open-interest recorder was due on 1 August. Windows says it ran on
3 August and succeeded. It did nothing at all** — no log line, no rows, no
commit. Five other scheduled jobs did the same thing in the same second and all
six reported success. **That is R-037 and it is the first fault on this ship
that is not in a gate — it is in the COLLECTING.**

**The data was recovered in time.** The real batch was run by hand: 41 rows per
asset, 221 stored, committed `5c7c54a`, pushed. **Had nothing run before the next
scheduled date of 1 September, 99 rows would have been gone permanently.**

**Two things were NOT done and you inherit both:** the ordered repairs to **S6
(R-034)** and **B1 (R-031)** did not happen, and **the mechanism behind R-037 is
not repaired** — nothing stops it happening again at the next boot after a gap.

---

# **PART 1 — ATTACK. AND YOUR TARGET IS TIME-LIMITED, SO DO IT FIRST.**

## **>>> R-038 — CHECK THE 123 ROWS THE LAST SESSION PUT INTO THE ARCHIVE. IT CANNOT BE CHECKED AFTER ~2026-09-02.**

**The fifteenth generation found the problem, performed the remedy, and verified
its own work. That is exactly the arrangement this ship does not accept.** It
proved the OLD rows survived — the byte prefix of each file still hashes to its
old value — **but nobody independent has checked that the 41 NEW rows in each
file are the rows Binance actually served.**

**THIS IS A REAL DEADLINE, NOT A FIGURE OF SPEECH.** Those rows sit inside a
rolling 30-day window. Once `2026-08-03T08:00:00Z` falls out of it — **around
2026-09-02** — nothing on earth can check them against the source again. **They
would simply be believed, forever, on the word of the session that wrote them.**

**HOW:** fetch the window yourself, from your own raw call, and compare it row for
row and field for field against what is on disk between `2026-07-27T16:00:00Z`
and `2026-08-03T08:00:00Z`. **Never ask the module where the file is or what the
rows should be** — that is B14's and R-014's lesson.

**REPORT IT EITHER WAY.** *"I checked all 123 rows against Binance and they
match"* is a real, valuable result and it clears R-038. **Do not manufacture a
defect to justify the session.**

## THEN INVENT ONE NEW SABOTAGE, AS ALWAYS

**A suggestion, not an order, and the Commander named it himself as the attack
nobody has ever made (desk item 3, now R-035):** every gate on this ship proves
the printed line matches what the source SENT. **Nothing anywhere asks whether
the source was RIGHT.** If a source served a wrong number, the Brief would print
it in perfect confidence and every alarm would stay green.

**Follow `THE_PATTERN.md`:** write the bars first, break a copy OUTSIDE the repo,
run the untouched control too, and **fill in THE FINDING REPORT before repairing
anything.**

---

# **PART 2 — BUILD. THE ORDER OF THESE TWO IS THE COMMANDER'S TO SET.**

## **JOB A — R-037: MAKE IT IMPOSSIBLE FOR A COLLECTION TO FAIL IN SILENCE**

**>>> DO NOT START THIS UNTIL YOU HAVE READ WHAT THE COMMANDER RULED. It is on
his desk below and the choice between these shapes is his, not yours.**

**THE FOUR CANDIDATES, WEAKEST TO STRONGEST. They are not alternatives — the
last one is the only one that does not depend on guessing the cause:**

1. **GIVE EACH TASK ITS OWN LOG FILE.** Six jobs append to one
   `journal/daily_runs.log` with `>>`. Reproduced: launch six together and five
   write nothing at all. **Removes the contention completely and costs one line
   per batch file.**
2. **THE ALARM MUST NOT BE ADDRESSED TO THE FILE THAT IS UNAVAILABLE.**
   `run_oi_recorder.bat` writes *"RECORDER FAILED — NOTHING WAS WRITTEN"* with
   `>> journal\daily_runs.log`. **The one line that would have told him it failed
   cannot be written for exactly the reason it needed writing.** This part needs
   no theory — it is plain in the file.
3. **ENABLE THE TASK SCHEDULER OPERATIONAL LOG.** It is **disabled**, which is
   why the record of 11:47:41 does not exist and the cause is still unproven.
   **Costs nothing and means the next occurrence leaves evidence.**
4. **>>> THE ONE THAT CATCHES ALL CAUSES, INCLUDING THE ONE NOBODY HAS PROVED:
   CHECK THE OUTCOME, NOT THE JOB.** Something the Commander already reads should
   state **the newest row in `data/oi_history/` and how many days old it is.**
   **Every fix above guards a mechanism. This one guards the DATA, and it would
   have caught this failure without anyone knowing why it happened.**
   **Where it goes is a real decision:** `cockpit/brief.py` is what he reads
   daily, but **he has ruled it gets no gate yet**, so putting a new check there
   adds ungated code to the one file with no guard. `CHECK_STATUS.bat` is the
   honest alternative. **Ask him; do not choose for him.**

**AND THE CHEAPEST FIX OF ALL, WHICH IS NOT CODE AT ALL — RUN IT WEEKLY.**
The batch file's own comment says *"a single missed month loses nothing. TWO
missed months in a row would."* **THAT REASONING IS NOW KNOWN TO BE WRONG, and
this session is where it broke:** the task ran, silently did nothing, and the
next attempt was a month away — so **ONE silent failure was enough to cost 99
irreplaceable rows.** **On a weekly schedule a silent failure costs nothing at
all**, because the next run still reaches back a full 30 days. **It is one line
in Task Scheduler and it removes most of the danger without a single code
change. Recommended strongly; his to rule.**

## **JOB B — THE TWO REPAIRS THAT DID NOT HAPPEN: S6 (R-034) AND B1 (R-031)**

**These are unchanged and fully specified. Both are faults in an ALARM, not in
any number the Commander reads — say that plainly in your report.**

**S6 — `cockpit/funding.py`.** It rotates the tickers but the printed LABEL comes
from the dictionary KEY, so the block is byte-identical whenever all three rates
format the same, and the gate prints *"ESCAPED — THE GATE IS DECORATIVE"* about a
lie it never told. **Measured over 6,441 real settlements: 15.84%, one in 6.3 —
an UPPER BOUND, because it is measured on SETTLED rates and the Brief prints the
running ESTIMATE. Do not quote it as the live figure.**

**B1 — `data/open_interest.py`.** It formats the time as LOCAL instead of UTC, so
**on a UTC machine it changes nothing.** The Commander's laptop is UTC+5, so B1
works here and is NOT costing him anything; **it is blind on the cloud.** Fix it
anyway — same shape, twenty minutes.

**THE TEMPLATE FOR BOTH IS ALREADY IN THE REPO AND ALREADY GREEN. YOU ARE
COPYING, NOT INVENTING:**

- **S6's template:** the section titled **`2b) F10'S TWO BRANCHES (Gate 3.1-R7 a)`**
  in `cockpit/fear_greed.py`'s `__main__`. It proves three things every run:
  values DIFFER → the lie speaks · values EQUAL → the repair makes it speak
  anyway, **using a number THE GATE holds, never one read from the file on
  trial** · values EQUAL through the **OLD** form → **required to be a no-op**,
  which is what proves the defect was real. **Your S6 repair must print the same
  three lines, and BOTH branches must run every time whatever the market is
  doing.**
- **B1's template:** sabotage **`S5`** in `cockpit/funding.py`, whose author wrote
  the reason down on 2026-07-28: *"S5 shifts by a fixed hour rather than dropping
  the timezone: dropping it is a no-op on a machine already set to UTC, and a
  drill that only works on some machines is not a drill."*
  **>>> AND RUN YOUR FINISHED GATE WITH THE CLOCK SET TO UTC.** `TZ=UTC0` —
  Windows Python honours it, measured. **Run it BOTH ways, UTC+5 and UTC, and
  print both results. A repair for a UTC-only fault never run on a UTC clock is
  not tested.**

### THE RULES THAT APPLY TO EVERY BUILD ABOVE

(a) **DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
    `.py` IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves the
    bar came first. **Record the hash AFTER your final push** — the cloud watchman
    pushes every four hours and a rebase rewrites your hashes underneath you.
(b) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, never assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `open_interest.py` 243), AND a sha256 of the production
    half before and after, printed side by side.
    - `cockpit/funding.py`: **raw byte prefix up to the `if __name__ ==
      '__main__':` marker** (first N-1 lines joined by CRLF **WITH** a trailing
      CRLF) → `95069d1b…`
    - `data/open_interest.py`: first N-1 lines joined by CRLF with **NO**
      trailing separator → `5347bfec…`
    - **Reproducing `5347bfec…` exactly is what proves your script is right.
      Check that one first, then trust the other.**
(c) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never calls
    the helper under test to judge itself, and **never asks the module where to
    look.**
(d) **THE DRILL IS PERMANENT** — repaired breaks stay in, caught every run,
    originals restored and the restoration verified.
(e) **RE-RUN THE ORIGINAL FAULT AGAINST YOUR REPAIRED FILE.** For S6, force the
    three rates equal and show the gate goes GREEN where it went red. For B1, set
    the clock to UTC and show the same. **Show it failing for the reason it
    claims, not incidentally.**
(f) Everything the old gates did, they still do. **All 18 funding sabotages and
    all 14 recorder sabotages still caught.**
(g) **NO new file, NO new dependency, NO extra call from the Brief's path.**
(h) **RUN `py_compile` BEFORE THE GATE.**
(i) **FILE A REVIEW ITEM AGAINST EACH OF YOUR OWN REPAIRS AND LEAVE THEM OPEN.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

## **IF THERE IS NOT ROOM, STOP — AND DO NOT APOLOGISE FOR IT**

    PART 1 IS THE PROMISED RESULT. Everything in PART 2 is a bonus.
    A half-built part is worse than no part. Checking the 123 rows and
    reporting honestly is a complete, successful session. Say so plainly.

---

# **THE NEWS INSTRUMENT — STILL UNBUILT, AND IT IS NOW THIRD IN LINE**

**Do not start it unless PART 1 and JOB A are both finished and there is real
room.** Everything needed is in the orders of 2026-07-31 (evening), preserved in
`git show 5e6d306:SESSION_ORDERS.md`, and in `EXECUTION_PLAN.md` Phase 3 step 3
where the CryptoPanic correction is struck and left visible. In short:

- **THERE IS NOTHING TO SIGN UP FOR.** CryptoPanic is a paid product now —
  measured HTTP 403 / 404 unauthenticated. **The adopted source is the
  publishers' own public feeds**, read with Python's own
  `xml.etree.ElementTree`. No key, no account, no new dependency.
- **MEASURE R-036 FIRST, BEFORE ANY CODE.** Headlines land every few minutes, so
  the gate's fetch and the instrument's fetch can legitimately disagree and the
  gate would go red with nothing wrong. Fetch each feed twice ~90 s apart, record
  how often the top story changed and the median gap between stories, **and write
  the numbers into `PROGRESS_LOG.md` either way.**
- **THE FIX IF THE COLLISION IS REAL: one fetch, two readers** — plus a separate,
  deliberately LOOSE live check, because a gate that only judges handed-over
  bytes never tests the real trip to the internet.
- **A feed answering HTTP 200 with ZERO stories must FAIL LOUDLY.** Printing
  "0 headlines" as though the world were quiet is the worst thing this instrument
  can do, and it is the recorder's empty-result trap in a new hat.

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. **Outside a settlement window a red
  funding gate is a REAL failure — treat it as one.**
- **`python cockpit\funding.py` ALSO GOES RED ON S6 ROUGHLY ONE SETTLEMENT IN
  SIX** — that is R-034, unrepaired. Check section 1: if all three rates print the
  same, that is R-034 and not your breakage. **It was CAUGHT on 2026-08-03 only
  because the three rates differed. That was luck, not a fix.**
- **`data/open_interest.py` SCORES B1 AS CAUGHT ON THIS LAPTOP** because it runs
  at UTC+5. That is R-031 hiding, not R-031 absent.
- **IF `cockpit/fear_greed.py` GOES RED ON F10, THAT IS A REGRESSION OF A REPAIR
  AND IT IS SERIOUS** — it cannot happen unless someone undid it. **It was green
  on 2026-08-03, all three branches.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT. R-025 IS CLEARED.** The residue is R-033, still open.
5. **F10 was repaired on his ruling of 2026-07-31 and it holds.**
6. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.** He killed it himself
   and he was right.

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment and the housekeeping that has bitten this ship. None of it is
repeated here.**

1. **`REVIEW_QUEUE.md` — R-037 and R-038 are new and they are your worklist**,
   then R-034 and R-031. **R-006 may NEVER be cleared by you or any in-house
   session.**
2. **The `2b) F10'S TWO BRANCHES` section of `cockpit/fear_greed.py`'s
   `__main__`** — your template for S6, shipped and green.
3. **The `S5` comment in `cockpit/funding.py`'s `_SABOTAGES` list** — your
   template for B1, in its author's own words.
4. **The LAST TWO entries of `PROGRESS_LOG.md`.** The file is ~530 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 28 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Five consecutive sessions have guarded this way and never once been wrong.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first. `py_compile` before the gate.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
  Use Python with `encoding='utf-8'` or the editor tools.
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`, `Â·`,
  `â†`, `Ã`, `âœ`. **MEASURED 2026-08-03: `PROGRESS_LOG.md` holds 7 hits (2 + 3 +
  2), all pre-existing deliberate quotations of old damage. Compare your count
  against `git show HEAD:<file>` so you know whether YOU added any** — that is
  cheaper and surer than eyeballing it.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> R-037 — HIS RULING IS NEEDED BEFORE JOB A STARTS.** An unattended job
   can do nothing, write nothing and report success. **The data was saved this
   time; the mechanism is unrepaired and the next scheduled run is 1 September.**
   **The single cheapest protection is a schedule change, not code: run the
   recorder WEEKLY.** Then choose among the four shapes in JOB A — and note that
   only the fourth, checking the DATA rather than the job, catches a cause nobody
   has proved.
2. **>>> DOES THE ONE-SESSION EXCEPTION CARRY?** He suspended PART 1 so that S6
   and B1 would be repaired. The session it applied to did not repair them.
   **A session may not extend a suspension of the rules to itself, so the next
   one attacks first unless he says otherwise.**
3. **>>> R-038 HAS A DEADLINE OF ABOUT 2026-09-02.** The 123 rows the last
   session appended can only be checked against Binance while they remain inside
   the rolling 30-day window. **After that they are believed forever on one
   session's word.**
4. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED BY THREE FILES AND FIVE
   SESSIONS:** *"A SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS
   VERDICT MEANS ANYTHING."* F10, B1 and S6 are the same fault in three files.
   **A session may never promote its own idea to law. It is his and only his.**
   **THIRTEEN OTHER CANDIDATES REMAIN UNADOPTED.**
5. **NOBODY HAS EVER ASKED WHETHER A SOURCE ITSELF CAN LIE (R-035).** No file on
   this ship talks to more than one source. **Every gate proves the printed line
   matches what the source SENT; nothing asks whether the source was RIGHT.**
   **His own words: that is fake data on his screen in real time, and it is the
   only door with nobody standing at it.**
6. **THE CATEGORY B PILE IS THIRTEEN DEEP** — R-038 added, nothing removed.
   **Cleared before the ship is used for real, at the same moment `brief.py` gets
   its gate.**
7. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
8. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this class is `symbols=None`, resolved in the body — `funding.py` already does
   it that way.** It touches what the pilot reads, so no session may make it
   during a repair to a test. **Ten generations have fixed the instance and left
   the pattern.**
9. **`cockpit/brief.py` HAS NO GATE** — he has ruled: not now, before going live.
10. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
11. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
12. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
13. **The settled-rate anchor (R-004)** — returned to him on correct facts.
14. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
15. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SEVEN TIMES, NOT ADOPTED.**
16. **BOTH COCKPIT GATES ARE SLOW BECAUSE OF DOOR 3** — ~125 s and ~60 s — **and
    that slowness turned out to be load-bearing** (R-033). **Making them faster is
    no longer a free change and somebody must say so if he asks.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.**
