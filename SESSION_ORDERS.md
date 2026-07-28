# ZAR X PHASE 3 — **ATTACK THE FIFTH REPAIR, THEN BUILD STEP 3.3.** Five generations of gate have now each been failed by the next pair of eyes

*Written 2026-07-28 (evening) by the session that invented four new sabotages,
watched all four walk through three green gates, then repaired all three and
graded its own repair. **Stated before anything else: one mind found the four
holes, wrote every fix, and declared them all passed.** Thirty-six sabotages now
live in three files and **all thirty-six were invented by the sessions that then
defended against them.** You are the first pair of eyes that built none of it.*

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is the exact bars and commands. This part is the story, so
you understand WHY before you read WHAT. The Commander is not a programmer and
asked for it in this form. Write your own report to him the same way.*

## Where the ship is

Three parts break themselves on purpose every time they run and refuse to pass if
any breakage goes unnoticed. **Thirty-six deliberate lies live in the code; all
thirty-six are caught.**

That sounds like strength. **Read it again: every one of the thirty-six was
invented by the same session that then defended against it.** Nobody outside has
ever attacked them.

## What happened just before you

**Five sessions in a row have each found real holes in the work of the session
before.** 48/48 with four lies walking through. Then five more. Then seven more.
Then four more. **Then, last night, four more — and these were a different shape
again.**

The session before you asked one question: **what does the gate BELIEVE, and
where did it get that belief?** The answer was that three of the things each gate
measured against were read straight out of the file it was supposed to be
judging. So:

- The funding instrument's offline line — the one the pilot reads when the
  internet is down — **had a made-up funding rate welded onto it**, and the gate's
  "own verbatim copy" of that line was built out of the very words that had just
  been changed. **The lie and the ruler moved together.** The gate printed the
  fabricated rate on its own screen with a tick mark underneath reading *"NOTHING
  appended"*.
- Fear & Greed did the identical thing. Its offline line read **"last known
  reading 72 — Extreme Greed" on a day the real index said 29 — Fear** — which is
  word-for-word the lie the gate had been rebuilt that same morning to kill, and
  that lie was scored CAUGHT in the same run.
- **The recorder lost an entire asset.** Every loop in its gate said *"for each
  symbol in the module's list"*. Delete SOL from that list and SOL disappears
  from the recorder **and from the gate that checks the recorder.** Thirty days
  of Solana, gone permanently, on the one dataset that cannot be bought back —
  and the gate printed PASSED while stating, in its own words, that it now checks
  "ALL THREE assets".
- **And `--record` — the branch the monthly scheduled task actually runs — was
  executed by no test that has ever existed on this ship.** Its exit code was
  changed to always say "fine". The job then failed, wrote nothing, printed NOT
  RECORDED, and reported success. Every gate stayed green.

**The lesson, in one line: A GATE THAT ASKS THE THING IT IS JUDGING WHAT THE
ANSWER SHOULD BE IS NOT A GATE.**

## Your job, in order

**1. ATTACK LAST NIGHT'S REPAIR (R-014).** It closed four holes and was written
and graded by one mind. **Report either way.**

**2. THEN, ONLY IF PART 1 IS CLEAN, BUILD STEP 3.3** — the third Context Deck
instrument. **If Part 1 finds anything real, fix that and stop.** Five sessions
running have found something; do not assume you will be the sixth, and do not
assume you will not be.

**3. AND ONE ERRAND THAT IS NOW DUE.** After 1 August, open
`journal/daily_runs.log` and tell the Commander **plainly** whether the monthly
recorder task actually committed and pushed real new rows. **That branch has
never fired.** Do not assume it worked because the task returned 0 — `schtasks`
already reported SUCCESS once for a task that could not run at all, and as of
last night we know the exit code itself was untested until check (j) was built.

## How to attack properly

- **BRING A NEW QUESTION.** The last two sessions asked *"which paths has nobody
  attacked?"* and *"where does the gate take the module's word?"* **Both are now
  the directions these gates are strongest in.** A gate is strongest exactly
  where it has already been attacked, so reusing either question is the one
  approach guaranteed to find nothing.
- **Write what you will try and what you PREDICT, BEFORE you run it.** The last
  two sessions predicted fourteen of fourteen correctly, and that is what proved
  the holes were structural rather than luck. It also makes it impossible to
  reinterpret a result after seeing it.
- **Work on copies OUTSIDE the repo.** Never break the real files. Check
  `git status` is clean when you are done.
- **Run the untouched control first.** If the healthy copy does not pass, your rig
  is broken and nothing you conclude means anything.
- **Watch your own test. A sabotage that CRASHES is scored "caught"**, so one that
  never really ran looks like a success. **PRINT what your broken version produces
  and confirm it is visibly wrong before you believe any verdict.** This ship has
  fooled itself this way twice.
