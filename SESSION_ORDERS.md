# ZAR X PHASE 3 — **ATTACK THE NEWS INSTRUMENT. IT IS NEW, NOBODY HAS EVER ATTACKED IT, AND IT IS ON HIS SCREEN.**

*Written 2026-08-04 by the seventeenth generation, which built the thing you are
about to attack. **I have given you no cap and no exemption, because I am not
allowed to and because I am the last person who should.***

---

# **>>> PART 1 IS BACK. FULLY. NO CAP, NO EXEMPTION, NO LIMIT.**

    YOUR SESSION:  PART 1 — ATTACK what I built. Uncapped.
                   PART 2 — BUILD the next thing, if PART 1 leaves room.

**THE OUTSIDE CHECK WAS REDUCED THREE SESSIONS RUNNING** — exemption
(2026-07-31), exemption (2026-08-03), cap (2026-08-03). **All three were the
Commander's, all three were justified on their own, and all three are over.**
The previous orders said a fourth would be the moment to ask him directly
whether the outside check still exists. **There is no fourth. The count is
reset and this line exists so nobody has to reconstruct it from the log.**

**AND THE REASON IT DOES NOT TRANSFER TO ME IS HIS OWN Q2, IN ONE LINE:**

    the last session's repairs .. repairs to an ALARM. Nothing found in them
                                  could make a price, a rate or a saved row
                                  wrong. Q2 = NO -> SMALL -> safely capped.
    MY NEWS INSTRUMENT .......... a NEW LINE ON HIS BRIEF that he reads with
                                  his own eyes. A fault in it puts a WRONG,
                                  STALE or INVENTED headline on his screen.
                                  Q2 = YES -> the exact opposite of SMALL.

**A BUILDER CAPPING THE REVIEW OF THEIR OWN BUILD IS NOT A CAP — IT IS A
BUILDER MARKING THEIR OWN HOMEWORK, WHICH THIS SHIP HAS NEVER ALLOWED.**

**EVERY INSTRUMENT ON THIS SHIP LEAKED WHEN SOMEBODY FINALLY TRIED.** Gate 3.2
reported 48/48 with four lies walking through it. Gate 3.1-R let five through.
Both rebuilds were failed the next day by a session that invented seven more.
**Not one was found by its builder being careful, and I was careful.**

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
    cockpit/news.py             GATE 3.3      PASSED  exit 0  0 red  ~25 s
    vault INTACT · Brief 3/3 · lab/ untouched
    data/oi_history/  3 files, 222 lines each — untouched; I did not run
                      the recorder. Next scheduled run 10-Aug-2026 09:00.

**EVERY GATE ON THIS SHIP IS GREEN AND ALL FIVE INSTRUMENTS ARE CORRECT.**

## What happened in the session before you, in four lines

1. **R-038 IS CLEARED AND ITS DEADLINE IS BEATEN.** 123 of 123 recovered rows
   and 537 of 537 in-window rows are digit for digit what Binance serves.
2. **R-034 (S6) AND R-031 (B1) ARE CLEARED.** Both repairs hold, both proved
   on this run rather than remembered.
3. **THE NEWS INSTRUMENT IS BUILT, GATED AND ON HIS BRIEF.** Phase 3 step 3,
   deferred eight times, is done. The Context Deck is three of five.
4. **I GOT TWO THINGS WRONG AND BOTH ARE IN `PROGRESS_LOG.md`** — I adopted a
   publisher that turned out to rate-limit, and I wrote a sabotage that could
   not change anything **while writing the rule that forbids exactly that.**

---

# **JOB 1 — ATTACK `cockpit/news.py`. THIS IS YOUR SESSION AND IT IS UNCAPPED.**

**INVENT A SABOTAGE I NEVER THOUGHT OF. THAT IS THE ONE THING I COULD NOT DO
FOR MYSELF.** Break it on purpose **in a copy of the whole repo OUTSIDE the
repo**, run the untouched copy first so you know the rig works, and **write it
up either way** — *"I attacked it hard and found nothing"* is a real, successful
result and clears the item.

## **>>> START HERE. I HAVE ALREADY TOLD YOU WHERE IT IS WEAKEST.**

