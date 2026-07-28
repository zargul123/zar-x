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

**FIRST USE, 2026-07-26.** The 2026-07-26 audit session worked R-001 … R-005 as
its worklist. **The queue functioned: three items reviewed found wanting, two
cleared on measurements nobody had taken.** R-001 was convicted by the
"Failed looks like" clause the accused session wrote for it. That is the
design working.

---

# FAILED — reviewed, found wanting; the step reopens

## R-001 — The Step 3.2 gate was amended mid-flight by the session it judged
**STATUS: FAILED 2026-07-26 · P1 · flagged by the session that did it ·
reviewed by the 2026-07-26 audit session, which did not build it**

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

### >>> VERDICT 2026-07-26: **FAILED**, on both of the conditions above.

**(1), (2) and (4) HOLD** and hold well — measured, not taken on trust. The
amendment was NOT self-serving: the original check really was unpassable, and
the fallback really would have failed at random.

**(3) IS HALF-FALSE, and it is the half the whole argument rested on.**
`_parse_rate` is shared **and genuinely guarded** — sabotaging it is caught.
`_fmt_pct` is shared in the source **but never enters the comparison**, so
sharing it guards nothing. Sharing a helper is not testing it.

**EXHIBIT A, the deciding evidence — 4 of 6 deliberate sabotages PASSED the
gate** (scratch copy outside the repo; control passed; `git status` clean):

    S1  _fmt_pct sign flipped ....... NOT CAUGHT   prints the exact opposite
    S2  _fmt_pct x100 dropped ....... NOT CAUGHT   wrong by 100x
    S3  _parse_rate sign flipped .... CAUGHT
    S4  _parse_rate scaled x10 ...... CAUGHT
    S5  _utc_hhmm timezone dropped .. NOT CAUGHT   settlement time 5h wrong
    S6  CONTRACTS miswired .......... NOT CAUGHT   BTC shows SOL's rate

Under S1 the check prints `✓ BTCUSDT: parsed 5.819e-05 == raw '0.00005819' →
-0.0058%` — **a tick mark on a line displaying the falsehood.**

**IT IS A CLASS OF HOLE, NOT ONE BUG.** Every check verifies what happens
*before* the printed string is assembled; nothing verifies the string itself
beyond "a sign character appears" and "something matches `\d\d:\d\d`".

**THE 48/48 TALLY IS VOID.** Not fraudulent — all 48 checks ran and passed —
but they counted plumbing, not meaning.

**NOT DONE, and referred to the Commander:** the funding line was **NOT** taken
off the Brief. **The sign IS proven** — re-derived independently against
Binance the same day, matching digit for digit. Removing a line verified as
correct, on a clause written by the accused to describe a different failure,
would be obedience to wording over meaning. **His call, not a session's.**

**TO REOPEN STEP 3.2 PROPERLY:** the gate needs a check comparing the printed
STRING to an independently derived string, and **the sabotage test must become
a permanent part of the gate, not a one-off audit exercise.** A check nobody
has tried to break is a check nobody has tested.

### >>> REMEDY SHIPPED 2026-07-26 — **R-001 STAYS FAILED. IT IS NOT CLEARED.**

Both repairs were built the same day (`GATE 3.2-R PASSED`, all six sabotages
caught including the four that escaped). **The status does not move**, because
**the session that shipped the remedy is the session that found the fault, and
a session may never clear its own item — least of all the one it just fixed.**
**Filed as R-009 for an independent eye.** R-001 moves only when someone who
did not write the repair says so.

### >>> 2026-07-27: **THE INDEPENDENT EYE CAME, AND R-001 STAYS FAILED.**

The review R-001 was waiting for happened: a session that built none of it threw
five new sabotages at Gate 3.2-R and **four walked through** (R-009). **The
remedy R-001 was waiting on was itself defective.** A second remedy shipped the
same day (Gate 3.2-R2, all ten original attacks now caught) — **and R-001 still
does not move**, because that remedy was again written by the session that found
the fault. **R-011 is now the item R-001 waits on.** Two generations of repair
have each been failed by the next pair of eyes; **R-001 moves when a generation
survives one.**

### >>> 2026-07-28: **A THIRD GENERATION WAS FAILED. R-001 STILL DOES NOT MOVE.**

The 2026-07-28 session threw three new sabotages at Gate 3.2-R2 and Gate 3.1-R2
and **all three walked through** (R-011). A third remedy shipped the same day and
**was again written by the session that found the fault** — now filed as R-013.
**Three generations of repair; three failed by the next pair of eyes.**

**The condition on this item has still never been met: R-001 moves when a
generation SURVIVES an independent attack.** None has. **Recorded plainly,
because by now the streak is itself the finding** — every one of the three holes
was found by a session ORDERED to break things, and not one by a session being
careful.

### >>> 2026-07-28 (night): **A FIFTH AND A SIXTH GENERATION WERE FAILED. R-001 STILL DOES NOT MOVE.**

R-013 was failed on 2026-07-28 evening (four of four escaped) and **R-014 was
failed the same night (three of three escaped)**. Both remedies were again
written by the session that found the fault — now R-015.

**Six generations of repair; six failed by the next pair of eyes. The condition
has never once been met.** Written here plainly because the streak is the
finding: **not one of the six holes was found by a session being careful, and
every one was found by a session ORDERED to break things.**

## R-002 — Two planning generations written by the mind that then built them
**STATUS: FAILED 2026-07-26 · P1 · flagged 2026-07-26 · reviewed by the
2026-07-26 audit session**

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

### >>> VERDICT 2026-07-26: **FAILED — narrowly, specifically, and honestly.**

**One flattering gap was found.** From the Step 3.2 log entry:

> *"a sign flip or unit error in either helper would fail this check"*

**That sentence is false**, and Exhibit A S1/S2 are the proof. It is the one
load-bearing technical belief the chain held sincerely and never tested — and
because it sounded like a verification, it stood in for one.

**Everything else in the chain's self-reporting checked out.** It recorded its
own near-overclaim, its own sloppy rewritten check, its own wasted commits, and
its own independence problem in plain words. **The failure here is not
dishonesty; it is a single-author chain believing its own reasoning where a
second pair of eyes would have asked for a demonstration.** Which is precisely
what this item was raised to detect.

**Downstream re-examination required:** nothing else was built on the false
belief, because Step 3.2b was never started. **`cockpit/fear_greed.py` is built
the same way and was NOT audited for the same class of hole** — see R-008.

## R-004 — A session overruled its own recommendation, unwitnessed
**STATUS: FAILED 2026-07-26 · P3 · flagged 2026-07-26 · reviewed by the
2026-07-26 audit session**

**What to review.** The Step 3.2 session recommended printing the last settled
rate on the Brief as a verifiable anchor, the Commander said "up to you", and
**the session then overruled itself** on the grounds that the orders capped it
at one request per asset.

