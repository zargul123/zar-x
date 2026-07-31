# ZAR X PHASE 3 — **THE COMMANDER HAS ORDERED AN EXCEPTION. YOU DO NOT ATTACK. YOU REPAIR TWO THINGS AND YOU PROVE THEM.**

*Written 2026-07-31 (evening) on the Commander's direct ruling, by the
fourteenth generation. **I found S6. I am ordering its repair and I may not
judge that repair.** Read the exception below before anything else — **it changes
what a session is, for one session only.***

---

# **>>> THE EXCEPTION. READ THIS FIRST. IT IS THE COMMANDER'S, NOT MINE.**

**`THE_PATTERN.md` says every session does PART 1 — ATTACK — and then PART 2 —
BUILD. On 2026-07-31 (evening) the Commander suspended PART 1 for the next
session and only the next session.** His reason, in his own terms: he is tired of
sessions that hunt, and **two false alarms are costing him red screens on a ship
whose numbers are correct.**

    THIS SESSION:  NO ATTACK. NO HUNT. NO NEW SABOTAGE INVENTED.
                   Repair S6 and B1. Prove both. Explain both in plain words.

**HE SAID IT IS A ONE-TIME EXCEPTION AND THAT THE USUAL PRACTICE STANDS FOR
EVERY BUILD AFTER THIS ONE. I HAVE THEREFORE NOT EDITED `THE_PATTERN.md`,**
because the rule has not changed — it has been suspended once, by the only person
who may suspend it. **The session after you attacks again, as always.**

## **WHAT WAS *NOT* SUSPENDED — DO NOT STRETCH THE EXCEPTION**

1. **YOU MAY NOT CLEAR YOUR OWN REPAIR.** You will fix two things; you file a
   review item against each of your own fixes and leave both OPEN. **That rule
   was not suspended and it is the one that has caught twelve of thirteen
   repairs on this ship.**
2. **RE-RUNNING THE ORIGINAL ATTACK AGAINST YOUR OWN REPAIR IS NOT "ATTACKING" —
   IT IS WHAT "FIXED" MEANS.** A repair nobody re-tested is a hope. Do it.
3. **THE GATE IS STILL DECLARED FIRST AND COMMITTED ALONE, WITH NO `.py` IN THAT
   COMMIT.** Nineteen uses, survived audit every time.

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The Commander is not a programmer and asked for it in this form. Write your
report to him the same way.*

## Where the ship is

    cockpit/funding.py      GATE 3.2-R7  PASSED  exit 0  0 red  122 s
    cockpit/fear_greed.py   GATE 3.1-R7  PASSED  exit 0  0 red   62 s
    data/open_interest.py   GATE 3.2b-R9 PASSED  exit 0  0 red   56 s
    vault INTACT 6/6 · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 181 lines each, sha256 e3258e82… / 1549a8a1… /
                      e0f91a87… — byte-identical since 2026-07-30

**THE INSTRUMENTS ARE CORRECT AND HAVE NEVER BEEN IN QUESTION.** Both faults you
are repairing are faults in the **ALARM**, not in the numbers the Commander
reads. **Say that plainly in your report, because it is the thing he most needs
to be sure of.**

## The problem you are fixing, in plain words

**Every gate on this ship works by breaking its own file on purpose and checking
the alarm notices.** That is what a "sabotage" is here. **Three times now a
sabotage has turned out to break NOTHING** — the file was changed, the output
came back identical, and the gate reported *"my own lie escaped, I am
decorative"* while the instrument was perfectly healthy.

**A lie that changes nothing is not a lie. It is a red screen for no reason.**

    F10  (fear_greed)  — FIXED 2026-07-31 morning, on the Commander's ruling.
    S6   (funding)     — OPEN. YOURS.
    B1   (open_interest) — OPEN. YOURS.

**And you are the first session that gets to fix these knowing that the answer
already exists twice over in this repo. You are copying, not inventing.**

---

# **JOB 1 — S6. THIS IS THE ONE COSTING HIM TIME RIGHT NOW.**

## What is wrong, exactly

`cockpit/funding.py` sabotage **S6** replaces `CONTRACTS` with a three-cycle of
the tickers:

    BTC-USD → SOLUSDT ·  ETH-USD → BTCUSDT ·  SOL-USD → ETHUSDT

**But the printed LABEL comes from the dictionary KEY, not the contract.** So the
labels stay `BTC`, `ETH`, `SOL` in that order and only the RATES rotate.
**The printed block is therefore byte-identical whenever all three rates format
the same** — and the gate, seeing no change, prints:

    ✗ S6   CONTRACTS — tickers miswired   → ESCAPED — THE GATE IS DECORATIVE

