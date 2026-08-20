# ZAR X — **YOUR JOB 1 IS TO ATTACK `journal/log_trade.py`, WHICH THE LAST SESSION BUILT AND NOBODY ELSE HAS EVER LOOKED AT. THAT IS R-072. NO EXEMPTION EXISTS, NONE WAS HELD, AND I COULD NOT HAVE GRANTED YOU ONE.**

*Written 2026-08-20 (morning) by the twenty-fourth generation, which attacked
`cockpit/carry.py`, cleared R-067, and then built the trade logger under
GATE 5.1. **Only the Commander may grant an exemption, and only out loud.***

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **ATTACK `journal/log_trade.py`.** Invent a break
                            its author never imagined. This is R-072 and it is
                            the whole reason the rhythm exists.
                   PART 2 — **BUILD `journal/mirror.py`** (Phase 5, second
                            half) — **ONLY IF PART 1 PERMITS IT, AND ONLY
                            AFTER YOU HAVE DECLARED GATE 5.2 AND COMMITTED IT
                            ALONE, WITH NO CODE IN THAT COMMIT.**

**PART 2 IS CONDITIONAL AND THE COMMANDER DECIDES, NOT YOU.** If Part 1 finds
something, **fill in THE FINDING REPORT in `THE_PATTERN.md` BEFORE repairing
anything**, then: SERIOUS -> fix it and stop. BORDERLINE -> report and stop, he
rules. SMALL -> file it CATEGORY B and carry on to Part 2.

**"I ATTACKED IT HARD AND FOUND NOTHING" IS A SUCCESS. SAY IT PLAINLY AND CLEAR
R-072.** Do not manufacture a defect to justify a session — a stretched finding
costs him an instrument he actually wanted.

---

# THE BRIEF, IN PLAIN WORDS

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red   58 green
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red   71 green
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red   88 green
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red   88 green
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  (OK/FAIL)
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red   54 green
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red   69 green
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red   69 green
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red  107 green
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red  107 green
    cockpit/carry.py            GATE 4.1      PASSED  exit 0  0 red   87 green
      the same file at TZ=UTC0  GATE 4.1      PASSED  exit 0  0 red   87 green
    journal/log_trade.py        GATE 5.1      PASSED  exit 0  0 red   64 green
      the same file at TZ=UTC0  GATE 5.1      PASSED  exit 0  0 red   64 green
                                TWELVE sabotages, none INERT, tick sequences
                                identical BY MACHINE
    vault INTACT 6 of 6 · Brief 3/3 · lab/ untouched
    journal/my_trades.csv DOES NOT EXIST — his first real trade creates it

**PHASE 4 IS COMPLETE AND PHASE 5 IS HALF BUILT.**

## What the last session did, in seven lines

1. **Proved the ship alive first** — TWELVE invocations, 885 green, red counted
   by machine three ways. The three hits were the same prose traps as ever and
   were read by eye.
2. **Attacked `cockpit/carry.py` with five faults installed as TEXT EDITS** in
   copies outside the repo, control first. **Three were caught, and they were
   the three that could have made a figure wrong.** R-067 CLEARED.
3. **Two escaped, both in the GATE and not the instrument** — R-070 and R-071,
   both graded SMALL with the reasoning shown, both filed CATEGORY B.
4. **Declared its awkward edge cases in `PROGRESS_LOG.md` and committed them
   with NO CODE in that commit** (`git show --stat 277b34f` is the proof).
5. **Built `journal/log_trade.py` under GATE 5.1** — 64 checks, 0 red, twice.
6. **CERTIFIED BY ATTACK: three of six real faults escaped the FIRST version of
   its own gate.** The gate was hardened once per escape until all six failed.
7. **THE CATEGORY B PILE IS FORTY-TWO.** One item was cleared (R-067), by
   somebody who did not build what they cleared.

---

# **JOB 1 — ATTACK `journal/log_trade.py` (R-072)**

## WHAT THE INSTRUMENT IS FOR — Q1 OF THE FINDING REPORT, ANSWERED FOR YOU

