# ZAR X — SESSION ORDERS: PHASE 3, STEP 3.2 — FUNDING RATES

*Written 2026-07-26 — **by Opus wearing Fable's hat.** Fable was unavailable,
so the planning chair was filled by the same model that built Step 3.1. That
is recorded here because it matters: the builder and the planner were the same
mind, which is exactly the independence this ship normally relies on. The
protection that survives is the one that always did the real work — **the gate
below is declared BEFORE the build, and a FRESH session builds to it.** See
"WHO CHECKS THE CHECKER" at the bottom; it is part of these orders, not a
footnote.*

## READ FIRST, IN THIS ORDER, BEFORE TOUCHING ANYTHING

1. `EXECUTION_PLAN.md` — the PHASE 3 block, the CURRENT POSITION MARKER, and
   **the CORRECTION NOTE on Phase 3 #2** (the funding-recording premise was
   measured and found false — read it before you believe anything about
   funding history).
2. The last two entries of `PROGRESS_LOG.md` — Step 3.1's gate, and the
   planning entry that corrected the funding premise and measured the real
   depth of every free source.
3. `SHIP_LAWS.md` — all seven laws.
4. `cockpit/fear_greed.py` — 156 lines, read all of them. **Step 3.2 is its
   twin.** Copy its shape: injectable base URL, one doorway, never raises,
   its own smoke test with a live half and an offline drill. Do not invent a
   new pattern when a proven one is sitting next door.
5. `cockpit/brief.py` — read the Context Deck wiring you are extending.
6. `data/market_data.py` — the plain-`requests` house style for HTTP.
7. `ROADMAP.md` — the MEASURED data-source facts table.

## SESSION RULES (the standing ones, restated so they cannot be missed)

1. `git pull` FIRST. The cloud watchman commits every 4 hours.
2. Run environment: `C:\Users\hp\miniconda3\envs\tfdml\python.exe` with
   `PYTHONUTF8=1`. The Commander is a non-programmer: plain words, gray-box
   commands, explain then commit (Law 5).
3. Build ONLY Step 3.2. Do NOT start Step 3.3 (news headlines) and do NOT
   build the open-interest recorder, however tempting — it has its own step
   and its own gate. One part, one gate, one commit.
4. INFORMATION for the Brief, never a signal (the tool-doorway law). Law 7
   does not bite — nothing enters the Lab — but the signals doorway stands.
5. Do NOT compute the delta-neutral carry. That is Phase 4's whole job and it
   ships with mandatory risk caveats. A bare annualised percentage on the
   Brief without those caveats is the kind of number that gets a pilot hurt.

## WHAT TO BUILD

**One new file: `cockpit/funding.py`. One minimal wiring change:
`cockpit/brief.py`.** Those are the ONLY two code files this session may
touch. All of `lab/` stays byte-for-byte untouched, vault read-only, and
`data/ indicators/ regime/ risk/ signals/ journal/ config.py` untouched —
including the symbol mapping, which lives inside `funding.py` (the compartment
owns its own source mapping, Law 2).

### The instrument — `cockpit/funding.py`

- **SOURCE: Binance USDⓈ-M futures public API. Free, NO key, no .env change,
  no new dependency.** Verified reachable from the Commander's connection on
  2026-07-26 (HTTP 200, both endpoints below).
  - Current/predicted rate:
    `GET https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT`
    → returns `lastFundingRate`, `nextFundingTime` (ms), `markPrice`.
  - Last settled rates for context (optional, one call per asset):
    `GET https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=3`
    → the actually-settled 8-hourly rates.
  - **VERIFY the live schema at build time and record the REAL shape in the
    log**, exactly as Step 3.1 did. Values arrive as STRINGS.
- **SYMBOLS:** our assets are `BTC-USD / ETH-USD / SOL-USD`; the perpetual
  contracts are `BTCUSDT / ETHUSDT / SOLUSDT`. The mapping is a dict inside
  this file. **Say plainly in the output or the docstring that these are the
  USDT perpetual contracts** — they are not the same instrument as the spot
  pair the rest of the Brief prices, and pretending otherwise is a small lie
  that becomes a big one in Phase 6.
