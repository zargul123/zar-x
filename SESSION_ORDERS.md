# ZAR X — **YOUR JOB 1 IS TO ATTACK GATE 5.1-R1, WHICH I BUILT THIS EVENING AND NOBODY ELSE HAS EVER LOOKED AT. THAT IS R-078, AND R-072 IS STILL OPEN BECAUSE THE SESSION THAT FOUND THE FAULT WROTE THE FIX. NO EXEMPTION EXISTS, NONE WAS HELD, AND I COULD NOT HAVE GRANTED YOU ONE.**

*Written 2026-08-20 (evening) by the twenty-fifth generation, which attacked
`journal/log_trade.py`, found three real faults walking through GATE 5.1, was
ruled SERIOUS by the Commander, and repaired it under GATE 5.1-R1. **Only the
Commander may grant an exemption, and only out loud.***

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **ATTACK GATE 5.1-R1.** I found the fault AND
                            wrote the repair, which is the exact situation
                            the rule exists for. Invent a break I never
                            imagined. This is R-078.
                   PART 2 — **BUILD `journal/mirror.py`** (Phase 5, second
                            half) — **ONLY IF PART 1 PERMITS IT, AND ONLY
                            AFTER YOU HAVE DECLARED GATE 5.2 AND COMMITTED
                            IT ALONE, WITH NO CODE IN THAT COMMIT.**

**PART 2 IS CONDITIONAL AND THE COMMANDER DECIDES, NOT YOU.** If Part 1 finds
something, **fill in THE FINDING REPORT in `THE_PATTERN.md` BEFORE repairing
anything**, then: SERIOUS -> fix it and stop. BORDERLINE -> report and stop, he
rules. SMALL -> file it CATEGORY B and carry on to Part 2.

**"I ATTACKED IT HARD AND FOUND NOTHING" IS A SUCCESS. SAY IT PLAINLY AND CLEAR
R-078.** Do not manufacture a defect to justify a session — **a stretched
finding costs him the Mirror, which he has now been waiting two sessions for.**

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
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red  107 green
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red  107 green
    cockpit/carry.py            GATE 4.1      PASSED  exit 0  0 red   87 green
      the same file at TZ=UTC0  GATE 4.1      PASSED  exit 0  0 red   87 green
    journal/log_trade.py        GATE 5.1-R1   PASSED  exit 0  0 red   70 green
      the same file at TZ=UTC0  GATE 5.1-R1   PASSED  exit 0  0 red   70 green
    vault INTACT 6 of 6 · Brief 3/3 · lab/ untouched
    journal/my_trades.csv DOES NOT EXIST — his first real trade creates it

**PHASE 4 IS COMPLETE. PHASE 5 IS STILL HALF BUILT — THE MIRROR DOES NOT EXIST.**

## What I did, in seven lines

1. **Proved the ship alive first** — fourteen invocations, 1,013 green, red
   counted by machine three ways, every hit read by eye. **The funding gate's
   "escaped" trap did not fool me because the orders named it. Keep naming it.**
2. **Attacked `journal/log_trade.py` with six faults installed as TEXT EDITS**
   in copies outside the repo, control first. **THREE ESCAPED** — all three the
   same hole: **the gate never called the doorway the way the shell calls it**,
   with no `path` and no `now`.
3. **MY FIRST RIG WAS CONTAMINATED AND SCORED TWO LIVE ESCAPES AS `CAUGHT`.**
   Found by reading which check went red, not by any check of mine. **R-076.**
4. **Graded BORDERLINE, repaired nothing, reported. The Commander ruled
   SERIOUS: *"ok lets fix it"*.**
5. **Declared GATE 5.1-R1 and committed the bar ALONE** — one document, 154
   lines, no `.py`. Then built check (m): six checks, 64 -> 70.
6. **CERTIFIED BY ATTACK: all six faults re-run: the three that escaped now
   turn the gate red, the three already caught still are.** PASSED 70/0 three
   times, tick sequences byte-identical by machine.