**The rows in `journal/my_trades.csv` — the Commander's own record of trades he
has closed, in his own words.** It is not read on a screen each morning like
the Brief; **it is an ARCHIVE, and the Mirror will one day grade him on it.**
That makes a row that is wrong, missing or silently altered worse here than a
number that is merely stale, because nobody re-types a trade they logged in
March.

    logged: BTC-USD long 100.50 -> 111.00, size 0.25, feeling calm,
            at 2026-08-20T09:30:15+00:00

## >>> WHERE ITS AUTHOR SAYS HE DID NOT LOOK — A STARTING POINT, NOT A LIST TO TICK

**A builder cannot invent the attack he is blind to. These are R-072's five,
and the best attack is one that appears nowhere here:**

1. **>>> THE SEVEN INTERACTIVE QUESTIONS ARE TESTED BY NOBODY, AND THIS IS THE
   ONE I WOULD ATTACK FIRST.** D1 says a prompt is beyond a gate's reach and
   that is true — **every one of the 64 checks calls the doorway directly, so
   the ORDER of the seven `input()` calls is checked by nothing.** Swap two and
   his exit price goes into the size field forever, in his own archive, with
   the gate still printing 64/0. It was driven once by hand.
2. **`_needs_header` decides on `os.path.getsize`.** A journal whose header
   somebody deleted by hand, leaving the rows, never gets one back.
3. **A partial write.** The row is composed in memory so it reaches the disk in
   ONE `write` call — that is not an atomicity guarantee (R-073).
4. **The refusal messages echo his own text back with `!r`.** Never stored,
   never leaves his console, and not thought about hard.
5. **`_feeling` lower-cases and `_why` does not.** Deliberate and written down,
   but one mind's judgement about a file the Mirror does not yet exist to
   disagree with.

## WHAT PART 1 LOOKS LIKE

1. Write the bars for "this review clears" into notes **before running
   anything**, and name your candidate attacks there so you cannot claim
   afterwards to have planned one you stumbled into.
2. Invent at least one **NEW** sabotage. Break the code on purpose **in a
   scratch copy OUTSIDE the repo**. **Run the untouched copy too — if the
   control does not pass, the rig is broken and nothing you conclude means
   anything.** **PROVE EACH FAULT CHANGES WHAT SOMEBODY READS OR WHAT LANDS ON
   DISK before its verdict counts.**
3. Confirm `git status` is clean afterwards.
4. **Write it up either way**, and record the verdict in `REVIEW_QUEUE.md`.

**YOU MAY CLEAR R-072** — you did not build it. **YOU MAY NOT CLEAR R-070,
R-071, R-073, R-074 or R-075**; they were filed by the session that made them.
**AND R-066 IS STILL OPEN AND STILL UN-ATTACKED — NOW FOR THREE GENERATIONS.**
It is about `cockpit/whales.py`'s `_get` repair, and **any session that did not
build that repair may attack it.** Say the words "still un-attacked" to him.

---

# **JOB 2 — ONLY IF JOB 1 PERMITS: `journal/mirror.py` (PHASE 5, SECOND HALF)**

**A half-built Mirror is worse than no Mirror. If you run short, do Part 1
properly and leave Part 2 entirely.**

## >>> THE GATE DOES NOT EXIST YET. YOU DECLARE IT, AND YOU COMMIT IT ALONE.

GATE 4.1 and GATE 5.1 were both declared by a session that then stopped, and
**both are the bars that survived attack best, because not a word of either
could be bent to match what got built.** You do not have that luxury: nobody
has declared GATE 5.2. **So declare it in `PROGRESS_LOG.md`, commit it with NO
`.py` FILE IN THAT COMMIT, and only then write code** — `git show --stat` is
what proves the bar came first.

**WHAT THE PLAN ASKS OF THE MIRROR** (`EXECUTION_PLAN.md` Phase 5, item 2):
monthly, the Commander's logged trades vs what the system's instruments said at
those moments (from `journal/snapshots_*.csv`) vs what a disciplined 1%-risk
version of the same trades would have done. **Output: plain-words report. No
shaming, arithmetic only.**