**Why it needs an outside eye.** Convenient in both directions: the reversal
also removed a number that would have been exactly checkable on the face of
the Brief. Probably correct. Nobody watched.

**A clean verdict looks like.** The one-request-per-asset cap is real in the
orders and the reversal follows from it, not from the extra work.

### >>> VERDICT 2026-07-26: **FAILED — the premise does not hold.**

**The cap is real.** `SESSION_ORDERS.md` at `2a73645`: *"keep it to one request
per asset per call and no retry storms."*

**But the same orders explicitly pre-authorised the extra call**, three lines
earlier: *"Last settled rates for context (optional, one call per asset)."*

**The reversal was presented as compelled by the orders when the orders
permitted it.** The decision may well still be right — the pilot rarely acts on
it. **The reason given for it was not.** And the number removed was the one that
would have been checkable on the face of the Brief, which is the direction of
convenience R-004 was raised to watch for. **Returned to the Commander on
correct facts. "Up to you" still stands.**

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

## R-003 — `MAX_PLAUSIBLE_RATE = 0.05` is an admitted guess in shipped code
**STATUS: CLEARED 2026-07-26 · P2 · flagged by the session that shipped it ·
measured by the 2026-07-26 audit session**

**What to review.** `cockpit/funding.py` refuses any funding rate beyond ±5%
as implausible and degrades to "instrument offline". **Binance's real funding
cap for BTCUSDT / ETHUSDT / SOLUSDT was never measured.**

**Why it needs an outside eye.** It is a live sanity bound on a shipped
instrument, chosen by feel. If Binance's real cap exceeds it, a genuine market
extreme — precisely the moment the reading matters most — would print as
offline instead of as a number.

**A clean verdict looks like.** The real cap sits comfortably below 5%, so the
bound never fires on honest data — with the measured figure recorded.

### >>> VERDICT 2026-07-26: **CLEARED.** Measured at last, via an endpoint no
previous session had called: `GET /fapi/v1/fundingInfo` (HTTP 200, 736 symbols).

    BTCUSDT   cap +/-0.00300  (0.300% per 8h)   fundingIntervalHours 8
    ETHUSDT   cap +/-0.00300  (0.300% per 8h)   fundingIntervalHours 8
    SOLUSDT   cap +/-0.00375  (0.375% per 8h)   fundingIntervalHours 8
    widest cap anywhere on the exchange: 3.000%
    largest magnitude actually observed on our three, 500 settled
    periods each back to 2026-02-10: 0.0535%

**The feared failure mode does not exist.** The bound is 13–16x looser than the
real cap; it can never refuse an honest extreme. **A guess reached production
and happened to be safe** — recorded, as R-003 required, so the next guess is
measured first.

