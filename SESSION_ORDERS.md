# ZAR X — **THE LAST SESSION SHIPPED NO CODE, SO YOU HAVE NOTHING OF ITS BUILDING TO ATTACK. YOUR JOB 1 IS INSTEAD TO RE-GRADE ITS FINDING WITH YOUR OWN EYES, BECAUSE IT GRADED ITSELF AND FILED THAT AGAINST ITSELF AS R-065.**

*Written 2026-08-18 by the twenty-second generation, which built nothing,
repaired nothing, attacked `cockpit/whales.py` under orders it did not write,
and found two sabotages walking through a gate reporting `100 checks, 0 red`.*

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — RE-GRADE R-060 INDEPENDENTLY. The last session
                            found it AND recommended its severity, which is
                            the conflict THE_PATTERN warns about. **Reproduce
                            it yourself before you believe a word of it.**
                   PART 2 — CONDITIONAL, AND IT DEPENDS ENTIRELY ON WHAT THE
                            COMMANDER RULED ON R-060. See JOB 2. **If he has
                            not ruled, ASK HIM AND DO NOT GUESS.**

**NOTHING WAS REPAIRED AND NOTHING WAS BUILT ON 2026-08-18.** The finding graded
BORDERLINE, and THE_PATTERN is explicit: *"BORDERLINE — do NOT fix it. Report and
stop. The Commander rules."* **That is the only reason the ship stood still.**

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~63 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~124 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  ~56 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red  ~58 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~7 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~6 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  ~0.6 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red  ~1.4 s
    cockpit/whales.py           GATE 3.5      PASSED  exit 0  0 red  ~8 s
      the same file at TZ=UTC0  GATE 3.5      PASSED  exit 0  0 red  ~7 s
                                100 checks, 14 sabotages, all CAUGHT
    vault INTACT 6 of 6 · Brief 3/3, FIVE Context Deck lines · lab/ untouched

**PHASE 3'S CONTEXT DECK IS COMPLETE — FIVE INSTRUMENTS OF FIVE. THERE IS NO
SIXTH INSTRUMENT AND THE PLAN DOES NOT HAVE ONE.**

## What the last session did, in six lines

1. **ATTACKED `cockpit/whales.py`** — copied the whole repo outside the repo,
   passed the untouched control FIRST, and invented five sabotages that were
   not on the author's list of fourteen.
2. **TWO OF THEM WALKED THROUGH A GREEN GATE.** Both live in `_get`, the
   four-line function that is the only code on this ship that actually speaks
   to Binance. **X15** made ETH and SOL print BTC's numbers; **X16** made
   "all accounts" print the top-account figure for every coin. Both times:
   **`GATE 3.5 PASSED — 100 checks, 0 red`.**
3. **THE REASON IS STRUCTURAL, NOT CARELESS.** Almost every check injects a
   fake transport, so `_get` never runs. Even the recording transport — which
   is excellent, and which caught the control sabotage instantly — **replaces**
   `_get` and so can never testify about it.
4. **TWO SABOTAGES WERE INERT AND ITS VERDICTS WERE THROWN AWAY.** Said plainly:
   X17 and X25 could not be proved to change anything.
5. **FOUR SMALLER THINGS were measured and filed CATEGORY B** (R-061 to R-064),
   including **R-058's doubt 2 settled against its author** — the no-shorts case
   really can misreport.
6. **THE CATEGORY B PILE IS THIRTY-FIVE.**

---

# **JOB 1 — RE-GRADE R-060 WITH YOUR OWN EYES. DO NOT INHERIT ITS GRADE.**

**WHY THIS IS YOUR JOB.** The last session found the fault and then decided how
serious it was. **That is the conflict of interest THE_PATTERN names**, and it
filed it against itself as **R-065 doubt 2**. One answer is carrying the whole
grade, and it is **Step 2.2 — would the Commander see it with his own eyes?**
That session answered **YES**, on the ground that three coins showing
byte-identical numbers is wrong on its face to a stranger. **If you answer NO,
R-060 becomes SERIOUS and must be fixed before anything else happens.**

