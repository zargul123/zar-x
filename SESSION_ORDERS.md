# ZAR X PHASE 3 — **ATTACK GATE 3.2b-R9 (R-027). THEN BUILD DOOR 3 — IT IS STILL HIS ORDER AND IT HAS NOW SLIPPED TWICE.**

*Written 2026-07-30 (evening) by the twelfth generation — the session that
attacked R-026, found TWO blind spots, repaired both, and **did not build Door 3
because its own grade forbade it.** I may not clear my own repair. That is your
Part 1. **And the reason Door 3 is still unbuilt is a decision waiting on the
Commander — read "ON THE COMMANDER'S DESK", item 1, before you plan your day.***

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is exact bars and commands. This part is the story, so you
know WHY before you read WHAT. The Commander is not a programmer and asked for it
in this form. Write your report to him the same way.*

## Where the ship is

    data/open_interest.py   GATE 3.2b-R9 PASSED  exit 0  0 red, 14/14 CAUGHT  74 s
    cockpit/fear_greed.py   GATE 3.1-R6  PASSED  exit 0  0 red                40 s
    cockpit/funding.py      GATE 3.2-R6  PASSED  exit 0  0 red  128 s — SEE R-025
    vault INTACT 6/6 · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/        3 files, correctly named, 181 lines each, sha256
                            e3258e82… / 1549a8a1… / e0f91a87… unchanged all session

## What I found, in two paragraphs

**FINDING 1 — THE GATE CERTIFIED A SABOTAGE THAT COULD NOT TOUCH THE RECORDER.**
Check (n) printed, of every globals-swap sabotage, *"looked up at CALL TIME, so
the swap reaches the module."* **What it actually measured was only that the name
was not frozen as a default argument.** Those are different claims. I added one
sabotage rebinding `_rows` — the gate's OWN CSV reader, defined inside `__main__`,
which the recorder cannot even name. The gate printed `✓ BX … → CAUGHT`, printed
`✓ BX rebinds '_rows' → the swap reaches the module`, printed zero red ticks and
exited 0 — **while the recorder wrote 180 perfect rows spanning a full 30-day
window, completely untouched.** That is B9's shape with the freeze taken out, and
B9 walked through four generations.

**FINDING 2 — THE DETECTOR NAMED "A CLASS BODY" AND HAD ONLY EVER TESTED ONE
CORNER OF IT.** Its control planted a plain method. I planted nine shapes and it
reported four: `@staticmethod`, `@classmethod` and `property` were all invisible,
because in Python 3.10 none of the three exposes `__defaults__` through
`vars(cls)`. **Both findings graded SERIOUS. Both are LATENT** — every real
sabotage targets a production name, and this module has one class with no methods
— **so nothing shipped was weaker than it looked. What was wrong was the CLAIM.**
That is word for word what the eleventh generation found one day earlier, in the
same check.

## **THE MOST USEFUL THING I CAN TELL YOU: MY BEST CONTROL CAME OUT OF MY OWN SLOPPY GREP**

My first search for `_rows` in the production half said six. **All six were
`new_rows`.** I only noticed because the count for `new_rows` was also six. So
the positive control now states the naive count out loud — *"reported ABSENT even
though a naive substring search finds it 6 times inside 'new_rows'"* — and nobody
can quietly regress it to a substring search. **Read R-027 doubt 1 before you
trust that rule at all: it is a TEXT search, so a name that appears only in a
COMMENT still counts as code. That is the same disease and I did not test it.**

## **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

**`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT AND IS GREEN THE
REST OF THE TIME. R-021, CATEGORY B, SMALL.** Binance settles at **00:00, 08:00
and 16:00 UTC**. I ran it at 13:20 UTC and it passed first time.

**>>> OUTSIDE A SETTLEMENT WINDOW, A RED FUNDING GATE IS A REAL FAILURE. TREAT IT
AS ONE.** Check the clock, run it again, and say how many runs it took.

## **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET — NOT NOW, BEFORE GOING LIVE.**
2. **R-016 IS OFF HIS DESK.** Still not CLEARED — that is R-022, a session's job.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 of THE FINDING REPORT carries his own
   wording in `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **R-025 IS RULED SERIOUS AND DOOR 3 IS AN ORDER, NOT A PROPOSAL.** Do not
   re-open the ruling. **Whether it is built BEFORE or AFTER another repair is
   the open question, and that one IS his — item 1 on his desk.**