7. **R-066 IS NO LONGER UN-ATTACKED** — its doubt 2 was right (R-077). **THE
   CATEGORY B PILE IS FORTY-FIVE. Nothing was cleared by anybody, including
   me.**

---

# **JOB 1 — ATTACK GATE 5.1-R1 (R-078)**

## WHAT THE INSTRUMENT IS FOR — Q1 OF THE FINDING REPORT, ANSWERED FOR YOU

**The rows in `journal/my_trades.csv` — his own record of trades he has closed,
in his own words.** It is not read each morning like the Brief; **it is an
ARCHIVE, and the Mirror will one day grade him on it.** A row that is wrong,
missing or silently altered is worse here than a stale number, because **nobody
re-types a trade they logged in March.**

## WHAT CHECK (m) IS AND WHY IT LOOKS UNLIKE EVERY OTHER CHECK IN THE FILE

Check (m) calls the doorway **with no `path` and no `now`** — the production
calling convention — **in a child interpreter against a byte copy of the module
in a temporary tree.** It has to be a copy, because **a no-`path` call writes
into whatever `journal/` folder the module sits in**, and against the real
module that is his archive.

    R1  the child imported THE COPY (it reports back its own `__file__`)
    R2  the file at an address THE GATE TYPES OUT, never one read from the
        module
    R3  and no other `.csv` beside it
    R4  the stamp inside a window the gate measures itself, ±2 seconds
    R5  and it carries the zone — a SEPARATE check on purpose
    R6  the window judge proved able to SAY NO, in the same run

## >>> WHERE I SAY I DID NOT LOOK — A STARTING POINT, NOT A LIST TO TICK

**A builder cannot invent the attack he is blind to. These are R-078's five,
and the best attack is one that appears nowhere here:**

1. **>>> THE DRILL CANNOT REACH CHECK (m) AND I LEFT IT THAT WAY. THIS IS THE
   ONE I WOULD ATTACK FIRST.** A `globals()` swap cannot cross into a child
   interpreter reading a copy off the disk, so any sabotage would be INERT —
   and an INERT break is a FAIL here. **Check (m) is therefore the ONLY part of
   this gate with no permanent break testing it, certified by an attack I ran
   once, by hand, today.** **Re-run those three text edits yourself rather than
   trusting my paragraph** — they are named below.
2. **THE TWO-SECOND TOLERANCE IN R4 IS REASONING, NOT A MEASUREMENT.** I argued
   nothing on this ship produces a clock error between two seconds and five
   hours. **A drift of a few minutes — a bad time sync, a VM resuming from
   sleep — would pass R4 and I have not tested one.**
3. **R4 AND R6 SHARE ONE FUNCTION, SO A FAULT IN `_inside` IS INVISIBLE TWICE.**
   R6 exists to prove `_inside` can say no, **and R6 calls the same `_inside`
   it is vouching for.**
4. **THE CHILD RUNS ONE HAPPY TRADE AND NOTHING ELSE.** **The eighteen refusal
   shapes are still only ever exercised with an injected `path` and `now`.** I
   fixed the path that writes and left the path that refuses exactly as blind
   as I found it.
5. **I PROVED THE CHILD IMPORTS THE COPY BY READING, NOT BY PLANTING A
   COMPETING `journal/log_trade.py` IN ITS PATH AND WATCHING R1 GO RED.** A
   positive control I did not build.

## AND THE FIVE THAT NOBODY HAS EVER ATTACKED — NOT THE AUTHOR, NOT ME

Still untouched by anybody, and still worth your time:

1. **>>> THE SEVEN INTERACTIVE QUESTIONS ARE TESTED BY NOBODY.** Every check
   calls the doorway directly, so **the ORDER of the seven `input()` calls is
   checked by nothing.** Swap two and his exit price goes into the size field
   forever. **I read the order by eye and it is correct today — that is
   reading, not a check.**
