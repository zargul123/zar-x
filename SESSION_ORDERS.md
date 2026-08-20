# ZAR X — **YOUR SESSION IS DECIDED BY ONE THING THE COMMANDER SAYS OUT LOUD: HIS RULING ON R-072. ASK HIM FIRST, BEFORE YOU TOUCH ANYTHING. BOTH ANSWERS ARE WRITTEN OUT BELOW AND YOU DO NOT NEED TO THINK OF A THIRD.**

*Written 2026-08-20 (afternoon) by the twenty-fifth generation, which attacked
`journal/log_trade.py`, found three real faults walking through GATE 5.1, graded
the finding BORDERLINE, **repaired nothing and built nothing** — because
BORDERLINE means report and stop. **I held no exemption and I grant you none.
Only the Commander may grant one, and only in words.***

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

**I did not build anything, so there is nothing of mine to attack in the usual
way.** What I did instead was attack my predecessor's work and find something.
**So your session begins with a question, not a task:**

    ASK HIM:  "R-072 was graded BORDERLINE. Do you rule it SERIOUS or SMALL?"

    HE SAYS SERIOUS (or "fix it")  ->  JOB A. Repair GATE 5.1 under a bar you
                                       declare and commit ALONE first. Then
                                       STOP. Build no Mirror.
    HE SAYS SMALL                  ->  JOB B. File it CATEGORY B (the pile
                                       becomes forty-five) and BUILD
                                       `journal/mirror.py` under GATE 5.2,
                                       which you declare and commit ALONE
                                       first.

**AND WHICHEVER HE SAYS, YOU ALSO OWE JOB C: ATTACK MY WORK.** I filed R-076
against my own attack and I may not clear it. **You did not build it, so you
may.** It is short and it is real — my first rig was contaminated and scored two
live escapes as CAUGHT.

**IF HE IS NOT AVAILABLE TO RULE, DO JOB C AND STOP.** Do not guess his ruling.
Do not build the Mirror on an assumption about what he would have said —
**a machine predicting him is exactly what Step 2.2 of the form forbids.**

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
    journal/log_trade.py        GATE 5.1      PASSED  exit 0  0 red   64 green
      the same file at TZ=UTC0  GATE 5.1      PASSED  exit 0  0 red   64 green
    1,013 green across the FOURTEEN · vault INTACT 6 of 6 · Brief 3/3
    lab/ untouched · journal/my_trades.csv DOES NOT EXIST

**PHASE 4 IS COMPLETE. PHASE 5 IS STILL HALF BUILT — THE MIRROR DOES NOT EXIST
AND I DID NOT START IT.**

## What I did, in seven lines

1. **Proved the ship alive first** — fourteen invocations, 1,013 green, red
   counted by machine three ways, every hit read by eye. **The funding gate's
   "escaped" trap did not fool me because the orders named it.**
2. **Attacked `journal/log_trade.py` with six faults installed as TEXT EDITS**
   in copies outside the repo, control first. **THREE ESCAPED, THREE WERE
   CAUGHT.**
3. **The three escapes are ONE hole: GATE 5.1 never drives the doorway the way
   the shell drives it** — no `path`, no `now` — so `TRADES_FILE` and
   `datetime.now(timezone.utc)` are judged by nothing.
4. **Graded BORDERLINE. Repaired nothing. Built nothing.** R-072 OPEN.
5. **MY OWN RIG WAS CONTAMINATED FIRST TIME AND SCORED TWO LIVE ESCAPES AS
   `CAUGHT`.** I found it by reading which check went red. R-076 is filed
   against my attack and **is yours to attack.**
6. **R-066 IS NO LONGER UN-ATTACKED.** I attacked its doubt 2 and it was right:
   `_get` loses its timeout and hangs forever while GATE 3.5-R1 prints 107/0.
   **R-077, CATEGORY B. Four of R-066's five doubts are still untested.**
7. **THE CATEGORY B PILE IS FORTY-FOUR.** Nothing was cleared by anybody,
   including me — **I could have cleared R-072 and did not, because it did not
   survive.**

