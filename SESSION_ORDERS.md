# ZAR X — **YOUR JOB 1 IS TO ATTACK TWO REPAIRS I MADE TONIGHT, WHICH NOBODY ELSE HAS EVER LOOKED AT. IN BOTH, THE SAME MIND FOUND THE FAULT AND WROTE THE FIX. THE COMMANDER ORDERED THIS IN WORDS: "next session will attack the repairs." NO EXEMPTION EXISTS, NONE WAS HELD, AND I COULD NOT HAVE GRANTED YOU ONE.**

*Written 2026-08-20 (night) by the twenty-fifth generation, which attacked
`journal/log_trade.py`, found three real faults walking through GATE 5.1,
answered R-066's three-generation-old doubt 2, and — on two separate rulings
from the Commander — repaired both. **Only the Commander may grant an exemption,
and only out loud.***

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **ATTACK GATE 5.1-R1 AND GATE 3.5-R2.** Invent
                            breaks I never imagined. These are R-078 and
                            R-079, and R-072 and R-077 are still open
                            behind them.
                   PART 2 — **BUILD `journal/mirror.py`** (Phase 5, second
                            half) — **ONLY IF PART 1 PERMITS IT, AND ONLY
                            AFTER YOU HAVE DECLARED GATE 5.2 AND COMMITTED
                            IT ALONE, WITH NO CODE IN THAT COMMIT.**

**PART 2 IS CONDITIONAL AND THE COMMANDER DECIDES, NOT YOU.** If Part 1 finds
something, **fill in THE FINDING REPORT in `THE_PATTERN.md` BEFORE repairing
anything**, then: SERIOUS -> fix it and stop. BORDERLINE -> report and stop, he
rules. SMALL -> file it CATEGORY B and carry on to Part 2.

**"I ATTACKED BOTH HARD AND FOUND NOTHING" IS A SUCCESS. SAY IT PLAINLY AND
CLEAR R-078 AND R-079.** Do not manufacture a defect — **he has now been
waiting two sessions for the Mirror, and a stretched finding costs him a third.**

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
    journal/log_trade.py        GATE 5.1-R1   PASSED  exit 0  0 red   70 green
      the same file at TZ=UTC0  GATE 5.1-R1   PASSED  exit 0  0 red   70 green
    vault INTACT 6 of 6 · Brief 3/3 (Whale watch 6 of 6) · lab/ untouched
    journal/my_trades.csv DOES NOT EXIST — his first real trade creates it

**>>> TWO COUNTS CHANGED TONIGHT: whales 107 -> 111, log_trade 64 -> 70.** If
you find different numbers, something is wrong and it is not a rounding error.

**PHASE 4 IS COMPLETE. PHASE 5 IS STILL HALF BUILT — THE MIRROR DOES NOT EXIST.**

## What I did, in eight lines

1. **Proved the ship alive first** — fourteen invocations, 1,013 green, red
   counted by machine three ways, every hit read by eye. **The funding gate's
   "escaped" trap did not fool me because the orders named it. Keep naming it.**
2. **Attacked `journal/log_trade.py` with six TEXT-EDIT faults**, control
   first. **THREE ESCAPED** — one hole: **the gate never called the doorway the
   way the shell calls it**, with no `path` and no `now`.
3. **MY FIRST RIG WAS CONTAMINATED AND SCORED TWO LIVE ESCAPES AS `CAUGHT`.**
   Found by reading which check went red. **R-076.**
4. **Graded BORDERLINE, repaired nothing, reported. He ruled SERIOUS.**
   Declared GATE 5.1-R1, committed the bar ALONE, built check (m): 64 -> 70.
   **All three escapes now turn the gate red.**
5. **Answered R-066's doubt 2, open for three generations:** `_get` loses its
   timeout and hangs forever while GATE 3.5-R1 printed 107/0.
