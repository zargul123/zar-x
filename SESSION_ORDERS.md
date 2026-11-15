# ZAR X — **GAUNTLET SLOT 1 IS SET UP AND HAS NOT BEEN RUN. DO NOT RUN IT. IT WAITS FOR THE COMMANDER'S ANSWER TO ONE QUESTION, AND THE ANSWER DECIDES YOUR WHOLE SESSION.**

*Written 2026-11-15 by Fable, at the end of a long session that finished
Phase 5 and then, on the Commander's order, began Phase 6. **I hold no
power to grant you an exemption and I have not written one. What follows
reports HIS rulings.***

---

# **>>> FIRST: THE ONE COMMAND YOU MUST NOT TYPE WITHOUT HIS WORD**

    python lab/gauntlet.py --slot 1 --go

**IT SPENDS ONE OF THE THREE SLOTS OF THE PROMISE, FOR EVER.** It writes a
marker file before it opens the vault, and a second run is refused. **There
is no undo.** `python lab/gauntlet.py --gate` and `python signals/turtle.py
--gate` are safe: they never open the vault.

**AND DO NOT OPEN THE VAULT'S DAILY FILES TO "HAVE A LOOK".** A look at the
hold-out is a look at the result. What has been seen so far is written
down, to the candle, in `PROGRESS_LOG.md` 2026-11-15.

---

# **>>> SECOND: TWO RULINGS OF 2026-11-15 THAT CHANGE HOW THIS SHIP RUNS**

**1. A BUILD MADE BY FABLE IS NOT ATTACKED BY THE NEXT SESSION** (ruled
2026-11-14, repeated to me in words). That covers Phase 5's logger and
Mirror and this Phase 6 setup. `THE_PATTERN.md` says you may not take it
from a document, so **ask him one line**: *"The last builds were made by
Fable. Do I skip attacking them, as you ruled?"* **If he says no or does
not answer, attack them** - R-085, R-086 and R-088 are my own lists of
where I did not look.

**2. NO OTHER MODEL CHECKS WHAT FABLE BUILDS - INCLUDING PHASE 6.** His
words: *"which ever step fable builds no other model will check so
continue"*. **This waives R-006 - the independent review of the gauntlet -
for builds made by Fable.** It was the one guard this ship called absolute.
He was told the cost twice and ruled anyway; it is his to rule.

**WHAT THAT MEANS FOR YOU, WHOEVER YOU ARE:**

    HE HAS SAID IN WORDS THAT YOU ARE FABLE
      -> you may carry on with Phase 6 under his ruling. **FILE MORE
         AGAINST YOURSELF, NOT LESS.** R-088 is the model.
    HE HAS NOT SAID IT
      -> **YOU ARE AN ORDINARY ZAR X SESSION. R-006 APPLIES TO ANYTHING
         YOU BUILD IN PHASE 6, IN FULL**, and you may not run a slot that
         another AI has not reviewed.
      -> **AND YOU ARE THE SECOND MIND THIS SETUP NEVER HAD.** If he lets
         you, attack `signals/turtle.py`, `lab/gauntlet.py` and the bar
         BEFORE the slot is run. R-088 is the list. **That would be worth
         more than anything else you could do this session, and I am
         asking him to allow it.**

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — ask the one line about skipping the attack.
                            Prove the ship alive (EIGHTEEN invocations now).
                   PART 2 — **ASK HIM THE QUESTION BELOW IF HE HAS NOT
                            ANSWERED IT, AND DO WHAT HE CHOOSES.**

## THE QUESTION ON HIS DESK

**Slot 1 as declared will probably fail before it starts, on arithmetic.**
The locked bar needs 30 hold-out trades. On 60 trendless made-up markets
the test produced a median of 25 and reached 30 in only 18. It did not pass
noise (0 of 60) - it simply cannot find enough trades in 297 days.

    (1) RUN IT AS DECLARED.
        -> type the one command, save everything it prints, write the
           verdict into PROGRESS_LOG.md. If it FAILS: the obituary, and
           Slot 2 is next. If it PASSES: Phase 7's proving voyage, on
           paper. **If the too-good alarm sounds: no pass - hunt a leak.**
    (2) RE-SPECIFY THE SLOT TO 4-HOUR CANDLES, BEFORE ANYTHING IS RUN.
        -> about six times the candles and the trades, and the ship's full
           regime vane is calibrated on 4h. **A new bar is declared and
           committed alone first** - the channel, the weekly filter and
           the warm-up all have to be restated in 4h candles, with where
           each number comes from - **then the strategy and the runner are
           changed, both gates re-run, and the attack repeated.** Only he
           can change a locked slot, and only because no result has been
           seen.
    (3) NOT YET.
        -> leave Slot 1 unspent. Slot 2 (the funding-rate fade) can be set
           up instead: Binance serves funding history back to 2019, free.