---

# **JOB A — ONLY IF HE RULES SERIOUS: REPAIR GATE 5.1'S BLIND SPOT, THEN STOP**

## What is wrong, in one paragraph

The only real caller of the logger is line 314: **`log_trade(*answers)` — no
`path`, no `now`.** All 64 of GATE 5.1's checks either inject both, or (check
(a)'s first call) inject `path=` and then inspect only the first eight
characters of the returned line. **So the two values the production path
resolves from the module's own constants — `TRADES_FILE` and
`datetime.now(timezone.utc)` — are checked by nothing at all.**

**THE SHIPPED FILE IS CORRECT TODAY. MEASURE IT YOURSELF BEFORE YOU BELIEVE ME:**
the control's stamp offset from true UTC is `+0.00 hours`. **You are repairing a
gate, not a bug.**

## What the repair looks like — described, not prescribed

Three checks that drive the doorway with **no `path` and no `now`**, plus
`EXPECTED_CHECKS` moving from 64 to 67.

  * **the stamp** — assert it is within a few seconds of a UTC clock the gate
    reads ITSELF, and that it carries `+00:00`. **A tolerance is required here
    and you must say what it is and why**; R-069 is what a zero-tolerance live
    check costs.
  * **the address** — assert `TRADES_FILE`'s basename is `my_trades.csv` **and
    that its folder is the module's own folder.** B14 moved an archive with
    every row inside it perfect.
  * **>>> THE TRAP, AND IT IS THE WHOLE DIFFICULTY: A NO-`path` CALL WRITES
    INTO THE REAL `journal/` FOLDER.** You may not simply call it. Run it in a
    **CHILD INTERPRETER against a COPY of the module in a temporary tree** —
    the gate already owns exactly that machinery in check (i), and check (i)
    already passes a journal path to its child for this reason. **Monkeypatching
    `TRADES_FILE` defeats the entire point of the check.**

## The bars this repair must meet

1. **DECLARE THE BAR IN `PROGRESS_LOG.md` AND COMMIT IT ALONE, NO `.py` IN THAT
   COMMIT.** `git show --stat` is what proves it came first.
2. **RE-RUN MY THREE ORIGINAL FAULTS AGAINST YOUR REPAIR** as TEXT EDITS in
   copies outside the repo, control first. **All three must turn the gate red.**
   They are, exactly:
   * in `_stamp`, `datetime.now(timezone.utc)` -> `datetime.now().replace(tzinfo=timezone.utc)`
   * in `_stamp`, `datetime.now(timezone.utc)` -> `datetime(2020, 1, 1, tzinfo=timezone.utc)`
   * `TRADES_FILE = os.path.join(JOURNAL_DIR, 'my_trades.csv')` -> `'trades.csv'`
   **>>> THE SHORT ANCHOR FOR THE FIRST TWO MATCHES TWICE** — the gate's own
   T10 sabotage `_stamp_local` copies the production line character for
   character. **Lengthen the anchor to the line after it and make your writer
   REFUSE rather than replace both.**
3. **The production half of `journal/log_trade.py` must not change at all.**
   Prove it with `git`, not with a hash: compare the working tree against
   `git show HEAD:journal/log_trade.py` with CRLF normalised to LF on both
   sides, and separately assert the working tree has zero bare LF.
4. **File a review item against your own repair and leave it open.**
5. **THEN STOP. BUILD NO MIRROR.** A repair and a build in one session is how
   six consecutive generations got away with grading their own work.

---

# **JOB B — ONLY IF HE RULES SMALL: BUILD `journal/mirror.py` (PHASE 5, SECOND HALF)**

**A half-built Mirror is worse than no Mirror. If you run short, do JOB C
properly and leave this entirely.**

## >>> GATE 5.2 DOES NOT EXIST. YOU DECLARE IT, AND YOU COMMIT IT ALONE.

