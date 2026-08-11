# ZAR X — **YOUR JOB 1 IS TO ATTACK THE WHALE WATCH. THE COMMANDER ASKED FOR THAT SENTENCE HIMSELF. THE EXEMPTION THE LAST SESSION HAD DIED WITH IT AND YOU DO NOT HAVE ONE.**

*Written 2026-08-11 (night) by the twenty-first generation, which built
`cockpit/whales.py` under a gate it did not write, passed it 100/100 twice, got
caught by its own gate telling a lie about floating-point arithmetic, and filed
three doubts against itself.*

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **ATTACK `cockpit/whales.py`. IT IS BRAND NEW,
                            NOBODY BUT ITS AUTHOR HAS EVER LOOKED AT IT, AND
                            ITS AUTHOR WROTE ALL 100 OF ITS CHECKS.**
                            This is R-058 and it is your whole first job.
                   PART 2 — **ONLY IF PART 1 LEAVES ROOM, AND IT IS NOT A
                            BUILD.** Phase 3's five instruments are DONE.
                            What is left is on the Commander's desk, not in
                            the compiler. See JOB 2.

**THE COMMANDER'S OWN WORDS, 2026-08-11, WHICH IS WHY JOB 1 IS WHAT IT IS:**

> *"in next session when he write session orders and well after others too every
> time new session has to attack the build of previous session."*

**HE EXEMPTED EXACTLY ONE SESSION FROM PART 1 AND SAID SO IN WORDS. THAT
EXEMPTION IS SPENT.** You do not have one, you may not grant yourself one, and
you may not grant one to the session after you. **Only he can, and he says so in
words when he does.**

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The Commander is not a programmer and asked for it in this form. Write your
report to him the same way.*

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~63 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~122 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  ~50 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red  ~48 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~0.7 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~5 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  ~0.3 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red  ~0.3 s
    cockpit/whales.py           GATE 3.5      PASSED  exit 0  0 red  ~7 s
      the same file at TZ=UTC0  GATE 3.5      PASSED  exit 0  0 red  ~7 s
                                100 checks, 14 sabotages, all CAUGHT
    vault INTACT 6 of 6 · Brief 3/3, FIVE Context Deck lines · lab/ untouched

**PHASE 3'S CONTEXT DECK IS COMPLETE — FIVE INSTRUMENTS OF FIVE.**

## What the last session did, in six lines

1. **BUILT THE WHALE WATCH**, instrument 5 of 5, under a gate declared by
   somebody else. Two Binance endpoints side by side for BTC/ETH/SOL: its
   largest accounts by position size, beside every account on the venue.
2. **THE HONEST GAP IS ON THE BRIEF, NOT IN A DOCSTRING.** Exchange reserve and
   netflow data is PAID, so the line says **NOT exchange flows, NOT wallet
   tracking, NOT the world's whales**, every morning, in his sight.
3. **ITS OWN GATE CAUGHT IT LYING.** A claim about floating-point rounding went
   red on the first run — 1 red of 100 — **because it had been written as a
   check rather than as a sentence.** Corrected by enumerating all 10,001
   possible values: 501 really do disagree, and the one in the claim was not
   one of them.
4. **THE SHIP-ALIVE COUNTER HAD A HOLE** and it was filed against itself as
   R-057: it counted tick marks, and one gate does not print tick marks.
5. **NOTHING WAS CLEARED, ON PURPOSE.** The only item in reach was R-056, and
   the session that adopted the source is the wrong session to certify it.
6. **THE CATEGORY B PILE IS THIRTY.**

---

# **JOB 1 — ATTACK `cockpit/whales.py`. THIS IS LAYER 3 AND IT IS THE ONLY PART OF THIS SHIP A BUILDER CAN NEVER DO FOR THEMSELVES.**

**WHAT YOU ARE ATTACKING:** a 1,460-line file, built yesterday, whose gate
reports 100 green and 14 sabotages CAUGHT. **Every one of those checks and every
one of those sabotages was written by the person who wrote the code being
checked.** GATE 3.4 also reported 69 green — and on 2026-08-11 a fresh session
found three sabotages walking straight through it in a morning.

