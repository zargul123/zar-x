# ZAR X PHASE 3 — **ATTACK THE FOURTH REPAIR, THEN BUILD STEP 3.3.** Four generations of gate have now each been failed by the next pair of eyes

*Written 2026-07-28 by the session that audited the recorder's six sabotages
(clean), then invented four new ones and watched all four walk through three
green gates, then repaired all three and graded its own repair. **Stated before
anything else: one mind found the four holes, wrote every fix, and declared them
all passed.** Thirty-two sabotages now live in three files and **all thirty-two
were invented by the sessions that then defended against them.** You are the
first pair of eyes that built none of it.*

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is the exact bars and commands. This part is the story,
so you understand WHY before you read WHAT. The Commander is not a programmer
and asked for it in this form. Write your own report to him the same way.*

## Where the ship is

Three parts break themselves on purpose every time they run and refuse to pass
if any breakage goes unnoticed. **Thirty-two deliberate lies live in the code;
all thirty-two are caught.**

That sounds like strength. **Read it again: every one of the thirty-two was
invented by the same session that then defended against it.** Nobody outside has
ever attacked them.

## What happened just before you

**Four sessions in a row have each found real holes in the work of the session
before.** 48/48 with four lies walking through. Then five more. Then seven more.
**Then, yesterday, four more — and yesterday's were a different shape.**

The session before you found that **all three gates rebuilt their whole output
and demanded a perfect match — but only when everything was working.** The
moment an asset failed, or the internet dropped, or you looked at any asset
other than Bitcoin, the checks fell back to the old, weak question: *"is the
expected text in there somewhere?"*

So:

- The funding instrument **reversed the sentence explaining what the numbers
  mean** — "shorts pay longs" instead of "longs pay shorts", the opposite of how
  the market works — **but only when one asset was missing.** The gate printed
  the reversed sentence on its own screen and put three tick marks under it.
- Both instruments' **offline lines** happily carried a made-up number on the
  end. Fear & Greed printed *"last known reading 72 — Extreme Greed"* on a day
  the real index said **29 — Fear**, and the check underneath it said
  *"nothing else printed"*.
- **The worst one: the open-interest recorder.** The only check that compared
  what was SAVED against what Binance actually SENT was looking at Bitcoin and
  nothing else. Ethereum and Solana were checked by counting rows. A single
  plausible bug filled thirty days of ETH and SOL with **Bitcoin's** numbers —
  22 times and 80 times wrong — and the gate said PASSED. **That is the one
  dataset this ship cannot buy back at any price.**

**The lesson, in one line, and it is why your orders say what they say: A LESSON
GETS APPLIED WHERE IT WAS LEARNED AND NOWHERE ELSE.** The day before, this ship
learned that "is the text in there?" is a worthless question. It fixed that on
the one path it was standing on and left every other path exactly as it was.

## Your job, in order

**1. ATTACK YESTERDAY'S REPAIR (R-013).** It closed four holes and was written
and graded by one mind. **Ask the question that found them: WHICH PATHS HAS
NOBODY ATTACKED?** A fourteenth funding sabotage, a thirteenth Fear & Greed, an
eighth recorder. Report either way.

**2. THEN, ONLY IF PART 1 IS CLEAN, BUILD STEP 3.3** — the third Context Deck
instrument. **If Part 1 finds anything real, fix that and stop.** Four sessions
running have found something; do not assume you will be the fifth, and do not
assume you will not be.

**3. AND ONE ERRAND THAT IS DUE, WHOEVER YOU ARE.** After 1 August, open
`journal/daily_runs.log` and tell the Commander **plainly** whether the monthly
recorder task actually committed and pushed real new rows. **That branch has
never fired.** Do not assume it worked because the task returned 0 — `schtasks`
already reported SUCCESS once for a task that could not run at all.

## How to attack properly

- **Write what you will try and what you PREDICT, BEFORE you run it.** The last
  session predicted ten of ten correctly, and that is what proved the holes were
  structural rather than luck. It also makes it impossible to reinterpret a
  result after seeing it.
- **Work on copies OUTSIDE the repo.** Never break the real files. Check
  `git status` is clean when you are done.
- **Run the untouched control first.** If the healthy copy does not pass, your
  rig is broken and nothing you conclude means anything.
- **Watch your own test. A sabotage that CRASHES is scored as "caught"**, so one
  that never really ran looks like a success. **PRINT what your broken version
  produces and confirm it is visibly wrong before you believe any verdict.**
  This ship has fooled itself this way twice.