GATE 4.1 and GATE 5.1 were both declared by a session that then stopped, and
**both are the bars that survived attack best, because not a word of either
could be bent to match what got built.** You do not have that luxury. **Declare
GATE 5.2 in `PROGRESS_LOG.md`, commit it with NO `.py` in that commit, and only
then write code.**

**WHAT THE PLAN ASKS** (`EXECUTION_PLAN.md` Phase 5, item 2): monthly, the
Commander's logged trades vs what the system's instruments said at those moments
(from `journal/snapshots_*.csv`) vs what a disciplined 1%-risk version of the
same trades would have done. **Output: plain-words report. No shaming,
arithmetic only. NEVER a signal.**

**FIVE THINGS YOU WILL MEET ON YOUR FIRST AFTERNOON, NAMED SO THEY DO NOT
AMBUSH YOU:**

  * **>>> THE TWO FILES DISAGREE ABOUT WHAT A TIME LOOKS LIKE. THAT IS R-074.**
    `my_trades.csv` writes `2026-08-20T09:30:15+00:00`; **every snapshot row
    since Phase 2 says `2026-07-21 11:35` with no zone at all.** Decide the
    reconciliation deliberately and **write the decision down BEFORE coding**;
    do not discover it in a join.
    **>>> AND READ THIS BEFORE YOU TOUCH IT: R-072's whole finding is that the
    stamp line in `log_trade.py` is guarded by nothing. You are the session
    with its hands on that exact line. If you change how a stamp is made,
    YOU are the one mistake the finding counted.**
  * **THE ASSET NAMES WERE MADE TO MATCH ON PURPOSE.** `log_trade.py` stores
    `BTC-USD`, the same string every snapshot row uses. **No translation table
    is needed.** That was a Law 2 decision and the three names live in
    `log_trade.py`, not in `config.py`.
  * **`journal/my_trades.csv` MAY NOT EXIST WHEN YOU ARRIVE**, and that is
    correct — his first real trade creates it. **A Mirror that crashes on an
    empty journal greets him with a traceback on the day he first tries it.**
    **If it DOES exist, every row is real and yours to protect: read it, never
    write it, and never drive `python journal\log_trade.py` by hand against the
    real journal.**
  * **NO GRADING AT ENTRY TIME REMAINS ABSOLUTE.** The logger never judges. The
    Mirror is the only thing on this ship allowed to, and **arithmetic only.**
  * **THE 1%-RISK COMPARISON NEEDS A DECISION HE HAS NOT MADE.** Desk item 14:
    the 25% position cap means real risk is ~0.49% per trade, not 1%. **The plan
    asks you to compare against "a disciplined 1%-risk version". Ask him which
    number that means before you code it.**

---

# **JOB C — YOU OWE THIS WHATEVER HE RULES: ATTACK MY WORK (R-076), AND THE FIVE DOUBTS NOBODY HAS EVER ATTACKED**

**This is the Part 1 you owe. I built nothing, so what you attack is my
ATTACK — and the parts of `journal/log_trade.py` that neither its author nor I
ever touched.**

## R-076 — against my own attack. **You may clear it. I may not.**

Its five doubts are in `REVIEW_QUEUE.md`. The one worth your time first:

**>>> MY FIRST RIG WAS CONTAMINATED AND REPORTED TWO LIVE ESCAPES AS `CAUGHT`.**
My witness calls the doorway with **no `path`**, which writes into the copy's
own `journal/` folder. I ran it against the **same copy** I then gated, so the
gate's last check — *"the REAL journal was never created or touched"* — went red
for a reason of **my own making**, and both faults were scored CAUGHT by a red I
had planted. **I found it by reading WHICH check went red instead of accepting
the verdict. Nothing in my rig would have told me.**

**The obvious question for you: is my SECOND rig contaminated in some way I
also cannot see?** Run it. It is in the scratchpad but **treat it as untrusted
and rebuild it if you prefer** — that is a better use of your time than reading
mine.

## The five doubts of R-072 that NOBODY has attacked — not its author, not me

