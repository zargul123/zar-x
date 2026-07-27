# ZAR X PHASE 3 — **THIS SESSION IS ALL ATTACK AND NO BUILD.** Two instruments and a recorder, all three built and graded by the sessions that wrote them

*Written 2026-07-27 by the session that failed both Context Deck gates, repaired
them, then built the open-interest recorder — and filed R-011 and R-012 against
its own two deliverables. **Stated before anything else: one mind found the
faults, wrote both fixes, built the new part, wrote its gate, and graded
everything.** Twenty-eight sabotages now live in three files and **all
twenty-eight were invented by the sessions that then defended against them.**
You are the first pair of eyes that built none of it.*

## WHAT YOU ARE NOT DOING

**YOU ARE NOT BUILDING ANYTHING.** No Step 3.3, no Whale Watch instrument, no
new source. **Two deliverables shipped in one day and neither has been looked at
by anyone but its author.** The build queue waits.

## WHAT HAPPENED THE DAY BEFORE YOU, IN SIX LINES

On 2026-07-26 Gate 3.2 reported 48/48 while four deliberate lies walked through
it; it was voided and rebuilt, and the same knife found five more in
`cockpit/fear_greed.py`. Both were rebuilt and both passed. **On 2026-07-27 a
third session failed BOTH rebuilds — seven of ten new sabotages escaped.** One
printed `positive = shorts pay longs`, **the exact opposite of how the market
works**, beside three perfectly correct numbers, and the gate said PASSED.
Another printed `>> strong buy signal` on the deck of a ship whose first rule is
INFORMATION, NEVER A SIGNAL. **Cause both times: every check asked whether an
expected string was PRESENT; none asked whether anything ELSE was present, and
none checked the fixed words at all.** Both were repaired the same day. **Then,
on the Commander's explicit direction, the same session also built Step 3.2b.**

**THE PATTERN THAT SHOULD SHAPE YOUR WHOLE SESSION: three sessions in a row have
each found real holes in the work of the session before, and every one of those
holes was found by a session ORDERED TO TRY TO BREAK THE CODE — never by one
being careful.** Two generations of repair have each been failed by the next
pair of eyes.

## READ THESE FIRST

Read these files in `C:\Users\hp\Downloads\zargul trader\zar-x`:

0a. **`THE_PATTERN.md` — how a session runs, in plain words.** The three layers
   (the gate declared first · the sabotage drill that lives in the code forever
   · the independent attack), the two-job rhythm, and the housekeeping that has
   already bitten this ship. **Not a law; if it and `SHIP_LAWS.md` disagree, the
   laws win.** Read it first if you have never worked on this ship.
0. **`README.md` — it carries THE PROMISE**, which Law 6 points at by name:
   three sealed gauntlet slots and then the signals chapter closes. It is 1.7 KB.
1. `SHIP_LAWS.md` — all seven laws. Law 4 (gates before tests) especially.
2. `EXECUTION_PLAN.md` — the PHASE 3 block and the CURRENT POSITION MARKER.
3. The last FOUR entries of `PROGRESS_LOG.md` — the review that failed both
   gates, the repair, the Step 3.2b decisions, and the Step 3.2b build.
   **Read the last three as CLAIMS, not results. They are what you are
   auditing.**
4. `cockpit/funding.py` and `cockpit/fear_greed.py` — production paths and
   `__main__` blocks both.
5. **`data/open_interest.py` — the newest part, ~640 lines, and the one nobody
   has ever attacked.** Read it looking for the same shape as the others' holes.
6. `ROADMAP.md` — what exists and works, and the **MEASURED data-source facts
   table**. If anything you measure disagrees with it, **your measurement wins
   and you write the correction down.**
7. `REVIEW_QUEUE.md` — **R-011 and R-012 are your worklist.** R-001, R-008,
   R-009 and R-010 may also be settled by you, since you built none of it.
   **R-006 may NEVER be cleared by you or any in-house session.**

**`PROGRESS_LOG.md` is ~215 KB and reading all of it will eat the budget you
need for the actual work.** The last four entries are the assignment.

Then: **`git pull` FIRST** — a scheduled task pushes snapshots from elsewhere.
Use `git commit -F <file>` for multi-line messages. **NEVER use PowerShell
`Get-Content` / `Add-Content` / `Set-Content` on this repo's UTF-8 files** —
PowerShell 5.1 reads BOM-less UTF-8 as ANSI and silently eats every em-dash,
mid-dot, arrow and tick mark. It corrupted four commits on 2026-07-26 and **six
of the arrows were still there on 2026-07-27**, in a file that day's note
declared clean. Use Python (`open(p, encoding='utf-8')`) or the editor tools.

