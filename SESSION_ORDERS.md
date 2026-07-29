# ZAR X PHASE 3 — **ATTACK THE NINTH REPAIR. THEN CLOSE THE BRIEF'S TWO DOORS — THAT IS THE COMMANDER'S OWN ORDER AND IT HAS NOW WAITED THROUGH TWO SESSIONS.**

*Written 2026-07-29 (evening) by the session that invented a fourteenth
sabotage, watched it walk through a green gate, and repaired it. **Stated before
anything else: I found the fault and I wrote the repair, so I may not grade it —
that is R-020 and it is your worklist.** Forty-five sabotages now live in three
files and **all forty-five were invented by the sessions that then defended
against them.** You are the first pair of eyes that built none of it.*

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is the exact bars and commands. This part is the story,
so you understand WHY before you read WHAT. The Commander is not a programmer
and asked for it in this form. Write your own report to him the same way.*

## Where the ship is

Three parts break themselves on purpose every time they run and refuse to pass
if any breakage goes unnoticed. **Forty-five deliberate lies live in the code;
all forty-five are caught.**

**Read that the way this ship has learned to read it: every one of the forty-five
was invented by the session that then defended against it.** And on 2026-07-29
evening a brand-new one walked straight through the newest gate.

## What happened just before you

**Nine sessions in a row have each found real holes in the work of the session
before.** 48/48 with four lies walking through. Then five more. Then seven. Then
four. Then four again. Then three. Then three more. Then two. **Then one — and
it is the quietest defect this ship has recorded.**

Every earlier session asked what the gate was *looking at*, or *what world it
could build*. **Yesterday evening's session asked something different: every
check finds the recorder's work by ASKING THE RECORDER WHERE IT PUT IT. WHAT IF
IT PUTS IT SOMEWHERE ELSE?**

The answer was one line long. This ship had learned R-014's lesson — *a gate may
not take anything it measures by from the file it is judging* — and applied it
five separate times. **Every single application was to a VALUE the gate
compares.** Nobody applied it to `csv_path()`, because `csv_path()` is not a
value. **It is the address the gate walks to before it compares anything.**

- **B14 — the archive quietly moves.** `csv_path` returns `f"{symbol}.csv"`
  instead of `f"{symbol}_{PERIOD}.csv"`. An ordinary filename tidy-up. **It
  breaks no logic, writes no wrong number, loses no row from the file it writes,
  and its printed report is entirely TRUE about that file.** All twenty-three
  places in the recorder that locate a CSV followed it to the new name.
  **13 of 13 caught, GATE PASSED, exit 0.**

**The most damning line in the whole run was check (m) — the check built the day
before for the sole purpose of proving the archive survives.** It seeded the
archive rows into the new filename, watched the recorder append to the new
filename, read them back from the new filename, and certified them: *"12 archive
row(s) the source NO LONGER SERVES survived byte for byte."*

Run against a byte-for-byte copy of the REAL archive, through `--record` which
is what the monthly task calls: the archive `<SYMBOL>_4h.csv` was left **frozen
at 180 rows**, a second file was started, and the line the Commander is under
standing order to judge this recorder by read **`180 new row(s) appended, 180
stored`** where the honest run prints **192**.

**The lesson, in one line: A GATE THAT ASKS THE MODULE WHERE TO LOOK WILL FIND
EVERYTHING PERFECT WHEN IT GETS THERE.**

**Graded SERIOUS and repaired** under Gate 3.2b-R6, declared before the code
existed. **Step 3.3 was therefore deferred a SEVENTH time.**

**AND THE HONEST QUALIFICATION, WHICH CUTS AGAINST THE FINDING: B14 DESTROYS
NOTHING.** B13 deleted 34 irreplaceable rows. B14 deletes none — the two files
together still hold every row, and concatenating them repairs it. **It is
SERIOUS because it is invisible and happens by accident, not because anything is
lost.** Do not let a later session quote it as another B13.

