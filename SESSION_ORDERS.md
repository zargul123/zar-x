# ZAR X PHASE 3 — **PART 2 IS BLOCKED ON A FREE SIGNUP. CHECK WHETHER HE DID IT, THEN BUILD OR ATTACK ACCORDINGLY. AND THE 1 AUGUST ERRAND IS NOW OVERDUE.**

*Written 2026-07-31 (afternoon) by the fourteenth generation — the session that
attacked Door 3, found one blind spot in it, swept the third file for the disease
that had already been found in two, and then **could not build instrument 3
because there is no CryptoPanic key on this machine.** I built nothing and
repaired nothing. **Both my findings graded SMALL and neither of them is why
Part 2 did not happen.***

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The rest of this file is exact bars and commands. This part is the story, so
you know WHY before you read WHAT. The Commander is not a programmer and asked
for it in this form. Write your report to him the same way.*

## Where the ship is

    cockpit/funding.py      GATE 3.2-R7  PASSED  exit 0  0 red  122 s
    cockpit/fear_greed.py   GATE 3.1-R7  PASSED  exit 0  0 red   62 s
    data/open_interest.py   GATE 3.2b-R9 PASSED  exit 0  0 red   56 s
    vault INTACT 6/6 · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 181 lines each, sha256 e3258e82… / 1549a8a1… /
                      e0f91a87… — byte-identical since 2026-07-30

**Everything was green when I arrived and everything is green now. No `.py` file
was edited this session.** The only change in my commit is the five documents.

## What happened, in four paragraphs

**I ATTACKED DOOR 3 AND IT MOSTLY HELD.** I invented shape **A5** — shape A1 with
**one word changed**, `daemon=False` → `daemon=True` — and let **Door 3's own
judge** score it. A1, A2, A3 and A4 were caught. **A5 escaped.** A daemon thread
is not joined when the interpreter shuts down, so the child kills it and exits
clean. **Door 3's comment says truthfully that shutdown "joins non-daemon
threads"; the line it PRINTS when it passes says "nothing was deferred to a
thread."** Those are different sentences and only the first one is tested.

**THEN I DID THE THING THAT MATTERS MORE, AND IT COST ME MY OWN FINDING.** I
planted A5 in the production path and ran the real Brief — **and nothing
appeared.** My own sabotage was inert, which is the exact disease I had come to
sweep for, committed by me within an hour of reading about it. So I measured the
window instead of arguing about it: **Door 3's child stops watching 0.5-1.0 s
after the doorway; the Commander's Brief is still on screen until 1.5-2.0 s.** I
predicted a shape in that band would sail through the whole gate. **It does not
— Door 1 catches it, by accident, because the gate calls the doorway dozens of
times.** Measured red at 1.25 s and 1.75 s. **I recorded that instead of grading
on my prediction, which is what would have turned a SMALL into a BORDERLINE.**

**THE SWEEP OF THE THIRD FILE FOUND THE F10/B1 DISEASE AGAIN AND WORSE.**
`funding.py`'s **S6** miswires the tickers in a three-cycle, but the printed
LABEL comes from the dictionary KEY — so **the block is byte-identical whenever
all three rates format the same.** Measured over 6,441 real Binance settlements:
**15.84%. One day in 6.3.** Most recently 2026-06-02, all three at +0.0100%.
**Seventeen of the eighteen swept clean and I say so plainly.**

**AND THEN PART 2 STOPPED DEAD.** Both findings are CATEGORY B, and the
Commander's own three questions say CATEGORY B does not stop the building — **so
I went to build instrument 3 and found there is no CryptoPanic key.** `.env`
holds `TWELVEDATA_API_KEY` and nothing else; unauthenticated the API returns
**403** and **404**. **Every gate here measures a printed line against a raw
fetch. With no fetch there is nothing to measure against.**

## **WHAT YOU MUST CHECK BEFORE YOU PLAN ANYTHING — IT DECIDES YOUR WHOLE SESSION**

    grep -c CRYPTOPANIC .env      (or just read the key names)