Run env: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with `PYTHONUTF8=1`.
The Commander is a non-programmer — plain words, gray-box commands, explain
before you change, commit after.

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A **TWELFTH** sabotage, invented by you, thrown at Gate 3.2-R2 (funding),
   result recorded either way.
2. The same against Gate 3.1-R2 (Fear & Greed).
3. A **SEVENTH** sabotage against Gate 3.2b (the open-interest recorder) —
   **and a check that each of its six existing sabotages fails for the reason
   its label claims.**
4. Any leak found is REPAIRED under a gate declared before the code exists.
5. `lab/` byte-identical, vault INTACT 6/6, the Brief still 3/3, and the
   recorded CSVs unchanged unless the recorder legitimately appended.

**Five of five or it has not cleared, and "four of five with a good
explanation" is the phrasing this ship exists to refuse.**

**AND THE PRACTICE THAT PAID OFF TWICE: write your PREDICTION for each sabotage
BEFORE you run it.** The 2026-07-27 session predicted ten of ten correctly,
which is what showed the holes were structural rather than lucky — and it makes
it impossible to reinterpret a result after seeing it.

---

# PART 1 — THE TWO CONTEXT DECK INSTRUMENTS (R-011)

`python cockpit\funding.py` and `python cockpit\fear_greed.py` each break
themselves **eleven** ways every run and catch all eleven. **That is the claim
under review, not the verdict.**

**What the gates now do** — read this as the list of places they are ALREADY
strongest, and therefore where NOT to spend your time:

- rebuild the **WHOLE printed block** from the source, using their own
  arithmetic, and require **exact equality** — so nothing can be appended
- hold their **own verbatim copy** of every fixed sentence, checked by name
- funding **rotates** its partial-failure drill through all three assets
- Fear & Greed holds its **own `GATE_LIMIT`** and compares the module's
  `HISTORY_LIMIT` against it
- funding keeps its before/after drift allowance; Fear & Greed keeps its
  once-only day-rollover re-fetch

## THE THREE DOUBTS ITS AUTHOR COULD NOT SETTLE — starting points, NOT the assignment

1. **THE GATES NOW CONTAIN A COPY OF THE EXACT WORDS THE BRIEF PRINTS.** The
   next time anyone legitimately improves that wording, the gate FAILS — and the
   obvious move is to edit the gate to match. **That is how a gate gets fitted to
   the code instead of the code to the gate, which is what R-001 was convicted
   of.** Nothing enforces that such an edit is deliberate and recorded. **Is that
   a defect or an accepted cost? Say which, out loud.**
2. **THE PERMANENT SABOTAGES CORRUPT OUTPUT, NOT THE FILE.** S7-S11 and F7-F11
   wrap `section_text` and rewrite what it returns. That proves the checks can
   say no to a corrupted SENTENCE. **It does not prove they would say no to every
   corrupted CODE PATH that could produce one.** The scratch rig that edited the
   real files ran once and is not part of the gate.
3. **NOTHING CHECKS THAT A GATE'S OWN DESCRIPTION MATCHES WHAT IT DOES.**

## IDEAS TO GET YOU STARTED — do not stop at these

    - the drift allowance: the funding block passes if it matches the BEFORE or
      the AFTER snapshot. Can a lie be made to live in that gap?
    - the offline paths: make one print something plausible instead of the
      offline line, without touching the happy path
    - MAX_PLAUSIBLE_RATE is still 0.05, still 13-16x looser than Binance's real
      cap. Does anything notice if it is removed entirely?
    - Fear & Greed's `_parse` range guard and its `metadata.error` handling are
      not reachable from a live fetch. Are they ever actually exercised?
    - what if the source serves a GAP, or duplicates a day?

---

# PART 2 — THE OPEN-INTEREST RECORDER (R-012) — **the one nobody has ever attacked**

`python data\open_interest.py` runs nine bars and breaks itself six ways.
**It guards the ONE dataset on this ship that cannot be recovered if it is
lost** — Binance serves a 30-day window and refuses anything older, so a defect
here is not repairable later at any price. **Attack it hardest.**

## **START HERE: ONE OF ITS SIX SABOTAGES WAS SCORED "CAUGHT" WITHOUT EVER REACHING THE CHECK IT WAS MEANT TO PROVE**

