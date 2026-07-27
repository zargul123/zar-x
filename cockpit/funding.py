"""
Zar X cockpit — the funding-rate instrument (Context Deck, Phase 3, Step 3.2).

Perpetual futures have no expiry, so an exchange keeps their price tethered to
spot by making one side pay the other every 8 hours. That payment is the
funding rate, and its SIGN says which way the crowd is leaning: when it is
positive, traders holding longs pay traders holding shorts; when it is
negative, shorts pay longs. Binance settles at 00:00, 08:00 and 16:00 UTC.

**These are the USDT PERPETUAL CONTRACTS (BTCUSDT / ETHUSDT / SOLUSDT), not
the spot pairs the rest of the Brief prices.** They are different instruments
that happen to track each other, and saying so plainly is the whole reason
this note exists.

The number printed is Binance's running ESTIMATE for the NEXT settlement, not
a payment that has already happened — `lastFundingRate` moves until it
settles, and Binance's own documentation calls it an estimation. The last
SETTLED rate is read too, but only by the smoke test below, where it serves as
the exact-identity check on this file's parsing: settled rates are fixed
historical facts, so they must match the raw response digit for digit. Both
values pass through the SAME parse and format helpers, so that exact check
guards the printed path as well.

INFORMATION, NEVER A SIGNAL. This part reports crowd positioning; it never
says what to do about it. Stating that longs pay shorts is a fact about the
mechanism, exactly like saying RSI is 46 — it is not a suggestion to trade.
No delta-neutral carry number is computed here: that is Phase 4's job and it
ships with mandatory risk caveats a bare percentage would leave out.

Fail-safe (Law 3): every failure becomes an honest line and the Brief carries
on. If SOME assets answer and others do not, the ones that answered are
printed and the ones that did not are NAMED — partial truth labelled as
partial is honest; silently dropping an asset is not.

Standalone smoke test:
    python cockpit/funding.py       (live block, exact-identity check, drill)
"""
import re
import sys
from datetime import datetime, timezone

import requests

FAPI_BASE = 'https://fapi.binance.com'
TIMEOUT = 10           # seconds; one attempt per asset, never a retry storm
OFFLINE_WORDS = "Funding instrument offline"

# Our assets are spot pairs; funding exists only on the perpetual contracts.
# The mapping lives here because the compartment owns its own source mapping
# (Law 2) — no other part needs to know Binance's naming.
CONTRACTS = {
    'BTC-USD': 'BTCUSDT',
    'ETH-USD': 'ETHUSDT',
    'SOL-USD': 'SOLUSDT',
}

# Sanity bound. Binance caps funding well below this; a value outside it means
# we are reading something that is not a funding rate, and refusing a number we
# do not understand is honest where printing it is not.
MAX_PLAUSIBLE_RATE = 0.05      # 5% per 8h

# Used only by the offline drill: the .invalid top-level domain is reserved by
# the RFCs and can never resolve, so the drill proves the fail-safe without
# unplugging the Commander's internet.
OFFLINE_DRILL_URL = 'https://zar-x-offline-drill.invalid'