6. **He ruled on that too — "repair the whale thing".** Declared GATE 3.5-R2,
   committed the bar ALONE, built four checks: 107 -> 111. **The same edit that
   printed `PASSED — 107 checks, 0 red` now prints `FAILED — 2 red of 111`.**
7. **>>> THE FIRST DRAFT OF THAT SECOND REPAIR DIED IN A TRACEBACK UNDER THE
   VERY FAULT IT WAS BUILT FOR — AND THE HEALTHY GATE PASSED 111/0 WITH THE BUG
   IN IT.** Only the attack could have found it. Fixed; recorded; R-079 doubt 1.
8. **THE CATEGORY B PILE IS FORTY-SIX. Nothing was cleared by anybody,
   including me** — I could have cleared R-072 and did not, because it did not
   survive.

---

# **JOB 1 — ATTACK BOTH REPAIRS (R-078 AND R-079)**

## WHAT THE TWO INSTRUMENTS ARE FOR — Q1, ANSWERED FOR YOU

**`journal/log_trade.py`** — the rows in `journal/my_trades.csv`, his own
record of closed trades, in his own words. **It is an ARCHIVE and the Mirror
will grade him on it. Nobody re-types a trade they logged in March.**

**`cockpit/whales.py`** — the Whale watch line on the Brief, and **whether the
Brief appears at all**: a `_get` that never returns means no Brief, forever.

## REPAIR ONE — GATE 5.1-R1, check (m), `journal/log_trade.py` from line 990

Calls the doorway **with no `path` and no `now`** — the production calling
convention — **in a child interpreter against a byte copy of the module in a
temporary tree.** It must be a copy: **a no-`path` call writes into whatever
`journal/` folder the module sits in.**

    R1 the child imported THE COPY (proved by the `__file__` it reports back)
    R2 the file at an address THE GATE TYPES OUT, never one from the module
    R3 and no other `.csv` beside it
    R4 the stamp inside a window the gate measures itself, ±2 seconds
    R5 and it carries the zone — a SEPARATE check on purpose
    R6 the window judge proved able to SAY NO, in the same run

### >>> WHERE I SAY I DID NOT LOOK — A STARTING POINT, NOT A LIST TO TICK

1. **>>> THE DRILL CANNOT REACH CHECK (m) AT ALL AND I LEFT IT THAT WAY.** A
   `globals()` swap cannot cross into a child interpreter reading a copy off
   the disk, so any sabotage would be INERT — and an INERT break is a FAIL
   here. **Check (m) is the ONLY part of that gate with no permanent break
   testing it, certified by an attack I ran once, by hand.**
2. **THE TWO-SECOND TOLERANCE IN R4 IS REASONING, NOT MEASUREMENT.** A drift of
   a few minutes — bad time sync, a VM resuming from sleep — would pass R4.
3. **R4 AND R6 SHARE ONE FUNCTION, SO A FAULT IN `_inside` IS INVISIBLE TWICE.**
   R6 exists to prove `_inside` can say no, **and R6 calls the same `_inside`.**
4. **THE CHILD RUNS ONE HAPPY TRADE.** **The eighteen refusal shapes are still
   only ever exercised with an injected `path` and `now`.**
5. **I PROVED THE CHILD IMPORTS THE COPY BY READING, NOT BY PLANTING A
   COMPETING `journal/log_trade.py` IN ITS PATH AND WATCHING R1 GO RED.**

## REPAIR TWO — GATE 3.5-R2, `cockpit/whales.py` from line 1575

Four checks against a listener that **accepts the connection and holds it open,
saying nothing** — what a wedged venue looks like from outside.

    S1 the module's own `_get` CAME BACK ON ITS OWN     raised after 3.03s
    S2 and as a TIMEOUT specifically, through `_why`  ReadTimeout->'timed out'
    S3 THE POSITIVE CONTROL — the same request, no
       timeout, did NOT come back              still running, waited 8.00s
    S4 the silent server closed                        socket fileno: -1