The author's own log records it: sabotage **B5**'s first version returned an
empty list and was scored CAUGHT — **by an `IndexError` two lines later**, not by
the empty-result check. **The gate printed a tick mark for a sabotage that never
touched the thing under test.** It was found by READING the drill, not by any
check, and it was rewritten.

**YOUR FIRST JOB IS THEREFORE NOT A NEW SABOTAGE. It is to confirm that each of
the six existing ones fails for the reason its label claims** — print the CSV
each produces and look at it. **If one of them passes by accident, that is a
real finding and it outranks anything else you could do this session.**

## THEN THE SEVENTH, AND THE FOUR DOUBTS ITS AUTHOR COULD NOT SETTLE

1. **THE POINT-SAMPLE MEASUREMENT IS LOAD-BEARING AND WAS TAKEN ONCE.** The
   decision to store the newest row rests on one day's evidence: 33 of 33
   overlapping 4h rows matched the 5m reading at the same instant. **Re-measure
   it.** If a 4h row can move, stored rows will disagree on re-read — the
   recorder reports that loudly and never overwrites, so the failure is loud,
   **but the decision has one day behind it.**
2. **BAR (f) IS THE ONE BAR THE PROGRAM DOES NOT CHECK.** The gate prints an
   instruction to run `cockpit\brief.py` rather than running it — deliberately,
   because a recorder that imports the cockpit is no longer a sealed
   compartment. **But a tally counts only what a machine checked.**
3. **NOTHING PROVES THE RECORDER IS EVER RUN.** There is no alarm anywhere for
   "the open-interest file has not grown in two months."
4. **THE 10% PLAUSIBILITY BAR IN CHECK (g) IS A GUESS**, chosen by feel exactly
   as `MAX_PLAUSIBLE_RATE = 0.05` was. It measured 0.03% today.

## IDEAS FOR THE SEVENTH — find your own

    - append a row for a timestamp Binance never served
    - write a row for the WRONG symbol into the right file
    - make the disagreement report fire but the run still exit 0
    - make the offline path write a partial file before failing
    - reverse the row order on disk, or drop the header
    - make the de-dup key case-sensitive, or whitespace-sensitive

## **AND THE STANDING INSTRUCTION IF YOU FAIL IT**

**If Gate 3.2b leaks, the recorder KEEPS RUNNING while it is repaired.**
Collecting a flawed record of an expiring dataset beats collecting nothing while
the gate is argued about. **Say that out loud rather than switching it off.**

---

# THE RIG (defined before you run, because a broken rig proves nothing)

**Do the sabotage in a scratch copy OUTSIDE the repo.** Confirm `git status` is
clean afterwards. **Run the untouched control too** — if the control does not
pass, your rig is broken and nothing you conclude means anything.

**CHECK YOUR OWN HARNESS: a sabotage that CRASHES is scored as "caught".** So a
sabotage that never really ran is recorded as a pass. **Print the output your
sabotage produces and confirm it is visibly wrong before you trust the verdict.**
**This ship has now done this to itself twice** — once with an anchor that
matched nothing, once with B5.

**If your text-replacement anchor matches more than once, REFUSE TO RUN rather
than editing the first match.** All three gates now hold their own copies of
production text, so several obvious anchors appear twice.

**FOR THE RECORDER SPECIFICALLY: point it at a scratch `history_dir`.** Every
function takes one. **Do not let a drill write to `data/oi_history/`** — and
check the real CSVs are unchanged when you are done.

---

# IF ANYTHING LEAKS: REPAIR UNDER A GATE DECLARED FIRST

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves
the bar preceded the work. **Six uses of this pattern, and it has survived audit
every time.** Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits confined to the `__main__`
    block — **prove it two ways, do not assert it:** every diff hunk at or after
    the `__main__` line (`funding.py` 160, `fear_greed.py` 113,
    `open_interest.py` — check it, do not assume), AND a sha256 of the
    production half before and after, printed side by side.
(b) **THE OUTPUT IS VERIFIED** against a raw fetch, using the test's own
    arithmetic. **The helper under test is never called to judge itself.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others,
    caught every run, originals restored and the restoration verified.
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT. **That is the evidence; the
    in-run drill is not.**
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL and is not committed as a pass and is not called "mostly passed".**

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the
actual output, and the verdict — **including if it is all clean.** A review that
only appears in the log when it finds something teaches the next session that
silence means safety.

