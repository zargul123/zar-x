# ZAR X — SESSION ORDERS: PHASE 3, STEP 3.1 — FEAR & GREED
*Written 2026-07-26 by Fable, immediately after Phase 2 closed (Gate 2.5
passed 37/37, Law 7 adopted). These are the orders for the NEXT build session
(Opus or any model). Fable will verify the work afterward — the verification
exam is at the bottom of this file and it WILL be run exactly as written, so
build to it. When this step is done and verified, this file gets rewritten
with the next step's orders.*

## READ FIRST, IN THIS ORDER, BEFORE TOUCHING ANYTHING

1. `EXECUTION_PLAN.md` — the PHASE 3 block and the CURRENT POSITION MARKER
   (Phase 2 complete; Step 3.1 ready).
2. The last three entries of `PROGRESS_LOG.md` — the Gate 2.5 trilogy: the
   failure, the independent review, the decision that created Law 7.
3. `SHIP_LAWS.md` — all SEVEN laws. Law 7 is new since Phase 2.
4. `cockpit/brief.py` — 92 lines, read all of them. You will wire into this.
5. `config.py` — where settings live. `data/market_data.py` — copy its
   plain-`requests` style for HTTP, do not invent a new pattern.

## SESSION RULES (the standing ones, restated so they cannot be missed)

1. `git pull` FIRST. The cloud commits every 4 hours.
2. Run environment: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with
   `PYTHONUTF8=1`. The Commander is a non-programmer: plain words, gray-box
   commands, explain then commit (Law 5).
3. Build ONLY Step 3.1. Do NOT start Step 3.2 (funding rates), even if 3.1
   goes quickly. One part, one gate, one commit.
4. This is INFORMATION for the Brief, never a signal (the tool-doorway law).
   No buy/sell words anywhere in its output. Law 7 does not bite here —
   nothing enters the Lab — but the signals doorway stands.

## WHAT TO BUILD

**One new file: `cockpit/fear_greed.py`. One minimal wiring change:
`cockpit/brief.py`.** Those are the ONLY two code files this session may
touch. Everything in `lab/` stays byte-for-byte untouched, vault read-only,
and `data/ indicators/ regime/ risk/ signals/ journal/` untouched.

### The instrument — `cockpit/fear_greed.py`

- SOURCE: the alternative.me Crypto Fear & Greed Index. Free, NO key, no
  .env change, no new dependencies. One request:
  `GET https://api.alternative.me/fng/?limit=8`
  — one call returns today plus a week of history. Expected shape (VERIFY at
  build time and record the REAL shape in the log): a JSON object with a
  `data` list, each item carrying `value` ("0"–"100", a string),
  `value_classification` ("Extreme Fear" … "Extreme Greed"), and a unix
  `timestamp`. If the real shape differs, adapt the parser and write what
  you actually received into the log.
- OUTPUT: a `section_text()` (or similar single doorway) returning the
  plain-words block the Brief will print, roughly:

      CONTEXT DECK
      Fear & Greed : 25 — Extreme Fear   (yesterday 30 · a week ago 55)
      (crowd-mood gauge from alternative.me — information, not a signal)

  Numbers and honest context only. Never advice.
- FAIL-SAFE (Law 3): ANY failure — timeout, HTTP error, surprise schema,
  no internet — produces one line, "Fear & Greed instrument offline", and
  NOTHING else breaks. Timeout ~10s. No retry storms.
- The module must accept an injectable base URL (parameter or argument) so
  the offline drill can point it at an unreachable address WITHOUT
  disconnecting the internet.
- STANDALONE SMOKE TEST (`__main__`): (1) print the live section; (2) run
  the offline drill against the injected bad URL and print the offline line;
  exit 0 only if both behaved.

### The wiring — `cockpit/brief.py`

- One new CONTEXT DECK block printed AFTER the per-asset briefings and
  BEFORE the closing footer. Keep the touch minimal.
- The Brief's contract must not change: the `ok` count still counts ASSETS
  only; a dead Fear & Greed instrument must not change the count, the exit
  code, or any existing line of output.

### Deliberately NOT built (write this into the log)

- NO CSV recording of the index. alternative.me serves its FULL history on
  demand (`limit=0`), so there is nothing to collect that cannot be fetched
  later. This is the opposite of Step 3.2: funding history is NOT served
  deep by the free source, so funding recording MUST start the day 3.2
  ships. Do not confuse the two.

## GATE 3.1 — DECLARED HERE, BEFORE THE BUILD (Law 4)

(a) Standalone run prints a live value in 0–100 with its classification and
    the yesterday / week-ago context values.
(b) The value matches what alternative.me itself publishes that day
    (https://alternative.me/crypto/fear-and-greed-index/) — same number.
(c) THE OFFLINE DRILL: with the injected unreachable URL, the instrument
    prints its one offline line — no traceback, no crash — and a full Brief
    run still completes with 3/3 assets reporting.
(d) A full live Brief run shows the new CONTEXT DECK section AND every
    section that existed before, unchanged, 3/3 assets reporting.
(e) The Brief runs twice, back to back, completing both times. The index
    value MAY differ between runs — that is live data being live, not
    nondeterminism; note it, do not chase byte-identity here.

## IF / THEN

| IF | THEN |
|---|---|
| The API is dead, moved, or paywalled | Do NOT substitute another source. Write the blocker into PROGRESS_LOG.md, tell the Commander, stop the step (Rule 6). Never a paid API without the Commander's yes. |
| The response schema differs from the expected shape | Adapt the parser; record the REAL schema in the log. |
| The wiring breaks anything on the existing Brief | Revert the wiring. A failing gate is never committed. |
| The gate fails twice | STOP. Write it up, tell the Commander; he will ask Fable. |

## IF EVERYTHING PASSES

1. PROGRESS_LOG.md entry: what was built, the gate tally with the actual
   live numbers seen, the real API schema received, the no-recording-needed
   fact and the 3.2 recording reminder, and anything that went wrong on the
   way (Law 1: rights AND wrongs).
2. Marker in EXECUTION_PLAN.md → "Step 3.1 DONE <date>, GATE 3.1 PASSED.
   Step 3.2 (Funding rates display, Binance public API) READY — funding
   recording to CSV starts the day 3.2 ships."
3. Commit with full notes, push.

## THE EXAM FABLE WILL RUN AFTERWARD (build to this)

1. `git diff` scope: ONLY `cockpit/fear_greed.py`, `cockpit/brief.py`,
   `PROGRESS_LOG.md`, `EXECUTION_PLAN.md` (and this file if marked done)
   changed. All of `lab/` byte-identical. Vault verifies INTACT.
2. Fresh standalone run of the instrument — live section prints, offline
   drill behaves, exit 0.
3. Fresh full Brief run — CONTEXT DECK present, 3/3 assets, all pre-existing
   sections intact.
4. The printed value independently cross-checked against alternative.me.
5. The log entry contains the gate tally, the real schema, and the 3.2
   recording reminder.
6. Marker correct; commit message honest about anything that failed en route;
   pushed to GitHub.
