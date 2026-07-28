# ZAR X PHASE 3 — **ATTACK THE SIXTH REPAIR, THEN BUILD STEP 3.3.** Six generations of gate have now each been failed by the next pair of eyes

*Written 2026-07-28 (night) by the session that invented three new sabotages,
watched all three walk through three green gates, then repaired all three and
graded its own repair. **Stated before anything else: one mind found the three
holes, wrote every fix, and declared them all passed.** Thirty-nine sabotages now
live in three files and **all thirty-nine were invented by the sessions that then
defended against them.** You are the first pair of eyes that built none of it.*

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is the exact bars and commands. This part is the story, so
you understand WHY before you read WHAT. The Commander is not a programmer and
asked for it in this form. Write your own report to him the same way.*

## Where the ship is

Three parts break themselves on purpose every time they run and refuse to pass if
any breakage goes unnoticed. **Thirty-nine deliberate lies live in the code; all
thirty-nine are caught.**

That sounds like strength. **Read it again: every one of the thirty-nine was
invented by the same session that then defended against it.** Nobody outside has
ever attacked them.

## What happened just before you

**Six sessions in a row have each found real holes in the work of the session
before.** 48/48 with four lies walking through. Then five more. Then seven more.
Then four more. Then four more again. **Then, last night, three more — and these
were a different shape from all of them.**

Every gate on this ship had been made very good at one job: checking that the
*words a part hands back* are true. Last night's session asked a different
question — **not "is the answer right?" but "is the gate even looking at the
right thing?"** It was not.

- **The funding instrument and the Fear & Greed instrument each got one extra
  line of code that simply PRINTS a trade instruction to the screen** — *"close
  longs before the 16:00 settlement"*, *"historically a buying opportunity"* —
  while handing back exactly the same honest text as always. The Morning Brief
  runs those parts and then prints what they hand back, so **the instruction
  lands on the Commander's screen.** Every check looks only at the handed-back
  text. **It printed thirty times on the gate's own screen and the gate said
  PASSED.** On a ship whose founding rule is INFORMATION, NEVER A SIGNAL.
- **The recorder writes a file once a month. It ADDS to a file that is already
  there.** Every check in its gate builds a brand-new empty folder first — so
  **the gate had only ever tested the very first month, and the first month
  happens once.** A defect that only shows up when adding to an existing file was
  invisible. Built by hand: **80 of 180 rows landed on disk 64,763 times too
  large**, and the gate reported all nine sabotages caught — **including the one
  that is that exact same lie, just on the other path.**

**The lesson, in one line: A GATE CAN BE PERFECTLY HONEST ABOUT THE WRONG
OBJECT.**

## Your job, in order

**1. ATTACK LAST NIGHT'S REPAIR (R-015).** It closed three holes and was written
and graded by one mind. **Report either way.**

**2. THEN, ONLY IF PART 1 IS CLEAN, BUILD STEP 3.3** — the third Context Deck
instrument. **If Part 1 finds anything real, fix that and stop.** Six sessions
running have found something; do not assume you will be the seventh, and do not
assume you will not be.

**3. AND ONE ERRAND THAT IS NOW DUE.** After 1 August, open
`journal/daily_runs.log` and tell the Commander **plainly** whether the monthly
recorder task actually committed and pushed real new rows. **That branch has
never fired.** Do not assume it worked because the task returned 0 — `schtasks`
already reported SUCCESS once for a task that could not run at all.
**AND NOTE WHAT IS NEW: 1 August is the first time the recorder will EVER take
the append path for real.** That is precisely the path last night proved had
never been checked. Read the file and count the rows yourself.

## How to attack properly

- **BRING A NEW QUESTION. THREE ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* **All three are now the directions these
  gates are strongest in, and reusing any of them is the approach most likely to
  find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** Each of
  the last three sessions predicted EVERY ONE of its attacks correctly before
  running anything, and that is what proved the holes were structural rather than
  luck. It also makes it impossible to reinterpret a result after seeing it.
