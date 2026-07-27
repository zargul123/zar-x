# ZAR X — THE PATTERN (how a session runs, every time)

**What this file is.** The rhythm this ship works to, written in plain words so
the Commander can hold every session to it without being a programmer, and so a
session with no memory of the last one knows exactly what is expected.

**What this file is NOT.** It is **not a law.** `SHIP_LAWS.md` has seven laws and
each was adopted by the Commander after a failure that earned it. This file only
describes the practice that grew out of those laws. **If this file and
`SHIP_LAWS.md` ever disagree, the laws win.**

---

# WHY THIS EXISTS: FABLE IS GONE

Until Phase 2, the ship had a second, genuinely independent AI — **Fable** — who
checked work someone else had built. That mattered, and it was proven to matter:
**Fable's review caught a real defect a builder could not see** (a reviewer's own
hardcoded "15/15", recorded as R-000).

Fable is unavailable. **The substitute is separation in TIME instead of
separation in IDENTITY:** a fresh session, with no memory of writing the code,
attacks what the previous session built.

**It is weaker than Fable and everyone should say so out loud.** It is also not
nothing — **on 2026-07-26 a fresh session found four deliberate lies walking
through a gate that was reporting 48/48**, in code it had no memory of writing.

---

# THE THREE LAYERS (they are not the same thing, and this is where confusion starts)

## Layer 1 — THE GATE: the standard, written down BEFORE building

The pass/fail bar is declared and **committed on its own, with no code in that
commit**, before the thing being measured exists. Then `git show --stat` proves
the bar came first and nobody quietly lowered it to match what got built.

*Who can do this: the builder.*

## Layer 2 — THE SABOTAGE DRILL: the code breaks itself, forever, every run

The part deliberately breaks itself several ways every single time it runs, and
**fails loudly if any breakage goes uncaught.** This proves the alarm is capable
of saying no.

**This is the layer the ship did not have, and its absence cost a voided 48/48.**
Nine deliberate lies were walking through two green gates on 2026-07-26 —
**every check ran, every check passed, nobody had ever tried to break them.**

*Who can do this: the builder.*

## Layer 3 — THE INDEPENDENT ATTACK: fresh eyes invent a NEW way to break it

A session that did **not** build the thing invents a sabotage the builder never
thought of, and reports the result either way.

**THIS IS THE ONE A BUILDER CAN NEVER DO FOR THEMSELVES.** Not by being careful,
not by passing a gate, not by any tally. **You cannot invent an attack you are
blind to.** A gate is strongest exactly where it has already been attacked — so
the only useful attack is one its author never imagined.

*Who can do this: only someone who did not build it.*

---

# THE RHYTHM: EVERY SESSION DOES TWO JOBS, IN THIS ORDER

    PART 1 — ATTACK what the last session built.   (Layer 3)
    PART 2 — BUILD the next thing.                 (Layers 1 and 2)

**PART 2 IS CONDITIONAL. If Part 1 finds a real problem, fix that and stop.**
A session that reviews its predecessor and then hurries into building has not
reviewed anything; it has performed a review.

**If the session is running short, do PART 1 properly and leave PART 2 entirely.**
A half-built part is worse than no part.

## What PART 1 looks like

1. Write the bars for "this review clears" into notes **before running anything**.
2. Invent at least one **NEW** sabotage. Break the code on purpose **in a scratch
   copy outside the repo**. Run the untouched copy too — if the control does not
   pass, the rig is broken and nothing concluded means anything.
3. Confirm `git status` is clean afterwards.
4. **Write it up either way.** "Reviewed, found nothing" is a real result.
   A review that only appears in the log when it finds something teaches the next
   session that silence means safety.
5. Record the verdict in `REVIEW_QUEUE.md`.

## What PART 2 looks like

1. **Declare the gate. Commit it alone, with no code in that commit.**
2. Define the awkward edge cases **before** writing code, not after discovering
   them.
3. Build. Confine changes as narrowly as possible and **prove the confinement**
   (e.g. diff hunk line numbers), never assert it.
4. Run the gate. **Every check green, including every sabotage caught.**
5. **A failing gate is never committed and never called "mostly passed".**
6. Record everything in `PROGRESS_LOG.md` — mistakes as plainly as successes.
7. File what you could not certify in `REVIEW_QUEUE.md`. Commit. Push.
8. Write the next session's orders in `SESSION_ORDERS.md`.

---

# THE RULES THAT KEEP IT HONEST

**A SESSION MAY NEVER CLEAR ITS OWN ITEM.** However confident it is. However
good the fix. **If you found the fault and wrote the repair, you file a new
review item against your own repair and leave it open.**

**A TALLY COUNTS ONLY WHAT A MACHINE ACTUALLY CHECKED.** Not what looked right in
the output. "48/48" was honest arithmetic over an incomplete set, and the
headline number made the set look complete.

**THE MEASUREMENT ALWAYS WINS.** If any planning document contradicts something
you just measured, the measurement wins and **you write the correction down.**
This has been needed four times.

**IF YOU CHANGE A RULE YOU ARE ABOUT TO BE MEASURED BY, SAY SO IN BOLD.** Not
quietly, not in passing.

**"PROBABLY", "ALMOST CERTAINLY", "THIS SHOULD BE FINE" — FILE IT.** If you catch
yourself writing one of those about something that ships, it goes in
`REVIEW_QUEUE.md` before the commit that ships it. Filing costs one paragraph.
Not filing costs whatever the mistake costs, found later by someone who trusted
you.

**DO NOT MANUFACTURE A DEFECT TO JUSTIFY A SESSION.** The pressure after a
session that found something big is to also find something. A clean review is a
legitimate outcome.

---

# HOUSEKEEPING THAT HAS ALREADY BITTEN US

- **`git pull` FIRST, every session.** A scheduled task pushes snapshots from
  elsewhere.
- **`git commit -F <file>`** for multi-line messages. PowerShell here-strings
  mangle quotes.
- **NEVER use PowerShell `Get-Content` / `Add-Content` / `Set-Content` on this
  repo's UTF-8 files.** PowerShell 5.1 reads BOM-less UTF-8 as ANSI and
  **silently eats every em-dash, mid-dot, arrow and tick mark.** It corrupted
  four commits on 2026-07-26 before anyone noticed. Use Python
  (`open(p, encoding='utf-8')`) or the editor tools.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with `PYTHONUTF8=1`.
- **The Commander is a non-programmer.** Plain words, gray-box commands, explain
  before changing, commit after.

---

# WHAT THIS PATTERN CANNOT DO

**It cannot replace Fable at Phase 6.** Information instruments — the Brief, the
Context Deck — can carry this lighter guard. **The gauntlet cannot.** THE PROMISE
allows exactly three sealed slots and then the signals chapter closes; there is
no second attempt to catch a mistake with, and Law 7 proved the Lab's own numbers
can never detect a leak.

**At Phase 6 a second, genuinely independent AI reviews the test setup before it
runs and its verdict after. That is locked in `EXECUTION_PLAN.md` and is NOT
waived by Fable's absence.** It is R-006 in the queue and **no in-house session
may ever clear it.** If no independent AI is available when Phase 6 arrives,
**Phase 6 waits.**
