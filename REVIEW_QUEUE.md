# ZAR X — THE REVIEW QUEUE (the docket for an independent reviewer)

**What this file is.** A short, standing list of everything on this ship that a
session judged **cannot honestly certify itself**. When Fable — or any second,
genuinely independent AI — returns, this is the file they open. Not the 128 KB
log. Not four commit hashes scattered across three documents.

**Why it exists.** Every self-doubt this ship has recorded so far was written
into `PROGRESS_LOG.md` honestly — and then buried under the next entry. A
finding nobody can find is a finding that does not exist. The log is the
ship's memory; **this file is its conscience, kept short enough to actually
be read.**

**What this file is NOT.** It is not a law and does not create one. Nothing
here overrides `SHIP_LAWS.md`. A related law was proposed and deliberately
**not** adopted — see the Commander's desk at the bottom. No session promotes
its own idea to law.

**STATUS values:** `OPEN` (awaiting an independent eye) · `CLEARED` (reviewed
by someone who did not build it, verdict recorded) · `FAILED` (reviewed, found
wanting — the step reopens) · `SUPERSEDED` (the thing it questioned no longer
exists). **Only an independent reviewer may move an item to CLEARED. A session
may never clear its own item, however confident it is.**

**PRIORITY:** `P1` affects what the ship prints or does today, or blocks
Phase 6 · `P2` should be reviewed before the surrounding area is built on ·
`P3` worth an outside look, not blocking.

---

# OPEN

## R-001 — The Step 3.2 gate was amended mid-flight by the session it judged
**STATUS: OPEN · P1 · flagged 2026-07-26 by the session that did it**

**What to review.** Gate 3.2's check (b) — the only check standing between this
ship and printing the opposite of the truth on the Brief every morning — was
declared in advance, then **rewritten by the very session that was about to be
graded by it, which then reported passing the rewritten version 48/48.**

**Why it needs an outside eye.** This is structurally indistinguishable from a
session that found a gate inconvenient and softened it. The reasoning looks
sound to its author, which is exactly what it would look like either way. **The
quality of the argument is not the evidence; the measurements are.**

**Evidence.** Amendment commit `cbfcff4` (planning documents only, no `.py`
files). Build commit `c301f54`. `SESSION_ORDERS.md` at `cbfcff4` carries the
struck original beside the replacement. `PROGRESS_LOG.md`, entry
*"GATE 3.2 CHECK (b) WAS UNPASSABLE AS WRITTEN"*.

**Reproduce.** `git show cbfcff4 --stat` · `git log --oneline cbfcff4 c301f54`
· then call `/fapi/v1/premiumIndex` and `/fapi/v1/fundingRate` yourself.

**A clean verdict looks like.** All four hold: (1) `lastFundingRate` really is
a different quantity from the newest settled `fundingRate` (compare
`nextFundingTime` to the newest `fundingTime`); (2) settled signs really do
flip between consecutive periods for ETH and SOL, making sign-agreement an
invalid fallback; (3) `_parse_rate` and `_fmt_pct` really are shared between
the settled reader and the printed path, so "exact identity" is genuinely
stricter and not theatre; (4) `cbfcff4` contains no code and precedes
`c301f54`.

**Failed looks like.** Any one of those four not holding — especially (3), the
sharing being asserted rather than real. **Also failed:** if the sabotage test
(Exhibit A in `SESSION_ORDERS.md`) shows the exact-identity check cannot
actually fail when `_fmt_pct` is deliberately broken. A check that cannot fail
is not a check.

**If it fails.** Step 3.2 reopens, the funding line comes off the Brief until
the sign is proven, and the 48/48 tally is void.

## R-002 — Two planning generations written by the mind that then built them
**STATUS: OPEN · P1 · flagged 2026-07-26**

**What to review.** Fable was unavailable. The Step 3.2 orders (`2a73645`), the
gate, the build, the self-grade, the audit instructions, and the Step 3.2b
orders were **all written by the same model in an unbroken chain.** The
substitute protection was separation in *time* — gate declared before code,
fresh session builds, third session reviews — not separation in *identity*.

**Why it needs an outside eye.** Separation in time is a real protection but a
weaker one, and it has now been stretched across two steps. Blind spots
propagate silently down a single-author chain; that is the whole reason this
ship books an independent reviewer at all.

**Evidence.** `2a73645`, `cbfcff4`, `c301f54`, `893f911`, `3423055`, and the
three most recent `PROGRESS_LOG.md` entries.

**A clean verdict looks like.** The chain's own stated weaknesses match what
the code and commits actually show — no flattering gaps between what the log
says went wrong and what the diffs reveal.

**If it fails.** Everything downstream of the first bad link is re-examined.

## R-003 — `MAX_PLAUSIBLE_RATE = 0.05` is an admitted guess in shipped code
**STATUS: OPEN · P2 · flagged 2026-07-26 by the session that shipped it**

**What to review.** `cockpit/funding.py` refuses any funding rate beyond ±5%
as implausible and degrades to "instrument offline". **Binance's real funding
cap for BTCUSDT / ETHUSDT / SOLUSDT was never measured.**