- **RATE COUNT:** three assets = three requests minimum. Binance's public
  weight limits are generous, but keep it to one request per asset per call
  and no retry storms.
- **OUTPUT:** one added block under the existing CONTEXT DECK, roughly:

      Funding (8h) : BTC +0.0069%  ·  ETH +0.0041%  ·  SOL -0.0032%
      (positive = longs pay shorts · next settlement 16:00 UTC — crowd
       positioning, information, not a signal)

  Numbers and honest mechanics only.
- **THE SIGN IS THE WHOLE INSTRUMENT — GET IT RIGHT.** A positive funding rate
  means holders of long positions pay holders of short positions; negative
  means the reverse. **Getting this backwards would print the exact opposite
  of the truth on the Brief every morning**, and no gate that only checks "a
  number appeared" would catch it. Check (b) below exists for this reason
  alone.
- **ON THE WORDS "LONGS" AND "SHORTS" — settled here so the session does not
  agonise.** Step 3.1's orders said no buy/sell words. That rule forbids
  *telling the pilot what to do*. Stating that longs pay shorts is a fact
  about how the funding mechanism works, exactly like saying RSI is 46, and
  EXECUTION_PLAN Phase 3 #2 prescribes that wording itself. **Permitted:**
  "positive = longs pay shorts", "the crowd is leaning long". **Forbidden:**
  anything that recommends, suggests, or hints at an action — "so consider
  fading it", "a good time to short", "bullish", "bearish".
- **FAIL-SAFE (Law 3):** ANY failure — timeout, HTTP error, surprise schema,
  no internet, a single asset missing — degrades honestly. A total failure
  prints one line, "Funding instrument offline". **If some assets answer and
  others do not, print the ones that answered and name the ones that did
  not** — partial truth labelled as partial is honest; silently dropping an
  asset is not. Timeout ~10s. No retry storms.
- **Injectable base URL** (parameter or argument), so the offline drill points
  at an unreachable address WITHOUT disconnecting the internet. Reuse Step
  3.1's `.invalid` trick.
- **STANDALONE SMOKE TEST (`__main__`):** (1) print the live block; (2) run
  the offline drill against the injected bad URL and print the offline line;
  exit 0 only if both behaved.

### The wiring — `cockpit/brief.py`

- The funding block joins the EXISTING CONTEXT DECK section — **one deck, two
  instruments.** Do not print a second "CONTEXT DECK" header. Keep the touch
  minimal; the Fear & Greed line must appear above it, unchanged.
- The Brief's contract must not change: the `ok` count still counts ASSETS
  only; a dead funding instrument must not change the count, the exit code, or
  any existing line of output — including the Fear & Greed line, which must
  still print normally when funding is dead, and vice versa. **The two
  instruments must be independently killable.**

### Deliberately NOT built (write this into the log)

- **NO CSV recording of funding rates — and the reason is the opposite of what
  the plan used to say.** Measured 2026-07-26: Binance serves settled funding
  history back to contract inception (BTC 2019-09-10, ETH 2019-11-27, SOL
  2020-09-13), paginated `startTime` + `limit=1000`. Nothing is lost by not
  collecting it, so a recorder would be a second copy of a public archive.
  **Phase 6 Slot 2 (funding-rate extreme fade) can be tested whenever we
  choose.** The old "recording must start the day 3.2 ships" instruction was
  written from assumption, was never true, and is corrected in
  EXECUTION_PLAN.md and ROADMAP.md.
- **NO open-interest recorder in this step**, even though OI is the one thing
  that genuinely expires (30-day window, `code -1130` for anything older). It
  gets its own step, its own gate, and a backfill at birth. Because every read
  reaches back 30 days, a recorder that runs monthly loses nothing — there is
  a deadline, not an emergency. Do not smuggle it in here.
