# ZAR X — **ALL THREE GAUNTLET SLOTS ARE SPENT AND ALL THREE FAILED (SLOT 1 AND SLOT 3 WERE RUN ON 2026-11-17; SLOT 2 THE DAY BEFORE). THE PAPER-WATCH IS BUILT AND RUNNING: 13 COINS, 2 RULES, 2 EXITS, NO MONEY. YOUR JOB: (1) PROVE THE SHIP ALIVE - 38 INVOCATIONS. (2) THE CLOUD NOW KEEPS ITS OWN SEPARATE RECORD (BUILT THE SAME NIGHT; THE TWO RECORDS AGREE 26 OF 26) - READ ITS FIRST SCHEDULED RUNS. (3) SETTLE HOW HE IS TOLD OF SIGNALS. (4) A PAPER LINE ON HIS BRIEF. (5) THE WEEKLY AUTOPSY WHEN HE ASKS FOR IT.**

*Written 2026-11-17 (night) by Fable at the end of a very long session.
He opened it with "zarx fable here". Asked "The last builds were made by
Fable. Do I skip attacking them, as you ruled?" **HE ANSWERED "Yes, skip
it".** I hold no power to grant you an exemption and have not written
one. What follows reports HIS rulings.*

**READ `PROGRESS_LOG.md`'s LAST ENTRY FIRST** (the paper-watch's account),
then the bar above it. **HE IS NOT A PROGRAMMER AND SAYS SO OFTEN: "im a
noob dont understand that much maths". EASY WORDS. MONEY ON 1,000 DOLLARS.
NO GATE NUMBERS. WHEN HE ASKS WHICH OPTION IS BETTER, ANSWER WITH ONE.**

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

## Where the ship is

    THE GAUNTLET - FINISHED. On 1,000 dollars, October 2025 to July 2026:
      Slot 1  the breakout ........ FAILED 3 of 5 ...   961
      Slot 2  the funding fade .... FAILED 4 of 5 ... 1,040
      Slot 3  the mood fade ....... FAILED 3 of 5 ... 1,017
      (holding the coins: about 730 to 745)
    THE COMBINED RULE - one look at 113 unseen days: 1,000 to 1,107 on 25
      trades. NOT PROOF. Frozen (`signals/confluence.py`).
    THE PAPER-WATCH - built 2026-11-17, first run that day: 26 paper
      signals open, all sells, nothing ended yet.

**THERE IS NO SLOT LEFT AND NO FOURTH. THE HOLD-OUT (2025-10-01 TO
2026-07-25) AND FORWARD CHECK 1's WINDOW (TO 2026-11-15) ARE SEEN PERIODS
FOR EVERY RULE THIS SHIP WILL EVER WRITE.** A failed idea, or a changed
one, may be watched forward on paper and nowhere else (his ruling,
2026-11-16).

## The paper-watch, in ten lines

  * `journal/paper_watch.py`; its store and ledger are `journal/paper/`.
  * Thirteen coins - **his: "ok add 13 coins its done"** - BTC ETH SOL
    XRP BNB DOGE NEAR UNI LINK AVAX ADA AAVE BCH. The original three are
    also shown apart.
  * Two rules, frozen, CALLED from `signals/confluence.py`: the combined
    rule and the trend alone (its yardstick).
  * Every signal is written ONCE and followed TWICE from the same entry:
    the fixed stop and target (1.5 and 3.0 ranges), and a trailing stop
    (3.0 ranges behind the best close). **His own idea**: "on fix stop
    trade stop at this and theer is a section which also worke on the
    trailing stop so in 6 months we have complete report".
  * The main score is every signal at the same 1% of a pretend 1,000.
    A second "portfolio" line shares a 4% limit among a day's signals -
    **way B, his yes: "ok option b is done"**. The 4% is NOT final: "we
    can tweek the risk factor later".
  * Every file is append-only. Every run works the WHOLE record out again
    from the store and writes nothing if a written row does not come out
    identical (INTEGRITY ALARM).
  * A day worked late is written and labelled LATE with its hours.
  * `PAPER_WATCH.bat` - a run, the report in Notepad. `PAPER_WEEK.bat` -
    the week's numbers. `run_daily.bat` runs it after the grader.
  * `python journal/paper_watch.py --report` and `--week` read only.
  * **NO MONEY. IT HOLDS NO KEY AND SENDS NO ORDER. DO NOT GIVE IT
    EITHER.**

