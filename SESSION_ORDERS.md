# ZAR X — **YOU HAVE AN EXEMPTION FROM PART 1. THE COMMANDER GRANTED IT HIMSELF, IN WORDS, AND IT IS THE SECOND ONE IN THIS SHIP'S HISTORY. YOU DO NOT ATTACK THE LAST SESSION'S REPAIR. YOU BUILD. AND THE EXEMPTION DIES WITH YOU.**

*Written 2026-08-18 (night) by the twenty-second generation, which attacked
`cockpit/whales.py`, found two breaks walking through a gate reporting
`100 checks, 0 red`, was ordered to correct it, and built GATE 3.5-R1 under a
bar it committed alone. **It is not the session you are building for. It is the
session whose work you have been excused from checking.***

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **NONE. YOU ARE EXEMPT.** Do not attack
                            GATE 3.5-R1. Do not "just have a quick look".
                            **Build.**
                   PART 2 — **BUILD `cockpit/carry.py`, THE CARRY MONITOR.**
                            Phase 4. The gate is already declared and
                            committed — you did not write it and you may not
                            reinterpret it.

## THE EXEMPTION, IN HIS OWN WORDS, 2026-08-18

> *"OK SO WRITE NEXT SESSION ORDER AND ITS THE ONY EXEMPTION FOR NEXT SESSION IT
> WILL NOT ATTACK YOUR FIX AND IT BUILDS THE NEXT SESSION AND IN NEXT SESSION
> ORDER AFTER BUILD IT WOULD BE SAME THAT NEXT SESSION WILL ATTACK THE BUILD AND
> SO ON"*

**THREE THINGS FOLLOW AND NONE OF THEM IS OPTIONAL:**

1. **It is YOURS ALONE and it covers ONE THING** — attacking GATE 3.5-R1.
2. **IT DIES WITH YOU.** *"and so on"* are his words. **The session after you
   attacks what YOU build, and you write that into their orders.** You may not
   pass your exemption on, and you may not grant one.
3. **IT DEFERS A DOUBT; IT DOES NOT RESOLVE ONE.** **R-066 stays OPEN and
   UN-ATTACKED** — one mind found R-060, graded it and repaired it, and nobody
   has checked any of the three. He was told that plainly before he ruled. **Say
   the words "still un-attacked" when you report to him, so it does not quietly
   become a thing everyone assumes was handled.**

---

# THE BRIEF, IN PLAIN WORDS

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~63 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~124 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  ~56 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red  ~58 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~7 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~6 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  ~0.6 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red  ~1.4 s
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red  ~7 s
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red  ~8 s
                                107 checks, SEVENTEEN sabotages, all CAUGHT
    vault INTACT 6 of 6 · Brief 3/3, FIVE Context Deck lines · lab/ untouched

**PHASE 3 IS COMPLETE — FIVE CONTEXT DECK INSTRUMENTS OF FIVE. PHASE 4 IS ONE
INSTRUMENT AND YOU ARE BUILDING IT.**

## What the last session did, in six lines

1. **ATTACKED `cockpit/whales.py`** and found **two breaks inside `_get`** — the
   four lines that are the only code on this ship that actually speaks to
   Binance — **each walking through `GATE 3.5 PASSED — 100 checks, 0 red`.**
2. **The Commander ruled: correct it.** The bar was declared and committed alone
   (`cacf355`, no `.py` in it), then built.
3. **THE REPAIR: the gate stands up an HTTP server of its own on `127.0.0.1`**
   and makes the REAL `_get` walk to it, judging **what it asked for** against
   tuples typed out in the gate, beside **what came back**. **>>> YOU ARE
   COPYING THIS. It is condition 9 of your gate.**
4. **CERTIFIED BY THE ATTACK, NOT THE DRILL** — the three original faults
   re-applied as real text edits: exit 1 with 4, 3 and 2 red.
5. **The Brief went 2/3 once** — a TwelveData read timeout on BTC — **and 3/3 on
   an immediate re-run.** A transient. The fail-safe named the dead asset.
6. **THE CATEGORY B PILE IS THIRTY-FIVE.** Nothing was cleared by anybody.

---

# **JOB 1 — BUILD `cockpit/carry.py`, THE CARRY MONITOR (PHASE 4)**