**S3 IS THE HALF THAT MAKES S1 MEAN ANYTHING.** Without it, S1 passing could
just mean the server answered — **which is exactly how this gate came to
certify a `_get` that could hang forever.**

### >>> WHERE I SAY I DID NOT LOOK

1. **>>> THE FIRST DRAFT DIED IN A TRACEBACK UNDER THE FAULT IT WAS BUILT FOR,
   AND THE HEALTHY GATE PASSED 111/0 WITH THAT BUG IN IT.** `answer['how']` is
   set inside the worker thread and a call that never returns never gets there.
   **A guard on a detail line only runs when the check FAILS.** Fixed by seeding
   the report before the thread starts. **I cannot know whether S2, S3 and S4
   hide the same class of bug in a failure mode I did not trigger. THIS IS THE
   ONE I WOULD ATTACK FIRST: make each of the four fail, one at a time, and
   check the gate still finishes its report.**
2. **A BENIGN RACE IN `_timed`:** if the worker finishes just after `join()`
   times out, `stuck` is True while `how` may say `returned`. **The verdict
   uses `stuck`, so no grade can move — but the detail line could contradict
   itself.**
3. **THE 3s/8s NUMBERS ARE A JUDGEMENT.** A venue that is merely very slow —
   thirty seconds — would make S1 red, and it would be the venue, not the code.
4. **THIS GATE STILL DOES NOT KNOW HOW MANY CHECKS IT OWES.** I moved it 107 ->
   111 and nothing verified it. **That is R-070, on his desk, now demonstrated
   inside the file that proves the point.**
5. **IT DOES NOT PROVE "ONE REQUEST, NO RETRIES"**, which `_get`'s docstring
   claims.
6. **TWO LOCAL PORTS AND A HUNG DAEMON THREAD, LEFT ON PURPOSE, EVERY RUN.**
   Nobody has run this behind a firewall or a real proxy — R-066 doubt 3,
   untested, now doubled.

## RE-RUN MY FOUR FAULTS. IF ANY FAILS TO GO RED, A REPAIR IS DECORATIVE.

Install as **TEXT EDITS** in copies outside the repo, **control first**.

    journal/log_trade.py, in `_stamp`:
      datetime.now(timezone.utc) -> datetime.now().replace(tzinfo=timezone.utc)
        expect 1 red, R4
      datetime.now(timezone.utc) -> datetime(2020, 1, 1, tzinfo=timezone.utc)
        expect 1 red, R4
    journal/log_trade.py:
      TRADES_FILE = os.path.join(JOURNAL_DIR, 'my_trades.csv') -> 'trades.csv'
        expect 4 red — R2, R3, and R4/R5 (no file left to read a stamp from)
    cockpit/whales.py, in `_get`:
      requests.get(f"{base_url}{path}", params=params, timeout=timeout)
        -> requests.get(f"{base_url}{path}", params=params)
        expect 2 red — S1 and S2, with S3 still GREEN as it must be

**>>> THE `_stamp` ANCHOR MATCHES TWICE** — the drill's own T10 sabotage
`_stamp_local` copies the production line character for character. **Make your
writer REFUSE rather than replace both.**

## WHAT PART 1 LOOKS LIKE

1. Write the bars for "this review clears" into notes **before running
   anything**, and **name your candidate attacks there.**
2. Invent at least one **NEW** sabotage per repair, in scratch copies
   **outside the repo**. **Run the untouched control too.**
3. **>>> NEVER RUN A WITNESS AND A GATE AGAINST THE SAME COPY.** A witness that
   exercises the production path WRITES, and what it writes turns the gate red
   for reasons that are not the fault. **This cost me my first two results.**
4. **PROVE YOUR WITNESS CAN SEE THE FAULT BEFORE YOU BELIEVE ITS VERDICT.**
5. **>>> AND THE NEW ONE, EARNED TONIGHT: MAKE THE CHECK FAIL AND SEE WHETHER
   THE GATE CAN STILL REPORT.** A green run never executes a failure path.