## HOW TO DO IT

1. **REPRODUCE IT BEFORE YOU BELIEVE IT.** Copy the repo outside the repo. Run
   the untouched control FIRST (Step 0.1) — GATE 3.5, exit 0, 0 red, 100 checks.
   Then make this one byte-level edit to `cockpit/whales.py` in the copy and
   run the gate again:

       in `_get`, before the `requests.get` line, insert
           params = dict(params, symbol="BTCUSDT")

   **Expected: the live block shows all three coins carrying identical numbers,
   and the gate still prints `100 checks, 0 red`.** If it does not reproduce,
   **that is your finding** and R-060 was wrong.
2. **THEN LOOK AT THE BROKEN BLOCK AS A STRANGER WOULD** and answer Step 2.2
   yourself, in writing, in `REVIEW_QUEUE.md`, before you read the last
   session's answer again.
3. **INVENT A SUBTLER ONE.** The two on record are deliberate-looking, which is
   the weakest part of the finding (Step 2.1). **A fault inside `_get` that
   looks like an ordinary maintenance slip — a retry, a shared session object, a
   reused params dict, a proxy, a rate-limit backoff — would settle the argument
   one way or the other.** R-056 already points at rate-limiting, so this is not
   hypothetical.
4. **MEASURE THE TWO THINGS NOBODY HAS MEASURED (R-058 doubts 3 and 4),** if you
   have room. Both are numbers somebody chose: how long Binance really goes
   between bucket updates (`MAX_AGE_MIN = 30`), and how far the BTC figure
   really moves between two calls seconds apart (the live tolerance of 1.0
   point). **Sampling either is an afternoon's work and would retire a doubt
   that has been carried unexamined.**

## THE REPAIR THAT IS ALREADY WRITTEN DOWN AND DELIBERATELY NOT APPLIED

**Only if the Commander rules SERIOUS, or rules that it be fixed.** A check that
runs the REAL `_get` against a server the gate controls: a `http.server` on
`127.0.0.1`, started by the gate, which **records the path and query string it
was asked for** and answers with bytes the gate typed out itself. That exercises
the actual transport end to end, **makes no Binance request at all**, and would
have caught both X15 and X16 on the first run. **It belongs entirely inside
`__main__`; not one byte of the production half needs to change** — and if you
build it, prove that two ways as rule (a) below requires.

**AND DECLARE THE GATE BEFORE YOU WRITE IT. Commit the bar ALONE, with no `.py`
in that commit.**

---

# **JOB 2 — CONDITIONAL. THERE IS NO INSTRUMENT LEFT TO BUILD.**

**Do not go looking for a sixth Context Deck instrument. The plan does not have
one, and a session that invents work is a session that has stopped reading its
orders.**

1. **R-049, AND SAY "FOURTH TIME" OUT LOUD WHEN YOU RAISE IT.** The X1 repair in
   `cockpit/news.py` is self-marked — the session that found the fault wrote the
   fix and wrote the checks that say the fix works — it changed how all six
   fields of every story are read, and it runs on every headline he sees every
   morning. **The last session was told to offer it a third time and did not
   reach it.** The measurement that argues for leaving it: 136 real headlines,
   not one carrying markup. **Offer it to him; do not decide it.**
2. **`cockpit/brief.py` STILL HAS NO GATE.** He ruled: not now, before going
   live. **That is the same moment the whole Category B pile is cleared, and the
   pile is THIRTY-FIVE.** Keep saying the number.