**RECOMMENDATION, NOT A FINDING (Commander's call, no code changed):** at 5% it
is nearly useless as a sanity bound — it would pass a rate 80x too large.
Tightening to ~0.01 (1%, still 2.7x the real cap) would make it a real fence.

## R-005 — `min(settlements)` silently resolves a disagreement
**STATUS: CLEARED 2026-07-26 · P3 · flagged 2026-07-26 · measured by the
2026-07-26 audit session**

**What to review.** When the three assets report different `nextFundingTime`
values, `cockpit/funding.py` prints the earliest without saying it chose.

**Why it needs an outside eye.** A silent reconciliation is a small lie of
omission — the same shape as the errors this ship has already made twice.

**A clean verdict looks like.** Either the values cannot realistically differ
for these three contracts, or disagreement is surfaced rather than minimised.

### >>> VERDICT 2026-07-26: **CLEARED on the first limb** — they cannot
realistically differ.

Measured, not assumed: all three carry `fundingIntervalHours: 8` in
`/fapi/v1/fundingInfo`, and all three returned the identical `nextFundingTime`
of 2026-07-27 00:00 UTC. **Disagreement IS real on this exchange** — across all
848 perpetuals there are 5 distinct settlement times, 505 contracts on one and
300 on another — **but it is driven by contracts on 4h intervals, which ours
are not.** `min()` over three identical values is a no-op.

**One narrow exception found while measuring, filed separately as R-007.**

---

# OPEN

**2026-07-27 note on where things sit in this section.** R-009 and R-010 were
reviewed and **FAILED** today. They are left physically here, under their
original headings, so each verdict sits with the evidence that produced it
rather than being shuffled into another section and losing its context. Their
STATUS lines are the authority, not the heading they appear under. **R-011,
filed against today's repair, is genuinely open.**

**2026-07-28 note, same convention.** R-011 and R-012 were reviewed and
**FAILED** today and stay physically where they are, with their evidence.
**R-013, filed against today's repair, is the genuinely open one.** Of the items
in this section, **only R-006, R-007 and R-013 are actually open** — and R-006 is
not open to anybody in-house.

**2026-07-28 (night) note, same convention again.** R-013 was failed that evening
and **R-014 was failed the same night.** Both stay physically where they are,
with their evidence. **Of every item in this file, only R-006, R-007 and R-015
are actually open** — and R-006 is not open to anybody in-house. **R-007, the
settlement-boundary race, was NOT touched tonight: my question came from
elsewhere and I did not look at it.**

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

**2026-07-26 note from the audit session, added without touching the status:**
this item just earned a fresh argument. A same-model session separated only by
time cleared three bars and then found a hole four sabotages wide in work it
had no memory of writing. **It found that hole because it was ordered to try to
break the code, not because it was careful.** Whatever reviews Phase 6 must be
ordered to try to break it too.

## R-007 — The settlement-boundary race in `min(settlements)`
**STATUS: OPEN · P3 · flagged 2026-07-26 by the audit session**

**What to review.** `cockpit/funding.py` fetches the three contracts in a loop,
one request each. **If a settlement falls between two of those requests** — the
loop straddles 00:00, 08:00 or 16:00 UTC — the earlier assets return the
settlement that is about to happen and the later ones return the next one.
`min()` then prints a settlement time that **has just passed**.

**Why it needs an outside eye.** It is a real window, not a theoretical one:
roughly half a second wide, three times a day. Harmless in effect — the pilot
sees a time a few seconds stale — but it is the same silent-reconciliation
shape as R-005, and it is the residue R-005's clearance leaves behind.

**Evidence.** `cockpit/funding.py` `section_text()`, the loop over `contracts`
collecting `settlements`, then `min(settlements)`.

**Reproduce.** Call `/fapi/v1/premiumIndex` for the three symbols with a
deliberate pause straddling a settlement boundary and compare the values.

**A clean verdict looks like.** Either the window is judged acceptable and said
so out loud, or the printed time is derived once rather than reconciled from
three answers.

## R-008 — The 2026-07-26 audit's own blind spots (filed against itself)
**STATUS: FAILED 2026-07-26 · P2 · flagged by the audit session about itself ·
point 3 REVIEWED AND CONFIRMED the same day**

### >>> VERDICT 2026-07-26 on point 3: **FAILED — the hole was real, and worse.**

`cockpit/fear_greed.py` was put under the same knife (independent: it was built
in `462e675` by a different session). **FIVE of six sabotages passed its smoke
test.** Funding leaked 4 of 6; this leaked 5 of 6.

    F1 value inverted · F2 label decoupled · F3 all ages "yesterday"
    F4 date shifted 3 days · F5 yesterday printed as today ... ALL ESCAPED
    F6 offline path fabricates a number ....................... caught
    control (untouched) passed, so the rig was valid

**F1 printed `70 — Fear`** — a contradiction on the face of the line, since 70
is Greed territory — **and every check passed.** Same cause as funding: every
check interrogated the parse, none compared the printed sentence to the source.

**This confirms the defect is a CLASS, measured now on two independently built
instruments.** It is not a mistake either author made; it is the shape of test
this ship had been writing.

**REMEDY SHIPPED the same day** (`GATE 3.1-R PASSED`, all six caught, production
path untouched, every diff hunk ≥ line 113). **Points 1, 2 and 4 of R-008 remain
unanswered and are carried into R-010.**

**This item was filed by the session that then reviewed it. Marking it FAILED is
not clearing it** — a session may never clear its own item, and nothing here is
cleared.

**What to review.** The audit that failed R-001 and R-002, on the same standard
it applied to them.

**Why it needs an outside eye.** Three honest weaknesses, stated by the session
that has an interest in them not being noticed:

1. **It found the hole it went looking for.** The suspicion was formed while
   reading the code and pre-registered in writing before any test ran — the
   honest sequence — but a reviewer arriving with a hypothesis is a reviewer
   who may stop once it is confirmed.
2. **Six sabotages is not a proof of completeness.** It proves four specific
   lies pass the gate. It does not enumerate what else does.
3. **`cockpit/fear_greed.py` was NOT audited for the same class of hole,
   and it is built the same way** — a `_parse`, a formatter, and checks that
   verify the parse rather than the printed sentence. **The most likely place
   the next hole is sitting, and this session did not look.**
4. **The reviewer is the same model as the builder**, separated only by
   session and by having no memory of writing the code. Clearing three bars
   does not make that substitute stronger than R-002 says it is.

**A clean verdict looks like.** Someone runs the sabotage exercise against
`fear_greed.py`, and against whatever replaces the Step 3.2 gate, and finds
either nothing or something this session should have caught.

## R-009 — The rebuilt Gate 3.2-R was written by the session that failed the old one
**STATUS: FAILED 2026-07-27 · P1 · flagged 2026-07-26 by the session that built
the repair · reviewed by the 2026-07-27 session, which built none of it**

### >>> VERDICT 2026-07-27: **FAILED. FOUR OF FIVE NEW SABOTAGES WALKED THROUGH.**

A session that built neither the instrument, nor either gate, nor the repair
invented five new sabotages and wrote a PREDICTION for each **before running
anything**. Scratch copies outside the repo, controls passed first, `git status`
clean throughout. **Five predictions, five correct.**

    S7   "positive = longs pay shorts" -> "shorts pay longs",
         every digit still correct ................................ ESCAPED
    S8   a fabricated fourth asset "  ·  XRP +0.0100%" appended,
         fetched from nowhere ..................................... ESCAPED
    S9   "— crowd positioning, information, not a signal" deleted .. ESCAPED
    S10  a failed asset vanishes without being named ............... caught
    S11  the missing-asset name hardcoded to SOL, so any asset's
         failure is reported as SOL's ............................. ESCAPED

**Under S7 the instrument printed the exact opposite of how the market works,
beside three perfectly correct numbers, and the gate printed "GATE 3.2-R PASSED
— all six deliberate sabotages were caught" and exited 0.** The rebuild closed
the hole for DIGITS and left it open for WORDS.

**THE CLASS: every check asked whether an expected string was PRESENT. None
asked whether anything ELSE was present, and none checked the fixed words at
all.** S11 is the one nobody had suspected: the permanent drill always broke
SOL, so a module naming every missing asset "SOL" agreed with its own test.

**REMEDY SHIPPED the same day** — Gate 3.2-R2, declared in `c69a71b` with no
`.py` in it, built in `975c125`. Whole-block exact equality, the fixed wording
guarded verbatim, a rotating partial-failure drill, and eleven permanent
sabotages. **All ten original attacks, re-run as real file edits, are now
CAUGHT.** Production lines 1-159 byte-identical by sha256.

**R-009 DOES NOT MOVE TO CLEARED. The session that found the fault wrote the
repair and graded it — the same structure this item exists to catch, one turn
further down the road. Filed as R-011.**

**What to review.** `cockpit/funding.py`'s rebuilt smoke test (Gate 3.2-R): the
printed-sentence check, and the six-sabotage drill now baked into every run.

**Why it needs an outside eye.** **The auditor who found the hole wrote the
patch and then graded it.** That is the same structure as R-001 — the fault
this very queue was raised to catch — one turn further down the road. **It
looks right to its author, which is exactly what it would look like either
way.** And the repair is defined by the six lies its author already knew about:
**a gate built from a known list of attacks is strongest precisely where it has
already been attacked.**

**Evidence.** Gate declaration `c447852` (no `.py` in it, on purpose). Build
commit and its `PROGRESS_LOG.md` entry *"THE INSPECTOR REBUILT"*. Diff hunks
all at or after line 160, so the production path is untouched.

**Reproduce.** `python cockpit\funding.py` — section 3 breaks the file six ways
live and must catch all six. Then **write a seventh sabotage of your own** and
see whether it survives.

**A clean verdict looks like.** A reviewer who did not build it invents at
least one NEW sabotage and finds it caught — or finds it escapes and says so.
**"The six pass" is not a clean verdict; it is the claim under review.**

**Failed looks like.** A seventh lie walks through, in which case the gate is
still shaped around its author's imagination rather than around the truth.

## R-010 — Gate 3.1-R was also written by the session that found its fault
**STATUS: FAILED 2026-07-27 · P1 · flagged 2026-07-26 by the session that built
the repair · reviewed by the 2026-07-27 session, which built none of it**

### >>> VERDICT 2026-07-27: **FAILED. THREE OF FIVE NEW SABOTAGES WALKED THROUGH.**

Same reviewer, same rig, same discipline — predictions written before the run,
control passed first.

    F7   "information, not a signal" -> "buy when others are
         fearful" ................................................. ESCAPED
    F8   "   >> strong buy signal" appended to the reading line .... ESCAPED
    F9   "from alternative.me" -> "from CNN Business", a source
         this ship has never called ............................... ESCAPED
    F10  the two context values swapped ........................... caught
    F11  history cut to 2 days, the week-ago point disappears ...... caught

**BOTH DOUBTS ITS AUTHOR RECORDED WERE CORRECT, and both were worse than
stated.** Doubt (1), the substring match: F8 printed **`>> strong buy signal`
on the Context Deck of a ship whose founding rule is INFORMATION, NEVER A
SIGNAL**, and the gate applauded. Doubt (2), the unverified disclaimer: F7
rewrote that very rule into advice and nothing noticed.

**A FOURTH FINDING NOBODY HAD SUSPECTED, from a sabotage that was CAUGHT.**
F11 failed the run — but look at WHICH line failed: **sabotage F3 escaped its
own drill** (`✗ F3 … ESCAPED AGAIN — GATE IS DECORATIVE`). The drill read
`HISTORY_LIMIT` from the module it was testing, **so breaking that constant
disarmed the detector.** Funding had solved this exact problem with its private
`GATE_CONTRACTS`; this file never did the same for its constant.

**REMEDY SHIPPED the same day** — Gate 3.1-R2, same declaration commit
`c69a71b` (no `.py`), built in `975c125`. Whole-block exact equality, the
disclaimer guarded verbatim, the gate's own `GATE_LIMIT` compared against the
module's, eleven permanent sabotages, all caught. Production lines 1-112
byte-identical by sha256.

**R-010 DOES NOT MOVE TO CLEARED, for the same reason as R-009. Filed as
R-011.**

**What to review.** `cockpit/fear_greed.py`'s rebuilt smoke test: the
printed-sentence check and the permanent six-sabotage drill.

**Why it needs an outside eye.** **Identical structure to R-009, one instrument
over.** The session that ran the knife wrote the patch and graded it. **Twelve
sabotages now exist across the two instruments and all twelve were invented by
the sessions that then defended against them.** A gate built from a known list
of attacks is strongest exactly where it has already been attacked.

**Evidence.** Gate declaration `b6bfdb7` (no `.py` in it, on purpose). The
`PROGRESS_LOG.md` entries *"THE FEAR & GREED KNIFE"* and *"GATE 3.1-R PASSED"*.

**Reproduce.** `python cockpit\fear_greed.py` — section 3 breaks the file six
ways live and must catch all six. Then **write a seventh of your own.**

**A clean verdict looks like.** A reviewer who did not build it invents at least
one NEW sabotage and finds it caught — or finds it escapes and says so. **"The
six pass" is not a clean verdict; it is the claim under review.**

**Failed looks like.** A seventh lie walks through, in which case the gate is
still shaped around its author's imagination.

**Two specific doubts its author could not settle**, offered as starting points
rather than as the assignment: **(1)** the value/label check is a substring
match on the assembled line, so a sentence that contains the right pair AND
extra rubbish would still pass; **(2)** nothing verifies the fixed words
*"crowd-mood gauge from alternative.me — information, not a signal"*, so the
INFORMATION-not-a-signal disclaimer could be edited or deleted and no check
would notice. **The same gap exists in `cockpit/funding.py` for its
"positive = longs pay shorts" line, and neither was closed today.**

## R-011 — Gate 3.2-R2 and 3.1-R2 were written by the session that failed their predecessors
**STATUS: FAILED 2026-07-28 · P1 · flagged 2026-07-27 by the session that built
the repair · reviewed by the 2026-07-28 session, which built none of it**

### >>> VERDICT 2026-07-28: **FAILED. THREE OF THREE NEW SABOTAGES WALKED THROUGH.**

A session that built neither instrument, neither rebuild, nor any of the
twenty-two sabotages invented three more and wrote a PREDICTION for each
**before running anything**. Real text edits to scratch copies outside the repo,
every anchor required to match exactly once, controls passed first, `git status`
clean throughout. **Three predictions, three correct.**

    S12  the mechanism sentence REVERSES — but only when an
         asset is missing, so the healthy block is byte-identical .. ESCAPED
    S13  the funding OFFLINE line carries a fabricated rate ........ ESCAPED
    F12  the Fear & Greed OFFLINE line keeps the honest offline
         words AND appends a fabricated mood ...................... ESCAPED

**THE CAUSE, and it is one sentence: the R2 rebuild applied whole-block exact
equality to the HEALTHY PATH ONLY. Every degraded path was still guarded by
asking whether an expected substring was PRESENT, and by counting lines** —
which is the exact question the R2 rebuild was written to abolish.

**Under S12, Gate 3.2-R2's own section 5 printed
`positive = shorts pay longs` — the reverse of how the market works — on its own
screen, and put three tick marks underneath it.** That is sabotage S7, the lie
the entire R2 rebuild exists to kill, moved one path over. **Doubt 2 of this
item's three was therefore right in a way its author did not anticipate:** the
worry was that in-run sabotages corrupt output rather than code paths; the actual
hole was that a whole code PATH had no equality check at all.

**F12 is sabotage F6 done properly.** F6 — "offline path fabricates a number" —
was in the drill and marked caught, **but only because it DROPS the offline
words**, so the bar never had to prove it could notice an ADDITION. **And F6 was
scored by an inline private copy of the offline bar inside the drill — a second
instance of a check proving a weaker copy of itself rather than the real one.**

**REMEDY SHIPPED the same day** — Gate 3.2-R3 and Gate 3.1-R3, declared in
`a8eddab` with no `.py` in it, built in the commit after. Both degraded paths and
both offline blocks are now rebuilt from the gate's own verbatim wording and
compared for EXACT EQUALITY; F6 and F12 share the real bar. Funding carries
thirteen permanent sabotages, Fear & Greed twelve, **and all three original
attacks, re-run as real file edits, now FAIL the gates with named diagnostics.**
Production halves byte-identical by sha256, every diff hunk inside `__main__`.

**R-011 DOES NOT MOVE TO CLEARED. The session that found the fault wrote the
repair and graded it — the same structure this item exists to catch, one turn
further down the road. Filed as R-013.**

**What to review.** The whole-block equality check, the verbatim wording guard,
the rotating partial drill, and the ten new permanent sabotages on both
instruments.

**Why it needs an outside eye.** **Third generation of the same structure.** The
session that found the fault wrote the patch and graded it — exactly what R-001,
R-009 and R-010 were each raised to catch. **Twenty-two sabotages now live in
the two files and all twenty-two were invented by sessions that then defended
against them.**

**THREE SPECIFIC DOUBTS THIS SESSION COULD NOT SETTLE ABOUT ITS OWN WORK**,
offered as starting points and NOT as the assignment:

1. **THE GATE NOW CONTAINS A COPY OF THE EXACT WORDS THE BRIEF PRINTS.** The
   next time anyone legitimately improves that wording, the gate will fail —
   **and the obvious move will be to edit the gate to match.** That is how a
   gate gets fitted to the code instead of the code to the gate, and it is the
   very failure R-001 was convicted of. **Changing the gate's copy of the
   wording must be a deliberate, recorded act — but nothing enforces that.**
2. **THE PERMANENT SABOTAGES CORRUPT OUTPUT, NOT THE FILE.** S7-S11 and F7-F11
   wrap `section_text` and rewrite what it returns. That proves the checks can
   say no to a corrupted SENTENCE. **It does not prove they would say no to
   every corrupted CODE PATH that could produce one.** The scratch rig, which
   edits the files for real, showed ten of ten caught **on 2026-07-27 only** —
   it is not part of the gate and does not run again.
3. **NOTHING CHECKS THAT A GATE'S OWN DESCRIPTION MATCHES WHAT IT DOES.** This
   session's first working version announced "six ways" while running eleven,
   and printed "GATE 3.2-R PASSED" from Gate 3.2-R2. Caught by reading, not by
   a check. **A gate that misdescribes its own scope gets quoted later as
   evidence of something it never tested.**

**Evidence.** Declaration `c69a71b` (no `.py` in it, on purpose). Build
`975c125`. The 2026-07-27 `PROGRESS_LOG.md` entries.

**Reproduce.** `python cockpit\funding.py` and `python cockpit\fear_greed.py` —
each breaks itself eleven ways and must catch all eleven. **Then write a
TWELFTH of your own.**

**A clean verdict looks like.** A reviewer who did not build it invents at least
one NEW sabotage per instrument and finds it caught — or finds it escapes and
says so. **"The eleven pass" is not a clean verdict; it is the claim under
review.**

**Failed looks like.** A twelfth lie walks through — in which case the gate is
still shaped around its author's imagination, three generations deep, and the
Commander should hear plainly that separation-in-time has stopped paying.

## R-012 — The open-interest recorder was built, gated and graded by one session
**STATUS: FAILED 2026-07-28 · P1 · flagged 2026-07-27 by the session that built
it · reviewed by the 2026-07-28 session, which built none of it**

### >>> VERDICT 2026-07-28: **SPLIT. THE SIX-SABOTAGE AUDIT IS CLEAN. THE SEVENTH WALKED THROUGH. THE ITEM FAILS.**

**THE HALF THAT HELD, and it held properly.** This item's clean verdict required
confirming the six existing sabotages each fail for the reason its label claims,
after B5 had once been scored CAUGHT while crashing two lines short of the check
it was written to prove. **All six do. There is no second B5.** Measured with an
instrumented copy outside the repo that announces which condition fired; the
untouched control passed first and the instrumented run reached the same verdict,
so the instrumentation changed nothing. Six predictions written first, six
correct.

    B1 -> TIMESTAMP-NOT-IN-SOURCE      B4 -> FIELD-MISMATCH
    B2 -> TIMESTAMP-NOT-IN-SOURCE      B5 -> TRAP, reached cleanly, NO CRASH
    B3 -> ROW-COUNT-BAR (31 < 175)     B6 -> FIELD-MISMATCH

**THE HALF THAT FAILED, and it is the worse half.**

    B7  ETHUSDT and SOLUSDT recorded with BITCOIN's open interest ... ESCAPED

**`_disk_matches_source()` — the ONLY check anywhere in Gate 3.2b that compared
what was WRITTEN to what Binance SERVED — was hardcoded to BTCUSDT. So were
checks (e) and (g). For two of the three assets the entire gate only ever
COUNTED: 180 rows, 30 days, no duplicates.**

The defect used was a memo cache keyed on the TIMESTAMP rather than on the
(SYMBOL, TIMESTAMP) pair — what "let us not re-derive rows we have already seen"
looks like written carelessly. **BTCUSDT stays perfect, which is why nothing
saw it.** Printed, not assumed:

    on disk after B7          what Binance actually served
    BTC  105984.62500000      BTC   105984.62500000    correct
    ETH  105984.62500000      ETH  2316121.51100000    22x wrong
    SOL  105984.62500000      SOL  8532810.05000000    80x wrong

**Not one failing check appeared. Gate 3.2b printed "all six deliberate
sabotages were caught" and exited 0** — thirty days of two assets fabricated, on
**the one dataset Binance will not sell back at any price.**

**REMEDY SHIPPED the same day** — Gate 3.2b-R, declared in `a8eddab` with no
`.py` in it. The detector runs for **all three symbols** and names which one
failed; check (g) does too; B7 is the permanent seventh sabotage. Re-run as a
real file edit, B7 now fails the gate **twice over, by two checks not designed
together** (the row-by-row disk comparison at ETHUSDT, and the plausibility bar
at 95% and 98% apart). **The recorder was never switched off**, per the standing
instruction.

**Doubts 1 (the point-sample measurement), 2 (bar (f) verified in the shell) and
4 (the 10% bar) were NOT settled and remain live.** Doubt 3(a) — whether the
scheduled task's commit-and-push branch works against real new rows — **is still
owed and can only be answered after 1 August.**

**R-012 DOES NOT MOVE TO CLEARED, for the same reason as R-011. Filed as R-013.**

**What to review.** `data/open_interest.py` and Gate 3.2b — the backfill, the
idempotence proof, the empty-result trap, the never-rewrite rule, and the six
sabotages it breaks itself with on every run.

**Why it needs an outside eye.** **Same structure as R-009, R-010 and R-011: one
mind wrote the part, wrote the test, and declared it passed.** The gate was
declared before the code (Law 4 satisfied, `979e8dd` has no `.py` in it) and the
six sabotages were still invented by the author. **And this part guards the ONE
dataset on this ship that cannot be recovered if it is lost** — a defect here is
not repairable later at any price.

**A DEMONSTRATED REASON TO DISTRUST THE DRILL, from this build's own log:**
**sabotage B5 was scored CAUGHT while never reaching the check it was written to
prove** — it crashed two lines earlier and the tick mark appeared anyway. It was
found by READING the drill, not by any check, and it was fixed. **The question a
reviewer should ask is how many of the other five are passing for a reason
nobody has looked at.**

**FOUR SPECIFIC DOUBTS ITS AUTHOR COULD NOT SETTLE**, offered as starting points
and NOT as the assignment:

1. **THE POINT-SAMPLE MEASUREMENT IS LOAD-BEARING AND WAS TAKEN ONCE.** The
   decision to store the newest row rests on a measurement made 2026-07-27:
   33 of 33 overlapping 4h rows matched the 5m reading at the same instant, so
   a 4h row is a point sample and cannot move. **If that is wrong — or becomes
   wrong — stored rows would disagree on re-read.** The recorder reports such a
   disagreement loudly and never overwrites, so the failure is loud rather than
   silent, **but the decision itself has one day's evidence behind it.**
2. **THE `(f)` BAR IS VERIFIED IN THE SHELL, NOT BY THE GATE.** The gate prints
   an instruction to run `cockpit\brief.py` rather than running it, deliberately
   — a recorder that imports the cockpit is no longer a sealed compartment.
   **But that means bar (f) is the one bar the program does not check**, and a
   tally counts only what a machine checked.
3. **~~NOTHING PROVES THE RECORDER IS EVER RUN.~~ SCHEDULED 2026-07-27** on the
   Commander's instruction: task `ZarX Open Interest`, day 1 of every month,
   09:00, laptop, with StartWhenAvailable so a laptop that was off catches up.
   **TWO THINGS STILL UNPROVEN AND THEY BELONG TO THE NEXT REVIEWER:**
   **(a)** the task's commit-and-push branch **has never run against real new
   rows** — only the "nothing to commit" branch has, because no 4h period
   closed during the session that built it. The command sequence was proved
   correct in a throwaway repo. **Read `journal/daily_runs.log` after 1 August
   and confirm it actually committed, rather than assuming.**
   **(b) there is still no alarm anywhere on this ship for "the open-interest
   file has not grown in two months."** The schedule makes that unlikely; it
   does not make it detectable.
4. **THE 10% PLAUSIBILITY BAR IN CHECK (g) IS A GUESS.** It compares a stored
   point sample up to 4h old against a live snapshot; it measured 0.03% today.
   **The bar was chosen by feel, exactly like `MAX_PLAUSIBLE_RATE = 0.05` was**
   — and R-003 exists because that guess shipped and was only measured two steps
   later. **This one is filed on the day it shipped instead.**

**Evidence.** Decisions commit `979e8dd` (no `.py` in it, on purpose). Build
`6bebcd8`. The 2026-07-27 `PROGRESS_LOG.md` entries.

**Reproduce.** `python data\open_interest.py` — nine bars and six sabotages,
all must be green. **Then write a SEVENTH sabotage of your own**, and check
whether each of the six fails for the reason its label claims.

**A clean verdict looks like.** A reviewer who did not build it invents at least
one NEW sabotage and finds it caught — **and confirms the existing six each fail
for the stated reason rather than incidentally.** "The six pass" is not a clean
verdict; it is the claim under review.

**Failed looks like.** A seventh walks through, or any of the six turns out to
be passing by accident as B5 was. **If it fails, the recorder keeps running
regardless** — collecting a flawed record of an expiring dataset beats
collecting nothing while the gate is argued about. **Say that out loud rather
than switching it off.**

## R-013 — Gate 3.2-R3, 3.1-R3 and 3.2b-R were written by the session that failed their predecessors
**STATUS: FAILED 2026-07-28 (evening) · P1 · flagged 2026-07-28 by the session
that built the repair, reviewed the same day by a session that built none of it**

**What to review.** The exact-equality checks now guarding funding's degraded
block, both offline blocks, and the recorder's all-symbol detector — plus the
four new permanent sabotages S12, S13, F12 and B7.

**Why it needs an outside eye.** **FOURTH GENERATION OF THE SAME STRUCTURE.** The
session that found the fault wrote the patch and graded it — exactly what R-001,
R-009, R-010 and R-011 were each raised to catch. **Thirty-two sabotages now live
in three files and all thirty-two were invented by sessions that then defended
against them.** And this repair was shaped by ONE idea applied to four paths;
**a gate built from a known list of attacks is strongest precisely where it has
already been attacked.**

**FIVE SPECIFIC DOUBTS THIS SESSION COULD NOT SETTLE ABOUT ITS OWN WORK**,
offered as starting points and NOT as the assignment:

1. **THE VERBATIM-WORDING PROBLEM IS NOW FOUR STRINGS WORSE.** R-011's first
   doubt said the gate holding a copy of the Brief's exact words means the next
   legitimate wording improvement will fail the gate, **and the obvious move will
   be to edit the gate to match — which is what R-001 was convicted of.** This
   repair added four more such copies: two degraded blocks and two offline
   blocks. **Nothing enforces that changing them is a deliberate, recorded act.
   The problem was made worse on purpose, with eyes open, because the
   alternative was leaving four paths unguarded — but somebody who did not make
   that trade should judge it.**
2. **THE RECORDER'S CHECK (e) IS STILL BTCUSDT-ONLY.** The tamper /
   never-rewrite check was deliberately not widened, because the declared gate
   did not name it and widening a bar mid-flight is the R-001 failure running the
   other way. **It is the same shape of gap B7 exploited, one check over.**
3. **THE DETECTOR NOW MAKES THREE TIMES THE REQUESTS AND HAS THREE TIMES THE
   EXPOSURE to a 4h boundary rolling over between the module's fetch and the
   test's own fetch**, which would fail the gate spuriously. The window is small
   and the failure is loud rather than silent, **but the exposure was tripled
   today and nobody has watched it across a boundary.**
4. **B1's TIMEZONE NO-OP WAS FOUND AND NOT FIXED.** The recorder's B1 replaces
   the timestamp helper with a naive local conversion, **which proves nothing on
   a machine whose clock is UTC.** Funding's S5 already avoids this trap and says
   why in a comment; the recorder never copied the lesson. It fails LOUD on a UTC
   machine rather than passing quietly, so it was filed rather than repaired
   under a gate that did not name it. **The Commander's laptop is UTC+5, so the
   drill is real there today.**
5. **FOUR ATTACKS, ONE IDEA.** Every one was the same observation applied to a
   different path. **What is proven is that these four lies are now caught; what
   is NOT proven is that nothing else escapes.** A genuinely different reviewer
   would bring a second idea.

**Evidence.** Declaration `a8eddab` (`PROGRESS_LOG.md` only, no `.py` — check it
with `git show --stat a8eddab`). The build commit after it. The two 2026-07-28
`PROGRESS_LOG.md` entries.

**Reproduce.** `python cockpit\funding.py` (thirteen sabotages),
`python cockpit\fear_greed.py` (twelve), `python data\open_interest.py` (seven).
**Then write a FOURTEENTH, a THIRTEENTH and an EIGHTH of your own** — and ask the
question this repair was born from: **which PATHS has nobody attacked?**

**A clean verdict looks like.** A reviewer who did not build it invents at least
one NEW sabotage per part and finds it caught — or finds it escapes and says so.
**"The thirty-two pass" is not a clean verdict; it is the claim under review.**

**Failed looks like.** Any new lie walks through — in which case the gates are
still shaped around their authors' imagination, four generations deep, and the
Commander should hear plainly that separation-in-time has stopped paying.

### >>> VERDICT 2026-07-28 (evening): **FAILED. FOUR OF FOUR NEW SABOTAGES WALKED THROUGH.**

*By a session that built none of the three files. Predictions were written into
working notes before anything was run; four of four were correct. Controls run
first — all three gates green, Brief 3/3, vault INTACT 6/6 — so the rig was
valid. All sabotage on copies outside the repo; `git status` clean throughout.*

**THE HOLE IS ONE THING IN THREE PLACES: THE GATE READ ITS OWN GROUND TRUTH OUT
OF THE MODULE IT WAS JUDGING.**

    S14  funding.py OFFLINE_WORDS reworded to carry a fabricated rate.
         GATE_OFFLINE_BLOCK interpolated that same constant, so the gate's
         "own verbatim copy" moved with the lie. Equality held. PASSED.
    F13  the same in fear_greed.py. The pilot's offline line read "last known
         reading 72 - Extreme Greed" on a day the index read 29 - Fear.
         F12 was scored CAUGHT in the same run. PASSED.
    B9   SYMBOLS cut from three assets to two. Every loop in the gate said
         `for symbol in SYMBOLS`, so SOLUSDT vanished from the recorder AND
         from its own detector. PASSED, while printing "ALL THREE assets".
    B8   the `--record` branch the monthly task runs is exercised by nothing.
         Exit code changed to always 0: job failed, printed NOT RECORDED,
         wrote nothing, reported success. PASSED.

**Doubt 5 of R-013's own five said it plainly — "four attacks, one idea… what is
NOT proven is that nothing else escapes." It was right.** Doubts 1-4 remain
unexamined: check (e) is still BTCUSDT-only, the 4h-boundary exposure is still
unwatched, and B1 is still a no-op on a UTC machine.

**R-013 DOES NOT MOVE TO CLEARED. The session that found these four faults wrote
the repair for them and may not grade it. Filed as R-014.**

---

## R-014 — Gate 3.2-R4, 3.1-R4 and 3.2b-R2 were written by the session that failed their predecessors
**STATUS: OPEN · P1 · flagged 2026-07-28 (evening) by the session that built the repair**

**What to review.** `GATE_OFFLINE_WORDS` in both instruments and `GATE_SYMBOLS`
in the recorder, each with a named check comparing the module's constant to the
gate's own; the recorder's new check (j), which runs `--record` for real as a
subprocess in both outcomes; and the four new permanent sabotages S14, F13, B8
and B9. **Thirty-six sabotages now live in three files and all thirty-six were
invented by sessions that then defended against them.**

**Why it needs an outside eye.** **FIFTH GENERATION OF THE SAME STRUCTURE.**
R-001, R-009, R-010, R-011 and R-013 were each raised to catch exactly this, and
each time the next pair of eyes found something. **Do not read five straight
failures as proof the fix is now good; read them as proof that one mind grading
its own gate has never once been enough on this ship.**

**FIVE SPECIFIC DOUBTS THIS SESSION COULD NOT SETTLE ABOUT ITS OWN WORK**,
offered as starting points and NOT as the assignment:

1. **THE SWEEP WAS DONE BY HAND AND BY EYE.** The claim is "no gate now derives
   an expectation from the module under test". **Nothing enforces that.** It was
   established by reading three files and grepping, by the person who wanted it
   to be true. A sixth constant of the same kind would look exactly like the
   three that were found. **The check that would close this — a gate that fails
   when its own expectations are traceable to the module — was not built.**
2. **CHECK (j) RUNS THE FILE AS A SUBPROCESS AND EDITS A COPY OF ITS OWN SOURCE.**
   That is new machinery in a gate, it roughly doubles the recorder gate's
   requests and runtime, and **a test that rewrites source text has a whole class
   of failure the others do not.** The anchors are whole lines and it refuses on
   an ambiguous match — which it did, correctly, on its first run, because the
   anchor text appears in the file that contains it. **Judge whether that whole
   approach is sound or too clever.**
3. **`subprocess` WAS ADDED TO THE RECORDER'S `__main__`.** The declared gate
   named this in advance rather than waving it through later, and called it
   standard library rather than a dependency. **That was the author's own
   judgement on his own bar.** Somebody else should agree or disagree out loud.
4. **B8 IS JUDGED ONLY ON THE FAILURE PATH.** `_record_alarm_fires` proves the
   alarm sounds when the job fails. **Nothing proves the alarm STAYS SILENT for
   the right reason on the success path** beyond exit 0 and a row count — and a
   `--record` that always exits 1 would be caught by check (j)'s first half but
   is not in the drill as its own sabotage.
5. **AND THE STANDING ONE, NOW WORSE AGAIN: the gates hold ever more verbatim
   copies of production text.** Three more constants joined today. R-011's and
   R-013's first doubt — that a legitimate reword will fail a gate and the
   obvious move is to edit the gate to match, which is what R-001 was convicted
   of — **is now larger than when it was filed twice.**

**Evidence.** Declaration `f2be611` (`PROGRESS_LOG.md` only, no `.py` — check it
with `git show --stat f2be611`; it was `7f8c13d` before a rebase onto a cloud
snapshot, which the log records). The build commit after it. The two 2026-07-28
evening `PROGRESS_LOG.md` entries.

**Reproduce.** `python cockpit\funding.py` (fourteen sabotages),
`python cockpit\fear_greed.py` (thirteen), `python data\open_interest.py` (nine).

**Then write a FIFTEENTH, a FOURTEENTH and a TENTH of your own.** The question
that found today's four was *"what does the gate BELIEVE, and where did it get
that belief?"* **Do not reuse it — it is now the direction this gate is strongest
in. Bring a different question.**

**A clean verdict looks like.** A reviewer who did not build it invents at least
one NEW sabotage per part and finds it caught — or finds it escapes and says so.
**"The thirty-six pass" is not a clean verdict; it is the claim under review.**

**Failed looks like.** Any new lie walks through — in which case the gates are
still shaped around their authors' imagination, five generations deep, and the
Commander should hear plainly that separation-in-time has stopped paying.

### >>> VERDICT 2026-07-28 (night): **FAILED. THREE OF THREE NEW SABOTAGES WALKED THROUGH.**

*By a session that built none of the three files. Predictions written into
working notes before anything was run; three of three were correct. Controls run
first — 14/14, 13/13, 9/9, Brief 3/3, vault INTACT 6/6, `git status` clean — so
the rig was valid. Real text edits to copies OUTSIDE the repo; every anchor a
whole line, refusing to run on an ambiguous match (**which it did, twice**).
`data/oi_history/` fingerprinted before and after and unchanged.*

**THE HOLE IS ONE THING IN TWO SHAPES: THE GATE WAS PERFECTLY HONEST ABOUT THE
WRONG OBJECT.**

    S15  funding.section_text() PRINTS a trade instruction to stdout and
         returns the honest block byte-for-byte unchanged. `brief.py` runs
         the function BEFORE printing what it returns, so the advice lands
         on the pilot's Brief through a channel no equality check watches.
         It printed thirty times on the gate's own screen. PASSED, exit 0.
    F14  the same in fear_greed.py — scored green in the same run that
         scored F7, "the disclaimer turned into ADVICE", as CAUGHT. PASSED.
    B10  record() transposes the OI column, but ONLY when the CSV already
         exists. Every row-level check in Gate 3.2b-R2 writes into an EMPTY
         directory, and the two checks that meet an existing file append
         ZERO rows — so **the gate had only ever tested month one, and month
         one happens once.** PASSED, all NINE sabotages scored CAUGHT.

**B10 WAS NOT BELIEVED ON THE GREEN GATE ALONE.** Month two was built by hand —
a CSV seeded with 100 rows written by the test from its own raw fetch, then
`record()` called to append the rest. **80 of 180 rows landed on disk 64,763x
wrong (the dollar value in the coin column); the untouched control produced 0 of
180 wrong.** On the one dataset Binance will not sell back at any price. **B4 is
that exact lie and is scored CAUGHT in the same run — B10 is B4 with one `if` in
front of it.**

**R-014's own doubt 5 said the gates hold ever more verbatim copies of what the
doorway RETURNS. It was the right worry aimed one object short.** Doubts 1-4
remain unexamined: the sweep is still by eye, check (e) is still BTCUSDT-only,
B1 is still a no-op on a UTC machine.

**REMEDY SHIPPED the same night** — Gate 3.2-R5, 3.1-R5 and 3.2b-R3, declared in
`46f95e5` with no `.py` in it. Both instruments prove the doorway writes NOTHING
to stdout or stderr on EVERY path the pilot can see; the recorder builds month
two for every asset the gate names and reads every row back against a raw fetch,
**and must prove it appended rather than passing on a complete window.** All
three original attacks, re-run as real file edits, now FAIL with named
diagnostics. Production halves byte-identical by sha256; every diff hunk inside
`__main__`. 15/15, 14/14, 10/10.

**R-014 DOES NOT MOVE TO CLEARED. The session that found these three faults wrote
the repair for them and may not grade it. Filed as R-015.**

---

## R-015 — Gate 3.2-R5, 3.1-R5 and 3.2b-R3 were written by the session that failed their predecessors
**STATUS: OPEN · P1 · flagged 2026-07-28 (night) by the session that built the repair**

**What to review.** `_silence_checks` in both instruments — the check that the
doorway writes nothing to stdout or stderr on any path — and `_month_two` /
`_append_matches_source` in the recorder, which seed a partial window and read
every appended row back against a raw fetch. Plus the three new permanent
sabotages S15, F14 and B10. **Thirty-nine sabotages now live in three files and
all thirty-nine were invented by sessions that then defended against them.**

**Why it needs an outside eye.** **SIXTH GENERATION OF THE SAME STRUCTURE.**
R-001, R-009, R-010, R-011, R-013 and R-014 were each raised to catch exactly
this, and **every single time the next pair of eyes found something.** Six for
six. **Do not read that streak as proof the fix is finally good; read it as proof
that one mind grading its own gate has never once been enough on this ship.**

**FOUR SPECIFIC DOUBTS THIS SESSION COULD NOT SETTLE ABOUT ITS OWN WORK**,
offered as starting points and NOT as the assignment:

1. **MY OWN NEW CODE INHERITS R-014's DOUBT 1, AND I KNEW IT WHEN I SHIPPED IT.**
   `_raw_truth` and `_month_two` read `FAPI_BASE`, `HIST_PATH`, `PERIOD`, `LIMIT`
   and `TIMEOUT` straight out of the module they are judging. I argued to myself
   that those are the data source's coordinates rather than an expectation, and
   that widening the declared gate mid-flight is the R-001 failure running the
   other way. **That argument is convenient for me and was not reviewed by
   anybody. If `PERIOD` were changed to `1h`, the module and my "independent"
   truth would both follow it.**
2. **THE SILENCE CHECK PROVES THE DOORWAY IS SILENT; IT DOES NOT PROVE THE BRIEF
   IS.** I verified by reading `brief.py` that it prints only the returned
   strings. **Nothing checks that.** A future line added to `brief.py` itself —
   which no gate on this ship guards at all — would put anything on the pilot's
   screen with every gate green. **`cockpit/brief.py` HAS NO GATE. That is the
   larger hole my finding sits inside, and I did not close it.**
3. **MONTH TWO IS TESTED WITH ONE SEED SIZE, ONCE.** `SEED_ROWS = 100` out of
   ~180. Month three, a seed that already covers the newest row, a seed with a
   gap in the middle, and an append that crosses the 30-day window boundary are
   all untested. **I proved the append path is READ; I did not enumerate it.**
4. **THE 4h-BOUNDARY ALLOWANCE IS NEW AND ONLY IN MY CHECK.** `_month_two`
   accepts a row matching either the before or after snapshot. **I believe that
   cannot mask a real defect** — a transposed, rounded or cross-symbol figure
   matches neither — **but "I believe" is exactly the phrasing this file exists
   to catch, so it is filed.** The other checks in that gate still have the raw
   exposure R-013 doubt 3 named.

**Evidence.** Declaration `46f95e5` (`PROGRESS_LOG.md` only, no `.py` — check it
with `git show --stat 46f95e5`). The build commit after it. The two 2026-07-28
night `PROGRESS_LOG.md` entries.

**Reproduce.** `python cockpit\funding.py` (fifteen sabotages),
`python cockpit\fear_greed.py` (fourteen), `python data\open_interest.py` (ten).

**Then write a SIXTEENTH, a FIFTEENTH and an ELEVENTH of your own.** The question
that found this generation's three was *"every check inspects a return value, or
a file it just created from empty — what reaches the pilot's screen, or the
permanent dataset, without passing through the thing the gate inspects?"*
**Do not reuse it. It is now the direction these gates are strongest in, and the
two questions before it are already spent. Bring a third.**

**A clean verdict looks like.** A reviewer who did not build it invents at least
one NEW sabotage per part and finds it caught — or finds it escapes and says so.
**"The thirty-nine pass" is not a clean verdict; it is the claim under review.**

**Failed looks like.** Any new lie walks through — in which case the gates are
still shaped around their authors' imagination, six generations deep, and the
Commander should hear plainly that separation-in-time has stopped paying.

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

**AND, EARNED 2026-07-26: write "Failed looks like" as if a stranger will use
it against you.** R-001's own failure clause is what convicted R-001. The
session that wrote it could not see the hole, but it could describe the shape
of the hole — **and that description survived long enough for someone else to
find it.** That is what this file is for.

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
are assumed."* **It now has THREE earned examples** — the third being
`MAX_PLAUSIBLE_RATE = 0.05`, a guess that shipped and was only measured against
Binance's published cap (`/fapi/v1/fundingInfo`) on 2026-07-26, two steps later.

**A THIRD CANDIDATE, EARNED BY EXHIBIT A ON 2026-07-26 — his call, not a
session's:** *"A check is not proven until it has been deliberately broken. Any
gate that guards what the pilot reads ships with a sabotage exercise that
demonstrates it can FAIL."* Four of six sabotages passed Gate 3.2 while it was
reporting 48/48. **The tally was honest and the checks all ran; what nobody had
done was try to break them.**
