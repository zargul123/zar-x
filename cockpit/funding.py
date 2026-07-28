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

    # =====================================================================
    # GATE 3.2-R3, added 2026-07-28 after an independent session threw two
    # NEW sabotages at Gate 3.2-R2 and BOTH walked through.
    #
    # R2 rebuilt the WHOLE block and demanded exact equality — ON THE HEALTHY
    # PATH ONLY. Every DEGRADED path was still guarded the old way: by asking
    # whether an expected substring was PRESENT, and by counting lines. That is
    # the exact question R2 was written to abolish, abolished on one path and
    # left standing on the others.
    #
    # S12 reversed "positive = longs pay shorts" to its opposite BUT ONLY WHEN
    # AN ASSET WAS MISSING, so the healthy block stayed byte-identical and
    # `_core_checks` never saw it. That is sabotage S7 — the lie the entire R2
    # rebuild exists to kill — moved one path over. The gate printed the
    # reversed sentence on its own screen in section 5 and put three tick marks
    # underneath it.
    #
    # S13 appended a fabricated rate to the OFFLINE line. The old bar asked
    # only "are the offline words present AND is it one line", and an appended
    # phrase satisfies both.
    #
    # SO: THE DEGRADED PATHS NOW GET THE STANDARD THE HEALTHY PATH ALREADY HAS.
    # Both are rebuilt from the gate's own verbatim wording and its own
    # arithmetic and compared for EXACT EQUALITY. No substring test remains as
    # the only guard on any path that reaches the pilot's eye.
    # =====================================================================

    # The offline line, held verbatim by the test. `section_text` raises
    # ConnectionError("no asset answered") when every asset fails, so the
    # exception name in the honest line is deterministic.
    #
    # =====================================================================
    # GATE 3.2-R4, added 2026-07-28 (evening) after an independent session
    # threw a FOURTEENTH sabotage at Gate 3.2-R3 and it walked through.
    #
    # **THIS LINE USED TO INTERPOLATE THE MODULE'S OWN `OFFLINE_WORDS`.** So it
    # was never a verbatim copy at all — it was a MIRROR. S14 changed that one
    # production constant to
    #
    #     "Funding instrument offline — last reading BTC +0.0100%, longs paying"
    #
    # and the gate's "own copy" changed itself to match, in lockstep. Equality
    # held against the lie, S13 was scored CAUGHT in the same run, and section 6
    # printed the fabricated rate on its own screen with a tick mark under it
    # reading "NOTHING appended". BTC was +0.0027% at that moment, and ETH and
    # SOL were both negative.
    #
    # `GATE_CONTRACTS` exists, twenty lines above, precisely because a test that
    # reads its ground truth from the module will follow that module into a
    # miswiring and cheerfully confirm it. **The identical mistake was sitting
    # further down the same file the whole time.** The words are now typed out
    # here, and the module's are compared AGAINST them by a named check.
    # =====================================================================
    GATE_OFFLINE_WORDS = "Funding instrument offline"
    GATE_OFFLINE_BLOCK = f"  🔌 {GATE_OFFLINE_WORDS} (ConnectionError)"

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
        # GATE 3.2-R4: the gate's own copy, never the module's. A guard that
        # asks the module what its own failure looks like stops recognising a
        # failure the moment the module renames it.
        if GATE_OFFLINE_WORDS in live:
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

    def _expected_partial_block(snap, broken):
        """The ENTIRE degraded block the Brief ought to print when one asset
        fails, assembled from raw by this test's own arithmetic and its own
        wording. `section_text` only collects settlement times from assets that
        ANSWERED, so the expected stamp is the minimum over the survivors."""
        others = [a for a in GATE_CONTRACTS if a != broken]
        parts = [f"{a.split('-')[0]} {_expected_pct(snap[a][0])}"
                 for a in others]
        stamp = _expected_hhmm(min(snap[a][1] for a in others))
        return "\n".join([
            (GATE_LINE1_PREFIX + GATE_SEP.join(parts)
             + f"   [no data: {broken.split('-')[0]}]"),
            GATE_LINE2_HEAD + stamp + GATE_LINE2_TAIL,
            GATE_LINE3_DISCLAIMER,
        ])

    def _partial_checks(verbose=True):
        """GATE 3.2-R2 (d) · 3.2-R3 (a): THE ROTATING PARTIAL-FAILURE DRILL,
        NOW JUDGED BY EXACT EQUALITY.

        The old drill always broke SOL, so it could only ever prove SOL. A
        module that named the missing asset 'SOL' no matter which one failed
        (sabotage S11) agreed with the drill and walked through. Each asset
        now takes a turn as the bogus symbol and must be named BY ITS OWN NAME,
        with the other two still printed.

        **AND, 2026-07-28: the check is no longer a substring test.** It asked
        three questions — is '[no data: X]' there, does each survivor carry a
        sign, is the offline phrase absent — and never looked at the digits, the
        settlement time, the mechanism sentence or the disclaimer. So S12
        reversed the meaning of the instrument on this path alone and the drill
        applauded. The WHOLE degraded block is now rebuilt and compared exactly:
        a reversed sentence, a deleted disclaimer, a wrong rate and an appended
        phantom all fail, because nothing can be added to a string that must
        match exactly.

        The before/after drift allowance is the same one `_core_checks` uses and
        for the same reason — funding is quoted continuously — and it is taken
        PER ASSET, because three degraded blocks are built one after another and
        a snapshot taken before the first is already stale by the third."""
        say = print if verbose else (lambda *a, **k: None)
        ok = True
        for broken in GATE_CONTRACTS:
            short = broken.split('-')[0]
            contracts = {a: ('NOTAREALSYMBOL' if a == broken else c)
                         for a, c in GATE_CONTRACTS.items()}
            before = _raw_snapshot()
            out = section_text(contracts=contracts)
            want = _expected_partial_block(before, broken)
            hit = (out == want)
            if not hit:
                want = _expected_partial_block(_raw_snapshot(), broken)
                hit = (out == want)
            others = [x.split('-')[0] for x in GATE_CONTRACTS if x != broken]
            say(f"   {'✓' if hit else '✗'} {short} broken → the WHOLE degraded "
                f"block equals the block rebuilt from Binance raw: "
                f"'[no data: {short}]' named, {' and '.join(others)} still "
                f"printed, mechanism sentence and disclaimer intact")
            if not hit:
                for i, (got, exp) in enumerate(
                        zip_longest(out.splitlines(), want.splitlines(),
                                    fillvalue=''), start=1):
                    if got != exp:
                        say(f"      line {i} printed : {got!r}")
                        say(f"      line {i} expected: {exp!r}")
            ok = ok and hit
        return ok

    def _offline_checks(verbose=True):
        """GATE 3.2-R3 (b): THE OFFLINE BLOCK, EXACT EQUALITY.

        The old bar asked whether the offline words were present and whether
        there was one line. Sabotage S13 appended a fabricated rate to that one
        line — '— last reading BTC +0.0100%, longs paying' — and satisfied both
        conditions. **An instrument that has just admitted it cannot see
        anything must print NOTHING ELSE**, and the only check that can enforce
        'nothing else' is equality.

        GATE 3.2-R4 (b): AND THE WORDING THE BAR IS BUILT FROM IS NOW CHECKED
        AGAINST THE MODULE'S. Equality is only worth something if the thing
        being compared TO cannot move with the thing being tested. It could,
        and S14 moved it."""
        say = print if verbose else (lambda *a, **k: None)

        # --- GATE 3.2-R4 (b): THE MODULE'S WORDING vs THE GATE'S OWN COPY ---
        # Named separately so a failure says WHICH constant moved, rather than
        # leaving the next session to diff two long strings by eye.
        words_ok = (OFFLINE_WORDS == GATE_OFFLINE_WORDS)
        say(f"   {'✓' if words_ok else '✗'} the module's OFFLINE_WORDS equals "
            f"the gate's own copy ({GATE_OFFLINE_WORDS!r})")
        if not words_ok:
            say(f"      module : {OFFLINE_WORDS!r}")
            say(f"      gate   : {GATE_OFFLINE_WORDS!r}")

        drill = section_text(base_url=OFFLINE_DRILL_URL)
        hit = (drill == GATE_OFFLINE_BLOCK)
        say(f"   {'✓' if hit else '✗'} the offline block equals the gate's own "
            f"verbatim copy exactly — one honest line, no traceback, and "
            f"NOTHING appended")
        if not hit:
            say(f"      printed : {drill!r}")
            say(f"      expected: {GATE_OFFLINE_BLOCK!r}")
        return hit and words_ok

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

    def _sab_partial_meaning_reversed(*a, **k):
        """S12, from the independent review of 2026-07-28. The mechanism
        sentence reverses itself ONLY when an asset is missing, so the healthy
        block stays byte-identical and the whole-block equality check on the
        happy path never sees it. This is S7 moved onto the degraded path —
        which is precisely the path the pilot is reading on a bad morning."""
        out = _SECTION_TEXT_ORIGINAL(*a, **k)
        if '[no data:' in out:
            out = out.replace('positive = longs pay shorts',
                              'positive = shorts pay longs')
        return out

    def _sab_offline_fabricates(*a, **k):
        """S13, from the same review. The offline line keeps the honest offline
        words AND appends a rate that was fetched from nowhere. The old bar —
        'the words are present and it is one line' — was satisfied by both."""
        out = _SECTION_TEXT_ORIGINAL(*a, **k)
        if OFFLINE_WORDS in out:
            out += " — last reading BTC +0.0100%, longs paying"
        return out

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
        # S12 and S13, from the independent review of 2026-07-28. BOTH walked
        # through Gate 3.2-R2. Both live on a DEGRADED path, which is why the
        # whole-block equality check added the day before could not see them.
        ('S12', 'the meaning reverses when an asset fails', 'ESCAPED',
         'section_text', _sab_partial_meaning_reversed, 'partial'),
        ('S13', 'the offline line carries a made-up rate', 'ESCAPED',
         'section_text', _sab_offline_fabricates, 'offline'),
        # S14, from the independent review of 2026-07-28 (evening). It walked
        # through Gate 3.2-R3. **It changes no logic whatsoever** — it rewords
        # one production constant, and the gate's "verbatim copy" of the offline
        # line, which interpolated that same constant, followed it into the lie
        # and confirmed it. It is S13's exact payload delivered through the door
        # the check against S13 was holding open.
        ('S14', 'the offline WORDS themselves reworded', 'ESCAPED',
         'OFFLINE_WORDS',
         "Funding instrument offline — last reading BTC +0.0100%, longs paying",
         'offline'),
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
                survived = {'partial': _partial_checks,
                            'offline': _offline_checks}.get(
                    judge, _core_checks)(verbose=False)
            except Exception:
                survived = False        # a crash is a catch: it did not pass
            finally:
                globals()[attr] = original
            caught = not survived
            print(f"   {'✓' if caught else '✗'} {tag:<4} {words:<40} "
                  f"[old gate: {old:<7}] → "
                  f"{'CAUGHT' if caught else 'ESCAPED AGAIN — GATE IS DECORATIVE'}")
            ok = ok and caught
        restored = (_core_checks(verbose=False) and _partial_checks(verbose=False)
                    and _offline_checks(verbose=False))
        print(f"   {'✓' if restored else '✗'} every original restored — the "
              f"clean checks pass again afterwards")
        return ok and restored

    ok = True
    print("GATE 3.2-R4 — the funding instrument's self-test, hardened")
    print("2026-07-28 (evening). Version 1 reported 48/48 while four deliberate")
    print("lies walked through. Version 2 checked the digits and missed the")
    print("WORDS. Version 3 held every path to exact equality — but built the")
    print("offline bar out of the MODULE'S OWN wording, so rewording that one")
    print("constant moved the lie and the bar together and the gate confirmed")
    print("it. Version 4 holds its own copy and checks the module's against it.")

    print("\n1) LIVE BLOCK — what the Brief will print")
    live = section_text()
    print()
    print(live)
    print()
    if GATE_OFFLINE_WORDS in live:      # the gate's own copy — see 3.2-R4 (b)
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

    print("\n3) EXHIBIT A, MADE PERMANENT (Gate 3.2-R e, f · 3.2-R2 f ·"
          "\n   3.2-R3 c · 3.2-R4 d) — the file is broken on purpose FOURTEEN"
          "\n   ways and each break MUST be caught. Four of the first six"
          "\n   escaped the gate of 2026-07-26; four of the next five escaped"
          "\n   the gate of the day after; BOTH of the next two escaped the gate"
          "\n   of 2026-07-27 by living on a path it only counted; and the"
          "\n   FOURTEENTH escaped the gate of 2026-07-28 by rewording a"
          "\n   constant the gate was reading its own expectation out of.")
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

    print("\n6) OFFLINE DRILL (Gate 3.2-R3 b) — injected unreachable URL,"
          "\n   internet untouched. Judged by EXACT EQUALITY against the gate's"
          "\n   own verbatim copy: sabotage S13 appended a fabricated rate to"
          "\n   this line and the old 'words present, one line' bar passed it.")
    print(f"   pointing the instrument at {OFFLINE_DRILL_URL}")
    print()
    print(section_text(base_url=OFFLINE_DRILL_URL))
    drill_ok = _offline_checks(verbose=True)
    ok = ok and drill_ok

    if ok:
        print("\nGATE 3.2-R4 PASSED — the WHOLE printed block was rebuilt from "
              "Binance\nraw and matched exactly on EVERY path the pilot can "
              "see — healthy,\ndegraded and offline — the fixed wording was "
              "checked verbatim, the\ngate's own offline wording was compared "
              "to the module's, every asset\ntook a turn at failing, and all "
              "FOURTEEN deliberate sabotages were\ncaught. Every expectation in "
              "this gate is now typed out here rather\nthan read from the file "
              "on trial. This test has demonstrated, this\nrun, that it can say "
              "no.")
    else:
        print("\nGATE 3.2-R4 FAILED — see the ✗ lines above.")
    sys.exit(0 if ok else 1)