I attacked one family only: the production calling convention. **A gate is
strongest exactly where it has been attacked, which is the same as saying it is
weakest everywhere else.** These five are its author's own list and are **still
untouched by anybody:**

1. **>>> THE SEVEN INTERACTIVE QUESTIONS ARE TESTED BY NOBODY.** Every one of
   the 64 checks calls the doorway directly, so **the ORDER of the seven
   `input()` calls is checked by nothing.** Swap two and his exit price goes
   into the size field forever, with the gate still printing 64/0. **I read the
   order by eye and it is correct today — that is reading, not a check.**
2. **`_needs_header` decides on `os.path.getsize`.** A journal whose header
   somebody deleted by hand, leaving the rows, never gets one back.
3. **A partial write** (R-073). The row reaches the disk in ONE `write` call;
   that is not an atomicity guarantee.
4. **The refusal messages echo his own text back with `!r`.**
5. **`_feeling` lower-cases and `_why` does not.**

**AND ONE I FOUND BUT COULD NOT REACH, WHICH IS WHY IT IS A NOTE AND NOT A
FINDING:** check (d) proves eighteen **validation** refusals write nothing. It
never exercises `log_trade`'s `except OSError` / `except Exception` branch —
**the only branch that can return `[not logged: ...]` while bytes are already on
the disk.** If he re-logged a trade he was told was not logged, D3 says the
duplicate is kept and the Mirror grades him on a trade he made once. **I could
not reach that branch with one edit and I did not manufacture a way. It sits
next to R-073 and remains unexamined.**

## R-066 — four of five doubts still untested

**Stop saying "un-attacked" — it is no longer true and I did the work.** Say
this instead: **"R-066 is OPEN with four of its five doubts untested."** Doubt 2
was attacked and was right (R-077). Doubts 1 (real-venue behaviour: redirects,
gzip, a 429 with `Retry-After`, a reset mid-body), 3 (the listening socket under
a firewall or a real proxy), 4 and 5 are untouched by anybody.

---

# WHAT YOU STILL OWE, WHATEVER YOU DO

1. **PROVE THE SHIP IS ALIVE FIRST.** All FOURTEEN invocations, output to a
   file, **red counted BY MACHINE three ways** (the tick character, the first
   word of a line, and `GATE ... FAILED`), **then READ any hit with your own
   eyes.** `collection_guard.py` prints `OK`/`FAIL`, not ticks; `fear_greed.py`
   and `funding.py` both carry **FAILURE** at the start of a line inside their
   own PASS text; **and `funding.py` line 69 starts a line with "escaped" — it
   fooled three consecutive sessions and did NOT fool the fourth, because these
   orders named it. Keep naming it.**
2. **NAME YOUR AWKWARD EDGE CASES IN `PROGRESS_LOG.md` BEFORE YOU WRITE CODE**
   and commit them with no code in that commit.
3. **Confine the change and PROVE the confinement** — `git` as the primary
   proof, not a hash. See (a) below.
4. **RUN THE GATE. Every check green, every sabotage CAUGHT.** A failing gate is
   never committed and never called "mostly passed".
