# ZAR X PHASE 3 — **ATTACK THE NINTH REPAIR (R-020). IT WAS NOT TOUCHED LAST SESSION AND THAT IS SAID PLAINLY. THEN ATTACK THE TENTH (R-022).**

*Written 2026-07-29 (night) by the session the Commander ordered to build first
and attack second. **His order is done: the Brief's two doors are closed.** I
found none of the faults I fixed by attacking someone else's work — I fixed the
two the previous session had already named, so **there is no independent review
in this session at all** and the ship has now gone one full generation without
one. **Two repairs are waiting for a first pair of eyes, not one.**

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is the exact bars and commands. This part is the story,
so you understand WHY before you read WHAT. The Commander is not a programmer
and asked for it in this form. Write your own report to him the same way.*

## Where the ship is

**R-016 IS DONE.** The Commander ruled twice that the Brief's two doors were to
be closed, two sessions deferred it, and he ruled a third time — *"do not defer
my order a third time"* — and reversed the rhythm himself so it would happen.
**It happened.**

    cockpit/fear_greed.py   GATE 3.1-R6 PASSED  exit 0  17 sabotages caught
    cockpit/funding.py      GATE 3.2-R6 PASSED  exit 0  18 sabotages caught
                                                55 checks green, 0 red
    data/open_interest.py   GATE 3.2b-R6 PASSED (2026-07-29 evening, 14)

**Fifty-one deliberate lies now live in three files and all fifty-one are
caught.** Read that the way this ship has learned to read it: **every one of
the fifty-one was invented by the session that then defended against it.**

## What happened just before you — **AND THE PART THAT MATTERS MOST**

**NINE SESSIONS IN A ROW EACH FOUND REAL HOLES IN THE WORK OF THE SESSION
BEFORE. THE TENTH — MINE — FOUND NONE, BECAUSE IT WAS NOT LOOKING.** The
Commander ordered building instead, for a good reason, and authorised it in
advance. **But the consequence is yours to carry: TWO repairs now sit
un-attacked instead of one.**

- **R-020** — the ninth repair, Gate 3.2b-R6, the open-interest recorder.
  **Not one of its five recorded doubts was tested. It is completely untouched.**
- **R-022** — the tenth, Gates 3.1-R6 and 3.2-R6, built last night by me.

**DO R-020 FIRST.** It has waited two sessions, exactly as R-016 did, and this
is how an item becomes permanent furniture.

## The two doors, and what closing them actually looked like

**Both were proved OPEN before anything was repaired**, predictions written down
first:

    control  print()           -> the old ear heard 'ADVICE VIA print()'
    os.write(1, ...)           -> the old ear heard ''   *** ESCAPED ***
    logging -> real stderr     -> the old ear heard ''   *** ESCAPED ***

The old ear used `redirect_stdout`/`redirect_stderr`, which rebind the **NAMES**
`sys.stdout` and `sys.stderr`. They do not own the descriptors underneath, and
they cannot reach an object somebody already holds a reference to. **A logging
handler built during an import is the dangerous one, because nothing about it is
exotic.**

**Door 2 was worse.** Nothing anywhere watched what a module writes at IMPORT
time, and `brief.py` imports both instruments. One injected line:

    >> funding is negative on all three - the crowd is short, go long
    ==============================================================
      ZAR X — MORNING BRIEF   2026-07-29 20:44   [4h]

**The trade instruction lands ABOVE THE HEADER — the first thing on the page —
and the gate printed three green ticks underneath reading "the doorway wrote
NOTHING".**

**THE LESSON, IN ONE LINE: A LISTENER THAT CANNOT HEAR REPORTS SILENCE, AND
SILENCE IS WHAT A PASSING GATE LOOKS LIKE.** So the ear is now **made to prove
it can hear down all three routes before its silence is believed.** That check
runs first and everything else in the section depends on it.

## **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