- **NO carry calculation.** Phase 4.

## GATE 3.2 — DECLARED HERE, BEFORE THE BUILD (Law 4)

(a) Standalone run prints a current funding rate for all THREE assets, each
    with its sign, plus the next settlement time; exit 0.
(b) ~~**THE SIGN AND MAGNITUDE CHECK — the one that actually matters.** Each
    printed rate is cross-checked against Binance's own published figure for
    that contract, from a surface independent of the one the instrument used
    (the exchange's funding-rate page, or the `fundingRate` history endpoint
    if the instrument used `premiumIndex`). Same number within rounding, and
    **the same sign**. A session that cannot demonstrate the sign is correct
    has not passed this gate.~~

**(b) AMENDED 2026-07-26 BY MEASUREMENT, BEFORE ANY CODE EXISTED. The struck
text above rests on a fact that is false, and is left legible because a plan
that quietly edits its own errors teaches the next session nothing.**

*What was measured, on all three assets, before the amendment was written:*

| | BTC | ETH | SOL |
|---|---|---|---|
| `premiumIndex.lastFundingRate` | 0.00006211 | 0.00001104 | 0.00001776 |
| newest settled `fundingRate` | 0.00005884 | 0.00002358 | 0.00006371 |
| identical? | **no** | **no** | **no** |

*The struck check assumes `lastFundingRate` IS the last settled rate. It is
not. It is the running **estimate** for the NEXT settlement (16:00 UTC, while
the newest settled payment was 08:00 UTC) — Binance's own documentation says
the pre-settlement figure "represents an estimation." The two endpoints report
**different quantities**, so "same number within rounding" cannot pass, and no
correct implementation could ever make it pass.*

*Worse, the weaker fallback of "at least the same sign" is ALSO invalid: the
last three settled rates ran `+ − +` for ETH and `− + +` for SOL. The sign
genuinely flips between 8-hour periods, so a sign-agreement check between the
two surfaces would fail at random and invite a session to shrug off a real
failure.*

**The amended check — three parts, ALL required, and stricter than the struck
one. It is written and committed BEFORE the instrument exists:**

  **b1 — EXACT IDENTITY (catches a sign flip in our code).** The instrument
       also reads the last SETTLED rate for each asset. A settled rate is a
       fixed historical fact, so the instrument's parsed value must match a
       freshly-fetched raw value **exactly — digit for digit, sign included**,
       not merely "within rounding". The settled and printed-estimate values
       MUST pass through the SAME parsing and formatting helpers, so this
       exact check guards the printed path too. If they do not share that
       code, this check proves nothing and the gate FAILS.
  **b2 — THE PRINTED NUMBER (catches a formatting or unit error).** Every
       rate printed on the Brief is re-derived BY HAND from a fresh raw
       `premiumIndex` response — same sign, same magnitude, allowing only for
       the drift of the minutes between calls. The re-derivation is recorded
       in the log with both numbers visible.
  **b3 — THE MEANING (the risk this whole check exists for).** "Positive =
       longs pay shorts" is a fact about the WORLD, not about our code, and
       **no endpoint can prove a naming convention**. It is verified against
       Binance's own published documentation — a surface independent of the
       API entirely — and the supporting sentence is QUOTED in the log.

*A session that cannot demonstrate all three has not passed this gate.*
(c) THE OFFLINE DRILL: with the injected unreachable URL, the instrument
    prints its one offline line — no traceback, no crash — AND the Fear &
    Greed line still prints normally in the same run, AND a full Brief still
    completes with 3/3 assets reporting.
(d) A full live Brief shows the funding block inside the existing CONTEXT
    DECK, with the Fear & Greed line still above it, AND every section that
    existed before unchanged, 3/3 assets reporting.
(e) The Brief runs twice, back to back, completing both times. The funding
    numbers MAY differ between runs — funding is quoted continuously; that is
    live data being live, not nondeterminism. Note it, do not chase
    byte-identity.
