# ZAR X PHASE 3 — **ATTACK GATE 3.2b-R8 (R-026). THEN BUILD DOOR 3: THE COMMANDER HAS RULED R-025 SERIOUS.**

*Written 2026-07-30 (afternoon) by the eleventh generation — the session that
attacked R-024 and R-022, found a blind spot in each, repaired ONE of them, and
**failed its own gate once on the way.** I may not clear my own repair. That is
your Part 1.*

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is the exact bars and commands. This part is the story, so
you know WHY before you read WHAT. The Commander is not a programmer and asked for
it in this form. Write your report to him the same way.*

## Where the ship is

    data/open_interest.py   GATE 3.2b-R8 PASSED  exit 0  0 red, 14/14 CAUGHT
    cockpit/fear_greed.py   GATE 3.1-R6  PASSED  exit 0  0 red
    cockpit/funding.py      GATE 3.2-R6  PASSED  exit 0  0 red  — BUT SEE R-025
    vault INTACT 6/6 · Brief 3/3 · lab/ untouched
    data/oi_history/        3 files, correctly named, 181 lines each, sha256
                            e3258e82… / 1549a8a1… / e0f91a87… unchanged all session

## What I found, in two paragraphs

**FINDING 1 — the check built yesterday morning to stop B9's class coming back
could only see one of the ways it comes back.** `_frozen_as_default` read
`__defaults__` and nothing else, so a KEYWORD-ONLY default, a `functools.partial`
and a class body were all invisible to it. I proved it with a real two-line edit:
the gate scored B1 and B2 **ESCAPED** on one line and then certified, thirty
lines later, that **"the swap reaches the module."** Graded SERIOUS on 2.1 (a
`*,` in a signature is ordinary Python), repaired under GATE 3.2b-R8. **Nothing
in the shipped file was frozen that way — I had to write it — and when I did the
drill went red loudly. What was broken was the CLAIM, not the protection.**

**FINDING 2 — R-022 doubt 1 was right, and it is NOT repaired.** The ear shuts the
instant the doorway returns. A thread, a kept-alive buffer over descriptor 1 and
an atexit handler put **162 lines of trading advice on the pilot's screen** while
GATE 3.2-R6 printed *"the doorway wrote NOTHING"* three times, passed its own ear
control 3/3, and exited 0. **I graded it SERIOUS and left it on the Commander's
desk as R-025.**

## **THE MOST USEFUL THING I CAN TELL YOU: MY FIRST DRAFT FAILED ITS OWN GATE**

I counted a module-level alias as a freeze. The healthy file went **red fourteen
times** — because `_RECORD_ORIGINAL = record` is the drill's own saved original,
working as designed. **The distinction I had wrong: what matters is not that
another name holds the old object, it is that the module USES the old object
without looking the name up again.** I removed the rule and turned it into a
permanent negative control. **Read R-026 doubt 9 before you trust that control:
it encodes MY judgement, and if my judgement is wrong the control will actively
stop you finding the thing it hides.**

## **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

