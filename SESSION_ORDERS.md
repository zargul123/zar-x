# ZAR X PHASE 3 — **THE NORMAL RHYTHM IS BACK. YOU ATTACK FIRST, THEN YOU BUILD.**

*Written 2026-08-03 (third) by the sixteenth generation, whose one-session
exception died with it. **There is no exception in these orders and I had no
power to grant one.** Read the box at the bottom of this file if you want to
know why that sentence is here.*

---

# **>>> THERE IS NO EXCEPTION FOR YOU. THIS IS NOT AN OVERSIGHT.**

**The Commander suspended PART 1 — ATTACK — twice, for one session each. The
second of those was mine. It is over.**

    YOUR SESSION:  PART 1 — ATTACK what the last session built.
                   PART 2 — BUILD the next thing, if PART 1 leaves room.

**I could not have given you an exception even if I thought you needed one.
Only the Commander can, and only he can decide to do it again.** If you think
the ship would be better served by another one, **say so to him in your report
as a recommendation** — and do PART 1 anyway unless he answers.

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

*The Commander is not a programmer and asked for it in this form. Write your
report to him the same way.*

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~60 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~125 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  ~55 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~10 s
    vault INTACT · Brief 3/3 · lab/ untouched · git status clean
    data/oi_history/  3 files, 222 lines each (221 rows), sha256
                      a1ed6729bef45be6 / a077cf034bf66c26 / c8d97f7122544f70
                      window 2026-06-27T16:00:00Z → 2026-08-03T08:00:00Z

**EVERY GATE ON THIS SHIP IS GREEN AND ALL FOUR INSTRUMENTS ARE CORRECT.**

## What happened in the session before you

**The three inert-sabotage faults are gone.** F10 was repaired on 2026-07-31;
**S6 and B1 were repaired together on 2026-08-03** under `GATE 3.2-R8` and
`GATE 3.2b-R10`. All three were the same fault in three files: a deliberate
break that could not change the output, scored ESCAPED, turning a gate red about
a lie it had never managed to tell.

**Both defects were reproduced before they were called fixed** — S6 with Binance
stubbed to answer the same rate for all three contracts, B1 with the whole repo
copied outside itself and run at `TZ=UTC0`. Both re-runs are in
`PROGRESS_LOG.md`.

**Nothing the pilot reads changed**, proved two ways: every diff hunk inside
`__main__`, and both production halves hashing to what they hashed to before.

---

# **JOB 1 — R-038, AND IT HAS A DEADLINE. DO IT FIRST.**

**THIS IS THE ONE JOB ON THIS SHIP THAT EXPIRES.** On 2026-08-03 the recorder's
failure was caught and **123 rows (41 per asset) were recovered** and pushed as
`5c7c54a`. **Nobody has ever checked those rows against Binance.** They can only
be checked while they remain inside Binance's rolling 30-day window —
**until about 2026-09-02.**

**IT HAS NOW BEEN DEFERRED ONCE ALREADY**, by the exception the Commander
granted to my session. **He was told plainly when he granted it. Do not let it
be deferred twice.**

    Fetch the live 30-day window for all three assets. For every stored row
    that still falls inside it, compare the stored figures to what Binance
    serves TODAY, digit for digit. Report the count checked, the count
    matched, and EVERY mismatch with both values printed.

**IF ROWS DISAGREE, THAT IS A FINDING ABOUT THE ONLY DATASET ON THIS SHIP THAT
CANNOT BE BOUGHT BACK AT ANY PRICE.** Fill in THE FINDING REPORT before
repairing anything, and remember `THE_PATTERN.md`'s rule: **foundation faults
are treated harder even when the chain is longer**, because corrupt data there
silently poisons a test that THE PROMISE only allows three attempts at.

**IF THEY ALL MATCH, SAY SO PLAINLY AND CLEAR R-038.** *"I checked it hard and
found nothing"* is a real result and a good one. **You did not create R-038, so
you may clear it.**

---

# **JOB 2 — PART 1 PROPER: ATTACK THE TWO REPAIRS I JUST MADE**

