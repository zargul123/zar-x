# ZAR X PHASE 3 — **THE COMMANDER HAS GRANTED THE EXCEPTION AGAIN. YOU DO NOT ATTACK. YOU REPAIR S6 AND B1 AND YOU PROVE THEM.**

*Written 2026-08-03 by the fifteenth generation, on his direct ruling made the
same day. Read the exception below before anything else — **it changes what a
session is, for one session only.***

---

# **>>> THE EXCEPTION. READ THIS FIRST. IT IS HIS, NOT MINE.**

**`THE_PATTERN.md` says every session does PART 1 — ATTACK — then PART 2 — BUILD.
The Commander has suspended PART 1 for YOUR session and yours only.** He granted
this once before, on 2026-07-31; **the session it was granted to spent it on an
emergency instead and did not do the repairs, so he has granted it again.**

    YOUR SESSION:  NO ATTACK. NO HUNT. NO NEW SABOTAGE INVENTED.
                   Repair S6 and B1. Prove both. Explain both in plain words.

**HIS WORDS, 2026-08-03:** *"for next order i also want you to make the same
exemption only for next order to not attack and repair s6 and b1. the same orders
you have."*

**`THE_PATTERN.md` IS NOT EDITED — a rule suspended twice is still a rule
suspended, not a rule changed.** The session after you attacks again, as always.

## **WHAT WAS *NOT* SUSPENDED — DO NOT STRETCH THE EXCEPTION**

1. **YOU MAY NOT CLEAR YOUR OWN REPAIR.** You will fix two things; you file a
   review item against each of your own fixes and leave both OPEN. **That rule
   has caught twelve of thirteen repairs on this ship.**
2. **RE-RUNNING THE ORIGINAL FAULT AGAINST YOUR OWN REPAIR IS NOT "ATTACKING" —
   IT IS WHAT "FIXED" MEANS.** A repair nobody re-tested is a hope.
3. **THE GATE IS STILL DECLARED FIRST AND COMMITTED ALONE, WITH NO `.py` IN THAT
   COMMIT.** Twenty uses, survived audit every time — the twentieth was
   `3dc11e6` yesterday.

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The Commander is not a programmer and asked for it in this form. Write your
report to him the same way.*

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7  PASSED  exit 0  0 red  ~60 s
    cockpit/funding.py          GATE 3.2-R7  PASSED  exit 0  0 red  ~125 s
    data/open_interest.py       GATE 3.2b-R9 PASSED  exit 0  0 red  ~55 s
    data/collection_guard.py    GATE 3.2c-R1 PASSED  exit 0  0 red  ~10 s
    vault INTACT · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 222 lines each (221 rows), sha256
                      a1ed6729bef45be6 / a077cf034bf66c26 / c8d97f7122544f70
                      window 2026-06-27T16:00:00Z → 2026-08-03T08:00:00Z

**ALL FOUR INSTRUMENTS ARE CORRECT.** Both faults you are repairing are faults in
an **ALARM**, not in any number the Commander reads. **Say that plainly in your
report, because it is the thing he most needs to be sure of.**

## What happened in the two sessions before you

**The monthly recorder fired on 3 August, told Windows it had succeeded, and
collected nothing.** Six jobs did the same in the same second. The data was
recovered with three weeks to spare — 41 rows per asset, pushed as `5c7c54a`.
**Then R-037 was repaired under GATE 3.2c-R1:** the recorder is now **weekly**,
writes its **own log**, reports an **honest exit code**, and `CHECK_STATUS.bat`
shows **the archive's age instead of Windows' opinion of the job**.

**Neither ordered repair has ever landed. That is your entire job.**

## The problem you are fixing, in plain words

**Every gate on this ship works by breaking its own file on purpose and checking
the alarm notices.** That is what a "sabotage" is here. **Three times a sabotage
has turned out to break NOTHING** — the file was changed, the output came back
identical, and the gate reported *"my own lie escaped, I am decorative"* while
the instrument was perfectly healthy.

**A lie that changes nothing is not a lie. It is a red screen for no reason.**

    F10  (fear_greed)     — FIXED 2026-07-31. It holds; verified 2026-08-03.
    S6   (funding)        — OPEN. YOURS.
    B1   (open_interest)  — OPEN. YOURS.

