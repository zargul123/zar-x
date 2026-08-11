# ZAR X PHASE 3 — **VERIFY R-049. THEN BUILD INSTRUMENT 5 OF 5 UNDER A GATE THAT IS ALREADY DECLARED AND THAT YOU CANNOT LOWER.**

*Written 2026-08-11 by the twentieth generation, which attacked the event
calendar uncapped, cleared two review items, filed three, built nothing, and
declared GATE 3.5 before stopping.*

---

# **>>> READ THIS FIRST. YOUR GATE IS ALREADY WRITTEN AND IT IS NOT YOURS TO EDIT.**

    YOUR SESSION:  PART 1 — **VERIFY R-049**, the X1 repair in `cockpit/news.py`.
                            Unverified for TWO generations now.
                   PART 2 — **BUILD THE WHALE WATCH under GATE 3.5**, which is
                            already declared in `PROGRESS_LOG.md`, committed
                            alone, by a session that will never build it.

**PART 1 IS UNCAPPED AND UNEXEMPTED.** The 2026-08-05 exemption is long spent
and nothing has replaced it. **The count that the last three sessions were told
to say out loud — "Part 1 has been reduced four times running" — is finished
business: the session before you was not reduced, and neither are you. Do not
raise it with him again unless somebody reduces Part 1 a fifth time.**

## **>>> AND THE THING THAT MAKES YOUR BUILD DIFFERENT FROM EVERY BUILD BEFORE IT**

**GATE 3.5 WAS DECLARED BY SOMEBODY WHO IS NOT YOU AND WHO HAS NOTHING TO GAIN
FROM WHERE THE BAR SITS.** Every gate on this ship before it was written by the
session that then built the thing. **You cannot quietly reinterpret a word of it
to match what you managed to build.** If you think a condition in it is wrong,
**say so to the Commander out loud, in your report, and let him rule — never
edit it and carry on.**

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The Commander is not a programmer and asked for it in this form. Write your
report to him the same way.*

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~66 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~125 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  ~66 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red  ~62 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~8 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~5 s
                                54 checks · live: 80 stories, 5 of 5 publishers
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  ~1.5 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red
                                69 checks, 12 sabotages, all CAUGHT
    vault INTACT 6 of 6 · Brief 3/3, FOUR Context Deck lines · lab/ untouched

**EVERY GATE ON THIS SHIP IS GREEN AND ALL SIX INSTRUMENTS ARE CORRECT.**

**>>> THOSE TIMINGS ARE MEASURED, 2026-08-11, AND TWO OF THEM CORRECT THE ORDERS
YOU WOULD OTHERWISE HAVE INHERITED.** The old orders said news ~25 s and events
~5 s. **They run in ~5 s and ~1.5 s. A fast run is not a broken run.**

## What happened in the session before you, in six lines

1. **THE EVENT CALENDAR'S OUTPUT IS RIGHT AND IT WAS PROVED THREE SEPARATE
   WAYS** — hand arithmetic done without `zoneinfo`, the Fed's own page, and the
   BLS's own page, all on 2026-08-11.
2. **NOT ONE OF THE SIXTEEN DATES HAS MOVED.** The first time anybody on this
   ship has asked a source whether it still says the same thing. It took four
   minutes. **`bls.gov` still answers HTTP 403 to a non-browser fetch.**
3. **BUT THREE OF FOUR NEW SABOTAGES WALKED STRAIGHT THROUGH GATE 3.4** at a
   boundary nobody had ever tested. **That is R-054 and it is on his desk.**
4. **R-050 AND R-052 ARE CLEARED. THE CATEGORY B PILE SHRANK FOR THE FIRST TIME
   EVER — and still went up, to twenty-seven.**
5. **NOTHING WAS BUILT, ON PURPOSE.** An instrument to this ship's standard
   would not have fitted honestly, and a half-built part is worse than no part.
6. **THE SOURCES FOR YOUR BUILD ARE ALREADY MEASURED AND THE NUMBERS ARE IN
   `ROADMAP.md`. YOU DO NOT GET TO CHOOSE ON A GUESS.**

---

# **JOB 1 — VERIFY R-049. IT HAS BEEN WAITING TWO GENERATIONS.**

`cockpit/news.py`'s X1 repair changed how **all six fields of every story** are
read — title, guid, link, pubDate and both Atom stamps. **The session that found
the fault wrote the fix, and the checks that say it works were written by that
same session.** It went unverified because the Commander bought a build with it,
knowingly; the session after that ran out of room; **you are the third.**

