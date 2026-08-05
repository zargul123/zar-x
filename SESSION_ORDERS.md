# ZAR X PHASE 3 — **ATTACK MY REPAIR. I CHANGED HOW EVERY FIELD IN EVERY FEED IS READ, AND I AM THE ONLY PERSON WHO HAS EVER RUN THE CHECKS THAT SAY IT WORKS.**

*Written 2026-08-05 by the eighteenth generation, which attacked the news
instrument, found it rewriting publishers' headlines, and repaired it. **I have
given you no cap and no exemption. I am not allowed to, and I am the last person
who should.***

---

# **>>> YOUR SESSION**

    PART 1 — ATTACK what I repaired. UNCAPPED. NO EXEMPTION.
    PART 2 — BUILD step 3b, the daily news count archive, if PART 1 leaves room.

**THE OUTSIDE CHECK IS FULL AND UNRESTRICTED.** It was reduced three sessions
running (exemption, exemption, cap — all three the Commander's, all three
justified, all three over). **The seventeenth generation reset the count and
took a full attack. It found something. I took a full attack on its work and
found something. The count stays reset and you take a full one too.**

**AND HERE IS WHY IT DOES NOT TRANSFER TO ME, IN HIS OWN Q2:**

    my repair ... `_parse` is the code that turns a publisher's bytes into the
                  words on his Brief. I changed how SIX fields are read, not
                  one. A fault in it puts a WRONG or MISSING headline on his
                  screen. **Q2 = YES. The opposite of SMALL.**

**I FOUND A REAL LEAK IN A FILE ITS BUILDER HAD JUST ATTACKED CAREFULLY AND
HONESTLY — AND IT WAS IN NONE OF THE FIVE PLACES HE NAMED.** His list was good.
It was still the wrong list, **because nobody can invent the attack they are
blind to.** Assume the same is true of everything below.

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
    cockpit/news.py             GATE 3.3-R1   PASSED  exit 0  0 red  ~25 s
                                54 checks, 12 sabotages, all CAUGHT
    vault INTACT · Brief 3/3 · lab/ untouched
    data/oi_history/  3 files, 222 lines each — untouched; I did not run the
                      recorder. Next scheduled run 10-Aug-2026 09:00.

**EVERY GATE ON THIS SHIP IS GREEN AND ALL FIVE INSTRUMENTS ARE CORRECT.**

## What happened in the session before you, in four lines

1. **THE NEWS INSTRUMENT WAS SILENTLY REWRITING PUBLISHERS' HEADLINES.** A
   headline written `Bitcoin <b>crashes</b> 20% as ETF outflows accelerate`
   reached the Brief as the single word **`Bitcoin`** — no clip mark, nothing
   saying so, fifty green checks while it happened. **Repaired.**
2. **IT WAS NEVER FIRING, AND I MEASURED THAT INSTEAD OF ASSUMING IT.** 136 real
   titles across all five publishers that morning: none carried markup. **I
   reported the number that argued against my own finding.**
3. **TWO MORE FAULTS ARE FILED AND DELIBERATELY NOT FIXED** — R-047 and R-048,
   both graded SMALL. **R-047 is the interesting one: a single future-dated
   stamp walks straight past the dead-feed guard this whole file is built
   around.**
4. **THE DAILY COUNT ARCHIVE IS STILL NOT BUILT.** Deferred twice now. It is
   your JOB 2 and it is the last unbuilt thing in Phase 3 step 3.

---

# **JOB 1 — ATTACK `cockpit/news.py`'s REPAIRED `_parse`. UNCAPPED.**

**BREAK IT IN A COPY OF THE WHOLE REPO OUTSIDE THE REPO**, run the untouched
copy FIRST so you know the rig works, and **write it up either way** — *"I
attacked it hard and found nothing"* is a real, successful result and clears the
item. **DO NOT MANUFACTURE A DEFECT TO JUSTIFY A SESSION.**

## **>>> START HERE. R-049 IS MY OWN LIST OF WHERE I AM WEAKEST.**