**R-046 — MY DOOR 3 IS THE WEAKEST ON THIS SHIP AND I SAID SO BEFORE ANYBODY
FOUND IT.** GATE 3.3's door 3 listens at `sys.stdout` and `sys.stderr` — the
**Python level** — on four paths. **`fear_greed.py` and `funding.py` listen at
the FILE DESCRIPTOR and run a fresh interpreter against a real edited copy
outside the repo.**

    THREE THINGS THEY CATCH THAT MINE WOULD NOT:
      * a write to descriptor 1 that bypasses sys.stdout entirely
                        -> os.write(1, b'>> go long') would be INVISIBLE to me
      * a write deferred to a non-daemon thread, landing after the doorway
        has already returned
      * an atexit handler that writes at interpreter shutdown

**A1, A2 AND A3 IN THE OTHER TWO GATES ARE EXACTLY THOSE THREE, AND ALL THREE
WERE CAUGHT THERE THIS SESSION. GO AND PROVE MINE IS BLIND** — it should take
you one sabotage and it is the single most likely real finding in this file.
**The machinery to fix it is in `cockpit/funding.py` and can be copied.**

**WHY I SHIPPED IT ANYWAY, SO YOU CAN JUDGE THE DECISION AND NOT JUST THE CODE:**
I judged a fully-gated instrument with a named weakness beat a half-built one.
**That is a judgement about my own budget, made by me, benefiting me** — the
exact shape R-019 exists to distrust. **You may rule the trade was wrong.**

## THE OTHER FOUR PLACES I WOULD LOOK, IN ORDER

2. **R-045 — MY THREE NUMBERS ARE JUDGEMENTS DRESSED AS CONSTANTS.**
   `DEAD_FEED_H = 48`, `WINDOW_H = 24`, `TITLE_MAX = 84`. **48 hours can
   silence a live publisher having a quiet holiday weekend** — measured the
   same day, Bitcoin Magazine sat at 15.9 h and Bitcoinist at 27.4 h, both
   alive. **Is 48 right? I chose it from one afternoon of readings.**
3. **THE ONE I LIKE LEAST, AND IT IS INSIDE `section_text`.** If publishers
   answer but **no story falls inside 24 hours**, I treat that as a fault and
   print the offline line. **A genuinely quiet spell would be reported as an
   instrument failure.** My reasoning is in R-045; **it is reasoning, not a
   measurement.**
4. **THE DEAD-FEED GUARD ITSELF.** It compares `now` to the newest story's
   stamp. **What does it do when a publisher's clock runs AHEAD of ours?** I
   drop future-dated stories from the window and I clamp `_age_words` at zero
   so nothing prints "-3m ago" — **but I never tested a feed dated a week into
   the future**, and The Defiant really did serve a story stamped very slightly
   ahead of my clock on 2026-08-04. **That is a real observed shape and I did
   not build a case for it.**
5. **`_parse`'s RSS-BEFORE-ATOM ORDER.** I read `<item>` elements first and only
   look for Atom `<entry>` if none are found. **A feed carrying both would have
   its Atom half silently ignored.** I have not seen one. I have not looked.

## **>>> AND THE RULE THAT DECIDES WHETHER WHAT YOU FIND STOPS YOU**

**Fill in THE FINDING REPORT in `THE_PATTERN.md` BEFORE repairing anything —
the report comes before the repair, always.** Then his own scoring:

    it puts a WRONG, STALE or INVENTED headline on his Brief ... it STOPS you.
    it touches the SAVED ARCHIVE .............................. it STOPS you.
    it is a weakness in the TEST that cannot reach his screen . Q2 = NO ->
                                                 SMALL. File it CATEGORY B and
                                                 KEEP BUILDING.

**DO NOT MANUFACTURE A DEFECT TO JUSTIFY A SESSION.** The pressure after a
session that built something is to find something. **A stretched finding costs
him an instrument he actually wanted.**

---

# **JOB 2 — RULE ON MY THREE ITEMS. YOU MAY; I MAY NOT.**

**R-044, R-045 and R-046 are MY OWN doubts, filed with the build and not after
somebody asked.** Read them in `REVIEW_QUEUE.md`. Say plainly whether each
holds. **R-042 and R-043 are still open too** — the previous session was capped
away from them and I ruled on exactly one of R-042's doubts (the S6 label-order
question: **acceptable**, reasoning in `PROGRESS_LOG.md`). **The rest is
untouched and it is yours if you want it.**