**Why it needs an outside eye.** It is a live sanity bound on a shipped
instrument, chosen by feel. If Binance's real cap exceeds it, a genuine market
extreme — precisely the moment the reading matters most — would print as
offline instead of as a number.

**Reproduce.** Measure Binance's published funding cap for the three
contracts; compare to `0.05`.

**A clean verdict looks like.** The real cap sits comfortably below 5%, so the
bound never fires on honest data — with the measured figure recorded.

**If it fails.** The constant is corrected to the measured cap and the log
records that a guess reached production.

## R-004 — A session overruled its own recommendation, unwitnessed
**STATUS: OPEN · P3 · flagged 2026-07-26**

**What to review.** The Step 3.2 session recommended printing the last settled
rate on the Brief as a verifiable anchor, the Commander said "up to you", and
**the session then overruled itself** on the grounds that the orders capped it
at one request per asset.

**Why it needs an outside eye.** Convenient in both directions: the reversal
also removed a number that would have been exactly checkable on the face of
the Brief. Probably correct. Nobody watched.

**A clean verdict looks like.** The one-request-per-asset cap is real in the
orders and the reversal follows from it, not from the extra work.

## R-005 — `min(settlements)` silently resolves a disagreement
**STATUS: OPEN · P3 · flagged 2026-07-26**

**What to review.** When the three assets report different `nextFundingTime`
values, `cockpit/funding.py` prints the earliest without saying it chose.

**Why it needs an outside eye.** A silent reconciliation is a small lie of
omission — the same shape as the errors this ship has already made twice.

**A clean verdict looks like.** Either the values cannot realistically differ
for these three contracts, or disagreement is surfaced rather than minimised.

## R-006 — THE PHASE 6 SECOND-AI REVIEW **(cannot be cleared in-house)**
**STATUS: OPEN · P1 · LOCKED BY `EXECUTION_PLAN.md` PHASE 6**

**What to review.** The gauntlet's test setup **before** it runs, and its
verdict **after**.

**Why it needs an outside eye.** THE PROMISE allows exactly three sealed slots
and then the signals chapter closes. There is no second attempt to catch a
mistake with. Law 7 proved the Lab's numbers cannot detect a leak, and that a
leak can clear every bar with the too-good alarm silent.

**This item is NOT waived by Fable's absence and NO session may clear it** —
not by being careful, not by passing a gate, not by a 48/48 tally. It is
cleared only by a second, genuinely independent AI. If none is available when
Phase 6 arrives, **Phase 6 waits.**

---

# CLEARED

## R-000 — Gate 2.5 and the birth of Law 7
**STATUS: CLEARED 2026-07-26 · reviewed independently by Fable**

Gate 2.5 was reviewed by someone who did not build it, and **the review caught
a real defect: a reviewer's own hardcoded "15/15"**. The finding stood, the
gate was blocked on an honest blocker until the Commander decided, and the
outcome became Law 7 — the Leak Law. Recorded here as the worked example of
this queue functioning: **an outside eye found something the builder could
not, and clearing was earned rather than assumed.**

---

# HOW TO FILE AN ITEM (every session, every time)

**If you catch yourself writing "probably", "almost certainly", "I believe", or
"this should be fine" about something that ships — file it.** If you grade your
own work, file it. If you change a rule you are about to be measured by, file
it in bold. Filing costs one paragraph; not filing costs whatever the mistake
costs, discovered later by someone who trusted you.

Copy this form, append under OPEN, keep it tight:

    ## R-0NN — <one-line title, the doubt not the feature>
    **STATUS: OPEN · P1|P2|P3 · flagged <date> by <who>**
    **What to review.**            plain words, no jargon
    **Why it needs an outside eye.** the honest reason, including self-interest
    **Evidence.**                  exact commits, files, log entry titles
    **Reproduce.**                 the command a reviewer runs
    **A clean verdict looks like.** stated BEFORE the review, Law 4's spirit
    **Failed looks like.**         and what reopens if it does

**Never delete an item. Never edit a cleared verdict.** Move it between
sections and leave the history legible — a docket that quietly tidies itself
teaches the next session nothing.

---

# ON THE COMMANDER'S DESK

**A LAW CANDIDATE, PROPOSED AND DELIBERATELY NOT ADOPTED — his call:**

> *"A session may not certify its own work. Anything a session cannot honestly
> certify itself is filed in REVIEW_QUEUE.md before the commit that ships it,
> and only an independent reviewer may clear it."*

This session wrote the file but **did not write the law**, because the law book
has seven laws and each was adopted by the Commander after a failure that
earned it — not by a session that liked its own idea. Seven laws get read;
twelve get skimmed.

**The other standing candidate, from 2026-07-26, still undecided:** *"A claim
about what a data source will or will not give us is not a fact until it has
been called; planning documents must mark which claims are measured and which
are assumed."* **It now has two earned examples**, the second being a false
claim inside a gate's own most important check.