1. **N12 AND CHECKS (r1)-(r4) WERE WRITTEN BY THE PERSON THEY ARE MEANT TO
   CATCH.** N12 reverts `_text` to the original fault and is proved to change
   the block before its verdict counts, so it is not the inert kind. **It is
   still marking its author's homework. Make the repaired `_parse` lie in a way
   N12 would not notice.** This is the sharpest thing on the list.
2. **FOUR SHAPES I TESTED WHILE WRITING THESE ORDERS — RECORDED SO YOU DO NOT
   REDO THEM, AND SO YOU CAN CHECK MY WORKING:**

       a nested tree  <b>crashes <i>hard</i></b> .. "Bitcoin crashes hard today"
       an XML comment inside the title ............ "Bitcoin crashes 20%"
       markup inside <pubDate> ................... parsed fine, story in window
       no space around the tag  Bitcoin<b>crashes</b>20%
                                                 .. "Bitcoincrashes20%"

   **The first three are correct. The fourth is correct too, and I want to be
   precise about why rather than leave you chasing it:** joining an element's
   text with nothing between the pieces is exactly what XML text content means
   — a browser renders `Bitcoin<b>crashes</b>20%` as `Bitcoincrashes20%` as
   well. **The instrument is reproducing the publisher faithfully, which is the
   whole point.** **I first wrote this bullet claiming it was the most likely
   real finding in the file. I went and ran it instead of shipping the claim,
   and it was wrong. THAT correction is the useful part of this bullet.**
3. **SO `itertext()` IS TESTED TO TWO LEVELS AND NO FURTHER.** I did not serve a
   processing instruction, a CDATA section mixed with elements, or a title
   built from ten nested spans. **Go deeper than I did.**
4. **AND THE PLACE NOBODY HAS EVER LOOKED: `_fetch` FOLLOWS REDIRECTS.**
   `requests.get` follows them by default and nothing checks where it landed.
   **A publisher whose domain lapses could serve another company's feed and
   this instrument would attribute every headline to the name in `FEEDS`.** I
   did not test it. It is not in any review item. **It is yours if you want it.**

## THE OTHER TWO THINGS WORTH YOUR TIME

6. **R-047 — THE DEAD-FEED GUARD HAS A GAP AND I LEFT IT THERE ON PURPOSE.**
   One future-dated story sorts to the front, the computed age goes negative,
   and the abandoned-feed check never fires. **I graded it SMALL because no
   stale headline reaches the Brief — only the publisher count and the
   `[no data:]` naming are lost. Read the item and decide whether I graded it
   too kindly.** The fix is a handful of lines inside `_gather`.
7. **R-035 — CAN A SOURCE ITSELF LIE?** Still the strongest candidate for a
   whole session's attack, and **X1 is a new argument for it**: that was not a
   source lying, it was us mis-reading a source telling the truth perfectly —
   and it landed in the same place, a false headline nothing would have flagged.

## **>>> THE RULE THAT DECIDES WHETHER WHAT YOU FIND STOPS YOU**

**Fill in THE FINDING REPORT in `THE_PATTERN.md` BEFORE repairing anything — the
report comes before the repair, always.** Then his own scoring:

    it puts a WRONG, STALE or INVENTED headline on his Brief ... it STOPS you.
    it touches the SAVED ARCHIVE .............................. it STOPS you.
    it is a weakness in the TEST that cannot reach his screen . Q2 = NO ->
                                                 SMALL. File it CATEGORY B and
                                                 KEEP BUILDING.

---

# **JOB 2 — RULE ON MY THREE ITEMS. YOU MAY; I MAY NOT.**

**R-047, R-048 and R-049 are MY OWN doubts, filed with the work and not after
somebody asked.** Read them in `REVIEW_QUEUE.md` and say plainly whether each
holds. **R-042, R-043, R-044, R-045 and R-046 are also still open** — I verified
R-044 and R-046 rather than clearing them, and my reasons are in the queue.
**R-042 and R-043 I never touched at all.**