## Your job, in order

**1. ATTACK R-027 — MY REPAIR, GATE 3.2b-R9.** Ten doubts filed against my own
work. They are starting points, **not** the assignment.

**2. THEN BUILD DOOR 3** unless he has said otherwise — see his desk, item 1.

**3. THE 1 AUGUST ERRAND — CHECK TODAY'S DATE FIRST.** On 2026-07-30 it was NOT
due. **Six sets of orders have now got this wrong in one direction or the other.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment and the housekeeping that has bitten this ship. None of it is
repeated here. I did NOT edit it** — I earned no lesson it does not already state.

**Specific to THIS job:**

1. **The LAST TWO entries of `PROGRESS_LOG.md`** — my declaration and my results.
   **Read them as a CLAIM, not a result.** The file is ~457 KB; reading all of it
   will eat your budget.
2. **`data/open_interest.py`, the `__main__` half only** — `_frozen_as_default`
   with its nested `_unwrap` and `_holds`; `_production_half` and
   `_named_in_production`; `_reachability_rule_can_fire` with its two positive
   and four negative controls; `_detector_sees_every_shape` with its now EIGHT
   positive and TWO negative controls; and the loop at the top of
   `_installer_can_install`.
3. **`REVIEW_QUEUE.md` — R-027 and R-025 are your worklist**, plus R-022 doubt 6
   if you have room. **R-006 may NEVER be cleared by you or any in-house session.**
4. **`ROADMAP.md`** — the MEASURED facts table. If anything you measure disagrees
   with it, **your measurement wins and you write the correction down.** I had to
   do that for three runtime figures tonight.

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A new sabotage, invented by you, thrown at **Gate 3.2b-R9 (R-027)**, result
   recorded either way.
2. **R-022 doubt 6** tested — nobody has touched it in nine sessions and it is
   now the oldest untouched doubt on the ship. Recorded either way.
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

# PART 1 — MY REPAIR (R-027). **NEVER ATTACKED.**

`python data\open_interest.py` — **timed five times tonight at 73-80 seconds**,
not the "55 seconds" the last orders record and not the "~4 minutes" the log
records. Fourteen sabotages, eighteen control lines, zero red ticks. **That is
the claim under review, not the verdict.**

**Where this repair is strongest — do NOT spend your time here:** the
reachability rule has two positive controls (the gate's own reader, and a name
that exists nowhere) and four negative ones (`_utc_iso`, `record`, `csv_path`,
`SYMBOLS` must all be found), so it is proved able to fire AND proved not to flag
everything; the whole-word trap is stated out loud with its own count; the
detector now proves eight shapes instead of five; both old negative controls
still stay silent; the production half's sha256 is byte-identical before and
after (`5347bfec…`, computed as the first 242 lines joined by CRLF with **no
trailing separator** — that is the recipe, written down so you do not have to
find it by experiment); and my own BX attack, re-applied to the repaired file,
now goes red BY NAME AND REASON and the gate exits 1.

## THE TEN DOUBTS I FILED AGAINST MY OWN WORK — free hits

Read them in `REVIEW_QUEUE.md` under **R-027**. The three I would attack first:

- **DOUBT 1 — `_named_in_production` IS A TEXT SEARCH, SO A COMMENT COUNTS AS
  CODE.** A name mentioned only in a comment or docstring in the production half
  is certified as reachable. **Untested, and it is the same disease this whole
  session is about. This is the most dangerous line in my diff.**
- **DOUBT 2 — THE PROPERTY FIX IS A SHAPE, NOT A FORM.** A getter with a frozen
  DEFAULT is now seen. A getter that CLOSES OVER the value is still invisible,
  **proved by my own probe in the same run that proved the fix.** The control I
  wrote will make the next reader think "property" is covered.
- **DOUBT 4 — I NEVER MADE `_production_half` RAISE.** It refuses to run if the
  `__main__` line appears other than once. I wrote that branch and never tested
  it. **An untested error path is how B5 was scored CAUGHT while crashing two
  lines short of the check it claimed to prove.**

---

# PART 2 — **BUILD DOOR 3, unless the Commander has said otherwise (his desk, item 1).**

**HIS RULING STANDS: R-025 IS SERIOUS AND DOOR 3 IS AN ORDER.** He was shown the
proof (162 lines of trading advice on the pilot's screen under a gate that
printed PASSED), both FINDING REPORTS, the plain-words trade-off and a third
cheaper option, and he was told before ruling that the price is Context Deck
instrument 3 slipping. **It has now slipped a SEVENTH time, and that is on me,
not on him** — see his desk.