3. **R-057's REAL QUESTION IS STILL UNTOUCHED:** how many other checks on this
   ship count only the markers their author happened to think of? **The last
   session added evidence pointing the other way — its own counter INVENTED a
   red out of the word "escaped" in a sentence.**

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after.

    **THE RECIPE, RE-CONFIRMED 2026-08-11: the hashes come from the prefix
    WITHOUT the anchor line.** On untouched files:

        cockpit/fear_greed.py       __main__ 112   bb31626c493a1ac6
        cockpit/funding.py          __main__ 159   95069d1bef8316d7
        cockpit/news.py             __main__ 271   503663762315b2f2
        data/collection_guard.py    __main__ 155   d6518cd7208eb611
        cockpit/events.py           __main__ 371   6fc5ce7d67aa8f24
        cockpit/whales.py           __main__ 362   d2cd1b58373d2fcb

    **AND `data/open_interest.py` CANNOT BE HASHED THIS WAY AT ALL: the anchor
    string appears TWICE in it** — once as the real line, once quoted inside its
    own gate at line 1918. **Refuse, and prove that file untouched with
    `git status` instead.**

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.** The last
    session threw away two of its own verdicts under this rule and said so.
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN ALL TEN INVOCATIONS AND READ THEIR OUTPUT before you change anything.**
    **AND COUNT RED THREE WAYS** — the tick character, the first word of a line,
    and the phrase "GATE ... FAILED" — **then READ any hit with your own eyes
    before you believe it.** `collection_guard.py` prints `OK  `/`FAIL `, not
    ticks; `fear_greed.py` has the word FAILURE inside its own pass text; and
    the funding gate's prose contains the word "escaped" at the start of a line,
    which fooled the last session's counter within the hour.
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may
    clear R-042 through R-065 — **but check first whether you are the one who
    benefits from clearing them.** **You may NOT clear R-065; it is the last
    session's item against itself, and its second doubt is your Job 1.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. **Outside a settlement window a
  red funding gate is a REAL failure — treat it as one.**
- **`cockpit\whales.py --gate` READS BINANCE LIVE in its last two sections and
  makes at least SEVEN requests.** Its live bar is **at least 3 of 6 readings,
  at least one per asset**, and a BTC figure within 1.0 point of the gate's own
  fetch. **A genuine Binance outage turns it red and that is correct.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories. Below 3 of 5 is real and it is
  R-044.
- **ANY DRILL PRINTING `INERT` INSTEAD OF `CAUGHT` IS A FAIL.**
- **S6, F10 AND B1 NO LONGER GO RED.** If any goes red it is a regression of a
  shipped repair and SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **THE RECORDER'S GATE AND GATE 3.4 AND GATE 3.5 ARE EACH RUN TWICE** — once
  normally and once with `TZ=UTC0`.
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** The laptop's scheduled snapshot writes it while you work. **Commit it
  SEPARATELY, labelled as the laptop task's work.**
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.** Still not
  in `.gitignore`. **Leave it or ignore it deliberately; do not sweep it into a
  commit without deciding.** The last session left it alone.
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** On
  2026-08-18 the repo was two commits ahead of `origin` before this session
  began — `0917472 oi: weekly open-interest rows recorded by the laptop task`,
  126 rows across the three assets, plus a merge. **That is the task working, not
  a problem. Pull, and push whatever it left behind.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **R-054 IS SMALL.** Ruled 2026-08-11 (evening). CATEGORY B.
2. **R-047 AND R-048 ARE SMALL.** Ruled 2026-08-05.
3. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
   His words. **It waits.**
4. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
5. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
6. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything — Job 1 turns on
   that exact question.**
7. **DOOR 3 IS BUILT IN BOTH COCKPIT INSTRUMENTS, THE EVENT CALENDAR AND THE
   WHALE WATCH. R-025 IS CLEARED.** Residue R-033. **`news.py` is still the one
   without it (R-046).**
8. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
9. **NEWS, THE CALENDAR AND THE WHALE WATCH ARE INFORMATION AND CAN NEVER
   BECOME SIGNALS.** Phase 6's three slots are locked BY NAME: Turtle/Donchian,
   funding-rate fade, on-chain cycle thermometer.

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`PROGRESS_LOG.md`, the LAST TWO entries** — the whale watch's build, and
   the 2026-08-18 attack on it with its FINDING REPORT in full. The file is
   ~700 KB; do not read it all.
2. **`REVIEW_QUEUE.md`, the 2026-08-18 block** — R-058's verdict, R-060 to
   R-065.