## WHAT IT IS, IN PLAIN WORDS, BECAUSE YOU WILL HAVE TO EXPLAIN IT TO HIM

There is a way to earn in crypto that needs no view on direction at all: hold
the coin, and at the same time hold an equal, opposite bet on the futures
market. The two cancel out, so the price can do what it likes. But every eight
hours the exchange makes one side of that futures bet pay the other. **The Carry
Monitor works out what that stream adds up to over a year and prints it.** It is
a readout. It never tells him to do it.

## >>> THE GATE IS ALREADY DECLARED. GO AND READ IT BEFORE YOU WRITE ANYTHING.

**`PROGRESS_LOG.md`, the entry of 2026-08-18 (night): GATE 4.1 — five design
decisions and fourteen conditions.** It was declared and committed **before this
instrument existed, by a session that will not build it**, exactly as GATE 3.5
was — and GATE 3.5 is the bar that held up best under attack, because not a word
of it could be bent to match what got built.

**YOU MAY NOT LOWER IT, REINTERPRET IT, OR DECIDE A CONDITION "DOES NOT APPLY".**
If you believe a condition is wrong, **say so to the Commander out loud and let
him rule** — never quietly.

**THE FOUR THINGS IN IT MOST LIKELY TO BE FUDGED, NAMED HERE SO THEY CANNOT BE:**

  * **D1 — A SINGLE FUNDING PRINT MAY NOT BE ANNUALISED.** One 8-hour reading of
    0.05% becomes **54% a year** on paper, and that number would be a lie
    sitting on his Brief. **Average the SETTLED rates over a stated window and
    NAME THE WINDOW ON THE LINE.**
  * **CONDITION 4 — THE SIGN IS PROVED AGAINST AN INDEPENDENT BINANCE SURFACE.**
    Positive funding means longs pay shorts; the carry is SHORT the perp, so
    positive funding **earns**. **Printing "pays 11%" when it costs 11% is the
    worst thing this instrument can do and no "a number appeared" check catches
    it.**
  * **CONDITION 9 — THE REAL TRANSPORT UNDER A CHECK FROM BIRTH.** Copy the
    door-server check out of `cockpit/whales.py`. **R-060 cost a whole session;
    this instrument does not get to repeat it.**
  * **CONDITION 11 — EVERY SABOTAGE PROVED TO CHANGE WHAT SOMEBODY READS.**
    **ANY BREAK REPORTED `INERT` IS A FAIL.** Two INERT verdicts were thrown
    away on 2026-08-18 and the session said so rather than counting them.

## WHAT YOU STILL OWE

1. **PROVE THE SHIP IS ALIVE FIRST.** All TEN invocations, output to a file, red
   counted BY MACHINE **three ways** — the tick character, the first word of a
   line, and the phrase "GATE ... FAILED" — **then READ any hit with your own
   eyes.** `collection_guard.py` prints `OK  `/`FAIL `, not ticks;
   `fear_greed.py` has FAILURE inside its own pass text; **the funding gate's
   prose contains the word "escaped" at the start of a line and it fooled the
   last session's counter within the hour.**
2. **NAME YOUR AWKWARD EDGE CASES IN `PROGRESS_LOG.md` BEFORE YOU WRITE CODE**,
   not after discovering them. GATE 4.1 names five; **find your own as well.**
3. **BUILD. Confine the change and PROVE the confinement two ways** — diff hunk
   line numbers, and a sha256 of each production half before and after.
4. **RUN THE GATE. Every check green, every sabotage CAUGHT.** A failing gate is
   never committed and never called "mostly passed".
5. **RUN THE BRIEF AND READ IT.** The new line must be on it, and the assets
   must still report. **If BTC goes offline again, say so — it did once today
   and recovered.**
6. **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.**
7. `git status` clean when you finish.

**YOU MAY CLOSE R-060** — you neither found it, graded it nor fixed it. **YOU MAY
NOT CLEAR R-066**, and under your exemption you are not even looking at it.

---

# **JOB 2 — ONLY IF JOB 1 IS FINISHED AND GREEN**

**A half-built instrument is worse than no instrument. If you run short, finish
Job 1 properly and leave Job 2 entirely.**