---

# **JOB 3 — BUILD STEP 3b: THE DAILY NEWS COUNT ARCHIVE. ONLY IF PART 1 LEAVES ROOM.**

**I DID NOT BUILD IT AND I TOLD HIM SO RATHER THAN LET HIM NOTICE.** The orders
described it, he ruled yes to it, and I left it out on purpose.

**WHY, SO YOU CAN DISAGREE WITH ME:** it is a **WRITER**, and a writer on this
ship needs its own fail-safe, its own duplicate guard and its own gate —
`open_interest.py` is 2279 lines and most of them are that argument. **Building
half of it beside a full instrument is what "a half-built part is worse than no
part" forbids.** The orders themselves rank it *"cheap insurance for a maybe"*
and rank the instrument as the point.

    date,       total,  coindesk,  cointelegraph,  decrypt,  beincrypto,  bitcoin_com
    2026-08-04,   81,      25,          30,           12,        10,           4

**WHY IT EXISTS AT ALL, IN HIS words: you cannot know that 43 headlines an hour
is unusual unless you know that 11 is normal — and the feeds hand you only the
last 10 to 39 stories, a few hours' worth. THERE IS NO ARCHIVE AND THE PAST
CANNOT BE BOUGHT**, because old articles are edited, retitled and deleted, so
any sold "news history" is polluted by hindsight — which Law 7 says the Lab's
own numbers can never detect. **`data/oi_history/` exists for exactly this
reason.**

**BUILD THE BORING FILE. DO NOT BUILD THE NEWS-STORM FLAG** — it is in the
README's vision and is **NOT a scheduled step in Phases 3-8**, and a session
that finds itself building a signal out of headlines has misread the plan.

**DECLARE ITS GATE AND COMMIT IT ALONE WITH NO `.py` IN THE COMMIT.** Name the
awkward cases first: two runs on one day, a run that fails halfway, a day with
no run at all, a publisher that was dead that day, and the file being read by a
later session that must not be able to tell a real zero from a missing day.

**IF IT WILL NOT FIT, BUILD NOTHING AND SAY SO.** That rule is not capped and
never will be.

## **>>> AND THE THING YOU MUST WRITE INTO YOUR OWN ORDERS**

    >>> IF YOU BUILD ANYTHING, THE ORDERS YOU WRITE MUST SEND THE SESSION
    >>> AFTER YOU TO ATTACK IT — FULLY, AND WITH NO CAP OF ANY KIND.
    >>> YOU MAY NOT GRANT AN EXEMPTION OR A CAP TO ANYONE, INCLUDING THE
    >>> SESSION AFTER YOU. ONLY THE COMMANDER CAN.
    >>> AN EXEMPTION DIES WITH THE SESSION IT WAS GRANTED TO. SO DOES A CAP.
    >>> THEY ARE THE SAME ANIMAL AT DIFFERENT SIZES.

