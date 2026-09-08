# ZAR X — **YOUR JOB 1 IS TO ATTACK GATE 5.1-R2, WHICH I BUILT TODAY AND NOBODY ELSE HAS EVER LOOKED AT. I FOUND THE FAULT AND I WROTE THE FIX. THAT IS R-080, AND ONLY A SESSION THAT DID NEITHER MAY CLEAR IT.**

*Written 2026-09-08 by the twenty-sixth generation, which attacked both of the
twenty-fifth's repairs, cleared five items, found a hole beside one of them —
**the seven interactive questions no gate had ever reached** — and repaired it
on the Commander's ruling of SERIOUS. **I hold no exemption. I wrote none for
you. Only he grants one, and only out loud.***

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **ATTACK GATE 5.1-R2, check (n).** Invent breaks
                            I never imagined. That is R-080 and R-081, with
                            R-070, R-071, R-073, R-074 and R-075 still open
                            behind them.
                   PART 2 — **BUILD `journal/mirror.py`** (Phase 5, second
                            half) — **ONLY IF PART 1 PERMITS IT, AND ONLY
                            AFTER YOU HAVE DECLARED GATE 5.2 AND COMMITTED
                            IT ALONE, WITH NO CODE IN THAT COMMIT.**

**PART 2 IS CONDITIONAL AND THE COMMANDER DECIDES, NOT YOU.** If Part 1 finds
something, **fill in THE FINDING REPORT in `THE_PATTERN.md` BEFORE repairing
anything**, then: SERIOUS -> fix it and stop. BORDERLINE -> report and stop,
he rules. SMALL -> file it CATEGORY B and carry on to Part 2.

**"I ATTACKED IT HARD AND FOUND NOTHING" IS A SUCCESS. SAY IT PLAINLY AND
CLEAR R-080 AND R-081.** **>>> THE MIRROR HAS NOW WAITED THREE SESSIONS.** Do
not manufacture a defect — a stretched finding costs him a fourth.

**>>> AND THE TEST HE GAVE ME, IN HIS OWN WORDS, WHICH NOW APPLIES TO EVERY
FINDING ON THIS SHIP:** *"our actual goal is to make a correct thing in actual
real environment. so those things which cant be done in actual scenarios at
those we have to ignore those."* **He is not loosening the checks.** He asked
me directly *"who will swap those questions other than me? if any 3rd party
can do it"*, and the honest answer — no third party can, he would not, **but a
later session will, and three have edited that file in three weeks** — is what
earned the repair. **Answer that question about YOUR finding before you grade
it.**

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
    journal/log_trade.py        GATE 5.1-R2   PASSED  exit 0  0 red   77 green
      the same file at TZ=UTC0  GATE 5.1-R2   PASSED  exit 0  0 red   77 green
    vault INTACT 6 of 6 · Brief 3/3 (Whale watch 6 of 6) · lab/ untouched
    journal/my_trades.csv DOES NOT EXIST — his first real trade creates it

**>>> ONE COUNT CHANGED TODAY: log_trade 70 -> 77.** Everything else is
exactly where you find it above. **If you measure something different, it is
not a rounding error.**

**PHASE 4 IS COMPLETE. PHASE 5 IS STILL HALF BUILT — THE MIRROR DOES NOT
EXIST.**

## What I did, in eight lines

1. **Proved the ship alive first** — fourteen invocations, **1,033 green, 0
   red**, counted by machine three ways and every one of the 38 word-hits read
   by eye. **The funding gate's "escaped" trap did not fool me because these
   orders named it. Keep naming it.**
2. **Attacked GATE 3.5-R2 with two new sabotages, control first.** Both
   CAUGHT. **My best one — the PRODUCTION doorway losing its timeout — walked
   through all four new checks exactly as I predicted, and check (e) caught
   it.** The repair did not catch my attack; an older check did.
3. **Attacked check (m) with a fourth fault and re-ran the three it was built
   for.** All caught, at the exact counts predicted. **And I forced R1-R6 red
   one at a time — the first time any of that check's failure paths had ever
   been executed.**
4. **>>> ONE THING ESCAPED, AND IT WAS BESIDE THE REPAIR, NOT INSIDE IT.** The
   seven `input()` questions. The file called them unreachable; **that was a
   claim nobody had run and it was false.**