---

# **JOB 3 — BUILD STEP 3b: THE DAILY NEWS COUNT ARCHIVE. ONLY IF PART 1 LEAVES ROOM.**

**IT HAS NOW BEEN DEFERRED TWICE AND THE COMMANDER SHOULD NOT HAVE TO NOTICE
THAT FOR HIMSELF.** The seventeenth generation left it out as a half-built
writer. **I left it out because X1 graded SERIOUS and SERIOUS means fix it and
stop.** Both reasons were the rules working. **Twice is still twice.**

    date,       total,  coindesk,  cointelegraph,  decrypt,  beincrypto,  bitcoin_com
    2026-08-05,   86,      25,          30,           12,        10,           4

**WHY IT EXISTS, IN HIS OWN WORDS: you cannot know that 43 headlines an hour is
unusual unless you know that 11 is normal — and the feeds hand you only the last
10 to 59 stories, a few hours' worth. THERE IS NO ARCHIVE AND THE PAST CANNOT BE
BOUGHT**, because old articles are edited, retitled and deleted, so any sold
"news history" is polluted by hindsight — which Law 7 says the Lab's own numbers
can never detect. **`data/oi_history/` exists for exactly this reason.**

**BUILD THE BORING FILE. DO NOT BUILD THE NEWS-STORM FLAG** — it is in the
README's vision and is **NOT a scheduled step in Phases 3-8**, and a session
that finds itself building a signal out of headlines has misread the plan.

**DECLARE ITS GATE AND COMMIT IT ALONE WITH NO `.py` IN THE COMMIT.** Name the
awkward cases first: two runs on one day, a run that fails halfway, a day with no
run at all, a publisher that was dead that day, and **the file being read by a
later session that must not be able to tell a real zero from a missing day.**

**IF IT WILL NOT FIT, BUILD NOTHING AND SAY SO.** That rule is not capped and
never will be. **A half-built part is worse than no part.**

## **>>> AND THE THING YOU MUST WRITE INTO YOUR OWN ORDERS**

    >>> IF YOU BUILD ANYTHING, THE ORDERS YOU WRITE MUST SEND THE SESSION
    >>> AFTER YOU TO ATTACK IT — FULLY, AND WITH NO CAP OF ANY KIND.
    >>> YOU MAY NOT GRANT AN EXEMPTION OR A CAP TO ANYONE, INCLUDING THE
    >>> SESSION AFTER YOU. ONLY THE COMMANDER CAN.
    >>> AN EXEMPTION DIES WITH THE SESSION IT WAS GRANTED TO. SO DOES A CAP.
    >>> THEY ARE THE SAME ANIMAL AT DIFFERENT SIZES.

---

# THE RULES THAT APPLY TO WHATEVER YOU DO

**DECLARE THE GATE IN `PROGRESS_LOG.md` AND COMMIT THAT ENTRY ALONE, WITH NO
`.py` IN THE COMMIT, BEFORE WRITING CODE.** Twenty-three uses, twenty-three
audits survived; mine was `f17f32f`. **RECORD YOUR HASH *AFTER* YOUR FINAL
PUSH** — the cloud watchman pushes every four hours and `git pull --rebase`
rewrites hashes underneath you.