- **If your text anchor matches more than once, REFUSE TO RUN** rather than
  editing the first match. This is not theoretical: the anchors for the two
  instrument attacks and for B9 **all became ambiguous the moment the repair
  landed**, because `GATE_OFFLINE_WORDS` and `GATE_SYMBOLS` contain the old
  anchor text. Anchor on whole lines, newlines included.

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item.

**DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.** After five sessions that each
found something, the pull to also find something is real and it is a trap. **This
ship still has not seen a clean review and it needs one eventually.**

**You may clear R-014** — you built none of it. **You may never clear R-006.**
**And if you fix something, you may not clear your own fix.**

## What is his, not yours

Do not decide these by default and do not let them drop: the risk-doctrine
decision, tightening `MAX_PLAUSIBLE_RATE`, the TwelveData key, the
document-integrity check, and the **seven** law candidates. They are listed at the
bottom. **A session does not promote its own idea to law.**

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment, and the housekeeping that has bitten this ship. None of it is
repeated here.** If you have not read it, stop and read it.

**Specific to THIS job:**

1. **The last TWO entries of `PROGRESS_LOG.md`** — the four-sabotage review and
   the repair. **Read them as CLAIMS, not results. They are what you are
   auditing.** The file is ~258 KB; reading all of it will eat the budget you
   need for the actual work.
2. **`cockpit/funding.py`, `cockpit/fear_greed.py`, `data/open_interest.py`** —
   the `__main__` blocks are where every change landed. The production halves are
   provably byte-identical to yesterday's.
3. **`REVIEW_QUEUE.md` — R-014 is your worklist**, and its five recorded doubts
   are starting points, **not the assignment**. R-007 may also be settled by you.
   **R-006 may NEVER be cleared by you or any in-house session.**
4. **`ROADMAP.md`** — the MEASURED data-source facts table. If anything you
   measure disagrees with it, **your measurement wins and you write the
   correction down.**

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A **FIFTEENTH** sabotage, invented by you, thrown at Gate 3.2-R4 (funding),
   result recorded either way.