**`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT AND IS GREEN
THE REST OF THE TIME. R-021, CATEGORY B, graded SMALL at the Step 1 veto.**

**BINANCE SETTLES AT 00:00, 08:00 AND 16:00 UTC. Check the clock before you
believe a red funding gate.** The controlled comparison — the untouched `3.2-R5`
bytes from commit `74ec950` run in a scratch tree beside the new gate:

    ~15:30-15:45 UTC   OLD 3.2-R5 (untouched, on arrival)   FAIL x4
    16:02-16:15 UTC    NEW 3.2-R6                           FAIL, FAIL, FAIL, PASS
    16:52-16:56 UTC    OLD 3.2-R5                           **PASS x2**
    16:57-17:03 UTC    NEW 3.2-R6                           **PASS x3**

**Both versions fail inside the window and both pass outside it**, so it is not
the R-016 repair and it is not new. Runtime is ~130 seconds per run — which also
answers R-020's own fifth doubt, unmeasured for two sessions.

**>>> AND THE WARNING THAT MATTERS MOST: OUTSIDE A SETTLEMENT WINDOW, A RED
FUNDING GATE IS A REAL FAILURE. TREAT IT AS ONE.** The first draft of these
orders said the gate is "red three runs in four" full stop — **written from one
45-minute window and corrected the same night after the Commander asked why it
had passed in previous sessions.** A session that shrugs at a red gate because
"R-021 says it does that" is doing the exact thing this ship exists to prevent.

**The cause:** `_core_checks` and `_partial_checks` bracket the module's fetch
with a `before` snapshot and an `after` snapshot and accept either. Binance's
`lastFundingRate` is a running estimate — measured moving twice in eleven
seconds — so **when it moves twice inside the bracket, the module's HONEST value
matches neither bookend.**

**IF IT IS RED, CHECK THE UTC CLOCK FIRST, THEN RUN IT AGAIN AND SAY HOW MANY
RUNS IT TOOK. Never call a red gate "the known flakiness" and move on** — the moment anyone does that, this SMALL
finding has become the thing that breaks the ship's honesty.

**IF YOU REPAIR IT: TIGHTEN THE BRACKET, NEVER THE BAR.** The obvious move is to
allow "close enough" and that is R-001's conviction in one line of diff. The
honest repair is **bounded re-observation** — take a fresh bracket, try again, a
small fixed number of times, still demanding EXACT equality against a value
Binance actually served. A sign flip, a dropped x100 or a miswired ticker
matches no observed value on any attempt, so **nothing is weakened; only the
number of chances to hit a moving target changes.**

## **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

**1. R-016 IS DONE.** Take it off his desk. Do not re-open it, do not re-argue
it. **It is NOT CLEARED — that is R-022 and it is your job, not his.**

**2. `cockpit/brief.py` GETS NO GATE YET.** He has ruled: **NOT NOW, BEFORE
GOING LIVE.** Do not build it and do not re-argue it. **This matters more than
it did yesterday** — see R-022 doubt 2 below, which is about the Brief's import
surface and is NOT the same thing as building brief.py a gate.

**3. R-019 IS CLEARED BY HIM.** Step 2.2 of THE FINDING REPORT carries his own
wording, verbatim, in `THE_PATTERN.md`. **Read it before you grade anything.**

## Your job, in order

**1. ATTACK R-020 — THE NINTH REPAIR.** Gate 3.2b-R6, `GATE_CSV_SUFFIX`,
`_gate_csv_path`, the named check (c), the REFUSES-TO-RUN branch, sabotage B14.
**Two sessions have now failed to look at it. Report either way.**

**2. ATTACK R-022 — LAST NIGHT'S REPAIR.** Its author filed **seven** doubts
against his own work. **They are starting points, not the assignment.**

**3. THE 1 AUGUST ERRAND — CHECK TODAY'S DATE FIRST.** On 2026-07-29 it was NOT
due. See its own section.

## How to attack properly

- **BRING A NEW QUESTION. SEVEN ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* · *"What is the gate's own detector deaf
  to?"* · *"What shape does the real world have that the gate's world cannot?"*
  · *"What if the module puts its work somewhere the gate is not looking?"* ·
  **and now** *"What happens BEFORE the gate is alive to watch?"* **All seven
  are the directions these gates are strongest in, and reusing any of them is
  the approach most likely to find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** Seven
  sessions running have now predicted their attacks correctly beforehand, and
  that is what proves a hole is structural rather than luck.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo. Check
  `git status` is clean when you are done.
- **EDIT IN BINARY MODE.** These files are CRLF. A text-mode round trip once
  converted 1,528 line endings and turned a one-line sabotage into a whole-file
  rewrite. **Always diff the sabotage and confirm it is the number of lines you
  meant** — last night's import drill prints exactly that, and you should too.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE, REFUSE TO RUN.** This is not
  theoretical any more. **Last night's guard fired on its very first run** — the
  anchor matched twice because writing it into the file created the second
  match. Without it, the sabotage would have been injected into its own anchor
  definition and scored ESCAPED for a reason that had nothing to do with the
  door.
- **Run the untouched control FIRST — and run it inside the scratch copy too.**
- **A GREEN GATE IS NOT THE EVIDENCE. PRINT THE DAMAGE.** **A sabotage that
  CRASHES is scored "caught", so one that never really ran looks like a
  success.**

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item. **This ship still has not seen a clean review.**

**DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.**

**You may clear R-020 and R-022** — you built neither. **You may clear R-007**,
untouched for six sessions. **You may NEVER clear R-006.** **You may not clear
R-016; only an attack on R-022 settles that.** **And if you fix something, you
may not clear your own fix.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment, and the housekeeping that has bitten this ship. None
of it is repeated here.** **It was NOT edited last night** — the Commander
reversed the rhythm for one session only, by name, and the rhythm stands.

**Specific to THIS job:**

1. **The last TWO entries of `PROGRESS_LOG.md`** — the ninth repair and last
   night's build. **Read them as CLAIMS, not results. They are what you are
   auditing.** The file is ~370 KB; reading all of it will eat your budget.
2. **`data/open_interest.py`** for R-020, and **the `__main__` halves of
   `cockpit/funding.py` and `cockpit/fear_greed.py`** for R-022. **All three
   production halves are provably byte-identical, by sha256, printed in the
   log.**
3. **`REVIEW_QUEUE.md` — R-020 and R-022 are your worklist**, and their recorded
   doubts are starting points, **not the assignment.** **R-006 may NEVER be
   cleared by you or any in-house session.**
4. **`ROADMAP.md`** — the MEASURED data-source facts table. If anything you
   measure disagrees with it, **your measurement wins and you write the
   correction down.**

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A new sabotage, invented by you, thrown at **Gate 3.2b-R6 (R-020)**, result
   recorded either way.
2. A new sabotage, invented by you, thrown at **Gate 3.1-R6 or 3.2-R6
   (R-022)**, result recorded either way.
3. Any leak found is graded on THE FINDING REPORT **before** any repair, using
   **the Commander's wording of Step 2.2**, and repaired only if that grade says
   to.
4. `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3, and
   `data/oi_history/` unchanged **unless a legitimate run appended** — in which
   case say so, with the row count, and check it. **Confirm there are exactly
   THREE files named `BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`, `SOLUSDT_4h.csv`** —
   the check B14 earned. They were 181 lines each on 2026-07-29 night.