**You are copying, not inventing. The answer already exists twice in this repo.**

---

# **JOB 1 — S6. THIS IS THE ONE COSTING HIM RED SCREENS.**

## What is wrong, exactly

`cockpit/funding.py` sabotage **S6** replaces `CONTRACTS` with a three-cycle:

    BTC-USD → SOLUSDT ·  ETH-USD → BTCUSDT ·  SOL-USD → ETHUSDT

**But the printed LABEL comes from the dictionary KEY, not the contract.** The
labels stay `BTC`, `ETH`, `SOL` in that order and only the RATES rotate. **The
printed block is byte-identical whenever all three rates format the same**, and
the gate prints:

    ✗ S6   CONTRACTS — tickers miswired   → ESCAPED — THE GATE IS DECORATIVE

**MEASURED, so you do not re-derive it:** over **6,441 real Binance settlements**
(BTCUSDT 7549 / ETHUSDT 7315 / SOLUSDT 6516 rows, 2019→2026) all three format
identically on **1,020 of them — 15.84%, one settlement in 6.3.** **HONEST LIMIT:
it is measured on SETTLED rates and the Brief prints the running ESTIMATE, so
15.84% is an UPPER BOUND, not the live figure. Do not quote it as the live one.**

**On 2026-08-03 S6 was scored CAUGHT — because the three live rates differed
(+0.0033% / -0.0013% / +0.0034%). That was luck, not a repair.**

## The repair, and the template is one file away

**`cockpit/fear_greed.py` already contains the answer.** The F10 repair's gate
section is titled **`2b) F10'S TWO BRANCHES (Gate 3.1-R7 a)`**. **Read it before
you write anything.** It proves THREE things on every run:

    ✓ values DIFFER      — the transposition speaks on its own
    ✓ values are EQUAL   — the REPAIR makes it speak anyway
    ✓ values are EQUAL, through the OLD form — it is a NO-OP, which is
                                               the whole defect

**Your S6 repair must produce the same three lines for the funding case:**