6. Confirm `git status` is clean afterwards.
7. **Write it up either way**, and record verdicts in `REVIEW_QUEUE.md`.

**YOU MAY CLEAR R-072, R-076, R-077, R-078 AND R-079** — you built none of
them. **YOU MAY NOT CLEAR R-070, R-071, R-073, R-074 or R-075.**

---

# **JOB 2 — ONLY IF JOB 1 PERMITS: `journal/mirror.py` (PHASE 5, SECOND HALF)**

**A half-built Mirror is worse than no Mirror. If you run short, do Part 1
properly and leave Part 2 entirely.**

## >>> GATE 5.2 DOES NOT EXIST. YOU DECLARE IT, AND YOU COMMIT IT ALONE.

**Declare GATE 5.2 in `PROGRESS_LOG.md`, commit it with NO `.py` in that
commit, and only then write code.** `git show --stat` is what proves the bar
came first. **I did this twice tonight and both repairs went in first time
because the bar named the edge cases before any code existed.**

**WHAT THE PLAN ASKS** (`EXECUTION_PLAN.md` Phase 5, item 2): monthly, the
Commander's logged trades vs what the instruments said at those moments (from
`journal/snapshots_*.csv`) vs what a disciplined 1%-risk version of the same
trades would have done. **Output: plain-words report. No shaming, arithmetic
only. NEVER a signal.**

**FIVE THINGS YOU WILL MEET ON YOUR FIRST AFTERNOON:**

  * **>>> THE TWO FILES DISAGREE ABOUT WHAT A TIME LOOKS LIKE. THAT IS R-074.**
    `my_trades.csv` writes `2026-08-20T09:30:15+00:00`; **every snapshot row
    since Phase 2 says `2026-07-21 11:35` with no zone at all.** Decide the
    reconciliation deliberately and **write it down BEFORE coding.**
    **>>> AND NOTE WHAT CHANGED TONIGHT: the stamp line is no longer
    unguarded. R4 and R5 of check (m) watch it. If you change how a stamp is
    made, those are the checks that will stop you, and they are supposed to.**
  * **THE ASSET NAMES WERE MADE TO MATCH ON PURPOSE.** `log_trade.py` stores
    `BTC-USD`, the same string every snapshot row uses. **No translation table.**
  * **`journal/my_trades.csv` MAY NOT EXIST WHEN YOU ARRIVE**, and that is
    correct. **A Mirror that crashes on an empty journal greets him with a
    traceback on the day he first tries it.** **If it DOES exist, every row is
    real and yours to protect: read it, never write it.**
  * **NO GRADING AT ENTRY TIME REMAINS ABSOLUTE.** The logger never judges.
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
   own PASS text; **and `funding.py` line 69 starts a line with "escaped" — it
   fooled three consecutive sessions and did NOT fool the fourth, because the
   orders named it.**
   **>>> COUNT TICKS BY CHARACTER, NOT BY BYTE.** The tick is three bytes in
   UTF-8. I briefly had "278 ticks" for a gate that ran 70.
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

    **>>> THE PREFIX HASHES FOR `cockpit/whales.py` AND `journal/log_trade.py`
    ARE BOTH DEAD.** Both production halves are unchanged, but both FILES are
    longer. **Do not compare against `d2cd1b58373d2fcb` or
    `652378043e01b8e4`.** Production halves: `log_trade` lines 1-286, `whales`
    lines 1-362. **Prove them against HEAD normalised, not against a number.**
    The remaining six files' hashes are unchanged and are in the previous
    orders' table if anybody needs them.

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.** Check (m)'s R2 is the worked example.
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **>>> CERTIFY BY ATTACK, NOT BY THE DRILL — AND TONIGHT PROVED IT TWICE,
    FROM TWO DIFFERENT DIRECTIONS.** GATE 5.1's drill owns **T10, a sabotage
    for the exact fault installed as A1: it ran, it reported CAUGHT, and the
    fault walked through anyway.** And **GATE 3.5-R2's first draft passed
    111/0 three times while carrying a bug that destroyed its own report the
    moment it caught anything** — *"the gate could not REPORT the fault it did
    catch"*, which no green run can ever reveal.