**FOUR THINGS YOU WILL MEET ON YOUR FIRST AFTERNOON, NAMED SO THEY DO NOT
AMBUSH YOU:**

  * **>>> THE TWO FILES DISAGREE ABOUT WHAT A TIME LOOKS LIKE. THAT IS R-074
    AND IT IS YOURS.** `my_trades.csv` writes `2026-08-20T09:30:15+00:00`,
    because condition 12 of GATE 5.1 demanded the zone and I would not weaken
    it. **Every snapshot row since Phase 2 says `2026-07-21 11:35` with no zone
    at all.** Decide the reconciliation deliberately and write the decision
    down BEFORE coding; do not discover it in a join.
  * **THE ASSET NAMES WERE MADE TO MATCH ON PURPOSE.** `log_trade.py` stores
    `BTC-USD`, the same string every snapshot row uses, precisely so you do not
    need a translation table. **That was a Law 2 decision and the three names
    live in `log_trade.py`, not in `config.py`.**
  * **`journal/my_trades.csv` MAY NOT EXIST WHEN YOU ARRIVE**, and that is
    correct — it is created by his first real trade. **A Mirror that crashes on
    an empty journal is a Mirror that greets him with a traceback on the day he
    first tries it.** And **if it DOES exist, every row in it is real and yours
    to protect: read it, never write it.**
  * **NO GRADING AT ENTRY TIME REMAINS ABSOLUTE.** The logger never judges. The
    Mirror is the only thing on this ship allowed to, and **arithmetic only —
    no shaming, and never a signal.**

## WHAT YOU STILL OWE (both jobs)

1. **PROVE THE SHIP IS ALIVE FIRST.** All FOURTEEN invocations now — the twelve
   from before plus `journal/log_trade.py --gate` twice — output to a file,
   **red counted BY MACHINE three ways** (the tick character, the first word of
   a line, and the phrase "GATE ... FAILED"), **then READ any hit with your own
   eyes.** `collection_guard.py` prints `OK`/`FAIL`, not ticks; `fear_greed.py`
   and `funding.py` both carry **FAILURE** at the start of a line inside their
   own PASS text; **and the funding gate carries "escaped" at the start of a
   line — it has now fooled the counters of THREE consecutive sessions.**
2. **NAME YOUR AWKWARD EDGE CASES IN `PROGRESS_LOG.md` BEFORE YOU WRITE CODE**
   and commit them with no code in that commit.
3. **Confine the change and PROVE the confinement.** See the corrected recipe
   below, and **use `git` as the primary proof, not the hash.**
4. **RUN THE GATE. Every check green, every sabotage CAUGHT.** A failing gate is
   never committed and never called "mostly passed".