**IF A CRYPTOPANIC TOKEN IS NOW IN `.env`, HE HAS DONE IT AND YOUR PART 2 IS
BUILD INSTRUMENT 3.** If it is still not there, **do NOT invent a data source and
do NOT build a gate against invented data.** Do Part 1, attack hard, and put the
key back on his desk in your report — **that is the whole ask and it is one free
signup at cryptopanic.com.**

## **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

**`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT. R-021,
CATEGORY B, SMALL.** Binance settles at **00:00, 08:00 and 16:00 UTC**. Three
clean first-time runs now stand at **+1h42m, +2h15m and +3h12m** past a
settlement. **OUTSIDE A SETTLEMENT WINDOW, A RED FUNDING GATE IS A REAL FAILURE.
TREAT IT AS ONE.** Check the clock, run it again, say how many runs it took.

**AND NOW A SECOND ONE, WHICH IS MINE: `python cockpit\funding.py` WILL ALSO GO
RED ON `S6` ON ROUGHLY ONE SETTLEMENT IN SIX**, whenever BTC, ETH and SOL funding
all print the same percentage. **That is R-034, it is CATEGORY B, and the
instrument is CORRECT when it happens.** Check the three rates in section 1 of
the output: if they are identical, that is R-034 and not your breakage.

**IF `cockpit\fear_greed.py` GOES RED ON F10, THAT IS A REGRESSION OF THE
THIRTEENTH GENERATION'S REPAIR AND IT IS SERIOUS** — it cannot happen unless
someone undid it. It did not happen to me.

## **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT AND R-025 IS NOW CLEARED** — by me, on the limb it filed,
   after attacking it. **The residue is R-033 and R-033 is still open.**
5. **F10 was repaired on his ruling of 2026-07-31 and it holds.**

## Your job, in order

**1. ATTACK. Pick from the list below — R-033 and R-032 are the richest.**

**2. PART 2, CONDITIONAL: if the CryptoPanic key exists, build Context Deck
instrument 3. If it does not, build nothing and say why.**

**3. THE 1 AUGUST ERRAND IS NOW OVERDUE. IT WAS NOT DUE ON MY WATCH AND I
CHECKED, WHICH COST ONE COMMAND.** Details below.

---

## READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is for,
the run environment and the housekeeping that has bitten this ship. None of it is
repeated here. I did NOT edit it.**

**Specific to THIS job:**

1. **The LAST entry of `PROGRESS_LOG.md`** — mine. **Read it as a CLAIM, not a
   result.** The file is ~510 KB; reading all of it will eat your budget.
2. **`REVIEW_QUEUE.md` — R-033 and R-034 are new and both are mine**, plus R-032
   (nine of ten doubts still untested) and R-029/R-030/R-031 if you have room.
   **R-006 may NEVER be cleared by you or any in-house session.**
3. **`cockpit/fear_greed.py`, the `__main__` half only** — `_door3_probe`,
   `GATE_DOOR3_SHAPES`, `_door3_drill`, and the `_capture` ear above them.
4. **`ROADMAP.md`** — the MEASURED facts table, which I added a block to. If
   anything you measure disagrees with it, **your measurement wins and you write
   the correction down.**

---

# LOCK THE BARS BEFORE YOU RUN ANYTHING

Write these into your working notes first so they cannot soften as you go:

1. A new sabotage, invented by you, thrown at something you did not build,
   **and PROVED ABLE TO CHANGE THE OUTPUT before its verdict means anything.**
   Result recorded either way.
2. **THE QUESTION I COULD NOT ANSWER AND NOBODY HAS: R-032 DOUBT 2.** Door 3
   judges the child on `stdout + stderr` of a **pipe**. **What happens to a write
   that goes to the real console device, to descriptor 3, or through a re-opened
   `CONOUT$`?** Nobody on this ship knows. It is a Windows-specific question with
   a definite answer and it is one experiment.
3. Any leak graded on THE FINDING REPORT **before** any repair, using **the
   Commander's three questions and his wording of Step 2.2**, repaired only if
   that grade says to.
4. `lab/` byte-identical, vault INTACT 6/6, Brief 3/3, and **exactly THREE files
   in `data/oi_history/`** named `BTCUSDT_4h.csv`, `ETHUSDT_4h.csv`,
   `SOLUSDT_4h.csv`. **A fourth file, or a different name, is B14 arriving for
   real.** After the 1 August run they should be **~211 lines each, NOT 181.**

**Four of four or it has not cleared, and "three of four with a good
explanation" is the phrasing this ship exists to refuse.**

---

# PART 1 — WHAT TO ATTACK, RICHEST FIRST

## **A. R-032 DOUBT 2 — THE ONE NOBODY HAS ANSWERED. START HERE.**

Door 3 runs the child with `capture_output=True` and judges `stdout + stderr`.
**On Windows a child of a console process inherits that console.** So a shape
that opens `CONOUT$` and writes to it, or writes to a descriptor the pipe does
not own, **may reach the Commander's terminal while Door 3 sees an empty pipe.**
**Its author wrote "I planted none of those and I do not know the answer."
Neither do I.** One experiment settles it. **And if it escapes, ask the second
half immediately: does it also reach the real `cockpit\brief.py` screen?** Mine
did not, and that is the difference between a note and a finding.

## **B. R-033 — MY OWN NEW ITEM. THE BACKSTOP IS UNMEASURED.**

Door 1 currently catches what Door 3 misses, **by accident**. I measured it red
at 1.25 s and 1.75 s. **Nobody knows its ceiling.** And the funding instrument's
equivalent protection is **the ORDER OF TWO LINES in `brief.py`** — line 90 calls
the Fear & Greed doorway, line 91 the funding one, so funding has almost no
process life after it. **Swap them and funding inherits the 1.5-second window.
Nothing anywhere tests that order.** That is a check somebody could write.

## **C. THE SWEEP NOBODY HAS FINISHED.** I swept `funding.py`'s eighteen and found
S6. **`fear_greed.py`'s sixteen and `open_interest.py`'s fourteen have only ever
been swept where a red gate forced it (F10, B1).** Go through them deliberately:
*is there a data or environment condition under which this changes nothing?*

## **D. THE ENVIRONMENT.** The twelfth generation's best attack edited no file at
all — it changed `TZ` and the gate went red. **Windows Python honours `TZ`,
measured.** Ask what else the gates silently depend on: locale, `PYTHONHASHSEED`,
console code page, a `__pycache__` that outlives an edit, `PYTHONPATH`.

## HOW TO ATTACK PROPERLY

- **BRING A NEW QUESTION. TWELVE ARE NOW SPENT.** *"Which paths has nobody
  attacked?"* · *"Where does the gate take the module's word?"* · *"Is the gate
  looking at the right object at all?"* · *"What is the gate's own detector deaf
  to?"* · *"What shape does the real world have that the gate's world cannot?"* ·
  *"What if the module puts its work somewhere the gate is not looking?"* ·
  *"What happens BEFORE the gate is alive to watch?"* · *"Is the sabotage
  actually IN EFFECT when the judge runs?"* · *"WHEN does the gate stop watching,
  and what does the part do after that?"* · *"WHOSE CODE does the swap reach?"* ·
  *"CAN THE SABOTAGE EXPRESS THE LIE, OR DOES THE DATA MAKE IT A NO-OP?"* ·
  **and now mine:** *"THE CHILD DIES IN ONE SECOND AND THE PILOT LIVES FOR A
  MINUTE — WHAT WRITES IN BETWEEN?"* **All twelve are the directions these gates
  are now strongest in. Reusing one is the approach most likely to find nothing.**
- **Write what you will try and what you PREDICT, BEFORE you run it.** I wrote
  six. **Four right, two wrong — and both wrong ones made the session better,**
  because one proved my own sabotage was inert and the other cost me a severity
  grade I would otherwise have claimed.
- **>>> AND THE ONE THE LAST TWO SESSIONS BOTH EARNED THE HARD WAY: A SABOTAGE
  MUST BE PROVED ABLE TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING.**
  Run it against the REAL `cockpit\brief.py`, not only against a gate. **I did
  this and it destroyed my first result, which is exactly what it is for.**
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; it costs nothing
  (28 MB). Check `git status` is clean when you are done. I used five copies.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`, NEVER BY HAND-ESCAPING**, and put
  **no backslash escapes in a payload at all** — use `bytes([10])` for a newline.
  **I lost a run to `\\n` surviving two levels of quoting; an assertion on the
  bare-LF count caught it before it wrote anything.**
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **It has now guarded four consecutive sessions and has never once been wrong.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first. Run `py_compile` before the gate.
- **Run the untouched control FIRST — and run it inside the scratch copy too.**
- **A GREEN GATE IS NOT THE EVIDENCE. PRINT THE DAMAGE.** A sabotage that
  CRASHES is scored "caught", so one that never really ran looks like a success.