## **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

**1. R-016 — HE HAS RULED: CLOSE THE TWO DOORS. IT IS NOT DONE.** Asked in plain
words on 2026-07-29 evening, having deferred it once with *"attack first, then
decide"*, he ruled **close them now**. **The session then deferred his order**,
because B14 graded SERIOUS the same evening and his own rule says SERIOUS means
*fix it and stop, build nothing.* **That was a session's judgement about the
Commander's own instruction and it is recorded rather than hidden.**

**IT IS YOUR PART 2 AND IT IS NOT OPTIONAL. Do not re-argue it and do not ask him
to confirm it — he has ruled.** Until it is done this stays true: **one line of
code in either Context Deck instrument can put a trade instruction on his Morning
Brief with every gate green.**

**2. R-019 — SETTLED, AND `THE_PATTERN.md` IS ALREADY EDITED.** He refused the
wording a session proposed for Step 2.2 of THE FINDING REPORT and **wrote his
own**, which is now in the file verbatim under a heading saying the words are
his. **Read it before you grade anything.** His version is stricter than the
draft in a way nobody proposed: **his knowledge of this ship's own rules counts
as a prediction about him, not as something the output shows.** R-019 is CLEARED
— by him, the only authority who could clear it. **Nothing is owed to him on it.**

## Your job, in order

**1. ATTACK LAST NIGHT'S REPAIR (R-020)** — Gate 3.2b-R6, `GATE_CSV_SUFFIX`,
`_gate_csv_path`, the named check (c), the REFUSES-TO-RUN branch and the new
sabotage B14. **Report either way.**

**2. THEN CLOSE THE BRIEF'S TWO DOORS (R-016) — HIS ORDER.** Gate declared
first, committed alone with no `.py` in it. What closing it looks like: the
silence check compares `sys.stdout`/`sys.stderr` against
`sys.__stdout__`/`sys.__stderr__` and captures at the **file-descriptor** level
rather than the name level, and **something watches what the modules write at
IMPORT time**. Neither is written. **If Part 1 finds something SERIOUS, grade it
on THE FINDING REPORT first and tell him the doors are waiting again — but say
so out loud, because that will be the third session in a row.**

**3. THE 1 AUGUST ERRAND — CHECK TODAY'S DATE FIRST.** See its own section.

## How to attack properly

- **BRING A NEW QUESTION. SIX ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* · *"What is the gate's own detector deaf
  to?"* · *"What shape does the real world have that the gate's world cannot?"*
  · **and now** *"What if the module puts its work somewhere the gate is not
  looking?"* **All six are the directions these gates are strongest in, and
  reusing any of them is the approach most likely to find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** Six
  sessions running have now predicted every one of their attacks correctly
  beforehand, and that is what proves a hole is structural rather than luck.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo. Check
  `git status` is clean when you are done.
- **EDIT IN BINARY MODE.** These files are CRLF. Last night's first attempt read
  the source in text mode and wrote it back with `newline=''`, silently
  converting 1,528 line endings and turning a one-line sabotage into a whole-file
  rewrite. **It was caught in the diff and thrown away, but a conclusion drawn
  from it would have been worthless.** Always diff the sabotage and confirm it is
  the number of lines you meant.
- **Run the untouched control FIRST — and run it inside the scratch copy too.**
  If the healthy copy does not pass there, your rig is broken and nothing you
  conclude means anything.
- **A GREEN GATE IS NOT THE EVIDENCE. PRINT THE DAMAGE.** B14 was believed only
  after a side-by-side `--record` run against a copy of the real archive showed
  the file frozen and a second one started. **A sabotage that CRASHES is scored
  "caught", so one that never really ran looks like a success.**
- **If your text anchor matches more than once, REFUSE TO RUN** rather than
  editing the first match.

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item. **This ship still has not seen a clean review and it
needs one eventually.**

**DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.** After nine sessions that each
found something, the pull to also find something is real and it is a trap.