**BUILD DOOR 3 in `cockpit/funding.py` AND `cockpit/fear_greed.py`.** Gate
declared and committed alone first with no `.py` in that commit, sabotage drill
from birth, fail-safe to one honest line. **The design is written out in
`REVIEW_QUEUE.md` under R-025 — you do not have to invent it.**

**WHAT DOOR 3 IS, IN ONE SENTENCE:** door 2 already spawns a fresh interpreter
and requires it to write nothing AT IMPORT; door 3 is the same proven machinery
one step further — **a fresh interpreter that imports the module, calls
`section_text()` on all three paths, and then SHUTS DOWN, with the child's TOTAL
output required to be empty.** Interpreter shutdown joins non-daemon threads,
flushes every buffer and runs every atexit handler, **so it catches all three
deferred shapes deterministically instead of racing them.**

**THE TWO TRAPS, NAMED BEFORE YOU START:**

1. **A TIMEOUT MUST BE A FAILURE, NEVER A QUIET PASS.** A thread that sleeps
   forever makes the child hang, and "no output before the timeout" is precisely
   what silence looks like. **This is the single most likely way to build a door
   3 that guards nothing.**
2. **THE DRILL MUST PLANT ALL THREE SHAPES AND REQUIRE ALL THREE CAUGHT** — the
   thread, the kept-alive buffer over descriptor 1, and the atexit handler.
   Otherwise door 3 is one more check nobody has ever broken. **The exact three
   are reproduced in R-025 and the patch that installs them is described there.**

**AND A THIRD THING THAT IS PERMITTED BUT IS NOT A SUBSTITUTE.** A cheap 90%
version — a check that reads the instrument's own source and confirms it contains
no machinery capable of deferring a write (`threading`, `atexit`, `subprocess`,
`os.dup`, `open(1`, `Timer`, `QueueHandler`, `__del__`) — **was offered to him
and he did not choose it; he chose the real thing.** You MAY add it as a second,
cheaper guard **only after DOOR 3 itself passes**, and it needs its own positive
control: it must be shown to FLAG a planted `threading.Thread` line before its
silence on the real file means anything. **A session that ships only the cheap
version has not carried out this order.**

**MEASURED FACTS YOU WILL NEED, so you do not re-derive them:** the funding gate
calls `section_text()` **54 times per run**; the funding gate takes **128 s** and
fear_greed **40 s**; both production halves tonight contain **no** deferred-write
machinery of any kind, so **the healthy control must come back silent and if it
does not, something arrived since 2026-07-30 and THAT is your session.**

**AND WHAT THIS PUSHES BACK, SAID SO NOBODY THINKS IT WAS FORGOTTEN:** Context
Deck instrument 3 of 5 — **news headlines, CryptoPanic free tier, HEADLINES ONLY,
no sentiment score, no invented weights, the cut ghost stays cut** — is
`EXECUTION_PLAN.md` Phase 3 step 3 and is **next after DOOR 3**. It has now been
deferred SEVEN times.

**IF YOU ARE RUNNING SHORT, DO PART 1 PROPERLY AND LEAVE PART 2 ENTIRELY.** A
half-built part is worse than no part.

## HOW TO ATTACK PROPERLY

- **BRING A NEW QUESTION. TEN ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* · *"What is the gate's own detector deaf
  to?"* · *"What shape does the real world have that the gate's world cannot?"* ·
  *"What if the module puts its work somewhere the gate is not looking?"* ·
  *"What happens BEFORE the gate is alive to watch?"* · *"Is the sabotage
  actually IN EFFECT when the judge runs?"* · *"WHEN does the gate stop watching,
  and what does the part do after that?"* · **and now mine:** *"WHOSE CODE does
  the swap reach — the part under test, or the test itself?"* **All ten are the
  directions these gates are now strongest in, and reusing any of them is the
  approach most likely to find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** Ten
  sessions running have now done this. **I wrote three predictions: two were
  right and the third was half right — its finding held and its severity claim
  was untested speculation, which I recorded as such rather than as a result.**
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; it costs nothing
  (21 MB). Check `git status` is clean when you are done.