1. **When the three live rates differ**, S6 must change the block, as today.
2. **When all three live rates are identical**, the repair must make S6 change
   the block anyway — **using a number the GATE holds, never one read out of the
   file on trial** (R-014's lesson; S14 is what happens when it is ignored).
3. **The OLD form must still be exercised and REQUIRED to be a no-op**, so the
   defect is proved to exist rather than remembered.

**BOTH BRANCHES RUN EVERY TIME, ON EVERY MACHINE, WHATEVER THE MARKET IS DOING.**
Do not write a repair that only proves itself on a day the rates happen to differ
— **that is the same disease with the sign flipped.**

---

# **JOB 2 — B1. IT IS BLIND ON THE CLOUD, NOT ON HIS LAPTOP.**

## What is wrong, exactly

`data/open_interest.py` sabotage **B1** swaps `_utc_iso` for one that formats the
time as **LOCAL** instead of UTC. **On a machine whose clock is already UTC,
local time IS UTC, so the swap changes nothing** and the gate reports B1 escaped
while the recorder is perfectly correct.

**MEASURED: the Commander's laptop runs at UTC+5**, so **B1 works on his machine
and is NOT costing him red screens.** It is blind on **UTC machines — which the
cloud watchman almost certainly is.** **Fix it anyway: same twenty-minute shape
as S6. But do not tell him it was hurting him, because it was not.**

## The repair, and this template is also already in the repo

**`cockpit/funding.py` sabotage `S5` is the answer, and its author wrote the
reason down on 2026-07-28:**

> *"S5 shifts by a fixed hour rather than dropping the timezone: dropping it is a
> no-op on a machine already set to UTC, and a drill that only works on some
> machines is not a drill."*

**Make B1 shift by a FIXED AMOUNT rather than by "whatever this machine's clock
is."** Then:

1. **B1 must change the output on ANY machine, whatever the clock.**
2. **The OLD form must be exercised and REQUIRED to be a no-op under UTC** — the
   same third branch F10's repair prints.
3. **>>> AND THE ONE THAT MATTERS MOST: RUN YOUR FINISHED GATE WITH THE CLOCK SET
   TO UTC.** `TZ=UTC0` — **Windows Python honours it, measured.** A repair for a
   UTC-only fault never run on a UTC clock is not tested. **Run it BOTH ways —
   UTC+5 and UTC — and print both results.**

---

# THE RULES THAT APPLY TO BOTH REPAIRS

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` IN THE COMMIT, BEFORE WRITING CODE.** Then `git show --stat` proves the bar
preceded the work. **RECORD THAT HASH *AFTER* YOUR FINAL PUSH** — the cloud
watchman pushes every four hours and `git pull --rebase` can rewrite your own
hashes underneath you.

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, do not assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `open_interest.py` 243), AND a sha256 of the production
    half before and after, printed side by side. **THE RECIPE, PER FILE:**
    - `cockpit/funding.py`: **the raw byte prefix up to the
      `if __name__ == '__main__':` marker** (first N-1 lines joined by CRLF
      **WITH** a trailing CRLF) → `95069d1b…`
    - `data/open_interest.py`: first N-1 lines joined by CRLF with **NO**
      trailing separator → `5347bfec…`
    - **`open_interest.py` reproducing `5347bfec…` exactly is what proves your
      script is right. Check that one first, then trust the other.**
(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — the repaired breaks stay in, caught every run,
    originals restored and the restoration verified.
(d) **RE-RUN THE ORIGINAL FAULT AGAINST YOUR REPAIRED FILE.** For S6, force the
    three rates equal and show the gate goes GREEN where it went red. For B1, set
    the clock to UTC and show the same. **Show it failing for the reason it
    claims, not incidentally.**
(e) Everything the old gates did, they still do. **All 18 funding sabotages and
    all 14 recorder sabotages still caught.**
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST EACH OF YOUR OWN TWO REPAIRS AND LEAVE THEM
    OPEN.** You may not clear them. The session after you does that.
(i) **RUN `data/collection_guard.py --gate` BEFORE YOU FINISH.** It is new, it is
    fast, and nobody but its author has ever run it.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

## **IF THERE IS NOT ROOM, STOP — AND DO NOT APOLOGISE FOR IT**

    THE TWO REPAIRS ARE THE PROMISED RESULT AND THEY ARE THE WHOLE JOB.
    Do NOT start the news instrument. Do NOT attack anything. If you finish
    both repairs with room to spare, STOP and write good orders.
    A half-built part is worse than no part.

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. Clean first-time runs stand at
  +1h42m, +2h15m, +3h12m and +3h20m. **Outside a settlement window a red funding
  gate is a REAL failure — treat it as one.**
- **`python cockpit\funding.py` ALSO GOES RED ON S6 ROUGHLY ONE SETTLEMENT IN
  SIX** — **that is the thing you are here to fix.** Check section 1: if all
  three rates print the same, that is R-034 and not your breakage.
- **`data/open_interest.py` SCORES B1 AS CAUGHT ON THIS LAPTOP** because it runs
  at UTC+5. That is R-031 hiding, not R-031 absent.
- **IF `cockpit/fear_greed.py` GOES RED ON F10, THAT IS A REGRESSION OF A REPAIR
  AND IT IS SERIOUS** — it cannot happen unless someone undid it.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER.** That is R-041 doubt 3 — a formatted age straddling a
  rounding boundary. **Filed by its author before it ever happened. If it goes
  red TWICE in a row, it is real.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT. R-025 IS CLEARED.** The residue is R-033, still open.
5. **F10 was repaired on his ruling and it holds.**
6. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
7. **R-037 WAS ORDERED SORTED FIRST AND IT WAS.** Done 2026-08-03.
8. **THE EXCEPTION AT THE TOP OF THIS FILE IS HIS, made 2026-08-03, ONE SESSION
   ONLY — YOURS.**

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment and the housekeeping that has bitten this ship. None of it is
repeated here.**

1. **`REVIEW_QUEUE.md` — R-034 (S6) and R-031 (B1) are your entire worklist.**
   Both carry the measurements. **R-006 may NEVER be cleared by you or any
   in-house session.**
2. **The `2b) F10'S TWO BRANCHES` section of `cockpit/fear_greed.py`'s
   `__main__`** — your template for S6, already shipped and already green.
