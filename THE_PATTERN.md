# ZAR X — THE PATTERN (how a session runs, every time)

**What this file is.** The rhythm this ship works to, written in plain words so
the Commander can hold every session to it without being a programmer, and so a
session with no memory of the last one knows exactly what is expected.

**What this file is NOT.** It is **not a law.** `SHIP_LAWS.md` has seven laws and
each was adopted by the Commander after a failure that earned it. This file only
describes the practice that grew out of those laws. **If this file and
`SHIP_LAWS.md` ever disagree, the laws win.**

**THIS FILE EXISTS SO NOTHING HERE EVER HAS TO BE EXPLAINED AGAIN.** The
Commander should never have to tell a session how the ship works, which file to
read, or where to write something down. **If he finds himself explaining any of
that, this file has failed and fixing it is that session's first job.**

---

# HOW A SESSION BEGINS

**The Commander says: `ZAR X`.** That is the whole thing. He names no file,
remembers no command, and repeats nothing from last time.

**Everything after that is the session's job:**

1. `cd "C:\Users\hp\Downloads\zargul trader\zar-x"` — **note the folder.** There
   is an older directory called `SAFE COPY OF LATEST ZARGUL 2` and the Commander
   often has it open. The live ship is `zar-x`. A command run in the wrong one
   fails with *"can't open file"* — this has already happened.
2. **`git pull` FIRST.** A laptop task and a cloud watchman both push here while
   nobody is looking. Skipping the pull is how two sessions overwrite each other.
3. **Read this file, then `SESSION_ORDERS.md`.** The orders open with a
   plain-words brief and carry their own read list for anything else needed.
4. **Prove the ship is alive before changing anything** — every gate green, the
   Brief `3/3`, the vault `INTACT`. **If something is already broken when you
   arrive, that is your session.** Say so and fix that instead.
5. Then do what the orders say. **They outrank anything you think of**, because
   they were written deliberately by someone who had just finished the work you
   are about to check. Disagree out loud to the Commander — never quietly.

**If a session asks the Commander what to do next, it has not read its orders.**

---

# THE NINE FILES — what each one is for, and where things get written

**Nothing else gets created.** If you want to write something down, it belongs in
one of these. **A tenth file is almost always a sign you did not read the nine.**

## The four that hold still

| File | What it is | Who may change it |
|---|---|---|
| `README.md` | **THE PROMISE** — three sealed signal slots, then the signals chapter closes. The rule the whole ship is built around. | Nobody |
| `SHIP_LAWS.md` | **The seven laws.** Each adopted after a failure earned it. | **The Commander only.** A session may propose; it may never promote its own idea to law. |
| `THE_PATTERN.md` | **This file. How a session runs.** | A session, **only** on a genuinely new lesson |
| `EDGE_STACK_RESEARCH.md` | Why the ship is designed this way. History. | Nobody |

## The five that every session updates

| File | The one question it answers | What goes in it |
|---|---|---|
| `PROGRESS_LOG.md` | **"What happened?"** | Every action, the real numbers, the real output, and **every mistake as plainly as every success.** Append only — never edit an old entry. It is the ship's memory and outranks anyone's recollection. |
| `REVIEW_QUEUE.md` | **"What can't we trust yet?"** | Every doubt, numbered `R-000`, `R-001`… Filed by the session that has the doubt — **including doubts about its own work.** Never deleted, never cleared by its own author. |
| `EXECUTION_PLAN.md` | **"Where is the ship right now?"** | The CURRENT POSITION MARKER — the truth including what is broken or unproven — plus the phases and their gates. |
| `ROADMAP.md` | **"What exists and works?"** | What shipped, and the **MEASURED data-source facts** table. |
| `SESSION_ORDERS.md` | **"What does the next session do?"** | Rewritten in full each time, opening with a plain-words brief. |

## Which file do I write THIS in?

    something I did, or got wrong ............ PROGRESS_LOG.md
    something I am not sure about ............ REVIEW_QUEUE.md  (as R-0NN)
    where the ship now stands ................ EXECUTION_PLAN.md
    a part that now works .................... ROADMAP.md
    a job for whoever comes next ............. SESSION_ORDERS.md
    a decision only the Commander can make ... SESSION_ORDERS.md, on his desk
    a new rule for how sessions work ......... nowhere yet — propose it to him