**What that means concretely:** `_text` walks an element and gathers every scrap
of text in it. Checks (r1)-(r4) and sabotage N12 exist to prove it. **Attack the
repair, not the original fault** — the original fault is well documented and
reproducing it proves nothing new.

**AND THE MEASUREMENT THE REPAIR'S OWN AUTHOR REPORTED AGAINST HIS OWN
INTEREST:** 136 real titles across all five publishers, **not one carrying
markup**. The repair has never once fired in production. **That cuts both ways
and you should say which way you think it cuts.**

**IF R-049 COMES UP CLEAN QUICKLY, SAY SO PLAINLY AND MOVE TO JOB 2.** "I
attacked it hard and found nothing" is a real result. **DO NOT MANUFACTURE A
DEFECT TO JUSTIFY A SESSION.**

## HOW PART 1 IS DONE — THE TEETH, NOT A SUMMARY

1. **Write the bars for "this review clears" BEFORE running anything.**
2. **Invent at least one NEW sabotage.** Break it in a copy of the WHOLE repo
   **outside the repo**, and **run the untouched copy FIRST — if the control is
   not green the rig is broken and nothing you conclude means anything.** Prove
   a positive control can turn the gate RED before you believe any green.
3. **Every break must be PROVED to change what somebody reads before its verdict
   counts.** A break that changes nothing is INERT and proves nothing.
4. **FILL IN THE FINDING REPORT BEFORE REPAIRING ANYTHING.** `THE_PATTERN.md`
   carries it; the Commander's Three Questions come first. **THE REPORT COMES
   BEFORE THE REPAIR, ALWAYS.**
5. `git status` clean afterwards. Verdict recorded in `REVIEW_QUEUE.md`.

---

# **JOB 2 — THE WHALE WATCH, INSTRUMENT 5 OF 5, UNDER GATE 3.5**

**READ THE GATE FIRST. It is the 2026-08-11 entry in `PROGRESS_LOG.md`, thirteen
numbered conditions and one acceptable outcome that is not a failure.** Two of
its conditions exist because of what happened to GATE 3.4 on 2026-08-11 and you
should understand them before you write a line:

- **CONDITION 11 — EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT TURNS
  OVER, AND ONE STEP EITHER SIDE.** A threshold tested only far from its edge is
  a threshold nobody has tested.
- **CONDITION 12 — EVERY DEFAULT THE COMMANDER IS INVITED TO RELY ON IS
  EXERCISED BY A CHECK, NOT MERELY PINNED AS A CONSTANT.**

## THE SOURCES ARE MEASURED. HERE IS WHAT YOU ARE WORKING WITH.

**Probed 2026-08-11 08:44 UTC, full numbers in `ROADMAP.md`:**

    /futures/data/topLongShortPositionRatio    200  0.48 s  newest 5 min
    /futures/data/topLongShortAccountRatio     200  0.33 s  newest 5 min
    /futures/data/globalLongShortAccountRatio  200  0.33 s  newest 5 min
    /futures/data/takerlongshortRatio          200  0.30 s  newest 10 min
    api.blockchain.info charts                 200  ~1.1 s
    api.blockchair.com/bitcoin/stats           200  1.04 s
    mempool.space fees                         200  0.61 s

**THE STRONGEST HONEST CANDIDATE IS `topLongShortPositionRatio` BESIDE
`globalLongShortAccountRatio`** — the biggest accounts on the venue, weighted by
position size, next to everybody else. Free, keyless, five minutes fresh, on a
host this ship already reaches and already trusts for funding and open interest.

**>>> AND THE GAP YOU MUST NOT PAPER OVER: exchange RESERVE and NETFLOW data —
what the plan asks for most directly — IS PAID.** CryptoQuant, Glassnode and
Whale Alert all require a key. **So whatever you build is NOT an exchange-flow
instrument and the wording on the Brief must not imply that it is.** It is one
venue's own reported figures about its own customers, and the line must say so.

**RE-PROBE BEFORE YOU CHOOSE ANYWAY. R-056 is open precisely because nine
endpoints answering on one morning is not nine endpoints that work** — CryptoSlate
was found rate-limiting within an hour of being adopted, exactly as a filed doubt
had warned.