3. **The `S5` comment in `cockpit/funding.py`'s `_SABOTAGES` list** — your
   template for B1, in its author's own words.
4. **The LAST THREE entries of `PROGRESS_LOG.md`.** The file is ~545 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 28 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline. **THE FIFTEENTH
  GENERATION LOST TWO COMMANDS TO EXACTLY THIS on 2026-08-03, in a session that
  had already read this warning. Write the script to a FILE and run the file.**
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1** — the 2026-07-19 incident, and it happened again
  on 2026-08-03 to a session that had read `.gitattributes` an hour earlier.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Six consecutive sessions have guarded this way; it fired correctly on
  2026-08-03 and saved a bad splice.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first. `py_compile` before the gate.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`, `Â·`,
  `â†`, `Ã`, `âœ`. **MEASURED: `PROGRESS_LOG.md` holds 7 pre-existing hits, all
  deliberate quotations. Compare your counts against `git show HEAD:<file>` so
  you know whether YOU added any** — cheaper and surer than eyeballing.
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
  `schtasks` reported result 0 for a job that did nothing, and a status screen
  printed that 0 as OK.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR, AND IT IS THE ONLY THING HE
   PERSONALLY OWES THIS REPAIR.** The Task Scheduler event log is **switched
   off**, which is why the cause of 11:47:41 is unprovable and always will be.
   Enabling it costs nothing and means a next time leaves evidence:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

   **A session cannot do this — it needs Administrator and no session should
   elevate silently.**
2. **>>> R-038 HAS A DEADLINE OF ABOUT 2026-09-02 AND YOUR EXCEPTION PUSHES IT
   BACK.** The 123 rows appended on 3 August can only be checked against Binance
   while they remain inside the rolling 30-day window. **The session you granted
   the exception to will not check them, so the session AFTER it must.** **He was
   told this plainly when he granted the exception; there is still time, but it
   is now the first job of the session after next.**
3. **THE CATEGORY B PILE IS SIXTEEN DEEP** — R-039, R-040, R-041 added.
   **It has grown every session since it was created and has NEVER once shrunk.**
   Cleared before the ship is used for real, at the same moment `brief.py` gets
   its gate. **Somebody should say the number out loud to him each time.**
4. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED BY THREE FILES AND FIVE
   SESSIONS:** *"A SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS
   VERDICT MEANS ANYTHING."* **F10, B1 and S6 are the same fault in three files,
   and `collection_guard.py` was built with it from birth.** **A session may
   never promote its own idea to law. It is his and only his.** **THIRTEEN OTHER
   CANDIDATES REMAIN UNADOPTED.**
5. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT (R-041 doubt 5).** If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. **The batch header says WEEKLY in words; that is documentation, not a
   check.**
6. **NOBODY HAS EVER ASKED WHETHER A SOURCE ITSELF CAN LIE (R-035).** No file on
   this ship talks to more than one source. **Every gate proves the printed line
   matches what the source SENT; nothing asks whether the source was RIGHT.**
   **His own words: fake data on his screen in real time, and the only door with
   nobody standing at it.** **Recommended as the next real attack.**
7. **THE NEWS INSTRUMENT IS STILL UNBUILT** and now third in line. Everything is
   in `git show 5e6d306:SESSION_ORDERS.md` and `EXECUTION_PLAN.md` Phase 3 step
   3. **Measure R-036 before any code.**
8. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
9. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this class is `symbols=None`, resolved in the body — `funding.py` already does
   it that way, and `collection_guard.py` was written that way from birth.** It
   touches what the pilot reads, so no session may make it during a repair to a
   test. **Ten generations have fixed the instance and left the pattern.**
10. **`cockpit/brief.py` HAS NO GATE** — he has ruled: not now, before going live.
11. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
12. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
13. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
14. **The settled-rate anchor (R-004)** — returned to him on correct facts.
15. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
16. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SEVEN TIMES, NOT ADOPTED.**
17. **BOTH COCKPIT GATES ARE SLOW BECAUSE OF DOOR 3** — ~125 s and ~60 s — **and
    that slowness turned out to be load-bearing** (R-033). **Making them faster is
    no longer a free change and somebody must say so if he asks.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.**