**Four of four or it has not cleared, and "three of four with a good
explanation" is the phrasing this ship exists to refuse.**

---

# PART 1 — THE NINTH REPAIR (R-020). **UNTOUCHED THROUGH TWO SESSIONS.**

`python data\open_interest.py` — fourteen sabotages, check (c), sections (l)
and (m). **That is the claim under review, not the verdict.**

**Where this gate is STRONGEST — so do NOT spend your time here:** it holds its
own `GATE_CSV_SUFFIX` and every check locates files with `_gate_csv_path`; a
named check prints the module's filenames beside the gate's own; the folder is
pinned by `_record_does_the_job` and has held twice; both ends of the printed
window are compared to a fetch the gate makes itself; rows the source no longer
serves are seeded and required to survive byte for byte; the printed counts are
compared to rows the gate counts itself; an unparseable report line is a FAILURE
not a skip; every loop runs over `GATE_SYMBOLS`; `--record` is driven for real
as a subprocess in both outcomes.

## THE FIVE DOUBTS ITS AUTHOR FILED AGAINST IT — free hits, still untested

1. **HE FIXED THE ADDRESS OF ONE FILE AND SWEPT FOR NO OTHERS.** The whole
   finding was that this ship applies R-014's lesson to VALUES and never to
   ADDRESSES — **and then he fixed exactly the one address he had attacked.**
   `cockpit/funding.py` and `cockpit/fear_greed.py` were never examined for the
   same class. **THIS IS STILL THE STRONGEST LEAD IN THE BUILDING** — and note
   that last night's work added a NEW address to both of them, `_REPO_ROOT`,
   **derived from `__file__`.** See R-022 doubt 3.