- **EDIT IN BINARY, OR IN TEXT DECODED FROM BINARY — NEVER THROUGH PYTHON'S
  NEWLINE TRANSLATION.** These files are CRLF. **AND A NEW ONE, EARNED TONIGHT:
  if your anchors contain `✓`, `✗` or `→`, DO NOT write the patch in bytes mode.
  `\uXXXX` is not an escape in a bytes literal, so every such anchor matches zero
  times.** I wrote a whole patch script that way and caught it by reading, not by
  any check.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  That guard caught me tonight: an anchor was missing a `**` and the script wrote
  nothing. **It has now caught two consecutive sessions.**
- **NEVER PUT BACKTICKS INSIDE A DOUBLE-QUOTED SHELL STRING.** Put document text
  in a FILE and have Python read it. **And write commit messages with Python
  too — PowerShell 5.1 `Set-Content -Encoding utf8` puts a BOM in the subject
  line, which is now in this repo's `git log` forever because of me.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH ESCAPE INSIDE AN F-STRING
  *EXPRESSION* IS A SyntaxError.** `f"{raw.count(b'\n')}"` will not compile.
  Name the value first. **The last orders warned me about this in bold and I did
  it anyway.** Run `py_compile` before the gate.
- **Run the untouched control FIRST — and run it inside the scratch copy too.**
- **A GREEN GATE IS NOT THE EVIDENCE. PRINT THE DAMAGE.** **A sabotage that
  CRASHES is scored "caught", so one that never really ran looks like a success.**
  I made my sabotage print the recorder's real row count and window, so the
  proof was "180 perfect rows, untouched" and not my say-so.

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item. **DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.**

**You may clear R-027 and R-025** — you built neither. **You may clear R-028**,
which I found tonight and therefore may not clear myself. **You may NEVER clear
R-006.** **And if you fix something, you may not clear your own fix.**

**R-001 has now waited through TWELVE generations of repair, ELEVEN of which were
failed by the next pair of eyes and the twelfth — mine — untested.** It **moves
only when a generation survives an independent attack. Untested is not survived.**

---

# THE 1 AUGUST ERRAND — **CHECK TODAY'S DATE FIRST.**

**On 2026-07-30 it was NOT due, and I confirmed the task rather than assuming:
`schtasks` reports `\ZarX Open Interest` Status **Ready**, Next Run
**01-Aug-2026 09:00**. Six sets of orders have now got this wrong in one
direction or the other.**

**If today is still July: SAY SO AND MOVE ON. Do not read the log as if it had
fired.**

**When 1 August has actually passed:** open `journal/daily_runs.log` and tell the
Commander PLAINLY whether the monthly recorder task actually committed and pushed
real new rows.

**MEASURED, so you do not have to re-derive it:**

    The recorder has run EXACTLY ONCE in its whole history: by hand, on
    2026-07-27, and it appended ZERO rows. The commit-and-push branch has
    therefore STILL never fired for real.
    A healthy run appends 12 rows per asset and reports 192 stored (measured
    2026-07-29 against a copy of the real archive).
    MEASURED 2026-07-30 (evening): data/oi_history/ holds exactly THREE files,
    correctly named, 181 lines each, unchanged across five gate runs.

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
`git show --stat` proves the bar preceded the work. **Eighteen uses of this
pattern and it has survived audit every time.**

**AND RECORD THAT HASH *AFTER* YOUR FINAL PUSH, NOT WHEN YOU WRITE THE ENTRY.**
The cloud watchman pushes every four hours, so `git pull --rebase` before your
push can rewrite your own commit hashes underneath you. Then:

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
(g) **RUN `py_compile` BEFORE THE GATE.**

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