(h) **PROVE YOUR WITNESS CAN SEE THE FAULT BEFORE YOU BELIEVE ITS VERDICT.**
(i) **NEVER RUN A WITNESS AND A GATE AGAINST THE SAME COPY.**
(j) **TELL YOUR GATE HOW MANY CHECKS IT OWES.** `journal/log_trade.py` (70) is
    STILL the only gate on this ship that does. **`cockpit/whales.py` went
    107 -> 111 tonight and nothing verified it.**
(k) **>>> A FAILING GATE MUST STILL BE ABLE TO FINISH REPORTING — AND YOU MUST
    PROVE IT, NOT INTEND IT.** I wrote this rule into the orders this afternoon
    and broke it the same night. **Make each new check fail on purpose and read
    the output.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **>>> `cockpit/whales.py --gate` NOW TAKES ~18 SECONDS, UP FROM ~8, AND THAT
  IS CORRECT.** Eleven of those seconds ARE the new check — three proving the
  honest call returns, eight proving the timeout-less one does not. **Do not
  trim the patience to make the gate feel faster.**
- **>>> IT ALSO BINDS A SECOND LOCAL PORT AND LEAVES A HUNG DAEMON THREAD
  BEHIND, ON EVERY RUN, ON PURPOSE.** The thread is a daemon and dies with the
  interpreter. **A future session will find it and want to "fix" it. It is the
  check.**
- **>>> `journal/log_trade.py --gate` NOW LAUNCHES TWO CHILD INTERPRETERS**
  (check (i) and check (m)). Each gets 90 seconds and **a timeout is RED.**
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
- **>>> GATE TIMINGS ON RECORD ARE WEATHER REPORTS, NOT CHECKS.** `carry` is
  recorded at ~35 s and took **5 seconds** today; `fear_greed` is recorded at
  ~40 s and took **63**. **Fifth time a recorded timing has proved to be one
  unrepresentative reading.**
- **>>> `journal/my_trades.csv` DOES NOT EXIST AND THAT IS CORRECT.** Do not
  create it. **If it exists, he has logged a real trade and every row is his:
  read it, never write it, and NEVER drive `python journal\log_trade.py` by
  hand against the real journal.** **A no-`path` call writes into whatever
  `journal/` folder the module sits in — that is what check (m) is built
  around and what contaminated my first rig.**
- **THE BRIEF WENT 2/3 TWICE.** It was **3/3** today, twice. **KEEP THE WHOLE
  OUTPUT OF YOUR FIRST BRIEF RUN, not the tail.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.**
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **THE EXEMPTION IS SPENT AND IT STAYED SPENT.** I held none and asked for
   none. **You do the same, and write the same into the orders you leave.
   NEVER WRITE ONE — only he grants one, in words.**
2. **>>> R-072: HE RULED SERIOUS — *"ok lets fix it"*. REPAIRED (GATE 5.1-R1).**
3. **>>> R-077: HE RULED IT SHOULD BE REPAIRED — *"we should repair the whale
   thing and then next session will attack the repairs"*. REPAIRED (GATE
   3.5-R2).** **The second half of that sentence is YOUR JOB 1.**
4. **R-060: HE RULED "CORRECT IT".** Corrected. R-066 open, four of five doubts
   untested — **doubt 2 is now answered AND repaired.**
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
   the fourth session carrying it.** It prints a percent-a-year figure, the
   closest this ship has come to something that sounds like an opportunity, and
   **Step 2.2 forbids a machine answering that by predicting him.**
2. **AND BESIDE THAT QUESTION:** the figure is the funding yield on the PERP
   NOTIONAL. Running the trade needs money on BOTH legs at once, so **the
   return on the capital he would actually deploy is lower than the number on
   the line.** **Not a defect — the arithmetic is right for what the line
   names. His call.**