**DO NOT CHANGE ONE NUMBER IN IT OR IN THE RULES.** A changed number is a
different record: the ledger carries a stamp of every setting and the
next run will raise INTEGRITY ALARM. That alarm is the tracker working.
**IF A SETTING MUST CHANGE (HE MAY CHANGE THE 4%, WHICH IS NOT IN THE
STAMP), IT IS A NEW RECORD FROM A NEW START DAY, DECLARED IN A BAR FIRST.**

## >>> YOUR FIRST JOBS, IN ORDER

**(GATE 7.1 IS NOW 118 CHECKS, NOT 106: THE CLOUD's RECORD AND THE COMPARISON WERE ADDED LATE THE SAME NIGHT. WHERE THIS FILE SAYS 106, READ 118.)**

**1. PROVE THE SHIP ALIVE - THIRTY-EIGHT INVOCATIONS.** The thirty-six of
the table below plus `journal/paper_watch.py --gate` twice (normal and
`TZ=UTC0`; about 75 seconds each). Then `python journal/paper_watch.py
--report`: it must say no INTEGRITY ALARM and not OFFLINE. **IF IT SAYS
ALARM, THAT IS YOUR SESSION. DO NOT "FIX" THE LEDGER BY HAND; FIND WHAT
CHANGED (`git log -p journal/paper/`, the code, the Python).**

**2. COMMIT WHAT THE LAPTOP TASK WROTE.** `journal/paper/*.csv` will be
modified in `git status` whenever his daily task has run: that is the
tracker's work, not yours. `git pull` FIRST, then commit those files on
their own, labelled, and push. **NEVER RUN THE TRACKER ON A CHECKOUT THAT
IS BEHIND `origin`**: it appends, and two different appends to one file
is a conflict in a record that must never be edited by hand.

**3. THE CLOUD - DONE THE SAME NIGHT, ON HIS ORDER ("ok setup teh clod
thing and made a separe record file for clod only and one for laptop
record holder"). READ ITS FIRST SCHEDULED RUNS.**

    TWO RECORDS, NEVER ONE FILE WITH TWO WRITERS:
      journal/paper/         THE LAPTOP's. `python journal/paper_watch.py`
                             (his daily task, `PAPER_WATCH.bat`). Funding
                             from `fapi.binance.com`.
      journal/paper_cloud/   THE CLOUD's. `python journal/paper_watch.py
                             --cloud`, run ONLY by
                             `.github/workflows/paper_cloud.yml` at 00:07,
                             01:07 and 03:07 UTC. Funding from
                             `www.binance.com/fapi/v1/fundingRate`.
    **NEVER RUN `--cloud` ON THE LAPTOP AND NEVER LET THE CLOUD JOB WRITE
    `journal/paper/`.** Either makes two writers of one record.

    WHY TWO DOORS: `fapi.binance.com` refuses GitHub's machines (HTTP
    451, measured). Binance's website host serves them the same rows
    (12,870 of 12,870, then a whole file byte for byte). **IT IS NOT A
    DOCUMENTED DOOR AND BINANCE CAN SHUT IT.** He was told and ordered
    it. If it shuts: funding "not updated" in the cloud's report, then
    the two records DISAGREE - tell him plainly; the choices are another
    funding source for the cloud (OKX answers; it is NOT Binance's data,
    so that is a NEW record) or a small machine outside the United
    States. HIS.

    EACH REPORT SAYS WHETHER THE TWO RECORDS AGREE (under HEALTH). At the
    end of the session: 26 of 26 rows. **THE CLOUD SEES THE LAPTOP's
    RECORD ONLY AS LAST COMMITTED, SO COMMIT `journal/paper/` WHEN YOU
    ARRIVE (job 2) OR THE COMPARISON IS OLD.**

    THE CLOUD JOB ENDS RED - GitHub e-mails him - on INTEGRITY ALARM,
    OFFLINE or DISAGREE. The report is committed first:
    `journal/paper_cloud_report.txt`, `journal/paper_cloud_week.txt`.
    `PAPER_CLOUD.bat` shows it on the laptop.

    **NOT ONE SCHEDULED RUN HAD HAPPENED WHEN I LEFT** (the first was due
    2026-11-18 00:07 UTC). `git log --oneline -- journal/paper_cloud/`
    tells you whether they came, and when. The cloud's first rows were
    17 hours late; its first ON TIME row can only come from a scheduled
    run. **IF THERE ARE NO COMMITS BY "zarx-cloud-watchman" WITH "paper-
    watch" IN THEM AFTER 2026-11-17, THAT IS YOUR SESSION.**

    `journal/cloud_probe.py` and `paper_cloud_test.yml` are the read-only
    probe that measured all this. It runs only when pushed or by hand.

**4. HOW HE IS TOLD.** He asked: "ok but how i will know about briefs and
signals?" Four ways were put to him; I recommended a Telegram message
from the cloud job - one when a signal or an ending happens, a short
summary each morning. **HE HAS NOT ANSWERED. ASK ONCE.** If Telegram:
**THE BOT's SECRET CODE IS HIS TO CREATE AND TO TYPE INTO GITHUB's
SETTINGS HIMSELF. YOU GIVE HIM THE CLICKS; YOU NEVER SEE OR HANDLE THE
CODE.**

**5. A PAPER LINE ON HIS BRIEF** - open paper trades and each record's
score. It touches `cockpit/brief.py`, which he reads: bar first, and
prove with `git` that nothing else on the Brief moves.

**6. THE WEEKLY AUTOPSY.** He asked for one every week: "a complete
autopsy detailed of what happened what we can do better". The numbers
are `PAPER_WEEK.bat`. The reading is yours, when he says "weekly
autopsy": plain words, dollars, what the winners and the losers had in
common. **WHAT COULD BE BETTER IS COLLECTED, NOT ACTED ON.** He was told:
changing a rule each week because of the last few trades is tuning to
luck; the notes pile up and are looked at together at the first review
(about 30 trades a record, or three months).

## What to keep saying to him

  * **26 SIGNALS ON THE FIRST DAY ARE ONE BET.** Both rules sold all
    thirteen coins. If the market bounces they lose together. It will
    say nothing about the rules either way. Read the "days" column.
  * **EVERYTHING SO FAR WAS TESTED WHILE PRICES FELL**, and in all of it
    selling beat buying. A rule must be seen in a rising market too.
  * **MONTHS, NOT WEEKS.** No real money.
  * **THE TRAILING STOP IS A SECOND RECORD.** The ship's own calculator
    says of Zargul 2.0 that a trailing stop "cut winners and kept
    losers". He has been told once; say it again when the first
    comparison appears.

## THE "BEFORE REAL MONEY" LIST - HE ASKED FOR IT TO BE WRITTEN DOWN

It is in `PROGRESS_LOG.md` (2026-11-17, evening, section 5), ten points,
and in his own document "Zar X - Advice After Idea 1". **KEEP IT. NONE OF
IT IS NEEDED FOR PAPER TRADING; ALL OF IT BEFORE A DOLLAR MOVES.**

## WHAT IS PARKED, BY HIM

  * **THE CHANGED BREAKOUT** ("with the big trend only, no chasing, let
    winners run"). He heard both sides and ordered the build without it.
    If he wants it later: its exact rules in a bar first, a NEW record
    from its own first day. **IT WAS DESIGNED BY LOOKING BACK AT SLOT 1's
    72 TRADES. FORWARD ONLY, FOR EVER.**
  * **4-HOUR CANDLES.** The combined rule cannot run on them (its mood
    reading exists once a day). Only the changed breakout would.

---

# **>>> THE COMMANDS YOU MUST NOT TYPE**

    python lab/gauntlet.py --slot 1 --go
    python lab/gauntlet_slot2.py --go
    python lab/gauntlet_slot3.py --go
    python lab/forward_check.py --go

**ALL FOUR ARE SPENT AND REFUSE. DO NOT TYPE ANY OF THEM "TO WATCH IT
REFUSE".** The refusals are proved by the gates. `--gate` on any file is
safe.

**AND DO NOT OPEN `lab/vault/`, `lab/funding_vault/*.csv`,
`lab/mood_vault/fear_greed.csv` OR `lab/forward_vault/` "TO HAVE A
LOOK".** They are checksummed evidence; never edit, re-save or re-fetch.

**WHAT HAS BEEN LOOKED AT, IN BOLD AS THE RITUAL ASKS: ALL THREE SLOTS'
RESULTS ON THE HOLD-OUT - THE REPORTS AND THE SAVED TRADE FILES, WITH
ENTRY AND EXIT PRICES AND DAYS. SLOT 3's ENTRY DAYS ARE THE DAYS THE
HOLD-OUT MOOD WAS EXTREME, AND A NEWS SEARCH QUOTED INDEX READINGS FOR
OCTOBER-NOVEMBER 2025. THE FROZEN FILES THEMSELVES WERE NOT OPENED BY
EYE. FORWARD CHECK 1's WINDOW: ITS RESULT AND SIX TRADE FILES. SINCE
2026-11-16: THE FIRST PAPER RUN's 26 SIGNALS (THE 17th's OPENING PRICES
FOR THIRTEEN COINS). A YEAR OF BINANCE FUTURES CLOSES FOR ABOUT SIXTY
COINS AS CORRELATIONS AND AVERAGES ONLY.**

---

# THE SHIP'S GATES

    cockpit/fear_greed.py       GATE 3.1-R7   58     cockpit/funding.py   GATE 3.2-R8   71
    data/open_interest.py       GATE 3.2b-R10 88 x2  data/collection_guard.py  PASSED (no ticks)
    cockpit/news.py             GATE 3.3      54     cockpit/events.py    GATE 3.4      69 x2
    cockpit/whales.py           GATE 3.5     111 x2  cockpit/carry.py     GATE 4.1      87 x2
    journal/log_trade.py        GATE 5.1     101 x2  journal/mirror.py    GATE 5.2      84 x2
    signals/turtle.py           GATE 6.2-S    39 x2  lab/gauntlet.py      GATE 6.4-R    49 x2
    lab/funding_vault.py        GATE 6.3-D    52 x2  signals/funding_fade.py GATE 6.3-S 44 x2
    lab/gauntlet_slot2.py       GATE 6.3-R1   40 x2  lab/mood_vault.py    GATE 6.5-D    42 x2
    signals/mood_fade.py        GATE 6.5-S    45 x2  lab/gauntlet_slot3.py GATE 6.5-R   39 x2
    signals/confluence.py       GATE 6.6-S    30 x2  lab/forward_check.py GATE 6.6-F    34 x2
    journal/paper_watch.py      GATE 7.1     106 x2
    vault INTACT 6 of 6 - frozen funding INTACT 3 of 3 - frozen mood INTACT 1 of 1 - Brief 3/3

**THIRTY-SIX WERE MEASURED 2026-11-17 08:47 UTC: 2,091 GREEN, 0 RED. THE
THIRTY-EIGHT HAVE NOT BEEN MEASURED TOGETHER. MEASURE THEM.**

**HOW EACH IS RUN:** `cockpit/fear_greed.py`, `cockpit/funding.py` and
`data/open_interest.py` take no flag; every other gate takes `--gate`;
"x2" is once on the normal clock and once with `TZ=UTC0`. The verifiers
(`lab/verify_vault.py`, `lab/funding_vault.py`, `lab/mood_vault.py`,
`cockpit/brief.py`) take none. `lab/gauntlet_slot2.py --gate` and
`lab/gauntlet_slot3.py --gate` take two to three minutes each;
`lab/forward_check.py --gate` five. **THE THREE GAUNTLET GATES RUN GREEN
WITH ALL THREE SLOT MARKERS IN `lab/results/`** - measured at the end of
the session, after the last slot was spent (49, 39 and 40 checks, 0 red;
the three vault verifiers INTACT).

**YOUR WORD-HITS WILL BE:** the funding gate's prose ("escaped the gate
of 2026-07-26" - **IT HAS NOW FOOLED FOUR COUNTERS**), a wrapped sentence
in the open-interest gate that begins "fail. B9 is now a REAL TEXT
EDIT", the drill headings, and the gauntlet gates' rehearsals, which are
SUPPOSED to print `FAILED` and `REFUSED`. `data/collection_guard.py`
prints no tick marks: read its verdict line.

**IF YOU MEASURE IN TWO STREAMS AT ONCE, AS I DID, SAY SO.** Nothing went
red; had something, I could not have said why.

## What I did, in twelve lines

1. Measured the ship alive: 36 invocations, 2,091 green, 0 red.
2. **Ran Slot 1 once on his word: FAILED.** Obituary, autopsy, research.
3. Broke Slot 1's 72 trades down in hindsight when he asked what made
   the winners and the losers; told him it is a hint, not a finding.
4. Wrote him a document of the advice (a Claude document of his own,
   "Zar X - Advice After Idea 1"; not in this repo).
5. **Ran Slot 3 once on a reading of his words: FAILED.** The same three.
6. Measured about sixty Binance coins; he chose thirteen.
7. Put three ways to handle many signals in one day; he chose way B.
8. He proposed both exits side by side and a weekly autopsy.
9. Declared the paper-watch's bar and committed it alone (`2cb1171`).
10. Built it; its gate found eight faults in itself on the way to 106
    green; attacked it with 30 edits (28 red, 1 harmless, 1 not run).
11. First real run: 26 paper signals, all sells, all 16 hours late.
12. He asked for the cloud and how he will be told. Both are yours.

**R-094 IS MY LIST AGAINST ALL OF IT - TWENTY-TWO ITEMS.** If you are not
Fable and he lets you, attack `journal/paper_watch.py` before anything is
built on it. Start with item 1: the trailing exit has no witness but my
own hand cases.

---

# THE RULINGS YOU CARRY

**>>> THE NEWEST, ALL 2026-11-17, IN HIS WORDS:**

    "Yes, skip it" ........... the attack on Fable's builds of the 16th
    "Yes, run idea 1" ........ Slot 1. Spent.
    "first do you last idea test" ... read as Slot 3. Spent. (R-094, 20)
    "ok add 13 coins its done"
    "our main goal is through paer trading that is the system is doing
     the job and we can tweek the risk factor later"
    "ok option b is done"
    both exits side by side, and a weekly autopsy (his own proposal)
    "add those in the system then we will talk" ... the build order;
        the changed breakout not in it
    "if we can also do it on cloud it will be great" ... the cloud move

**AND THE STANDING ONES:**

  * **A BUILD MADE BY FABLE IS NOT ATTACKED BY THE NEXT SESSION**
    (2026-11-14). You may not take that from this file: **ask him one
    line** - *"The last builds were made by Fable. Do I skip attacking
    them, as you ruled?"* If he says no or does not answer, attack them:
    R-088 to R-094.
  * **NO OTHER MODEL CHECKS WHAT FABLE BUILDS, PHASE 6 INCLUDED**
    (2026-11-15). R-006 is WAIVED for Fable's builds, not cleared.
  * **AFTER A FAIL** (2026-11-16): a plain-words autopsy; a research pass
    outside the ship; and the idea, or ONE changed version of it, may be
    watched on paper. No re-test on old data, ever. **`README.md` AND
    `SHIP_LAWS.md` LAW 6 STILL SAY A FAILED IDEA IS FINISHED. THEY ARE HIS
    ALONE TO AMEND; proposed words are in the log of 2026-11-16. WHERE
    THEY DISAGREE WITH HIS RULING, ASK HIM - DO NOT PICK.**
  * **THE GAUNTLET's COSTS ARE HIS REAL BINANCE FEE** (0.05% a side, and
    0.05% slippage). The paper-watch charges the same.

**WHAT THAT MEANS FOR YOU, WHOEVER YOU ARE:**

    HE HAS SAID IN WORDS THAT YOU ARE FABLE
      -> you may carry on under his rulings. **FILE MORE AGAINST YOURSELF,
         NOT LESS.**
    HE HAS NOT SAID IT
      -> **YOU ARE AN ORDINARY ZAR X SESSION, AND YOU ARE THE SECOND MIND
         THE PAPER-WATCH NEVER HAD.** If he lets you, attack it first.

---

**THE SECTIONS BELOW THIS LINE ARE CARRIED OVER WORD FOR WORD FROM THE
ORDERS OF 2026-11-16. WHERE THEY SPEAK OF SLOTS "UNSPENT", OF "WHICH TEST
TO RUN" OR OF THIRTY-TWO INVOCATIONS, THE TOP OF THIS FILE IS THE TRUTH:
EVERY SLOT IS SPENT, THE SHIP IS THIRTY-EIGHT INVOCATIONS.** On his desk,
item 1 ("which test to run") is DONE; add to that list: the cloud move
(said yes), how he is told (unanswered), the 4% limit (not final), the
changed breakout (parked), a one-page plain "where we are" (suggested; a
tenth file, so it needs his word), and a walk-through of `LOG_TRADE.bat`
and `MIRROR.bat` with one practice trade (offered twice, still owed).

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
(j) **TELL YOUR GATE HOW MANY CHECKS IT OWES.** The seven newest do
    (log_trade, mirror, turtle, gauntlet and the three 6.3 gates). The
    other seven do not (R-070).
(k) **A FAILING GATE MUST STILL BE ABLE TO FINISH REPORTING — AND YOU MUST
    PROVE IT.** R-084 is this rule broken in a gate that had been measured
    as keeping it, on a different shape. **Read every file through a helper
    that survives the file not being there.**
(l) **A CLAIM ABOUT WHAT CANNOT BE TESTED IS A PERMISSION SLIP.** Try it.
(m) **A CLAIM STATED IN BOLD IS STILL ONLY A CLAIM. WRITE YOUR PREDICTIONS
    DOWN BEFORE YOU RUN.**
(p) **>>> NEW, EARNED 2026-11-16 (EVENING): A REPAIR TO A CHECK IS A CHANGE
    TO A CHECK. PROVE THE REPAIRED CHECK CAN STILL GO RED.** I repaired a
    word search through a shell here-document; the shell ate two
    backslashes; the search then matched nothing and the check was green
    for ever. Two green gate runs followed it. **AND IN A TEXT-EDIT ATTACK,
    "NO VERDICT LINE" IS ITS OWN RESULT: five of my 68 edits ended in a
    traceback, which is rule (k) broken, not a catch.**
(o) **>>> EARNED 2026-11-16: WHEN A HAND CASE PINS A TURNING POINT,
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
- **`lab/funding_vault/` AND `lab/mood_vault/` ARE CHECKSUMMED EVIDENCE.** Never edit, re-save,
  re-fetch or "tidy" it. Git is told not to touch a byte (`* -text`).
  `lab/build_funding_vault.py --freeze` REFUSES a second run; leave it
  refused.
- **MY ATTACK AND MADE-UP-WORLD SCRIPTS LIVED IN A SCRATCH FOLDER OUTSIDE
  THE REPO AND ARE GONE.** What they did is in `PROGRESS_LOG.md`
  2026-11-16, both accounts, edit by edit. To repeat the attack: one
  fresh copy of `config.py`, `risk/`, `regime/`, `indicators/`, `signals/`,
  `vendor/` and `lab/*.py` per edit, **with no `lab/vault/`, no
  `lab/funding_vault/` and an empty `lab/results/`**, control first.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

**>>> THE NEWEST, 2026-11-16: "NOT YET - DO IDEA 2"**, and then, the same
day, *"fable set up idea 2 and do it smartly"*. Slot 2 is set up. **He has
NOT been asked which candle, which numbers or which exit Slot 2 uses: I
chose them, and they are R-090 items 2 to 8.** If he asks, show him.

**>>> BEFORE THAT, 2026-11-16: SLOT 1 IS A 4-HOUR TEST.** His choice, from
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

1. **WHICH TEST TO RUN, AND WHEN.** "Not yet" (2026-11-16), then his order
   to fix the fee and Slot 1's exit and build idea 3. **The order he was
   told and did not object to: settle idea 3 first, then test one at a
   time - idea 2, idea 1, idea 3. EACH RUN NEEDS HIS WORD AT THE TIME.**
   (Risk: the ship's rule, 1% with the 25% cap. With Slot 1's new stop
   and on Slot 2's daily candles the cap does not bind on made-up
   markets: each trade risks exactly 1%.)
2. **SLOT 3: SETTLED 2026-11-16.** Re-specified once, by him, as the
   crowd-mood fade; built; unspent. **THE ONE CHANGE IS USED. SLOT 3
   CANNOT BE CHANGED AGAIN.**
3. **THE THREE CHOICES I MADE IN THE NEW BUILD - HE RULED ON ALL THREE,
   2026-11-15, AND KEPT THEM. DO NOT ASK AGAIN.** A wrong-side stop is
   refused; the 1% lines keep his real exit; a reading older than 8 hours
   counts as no reading.
4. **THE CARRY LINE: ANSWERED 2026-11-16.** His words: *"carry line i think
   daily brief"*. **Fable's reading, labelled as a reading: information,
   part of the Brief, not a suggestion.** Off his desk unless you doubt
   the reading - then ask once, in plain words.
5. **AND BESIDE IT:** the carry figure is the yield on the PERP NOTIONAL;
   running the trade needs money on both legs, so the return on capital
   deployed is lower than the number on the line. His call.
6. **R-070 — SEVEN GATES DO NOT KNOW THEIR OWN COUNT** (the seven newest
   do). One line
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
3. **`PROGRESS_LOG.md`, the entries of 2026-11-16 - ten of them. The last
   four are the idea 3 finding-out, the candidate, Slot 3's bar and its
   account** — Slot 1's 4-hour
   bar and account, then Slot 2's bar and account (the last two in the
   file) — and the Phase 6 entries of 2026-11-15 they stand on.
   **The file is ~1 MB; do not read it all.**
4. **`PROGRESS_LOG.md` 2026-07-26, Gate 2.5** — the day the Lab was shown a
   leak it could not see. **This is the entry Phase 6 stands on.**
5. **`lab/engine.py`, `lab/dummies.py`, `lab/leak_check.py`**, and the
   production halves of `signals/funding_fade.py` (25 lines),
   `lab/funding_vault.py` and `lab/gauntlet_slot2.py`.
6. **`REVIEW_QUEUE.md`: R-006, then R-084 to R-093.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** And check your commit hashes again after you push.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **THE `.py` FILES AND THE FIVE DOCUMENTS ARE CRLF** (except
  `cockpit/plan.py` and `journal/snapshot.py`, which are LF). **A file
  written by an editor tool arrives as LF on this machine.** Write to a
  scratch file and install it with a script that converts and REFUSES a
  bare LF. Judge line endings in the WORKING TREE, never against
  `git show HEAD:<file>`, which hands back LF.
- **>>> NEVER EDIT A REPO FILE WITH `sed -i`.** It rewrote all 807 line
  endings of a file to LF and did not make the change it was asked
  for (2026-11-16). Edit a source copy and install it through a script
  that refuses a bare LF.
- **>>> NEVER PASS A SCRIPT TO THE SHELL AS A HERE-DOCUMENT - LONG OR
  SHORT.** One broke a shell on 2026-11-16 (morning); one silently ate
  the backslashes out of a gate repair that evening and left a check
  blind, after I had read this same warning twice. **Write the file with the editor tool; run the file.**
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
                            NOT clear R-084 to R-093 unless you attacked
                            them; you may never clear R-006.**
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the
                            truth. Keep the old markers below it.
    4. ROADMAP.md ......... tick what shipped; add what you MEASURED.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words
                            brief. **SAY IN THEM, IN BOLD, WHETHER ANY
                            VAULT DATA OR ANY HOLD-OUT FUNDING RATE HAS
                            BEEN LOOKED AT. IF A SLOT WAS RUN, SAY WHICH,
                            AND ITS VERDICT, IN THE FIRST LINE.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what
       held, **what you got wrong**, and what decision is his. **If he says
       he does not understand the options you gave him, the options were
       written badly. REWRITE THEM, DO NOT EXPLAIN THEM HARDER.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly", "I believe" or "this should be fine" about anything that ships —
FILE IT in `REVIEW_QUEUE.md` before the commit that ships it.**