**The difference between the queue and the orders, because it is the one that
matters:** `REVIEW_QUEUE.md` is the ship's **conscience** — a doubt goes in and
does not come out until someone who did not create it says so. `SESSION_ORDERS.md`
is the **instruction** — it is thrown away and rewritten every session.

---

# WHY THIS EXISTS: FABLE IS GONE

Until Phase 2, the ship had a second, genuinely independent AI — **Fable** — who
checked work someone else had built. That mattered, and it was proven to matter:
**Fable's review caught a real defect a builder could not see** (a reviewer's own
hardcoded "15/15", recorded as R-000).

Fable is unavailable. **The substitute is separation in TIME instead of
separation in IDENTITY:** a fresh session, with no memory of writing the code,
attacks what the previous session built.

**It is weaker than Fable and everyone should say so out loud.** It is also not
nothing — **on 2026-07-26 a fresh session found four deliberate lies walking
through a gate that was reporting 48/48**, in code it had no memory of writing.

---

# THE THREE LAYERS (they are not the same thing, and this is where confusion starts)

## Layer 1 — THE GATE: the standard, written down BEFORE building

The pass/fail bar is declared and **committed on its own, with no code in that
commit**, before the thing being measured exists. Then `git show --stat` proves
the bar came first and nobody quietly lowered it to match what got built.

*Who can do this: the builder.*

## Layer 2 — THE SABOTAGE DRILL: the code breaks itself, forever, every run

The part deliberately breaks itself several ways every single time it runs, and
**fails loudly if any breakage goes uncaught.** This proves the alarm is capable
of saying no.

**This is the layer the ship did not have, and its absence cost a voided 48/48.**
Nine deliberate lies were walking through two green gates on 2026-07-26 —
**every check ran, every check passed, nobody had ever tried to break them.**

*Who can do this: the builder.*

## Layer 3 — THE INDEPENDENT ATTACK: fresh eyes invent a NEW way to break it

A session that did **not** build the thing invents a sabotage the builder never
thought of, and reports the result either way.

**THIS IS THE ONE A BUILDER CAN NEVER DO FOR THEMSELVES.** Not by being careful,
not by passing a gate, not by any tally. **You cannot invent an attack you are
blind to.** A gate is strongest exactly where it has already been attacked — so
the only useful attack is one its author never imagined.

*Who can do this: only someone who did not build it.*

---

# THE RHYTHM: EVERY SESSION DOES TWO JOBS, IN THIS ORDER

    PART 1 — ATTACK what the last session built.   (Layer 3)
    PART 2 — BUILD the next thing.                 (Layers 1 and 2)

**PART 2 IS CONDITIONAL ON HOW BAD THE PROBLEM IS — AND THE COMMANDER DECIDES
THAT, NOT THE SESSION.** If Part 1 finds something, **fill in THE FINDING REPORT
below BEFORE repairing anything**, then:

    SERIOUS ....... fix it, and stop. Build nothing.
    BORDERLINE .... do NOT fix it. Report and stop. The Commander rules.
    SMALL ......... do NOT fix it. File it in REVIEW_QUEUE.md as CATEGORY B
                    and carry on to PART 2.

**THE REPORT COMES BEFORE THE REPAIR, ALWAYS.** Its entire purpose is to decide
whether the repair is worth doing now. A session that repairs first and grades
afterwards has spent the time it was supposed to be deciding about, and is asking
the Commander to approve something already done.

**A session may recommend. It may never rule** — and it may never grade its own
repair. **Adopted 2026-07-28 (night) by the Commander**, after six consecutive
reviews each found something and Step 3.3 was deferred four times running while
the severity of what was being found fell from *"prints the opposite of the
truth"* to *"would not catch a line nobody has written."*

A session that reviews its predecessor and then hurries into building has not
reviewed anything; it has performed a review. **But a session that repairs every
imaginable weakness in a test before it is allowed to build has stopped
protecting the project and become the project.**

**If the session is running short, do PART 1 properly and leave PART 2 entirely.**
A half-built part is worse than no part.

## What PART 1 looks like

1. Write the bars for "this review clears" into notes **before running anything**.
2. Invent at least one **NEW** sabotage. Break the code on purpose **in a scratch
   copy outside the repo**. Run the untouched copy too — if the control does not
   pass, the rig is broken and nothing concluded means anything.