5. **MY FIRST WHALE RIG'S CONTROL FAILED 3 RED** — I copied the file one folder
   too shallow. **I threw the whole run away and rebuilt it. R-076's lesson,
   learned again by me.**
6. **MY FIRST WITNESS WAS BLIND.** It piped seven lines down a pipe, **and a
   pipe does not read a prompt**, so the archive came back correct and it
   proved nothing. Rebuilt under `-u`, reading each prompt.
7. **He ruled SERIOUS.** Declared GATE 5.1-R2, committed the bar ALONE
   (`88a183c`, 317 lines, no `.py`), built check (n): **70 -> 77.** The same
   edit that printed `PASSED — 70 checks, 0 red` now prints `FAILED — 1 red
   of 77`.
8. **FIVE ITEMS CLEARED — R-072, R-076, R-077, R-078, R-079.** **THE CATEGORY
   B PILE IS FORTY-SEVEN.** I could not clear R-080; it is mine.

---

# **JOB 1 — ATTACK GATE 5.1-R2, CHECK (n) (R-080 AND R-081)**

## WHAT THIS INSTRUMENT IS FOR — Q1, ANSWERED FOR YOU

**The rows in `journal/my_trades.csv`** — his own record of closed trades, in
his own words. **It is an ARCHIVE and the Mirror will grade him on it. Nobody
re-types a trade they logged in March.** Check (n) guards **the only surface
between his fingers and that archive**: the seven questions the shell asks.

## WHAT CHECK (n) DOES — `journal/log_trade.py` from line 1167

A child interpreter runs a **byte copy** of the module as `__main__`, under
**`-u`**, in a tree of its own, with **no `path` and no `now`**. A reader on
the child's stdout answers **the question that was asked**, recognised by
words the gate types out.

    N1 the shell was RUN, not read, and the child finished ON ITS OWN
    N2 all seven questions asked and recognised BY THE GATE'S OWN WORDS
    N3 seven DISTINCT answers, none sent by counting, none sent twice
    N4 the answer typed at `price you got IN at` is in the `entry` column,
       and the one typed at `price you got OUT at` is in `exit` — the column
       found by a header name THE GATE TYPES OUT
    N5 and every other answer in its own column, including his own words
       WITH A COMMA IN THEM
    N6 the screen and the notebook agree
    N7 the judge proved able to SAY NO, in the same run, four ways

### >>> WHERE I SAY I DID NOT LOOK — A STARTING POINT, NOT A LIST TO TICK

1. **>>> MY DECLARED BAR WAS SHARPER THAN THE THING I BUILT AND I ONLY FOUND
   OUT BY RUNNING IT.** Edge case E4 promised that closing the child's stdin
   after the seventh answer makes an eighth question fail FAST. **It only does
   when the extra question comes AFTER all seven.** Mine went before the last
   one and **the 60-second deadline is what actually saved the gate.** **THIS
   IS THE ONE I WOULD ATTACK FIRST: find a shape of this check that the
   deadline does not save.**
2. **THE DRILL CANNOT REACH CHECK (n)**, for the same reason it cannot reach
   check (m). **It is certified by attack and by nothing else.**
3. **N4 AND N5 BOTH STAND ON `n_at`, SO A FAULT IN IT IS INVISIBLE TWICE.**
   N7 exists to prove `n_at` can say no — **and N7 calls the same `n_at`.**
   R-078's doubt 3, reproduced knowingly.
4. **CHECK (n) DRIVES ONE HAPPY TRADE.** No refusal is ever driven through the
   seven questions.
5. **I DID NOT PLANT A COMPETING `journal/log_trade.py` ON THE CHILD'S PATH
   AND WATCH N1 GO RED.** A positive control I did not build, now missing from
   two checks instead of one.
6. **THE 60s AND 15s NUMBERS ARE JUDGEMENTS.** The healthy child answers all
   seven in under two seconds here. **Nobody has run this on a loaded machine.**
7. **IT READS THE CHILD ONE BYTE AT A TIME OVER A PIPE ON WINDOWS**, and has
   never run anywhere else.

## RE-RUN MY FAULTS. IF ANY FAILS TO GO RED, THE REPAIR IS DECORATIVE.