**COPY THE MACHINERY, DO NOT REINVENT IT.** `cockpit/events.py` is the newest and
has the most complete guard on this ship — one doorway, everything injectable, a
gate holding its own expectations, **door 3 at the FILE DESCRIPTOR plus a
fresh-interpreter check**, and a permanent twelve-break drill.
`cockpit/news.py` is the model for anything that fetches over the internet.

**IF IT WILL NOT FIT, BUILD NOTHING AND SAY SO. A half-built part is worse than
no part, that rule is not exempted and never will be, and the session before you
obeyed it.**

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after.

    **PICK ONE JOIN VARIANT, USE IT ON BOTH SIDES, AND VERIFY THE JOIN IS THE
    RAW PREFIX OF THE FILE BEFORE PRINTING ANY HASH.** R-053 settled this:
    **both variants are byte-for-byte raw prefixes of all five instrument files
    — the files do not differ, only which variant a session picked.** With the
    trailing CRLF, measured 2026-08-07:

        cockpit/fear_greed.py       __main__ line 113   bb31626c493a1ac6…
        cockpit/funding.py          __main__ line 160   95069d1bef8316d7…
        cockpit/news.py             __main__ line 272   503663762315b2f2…
        data/open_interest.py       __main__ line 243   c68508e881524cf0…
        data/collection_guard.py    __main__ line 156   d6518cd7208eb611…
        cockpit/events.py           __main__ line 372   NEVER MEASURED

    **DO NOT TRUST THOSE NUMBERS. RE-MEASURE THEM.** A remembered hash is exactly
    what R-053 is about. **A WHOLE-FILE HASH CANNOT DO THIS JOB** — it cannot tell
    "the pilot's code changed" from "the test around it changed".

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.** R-014 was the first; B14 was the same shape in a report.
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE. A repair nobody
    re-tested is a hope.**
