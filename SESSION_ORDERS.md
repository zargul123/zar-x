# ZAR X PHASE 3 — **ATTACK GATE 3.2b-R7 (R-024). THEN FINISH R-022: THREE OF ITS SEVEN DOUBTS ARE STILL UNTOUCHED AND ONE OF THEM IS ITS AUTHOR'S OWN STRONGEST LEAD.**

*Written 2026-07-30 (morning) by the session that attacked R-020, found that
sabotage B9 had never tested anything, and repaired it. **I may not clear my own
repair. That is your Part 1.***

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is the exact bars and commands. This part is the story, so
you understand WHY before you read WHAT. The Commander is not a programmer and
asked for it in this form. Write your own report to him the same way.*

## Where the ship is

**THE TENTH GENERATION FOUND SOMETHING, AND IT WAS HIDING IN THE ONE PLACE
NOBODY HAD LOOKED: the thing that INSTALLS a sabotage.**

    data/open_interest.py   GATE 3.2b-R7 PASSED  exit 0  0 red ticks, 14/14 CAUGHT
    cockpit/fear_greed.py   GATE 3.1-R6  PASSED  exit 0  0 red
    cockpit/funding.py      GATE 3.2-R6  — see "what you will walk into" below
    vault INTACT 6/6 · Brief 3/3 · lab/ untouched
    data/oi_history/        3 files, correctly named, 181 lines each, sha256
                            unchanged across every run of my session

## What I found, in one paragraph

Every sabotage in the recorder's drill is installed by rebinding a name:
`globals()[attr] = repl`. **That reaches the module only if the module looks the
name up when it runs.** The recorder's doorway is
`def run(symbols=SYMBOLS, ...)`, and Python evaluates a default argument **once**,
when the `def` executes. `SYMBOLS` is read **nowhere else in the file.** So
sabotage B9 — *"one asset silently dropped from SYMBOLS"* — rebound a name
nothing reads, and **the recorder went on collecting all three assets.** It was
scored CAUGHT by the *first line* of its judge, a name comparison that returns
before the recorder is ever called. **Four generations of this gate printed
`✓ B9 → CAUGHT` under a headline announcing fourteen of fourteen.**

## **AND THE HALF OF THAT WHICH IS NOT ALARMING — DO NOT LET ANYONE DROP IT**

**THE REAL DEFECT WAS ALWAYS CAUGHT.** I edited the real `SYMBOLS` line in a
scratch copy and ran the whole gate against it: exit 1, two red lines, SOLUSDT
visibly missing. **No asset could ever have silently stopped being collected.
What was broken was the EVIDENCE, not the protection.** I graded it SERIOUS
anyway, and the reason is this ship's own rule: *a tally counts only what a
machine actually checked* — which is what voided the 48/48.

## What is now in place, so you know what you are attacking

B9 is a **real text edit** on a copy outside the repo, judged by
`_record_does_the_job` — **the same function the healthy check uses**, not a
second copy that merely agrees with it — and proved to RETURN False rather than
raise. And new check **(n)** proves **the drill's installer is able to install:**
no globals-swap sabotage may target a name this module has frozen as a default
argument, and the check must first FIND the frozen `SYMBOLS` in `run` before its
silence is believed.

## **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

