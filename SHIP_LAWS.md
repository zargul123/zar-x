# ZAR X — SHIP LAWS
*Set by the Commander at founding. Every builder — human or AI, any model, any session — obeys these.*

## Law 1 — Everything is recorded
Every action gets written to PROGRESS_LOG.md: **what** was done, the **result** (win or
loss, exact numbers), and **why** any change was made. No silent changes. No unrecorded
results. The log is the ship's memory and outranks anyone's recollection.

## Law 2 — Code lives in parts
Every new capability is built as its own part inside its compartment
(`data/ indicators/ regime/ signals/ risk/ lab/ cockpit/`). Parts talk only through
small, simple doorways (function calls). No part reaches into another's guts.
When an error occurs, it is corrected **in isolation** — one part on the operating
table, the rest of the ship running.

## Law 3 — Every part fails safe
A part that errors reports "instrument offline" and steps aside. It never crashes the
ship. Every part ships with its own smoke test that proves it alive on its own.

## Law 4 — Gates before tests
Any test of any signal idea has its pass/fail bar declared and recorded **before** the
test runs. Results are judged against the pre-declared bar only. No moving goalposts,
no grading on a curve, no best-of-many cherry-picking.

## Law 5 — Explain before change, commit after change
Every code change is explained to the Commander in plain words before it is made,
checked for compatibility with the other parts, then committed to git with full notes.
Push to GitHub at every milestone.

## Law 6 — THE PROMISE (see README.md)
Three sealed gauntlet slots. Gates first. If all three fail, the signals chapter closes:
no 4th slot, no re-tests, information-only cockpit. The discipline is in stopping.