2. **`_needs_header` decides on `os.path.getsize`.** A journal whose header
   somebody deleted by hand never gets one back.
3. **A partial write** (R-073).
4. **The refusal messages echo his own text back with `!r`.**
5. **`_feeling` lower-cases and `_why` does not.**

**AND ONE I FOUND BUT COULD NOT REACH:** check (d) proves eighteen
**validation** refusals write nothing. It never exercises `log_trade`'s
`except OSError` / `except Exception` branch — **the only branch that can say
`[not logged: ...]` while bytes are already on the disk.** If he re-logged a
trade he was told was not logged, D3 keeps the duplicate and the Mirror grades
him on a trade he made once.

## THE THREE FAULTS THAT ESCAPED THIS MORNING — RE-RUN THEM AGAINST MY REPAIR

Install as **TEXT EDITS** in copies outside the repo, **control first**. All
three must turn the gate red; if any does not, my repair is decorative.

    in `_stamp`:  datetime.now(timezone.utc)
                    -> datetime.now().replace(tzinfo=timezone.utc)
                    (expect: 1 red, R4)
    in `_stamp`:  datetime.now(timezone.utc)
                    -> datetime(2020, 1, 1, tzinfo=timezone.utc)
                    (expect: 1 red, R4)
    TRADES_FILE = os.path.join(JOURNAL_DIR, 'my_trades.csv')
                    -> ...'trades.csv'
                    (expect: 4 red — R2, R3, and R4/R5 because there is no
                     file left to read a stamp from)

**>>> THE ANCHOR FOR THE FIRST TWO MATCHES TWICE** — the drill's own T10
sabotage `_stamp_local` copies the production line character for character.
**Make your writer REFUSE rather than replace both.** Lengthen it to the line
that follows, which is unique.

## WHAT PART 1 LOOKS LIKE

1. Write the bars for "this review clears" into notes **before running
   anything**, and **name your candidate attacks there** so you cannot claim
   afterwards to have planned one you stumbled into.
2. Invent at least one **NEW** sabotage, in a scratch copy **outside the repo**.
   **Run the untouched control too** — if it does not pass, the rig is broken
   and nothing you conclude means anything.
3. **>>> NEVER RUN A WITNESS AND A GATE AGAINST THE SAME COPY.** A witness that
   exercises the production path WRITES, and what it writes turns the gate red
   for reasons that are not the fault. **This cost me my first two results.**
4. **PROVE YOUR WITNESS CAN SEE THE FAULT BEFORE YOU BELIEVE ITS VERDICT.** My
   first witness logged one trade with a lower-case feeling and two of my six
   faults were byte-identical to the control under it.
5. Confirm `git status` is clean afterwards.
6. **Write it up either way**, and record the verdict in `REVIEW_QUEUE.md`.

**YOU MAY CLEAR R-078 AND R-072 AND R-076** — you built none of them. **YOU MAY
NOT CLEAR R-070, R-071, R-073, R-074, R-075 or R-077.**

---

# **JOB 2 — ONLY IF JOB 1 PERMITS: `journal/mirror.py` (PHASE 5, SECOND HALF)**

**A half-built Mirror is worse than no Mirror. If you run short, do Part 1
properly and leave Part 2 entirely.**

## >>> GATE 5.2 DOES NOT EXIST. YOU DECLARE IT, AND YOU COMMIT IT ALONE.

