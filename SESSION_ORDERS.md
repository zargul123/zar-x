# ZAR X — **YOUR JOB 1 IS TO ATTACK THE REPAIR THE LAST SESSION BUILT. IT FOUND THE FAULT, GRADED IT AND FIXED IT — ALL THREE — AND FILED THAT AGAINST ITSELF AS R-066. YOU DO NOT HAVE AN EXEMPTION AND MAY NOT WRITE YOURSELF ONE.**

*Written 2026-08-18 by the twenty-second generation, which attacked
`cockpit/whales.py`, found two breaks walking through a gate reporting
`100 checks, 0 red`, took the Commander's ruling — "OK CORRECT IT" — and built
GATE 3.5-R1 under a bar it committed alone, with no code in that commit.*

---

# **>>> READ THIS FIRST, IN PLAIN WORDS**

    YOUR SESSION:  PART 1 — **ATTACK GATE 3.5-R1**, the new check in
                            `cockpit/whales.py` below its `__main__` line.
                            **The same mind wrote the attack in the morning
                            and the defence in the afternoon.** That is
                            R-066 and it is your whole first job.
                   PART 2 — **CONDITIONAL, AND IT IS NOT A NEW INSTRUMENT.**
                            Phase 3's five are DONE. See JOB 2.

**THE COMMANDER'S STANDING RULE, IN HIS OWN WORDS, 2026-08-11:**

> *"in next session when he write session orders and well after others too every
> time new session has to attack the build of previous session."*

**HE HAS GRANTED EXACTLY ONE EXEMPTION EVER AND SAID SO IN WORDS. YOU DO NOT
HAVE ONE.** Only he can give one, and only out loud.

---

# THE BRIEF, IN PLAIN WORDS — READ THIS BEFORE ANYTHING ELSE

## Where the ship is

    cockpit/fear_greed.py       GATE 3.1-R7   PASSED  exit 0  0 red  ~63 s
    cockpit/funding.py          GATE 3.2-R8   PASSED  exit 0  0 red  ~124 s
    data/open_interest.py       GATE 3.2b-R10 PASSED  exit 0  0 red  ~56 s
      the same file at TZ=UTC0  GATE 3.2b-R10 PASSED  exit 0  0 red  ~58 s
    data/collection_guard.py    GATE 3.2c-R1  PASSED  exit 0  0 red  ~7 s
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~6 s
    cockpit/events.py           GATE 3.4      PASSED  exit 0  0 red  ~0.6 s
      the same file at TZ=UTC0  GATE 3.4      PASSED  exit 0  0 red  ~1.4 s
    cockpit/whales.py           GATE 3.5-R1   PASSED  exit 0  0 red  ~7 s
      the same file at TZ=UTC0  GATE 3.5-R1   PASSED  exit 0  0 red  ~8 s
                                107 checks, SEVENTEEN sabotages, all CAUGHT
    vault INTACT 6 of 6 · Brief 3/3, FIVE Context Deck lines · lab/ untouched

**PHASE 3'S CONTEXT DECK IS COMPLETE — FIVE INSTRUMENTS OF FIVE. THERE IS NO
SIXTH AND THE PLAN DOES NOT HAVE ONE.**

## What the last session did, in seven lines

1. **ATTACKED `cockpit/whales.py`** and found **two breaks inside `_get`** — the
   four lines that are the only code on this ship that actually speaks to
   Binance — **each walking through `GATE 3.5 PASSED — 100 checks, 0 red`.**
   One made ETH and SOL print Bitcoin's numbers; one made "all accounts" print
   the top-account figure for every coin.
2. **THE COMMANDER RULED: CORRECT IT.**
3. **THE BAR WAS DECLARED AND COMMITTED ALONE** — commit `cacf355`, one document
   changed, no `.py` in it. `git show --stat cacf355` is the proof.
4. **THE REPAIR: the gate stands up an HTTP server of its own on `127.0.0.1`**
   and makes the REAL `_get` walk to it over a real socket, judging **what it
   asked for** (compared to six tuples typed out in the gate) beside **what came
   back** (held to the same block the fake transport must produce). **No Binance
   request is made by the new check.**
5. **THREE NEW PERMANENT SABOTAGES — W15, W16, W17.** W17 was INERT in the
   morning and its verdict was thrown away; it is provable now because the
   gate's own server answers an unknown request with **HTTP 500**.
6. **CERTIFIED BY THE ATTACK, NOT BY THE DRILL.** X15, X16 and X17 re-applied as
   REAL TEXT EDITS to a copy outside the repo: **exit 1 with 4, 3 and 2 red**,
   after the repaired control passed first.
7. **THE CATEGORY B PILE IS THIRTY-FIVE.** Nothing was cleared by anybody.

---