Install as **TEXT EDITS** in copies outside the repo, **control first**.

    journal/log_trade.py, in the SHELL, the two price questions exchanged
      whole (both lines, prompt and position together)
        expect 1 red — N4, and N4 alone. **N6 STAYS GREEN AND THAT IS
        CORRECT: the screen and the notebook are wrong TOGETHER, which is
        exactly what made this invisible to a human.**
    an EIGHTH question inserted before the last one
        expect 5 red — N1, N2, N4, N5, N6 — and the run takes ~78 seconds
    `price you got IN at` renamed to `entry price`
        expect 5 red — the same five, ~78 seconds

**AND THE FOUR FROM THE GENERATION BEFORE ME, WHICH I RE-RAN AND WHICH STILL
GO RED:** the `_stamp` clock relabelled (1 red, R4), frozen at 2020 (1 red,
R4), `TRADES_FILE` renamed (4 red), and `_get`'s `timeout=timeout` dropped in
`cockpit/whales.py` (2 red, S1 and S2, **S3 still green**).

**>>> THE `_stamp` ANCHOR STILL MATCHES TWICE** — the drill's `_stamp_local`
copies the production line character for character at a deeper indent. **Put a
CRLF on the front of your anchor and it matches once. Make your writer REFUSE
rather than replace both.**

## WHAT PART 1 LOOKS LIKE

1. Write the bars for "this review clears" into notes **before running
   anything**, and **name your candidate attacks there.**
2. Invent at least one **NEW** sabotage, in scratch copies **outside the
   repo**. **Run the untouched control too.**
3. **>>> YOUR SCRATCH COPY MUST SIT AT THE SAME DEPTH AS THE REAL ONE.**
   `cockpit/whales.py` needs `<tree>/cockpit/whales.py` because check (k)'s
   child runs `import cockpit.whales` from the tree's root; `log_trade.py`
   needs `<tree>/journal/`. **MY CONTROL FAILED 3 RED BECAUSE I GOT THIS
   WRONG, AND A FINDING ON A RIG WHOSE CONTROL FAILS IS NOT PROVEN.**
4. **>>> NEVER RUN A WITNESS AND A GATE AGAINST THE SAME COPY.**
5. **PROVE YOUR WITNESS CAN SEE THE FAULT BEFORE YOU BELIEVE ITS VERDICT.**
   **>>> AND THE NEW ONE, EARNED TODAY: A PIPE DOES NOT READ A PROMPT.** If
   you are testing anything a human answers, drive it under `-u` and reply to
   the words on the screen. Feeding a list of answers down a pipe tests
   POSITION and nothing else, and it will tell you a real fault is not there.
6. **MAKE EACH CHECK FAIL AND SEE WHETHER THE GATE CAN STILL REPORT.**
7. Confirm `git status` is clean afterwards.
8. **Write it up either way**, and record verdicts in `REVIEW_QUEUE.md`.

**YOU MAY CLEAR R-080 AND R-081** — you built neither. **YOU MAY NOT CLEAR
R-070, R-071, R-073, R-074 or R-075.**

---

# **JOB 2 — ONLY IF JOB 1 PERMITS: `journal/mirror.py` (PHASE 5, SECOND HALF)**

**A half-built Mirror is worse than no Mirror. If you run short, do Part 1
properly and leave Part 2 entirely.**

## >>> GATE 5.2 DOES NOT EXIST. YOU DECLARE IT, AND YOU COMMIT IT ALONE.

**Declare GATE 5.2 in `PROGRESS_LOG.md`, commit it with NO `.py` in that
commit, and only then write code.** `git show --stat` is what proves the bar
came first. **I did this once today and the repair went in first time, because
the bar named twelve edge cases before any code existed — and one of those
twelve turned out to be half wrong, which I only discovered by running it.
NAME THEM ANYWAY. A bar you can be proved wrong against is worth more than one
you cannot.**

**WHAT THE PLAN ASKS** (`EXECUTION_PLAN.md` Phase 5, item 2): monthly, the
Commander's logged trades vs what the instruments said at those moments (from
`journal/snapshots_*.csv`) vs what a disciplined 1%-risk version of the same
trades would have done. **Output: plain-words report. No shaming, arithmetic
only. NEVER a signal.**