5. **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.**
6. `git status` clean when you finish.

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT ALREADY READS CHANGES** except what your orders call
    for — prove it two ways, never assert it.

    **>>> THE PROOF THAT NEEDS NO RECIPE AND CANNOT DRIFT, AND THE ONE YOUR
    CONFINEMENT SHOULD STAND ON:** compare each file's working-tree bytes
    against `git show HEAD:<file>` **with CRLF normalised to LF on both
    sides**, and separately assert the WORKING TREE has zero bare LF. That
    answers "did the content change" and "are the line endings right" as two
    different questions, and neither depends on anybody's recipe. **A hash
    whose recipe nobody can reproduce is a number, not a proof — and the recipe
    in the orders two generations ago was wrong for six of the seven files in
    its own table.**

    The prefix hashes are kept below only so a number found elsewhere can be
    identified. **CRLF, WITH a trailing separator, excluding the anchor line:**

        file                     __main__  WITH trailing CRLF  WITHOUT
        cockpit/fear_greed.py      113     bb31626c493a1ac6    d09fba1dde6d9517
        cockpit/funding.py         160     95069d1bef8316d7    2dab48ecb0d00927
        cockpit/news.py            272     503663762315b2f2    6f4f69f4377e4158
        data/collection_guard.py   156     d6518cd7208eb611    c0f41d6044225baf
        cockpit/events.py          372     6fc5ce7d67aa8f24    481f97bdf59980f3
        cockpit/whales.py          363     d2cd1b58373d2fcb    7a7926f5badb7f3d
        cockpit/carry.py           416     540e057ad7a2cd40    ec5455596007b590
        journal/log_trade.py       287     7d9252b099d38df9    652378043e01b8e4

    **AND `data/open_interest.py` STILL CANNOT BE HASHED THIS WAY: the anchor
    appears TWICE in it.** Refuse, and prove it untouched with `git status`.

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.**
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **>>> CERTIFY BY ATTACK, NOT BY THE DRILL — AND THIS SESSION IS THE
    STRONGEST EVIDENCE YET.** GATE 5.1's drill contains **T10, a sabotage for
    the exact fault I installed as A1. It ran. It reported CAUGHT. And the fault
    walked through anyway**, because T10 replaces `_stamp` wholesale and never
    reaches the edited branch. **A drill only ever proves a gate can catch a
    monkeypatch.** Install the real fault as a TEXT EDIT in a copy outside the
    repo, run the untouched control FIRST, and report both.
(h) **>>> AND THE NEW ONE THIS SESSION EARNED: PROVE YOUR WITNESS CAN SEE THE
    FAULT BEFORE YOU BELIEVE ITS VERDICT.** My first witness logged one trade
    with a lower-case feeling, and against it two of my six faults were
    byte-identical to the control. **A witness's blindness is invisible from
    inside the witness.** Give it two rows, mixed case, and a comma.
(i) **>>> AND THE OTHER ONE: NEVER RUN A WITNESS AND A GATE AGAINST THE SAME
    COPY.** A witness that exercises the production path WRITES, and what it
    writes turns the gate red for reasons that are not the fault. **Two copies.
    This cost me my first two results.**
(j) **TELL YOUR GATE HOW MANY CHECKS IT OWES.** `journal/log_trade.py` is still
    the only gate on this ship that does.
(k) **A FAILING GATE MUST STILL BE ABLE TO FINISH REPORTING.** Guard your
    detail lines.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **>>> `cockpit/carry.py --gate` CAN GO RED THROUGH NO FAULT OF THE FILE IF YOU
  RUN IT WITHIN SECONDS OF A FUNDING SETTLEMENT (00:00, 08:00, 16:00 UTC).**
  That is R-069 and it was deliberate. **Re-run it once, away from the
  settlement, before concluding anything.**
- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021) —
  the same three times. Outside a settlement window a red funding gate is REAL.
- **`cockpit\whales.py --gate` AND `cockpit\carry.py --gate` BOTH BIND A LOCAL
  PORT.** If your machine refuses the port, those checks go red and it is the
  machine. **`journal/log_trade.py --gate` binds no port and touches no
  network at all.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories.
- **S6, F10 AND B1 NO LONGER GO RED.** If any does, it is a regression and
  SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **>>> GATE TIMINGS ON RECORD ARE WEATHER REPORTS, NOT CHECKS.** `carry` is
  recorded at ~35 s and took **5 seconds** today; `fear_greed` is recorded at
  ~40 s and took **63**. **This is the fifth time a timing on record has turned
  out to be one unrepresentative reading. Never conclude a check was skipped
  because a gate was fast — read its output.**
- **>>> `journal/my_trades.csv` DOES NOT EXIST AND THAT IS CORRECT.** Do not
  create it. **If it exists, the Commander has logged a real trade and every row
  in it is his: read it, never write it, and NEVER drive
  `python journal\log_trade.py` by hand against the real journal.** Drive it in
  a copy outside the repo. **And remember that a no-`path` call writes into
  whatever `journal/` folder the module sits in.**
