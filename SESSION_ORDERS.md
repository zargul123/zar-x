# ZAR X PHASE 3 — **DOOR 3 IS BUILT. ATTACK IT, THEN BUILD INSTRUMENT 3. AND THE 1 AUGUST ERRAND IS DUE TODAY.**

*Written 2026-07-31 by the thirteenth generation — the session that arrived to a
RED ship, put the collision to the Commander, repaired F10 on his ruling, and
**built DOOR 3 in both cockpit files after it had been deferred seven times.**
I may not clear my own repair. That is your Part 1. **And for the first time in
eight sessions, nothing is standing in front of Context Deck instrument 3.***

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is exact bars and commands. This part is the story, so
you know WHY before you read WHAT. The Commander is not a programmer and asked
for it in this form. Write your report to him the same way.*

## Where the ship is

    cockpit/funding.py      GATE 3.2-R7  PASSED  exit 0  0 red  122 s
    cockpit/fear_greed.py   GATE 3.1-R7  PASSED  exit 0  0 red   62 s
    data/open_interest.py   GATE 3.2b-R9 PASSED  exit 0  0 red   56 s
    vault INTACT 6/6 · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 181 lines each, sha256 e3258e82… / 1549a8a1… /
                      e0f91a87… — byte-identical since 2026-07-30

## What happened, in three paragraphs

**THE SHIP WAS RED WHEN I ARRIVED AND NOBODY HAD BROKEN ANYTHING.** Sabotage F10
swaps yesterday's Fear & Greed number with the one from a week ago. **Both were
28.** Swapping 28 with 28 changes nothing, so the drill looked at the unchanged
output and reported that its own lie had escaped. **Measured against the index's
whole 3,099-day history, that happens on 6.05% of days — one in every 16.5.**
The instrument and the Brief were correct the whole time.

**THAT COLLIDED WITH THE DOOR 3 ORDER AND ONLY THE COMMANDER COULD SETTLE IT.**
Door 3 goes into `fear_greed.py`, and a failing gate is never committed. I graded
F10 SMALL, said so, and gave him three options. **He ruled: fix F10 first, then
build Door 3 in both.** So I repaired something I had myself graded SMALL —
**a rule bent on his word, not on mine.**

**THEN I ATTACKED THE RECORDER WITH THE QUESTION F10 HANDED ME, AND FOUND THE
SAME DISEASE IN A SECOND FILE.** `B1` is a **no-op on any machine whose clock is
UTC**. I changed no file at all — **the sabotage is the environment.** Control
passed in the same tree; only the clock changed; the gate went red and called
B1 escaped. **This ship predicted it on 2026-07-28 (R-013 doubt 4) and left it
for three sessions.**

## **THE ONE THING I MOST WANT YOU TO SEE, AND IT IS NOT THE FINDING**

In the SAME failing run the recorder's gate printed **both** of these:

    ✓ B1  rebinds '_utc_iso'  → … so the swap reaches the code the pilot runs
    ✗ B1  timestamps converted as LOCAL time → ESCAPED

**Both statements are true.** The swap really does reach the recorder. **It just
changes nothing when it gets there.** The eleventh and twelfth generations each
spent a whole session hardening that reachability claim. **A sabotage can
satisfy it completely and still be inert — and nothing on this ship has ever
measured EFFECT as opposed to REACH.**

## **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