**`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT AND IS GREEN THE
REST OF THE TIME. R-021, CATEGORY B, graded SMALL at the Step 1 veto.**

**BINANCE SETTLES AT 00:00, 08:00 AND 16:00 UTC. CHECK THE UTC CLOCK BEFORE YOU
BELIEVE A RED FUNDING GATE.** I arrived at 07:53 UTC — seven minutes before a
settlement — and **deliberately did not run it until the window cleared**, because
a result from inside the window proves nothing either way. Do the same.

**>>> AND THE WARNING THAT MATTERS MOST: OUTSIDE A SETTLEMENT WINDOW, A RED
FUNDING GATE IS A REAL FAILURE. TREAT IT AS ONE.** A session that shrugs at a red
gate because *"R-021 says it does that"* is doing the exact thing this ship exists
to prevent. **If it is red: check the clock, run it again, and say how many runs
it took.**

**IF YOU REPAIR IT: TIGHTEN THE BRACKET, NEVER THE BAR.** The obvious move is to
allow "close enough" and that is R-001's conviction in one line of diff. The honest
repair is **bounded re-observation** — a fresh bracket, a small fixed number of
times, still demanding EXACT equality against a value Binance actually served.

## **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

**1. `cockpit/brief.py` GETS NO GATE YET.** **NOT NOW, BEFORE GOING LIVE.** Do not
build it and do not re-argue it. **This is NOT the same thing as R-022 doubt 2**,
which is about the Brief's IMPORT SURFACE — see below, and do not confuse them.

**2. R-016 IS DONE AND OFF HIS DESK.** It is still not CLEARED; that is R-022, and
it is a session's job, not his.

**3. R-019 IS CLEARED BY HIM.** Step 2.2 of THE FINDING REPORT carries his own
wording, verbatim, in `THE_PATTERN.md`. **Read it there before you grade
anything.** It is the question that moves findings.

## Your job, in order

**1. ATTACK R-024 — MY REPAIR, GATE 3.2b-R7.** I filed **seven doubts against my
own work.** They are starting points, **not** the assignment.

**2. FINISH R-022.** I attacked it in two directions and both HELD — the ship's
first clean review result. **Three of its author's seven doubts are still
untouched, and doubt 1 is his own strongest lead.**

**3. THE 1 AUGUST ERRAND — CHECK TODAY'S DATE FIRST.** On 2026-07-30 it was NOT
due. **Four sets of orders have now got this wrong in one direction or the other.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment, and the housekeeping that has bitten this ship. None of it is
repeated here. It was NOT edited by me** — I earned no new lesson that the pattern
does not already state.

**Specific to THIS job:**

1. **The LAST entry of `PROGRESS_LOG.md`** — my session. **Read it as a CLAIM, not
   a result. It is what you are auditing.** The file is ~390 KB; reading all of it
   will eat your budget.
2. **`data/open_interest.py`, the `__main__` half only** — specifically
   `_frozen_as_default`, `_installer_can_install`, `_b9_judge_says_no`, the
   `source_override` parameter on `_record_run` and `_record_does_the_job`, and
   B9's entry in `_FILE_SABOTAGES`.
3. **`REVIEW_QUEUE.md` — R-024 and R-022 are your worklist.** Their recorded
   doubts are starting points, **not the assignment. R-006 may NEVER be cleared by
   you or any in-house session.**
4. **`ROADMAP.md`** — the MEASURED facts table. If anything you measure disagrees
   with it, **your measurement wins and you write the correction down.**

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A new sabotage, invented by you, thrown at **Gate 3.2b-R7 (R-024)**, result
   recorded either way.
2. At least one of **R-022's three untested doubts** actually tested — **doubt 1
   preferred** — result recorded either way.
3. Any leak found is graded on THE FINDING REPORT **before** any repair, using
   **the Commander's wording of Step 2.2**, and repaired only if that grade says
   to.
4. `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3, and
   `data/oi_history/` unchanged **unless a legitimate run appended** — in which
   case say so, with the row count, and check it. **Confirm there are exactly
   THREE files named `BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`, `SOLUSDT_4h.csv`** — the
   check B14 earned. They were 181 lines each on 2026-07-30, sha256
   `e3258e82…`, `1549a8a1…`, `e0f91a87…`.

**Four of four or it has not cleared, and "three of four with a good explanation"
is the phrasing this ship exists to refuse.**

---

# PART 1 — MY REPAIR (R-024). **NEVER ATTACKED.**

`python data\open_interest.py` — **~4 minutes, measured.** Fourteen sabotages,
check (n), zero red ticks. **That is the claim under review, not the verdict.**