- **Work on copies OUTSIDE the repo.** Never break the real files. Check
  `git status` is clean when you are done.
- **Run the untouched control first.** If the healthy copy does not pass, your rig
  is broken and nothing you conclude means anything.
- **Watch your own test. A sabotage that CRASHES is scored "caught"**, so one that
  never really ran looks like a success. **PRINT what your broken version produces
  and confirm it is visibly wrong before you believe any verdict.** Last night's
  B10 was only believed because month two was built by hand and the 80 wrong rows
  were printed beside what Binance actually served. **A green gate is not evidence
  your sabotage fired.**
- **If your text anchor matches more than once, REFUSE TO RUN** rather than
  editing the first match. **This stopped last night's session twice**, once
  because `now = readings[0]` appears in both halves of `fear_greed.py`.

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item.

**DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.** After six sessions that each
found something, the pull to also find something is real and it is a trap. **This
ship still has not seen a clean review and it needs one eventually.**

**You may clear R-015** — you built none of it. **You may never clear R-006.**
**And if you fix something, you may not clear your own fix.**

## What is his, not yours

Do not decide these by default and do not let them drop: the risk-doctrine
decision, tightening `MAX_PLAUSIBLE_RATE`, the TwelveData key, the
document-integrity check, and the **eight** law candidates. They are listed at the
bottom. **A session does not promote its own idea to law.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment, and the housekeeping that has bitten this ship. None of it is
repeated here.** If you have not read it, stop and read it.

**Specific to THIS job:**

1. **The last TWO entries of `PROGRESS_LOG.md`** — the three-sabotage review and
   the repair. **Read them as CLAIMS, not results. They are what you are
   auditing.** The file is ~270 KB; reading all of it will eat the budget you
   need for the actual work.
2. **`cockpit/funding.py`, `cockpit/fear_greed.py`, `data/open_interest.py`** —
   the `__main__` blocks are where every change landed. The production halves are
   provably byte-identical to yesterday's, by sha256.
3. **`REVIEW_QUEUE.md` — R-015 is your worklist**, and its four recorded doubts
   are starting points, **not the assignment**. R-007 may also be settled by you
   and **was not touched last night.** **R-006 may NEVER be cleared by you or any
   in-house session.**
4. **`ROADMAP.md`** — the MEASURED data-source facts table. If anything you
   measure disagrees with it, **your measurement wins and you write the
   correction down.**

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A **SIXTEENTH** sabotage, invented by you, thrown at Gate 3.2-R5 (funding),
   result recorded either way.