3. Confirm `git status` is clean afterwards.
4. **Write it up either way.** "Reviewed, found nothing" is a real result.
   A review that only appears in the log when it finds something teaches the next
   session that silence means safety.
5. Record the verdict in `REVIEW_QUEUE.md`.

## What PART 2 looks like

1. **Declare the gate. Commit it alone, with no code in that commit.**
2. Define the awkward edge cases **before** writing code, not after discovering
   them.
3. Build. Confine changes as narrowly as possible and **prove the confinement**
   (e.g. diff hunk line numbers), never assert it.
4. Run the gate. **Every check green, including every sabotage caught.**
5. **A failing gate is never committed and never called "mostly passed".**
6. Record everything in `PROGRESS_LOG.md` — mistakes as plainly as successes.
7. File what you could not certify in `REVIEW_QUEUE.md`. Commit. Push.
8. Write the next session's orders in `SESSION_ORDERS.md`.

---

# THE FINDING REPORT — filled in for EVERY finding, BEFORE any repair

**Why it exists.** The Commander is not a programmer. Without a fixed form he
cannot tell a bug that would quietly cost him money from one that could only
happen if somebody set out to cause it — so every finding looked equally urgent,
building stopped every time, and the Context Deck sat at two instruments of five.

**He judges the ANSWERS, not the code.** Every question is answerable in one
plain sentence. **A vague or dodged answer is itself the warning sign**, and
spotting a dodged question needs no technical knowledge at all.

**Every question below was earned by something that actually happened on this
ship.** None was invented for tidiness.

## STEP 0 — IS THE FINDING EVEN TRUSTWORTHY?

*Any wrong answer here and the finding is NOT PROVEN. Do not classify it. Redo
the test.*

    0.1  Did the healthy, untouched system pass FIRST?                bad: no
    0.2  Did you PRINT the broken version's output and show it is
         visibly wrong?                                               bad: no
    0.3  Are you judging your OWN work?                              bad: yes

**Earned by:** sabotage B5, scored CAUGHT while crashing two lines before the
check it claimed to prove — found by reading, not by any check. And by six
straight generations where the builder graded himself and the next pair of eyes
found something every time.

## STEP 1 — THE VETO QUESTION. ASK IT FIRST.

    If this went wrong, would it change something the Commander would ACT on,
    or damage a record we keep?

    NO  -> it CANNOT be serious. File as CATEGORY B. Stop here.
    YES -> continue.

**Earned by R-007:** a genuine race that can print a settlement time a few
seconds stale. A real defect. **It changes nothing for anybody**, and rating it
P3 was correct.

## STEP 2 — THE THREE BIG ONES. ANY BAD ANSWER = SERIOUS.

    2.1  Could this happen BY ACCIDENT, or only if someone did it
         on purpose?                                        bad: by accident
    2.2  Would the Commander SEE it with his own eyes?              bad: no
    2.3  Could it be UNDONE later?                                  bad: no

**Earned by:** B10 — one tiny slip away from B4, which was already on the list
(2.1). The very first sabotage ever found, a flipped sign printing the exact
opposite of the truth on a screen that looked perfectly normal (2.2). And
Binance's 30-day window, which cannot be bought back at any price (2.3).

## STEP 3 — WHAT MAKES IT WORSE. ANY YES = BORDERLINE, THE COMMANDER RULES.

    3.1  Would the system still report "all fine" while this happened?
    3.2  Does it touch the saved records that cannot be re-bought?
    3.3  Does it touch anything that TELLS HIM TO ACT — advice, or the
         signals chapter?
    3.4  Does it affect one thing once, or everything, forever?

**Earned by:** the naive recorder that would have **reported success every month
while collecting nothing** (3.1); sabotage F8, which printed *">> strong buy
signal"* on the deck of an information-only ship while the gate applauded (3.3);
and B7, which left the first asset perfect and quietly ruined the other two
(3.4).

## STEP 4 — SAY IT IN PLAIN WORDS

    4.1  In ONE sentence: what would actually happen to the Commander if this
         went wrong?
    4.2  My recommendation: SERIOUS / BORDERLINE / SMALL — and why, in one line.