**PUT IT TO HIM IN PLAIN WORDS WITH THE OPTIONS LAID OUT. DO NOT PICK.**

---

# THE BRIEF, IN PLAIN WORDS

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   58     cockpit/funding.py   GATE 3.2-R8   71
    data/open_interest.py       GATE 3.2b-R10 88 x2  data/collection_guard.py  OK/FAIL
    cockpit/news.py             GATE 3.3-R1   54     cockpit/events.py    GATE 3.4      69 x2
    cockpit/whales.py           GATE 3.5-R2  111 x2  cockpit/carry.py     GATE 4.1      87 x2
    journal/log_trade.py        GATE 5.1-R3  101 x2  journal/mirror.py    GATE 5.2      84 x2
    signals/turtle.py           GATE 6.1-S    32 x2  lab/gauntlet.py      GATE 6.1-R    42 x2
    vault INTACT 6 of 6 - Brief 3/3 - lab/results/ holds NO slot marker
    journal/my_trades.csv DID NOT EXIST when I left

**EIGHTEEN INVOCATIONS. THE FIRST SIXTEEN MEASURED 1,263 GREEN, 0 RED on
2026-11-15 and were NOT re-run after the Phase 6 files were added; the two
new gates measured 32 and 42, twice each. If nothing drifted the total is
1,411 - that is a sum, not a measurement. MEASURE IT.**

**HOW EACH GATE IS RUN:** `cockpit/fear_greed.py`, `cockpit/funding.py` and
`data/open_interest.py` take no flag; every other gate takes `--gate`;
`lab/verify_vault.py` and `cockpit/brief.py` take none. Seven of them are
run a second time at `TZ=UTC0` (the ones marked x2 above).

**YOUR WORD-HITS WILL BE:** fear_greed line 147, funding lines 69 and 190 -
all innocent prose. **THE FUNDING GATE'S "escaped" LINE HAS FOOLED THREE
SESSIONS. KEEP NAMING IT.**

## What I did after Phase 5, in seven lines

1. **Recorded his ruling in his own words** and declared Slot 1's bar,
   committed alone.
2. **Ran the Lab's own four gates** - all passed, first time since July.
3. **Built the strategy** (140 lines, numpy only) and **the runner** (a new
   file; nothing existing in `lab/` changed).
4. **Rehearsed the whole run on made-up coins** through the Lab's real
   engine. The vault was never opened by anything I wrote.
5. **Attacked both with 44 text edits.** Six holes in my own gates, three
   of them on the real run's path. All closed.
6. **Found that my own gate could have spent the slot it guards.** Fixed.
7. **Measured the test on 72 made-up worlds** and found the count problem
   that is now on his desk.

---

# WHAT YOU OWE WHICHEVER WAY HE ANSWERS

1. **PROVE THE SHIP IS ALIVE FIRST**, eighteen invocations, red counted by
   machine three ways, every hit read by eye.
2. **IF A SLOT IS RUN, EVERYTHING IT PRINTS GOES INTO `PROGRESS_LOG.md`
   UNEDITED**, the five bars, the alarm, and each coin's information card.
   **A FAIL IS WRITTEN AS PLAINLY AS A PASS. No "nearly", no "promising",
   no second try.**
3. **`journal/my_trades.csv`, if it exists, is his.** Read it, never write
   it. **And ask him how `LOG_TRADE.bat` and `MIRROR.bat` went** - nobody
   has ever answered the ten questions by hand.

---


# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT ALREADY READS CHANGES** except what your orders call
    for — prove it with `git`, never assert it.