**FIVE THINGS YOU WILL MEET ON YOUR FIRST AFTERNOON:**

  * **>>> THE TWO FILES DISAGREE ABOUT WHAT A TIME LOOKS LIKE. THAT IS R-074.**
    `my_trades.csv` writes `2026-09-08T09:30:15+00:00`; **every snapshot row
    since Phase 2 says `2026-07-21 11:35` with no zone at all.** Decide the
    reconciliation deliberately and **write it down BEFORE coding.**
  * **>>> AND NOTE WHAT CHANGED TODAY: THE SEVEN QUESTIONS ARE NOW UNDER A
    CHECK.** Reorder them freely — that is not a fault and check (n) does not
    mind. **RENAME one, or ADD an eighth, and the gate goes RED, on purpose.**
    If the Mirror needs a risk figure and you decide to ask for it, **teaching
    check (n) the new question is one deliberate line in `N_ASK`** — made by
    somebody who has looked, which is the entire point.
  * **THE ASSET NAMES WERE MADE TO MATCH ON PURPOSE.** `log_trade.py` stores
    `BTC-USD`, the same string every snapshot row uses. **No translation table.**
  * **`journal/my_trades.csv` MAY NOT EXIST WHEN YOU ARRIVE**, and that is
    correct. **A Mirror that crashes on an empty journal greets him with a
    traceback on the day he first tries it.** **If it DOES exist, every row is
    real and yours to protect: read it, never write it.**
  * **THE 1%-RISK COMPARISON NEEDS A DECISION HE HAS NOT MADE.** Desk item 12:
    the 25% position cap means real risk is ~0.49% per trade, not 1%. **Ask him
    which number "a disciplined 1%-risk version" means before you code it.**

---

# WHAT YOU STILL OWE (both jobs)

1. **PROVE THE SHIP IS ALIVE FIRST.** All FOURTEEN invocations, output to a
   file, **red counted BY MACHINE three ways** (the tick character, the first
   word of a line, and `GATE ... FAILED`), **then READ any hit with your own
   eyes.** `collection_guard.py` prints `OK`/`FAIL`, not ticks; `fear_greed.py`
   and `funding.py` both carry **FAILURE** at the start of a line inside their
   own PASS text; **and `funding.py` line 137 starts a line with "escaped" — it
   fooled three consecutive sessions and has not fooled the two since, because
   the orders named it.** **My run produced 38 word-hits and every one was
   innocent prose. Read them anyway.**
   **>>> COUNT TICKS BY CHARACTER, NOT BY BYTE.** The tick is three bytes in
   UTF-8.
2. **NAME YOUR AWKWARD EDGE CASES IN `PROGRESS_LOG.md` BEFORE YOU WRITE CODE**
   and commit them with no code in that commit.
3. **Confine the change and PROVE the confinement** — `git` as the primary
   proof, not a hash.
4. **RUN THE GATE. Every check green, every sabotage CAUGHT.**
5. **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.**
6. `git status` clean when you finish.

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT ALREADY READS CHANGES** except what your orders call
    for — prove it two ways, never assert it.

    **>>> THE PROOF THAT NEEDS NO RECIPE AND CANNOT DRIFT:** compare each
    file's working-tree bytes against `git show HEAD:<file>` **with CRLF
    normalised to LF on both sides**, and separately assert the WORKING TREE
    has zero bare LF. **A hash whose recipe nobody can reproduce is a number,
    not a proof.**

    **>>> DO NOT COMPARE `journal/log_trade.py` AGAINST ANY PREFIX HASH — IT
    IS DEAD AGAIN.** The production half is unchanged; the FILE is 59,769 ->
    73,154 bytes. **Production half: lines 1-286.** `cockpit/whales.py`:
    lines 1-362. **Prove them against HEAD normalised, not against a number.**

    **>>> AND TWO `.py` FILES ON THIS SHIP ARE LF, NOT CRLF.**
    `cockpit/plan.py` (67 bare LF) and `journal/snapshot.py` (80). **Neither
    is a defect and neither is yours.** Do not "fix" them and do not let a
    bare-LF assertion over the whole tree fail because of them.

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.** Check (m)'s R2 and check (n)'s `N_HEADER` are the worked
    examples.
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **>>> CERTIFY BY ATTACK, NOT BY THE DRILL — AND TODAY PROVED IT FROM A
    THIRD DIRECTION.** GATE 5.1's drill owns T10, a sabotage for a fault that
    walked through anyway. GATE 3.5-R2's first draft passed 111/0 carrying a
    bug that destroyed its own report. **And today: a gate printed 70 checks,
    0 red over a shell that had been edited to file his winning trades as
    losses — because no check had ever RUN the shell.**
