# ZAR X — **GAUNTLET SLOT 1 IS NOW A 4-HOUR TEST. IT IS SET UP AND HAS NOT BEEN RUN. DO NOT RUN IT. IT WAITS FOR THE COMMANDER'S "GO", AND HE HAS BEEN TOLD IT WILL MOST LIKELY FAIL.**

*Written 2026-11-16 by Fable. He opened the session with "zarx and this
session is for fable", so his rulings about Fable applied to it. **I hold
no power to grant you an exemption and I have not written one. What
follows reports HIS rulings.***

---

# **>>> FIRST: THE ONE COMMAND YOU MUST NOT TYPE WITHOUT HIS WORD**

    python lab/gauntlet.py --slot 1 --go

**IT SPENDS ONE OF THE THREE SLOTS OF THE PROMISE, FOR EVER.** It writes a
marker file before it opens the vault, and a second run is refused. **There
is no undo.** `python lab/gauntlet.py --gate` and `python signals/turtle.py
--gate` are safe: they never open the vault.

**AND DO NOT OPEN THE VAULT'S FILES TO "HAVE A LOOK".** A look at the
hold-out is a look at the result. **WHAT HAS BEEN LOOKED AT, IN BOLD AS
THE RITUAL ASKS: ON 2026-11-16, THE DATE COLUMN OF THE THREE 4-HOUR FILES
AND THE INSPECTOR'S ONE-WORD VERDICTS - NO PRICE. ON 2026-11-15, TWO ROWS
OF BTC DAILY FROM JULY 2023 AND ONE ETH DAILY CANDLE OF 2025-10-10. THE
BTC 4-HOUR FILE HAS BEEN WALKED, HOLD-OUT INCLUDED, BY THE LAB'S OWN EXAM
STRATEGIES; ETH AND SOL 4-HOUR BY NOTHING.**

---

# **>>> SECOND: THE RULINGS THAT GOVERN PHASE 6**

**1. A BUILD MADE BY FABLE IS NOT ATTACKED BY THE NEXT SESSION** (ruled
2026-11-14). That covers Phase 5 and both Phase 6 setups. `THE_PATTERN.md`
says you may not take it from a document, so **ask him one line**: *"The
last builds were made by Fable. Do I skip attacking them, as you ruled?"*
**If he says no or does not answer, attack them** - R-085, R-086, R-088
and R-089 are my own lists of where I did not look.

**2. NO OTHER MODEL CHECKS WHAT FABLE BUILDS - INCLUDING PHASE 6**
(2026-11-15): *"which ever step fable builds no other model will check so
continue"*. **R-006 is WAIVED for builds made by Fable, not cleared.**

**3. SLOT 1 IS RE-SPECIFIED TO 4-HOUR CANDLES** (2026-11-16). Asked "run as
declared / change to 4-hour candles / not yet", **he chose "Change to
4-hour candles".** The plan's slot line now reads 4-hour. The daily build
was never run and is withdrawn.

**WHAT THAT MEANS FOR YOU, WHOEVER YOU ARE:**

    HE HAS SAID IN WORDS THAT YOU ARE FABLE
      -> you may carry on with Phase 6 under his ruling. **FILE MORE
         AGAINST YOURSELF, NOT LESS.** R-089 is the model.
    HE HAS NOT SAID IT
      -> **YOU ARE AN ORDINARY ZAR X SESSION. R-006 APPLIES TO ANYTHING
         YOU BUILD IN PHASE 6, IN FULL**, and you may not run a slot that
         another AI has not reviewed.
      -> **AND YOU ARE THE SECOND MIND THIS SETUP NEVER HAD.** If he lets
         you, attack `signals/turtle.py`, `lab/gauntlet.py` and the bar
         BEFORE the slot is run. R-088 and R-089 are the list.

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — ask the one line about skipping the attack.
                            Prove the ship alive (TWENTY invocations).
                   PART 2 — **ASK HIM THE QUESTION BELOW IF HE HAS NOT
                            ANSWERED IT, AND DO WHAT HE CHOOSES.**

## THE QUESTION ON HIS DESK