(a) **NOTHING THE PILOT READS CHANGES unless that IS the job — prove it two
    ways, never assert it:** every diff hunk at or after the `__main__` line,
    AND a sha256 of the production half printed before and after. **THE
    RECIPES DIFFER BETWEEN FILES AND HAVE BEEN WRONG ON RECORD BEFORE:**
    - `cockpit/funding.py` — `__main__` at line 160; lines 1..159 joined by
      CRLF **WITH** a trailing CRLF → `95069d1bef8316d766910abda1880931…`
    - `data/open_interest.py` — `__main__` at line 243; lines 1..242 joined by
      CRLF with **NO** trailing separator → `5347bfecdf2ccfb2009770f9161dd6c5…`
    - **`cockpit/news.py` — `__main__` MOVED FROM 250 TO 272 WHEN I REPAIRED
      `_parse`.** Lines 1..271 joined by CRLF **WITH** a trailing CRLF →
      `503663762315b2f271d74dd2bdcf43bd…` **(it was `0f0d6386…` before my
      repair; the production half changed BECAUSE THE REPAIR WAS THE JOB).**
      The no-trailing-separator form is `6f4f69f4377e4158…` and is NOT the
      prefix for this file.
    - **>>> DO NOT TRUST ANY OF THOSE NUMBERS. VERIFY THE JOIN IS BYTE-FOR-BYTE
      THE RAW PREFIX OF THE FILE and refuse to print a hash if it is not.**
      That is how I confirmed the recipe rather than inherited it.
    - **A WHOLE-FILE HASH CANNOT DO THIS JOB.** It cannot tell "the pilot's
      code changed" from "the test around it changed".
(b) **THE GATE NEVER READS ITS EXPECTATION OUT OF THE FILE ON TRIAL**, never
    calls the helper under test to judge itself, and **NEVER ASKS THE MODULE
    WHERE TO LOOK.**
(c) **THE DRILL IS PERMANENT** — breaks stay in, caught every run, originals
    restored and the restoration verified. **`_text` is now in that restoration
    check; if you add a break, add it there too.**
(d) **EVERY SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT
    COUNTS, AND ON THE CHANNEL IT ACTUALLY AFFECTS.** N10 returns a
    byte-identical block and only changes stdout — a drill measuring every
    sabotage on one channel would score it INERT and delete the only check that
    catches it.
(e) **RE-RUN THE ORIGINAL FAULT AGAINST ANY REPAIR YOU MAKE. A repair nobody
    re-tested is a hope.**
(f) Everything the old gates did, they still do.
(g) **RUN `py_compile` BEFORE THE GATE.**
(h) **FILE A REVIEW ITEM AGAINST YOUR OWN WORK AND LEAVE IT OPEN.** You may not
    clear your own. **You MAY clear R-042 through R-049 — but check first
    whether you are the one who benefits from clearing them.** That test is why
    I did not clear R-046.

**PASS = every check green including every sabotage CAUGHT. Anything less is a
FAIL, is not committed as a pass, and is not called "mostly passed."**

---

# **WHAT YOU WILL WALK INTO — DO NOT MISTAKE IT FOR YOUR OWN BREAKAGE**

- **`python cockpit\funding.py` GOES RED NEAR A FUNDING SETTLEMENT** (R-021).
  Binance settles **00:00, 08:00, 16:00 UTC**. I ran clean at 12:10 UTC, about
  3h50m clear. **Outside a settlement window a red funding gate is a REAL
  failure — treat it as one.**
- **`cockpit\news.py --gate` MAY PRINT `[no data: <publisher>]` IN ITS LIVE
  CHECK (c) AND STILL PASS.** The bar is **at least 3 of 5 publishers and at
  least 3 stories.** **All five answered on all three of my readings.** **If it
  drops BELOW 3 of 5, that is real and it is R-044.**
- **THE `(l)` DRILL PRINTS `INERT` INSTEAD OF `CAUGHT` IF A SABOTAGE STOPS
  CHANGING THE OUTPUT, AND INERT IS A FAIL.** **If you see INERT, something
  real has drifted.**
- **S6, F10 AND B1 NO LONGER GO RED.** If any goes red it is a regression of a
  shipped repair and SERIOUS.
- **`data/collection_guard.py --gate` MAY GO RED ON CHECK (g) ONCE AND GREEN
  IMMEDIATELY AFTER** (R-041 doubt 3). **It was green first time for me.** If
  it goes red TWICE in a row, it is real.
- **THE RECORDER'S GATE TAKES ~55 s AND MUST BE RUN TWICE** — once normally and
  once with `TZ=UTC0`.
- **`journal/snapshots_local.csv` WILL BE MODIFIED IN `git status` AND IT IS NOT
  YOU.** The laptop's own scheduled snapshot writes it while you work. **Do not
  commit it as part of your change and do not revert it.**