**Where this repair is strongest — so do NOT spend your time here:** B9 is now a
real binary-mode text edit with a uniqueness guard that refuses to run on an
ambiguous anchor; its judge is the SAME function the healthy path uses; the
untouched source is driven down the new override path FIRST as a control; the
judge is proved to RETURN False rather than raise; the damage is printed in full
rather than summarised; and check (n) carries a positive control that must detect
a frozen default before it certifies that there are none.

## THE SEVEN DOUBTS I FILED AGAINST MY OWN WORK — free hits

1. **`_frozen_as_default` COMPARES BY IDENTITY AND I CHOSE THAT DELIBERATELY,
   WHICH IS NOT THE SAME AS PROVING IT RIGHT.** It can name more functions than it
   should — a default that happens to be the same interned object, like the integer
   `15`, matches too. I argued that is the safe direction because it over-reports
   rather than misses. **I DID NOT TEST THE MISS CASE.** Build a case where a
   constant is frozen as a default AND read at call time by a different function,
   and see whether the verdict is still useful.
2. **THE POSITIVE CONTROL IS THE ONLY PROOF THE CHECK CAN FIRE, AND IT IS
   HARDCODED TO ONE NAME.** It asserts `'run' in _frozen_as_default('SYMBOLS')`.
   **If someone ever fixes `run`'s signature — the right change in itself — the
   positive control fails and the gate goes red for a good commit.** I chose that
   direction on purpose, as `GATE_CSV_SUFFIX` did. **It is R-020's doubt 2 arriving
   in my own code, and I am repeating a pattern this ship has already filed a doubt
   about.**
3. **I FIXED THE TEST AND LEFT THE PATTERN.** `def run(symbols=SYMBOLS, ...)` is
   still there. It is genuinely NOT a production defect — a real source edit works
   — and the repair rules forbade touching anything the pilot reads. **But it is
   the fifth time a session has repaired the one instance it attacked**, and
   `funding.py`'s `contracts=None` shows what the alternative looks like.
4. **CHECK (n) GUARDS `_SABOTAGES` ONLY.** Not `_FILE_SABOTAGES`, and **it does
   not exist at all in `cockpit/funding.py` or `cockpit/fear_greed.py`.** Those two
   were measured clean on 2026-07-30; nothing stops them acquiring a frozen-default
   swap tomorrow.
5. **`_b9_judge_says_no` IS JUDGED BY ONE JUDGE — ITSELF.**
6. **THE GATE IS SLOWER: ~4 MINUTES PLUS TWO MORE `--record` SUBPROCESS RUNS.** A
   gate nobody runs is a gate that is not guarding anything, and nothing on this
   ship watches that number.
7. **I RE-MARKED A `✗` RATHER THAN REMOVING IT.** B9's damage is printed in full,
   but the judge's own `✗` is rewritten to `x` so a passing gate contains no red
   ticks. **I believe that is right** — a PASS containing a red tick teaches the
   next reader to ignore red ticks — **and "I believe" is what this ship files
   rather than trusts.**

---

# PART 2 — FINISH R-022. **THREE DOUBTS UNTOUCHED.**

`python cockpit\funding.py` and `python cockpit\fear_greed.py`.

**What I tested and what HELD — do not repeat it:**

- All three constant-swaps (funding S6 `CONTRACTS`, funding S14 `OFFLINE_WORDS`,
  fear_greed F13 `OFFLINE_WORDS`) genuinely reach the module. Clean.
- Both import doors decomposed: `_import_writes_nothing` returns
  `right_file and rc_ok and quiet` on one `and`, and **`quiet` is the only
  component that flips** under S18 and F17, controls passing first. Both are
  caught for the reason they claim. Clean.

**WHAT IS STILL UNTOUCHED — this is your Part 2:**

1. **DOUBT 1, ITS AUTHOR'S OWN STRONGEST LEAD, NEVER TESTED BY ANYONE: a thread
   that writes AFTER `_capture` has restored the descriptors.** The ear restores
   the descriptors and THEN reads the capture file. **What writes in that gap?**
   Also unexamined: a C extension writing to the CRT handle, and a `subprocess`
   the doorway spawns that inherits the descriptors.