## What you are allowed to conclude

**"I attacked it and found nothing" is a real, honest, valuable result.** Say it
plainly and clear the item. **DO NOT INVENT A FAULT TO JUSTIFY THE SESSION.**
Seventeen of my eighteen swept clean and that is written down as plainly as the
one that did not.

**You may clear R-033 and R-034 — I filed both and may clear neither.** You may
clear R-032, R-029, R-030 and R-031. **You may NEVER clear R-006.** **And if you
fix something, you may not clear your own fix.**

**R-001 has now waited through FOURTEEN generations of repair, TWELVE of which
were failed by the next pair of eyes.** The thirteenth (Door 3) has now been
attacked once and survived with one blind spot named — **that is the first
generation in a long time that was neither failed outright nor left untested.**

---

# PART 2 — **CONDITIONAL. CHECK THE KEY FIRST.**

## IF THE CRYPTOPANIC TOKEN EXISTS: BUILD CONTEXT DECK INSTRUMENT 3 OF 5

**`EXECUTION_PLAN.md` Phase 3, step 3.** CryptoPanic free tier. **HEADLINES
ONLY.** No sentiment score, no invented weights, **the cut ghost stays cut.** It
joins the existing Context Deck the way funding does — one deck, no header of its
own.

**BUILD IT THE WAY EVERYTHING HERE IS BUILT:**
- **Declare the gate and commit it ALONE with no `.py` in that commit.**
- Name the awkward edge cases **before** writing code. At minimum: a headline
  containing the ship's own disclaimer wording; an empty result set; a headline
  that is itself advice; a source name that is missing; and non-ASCII in a title.