## HOW TO DO IT — the method that has worked every time

1. **WRITE YOUR BARS DOWN BEFORE YOU RUN ANYTHING.** What would make you say
   "this file is sound"? Put it in a scratch file first, so you cannot move it
   afterwards.
2. **COPY THE WHOLE REPO OUTSIDE THE REPO** (34 MB, costs nothing) and break
   things THERE. `git status` clean when you finish.
3. **RUN THE UNTOUCHED CONTROL FIRST.** If the healthy copy does not pass, your
   rig is broken and nothing you conclude means anything. **That is Step 0.1 and
   it has caught a false finding before.**
4. **INVENT SABOTAGES ITS AUTHOR DID NOT.** The fourteen it already carries are
   listed in the 2026-08-11 (night) PROGRESS_LOG entry. **The useful one is the
   fifteenth.** X1's lesson: the real finding is usually NOT on the builder's
   own list.
5. **PROVE EVERY BREAK CHANGES WHAT SOMEBODY READS** before its verdict counts.
   An INERT break proves nothing.
6. **FILL IN THE FINDING REPORT BEFORE REPAIRING ANYTHING.** The Commander's
   Three Questions come first, and they can end it on their own. **THE REPORT
   COMES BEFORE THE REPAIR, ALWAYS.**

## WHERE ITS AUTHOR THINKS IT IS WEAKEST — **AND THEREFORE PROBABLY NOT WHERE THE FINDING IS**

Read R-058 in `REVIEW_QUEUE.md` for all six in full. In short:

  * **The ratio cross-check is SKIPPED when the short share is exactly zero.**
    The author believes the sum check makes that safe. "Believes" is why it is
    filed.
  * **`MAX_AGE_MIN = 30` is a number the author chose**, not one anybody
    measured. So is the live check's 1.0-point tolerance.
  * **The gate makes seven or more live Binance requests per run.**
  * **THE WORDING IS A JUDGEMENT ABOUT A READER AND A MACHINE MAY NOT MAKE
    ONE.** Whether "Whale watch" plus a footer really stops the line reading as
    "all the whales in the world" is **the Commander's to say, not yours.**
    Show him the line and ask.

## THINGS WORTH TRYING THAT ITS AUTHOR DID NOT

    · what happens when Binance answers 200 with a row from THE FUTURE?
      the staleness guard only looks one way (now - stamp > limit)
    · two rows with the SAME timestamp and different numbers
    · a row where longShortRatio is negative, or enormous
    · what the block does if `symbols` has an asset Binance does not list
    · run the gate twice in the same second — does anything cache?
    · does anything in it write to disk, or leave a temp directory behind?
    · read `section_text` and ask: can any input make it print instead of
      return? Door 3 only proves it did not, on the paths that were tried.

## WHAT YOU STILL OWE, WHATEVER YOU FIND

1. **PROVE THE SHIP IS ALIVE FIRST.** All TEN invocations now (whales joins the
   list, twice), output to a file, red ticks counted BY MACHINE. **AND READ
   R-057 BEFORE YOU WRITE THAT COUNTER:** `data/collection_guard.py` prints
   `OK  ` and `FAIL `, not `✓` and `✗`, and `fear_greed.py` has the word
   FAILURE inside its own pass text. **Count three ways: the tick character,
   the first word of a line, and the phrase "GATE ... FAILED".**
2. **"I ATTACKED IT HARD AND FOUND NOTHING" IS A SUCCESS.** Say it plainly and
   clear R-058. **DO NOT MANUFACTURE A DEFECT TO JUSTIFY A SESSION.**
3. **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.**
4. `git status` clean when you finish.

---

# **JOB 2 — ONLY IF PART 1 LEAVES ROOM. THERE IS NO INSTRUMENT LEFT TO BUILD.**

**PHASE 3'S FIVE INSTRUMENTS ARE ALL BUILT AND ALL GREEN.** Do not go looking
for a sixth — **the plan does not have one, and a session that invents work is a
session that has stopped reading its orders.**

