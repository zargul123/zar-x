# ZAR X PHASE 3 — **ATTACK THE EVENT CALENDAR. NOBODY HAS. THEN BUILD INSTRUMENT 5 OF 5.**

*Written 2026-08-07 by the nineteenth generation, which built the event calendar
under GATE 3.4 and attacked nothing, because the Commander had exempted it.*

---

# **>>> READ THIS FIRST. YOUR PART 1 IS BACK, IN FULL, WITH NO CAP.**

    YOUR SESSION:  PART 1 — **ATTACK `cockpit/events.py`. UNCAPPED. NO EXEMPTION.**
                   PART 2 — BUILD the whale watch, instrument 5 of 5 —
                            **ONLY IF PART 1 ALLOWS IT.**

**THE EXEMPTION THE LAST SESSION HAD WAS THE COMMANDER'S, IT WAS FOR ONE
SESSION, AND IT DIED WITH THAT SESSION.** It was not inherited, it was not
renewed by silence, and **no session may grant one to itself or to anyone else.
Only he can.**

## **>>> AND THE NUMBER HE MUST BE TOLD, WHICH IS WHY IT IS AT THE TOP**

    PART 1 HAS NOW BEEN REDUCED FOUR TIMES RUNNING.

    exemption (2026-07-31) · exemption (2026-08-03) · cap (2026-08-03) ·
    exemption (2026-08-05, which covered the session that wrote this file)

**Each was his, each was justified on its own, and each died with its session.
The last session was ordered to say the number out loud to him and did.
A FIFTH IN A ROW IS THE MOMENT TO ASK HIM DIRECTLY WHETHER THE OUTSIDE CHECK
STILL EXISTS** — not to refuse him, but because four in a row is a pattern and
he is the only person who can see it and decide it is fine.

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
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  ~5 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red
                                69 checks, 12 sabotages, all CAUGHT
    vault INTACT · Brief 3/3, FOUR Context Deck lines · lab/ untouched
    data/oi_history/  3 files, 222 lines each — untouched. Next scheduled
                      run 10-Aug-2026 09:00.

**EVERY GATE ON THIS SHIP IS GREEN AND ALL SIX INSTRUMENTS ARE CORRECT.**

## What happened in the session before you, in five lines

1. **THE BRIEF NOW SAYS WHAT IS COMING** — sixteen scheduled events ahead, the
   next three named, with the days until each and **the time on the Commander's
   own clock rather than New York's.**
2. **NO DATE WAS REMEMBERED BY A MODEL.** Every one was read off the Fed's and
   the BLS's own pages on 2026-08-07. **`bls.gov` answers HTTP 403 to a
   non-browser fetch** — the same edge block that killed The Block — so it was
   read in a real browser.
3. **THE BLS SCHEDULE STOPS DEAD AT 10 DEC 2026, so the built-in CPI list runs
   out in about four months.** That is a dated fact, not a decorative horizon,
   and the staleness guard is built around it.
4. **IT ATTACKED NOTHING. THAT WAS HIS ORDER, AND IT IS OVER.**
5. **THE CONTEXT DECK IS FOUR OF FIVE. YOU ATTACK THE FOURTH, THEN BUILD THE
   FIFTH.**

---

# **JOB 1 — ATTACK `cockpit/events.py`. THIS IS THE JOB. THE BUILD IS SECOND.**

**IT WAS BUILT YESTERDAY BY A SESSION THAT ALSO WROTE EVERY CHECK THAT SAYS IT
WORKS, AND ITS AUTHOR SAID SO IN WRITING.** That is Layer 3's entire reason to
exist: **a builder cannot invent the attack they are blind to.** On 2026-08-05 a
fresh session found X1 in `news.py` — **in none of the five places its builder
had named as weakest** — in a morning.

## **>>> START HERE: THE ONE THING ITS AUTHOR IS MOST WORRIED ABOUT (R-050)**

**EVERY EXPECTED STRING IN GATE 3.4 WAS COMPUTED IN A MODEL'S HEAD, AND ALL 69
CHECKS WENT GREEN ON THE VERY FIRST RUN.** Weekdays, day counts across month
boundaries, and **four answers that turn on United States daylight saving**:

    28 Jan 2027 is EST (UTC-5) · 17 Mar 2027 is EDT (UTC-4)
    an event at 18:00 in New York lands at 03:00 the NEXT day in Karachi

**Either the arithmetic was right, or the gate and the module agree with each
other about something false — which is R-014's exact shape.** **CHECK THE
DST ROWS AGAINST A CLOCK THAT HAS NOTHING TO DO WITH THIS SHIP.** If Python's
`zoneinfo` and the builder's head are wrong in the same direction, **nothing
currently on this ship would notice.**