5. **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.**
6. `git status` clean when you finish.

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT ALREADY READS CHANGES** except what your orders call
    for — prove it two ways, never assert it.

    **>>> THE RECIPE IN THE PREVIOUS ORDERS WAS WRONG FOR SIX OF THE SEVEN
    FILES IN ITS OWN TABLE, AND IT COST THIS SESSION HALF AN HOUR. MEASURED
    AND CORRECTED 2026-08-20.** Every variant was tried against all seven:
    **CRLF, WITH a trailing separator, excluding the anchor line, matches 6 of
    7**; the previously written recipe (no trailing separator) matches only
    `cockpit/carry.py`; every LF variant matches nothing. **Both columns are
    given so you can tell which recipe a number came from:**

        file                     __main__  WITH trailing CRLF  WITHOUT
        cockpit/fear_greed.py      113     bb31626c493a1ac6    d09fba1dde6d9517
        cockpit/funding.py         160     95069d1bef8316d7    2dab48ecb0d00927
        cockpit/news.py            272     503663762315b2f2    6f4f69f4377e4158
        data/collection_guard.py   156     d6518cd7208eb611    c0f41d6044225baf
        cockpit/events.py          372     6fc5ce7d67aa8f24    481f97bdf59980f3
        cockpit/whales.py          363     d2cd1b58373d2fcb    7a7926f5badb7f3d
        cockpit/carry.py           416     540e057ad7a2cd40    ec5455596007b590
        journal/log_trade.py       287     7d9252b099d38df9    652378043e01b8e4

    **AND `data/open_interest.py` STILL CANNOT BE HASHED THIS WAY: the anchor
    appears TWICE in it.** Refuse, and prove it untouched with `git status`.

    **>>> THE PROOF THAT NEEDS NO RECIPE AND CANNOT DRIFT, AND THE ONE THE
    CONFINEMENT SHOULD ACTUALLY STAND ON:** compare each file's working-tree
    bytes against `git show HEAD:<file>` **with CRLF normalised to LF on both
    sides**, and separately assert the WORKING TREE has zero bare LF. That
    answers "did the content change" and "are the line endings right" as two
    different questions, and neither depends on anybody's recipe. **A hash
    whose recipe nobody can reproduce is a number, not a proof.**

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.** A drill
    that measures every break on one channel scores the byte-identical ones
    INERT and then deletes the only check that catches them.
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **>>> CERTIFY BY ATTACK, NOT BY THE DRILL. THIS EARNED ITSELF TWICE IN ONE
    MORNING.** A drill only ever proves a gate can catch a monkeypatch. Install
    the real fault as a TEXT EDIT in a copy outside the repo, run the untouched
    control FIRST, and report both. **Three of six real faults walked through
    GATE 5.1's first version while it reported 61 checks and 0 red — and the
    production half was CORRECT in all three cases. The gate could not see the
    difference, which is the same thing as not having the check.**
(h) **>>> TELL YOUR GATE HOW MANY CHECKS IT OWES.** `journal/log_trade.py` is
    the only gate on this ship that does. See R-070 and the desk.
(i) **A FAILING GATE MUST STILL BE ABLE TO FINISH REPORTING.** GATE 5.1 died on
    a traceback in a DETAIL line under attack A1 and never printed the reds
    that came after it. Guard your detail lines.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **>>> `cockpit/carry.py --gate` CAN GO RED THROUGH NO FAULT OF THE FILE IF YOU
  RUN IT WITHIN SECONDS OF A FUNDING SETTLEMENT (00:00, 08:00, 16:00 UTC).**
  That is R-069 and it was deliberate: check (m) demands agreement to the digit
  with no tolerance. **Re-run it once, away from the settlement, before
  concluding anything.**
- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021) —
  the same three times. Outside a settlement window a red funding gate is REAL.
- **`cockpit\whales.py --gate` AND `cockpit\carry.py --gate` BOTH BIND A LOCAL
  PORT.** If your machine refuses the port, those checks go red and it is the
  machine, not the code. **`journal/log_trade.py --gate` binds no port and
  touches no network at all.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories.
- **S6, F10 AND B1 NO LONGER GO RED.** If any does, it is a regression and
  SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **>>> GATE TIMINGS ON RECORD ARE WEATHER REPORTS, NOT CHECKS.**
  `cockpit/carry.py --gate` is recorded at ~35 s and took **4 seconds** today
  with its live check present and green. **This is the fourth time a timing on
  record has turned out to be one unrepresentative reading. Never conclude a
  check was skipped because a gate was fast — read its output.**
- **>>> `journal/my_trades.csv` DOES NOT EXIST AND THAT IS CORRECT.** Do not
  create it. **If it exists when you arrive, the Commander has logged a real
  trade and every row in it is his: read it, never write it, and NEVER drive
  `python journal\log_trade.py` by hand against the real journal — that is how
  this session put a fake row in it and had to delete the file.** Drive it in a
  copy outside the repo.
- **THE BRIEF WENT 2/3 TWICE (2026-08-19 and once before).** It was **3/3**
  today and the drop did not reproduce. **KEEP THE WHOLE OUTPUT OF YOUR FIRST
  BRIEF RUN, not the tail**, and capture which asset drops if it happens.
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.**
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **THE EXEMPTION IS SPENT AND IT STAYED SPENT.** The last session held none,
   asked for none, and attacked what its predecessor built. **You do the same,
   and you write the same into the orders you leave. NEVER WRITE ONE — only he
   grants one, in words.**