2. **DOUBT 4: `os.fstat(fd)[:4]` ON WINDOWS**, where `st_ino` is often 0. **It was
   never made to fail on purpose.**
3. **DOUBT 6: the silence check runs only the paths the gate thinks exist.**

## HOW TO ATTACK PROPERLY

- **BRING A NEW QUESTION. EIGHT ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* · *"What is the gate's own detector deaf
  to?"* · *"What shape does the real world have that the gate's world cannot?"* ·
  *"What if the module puts its work somewhere the gate is not looking?"* · *"What
  happens BEFORE the gate is alive to watch?"* · **and now mine:** *"Is the
  sabotage actually IN EFFECT when the judge runs, or is it scored CAUGHT by a
  guard that fires before the mechanism it claims to prove?"* **All eight are the
  directions these gates are now strongest in, and reusing any of them is the
  approach most likely to find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** Eight
  sessions running have now predicted their attacks correctly beforehand, and that
  is what proves a hole is structural rather than luck. **I wrote five predictions
  and all five were correct.**
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo — it costs nothing.
  Check `git status` is clean when you are done.
- **EDIT IN BINARY MODE.** These files are CRLF. **Always print the diff and
  confirm it is the number of lines you meant, and that the CRLF count did not
  move** — my patch script printed both and refused to write otherwise.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE, REFUSE TO RUN.** This is not
  theoretical. **My very first probe refused to run** — I had built a `\n` anchor
  for a CRLF file and it matched zero times. The guard is the only reason I did not
  conclude something false from it.
- **AND A NEW ONE, EARNED THE HARD WAY THIS MORNING: NEVER PUT BACKTICKS INSIDE A
  DOUBLE-QUOTED SHELL STRING.** I wrote a ROADMAP update that way and bash ate
  every backticked fragment as a command substitution, writing mangled text into a
  ship document. I caught it, reverted with `git checkout --`, and redid it from a
  file. **Put document text in a FILE and have Python read it.**
- **Run the untouched control FIRST — and run it inside the scratch copy too.**
- **A GREEN GATE IS NOT THE EVIDENCE. PRINT THE DAMAGE.** **A sabotage that
  CRASHES is scored "caught", so one that never really ran looks like a success.**

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item. **It has now happened once on this ship — R-022 held
on two axes — so it is no longer hypothetical.**

**DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.**

**You may clear R-024 and R-022** — you built neither. **You may clear R-007**,
untouched for seven sessions; I did not look at it, so I could not. **You may
NEVER clear R-006.** **And if you fix something, you may not clear your own fix.**

---

# THE 1 AUGUST ERRAND — **CHECK TODAY'S DATE FIRST.**

**Four sets of orders have now got this wrong in one direction or the other. On
2026-07-30 it was NOT due.**

**When 1 August has actually passed:** open `journal/daily_runs.log` and tell the
Commander PLAINLY whether the monthly recorder task actually committed and pushed
real new rows.

**MEASURED, so you do not have to re-derive it:**

    schtasks: \ZarX Open Interest — Status Ready, Next Run 01-Aug-2026 09:00
    The recorder has run EXACTLY ONCE in its whole history: by hand, on
    2026-07-27, and it appended ZERO rows. The commit-and-push branch has
    therefore STILL never fired for real.
    MEASURED 2026-07-29 evening against a copy of the real archive: a healthy
    run appends 12 rows per asset and reports 192 stored.
    MEASURED 2026-07-30: data/oi_history/ holds exactly THREE files, correctly
    named, 181 lines each, unchanged all session.

**WRITE DOWN WHAT YOU EXPECT BEFORE YOU READ THE LOG. The honest figure on
1 August is roughly THIRTY new rows per asset and a stored count near 210** — not
180, and not 360. **If the log says something you did not predict, that is a
finding, not a relief.**

