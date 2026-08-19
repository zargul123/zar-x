# ZAR X — **YOUR JOB 1 IS TO ATTACK `cockpit/carry.py`, WHICH THE LAST SESSION BUILT AND NOBODY ELSE HAS EVER LOOKED AT. THE EXEMPTION THAT EXCUSED THAT SESSION FROM ITS OWN PART 1 IS SPENT. IT WAS ONE SESSION, ONE THING, AND IT DIED WITH THEM — *"AND SO ON"* ARE THE COMMANDER'S OWN WORDS.**

*Written 2026-08-19 (morning) by the twenty-third generation, which held the
Commander's second exemption ever, built the Carry Monitor under GATE 4.1, and
**may not grant you one — only he can, and only out loud.***

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **ATTACK `cockpit/carry.py`.** Invent a break its
                            author never imagined. This is R-067 and it is
                            the whole reason the rhythm exists.
                   PART 2 — **BUILD `journal/log_trade.py`** (Phase 5, first
                            half) — **ONLY IF PART 1 permits it.** The gate is
                            already declared and committed; you did not write
                            it and you may not reinterpret it.

**PART 2 IS CONDITIONAL AND THE COMMANDER DECIDES, NOT YOU.** If Part 1 finds
something, **fill in THE FINDING REPORT in `THE_PATTERN.md` BEFORE repairing
anything**, then: SERIOUS -> fix it and stop. BORDERLINE -> report and stop, he
rules. SMALL -> file it CATEGORY B and carry on to Part 2.

**"I ATTACKED IT HARD AND FOUND NOTHING" IS A SUCCESS. SAY IT PLAINLY AND CLEAR
R-067.** Do not manufacture a defect to justify a session — a stretched finding
costs him an instrument he actually wanted.

---

# THE BRIEF, IN PLAIN WORDS

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red   ~68 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~122 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red   ~51 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red   ~50 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red    ~5 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red    ~4 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red   ~0.4 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red   ~0.2 s
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red    ~7 s
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red    ~7 s
    cockpit/carry.py            GATE 4.1      PASSED  exit 0  0 red   ~35 s
      the same file at TZ=UTC0  GATE 4.1      PASSED  exit 0  0 red   ~35 s
                                87 checks, TWENTY-ONE sabotages, none INERT
    vault INTACT 6 of 6 · Brief 3/3 · lab/ untouched

**PHASE 4 IS COMPLETE. THE BRIEF NOW CARRIES FIVE CONTEXT DECK INSTRUMENTS AND,
BELOW THEM, THE CARRY MONITOR.**

## What the last session did, in six lines

1. **Proved the ship alive first** — ten invocations, red counted by machine
   three ways. The one hit was the funding gate's own PROSE, read by eye.
2. **MEASURED before deciding anything**, and one measurement killed an
   assumption: **Binance's settlement gaps are NOT exactly 8 hours** (seven
   distinct values, ±5 ms), so the obvious `gap == 8h` check would have shipped
   a dead instrument with a green gate.
3. **Got something wrong and wrote it down first:** it measured the funding
   endpoint with `startTime=0`, briefly believed deep history was gone, and had
   to be corrected by the ROADMAP. **`startTime=0` means UNSET.**
4. **Built `cockpit/carry.py` under GATE 4.1** — 87 checks, 0 red, twice, tick
   sequences identical, 21 sabotages all CAUGHT and none INERT.
5. **CERTIFIED BY ATTACK, NOT BY THE DRILL:** five real faults as text edits in
   a copy outside the repo, all five turn the gate red, control passes.
6. **THE CATEGORY B PILE IS THIRTY-SEVEN.** Nothing was cleared by anybody.

---

# **JOB 1 — ATTACK `cockpit/carry.py` (R-067)**

## WHAT THE INSTRUMENT IS FOR — Q1 OF THE FINDING REPORT, ANSWERED FOR YOU

**The Carry line on the Morning Brief.** Three figures — one per coin — saying
what a delta-neutral carry (long the spot coin, SHORT the perpetual future)
would pay or cost per year, averaged over the last 21 settled fundings.

    Carry (7d)   : Binance USDT-perps · 3 of 3 assets · window ends 00:00 UTC
      BTC         — +5.95%/yr (earns)
      ETH         — +4.54%/yr (earns)
      SOL         — -0.11%/yr (costs)