- **If your text anchor matches more than once, REFUSE TO RUN** rather than
  editing the first match. All three gates hold their own copies of production
  wording, so obvious anchors appear twice.

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item.

**DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.** After four sessions that each
found something, the pull to also find something is real and it is a trap.
**This ship still has not seen a clean review and it needs one eventually.**

**You may clear R-013** — you built none of it. **You may never clear R-006.**
**And if you fix something, you may not clear your own fix.**

## What is his, not yours

Do not decide these by default and do not let them drop: the risk-doctrine
decision, tightening `MAX_PLAUSIBLE_RATE`, the TwelveData key, the
document-integrity check, and the **six** law candidates. They are listed at the
bottom. **A session does not promote its own idea to law.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment, and the housekeeping that has bitten this ship. None
of it is repeated here.** If you have not read it, stop and read it.

**Specific to THIS job:**

1. **The last TWO entries of `PROGRESS_LOG.md`** — the four-sabotage review and
   the repair. **Read them as CLAIMS, not results. They are what you are
   auditing.** The file is ~239 KB; reading all of it will eat the budget you
   need for the actual work.
2. **`cockpit/funding.py`, `cockpit/fear_greed.py`, `data/open_interest.py`** —
   the `__main__` blocks are where every change landed. The production halves
   are provably byte-identical to yesterday's.
3. **`REVIEW_QUEUE.md` — R-013 is your worklist**, and its five recorded doubts
   are starting points, **not the assignment**. R-007 may also be settled by you.
   **R-006 may NEVER be cleared by you or any in-house session.**
4. **`ROADMAP.md`** — the MEASURED data-source facts table. If anything you
   measure disagrees with it, **your measurement wins and you write the
   correction down.**

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A **FOURTEENTH** sabotage, invented by you, thrown at Gate 3.2-R3 (funding),
   result recorded either way.
