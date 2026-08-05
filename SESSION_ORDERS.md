# ZAR X PHASE 3 — **BUILD THE EVENT CALENDAR. INSTRUMENT 4 OF 5. YOU HAVE AN EXEMPTION FROM PART 1 AND IT IS THE COMMANDER'S, NOT MINE.**

*Written 2026-08-05 by the eighteenth generation, which attacked the news
instrument, found it silently rewriting publishers' headlines, and repaired it.*

---

# **>>> READ THIS FIRST. IT IS THE ONLY REASON YOU ARE NOT ATTACKING ANYTHING.**

## **THE COMMANDER HAS EXEMPTED YOU FROM PART 1. HE GRANTED IT HIMSELF, IN WORDS, ON 2026-08-05.**

    YOUR SESSION:  PART 1 — **SKIPPED. BY HIS ORDER. NOT BY MINE.**
                   PART 2 — BUILD the event calendar, instrument 4 of 5.

**HIS WORDS:** *"news is working and it only for me and i want to move forward"*
and *"i exempt only this for next session."*

**WHAT THE EXEMPTION COVERS, EXACTLY:** you do **not** attack the X1 repair —
`_text`, `_parse`, sabotage N12, or checks (r1)-(r4) in `cockpit/news.py`.
**Nothing else about it is suspended.** Every gate still runs. Every drill still
breaks itself. The closing ritual is untouched.

## **>>> AND THE PART THAT MATTERS MORE THAN THE EXEMPTION ITSELF**

    THIS EXEMPTION DIES WITH YOU.

    IT IS NOT INHERITED. IT IS NOT RENEWED BY SILENCE. YOU MAY NOT EXTEND IT
    TO YOURSELF, AND YOU MAY NOT GRANT ONE TO THE SESSION AFTER YOU.
    **ONLY THE COMMANDER CAN.** A CAP IS THE SAME ANIMAL AT A SMALLER SIZE.

    >>> THE ORDERS YOU WRITE MUST SEND THE SESSION AFTER YOU TO ATTACK WHAT
    >>> YOU BUILD — FULLY, AND WITH NO CAP OF ANY KIND.

**AND WRITE THIS INTO YOUR OWN ORDERS TOO: PART 1 HAS NOW BEEN REDUCED FOUR
TIMES** — exemption (2026-07-31), exemption (2026-08-03), cap (2026-08-03),
exemption (2026-08-05). **Each was his, each was justified on its own, and each
died with its session.** **A fifth in a row would be the moment to ask him
directly whether the outside check still exists.** Say the number out loud to
him rather than let it accumulate quietly.

## WHAT IS BEING TRADED AWAY, SO NOBODY PRETENDS IT IS FREE

**R-049 GOES UNVERIFIED.** The X1 repair changed how all six fields of every
story are read; **it was written by the session that found the fault, and the
checks that say it works were written by that same session.** It is filed
CATEGORY B and **stays OPEN**. **The first session NOT covered by this exemption
should treat it as live work.**

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The Commander is not a programmer and asked for it in this form. Write your
report to him the same way.*

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~60 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~125 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  ~55 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~10 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~25 s
                                54 checks, 12 sabotages, all CAUGHT
    vault INTACT · Brief 3/3 · lab/ untouched
    data/oi_history/  3 files, 222 lines each — untouched. Next scheduled
                      run 10-Aug-2026 09:00.

**EVERY GATE ON THIS SHIP IS GREEN AND ALL FIVE INSTRUMENTS ARE CORRECT.**

## What happened in the session before you, in four lines

1. **THE NEWS INSTRUMENT WAS SILENTLY REWRITING HEADLINES.** A headline written
   `Bitcoin <b>crashes</b> 20% as ETF outflows accelerate` reached the Brief as
   the single word **`Bitcoin`** — no clip mark, nothing saying so, fifty green
   checks while it happened. **Repaired; the gate now re-breaks it every run.**
2. **IT WAS NEVER FIRING, AND THAT WAS MEASURED.** 136 titles that morning, and
   116 more later through BOTH the old and the new code with **zero
   disagreements**. The repair provably changed nothing about real news.
3. **THE COMMANDER RULED THREE TIMES** — R-047 and R-048 SMALL, your exemption,
   and the news count archive deferred until the whole programme is complete.
4. **THE CONTEXT DECK IS THREE OF FIVE. YOU BUILD THE FOURTH.**

---