def _get(base_url, path, params, timeout):
    """The only network call in this part. One request, no retries."""
    r = requests.get(f"{base_url}{path}", params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _parse_rate(raw) -> float:
    """Binance sends rates as STRINGS. Shared by the estimate and the settled
    reader so the smoke test's exact check covers the printed path too."""
    rate = float(str(raw).strip())
    if abs(rate) > MAX_PLAUSIBLE_RATE:
        raise ValueError(f"rate {rate} is outside +/-{MAX_PLAUSIBLE_RATE}")
    return rate


def _fmt_pct(rate: float) -> str:
    """Shared formatter. The sign is the whole instrument, so it is always
    shown explicitly — never left implied by its absence."""
    return f"{rate * 100:+.4f}%"


def _utc_hhmm(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime('%H:%M')


def read_estimate(base_url, contract, timeout=TIMEOUT):
    """The running estimate for the NEXT settlement, for one contract.

    Raises on anything unexpected; the doorway below turns a raise into an
    honest line.
    """
    payload = _get(base_url, '/fapi/v1/premiumIndex', {'symbol': contract},
                   timeout)
    if not isinstance(payload, dict):
        raise ValueError("premiumIndex response is not a JSON object")
    for field in ('lastFundingRate', 'nextFundingTime'):
        if field not in payload:
            raise ValueError(f"premiumIndex response has no {field!r}")
    return _parse_rate(payload['lastFundingRate']), int(payload['nextFundingTime'])


def read_settled(base_url, contract, timeout=TIMEOUT):
    """The most recent SETTLED rate — a payment that actually happened.

    Not printed on the Brief (the orders cap this instrument at one request per
    asset). It exists for the exact-identity check in the smoke test.
    """
    payload = _get(base_url, '/fapi/v1/fundingRate',
                   {'symbol': contract, 'limit': 1}, timeout)
    if not isinstance(payload, list) or not payload:
        raise ValueError("fundingRate response carries no rows")
    row = payload[0]
    return _parse_rate(row['fundingRate']), int(row['fundingTime'])


def section_text(base_url=FAPI_BASE, contracts=None, timeout=TIMEOUT):
    """The funding block the Brief prints — this part's single doorway.

    Never raises. Joins the EXISTING Context Deck, so it prints no header of
    its own: one deck, two instruments. base_url and contracts are injectable
    so the drills can point this at an unreachable address, or at a bogus
    symbol, without disconnecting anything.
    """
    contracts = CONTRACTS if contracts is None else contracts
    answered, missing, settlements = [], [], []
    try:
        for asset, contract in contracts.items():
            short = asset.split('-')[0]
            try:
                rate, next_ms = read_estimate(base_url, contract, timeout)
                answered.append(f"{short} {_fmt_pct(rate)}")
                settlements.append(next_ms)
            except Exception:
                missing.append(short)

        if not answered:
            raise ConnectionError("no asset answered")

        line = f"  Funding (8h) : {'  ·  '.join(answered)}"
        if missing:
            line += f"   [no data: {', '.join(missing)}]"
        return "\n".join([
            line,
            f"  (USDT perpetuals · positive = longs pay shorts · next "
            f"settlement {_utc_hhmm(min(settlements))} UTC",
            "   — crowd positioning, information, not a signal)",
        ])
    except Exception as e:
        return f"  🔌 {OFFLINE_WORDS} ({type(e).__name__})"


if __name__ == '__main__':
    # =====================================================================
    # GATE 3.2-R — rebuilt 2026-07-26, the day its predecessor was audited.
    #
    # The old gate reported 48/48 while FOUR of six deliberate sabotages
    # walked through it. It checked the parse and never the printed sentence:
    # a sign-flipped `_fmt_pct` printed the exact opposite of the truth and
    # collected a tick mark. Two rules came out of that audit and both live
    # below.
    #
    #   1. VERIFY WHAT THE PILOT READS, not what the parser returned. The
    #      checks re-derive the expected string from Binance raw using THIS
    #      BLOCK'S OWN arithmetic — never by calling the helper under test,
    #      because a check that reuses the code it is checking proves nothing.
    #
    #   2. A CHECK NOBODY HAS TRIED TO BREAK IS A CHECK NOBODY HAS TESTED.
    #      So this test breaks itself, all six ways, on EVERY run, and fails
    #      if any breakage goes uncaught. Exhibit A is no longer an auditor's
    #      one-off; it is part of the gate.
    #
    # Everything here lives inside `__main__` on purpose: the production path
    # above is untouched, so what the Brief prints cannot have changed.
    # =====================================================================

    # The test holds its OWN copy of the ground truth. If it read CONTRACTS
    # it would follow the module into a miswiring and cheerfully confirm it
    # (that is sabotage S6). An independent check needs an independent map.
    GATE_CONTRACTS = {
        'BTC-USD': 'BTCUSDT',
        'ETH-USD': 'ETHUSDT',
        'SOL-USD': 'SOLUSDT',
    }

    # Imported here rather than at the top so every diff hunk stays inside
    # `__main__` and the production path is provably untouched.
    from itertools import zip_longest

    def _raw_snapshot():
        """Raw values fetched by the TEST, straight from Binance, passing
        through none of this file's helpers."""
        snap = {}
        for asset, contract in GATE_CONTRACTS.items():
            p = requests.get(f"{FAPI_BASE}/fapi/v1/premiumIndex",
                             params={'symbol': contract}, timeout=TIMEOUT).json()
            snap[asset] = (str(p['lastFundingRate']), int(p['nextFundingTime']))
        return snap

    def _expected_pct(raw_str):
        """The percentage the Brief OUGHT to show. `_fmt_pct` is deliberately
        not called — it is the thing on trial."""
        return "%+.4f%%" % (float(raw_str) * 100)

    def _expected_hhmm(ms):
        """Likewise: `_utc_hhmm` is deliberately not called."""
        return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime('%H:%M')

    # =====================================================================
    # GATE 3.2-R2, added 2026-07-27 after an independent session threw five
    # NEW sabotages at Gate 3.2-R and FOUR walked through.
    #
    # The gate checked the DIGITS and never the WORDS. S7 flipped
    # "positive = longs pay shorts" to its opposite — the reverse of how the
    # market actually works — beside three perfectly correct numbers, and the
    # gate printed PASSED. S8 appended a fabricated fourth asset that was
    # never fetched from anywhere, and the gate printed PASSED.
    #
    # THE CAUSE: every check asked "is this expected string PRESENT?" None
    # asked "is anything ELSE present?", and none checked the fixed words at
    # all. So the gate now holds its OWN VERBATIM COPY of every fixed word and
    # rebuilds the WHOLE printed block for an EXACT-EQUALITY comparison.
    # Nothing can be appended to a string that must match exactly.
    # =====================================================================

    # The test's own copy of the wording. If it read these from the module it
    # would follow the instrument into a corrupted sentence and confirm it —
    # the same mistake `GATE_CONTRACTS` exists to prevent for the tickers.
    GATE_LINE1_PREFIX = "  Funding (8h) : "
    GATE_SEP = "  ·  "
    GATE_WORDS_MECHANISM = "positive = longs pay shorts"
    GATE_LINE2_HEAD = ("  (USDT perpetuals · positive = longs pay shorts · "
                       "next settlement ")
    GATE_LINE2_TAIL = " UTC"
    GATE_LINE3_DISCLAIMER = "   — crowd positioning, information, not a signal)"

    def _expected_block(snap):
        """The ENTIRE block the Brief ought to print, assembled from raw by
        this test's own arithmetic and its own wording. Compared for exact
        equality, so an extra asset, a reversed sentence or a deleted
        disclaimer all fail — none of which the old gate could see."""
        parts = [f"{a.split('-')[0]} {_expected_pct(snap[a][0])}"
                 for a in GATE_CONTRACTS]
        stamp = _expected_hhmm(min(v[1] for v in snap.values()))
        return "\n".join([
            GATE_LINE1_PREFIX + GATE_SEP.join(parts),
            GATE_LINE2_HEAD + stamp + GATE_LINE2_TAIL,
            GATE_LINE3_DISCLAIMER,
        ])

    def _core_checks(verbose=True):
        """The checks that guard the printed sentence — and, because they run
        against whatever the module's helpers CURRENTLY are, the detector the
        sabotage drill below uses on itself.

        THE DRIFT RULE, fixed before this was written: funding is quoted
        continuously, so a raw snapshot is taken before the line is built and
        another after, and the printed string must match one or the other.
        A moving rate lands on one of the two. A sign flip, a lost x100 or a
        miswired ticker lands on NEITHER. The tolerance is for time passing,
        never for being wrong.
        """
        say = print if verbose else (lambda *a, **k: None)
        ok = True
        before = _raw_snapshot()
        live = section_text()
        if OFFLINE_WORDS in live:
            say("   ✗ live block came back offline — the sentence cannot be verified")
            return False
        after = None

        for asset in GATE_CONTRACTS:
            short = asset.split('-')[0]
            want = _expected_pct(before[asset][0])
            hit = f"{short} {want}" in live
            shown = want
            if not hit:
                if after is None:
                    after = _raw_snapshot()
                want2 = _expected_pct(after[asset][0])
                hit = f"{short} {want2}" in live
                shown = f"{want} (before) or {want2} (after)"
            say(f"   {'✓' if hit else '✗'} {short}: Binance raw "
                f"{before[asset][0]!r} → expected {shown} → the printed line "
                f"{'carries it' if hit else 'DOES NOT CARRY IT'}")
            ok = ok and hit

        want_t = _expected_hhmm(min(v[1] for v in before.values()))
        hit_t = f"next settlement {want_t} UTC" in live
        shown_t = want_t
        if not hit_t:
            if after is None:
                after = _raw_snapshot()
            want_t2 = _expected_hhmm(min(v[1] for v in after.values()))
            hit_t = f"next settlement {want_t2} UTC" in live
            shown_t = f"{want_t} or {want_t2}"
        say(f"   {'✓' if hit_t else '✗'} settlement time: expected "
            f"{shown_t} UTC → the printed line "
            f"{'carries it' if hit_t else 'DOES NOT CARRY IT'}")
        ok = ok and hit_t

        # --- GATE 3.2-R2 (c): THE FIXED WORDS, GUARDED BY NAME ------------
        # Named separately from the block check below so a failure says WHICH
        # sentence changed. These are the sentences that tell the pilot what
        # the digits MEAN; a reversed meaning with correct numbers is the
        # defect S7 exposed.
        for words in (GATE_WORDS_MECHANISM,
                      GATE_LINE3_DISCLAIMER.strip()):
            hit_w = words in live
            say(f"   {'✓' if hit_w else '✗'} fixed wording present verbatim: "
                f"{words!r}")
            ok = ok and hit_w

        # --- GATE 3.2-R2 (b): THE WHOLE BLOCK, EXACT EQUALITY -------------
        # The check that kills S8. "Contains" can never notice an ADDITION;
        # equality can never miss one.
        want_block = _expected_block(before)
        block_ok = (live == want_block)
        if not block_ok:
            if after is None:
                after = _raw_snapshot()
            want_block = _expected_block(after)
            block_ok = (live == want_block)
        say(f"   {'✓' if block_ok else '✗'} the WHOLE printed block equals the "
            f"block rebuilt from Binance raw — nothing added, nothing removed")
        if not block_ok:
            for i, (got, want) in enumerate(
                    zip_longest(live.splitlines(), want_block.splitlines(),
                                fillvalue=''), start=1):
                if got != want:
                    say(f"      line {i} printed : {got!r}")
                    say(f"      line {i} expected: {want!r}")
        return ok and block_ok

    def _partial_checks(verbose=True):
        """GATE 3.2-R2 (d): THE ROTATING PARTIAL-FAILURE DRILL.

        The old drill always broke SOL, so it could only ever prove SOL. A
        module that named the missing asset 'SOL' no matter which one failed
        (sabotage S11) agreed with the drill and walked through. Each asset
        now takes a turn as the bogus symbol and must be named BY ITS OWN
        NAME, with the other two still printed."""
        say = print if verbose else (lambda *a, **k: None)
        ok = True
        for broken in GATE_CONTRACTS:
            short = broken.split('-')[0]
            contracts = {a: ('NOTAREALSYMBOL' if a == broken else c)
                         for a, c in GATE_CONTRACTS.items()}
            out = section_text(contracts=contracts)
            others = [x.split('-')[0] for x in GATE_CONTRACTS if x != broken]
            hit = (f"[no data: {short}]" in out
                   and all(f"{o} +" in out or f"{o} -" in out for o in others)
                   and OFFLINE_WORDS not in out)
            say(f"   {'✓' if hit else '✗'} {short} broken → named as "
                f"'[no data: {short}]' and {' and '.join(others)} still "
                f"printed")
            ok = ok and hit
        return ok

    # S7-S11 corrupt the OUTPUT rather than editing the file, because that is
    # what a drill running inside the file can do. The real proof that the
    # repair works is the scratch rig, which edits the file for real — see the
    # 2026-07-27 PROGRESS_LOG entry, Gate 3.2-R2 check (i).
    _SECTION_TEXT_ORIGINAL = section_text

    def _sab_reversed_meaning(*a, **k):
        return _SECTION_TEXT_ORIGINAL(*a, **k).replace(
            'positive = longs pay shorts', 'positive = shorts pay longs')

    def _sab_phantom_asset(*a, **k):
        lines = _SECTION_TEXT_ORIGINAL(*a, **k).splitlines()
        lines[0] += "  ·  XRP +0.0100%"
        return "\n".join(lines)

    def _sab_disclaimer_deleted(*a, **k):
        return _SECTION_TEXT_ORIGINAL(*a, **k).replace(
            '   — crowd positioning, information, not a signal)',
            '   — crowd positioning)')

    def _sab_silent_drop(*a, **k):
        return re.sub(r'\s*\[no data: [^\]]*\]', '',
                      _SECTION_TEXT_ORIGINAL(*a, **k))

    def _sab_always_sol(*a, **k):
        return re.sub(r'\[no data: [^\]]*\]', '[no data: SOL]',
                      _SECTION_TEXT_ORIGINAL(*a, **k))

    # The six from the audit of 2026-07-26 and the five from the independent
    # review of 2026-07-27, kept by name so the fix stays legible. S5 shifts by
    # a fixed hour rather than dropping the timezone: dropping it is a no-op on
    # a machine already set to UTC, and a drill that only works on some
    # machines is not a drill.
    #
    # The last column is WHICH JUDGE decides. S10 and S11 corrupt only the
    # partial-failure path, which the all-green core checks cannot see; judging
    # them by the core checks would record two guaranteed escapes as if the
    # gate were blind, and judging them by nothing at all is how S11 survived
    # in the first place.
    _SABOTAGES = [
        ('S1', '_fmt_pct — sign flipped', 'ESCAPED', '_fmt_pct',
         lambda rate: f"{-rate * 100:+.4f}%", 'core'),
        ('S2', '_fmt_pct — x100 dropped', 'ESCAPED', '_fmt_pct',
         lambda rate: f"{rate:+.4f}%", 'core'),
        ('S3', '_parse_rate — sign flipped', 'caught', '_parse_rate',
         lambda raw: -float(str(raw).strip()), 'core'),
        ('S4', '_parse_rate — scaled x10', 'caught', '_parse_rate',
         lambda raw: float(str(raw).strip()) * 10, 'core'),
        ('S5', '_utc_hhmm — shifted one hour', 'ESCAPED', '_utc_hhmm',
         lambda ms: datetime.fromtimestamp(ms / 1000 + 3600,
                                           timezone.utc).strftime('%H:%M'),
         'core'),
        ('S6', 'CONTRACTS — tickers miswired', 'ESCAPED', 'CONTRACTS',
         {'BTC-USD': 'SOLUSDT', 'ETH-USD': 'BTCUSDT', 'SOL-USD': 'ETHUSDT'},
         'core'),
        ('S7', 'the meaning REVERSED, digits intact', 'ESCAPED',
         'section_text', _sab_reversed_meaning, 'core'),
        ('S8', 'a phantom fourth asset appended', 'ESCAPED',
         'section_text', _sab_phantom_asset, 'core'),
        ('S9', 'the "not a signal" disclaimer deleted', 'ESCAPED',
         'section_text', _sab_disclaimer_deleted, 'core'),
        ('S10', 'a failed asset vanishes unnamed', 'caught',
         'section_text', _sab_silent_drop, 'partial'),
        ('S11', 'the missing asset always named SOL', 'ESCAPED',
         'section_text', _sab_always_sol, 'partial'),
    ]

    def _sabotage_drill():
        """EXHIBIT A, MADE PERMANENT. Break this file on purpose, one way at a
        time, and require the checks above to FAIL each time. Any sabotage
        that survives means the gate is decorative and the run must fail."""
        ok = True
        for tag, words, old, attr, repl, judge in _SABOTAGES:
            original = globals()[attr]
            globals()[attr] = repl
            try:
                survived = (_partial_checks(verbose=False) if judge == 'partial'
                            else _core_checks(verbose=False))
            except Exception:
                survived = False        # a crash is a catch: it did not pass
            finally:
                globals()[attr] = original
            caught = not survived
            print(f"   {'✓' if caught else '✗'} {tag:<4} {words:<38} "
                  f"[old gate: {old:<7}] → "
                  f"{'CAUGHT' if caught else 'ESCAPED AGAIN — GATE IS DECORATIVE'}")
            ok = ok and caught
        restored = _core_checks(verbose=False) and _partial_checks(verbose=False)
        print(f"   {'✓' if restored else '✗'} every original restored — the "
              f"clean checks pass again afterwards")
        return ok and restored

    ok = True
    print("GATE 3.2-R2 — the funding instrument's self-test, hardened 2026-07-27.")
    print("Its first version reported 48/48 while four deliberate lies walked")
    print("through it. Its second checked the digits and missed the WORDS: it")
    print("printed 'positive = shorts pay longs' — the opposite of the truth —")
    print("and passed. This one rebuilds the WHOLE block and compares it exactly.")

    print("\n1) LIVE BLOCK — what the Brief will print")
    live = section_text()
    print()
    print(live)
    print()
    if OFFLINE_WORDS in live:
        print("   ✗ the live block came back offline")
        ok = False
    for short in ('BTC', 'ETH', 'SOL'):
        # _fmt_pct always emits an explicit + or -, so requiring the sign is
        # what separates a printed rate from a name in the "no data" list.
        # NOTE: this check is WEAK on its own — a sign-flipped formatter still
        # prints a sign. Section 2 is what actually guards the sentence.
        signed = f"{short} +" in live or f"{short} -" in live
        print(f"   {'✓' if signed else '✗'} {short} rate printed with a sign")
        ok = ok and signed
    stamped = bool(re.search(r"next settlement \d{2}:\d{2} UTC", live))
    print(f"   {'✓' if stamped else '✗'} next settlement time printed as HH:MM UTC")
    ok = ok and stamped

    print("\n2) THE PRINTED SENTENCE vs BINANCE RAW (Gate 3.2-R b, c, d) — the"
          "\n   check whose absence voided the 48/48. Every expected string is"
          "\n   derived by this block's own arithmetic from a raw fetch; no"
          "\n   helper of the instrument is used to judge the instrument.")
    ok = _core_checks(verbose=True) and ok

    print("\n3) EXHIBIT A, MADE PERMANENT (Gate 3.2-R e, f · 3.2-R2 f) — the"
          "\n   file is broken on purpose ELEVEN ways and each break MUST be"
          "\n   caught. Four of the first six escaped the gate of 2026-07-26;"
          "\n   four of the last five escaped the gate of the day after.")
    ok = _sabotage_drill() and ok

    print("\n4) EXACT IDENTITY CHECK — the settled rate this file parses must"
          "\n   match the raw response digit for digit, sign included. Settled"
          "\n   rates are fixed historical facts, so 'close' is not a pass."
          "\n   Kept from the old gate: it is sound, it was never the problem.")
    for asset, contract in CONTRACTS.items():
        try:
            parsed, when = read_settled(FAPI_BASE, contract)
            raw = requests.get(f"{FAPI_BASE}/fapi/v1/fundingRate",
                               params={'symbol': contract, 'limit': 1},
                               timeout=TIMEOUT).json()[0]['fundingRate']
            exact = parsed == float(raw)
            stamp = datetime.fromtimestamp(when / 1000, timezone.utc)
            print(f"   {'✓' if exact else '✗'} {contract}: parsed {parsed} "
                  f"== raw {raw!r} → {_fmt_pct(parsed)} "
                  f"(settled {stamp:%Y-%m-%d %H:%M} UTC)")
            ok = ok and exact
        except Exception as e:
            print(f"   ✗ {contract}: settled read failed: {type(e).__name__}: {e}")
            ok = False

    print("\n5) ROTATING PARTIAL-FAILURE DRILL (Gate 3.2 f · 3.2-R2 d) — EACH"
          "\n   asset takes a turn as the bogus symbol. The old drill always"
          "\n   broke SOL, so it could only ever prove SOL: a module naming"
          "\n   every missing asset 'SOL' agreed with the drill and passed.")
    print()
    print(section_text(contracts={'BTC-USD': 'BTCUSDT',
                                  'ETH-USD': 'ETHUSDT',
                                  'SOL-USD': 'NOTAREALSYMBOL'}))
    print()
    partial_ok = _partial_checks(verbose=True)
    ok = ok and partial_ok

    print("\n6) OFFLINE DRILL — injected unreachable URL, internet untouched")
    print(f"   pointing the instrument at {OFFLINE_DRILL_URL}")
    drill = section_text(base_url=OFFLINE_DRILL_URL)
    print()
    print(drill)
    lines = drill.splitlines()
    drill_ok = OFFLINE_WORDS in drill and len(lines) == 1
    print(f"   {'✓' if drill_ok else '✗'} degraded to one offline line, "
          f"no traceback, nothing else printed")
    ok = ok and drill_ok

    if ok:
        print("\nGATE 3.2-R2 PASSED — the WHOLE printed block was rebuilt from "
              "Binance\nraw and matched exactly, the fixed wording was checked "
              "verbatim, every\nasset took a turn at failing, and all ELEVEN "
              "deliberate sabotages were\ncaught. This test has demonstrated, "
              "this run, that it is able to say no.")
    else:
        print("\nGATE 3.2-R2 FAILED — see the ✗ lines above.")
    sys.exit(0 if ok else 1)