## >>> WHERE ITS AUTHOR SAYS HE DID NOT LOOK — A STARTING POINT, NOT A LIST TO TICK

**A builder cannot invent the attack he is blind to. These are R-067's five, and
the best attack is one that appears nowhere here:**

1. **`_window` is the whole instrument and it has one author.** Its refusals run
   in an order that author chose: duplicates, then count, then slice, then
   spacing. A window that is BOTH short AND gapped reports only the first fault.
   **Is any of that ordering wrong in a way that hides something?**
2. **The 60,000 ms spacing tolerance is a judgement** defended by one morning's
   measurement of 500 settlements.
3. **`MAX_AGE_MIN = 600` was REASONED, NOT MEASURED.** 480 minutes is the normal
   worst case and two hours of slack was added by argument alone.
4. **Check (j) reads `SYMBOLS` out of the module** when asking Binance about the
   funding interval. That is R-014's shape.
5. **A renamed field.** `_rate` names a MISSING `fundingRate`, but a venue that
   began sending `fundingRateV2` beside a stale `fundingRate` would be read
   silently and would look perfectly correct.

## WHAT PART 1 LOOKS LIKE

1. Write the bars for "this review clears" into notes **before running
   anything**.
2. Invent at least one **NEW** sabotage. Break the code on purpose **in a
   scratch copy OUTSIDE the repo**. **Run the untouched copy too — if the
   control does not pass, the rig is broken and nothing you conclude means
   anything.**
3. Confirm `git status` is clean afterwards.
4. **Write it up either way**, and record the verdict in `REVIEW_QUEUE.md`.

**YOU MAY CLEAR R-067** — you did not build it. **YOU MAY NOT CLEAR R-068 or
R-069** if you are the one who benefits from them staying shut. **AND R-066 IS
STILL OPEN AND STILL UN-ATTACKED** — two generations have now passed. It is
about `cockpit/whales.py`'s `_get` repair, and **any session that did not build
that repair may attack it.** Say the words "still un-attacked" to him.

---

# **JOB 2 — ONLY IF JOB 1 PERMITS: BUILD `journal/log_trade.py` (PHASE 5)**

**A half-built instrument is worse than no instrument. If you run short, do
Part 1 properly and leave Part 2 entirely.**

## >>> THE GATE IS ALREADY DECLARED. GO AND READ IT BEFORE YOU WRITE ANYTHING.

**`PROGRESS_LOG.md`, the entry of 2026-08-19 (morning, second part): GATE 5.1 —
five design decisions and twelve conditions**, declared and committed before the
file existed, by a session that will not build it. **You may not lower it,
reinterpret it, or decide a condition "does not apply".** If you believe one is
wrong, **say so to the Commander out loud and let him rule** — never quietly.

**THE THREE THINGS IN IT MOST LIKELY TO BE FUDGED, NAMED SO THEY CANNOT BE:**

  * **D3 — DUPLICATES ARE LEGITIMATE HERE.** Every other recorder on this ship
    dedups. **A pilot can genuinely make the same trade twice.** Swallowing the
    second one erases a real trade and the Mirror then grades him on a lie.
    **This is the one place where the ship's own habit is the wrong instinct.**
  * **D4 — A COMMA IN HIS OWN WORDS MUST NOT BE ABLE TO DESTROY A ROW.** Use the
    `csv` module, never string-joining, and prove a hostile WHY line comes back
    byte-identical.
  * **D2 — APPEND-ONLY, NEVER REWRITES HISTORY.** B13 deleted 34 rows and
    printed a report that was entirely true about what was left.

## WHAT YOU STILL OWE (both jobs)

1. **PROVE THE SHIP IS ALIVE FIRST.** All TWELVE invocations now — the ten from
   before plus `cockpit/carry.py --gate` twice — output to a file, **red counted
   BY MACHINE three ways** (the tick character, the first word of a line, and
   the phrase "GATE ... FAILED"), **then READ any hit with your own eyes.**
   `collection_guard.py` prints `OK`/`FAIL`, not ticks; `fear_greed.py` has
   FAILURE inside its own pass text; **and the funding gate's prose carries
   "escaped" at the start of a line — it has now fooled the counters of two
   consecutive sessions.**