- **A sabotage drill from birth** — not added later — **and every sabotage proved
  able to CHANGE THE OUTPUT before its verdict counts.** You are the second
  session that gets to build this in from the start rather than discover it.
- **DOOR 1, DOOR 2 AND DOOR 3 FROM BIRTH.** The machinery exists in both cockpit
  files and can be copied. **A new instrument without all three doors is a new
  hole, and the last two were retrofitted at the cost of four sessions.**
- **AND ONE MORE, EARNED TODAY: DO NOT COPY DOOR 3'S PASS LINE VERBATIM.** It
  claims "nothing was deferred to a thread" and tests only non-daemon threads.
  **Write what you actually test.**

## IF IT DOES NOT EXIST: BUILD NOTHING

**Do NOT substitute another news source.** The orders name CryptoPanic and the
orders outrank a session's own ideas — **disagree out loud to the Commander,
never quietly.** Spend the session on Part 1, and put the key on his desk again.

**IF YOU ARE RUNNING SHORT, DO PART 1 PROPERLY AND LEAVE PART 2 ENTIRELY.** A
half-built part is worse than no part.

---

# THE 1 AUGUST ERRAND — **IT IS NOW OVERDUE. CHECK THE DATE ANYWAY.**

**On 2026-07-31 it was NOT yet due. I checked with `date -u` — 11:11 UTC, 31 July
— and moved on.** If you are reading this on 1 August or later, **it has fired
and you must read the result.**

**WRITE DOWN WHAT YOU EXPECT BEFORE YOU OPEN THE LOG.**

    MEASURED, so you do not re-derive it:
    The recorder has run EXACTLY ONCE in its whole history — by hand, on
    2026-07-27 — and it appended ZERO rows. THE COMMIT-AND-PUSH BRANCH HAS
    THEREFORE STILL NEVER FIRED FOR REAL.
    A healthy run appends 12 rows per asset and reports 192 stored (measured
    2026-07-29 against a copy of the real archive).
    The honest figure on 1 August is roughly THIRTY new rows per asset and a
    stored count near 210 — NOT 180, and NOT 360.
    The archive stood at 181 lines per file (180 rows + header) all through
    2026-07-31, sha256 e3258e82… / 1549a8a1… / e0f91a87… — I verified this
    myself on 2026-07-31 afternoon and it was unchanged.