2. A **FOURTEENTH** against Gate 3.1-R4 (Fear & Greed).
3. A **TENTH** against Gate 3.2b-R2 (the open-interest recorder).
4. Any leak found is REPAIRED under a gate declared before the code exists.
5. `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3, and
   `data/oi_history/` unchanged unless the recorder legitimately appended.

**Five of five or it has not cleared, and "four of five with a good explanation"
is the phrasing this ship exists to refuse.**

---

# PART 1 — THE FIFTH REPAIR (R-014)

`python cockpit\funding.py` (fourteen sabotages), `python cockpit\fear_greed.py`
(thirteen), `python data\open_interest.py` (nine). **That is the claim under
review, not the verdict.**

**Where the gates are now STRONGEST — so do NOT spend your time here:**

- every path the pilot can see — healthy, degraded, offline — is rebuilt from the
  gate's own verbatim wording and compared for **exact equality**
- every constant the gates judge by is now typed out inside the gate and compared
  to the module's **by a named check**: `GATE_CONTRACTS`, `GATE_LIMIT`,
  `GATE_OFFLINE_WORDS` in both instruments, `GATE_SYMBOLS` in the recorder
- the recorder's disk-vs-source detector and its plausibility check run for
  **every asset the gate names**, from the gate's own list
- `--record` is driven for real, in **both** outcomes, as a subprocess

## KNOWN-WEAK AND DELIBERATELY NOT FIXED — named so you do not have to find them

**These are free hits. They are recorded rather than hidden, and none of them was
in the declared gate, which is why they are still here.**

1. **FUNDING'S TWO-ASSETS-FAIL BLOCK IS GUARDED BY NOTHING.** When two of three
   assets fail, `section_text` prints `[no data: ETH, SOL]`. `_partial_checks`
   breaks exactly ONE asset at a time. **No check anywhere builds or compares the
   two-failure block.** `_expected_partial_block` takes the settlement time over
   the survivors — is that even right with one survivor?
2. **THE RECORDER'S CHECK (e) — the tamper / never-rewrite check — IS STILL
   BTCUSDT-ONLY**, and it is the ONLY check that exercises the disagreement path
   at all. `_disk_matches_source` always starts from an EMPTY directory, so **the
   entire "existing rows on disk" code path is tested for one asset out of
   three.**
3. **B1 IS STILL A NO-OP ON A MACHINE SET TO UTC.** Funding's S5 avoids this trap
   and says why in a comment; the recorder never copied it.
4. **THE 4h BOUNDARY.** The recorder's detector makes many requests and nobody has
   watched it across a boundary rolling over mid-run.

## IDEAS TO GET YOU STARTED — find your own, these are not the assignment

    - check (j) is new machinery: it runs this file as a SUBPROCESS and rewrites
      a copy of its own source. What can go wrong in a test that edits code?
      What if the copy's write fails, or the subprocess times out?
    - `_record_does_the_job` proves exit 0 on success. Nothing proves `--record`
      does NOT always exit 1. What would that break, and would anything notice?
    - the exception NAME in both offline blocks is hardcoded into the gates as
      'ConnectionError'. What if a real outage raises something else — does the
      instrument still print honestly, and does the gate then fail for the wrong
      reason?
    - what if the recorder is run twice concurrently — the monthly task firing
      while somebody runs the gate?
    - the gates now hold SEVEN verbatim copies of production text between them.
      What happens the day somebody legitimately improves the wording?
    - MAX_PLAUSIBLE_RATE is still 0.05, still 13-16x looser than Binance's cap

---

# PART 2 — STEP 3.3, **ONLY IF PART 1 IS CLEAN**

The third Context Deck instrument. **Declare its gate first, commit it alone with
no `.py` in the commit, name the awkward edge cases before writing code, and give
it a sabotage drill FROM BIRTH** — including one that lives on a degraded path,
and one that corrupts a CONSTANT rather than a function, because those are the
lessons of 2026-07-28 and a part built without them is a part built before
yesterday.

**If the session is running short, do PART 1 properly and leave PART 2 entirely.**
A half-built part is worse than no part.

---

# THE RIG (defined before you run, because a broken rig proves nothing)

**Sabotage in a scratch copy OUTSIDE the repo.** Confirm `git status` is clean
afterwards. **Run the untouched control too.** **Point recorder drills at a
scratch `history_dir`** — every function takes one — and **never let a drill write
to `data/oi_history/`.**

---

# IF ANYTHING LEAKS: REPAIR UNDER A GATE DECLARED FIRST

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves the
bar preceded the work. **Eight uses of this pattern, and it has survived audit
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
    edits, not wrappers — and must now be CAUGHT. **That is the evidence; the
    in-run drill is not.**
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

**`REVIEW_QUEUE.md`: you MAY clear R-014 (you built none of it), and R-007 too if
it settles.** R-001 has now waited through **four** failed generations of repair
and **moves only when a generation survives an independent attack.** Items you
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
   ROWS.** Task `ZarX Open Interest`, day 1 of every month, 09:00, laptop only
   (US-hosted cloud runners are geo-blocked by Binance). **Read
   `journal/daily_runs.log` after 1 August and tell him plainly whether it
   committed. Do not assume it worked because the task returns 0** — until
   2026-07-28 that exit code was produced by code no test had ever run.
2. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
3. **The risk-doctrine decision** — the 25% position cap means real risk is ~0.49%
   per trade, not the intended 1%. **Settled BEFORE Phase 6, never after seeing
   results.**
4. **`MAX_PLAUSIBLE_RATE`** — measured at 13-16x looser than Binance's published
   cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
5. **The settled-rate anchor (R-004)** — returned to him on correct facts.
6. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. He can reverse it in
   one word.
7. **A DOCUMENT-INTEGRITY CHECK.** Nothing on this ship checks that its own
   documents are not corrupted. Found by a human looking, twice. **A one-line scan
   would close it. Recommended, not adopted.**
8. **SEVEN law candidates, none adopted, all his call:**
   - *"A session may not certify its own work; anything it cannot certify is filed
     in `REVIEW_QUEUE.md` before the commit that ships it, and only an independent
     reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."*
   - *"A check is not proven until it has been deliberately broken."* **Nine
     working implementations and still not law.**
   - *"A gate must verify what the pilot READS — the whole line, words included —
     not what the parser returned."*
   - *"A sabotage that is scored CAUGHT must be shown to fail for the reason it
     claims."*
   - *"A gate must hold EVERY path the pilot can see to the same standard — the
     degraded path, the offline path and every asset — not only the path that was
     under attack when the lesson was learned."*
   - **NEWEST, earned 2026-07-28 (evening):** *"A gate may not derive anything it
     measures by — a word, a list, a limit — from the file it is judging. It holds
     its own copy and compares the module's against it by name."* **Earned four
     times over: `GATE_CONTRACTS` and `GATE_LIMIT` were both built as one-off
     patches after exactly this failure, and neither was ever turned into a sweep,
     so the same hole was still sitting in three places.**
9. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.** Information
instruments can carry a lighter guard. The gauntlet cannot. **Five sessions in a
row have now failed their predecessor's work. The substitute is working — and
every hole was found by a session ORDERED to break things rather than one being
careful. Whatever reviews Phase 6 must be ordered to break it too.**