# **JOB 1 — BUILD THE EVENT CALENDAR. `EXECUTION_PLAN.md` PHASE 3, INSTRUMENT 4 OF 5.**

**WHAT THE PLAN ASKS FOR, VERBATIM:** *"Event calendar (manual JSON file the
Commander can edit + known recurring events: FOMC, CPI dates)."*

**WHAT IT IS FOR, IN HIS TERMS:** a line on the Context Deck that says what is
COMING — *"FOMC decision in 3 days"*, *"US CPI tomorrow"* — so he is never
surprised by a scheduled event he could have seen coming. **The plan is explicit
that macro belongs HERE and not in the news instrument: numbers and dates for
the machine, headlines for the Commander.**

## **>>> THE TRAP THIS INSTRUMENT IS SHAPED AROUND, AND IT IS THE SAME ONE TWICE ALREADY**

**A HARDCODED LIST OF DATES GOES STALE, AND A STALE CALENDAR LOOKS EXACTLY LIKE
A HEALTHY ONE.** This is Blockworks again — the feed that answered HTTP 200 with
fifty perfect stories whose newest was 209 days old — and it is the recorder's
empty-list trap a third time.

    A calendar whose last event is in the PAST must say so LOUDLY.
    IT MUST NEVER PRINT NOTHING AND LET SILENCE READ AS "no events coming".

**THAT IS THE ONE THING THIS INSTRUMENT MUST GET RIGHT**, and it is the check I
would build first if I were you. **An empty deck line is indistinguishable from
a quiet month, and this ship has been bitten by exactly that shape twice.**

## NAME THE AWKWARD CASES BEFORE YOU WRITE CODE, NOT AFTER DISCOVERING THEM

    * the JSON file is MISSING entirely
    * the JSON file is MALFORMED — he edits it by hand, so this WILL happen
    * an event dated in the PAST (already happened)
    * an impossible date — 2026-13-45, or "next tuesday"
    * an event with no name, or a name 300 characters long
    * TWO events on the same day
    * an event TODAY vs one in 3 days vs one in 6 months — the wording differs
    * the file is empty, or is `[]`
    * **the hardcoded recurring list RUNS OUT** — see the trap above
    * a TIMEZONE: FOMC is announced in US Eastern and his Brief prints local
      time. **State which zone the file is in, in the file, or this instrument
      will one day be a day out and nothing will say so.**

## THE RULES THAT ARE NOT NEGOTIABLE

- **INFORMATION, NEVER A SIGNAL.** *"FOMC in 2 days"* is a fact. *"FOMC in 2
  days — consider reducing exposure"* is advice and is forbidden. **Phase 6's
  three slots are locked BY NAME and none of them is a calendar.**
- **LAW 3 — THE FAIL-SAFE.** Any failure becomes ONE honest line and the Brief
  carries on with everything else intact. **The doorway never raises and never
  prints; it RETURNS.**
- **LAW 2 — the file path and the recurring list live in THIS compartment and
  nowhere else**, so he can edit either with one line.
- **>>> DO NOT NAME THE FILE `cockpit/calendar.py`.** Python has a standard
  library module called `calendar`. **`cockpit/events.py` is the safe name** and
  costs nothing to choose now.

## HOW YOU BUILD IT — THE THREE LAYERS, IN ORDER

1. **DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
   `.py` IN THE COMMIT, BEFORE WRITING CODE.** Twenty-three uses, twenty-three
   audits survived; mine was `f17f32f`.
2. **BUILD IT WITH THE SABOTAGE DRILL FROM BIRTH.** `collection_guard.py` and
   `news.py` were, and both were the better for it. **EVERY SABOTAGE MUST BE
   PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT COUNTS, ON THE CHANNEL IT
   ACTUALLY AFFECTS.** F10, S6 and B1 were each a break that could change
   nothing, scored ESCAPED by three different gates, and each cost a generation
   to find. **An unprovable sabotage is INERT and INERT IS A FAIL.**
3. **RUN THE GATE. EVERY CHECK GREEN INCLUDING EVERY SABOTAGE CAUGHT.** A
   failing gate is never committed and never called "mostly passed."

**COPY THE MACHINERY, DO NOT REINVENT IT.** `cockpit/news.py` is the closest
model — one doorway, injectable inputs, exact-equality checks typed out in the
gate, a permanent drill. **`cockpit/funding.py` has the file-descriptor door 3
that `news.py` lacks; if the event calendar's doorway is simple enough to carry
it, carry it.**