(f) The partial-failure path is exercised, not just written: force ONE asset
    to fail (an unmapped or bogus symbol via the injectable parameter) and
    show the block prints the two that answered and NAMES the one that did
    not, with the Brief still at 3/3.

## IF / THEN

| IF | THEN |
|---|---|
| Binance answers HTTP 451 / "restricted location" | Do NOT quietly swap exchanges. STOP, write it into PROGRESS_LOG.md, tell the Commander. Bybit is verified reachable and is the standing candidate, but the plan names Binance and swapping the source is HIS call, not a session's. |
| The response schema differs from the shape above | Adapt the parser; record the REAL schema in the log. |
| The sign cannot be verified against an independent surface | The gate FAILS. Do not ship a funding line whose direction is unproven. |
| Some assets answer and some do not | That is the (f) path, not a failure — print the truth, name the gaps. |
| The wiring breaks anything on the existing Brief | Revert the wiring. A failing gate is never committed. |
| The gate fails twice | STOP. Write it up, tell the Commander. |
| Any planning document contradicts a measurement you just took | **The measurement wins, and you write the correction down.** This step exists because that rule was applied to the previous orders. |

## IF EVERYTHING PASSES

1. `PROGRESS_LOG.md` entry: what was built, the gate tally with the actual
   live numbers seen, the real API schema received, how the SIGN was proven,
   the no-recording-needed reasoning with its measured basis, and anything
   that went wrong on the way (Law 1: rights AND wrongs).
2. Marker in `EXECUTION_PLAN.md` → "Step 3.2 DONE <date>, GATE 3.2 PASSED.
   Step 3.2b (open-interest recorder, 30-day window, backfill at birth) READY."
3. `ROADMAP.md`: tick funding in the Context Deck row and the build queue.
4. Commit with full notes, push.

## WHO CHECKS THE CHECKER (read this, it is an order)

Fable normally verified this ship's work independently, and that verification
is what caught real problems — including a reviewer's own hardcoded "15/15" in
Gate 2.5. With Fable away, the substitute is **separation in time, not in
identity**:

1. These orders and this gate were written and committed **before** any Step
   3.2 code existed. Law 4 holds regardless of who holds the pen.
2. **A FRESH session builds** — one that has not read the reasoning behind
   these orders and must work from what is written down. If something here is
   unclear to a session with no memory of writing it, that is a defect in the
   orders, and the session should say so rather than guess.
3. **A THIRD fresh session reviews**, recomputing from raw evidence rather
   than trusting the build session's printed tally — the Gate 2.5 method.
4. **At Phase 6 this substitute expires.** A second, genuinely independent AI
   reviewing the test setup before and the verdict after is a locked
   requirement of EXECUTION_PLAN Phase 6 and is NOT waived by Fable's absence.
   Information instruments can carry a lighter guard; the gauntlet cannot.

## THE EXAM THE REVIEWING SESSION WILL RUN (build to this)

1. `git diff` scope: ONLY `cockpit/funding.py`, `cockpit/brief.py`,
   `PROGRESS_LOG.md`, `EXECUTION_PLAN.md`, `ROADMAP.md` (and this file if
   marked done) changed. All of `lab/` byte-identical. Vault verifies INTACT.
2. Fresh standalone run of the instrument — live block prints for all three
   assets, offline drill behaves, exit 0.
3. Fresh full Brief run — one CONTEXT DECK carrying BOTH instruments, 3/3
   assets, all pre-existing sections intact.
4. **The printed sign and magnitude independently re-verified against
   Binance**, by the reviewer, from scratch.
5. Each instrument killed separately: Fear & Greed dead → funding still
   prints; funding dead → Fear & Greed still prints; both dead → Brief still
   3/3.
6. The log entry contains the gate tally, the real schema, the sign proof, and
   the corrected recording reasoning.
7. Marker and ROADMAP correct; commit message honest about anything that
   failed en route; pushed to GitHub.
