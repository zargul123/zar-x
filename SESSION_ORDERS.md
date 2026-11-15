# ZAR X — **PHASE 5 IS COMPLETE AND FABLE BUILT IT. BY THE COMMANDER'S RULING YOU DO NOT ATTACK THAT BUILD. YOUR JOB IS THE FIRST HALF OF PHASE 6: SET UP GAUNTLET SLOT 1 — AND STOP BEFORE YOU RUN IT.**

*Written 2026-11-15 by Fable, which re-ran the previous session's review
(R-083 clears), took the Commander's four answers, changed the trade logger
from seven questions to ten under GATE 5.1-R3, and built `journal/mirror.py`
under GATE 5.2. **I hold no power to grant you an exemption and I have not
written one. What follows reports HIS ruling.***

---

# **>>> FIRST: WHY YOU ARE NOT ATTACKING WHAT I BUILT, AND WHO SAID SO**

**THE COMMANDER'S RULING OF 2026-11-14, IN `THE_PATTERN.md`:** *a build made
by Fable is not attacked by the next session.* **On 2026-11-15 he said it
again, in words, to me:** *"i also wrote an exemption that your build like
any build made by fable no next session will attack your build."*

**`THE_PATTERN.md` SAYS YOU MAY NOT TAKE THIS FROM A DOCUMENT. SO ASK HIM ONE
LINE BEFORE YOU START:**

    "The last build - the ten-question logger and the Mirror - was made by
     Fable on 2026-11-15. Do I skip attacking it, as you ruled?"

    HE SAYS YES  -> skip PART 1 for that build. Go to PART 2.
    HE SAYS NO, OR DOES NOT ANSWER -> **ATTACK IT LIKE ANY OTHER BUILD.**
        R-085 and R-086 in `REVIEW_QUEUE.md` are my own list of where I did
        not look. Start at R-086 item 6.

**THE COST OF THE RULING, WHICH HE WAS TOLD BEFORE HE MADE IT:** both files
ship having been read by nobody but their author. **The guard is R-084,
R-085, R-086 and R-087. Do not let them quietly become a place findings go
to die.** The Category B pile is **FIFTY-ONE**.

**AND YOU, WHOEVER YOU ARE, ARE NOT FABLE UNLESS HE SAYS SO IN YOUR
CONVERSATION.** If you are an ordinary Zar X session, **what YOU build is
attacked exactly as before.**

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — ask the one line above. If he says yes, there
                            is nothing to attack. Prove the ship alive and
                            move on.
                   PART 2 — **PHASE 6, SLOT 1, THE SETUP ONLY.** Build the
                            Turtle/Donchian strategy and everything needed
                            to test it, write down exactly how it will be
                            tested, **AND DO NOT RUN IT ON THE VAULT.**
                            Then stop. The Commander brings Fable to review
                            the setup BEFORE it runs.

**WHY PART 2 STOPS WHERE IT STOPS.** THE PROMISE gives three sealed slots and
then the signals chapter closes for ever. There is no second test to catch
the first one's mistake. **Law 7 proved the Lab's own numbers cannot detect a
leak** — a strategy that looks profitable because of a bug passes every
number it produces. So `EXECUTION_PLAN.md` Phase 6 says, and R-006 repeats:
**a second AI that did not build the test reviews the setup BEFORE it runs
and the verdict AFTER.** The Commander's plan, said to me on 2026-11-15:
**a Zar X session builds Phase 6; Fable comes back and tests it.**

    a Zar X session BUILDS the gauntlet -> FABLE reviews it .......... OK
    FABLE builds the gauntlet -> a ZAR X SESSION reviews it .......... OK
    ONE AI builds it AND reviews it -> NOBODY reviewed it ............ NO

**IF YOU RUN THE HOLD-OUT BEFORE THE REVIEW, THE SLOT IS SPENT AND THE
REVIEW IS WORTHLESS. THIS IS THE ONE INSTRUCTION IN THESE ORDERS THAT CANNOT
BE UNDONE IF YOU GET IT WRONG.**

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
    cockpit/whales.py           GATE 3.5-R2   PASSED  exit 0  0 red  111 green
      the same file at TZ=UTC0  GATE 3.5-R2   PASSED  exit 0  0 red  111 green
    cockpit/carry.py            GATE 4.1      PASSED  exit 0  0 red   87 green
      the same file at TZ=UTC0  GATE 4.1      PASSED  exit 0  0 red   87 green
    journal/log_trade.py        GATE 5.1-R3   PASSED  exit 0  0 red  101 green
      the same file at TZ=UTC0  GATE 5.1-R3   PASSED  exit 0  0 red  101 green
    journal/mirror.py           GATE 5.2      PASSED  exit 0  0 red   84 green
      the same file at TZ=UTC0  GATE 5.2      PASSED  exit 0  0 red   84 green
    vault INTACT 6 of 6 - Brief 3/3 (Whale watch 6 of 6) - lab/ untouched
    journal/my_trades.csv DID NOT EXIST when I left