# **JOB 1 — ATTACK GATE 3.5-R1. THIS IS LAYER 3 AND ITS AUTHOR CANNOT DO IT.**

## WHERE ITS AUTHOR THINKS IT IS WEAKEST — **AND THEREFORE PROBABLY NOT WHERE THE FINDING IS**

Read **R-066** in full. In short:

  * **The new check proves the trip to a server that is NOT Binance.** Redirects,
    gzip, chunked encoding, a 429 with `Retry-After`, a connection reset
    mid-body — **my server is polite in ways the real venue may not be.**
  * **The three sabotages are the three faults its author already knew about.**
    He wrote the attack in the morning and the defence in the afternoon.
    **The fourth fault in `_get` is the one that matters.**
  * **This gate now BINDS A PORT and starts a THREAD.** Nobody has run it behind
    a firewall, with a proxy genuinely configured, or twice at the same instant.
  * **`DOOR_BODY = dict(GOLD)`** reuses the fixture payloads on purpose, so a
    fault in those payloads is now invisible in two places instead of one.

## THINGS WORTH TRYING THAT ITS AUTHOR DID NOT

    · run TWO copies of the gate at the same moment - does either wedge?
    · set HTTP_PROXY / HTTPS_PROXY in the environment and run it. The gate
      sets NO_PROXY inside itself and puts it back; nobody has tested the
      path where a proxy is really configured, or whether it is restored
      when a check above it raises.
    · make the gate's own server answer a REDIRECT, or gzip, or hang past
      the timeout - does `_get` behave, and does anything notice?
    · kill the server thread mid-run and see what the gate says.
    · does the gate still pass with no network at all? It should - the new
      check is local - but the live check (l) will go red, and the two
      failures must be TELLABLE APART.
    · read `door_run` and `door_refusal` and ask whether the recorded log
      could ever be read STALE - it is reset at the top of each call, and
      the drill calls them repeatedly.
    · the shutdown check: force an exception between the server starting
      and the shutdown, and see whether a listener is left behind.

## WHAT YOU STILL OWE, WHATEVER YOU FIND

1. **PROVE THE SHIP IS ALIVE FIRST.** All TEN invocations, output to a file,
   red counted BY MACHINE **three ways** — the tick character, the first word of
   a line, and the phrase "GATE ... FAILED" — **and then READ any hit with your
   own eyes.** `collection_guard.py` prints `OK  `/`FAIL `, not ticks;
   `fear_greed.py` has FAILURE inside its own pass text; and **the funding
   gate's prose contains the word "escaped" at the start of a line, which fooled
   the last session's counter within the hour.**
2. **WRITE YOUR BARS DOWN BEFORE YOU RUN ANYTHING**, in a scratch file, so you
   cannot move them afterwards.
3. **COPY THE WHOLE REPO OUTSIDE THE REPO** (39 MB) and break things THERE.
   **RUN THE UNTOUCHED CONTROL FIRST** — that is Step 0.1 and it has caught a
   false finding before.
4. **PROVE EVERY BREAK CHANGES WHAT SOMEBODY READS** before its verdict counts.
   The last session threw away two of its own escapes under this rule.
5. **FILL IN THE FINDING REPORT BEFORE REPAIRING ANYTHING.** The Commander's
   Three Questions come first and can end it on their own.
6. **"I ATTACKED IT HARD AND FOUND NOTHING" IS A SUCCESS.** Say it plainly and
   clear R-066. **DO NOT MANUFACTURE A DEFECT TO JUSTIFY A SESSION.**
7. **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.**
8. `git status` clean when you finish.

**YOU MAY CLOSE R-060** — you neither found it, graded it nor fixed it — **but
only after you have satisfied yourself the repair really holds. You may NOT
clear R-066.**

---

# **JOB 2 — CONDITIONAL. THERE IS NO INSTRUMENT LEFT TO BUILD.**

1. **>>> THE BRIEF FAILED ONCE AND THEN RECOVERED ON 2026-08-18 — WATCH IT.**
   The first run after the repair printed **2/3**: TwelveData timed out reading
   BTC and the Yahoo fallback returned a `JSONDecodeError`. **An immediate
   re-run was 3/3**, so it was a transient, and the fail-safe named the dead
   asset instead of hiding it. **It is not the whale watch and not the repair.**
   **Run the Brief early in your session and read its output.** If BTC goes
   offline more than once, that is your session — and item 12 below, the
   TwelveData key awaiting rotation since Phase 2, is the first suspect.
2. **R-049, AND SAY "FOURTH TIME" OUT LOUD.** The X1 repair in `cockpit/news.py`
   is self-marked — the session that found the fault wrote the fix and the
   checks that say the fix works — and it runs on every headline he sees. The
   measurement that argues for leaving it: 136 real headlines, not one carrying
   markup. **Offer it to him; do not decide it.**