**You may clear R-020** — you built none of it. **You may clear R-007**, which
has now been untouched for five sessions running. **You may never clear R-006.**
**And if you fix something, you may not clear your own fix.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment, and the housekeeping that has bitten this ship. None
of it is repeated here.** If you have not read it, stop and read it. **It changed
last night: Step 2.2 of THE FINDING REPORT now carries the Commander's own
wording.**

**Specific to THIS job:**

1. **The last TWO entries of `PROGRESS_LOG.md`** — the review and the repair.
   **Read them as CLAIMS, not results. They are what you are auditing.** The file
   is ~347 KB; reading all of it will eat the budget you need for the work.
2. **`data/open_interest.py`** — `GATE_CSV_SUFFIX`, `_gate_csv_path`, the named
   check (c) in section (a), the REFUSES-TO-RUN branch, and the new sabotage
   B14. **All of it inside `__main__`; the production half is provably
   byte-identical, by sha256.**
3. **`REVIEW_QUEUE.md` — R-020 is your worklist**, and its five recorded doubts
   are starting points, **not the assignment**. **R-006 may NEVER be cleared by
   you or any in-house session.**
4. **`ROADMAP.md`** — the MEASURED data-source facts table. If anything you
   measure disagrees with it, **your measurement wins and you write the
   correction down.**

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A **FIFTEENTH** sabotage, invented by you, thrown at Gate 3.2b-R6, result
   recorded either way.
2. **R-016's two doors CLOSED**, under a gate declared before the code exists —
   or, if Part 1 forbids it, the reason said out loud to the Commander.
3. Any leak found is graded on THE FINDING REPORT **before** any repair, using
   **the Commander's wording of Step 2.2**, and repaired only if that grade says
   to.