2. **THE GATE'S ADDRESS IS A HARDCODED `'_4h.csv'`.** A legitimate change of
   `PERIOD` fails this gate loudly and **the obvious move will be to edit the
   gate to match** — R-001's conviction, one string worse.
3. **THE REFUSES-TO-RUN BRANCH SKIPS THIRTEEN OF FOURTEEN SECTIONS** when the
   name check fails. The author *believes* that is right.
4. **B14 IS JUDGED IN THE DRILL BY ONE JUDGE.**
5. **THE RUNTIME WAS NEVER MEASURED.** **Partly answered: the FUNDING gate is
   ~130 seconds. The recorder's own runtime is still unmeasured**, and R-013's
   4h-boundary exposure is still unwatched.

---

# PART 2 — THE TENTH REPAIR (R-022). **BUILT LAST NIGHT, NEVER ATTACKED.**

`python cockpit\funding.py` and `python cockpit\fear_greed.py`.

**Where this repair is strongest — so do NOT spend your time here:** the ear
listens at the descriptor and compares raw BYTES; it is proved to hear down all
three routes before its silence is believed; the streams are proved untampered;
the descriptors are proved given back; the new judges are proved to RETURN False
rather than raise; the import check runs a fresh interpreter, proves it imported
the file the gate MEANT, proves it did not re-enter the gate, and drives its
sabotage by a real binary-mode edit outside the repo with a uniqueness guard.

## THE SEVEN DOUBTS ITS AUTHOR FILED AGAINST HIS OWN WORK

1. **THREE ROUTES WERE PROVED AND THERE MAY BE A FOURTH.** `print`,
   `os.write(1, …)` and a `logging` handler are the three he thought of. **He
   closed the doors he found — exactly the mistake doubt 1 of R-020 describes.**
   What about a C extension writing to the CRT handle, a `subprocess` the
   doorway spawns that inherits the descriptors, or **a thread that writes AFTER
   `_capture` has restored them?** **He names the last as the strongest lead and
   did not test it.**
2. **THE IMPORT CHECK IMPORTS THE MODULE, NOT THE BRIEF.** It proves
   `cockpit.funding` is silent alone. `brief.py` imports pandas, pandas_ta and
   five repo modules first — **and a `pandas_ta` UserWarning is ALREADY printing
   on the real Brief's first line, measured.** Nothing checks the Brief's own
   import surface. **This is the same class of hole one level up and it is not
   hypothetical.** *(It is NOT the brief.py gate the Commander deferred — do not
   confuse the two, and do not build that gate.)*
3. **`_REPO_ROOT` IS DERIVED FROM `__file__`** — an ADDRESS taken from the file
   being judged, **which is precisely B14.** He believes it unavoidable, and
   "I believe" is what this ship files rather than trusts.
4. **THE DESCRIPTOR-RESTORATION CHECK USES `os.fstat(fd)[:4]` ON WINDOWS**,
   where `st_ino` is often 0. **It was never made to fail on purpose.**