## THE FIVE PLACES ITS AUTHOR NAMED — SO YOU CAN START SOMEWHERE ELSE

*They are in `REVIEW_QUEUE.md` under R-052, listed honestly. **The X1 lesson is
that the finding will probably NOT be in this list**, so read it to know where
the builder already looked, not to be led there.*

1. `_instant` accepts `'2026-8-1'` — `strptime` does not demand two digits.
   **Measured: it is accepted. Never tested.**
2. Deduplication is `set()` on `(instant, name)` — two genuinely different
   events with the same name at the same minute **collapse and nothing counts
   or says so**, unlike a malformed entry, which IS counted.
3. `_label` prints the last TWO parts of a path, so two different `events.json`
   files in two different `data` directories print identically.
4. The whole block is one `try` — **a fault in the footer discards sixteen
   perfectly good events and prints the offline line.**
5. `SHOWN = 3` was chosen to match the news instrument and for no other reason.

## AND THE SHAPE THE ORDERS BEFORE THESE WOULD HAVE ASKED ABOUT

**THE HORIZON GUARDS THE LIST RUNNING OUT. NOTHING GUARDS A DATE CHANGING
INSIDE IT (R-051).** Eight of the sixteen dates are marked **TENTATIVE by the
Fed itself.** If one moves, the deck prints the old date, on the right weekday,
with a confident countdown, and **nothing anywhere says a word.** It is a
hardcoded list, so it cannot even be re-read. **Its author graded that SMALL and
the Commander has not ruled on it.**

## HOW PART 1 IS DONE — THE PATTERN ALREADY TOLD YOU, AND THESE ARE THE TEETH

1. **Write the bars for "this review clears" BEFORE running anything.**
2. **Invent at least one NEW sabotage.** Break it in a scratch copy **outside
   the repo**, and **run the untouched copy too — if the control does not pass,
   the rig is broken and nothing you conclude means anything.**
3. **FILL IN THE FINDING REPORT BEFORE REPAIRING ANYTHING.** `THE_PATTERN.md`
   carries it, the Commander's Three Questions first. **THE REPORT COMES BEFORE
   THE REPAIR, ALWAYS** — its whole purpose is to decide whether the repair is
   worth doing now, and a session that repairs first is asking him to approve
   something already done.
4. **"I ATTACKED IT HARD AND FOUND NOTHING" IS A SUCCESS. Say it plainly.**
   **DO NOT MANUFACTURE A DEFECT TO JUSTIFY A SESSION.**
5. `git status` clean afterwards. Record the verdict in `REVIEW_QUEUE.md`.

## R-049 IS LIVE WORK AGAIN AND IT IS NOT YOURS EITHER

The X1 repair in `news.py` changed how **all six fields of every story** are
read, it was written by the session that found the fault, and the checks that
say it works were written by that same session. **It went unverified because the
Commander bought a build with it, knowingly.** **It is no longer exempt.** If
the event calendar comes up clean quickly, this is the next place to look.

---

# **JOB 2 — ONLY IF PART 1 ALLOWS IT: THE WHALE WATCH, INSTRUMENT 5 OF 5**

**PART 2 IS CONDITIONAL AND THE COMMANDER DECIDES, NOT YOU:**

    SERIOUS ....... fix it, and stop. Build nothing.
    BORDERLINE .... do NOT fix it. Report and stop. He rules.
    SMALL ......... do NOT fix it. File it CATEGORY B and carry on to PART 2.

**WHAT THE PLAN ASKS FOR, VERBATIM:** *"WHALE WATCH (the Commander's requested
gap-closer): what the big money is doing, from FREE sources only — pick at build
time from: exchange netflow/large-transaction data (free tiers of blockchain
explorer APIs), Bitcoin exchange reserve trends, and the funding+open-interest
combination (crowd positioning) already collected in #2. Plain-words line on the
Brief. INFORMATION ONLY. True wallet-by-wallet whale tracking is
paid/unreliable; we show the honest free footprint, not a fake x-ray. **IF no
free source proves reliable at build time → the instrument reports "whale watch:
no honest free source available" rather than showing garbage** — and the
Commander decides if it's worth paying for."*

**THAT LAST SENTENCE IS AN INSTRUCTION, NOT A GET-OUT.** **PROBE THE SOURCES
FIRST AND WRITE THE NUMBERS DOWN BEFORE CHOOSING** — CryptoPanic was measured
dead, The Block measured 403, Blockworks measured 209 days stale, and **bls.gov
was measured 403 yesterday.** Four sources on this ship have been found broken
by measurement and none by assumption. **An honest "no free source is reliable"
is a real result and it is written into the plan as an acceptable one.**