**`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT. R-021,
CATEGORY B, SMALL.** Binance settles at **00:00, 08:00 and 16:00 UTC**. I ran it
at 09:42 and again at 10:15 UTC — 1h42m and 2h15m past 08:00 — and it passed
first time on both.

**>>> OUTSIDE A SETTLEMENT WINDOW, A RED FUNDING GATE IS A REAL FAILURE. TREAT
IT AS ONE.** Check the clock, run it again, and say how many runs it took.

**AND IF `cockpit\fear_greed.py` GOES RED ON F10 AGAIN, THAT IS A REGRESSION OF
MY REPAIR AND IT IS SERIOUS** — it cannot happen unless someone undid it.

## **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT. HIS ORDER IS CARRIED OUT. Do not re-open R-025** — but do
   not clear it either; see below.
5. **HE RULED ON 2026-07-31 that F10 was to be repaired before Door 3.** Done.

## Your job, in order

**1. ATTACK DOOR 3 (R-032). IT IS UNATTACKED AND I BUILT IT.** Ten doubts filed
against my own work — starting points, **not** the assignment.

**2. BUILD CONTEXT DECK INSTRUMENT 3 OF 5 — news headlines.** `EXECUTION_PLAN.md`
Phase 3 step 3. **It has been deferred SEVEN times and for the first time in
eight sessions nothing is in front of it.** CryptoPanic free tier, **HEADLINES
ONLY, no sentiment score, no invented weights, the cut ghost stays cut.**

**3. THE 1 AUGUST ERRAND — IT IS DUE TODAY. CHECK THE DATE FIRST ANYWAY.**
Details below. **Seven sets of orders have now got this wrong in one direction
or the other; I got it right by checking, which cost one command.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here. I did NOT edit it** — see the desk, item 1, for the lesson
I think it has now earned twice, which is his call and not mine.

**Specific to THIS job:**

1. **The LAST TWO entries of `PROGRESS_LOG.md`** — my declaration and my
   results. **Read them as a CLAIM, not a result.** The file is ~490 KB; reading
   all of it will eat your budget.
2. **`cockpit/funding.py` and `cockpit/fear_greed.py`, the `__main__` half
   only** — `_door3_probe`, `_door3_writes_nothing`, `GATE_DOOR3_SHAPES` and
   `_door3_drill` in both; plus `_f10_transpose` and `_f10_both_branches_fire`
   in `fear_greed.py`.
3. **`REVIEW_QUEUE.md` — R-032 is your worklist**, plus R-029/R-030/R-031 if you
   have room. **R-006 may NEVER be cleared by you or any in-house session.**
4. **`ROADMAP.md`** — the MEASURED facts table. If anything you measure disagrees
   with it, **your measurement wins and you write the correction down.** I had to
   do it for three runtimes and for the sha256 recipe.

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A new sabotage, invented by you, thrown at **DOOR 3 (R-032)**, result recorded
   either way.
2. **THE SWEEP NOBODY HAS DONE, and it is the highest-value thing on this list:**
   two files have now been caught carrying a sabotage that is inert under some
   reachable condition (F10, B1). **Nobody has swept the third.** Go through
   `funding.py`'s eighteen sabotages and ask of each: *is there a data or
   environment condition under which this changes nothing?* Recorded either way.
3. Any leak graded on THE FINDING REPORT **before** any repair, using **the
   Commander's wording of Step 2.2 and his three questions**, and repaired only
   if that grade says to.
4. `lab/` byte-identical, vault INTACT 6/6, Brief 3/3, and **exactly THREE files
   in `data/oi_history/`** named `BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`,
   `SOLUSDT_4h.csv`. **A fourth file, or a different name, is B14 arriving for
   real.** After the 1 August run they should be **~211 lines each, NOT 181** —
   see the errand.

**Four of four or it has not cleared, and "three of four with a good
explanation" is the phrasing this ship exists to refuse.**

---

# PART 1 — MY DOOR 3 (R-032). **NEVER ATTACKED.**

**What it does, in one sentence:** a fresh interpreter imports the module, calls
`section_text()` on every path the pilot can see, throws away what it returns,
and **then shuts down** — and the child's TOTAL output must be empty bytes.

**Why that catches things the old ear could not:** interpreter shutdown **joins
non-daemon threads, flushes every buffer and runs every atexit handler.** The old
ear gave the descriptors back the instant the doorway returned, so all three of
those shapes wrote to the pilot's screen completely unwatched.

**Where this build is strongest — do NOT spend your time here:** each of the
three shapes is planted **alone**, in a real binary-mode edit of a copy outside
the repo, and each must be caught **by its own marker** — so a patch that merely
crashed cannot be scored a success; the untouched control runs first in the same
scratch tree and the rig is declared broken if it is not silent; the anchor must
match exactly once or the drill refuses to run; **and A4 hangs the child on
purpose and the door is required to call that a FAILURE**, which is the exact
trap R-025 named.

## THE TEN DOUBTS I FILED AGAINST MY OWN WORK — free hits

Read them in `REVIEW_QUEUE.md` under **R-032**. The three I would attack first:

- **DOUBT 1 — DOOR 3 INHERITS R-022 DOUBT 6 WHOLE.** It calls **the paths the
  GATE names.** A doorway path nobody told it about is a path it does not watch.
  **I answered doubt 6 for today's source and then built something that depends
  on it staying answered. This is the most dangerous line in my diff.**
- **DOUBT 2 — THE CHILD IS JUDGED ON `stdout + stderr` OF A PIPE.** A shape that
  writes to the real console device, or to descriptor 3, or that re-opens
  `CONOUT$`, is invisible to it. **I planted none of those and I do not know the
  answer.**
- **DOUBT 3 — A2 MAY BE PASSING FOR A REASON I DID NOT VERIFY.** The child calls
  the doorway 2-3 times, so the earlier wrappers are rebound and garbage-collected
  — possibly flushing EARLY rather than at shutdown. **The marker comes back
  either way, so my check cannot tell the two mechanisms apart, and my comment
  claims the shutdown one.**

---

# **PART 2 — CONTEXT DECK INSTRUMENT 3 OF 5: NEWS HEADLINES. NOTHING IS IN FRONT OF IT ANY MORE.**

**`EXECUTION_PLAN.md` Phase 3, step 3. Deferred SEVEN times.** Every previous
deferral was a real finding that outranked it. **There is no such finding
outstanding today** — everything I found is CATEGORY B and the Commander's own
three questions say CATEGORY B does not stop the building.

**WHAT IT IS:** CryptoPanic free tier. **HEADLINES ONLY.** No sentiment score,
no invented weights, **the cut ghost stays cut.** It joins the existing Context
Deck the way funding does — one deck, no header of its own.

**BUILD IT THE WAY EVERYTHING HERE IS BUILT:**
- **Declare the gate and commit it ALONE with no `.py` in that commit.**
- Name the awkward edge cases **before** writing code.
- **A sabotage drill from birth** — not added later.
- **AND, EARNED TWICE TODAY: every sabotage you write must be proved able to
  CHANGE THE OUTPUT before its verdict means anything.** Do not ship a drill
  whose lies the data can silence. **You are the first session that gets to
  build this in from the start rather than discover it.**
- **DOOR 1, DOOR 2 AND DOOR 3 FROM BIRTH.** The machinery exists in both cockpit
  files and can be copied: the descriptor-level ear that must prove it can hear,
  the fresh-interpreter import check, and Door 3. **A new instrument without all
  three doors is a new hole, and the last two were retrofitted at the cost of
  four sessions.**

**IF YOU ARE RUNNING SHORT, DO PART 1 PROPERLY AND LEAVE PART 2 ENTIRELY.** A
half-built part is worse than no part.

## HOW TO ATTACK PROPERLY

- **BRING A NEW QUESTION. ELEVEN ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* · *"What is the gate's own detector deaf
  to?"* · *"What shape does the real world have that the gate's world cannot?"* ·
  *"What if the module puts its work somewhere the gate is not looking?"* ·
  *"What happens BEFORE the gate is alive to watch?"* · *"Is the sabotage
  actually IN EFFECT when the judge runs?"* · *"WHEN does the gate stop watching,
  and what does the part do after that?"* · *"WHOSE CODE does the swap reach?"* ·
  **and now mine:** *"CAN THE SABOTAGE ACTUALLY EXPRESS THE LIE IT CLAIMS TO
  TELL, OR DOES THE DATA MAKE IT A NO-OP?"* **All eleven are the directions
  these gates are now strongest in, and reusing any of them is the approach most
  likely to find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** I wrote
  four predictions: **three were right and the fourth was wrong in a way worth
  copying** — I attached a severity claim to it that my own form does not
  support, and I recorded that as an error rather than quietly dropping it.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; it costs nothing
  (27 MB). Check `git status` is clean when you are done.
- **THE BEST ATTACK I MADE TODAY EDITED NO FILE AT ALL.** I changed the clock
  (`TZ=UTC0`) and the gate went red. **Windows Python honours `TZ` — measured.**
  Ask what else about the ENVIRONMENT the gate silently depends on.
- **EDIT IN BINARY, OR IN TEXT DECODED FROM BINARY — NEVER THROUGH PYTHON'S
  NEWLINE TRANSLATION.** These `.py` files are CRLF and **so are all five
  documents** — `PROGRESS_LOG.md` is 8,831 CRLF and zero bare LF. **I asserted it
  was LF and was wrong; my first check read the file with newline translation on
  and counted zero CRLFs in a file that is nothing but.** An assertion caught it.
- **EMIT PAYLOADS AND ANCHORS WITH `repr()`, NEVER BY HAND-ESCAPING.** Two levels
  of escaping is how the twelfth generation wrote a whole patch that matched zero
  times. `repr()` cannot make that mistake.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **That guard caught me too:** I ordered a rename after inserting a block that
  QUOTED the old name, so it matched twice and the script wrote nothing. **It has
  now caught three consecutive sessions and has never once been wrong.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** `f"{x.count(b'\n')}"` will not compile. **The last two sets of
  orders warned about this in bold and both sessions did it anyway. So did I.**
  Name the value first. Run `py_compile` before the gate.
- **Run the untouched control FIRST — and run it inside the scratch copy too.**
- **A GREEN GATE IS NOT THE EVIDENCE. PRINT THE DAMAGE.** **A sabotage that
  CRASHES is scored "caught", so one that never really ran looks like a success.**

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item. **DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.**

**You may clear R-032, R-029, R-030 and R-031** — you built none of them. **You
may NEVER clear R-006.** **And if you fix something, you may not clear your own
fix.**

**>>> R-025 IS A TRAP AND I WALKED UP TO IT: my orders said I could clear it, and
I refused, because by the time I read that permission I had been ordered to BUILD
its repair.** **You did not build Door 3, so R-025 is genuinely yours to judge** —
but judge it by attacking Door 3, not by reading my report.

**R-001 has now waited through THIRTEEN generations of repair, TWELVE of which
were failed by the next pair of eyes and the thirteenth — mine — untested.** It
**moves only when a generation survives an independent attack. Untested is not
survived.**

---

# THE 1 AUGUST ERRAND — **IT IS DUE TODAY. CHECK THE DATE ANYWAY.**

**On 2026-07-31 it was NOT yet due and I said so and moved on.** If you are
reading this on 1 August or later, **it has fired and you must read the result.**

**WRITE DOWN WHAT YOU EXPECT BEFORE YOU OPEN THE LOG.**

    MEASURED, so you do not re-derive it:
    The recorder has run EXACTLY ONCE in its whole history — by hand, on
    2026-07-27 — and it appended ZERO rows. THE COMMIT-AND-PUSH BRANCH HAS
    THEREFORE STILL NEVER FIRED FOR REAL.
    A healthy run appends 12 rows per asset and reports 192 stored (measured
    2026-07-29 against a copy of the real archive).
    The honest figure on 1 August is roughly THIRTY new rows per asset and a
    stored count near 210 — NOT 180, and NOT 360.
    The archive stood at 181 lines per file (180 rows + header) all through
    2026-07-31, sha256 e3258e82… / 1549a8a1… / e0f91a87…

**Open `journal/daily_runs.log` and tell the Commander PLAINLY whether the task
actually committed and pushed real new rows.** **If the log says something you
did not predict, that is a finding, not a relief.**

**AND THE SECOND THING, EARNED BY B14: look at `data/oi_history/` itself and
confirm there are THREE files, correctly named.** A fourth file, or a different
name, is B14 arriving for real.

**Do not assume it worked because the task returned 0** — `schtasks` already
reported SUCCESS once for a task that could never run at all. **Read the file and
count the rows yourself** — and note that `count('\n') + 1` overcounts a file
ending in a newline, which is how I briefly told myself the archive had grown.

---

# IF ANYTHING LEAKS: GRADE IT FIRST, THEN REPAIR UNDER A GATE DECLARED FIRST

**FILL IN THE FINDING REPORT BEFORE YOU REPAIR ANYTHING** — the Commander's
three questions first, then the four steps, in `THE_PATTERN.md`. **Step 2.2
carries his own wording — read it there, not here.** Then:

    SERIOUS ....... fix it, and stop. Build nothing.
    BORDERLINE .... do NOT fix it. Report and stop. The Commander rules.
    SMALL ......... do NOT fix it. File it in REVIEW_QUEUE.md as CATEGORY B
                    and carry on.

**If you do repair: DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY
ALONE, WITH NO `.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then
`git show --stat` proves the bar preceded the work. **Nineteen uses of this
pattern and it has survived audit every time.**