**>>> SIXTEEN INVOCATIONS, 1,263 GREEN, 0 RED.** If you measure something
different, it is not a rounding error.

**PHASES 0 TO 5 ARE COMPLETE. PHASE 6 HAS NOT BEEN STARTED.**

## What I did, in eight lines

1. **Proved the ship alive first** — fourteen invocations, 1,047 green, 0
   red, 5 word-hits read by eye and innocent.
2. **Re-ran the last session's review with my own rig. Every number
   reproduced. R-083 CLEARS.** Twelve new sabotages against the checks he
   said he never attacked: eleven red, one green and proved harmless.
3. **Found one small thing: that gate could die in a traceback with no
   verdict line** (R-084). Exit 1, never a false green. Repaired in the new
   gate.
4. **Asked the Commander the question that blocked Phase 5, and found two
   more nobody had defined:** whether `size` is coins or dollars, and when
   he got in. **He answered all four.**
5. **Declared both bars and committed them alone** (`ef8509c`, no `.py`).
6. **The logger now asks TEN questions.** GATE 5.1-R3, 101 checks, 0 red.
   Attacked with 25 real text edits: 24 red, 1 green (a fault that fires
   only for a human at a keyboard — R-082 item 3, still open).
7. **Built the Mirror.** GATE 5.2, 84 checks, 0 red. Attacked with 34 text
   edits: **32 red and 2 green the first time; both greens were holes in my
   own gate; closed; 34 of 34 the second time.**
8. **Ran `MIRROR.bat` for real.** It works. Notepad opens on the report.

---

# **JOB 1 — ASK THE ONE LINE, THEN PROVE THE SHIP IS ALIVE**

**If he says the Fable build is not to be attacked, JOB 1 is the alive proof
and nothing else.** All SIXTEEN invocations, output to files, **red counted
BY MACHINE three ways** (the cross character counted BY CHARACTER, the first
word of a line, and `GATE ... FAILED`), **then READ every hit with your own
eyes.** My run produced 3 word-hits, all innocent prose:

    fear_greed line 147    "FAILURE, never a quiet pass**, which R-025 ..."
    funding line 69        "escaped the gate of 2026-07-26; four of the ..."
    funding line 190       "FAILURE, never a quiet pass**, which R-025 ..."

**THE FUNDING GATE'S "escaped" LINE FOOLED THREE CONSECUTIVE SESSIONS AND HAS
NOT FOOLED THE FOUR SINCE, BECAUSE THE ORDERS NAMED IT. KEEP NAMING IT.**

**HOW EACH GATE IS RUN** (it cost me a `grep` to find out, so here it is):

    cockpit/fear_greed.py           no flag
    cockpit/funding.py              no flag
    data/open_interest.py           no flag          (and again at TZ=UTC0)
    data/collection_guard.py        --gate
    cockpit/news.py                 --gate
    cockpit/events.py               --gate           (and again at TZ=UTC0)
    cockpit/whales.py               --gate           (and again at TZ=UTC0)
    cockpit/carry.py                --gate           (and again at TZ=UTC0)
    journal/log_trade.py            --gate           (and again at TZ=UTC0)
    journal/mirror.py               --gate           (and again at TZ=UTC0)
    lab/verify_vault.py             no flag   -> "VAULT INTACT"
    cockpit/brief.py                no flag   -> "3/3 instruments reporting"

**IF `journal/my_trades.csv` EXISTS WHEN YOU ARRIVE, HE HAS LOGGED A REAL
TRADE.** Every row is his. **Read it, never write it, and NEVER drive
`python journal\log_trade.py` by hand in the repo.** Both gates now
fingerprint the real journal before they start and require the same bytes at
the end, so a real journal no longer turns either gate red. **I did not test
that with a real journal present, because there was none. R-085 item 13.**

**AND IF HE HAS USED `LOG_TRADE.bat` OR `MIRROR.bat`, ASK HIM HOW IT WENT.**
Nobody has ever answered the ten questions by hand. **What he says about it
is worth more than any check I wrote.**

---

# **JOB 2 — PHASE 6, SLOT 1: THE TURTLE/DONCHIAN BREAKOUT. SETUP ONLY.**

**READ `EXECUTION_PLAN.md` PHASE 6 AND `SHIP_LAWS.md` LAW 7 BEFORE ANYTHING
ELSE. THEY OUTRANK THESE ORDERS.** The slot is locked BY NAME — *"Slot 1:
Turtle/Donchian breakout, daily (+weekly filter), regime-filtered"* — and
the pass bars were locked on 2026-07-26 and may not move:

    hold-out Profit Factor >= 1.15 AFTER costs
    >= 30 hold-out trades (fewer = FAIL, not "promising")
    walk-forward: profitable in >= 60% of windows, no window > 50% of profit
    Monte Carlo 5th percentile: max drawdown < 30%
    must beat buy-and-hold-with-1%-risk-sizing on the same window
    a second AI reviews the setup BEFORE and the verdict AFTER