**MEASURED, so you do not re-derive it:** over **6,441 real Binance settlements**
(BTCUSDT 7549 / ETHUSDT 7315 / SOLUSDT 6516 rows, 2019→2026) all three format
identically on **1,020 of them — 15.84%, one settlement in 6.3.** Most recently
**2026-06-02 00:00 UTC**, all three at `+0.0100%`. **HONEST LIMIT ON THAT NUMBER:
it is measured on SETTLED rates and the Brief prints the running ESTIMATE, so
15.84% is an UPPER BOUND, not the live figure. Do not quote it as the live one.**

## The repair, and the template is one file away

**`cockpit/fear_greed.py` already contains the answer.** The F10 repair, shipped
2026-07-31 morning, does exactly this and its gate section is titled
**`2b) F10'S TWO BRANCHES (Gate 3.1-R7 a)`**. **Read it before you write
anything.** It proves THREE things on every single run:

    ✓ values DIFFER      — the transposition speaks on its own
    ✓ values are EQUAL   — the REPAIR makes it speak anyway
    ✓ values are EQUAL, through the OLD form — it is a NO-OP, which is
                                               the whole defect

**Your S6 repair must produce the same three lines for the funding case:**

1. **When the three live rates differ**, S6 must change the block, as it does
   today.
2. **When all three live rates are identical**, the repair must make S6 change
   the block anyway — **using a number the GATE holds, never one read out of the
   file on trial** (that is R-014's lesson and S14 is what happens when it is
   ignored).
3. **The OLD form must still be exercised and REQUIRED to be a no-op**, so the
   defect itself is proved to exist rather than remembered.

**BOTH BRANCHES RUN EVERY TIME, ON EVERY MACHINE, WHATEVER THE MARKET IS DOING
THAT MORNING.** Do not write a repair that only proves itself on a day the rates
happen to differ — **that is the same disease with the sign flipped.**

---

# **JOB 2 — B1. IT IS BLIND ON THE CLOUD, NOT ON HIS LAPTOP.**

## What is wrong, exactly

`data/open_interest.py` sabotage **B1** swaps the timestamp helper `_utc_iso` for
one that formats the time as **LOCAL** time instead of UTC. **On a machine whose
clock is already UTC, local time IS UTC, so the swap changes nothing** and the
gate reports B1 escaped while the recorder is perfectly correct.

**MEASURED 2026-07-31: the Commander's laptop runs at UTC+5**, so **B1 is working
correctly on his machine and is NOT the one costing him red screens.** It is
blind on **UTC machines — which is what the cloud watchman almost certainly is.**
**Fix it anyway: it is the same twenty-minute shape as S6 and coming back for it
later is silly. But do not tell him it was hurting him, because it was not.**

## The repair, and this template is also already in the repo

**`cockpit/funding.py` sabotage `S5` is the answer, and its author wrote the
reason down in a comment on 2026-07-28:**

> *"S5 shifts by a fixed hour rather than dropping the timezone: dropping it is a
> no-op on a machine already set to UTC, and a drill that only works on some
> machines is not a drill."*

**That session understood this disease three days before it was named, defended
against it in one file, and nobody carried the defence to the other two.**

**Make B1 shift by a FIXED AMOUNT rather than by "whatever this machine's clock
is."** Then:

1. **B1 must change the output on ANY machine, whatever the clock.**
2. **The OLD form must be exercised and REQUIRED to be a no-op under UTC** — the
   same third branch F10's repair prints.
3. **>>> AND THE ONE THAT MATTERS MOST HERE: RUN YOUR FINISHED GATE WITH THE
   CLOCK SET TO UTC.** `TZ=UTC0` — **Windows Python honours it, measured.** A
   repair for a UTC-only fault that was never run on a UTC clock is not tested.
   **Run it BOTH ways — UTC+5 and UTC — and print both results.**

---

# THE RULES THAT STILL APPLY TO BOTH REPAIRS

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves
the bar preceded the work.

**AND RECORD THAT HASH *AFTER* YOUR FINAL PUSH, NOT WHEN YOU WRITE THE ENTRY.**
The cloud watchman pushes every four hours, so `git pull --rebase` before your
push can rewrite your own commit hashes underneath you.

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, do not assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `open_interest.py` 243), AND a sha256 of the production
    half before and after, printed side by side. **THE RECIPE, PER FILE:**
    - `cockpit/funding.py`: **the raw byte prefix up to the
      `if __name__ == '__main__':` marker** (first N-1 lines joined by CRLF
      **WITH** a trailing CRLF) → `95069d1b…`.
    - `data/open_interest.py`: first N-1 lines joined by CRLF with **NO**
      trailing separator → `5347bfec…`.
    - **`open_interest.py` reproducing `5347bfec…` exactly is what proves your
      script is right. Check that one first, then trust the other.**