GATE 4.1 and GATE 5.1 were both declared by a session that then stopped, and
**both are the bars that survived attack best, because not a word of either
could be bent to match what got built.** **Declare GATE 5.2 in
`PROGRESS_LOG.md`, commit it with NO `.py` in that commit, and only then write
code.** `git show --stat` is what proves the bar came first.

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
    **>>> AND READ THIS BEFORE YOU TOUCH IT: R-072's whole finding was that
    the stamp line was guarded by nothing. It is guarded now — by R4 and R5 of
    check (m). If you change how a stamp is made, THOSE are the checks that
    will stop you, and they are supposed to.**
  * **THE ASSET NAMES WERE MADE TO MATCH ON PURPOSE.** `log_trade.py` stores
    `BTC-USD`, the same string every snapshot row uses. **No translation table
    needed.** Law 2 — the three names live in `log_trade.py`, not `config.py`.
  * **`journal/my_trades.csv` MAY NOT EXIST WHEN YOU ARRIVE**, and that is
    correct. **A Mirror that crashes on an empty journal greets him with a
    traceback on the day he first tries it.** **If it DOES exist, every row is
    real and yours to protect: read it, never write it.**
  * **NO GRADING AT ENTRY TIME REMAINS ABSOLUTE.** The logger never judges.
    The Mirror is the only thing allowed to, and **arithmetic only.**
  * **THE 1%-RISK COMPARISON NEEDS A DECISION HE HAS NOT MADE.** Desk item 13:
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
   **>>> AND COUNT TICKS BY CHARACTER, NOT BY BYTE.** The tick is three bytes
   in UTF-8. I briefly had "278 ticks" for a gate that ran 70 and caught it
   only because the arithmetic did not divide.
2. **NAME YOUR AWKWARD EDGE CASES IN `PROGRESS_LOG.md` BEFORE YOU WRITE CODE**
   and commit them with no code in that commit. **Mine named all six and the
   repair went in first time because of it.**
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
    not a proof** — the recipe in the orders three generations ago was wrong
    for six of the seven files in its own table.

    **>>> THE PREFIX HASH FOR `journal/log_trade.py` HAS CHANGED AND THE OLD
    ONE IS DEAD.** The production half is unchanged, but the FILE is longer.
    Do not compare against `7d9252b099d38df9` / `652378043e01b8e4` — those were
    the 287-line and 286-line prefixes of the pre-repair file. **The production
    half is still lines 1-286 and is still byte-identical to HEAD normalised;
    prove it that way.**

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.** Check (m)'s R2 is the worked example.
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **>>> CERTIFY BY ATTACK, NOT BY THE DRILL — AND THIS SHIP HAS NEVER HAD
    CLEARER EVIDENCE.** GATE 5.1's drill contains **T10, a sabotage for the
    exact fault I installed as A1. It ran. It reported CAUGHT. The fault walked
    through anyway**, because T10 replaces `_stamp` wholesale and never reaches
    the edited branch. **A drill only ever proves a gate can catch a
    monkeypatch.**
(h) **PROVE YOUR WITNESS CAN SEE THE FAULT BEFORE YOU BELIEVE ITS VERDICT.**
(i) **NEVER RUN A WITNESS AND A GATE AGAINST THE SAME COPY.**
(j) **TELL YOUR GATE HOW MANY CHECKS IT OWES.** `journal/log_trade.py` (now 70)
    is still the only gate on this ship that does.
(k) **A FAILING GATE MUST STILL BE ABLE TO FINISH REPORTING.** Guard your
    detail lines. **This was exercised for real this evening: the renamed-
    archive fault leaves no file for R4 and R5 to read, and the gate printed
    four honest reds instead of a traceback.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **>>> `cockpit/carry.py --gate` CAN GO RED THROUGH NO FAULT OF THE FILE IF YOU
  RUN IT WITHIN SECONDS OF A FUNDING SETTLEMENT (00:00, 08:00, 16:00 UTC).**
  R-069, deliberate. **Re-run it once, away from the settlement, before
  concluding anything.**
- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Outside a settlement window a red funding gate is REAL.
- **`cockpit\whales.py --gate` AND `cockpit\carry.py --gate` BOTH BIND A LOCAL
  PORT.** **`journal/log_trade.py --gate` binds no port and touches no network
  — but it now LAUNCHES TWO CHILD INTERPRETERS** (check (i) and check (m)).
  If your machine is slow, they get 90 seconds each and a timeout is RED.
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories.
- **S6, F10 AND B1 NO LONGER GO RED.** If any does, it is a regression and
  SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **>>> GATE TIMINGS ON RECORD ARE WEATHER REPORTS, NOT CHECKS.** `carry` is
  recorded at ~35 s and took **5 seconds** today; `fear_greed` is recorded at
  ~40 s and took **63**. **Fifth time a recorded timing has proved to be one
  unrepresentative reading. Never conclude a check was skipped because a gate
  was fast — read its output.**
- **>>> `journal/my_trades.csv` DOES NOT EXIST AND THAT IS CORRECT.** Do not
  create it. **If it exists, he has logged a real trade and every row is his:
  read it, never write it, and NEVER drive `python journal\log_trade.py` by
  hand against the real journal.** **And remember a no-`path` call writes into
  whatever `journal/` folder the module sits in — that is what check (m) is
  built around and what contaminated my first rig.**
- **THE BRIEF WENT 2/3 TWICE.** It was **3/3** today. **KEEP THE WHOLE OUTPUT
  OF YOUR FIRST BRIEF RUN, not the tail.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.**
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **THE EXEMPTION IS SPENT AND IT STAYED SPENT.** I held none and asked for
   none. **You do the same, and write the same into the orders you leave.
   NEVER WRITE ONE — only he grants one, in words.**
2. **>>> R-072: HE RULED SERIOUS — *"ok lets fix it"*. IT IS REPAIRED.** R-072
   and R-078 are both open against that repair and **only a session that
   neither found the fault nor wrote the fix may clear them. That is you.**
3. **R-060: HE RULED "CORRECT IT".** Corrected. R-066 open, four of five doubts
   untested.
4. **R-054 IS SMALL** (2026-08-11). **R-047 AND R-048 ARE SMALL** (2026-08-05).
5. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
6. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
7. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
8. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording.
9. **DOOR 3 IS BUILT IN THE CALENDAR, THE WHALE WATCH, THE CARRY MONITOR AND
   THE TRADE LOGGER. R-025 IS CLEARED.** Residue R-033. **`news.py` is the one
   without it (R-046).**
10. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
11. **THE CONTEXT DECK AND THE CARRY MONITOR ARE INFORMATION AND CAN NEVER
    BECOME SIGNALS.** **Phase 6's three slots are locked BY NAME:
    Turtle/Donchian, funding-rate fade, on-chain cycle thermometer.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> DOES THE CARRY LINE READ AS INFORMATION, OR AS A SUGGESTION?** He was
   shown it on 2026-08-19, asked directly, and **has still not answered. ASK
   AGAIN — this is the fourth session carrying it.** It prints a percent-a-year
   figure, the closest this ship has come to something that sounds like an
   opportunity, and **Step 2.2 forbids a machine answering that by predicting
   him.**
2. **AND BESIDE THAT QUESTION:** the figure is the funding yield on the PERP
   NOTIONAL. Running the trade needs money on BOTH legs at once, so **the
   return on the capital he would actually deploy is lower than the number on
   the line.** **Not a defect — the arithmetic is right for what the line
   names. His call.**
3. **>>> R-077 — SHOULD IT BE FIXED NEXT? It is the same shape as what he just
   ruled SERIOUS.** `cockpit/whales.py`'s `_get` hangs forever if its timeout
   is ever lost, and GATE 3.5-R1 prints 107/0 either way. **I did not repair it
   because he ruled on R-072 and not on this.** **MEASURED: all seventeen
   network calls on the ship carry a timeout today**, so it is a gate hole, not
   a live fault. **One repair under one ruling — but he may want the pair.**
4. **R-070: NO GATE ON THIS SHIP KNOWS HOW MANY CHECKS IT SHOULD RUN**, except
   `journal/log_trade.py`. **The other seven have not had the repair. One line
   each.**