(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and never asks the module
    where to look.
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and the restoration verified.
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.** A
    sabotage that cannot run looks exactly like a gate that held.
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **CERTIFY BY ATTACK, NOT BY THE DRILL** — real text edits in copies
    outside the repo, control first. **AND WRITE THE ATTACK LIST BEFORE YOU
    RUN IT: writing mine showed me three holes in my own gate before a
    single attack ran, and running it showed two more.**
(h) **PROVE YOUR WITNESS CAN SEE THE FAULT BEFORE YOU BELIEVE ITS VERDICT.**
(i) **NEVER RUN A WITNESS AND A GATE AGAINST THE SAME COPY.**
(j) **TELL YOUR GATE HOW MANY CHECKS IT OWES.** `log_trade.py` (101) and
    `mirror.py` (84) do. The other seven do not (R-070).
(k) **A FAILING GATE MUST STILL BE ABLE TO FINISH REPORTING — AND YOU MUST
    PROVE IT.** R-084 is this rule broken in a gate that had been measured
    as keeping it, on a different shape. **Read every file through a helper
    that survives the file not being there.**
(l) **A CLAIM ABOUT WHAT CANNOT BE TESTED IS A PERMISSION SLIP.** Try it.
(m) **A CLAIM STATED IN BOLD IS STILL ONLY A CLAIM. WRITE YOUR PREDICTIONS
    DOWN BEFORE YOU RUN.**
(n) **>>> NEW, EARNED 2026-11-15: BEFORE YOU BUILD ANYTHING THAT COMPUTES,
    WRITE THE ARITHMETIC DOWN AND ASK WHAT EVERY INPUT'S UNIT IS.** `size`
    had been in the journal's design since August and nobody had ever said
    whether it was coins or dollars. **The orders named two missing
    figures. There were four undefined things, and the two nobody had
    noticed were the two that would have printed wrong numbers on a screen
    that looked normal.**

**PASS = every check green including every sabotage CAUGHT. Anything less is
a FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`journal/log_trade.py --gate` LAUNCHES FIVE CHILD INTERPRETERS** (checks
  (i), (m), and three shells in check (n), side by side). ~0.8 s healthy.
  **WHEN CHECK (n) MEETS A QUESTION IT DOES NOT RECOGNISE IT TAKES ~76
  SECONDS** — one 60-second deadline plus a 15-second wait. **RED, and not a
  hang.** Do not trim the deadline.
- **`journal/mirror.py --gate` IMPORTS THE REAL `log_trade.py` FROM ITS OWN
  FOLDER** to write its fake trades. A copy of `mirror.py` alone, in a tree
  with no `log_trade.py` beside it, cannot run its gate. **The production
  half imports nothing from it.**
- **`cockpit/whales.py --gate` TAKES ~19 SECONDS, BINDS TWO LOCAL PORTS AND
  LEAVES A HUNG DAEMON THREAD BEHIND, ON PURPOSE.**
- **`cockpit/carry.py --gate` AND `cockpit/funding.py` CAN GO RED WITHIN
  SECONDS OF A FUNDING SETTLEMENT (00:00, 08:00, 16:00 UTC).** R-069, R-021.
  Re-run once, away from the settlement. Outside that window red is REAL.
- **`cockpit/funding.py` TAKES TWO MINUTES** (120 s and 133 s today).
  `cockpit/fear_greed.py` takes one. `data/open_interest.py` takes one each.
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL
  PASS.** The bar is 3 of 5 publishers.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **GATE TIMINGS ON RECORD ARE WEATHER REPORTS, NOT CHECKS.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS
  NOT YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.**
- **THE CLOUD WATCHMAN PUSHES EVERY FEW HOURS. `git pull` FIRST**, and check
  your commit hashes again after you push.
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull,
  and push whatever it left behind.
- **A NOTEPAD WINDOW SHOWING `zarx_mirror.txt` MAY STILL BE OPEN ON HIS
  SCREEN FROM MY TEST.** I did not close it: he keeps his own notes in
  Notepad and I would not kill a process by name.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

**>>> THE FOUR NEWEST, ALL 2026-11-15:**

    (i)   THE LOGGER ASKS FOR THE STOP AND THE ACCOUNT. ("Ask me 2 more
          questions.")
    (ii)  THE MIRROR SHOWS BOTH RISK LINES, NAMED - pure 1%, and 1% with
          the 25% cap. **For the Mirror. Not ruled for the gauntlet.**
    (iii) `size` IS A DOLLAR AMOUNT, NOT A NUMBER OF COINS.
    (iv)  THE LOGGER ASKS "HOW MANY HOURS AGO DID YOU GET IN?"

1. **A BUILD MADE BY FABLE IS NOT ATTACKED BY THE NEXT SESSION** (2026-11-14).
   He was told it means such a build ships read by nobody but its author,
   and ruled it anyway. **Carry it; do not reopen it; do not extend it to
   yourself.**
2. **PHASE 6's INDEPENDENCE IS BY ROLE, NOT BY BRAND** (2026-11-14). Whoever
   builds, the other one reviews. One AI doing both is the only forbidden
   case. **If only one is available when Phase 6 arrives, PHASE 6 WAITS.**
3. **HIS TEST FOR EVERY FINDING, IN HIS OWN WORDS:** *"our actual goal is to
   make a correct thing in actual real environment. so those things which
   cant be done in actual scenarios at those we have to ignore those."*
   **THIS SHARPENS THE ATTACK, IT DOES NOT EXCUSE ONE.**
4. **R-080 WAS RULED SERIOUS, REPAIRED, AND CLEARED** by a session that did
   neither. R-081 and R-083 are cleared the same way.
5. **R-060: "CORRECT IT".** Corrected. R-066 open.
6. **R-054, R-047 AND R-048 ARE SMALL.**
7. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS DONE.**
8. **`cockpit/brief.py` GETS NO GATE YET** — before going live, with the
   Category B pile.
9. **R-016 IS OFF HIS DESK; R-019 IS CLEARED BY HIM; R-025 IS CLEARED.**
10. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
11. **THE CONTEXT DECK, THE CARRY MONITOR AND THE MIRROR ARE INFORMATION AND
    CAN NEVER BECOME SIGNALS.** **Phase 6's three slots are locked BY NAME:
    Turtle/Donchian, funding-rate fade, on-chain cycle thermometer.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> THE ONE THAT DECIDES WHAT HAPPENS NEXT: RUN SLOT 1 AS DECLARED,
   RE-SPECIFY IT TO 4-HOUR CANDLES, OR NOT YET.** Put to him 2026-11-15
   with the made-up-market figures. **DO NOT RUN IT WITHOUT HIS ANSWER.**
   (The risk figure is settled: asked, he said "No preference", and the
   gauntlet uses the ship's own rule, 1% with the 25% cap.)
2. **>>> SLOT 3'S DATA SOURCE** — is there a free on-chain cycle source
   (MVRV or similar)? If not he may re-specify the slot ONCE, before testing
   begins.
3. **THE THREE CHOICES I MADE IN THE NEW BUILD - HE RULED ON ALL THREE,
   2026-11-15, AND KEPT THEM. DO NOT ASK AGAIN.** A wrong-side stop is
   refused; the 1% lines keep his real exit; a reading older than 8 hours
   counts as no reading.
4. **DOES THE CARRY LINE READ AS INFORMATION, OR AS A SUGGESTION?** Shown to
   him 2026-08-19. **Still not answered — this is the SEVENTH session
   carrying it. I did not ask it today; I spent his attention on the four
   questions that blocked the build.** ASK.
5. **AND BESIDE IT:** the carry figure is the yield on the PERP NOTIONAL;
   running the trade needs money on both legs, so the return on capital
   deployed is lower than the number on the line. His call.
6. **R-070 — SEVEN OF NINE GATES DO NOT KNOW THEIR OWN COUNT.** One line
   each. He has never ruled.
7. **R-049 — offer it a TENTH time.** The X1 repair in `cockpit/news.py`.
8. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED.**
9. **THE CATEGORY B PILE IS FIFTY-ONE.** Cleared before the ship is used for
   real. **Keep saying the number.**
10. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR** (the R-037 repair). **Start
    -> type `powershell` -> right-click -> Run as administrator:**

        wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

11. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
    RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
12. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto
    and Bitcoin.com.
13. **THE RULES HE HAS NOT YET ADOPTED**, each earned many times: *a
    sabotage must be proved to change the output*; *every threshold tested
    at the exact value where it turns over*; **candidate Law 8 — "a claim
    about how something behaves is not a fact until it has been run"**; *a
    gate must be told how many checks it owes*; *a gate must call the thing
    the way its only real caller calls it*; *every check must be made to
    fail once*; *a claim about what cannot be tested is a permission slip*.
    **AND ONE MORE, PROPOSED TODAY AND NOT ADOPTED: "before building
    anything that computes, write down every input's unit."**
14. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
15. **`MAX_PLAUSIBLE_RATE` in `cockpit/funding.py`** — 13-16x looser than
    Binance's cap. Recommendation: ~0.01. Still not done.
16. **`def run(symbols=SYMBOLS, ...)` and `fetch_history` still freeze their
    globals.**
17. **The settled-rate anchor (R-004).**
18. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED FIFTEEN TIMES, NOT ADOPTED.**

---

# READ THESE FIRST

1. **`EXECUTION_PLAN.md` PHASE 6** and the CURRENT POSITION MARKER.
2. **`SHIP_LAWS.md`, Law 7**, and `README.md` — THE PROMISE.
3. **`PROGRESS_LOG.md`, the two entries of 2026-11-15** — the bars, then the
   account. **The file is ~950 KB; do not read it all.**
4. **`PROGRESS_LOG.md` 2026-07-26, Gate 2.5** — the day the Lab was shown a
   leak it could not see. **This is the entry Phase 6 stands on.**
5. **`lab/engine.py`, `lab/dummies.py`, `lab/leak_check.py`.**
6. **`REVIEW_QUEUE.md`: R-006, then R-084 to R-087.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** And check your commit hashes again after you push.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **THE `.py` FILES AND THE FIVE DOCUMENTS ARE CRLF** (except
  `cockpit/plan.py` and `journal/snapshot.py`, which are LF). **A file
  written by an editor tool arrives as LF on this machine.** Write to a
  scratch file and install it with a script that converts and REFUSES a
  bare LF. Judge line endings in the WORKING TREE, never against
  `git show HEAD:<file>`, which hands back LF.
- **>>> NEVER PASS A LONG SCRIPT TO THE SHELL AS A HERE-DOCUMENT.** A
  here-doc with quotes in it broke my shell today, after I had read this
  same warning. **Write the file with the editor tool; run the file.**
- **`.bat` FILES MUST BE CRLF AND ASCII-ONLY.** To RUN one from a tool, use
  PowerShell and its full path: `& "C:\...\zar-x\MIRROR.bat"`. `cmd /c`
  from a bash shell does not find it.
- **PYTHON HERE IS 3.10**: no backslash inside an f-string expression.
- **SET `PYTHONUTF8=1` ON YOUR OWN HARNESS TOO.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ` — and compare the counts against HEAD.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH** — and before a command, reach for the `.bat`:
  `SHOW_REPORT.bat` (the latest Brief), `run_daily.bat` (a fresh one),
  `CHECK_STATUS.bat` (the collection's health), `LOG_TRADE.bat` (**ten
  questions**, logs a closed trade), **`MIRROR.bat` (his trades, graded by
  arithmetic, in Notepad).**

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL.

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY
                            mistake as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... one OPEN item against your own work. **You may
                            NOT clear R-084 to R-087 unless you attacked
                            them; you may never clear R-006.**
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the
                            truth. Keep the old markers below it.
    4. ROADMAP.md ......... tick what shipped; add what you MEASURED.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words
                            brief. **>>> IF YOU BUILT SLOT 1's SETUP, THE
                            NEXT SESSION'S JOB IS FABLE'S: REVIEW THAT SETUP
                            BEFORE IT RUNS. Write the orders for a reviewer
                            who did not build it and must not have to ask
                            you anything. AND SAY IN THEM, IN BOLD, WHETHER
                            ANY VAULT DATA HAS BEEN LOOKED AT.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what
       held, **what you got wrong**, and what decision is his. **If he says
       he does not understand the options you gave him, the options were
       written badly. REWRITE THEM, DO NOT EXPLAIN THEM HARDER.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly", "I believe" or "this should be fine" about anything that ships —
FILE IT in `REVIEW_QUEUE.md` before the commit that ships it.**