2. **R-060: HE RULED "CORRECT IT".** It is corrected. **R-066 against that
   repair is still open and still un-attacked, for the third generation.**
3. **R-054 IS SMALL** (2026-08-11). **R-047 AND R-048 ARE SMALL** (2026-08-05).
4. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
5. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
6. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
7. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`.
8. **DOOR 3 IS BUILT IN THE CALENDAR, THE WHALE WATCH, THE CARRY MONITOR AND
   NOW THE TRADE LOGGER. R-025 IS CLEARED.** Residue R-033. **`news.py` is the
   one without it (R-046).**
9. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
10. **THE CONTEXT DECK AND THE CARRY MONITOR ARE INFORMATION AND CAN NEVER
    BECOME SIGNALS.** **Phase 6's three slots are locked BY NAME:
    Turtle/Donchian, funding-rate fade, on-chain cycle thermometer.**

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None
of it is repeated here.**

1. **`PROGRESS_LOG.md`, the three entries of 2026-08-20** — the attack on
   `cockpit/carry.py`, the edge cases declared before any code, and the build.
   The file is ~800 KB; do not read it all.
2. **`journal/log_trade.py`** — **what you are attacking.** Production half
   lines 1-286, gate from 287.
3. **`REVIEW_QUEUE.md`, R-070 to R-075** — including R-072's five doubts.
4. **`EXECUTION_PLAN.md` PHASE 5** and the CURRENT POSITION MARKER.
5. **`PROGRESS_LOG.md` 2026-08-19 (morning, second part) — GATE 5.1** — read it
   to see what a bar declared by a non-builder looks like, because **you are
   writing GATE 5.2 yourself and nobody is checking it before you build.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` or `chr(10)` for a newline.
- **>>> AN ANCHOR MUST NEVER SPLIT A CRLF PAIR**, and must match exactly once.
  **Write your writer to REFUSE on both, and to refuse a result carrying a bare
  LF.** The one used on 2026-08-20 did all three and is worth rebuilding.
- **>>> A FILE WRITTEN BY AN EDITOR TOOL ARRIVES AS LF ON THIS MACHINE.**
  `journal/log_trade.py` was created with 1,021 bare LF and had to be converted
  before it matched every other file in the repo. **Check the endings of
  anything you create, before you commit it.**
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
  **Comparing CONTENT against the blob, with both sides normalised, is fine and
  is the best confinement proof there is.**
- **`.bat` FILES MUST BE CRLF, AND KEEP THEM ASCII-ONLY.** `run_daily.bat`
  already carries `???` where an em-dash used to be.
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING**, and write documents with an editor
  tool or a binary appender, not with `cat <<EOF`.
- **>>> SET `PYTHONUTF8=1` ON YOUR OWN HARNESS TOO, NOT ONLY ON THE GATE.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** —
  `â€`, `Â·`, `â†`, `Ã`, `âœ`. **Compare the counts against
  `git show HEAD:<file>` so a fingerprint that was ALREADY there is not
  blamed on you, and one you ADDED cannot hide behind one that was.**
  Ignore hits inside backticks — including the five on this very line, which
  are deliberate quotations of the damage and will show as +1 each.
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH.** His PowerShell opens at `C:\WINDOWS\system32`:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces
  a fresh one, `CHECK_STATUS.bat` shows the collection's health, and
  **`LOG_TRADE.bat` — NEW — asks him the seven questions and logs a trade.**

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL.

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... your verdict on R-072, plus one OPEN item against
                            your own work. **R-066 stays open until somebody
                            actually attacks it.**
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; add what you MEASURED.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words brief.
                            **>>> AND THEIR JOB 1 IS: ATTACK WHAT YOU BUILT.
                            YOU MAY NOT GRANT AN EXEMPTION.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> DOES THE CARRY LINE READ AS INFORMATION, OR AS A SUGGESTION?** He was
   shown it on 2026-08-19 and asked directly, and **he has still not answered.
   ASK AGAIN.** It prints a percent-a-year figure, the closest this ship has
   come to something that sounds like an opportunity, and **Step 2.2 forbids a
   machine answering that question by predicting him.**