**COPY THE MACHINERY, DO NOT REINVENT IT.** `cockpit/events.py` is the newest
and has the most complete guard on this ship — one doorway, everything
injectable, a gate holding its own expectations, **door 3 at the FILE
DESCRIPTOR plus a fresh-interpreter check**, and a permanent twelve-break drill.
`cockpit/news.py` is the model for anything that fetches.

**IF IT WILL NOT FIT, BUILD NOTHING AND SAY SO. A half-built part is worse than
no part, and that rule is not exempted and never will be.**

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after.

    **>>> AND THE CORRECTION THIS SESSION OWES THE ORDERS IT INHERITED (R-053).**
    The orders before these recorded that `funding.py` and `news.py` join
    **WITH** a trailing CRLF while `open_interest.py` joins with **NO** trailing
    separator, as though the files differed. **MEASURED 2026-08-07: BOTH JOINS
    ARE BYTE-FOR-BYTE RAW PREFIXES OF ALL FIVE INSTRUMENT FILES. THE FILES DO
    NOT DIFFER.** The "recipe" was only ever which variant each session picked.
    **A session that follows the old wording literally can see a mismatch and
    conclude the pilot's code changed when nothing did.**

    **SO: PICK ONE VARIANT, USE IT ON BOTH SIDES, AND VERIFY THE JOIN IS THE RAW
    PREFIX BEFORE PRINTING ANY HASH.** With the trailing CRLF, measured today:

        cockpit/fear_greed.py       __main__ line 113   bb31626c493a1ac6…
        cockpit/funding.py          __main__ line 160   95069d1bef8316d7…
        cockpit/news.py             __main__ line 272   503663762315b2f2…
        data/open_interest.py       __main__ line 243   c68508e881524cf0…
        data/collection_guard.py    __main__ line 156   d6518cd7208eb611…

    **DO NOT TRUST THOSE NUMBERS EITHER. RE-MEASURE THEM.** A remembered hash
    is exactly what this item is about. **A WHOLE-FILE HASH CANNOT DO THIS JOB:**
    it cannot tell "the pilot's code changed" from "the test around it changed".

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.** R-014 was exactly that; B14 was the same shape in a report.
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE. A repair nobody
    re-tested is a hope.**
(f) Everything the old gates did, they still do. **Run all EIGHT invocations and
    read their output before you change anything.**
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may not
    clear your own. **You MAY clear R-042 through R-053 — but check first
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
  3 stories. **All five answered on every reading on 2026-08-07, 82 stories.**
  **Below 3 of 5 is real and it is R-044.**
- **`cockpit\events.py --gate` HAS NO NETWORK AND NO CLOCK DEPENDENCE except in
  its live check (r), which reads the real file with the real clock.** It should
  take about five seconds. **If it is slow, something is wrong.**
- **ANY DRILL PRINTING `INERT` INSTEAD OF `CAUGHT` IS A FAIL.** That is
  deliberate. **If you see INERT, something real has drifted.**
- **S6, F10 AND B1 NO LONGER GO RED.** If any goes red it is a regression of a
  shipped repair and SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **THE RECORDER'S GATE TAKES ~55 s AND MUST BE RUN TWICE** — once normally and
  once with `TZ=UTC0`. **GATE 3.4 is run twice for the same reason.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** The laptop's own scheduled snapshot writes it while you work. **Commit
  it SEPARATELY, labelled as the laptop task's work — do not fold it into your
  change and do not revert it.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **THE 2026-08-05 EXEMPTION IS SPENT.** It covered one session. **You are not
   it.** See the top of this file.
2. **R-047 AND R-048 ARE SMALL.** Ruled 2026-08-05. **Filed, not fixed, not
   cleared.**
3. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS
   COMPLETE.** His words: *"we will build news section after when all the
   programme will be completed."* **He was told once, plainly, that this is the
   only deferral on the ship whose cost is permanent. He ruled. It waits. Do not
   re-argue it.**
4. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
5. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
6. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
7. **DOOR 3 IS BUILT IN BOTH COCKPIT INSTRUMENTS AND NOW IN THE EVENT CALENDAR
   TOO. R-025 IS CLEARED.** Residue R-033. **`news.py` is still the one without
   it (R-046).**
8. **F10, S6 AND B1 WERE ALL REPAIRED ON HIS RULING, AND ALL THREE HOLD.**
9. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
10. **NEWS IS INFORMATION AND CAN NEVER BECOME A SIGNAL, AND NEITHER CAN THE
    CALENDAR.** Phase 6's three slots are locked BY NAME — Turtle/Donchian,
    funding-rate fade, on-chain cycle thermometer.

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`cockpit/events.py`** — **your target.** ~1270 lines; the instrument is the
   first ~300 and the gate is the rest.
2. **`REVIEW_QUEUE.md`, the 2026-08-07 block** — R-050 to R-053, written by the
   builder against itself. **Read it to know where he already looked.**