- **THE BRIEF WENT 2/3 TWICE** (2026-08-19 and once before). It was **3/3**
  today and the drop did not reproduce. **KEEP THE WHOLE OUTPUT OF YOUR FIRST
  BRIEF RUN, not the tail**, and capture which asset drops if it happens.
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.**
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **THE EXEMPTION IS SPENT AND IT STAYED SPENT.** I held none and asked for
   none. **You do the same, and you write the same into the orders you leave.
   NEVER WRITE ONE — only he grants one, in words.**
2. **R-060: HE RULED "CORRECT IT".** It is corrected. R-066 against that repair
   is **open, with four of five doubts untested.**
3. **R-054 IS SMALL** (2026-08-11). **R-047 AND R-048 ARE SMALL** (2026-08-05).
4. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
5. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
6. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
7. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`.
8. **DOOR 3 IS BUILT IN THE CALENDAR, THE WHALE WATCH, THE CARRY MONITOR AND
   THE TRADE LOGGER. R-025 IS CLEARED.** Residue R-033. **`news.py` is the one
   without it (R-046).**
9. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
10. **THE CONTEXT DECK AND THE CARRY MONITOR ARE INFORMATION AND CAN NEVER
    BECOME SIGNALS.** **Phase 6's three slots are locked BY NAME:
    Turtle/Donchian, funding-rate fade, on-chain cycle thermometer.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> HIS RULING ON R-072. THIS ONE DECIDES YOUR SESSION AND IT IS FIRST FOR
   THAT REASON.** BORDERLINE, recommended by a session that did not build the
   thing. The full Finding Report is in `PROGRESS_LOG.md` 2026-08-20
   (afternoon). **The honest counter-argument is in there too: R-070 and R-071
   were gate holes and he graded them SMALL, and grading this one SMALL is a
   completely defensible reading of his own form.**
2. **>>> DOES THE CARRY LINE READ AS INFORMATION, OR AS A SUGGESTION?** He was
   shown it on 2026-08-19, asked directly, and **has still not answered. ASK
   AGAIN — this is the third session carrying it.** It prints a percent-a-year
   figure, the closest this ship has come to something that sounds like an
   opportunity, and **Step 2.2 forbids a machine answering that question by
   predicting him.**
3. **AND BESIDE THAT QUESTION:** the figure is the funding yield on the PERP
   NOTIONAL. Running the trade needs money on BOTH legs at once, so **the
   return on the capital he would actually deploy is lower than the number on
   the line.** The footer says "capital tied up on BOTH legs at once" and does
   not quantify it. **Not a defect — the arithmetic is right for what the line
   names. His call.**
4. **R-077 — the whale watch hangs forever if `_get`'s timeout is ever lost, and
   GATE 3.5-R1 prints 107/0 either way.** CATEGORY B. **All seventeen network
   calls on the ship carry a timeout today — measured.**
5. **R-070: NO GATE ON THIS SHIP KNOWS HOW MANY CHECKS IT SHOULD RUN**, except
   `journal/log_trade.py`. **The other seven have not had the repair. It is one
   line each.**
6. **R-049 — offer it a SEVENTH time.** The X1 repair in `cockpit/news.py` is
   self-marked and runs on every headline he sees. The measurement that argues
   for leaving it: 136 real headlines, not one carrying markup.
7. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** — how long Binance really
   goes between bucket updates (`MAX_AGE_MIN = 30`), and how far the BTC figure
   really moves between two calls seconds apart.
8. **THE CATEGORY B PILE IS FORTY-FOUR** (forty-five if he rules R-072 SMALL).
   Cleared before the ship is used for real, at the same moment
   `cockpit/brief.py` gets its gate. **Keep saying the number.**
9. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR**, the only thing he personally
   owes the R-037 repair:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

10. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
    RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
11. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
    Bitcoin.com.
12. **THE RULES HE HAS NOT YET ADOPTED**, each now earned many times over: *"A
    SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS
    ANYTHING"*; *"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT TURNS
    OVER"*; **candidate Law 8 — "a claim about how something behaves is not a
    fact until it has been run"**; **"A GATE MUST BE TOLD HOW MANY CHECKS IT
    OWES"**; and **NEW, EARNED 2026-08-20 (afternoon) — "A GATE MUST BE MADE TO
    CALL THE THING THE WAY ITS ONLY REAL CALLER CALLS IT."**
13. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
    **The Brief has dropped an asset twice; it was 3/3 today.**
14. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, and the
    Mirror needs it the moment anybody builds it: the plan asks it to compare
    his trades against "a disciplined 1%-risk version of the same trades."**
15. **`MAX_PLAUSIBLE_RATE` in `cockpit/funding.py`** — measured 13-16x looser
    than Binance's published cap. **Recommendation: tighten to ~0.01. STILL NOT
    DONE.** `cockpit/carry.py` shipped with exactly that bound.
16. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py`,
    `cockpit/carry.py` and `journal/log_trade.py` are the worked examples built
    the right way from birth.**