2. **>>> AND ONE THING TO PUT BESIDE THAT QUESTION, NOTICED 2026-08-20.** The
   figure is the funding yield on the PERP NOTIONAL. Running the trade needs
   money on BOTH legs at once — spot in full, plus margin on the perp — so
   **the return on the capital he would actually deploy is lower than the
   number on the line, and how much lower depends on how much margin he
   posts.** The footer says "capital tied up on BOTH legs at once" and does not
   quantify it. **This is not a defect and the arithmetic is right for what the
   line names — it is a question about whether the line means to him what it
   means. His call, not a session's.**
3. **R-072 — nobody but its author has looked at `journal/log_trade.py`.** That
   is the next session's Job 1.
4. **R-066 IS OPEN AND UN-ATTACKED**, now for THREE generations. **Say so.**
5. **>>> R-070: NO GATE ON THIS SHIP KNOWS HOW MANY CHECKS IT SHOULD RUN.**
   Proved 2026-08-20 by deleting five checks from GATE 4.1 and watching it
   print `PASSED — 82 checks, 0 red` while its own banner claimed all twenty-one
   sabotages had run. **`journal/log_trade.py` shipped with the repair; the
   other seven gates have not. It is one line each.** Graded SMALL by the form
   with the qualifier shown — **he may overrule that reading; it is his form.**
6. **R-049 — offer it a SIXTH time.** The X1 repair in `cockpit/news.py` is
   self-marked and runs on every headline he sees. The measurement that argues
   for leaving it: 136 real headlines, not one carrying markup.
7. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** — how long Binance really
   goes between bucket updates (`MAX_AGE_MIN = 30` in the whale watch), and how
   far the BTC figure really moves between two calls seconds apart.
8. **THE CATEGORY B PILE IS FORTY-TWO.** Cleared before the ship is used for
   real, at the same moment `cockpit/brief.py` gets its gate. **Keep saying the
   number.**
9. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR**, the only thing he personally
   owes the R-037 repair:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

10. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
    RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
11. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
    Bitcoin.com.
12. **THE RULES HE HAS NOT YET ADOPTED**, each now earned many times over: *"A
    SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS
    ANYTHING"*; *"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT TURNS
    OVER"*; **candidate Law 8 — "a claim about how something behaves is not a
    fact until it has been run"**; and **NEW, EARNED 2026-08-20 — "A GATE MUST
    BE TOLD HOW MANY CHECKS IT OWES."**
13. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
    **The Brief has dropped an asset twice; it was 3/3 on 2026-08-20 and the
    drop did not reproduce.**
14. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, and the
    Mirror is about to need it: the plan asks it to compare his trades against
    "a disciplined 1%-risk version of the same trades."**
15. **`MAX_PLAUSIBLE_RATE` in `cockpit/funding.py`** — measured 13-16x looser
    than Binance's published cap. **Recommendation: tighten to ~0.01. STILL NOT
    DONE.** `cockpit/carry.py` shipped with exactly that bound.
16. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py`,
    `cockpit/carry.py` and `journal/log_trade.py` are the worked examples built
    the right way from birth.**
17. **The settled-rate anchor (R-004).**
18. **ALL FIVE CONTEXT DECK LINES AND THE CARRY LINE ARE ON THE BRIEF.** One
    word removes any of them. **The trade logger is NOT on the Brief and never
    will be — it is a command he runs, not a line he reads.**
19. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED ELEVEN TIMES, NOT ADOPTED.**
    **And it just earned itself again from a new direction: the prefix-hash
    recipe in the last orders was wrong for six of the seven files in its own
    table, and nothing anywhere would ever have noticed.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**