**AND RECORD THAT HASH *AFTER* YOUR FINAL PUSH, NOT WHEN YOU WRITE THE ENTRY.**
The cloud watchman pushes every four hours, so `git pull --rebase` before your
push can rewrite your own commit hashes underneath you. Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, do not assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a sha256
    of the production half before and after, printed side by side.
    **>>> THE RECIPE ON RECORD WAS WRONG FOR TWO OF THE THREE FILES AND I HAD TO
    FIND IT BY EXPERIMENT, WHICH THE ORDERS PROMISED I WOULD NOT HAVE TO. HERE IT
    IS CORRECTLY, PER FILE:**
    - `cockpit/funding.py` and `cockpit/fear_greed.py`: **the raw byte prefix up
      to the `if __name__ == '__main__':` marker** (i.e. the first N-1 lines
      joined by CRLF **WITH** a trailing CRLF) → `95069d1b…` and `bb31626c…`.
    - `data/open_interest.py`: the first N-1 lines joined by CRLF with **NO**
      trailing separator → `5347bfec…`.
    - **`open_interest.py` reproducing `5347bfec…` exactly is what proves your
      script is right. Check that one first, then trust the other two.**
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself, the gate
    never reads a constant belonging to the file it is judging, and THE GATE
    NEVER ASKS THE MODULE WHERE TO LOOK.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others, caught
    every run, originals restored and the restoration verified. **And check your
    new break is actually IN EFFECT, and actually CHANGES SOMETHING, when its
    judge runs.**
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT, **and must be shown to fail for
    the reason it claims, not incidentally.**
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**
(g) **RUN `py_compile` BEFORE THE GATE.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

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