**IF IT WILL NOT FIT, BUILD NOTHING AND SAY SO. A half-built part is worse than
no part, and that rule is not exempted and never will be.**

---

# **JOB 2 — ONLY IF THE BUILD IS FINISHED AND GATED**

**R-042, R-043, R-044, R-045 and R-046 are still open** and none of them is
yours. **R-047, R-048 and R-049 are the eighteenth generation's own** — R-047
and R-048 have been ruled SMALL by the Commander and are closed as questions of
severity, **but neither is cleared.** **R-006 may NEVER be cleared by you or any
in-house session.**

**DO NOT GO HUNTING IN `news.py`. THAT IS WHAT THE EXEMPTION MEANS.**

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after. **THE RECIPES
    DIFFER BETWEEN FILES AND HAVE BEEN WRONG ON RECORD BEFORE:**
    - `cockpit/funding.py` — `__main__` at line 160; lines 1..159 joined by
      CRLF **WITH** a trailing CRLF → `95069d1bef8316d766910abda1880931…`
    - `data/open_interest.py` — `__main__` at line 243; lines 1..242 joined by
      CRLF with **NO** trailing separator → `5347bfecdf2ccfb2009770f9161dd6c5…`
    - `cockpit/news.py` — `__main__` at line 272; lines 1..271 joined by CRLF
      **WITH** a trailing CRLF → `503663762315b2f271d74dd2bdcf43bd…`
      (it was `0f0d6386…` at line 250 before the X1 repair moved it).
    - **>>> DO NOT TRUST ANY OF THOSE NUMBERS. VERIFY THE JOIN IS BYTE-FOR-BYTE
      THE RAW PREFIX OF THE FILE and refuse to print a hash if it is not.**
    - **A WHOLE-FILE HASH CANNOT DO THIS JOB.** It cannot tell "the pilot's code
      changed" from "the test around it changed".