# **WHAT THE COMMANDER HAS ALREADY RULED — DO NOT ASK HIM AGAIN**

1. **`cockpit/brief.py` GETS NO GATE YET** — not now, before going live.
2. **R-016 IS OFF HIS DESK.** Still not cleared; that is R-022.
3. **R-019 IS CLEARED BY HIM.** Step 2.2 carries his own wording in
   `THE_PATTERN.md`. **Read it there before you grade anything.**
4. **DOOR 3 IS BUILT IN BOTH COCKPIT FILES. R-025 IS CLEARED.** Residue R-033.
5. **F10, S6 AND B1 WERE ALL REPAIRED ON HIS RULING, AND ALL THREE HOLD.**
6. **THE CRYPTOPANIC SIGNUP IS OFF HIS DESK PERMANENTLY.**
7. **R-037 WAS ORDERED SORTED FIRST AND IT WAS.** Done 2026-08-03.
8. **THE EXEMPTION AND THE CAP ARE BOTH OVER.** They died with the sessions they
   were granted to. **You have neither.**
9. **NEWS IS INFORMATION AND CAN NEVER BECOME A SIGNAL.** Phase 6's three slots
   are locked BY NAME — Turtle/Donchian, funding-rate fade, on-chain cycle
   thermometer. **None is news.** A headline that is advice is printed in quotes
   and attributed; **the Brief's own voice never adopts it.**

# READ THESE FIRST

**`THE_PATTERN.md` already told you how a session begins, what every file is
for, the run environment and the housekeeping that has bitten this ship. None of
it is repeated here.**

1. **`REVIEW_QUEUE.md` — R-047, R-048 and R-049 are your worklist**, plus
   R-042 to R-046 if you want them. **R-006 may NEVER be cleared by you or any
   in-house session.**
2. **`cockpit/news.py`** — the whole file. It is 930 lines; **the part the pilot
   reads is lines 1..271** and the gate is everything from line 272 on. **The
   repair is `_text` at lines 127-148 and its two call sites in `_parse`.**
3. **The LAST TWO entries of `PROGRESS_LOG.md`.** The file is ~600 KB; reading
   all of it will eat your budget.

# HOUSEKEEPING THAT HAS ALREADY BITTEN THIS SHIP

- **`git pull` FIRST.** A cloud watchman pushes every four hours.
- **Work on copies OUTSIDE the repo**, and copy the WHOLE repo; 34 MB, costs
  nothing. `git status` clean when you are done.
- **EDIT IN BINARY. These `.py` files are CRLF and so are all five documents.**
  **EMIT PAYLOADS AND ANCHORS WITH `repr()`**, and put **no backslash escapes in
  a payload at all** — use `bytes([10])` for a newline.
- **>>> WRITE THE SCRIPT TO A FILE AND RUN THE FILE. NEVER PASS PYTHON TO A
  SHELL AS A `-c` STRING OR A HERE-STRING.** PowerShell eats the quotes and
  **bash eats every BACKTICK as a command substitution.** **The fifteenth
  generation lost two commands to this, the sixteenth lost one after reading the
  warning, the seventeenth lost one after reading BOTH.** **I obeyed it and lost
  none. It works if you actually do it.**
- **`.bat` FILES MUST BE CRLF.** A LF-only batch is silently refused by `cmd`
  with **no output and exit 1**.
- **IF YOUR TEXT ANCHOR MATCHES MORE THAN ONCE — OR ZERO TIMES — REFUSE TO RUN.**
  **Nine consecutive sessions have guarded this way.**
- **PYTHON HERE IS 3.10, WHERE A BACKSLASH INSIDE AN F-STRING *EXPRESSION* IS A
  SyntaxError.** Name the value first, or use `chr(10)`.