3. **`EXECUTION_PLAN.md` PHASE 3, instrument 5** — that is your build, and the
   plan's own words are the specification.
4. **The LAST TWO entries of `PROGRESS_LOG.md`.** The file is ~640 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 34 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> AFTER ANY EDITOR EDIT, CHECK THE LINE ENDINGS AGAIN BEFORE COMMITTING.**
  An editing tool can hand back LF in a CRLF repo and nothing will say so. One
  command: count `\r\n` against bare `\n`. **This session converted after every
  single edit and lost nothing.**
- **>>> AND DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT
  HANDS BACK THE BLOB, WHICH IS LF, SO EVERY CRLF FILE ON THIS SHIP LOOKS
  LF-ONLY IN HEAD.** This session wrote that comparison, believed it for a
  minute, and nearly reported `README.md` and `SHIP_LAWS.md` as damaged when
  they have been LF-only all along. **Judge line endings in the WORKING TREE.
  Mojibake counts CAN be compared against HEAD — those come from decoded text.**
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1**.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Ten consecutive sessions have guarded this way.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** PowerShell eats the quotes and
  **bash eats every BACKTICK as a command substitution.** **Four commands lost
  across three generations. Two sessions running have obeyed it and lost none.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare your counts against `git show HEAD:<file>`;
  `PROGRESS_LOG.md` legitimately carries 3 mid-dots and 2 arrows inside
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

1. **>>> PART 1 HAS BEEN REDUCED FOUR TIMES RUNNING. A FIFTH IS THE MOMENT TO
   ASK HIM DIRECTLY WHETHER THE OUTSIDE CHECK STILL EXISTS.** Say the number.
2. **>>> A ONE-WORD DECISION THAT IS NEW TODAY: `data/events.json` SHIPS WITH
   ITS TIMEZONE SET TO `UTC`, AND HIS MACHINE RUNS UTC+5.** The file is his own
   and its zone line decides how anything HE adds is read. **UTC was chosen
   because it is never wrong-by-assumption and because guessing his zone from a
   measured clock offset is still a guess** — the file explains this in plain
   words and the Brief always prints the converted local time beside the event,
   so a mistake is visible rather than silent. **If he would rather write his own
   local times, one word changes `"timezone": "UTC"` to `"timezone":
   "Asia/Karachi"` and nothing else moves.** It does not affect FOMC or CPI,
   which carry their own zone.
3. **>>> R-049 IS STILL UNVERIFIED.** It was the price of his exemption and he
   was told before he ruled. **It is live work again for the first session that
   has room.**
4. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — still the only thing he
   personally owes the R-037 repair. The Task Scheduler event log is off, so a
   next time would leave no evidence either:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

5. **THE CATEGORY B PILE IS TWENTY-SIX DEEP.** **It has grown every single
   session since it was created and has never once shrunk.** Cleared before the
   ship is used for real, at the same moment `brief.py` gets its gate.
   **Somebody should keep saying the number out loud to him.**
6. **THE TWO NEW PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com. **All five answered on 2026-08-07, 82 stories.**
7. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED SEVEN TIMES:** *"A SABOTAGE
   MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."*
   **`cockpit/events.py` is the third file built with it from birth.** **A
   session may never promote its own idea to law. THIRTEEN OTHER CANDIDATES
   REMAIN UNADOPTED.**
8. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5). If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. Next run 10-Aug-2026 09:00.
9. **>>> NOBODY HAS EVER ASKED WHETHER A SOURCE ITSELF CAN LIE (R-035), AND THE
   EVENT CALENDAR IS A NEW ARGUMENT FOR IT (R-051).** Every gate proves the
   printed line matches what the source SENT; nothing asks whether the source was
   RIGHT. **The calendar is worse than the rest: it is a hardcoded list, so it
   cannot even be re-read.** **Still the strongest candidate for a whole
   session's attack.**
10. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
11. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **The one-line change that ends
    this class is `symbols=None`, resolved in the body.** It touches what the
    pilot reads, so no session may make it during a repair to a test.
    **`cockpit/events.py` was built with `path=None`, `now=None`,
    `recurring=None` and `horizons=None`, all resolved in the body — so the
    right pattern is now demonstrated on this ship rather than only described.**
12. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
13. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
14. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
15. **The settled-rate anchor (R-004)** — returned to him on correct facts.
16. **THE FUNDING, NEWS AND NOW EVENTS LINES ARE ALL ON THE BRIEF** and he was
    told. One word removes any of them.
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SEVEN TIMES, NOT ADOPTED.**
    **R-053 is a new argument for it: a remembered hash in the orders was an
    artifact for four generations and only came apart when somebody measured
    it.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**