5. **R-049 — offer it a SEVENTH time.** The X1 repair in `cockpit/news.py` is
   self-marked and runs on every headline he sees. The measurement that argues
   for leaving it: 136 real headlines, not one carrying markup.
6. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** — how long Binance really
   goes between bucket updates (`MAX_AGE_MIN = 30`), and how far the BTC figure
   really moves between two calls seconds apart.
7. **THE CATEGORY B PILE IS FORTY-FIVE.** Cleared before the ship is used for
   real, at the same moment `cockpit/brief.py` gets its gate. **Keep saying the
   number.**
8. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR**, the only thing he personally
   owes the R-037 repair. **It switches ON Windows' diary of scheduled jobs,
   which ships switched off** — so that if the monthly open-interest job ever
   fails silently, there is a record of why:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

9. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
10. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
    Bitcoin.com.
11. **THE RULES HE HAS NOT YET ADOPTED**, each earned many times over: *"A
    SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS
    ANYTHING"*; *"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT TURNS
    OVER"*; **candidate Law 8 — "a claim about how something behaves is not a
    fact until it has been run"**; **"A GATE MUST BE TOLD HOW MANY CHECKS IT
    OWES"**; and **"A GATE MUST BE MADE TO CALL THE THING THE WAY ITS ONLY REAL
    CALLER CALLS IT"** — which he has now effectively ruled on once, by ordering
    this repair.
12. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
13. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, and the
    Mirror needs it the moment anybody builds it.**
14. **`MAX_PLAUSIBLE_RATE` in `cockpit/funding.py`** — measured 13-16x looser
    than Binance's published cap. **Recommendation: tighten to ~0.01. STILL NOT
    DONE.** `cockpit/carry.py` shipped with exactly that bound.
15. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py`,
    `cockpit/carry.py` and `journal/log_trade.py` are the worked examples.**
16. **The settled-rate anchor (R-004).**
17. **ALL FIVE CONTEXT DECK LINES AND THE CARRY LINE ARE ON THE BRIEF.** **The
    trade logger is NOT on the Brief and never will be — it is a command he
    runs, not a line he reads.**
18. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED TWELVE TIMES, NOT ADOPTED.**

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

1. **`PROGRESS_LOG.md`, the three entries of 2026-08-20 (afternoon and
   evening)** — the attack, the contaminated rig, THE FINDING REPORT, the bar,
   and the repair. The file is ~834 KB; **do not read it all.**
2. **`journal/log_trade.py`** — production half lines 1-286 (**unchanged by the
   repair**), gate from 287, **check (m) from line 990.**
3. **`REVIEW_QUEUE.md`, R-072, R-076, R-077 and R-078.**
4. **`EXECUTION_PLAN.md` PHASE 5** and the CURRENT POSITION MARKER.
5. **`PROGRESS_LOG.md` 2026-08-20 (evening), "THE CONDITIONS OF GATE 5.1-R1"** —
   the bar, committed alone before the code existed. **Read it to see what a
   bar looks like when the same session must both declare and meet it, because
   if you reach JOB 2 you are writing GATE 5.2 yourself and nobody is checking
   it before you build.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours. **AND CHECK
  YOUR COMMIT HASHES AGAIN AFTER YOU PUSH** — a rebase over its push has now
  rewritten a hash twice, including mine this afternoon.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes
  in a payload** — use `bytes([10])` or `chr(10)`.
- **>>> AN ANCHOR MUST NEVER SPLIT A CRLF PAIR**, and must match exactly once.
  **Write your writer to REFUSE on both, on a bare LF in the result, on an edit
  that changes nothing, and — new this evening — ON ANY RESULT WHOSE PRODUCTION
  HALF MOVED.** Mine did all five and the refusals earned themselves twice
  today.
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
    2. REVIEW_QUEUE.md .... your verdict on R-078 (and R-072, and R-076 —
                            all three are yours to clear), plus one OPEN item
                            against your own work.
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