3. **>>> R-070 — AND IT EARNED ITSELF AGAIN TONIGHT, INSIDE THE FILE THAT
   PROVES THE POINT.** `cockpit/whales.py` went from 107 checks to 111 and
   **nothing anywhere verified that number.** No gate on this ship knows how
   many checks it owes except `journal/log_trade.py`. **It is one line each for
   the other seven.** He has never ruled on it.
4. **R-049 — offer it a SEVENTH time.** The X1 repair in `cockpit/news.py` is
   self-marked and runs on every headline he sees. The measurement that argues
   for leaving it: 136 real headlines, not one carrying markup.
5. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** — how long Binance really
   goes between bucket updates (`MAX_AGE_MIN = 30`), and how far the BTC figure
   really moves between two calls seconds apart.
6. **THE CATEGORY B PILE IS FORTY-SIX.** Cleared before the ship is used for
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
    fact until it has been run"**; **"A GATE MUST BE TOLD HOW MANY CHECKS IT
    OWES"**; **"A GATE MUST BE MADE TO CALL THE THING THE WAY ITS ONLY REAL
    CALLER CALLS IT"** (he has effectively ruled on this once, by ordering the
    first repair); and **NEW, EARNED TONIGHT — "EVERY CHECK MUST BE MADE TO
    FAIL ONCE, BECAUSE A GREEN RUN NEVER EXECUTES A FAILURE PATH."**
11. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
12. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, and the
    Mirror needs it the moment anybody builds it.**
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
17. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED TWELVE TIMES, NOT ADOPTED.**

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

1. **`PROGRESS_LOG.md`, the five entries of 2026-08-20** (afternoon, evening,
   evening second part, night, night second part) — the attack, the
   contaminated rig, THE FINDING REPORT, both bars, and both repairs. **The
   file is ~847 KB; do not read it all.**
2. **`journal/log_trade.py`** — production half lines 1-286 (**unchanged**),
   gate from 287, **check (m) from line 990.**
3. **`cockpit/whales.py`** — production half lines 1-362 (**unchanged**),
   **GATE 3.5-R2 from line 1575.**
4. **`REVIEW_QUEUE.md`, R-072 and R-076 through R-079.**
5. **`EXECUTION_PLAN.md` PHASE 5** and the CURRENT POSITION MARKER.
6. **`PROGRESS_LOG.md` 2026-08-20 (night), "THE CONDITIONS OF GATE 3.5-R2"** —
   a bar committed alone before its code existed, by the same session that
   would have to meet it. **Read it if you reach JOB 2, because you write GATE
   5.2 yourself and nobody checks it before you build.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours. **AND CHECK
  YOUR COMMIT HASHES AGAIN AFTER YOU PUSH** — a rebase over its push has
  rewritten a hash twice, including mine this afternoon.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes
  in a payload** — use `bytes([10])` or `chr(10)`.
- **>>> AN ANCHOR MUST NEVER SPLIT A CRLF PAIR**, and must match exactly once.
  **Write your writer to REFUSE on both, on a bare LF in the result, on an edit
  that changes nothing, and ON ANY RESULT WHOSE PRODUCTION HALF MOVED.** Mine
  did all five and the refusals earned themselves twice today.
- **>>> IF A REPAIR NEEDS A SECOND ATTEMPT, `git checkout --` THE FILE AND
  RE-RUN THE INSTALLER FROM CLEAN.** I did this on the whale repair so the
  shipped file is one clean run of the installer and not two edits stacked on
  each other.
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
  tool or a binary appender, not with `cat <<EOF`. **A here-string mangled a
  harness twice this session before I gave up and used a file.**
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
    2. REVIEW_QUEUE.md .... your verdicts on R-078 and R-079 (and R-072,
                            R-076, R-077 — all five are yours to clear), plus
                            one OPEN item against your own work.
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