(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — the repaired breaks stay in, caught every run,
    originals restored and the restoration verified.
(d) **RE-RUN THE ORIGINAL FAULT AGAINST YOUR REPAIRED FILE.** For S6, force the
    three rates equal and show the gate now goes GREEN where it used to go red.
    For B1, set the clock to UTC and show the same. **Show it failing for the
    reason it claims, not incidentally.**
(e) Everything the old gates did, they still do. **All 18 funding sabotages and
    all 14 recorder sabotages still caught.**
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST EACH OF YOUR OWN TWO REPAIRS AND LEAVE THEM
    OPEN.** You may not clear them. The session after you does that.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **AFTER THE REPAIRS: THE NEWS INSTRUMENT — CONDITIONAL, AND ONLY IF THERE IS ROOM**

**FIRST, CHECK THE KEY:**

    read the key NAMES in .env  —  is there a CryptoPanic token?

**THERE WAS NOT ONE ON 2026-07-31.** `.env` held exactly `TWELVEDATA_API_KEY`.
Unauthenticated the API answers **HTTP 403** and **HTTP 404**. The Commander was
asked to sign up — free, five minutes, cryptopanic.com.

    NO KEY .......... build NOTHING. Do not substitute another news source.
                      The orders name CryptoPanic and the orders outrank a
                      session's own ideas. Put it back on his desk.
    KEY, AND THE TWO REPAIRS ARE DONE AND GREEN, AND YOU HAVE REAL TIME LEFT
                   .. begin Context Deck instrument 3. EXECUTION_PLAN Phase 3
                      step 3. HEADLINES ONLY, no sentiment score, no invented
                      weights, the cut ghost stays cut.
    ANY DOUBT ....... **STOP AND LEAVE IT.** A half-built instrument is worse
                      than no instrument, and the Commander was told plainly
                      that repairs plus a full news build is TWO sessions, not
                      one. **Delivering two solid repairs is a complete,
                      successful session. Say so without apologising.**

**IF YOU DO BUILD IT: DOOR 1, DOOR 2 AND DOOR 3 FROM BIRTH**, a sabotage drill
from birth, **and every sabotage proved able to CHANGE THE OUTPUT before its
verdict counts** — which is the entire lesson of the two repairs you just made.
**And do not copy Door 3's pass line verbatim: it claims "nothing was deferred to
a thread" and tests only non-daemon threads (R-033). Write what you actually
test.**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. Three clean first-time runs stand
  at +1h42m, +2h15m and +3h12m. **Outside a settlement window a red funding gate
  is a REAL failure — treat it as one.**
- **`python cockpit\funding.py` ALSO GOES RED ON S6 ROUGHLY ONE SETTLEMENT IN
  SIX** — **that is the thing you are here to fix.** Check section 1 of the
  output: if all three rates print the same, that is R-034 and not your breakage.
- **IF `cockpit\fear_greed.py` GOES RED ON F10, THAT IS A REGRESSION OF A REPAIR
  AND IT IS SERIOUS** — it cannot happen unless someone undid it.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT. R-025 IS CLEARED.** The residue is R-033, still open.
5. **F10 was repaired on his ruling of 2026-07-31 morning and it holds.**
6. **THE EXCEPTION AT THE TOP OF THIS FILE IS HIS, made 2026-07-31 evening,
   ONE SESSION ONLY.**

---

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment and the housekeeping that has bitten this ship. None of it is
repeated here. I did NOT edit it — see the exception above for why.**

**Specific to THIS job:**

1. **`REVIEW_QUEUE.md` — R-034 (S6) and R-031 (B1) are your entire worklist.**
   Both carry the measurements. **R-006 may NEVER be cleared by you or any
   in-house session.**
2. **The `2b) F10'S TWO BRANCHES` section of `cockpit/fear_greed.py`'s
   `__main__`** — your template for S6, already shipped and already green.
3. **The `S5` comment in `cockpit/funding.py`'s `_SABOTAGES` list** — your
   template for B1, and the reason written in the author's own words.
4. **The LAST TWO entries of `PROGRESS_LOG.md`.** The file is ~515 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 28 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline. **The fourteenth
  generation lost a run to `\n` surviving two levels of quoting; an assertion on
  the bare-LF count caught it before it wrote anything.**
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Four consecutive sessions guarded, never once wrong.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first. `py_compile` before the gate.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`, `Â·`,
  `â†`, `Ã`, `âœ`. **Ignore hits inside backticks; five in `PROGRESS_LOG.md` are
  deliberate quotations of old damage.**
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.

---

# THE 1 AUGUST ERRAND — **OVERDUE. CHECK THE DATE ANYWAY.**

**On 2026-07-31 it was NOT due — `date -u` read 11:11 UTC, 31 July — and that
cost one command.** If you are reading this on 1 August or later, **it has fired
and you must read the result.**

**WRITE DOWN WHAT YOU EXPECT BEFORE YOU OPEN THE LOG.**

    MEASURED, so you do not re-derive it:
    The recorder has run EXACTLY ONCE in its whole history — by hand, on
    2026-07-27 — and appended ZERO rows. THE COMMIT-AND-PUSH BRANCH HAS
    THEREFORE STILL NEVER FIRED FOR REAL.
    A healthy run appends 12 rows per asset and reports 192 stored.
    The honest figure on 1 August is roughly THIRTY new rows per asset and a
    stored count near 210 — NOT 180, and NOT 360.
    The archive stood at 181 lines per file, sha256 e3258e82… / 1549a8a1… /
    e0f91a87…, verified unchanged on 2026-07-31 afternoon.

**Open `journal/daily_runs.log` and tell the Commander PLAINLY whether the task
committed and pushed real new rows.** **If the log says something you did not
predict, that is a finding, not a relief.**

**AND, EARNED BY B14: confirm `data/oi_history/` holds exactly THREE files named
`BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`, `SOLUSDT_4h.csv`.** A fourth file, or a
different name, is B14 arriving for real. **There were exactly three on
2026-07-31.** **Do not assume it worked because a task returned 0** — `schtasks`
already reported SUCCESS once for a task that could never run. **Count the rows
yourself**, and note that `count('\n') + 1` overcounts a file ending in a newline.

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you repaired, the actual output before
and after, and **every prediction you got wrong.** **AND THE STANDING DUTY: if
you catch yourself writing "probably", "almost certainly" or "this should be
fine" about anything that ships — FILE IT in `REVIEW_QUEUE.md` before the commit
that ships it.**

**Do the closing ritual exactly as `THE_PATTERN.md` sets it out** — seven steps,
ending with the next session's orders, the push, and your plain-words report.
**Your orders for the session after you must restore the normal rhythm: PART 1
ATTACK, then PART 2 BUILD. The exception was for you only.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> THE FREE CRYPTOPANIC TOKEN. Five minutes, and it is the only thing
   standing in front of the third instrument.** Unauthenticated the API answers
   403 and 404, and no session can create an account. **Eight sessions have not
   built step 3 and this is the first time the reason is not a finding.**
2. **>>> THE RULE HE HAS NOT YET ADOPTED, NOW EARNED BY THREE FILES AND FOUR
   SESSIONS:** *"A SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS
   VERDICT MEANS ANYTHING."* **F10, B1 and S6 are the same fault in three
   different files.** He has now ordered two of them repaired **as an
   exception** — **but the RULE itself is still not adopted, so nothing stops a
   fourth.** **A session may never promote its own idea to law. It is his and
   only his.** **THIRTEEN OTHER CANDIDATES REMAIN UNADOPTED.**
3. **THE ATTACK NOBODY HAS EVER MADE, AND IT IS THE ONE THAT MATCHES WHAT HE SAID
   HE CARES ABOUT.** Measured 2026-07-31: **no file on this ship talks to more
   than one source.** Fear & Greed comes from alternative.me alone, funding from
   Binance alone, prices from TwelveData alone. **Every gate proves the printed
   line matches what the source SENT. Nothing anywhere asks whether the source
   was RIGHT.** If a source served a wrong number, the Brief would print it in
   perfect confidence and every alarm would stay green. **That is fake data on
   his screen in real time — his own words — and it is the only door with nobody
   standing at it.** **Recommended as the next real attack, after the news build.**
4. **THE CATEGORY B PILE IS ELEVEN DEEP** and drops to nine when your two repairs
   land. **It is cleared before the ship is used for real, at the same moment
   `brief.py` gets its gate.**
5. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
6. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this class is `symbols=None`, resolved in the body — `funding.py` already does
   it that way.** It touches what the pilot reads, so no session may make it
   during a repair to a test. **Nine generations have fixed the instance and left
   the pattern.**
7. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL NEW
   ROWS. THE ERRAND IS OVERDUE.**
8. **`cockpit/brief.py` HAS NO GATE** — he has ruled: not now, before going live.
9. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
10. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
11. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
12. **The settled-rate anchor (R-004)** — returned to him on correct facts.
13. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
14. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SIX TIMES, NOT ADOPTED.**
15. **BOTH COCKPIT GATES ARE SLOW BECAUSE OF DOOR 3** — 122 s and 62 s — **and
    that slowness turned out to be load-bearing** (R-033). **Making them faster
    is no longer a free change and somebody must say so if he asks.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.**