3. **`cockpit/brief.py` STILL HAS NO GATE.** He ruled: not now, before going
   live. **That is the same moment the whole Category B pile is cleared, and the
   pile is THIRTY-FIVE.** Keep saying the number.
4. **R-058's DOUBTS 3 AND 4 ARE STILL UNMEASURED** and both are an afternoon's
   work: how long Binance really goes between bucket updates (`MAX_AGE_MIN =
   30`), and how far the BTC figure really moves between two calls seconds apart
   (the live tolerance of 1.0 point). **Retiring either would be real progress.**

**IF PART 1 FINDS SOMETHING SERIOUS, DO JOB 1 AND STOP.**

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after.

    **THE RECIPE, RE-CONFIRMED 2026-08-18: the hash is of the prefix BEFORE the
    `__main__` line, WITHOUT the anchor line, no trailing separator.** On
    untouched files:

        cockpit/fear_greed.py       __main__ 112   bb31626c493a1ac6
        cockpit/funding.py          __main__ 159   95069d1bef8316d7
        cockpit/news.py             __main__ 272   503663762315b2f2
        data/collection_guard.py    __main__ 155   d6518cd7208eb611
        cockpit/events.py           __main__ 372   6fc5ce7d67aa8f24
        cockpit/whales.py           __main__ 363   d2cd1b58373d2fcb

    **THE LINE NUMBERS FOR `news`, `events` AND `whales` ARE ONE HIGHER THAN THE
    OLDER RECORD SAYS — measured 2026-08-18. The hashes are identical, so only
    the counting of the anchor line differed. The measurement wins.**

    **AND `data/open_interest.py` CANNOT BE HASHED THIS WAY AT ALL: the anchor
    appears TWICE in it**, once for real and once quoted inside its own gate.
    **Refuse, and prove that file untouched with `git status` instead.**

