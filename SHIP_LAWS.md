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

## Law 7 — THE LEAK LAW (Gate 2.5's lesson, adopted 2026-07-26)
The Lab's numbers catch **overfitting**. They can **never** catch a **leak** — a strategy
fed the answers answers correctly everywhere, hold-out included. This was MEASURED, not
assumed: in Gate 2.5 a strategy that reads tomorrow's candle cleared every locked
Phase 6 bar (PF 1.39, walk-forward CONSISTENT 6 of 6, Monte Carlo 8.01%) and the
too-good alarm stayed SILENT (PF 1.39 < 2, win 57.6% < 70). A leak does not have to be
spectacular to be a lie; it only has to be good enough to win a slot. Therefore:

1. **No strategy enters Lab certification or a gauntlet slot until its code has been
   READ, line by line, for leaks** — by the working session, hunting specifically for:
   data the object carries that the engine never handed it, look-ahead indexing, file
   or API reads at call time, and anything else that could smuggle the future in.
   **The reading is RECORDED in PROGRESS_LOG.md** (who read, what was hunted, verdict).
   No recorded reading = no certification, whatever the numbers say.
2. **`lab/leak_check.py` is run on the strategy object and its report recorded.** It
   finds the most common smuggle (carried data) automatically. A clean scan is an aid,
   NEVER proof — the scan narrows the hunt; the reading is the verdict.
3. **The too-good alarm (PF > 2 or win rate > 70%) remains a flare, not a fence.** When
   it fires, hunt the leak. When it is silent, that silence proves nothing — Gate 2.5's
   leak never tripped it. The alarm is never to be lowered until an exhibit trips it:
   a detector tuned to flag one known cheat flags honest strategies too.

This law exists because the numbers cannot defend this door. A human reading code is
the ONLY defence against a leak, so the reading is law, not courtesy.