1. **>>> THE ONE I MOST WANT HIM TO RULE ON, AND IT IS EARNED TWICE IN ONE DAY BY
   TWO DIFFERENT FILES.** A pattern amendment, proposed and **NOT** adopted,
   because a session may never promote its own idea:
   *"A SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS
   ANYTHING."* **F10 and B1 are the same fault in two files: a lie the data can
   silence, reported as a gate that failed.** The ship already has the mirror
   rule for detectors — *a check that reports ABSENCE must be proved able to
   detect PRESENCE.* **This is that rule pointing at the drill instead of the
   detector, and it is the only candidate on the list earned twice in a single
   day.** **THIRTEEN OTHER CANDIDATES REMAIN UNADOPTED AND ALL ARE HIS CALL.**
2. **DOOR 3 IS BUILT AND THE HOLE IS SHUT — AND HE IS OWED THE RESULT IN PLAIN
   WORDS, WHICH THE LAST ORDERS SPECIFICALLY ASKED FOR.** Not "a gate went
   green": **the doorway is now watched after it has answered, a thread that
   sleeps past the end of the run cannot write on his Brief any more, and the
   one way to build this wrong — treating a hang as silence — is itself tested
   on every run.**
3. **HE PERSONALLY UNBLOCKED THIS SESSION.** The F10 collision would have cost
   an eighth deferral of Door 3. **He ruled in one word and the order got
   carried out the same day.** Worth him knowing the mechanism worked.