5. **S18/F17 IS JUDGED BY ONE JUDGE** — nothing else can see an import-time
   write.
6. **THE SILENCE CHECK RUNS ONLY THE PATHS THE GATE THINKS EXIST.**
7. **THE GATE NOW TAKES ~130 SECONDS AND SPAWNS SUBPROCESSES.** A gate nobody
   runs is a gate that is not guarding anything.

## STILL KNOWN-WEAK ACROSS THE SHIP — named so you do not have to find them

1. **FUNDING'S TWO-ASSETS-FAIL BLOCK IS GUARDED BY NOTHING.** `_partial_checks`
   breaks exactly ONE asset at a time. **Named in seven sets of orders now.**
2. **THE RECORDER'S CHECK (e) IS STILL BTCUSDT-ONLY.**
3. **B1 IS STILL A NO-OP ON A MACHINE SET TO UTC.**
4. **`_raw_truth` STILL READS `FAPI_BASE`, `HIST_PATH`, `PERIOD`, `LIMIT` AND
   `TIMEOUT` FROM THE MODULE IT JUDGES.** R-015 doubt 1, still open.
5. **`cockpit/brief.py` STILL HAS NO GATE** — **he has ruled: NOT NOW, BEFORE
   GOING LIVE. Do not build it and do not re-argue it.**
6. **NOTHING CHECKS THAT A GATE'S DESCRIPTION MATCHES WHAT IT DOES.** Section
   (h) announced "ELEVEN ways" while running thirteen. **R-011's third doubt,
   still unguarded** — and last night three gate headlines were hand-edited to
   new sabotage counts, **by hand, with nothing checking them.**

## IDEAS TO GET YOU STARTED — find your own, these are not the assignment

    - doubt 1's thread: the ear restores the descriptors and THEN reads the
      capture file. What writes in that gap?
    - `_capture` flushes `sys.stdout` before swapping. What if the doorway
      leaves something in a buffer that flushes LATER, after restoration?
    - the import check passes a probe PATH as argv. What if the module the
      child imports is not the one the gate believes — a stale
      `__pycache__`, a name shadowed on `sys.path`?
    - the drill deletes its scratch tree in `finally`. What if a check
      leaves a file behind that a LATER check then reads?
    - R-020's doubt 1 applied to last night's work: **what OTHER addresses
      did the two Context Deck gates acquire?**

---

# THE 1 AUGUST ERRAND — **CHECK TODAY'S DATE FIRST.**

**Three sets of orders have now got this wrong in one direction or the other.**
**On 2026-07-29 it was NOT due.** Check the date before you act on this section.

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
    MEASURED 2026-07-29 night: data/oi_history/ holds exactly THREE files,
    correctly named, 181 lines each, sha256 46094fc3…

**WRITE DOWN WHAT YOU EXPECT BEFORE YOU READ THE LOG. The honest figure on
1 August is roughly THIRTY new rows per asset and a stored count near 210** —
not 180, and not 360. **If the log says something you did not predict, that is a
finding, not a relief.**

**AND THE SECOND THING, EARNED BY B14: look at `data/oi_history/` itself and
confirm there are THREE files named `BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`,
`SOLUSDT_4h.csv`.** A fourth file, or a different name, is B14 arriving for real.

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

**And the trick that proved B13 and B14: seed a scratch folder with a
byte-for-byte copy of the REAL archive, put the module beside it, and run
`python open_interest.py --record`.** That is exactly what the monthly task does,
and it is the only rig that shows what the Commander will actually see.