**I repaired S6 and B1, I wrote the gates that judge my own repairs, and I ran
them. Every one of those is the same pair of eyes.** That is exactly the
condition PART 1 exists for. **Twelve of thirteen repairs on this ship have been
caught out by the session that came next.**

**R-042 AND R-043 ARE MY OWN DOUBTS ABOUT MY OWN WORK, FILED WITH THE REPAIRS
AND NOT AFTER SOMEBODY ASKED. Read them in `REVIEW_QUEUE.md` — they name what I
want attacked so you do not have to guess.** The short version:

**R-042 — S6.** My repaired payload rotates the dictionary's KEYS as well as its
values, so the labels print in a different order. **The sabotage is therefore
now catchable by ORDER ALONE.** Nothing is weaker today, because the whole-block
equality check catches it either way — but a gate that ever regressed to
checking only the label sequence would score S6 CAUGHT while blind to the
rate-swap S6 exists to test. **And my deviation from my own orders is in there
too: I was told to make S6 speak "using a number the GATE holds", I argued that
is impossible through `CONTRACTS`, and I used an ORDER instead. Check that
argument. It is written out in full twice so it can be checked rather than
taken.**

**R-043 — B1.** Both runs were on one machine wearing two hats. `TZ=UTC0` was
measured to work, which is better than believed, **but the cloud watchman has
never run this gate and R-031 existed precisely because nobody checked the other
clock.** `_b1_machine_offset_s` is new machinery nobody has attacked, and it has
not been tested across a DST boundary on a machine that observes one. **The
seven-hour fallback is my number and only half my reasoning about it is checked
by any machine.**

**THEN RULE ON R-034 AND R-031.** They are repaired and **NOT cleared** — I may
not clear my own work. **You may.** Say plainly whether each repair holds.

## **AND THE ATTACK I WOULD MOST LIKE SOMEBODY TO INVENT**

**A NEW sabotage that no author of these three repairs would have thought of.**
`THE_PATTERN.md` is blunt about this: **you cannot invent an attack you are
blind to, and a gate is strongest exactly where it has already been attacked.**
The three inert-sabotage faults were each found by fresh eyes, never by a
builder being careful.

**Aim it at the thing all three repairs now share:** every one of them proves a
break CHANGES THE OUTPUT before trusting the verdict. **Nobody has asked whether
that new machinery can itself go quietly inert.**

---

# **JOB 3 — PART 2: BUILD, BUT ONLY IF PART 1 LEAVES ROOM**

**IF JOBS 1 AND 2 FILL YOUR SESSION, STOP AND WRITE GOOD ORDERS. A half-built
part is worse than no part**, and PART 1 is the only thing on this ship a
builder cannot do for themselves.

**If there is room: THE NEWS INSTRUMENT, Phase 3 step 3.** It has been deferred
eight times and is now third in line. Everything needed is in
`git show 5e6d306:SESSION_ORDERS.md` and `EXECUTION_PLAN.md` Phase 3 step 3.
**MEASURE R-036 BEFORE ANY CODE.** CryptoPanic is dead and the publishers' own
feeds are adopted.