**Open `journal/daily_runs.log` and tell the Commander PLAINLY whether the task
actually committed and pushed real new rows.** **If the log says something you
did not predict, that is a finding, not a relief.**

**AND THE SECOND THING, EARNED BY B14: look at `data/oi_history/` itself and
confirm there are THREE files, correctly named.** A fourth file, or a different
name, is B14 arriving for real. **There were exactly three on 2026-07-31.**

**Do not assume it worked because the task returned 0** — `schtasks` already
reported SUCCESS once for a task that could never run at all. **Read the file and
count the rows yourself** — and note that `count('\n') + 1` overcounts a file
ending in a newline.

---

# IF ANYTHING LEAKS: GRADE IT FIRST, THEN REPAIR UNDER A GATE DECLARED FIRST

**FILL IN THE FINDING REPORT BEFORE YOU REPAIR ANYTHING** — the Commander's three
questions first, then the four steps, in `THE_PATTERN.md`. **Step 2.2 carries his
own wording — read it there, not here.** Then:

    SERIOUS ....... fix it, and stop. Build nothing.
    BORDERLINE .... do NOT fix it. Report and stop. The Commander rules.
    SMALL ......... do NOT fix it. File it in REVIEW_QUEUE.md as CATEGORY B
                    and carry on.

**If you do repair: DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY
ALONE, WITH NO `.py` FILE IN THE COMMIT, BEFORE WRITING CODE.** Then
`git show --stat` proves the bar preceded the work. **Nineteen uses and it has
survived audit every time.**

**AND RECORD THAT HASH *AFTER* YOUR FINAL PUSH, NOT WHEN YOU WRITE THE ENTRY.**
The cloud watchman pushes every four hours, so `git pull --rebase` before your
push can rewrite your own commit hashes underneath you. Then:

(a) **NOTHING THE PILOT READS CHANGES.** All edits inside `__main__` — **prove it
    two ways, do not assert it:** every diff hunk at or after the `__main__` line
    (`funding.py` 160, `fear_greed.py` 113, `open_interest.py` 243), AND a sha256
    of the production half before and after, printed side by side. **THE RECIPE,
    PER FILE, VERIFIED BY THE THIRTEENTH GENERATION:**
    - `cockpit/funding.py` and `cockpit/fear_greed.py`: **the raw byte prefix up
      to the `if __name__ == '__main__':` marker** (first N-1 lines joined by CRLF
      **WITH** a trailing CRLF) → `95069d1b…` and `bb31626c…`.
    - `data/open_interest.py`: first N-1 lines joined by CRLF with **NO** trailing
      separator → `5347bfec…`.
    - **`open_interest.py` reproducing `5347bfec…` exactly is what proves your
      script is right. Check that one first, then trust the other two.**
(b) **THE OUTPUT IS VERIFIED** against a raw fetch using the test's own
    arithmetic. **The helper under test is never called to judge itself, the gate
    never reads a constant belonging to the file it is judging, and THE GATE
    NEVER ASKS THE MODULE WHERE TO LOOK.**
(c) **THE SABOTAGE DRILL IS PERMANENT** — your new break joins the others, caught
    every run, originals restored and the restoration verified. **And check your
    new break is actually IN EFFECT, and actually CHANGES SOMETHING, when its
    judge runs.**
(d) **YOUR ORIGINAL ATTACK IS RE-RUN AGAINST THE REPAIRED FILE** — real text
    edits, not wrappers — and must now be CAUGHT, **and must be shown to fail for
    the reason it claims, not incidentally.**
(e) Everything the old gate did, it still does.
(f) **NO new file, NO new dependency, NO extra call from the Brief's path.**
(g) **RUN `py_compile` BEFORE THE GATE.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# WRITE IT UP EITHER WAY