**`REVIEW_QUEUE.md`: you MAY clear R-011 and R-012 (you built neither), and
R-001, R-008, R-009 and R-010 too if those clear.** R-001 has now waited through
two failed generations of repair and **moves only when a generation survives an
independent attack.** Items you cannot settle stay OPEN with a note on what is
missing; **leaving something open is a legitimate recorded outcome.**
**R-006 is not yours, ever. Never delete an item. Never edit a cleared verdict.**

**IF EVERY GATE CATCHES EVERYTHING YOU THROW: say so, and clear R-011 and
R-012.** "Reviewed, found nothing" is a real result. **DO NOT MANUFACTURE A
DEFECT TO JUSTIFY THE SESSION.** After three sessions that each found something
big, the pressure to also find something is real. **A clean review is a
legitimate outcome and this ship needs to see one eventually.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

---

# THE CLOSING RITUAL — no session ends without this

Before the final commit, in this order: **1.** `PROGRESS_LOG.md` (what happened,
mistakes as plainly as successes) · **2.** `REVIEW_QUEUE.md` (verdicts + new
doubts) · **3.** `EXECUTION_PLAN.md` (where the ship is now, including what is
unproven) · **4.** `ROADMAP.md` (what exists and works) · **5.**
`SESSION_ORDERS.md` (the next session's job, written for someone with NO memory
of you) · **6.** Commit. Push. **`THE_PATTERN.md` is the exception — do not
rewrite it unless a session earned a genuinely new lesson.**

**AND ONE CHECK THAT COSTS NOTHING AND HAS CAUGHT SOMETHING TWICE:** before your
final commit, scan the five documents for `â€`, `Â·`, `â†`, `Ã`, `âœ`. Those are
the fingerprints of the PowerShell encoding bug. **Six of them were still in
`PROGRESS_LOG.md` on 2026-07-27, in entries a note the day before had declared
clean.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **THE OPEN-INTEREST RECORDER IS NOT SCHEDULED, AND THIS IS THE LIVE ONE.**
   A recorder that is never run collects nothing, on the only dataset that
   cannot be recovered. **It must run on his LAPTOP, not the cloud watchman** —
   GitHub's runners are US-hosted and Binance geo-blocks US addresses, so a
   cloud recorder might collect nothing, silently, for weeks. The command:
   `C:\Users\hp\miniconda3\envs\tfdml\python.exe data\open_interest.py`
   **Monthly is enough** — every read reaches back 30 days, so nothing is lost
   unless two months pass with no run. **Presented, not decided.**
2. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
3. **The risk-doctrine decision** — the 25% position cap means real risk is
   ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6, never after
   seeing results.**
4. **`MAX_PLAUSIBLE_RATE`** — measured at 13-16× looser than Binance's published
   cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
5. **The settled-rate anchor (R-004)** — returned to him on correct facts.
6. **THE FUNDING LINE STAYED ON THE BRIEF, 2026-07-27, and he was told.** The
   sign has been proven repeatedly against Binance raw. **A session decided not
   to remove a line it had just verified as true. He can reverse it in one
   word.**
7. **A DOCUMENT-INTEGRITY CHECK.** Nothing on this ship checks that its own
   documents are not corrupted. Found by a human looking, twice. **A one-line
   scan would close it. Recommended, not adopted.**
8. **FIVE law candidates, none adopted, all his call:**
   - *"A session may not certify its own work; anything it cannot certify is
     filed in `REVIEW_QUEUE.md` before the commit that ships it, and only an
     independent reviewer may clear it."*
   - *"A claim about what a data source will or will not give us is not a fact
     until it has been called; planning documents must mark which claims are
     measured and which are assumed."* **Now FIVE earned examples** — the newest
     being the "incomplete period" trap that turned out not to exist.
   - *"A check is not proven until it has been deliberately broken."*
     **Five working implementations and still not law.**
   - *"A gate must verify what the pilot READS — the whole line, words included
     — not what the parser returned."* **Two instruments failed the same way
     twice each.**
   - **NEWEST, earned 2026-07-27:** *"A sabotage that is scored CAUGHT must be
     shown to fail for the reason it claims."* **B5 was scored caught while
     crashing two lines before the check it was written to prove. A drill can
     lie in exactly the way the code it guards can.**
9. Vault CSVs carry no volume column (TwelveData serves none for these pairs).

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6 and is **NOT waived by Fable's absence.**
Information instruments can carry a lighter guard. The gauntlet cannot.
**Three sessions in a row have now failed their predecessor's work. The
substitute is working — and every hole was found by a session ORDERED to break
things rather than one being careful. Whatever reviews Phase 6 must be ordered
to break it too.**