What is actually left is, in order of who owns it:

1. **R-049, AND SAY "THIRD TIME" OUT LOUD WHEN YOU RAISE IT.** The X1 repair in
   `cockpit/news.py` is self-marked — the session that found the fault wrote the
   fix and wrote the checks that say the fix works — it changed how all six
   fields of every story are read, and it runs on every headline he sees every
   morning. **It has now been passed over three times, and the deck he was
   finishing is finished.** The measurement that argues for leaving it: 136 real
   headlines, not one carrying markup. **Offer it to him; do not decide it.**
2. **`cockpit/brief.py` STILL HAS NO GATE.** He ruled: not now, before going
   live. **That is the same moment the whole Category B pile is cleared, and
   the pile is THIRTY.** Keep saying the number.
3. **R-057's REAL QUESTION IS UNTOUCHED:** how many other checks on this ship
   count only the markers their author happened to think of?

**IF PART 1 FINDS SOMETHING SERIOUS, DO JOB 1 AND STOP. A half-built anything is
worse than nothing, and that rule has never been exempted.**

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after.

    **>>> TWO CORRECTIONS TO THE RECIPE, MEASURED 2026-08-11 (night). THE
    MEASUREMENT WINS.** The orders you would otherwise have inherited say the
    recorded hashes were taken *"with the trailing CRLF"*. **THEY WERE NOT.**
    They come from the prefix **WITHOUT** the anchor line. Re-measured that way,
    on untouched files:

        cockpit/fear_greed.py       __main__ 112   bb31626c493a1ac6  matches record
        cockpit/funding.py          __main__ 159   95069d1bef8316d7  matches record
        cockpit/news.py             __main__ 271   503663762315b2f2  matches record
        data/collection_guard.py    __main__ 155   d6518cd7208eb611  matches record
        cockpit/events.py           __main__ 371   6fc5ce7d67aa8f24  first measurement
        cockpit/whales.py           __main__ 362   d2cd1b58373d2fcb  first measurement

    **AND `data/open_interest.py` CANNOT BE HASHED THIS WAY AT ALL: the anchor
    string appears TWICE in it** — once as the real line, once quoted inside its
    own gate at line 1918. A script that splits on the first hit gives a number
    that means nothing. **Refuse, as the eleven-session anchor rule says, and
    prove that file untouched with `git status` instead.**

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
    clear R-042 through R-059 — **but check first whether you are the one who
    benefits from clearing them.** R-058 is the one you are here to settle, and
    you may only settle it if you did not write the file.

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
  The bar is 3 of 5 publishers and 3 stories. **All five answered on 2026-08-11,
  84 stories. Below 3 of 5 is real and it is R-044.**
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
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.** The
  weekly open-interest task created it on 10-Aug-2026. It is still not in
  `.gitignore`. **Leave it or ignore it deliberately; do not sweep it into a
  commit without deciding.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **R-054 IS SMALL.** Ruled 2026-08-11 (evening). CATEGORY B: recorded,
   unrepaired, uncleared, cleared with the rest of the pile before the ship is
   used for real. **Do not re-argue it and do not repair GATE 3.4 as a favour.**
2. **R-047 AND R-048 ARE SMALL.** Ruled 2026-08-05.
3. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
   His words. He was told once, plainly, that this is the only deferral on the
   ship whose cost is permanent. **It waits.**
4. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
5. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
6. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
7. **DOOR 3 IS BUILT IN BOTH COCKPIT INSTRUMENTS, THE EVENT CALENDAR AND NOW
   THE WHALE WATCH. R-025 IS CLEARED.** Residue R-033. **`news.py` is still the
   one without it (R-046).**
8. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
9. **NEWS, THE CALENDAR AND THE WHALE WATCH ARE INFORMATION AND CAN NEVER
   BECOME SIGNALS.** Phase 6's three slots are locked BY NAME: Turtle/Donchian,
   funding-rate fade, on-chain cycle thermometer.

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`PROGRESS_LOG.md`, the LAST TWO entries** — the edge cases and fourteen
   breaks named before the code, and the build itself. The file is ~700 KB; do
   not read it all.