(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and **the restoration verified, not assumed.**
(d) **EVERY SABOTAGE PROVED TO CHANGE THE OUTPUT, ON ITS OWN CHANNEL.**
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE.** This is the one
    that certified GATE 3.5-R1, and a drill alone would not have.
(f) **RUN ALL TEN INVOCATIONS AND READ THEIR OUTPUT before you change anything.**
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may
    clear R-042 through R-065 — **check first whether you are the one who
    benefits.** **You may not clear R-066.**

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. **Outside a settlement window a
  red funding gate is a REAL failure.**
- **`cockpit\whales.py --gate` STILL READS BINANCE LIVE in its live section** —
  at least seven requests. **The NEW check does not: it talks only to
  127.0.0.1.** A genuine Binance outage turns the live section red and that is
  correct.
- **`cockpit\whales.py --gate` NOW BINDS A LOCAL PORT.** If your machine refuses
  that, the new checks go red and it is the machine, not the code — **say so
  rather than repairing the gate.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` AND STILL PASS.**
  The bar is 3 of 5 publishers and 3 stories.
- **ANY DRILL PRINTING `INERT` INSTEAD OF `CAUGHT` IS A FAIL** — **except that
  an INERT W15/W16/W17 now MEANS the real fault is already installed in the
  file.** That is not a false alarm; it is the drill saying "this break is
  already here."
- **S6, F10 AND B1 NO LONGER GO RED.** If any does, it is a regression and
  SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **Red TWICE in a row is real.**
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** Commit it SEPARATELY, labelled as the laptop task's work.
- **`journal/oi_recorder.log` IS UNTRACKED AND IT IS NOT YOU EITHER.** Still not
  in `.gitignore`. **Leave it or ignore it deliberately.**
- **THE WEEKLY OPEN-INTEREST TASK COMMITS LOCALLY WITHOUT PUSHING.** Pull, and
  push whatever it left behind.

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **R-060: HE RULED "CORRECT IT" ON 2026-08-18.** It is corrected. **Do not
   re-ask; do ATTACK the correction.**
2. **R-054 IS SMALL.** Ruled 2026-08-11. **R-047 AND R-048 ARE SMALL.** Ruled
   2026-08-05.
3. **THE DAILY NEWS COUNT ARCHIVE WAITS UNTIL THE WHOLE PROGRAMME IS COMPLETE.**
4. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
5. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
6. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
7. **DOOR 3 IS BUILT IN BOTH COCKPIT INSTRUMENTS, THE CALENDAR AND THE WHALE
   WATCH. R-025 IS CLEARED.** Residue R-033. **`news.py` is the one without it
   (R-046).**
8. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
9. **NEWS, THE CALENDAR AND THE WHALE WATCH ARE INFORMATION AND CAN NEVER
   BECOME SIGNALS.** Phase 6's three slots are locked BY NAME: Turtle/Donchian,
   funding-rate fade, on-chain cycle thermometer.

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship.**

1. **`PROGRESS_LOG.md`, the LAST THREE entries** — the attack, the gate
   declaration, and the repair. The file is ~750 KB; do not read it all.
2. **`REVIEW_QUEUE.md`, the two 2026-08-18 blocks** — R-058's verdict, R-060 to
   R-066.
3. **`cockpit/whales.py`** — the production half (1–363) to know what is being
   protected, then **the new section `(l2)` and the drill** to know what you are
   attacking.
4. **`ROADMAP.md`, the two 2026-08-18 measured-fact tables.**

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo.** `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **CHECK ALL YOUR ANCHORS BEFORE WRITING A SINGLE BYTE**, and refuse on any
  that matches other than exactly once. **Refuse again if the patched file
  carries one bare newline, and again if the production hash moved.** That is
  the shape the last patch used and it is the shape to copy.
- **>>> DO NOT COMPARE LINE ENDINGS AGAINST `git show HEAD:<file>`. THAT HANDS
  BACK THE BLOB, WHICH IS LF.** Judge line endings in the WORKING TREE.
- **`.bat` FILES MUST BE CRLF.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** **And a newer bite: a long shell
  HERE-DOCUMENT carrying this ship's prose failed to parse on 2026-08-18. Write
  documents with an editor tool, not with `cat <<EOF`.**
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare the counts against `git show HEAD:<file>`;
  `PROGRESS_LOG.md` legitimately carries a few inside backticks and
  `SESSION_ORDERS.md` carries this very line.**
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH. `python …` ON ITS OWN DOES NOT WORK ON HIS MACHINE.** His
  PowerShell opens at `C:\WINDOWS\system32`. The working form is one line:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces a
  fresh one, `CHECK_STATUS.bat` shows the collection's health.

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL.

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... your verdict on R-066 (you may clear it only if you
                            did not build the repair), plus one OPEN item
                            against whatever you did yourself.
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; correct any MEASURED fact that
                            moved.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words brief.
                            **>>> AND THEIR JOB 1 IS: ATTACK WHATEVER YOU BUILT
                            OR REPAIRED. If you shipped no code, say so plainly
                            and give them the next real job — but NEVER write an
                            exemption. Only the Commander grants one, in words.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> NEW AND FIRST: THE BRIEF'S PRICE DATA FAILED ON 2026-08-18.** Yahoo
   returned a `JSONDecodeError` for `BTC-USD` when the Brief was run after the
   repair. **It is not the whale watch and not this repair — the production half
   was never touched.** It may be a transient, or it may be **the TwelveData key
   that has been waiting for rotation since Phase 2** (item 12 below). **The
   next session checks it first.**
2. **>>> STILL HIS BECAUSE A MACHINE MAY NOT ANSWER IT: DOES THE WHALE WATCH
   LINE READ HONESTLY TO HIM?** The label says "Whale watch"; the words under it
   say NOT exchange flows, NOT wallet tracking, NOT the world's whales.
   **One word changes the label if he wants it changed.** (R-058 doubt 6.)
3. **>>> R-049 IS DEFERRED THREE TIMES. Offer it again and say "fourth time".**
4. **THE CATEGORY B PILE IS THIRTY-FIVE.** **Keep saying the number.**
5. **ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — the only thing he personally
   owes the R-037 repair:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

6. **`data/events.json` SHIPS WITH ITS TIMEZONE SET TO `UTC` AND HIS MACHINE
   RUNS UTC+5.** One word changes it to `"Asia/Karachi"`.
7. **THE TWO NEWER PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** BeInCrypto and
   Bitcoin.com.
8. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED ELEVEN TIMES:** *"A SABOTAGE
   MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."*
   **It earned its keep twice on 2026-08-18** — once making a session throw away
   two of its own escapes, and once turning W17 from a worthless check into a
   real one. Also unadopted: **"EVERY THRESHOLD IS TESTED AT THE EXACT VALUE
   WHERE IT TURNS OVER"**, and **candidate Law 8 — "a claim about how something
   behaves is not a fact until it has been run"**.
9. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5).
10. **R-051 — nothing re-reads the Fed's and the BLS's pages automatically.**
11. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.**
12. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2, and
    **now possibly implicated in item 1.**
13. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
14. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
15. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
    `fetch_history` still freeze their globals. **`cockpit/whales.py` is the
    worked example built the right way from birth.**
16. **The settled-rate anchor (R-004).**
17. **ALL FIVE CONTEXT DECK LINES ARE ON THE BRIEF** and he was told. One word
    removes any of them.
18. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED NINE TIMES, NOT ADOPTED.**

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** **Information instruments can carry the lighter guard. The gauntlet
cannot, at any weight.**