- **NEVER use PowerShell `Get-Content`/`Set-Content` on this repo's UTF-8 files.**
- **SCAN THE FIVE DOCUMENTS FOR MOJIBAKE BEFORE YOUR FINAL COMMIT** — `â€`,
  `Â·`, `â†`, `Ã`, `âœ`. **Compare your counts against `git show HEAD:<file>`;
  `PROGRESS_LOG.md` legitimately carries 2, 3 and 2 of the first three inside
  backticks, as deliberate quotations of the damage.**
- **RUN THE THING AND READ ITS OUTPUT.** "Success" from a tool is not evidence.
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe`, `PYTHONUTF8=1`.
- **>>> ANY COMMAND YOU HAND THE COMMANDER MUST CARRY THE FOLDER AND THE FULL
  INTERPRETER PATH. `python …` ON ITS OWN DOES NOT WORK ON HIS MACHINE** — bare
  `python` hits a **pyenv shim with no version selected**. His PowerShell opens
  at `C:\WINDOWS\system32`. The working form is one line:

      cd "C:\Users\hp\Downloads\zargul trader\zar-x"; $env:PYTHONUTF8=1; & "C:\Users\hp\miniconda3\envs\tfdml\python.exe" cockpit\brief.py

  **AND BEFORE REACHING FOR A COMMAND AT ALL, REACH FOR THE `.bat`.**
  `SHOW_REPORT.bat` opens the latest Brief in Notepad, `run_daily.bat` produces a
  fresh one, `CHECK_STATUS.bat` shows the collection's health. **They already
  carry the `cd /d` and the full interpreter path.**

---

# **>>> HOW YOUR SESSION ENDS**

## THE CLOSING RITUAL — SEVEN STEPS, NONE OPTIONAL

**`THE_PATTERN.md` sets these out in full and they are not repeated here.**

    1. PROGRESS_LOG.md .... what happened, the real numbers, and EVERY mistake
                            as plainly as every success. Append only.
    2. REVIEW_QUEUE.md .... verdicts on what you attacked, plus one OPEN item
                            against anything you built or repaired yourself.
    3. EXECUTION_PLAN.md .. the CURRENT POSITION MARKER, rewritten to the truth
                            including what is broken. Keep the old markers.
    4. ROADMAP.md ......... tick what shipped; correct any MEASURED fact that
                            moved.
    5. SESSION_ORDERS.md .. rewritten IN FULL, opening with a plain-words
                            brief, **WITH PART 1 ATTACK IN IT AND NO CAP.**
    6. Commit. Push. **Then check your commit hashes again.**
    7. **REPORT TO HIM IN PLAIN WORDS** — what you tried, what broke, what held,
       **what you got wrong**, and what decision is his.

**AND THE STANDING DUTY: if you catch yourself writing "probably", "almost
certainly" or "this should be fine" about anything that ships — FILE IT in
`REVIEW_QUEUE.md` before the commit that ships it.**

# ON THE COMMANDER'S DESK (do not let these drop)

1. **>>> R-047 IS HIS TO RULE ON AND IT IS THE ONE I MOST WANT HIM TO SEE.** I
   found that a single future-dated stamp walks straight past the dead-feed
   guard — **the guard the whole news file is shaped around** — and I graded it
   SMALL and did not fix it, because no stale headline reaches his Brief; only
   the publisher count and the `[no data:]` naming are lost. **He may think that
   is too kind. The fix is a handful of lines and one word from him orders it.**
2. **>>> THE TWO NEW PUBLISHER NAMES ARE STILL HIS TO OVERRULE.** He ruled the
   PRINCIPLE — five publishers, different owners, not one hundred. **The five
   NAMES came from one probe, and two of the originally-ordered five were dead**
   (The Block edge-blocked, Blockworks 209 days stale). BeInCrypto and
   Bitcoin.com were substituted. **Second-day evidence: all five answered on all
   three readings on 2026-08-05.** Law 2 means changing either is a one-line
   edit inside `cockpit/news.py`.
3. **>>> ONE COMMAND HE MUST RUN AS ADMINISTRATOR** — still the only thing he
   personally owes the R-037 repair. The Task Scheduler event log is switched
   off, so a next time would leave no evidence either:

       wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true

4. **THE CATEGORY B PILE IS TWENTY-TWO DEEP.** R-047, R-048 and R-049 added;
   nothing cleared. **It has grown every single session since it was created and
   has never once shrunk.** Cleared before the ship is used for real, at the
   same moment `brief.py` gets its gate. **Somebody should keep saying the
   number out loud to him, and this is me saying it.**
5. **THE RULE HE HAS NOT YET ADOPTED, NOW EARNED SIX TIMES:** *"A SABOTAGE MUST
   BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT MEANS ANYTHING."*
   **N12 is the sixth proof: it was written under that rule from birth and it is
   the check that would have caught X1 a day earlier had it existed.**
   **A session may never promote its own idea to law. THIRTEEN OTHER CANDIDATES
   REMAIN UNADOPTED.**
6. **THE WEEKLY SCHEDULE LIVES IN WINDOWS, NOT IN GIT** (R-041 doubt 5). If the
   laptop is rebuilt the task silently returns to monthly and no gate will say
   so. Next run 10-Aug-2026 09:00.
7. **>>> NOBODY HAS EVER ASKED WHETHER A SOURCE ITSELF CAN LIE (R-035).** No
   file on this ship talks to more than one source. **Every gate proves the
   printed line matches what the source SENT; nothing asks whether the source
   was RIGHT.** **X1 is a new argument for this: it was not a source lying — it
   was us mis-reading a source that was telling the truth perfectly — and it
   landed in exactly the same place, a false headline nothing would have
   flagged.** **Still the strongest candidate for a whole session's attack.**
8. **R-024 doubt 2 IS STILL HIS: the hardcoded positive control.** Unchanged.
9. **FIX THE PATTERN, NOT JUST THE TEST.** `def run(symbols=SYMBOLS, ...)` and
   `fetch_history` still freeze their globals. **The one-line change that ends
   this class is `symbols=None`, resolved in the body.** It touches what the
   pilot reads, so no session may make it during a repair to a test. **Thirteen
   generations have now fixed the instance and left the pattern — though X1's
   repair did NOT: it fixed all six fields, not the one that was caught.**
10. **`cockpit/brief.py` HAS NO GATE** — he has ruled: not now, before going
    live. **The inch between it and his screen was checked by hand for the first
    time on 2026-08-05 and is clean.**
11. **TwelveData key rotation** (.env + GitHub secret) — open since Phase 2.
12. **The risk-doctrine decision** — the 25% position cap means real risk is
    ~0.49% per trade, not the intended 1%. **Settled BEFORE Phase 6.**
13. **`MAX_PLAUSIBLE_RATE`** — measured 13-16x looser than Binance's published
    cap. **Recommendation: tighten to ~0.01. STILL NOT DONE.**
14. **The settled-rate anchor (R-004)** — returned to him on correct facts.
15. **THE FUNDING AND NEWS LINES STAYED ON THE BRIEF** and he was told. One word
    reverses either.
16. **A DOCUMENT-INTEGRITY CHECK. RECOMMENDED SEVEN TIMES, NOT ADOPTED.**
17. **BOTH COCKPIT GATES ARE SLOW BECAUSE OF DOOR 3** — ~125 s and ~60 s — **and
    that slowness turned out to be load-bearing** (R-033). **`news.py`'s gate is
    ~25 s precisely because it does NOT have that machinery, and R-046 is now
    PROVEN rather than suspected: an `os.write(1, …)` from inside the doorway
    was completely inaudible to it.** That is the trade, and it is visible in
    the clock.

**AND THE ONE THAT DOES NOT EXPIRE: at Phase 6 the "separation in time"
substitute for Fable EXPIRES.** A second, genuinely independent AI reviews the
gauntlet's test setup before it runs and its verdict after. Locked in
`EXECUTION_PLAN.md` Phase 6, it is R-006, and it is **NOT waived by Fable's
absence.** Information instruments can carry the lighter guard. **The gauntlet
cannot.**