(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.** R-014 was exactly that.
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE. A repair nobody
    re-tested is a hope.**
(f) Everything the old gates did, they still do. **Run all six invocations and
    read their output before you change anything.**
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may not
    clear your own. **You MAY clear R-042 through R-049 — but check first
    whether you are the one who benefits from clearing them.** That test is why
    the eighteenth generation did not clear R-046.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. **Outside a settlement window a
  red funding gate is a REAL failure — treat it as one.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` IN ITS LIVE
  CHECK (c) AND STILL PASS.** The bar is at least 3 of 5 publishers and at least
  3 stories. **All five answered on every reading on 2026-08-05.** **Below 3 of
  5 is real and it is R-044.**
- **ANY DRILL PRINTING `INERT` INSTEAD OF `CAUGHT` IS A FAIL.** That is
  deliberate. **If you see INERT, something real has drifted.**
- **S6, F10 AND B1 NO LONGER GO RED.** If any goes red it is a regression of a
  shipped repair and SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **THE RECORDER'S GATE TAKES ~55 s AND MUST BE RUN TWICE** — once normally and
  once with `TZ=UTC0`.
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** The laptop's own scheduled snapshot writes it while you work. **Commit
  it SEPARATELY, labelled as the laptop task's work — do not fold it into your
  change and do not revert it.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **>>> YOUR EXEMPTION FROM PART 1 IS HIS, IT IS FOR ONE SESSION, AND IT DIES
   WITH YOU.** See the top of this file.
2. **>>> R-047 AND R-048 ARE SMALL.** Ruled 2026-08-05 on the full facts,
   including that GATE 3.3's live check reads the very number R-047 corrupts.
   **Filed, not fixed, not cleared.**
3. **>>> THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS
   COMPLETE.** His words: *"we will build news section after when all the
   programme will be completed."* **He was told once, plainly, that this is the
   only deferral on the ship whose cost is permanent — the feeds hand out a few
   hours, old articles are edited and deleted, and the past cannot be bought
   back at any price. He ruled. It waits. Do not re-argue it.**
4. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
5. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
6. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
7. **DOOR 3 IS BUILT IN BOTH COCKPIT FILES. R-025 IS CLEARED.** Residue R-033.
8. **F10, S6 AND B1 WERE ALL REPAIRED ON HIS RULING, AND ALL THREE HOLD.**
9. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
10. **NEWS IS INFORMATION AND CAN NEVER BECOME A SIGNAL.** Phase 6's three slots
    are locked BY NAME — Turtle/Donchian, funding-rate fade, on-chain cycle
    thermometer. **None is news and none is a calendar.**

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`EXECUTION_PLAN.md` PHASE 3, instruments 4 and 5** — that is your build,
   and the plan's own words are the specification.
2. **`cockpit/news.py`** — **as a MODEL to copy, not a target to attack.** It is
   the newest and cleanest instrument on the ship: one doorway, injectable
   inputs, a gate holding its own expectations, a permanent drill.
3. **The LAST TWO entries of `PROGRESS_LOG.md`.** The file is ~620 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 34 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> IF YOU WRITE A WHOLE DOCUMENT OUT RATHER THAN EDITING IT, CHECK ITS LINE
  ENDINGS BEFORE YOU COMMIT.** **I rewrote `SESSION_ORDERS.md` and it came out
  LF-only in a repo where every document is CRLF.** Caught by my own check,
  converted back, no damage — **but nothing would have told me if I had not
  looked.** One command: count `\r\n` against bare `\n`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** PowerShell eats the quotes and
  **bash eats every BACKTICK as a command substitution.** **Four commands lost
  across three generations. I obeyed it and lost none. It works if you do it.**
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1**.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Nine consecutive sessions have guarded this way.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare your counts against `git show HEAD:<file>`;
  `PROGRESS_LOG.md` legitimately carries 2, 3 and 2 of the first three inside
  backticks, as deliberate quotations of the damage.**
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

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL. **THE EXEMPTION DOES NOT TOUCH THIS.**

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... verdicts on anything you ruled, plus one OPEN item
                            against whatever you built yourself.
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; correct any MEASURED fact that
                            moved.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words
                            brief, **WITH PART 1 ATTACK RESTORED AND NO CAP.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> PART 1 HAS NOW BEEN REDUCED FOUR TIMES RUNNING.** All four were his and
   each died with its session. **A fifth would be the moment to ask him directly
   whether the outside check still exists.** **Say the number to him.**
2. **>>> R-049 IS UNVERIFIED AND WILL STAY THAT WAY UNTIL SOMEBODY ATTACKS IT.**
   The X1 repair touched how every field of every story is read. **That is the
   price of the exemption and he was told it before he ruled.**
3. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — still the only thing he
   personally owes the R-037 repair. The Task Scheduler event log is off, so a
   next time would leave no evidence either:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

4. **THE CATEGORY B PILE IS TWENTY-TWO DEEP.** **It has grown every single
   session since it was created and has never once shrunk.** Cleared before the
   ship is used for real, at the same moment `brief.py` gets its gate.
   **Somebody should keep saying the number out loud to him.**
5. **THE TWO NEW PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** He ruled the
   PRINCIPLE — five publishers, different owners, not one hundred. BeInCrypto
   and Bitcoin.com were substituted for The Block (edge-blocked) and Blockworks
   (209 days stale). **All five answered on every reading on 2026-08-05.**
6. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED SIX TIMES:** *"A SABOTAGE MUST
   BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."* **N12 is
   the sixth proof.** **A session may never promote its own idea to law.
   THIRTEEN OTHER CANDIDATES REMAIN UNADOPTED.**
7. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5). If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. Next run 10-Aug-2026 09:00.
8. **>>> NOBODY HAS EVER ASKED WHETHER A SOURCE ITSELF CAN LIE (R-035).** Every
   gate proves the printed line matches what the source SENT; nothing asks
   whether the source was RIGHT. **X1 is a new argument for it: that was not a
   source lying — it was us mis-reading a source telling the truth perfectly —
   and it landed in exactly the same place.** **Still the strongest candidate
   for a whole session's attack.**
9. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
10. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **The one-line change that ends
    this class is `symbols=None`, resolved in the body.** It touches what the
    pilot reads, so no session may make it during a repair to a test.
11. **`cockpit/brief.py` HAS NO GATE** — not now, before going live. **The inch
    between it and his screen was checked by hand for the first time on
    2026-08-05 and is clean.**
12. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
13. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
14. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
15. **The settled-rate anchor (R-004)** — returned to him on correct facts.
16. **THE FUNDING AND NEWS LINES STAYED ON THE BRIEF** and he was told. One word
    reverses either.
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SEVEN TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard — and this
session's exemption is proof the Commander is willing to lighten it further when
he judges the risk small. The gauntlet cannot carry that, at any weight.**