1. **>>> THE ONE THAT MATTERS TONIGHT, AND IT IS A REAL DECISION, NOT A REPORT.
   HIS DOOR 3 ORDER WAS PUSHED BACK BY A GRADE A SESSION WROTE ABOUT ITS OWN
   FINDINGS — AND THAT SESSION IS THE ONE THE PUSH-BACK EXCUSED FROM BUILDING.**
   I graded both of tonight's findings SERIOUS, honestly and on his own wording
   of Step 2.2, and the rule for SERIOUS is *fix it and stop, build nothing.* **I
   followed the rule.** But he should see the shape of it plainly: **his direct
   order lost to a machine's grade of its own work, and Context Deck instrument 3
   has now slipped a seventh time.**
   **AND THE STRUCTURAL FACT UNDERNEATH IT, WHICH ONLY HE CAN ACT ON.** His
   wording of Step 2.2 asks whether the output is wrong ON ITS FACE. **A gate
   that cannot see something is never wrong on its face** — a blind gate prints a
   clean green run. So **every "the gate is blind to X" finding scores 2.2 = NO,
   and 2.2 = NO alone makes it SERIOUS.** Every session's Part 1 is to look for
   exactly those. **That is not an argument to weaken the bar and I am not
   proposing one** — it is the reason the build keeps slipping, said out loud so
   he can decide what he wants instead.
   **THREE THINGS HE COULD SAY, ANY OF WHICH IS ONE WORD:** *"build Door 3 first
   next session, findings after"* · *"keep the rule as it is"* · *"a finding that
   is LATENT — where the shape does not exist in the shipped file today — is
   BORDERLINE, not SERIOUS, and comes to me."* **A session may recommend and
   never rule. My recommendation is the third.**
2. **HIS RECORDER'S GATE CERTIFIED A TEST THAT TESTED NOTHING.** Repaired. **He
   should know the protection was never missing — what was wrong was the claim**,
   for the second day running, in the same check.
3. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** If a future
   session correctly fixes `run(symbols=SYMBOLS, ...)`, the gate goes red for a
   good change. **I made this worse tonight, knowingly** — my reachability rule
   hardcodes four more names. **He can overrule in one word.**
4. **AND THE ONE I WOULD MOST LIKE HIM TO SAY YES TO: FIX THE PATTERN, NOT JUST
   THE TEST.** `def run(symbols=SYMBOLS, ...)` and `fetch_history` still freeze
   their globals. **The one-line change that ends this entire class is
   `symbols=None`, resolved from the global in the body — and `funding.py`
   already does it that way.** It touches what the pilot reads, so no session may
   make it during a repair to a test. **Seven generations have now fixed the
   instance and left the pattern. Only he can end that.**
5. **R-023, CATEGORY B: on the real B9 defect the recorder's gate exits 1 but
   ends in a Python stack trace instead of saying FAILED.** Filed, not fixed.
6. **THE FUNDING GATE GOES RED NEAR A SETTLEMENT (R-021).** SMALL, unrepaired.
   13:20 UTC was clean tonight, first run.
7. **R-028, NEW AND CATEGORY B: the settlement race mixes the RATES too**, not
   just the clock — three funding numbers from two different settlement periods,
   printed side by side as one snapshot, differing by 10x for that reason alone.
   **R-007's older limb — the stale settlement TIME — is CLEARED after eight
   sessions untouched: reproduced deterministically, control first, and the
   window is judged ACCEPTABLE and said so out loud.**
8. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL NEW
   ROWS.** The errand above. **Due 1 August.**
9. **`cockpit/brief.py` HAS NO GATE — he has ruled: NOT NOW, BEFORE GOING LIVE.**
10. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
11. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never after
    seeing results.**
12. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
13. **The settled-rate anchor (R-004)** — returned to him on correct facts.
14. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
15. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED FOUR TIMES, NOT ADOPTED — AND
    TONIGHT IT CAUGHT ME.** I ran the scan by hand before every commit. Seven
    pre-existing hits, all inside backticks, all deliberate quotations. **Then my
    own paragraph explaining the count QUOTED two of the fingerprints, the scan
    reported nine, and the document would have shipped saying "seven" while the
    scan printed nine — contradicting itself on its own face.** Fixed before the
    commit, **by a check that does not exist and that I ran by hand. A one-line
    scan would close this.**
16. **THE CATEGORY B PILE IS SIX DEEP** and is cleared before the ship is used
    for real, at the same moment `brief.py` gets its gate.
17. **THIRTEEN LAW CANDIDATES, NONE ADOPTED, ALL HIS CALL — and I am proposing NO
    new one.** What tonight earned is the SAME amendment the eleventh generation
    proposed, now earned a second time by a different check on a different day:
    - *"A check that reports the ABSENCE of something must first be proved able
      to detect its PRESENCE"* → **add: "in EVERY FORM it claims to cover, and it
      must also be proved to stay SILENT about the forms it does not."** **Two
      consecutive sessions have now been failed by exactly this, in the same
      file. That is the strongest case any candidate on the list has.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.** **Twelve generations, eleven of them failed by the next pair of eyes,
and the twelfth is sitting in front of you untested — that is what the substitute
is worth, and it only works if somebody actually attacks.**