2. **`REVIEW_QUEUE.md`, the 2026-08-11 (night) block** — R-057, R-058, R-059.
3. **`cockpit/whales.py`** — the thing you are attacking. Read the production
   half (lines 1–362) properly before you break anything; **Law 7 says a human
   reading the code is the only defence the Lab's own numbers cannot provide.**
4. **`ROADMAP.md`, the 2026-08-11 measured facts** — the source numbers.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo. `git status`
  clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> AFTER ANY EDITOR EDIT, CHECK THE LINE ENDINGS AGAIN BEFORE COMMITTING.**
  An editing tool can hand back LF in a CRLF repo and nothing will say so. One
  command: count `\r\n` against bare `\n`.
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1**.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Twelve consecutive sessions have guarded this way, and on 2026-08-11 it
  earned its keep on `data/open_interest.py`.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** PowerShell eats the quotes and bash
  eats every BACKTICK.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare against `git show HEAD:<file>`;
  `PROGRESS_LOG.md` legitimately carries a few inside backticks.**
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
    2. REVIEW_QUEUE.md .... your verdict on R-058 (you may clear it ONLY if you
                            did not build the file), plus one OPEN item against
                            whatever you did yourself.
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

1. **>>> NEW, AND IT IS HIS BECAUSE A MACHINE MAY NOT ANSWER IT: DOES THE WHALE
   WATCH LINE READ HONESTLY TO HIM?** It is on his Brief now. The label says
   "Whale watch"; the words under it say NOT exchange flows, NOT wallet
   tracking, NOT the world's whales. **GATE 3.5 condition 4 says the wording
   fails if the line could be read as "all the whales in the world" — and Step
   2.2 says a session may not answer that by predicting him.** Show him the
   line. **One word changes the label if he wants it changed.**
2. **>>> R-049 IS DEFERRED THREE TIMES AND THE DECK IS NOW FINISHED.** The
   reason he set it aside — so the deck could be completed — no longer applies.
   **Offer it again and say "third time" out loud.**
3. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — still the only thing he
   personally owes the R-037 repair. The Task Scheduler event log is off, so a
   next time would leave no evidence either:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

4. **THE CATEGORY B PILE IS THIRTY** — three added this session, none cleared.
   Cleared before the ship is used for real, at the same moment `brief.py` gets
   its gate. **Keep saying the number out loud to him.**
5. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes `"timezone": "UTC"` to `"timezone":
   "Asia/Karachi"`. It does not affect FOMC or CPI, which carry their own zone.
6. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com. **All five answered on 2026-08-11, 84 stories.**
7. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED NINE TIMES:** *"A SABOTAGE MUST
   BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."* **A
   session may never promote its own idea to law.** Fourteen other candidates
   remain unadopted, including **"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE
   WHERE IT TURNS OVER"** (R-054 paid for it, and GATE 3.5 obeyed it) and
   **candidate Law 8 — "a claim about how something behaves is not a fact until
   it has been run"** — which was earned AGAIN on 2026-08-11 when a session
   asserted something false about floating-point arithmetic in three places at
   once and only the copy written as a CHECK ever went red.
8. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5). If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. **It ran on 10-Aug-2026 and pushed.**
9. **R-051 — nothing re-reads the Fed's and the BLS's pages automatically.** A
   later session could have the calendar do it and go red on a disagreement.
10. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
11. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py` was built
    the right way from birth — every default is `None`, resolved in the body —
    so there is now a worked example in the repo to copy.** It touches what the
    pilot reads, so no session may make the change during a repair to a test.
12. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
13. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
14. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
15. **The settled-rate anchor (R-004)** — returned to him on correct facts.
16. **ALL FIVE CONTEXT DECK LINES ARE ON THE BRIEF** and he was told. One word
    removes any of them.
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED EIGHT TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**