## THE SCORING

    Step 0 wrong ................ not proven. Test again.
    Step 1 = NO ................. SMALL
    Any Step 2 bad .............. SERIOUS
    Step 2 clean + any Step 3 ... BORDERLINE — the Commander rules
    Step 2 clean + no Step 3 .... SMALL

**CATEGORY B IS A PILE, AND PILES GROW.** Every SMALL finding is filed in
`REVIEW_QUEUE.md` marked **CATEGORY B**. One is nothing; twenty sitting under a
system about to be trusted with real money is not nothing. **THE WHOLE CATEGORY B
PILE IS CLEARED BEFORE THE SHIP IS USED FOR REAL** — the same moment
`cockpit/brief.py` finally gets its own gate. **A session may not quietly let the
pile become a place findings go to die.**

---

# THE CLOSING RITUAL — no session ends without this

**A session that does the work and does not write it down has not finished. The
next session inherits nothing but code it cannot trust.**

Before the final commit, EVERY session updates these, in this order:

**1. `PROGRESS_LOG.md` — WHAT HAPPENED.** Append a new entry. What was
attempted, the actual numbers and output, the verdict, and **every mistake as
plainly as every success.** Never edit an old entry; the log only ever grows.

**2. `REVIEW_QUEUE.md` — WHAT COULD NOT BE CERTIFIED.** Verdicts on the items
worked, plus any NEW doubt this session could not settle about its own work.
**Never delete an item. Never edit a cleared verdict. Never clear your own.**

**3. `EXECUTION_PLAN.md` — WHERE THE SHIP IS NOW.** The CURRENT POSITION MARKER,
rewritten to the truth, including what is broken or unproven. **Keep the previous
marker text below it for the record rather than erasing it.**

**4. `ROADMAP.md` — WHAT EXISTS AND WORKS.** Tick what shipped, correct the
MEASURED facts table if a measurement moved.

**5. `SESSION_ORDERS.md` — THE NEXT SESSION'S JOB.** Rewritten in full: what to
attack, what to build, the gate declared in advance, the edge cases named before
coding, and what is on the Commander's desk. **Write it for someone with NO
memory of you.** If a stranger could not act on it, it is not finished.

**6. Commit. Push.**

**7. REPORT TO THE COMMANDER IN PLAIN WORDS.** What you tried, what broke, what
held, **what you got wrong**, and what decision is his. Added 2026-07-27 **at his
explicit instruction**, not because a session liked the idea. **And for EVERY
finding, hand him THE FINDING REPORT above — all four steps, answered in plain
sentences. He rules SERIOUS or SMALL; you only recommend.**

**The reason is not politeness. He is not a programmer, and he is the only
person who can overrule a session.** An instruction he cannot read is an
instruction he cannot refuse, and a ship where the Commander cannot follow the
argument is a ship being steered by whoever writes the densest document. **The
orders you write in step 5 open the same way, for the same reason.**

---

# THE LOOP CLOSES ITSELF — THIS IS THE WHOLE SYSTEM, AND IT REPEATS FOREVER

    the Commander says "ZAR X"
        │
        ▼
    read THE_PATTERN.md  ──▶  read SESSION_ORDERS.md  ──▶  check the ship is alive
        │
        ▼
    PART 1 — ATTACK what the last session built
        │           found something? ──▶ fix it under a gate declared first, STOP
        ▼           found nothing?   ──▶ say so, clear the item, carry on
    PART 2 — BUILD the next thing (gate first, sabotage drill from birth)
        │
        ▼
    THE CLOSING RITUAL — log · queue · plan · roadmap · ORDERS · push · report
        │
        ▼
    the next session says "ZAR X" and starts at the top ─────────────────┐
        ▲                                                                │
        └────────────────────────────────────────────────────────────────┘

**EVERY SESSION ENDS BY WRITING THE NEXT SESSION'S JOB. That is what makes this
a loop instead of a list.** Whatever you build becomes what the next session is
ordered to attack, and whatever you fix becomes an item in `REVIEW_QUEUE.md`
that only a later session may clear. **Then that session builds something, files
its own doubts, writes the next orders — and the same thing happens to it.**

**Nobody has to restart this, remind anyone of it, or explain it again.** It
runs as long as each session performs the closing ritual honestly. **A session
that skips the ritual does not just fail to record its work — it breaks the
loop**, because the session after it arrives to no orders, no verdicts, and a
position marker describing a ship that no longer exists.