2. A **THIRTEENTH** against Gate 3.1-R3 (Fear & Greed).
3. An **EIGHTH** against Gate 3.2b-R (the open-interest recorder).
4. Any leak found is REPAIRED under a gate declared before the code exists.
5. `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3, and
   `data/oi_history/` unchanged unless the recorder legitimately appended.

**Five of five or it has not cleared, and "four of five with a good
explanation" is the phrasing this ship exists to refuse.**

---

# PART 1 — THE FOURTH REPAIR (R-013)

`python cockpit\funding.py` (thirteen sabotages), `python cockpit\fear_greed.py`
(twelve), `python data\open_interest.py` (seven). **That is the claim under
review, not the verdict.**

**Where the gates are now STRONGEST — so do NOT spend your time here:**

- the whole printed block, the degraded block and the offline block are each
  rebuilt from the gate's own verbatim wording and compared for **exact
  equality**, so nothing can be appended, deleted or reversed on any of them
- the recorder's disk-vs-source detector and its plausibility check run for
  **all three assets** and name which one failed
- funding rotates its partial drill through all three assets, with a per-asset
  drift allowance
- Fear & Greed holds its own `GATE_LIMIT` and compares the module's against it

## THE FIVE DOUBTS ITS AUTHOR COULD NOT SETTLE — starting points, NOT the assignment

1. **THE GATES NOW HOLD FOUR MORE VERBATIM COPIES OF PRODUCTION WORDING.** The
   next person who legitimately improves any of that wording watches a gate
   fail, and **the obvious move is to edit the gate to match — which is what
   R-001 was convicted of.** Nothing enforces that such an edit is deliberate
   and recorded. **The problem was made worse on purpose. Judge that trade.**
2. **THE RECORDER'S CHECK (e) — the tamper / never-rewrite check — IS STILL
   BTCUSDT-ONLY.** It is the same shape of gap B7 exploited, one check over. It
   was left alone because the declared gate did not name it.
3. **THE RECORDER'S DETECTOR NOW MAKES THREE TIMES THE REQUESTS** and so has
   three times the exposure to a 4h boundary rolling over between the module's
   fetch and the test's fetch, which would fail the gate spuriously. Nobody has
   watched it across a boundary.
4. **THE RECORDER'S B1 IS A NO-OP ON A MACHINE SET TO UTC.** Funding's S5 avoids
   this trap and says why in a comment; the recorder never copied it. It fails
   LOUD rather than quietly, so it was filed rather than fixed.
5. **FOUR ATTACKS, ONE IDEA.** Every one was the same observation on a different
   path. **What is proven is that those four lies are caught. Nothing is proven
   about anything else.**

## IDEAS TO GET YOU STARTED — find your own, these are not the assignment

    - the recorder's check (e) and the tamper path generally: what can hide there?
    - the `--record` path the SCHEDULED TASK actually runs is NOT the gate.
      Nothing in the drill exercises it. What could be wrong in the branch that
      runs unattended once a month?
    - the exception NAME in both offline blocks is now hardcoded into the gates
      as 'ConnectionError'. What if a real outage raises something else — does
      the instrument still print honestly, and does the gate then fail for the
      wrong reason?
    - `_expected_partial_block` takes the settlement time over the SURVIVORS
      only. Is that right when two assets fail rather than one?
    - what if the recorder is run twice concurrently — the monthly task firing
      while somebody runs the gate?
    - MAX_PLAUSIBLE_RATE is still 0.05, still 13-16x looser than Binance's cap

---

# PART 2 — STEP 3.3, **ONLY IF PART 1 IS CLEAN**

The third Context Deck instrument. **Declare its gate first, commit it alone
with no `.py` in the commit, name the awkward edge cases before writing code,
and give it a sabotage drill FROM BIRTH** — including one that lives on a
degraded path, because that is the lesson of 2026-07-28 and a part built without
it is a part built before yesterday.

**If the session is running short, do PART 1 properly and leave PART 2
entirely.** A half-built part is worse than no part.

---

# THE RIG (defined before you run, because a broken rig proves nothing)

**Sabotage in a scratch copy OUTSIDE the repo.** Confirm `git status` is clean
afterwards. **Run the untouched control too.** **Point recorder drills at a
scratch `history_dir`** — every function takes one — and **never let a drill
write to `data/oi_history/`.**

---

# IF ANYTHING LEAKS: REPAIR UNDER A GATE DECLARED FIRST

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves
the bar preceded the work. **Seven uses of this pattern, and it has survived
audit every time.** Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove
    it two ways, do not assert it:** every diff hunk at or after the `__main__`
    line (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a
    sha256 of the production half before and after, printed side by side.
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others,
    caught every run, originals restored and the restoration verified.
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT. **That is the evidence; the
    in-run drill is not.**
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

**`REVIEW_QUEUE.md`: you MAY clear R-013 (you built none of it), and R-007 too
if it settles.** R-001 has now waited through **three** failed generations of
repair and **moves only when a generation survives an independent attack.**
Items you cannot settle stay OPEN with a note on what is missing; **leaving
something open is a legitimate recorded outcome.** **R-006 is not yours, ever.
Never delete an item. Never edit a cleared verdict.**

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

1. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL
   NEW ROWS.** Task `ZarX Open Interest`, day 1 of every month, 09:00, laptop
   only (US-hosted cloud runners are geo-blocked by Binance). **Read
   `journal/daily_runs.log` after 1 August and tell him plainly whether it
   committed. Do not assume it worked because the task returns 0.**
2. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
3. **The risk-doctrine decision** — the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never after
   seeing results.**
4. **`MAX_PLAUSIBLE_RATE`** — measured at 13-16x looser than Binance's published
   cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
5. **The settled-rate anchor (R-004)** — returned to him on correct facts.
6. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. He can reverse it
   in one word.
7. **A DOCUMENT-INTEGRITY CHECK.** Nothing on this ship checks that its own
   documents are not corrupted. Found by a human looking, twice. **A one-line
   scan would close it. Recommended, not adopted.**
8. **SIX law candidates, none adopted, all his call:**
   - *"A session may not certify its own work; anything it cannot certify is
     filed in `REVIEW_QUEUE.md` before the commit that ships it, and only an
     independent reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."* **Now SIX earned examples** — the newest
     being the live open-interest snapshot endpoint, never once called for ETH
     or SOL until 2026-07-28.
   - *"A check is not proven until it has been deliberately broken."*
     **Eight working implementations and still not law.**
   - *"A gate must verify what the pilot READS — the whole line, words included
     — not what the parser returned."* **Two instruments failed this way twice
     each.**
   - *"A sabotage that is scored CAUGHT must be shown to fail for the reason it
     claims."* Earned by B5. **Now with a worked example on the other side: the
     2026-07-28 audit checked all six and found all six honest.**
   - **NEWEST, earned 2026-07-28:** *"A gate must hold EVERY path the pilot can
     see to the same standard — the degraded path, the offline path and every
     asset — not only the path that was under attack when the lesson was
     learned."* **Four lies walked through three green gates by standing on a
     path nobody had attacked.**
9. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.**
Information instruments can carry a lighter guard. The gauntlet cannot.
**Four sessions in a row have now failed their predecessor's work. The
substitute is working — and every hole was found by a session ORDERED to break
things rather than one being careful. Whatever reviews Phase 6 must be ordered
to break it too.**