(f) Everything the old gates did, they still do. **Run all EIGHT invocations and
    read their output before you change anything.** One script, output to a
    file, and **count the red ticks by machine rather than by eye.**
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may not
    clear your own. **You MAY clear R-042 through R-056 — but check first
    whether you are the one who benefits from clearing them.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. **Outside a settlement window a
  red funding gate is a REAL failure — treat it as one.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` IN ITS LIVE
  CHECK AND STILL PASS.** The bar is at least 3 of 5 publishers and at least 3
  stories. **All five answered on 2026-08-11, 80 stories. Below 3 of 5 is real
  and it is R-044.**
- **`cockpit\events.py --gate` HAS NO NETWORK DEPENDENCE except its live check.
  IT TAKES ABOUT 1.5 SECONDS, NOT 5.** That is measured, not a fault.
- **ANY DRILL PRINTING `INERT` INSTEAD OF `CAUGHT` IS A FAIL.** That is
  deliberate. **If you see INERT, something real has drifted.**
- **S6, F10 AND B1 NO LONGER GO RED.** If any goes red it is a regression of a
  shipped repair and SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **THE RECORDER'S GATE MUST BE RUN TWICE** — once normally and once with
  `TZ=UTC0`. **GATE 3.4 is run twice for the same reason.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** The laptop's own scheduled snapshot writes it while you work. **Commit
  it SEPARATELY, labelled as the laptop task's work.**
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.** The
  weekly open-interest task created it on 10-Aug-2026. It is not in
  `.gitignore`. **Leave it or ignore it deliberately; do not sweep it into a
  commit without deciding.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **R-047 AND R-048 ARE SMALL.** Ruled 2026-08-05. Filed, not fixed, not
   cleared.
2. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS
   COMPLETE.** His words. **He was told once, plainly, that this is the only
   deferral on the ship whose cost is permanent. He ruled. It waits. Do not
   re-argue it.**
3. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
4. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
5. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
6. **DOOR 3 IS BUILT IN BOTH COCKPIT INSTRUMENTS AND IN THE EVENT CALENDAR.
   R-025 IS CLEARED.** Residue R-033. **`news.py` is still the one without it
   (R-046).**
7. **F10, S6 AND B1 WERE ALL REPAIRED ON HIS RULING, AND ALL THREE HOLD.**
8. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
9. **NEWS IS INFORMATION AND CAN NEVER BECOME A SIGNAL, AND NEITHER CAN THE
   CALENDAR — NOR THE WHALE WATCH.** Phase 6's three slots are locked BY NAME:
   Turtle/Donchian, funding-rate fade, on-chain cycle thermometer.

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`PROGRESS_LOG.md`, the LAST TWO entries** — the 2026-08-11 attack and
   **GATE 3.5, which is your bar.** The file is ~660 KB; do not read it all.
2. **`REVIEW_QUEUE.md`, the 2026-08-11 block** — R-054, R-055, R-056, and the
   two clearances.
3. **`ROADMAP.md`, the 2026-08-11 measured facts** — your source numbers.
4. **`cockpit/news.py`** for Job 1, **`cockpit/events.py`** as the model for
   Job 2.
5. **`EXECUTION_PLAN.md` PHASE 3, instrument 5** — the plan's own words are the
   specification.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours and it pushed
  five times while the last session worked.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 34 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> AFTER ANY EDITOR EDIT, CHECK THE LINE ENDINGS AGAIN BEFORE COMMITTING.**
  An editing tool can hand back LF in a CRLF repo and nothing will say so. One
  command: count `\r\n` against bare `\n`.
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE. Mojibake
  counts CAN be compared against HEAD.
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1**.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Eleven consecutive sessions have guarded this way.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** PowerShell eats the quotes and bash
  eats every BACKTICK. **And do not run a script you have not written yet — the
  last session did exactly that and got "can't open file".**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare against `git show HEAD:<file>`;
  `PROGRESS_LOG.md` legitimately carries a few inside backticks as deliberate
  quotations of the damage.**
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH. `python …` ON ITS OWN DOES NOT WORK ON HIS MACHINE** — bare
  `python` hits a **pyenv shim with no version selected**. His PowerShell opens
  at `C:\WINDOWS\system32`. The working form is one line:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces a
  fresh one, `CHECK_STATUS.bat` shows the collection's health.

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL.

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... verdicts on anything you ruled, plus one OPEN item
                            against whatever you built yourself.
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; correct any MEASURED fact that
                            moved.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words brief.
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> NEW AND THE ONLY ONE THAT BLOCKS ANYTHING: R-054 — THREE SABOTAGES
   WALKED THROUGH GATE 3.4.** Twenty days of slack in the calendar's staleness
   guard, an off-by-one in it, and a change to the default-time path that moved
   one of his own events a whole day — **all three with the gate green.**
   **Recommended SMALL (file it, keep building); the argument for SERIOUS is
   written out beside it so he can overrule.** **If he rules SERIOUS, the next
   session repairs GATE 3.4 — three boundary checks and one default-time check,
   all below the `__main__` line — and builds nothing else.**
2. **>>> R-049 HAS NOW BEEN CARRIED FOR TWO GENERATIONS UNVERIFIED.** It is
   Job 1 above. **He should know it slipped twice.**
3. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — still the only thing he
   personally owes the R-037 repair. The Task Scheduler event log is off, so a
   next time would leave no evidence either:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

4. **THE CATEGORY B PILE IS TWENTY-SEVEN DEEP — AND IT SHRANK FOR THE FIRST TIME
   EVER THIS SESSION** (two cleared, three filed). Cleared before the ship is
   used for real, at the same moment `brief.py` gets its gate. **Somebody should
   keep saying the number out loud to him.**
5. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes `"timezone": "UTC"` to `"timezone":
   "Asia/Karachi"` if he would rather write his own local times. It does not
   affect FOMC or CPI, which carry their own zone. **Still his to decide.**
6. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com. **All five answered on 2026-08-11, 80 stories.**
7. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED EIGHT TIMES:** *"A SABOTAGE
   MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."*
   **A session may never promote its own idea to law. THIRTEEN OTHER CANDIDATES
   REMAIN UNADOPTED — and a fourteenth is now earned: "EVERY THRESHOLD IS TESTED
   AT THE EXACT VALUE WHERE IT TURNS OVER", which R-054 paid for.**
8. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5). If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. **It ran on 10-Aug-2026 and pushed.**
9. **R-035 IS A LITTLE LESS ABSTRACT THAN IT WAS.** Somebody asked a source
   whether it was still saying the same thing, for the first time, and it took
   four minutes. **A later session could have the calendar re-read
   `federalreserve.gov` and `bls.gov` and go red on a disagreement (R-051).**
10. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
11. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **The one-line change that ends
    this class is `symbols=None`, resolved in the body.** It touches what the
    pilot reads, so no session may make it during a repair to a test.
12. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
13. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
14. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
15. **The settled-rate anchor (R-004)** — returned to him on correct facts.
16. **THE FUNDING, NEWS AND EVENTS LINES ARE ALL ON THE BRIEF** and he was told.
    One word removes any of them.
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SEVEN TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**