**THE THREE THINGS THAT KEEP THE LOOP HONEST RATHER THAN JUST TURNING:**
a session may never clear its own work · a gate is declared before the thing it
measures exists · every part keeps breaking itself on every run, forever.
**Remove any one and the loop still spins, but it stops proving anything.**

## `THE_PATTERN.md` IS THE EXCEPTION — DO NOT REWRITE IT EVERY SESSION

The five files above change every session. **This one holds still on purpose.**
Edit it **only when a session earns a genuinely new lesson** — a failure that
teaches something the pattern does not already say.

**A document that changes every session stops being the thing anyone trusts.**
When you do change it, say in `PROGRESS_LOG.md` what failure earned the change.

---

# THE RULES THAT KEEP IT HONEST

**A SESSION MAY NEVER CLEAR ITS OWN ITEM.** However confident it is. However
good the fix. **If you found the fault and wrote the repair, you file a new
review item against your own repair and leave it open.**

**A TALLY COUNTS ONLY WHAT A MACHINE ACTUALLY CHECKED.** Not what looked right in
the output. "48/48" was honest arithmetic over an incomplete set, and the
headline number made the set look complete.

**THE MEASUREMENT ALWAYS WINS.** If any planning document contradicts something
you just measured, the measurement wins and **you write the correction down.**
This has been needed four times.

**IF YOU CHANGE A RULE YOU ARE ABOUT TO BE MEASURED BY, SAY SO IN BOLD.** Not
quietly, not in passing.

**"PROBABLY", "ALMOST CERTAINLY", "THIS SHOULD BE FINE" — FILE IT.** If you catch
yourself writing one of those about something that ships, it goes in
`REVIEW_QUEUE.md` before the commit that ships it. Filing costs one paragraph.
Not filing costs whatever the mistake costs, found later by someone who trusted
you.

**DO NOT MANUFACTURE A DEFECT TO JUSTIFY A SESSION.** The pressure after a
session that found something big is to also find something. A clean review is a
legitimate outcome.

---

# HOUSEKEEPING THAT HAS ALREADY BITTEN US

- **`git pull` FIRST, every session.** A scheduled task pushes snapshots from
  elsewhere.
- **`git commit -F <file>`** for multi-line messages. PowerShell here-strings
  mangle quotes.
- **NEVER use PowerShell `Get-Content` / `Add-Content` / `Set-Content` on this
  repo's UTF-8 files.** PowerShell 5.1 reads BOM-less UTF-8 as ANSI and
  **silently eats every em-dash, mid-dot, arrow and tick mark.** It corrupted
  four commits on 2026-07-26 before anyone noticed. Use Python
  (`open(p, encoding='utf-8')`) or the editor tools.
- **SCAN THE DOCUMENTS BEFORE YOUR FINAL COMMIT.** Search the five updated files
  for `â€`, `Â·`, `â†`, `Ã`, `âœ` — the fingerprints of the bug above. Ignore
  hits inside backticks; those are deliberate quotations of the damage.
  **Six corrupted arrows were still sitting in `PROGRESS_LOG.md` on 2026-07-27,
  in entries a note the day before had declared clean.** Both times it was found
  by a person looking, never by a check. **The scan costs one command.**
- **"SUCCESS" FROM A TOOL IS NOT EVIDENCE THAT SOMETHING WORKS.** `schtasks`
  reported a scheduled task created successfully and created a broken one that
  could never run. **Run the thing and read its output.**
- **Run env:** `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with `PYTHONUTF8=1`.
- **The Commander is a non-programmer.** Plain words, gray-box commands, explain
  before changing, commit after.

---

# WHAT THIS PATTERN CANNOT DO

**It cannot replace Fable at Phase 6.** Information instruments — the Brief, the
Context Deck — can carry this lighter guard. **The gauntlet cannot.** THE PROMISE
allows exactly three sealed slots and then the signals chapter closes; there is
no second attempt to catch a mistake with, and Law 7 proved the Lab's own numbers
can never detect a leak.

**At Phase 6 a second, genuinely independent AI reviews the test setup before it
runs and its verdict after. That is locked in `EXECUTION_PLAN.md` and is NOT
waived by Fable's absence.** It is R-006 in the queue and **no in-house session
may ever clear it.** If no independent AI is available when Phase 6 arrives,
**Phase 6 waits.**