(h) **PROVE YOUR WITNESS CAN SEE THE FAULT BEFORE YOU BELIEVE ITS VERDICT.**
(i) **NEVER RUN A WITNESS AND A GATE AGAINST THE SAME COPY.**
(j) **TELL YOUR GATE HOW MANY CHECKS IT OWES.** `journal/log_trade.py` (77) is
    STILL the only gate on this ship that does. **That is R-070 and he has
    never ruled on it.**
(k) **A FAILING GATE MUST STILL BE ABLE TO FINISH REPORTING — AND YOU MUST
    PROVE IT, NOT INTEND IT.** Every one of check (n)'s seven was forced red
    alone before it shipped.
(l) **>>> NEW, EARNED TODAY: A CLAIM IN A COMMENT ABOUT WHAT CANNOT BE TESTED
    IS NOT A WARNING. IT IS A PERMISSION SLIP.** The sentence *"an interactive
    prompt is something no gate can reach"* did not warn anybody off those
    seven lines; **it told every future session they were safe to change.** If
    you write down that something cannot be tested, **try it first.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **>>> `journal/log_trade.py --gate` NOW TAKES ~1.9 SECONDS, UP FROM ~0.9, AND
  LAUNCHES THREE CHILD INTERPRETERS** (checks (i), (m) and (n)). **AND WHEN
  CHECK (n) FAILS ON AN ADDED OR RENAMED QUESTION IT TAKES ~78 SECONDS** —
  that is the reader's 60-second deadline plus a 15-second wait, **it is RED
  and it is not a hang.** Do not trim the deadline to make the gate feel
  faster.
- **>>> `cockpit/whales.py --gate` TAKES ~19 SECONDS AND BINDS TWO LOCAL PORTS
  AND LEAVES A HUNG DAEMON THREAD BEHIND, ON EVERY RUN, ON PURPOSE.** The
  thread is a daemon and dies with the interpreter. **A future session will
  find it and want to "fix" it. It is the check.**
- **>>> `cockpit/carry.py --gate` CAN GO RED THROUGH NO FAULT OF THE FILE IF YOU
  RUN IT WITHIN SECONDS OF A FUNDING SETTLEMENT (00:00, 08:00, 16:00 UTC).**
  R-069, deliberate. **Re-run once, away from the settlement.**
- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Outside a settlement window a red funding gate is REAL.
- **`cockpit\whales.py --gate` AND `cockpit\carry.py --gate` BIND LOCAL PORTS.**
  If your machine refuses one, those checks go red and it is the machine.
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories.
- **S6, F10 AND B1 NO LONGER GO RED.** If any does, it is a regression and
  SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **>>> GATE TIMINGS ON RECORD ARE WEATHER REPORTS, NOT CHECKS.** `funding`
  took **148.9 s** today and `carry`, recorded at ~35 s, took **4.0**. **Sixth
  time a recorded timing has proved to be one unrepresentative reading.**
- **>>> `journal/my_trades.csv` DOES NOT EXIST AND THAT IS CORRECT.** Do not
  create it. **If it exists, he has logged a real trade and every row is his:
  read it, never write it, and NEVER drive `python journal\log_trade.py` by
  hand against the real journal.** **A no-`path` call writes into whatever
  `journal/` folder the module sits in — that is what checks (m) and (n) are
  built around.**
- **THE BRIEF WENT 2/3 TWICE.** It was **3/3** today. **KEEP THE WHOLE OUTPUT
  OF YOUR FIRST BRIEF RUN, not the tail.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.**
- **THE CLOUD WATCHMAN PUSHES `journal/snapshots_cloud.csv` AND
  `journal/cloud_grader_report.txt` EVERY FEW HOURS.** **`git pull` FIRST.**
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **THE EXEMPTION IS SPENT AND IT STAYED SPENT.** I held none and asked for
   none. **You do the same, and write the same into the orders you leave.
   NEVER WRITE ONE — only he grants one, in words.**
2. **>>> R-080: HE RULED SERIOUS.** He asked *"who will swap those questions
   other than me?"* first, was told the honest answer, and ruled. **REPAIRED
   under GATE 5.1-R2. Attacking it is YOUR JOB 1.**