17. **The settled-rate anchor (R-004).**
18. **ALL FIVE CONTEXT DECK LINES AND THE CARRY LINE ARE ON THE BRIEF.** **The
    trade logger is NOT on the Brief and never will be — it is a command he
    runs, not a line he reads.**
19. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED TWELVE TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**

---

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None
of it is repeated here.**

1. **`PROGRESS_LOG.md`, the entry of 2026-08-20 (afternoon)** — the attack, the
   contaminated rig, and **THE FINDING REPORT in full**. The file is ~817 KB;
   do not read it all.
2. **`journal/log_trade.py`** — production half lines 1-286, gate from 287.
   **The hole is that nothing in the gate calls it the way line 314 calls it.**
3. **`REVIEW_QUEUE.md`, R-072 and R-076 and R-077** — my verdict, my doubts
   about my own attack, and the whale-watch timeout.
4. **`EXECUTION_PLAN.md` PHASE 5** and the CURRENT POSITION MARKER.
5. **`PROGRESS_LOG.md` 2026-08-19 (morning, second part) — GATE 5.1** — read it
   to see what a bar declared by a non-builder looks like, because **if you
   reach JOB B you are writing GATE 5.2 yourself and nobody is checking it
   before you build.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` or `chr(10)` for a newline.
- **>>> AN ANCHOR MUST NEVER SPLIT A CRLF PAIR**, and must match exactly once.
  **Write your writer to REFUSE on both, and to refuse a result carrying a bare
  LF.** Mine did all three and **the refusal earned itself within the hour**:
  the natural one-line anchor for `_stamp` matches TWICE, because the gate's own
  T10 sabotage copies the production line character for character.
- **>>> A FILE WRITTEN BY AN EDITOR TOOL ARRIVES AS LF ON THIS MACHINE.**
  **Check the endings of anything you create, before you commit it.**
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
  **Comparing CONTENT against the blob, with both sides normalised, is fine and
  is the best confinement proof there is.**
- **`.bat` FILES MUST BE CRLF, AND KEEP THEM ASCII-ONLY.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING**, and write documents with an editor
  tool or a binary appender, not with `cat <<EOF`. **A here-string mangled a
  harness twice this session before I gave up and used a file.**
- **>>> SET `PYTHONUTF8=1` ON YOUR OWN HARNESS TOO, NOT ONLY ON THE GATE.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
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
    2. REVIEW_QUEUE.md .... your verdict on R-076, plus one OPEN item against
                            your own work. **R-072 stays open until he rules.
                            R-066 stays open until four more doubts are tested.**
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; add what you MEASURED.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words brief.
                            **>>> AND THEIR JOB 1 IS: ATTACK WHAT YOU BUILT.
                            YOU MAY NOT GRANT AN EXEMPTION.**
    6. Commit. Push. **Then check your commit hashes again** — a rebase over
       the cloud watchman's push has rewritten one before.
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**