1. **R-049, AND SAY "FOURTH TIME" OUT LOUD.** The X1 repair in `cockpit/news.py`
   is self-marked — the session that found the fault wrote the fix and the
   checks that say the fix works — and it runs on every headline he sees every
   morning. The measurement that argues for leaving it: 136 real headlines, not
   one carrying markup. **Offer it; do not decide it.**
2. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** and each is an afternoon:
   how long Binance really goes between bucket updates (`MAX_AGE_MIN = 30`), and
   how far the BTC figure really moves between two calls seconds apart (the
   1.0-point live tolerance). **Retiring either is real progress.**
3. **THE CATEGORY B PILE IS THIRTY-FIVE.** Cleared before the ship is used for
   real, at the same moment `cockpit/brief.py` gets its gate. **Keep saying the
   number to him.**

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT ALREADY READS CHANGES except the few lines that put your
    new line on the Brief — prove it two ways, never assert it:** every diff
    hunk at or after the `__main__` line, AND a sha256 of the production half
    printed before and after.

    **THE RECIPE, RE-CONFIRMED 2026-08-18: sha256 of the prefix BEFORE the
    `__main__` line, WITHOUT the anchor line, no trailing separator.**

        cockpit/fear_greed.py       __main__ 112   bb31626c493a1ac6
        cockpit/funding.py          __main__ 159   95069d1bef8316d7
        cockpit/news.py             __main__ 272   503663762315b2f2
        data/collection_guard.py    __main__ 155   d6518cd7208eb611
        cockpit/events.py           __main__ 372   6fc5ce7d67aa8f24
        cockpit/whales.py           __main__ 363   d2cd1b58373d2fcb

    **The line numbers for `news`, `events` and `whales` are ONE HIGHER than the
    older record says — measured 2026-08-18; the hashes are identical, so only
    the counting of the anchor line differed. The measurement wins.**

    **AND `data/open_interest.py` CANNOT BE HASHED THIS WAY: the anchor appears
    TWICE in it.** Refuse, and prove it untouched with `git status`.

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN ALL TEN INVOCATIONS AND READ THEIR OUTPUT before you change anything.**
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may
    clear R-042 through R-065 — **check first whether you are the one who
    benefits.** **Not R-066.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. **Outside a settlement window a
  red funding gate is a REAL failure — and it will matter to you, because your
  instrument reads the same numbers.**
- **`cockpit\whales.py --gate` NOW BINDS A LOCAL PORT** as well as reading
  Binance live. If your machine refuses the port, those checks go red and it is
  the machine, not the code.
- **AN `INERT` W15/W16/W17 IN THE WHALE WATCH MEANS THE REAL FAULT IS ALREADY
  INSTALLED IN THE FILE.** That is the drill talking, not a false alarm.
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories.
- **S6, F10 AND B1 NO LONGER GO RED.** If any does, it is a regression and
  SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **THE BRIEF WENT 2/3 ONCE ON 2026-08-18** — TwelveData read timeout on BTC,
  Yahoo fallback `JSONDecodeError` — **and 3/3 on an immediate re-run.** If it
  happens more than once, item 11 on his desk is the first suspect.
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.** Still not
  in `.gitignore`. Leave it or ignore it deliberately.
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **YOUR EXEMPTION.** Ruled 2026-08-18, quoted above. **One session, one thing,
   and it dies with you.**
2. **R-060: HE RULED "CORRECT IT".** It is corrected. **Not your business this
   session.**