4. `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3, and
   `data/oi_history/` unchanged **unless a legitimate run appended** — in which
   case say so, with the row count, and check it.

**Four of four or it has not cleared, and "three of four with a good
explanation" is the phrasing this ship exists to refuse.**

---

# PART 1 — THE NINTH REPAIR (R-020)

`python data\open_interest.py` — fourteen sabotages, check (c), sections (l) and
(m). **That is the claim under review, not the verdict.**

**Where this gate is now STRONGEST — so do NOT spend your time here:**

- the gate holds its own `GATE_CSV_SUFFIX` and every CHECK locates files with
  `_gate_csv_path`, never the module's `csv_path`
- a named check prints the module's filenames beside the gate's own, so a moved
  archive is diagnosed rather than merely fatal
- the folder `oi_history` is pinned by `_record_does_the_job` — **attacked twice
  now and it held both times**
- both ends of the printed window are compared to a fetch the gate makes itself,
  on both sides of the run
- rows the source no longer serves are seeded on disk and required to survive
  byte for byte, proved outside the window first
- the printed counts are compared to rows the gate counts itself, on two runs
- a report line that fails to parse is a FAILURE, never a skip
- every loop runs over `GATE_SYMBOLS`, the gate's own list
- `--record` is driven for real, in both outcomes, as a subprocess

## THE FIVE DOUBTS ITS AUTHOR FILED AGAINST IT — free hits, recorded not hidden

1. **I FIXED THE ADDRESS OF ONE FILE AND SWEPT FOR NO OTHERS.** The whole
   finding was that this ship applies R-014's lesson to VALUES and never to
   ADDRESSES — **and then I fixed exactly the one address I had attacked.**
   `cockpit/funding.py` and `cockpit/fear_greed.py` were not examined for the
   same class at all. **THIS IS THE STRONGEST LEAD IN THE BUILDING.**
2. **THE GATE'S ADDRESS IS A HARDCODED `'_4h.csv'`.** A legitimate change of
   `PERIOD` fails this gate loudly and **the obvious move will be to edit the
   gate to match** — R-001's conviction, one string worse.
3. **THE REFUSES-TO-RUN BRANCH SKIPS THIRTEEN OF FOURTEEN SECTIONS** when the
   name check fails. The author *believes* that is right. **"I believe" is the
   phrasing this ship files rather than trusts.**
4. **B14 IS JUDGED IN THE DRILL BY ONE JUDGE.** Check (c) catches it first, so
   there are two — but that is R-018's doubt 5 inherited, not closed.
5. **THE RUNTIME WAS STILL NEVER MEASURED**, two sessions after it was first
   filed. The 4h-boundary exposure R-013 named is still unwatched.

## STILL KNOWN-WEAK ACROSS THE SHIP — named so you do not have to find them

1. **FUNDING'S TWO-ASSETS-FAIL BLOCK IS GUARDED BY NOTHING.** `_partial_checks`
   breaks exactly ONE asset at a time. **Named in six sets of orders now.**
2. **THE RECORDER'S CHECK (e) IS STILL BTCUSDT-ONLY.**
3. **B1 IS STILL A NO-OP ON A MACHINE SET TO UTC.**
4. **`_raw_truth` STILL READS `FAPI_BASE`, `HIST_PATH`, `PERIOD`, `LIMIT` AND
   `TIMEOUT` FROM THE MODULE IT JUDGES.** R-015 doubt 1, still open.
5. **`cockpit/brief.py` STILL HAS NO GATE** — and the Commander has ruled: **NOT
   NOW, BEFORE GOING LIVE. Do not build it and do not re-argue it.**
6. **NOTHING CHECKS THAT A GATE'S DESCRIPTION MATCHES WHAT IT DOES.** Section
   (h) announced "ELEVEN ways" while running thirteen; it was found by reading
   and corrected by hand. **R-011's third doubt, still unguarded.**

## IDEAS TO GET YOU STARTED — find your own, these are not the assignment

    - doubt 1. Where else does a gate ask the thing it is judging where to
      look, or when, or how much? Try the two Context Deck instruments.
    - the gate deletes its scratch tree at the end. What if a check leaves a
      file behind that a LATER check then reads?
    - two checks run the recorder repeatedly. What if the monthly task fires
      WHILE the gate is running?
    - `_report_is_true` returns False on `if not good`. Is a sabotage that
      makes the run FAIL being scored "caught" while never reaching the
      comparison? **That is the B5 shape.**
    - the REFUSES-TO-RUN branch is new machinery that exits early. Can
      anything reach it that should not, or pass through it that should stop?

---

# PART 2 — CLOSE THE BRIEF'S TWO DOORS (R-016). **THE COMMANDER'S ORDER.**

**Not Step 3.3. He ruled on this and it has waited through two sessions.**

**Declare the gate first, commit it alone with no `.py` in the commit**, name the
awkward edge cases before writing code, and **give the new checks a sabotage
drill FROM BIRTH.** The two doors, from the review that found them:

- **S16 / F14's bigger brother — speaking PAST the ear.** `_capture` listens with
  `contextlib.redirect_stdout` / `redirect_stderr`, which rebind the **names**
  `sys.stdout` and `sys.stderr`. A `logging` handler bound to the real stderr at
  import time, or `os.write(1, …)` straight to the file descriptor, walks past
  both. **35 advice lines landed on the gate's own screen with three green ticks
  underneath reading "the doorway wrote NOTHING".**
- **F15 — speaking BEFORE the ear was listening.** Nothing anywhere watches what
  a module writes at IMPORT time, and `brief.py` line 23 imports one.

**Both were proved to reach the real Brief**, and `run_daily.bat` writes it to
`journal/daily_runs.log` with `2>&1` and copies it to the Commander's phone.

**If the session is running short, do PART 1 properly and leave PART 2
entirely** — but say so plainly, because that will be the third session running
in which his order did not get done.

---

# THE 1 AUGUST ERRAND — **CHECK TODAY'S DATE FIRST.**

**Two sets of orders have now got this wrong in one direction or the other.**
The orders of 2026-07-29 morning called it "NOW DUE" on 29 July, which it was
not. **Check the date before you act on this section.**

**When 1 August has actually passed:** open `journal/daily_runs.log` and tell
the Commander PLAINLY whether the monthly recorder task actually committed and
pushed real new rows.

**MEASURED, so you do not have to re-derive it:**

    schtasks: \ZarX Open Interest — Status Ready, Next Run 01-Aug-2026 09:00
    The recorder has run EXACTLY ONCE in its whole history: by hand, on
    2026-07-27, and it appended ZERO rows. The commit-and-push branch has
    therefore STILL never fired for real.
    MEASURED 2026-07-29 evening against a copy of the real archive: a
    healthy run appends 12 rows per asset and reports 192 stored.

**WRITE DOWN WHAT YOU EXPECT BEFORE YOU READ THE LOG. The honest figure on
1 August is roughly THIRTY new rows per asset and a stored count near 210** —
not 180, and not 360. **If the log says something you did not predict, that is a
finding, not a relief.**

**AND NOW THERE IS A SECOND THING TO CHECK, EARNED BY B14: look at
`data/oi_history/` itself and confirm there are THREE files and that they are
named `BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`, `SOLUSDT_4h.csv`.** A fourth file, or
a different name, is the defect B14 described arriving for real.

**Do not assume it worked because the task returned 0** — `schtasks` already
reported SUCCESS once for a task that could never run at all. **Read the file
and count the rows yourself.**

---

# THE RIG (defined before you run, because a broken rig proves nothing)

**Sabotage in a scratch copy OUTSIDE the repo.** All three modules import only
the standard library plus `requests` — no repo imports — so each can be copied
ALONE into scratch. **But copying the WHOLE repo is better and costs nothing.**
`open_interest.py` derives `HISTORY_DIR` from its own `__file__`, so **a copy in
scratch can only ever write to scratch.** Confirm `git status` is clean
afterwards. **Run the untouched control too, inside the copy. Never let a drill
write to `data/oi_history/` — fingerprint it by sha256 before and after.**

**And the trick that proved both B13 and B14: seed a scratch folder with a
byte-for-byte copy of the REAL archive, put the module beside it, and run
`python open_interest.py --record`.** That is exactly what the monthly task does,
and it is the only rig that shows what the Commander will actually see.

---

# IF ANYTHING LEAKS: GRADE IT FIRST, THEN REPAIR UNDER A GATE DECLARED FIRST

**FILL IN THE FINDING REPORT BEFORE YOU REPAIR ANYTHING.** Four steps, plain
sentences, in `THE_PATTERN.md`. **Step 2.2 now carries the Commander's own
wording — read it there, not here.** Then:

    SERIOUS ....... fix it, and stop. Build nothing.
    BORDERLINE .... do NOT fix it. Report and stop. The Commander rules.
    SMALL ......... do NOT fix it. File it in REVIEW_QUEUE.md as CATEGORY B
                    and carry on to PART 2.

**If you do repair: DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY
ALONE, WITH NO `.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then
`git show --stat` proves the bar preceded the work. **Fourteen uses of this
pattern, and it has survived audit every time.** Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove
    it two ways, do not assert it:** every diff hunk at or after the `__main__`
    line (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a
    sha256 of the production half before and after, printed side by side.
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself, the
    gate never reads a constant belonging to the file it is judging, and — B14's
    lesson — THE GATE NEVER ASKS THE MODULE WHERE TO LOOK.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others,
    caught every run, originals restored and the restoration verified.
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT, **and must be shown to fail
    for the reason it claims, not incidentally.** **That is the evidence; the
    in-run drill is not.** **And prove your new sabotage's judge returns False
    rather than raising** — a crash scored as a catch is the B5 failure.
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed".**

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the
actual output, and the verdict — **including if it is all clean.** A review that
only appears in the log when it finds something teaches the next session that
silence means safety.

**`REVIEW_QUEUE.md`: you MAY clear R-020 (you built none of it), and R-007 too
if it settles.** R-001 has now waited through **eight FAILED generations of
repair, with the ninth untested**, and **moves only when a generation survives an
independent attack. Untested is not survived.** Items you cannot settle stay OPEN
with a note on what is missing; **leaving something open is a legitimate recorded
outcome.** **R-006 is not yours, ever. Never delete an item. Never edit a cleared
verdict.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly", "I believe" or "this should be fine" about anything that ships —
FILE IT in `REVIEW_QUEUE.md` before the commit that ships it.**

---

# BEFORE YOU FINISH

**Do the closing ritual exactly as `THE_PATTERN.md` sets it out** — seven steps,
ending with the next session's orders, the push, and your plain-words report to
the Commander. **It is not repeated here.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **R-016 IS AN ORDER HE HAS ALREADY GIVEN AND IT IS STILL NOT DONE.** Close
   the two doors. **Do not ask him again; he ruled.** Tell him when it is done,
   or tell him plainly why it was deferred a third time.
2. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL
   NEW ROWS.** The errand above. **Due 1 August.**
3. **`cockpit/brief.py` HAS NO GATE — and he has ruled: NOT NOW, BEFORE GOING
   LIVE.** Recorded in `EXECUTION_PLAN.md` as a standing requirement. **Do not
   build it, and do not re-argue it.**
4. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
5. **The risk-doctrine decision** — the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never after
   seeing results.**
6. **`MAX_PLAUSIBLE_RATE`** — measured at 13-16x looser than Binance's published
   cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
7. **The settled-rate anchor (R-004)** — returned to him on correct facts.
8. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. He can reverse it
   in one word.
9. **A DOCUMENT-INTEGRITY CHECK.** Nothing on this ship checks that its own
   documents are not corrupted. Found by a human looking, twice. **A one-line
   scan would close it. Recommended, not adopted.**
10. **ELEVEN law candidates, none adopted, all his call:**
   - *"A session may not certify its own work; anything it cannot certify is
     filed in `REVIEW_QUEUE.md` before the commit that ships it, and only an
     independent reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."*
   - *"A check is not proven until it has been deliberately broken."*
     **Fourteen working implementations and still not law.**
   - *"A gate must verify what the pilot READS — the whole line, words included
     — not what the parser returned."*
   - *"A sabotage that is scored CAUGHT must be shown to fail for the reason it
     claims."*
   - *"A gate must hold EVERY path the pilot can see to the same standard — the
     degraded path, the offline path and every asset — not only the path that
     was under attack when the lesson was learned."*
   - *"A gate may not derive anything it measures by — a word, a list, a limit —
     from the file it is judging. It holds its own copy and compares the
     module's against it by name."*
   - *"A gate must be shown to be watching the OBJECT the pilot actually
     receives, and the STATE the part is actually in when it runs for real."*
   - *"Every output a human will act on must be checked against the thing it
     describes — including the output of the test itself, and including the
     sentence a part prints about its own work."*
   - *"A gate must be shown to BUILD the situations it claims to judge. Where
     the state a part meets in real life differs from the state the test
     creates, the test must construct the real one — and prove it constructed it
     — or say out loud that it has never been tested there."*
   - **NEWEST, earned 2026-07-29 (evening):** *"A gate must hold its own ADDRESS
     as well as its own expectations. It may not ask the file it is judging
     where that file put its work — it goes to the place IT names, and a module
     writing anywhere else is a failure, not a destination."* **Earned by B14,
     which moved the archive to another filename while fourteen checks — including
     the one built the day before to prove the archive survives — followed it
     there and certified it.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.** Information
instruments can carry a lighter guard. The gauntlet cannot. **NINE sessions in a
row have now failed their predecessor's work. The substitute is working — and
every hole was found by a session ORDERED to break things rather than one being
careful. Whatever reviews Phase 6 must be ordered to break it too.**