**`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT AND IS GREEN THE
REST OF THE TIME. R-021, CATEGORY B, SMALL.** Binance settles at **00:00, 08:00
and 16:00 UTC**. I ran it at **+55 minutes** and it passed first time.

**>>> OUTSIDE A SETTLEMENT WINDOW, A RED FUNDING GATE IS A REAL FAILURE. TREAT IT
AS ONE.** Check the clock, run it again, and say how many runs it took.

## **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET — NOT NOW, BEFORE GOING LIVE.** Do not
   build it, do not re-argue it.
2. **R-016 IS OFF HIS DESK.** Still not CLEARED — that is R-022, a session's job.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 of THE FINDING REPORT carries his own
   wording in `THE_PATTERN.md`. **Read it there before you grade anything.**

## Your job, in order

**1. ATTACK R-026 — MY REPAIR, GATE 3.2b-R8.** Nine doubts filed against my own
work. They are starting points, **not** the assignment.

**2. THEN YOUR PART 2 DEPENDS ON HIS RULING ON R-025** — the rule is written out
below so you do not have to guess.

**3. THE 1 AUGUST ERRAND — CHECK TODAY'S DATE FIRST.** On 2026-07-30 it was NOT
due. **Five sets of orders have now got this wrong in one direction or the other.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment and the housekeeping that has bitten this ship. None of it is
repeated here. I did NOT edit it** — I earned no lesson it does not already state.

**Specific to THIS job:**

1. **The LAST TWO entries of `PROGRESS_LOG.md`** — my declaration and my results.
   **Read them as a CLAIM, not a result.** The file is ~420 KB; reading all of it
   will eat your budget.
2. **`data/open_interest.py`, the `__main__` half only** — `_frozen_as_default`
   and its nested `_holds`, `_detector_sees_every_shape` (five positive controls,
   TWO negative), and the wiring at the top of `_installer_can_install`.
3. **`REVIEW_QUEUE.md` — R-026 and R-025 are your worklist**, plus R-022 doubt 6
   and R-007 if you have room. **R-006 may NEVER be cleared by you or any
   in-house session.**
4. **`ROADMAP.md`** — the MEASURED facts table. If anything you measure disagrees
   with it, **your measurement wins and you write the correction down.** I had to
   do that twice today.

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A new sabotage, invented by you, thrown at **Gate 3.2b-R8 (R-026)**, result
   recorded either way.
2. **R-022 doubt 6** tested, or **R-007** examined — one of the two that nobody
   has touched. Recorded either way.
3. Any leak graded on THE FINDING REPORT **before** any repair, using **the
   Commander's wording of Step 2.2**, and repaired only if that grade says to.
4. `lab/` byte-identical, vault INTACT 6/6, Brief 3/3, and **exactly THREE files
   in `data/oi_history/` named `BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`,
   `SOLUSDT_4h.csv`** — 181 lines each, sha256 `e3258e82…`, `1549a8a1…`,
   `e0f91a87…` on 2026-07-30. **A fourth file, or a different name, is B14
   arriving for real.**

**Four of four or it has not cleared, and "three of four with a good explanation"
is the phrasing this ship exists to refuse.**

---

# PART 1 — MY REPAIR (R-026). **NEVER ATTACKED.**

`python data\open_interest.py` — **timed twice today at 55 SECONDS**, not the
"~4 minutes" the previous log records. Fourteen sabotages, section (n) with five
positive and two negative controls, zero red ticks. **That is the claim under
review, not the verdict.**

**Where this repair is strongest — do NOT spend your time here:** the detector now
reads `__defaults__`, `__kwdefaults__`, `functools.partial` bindings and class
bodies; every one of those four is proved by a planted example the check must FIND
before it is allowed to speak; two negative controls prove it does not simply
report everything; the production half's sha256 is byte-identical before and after
(`5347bfec…`, computed as the first 242 lines joined by CRLF with no trailing
separator — **that is the recipe the log's figure uses, I had to find it by
experiment, and it is written down here so you do not have to**); and my own real
keyword-only edit is now caught by name.

## THE NINE DOUBTS I FILED AGAINST MY OWN WORK — free hits

Read them in `REVIEW_QUEUE.md` under **R-026**. The three I would attack first:

- **DOUBT 9 — the alias negative control encodes MY judgement about which freezes
  matter.** If I am wrong, that control will keep you from finding the thing it
  hides. **This is the most dangerous line in my diff.**
- **DOUBT 1 — the controls put seven names into the module's `globals()` and take
  them out in a `finally`. Nothing checks the namespace afterwards.** Every check
  that runs later runs in whatever namespace mine left behind.
- **DOUBT 3 — I found four places. I do not know there are only four.** Closures
  (`__closure__`), decorator wrappers, bound methods stored in globals, `__slots__`
  descriptors, dataclass fields. **The whole finding was a check speaking for
  places it had never read, and I may be doing a narrower version of the same
  thing.**

---

# PART 2 — **BUILD DOOR 3. THE COMMANDER RULED R-025 SERIOUS ON 2026-07-30 (afternoon). THE BRANCH IS CLOSED.**

**HIS RULING, RECORDED PLAINLY INCLUDING HOW IT WAS REACHED:** he was given both
findings, the full FINDING REPORT for each, the trade-off in plain words, and a
THIRD cheaper option nobody had asked for. **He ruled SERIOUS, and he did so on the
session's recommendation rather than against it** — that is written down because a
ruling reached by agreeing with the machine is a weaker thing than one reached
against it, and the next session is entitled to know which it was. **It is still
his ruling and it stands.**

**SO: BUILD DOOR 3 in `cockpit/funding.py` AND `cockpit/fear_greed.py`.** Gate
declared and committed alone first with no `.py` in that commit, sabotage drill
from birth, fail-safe to one honest line. **The design is written out in
`REVIEW_QUEUE.md` under R-025 — you do not have to invent it.**

**WHAT DOOR 3 IS, IN ONE SENTENCE:** door 2 already spawns a fresh interpreter and
requires it to write nothing AT IMPORT; door 3 is the same proven machinery one
step further — **a fresh interpreter that imports the module, calls
`section_text()` on all three paths, and then SHUTS DOWN, with the child's TOTAL
output required to be empty.** Interpreter shutdown joins non-daemon threads,
flushes every buffer and runs every atexit handler, **so it catches all three
deferred shapes deterministically instead of racing them.**

**THE TWO TRAPS, NAMED BEFORE YOU START:**

1. **A TIMEOUT MUST BE A FAILURE, NEVER A QUIET PASS.** A thread that sleeps
   forever makes the child hang, and "no output before the timeout" is precisely
   what silence looks like. **This is the single most likely way to build a door 3
   that guards nothing.**
2. **THE DRILL MUST PLANT ALL THREE SHAPES AND REQUIRE ALL THREE CAUGHT** — the
   thread, the kept-alive buffer over descriptor 1, and the atexit handler.
   Otherwise door 3 is one more check nobody has ever broken. **The exact three
   are reproduced in R-025 and the patch that installs them is described there.**

**AND A THIRD THING THAT IS PERMITTED BUT IS NOT A SUBSTITUTE.** The Commander was
also offered a cheap 90% version: a check that simply reads the instrument's own
source and confirms it contains **no machinery capable of deferring a write at
all** — no `threading`, no `atexit`, no `subprocess`, no `os.dup`, no `open(1`, no
`Timer`, no `QueueHandler`, no `__del__`. **He did not choose it; he chose the real
thing.** You MAY add it as a second, cheaper guard **only after DOOR 3 itself
passes**, and if you do it needs its own positive control — it must be shown to
FLAG a planted `threading.Thread` line before its silence on the real file means
anything. **It may never be built instead of DOOR 3, and a session that ships only
the cheap version has not carried out this order.**

**MEASURED FACTS YOU WILL NEED, so you do not re-derive them:** the gate calls
`section_text()` **54 times per run** (counted, from 54 copies of each planted
marker); the funding gate takes ~85 seconds; both production halves today contain
**no** deferred-write machinery of any kind, so **the healthy control must come
back silent and if it does not, something arrived since 2026-07-30 and THAT is your
session.**

**AND WHAT THIS PUSHES BACK, SAID SO NOBODY THINKS IT WAS FORGOTTEN:** Context Deck
instrument 3 of 5 — **news headlines, CryptoPanic free tier, HEADLINES ONLY, no
sentiment score, no invented weights, the cut ghost stays cut** — is
`EXECUTION_PLAN.md` Phase 3 step 3 and is **next after DOOR 3**. It has now been
deferred SIX times. **That is the price of this ruling and the Commander was told
the price before he made it.**

**IF YOU ARE RUNNING SHORT, DO PART 1 PROPERLY AND LEAVE PART 2 ENTIRELY.** A
half-built part is worse than no part. **I left Part 2 entirely today and said so.**

## HOW TO ATTACK PROPERLY

- **BRING A NEW QUESTION. NINE ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* · *"What is the gate's own detector deaf
  to?"* · *"What shape does the real world have that the gate's world cannot?"* ·
  *"What if the module puts its work somewhere the gate is not looking?"* · *"What
  happens BEFORE the gate is alive to watch?"* · *"Is the sabotage actually IN
  EFFECT when the judge runs?"* · **and now mine:** *"WHEN does the gate stop
  watching, and what does the part do after that?"* **All nine are the directions
  these gates are now strongest in, and reusing any of them is the approach most
  likely to find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** Nine
  sessions running have now done this. **I wrote seven predictions: five were
  right and TWO WERE WRONG, and both wrong ones are recorded in the log.** Getting
  one wrong is not a failure — hiding it is.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; it costs nothing.
  Check `git status` is clean when you are done.
- **EDIT IN BINARY MODE.** These files are CRLF. **Print the diff, confirm it is
  the number of lines you meant, and confirm the CRLF count did not move.** My
  patch scripts refused to write otherwise, and one of those guards caught me
  miscounting an insertion by one line.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE, REFUSE TO RUN.**
- **NEVER PUT BACKTICKS INSIDE A DOUBLE-QUOTED SHELL STRING** — bash eats them as
  command substitution and writes mangled text into ship documents. **Put document
  text in a FILE and have Python read it.** I appended every document with a
  Python helper that prints the byte and line-ending totals before and after.
- **AND ONE THIS ENVIRONMENT WILL BITE YOU WITH: PYTHON HERE IS 3.10, WHERE A
  BACKSLASH ESCAPE INSIDE AN F-STRING *EXPRESSION* IS A SyntaxError.**
  `f"{'✓' if ok else '✗'}"` will not compile. Name the glyphs first.
  **My first repair run died on exactly that**, which is why the repair script now
  runs `py_compile` before the gate.
- **Run the untouched control FIRST — and run it inside the scratch copy too.**
- **A GREEN GATE IS NOT THE EVIDENCE. PRINT THE DAMAGE.** **A sabotage that
  CRASHES is scored "caught", so one that never really ran looks like a success.**

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item. **DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.**

**You may clear R-026 and R-025** — you built neither. **You may clear R-007**,
untouched for eight sessions now. **You may NEVER clear R-006.** **And if you fix
something, you may not clear your own fix.**

**R-001 has now waited through ELEVEN generations of repair, ten of which were
failed by the next pair of eyes and the eleventh — mine — untested.** It **moves
only when a generation survives an independent attack. Untested is not survived.**

---

# THE 1 AUGUST ERRAND — **CHECK TODAY'S DATE FIRST.**

**On 2026-07-30 it was NOT due. Five sets of orders have now got this wrong in one
direction or the other.**

**When 1 August has actually passed:** open `journal/daily_runs.log` and tell the
Commander PLAINLY whether the monthly recorder task actually committed and pushed
real new rows.

**MEASURED, so you do not have to re-derive it:**

    schtasks: \ZarX Open Interest — Status Ready, Next Run 01-Aug-2026 09:00
    The recorder has run EXACTLY ONCE in its whole history: by hand, on
    2026-07-27, and it appended ZERO rows. The commit-and-push branch has
    therefore STILL never fired for real.
    A healthy run appends 12 rows per asset and reports 192 stored (measured
    2026-07-29 against a copy of the real archive).
    MEASURED 2026-07-30: data/oi_history/ holds exactly THREE files, correctly
    named, 181 lines each, unchanged all day.

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
`git show --stat` proves the bar preceded the work. **Seventeen uses of this
pattern and it has survived audit every time.**

**AND RECORD THAT HASH *AFTER* YOUR FINAL PUSH, NOT WHEN YOU WRITE THE ENTRY.**
The cloud watchman pushes every four hours, so `git pull --rebase` before your
push can rewrite your own commit hashes underneath you. **Mine did**, and three
documents named a commit that no longer existed until I corrected them. Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, do not assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a sha256
    of the production half before and after, printed side by side.
    **Current values, and the RECIPE, because the value alone is not
    reproducible:** hash the first N-1 lines joined by CRLF with **no trailing
    separator**. `open_interest.py` lines 1-242 =
    `5347bfecdf2ccfb2009770f9161dd6c51374f2ccdeae9a8c50793f3a57e2096f`;
    funding `95069d1b…`, fear_greed `bb31626c…`.
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself, the gate
    never reads a constant belonging to the file it is judging, and THE GATE NEVER
    ASKS THE MODULE WHERE TO LOOK.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others, caught
    every run, originals restored and the restoration verified. **And check your
    new break is actually IN EFFECT when its judge runs.**
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT, **and must be shown to fail for
    the reason it claims, not incidentally.**
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**
(g) **AND ONE I ADD FROM TODAY: RUN `py_compile` BEFORE THE GATE.** A syntax error
    costs you a whole run otherwise, and it cost me one.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed".**

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the actual
output, and the verdict — **including if it is all clean, and including every
prediction you got wrong.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly", "I believe" or "this should be fine" about anything that ships — FILE
IT in `REVIEW_QUEUE.md` before the commit that ships it.**

---

# BEFORE YOU FINISH

**Do the closing ritual exactly as `THE_PATTERN.md` sets it out** — seven steps,
ending with the next session's orders, the push, and your plain-words report to
the Commander. **It is not repeated here.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **R-025 IS ANSWERED. HE RULED IT SERIOUS ON 2026-07-30 (afternoon) AND DOOR 3
   IS NOW AN ORDER, NOT A PROPOSAL — DO NOT RE-OPEN IT WITH HIM.** He was shown
   the proof (162 lines of advice on the pilot's screen under a gate that printed
   PASSED), both FINDING REPORTS, the plain-words trade-off, and a third cheaper
   option. He was told before ruling that the price is Context Deck instrument 3
   slipping a sixth time, and he accepted that price. **He ruled with the
   session's recommendation rather than against it, which is recorded in Part 2
   because the next session is entitled to know which kind of ruling it was.**
   **What he is still owed on it: the result.** When DOOR 3 passes, tell him in
   plain words that the hole is shut and how you proved it — not that a gate went
   green.
2. **HIS RECORDER'S NEWEST GUARD COULD ONLY SEE ONE OF THE FOUR WAYS THE THING IT
   GUARDS AGAINST HAPPENS.** Repaired. **He should know the protection was never
   missing — what was wrong was the claim.** And that **my own first draft of the
   repair failed its own gate**, which is the drill doing its job on its author.
3. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** If a future
   session correctly fixes `run(symbols=SYMBOLS, ...)`, the gate goes red for a
   good change. I deliberately did NOT touch it. **He can overrule in one word.**
4. **AND THE ONE I WOULD MOST LIKE HIM TO SAY YES TO: FIX THE PATTERN, NOT JUST
   THE TEST.** `def run(symbols=SYMBOLS, ...)` and `fetch_history` still freeze
   their globals. **The one-line change that ends this entire class is
   `symbols=None`, resolved from the global in the body — and `funding.py` already
   does it that way.** It touches what the pilot reads, so no session may make it
   during a repair to a test. **Six generations have now fixed the instance and
   left the pattern. Only he can end that.**
5. **R-023, CATEGORY B: on the real B9 defect the recorder's gate exits 1 but ends
   in a Python stack trace instead of saying FAILED.** One branch would fix it.
   Filed, not fixed, because the rules say a SMALL finding is filed.
6. **THE FUNDING GATE GOES RED NEAR A SETTLEMENT (R-021).** SMALL, unrepaired.
   +55 minutes was clean today, first run.
7. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL NEW
   ROWS.** The errand above. **Due 1 August.**
8. **`cockpit/brief.py` HAS NO GATE — he has ruled: NOT NOW, BEFORE GOING LIVE.**
9. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
10. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never after
    seeing results.**
11. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published cap.
    **Recommendation: tighten to ~0.01. STILL NOT DONE.**
12. **The settled-rate anchor (R-004)** — returned to him on correct facts.
13. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
14. **A DOCUMENT-INTEGRITY CHECK.** Recommended three times, not adopted. **I ran
    one by hand before every commit today** — a Python scan for the five cp1252
    fingerprints — **and it found five pre-existing hits, all of them deliberate
    quotations inside backticks, and zero in anything I wrote.** The previous
    entry recorded "THREE"; the fuller scan finds five across three markers. **A
    one-line scan would close this. Recommended, not adopted.**
15. **THE CATEGORY B PILE IS FIVE DEEP** and is cleared before the ship is used
    for real, at the same moment `brief.py` gets its gate.
16. **THIRTEEN LAW CANDIDATES, NONE ADOPTED, ALL HIS CALL — and I am proposing NO
    new one.** Seven laws get read; twelve get skimmed. **What today earned is an
    AMENDMENT to one already on the list**, and I put it as an amendment on
    purpose rather than growing the pile:
    - *"A check that reports the ABSENCE of something must first be proved able to
      detect its PRESENCE"* → **add: "in EVERY FORM it claims to cover, and it
      must also be proved to stay SILENT about the forms it does not."** A
      detector that sees one shape and speaks for all of them is what check (n)
      was, and a detector that reports everything is what my own first draft was.
      **Both halves were earned by something that actually happened, one day apart.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time" substitute
for Fable EXPIRES.** A second, genuinely independent AI reviews the gauntlet's
test setup before it runs and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.** **Eleven generations, ten of them failed by the next pair of eyes, and
the eleventh is sitting in front of you untested — that is what the substitute is
worth, and it only works if somebody actually attacks.**
