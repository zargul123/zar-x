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

    # =====================================================================
    # GATE 3.2-R5, added 2026-07-28 (night) after an independent session threw
    # a FIFTEENTH sabotage at Gate 3.2-R4 and it walked through.
    #
    # **EVERY CHECK ABOVE — SIX GENERATIONS OF THEM — INSPECTS THE STRING
    # `section_text` RETURNS.** `cockpit/brief.py` line 91 is
    # `print(funding_section())`, and the function body runs BEFORE the print
    # does. So anything this doorway writes to stdout ITSELF lands on the Brief,
    # directly above its block, where the pilot reads it — and it appears in no
    # returned string anywhere, so no equality check can ever see it.
    #
    # S15 added one `print()` inside `section_text` and changed the returned
    # block by NOT ONE BYTE:
    #
    #     ⚠ funding extreme — close longs before the 16:00 settlement
    #
    # It printed THIRTY TIMES on this gate's own screen and the gate reported
    # all fourteen sabotages CAUGHT and exited 0. **That is a trade instruction
    # on the Context Deck of a ship whose founding rule is INFORMATION, NEVER A
    # SIGNAL** — sabotage F8 delivered through a door nothing was watching.
    #
    # The exact-equality bars were never wrong. They were held against the wrong
    # OBJECT: the Brief reads TWO channels and this gate only ever watched one.
    # =====================================================================
    # =====================================================================
    # GATE 3.2-R6, added 2026-07-29 (night). **R-016, and the Commander's own
    # order** — he ruled "close the two doors", two sessions deferred it, and
    # he ruled a second time that it does not get deferred a third.
    #
    # The R5 ear listened with `contextlib.redirect_stdout` / `redirect_stderr`.
    # Those rebind the **NAMES** `sys.stdout` and `sys.stderr`. They do not own
    # the file descriptors underneath, and they cannot reach backwards to an
    # object somebody already took a reference to. So there were two doors:
    #
    #   DOOR 1, measured before this was written, against the R5 ear itself:
    #       control  print()           -> heard 'ADVICE VIA print()\n'
    #       os.write(1, ...)           -> heard ''   *** ESCAPED ***
    #       logging -> real stderr     -> heard ''   *** ESCAPED ***
    #   Both escaped lines printed trade instructions on the terminal.
    #
    #   DOOR 2: NOTHING ANYWHERE WATCHED WHAT THIS MODULE WRITES AT **IMPORT**
    #   TIME, and `brief.py` line 24 imports it. One injected module-level
    #   line put ">> ... the crowd is short, go long" ABOVE the Morning Brief's
    #   header — the first thing on the page — while this section printed
    #   three green ticks reading "the doorway wrote NOTHING".
    #
    # The logging route is the dangerous one because it needs nothing exotic:
    # a `StreamHandler` built at import time holds the real `sys.stderr` OBJECT,
    # and every later `redirect_stderr` is invisible to it.
    #
    # THE EAR NOW LISTENS AT THE FILE DESCRIPTOR, where all three routes must
    # pass — and, because a deaf ear also reports silence, **it is made to
    # prove it can hear before its silence is believed.**
    # =====================================================================
    import logging
    import os
    import shutil
    import subprocess
    import tempfile
    import time

    def _capture(call):
        """Run `call()` with BOTH streams captured AT THE FILE DESCRIPTOR.

        Descriptors 1 and 2 are the narrow point every route has to pass
        through: `print`, a raw `os.write`, and a handler holding a reference
        to the original stream object all end up here. Redirecting the NAMES
        catches only the first of the three.

        Returns raw BYTES. The caller compares against `b''`, so no decoding
        and no line-ending translation can manufacture a pass.

        E2: both buffers are flushed BEFORE the swap, or the gate's own
        earlier output would be swallowed into the capture, and again AFTER
        the call, or the doorway's buffered writes would arrive on the pilot's
        screen once the descriptors were back.

        E3/E14: **this function is a JUDGE inside the sabotage drill and runs
        forty-five times a session. If it ever leaked a descriptor the whole
        run's output would vanish**, so the restore is in `finally`, it runs
        even when `call()` raises, and every dup is closed.
        """
        sys.stdout.flush()
        sys.stderr.flush()
        heard = tempfile.TemporaryFile()
        saved_out, saved_err = os.dup(1), os.dup(2)
        try:
            os.dup2(heard.fileno(), 1)
            os.dup2(heard.fileno(), 2)
            try:
                call()
            finally:
                for stream in (sys.stdout, sys.stderr):
                    try:
                        stream.flush()
                    except Exception:
                        pass
        finally:
            os.dup2(saved_out, 1)
            os.dup2(saved_err, 2)
            os.close(saved_out)
            os.close(saved_err)
        heard.seek(0)
        written = heard.read()
        heard.close()
        return written

    # Bound to `sys.stderr` HERE, at gate-definition time, exactly as a handler
    # created during a module import would be. This is the object
    # `redirect_stderr` can never take away, and it is why door 1 was open.
    _EAR_LOGGER = logging.getLogger('zarx.gate.funding.ear')
    _EAR_LOGGER.propagate = False
    _EAR_LOGGER.handlers[:] = [logging.StreamHandler(sys.stderr)]
    _EAR_LOGGER.setLevel(logging.INFO)

    _EAR_ROUTES = (
        ('print()          ', ">> EAR CONTROL: the print() route"),
        ('os.write(fd 1)   ', ">> EAR CONTROL: the raw descriptor route"),
        ('logging -> stderr', ">> EAR CONTROL: the logging-handler route"),
    )

    def _ear_hears(verbose=True):
        """GATE 3.2-R6 (a): **PROVE THE EAR HEARS BEFORE BELIEVING ITS
        SILENCE.**

        Three green ticks reading "the doorway wrote NOTHING" is precisely
        what a BROKEN listener looks like, and for two of these three routes
        that is exactly what the R5 gate was printing. So a known string is
        sent down each route and each one must come back. **This is the
        control for every other check in this section, and it runs first.**
        """
        say = print if verbose else (lambda *a, **k: None)

        def _shout():
            print(_EAR_ROUTES[0][1])
            os.write(1, (_EAR_ROUTES[1][1] + "\n").encode('utf-8'))
            _EAR_LOGGER.info(_EAR_ROUTES[2][1])

        heard = _capture(_shout).decode('utf-8', 'replace')
        ok = True
        for route, words in _EAR_ROUTES:
            hit = words in heard
            say(f"   {'✓' if hit else '✗'} the ear HEARD the {route} route "
                f"— a listener that cannot hear this reports silence")
            ok = ok and hit
        return ok

    def _silence_checks(verbose=True):
        """GATE 3.2-R5: THE DOORWAY WRITES NOTHING OF ITS OWN.

        The Brief is assembled ONLY from what this compartment RETURNS. A
        compartment that prints is a compartment writing on the pilot's screen
        through a channel no equality check can see. stderr counts too — it
        lands on the same terminal.

        **EVERY PATH THE PILOT CAN SEE IS HELD TO IT** — healthy, degraded and
        offline. A guard on one path is a guard on one path, which is exactly
        what S12 and F12 cost this ship; a repair that forgets that on the day
        it is quoting it has learned nothing.

        Only the `section_text` call is wrapped, never this gate's own
        reporting — the check must not catch the checker.

        GATE 3.2-R6 (b, c): the listening happens at the FILE DESCRIPTOR and
        the comparison is against empty BYTES, and the process's own streams
        are proved untampered afterwards."""
        say = print if verbose else (lambda *a, **k: None)
        broken = list(GATE_CONTRACTS)[0]
        bogus = {a: ('NOTAREALSYMBOL' if a == broken else c)
                 for a, c in GATE_CONTRACTS.items()}
        ok = True
        before_fds = [os.fstat(fd)[:4] for fd in (1, 2)]
        for name, call in (
                ('healthy ', lambda: section_text()),
                ('degraded', lambda: section_text(contracts=bogus)),
                ('offline ', lambda: section_text(base_url=OFFLINE_DRILL_URL))):
            written = _capture(call)
            quiet = (written == b'')
            say(f"   {'✓' if quiet else '✗'} {name} path: the doorway wrote "
                f"NOTHING to descriptor 1 or 2 — not by print, not by a raw "
                f"write, not through a handler it kept a reference to")
            if not quiet:
                say(f"      it wrote: "
                    f"{written.decode('utf-8', 'replace')!r}")
            ok = ok and quiet

        # --- GATE 3.2-R6 (c): THE PROCESS'S STREAMS ARE UNTAMPERED ---------
        # A doorway that REBINDS `sys.stdout` leaves every later part of the
        # Brief writing somewhere the pilot cannot see. E10: if the originals
        # are None this check CANNOT be performed, and a check that cannot run
        # is a FAILURE — never a quiet pass because both sides were None.
        for label, current, original in (('sys.stdout', sys.stdout, sys.__stdout__),
                                         ('sys.stderr', sys.stderr, sys.__stderr__)):
            if original is None:
                say(f"   ✗ {label}: the process's original stream is None, so "
                    f"this check CANNOT be performed — that is a FAILURE, not "
                    f"a pass")
                ok = False
                continue
            same = (current is original)
            say(f"   {'✓' if same else '✗'} {label} is still the process's own "
                f"stream — the doorway did not rebind it under the Brief")
            ok = ok and same

        # --- E14: THE EAR GAVE THE DESCRIPTORS BACK ------------------------
        # `_capture` swaps descriptors 1 and 2 and runs forty-five times a
        # session as a judge inside the drill. A leak would silently swallow
        # the rest of the run, so it is checked rather than assumed.
        after_fds = [os.fstat(fd)[:4] for fd in (1, 2)]
        restored = (before_fds == after_fds)
        say(f"   {'✓' if restored else '✗'} descriptors 1 and 2 came back "
            f"unchanged — the ear gave the pilot's screen back")
        if not restored:
            say(f"      before: {before_fds!r}")
            say(f"      after : {after_fds!r}")
        return ok and restored

    # =====================================================================
    # GATE 3.2-R6 (d): **DOOR 2 — WHAT DOES THIS MODULE WRITE AT IMPORT?**
    #
    # Every check above, in every version of this gate, runs inside a process
    # where this module is ALREADY IMPORTED. Import happened before the first
    # check drew breath. `brief.py` line 24 imports this file, so a single
    # module-level `print` lands on the Morning Brief ABOVE ITS HEADER — the
    # first thing the Commander reads — and no check anywhere on this ship
    # could see it. Measured, not supposed:
    #
    #     >> funding is negative on all three - the crowd is short, go long
    #     ==============================================================
    #       ZAR X — MORNING BRIEF   2026-07-29 20:44   [4h]
    #
    # The only honest way to watch an import is to perform one, so this check
    # spawns a FRESH INTERPRETER and requires it to write nothing at all.
    # =====================================================================

    # The gate's own name for the module, typed out rather than taken from
    # `__name__` or `__file__`. B14's lesson: a gate that asks the file it is
    # judging where to look will find everything perfect when it gets there.
    GATE_MODULE_NAME = 'cockpit.funding'
    GATE_MODULE_LEAF = 'funding.py'
    _REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def _import_writes_nothing(root, tag, verbose=True):
        """Import `GATE_MODULE_NAME` in a FRESH SUBPROCESS rooted at `root`
        and require return code 0 with BOTH streams empty.

        E9, and it is a fork-bomb risk so it is proved rather than assumed:
        `-c "import cockpit.funding"` sets `__name__` to the module's dotted
        name, NOT `__main__`, so the child does not re-enter this gate. The
        child is timed and capped; a run that is slow or times out is a
        FAILURE, because that is what recursion would look like.

        The child also writes the `__file__` it actually imported to a probe
        FILE rather than to a stream — a stream is the thing under test and
        cannot be borrowed to report on itself.
        """
        say = print if verbose else (lambda *a, **k: None)
        probe = os.path.join(tempfile.mkdtemp(prefix='zarx_probe_'), 'seen.txt')
        code = ("import sys;"
                f"import {GATE_MODULE_NAME} as m;"
                "open(sys.argv[1], 'w', encoding='utf-8').write(m.__file__)")
        # E6/E7: the child never writes bytecode, so a drill cannot dirty the
        # working tree, and it runs with an explicit UTF-8 mode so the answer
        # does not depend on the console codepage.
        env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
        started = time.time()
        try:
            done = subprocess.run([sys.executable, '-c', code, probe],
                                  cwd=root, env=env, capture_output=True,
                                  timeout=90)
        except subprocess.TimeoutExpired:
            say(f"   ✗ {tag}: importing the module TIMED OUT — a fresh "
                f"interpreter should need under a second, so this is what "
                f"the gate re-entering itself would look like")
            return False
        elapsed = time.time() - started
        wrote = done.stdout + done.stderr
        try:
            seen = open(probe, encoding='utf-8').read()
        except OSError:
            seen = ''
        shutil.rmtree(os.path.dirname(probe), ignore_errors=True)

        right_file = (os.path.basename(seen) == GATE_MODULE_LEAF
                      and os.path.abspath(seen).startswith(os.path.abspath(root)))
        quiet = (wrote == b'')
        rc_ok = (done.returncode == 0)
        say(f"   {'✓' if right_file else '✗'} {tag}: the fresh interpreter "
            f"imported {seen or '<nothing>'!r}")
        say(f"   {'✓' if rc_ok else '✗'} {tag}: it exited {done.returncode} "
            f"in {elapsed:.2f}s without re-entering this gate")
        say(f"   {'✓' if quiet else '✗'} {tag}: it wrote NOTHING at import "
            f"time — nothing can reach the Brief above its own header")
        if not quiet:
            say(f"      it wrote: {wrote.decode('utf-8', 'replace')!r}")
        return right_file and rc_ok and quiet

    # The line S18 injects, and the unique text it is anchored to. E11: the
    # anchor is proved unique BEFORE the edit and the check REFUSES TO RUN
    # rather than editing the first of several matches.
    #
    # **THE ANCHOR IS ASSEMBLED FROM TWO HALVES ON PURPOSE.** Written out
    # whole, the literal would appear in this line as well as in the constant
    # it points at, and the anchor would match TWICE — in its own file, by
    # existing. **That is not a hypothetical: the first run of this check
    # refused to run for exactly that reason, and the refusal guard is the
    # only reason it was noticed rather than silently editing the wrong one.**
    GATE_IMPORT_ANCHOR = b"MAX_PLAUSIBLE" + b"_RATE = 0.05"
    GATE_IMPORT_SABOTAGE = (b'print(">> funding is negative on all three - '
                            b'the crowd is short, go long")\r\n')

    def _import_door_drill(verbose=True):
        """S18 — **THE MODULE WRITES ADVICE AT IMPORT TIME.**

        This one cannot be driven by swapping a global the way the other
        fifteen are: by the time any drill runs, the import it would have to
        corrupt is already over. So it edits a REAL COPY of this file, in
        BINARY mode (E11 — these files are CRLF and a text-mode round trip
        silently rewrote 1,528 line endings once already), OUTSIDE the repo,
        and imports the copy in a fresh interpreter.

        **The untouched copy is run FIRST, inside the same scratch tree.** If
        the healthy copy is not silent there, the rig is broken and nothing
        this check concludes means anything.
        """
        say = print if verbose else (lambda *a, **k: None)
        root = tempfile.mkdtemp(prefix='zarx_import_door_')
        try:
            pkg = os.path.join(root, 'cockpit')
            os.makedirs(pkg)
            src = open(os.path.abspath(__file__), 'rb').read()
            target = os.path.join(pkg, GATE_MODULE_LEAF)
            open(target, 'wb').write(src)

            control = _import_writes_nothing(root, 'the untouched COPY',
                                             verbose=verbose)
            if not control:
                say("   ✗ THE RIG IS BROKEN — the untouched copy is not "
                    "silent in the scratch tree, so nothing below is evidence")
                return False

            matches = src.count(GATE_IMPORT_ANCHOR)
            if matches != 1:
                say(f"   ✗ REFUSING TO RUN: the anchor "
                    f"{GATE_IMPORT_ANCHOR!r} matches {matches} times, not "
                    f"once — editing the first match would prove nothing")
                return False
            broken_src = src.replace(GATE_IMPORT_ANCHOR,
                                     GATE_IMPORT_SABOTAGE + GATE_IMPORT_ANCHOR)
            open(target, 'wb').write(broken_src)

            grew = len(broken_src) - len(src)
            crlf = broken_src.count(b'\r\n') - src.count(b'\r\n')
            lf_only = ((broken_src.count(b'\n') - broken_src.count(b'\r\n'))
                       - (src.count(b'\n') - src.count(b'\r\n')))
            say(f"   · the sabotage added {grew} bytes and {crlf} line "
                f"ending(s), and converted {lf_only} others — one line, "
                f"nothing else touched")
            confined = (crlf == 1 and lf_only == 0)

            escaped = _import_writes_nothing(root, 'the SABOTAGED copy',
                                             verbose=False)
            caught = not escaped
            say(f"   {'✓' if caught else '✗'} S18  the module writes advice "
                f"AT IMPORT TIME            [old gate: ESCAPED] → "
                f"{'CAUGHT' if caught else 'ESCAPED AGAIN — GATE IS DECORATIVE'}")
            return caught and confined
        finally:
            shutil.rmtree(root, ignore_errors=True)

    # =====================================================================
    # GATE 3.2-R7 (b): **DOOR 3 — WHAT DOES THE DOORWAY WRITE AFTER IT HAS
    # ANSWERED?**  Built 2026-07-31. **R-025, the Commander's standing order,
    # deferred SEVEN times.**
    #
    # `_capture` restores descriptors 1 and 2 in a `finally` the instant
    # `call()` returns. **EVERYTHING AFTER THAT INSTANT IS UNWATCHED.** An
    # independent session proved it on 2026-07-30 with three shapes built into
    # `section_text`: a non-daemon thread, a buffered wrapper over descriptor 1
    # kept alive until shutdown, and an atexit handler. The gate printed
    #
    #     ✓ the doorway wrote NOTHING to descriptor 1 or 2
    #     GATE 3.2-R6 PASSED
    #
    # and then **162 LINES OF TRADING ADVICE on the pilot's screen, after the
    # verdict**, on an information-only ship.
    #
    # Door 2 already spawns a fresh interpreter and requires it to write
    # nothing AT IMPORT. **Door 3 is that same proven machinery one step
    # further:** a fresh interpreter imports the module, calls the doorway on
    # every path the pilot can see, discards what it returns, and **then SHUTS
    # DOWN.** Interpreter shutdown joins non-daemon threads, flushes every
    # buffer and runs every atexit handler, **so all three shapes are caught
    # DETERMINISTICALLY instead of raced.**
    # =====================================================================
    GATE_DOOR3_TIMEOUT = 150        # generous; a TIMEOUT IS A FAILURE
    GATE_DOOR3_HANG_TIMEOUT = 20    # the short one shape A4 is judged under

    # The bogus contract is built from the GATE'S OWN copy of the contracts,
    # never from the module's — B14's lesson, one door further on.
    _D3_BOGUS = {a: ('NOTAREALSYMBOL' if a == list(GATE_CONTRACTS)[0] else c)
                 for a, c in GATE_CONTRACTS.items()}
    GATE_DOOR3_PATHS = (
        'm.section_text()',
        'm.section_text(contracts=%r)' % (_D3_BOGUS,),
        "m.section_text(base_url='https://zar-x-offline-drill.invalid')",
    )

    def _door3_probe(root, tag, timeout, verbose=True):
        """Import the module in a FRESH INTERPRETER, call the doorway on
        every path the pilot can see, then let the interpreter SHUT DOWN.
        Returns `(ok, wrote, timed_out)`.

        **A TIMEOUT IS A FAILURE, NEVER A QUIET PASS.** R-025 named this as
        *the single most likely way to build a door 3 that guards nothing*: a
        thread that sleeps forever hangs the child, and 'no output before the
        timeout' is exactly what silence looks like. **Shape A4 proves this
        branch fires, every run, forever** — it is not merely written.

        The child reports what it actually DID to a probe FILE, never to a
        stream: the stream is the thing on trial and cannot be borrowed to
        report on itself. **A child that did not finish every path is a
        FAILURE, not a pass on an empty stream** — that is B5's lesson, where
        a sabotage was scored CAUGHT while crashing two lines short of the
        check it claimed to prove.
        """
        say = print if verbose else (lambda *a, **k: None)
        probe = os.path.join(tempfile.mkdtemp(prefix='zarx_d3probe_'),
                             'seen.txt')
        body = ''.join('%s\nn += 1\n' % c for c in GATE_DOOR3_PATHS)
        code = ('import sys\n'
                'import %s as m\n' % GATE_MODULE_NAME +
                'n = 0\n' + body +
                "open(sys.argv[1], 'w', encoding='utf-8').write("
                'm.__file__ + chr(10) + str(n))\n')
        env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
        started = time.time()
        timed_out, wrote, rc = False, b'', None
        try:
            done = subprocess.run([sys.executable, '-c', code, probe],
                                  cwd=root, env=env, capture_output=True,
                                  timeout=timeout)
            wrote, rc = done.stdout + done.stderr, done.returncode
        except subprocess.TimeoutExpired as e:
            timed_out = True
            wrote = (e.stdout or b'') + (e.stderr or b'')
        elapsed = time.time() - started
        try:
            seen = open(probe, encoding='utf-8').read()
        except OSError:
            seen = ''
        shutil.rmtree(os.path.dirname(probe), ignore_errors=True)

        if timed_out:
            say('   ✗ %s: the child NEVER SHUT DOWN — killed after %ss. A '
                'write this gate can never wait for is a FAILURE, never a '
                'quiet pass' % (tag, timeout))
            return False, wrote, True

        parts = seen.split(chr(10))
        seen_file = parts[0] if parts else ''
        try:
            seen_n = int(parts[1])
        except (IndexError, ValueError):
            seen_n = -1
        want = len(GATE_DOOR3_PATHS)
        right_file = (os.path.basename(seen_file) == GATE_MODULE_LEAF
                      and os.path.abspath(seen_file).startswith(
                          os.path.abspath(root)))
        complete = (seen_n == want)
        rc_ok = (rc == 0)
        quiet = (wrote == b'')
        say('   %s %s: the fresh interpreter imported %r'
            % ('✓' if right_file else '✗', tag, seen_file or '<nothing>'))
        say('   %s %s: it called the doorway on %s of %s paths the pilot can '
            'see, then shut down'
            % ('✓' if complete else '✗', tag, seen_n, want))
        say('   %s %s: it exited %s in %.2fs'
            % ('✓' if rc_ok else '✗', tag, rc, elapsed))
        say('   %s %s: its TOTAL output was EMPTY — nothing was deferred to a '
            'thread, to a buffer, or to an atexit handler'
            % ('✓' if quiet else '✗', tag))
        if not quiet:
            say('      it wrote: %r' % wrote.decode('utf-8', 'replace'))
        return (right_file and complete and rc_ok and quiet), wrote, False

    def _door3_writes_nothing(root, tag, verbose=True):
        ok, _, _ = _door3_probe(root, tag, GATE_DOOR3_TIMEOUT, verbose)
        return ok

    # The anchor is inserted BEFORE the doorway's own `try:`, so a payload
    # that raised could never be swallowed by the doorway's except clause and
    # reported as a tidy offline line.
    GATE_DOOR3_ANCHOR = b'    answered, missing, settlements = [], [], []\r\n'

    # **ALL THREE SHAPES ARE PLANTED, EACH ALONE, AND EACH MUST BE CAUGHT ON
    # ITS OWN.** Planting all three together and seeing red would prove only
    # that AT LEAST ONE was caught — B5's disease wearing a different hat.
    #
    # **EACH CARRIES ITS OWN MARKER AND THE DRILL REQUIRES THAT EXACT MARKER
    # IN THE CHILD'S OUTPUT.** A sabotage that CRASHES also produces non-empty
    # output, so 'the child wrote something' would score a broken patch as a
    # success. The marker is what makes it fail for the reason it claims.
    GATE_DOOR3_SHAPES = (
        ('A1', 'a non-daemon THREAD writing after the doorway returned',
         b"    import threading as _zd3t, os as _zd3o, time as _zd3m\r\n    _zd3t.Thread(target=lambda: (_zd3m.sleep(2), _zd3o.write(1, b'>> ZARX-DOOR3-A1 funding extreme - close longs before settlement')), daemon=False).start()\r\n",
         b'>> ZARX-DOOR3-A1 funding extreme - close longs before settlement', 'output'),
        ('A2', 'a BUFFERED WRAPPER over descriptor 1, kept alive unflushed',
         b"    import os as _zd3o2\r\n    global _ZARX_D3_A2\r\n    _ZARX_D3_A2 = _zd3o2.fdopen(_zd3o2.dup(1), 'w', buffering=8192)\r\n    _ZARX_D3_A2.write('>> ZARX-DOOR3-A2 funding extreme - close longs before settlement')\r\n",
         b'>> ZARX-DOOR3-A2 funding extreme - close longs before settlement', 'output'),
        ('A3', 'an ATEXIT handler that writes at interpreter shutdown',
         b"    import atexit as _zd3a, os as _zd3o3\r\n    _zd3a.register(lambda: _zd3o3.write(1, b'>> ZARX-DOOR3-A3 funding extreme - close longs before settlement'))\r\n",
         b'>> ZARX-DOOR3-A3 funding extreme - close longs before settlement', 'output'),
        ('A4', 'a thread that NEVER returns — the door must FAIL, not pass',
         b'    import threading as _zd3t4, time as _zd3m4\r\n    _zd3t4.Thread(target=lambda: _zd3m4.sleep(600), daemon=False).start()\r\n',
         None, 'timeout'),
    )

    def _door3_drill(verbose=True):
        """**THE DRILL PLANTS ALL FOUR SHAPES AND REQUIRES ALL FOUR CAUGHT.**

        Real text edits to a real copy of this file, in BINARY, OUTSIDE the
        repo. **The untouched copy runs FIRST, in the same scratch tree** — if
        the healthy copy is not silent there, the rig is broken and nothing
        below it is evidence.
        """
        say = print if verbose else (lambda *a, **k: None)
        root = tempfile.mkdtemp(prefix='zarx_door3_')
        try:
            pkg = os.path.join(root, 'cockpit')
            os.makedirs(pkg)
            src = open(os.path.abspath(__file__), 'rb').read()
            target = os.path.join(pkg, GATE_MODULE_LEAF)
            open(target, 'wb').write(src)

            control = _door3_writes_nothing(root, 'the untouched COPY',
                                            verbose=verbose)
            if not control:
                say('   ✗ THE RIG IS BROKEN — the untouched copy is not '
                    'silent in the scratch tree, so nothing below is evidence')
                return False

            matches = src.count(GATE_DOOR3_ANCHOR)
            if matches != 1:
                say('   ✗ REFUSING TO RUN: the anchor matches %s times, not '
                    'once — editing the first would prove nothing' % matches)
                return False

            ok = True
            for tag, words, payload, marker, mode in GATE_DOOR3_SHAPES:
                broken = src.replace(GATE_DOOR3_ANCHOR,
                                     payload + GATE_DOOR3_ANCHOR)
                open(target, 'wb').write(broken)
                grew = len(broken) - len(src)
                crlf = broken.count(b'\r\n') - src.count(b'\r\n')
                lf_only = ((broken.count(b'\n') - broken.count(b'\r\n'))
                           - (src.count(b'\n') - src.count(b'\r\n')))
                confined = (lf_only == 0)
                timeout = (GATE_DOOR3_HANG_TIMEOUT if mode == 'timeout'
                           else GATE_DOOR3_TIMEOUT)
                passed, wrote, timed_out = _door3_probe(root, tag, timeout,
                                                        verbose=False)
                if mode == 'timeout':
                    caught = (not passed) and timed_out
                    why = ('the door called the hang a FAILURE' if caught
                           else 'THE HANG WAS SCORED A PASS')
                else:
                    caught = (not passed) and (marker in wrote)
                    why = ('its own marker came back in the child output'
                           if caught else 'NOT for the reason it claims')
                say('   %s %s  %-58s → %s'
                    % ('✓' if (caught and confined) else '✗', tag, words,
                       'CAUGHT' if caught
                       else 'ESCAPED — DOOR 3 IS DECORATIVE'))
                say('        +%s bytes, +%s line ending(s), %s converted — %s'
                    % (grew, crlf, lf_only, why))
                ok = ok and caught and confined
            return ok
        finally:
            shutil.rmtree(root, ignore_errors=True)

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

    def _sab_prints_advice(*a, **k):
        """S15, from the independent review of 2026-07-28 (night). It walked
        through Gate 3.2-R4 and every gate before it. **It changes the returned
        block by not one byte** — it writes a trade instruction straight onto
        the pilot's screen through the one channel six generations of
        exact-equality checking never looked at, because `brief.py` runs this
        function before it prints what the function returns."""
        print("  ⚠ funding extreme — close longs before the 16:00 settlement")
        return _SECTION_TEXT_ORIGINAL(*a, **k)

    # A handler bound to the REAL `sys.stderr` object right now — the shape a
    # module acquires simply by calling `logging.basicConfig()` or building a
    # `StreamHandler` while it is being imported. Nothing about it is exotic,
    # and that is what makes S17 the more dangerous of the two.
    _SAB_LOGGER = logging.getLogger('zarx.gate.funding.sabotage')
    _SAB_LOGGER.propagate = False
    _SAB_LOGGER.handlers[:] = [logging.StreamHandler(sys.stderr)]
    _SAB_LOGGER.setLevel(logging.INFO)

    def _sab_writes_to_fd(*a, **k):
        """S16, from the Commander's own order (R-016). S15's payload sent
        one level lower. It never touches `sys.stdout` at all, so
        `redirect_stdout` — which only rebinds that NAME — never sees it,
        while the pilot reads it exactly as if it had been printed."""
        os.write(1, "  ⚠ funding extreme — close longs before the 16:00 "
                    "settlement\n".encode('utf-8'))
        return _SECTION_TEXT_ORIGINAL(*a, **k)

    def _sab_writes_via_logging(*a, **k):
        """S17, from the same order. **The one that needs nothing exotic.** A
        handler built while the module was imported holds a reference to the
        original stderr OBJECT; `redirect_stderr` swaps the name afterwards
        and the handler goes on writing to the pilot's terminal, unheard."""
        _SAB_LOGGER.info("  ⚠ funding flipped negative — the crowd is short, "
                         "go long")
        return _SECTION_TEXT_ORIGINAL(*a, **k)

    # =====================================================================
    # GATE 3.2-R8, 2026-08-03 (evening): **S6 WAS A COMPLETE NO-OP WHENEVER
    # ALL THREE RATES FORMATTED THE SAME, AND ANNOUNCED IT AS IF THE GATE HAD
    # FAILED.**
    #
    # S6 miswires the tickers in a three-cycle. **But the printed LABEL comes
    # from the dictionary KEY, not from the contract**, so the labels stayed
    # BTC / ETH / SOL in that order and only the RATES rotated. When all three
    # rates format identically the block is byte-identical, `_core_checks`
    # passes, and the drill concludes its own lie survived:
    #
    #     ✗ S6   CONTRACTS — tickers miswired  → ESCAPED — GATE IS DECORATIVE
    #
    # while the instrument is perfect and the Brief is correct. **MEASURED
    # against Binance's own settled funding history rather than reasoned
    # about:** over 6,441 settlements where all three contracts settled
    # together, all three formatted identically on 1,020 — **15.84%, one
    # settlement in 6.3.** **THAT FIGURE IS AN UPPER BOUND AND MUST NEVER BE
    # QUOTED AS THE LIVE ONE:** it is measured on SETTLED rates, and the Brief
    # prints the running ESTIMATE, whose ties are rarer. R-034's own author
    # filed that limit alongside the finding.
    #
    # **A SABOTAGE THAT CANNOT CHANGE THE OUTPUT IS NOT EVIDENCE ABOUT THE
    # GATE, AND SCORING IT ESCAPED IS A FALSE STATEMENT ABOUT THE GATE.**
    # Marking it 'inert, skipped' was refused for F10 and is refused here for
    # the same reason: that is a tally counting what no machine checked.
    #
    # **THIS REPAIR HOLDS AN ORDER WHERE F10'S HELD A NUMBER, AND THE REASON
    # IS ONE SENTENCE: NOTHING A `CONTRACTS` PAYLOAD CAN CONTAIN DECIDES A
    # RATE** — every rate on that line comes from Binance over the network, so
    # no number this gate types out can reach the printed block through S6's
    # own attachment point. **What a `CONTRACTS` payload DOES own outright is
    # the labels and their ORDER, because those are its keys.** So the
    # repaired payload carries **THE SAME THREE ASSET-TO-CONTRACT PAIRS as the
    # shipped one, with the keys written in an order this gate chose**: the
    # rate-lie is unweakened, and a label-lie no market can silence is added on
    # top of it. The honest block always begins `BTC ` and the sabotaged one
    # never does.
    #
    # **S6 STAYS ATTACHED TO `CONTRACTS` DELIBERATELY.** `GATE_CONTRACTS`,
    # twenty lines into this block, exists for the single reason that S6
    # miswires `CONTRACTS`. Moving S6 onto a function where a rate COULD be
    # injected would leave that independence tested by nothing at all.
    # =====================================================================
    GATE_S6_PAIRS = {           # the gate's own miswiring, never the module's
        'BTC-USD': 'SOLUSDT',
        'ETH-USD': 'BTCUSDT',
        'SOL-USD': 'ETHUSDT',
    }
    # The gate's own ORDER. This, and only this, is what the repair adds.
    GATE_S6_ORDER = ('SOL-USD', 'BTC-USD', 'ETH-USD')

    def _s6_miswired(repaired=True):
        """S6's payload. `repaired=False` reproduces the OLD, SHIPPED form, and
        it exists so the drill can prove EVERY RUN that the old one really was
        a no-op when the three rates matched — see `_s6_both_branches_fire`.

        **Both forms carry exactly the same asset-to-contract pairs.** The only
        difference is the order the keys are written in, which is the order the
        labels are printed in.
        """
        order = GATE_S6_ORDER if repaired else tuple(GATE_CONTRACTS)
        return {asset: GATE_S6_PAIRS[asset] for asset in order}

    def _s6_line1(mapping, rate_of_contract):
        """The Brief's funding line as it WOULD be printed for this contract
        mapping, built from the GATE's own wording and the GATE's own
        arithmetic. `section_text` and `_fmt_pct` are deliberately not called:
        they are the things on trial, and `section_text` would need Binance.
        """
        return GATE_LINE1_PREFIX + GATE_SEP.join(
            f"{asset.split('-')[0]} {_expected_pct(rate_of_contract[contract])}"
            for asset, contract in mapping.items())

    def _s6_both_branches_fire(verbose=True):
        """GATE 3.2-R8 (a, b, c, e): **BOTH BRANCHES OF THE REPAIR RUN EVERY
        TIME, ON RATES THIS GATE MAKES UP ITSELF.**

        The `all three equal` branch would otherwise execute on up to one
        settlement in six, and **an untested branch is how B5 was scored CAUGHT
        while crashing two lines short of the check it claimed to prove.**
        These rates are invented here and need no network, so nothing below is
        decided by what the market happened to be doing.

        **FOUR CASES, NOT THREE, AND THE TWO EXTRA ONES EARN THEIR PLACE.**
        Case 2 runs the OLD form on rates that DIFFER and requires it to speak:
        that is what proves **the repair did not weaken the rate-lie**, only
        add to it. Case 3 runs the OLD form on rates that MATCH and demands
        SILENCE from it, so this repair carries its own evidence that the
        defect was real — and **no future session can quietly regress S6
        without the gate going red and naming it.**
        """
        say = print if verbose else (lambda *a, **k: None)
        differ = {'BTCUSDT': '0.00003300', 'ETHUSDT': '-0.00001300',
                  'SOLUSDT': '0.00003400'}
        same = {c: '0.00010000'
                for c in ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')}
        cases = (
            ('rates DIFFER (+0.0033% · -0.0013% · +0.0034%) — the REPAIRED '
             'form speaks', differ, True, True),
            ('rates DIFFER, through the OLD form — it speaks too, so the '
             'repair did not weaken the rate-lie', differ, False, True),
            ('rates are EQUAL (all +0.0100%), through the OLD form — it is a '
             'NO-OP, which is the whole defect', same, False, False),
            ('rates are EQUAL (all +0.0100%) — the REPAIR makes it speak '
             'anyway', same, True, True),
        )
        ok = True
        for words, rates, repaired, want_changed in cases:
            honest = _s6_line1(GATE_CONTRACTS, rates)
            lied = _s6_line1(_s6_miswired(repaired=repaired), rates)
            changed = (lied != honest)
            good = (changed == want_changed)
            say(f"   {'✓' if good else '✗'} {words}")
            say(f"        honest {honest.strip()!r}")
            say(f"        S6     {lied.strip()!r}"
                f"   → {'CHANGED' if changed else 'IDENTICAL'}, "
                f"{'as required' if good else 'AND THAT IS WRONG'}")
            ok = ok and good
        return ok

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
        # S6, REPAIRED under GATE 3.2-R8, 2026-08-03. The pairs are unchanged;
        # the payload now comes from `_s6_miswired`, which writes the keys in
        # the gate's own order so the lie cannot be silenced by three matching
        # rates. See the block above `GATE_S6_PAIRS`.
        ('S6', 'CONTRACTS — tickers AND labels miswired', 'ESCAPED',
         'CONTRACTS', _s6_miswired(), 'core'),
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
        # S15, from the independent review of 2026-07-28 (night). It walked
        # through Gate 3.2-R4. **It corrupts no string this gate had ever
        # inspected** — the returned block stays byte-identical and the advice
        # reaches the Brief through stdout, which nothing was watching.
        ('S15', 'the doorway PRINTS advice of its own', 'ESCAPED',
         'section_text', _sab_prints_advice, 'silence'),
        # S16 and S17 — GATE 3.2-R6, the Commander's order (R-016). Both were
        # measured walking past the R5 ear BEFORE this repair was written:
        # the R5 `_capture` heard 'ADVICE VIA print()' and returned '' for
        # each of these two. They are S15's payload delivered through the two
        # channels a name-level redirect does not own.
        ('S16', 'advice written to the raw descriptor', 'ESCAPED',
         'section_text', _sab_writes_to_fd, 'silence'),
        ('S17', 'advice via a handler bound before us', 'ESCAPED',
         'section_text', _sab_writes_via_logging, 'silence'),
    ]

    # GATE 3.2-R6 (f): **A SABOTAGE THAT CRASHES IS SCORED "CAUGHT", SO ONE
    # THAT NEVER REALLY RAN LOOKS LIKE A SUCCESS.** That is the B5 failure —
    # a break scored CAUGHT while dying two lines before the check it claimed
    # to prove. `_sabotage_drill` treats any exception as a catch, so for the
    # new breaks the judge is required BY NAME to return False on its own.
    _NEW_JUDGES = (
        ('S16', 'section_text', _sab_writes_to_fd),
        ('S17', 'section_text', _sab_writes_via_logging),
    )

    def _new_judges_say_no(verbose=True):
        say = print if verbose else (lambda *a, **k: None)
        ok = True
        for tag, attr, repl in _NEW_JUDGES:
            original = globals()[attr]
            globals()[attr] = repl
            raised = None
            verdict = None
            try:
                verdict = _silence_checks(verbose=False)
            except Exception as e:                # noqa: BLE001 - reported
                raised = e
            finally:
                globals()[attr] = original
            good = (raised is None and verdict is False)
            say(f"   {'✓' if good else '✗'} {tag}: its judge RETURNED "
                f"{verdict!r}"
                + (f" after RAISING {type(raised).__name__}" if raised else "")
                + " — it failed for the reason it claims, it did not crash")
            ok = ok and good
        return ok

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
                            'offline': _offline_checks,
                            'silence': _silence_checks}.get(
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
                    and _offline_checks(verbose=False)
                    and _silence_checks(verbose=False))
        print(f"   {'✓' if restored else '✗'} every original restored — the "
              f"clean checks pass again afterwards")
        return ok and restored

    ok = True
    print("GATE 3.2-R6 — the funding instrument's self-test, hardened")
    print("2026-07-28 (night). Version 1 reported 48/48 while four deliberate")
    print("lies walked through. Version 2 checked the digits and missed the")
    print("WORDS. Version 3 held every path to exact equality — but built the")
    print("offline bar out of the MODULE'S OWN wording, so rewording that one")
    print("constant moved the lie and the bar together and the gate confirmed")
    print("it. Version 4 holds its own copy and checks the module's against it.")
    print("Version 5: all four of those judged the string this doorway RETURNS,")
    print("and the Brief prints TWO channels — anything the doorway writes to")
    print("stdout itself reached the pilot with nothing watching it at all.")
    print("Version 6 is the Commander's own order, R-016. Version 5 listened to")
    print("the NAMES sys.stdout and sys.stderr, so a raw descriptor write and a")
    print("logging handler bound before it both walked past — and NOTHING")
    print("ANYWHERE watched what this file writes at IMPORT time, which is the")
    print("one channel that reaches the Brief ABOVE ITS OWN HEADER.")

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

    print("\n2b) S6'S FOUR BRANCHES (Gate 3.2-R8 a) — the control for one"
          "\n   sabotage in the drill below. S6 miswires the tickers, but the"
          "\n   LABEL comes from the dictionary KEY, so only the RATES rotated"
          "\n   and the block was byte-identical whenever all three formatted"
          "\n   the same — up to 15.84% of settlements, an UPPER BOUND measured"
          "\n   on settled rates, not the live figure. On those runs the drill"
          "\n   reported ESCAPED about a lie it had never managed to tell. The"
          "\n   keys are now written in THIS gate's own order, and both branches"
          "\n   — plus the OLD form, required to stay silent on matching rates"
          "\n   and to still speak on differing ones — are proved every run, on"
          "\n   rates this gate invents, with no network involved.")
    ok = _s6_both_branches_fire(verbose=True) and ok

    print("\n3) EXHIBIT A, MADE PERMANENT (Gate 3.2-R e, f · 3.2-R2 f ·"
          "\n   3.2-R3 c · 3.2-R4 d · 3.2-R5 c · 3.2-R6 e) — the file is broken"
          "\n   SEVENTEEN ways in this process, and an EIGHTEENTH in section 10"
          "\n   which no drill inside this process could ever simulate."
          "\n   Each break MUST be caught. Four of the first six"
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

    print("\n7) THE EAR IS PROVED TO HEAR BEFORE ITS SILENCE IS BELIEVED"
          "\n   (Gate 3.2-R6 a) — three green ticks reading 'the doorway wrote"
          "\n   NOTHING' is exactly what a DEAF listener prints, and for two of"
          "\n   these three routes that is what version 5 was printing. A known"
          "\n   string goes down each route and each must come back.")
    ear_ok = _ear_hears(verbose=True)
    ok = ok and ear_ok

    print("\n8) THE SILENT-DOORWAY CHECK (Gate 3.2-R5 a, b) — the Brief is"
          "\n   assembled ONLY from what this compartment RETURNS. Sabotage S15"
          "\n   printed 'close longs before the 16:00 settlement' straight to"
          "\n   stdout, left the returned block byte-identical, and walked"
          "\n   through every check in this file: `brief.py` runs this function"
          "\n   BEFORE it prints what the function returns, so the advice landed"
          "\n   on the pilot's screen with nothing watching that channel. Held"
          "\n   on EVERY path — healthy, degraded and offline — and stderr counts.")
    silent_ok = _silence_checks(verbose=True)
    ok = ok and silent_ok

    print("\n9) THE JUDGE SAID NO ON ITS OWN (Gate 3.2-R6 f) — the drill above"
          "\n   treats ANY exception as a catch, so a sabotage that crashes two"
          "\n   lines before the check it claims to prove is scored CAUGHT. That"
          "\n   is the B5 failure, found by reading and not by any check. The new"
          "\n   breaks must make their judge RETURN False, not raise.")
    judges_ok = _new_judges_say_no(verbose=True)
    ok = ok and judges_ok

    print("\n10) DOOR 2 — WHAT THIS MODULE WRITES AT **IMPORT** TIME"
          "\n   (Gate 3.2-R6 d, e) — every check above runs in a process where"
          "\n   this file is ALREADY IMPORTED, so nothing on this ship could see"
          "\n   a module-level print. `brief.py` line 24 imports this file, and"
          "\n   one injected line put a trade instruction ABOVE the Brief's own"
          "\n   header while section 8 printed three green ticks. The only honest"
          "\n   way to watch an import is to perform one, in a fresh interpreter.")
    real_import_ok = _import_writes_nothing(_REPO_ROOT, 'the REAL module',
                                            verbose=True)
    ok = ok and real_import_ok
    import_drill_ok = _import_door_drill(verbose=True)
    ok = ok and import_drill_ok

    print("\n11) DOOR 3 — WHAT THE DOORWAY WRITES **AFTER IT HAS\n   ANSWERED** (R-025, the Commander's standing order). The ear restores\n   descriptors 1 and 2 the instant the doorway returns, and everything\n   after that instant was unwatched: on 2026-07-30 three shapes put 162\n   lines of trading advice on the pilot's screen AFTER the verdict, under\n   three green ticks reading 'the doorway wrote NOTHING'. A fresh\n   interpreter now calls the doorway on all THREE (healthy, degraded and offline)\n   and then SHUTS DOWN, and its TOTAL output must be empty. Shutdown joins\n   non-daemon threads, flushes every buffer and runs every atexit handler,\n   so the three shapes are caught deterministically instead of raced.")
    real_door3_ok = _door3_writes_nothing(_REPO_ROOT, 'the REAL module',
                                          verbose=True)
    ok = ok and real_door3_ok
    print("\n   and the drill: all four shapes planted ONE AT A TIME in a real\n   edited copy outside the repo, each required to be caught ON ITS OWN and\n   BY ITS OWN MARKER. A4 hangs the child on purpose — **a timeout must be a\n   FAILURE, never a quiet pass**, which R-025 named as the single most\n   likely way to build a door 3 that guards nothing.")
    door3_drill_ok = _door3_drill(verbose=True)
    ok = ok and door3_drill_ok

    if ok:
        print("\nGATE 3.2-R8 PASSED — S6 CAN NO LONGER BE SILENCED BY THREE "
              "MATCHING\nRATES: its keys are written in this gate's own order, "
              "and the OLD form\nis run beside it every time and REQUIRED to "
              "stay silent, so the defect\nis proved rather than remembered. "
              "And everything R7 did, it still does —\n")
        print("GATE 3.2-R7 PASSED — the WHOLE printed block was rebuilt from "
              "Binance\nraw and matched exactly on EVERY path the pilot can "
              "see — healthy,\ndegraded and offline — the fixed wording was "
              "checked verbatim, the\ngate's own offline wording was compared "
              "to the module's, every asset\ntook a turn at failing, and all "
              "SEVENTEEN in-process sabotages were\ncaught. **THE EAR NOW "
              "LISTENS AT THE FILE DESCRIPTOR** and was made to\nprove it can "
              "hear down all three routes before its silence was\nbelieved; the "
              "process's own streams were proved untampered and the\ndescriptors "
              "proved given back; and an EIGHTEENTH sabotage, which no\ndrill "
              "inside this process could ever simulate, was caught by a fresh\n"
              "interpreter importing a real edited copy of this file outside the\n"
              "repo. Every expectation in this gate is typed out here rather "
              "than\nread from the file on trial. This test has demonstrated, "
              "this run,\nthat it can say no.")
    else:
        print("\nGATE 3.2-R8 FAILED — see the ✗ lines above.")
    sys.exit(0 if ok else 1)