**AND IF YOU BUILD ANYTHING AT ALL, BUILD IT UNDER THE RULE THAT COST THIS SHIP
FOUR SESSIONS:** every sabotage must be **proved to change the output** before
its verdict means anything. `collection_guard.py` was built that way from birth.
Do not retrofit it four generations later, three times, as we did.

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` IN THE COMMIT, BEFORE WRITING CODE.** Twenty-one uses, twenty-one audits
survived; mine was `4d21191`. **RECORD YOUR HASH *AFTER* YOUR FINAL PUSH** — the
cloud watchman pushes every four hours and `git pull --rebase` rewrites hashes
underneath you. **That happened on 2026-08-03 and left four references pointing
at a hash that had ceased to exist.**

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after. **THE
    RECIPES, MEASURED AND REPRODUCED THIS SESSION:**
    - `cockpit/funding.py` — `__main__` at line 160; lines 1..159 joined by
      CRLF **WITH** a trailing CRLF → `95069d1bef8316d766910abda1880931…`
    - `data/open_interest.py` — `__main__` at line 243; lines 1..242 joined by
      CRLF with **NO** trailing separator → `5347bfecdf2ccfb2009770f9161dd6c5…`
    - **`open_interest.py` reproducing `5347bfec…` is what proves your script
      is right. Check that one first, then trust the other.**
    - **A WHOLE-FILE HASH CANNOT DO THIS JOB.** It cannot tell "the pilot's
      code changed" from "the test around it changed". `ROADMAP.md` carries a
      correction saying so.
(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and the restoration verified.
(d) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE. A repair nobody
    re-tested is a hope.** Show it failing for the reason it claims.
(e) Everything the old gates did, they still do.
(f) **RUN `py_compile` BEFORE THE GATE.**
(g) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may not
    clear your own. **You may clear R-034, R-031, R-038, R-042 and R-043 —
    check first whether you are the one who benefits from clearing them.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. Clean first-time runs stand at
  +1h42m, +2h15m, +3h12m, +3h20m, and this session ran clean at **-1h19m**
  (before the 16:00 settlement). **Outside a settlement window a red funding
  gate is a REAL failure — treat it as one.**
- **S6 NO LONGER GOES RED ON MATCHING RATES.** That was R-034 and it is fixed.
  **If it goes red now, it is a regression of a shipped repair and it is
  SERIOUS.** The same is true of F10 in `fear_greed.py` and B1 in
  `open_interest.py`.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER.** That is R-041 doubt 3 — a formatted age straddling a
  rounding boundary, filed by its author before it ever happened. **If it goes
  red TWICE in a row, it is real.** It has now been run green by two sessions.
- **THE RECORDER'S GATE TAKES ~55 s AND YOU SHOULD RUN IT TWICE** — once
  normally and once with `TZ=UTC0` — because that is what GATE 3.2b-R10
  requires and it is the only way B1's repair stays honest.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT. R-025 IS CLEARED.** The residue is R-033, still open.
5. **F10, S6 AND B1 WERE ALL REPAIRED ON HIS RULING, AND ALL THREE HOLD.**
6. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
7. **R-037 WAS ORDERED SORTED FIRST AND IT WAS.** Done 2026-08-03.
8. **THE EXCEPTION IS OVER.** Granted twice, spent twice, dead. **See the box at
   the bottom of this file.**

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`REVIEW_QUEUE.md` — R-038, R-042 and R-043 are your worklist**, plus your
   verdicts on R-034 and R-031. **R-006 may NEVER be cleared by you or any
   in-house session.**
2. **The `2b) S6'S FOUR BRANCHES` section of `cockpit/funding.py`'s `__main__`**
   and **the `(o) B1'S BRANCHES` section of `data/open_interest.py`'s** — the
   two repairs you are attacking.
3. **The LAST TWO entries of `PROGRESS_LOG.md`.** The file is ~570 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 28 MB, costs
  nothing. `git status` clean when you are done. **That is how B1's defect was
  reproduced this session without risking one row of the archive.**
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO
  POWERSHELL AS A HERE-STRING.** PowerShell eats the quotes. **The fifteenth
  generation lost two commands to this and wrote the warning down. The
  sixteenth read that warning and lost one anyway.** It has now cost three
  commands across two sessions.
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1**.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Seven consecutive sessions have guarded this way.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first. **The sixteenth generation wrote one of
  these and caught it by reading, not by running.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare your counts against `git show HEAD:<file>` so
  you know whether YOU added any** — cheaper and surer than eyeballing.
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.

---

# **>>> HOW YOUR SESSION ENDS — AND THE ONE THING YOU MUST NOT GET WRONG**

**THE COMMANDER ASKED FOR THIS IN WRITING ON 2026-08-03, IN THESE WORDS:**

> *"the next session understand the exemption is only for him — if it builds
> something, the next session there will be no exemption in his next orders. am i
> understanding right?"*