3. **`cockpit/whales.py`, lines 1–362** — the production half, and `_get` in
   particular. **Law 7: a human reading the code is the only defence the Lab's
   own numbers cannot provide, and R-060 is exactly a case of numbers not
   providing it.**
4. **`ROADMAP.md`, the 2026-08-18 measured facts.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo (39 MB).
  `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> AFTER ANY EDITOR EDIT, CHECK THE LINE ENDINGS AGAIN BEFORE COMMITTING.**
  Count `\r\n` against bare `\n`. **The last session's patch rig refused to run
  unless the patched file carried zero bare newlines, and that is the pattern to
  copy.**
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
- **`.bat` FILES MUST BE CRLF.**
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Thirteen consecutive sessions have guarded this way.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** **And note the newer bite: a long
  shell HERE-DOCUMENT carrying this ship's prose failed to parse on 2026-08-18.
  Write documents with an editor tool, not with `cat <<EOF`.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`.
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
    2. REVIEW_QUEUE.md .... your independent verdict on R-060, plus one OPEN
                            item against whatever you did yourself. **You may
                            not clear R-065.**
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; correct any MEASURED fact that
                            moved.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words brief.
                            **>>> AND THEIR JOB 1 IS: ATTACK WHATEVER YOU BUILT
                            OR REPAIRED. If you shipped no code, say so plainly
                            and give them the next real job instead — but never
                            write an exemption. Only the Commander grants one,
                            in words. HE ASKED FOR THIS RULE HIMSELF ON
                            2026-08-11.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> NEW AND FIRST: R-060. DOES HE WANT `_get` PUT UNDER A CHECK?** In his
   words: *the four lines that actually phone Binance are the one part of the
   whale watch that no test ever runs, and somebody editing them could put the
   wrong coin's numbers on your Brief every morning while every gate on the ship
   says "perfect".* Nothing is wrong today. **Graded BORDERLINE, and the grade
   was written by the session that found it — which is why the next session
   re-grades it.** The repair is small, lives entirely in the test half, and
   makes no Binance request.
2. **>>> STILL HIS BECAUSE A MACHINE MAY NOT ANSWER IT: DOES THE WHALE WATCH
   LINE READ HONESTLY TO HIM?** It is on his Brief now. The label says "Whale
   watch"; the words under it say NOT exchange flows, NOT wallet tracking, NOT
   the world's whales. **Show him the line. One word changes the label if he
   wants it changed.** (R-058 doubt 6, untouched.)
3. **>>> R-049 IS DEFERRED THREE TIMES. Offer it again and say "fourth time".**
4. **THE CATEGORY B PILE IS THIRTY-FIVE** — five added 2026-08-18, none cleared.
   **Keep saying the number out loud to him.**
5. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — still the only thing he
   personally owes the R-037 repair:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

6. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes it to `"Asia/Karachi"`. It does not affect
   FOMC or CPI, which carry their own zone.
7. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com.
8. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED TEN TIMES:** *"A SABOTAGE MUST
   BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."* **It
   earned its keep again on 2026-08-18**, when it made a session throw away two
   of its own escapes. Also still unadopted: **"EVERY THRESHOLD IS TESTED AT THE
   EXACT VALUE WHERE IT TURNS OVER"**, and **candidate Law 8 — "a claim about
   how something behaves is not a fact until it has been run"**, which earned
   itself again when `_newest`'s docstring was measured to be false about its
   own tie-breaking.
9. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5). It ran
   again and committed 126 rows before 2026-08-18.
10. **R-051 — nothing re-reads the Fed's and the BLS's pages automatically.**
11. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.**
12. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py` was built
    the right way from birth** — every default is `None`, resolved in the body —
    **and the 2026-08-18 attack confirmed that design holds under hostile
    input.** It touches what the pilot reads, so no session may make the change
    during a repair to a test.
13. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
14. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
15. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
16. **The settled-rate anchor (R-004).**
17. **ALL FIVE CONTEXT DECK LINES ARE ON THE BRIEF** and he was told. One word
    removes any of them.
18. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED NINE TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**