**The trade-count problem is solved. A different one took its place.** On
made-up 4-hour markets the test found a median of 147 trades (never fewer
than 115; the bar is 30). **But it passed NOTHING: 0 of 64 markets with no
trend, and 0 of 8 markets with a real, steady trend in them.** The reason
is costs: a trade here lasts about 20 hours and aims at a small move, and
the fee and slippage are a big slice of a small move.

    (1) GO. Run Slot 1 on 4-hour candles as declared.
        -> type the one command, save everything it prints, write the
           verdict into PROGRESS_LOG.md UNEDITED. If it FAILS: the
           obituary, and Slot 2 is next. If it PASSES: Phase 7's proving
           voyage, on paper. **If the too-good alarm sounds: no pass -
           hunt a leak.**
    (2) CHANGE THE CHANNEL TO TWENTY DAYS (120 candles) FIRST.
        -> a new bar committed alone, then the strategy, both gates, the
           attack and the made-up markets again. The exit stays the
           engine's, so the cost problem stays.
    (3) GO BACK TO DAILY CANDLES.
        -> the daily build is in git at `3880404`. The count problem
           returns: 30 trades reached in 18 of 60 made-up worlds.
    (4) NOT YET.
        -> leave Slot 1 unspent. Slot 2 (the funding-rate fade) can be set
           up instead: Binance serves funding history back to 2019, free.

**PUT IT TO HIM IN PLAIN WORDS WITH THE OPTIONS LAID OUT. DO NOT PICK.**
**He asked this session, in his own words, to have things explained "in
easy words" because he is "not a technical person". WRITE TO HIM THAT WAY:
what the test is, what the choice is, what each choice costs. No gate
numbers unless he asks.**

---

# THE BRIEF, IN PLAIN WORDS

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   58     cockpit/funding.py   GATE 3.2-R8   71
    data/open_interest.py       GATE 3.2b-R10 88 x2  data/collection_guard.py  25 OK
    cockpit/news.py             GATE 3.3-R1   54     cockpit/events.py    GATE 3.4      69 x2
    cockpit/whales.py           GATE 3.5-R2  111 x2  cockpit/carry.py     GATE 4.1      87 x2
    journal/log_trade.py        GATE 5.1-R3  101 x2  journal/mirror.py    GATE 5.2      84 x2
    signals/turtle.py           GATE 6.2-S    39 x2  lab/gauntlet.py      GATE 6.2-R    44 x2
    vault INTACT 6 of 6 - Brief 3/3 - lab/results/ holds NO slot marker
    journal/my_trades.csv DID NOT EXIST when I left

**TWENTY INVOCATIONS, 1,429 GREEN, 0 RED, MEASURED 2026-11-16.** (The
orders I inherited said "eighteen"; counting each `x2` twice it is twenty.
Eight files are run a second time at `TZ=UTC0`, not seven.) The eighteen
that are not the two new gates were measured at 06:04 UTC; the two new
gates in their final form at 06:41. **MEASURE IT AGAIN.**

**HOW EACH GATE IS RUN:** `cockpit/fear_greed.py`, `cockpit/funding.py` and
`data/open_interest.py` take no flag; every other gate takes `--gate`;
`lab/verify_vault.py` and `cockpit/brief.py` take none.
**`lab/gauntlet.py --gate` NOW TAKES 48 SECONDS** (it was 11).

**YOUR WORD-HITS WILL BE:** the fear_greed and funding gates' own prose
about old escapes (`[old gate: ESCAPED] → CAUGHT` is a PASS line), and the
gauntlet gate's hand cases, which are SUPPOSED to print `FAILED`. **THE
FUNDING GATE'S "escaped" LINES HAVE FOOLED THREE SESSIONS. KEEP NAMING
THEM.**

## What I did, in eight lines

1. **Measured the ship alive**: 1,411 green, 0 red - yesterday's sum, now
   a measurement.
2. **Put the question to him.** He chose 4-hour candles.
3. **Declared the new bar and committed it alone** (`023ff51`).
4. **Rebuilt the strategy and changed one line of the runner** (`0bae62e`).
   Nothing else in `lab/` changed.
5. **Counted the 4-hour vault from its date column only**: 5,624 candles a
   coin, 1,789 hold-out, the same on all three, no gap.
6. **Attacked both gates with 53 text edits, predictions written first.**
   Five holes - three mine from today, two a day old. All closed; 49 red
   and 4 that cannot change a result.
7. **Ran 72 made-up worlds**: plenty of trades, no passes, not even with a
   trend.
8. **Told him**, in easy words, that it will most likely fail and why.

---

# WHAT YOU OWE WHICHEVER WAY HE ANSWERS

1. **PROVE THE SHIP IS ALIVE FIRST**, twenty invocations, red counted by
   machine three ways, every hit read by eye.