**HE WAS UNDERSTANDING IT EXACTLY RIGHT, AND HE FOUND A HOLE IN A SET OF ORDERS
BY ASKING.** The instruction to restore PART 1 was sitting in a box at the top of
the file with nothing in the closing steps to carry it through, and a session
writing the next orders from memory could have carried an exemption forward
without ever deciding to.

    >>> AN EXEMPTION DIES WITH THE SESSION IT WAS GRANTED TO.
    >>> THE ORDERS YOU WRITE MUST SAY: PART 1 ATTACK, THEN PART 2 BUILD.
    >>> YOU MAY NOT GRANT AN EXEMPTION TO ANYONE, INCLUDING THE SESSION
        AFTER YOU. ONLY THE COMMANDER CAN, AND ONLY HE CAN DECIDE TO
        DO IT AGAIN.

**WHY THIS MATTERS MORE THAN IT LOOKS.** He has granted it twice. **Twice is how
a suspension quietly becomes the normal state** — and PART 1 is the only thing on
this ship that a builder cannot do for themselves. **If a session ever writes
"and the exemption continues" into the next orders, the ship has lost its only
independent check and nobody will have decided to give it up.**

**If you genuinely think the session after you should skip the attack, say so TO
HIM in your report as a recommendation — and write the orders with PART 1
restored anyway.** He rules; you recommend.

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL

**`THE_PATTERN.md` sets these out in full and they are not repeated here. In
order:**

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... verdicts on what you attacked, plus one OPEN item
                            against anything you built or repaired yourself.
                            You may not clear your own.
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the
                            truth including what is broken. Keep the old
                            markers below it.
    4. ROADMAP.md ......... tick what shipped; correct any MEASURED fact that
                            moved.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words
                            brief, **WITH PART 1 ATTACK IN IT** — see the box
                            above. Write it for someone with NO memory of you.
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what
       held, **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR, AND IT IS THE ONLY THING HE
   PERSONALLY OWES THE R-037 REPAIR.** The Task Scheduler event log is
   **switched off**, which is why the cause of 11:47:41 is unprovable and always
   will be. Enabling it costs nothing and means a next time leaves evidence:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

   **A session cannot do this — it needs Administrator and no session should
   elevate silently.**
2. **>>> R-038 EXPIRES ABOUT 2026-09-02 AND IT IS NOW JOB 1 ABOVE.** It has been
   deferred once already, by the exception he granted. **He was told plainly at
   the time. There is still room, but there is not room to defer it twice.**
3. **THE CATEGORY B PILE IS EIGHTEEN DEEP** — R-042 and R-043 added.
   **It has grown every session since it was created and has NEVER once
   shrunk.** Cleared before the ship is used for real, at the same moment
   `brief.py` gets its gate. **Somebody should say the number out loud to him
   each time.**
4. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED FOUR TIMES OVER:** *"A SABOTAGE
   MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."*
   **F10, B1 and S6 were the same fault in three files and all three are now
   repaired**, each by a different generation, each after a different session
   found it the hard way. `collection_guard.py` was built with the rule from
   birth. **A session may never promote its own idea to law. It is his and only
   his.** **THIRTEEN OTHER CANDIDATES REMAIN UNADOPTED.**
5. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT (R-041 doubt 5).** If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. **The batch header says WEEKLY in words; that is documentation, not a
   check.** Next run 10-Aug-2026 09:00.
6. **NOBODY HAS EVER ASKED WHETHER A SOURCE ITSELF CAN LIE (R-035).** No file on
   this ship talks to more than one source. **Every gate proves the printed line
   matches what the source SENT; nothing asks whether the source was RIGHT.**
   **His own words: fake data on his screen in real time, and the only door with
   nobody standing at it.** **Still the strongest candidate for a real attack
   once R-038 is settled.**
7. **THE NEWS INSTRUMENT IS STILL UNBUILT** and is Job 3 above. Everything is in
   `git show 5e6d306:SESSION_ORDERS.md` and `EXECUTION_PLAN.md` Phase 3 step 3.
   **Measure R-036 before any code.**
8. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
9. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this class is `symbols=None`, resolved in the body — `funding.py` already
   does it that way, and `collection_guard.py` was written that way from
   birth.** It touches what the pilot reads, so no session may make it during a
   repair to a test. **Eleven generations have fixed the instance and left the
   pattern.**
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
    that slowness turned out to be load-bearing** (R-033). **Making them faster
    is no longer a free change and somebody must say so if he asks.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.**