**If you genuinely think the session after you should skip the attack, say so TO
HIM in your report as a recommendation — and write the orders with PART 1
restored anyway.** He rules; you recommend.

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` IN THE COMMIT, BEFORE WRITING CODE.** Twenty-two uses, twenty-two audits
survived; mine was `016024e`. **RECORD YOUR HASH *AFTER* YOUR FINAL PUSH** — the
cloud watchman pushes every four hours and `git pull --rebase` rewrites hashes
underneath you.

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after. **THE
    RECIPES, WHICH DIFFER BETWEEN FILES AND HAVE BEEN WRONG ON RECORD BEFORE:**
    - `cockpit/funding.py` — `__main__` at line 160; lines 1..159 joined by
      CRLF **WITH** a trailing CRLF → `95069d1bef8316d766910abda1880931…`
    - `data/open_interest.py` — `__main__` at line 243; lines 1..242 joined by
      CRLF with **NO** trailing separator → `5347bfecdf2ccfb2009770f9161dd6c5…`
    - **`cockpit/news.py` — `__main__` at line 250**; lines 1..249 joined by
      CRLF **WITH** a trailing CRLF → `0f0d638662695c1de49d074823c09fe6…`
      **MEASURED 2026-08-04 and VERIFIED to be exactly the raw byte prefix of
      the file, not merely a join that looked plausible.** The no-trailing-
      separator form is `ff74d4a28990de6f…` and is NOT the prefix for this
      file. **The recipe differs between files on this ship and has been wrong
      on record before — check the assertion, do not trust the number.**
    - **A WHOLE-FILE HASH CANNOT DO THIS JOB.** It cannot tell "the pilot's
      code changed" from "the test around it changed".
(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and the restoration verified.
(d) **>>> EVERY SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT
    COUNTS, AND ON THE CHANNEL IT ACTUALLY AFFECTS.** `news.py` does this and
    `collection_guard.py` does this. **N10 returns a byte-identical block and
    only changes stdout — a drill measuring every sabotage on one channel would
    score it INERT and delete the only check that catches it.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE. A repair nobody
    re-tested is a hope.**
(f) Everything the old gates did, they still do.
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may not
    clear your own. **You MAY clear R-042, R-043, R-044, R-045 and R-046 —
    check first whether you are the one who benefits from clearing them.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. This session ran clean at about
  **-2h30m** before the 16:00 settlement. **Outside a settlement window a red
  funding gate is a REAL failure — treat it as one.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` IN ITS LIVE
  CHECK (c) AND STILL PASS.** That is the design working, not a fault: the bar
  is **at least 3 of 5 publishers and at least 3 stories.** **It happened on the
  first real run** — CryptoSlate answered HTTP 429 behind a Cloudflare
  challenge. **If it drops BELOW 3 of 5, that is real and it is R-044.**
- **THE `(l)` DRILL PRINTS `INERT` INSTEAD OF `CAUGHT` IF A SABOTAGE STOPS
  CHANGING THE OUTPUT, AND INERT IS A FAIL.** That is deliberate and it is the
  whole point of the file. **If you see INERT, something real has drifted.**
- **S6, F10 AND B1 NO LONGER GO RED.** All three are repaired and all three now
  hold. **If any goes red, it is a regression of a shipped repair and SERIOUS.**
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **If it goes red TWICE in a row, it is
  real.** Three sessions have now run it green.
- **THE RECORDER'S GATE TAKES ~55 s AND MUST BE RUN TWICE** — once normally and
  once with `TZ=UTC0`. That is what GATE 3.2b-R10 requires.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT IN BOTH COCKPIT FILES. R-025 IS CLEARED.** Residue R-033.
5. **F10, S6 AND B1 WERE ALL REPAIRED ON HIS RULING, AND ALL THREE HOLD.**
6. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
7. **R-037 WAS ORDERED SORTED FIRST AND IT WAS.** Done 2026-08-03.
8. **THE EXCEPTION IS OVER AND SO IS THE CAP.** Both died with the sessions
   they were granted to. **You have neither.**
9. **NEWS IS INFORMATION AND CAN NEVER BECOME A SIGNAL.** Phase 6's three slots
   are locked BY NAME — Turtle/Donchian, funding-rate fade, on-chain cycle
   thermometer. **None is news.** A headline that is advice is printed in
   quotes and attributed; **the Brief's own voice never adopts it.**

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`REVIEW_QUEUE.md` — R-044, R-045 and R-046 are your worklist**, plus
   R-042 and R-043 if you want them. **R-006 may NEVER be cleared by you or any
   in-house session.**
2. **`cockpit/news.py`** — the whole file. It is 813 lines; **the part the
   pilot reads is lines 1..249** and the gate is everything from line 250 on.
3. **The LAST TWO entries of `PROGRESS_LOG.md`.** The file is ~600 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 28 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** PowerShell eats the quotes and
  **bash eats every BACKTICK as a command substitution.** **The fifteenth
  generation lost two commands to this, the sixteenth lost one after reading
  the warning, and I lost one after reading BOTH — my ROADMAP row came out with
  three empty code spans and had to be rewritten.** **Four commands, three
  sessions. This warning does not work. Just write the file.**
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1**.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Eight consecutive sessions have guarded this way.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare your counts against `git show HEAD:<file>`.**
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH. `python …` ON ITS OWN DOES NOT WORK ON HIS MACHINE** — bare
  `python` hits a **pyenv shim with no version selected**. His PowerShell opens
  at `C:\WINDOWS\system32`. The working form is one line:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces
  a fresh one, `CHECK_STATUS.bat` shows the collection's health. **They already
  carry the `cd /d` and the full interpreter path.**

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL

**`THE_PATTERN.md` sets these out in full and they are not repeated here.**

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... verdicts on what you attacked, plus one OPEN item
                            against anything you built or repaired yourself.
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the
                            truth including what is broken. Keep the old
                            markers below it.
    4. ROADMAP.md ......... tick what shipped; correct any MEASURED fact that
                            moved.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words
                            brief, **WITH PART 1 ATTACK IN IT AND NO CAP.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what
       held, **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> THE TWO NEW PUBLISHER NAMES ARE HIS TO OVERRULE, AND HE SHOULD BE
   ASKED ONCE.** He ruled the PRINCIPLE — five publishers, different owners,
   not one hundred. **The five NAMES came from one probe on 2026-07-31 and two
   of them are dead:** The Block is edge-blocked (HTTP 403 x8) and Blockworks
   is **209 days stale behind an HTTP 200**. **I substituted BeInCrypto and
   Bitcoin.com News.** Law 2 means changing either is a one-line edit inside
   `cockpit/news.py`. **Measured and NOT chosen: The Defiant, Bitcoin Magazine
   (15.9 h stale), Bitcoinist (27.4 h), CoinJournal (9 items), CryptoBriefing
   (rejected — 25.8 stories/hour would drown a five-publisher count).**
2. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — still the only thing he
   personally owes the R-037 repair. The Task Scheduler event log is switched
   off, so a next time would leave no evidence either:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

3. **THE CATEGORY B PILE IS NINETEEN DEEP.** R-044, R-045 and R-046 added;
   R-038, R-034 and R-031 cleared. **It has never once meaningfully shrunk.**
   Cleared before the ship is used for real, at the same moment `brief.py` gets
   its gate. **Somebody should keep saying the number out loud to him.**
4. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED FIVE TIMES:** *"A SABOTAGE
   MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."*
   **`collection_guard.py` and now `news.py` were both built with it from
   birth; F10, S6 and B1 were each retrofitted a generation late.** **And the
   fifth proof is that I wrote an inert sabotage MYSELF, twenty minutes after
   writing the rule.** **A session may never promote its own idea to law.**
   **THIRTEEN OTHER CANDIDATES REMAIN UNADOPTED.**
5. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5). If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. Next run 10-Aug-2026 09:00.
6. **>>> NOBODY HAS EVER ASKED WHETHER A SOURCE ITSELF CAN LIE (R-035), AND IT
   IS NOW BIGGER THAN IT WAS.** No file on this ship talks to more than one
   source. **Every gate proves the printed line matches what the source SENT;
   nothing asks whether the source was RIGHT.** **The news instrument just
   added FIVE more sources nobody cross-checks — and a headline is not even the
   kind of thing a second source could confirm digit for digit.** **His own
   words: fake data on his screen in real time, and the only door with nobody
   standing at it.** **Still the strongest candidate for a whole session's
   attack.**
7. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
8. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this class is `symbols=None`, resolved in the body — `funding.py`,
   `collection_guard.py` and now `news.py` all do it that way.** It touches
   what the pilot reads, so no session may make it during a repair to a test.
   **Twelve generations have fixed the instance and left the pattern.**
9. **`cockpit/brief.py` HAS NO GATE** — he has ruled: not now, before going
   live. **It now imports THREE instruments and prints three sections.**
10. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
11. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
12. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
13. **The settled-rate anchor (R-004)** — returned to him on correct facts.
14. **THE FUNDING LINE STAYED ON THE BRIEF** and he was told. One word reverses
    it. **The same is now true of the NEWS line.**
15. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SEVEN TIMES, NOT ADOPTED.**
16. **BOTH COCKPIT GATES ARE SLOW BECAUSE OF DOOR 3** — ~125 s and ~60 s — **and
    that slowness turned out to be load-bearing** (R-033). **`news.py`'s gate is
    ~25 s precisely because it does NOT have that machinery. That is the trade
    R-046 is about, and it is visible in the clock.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.**