4. **THE CATEGORY B PILE IS NINE DEEP**, up from six in one session (R-029,
   R-030, R-031 added). **It is cleared before the ship is used for real, at the
   same moment `brief.py` gets its gate.** Said out loud, as the condition on
   which the category was granted.
5. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
6. **AND THE ONE I WOULD MOST LIKE HIM TO SAY YES TO, INHERITED AND STILL TRUE:
   FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this entire class is `symbols=None`, resolved in the body — and `funding.py`
   already does it that way.** It touches what the pilot reads, so no session may
   make it during a repair to a test. **Eight generations have now fixed the
   instance and left the pattern.**
7. **THE FUNDING GATE GOES RED NEAR A SETTLEMENT (R-021).** SMALL, unrepaired.
   Two clean runs today at +1h42m and +2h15m.
8. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL
   NEW ROWS. THE ERRAND IS DUE TODAY.**
9. **`cockpit/brief.py` HAS NO GATE** — he has ruled: not now, before going live.
10. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
11. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
12. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
13. **The settled-rate anchor (R-004)** — returned to him on correct facts.
14. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
15. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED FIVE TIMES, NOT ADOPTED.** I ran
    the mojibake scan by hand before every commit again. **A one-line scan would
    close this and it has been asked for five sessions running.**
16. **BOTH GATES ARE NOW SLOWER BECAUSE OF ME** — funding 88 s → 122 s,
    fear_greed 34 s → 62 s, because Door 3 spawns six child processes per run.
    **R-022 doubt 7 says a gate nobody runs is a gate that is not guarding
    anything.** Filed as R-032 doubt 5. **If he ever finds these too slow to run,
    that is a real cost and he should say so.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.** **Thirteen generations, twelve of them failed by the next pair of eyes,
and the thirteenth is sitting in front of you untested — that is what the
substitute is worth, and it only works if somebody actually attacks.**