3. **>>> HIS TEST FOR EVERY FUTURE FINDING, IN HIS OWN WORDS:** *"our actual
   goal is to make a correct thing in actual real environment. so those things
   which cant be done in actual scenarios at those we have to ignore those."*
   **THIS SHARPENS THE ATTACK, IT DOES NOT EXCUSE ONE.** Ask who would really
   do the thing your sabotage does, and answer honestly.
4. **R-060: HE RULED "CORRECT IT".** Corrected. R-066 open, four of five doubts
   untested.
5. **R-054 IS SMALL** (2026-08-11). **R-047 AND R-048 ARE SMALL** (2026-08-05).
6. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
7. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
8. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
9. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording.
10. **DOOR 3 IS BUILT IN THE CALENDAR, THE WHALE WATCH, THE CARRY MONITOR AND
    THE TRADE LOGGER. R-025 IS CLEARED.** Residue R-033. **`news.py` is the one
    without it (R-046).**
11. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
12. **THE CONTEXT DECK AND THE CARRY MONITOR ARE INFORMATION AND CAN NEVER
    BECOME SIGNALS.** **Phase 6's three slots are locked BY NAME:
    Turtle/Donchian, funding-rate fade, on-chain cycle thermometer.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> DOES THE CARRY LINE READ AS INFORMATION, OR AS A SUGGESTION?** Shown
   to him 2026-08-19, asked directly, **still not answered. ASK AGAIN — this is
   the fifth session carrying it.** It prints a percent-a-year figure, the
   closest this ship has come to something that sounds like an opportunity, and
   **Step 2.2 forbids a machine answering that by predicting him.**
2. **AND BESIDE THAT QUESTION:** the figure is the funding yield on the PERP
   NOTIONAL. Running the trade needs money on BOTH legs at once, so **the
   return on the capital he would actually deploy is lower than the number on
   the line.** **Not a defect — the arithmetic is right for what the line
   names. His call.**
3. **>>> R-070 — AND `journal/log_trade.py` WENT 70 -> 77 TODAY WHILE STILL
   BEING THE ONLY GATE THAT KNOWS ITS OWN COUNT.** The other seven do not.
   **It is one line each.** He has never ruled on it.
4. **R-049 — offer it an EIGHTH time.** The X1 repair in `cockpit/news.py` is
   self-marked and runs on every headline he sees. The measurement that argues
   for leaving it: 136 real headlines, not one carrying markup.
5. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** — how long Binance really
   goes between bucket updates (`MAX_AGE_MIN = 30`), and how far the BTC figure
   really moves between two calls seconds apart.
6. **THE CATEGORY B PILE IS FORTY-SEVEN.** Cleared before the ship is used for
   real, at the same moment `cockpit/brief.py` gets its gate. **Keep saying the
   number.**
7. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR**, the only thing he personally
   owes the R-037 repair. **It switches ON Windows' diary of scheduled jobs,
   which ships switched off** — so that if the monthly open-interest job ever
   fails silently, there is a record of why. **Start -> type `powershell` ->
   right-click -> Run as administrator:**

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

8. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
9. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com.
10. **THE RULES HE HAS NOT YET ADOPTED**, each earned many times over: *"A
    SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS
    ANYTHING"*; *"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT TURNS
    OVER"*; **candidate Law 8 — "a claim about how something behaves is not a
    fact until it has been run"** — **which earned itself outright today, in
    the most literal way possible: a comment saying a thing could not be
    tested, tested in twenty lines**; **"A GATE MUST BE TOLD HOW MANY CHECKS
    IT OWES"**; **"A GATE MUST BE MADE TO CALL THE THING THE WAY ITS ONLY REAL
    CALLER CALLS IT"**; **"EVERY CHECK MUST BE MADE TO FAIL ONCE, BECAUSE A
    GREEN RUN NEVER EXECUTES A FAILURE PATH"**; and **NEW — "A CLAIM ABOUT
    WHAT CANNOT BE TESTED IS A PERMISSION SLIP, NOT A WARNING."**
11. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
12. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, and the
    Mirror needs it the moment anybody builds it.** **And if the answer means
    asking him a new question when he logs a trade, check (n) must be taught
    it — one deliberate line in `N_ASK`.**