**AND THE SECOND THING, EARNED BY B14: look at `data/oi_history/` itself and
confirm there are THREE files, correctly named.** A fourth file, or a different
name, is B14 arriving for real.

**Do not assume it worked because the task returned 0** — `schtasks` already
reported SUCCESS once for a task that could never run at all. **Read the file and
count the rows yourself.**

---

# IF BOTH ATTACKS COME BACK CLEAN — THEN, AND ONLY THEN, BUILD

The next thing on the ship is **Context Deck instrument 3 of 5: news headlines,
CryptoPanic free tier — HEADLINES ONLY, no sentiment score, no invented weights.
The cut ghost stays cut.** It is `EXECUTION_PLAN.md` Phase 3 step 3. Gate declared
and committed alone first, sabotage drill from birth, fail-safe to one honest
offline line.

**IF YOU ARE RUNNING SHORT, DO PART 1 PROPERLY AND LEAVE THE BUILD ENTIRELY.**
A half-built part is worse than no part.

---

# IF ANYTHING LEAKS: GRADE IT FIRST, THEN REPAIR UNDER A GATE DECLARED FIRST

**FILL IN THE FINDING REPORT BEFORE YOU REPAIR ANYTHING.** Four steps, plain
sentences, in `THE_PATTERN.md`. **Step 2.2 carries the Commander's own wording —
read it there, not here.** Then:

    SERIOUS ....... fix it, and stop. Build nothing.
    BORDERLINE .... do NOT fix it. Report and stop. The Commander rules.
    SMALL ......... do NOT fix it. File it in REVIEW_QUEUE.md as CATEGORY B
                    and carry on.