A `PROGRESS_LOG.md` entry recording what you invented, what you broke, the actual
output, and the verdict — **including if it is all clean, and including every
prediction you got wrong.**

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly", "I believe" or "this should be fine" about anything that ships — FILE
IT in `REVIEW_QUEUE.md` before the commit that ships it.**

---

# BEFORE YOU FINISH

**Do the closing ritual exactly as `THE_PATTERN.md` sets it out** — seven steps,
ending with the next session's orders, the push, and your plain-words report to
the Commander. **It is not repeated here.**

---

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> THE ONE THING THAT UNBLOCKS THE SHIP, AND IT TAKES HIM FIVE MINUTES: A
   FREE CRYPTOPANIC API TOKEN.** Sign up at cryptopanic.com, copy the developer
   token, and it goes in `.env` as one line. **Phase 3 step 3 — the third
   instrument on the Context Deck — cannot be built or verified without it, and
   no session can create one.** Unauthenticated the API answers **403** and
   **404**. **Eight sessions have now not built step 3; this is the first time
   the reason is not a finding, and it is the only one he can personally fix.**
2. **>>> STILL HIS, INHERITED FROM THE THIRTEENTH GENERATION AND EARNED A THIRD
   TIME TODAY.** A pattern amendment, proposed and **NOT** adopted, because a
   session may never promote its own idea:
   *"A SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS
   ANYTHING."* **F10, B1 and now S6 are the same fault in three different files.**
   **And today the session that came to enforce that rule broke it itself** — my
   first sabotage was inert in the real Brief and I only found out because I ran
   the Brief. **THREE FILES AND FOUR SESSIONS. IT IS HIS CALL AND NOBODY ELSE'S.**
3. **DOOR 3 HAS NOW BEEN INDEPENDENTLY ATTACKED AND HE IS OWED THE RESULT IN
   PLAIN WORDS.** It does what it claims for the shapes it names, **and it is
   blind to one it does not name.** The hole does not reach his screen today, and
   the reason it does not is **an accident nobody designed.**
4. **R-025 IS CLEARED — the first old item cleared in several sessions**, on the
   limb it filed, by someone who did not build the repair. **The residue is R-033
   and it stays open.**
5. **THE CATEGORY B PILE IS ELEVEN DEEP**, up from nine (R-033, R-034 added).
   **It is cleared before the ship is used for real, at the same moment
   `brief.py` gets its gate.** Said out loud, as the condition on which the
   category was granted.
6. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
7. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this entire class is `symbols=None`, resolved in the body — and `funding.py`
   already does it that way.** It touches what the pilot reads, so no session may
   make it during a repair to a test. **Nine generations have now fixed the
   instance and left the pattern.**
8. **TWO REASONS THE FUNDING GATE GOES RED WITHOUT ANYTHING BEING WRONG:**
   R-021 near a settlement, and now **R-034 on roughly one settlement in six**,
   whenever all three funding rates print the same. Both SMALL, both unrepaired.
   **He should know that a red funding gate is not always a real alarm** — and
   that this is exactly the cost of leaving the disease in item 2 unruled.
9. **THE RECORDER'S COMMIT-AND-PUSH BRANCH HAS STILL NEVER FIRED AGAINST REAL
   NEW ROWS. THE ERRAND IS NOW OVERDUE.**
10. **`cockpit/brief.py` HAS NO GATE** — he has ruled: not now, before going live.
11. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
12. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
13. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
14. **The settled-rate anchor (R-004)** — returned to him on correct facts.
15. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses it.
16. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SIX TIMES, NOT ADOPTED.** I ran the
    mojibake scan by hand before my commit again. **A one-line scan would close
    this and it has been asked for six sessions running.**
17. **BOTH COCKPIT GATES ARE SLOW BECAUSE OF DOOR 3** — funding 122 s,
    fear_greed 62 s. **And today that slowness turned out to be load-bearing:**
    Door 1 only catches what Door 3 misses **because** the gate calls the doorway
    dozens of times. **If he ever asks for these to be made faster, that is not a
    free change any more, and somebody must say so.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. That is locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.** **Fourteen generations, twelve of them failed by the next pair of eyes,
and the thirteenth survived its first attack with one blind spot named — that is
what the substitute is worth, and it only works if somebody actually attacks.**