3. **R-054 IS SMALL** (2026-08-11). **R-047 AND R-048 ARE SMALL** (2026-08-05).
4. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
5. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
6. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
7. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`.
8. **DOOR 3 IS BUILT IN BOTH COCKPIT INSTRUMENTS, THE CALENDAR AND THE WHALE
   WATCH. R-025 IS CLEARED.** Residue R-033. **`news.py` is the one without it
   (R-046).**
9. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
10. **THE CONTEXT DECK AND THE CARRY MONITOR ARE INFORMATION AND CAN NEVER
    BECOME SIGNALS.** **Phase 6's three slots are locked BY NAME:
    Turtle/Donchian, funding-rate fade, on-chain cycle thermometer. The carry
    monitor is not one of them and never can be** — `EXECUTION_PLAN.md` says so
    and GATE 4.1 repeats it.

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`PROGRESS_LOG.md`, the entry of 2026-08-18 (night)** — **GATE 4.1, your
   bar.** Then the two before it, for the R-060 story you are inheriting.
   The file is ~750 KB; do not read it all.
2. **`EXECUTION_PLAN.md` line 271 — PHASE 4**, four lines, the source of the
   job. And the CURRENT POSITION MARKER at the top of that section.
3. **`cockpit/whales.py`** — **your template.** Read the production half
   (1–363) for the doorway shape, then the `(l2)` door-server section, which
   you are copying.
4. **`cockpit/funding.py`** — it already reads the very numbers you need, and
   its gate already proved the SIGN once. **Read how, then do it independently:
   Law 2 says your compartment owns its own source.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **CHECK ALL YOUR ANCHORS BEFORE WRITING A SINGLE BYTE**, refuse on any that
  matches other than exactly once, refuse if the patched file carries one bare
  newline, and refuse if a production hash moved. **That is the shape the last
  patch used; copy it.**
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
- **`.bat` FILES MUST BE CRLF.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** **And a newer bite: a long shell
  HERE-DOCUMENT carrying this ship's prose failed to parse on 2026-08-18. Write
  documents with an editor tool, not with `cat <<EOF`.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare the counts against `git show HEAD:<file>`;
  `PROGRESS_LOG.md` legitimately carries a few inside backticks and
  `SESSION_ORDERS.md` carries this very line.**
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH. `python …` ON ITS OWN DOES NOT WORK ON HIS MACHINE.** His
  PowerShell opens at `C:\WINDOWS\system32`. The working form is one line:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces a
  fresh one, `CHECK_STATUS.bat` shows the collection's health.

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL.

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... one OPEN item against your own build, plus anything
                            you could not certify. **R-066 stays open and you
                            do not touch it.**
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick the Carry Monitor; add what you MEASURED.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words brief.
                            **>>> AND THEIR JOB 1 IS: ATTACK WHAT YOU BUILT.
                            THE COMMANDER SAID "AND SO ON" AND THAT IS WHAT IT
                            MEANS. YOUR EXEMPTION IS NOT THEIRS. NEVER WRITE
                            ONE — only he grants one, in words.**
                            **AND TELL THEM R-066 IS STILL UN-ATTACKED.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his. **Show him the new
       Carry line and ask whether it reads as information rather than as a
       suggestion. That judgement is his, not yours.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> NEW, AND IT IS THE ONE TO PUT IN FRONT OF HIM WHEN YOU FINISH: DOES THE
   CARRY LINE READ AS INFORMATION, OR AS A SUGGESTION?** It prints a
   percent-a-year figure, which is the closest this ship has ever come to
   something that sounds like an opportunity. **The caveats are mandatory and
   verbatim, but whether the whole line still reads honestly to him is HIS
   judgement — Step 2.2 forbids a machine answering it by predicting him.**
2. **R-066 IS OPEN AND UN-ATTACKED**, by his own exemption. **Say so.**
3. **R-049 — offer it a FOURTH time.**
4. **THE CATEGORY B PILE IS THIRTY-FIVE.** Keep saying the number.
5. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR**, the only thing he personally
   owes the R-037 repair:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

6. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
7. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com.
8. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED ELEVEN TIMES:** *"A SABOTAGE
   MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."*
   Also unadopted: **"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT
   TURNS OVER"**, and **candidate Law 8 — "a claim about how something behaves
   is not a fact until it has been run"**.
9. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5).
10. **R-051 — nothing re-reads the Fed's and the BLS's pages automatically.**
    **R-024 doubt 2 — the hardcoded positive control.**
11. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2, and
    the first suspect if the Brief drops BTC again.
12. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
13. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE** — and it lives in
    `cockpit/funding.py`, which reads the same numbers your instrument does.
14. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py` is the
    worked example built the right way from birth — copy IT, not them.**
15. **The settled-rate anchor (R-004).**
16. **ALL FIVE CONTEXT DECK LINES ARE ON THE BRIEF** and he was told. One word
    removes any of them, and the same will be true of the Carry line.
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED NINE TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence — and it is certainly not waived by an exemption granted for one build
session.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**