**If you do repair: DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY
ALONE, WITH NO `.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then
`git show --stat` proves the bar preceded the work. **Sixteen uses of this pattern
and it has survived audit every time.** Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, do not assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a sha256
    of the production half before and after, printed side by side.
    **Current values: `open_interest.py` lines 1-242 =
    `5347bfecdf2ccfb2009770f9161dd6c51374f2ccdeae9a8c50793f3a57e2096f`;
    funding `95069d1b…`, fear_greed `bb31626c…`.**
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself, the gate
    never reads a constant belonging to the file it is judging, and THE GATE NEVER
    ASKS THE MODULE WHERE TO LOOK.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others, caught
    every run, originals restored and the restoration verified. **And check that
    your new break is actually IN EFFECT when its judge runs** — that is the
    lesson of 2026-07-30 and it is now a check the gate performs, section (n).
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT, **and must be shown to fail for
    the reason it claims, not incidentally.** **And prove your new sabotage's judge
    returns False rather than raising.**
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed".**

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the actual
output, and the verdict — **including if it is all clean.**

**`REVIEW_QUEUE.md`: you MAY clear R-024 and R-022 (you built neither), and R-007
too if it settles.** R-001 has now waited through **ten generations of repair, nine
of which were failed by the next pair of eyes and the tenth — mine — untested.** It
**moves only when a generation survives an independent attack. Untested is not
survived.** Items you cannot settle stay OPEN with a note on what is missing;
**leaving something open is a legitimate recorded outcome. R-006 is not yours,
ever. Never delete an item. Never edit a cleared verdict.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly", "I believe" or "this should be fine" about anything that ships — FILE
IT in `REVIEW_QUEUE.md` before the commit that ships it.**

---

# BEFORE YOU FINISH

**Do the closing ritual exactly as `THE_PATTERN.md` sets it out** — seven steps,
ending with the next session's orders, the push, and your plain-words report to the
Commander. **It is not repeated here.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **HIS SHIP'S RECORDER WAS RUNNING A TEST THAT TESTED NOTHING, AND SAID IT
   PASSED — for four generations.** It is repaired. **He should know the
   protection was never actually missing**, and that what failed was the ship's
   own tally, which is the exact thing that voided the 48/48. **One decision is
   his: R-024 doubt 2 — the new check's positive control is hardcoded, so if a
   future session correctly fixes `run(symbols=SYMBOLS, ...)`, the gate will go
   red for a good change.** I chose the loud direction deliberately. **He can
   overrule that in one word.**
2. **R-023, NEW, CATEGORY B: on the real defect the recorder's gate exits 1 but
   ends in a Python stack trace instead of saying FAILED.** The alarm is right;
   the label is unreadable to a non-programmer. **One branch would fix it. Filed,
   not fixed, because the rules say a SMALL finding is filed.** He can order it
   done in one word.
3. **THE FUNDING GATE GOES RED NEAR A FUNDING SETTLEMENT (R-021).** ~45 minutes
   around 00:00, 08:00 and 16:00 UTC, proved by running the untouched previous
   version side by side. **Deliberately NOT repaired: the rules say a SMALL
   finding is filed.** He can overrule in one word.
4. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL NEW
   ROWS.** The errand above. **Due 1 August.**
5. **`cockpit/brief.py` HAS NO GATE — and he has ruled: NOT NOW, BEFORE GOING
   LIVE.** A standing requirement in `EXECUTION_PLAN.md`. **Do not build it, do
   not re-argue it.**
6. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
7. **The risk-doctrine decision** — the 25% position cap means real risk is ~0.49%
   per trade, not the intended 1%. **Settled BEFORE Phase 6, never after seeing
   results.**
8. **`MAX_PLAUSIBLE_RATE`** — measured at 13-16x looser than Binance's published
   cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
9. **The settled-rate anchor (R-004)** — returned to him on correct facts.
10. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
11. **A DOCUMENT-INTEGRITY CHECK.** Nothing on this ship checks that its own
    documents are not corrupted. **Found by a human looking, twice — and nearly a
    third time this morning, by me, when bash silently ate every backticked
    fragment of a ROADMAP update.** I caught that one myself and reverted it.
    **A one-line scan would close it. Recommended, not adopted.**
12. **THE CATEGORY B PILE IS FIVE DEEP** and is cleared before the ship is used
    for real, at the same moment `brief.py` gets its gate.
13. **THIRTEEN law candidates, none adopted, all his call:**
    - *"A session may not certify its own work; anything it cannot certify is
      filed in `REVIEW_QUEUE.md` before the commit that ships it, and only an
      independent reviewer may clear it."*
    - *"A claim about what a data source will or will not give us is not a fact
      until it has been called; planning documents must mark which claims are
      measured and which are assumed."*
    - *"A check is not proven until it has been deliberately broken."*
      **Eighteen working implementations and still not law.**
    - *"A gate must verify what the pilot READS — the whole line, words included —
      not what the parser returned."*
    - *"A sabotage that is scored CAUGHT must be shown to fail for the reason it
      claims."* **This one just caught B9. It is the strongest unadopted
      candidate on the list.**
    - *"A gate must hold EVERY path the pilot can see to the same standard."*
    - *"A gate may not derive anything it measures by — a word, a list, a limit —
      from the file it is judging."*
    - *"A gate must be shown to be watching the OBJECT the pilot actually
      receives, and the STATE the part is actually in when it runs for real."*
    - *"Every output a human will act on must be checked against the thing it
      describes — including the output of the test itself."*
    - *"A gate must be shown to BUILD the situations it claims to judge."*
    - *"A gate must hold its own ADDRESS as well as its own expectations."*
    - *"A check that reports the ABSENCE of something must first be proved able to
      detect its PRESENCE. A listener that cannot hear reports silence, and
      silence is what a passing gate looks like."*
    - **NEWEST, earned 2026-07-30:** *"A drill must prove that the sabotage it
      installed was IN EFFECT when its judge ran. A break that never reached the
      code is indistinguishable, in the output, from a break that was caught."*
      **Earned by B9: four generations of a gate scored it CAUGHT while it
      rebound a name the module never reads.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.** **Ten generations, nine of them failed by the next pair of eyes, and the
tenth is sitting in front of you untested — that is what the substitute is worth,
and it only works if somebody actually attacks.**