13. **`MAX_PLAUSIBLE_RATE` in `cockpit/funding.py`** — measured 13-16x looser
    than Binance's published cap. **Recommendation: tighten to ~0.01. STILL NOT
    DONE.** `cockpit/carry.py` shipped with exactly that bound.
14. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py`,
    `cockpit/carry.py` and `journal/log_trade.py` are the worked examples.**
15. **The settled-rate anchor (R-004).**
16. **ALL FIVE CONTEXT DECK LINES AND THE CARRY LINE ARE ON THE BRIEF.** **The
    trade logger is NOT on the Brief and never will be — it is a command he
    runs, not a line he reads.**
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED THIRTEEN TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**

---

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping. None of it is repeated here.**

1. **`PROGRESS_LOG.md`, the two entries of 2026-09-08** (part one, the attack
   and THE FINDING REPORT; part two, the bar and the repair). **The file is
   ~872 KB; do not read it all.**
2. **`journal/log_trade.py`** — production half lines 1-286 (**unchanged**),
   gate from 287, **check (m) from line 990, check (n) from line 1167.**
3. **`REVIEW_QUEUE.md`, R-080 and R-081**, and the five verdicts above them.
4. **`EXECUTION_PLAN.md` PHASE 5** and the CURRENT POSITION MARKER.
5. **`PROGRESS_LOG.md` 2026-09-08, "GATE 5.1-R2 — THE BAR"** — a bar committed
   alone before its code existed, **with one of its twelve edge cases proved
   half wrong by the code that met it.** Read it if you reach JOB 2, because
   you write GATE 5.2 yourself and nobody checks it before you build.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every few hours. **AND CHECK
  YOUR COMMIT HASHES AGAIN AFTER YOU PUSH** — a rebase over its push has
  rewritten a hash more than once.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents**
  (**except `cockpit/plan.py` and `journal/snapshot.py`, which are LF**).
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes
  in a payload** — use `bytes([10])` or `chr(10)`.
- **>>> AN ANCHOR MUST NEVER SPLIT A CRLF PAIR**, and must match exactly once.
  **Write your writer to REFUSE on both, on a bare LF in the result, on an edit
  that changes nothing, and ON ANY RESULT WHOSE PRODUCTION HALF MOVED.** Mine
  did all five.
- **>>> IF A REPAIR NEEDS A SECOND ATTEMPT, `git checkout --` THE FILE AND
  RE-RUN THE INSTALLER FROM CLEAN**, so the shipped file is one clean run and
  not two edits stacked on each other.
- **>>> A FILE WRITTEN BY AN EDITOR TOOL ARRIVES AS LF ON THIS MACHINE.**
  **Check the endings of anything you create, before you commit it.**
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
  **Comparing CONTENT against the blob, both sides normalised, is fine and is
  the best confinement proof there is.**
- **`.bat` FILES MUST BE CRLF, AND KEEP THEM ASCII-ONLY.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING**, and write documents with an editor
  tool or a binary appender, not with `cat <<EOF`. **A `-c` string with a
  Windows path in it broke on a backslash for me today, exactly as the last
  four sets of orders warned.**
- **>>> SET `PYTHONUTF8=1` ON YOUR OWN HARNESS TOO, NOT ONLY ON THE GATE.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8
  files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** —
  `â€`, `Â·`, `â†`, `Ã`, `âœ`. **Compare the counts against
  `git show HEAD:<file>` so a fingerprint that was ALREADY there is not blamed
  on you, and one you ADDED cannot hide behind one that was.** Ignore hits
  inside backticks — including the five on this very line.
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH.** His PowerShell opens at `C:\WINDOWS\system32`:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces
  a fresh one, `CHECK_STATUS.bat` shows the collection's health, and
  **`LOG_TRADE.bat` asks him the seven questions and logs a trade.**

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL.

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... your verdicts on R-080 and R-081 — both are yours
                            to clear — plus one OPEN item against your own
                            work.
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; add what you MEASURED.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words brief.
                            **>>> AND THEIR JOB 1 IS: ATTACK WHAT YOU BUILT.
                            YOU MAY NOT GRANT AN EXEMPTION.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his. **He is a
       non-programmer and he says so. If he asks what a finding means in real
       terms, that is not an interruption — it is the most useful question
       anybody asks on this ship, and today it produced a rule.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**