**AND THE TRICK THAT PROVED BOTH DOORS LAST NIGHT: copy the module's OWN
`_capture` out into a scratch script and feed it a control first.** The control
is what turns "it returned nothing" into "it is deaf" instead of "it is silent".

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
`git show --stat` proves the bar preceded the work. **Fifteen uses of this
pattern, and it has survived audit every time.** Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove
    it two ways, do not assert it:** every diff hunk at or after the `__main__`
    line (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a
    sha256 of the production half before and after, printed side by side.
    **Last night's values: funding `95069d1b…`, fear_greed `bb31626c…`.**
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself, the
    gate never reads a constant belonging to the file it is judging, and THE
    GATE NEVER ASKS THE MODULE WHERE TO LOOK.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others,
    caught every run, originals restored and the restoration verified.
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT, **and must be shown to fail
    for the reason it claims, not incidentally.** **And prove your new
    sabotage's judge returns False rather than raising.**
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed".**

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the
actual output, and the verdict — **including if it is all clean.**

**`REVIEW_QUEUE.md`: you MAY clear R-020 and R-022 (you built neither), and
R-007 too if it settles.** R-001 has now waited through **nine FAILED
generations of repair, with the tenth untested**, and **moves only when a
generation survives an independent attack. Untested is not survived.** Items you
cannot settle stay OPEN with a note on what is missing; **leaving something open
is a legitimate recorded outcome.** **R-006 is not yours, ever. Never delete an
item. Never edit a cleared verdict.**

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

1. **R-016 IS DONE — TAKEN OFF HIS DESK.** He gave the order three times and it
   is carried out. **It is not CLEARED; that is R-022, and it is a session's
   job, not his.**
2. **THE FUNDING GATE GOES RED NEAR A FUNDING SETTLEMENT (R-021).** He should
   know his ship has a test that cries wolf in the ~45 minutes around 00:00,
   08:00 and 16:00 UTC, that it did so before last night too — **proved by
   running the untouched previous version side by side** — and that it was
   deliberately NOT repaired because the rules say a SMALL finding gets filed,
   not fixed. **He can overrule that in one word.** **He is the reason this is
   stated correctly: he asked why it had passed in earlier sessions, and the
   session had claimed it without measuring.**
3. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL
   NEW ROWS.** The errand above. **Due 1 August.**
4. **`cockpit/brief.py` HAS NO GATE — and he has ruled: NOT NOW, BEFORE GOING
   LIVE.** Recorded in `EXECUTION_PLAN.md` as a standing requirement. **Do not
   build it, and do not re-argue it.**
5. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
6. **The risk-doctrine decision** — the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never after
   seeing results.**
7. **`MAX_PLAUSIBLE_RATE`** — measured at 13-16x looser than Binance's published
   cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
8. **The settled-rate anchor (R-004)** — returned to him on correct facts.
9. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. He can reverse it
   in one word.
10. **A DOCUMENT-INTEGRITY CHECK.** Nothing on this ship checks that its own
   documents are not corrupted. Found by a human looking, twice. **A one-line
   scan would close it. Recommended, not adopted.**
11. **TWELVE law candidates, none adopted, all his call:**
   - *"A session may not certify its own work; anything it cannot certify is
     filed in `REVIEW_QUEUE.md` before the commit that ships it, and only an
     independent reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."*
   - *"A check is not proven until it has been deliberately broken."*
     **Seventeen working implementations and still not law.**
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
   - *"A gate must be shown to BUILD the situations it claims to judge."*
   - *"A gate must hold its own ADDRESS as well as its own expectations. It may
     not ask the file it is judging where that file put its work."*
   - **NEWEST, earned 2026-07-29 (night):** *"A check that reports the ABSENCE
     of something must first be proved able to detect its PRESENCE. A listener
     that cannot hear reports silence, and silence is what a passing gate looks
     like."* **Earned by R-016: for two of three routes the silence check was
     deaf, and printed three green ticks reading "the doorway wrote NOTHING"
     directly underneath the advice it had just failed to hear.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.** Information
instruments can carry a lighter guard. The gauntlet cannot. **NINE sessions in a
row found something; the tenth did not look, because it was ordered to build.
That is a legitimate exception the Commander made once, in writing — but it
means TWO repairs are now waiting for a first pair of eyes instead of one, and
the substitute only works if somebody actually attacks.**