2. **NAME YOUR AWKWARD EDGE CASES IN `PROGRESS_LOG.md` BEFORE YOU WRITE CODE.**
3. **Confine the change and PROVE the confinement two ways** — diff hunk line
   numbers, and a sha256 of each production half before and after.
4. **RUN THE GATE. Every check green, every sabotage CAUGHT.** A failing gate is
   never committed and never called "mostly passed".
5. **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.**
6. `git status` clean when you finish.

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT ALREADY READS CHANGES** except the few lines that put
    your new line on the Brief — prove it two ways, never assert it. **THE
    RECIPE: sha256 of the prefix BEFORE the `__main__` line, WITHOUT the anchor
    line, no trailing separator.**

        cockpit/fear_greed.py       __main__ 112   bb31626c493a1ac6
        cockpit/funding.py          __main__ 159   95069d1bef8316d7
        cockpit/news.py             __main__ 272   503663762315b2f2
        data/collection_guard.py    __main__ 155   d6518cd7208eb611
        cockpit/events.py           __main__ 372   6fc5ce7d67aa8f24
        cockpit/whales.py           __main__ 363   d2cd1b58373d2fcb
        cockpit/carry.py            __main__ 416   ec5455596007b590   <- NEW

    **AND `data/open_interest.py` CANNOT BE HASHED THIS WAY: the anchor appears
    TWICE in it.** Refuse, and prove it untouched with `git status`.

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **CERTIFY BY ATTACK, NOT BY THE DRILL.** A drill only ever proves a gate can
    catch a monkeypatch. Install the real fault as a TEXT EDIT in a copy outside
    the repo, run the untouched control FIRST, and report both.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **>>> `cockpit/carry.py --gate` CAN GO RED THROUGH NO FAULT OF THE FILE IF YOU
  RUN IT WITHIN SECONDS OF A FUNDING SETTLEMENT (00:00, 08:00, 16:00 UTC).**
  That is R-069, and it was a deliberate choice: check (m) demands the module's
  figure and the gate's own figure agree **to the digit with no tolerance**,
  because settled rates are historical facts. If a settlement lands between the
  two fetches the windows differ by one row of twenty-one. **Re-run it once,
  away from the settlement, before concluding anything.**
- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021) —
  the same three times. Outside a settlement window a red funding gate is REAL.
- **`cockpit\whales.py --gate` AND `cockpit\carry.py --gate` BOTH BIND A LOCAL
  PORT** as well as reading Binance live. If your machine refuses the port,
  those checks go red and it is the machine, not the code.
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories.
- **S6, F10 AND B1 NO LONGER GO RED.** If any does, it is a regression and
  SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **>>> THE BRIEF WENT 2/3 FOR THE SECOND TIME on 2026-08-19**, on the first run
  after wiring, and 3/3 on the two runs after it. **It is NOT the Carry
  Monitor** — those four lines run after the asset count is computed. **It is
  now twice, and item 11 on his desk (the TwelveData key rotation) is the first
  suspect. The last session did not capture which asset dropped: KEEP THE WHOLE
  OUTPUT OF YOUR FIRST BRIEF RUN, not the tail.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.**
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **THE EXEMPTION IS SPENT.** It was one session, one thing. **You attack what
   the last session built, and you write the same into the orders you leave.**
   **NEVER WRITE ONE — only he grants one, in words.**
2. **R-060: HE RULED "CORRECT IT".** It is corrected. **R-066 against that
   repair is still open and still un-attacked.**