## >>> TWO DECISIONS ARE HIS AND BOTH COME BEFORE ANY CODE. ASK FIRST.

    1. THE RISK FIGURE THE GAUNTLET SIZES WITH. The doctrine says 1% a
       trade; the 25% position cap makes the real figure about 0.49%.
       **This has been on his desk since Phase 2 with the words "decide
       BEFORE Phase 6, never after seeing results".** Phase 6 is now.
       (For the Mirror he ruled "show both, named". That was the Mirror.
       **Do not carry it to the gauntlet without asking** — the gauntlet
       produces ONE verdict per slot, not two.)
    2. SLOT 3'S DATA SOURCE. The plan allows the on-chain slot to be
       re-specified ONCE, by him, BEFORE testing begins. It does not block
       Slot 1 — but "before testing begins" starts counting when Slot 1
       runs, so it is cheaper asked now.

**PUT EACH TO HIM IN PLAIN WORDS WITH THE OPTIONS LAID OUT.** He is not a
programmer. On 2026-11-15 four questions put that way were answered in
minutes; one put as jargon had sat unanswered since August.

## WHAT "SETUP" MEANS, IN ORDER

1. **DECLARE THE BAR AND COMMIT IT ALONE** — `PROGRESS_LOG.md`, no `.py` in
   the commit. It must fix, BEFORE the strategy exists: the exact rules
   (entry channel, exit channel, the weekly filter, the regime filter, the
   stop), **every parameter as a number, with where the number comes from**
   — the published Turtle rules, not a search — the assets and timeframe,
   the cost model, and the train/hold-out line (**`train_end = 2025-10-01`,
   already fixed in Phase 2; it does not move**).
2. **NO PARAMETER MAY BE CHOSEN BY LOOKING AT RESULTS. NOT ONE.** *"Just try
   25 instead of 20"* is named in the plan as the overfitting death spiral
   and the answer is NO. **If you find yourself wanting to run it once "to
   see if it works", that is the moment to stop.**
3. **BUILD IT AS A `signal()` THE LAB CAN RUN** — `lab/engine.py`'s
   `run_backtest(data, signal, strategy_name, params=None, train_end=None,
   ...)`, and `lab/dummies.py` holds four worked examples including the two
   cheats the Lab was built to catch. `signals/` is empty; this is its
   first file.
4. **LAW 7 — THE LEAK LAW.** Run `lab/leak_check.py` on it AND read the code
   for look-ahead yourself, and write down what you read. **A clean scan is
   not innocence.** A signal that uses today's close to decide today's entry
   is the commonest leak and the scanner cannot see it.
5. **PROVE THE PLUMBING ON DATA THAT IS NOT THE VAULT.** A synthetic series
   you generate — a clean trend, a flat line, a sawtooth — where you can
   work out BY HAND what the strategy must do. **This is the gate for the
   setup: the strategy does what its rules say, on data whose answer you
   know.** It proves nothing about whether it makes money, and must not try
   to.
6. **WRITE THE SETUP DOCUMENT INTO `PROGRESS_LOG.md`**: everything a second
   AI needs to review the test without asking you anything.
7. **STOP. DO NOT CALL `load_vault`. DO NOT RUN THE HOLD-OUT. DO NOT RUN THE
   TRAIN SLICE EITHER** — a look at the train slice is a look at results,
   and the reviewer cannot un-know what you saw.

**IF YOU RUN SHORT, DO STEPS 1 AND 2 PROPERLY AND LEAVE THE REST.** A bar
with no code is a good day's work here. Half a strategy is not.

## THINGS YOU WILL MEET

  * **THE VAULT'S DAILY FILES HOLD 1,094 CANDLES, 2023-07-28 to 2026-07-25.**
    A 55-day channel and a weekly filter eat a warm-up before the first
    signal. **Count what is left on the hold-out side of 2025-10-01 before
    you promise 30 trades** — but count CANDLES, from the file's own dates,
    not trades. Counting trades is running it.
  * **THE VAULT CSVs HAVE NO VOLUME COLUMN.** Known since Phase 2.
  * **THE LAB'S OWN GATES** (`lab/gate_2_2.py` to `gate_2_5.py`) were green
    in July and nobody has run them since. **Run them before you lean on
    the Lab**, and say what they print.
  * **THE TOO-GOOD ALARM IS A FLARE, NOT A FENCE.** Gate 2.5 measured a
    leaked strategy clearing all four Phase-6 bars with the alarm silent.

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

1. **>>> BLOCKS PHASE 6: THE RISK FIGURE THE GAUNTLET SIZES WITH** — 1%, or
   the ~0.49% the 25% cap really produces. **Before any slot is tested,
   never after.** Open since Phase 2.
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