2. **IF A SLOT IS RUN, EVERYTHING IT PRINTS GOES INTO `PROGRESS_LOG.md`
   UNEDITED**, the five bars, the alarm, and each coin's information card.
   **A FAIL IS WRITTEN AS PLAINLY AS A PASS. No "nearly", no "promising",
   no second try.**
3. **`journal/my_trades.csv`, if it exists, is his.** Read it, never write
   it. **And ask him how `LOG_TRADE.bat` and `MIRROR.bat` went** - nobody
   has ever answered the ten questions by hand. I did not ask today.

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
(o) **>>> NEW, EARNED 2026-11-16: WHEN A HAND CASE PINS A TURNING POINT,
    PIN IT ON BOTH SIDES - LONG AND SHORT, ABOVE AND BELOW.** Every exact
    case in my first gate was on the long side, and `<=` on the short side
    walked through at 37/0. **AND TEST EVERY BAR NEAR ITS OWN LINE**: the
    drawdown bar had one case, a ruinous one, and a bar tripled to 90%
    went green for two days.
(n) **>>> EARNED 2026-11-15: BEFORE YOU BUILD ANYTHING THAT COMPUTES,
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
- **MY ATTACK AND MADE-UP-WORLD SCRIPTS LIVED IN A SCRATCH FOLDER OUTSIDE
  THE REPO AND ARE GONE.** What they did is in `PROGRESS_LOG.md`
  2026-11-16, sections 4 and 5, edit by edit. To repeat the attack: one
  fresh copy of `config.py`, `risk/`, `regime/`, `indicators/`, `signals/`
  and `lab/*.py` per edit, **with no `lab/vault/` and an empty
  `lab/results/`**, control first.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

**>>> THE NEWEST, 2026-11-16: SLOT 1 IS A 4-HOUR TEST.** His choice, from
three options with no recommendation. **Do not ask him again whether to
use daily or 4-hour unless he raises it** - what is open is go / change
the channel / back to daily / not yet.

**>>> THE FOUR BEFORE THAT, ALL 2026-11-15:**

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

1. **>>> THE ONE THAT DECIDES WHAT HAPPENS NEXT: GO ON THE 4-HOUR SLOT 1,
   CHANGE ITS CHANNEL TO TWENTY DAYS FIRST, GO BACK TO DAILY, OR NOT YET.**
   Put to him 2026-11-16 with the made-up-market figures. **DO NOT RUN IT
   WITHOUT HIS ANSWER.** (The risk figure: asked on 2026-11-15 he said "No
   preference", and the gauntlet uses the ship's own rule, 1% with the 25%
   cap. **ON 4-HOUR CANDLES THE CAP BINDS ON EVERY TRADE, so it is in
   practice a 25%-position rule. He has been told.**)
2. **>>> SLOT 3'S DATA SOURCE** — is there a free on-chain cycle source
   (MVRV or similar)? If not he may re-specify the slot ONCE, before testing
   begins.
3. **THE THREE CHOICES I MADE IN THE NEW BUILD - HE RULED ON ALL THREE,
   2026-11-15, AND KEPT THEM. DO NOT ASK AGAIN.** A wrong-side stop is
   refused; the 1% lines keep his real exit; a reading older than 8 hours
   counts as no reading.
4. **DOES THE CARRY LINE READ AS INFORMATION, OR AS A SUGGESTION?** Shown to
   him 2026-08-19. **Still not answered — this is the EIGHTH session
   carrying it. I did not ask it today either; his attention went to the
   slot.** ASK.
5. **AND BESIDE IT:** the carry figure is the yield on the PERP NOTIONAL;
   running the trade needs money on both legs, so the return on capital
   deployed is lower than the number on the line. His call.
6. **R-070 — SEVEN GATES DO NOT KNOW THEIR OWN COUNT** (the four newest
   do: log_trade, mirror, turtle, gauntlet). One line
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
3. **`PROGRESS_LOG.md`, the two entries of 2026-11-16** — the 4-hour bar,
   then the account — and the Phase 6 entries of 2026-11-15 they stand on.
   **The file is ~1 MB; do not read it all.**
4. **`PROGRESS_LOG.md` 2026-07-26, Gate 2.5** — the day the Lab was shown a
   leak it could not see. **This is the entry Phase 6 stands on.**
5. **`lab/engine.py`, `lab/dummies.py`, `lab/leak_check.py`.**
6. **`REVIEW_QUEUE.md`: R-006, then R-084 to R-089.**

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
                            NOT clear R-084 to R-089 unless you attacked
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