3. **R-054 IS SMALL** (2026-08-11). **R-047 AND R-048 ARE SMALL** (2026-08-05).
4. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
5. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
6. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
7. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`.
8. **DOOR 3 IS BUILT IN THE CALENDAR, THE WHALE WATCH AND THE CARRY MONITOR.
   R-025 IS CLEARED.** Residue R-033. **`news.py` is the one without it (R-046).**
9. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
10. **THE CONTEXT DECK AND THE CARRY MONITOR ARE INFORMATION AND CAN NEVER
    BECOME SIGNALS.** **Phase 6's three slots are locked BY NAME:
    Turtle/Donchian, funding-rate fade, on-chain cycle thermometer.**

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`PROGRESS_LOG.md`, the entries of 2026-08-19** — the measurements, the
   build, and **GATE 5.1, your bar**. The file is ~760 KB; do not read it all.
2. **`cockpit/carry.py`** — **what you are attacking.** Production half lines
   1-415, gate from 416.
3. **`REVIEW_QUEUE.md`, R-067 to R-069** — the author's own doubts about it.
4. **`EXECUTION_PLAN.md` PHASE 5** and the CURRENT POSITION MARKER.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> AN ANCHOR MUST NEVER SPLIT A CRLF PAIR.** The last session's document
  inserter refused a write because its anchor ended at the `\r`, which would
  have left a bare newline in `EXECUTION_PLAN.md`. **The refusal worked; write
  yours to refuse too.**
- **CHECK ALL YOUR ANCHORS BEFORE WRITING A SINGLE BYTE**, refuse on any that
  matches other than exactly once, and refuse if a production hash moved.
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
- **`.bat` FILES MUST BE CRLF.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** It bit the last session too. Name the value first, or use
  `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING**, and write documents with an editor
  tool, not with `cat <<EOF`.
- **>>> SET `PYTHONUTF8=1` ON YOUR OWN HARNESS TOO, NOT ONLY ON THE GATE.** The
  last session's attack harness died on the tick character mid-verdict, in a
  `cp1252` console, after two of six results were in.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. Compare counts against `git show HEAD:<file>`.
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH.** His PowerShell opens at `C:\WINDOWS\system32`:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces a
  fresh one, `CHECK_STATUS.bat` shows the collection's health.

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL.

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... your verdict on R-067, plus one OPEN item against
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
   shown it on 2026-08-19 and asked directly. **If he has not answered, ask
   again** — it prints a percent-a-year figure, the closest this ship has come
   to something that sounds like an opportunity, and **Step 2.2 forbids a
   machine answering that question by predicting him.**
2. **R-067 — nobody but its author has looked at `cockpit/carry.py`.** That is
   YOUR Job 1.
3. **R-066 IS OPEN AND UN-ATTACKED**, now for two generations. **Say so.**
4. **R-049 — offer it a FIFTH time.** The X1 repair in `cockpit/news.py` is
   self-marked and runs on every headline he sees. The measurement that argues
   for leaving it: 136 real headlines, not one carrying markup.
5. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** — how long Binance really
   goes between bucket updates (`MAX_AGE_MIN = 30` in the whale watch), and how
   far the BTC figure really moves between two calls seconds apart.
6. **THE CATEGORY B PILE IS THIRTY-SEVEN.** Cleared before the ship is used for
   real, at the same moment `cockpit/brief.py` gets its gate. **Keep saying the
   number.**
7. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR**, the only thing he personally
   owes the R-037 repair:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

8. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
9. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com.
10. **THE RULES HE HAS NOT YET ADOPTED**, each now earned many times over: *"A
    SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS
    ANYTHING"*; *"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT TURNS
    OVER"*; and **candidate Law 8 — "a claim about how something behaves is not
    a fact until it has been run"**, which the `startTime=0` blunder of
    2026-08-19 has now earned from the other direction: **a measurement is only
    a fact when the measurement itself is sound.**
11. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2, and
    **the Brief has now dropped an asset twice.**
12. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
13. **`MAX_PLAUSIBLE_RATE` in `cockpit/funding.py`** — measured 13-16x looser
    than Binance's published cap. **Recommendation: tighten to ~0.01. STILL NOT
    DONE.** `cockpit/carry.py` shipped with exactly that bound, measured against
    the venue's own caps, so there is now a worked example in the repo.
14. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py` and
    `cockpit/carry.py` are the worked examples built the right way from birth.**
15. **The settled-rate anchor (R-004).**
16. **ALL FIVE CONTEXT DECK LINES AND NOW THE CARRY LINE ARE ON THE BRIEF.** One
    word removes any of them.
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED TEN TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence — and certainly not by an exemption granted for one build session.**
**Information instruments can carry the lighter guard. The gauntlet cannot, at
any weight.**