2. A **FIFTEENTH** against Gate 3.1-R5 (Fear & Greed).
3. An **ELEVENTH** against Gate 3.2b-R3 (the open-interest recorder).
4. Any leak found is REPAIRED under a gate declared before the code exists.
5. `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3, and
   `data/oi_history/` unchanged unless the recorder legitimately appended.

**Five of five or it has not cleared, and "four of five with a good explanation"
is the phrasing this ship exists to refuse.**

---

# PART 1 — THE SIXTH REPAIR (R-015)

`python cockpit\funding.py` (fifteen sabotages), `python cockpit\fear_greed.py`
(fourteen), `python data\open_interest.py` (ten). **That is the claim under
review, not the verdict.**

**Where the gates are now STRONGEST — so do NOT spend your time here:**

- every path the pilot can see — healthy, degraded, offline — is rebuilt from the
  gate's own verbatim wording and compared for **exact equality**
- every constant the gates judge by is typed out inside the gate and compared to
  the module's **by a named check**
- both doorways are proved to write **nothing to stdout or stderr** of their own,
  on every path
- the recorder builds **month two** for every asset it names and reads every
  appended row back against its own raw fetch
- `--record` is driven for real, in **both** outcomes, as a subprocess

## THE BIGGEST HOLE ON THE SHIP RIGHT NOW, AND IT IS NOT IN THOSE THREE FILES

**`cockpit/brief.py` HAS NO GATE AT ALL.** It is the pilot's actual daily tool.
The five instruments it prints are guarded to the byte; **the file that assembles
them is checked by nothing whatsoever.** Last night's finding was that a
compartment could write on the Brief through an unwatched channel — **the Brief
itself is a completely unwatched channel, forty lines long, and nobody has ever
attacked it.** It was "verified by reading", which is what this ship has been
wrong about six times.

**This is the strongest lead in the building. It is R-015 doubt 2.**

## KNOWN-WEAK AND DELIBERATELY NOT FIXED — named so you do not have to find them

**These are free hits. They are recorded rather than hidden, and none of them was
in the declared gate, which is why they are still here.**

1. **FUNDING'S TWO-ASSETS-FAIL BLOCK IS GUARDED BY NOTHING.** `_partial_checks`
   breaks exactly ONE asset at a time. **No check anywhere builds or compares the
   `[no data: ETH, SOL]` block.** Is `_expected_partial_block` even right with one
   survivor? **Named in three sets of orders now and still not fixed.**
2. **THE RECORDER'S CHECK (e) — the tamper / never-rewrite check — IS STILL
   BTCUSDT-ONLY.**
3. **B1 IS STILL A NO-OP ON A MACHINE SET TO UTC.** Funding's S5 avoids this trap
   and says why in a comment; the recorder never copied it.
4. **THE 4h BOUNDARY IS NOW HANDLED IN EXACTLY ONE CHECK** (`_month_two`, which
   accepts either a before or an after snapshot). **Every other check in that
   gate still has the raw exposure**, and nobody has watched one across a
   boundary rolling over mid-run.

## IDEAS TO GET YOU STARTED — find your own, these are not the assignment

    - the silence check proves the DOORWAY is silent. What proves the BRIEF is?
    - `_month_two` uses one seed size, once. What about a seed that already
      holds the newest row, or one with a hole in the middle, or an append that
      crosses the 30-day window edge?
    - `_raw_truth` and `_month_two` read FAPI_BASE, PERIOD, LIMIT and TIMEOUT
      out of the module they judge. Last night's author argued those are the
      source's coordinates, not an expectation. Is that argument sound, or is
      it R-014's doubt 1 wearing a different hat? Change PERIOD to 1h and see.
    - what if the recorder is run twice concurrently — the monthly task firing
      while somebody runs the gate?
    - the gates now hold ELEVEN verbatim copies of production text between them.
      What happens the day somebody legitimately improves the wording?
    - MAX_PLAUSIBLE_RATE is still 0.05, still 13-16x looser than Binance's cap

---

# PART 2 — STEP 3.3, **ONLY IF PART 1 IS CLEAN**

The third Context Deck instrument. **Declare its gate first, commit it alone with
no `.py` in the commit, name the awkward edge cases before writing code, and give
it a sabotage drill FROM BIRTH** — including one on a degraded path, one that
corrupts a CONSTANT rather than a function, and **one that reaches the pilot
without going through the value the gate inspects**, because those are the
lessons of the last three days and a part built without them is a part built
before yesterday.

**If the session is running short, do PART 1 properly and leave PART 2 entirely.**
A half-built part is worse than no part.

---

# THE RIG (defined before you run, because a broken rig proves nothing)

**Sabotage in a scratch copy OUTSIDE the repo.** All three modules import only
the standard library plus `requests` — no repo imports — so each can be copied
ALONE into scratch and run there. `open_interest.py` derives `HISTORY_DIR` from
its own `__file__`, so **a copy in scratch can only ever write to scratch.**
Confirm `git status` is clean afterwards. **Run the untouched control too.**
**Never let a drill write to `data/oi_history/` — fingerprint it before and
after.**

---

# IF ANYTHING LEAKS: REPAIR UNDER A GATE DECLARED FIRST

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves the
bar preceded the work. **Nine uses of this pattern, and it has survived audit
every time.** Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, do not assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a sha256
    of the production half before and after, printed side by side.
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself, and the
    gate never reads a constant belonging to the file it is judging.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others, caught
    every run, originals restored and the restoration verified.
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT, **and must be shown to fail for
    the reason it claims, not incidentally.** **That is the evidence; the in-run
    drill is not.**
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed".**

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the actual
output, and the verdict — **including if it is all clean.** A review that only
appears in the log when it finds something teaches the next session that silence
means safety.

**`REVIEW_QUEUE.md`: you MAY clear R-015 (you built none of it), and R-007 too if
it settles.** R-001 has now waited through **five FAILED generations of repair,
with the sixth untested**, and **moves only when a generation survives an
independent attack. Untested is not survived.** Items you
cannot settle stay OPEN with a note on what is missing; **leaving something open
is a legitimate recorded outcome.** **R-006 is not yours, ever. Never delete an
item. Never edit a cleared verdict.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

---

# BEFORE YOU FINISH

**Do the closing ritual exactly as `THE_PATTERN.md` sets it out** — seven steps,
ending with the next session's orders, the push, and your plain-words report to
the Commander. **It is not repeated here.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL NEW
   ROWS**, and **1 August is also the first time it will ever take the APPEND
   path for real** — the path proved untested on 2026-07-28 night. Task
   `ZarX Open Interest`, day 1 of every month, 09:00, laptop only (US-hosted
   cloud runners are geo-blocked by Binance). **Read `journal/daily_runs.log`
   after 1 August and tell him plainly whether it committed. Do not assume it
   worked because the task returns 0.**
2. **~~`cockpit/brief.py` HAS NO GATE.~~ DECIDED BY THE COMMANDER 2026-07-28
   (night): IT GETS ONE.** His instruction: *when we are finalising things, we
   make an inspector for `brief.py` too.* **Written into `EXECUTION_PLAN.md` as
   STEP 3.6, with its bars declared in advance and the reason it waits until all
   five instruments exist.** No session needs to re-argue this and no session may
   quietly drop it. **It is still the biggest unwatched thing on the ship until
   it is built.**
3. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
4. **The risk-doctrine decision** — the 25% position cap means real risk is ~0.49%
   per trade, not the intended 1%. **Settled BEFORE Phase 6, never after seeing
   results.**
5. **`MAX_PLAUSIBLE_RATE`** — measured at 13-16x looser than Binance's published
   cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
6. **The settled-rate anchor (R-004)** — returned to him on correct facts.
7. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. He can reverse it in
   one word.
8. **A DOCUMENT-INTEGRITY CHECK.** Nothing on this ship checks that its own
   documents are not corrupted. Found by a human looking, twice. **A one-line scan
   would close it. Recommended, not adopted.**
9. **EIGHT law candidates, none adopted, all his call:**
   - *"A session may not certify its own work; anything it cannot certify is filed
     in `REVIEW_QUEUE.md` before the commit that ships it, and only an independent
     reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."*
   - *"A check is not proven until it has been deliberately broken."* **Ten
     working implementations and still not law.**
   - *"A gate must verify what the pilot READS — the whole line, words included —
     not what the parser returned."*
   - *"A sabotage that is scored CAUGHT must be shown to fail for the reason it
     claims."*
   - *"A gate must hold EVERY path the pilot can see to the same standard — the
     degraded path, the offline path and every asset — not only the path that was
     under attack when the lesson was learned."*
   - *"A gate may not derive anything it measures by — a word, a list, a limit —
     from the file it is judging. It holds its own copy and compares the module's
     against it by name."*
   - **NEWEST, earned 2026-07-28 (night):** *"A gate must be shown to be watching
     the OBJECT the pilot actually receives, and the STATE the part is actually
     in when it runs for real — not only the value it hands back, and not only
     the first time it ever runs."* **Earned twice over in one night: the two
     instruments were judged solely on their return value while a second channel
     reached the Brief unwatched, and the recorder was judged solely on files
     built from empty while every month after the first one appends.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.** Information
instruments can carry a lighter guard. The gauntlet cannot. **SIX sessions in a
row have now failed their predecessor's work. The substitute is working — and
every hole was found by a session ORDERED to break things rather than one being
careful. Whatever reviews Phase 6 must be ordered to break it too.**
