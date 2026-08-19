"""
Zar X cockpit — the Carry Monitor (Phase 4, Layer 7).

There is a way to earn in crypto that needs no view on direction at all.
Hold the coin, and at the same time hold an equal and opposite bet on the
futures market. The two cancel out, so the price can do whatever it likes.
But every eight hours the exchange makes one side of that futures bet pay
the other, and that stream is what this part measures.

    long the spot coin  +  SHORT the perpetual futures  =  delta-neutral

**THE SIGN IS THE WHOLE INSTRUMENT.** Positive funding means longs pay
shorts. The carry is SHORT the perp, so **positive funding EARNS and
negative funding COSTS**. Printing "it pays 11%" when it in fact costs 11%
is the worst thing this file can do, and no check that merely asks whether
a number appeared would ever catch it. So the sign is never left implied:
every figure carries an explicit `+` or `-` AND the word `(earns)` or
`(costs)` beside it, and the gate proves the printed word against a worked
example typed out in plain words.

**WHY A SINGLE FUNDING PRINT IS NEVER ANNUALISED, WHICH IS THE BIGGEST
HONESTY TRAP IN THIS INSTRUMENT.** One eight-hour print of 0.05% becomes
54% a year on paper — a number that will never persist and that would sit
on the Morning Brief looking like a fortune. This part reads the last
WINDOW **SETTLED** fundings, averages those, and NAMES THE WINDOW on the
line the Commander reads. Settled rates are payments that actually
happened; the running estimate for the next settlement is not one, and is
not used here.

**WHAT THE x1,095 STANDS ON, said out loud because nothing in the numbers
would look wrong if it broke.** Three settlements a day, 365 days. That is
true only while the venue settles these contracts every EIGHT HOURS. If a
contract moved to four-hourly funding, the true annual figure would be
DOUBLE what this file prints and every digit on the screen would still look
healthy. So the spacing between the settlements in the window is checked on
every single read, and a window whose settlements are not eight hours apart
is REFUSED BY NAME rather than annualised. **MEASURED 2026-08-19: the real
gaps are not exactly eight hours — they wobble across seven distinct values
between 28,799,995 ms and 28,800,002 ms — so the check carries a tolerance
of 60 seconds: twelve thousand times the largest wobble ever seen, and
still far too tight to let a missed settlement through.**

**IT IS A NUMBER BEFORE COSTS.** Spot fee, perp fee, the spread, and
capital tied up on both legs at once. A carry figure with no cost warning
is closer to a sales pitch than a readout, so the warning is unconditional:
it prints on every run, not only when the number is large.

INFORMATION, NEVER A SIGNAL — and this file needs that rule more than any
other on this ship, because it prints a percent-a-year figure, which is the
closest Zar X has ever come to something that sounds like an opportunity.
**The three assets are printed in a FIXED ORDER and are NEVER sorted by
which pays most: ranking them is a recommendation however carefully the
words around it are chosen.** It never says "do it". **Phase 6's three
signal slots are locked BY NAME — Turtle / Donchian, funding-rate fade,
on-chain cycle thermometer — and the carry monitor is not one of them and
never can be.**

LAW 2 — the compartment owns its sources: the host, the path, the symbol
mapping and the window live in THIS file and nowhere else. It does NOT
import `cockpit/funding.py`, so either instrument can be killed without
touching the other. The cost of that is named rather than hidden: two
instruments now call the same host each morning, which is R-056's
territory.

LAW 3 — the doorway never raises and never prints; it RETURNS. Every
failure becomes one honest, NAMED line and the Brief carries on. An asset
whose reading failed still gets its row: an asset that quietly vanishes is
B7's shape.

Standalone smoke test:
    python cockpit/carry.py          (live block, then the failure drills)
    python cockpit/carry.py --gate   (gate 4.1, including the sabotage drill)
"""
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

import requests

FAPI_BASE = 'https://fapi.binance.com'
FUNDING_PATH = '/fapi/v1/fundingRate'

# Law 2: our assets are spot pairs; funding exists only on the perpetual
# contracts, which are DIFFERENT INSTRUMENTS that happen to track them. A
# tuple, not a dict, because the ORDER is what the Commander reads and it is
# never sorted.
SYMBOLS = (('BTC', 'BTCUSDT'), ('ETH', 'ETHUSDT'), ('SOL', 'SOLUSDT'))

WINDOW = 21                  # settled fundings averaged: 7 days at three a day
SETTLEMENTS_A_YEAR = 1095    # 3 x 365. SIMPLE, never compounded.
INTERVAL_MS = 8 * 60 * 60 * 1000        # the 8 hours the multiplier stands on
INTERVAL_TOL_MS = 60 * 1000             # measured wobble is <= 5 ms
TIMEOUT = 10                 # seconds; one attempt per asset, never a storm
MIN_ROWS = 1                 # fewer than this is `no rows`, never a blank
MAX_AGE_MIN = 600            # the newest settlement is <= 480 min old normally

# Sanity bound on ONE settled rate. MEASURED 2026-08-19 from Binance's own
# `/fapi/v1/fundingInfo`: the cap is 0.00300 for BTCUSDT and ETHUSDT and
# 0.00375 for SOLUSDT. This bound is 2.7x the largest of those, so it can
# never refuse a legitimate reading, and one fifth of the 0.05 in
# `cockpit/funding.py` that the Commander's desk has wanted tightened since
# Phase 3. It exists to catch a parse disaster, not to second-guess the venue.
MAX_PLAUSIBLE_RATE = Decimal('0.01')

PLACES = Decimal('0.01')     # two decimal places, ROUND_HALF_UP

VENUE_WORDS = "Binance USDT-perps"
OFFLINE_WORDS = "Carry monitor offline"
EARNS_WORD = '(earns)'
COSTS_WORD = '(costs)'
FLAT_WORD = '(flat)'

# The caveats. VERBATIM AND UNCONDITIONAL — every run, not only when the
# number is large. Each is its own constant so the drill can reword exactly
# one of them and be caught doing it.
FOOT_METHOD = "  (long spot + SHORT the perp, delta-neutral — the two cancel out)"
FOOT_SIGN = "   · plus = the carry EARNS it, minus = the carry COSTS it"
FOOT_IF = "   · it pays this IF you run it — this is not advice to run it"
FOOT_COSTS = (
    "   · BEFORE costs: spot fee, perp fee, the spread, and capital tied",
    "     up on BOTH legs at once",
)
FOOT_RISK = (
    "   · exchange counterparty risk · funding can flip negative at any",
    "     settlement",
)
FOOTER_TAIL = "information, not a signal)"

# Used only by the offline drill: the .invalid top-level domain is reserved by
# the RFCs and can never resolve, so the drill proves the fail-safe without
# unplugging the Commander's internet.
OFFLINE_DRILL_URL = 'https://zar-x-carry-drill.invalid'


class CarryError(Exception):
    """A failure this compartment turns into a NAMED absence on the deck.

    Its message is written to be read by the Commander, not by a programmer:
    it is printed verbatim inside `[no data: ...]`.
    """


def _get(base_url, path, params, timeout):
    """The only network call in this part. One request, no retries.

    Returns RAW BYTES rather than parsed JSON so that everything downstream —
    including the gate, which hands over bytes it typed out itself — travels
    the same road.
    """
    reply = requests.get(f"{base_url}{path}", params=params, timeout=timeout)
    reply.raise_for_status()
    return reply.content


def _why(exc):
    """A transport failure -> the words on his screen. **Each shape is named
    separately**: "the carry monitor is a bit broken" is not something anybody
    can act on, and a timeout and a 503 call for different reactions."""
    if isinstance(exc, requests.Timeout):
        return 'timed out'
    status = getattr(getattr(exc, 'response', None), 'status_code', None)
    if isinstance(status, int):
        return f'HTTP {status}'
    return 'unreachable'


def _rows(raw):
    """The raw reply -> the list Binance sent. Every way this can fail is a
    different, named refusal.

    MEASURED 2026-08-19, and both of these answer HTTP 200: a bogus symbol
    comes back as `[]`, and an illegal `limit` comes back as a JSON OBJECT
    carrying an error rather than a list at all.
    """
    if isinstance(raw, bytes):
        try:
            text = raw.decode('utf-8')
        except Exception:
            raise CarryError('unreadable reply')
    elif isinstance(raw, str):
        text = raw
    else:
        raise CarryError('the reply is not text')
    try:
        data = json.loads(text)
    except Exception:
        raise CarryError('unreadable reply')
    if not isinstance(data, list):
        raise CarryError('the reply is not a list')
    if len(data) < MIN_ROWS:
        raise CarryError('no rows')
    return data


def _rate(row):
    """One row -> its settled rate, as Decimal parsed from the RAW STRING.

    A float here would decide the rounding on the reader's behalf: the whale
    watch measured that 501 of the 10,001 four-decimal values a venue can send
    disagree between the float route and half-up.
    """
    if not isinstance(row, dict):
        raise CarryError('a row is not an object')
    if 'fundingRate' not in row:
        raise CarryError('no fundingRate field')
    try:
        rate = Decimal(str(row['fundingRate']).strip())
    except Exception:
        raise CarryError('fundingRate is not a number')
    if not rate.is_finite():
        raise CarryError('fundingRate is not a number')
    if abs(rate) > MAX_PLAUSIBLE_RATE:
        raise CarryError(f'a rate of {rate} is outside +/-{MAX_PLAUSIBLE_RATE}')
    return rate


def _stamp(row):
    """One row -> the millisecond stamp of the settlement it records."""
    if not isinstance(row, dict):
        raise CarryError('a row is not an object')
    if 'fundingTime' not in row:
        raise CarryError('no fundingTime field')
    try:
        return int(row['fundingTime'])
    except (TypeError, ValueError):
        raise CarryError('fundingTime is not a number')


def _window(rows, window):
    """The rows Binance sent -> exactly `window` settlements, proved to BE a
    window. Every refusal below is a named absence, never a quiet short
    average.

    Sorted by stamp rather than trusted by position: the venue happens to send
    oldest first, and a day it sent them the other way round would otherwise
    move the window without a word.
    """
    pairs = sorted((_stamp(row), _rate(row)) for row in rows)
    stamps = [stamp for stamp, _rate_ in pairs]
    if len(set(stamps)) != len(stamps):
        raise CarryError('the same settlement was sent twice')
    if len(pairs) < window:
        raise CarryError(f'only {len(pairs)} settled fundings, {window} asked '
                         f'for')
    pairs = pairs[-window:]
    for older, newer in zip(pairs, pairs[1:]):
        gap = newer[0] - older[0]
        if abs(gap - INTERVAL_MS) <= INTERVAL_TOL_MS:
            continue
        missing = int(round(gap / INTERVAL_MS)) - 1
        if missing >= 1:
            raise CarryError(f'{missing} settlement(s) missing from the window')
        raise CarryError('the settlements are not 8 hours apart')
    return pairs


def _average(pairs):
    """The mean settled rate over the window. Decimal from end to end."""
    return sum(rate for _stamp_, rate in pairs) / Decimal(len(pairs))


def _annual(average):
    """The average rate -> percent a year, SIMPLE and never compounded.

    Compounding assumes the proceeds are reinvested into the same trade, which
    is an assumption about the reader rather than a fact about the venue, so
    it is not made here and the line says which one it is.
    """
    return average * SETTLEMENTS_A_YEAR * 100


def _fmt(percent):
    """-0.1123... -> '-0.11%/yr (costs)'.

    The sign is decided from the ROUNDED figure, so an average that rounds to
    nought prints `0.00%/yr (flat)` and never the nonsense `-0.00%/yr`.
    """
    shown = percent.quantize(PLACES, rounding=ROUND_HALF_UP)
    if shown == 0:
        return f"0.00%/yr {FLAT_WORD}"
    if shown > 0:
        return f"+{shown}%/yr {EARNS_WORD}"
    return f"{shown}%/yr {COSTS_WORD}"


def _hhmm(stamp_ms):
    """A Binance millisecond stamp -> '08:00', always UTC."""
    return datetime.fromtimestamp(stamp_ms / 1000,
                                  timezone.utc).strftime('%H:%M')


def _stale(stamp_ms, now_ms, max_age_min):
    """Older than the limit -> stale. Compared in whole milliseconds so the
    boundary is exact: AT the limit a reading still counts, one millisecond
    past it does not."""
    return (now_ms - stamp_ms) > int(max_age_min * 60000)


def _no_data(reason):
    """A reading that did not happen, NAMED. Never a blank, never a dash."""
    return f"[no data: {reason}]"


def _asset_line(short, text):
    """One asset's row. **Printed even when its reading failed** — an asset
    that quietly disappears is B7's shape."""
    return f"    {short:<12}— {text}"


def _count_words(good, total):
    """How many assets actually answered. The denominator is the number
    ATTEMPTED, so an asset that vanished cannot flatter the count."""
    return f"{good} of {total} assets"


def _window_end(stamps):
    """The window's end stamp across the assets. The OLDEST is used: the
    newest would flatter it, letting one current asset make a stale one look
    current."""
    return min(stamps)


def _window_words(window):
    """The window, in the words on his screen. Named on the line so a single
    print can never masquerade as a rate that persists."""
    if window % 3 == 0:
        return f"{window // 3}d"
    return f"{window}x8h"


def _order(entries):
    """The assets in the order they were declared. THIS FUNCTION DOES NOTHING
    ON PURPOSE.

    Said plainly because it is code that exists for a test: the fixed order is
    a promise the Commander is invited to rely on — sorting the three by which
    pays most IS a recommendation — and a promise no check can reach is a
    promise nobody can keep. The drill replaces this with a sort by size and
    proves the gate refuses it.
    """
    return entries


def _read_one(base_url, symbol, window, timeout, now_ms, max_age_min, fetch):
    """One asset. Returns (text, window-end stamp) or raises CarryError with
    the words the Commander will read."""
    try:
        raw = fetch(base_url, FUNDING_PATH,
                    {'symbol': symbol, 'limit': window}, timeout)
    except CarryError:
        raise
    except Exception as exc:
        raise CarryError(_why(exc))
    pairs = _window(_rows(raw), window)
    newest = pairs[-1][0]
    if _stale(newest, now_ms, max_age_min):
        raise CarryError(f'stale, newest settlement {_hhmm(newest)} UTC, over '
                         f'{max_age_min} min old')
    return _fmt(_annual(_average(pairs))), newest


def section_text(base_url=None, symbols=None, window=None, timeout=None,
                 max_age_min=None, now=None, fetch=None):
    """The Carry Monitor block the Brief prints — this part's single doorway.

    Never raises and never prints; it RETURNS. Every input is resolved from
    None IN THE BODY rather than frozen into the signature at import time, so
    a caller can replace any of them and the module's own constants are read
    fresh on every call.
    """
    try:
        base_url = FAPI_BASE if base_url is None else base_url
        symbols = SYMBOLS if symbols is None else symbols
        window = WINDOW if window is None else window
        timeout = TIMEOUT if timeout is None else timeout
        max_age_min = MAX_AGE_MIN if max_age_min is None else max_age_min
        fetch = _get if fetch is None else fetch
        now_ms = (int(datetime.now(timezone.utc).timestamp() * 1000)
                  if now is None else int(now.timestamp() * 1000))

        entries, stamps, good = [], [], 0
        for short, symbol in symbols:
            try:
                text, stamp = _read_one(base_url, symbol, window, timeout,
                                        now_ms, max_age_min, fetch)
            except CarryError as exc:
                entries.append((short, _no_data(str(exc))))
            except Exception as exc:
                entries.append((short, _no_data(type(exc).__name__)))
            else:
                entries.append((short, text))
                stamps.append(stamp)
                good += 1

        label = f"Carry ({_window_words(window)})"
        head = f"  {label:<13}: {VENUE_WORDS} · {_count_words(good, len(symbols))}"
        if stamps:
            head += f" · window ends {_hhmm(_window_end(stamps))} UTC"
        lines = [head]
        for short, text in _order(entries):
            lines.append(_asset_line(short, text))
        lines.append(FOOT_METHOD)
        lines.append(f"   · the average of the last {window} SETTLED fundings "
                     f"({_window_words(window)}, three a day)")
        lines.append(f"     x {SETTLEMENTS_A_YEAR} a year · SIMPLE, not "
                     f"compounded")
        lines.append(FOOT_SIGN)
        lines.append(FOOT_IF)
        lines.extend(FOOT_COSTS)
        lines.extend(FOOT_RISK)
        lines.append(f"   — {FOOTER_TAIL}")
        return "\n".join(lines)
    except Exception as exc:
        return f"  \U0001f50c {OFFLINE_WORDS} ({type(exc).__name__})"
if __name__ == '__main__':
    if '--gate' not in sys.argv:
        print(section_text())
        print()
        print("--- drill: the exchange is unreachable, nothing else touched ---")
        print(section_text(base_url=OFFLINE_DRILL_URL, timeout=3))
        print()
        print("--- drill: every window years older than the staleness limit ---")
        print(section_text(now=datetime(2020, 1, 1, tzinfo=timezone.utc)))
        sys.exit(0)

    # =====================================================================
    # GATE 4.1 — declared in PROGRESS_LOG.md on 2026-08-18 (night) and
    # committed ALONE, with no .py file in that commit, BEFORE this file
    # existed. Commit 37738cf; `git show --stat 37738cf` is the proof the
    # bar came first.
    #
    # **THE SESSION THAT SET THIS BAR IS NOT THE SESSION THAT BUILT THIS
    # FILE.** That is the shape GATE 3.5 had, and GATE 3.5 is the bar that
    # held up best under attack, because not a word of it could be bent to
    # match what got built. Fourteen conditions and five design decisions,
    # none of them lowered, reinterpreted, or declared not to apply.
    #
    # Everything below lives inside `__main__` on purpose: the production
    # half above is untouched, and that is proved by a sha256 of the file's
    # prefix rather than asserted.
    # =====================================================================
    import http.server
    import math
    import os
    import re
    import shutil
    import socketserver
    import subprocess
    import tempfile
    import threading
    import time
    import urllib.parse
    from fractions import Fraction

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(good)
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def show(label, expected, got):
        print(f"     ---- the gate expected ({label}) ----")
        for line in expected.split('\n'):
            print(f"     {line!r}")
        print("     ---- the doorway returned ----")
        for line in got.split('\n'):
            print(f"     {line!r}")

    def same(label, expected, got):
        ok = expected == got
        if not ok:
            show(label, expected, got)
        return ok

    # ---- THE GATE'S OWN CLOCK AND THE GATE'S OWN BYTES -------------------
    # Nothing below asks the module to build anything the gate then judges.
    # The payloads are raw JSON text composed HERE, character by character,
    # in the shape Binance really sends — the rate as a STRING, the stamp as
    # an integer millisecond count — and handed over as BYTES.
    NOW = datetime(2026, 8, 19, 8, 5, tzinfo=timezone.utc)
    NOW_MS = int(NOW.timestamp() * 1000)
    END = int(datetime(2026, 8, 19, 8, 0, tzinfo=timezone.utc).timestamp() * 1000)
    STEP = 28800000              # eight hours, typed here, not read from the file
    MINUTE = 60000

    def payload(rates, end=END, step=STEP, symbol='GATE', stamps=None):
        """Rate strings, OLDEST FIRST -> the bytes Binance would send."""
        if stamps is None:
            n = len(rates)
            stamps = [end - (n - 1 - i) * step for i in range(n)]
        rows = []
        for rate, stamp in zip(rates, stamps):
            rows.append('{"symbol":"%s","fundingTime":%d,"fundingRate":"%s",'
                        '"markPrice":"64000.00000000","rateType":"Regular"}'
                        % (symbol, stamp, rate))
        return ('[' + ','.join(rows) + ']').encode('utf-8')

    def serve(table):
        """A transport answering from a table this gate typed out. A value
        that is an Exception is RAISED; anything else is returned as the
        reply. A missing key raises, which shows up as a changed block."""
        def fetch(base_url, path, params, timeout):
            answer = table[(path, params.get('symbol'))]
            if isinstance(answer, Exception):
                raise answer
            return answer
        return fetch

    ONE = (('BTC', 'BTCUSDT'),)          # a one-asset run, for the boundaries
    PATH = '/fapi/v1/fundingRate'        # typed here; R-014

    # ---------------------------------------------------------------- gold
    # BTC: 21 identical rates -> a clean average.
    # ETH: eleven of one and ten of another -> an average that is NOT any
    #      rate in the window, so a file that printed the newest, the oldest
    #      or the largest instead of the mean would be caught.
    # SOL: NEGATIVE throughout -> the carry COSTS, and the words must say so.
    BTC_RATES = ['0.00010000'] * 21
    ETH_RATES = ['0.00008000'] * 11 + ['0.00001000'] * 10
    SOL_RATES = ['-0.00002000'] * 21

    GOLD = {
        (PATH, 'BTCUSDT'): payload(BTC_RATES),
        (PATH, 'ETHUSDT'): payload(ETH_RATES),
        (PATH, 'SOLUSDT'): payload(SOL_RATES),
    }

    # The footer, TYPED OUT HERE character for character. The gate never
    # reads its expectation out of the file on trial (R-014).
    FOOT = (
        "  (long spot + SHORT the perp, delta-neutral — the two cancel out)\n"
        "   · the average of the last 21 SETTLED fundings (7d, three a day)\n"
        "     x 1095 a year · SIMPLE, not compounded\n"
        "   · plus = the carry EARNS it, minus = the carry COSTS it\n"
        "   · it pays this IF you run it — this is not advice to run it\n"
        "   · BEFORE costs: spot fee, perp fee, the spread, and capital tied\n"
        "     up on BOTH legs at once\n"
        "   · exchange counterparty risk · funding can flip negative at any\n"
        "     settlement\n"
        "   — information, not a signal)"
    )
    GOLD_EXPECTED = (
        '  Carry (7d)   : Binance USDT-perps · 3 of 3 assets · '
        'window ends 08:00 UTC\n'
        '    BTC         — +10.95%/yr (earns)\n'
        '    ETH         — +5.11%/yr (earns)\n'
        '    SOL         — -2.19%/yr (costs)\n'
        + FOOT
    )

    def gold(**kw):
        args = dict(fetch=serve(GOLD), now=NOW)
        args.update(kw)
        return section_text(**args)

    print("=" * 70)
    print("GATE 4.1 — THE CARRY MONITOR. Fourteen conditions, declared before")
    print("this file existed, by a session that did not build it.")
    print("=" * 70)

    print("\n(a) CONDITION 1 — ONE DOORWAY THAT NEVER RAISES AND NEVER PRINTS,"
          "\n    with every input resolved from None IN THE BODY. A default"
          "\n    frozen into the signature is read once at import and can"
          "\n    never be replaced by a caller — item 14 on the Commander's"
          "\n    desk, still open in two older files.")
    import inspect
    sig = inspect.signature(section_text)
    frozen = [name for name, p in sig.parameters.items()
              if p.default is not None and p.default is not inspect.Parameter.empty]
    mark(list(sig.parameters) == ['base_url', 'symbols', 'window', 'timeout',
                                  'max_age_min', 'now', 'fetch'],
         "the doorway takes exactly the seven inputs the gate expects",
         str(list(sig.parameters)))
    mark(not frozen,
         "and EVERY ONE of them defaults to None, resolved in the body",
         f"frozen defaults found: {frozen}")
    mark(isinstance(gold(), str), "the doorway RETURNS a string")

    print("\n(b) CONDITION 2 — EXACT EQUALITY ON BYTES THE GATE COMPOSED"
          "\n    ITSELF. The whole block, character for character, against a"
          "\n    copy typed out in this file. 'The words are present' is the"
          "\n    bar S14 walked straight through and it appears nowhere here.")
    mark(same('gold', GOLD_EXPECTED, gold()),
         "the healthy block matches the gate's own copy BYTE FOR BYTE")

    print("\n(c) >>> CONDITION 3 — THE ARITHMETIC, CHECKED BY A SECOND AND"
          "\n    GENUINELY DIFFERENT CALCULATION. The module works in"
          "\n    `Decimal`; this check works in exact RATIONAL arithmetic"
          "\n    (`fractions.Fraction`), which has no rounding at all until"
          "\n    the last step, and the two must agree to the printed digit."
          "\n    The helper under test is never called to judge itself.")

    def by_hand(rate_strings):
        """The whole sum, in exact rationals, rounded half-up at the end."""
        total = sum(Fraction(r) for r in rate_strings)
        annual = total / len(rate_strings) * 1095 * 100
        # half-up, away from zero, done on integers so nothing rounds twice
        sign = -1 if annual < 0 else 1
        cents = math.floor(abs(annual) * 100 + Fraction(1, 2))
        return sign * Fraction(cents, 100)

    for short, rates, want in (('BTC', BTC_RATES, '+10.95%/yr (earns)'),
                               ('ETH', ETH_RATES, '+5.11%/yr (earns)'),
                               ('SOL', SOL_RATES, '-2.19%/yr (costs)')):
        exact = by_hand(rates)
        printed = [l for l in gold().split('\n')
                   if l.startswith(f'    {short:<12}—')][0].split('— ')[1]
        number = Fraction(printed.split('%')[0].replace('+', ''))
        mark(number == exact and printed == want,
             f"{short}: the Brief's figure equals the gate's own exact "
             f"rational arithmetic",
             f"printed {printed!r}, by hand {float(exact):+.4f}%/yr")

    print("\n(d) >>> CONDITION 4 — THE SIGN. THE CONDITION THAT MATTERS MOST,"
          "\n    AND THE WORKED EXAMPLE IS WRITTEN OUT IN PLAIN WORDS SO A"
          "\n    READER WHO IS NOT A PROGRAMMER CAN CHECK IT:"
          "\n"
          "\n        Funding is POSITIVE."
          "\n        Positive funding means LONGS PAY SHORTS."
          "\n        The carry position is long spot and SHORT the perp."
          "\n        The short side RECEIVES the payment."
          "\n        Therefore a positive funding rate EARNS,"
          "\n        and the figure on the Brief must be a PLUS."
          "\n"
          "\n        Funding is NEGATIVE -> shorts pay longs -> the carry is"
          "\n        SHORT the perp, so it PAYS OUT -> it COSTS -> MINUS."
          "\n"
          "\n    Printing 'the carry pays 11%' when it in fact costs 11% is"
          "\n    the single worst thing this instrument can do, and no 'a"
          "\n    number appeared' check would ever catch it. So both"
          "\n    polarities are exercised, and the WORD is checked beside the"
          "\n    SIGN: a file that got the words right and the sign backwards"
          "\n    would be caught, and so would the reverse.")
    pos_line = [l for l in gold().split('\n') if l.startswith('    BTC')][0]
    neg_line = [l for l in gold().split('\n') if l.startswith('    SOL')][0]
    mark('+' in pos_line and '(earns)' in pos_line and '(costs)' not in pos_line,
         "POSITIVE funding (+0.0001 every 8h) prints a PLUS and the word "
         "(earns) — longs pay shorts, the carry is short, so it receives",
         pos_line.strip())
    mark('-' in neg_line and '(costs)' in neg_line and '(earns)' not in neg_line,
         "NEGATIVE funding (-0.00002 every 8h) prints a MINUS and the word "
         "(costs) — shorts pay longs, and the carry is the short",
         neg_line.strip())
    flip = {(PATH, 'BTCUSDT'): payload(['-0.00010000'] * 21),
            (PATH, 'ETHUSDT'): payload(ETH_RATES),
            (PATH, 'SOLUSDT'): payload(['0.00002000'] * 21)}
    flipped = section_text(fetch=serve(flip), now=NOW)
    mark('    BTC         — -10.95%/yr (costs)' in flipped
         and '    SOL         — +2.19%/yr (earns)' in flipped,
         "and with the SAME rates negated, both figures and both words turn "
         "over together — the sign is carried by the data, not by a habit",
         ' | '.join(l.strip() for l in flipped.split('\n')[1:4]))

    print("\n(e) >>> CONDITION 5 — THE WINDOW IS PROVED TO BE A WINDOW, AND"
          "\n    D1 IS THE BIGGEST HONESTY TRAP IN THIS INSTRUMENT: ONE"
          "\n    EIGHT-HOUR PRINT OF 0.05% BECOMES 54% A YEAR ON PAPER. A"
          "\n    single snapshot is never annualised; the average is taken"
          "\n    over settled fundings whose count and span are checked, and"
          "\n    the window is NAMED on the line the Commander reads.")
    mark('Carry (7d)' in gold() and '21 SETTLED fundings (7d, three a day)'
         in gold(),
         "the window is named TWICE on his screen — in the label and in the "
         "method line — so a shortened window cannot hide")

    SHORT_ROWS = {(PATH, 'BTCUSDT'): payload(['0.00010000'] * 20)}
    mark(section_text(fetch=serve(SHORT_ROWS), symbols=ONE, now=NOW).split('\n')[1]
         == '    BTC         — [no data: only 20 settled fundings, 21 asked for]',
         "TWENTY rows where twenty-one were asked for is a NAMED ABSENCE, "
         "never a quiet short average",
         section_text(fetch=serve(SHORT_ROWS), symbols=ONE,
                      now=NOW).split('\n')[1].strip())

    # A settlement missing from the middle: 21 rows spanning 22 slots.
    gap_stamps = [END - (21 - i) * STEP for i in range(21)]
    gap_stamps = [s for i, s in enumerate(gap_stamps) if i != 10] + [END]
    GAP_ROWS = {(PATH, 'BTCUSDT'): payload(['0.00010000'] * 21,
                                           stamps=sorted(gap_stamps))}
    mark(section_text(fetch=serve(GAP_ROWS), symbols=ONE, now=NOW).split('\n')[1]
         == '    BTC         — [no data: 1 settlement(s) missing from the window]',
         "a settlement MISSING from the middle of the window is named — the "
         "count is right, the span is wrong, and nothing else would notice",
         section_text(fetch=serve(GAP_ROWS), symbols=ONE,
                      now=NOW).split('\n')[1].strip())

    dup_stamps = [END - (20 - i) * STEP for i in range(21)]
    dup_stamps[5] = dup_stamps[6]
    DUP_ROWS = {(PATH, 'BTCUSDT'): payload(['0.00010000'] * 21,
                                           stamps=dup_stamps)}
    mark(section_text(fetch=serve(DUP_ROWS), symbols=ONE, now=NOW).split('\n')[1]
         == '    BTC         — [no data: the same settlement was sent twice]',
         "the SAME settlement sent twice is refused — it would silently "
         "double-weight one payment and no total would look wrong",
         section_text(fetch=serve(DUP_ROWS), symbols=ONE,
                      now=NOW).split('\n')[1].strip())

    # More rows than asked for: the NEWEST 21 are the window.
    MORE_ROWS = {(PATH, 'BTCUSDT'): payload(['0.00050000'] * 4
                                            + ['0.00010000'] * 21)}
    mark(section_text(fetch=serve(MORE_ROWS), symbols=ONE, now=NOW).split('\n')[1]
         == '    BTC         — +10.95%/yr (earns)',
         "TWENTY-FIVE rows -> the NEWEST twenty-one are the window; four "
         "older and much larger rates are outside it and change nothing",
         section_text(fetch=serve(MORE_ROWS), symbols=ONE,
                      now=NOW).split('\n')[1].strip())

    # Out of order: the venue sends oldest first today; a day it sent them
    # the other way round must not move the window.
    rev = json.loads(payload(['0.00008000'] * 11 + ['0.00001000'] * 10)
                     .decode('utf-8'))
    REV_ROWS = {(PATH, 'BTCUSDT'):
                json.dumps(list(reversed(rev))).encode('utf-8')}
    mark(section_text(fetch=serve(REV_ROWS), symbols=ONE, now=NOW).split('\n')[1]
         == '    BTC         — +5.11%/yr (earns)',
         "rows sent NEWEST FIRST give the identical answer — the window is "
         "taken by stamp, never by position in the list")

    print("\n(f) >>> CONDITION 6 — EVERY THRESHOLD AT THE EXACT VALUE WHERE IT"
          "\n    TURNS OVER, AND ONE STEP EITHER SIDE. R-054 paid for this"
          "\n    rule: GATE 3.4's staleness guard was exercised 26 days and a"
          "\n    year past its horizon and never once on the day it fires.")

    def one_asset(rates, now=NOW, **kw):
        table = {(PATH, 'BTCUSDT'): payload(rates)}
        return section_text(fetch=serve(table), symbols=ONE, now=now,
                            **kw).split('\n')[1]

    # -- the staleness limit, 600 minutes, to the millisecond
    fresh_at = datetime.fromtimestamp((END + 600 * MINUTE) / 1000, timezone.utc)
    stale_at = datetime.fromtimestamp((END + 600 * MINUTE + 1) / 1000,
                                      timezone.utc)
    just_in = datetime.fromtimestamp((END + 600 * MINUTE - 1) / 1000,
                                     timezone.utc)
    mark(one_asset(BTC_RATES, now=just_in).endswith('+10.95%/yr (earns)'),
         "at 599 min 59.999 s old the window still counts")
    mark(one_asset(BTC_RATES, now=fresh_at).endswith('+10.95%/yr (earns)'),
         "AT EXACTLY 600 MINUTES it still counts — the boundary is inclusive "
         "and that is a decision, not an accident")
    mark(one_asset(BTC_RATES, now=stale_at) ==
         '    BTC         — [no data: stale, newest settlement 08:00 UTC, '
         'over 600 min old]',
         "ONE MILLISECOND past it is STALE, refused WITH ITS OWN STAMP — "
         "Blockworks answered 200 with fifty beautiful stories 209 days old",
         one_asset(BTC_RATES, now=stale_at).strip())

    # -- the plausibility bound on a single rate, exactly at the cap
    mark(one_asset(['0.01000000'] * 21).endswith('+1095.00%/yr (earns)'),
         "a rate of EXACTLY the 0.01 bound is accepted (and annualises to an "
         "absurd figure, which is why the bound exists at all)",
         one_asset(['0.01000000'] * 21).strip())
    mark(one_asset(['0.01000001'] * 21) ==
         '    BTC         — [no data: a rate of 0.01000001 is outside '
         '+/-0.01]',
         "one hundred-millionth past it is refused BY NAME",
         one_asset(['0.01000001'] * 21).strip())

    # -- the gap tolerance, exactly 60 seconds of wobble
    def wobbled(extra):
        stamps = [END - (20 - i) * STEP for i in range(21)]
        stamps = [s if i < 10 else s + extra for i, s in enumerate(stamps)]
        table = {(PATH, 'BTCUSDT'): payload(['0.00010000'] * 21,
                                            stamps=stamps)}
        return section_text(fetch=serve(table), symbols=ONE,
                            now=datetime.fromtimestamp(
                                (END + extra + 5 * MINUTE) / 1000,
                                timezone.utc)).split('\n')[1]
    mark(wobbled(60000).endswith('%/yr (earns)'),
         "a settlement EXACTLY 60 s off its slot is still one window — the "
         "real wobble measured on Binance is five MILLISECONDS")
    mark(wobbled(60001) == '    BTC         — [no data: the settlements are '
                           'not 8 hours apart]',
         "one millisecond further out is refused BY NAME — and this check is "
         "the ONLY thing guarding the x1095 multiplier",
         wobbled(60001).strip())

    # -- the rounding rule, at an exact half-cent
    mark(one_asset(['0.00001000'] * 21) == '    BTC         — +1.10%/yr (earns)',
         "a rate of 0.00001 annualises to EXACTLY 1.095% — the half-cent "
         "turnover — and rounds HALF-UP to 1.10, never truncated to 1.09",
         one_asset(['0.00001000'] * 21).strip())
    mark(one_asset(['0.00000999'] * 21) == '    BTC         — +1.09%/yr (earns)'
         and one_asset(['0.00001001'] * 21) == '    BTC         — +1.10%/yr (earns)',
         "and one step either side of that turnover lands where it should")

    # -- the signed zero
    ZERO_RATES = ['0.00002000'] * 10 + ['-0.00002000'] * 10 + ['0.00000000']
    mark(one_asset(ZERO_RATES) == '    BTC         — 0.00%/yr (flat)',
         "a window that averages to nought prints `0.00%/yr (flat)` with NO "
         "sign — `-0.00%/yr` is nonsense on a screen and it never appears",
         one_asset(ZERO_RATES).strip())
    mark(_fmt(Decimal('-0.0049')) == '0.00%/yr (flat)'
         and _fmt(Decimal('0.0049')) == '0.00%/yr (flat)'
         and _fmt(Decimal('-0.005')) == '-0.01%/yr (costs)'
         and _fmt(Decimal('0.005')) == '+0.01%/yr (earns)',
         "and either side of the half-cent, a figure too small to show is "
         "FLAT while a figure that rounds to one hundredth keeps its sign")

    print("\n(g) CONDITION 7 — EVERY FAILURE NAMED SEPARATELY. SILENCE IS"
          "\n    FORBIDDEN. A timeout, an HTTP status, an unreadable reply, a"
          "\n    reply that is not a list, an empty list and a missing field"
          "\n    are SIX DIFFERENT NAMES, not one shrug. **MEASURED: a bogus"
          "\n    symbol really does answer HTTP 200 with `[]`, and an illegal"
          "\n    limit really does answer HTTP 200 with an error OBJECT.**")

    class _Resp:
        status_code = 503

    DEAD_A = {
        (PATH, 'BTCUSDT'): requests.HTTPError(response=_Resp()),
        (PATH, 'ETHUSDT'): requests.Timeout(),
        (PATH, 'SOLUSDT'): b'not json at all',
    }
    DEAD_A_EXPECTED = (
        '  Carry (7d)   : Binance USDT-perps · 0 of 3 assets\n'
        '    BTC         — [no data: HTTP 503]\n'
        '    ETH         — [no data: timed out]\n'
        '    SOL         — [no data: unreadable reply]\n'
        + FOOT
    )
    mark(same('dead A', DEAD_A_EXPECTED,
              section_text(fetch=serve(DEAD_A), now=NOW)),
         "three transports fail three ways and each is named — and EVERY "
         "asset keeps its row, which is B7's shape")

    DEAD_B = {
        (PATH, 'BTCUSDT'): b'{"status":"ERROR","errorData":"illegal params."}',
        (PATH, 'ETHUSDT'): b'[]',
        (PATH, 'SOLUSDT'): payload(BTC_RATES).replace(b'fundingRate',
                                                      b'fundingRateX'),
    }
    DEAD_B_EXPECTED = (
        '  Carry (7d)   : Binance USDT-perps · 0 of 3 assets\n'
        '    BTC         — [no data: the reply is not a list]\n'
        '    ETH         — [no data: no rows]\n'
        '    SOL         — [no data: no fundingRate field]\n'
        + FOOT
    )
    mark(same('dead B', DEAD_B_EXPECTED,
              section_text(fetch=serve(DEAD_B), now=NOW)),
         "and the three shapes that arrive wearing HTTP 200 — an error "
         "object, an empty list and a missing field — are named too")

    MIXED = {
        (PATH, 'BTCUSDT'): payload(BTC_RATES),
        (PATH, 'ETHUSDT'): payload(['0.00008000'] * 20),
        (PATH, 'SOLUSDT'): requests.Timeout(),
    }
    MIXED_EXPECTED = (
        '  Carry (7d)   : Binance USDT-perps · 1 of 3 assets · '
        'window ends 08:00 UTC\n'
        '    BTC         — +10.95%/yr (earns)\n'
        '    ETH         — [no data: only 20 settled fundings, 21 asked for]\n'
        '    SOL         — [no data: timed out]\n'
        + FOOT
    )

    def mixed(**kw):
        args = dict(fetch=serve(MIXED), now=NOW)
        args.update(kw)
        return section_text(**args)

    mark(same('mixed', MIXED_EXPECTED, mixed()),
         "one asset answering and two failing prints the truth about all "
         "three, and the count says 1 of 3 rather than flattering itself")

    print("\n(h) CONDITION 12 — THE CAVEATS ARE VERBATIM AND UNCONDITIONAL."
          "\n    Every run, not only when the number is large: exchange"
          "\n    counterparty risk, funding can flip negative, capital needed"
          "\n    on BOTH legs, and the figure is BEFORE costs. The line never"
          "\n    says 'do it'. F8 printed '>> strong buy signal' on the deck"
          "\n    of an information-only ship while its gate applauded.")
    # The offline block is fetched ONCE here and re-used by check (l): the
    # .invalid address cannot resolve, and three DNS failures are three real
    # waits.
    off = section_text(base_url=OFFLINE_DRILL_URL, timeout=3, now=NOW)
    EVERY_BLOCK = (gold(), mixed(), section_text(fetch=serve(DEAD_A), now=NOW),
                   off)
    for words in ("exchange counterparty risk",
                  "funding can flip negative at any",
                  "BEFORE costs: spot fee, perp fee, the spread",
                  "up on BOTH legs at once",
                  "SIMPLE, not compounded",
                  "it pays this IF you run it",
                  "   — information, not a signal)"):
        mark(all(words in block for block in EVERY_BLOCK),
             f"on the healthy, the degraded, the dead AND the offline block: "
             f"{words!r}")
    advice_words = ('buy', 'sell', 'should', 'recommend', 'opportunity',
                    'you should', 'do it', 'free money', 'guaranteed')
    lowered = gold().lower()
    mark(not any(w in lowered for w in advice_words),
         "and not one word of advice anywhere in the block",
         f"searched for {list(advice_words)}")

    print("\n(i) >>> D5 — FIXED ORDER, NEVER SORTED. Sorting the three by"
          "\n    which pays most IS a recommendation, however carefully the"
          "\n    words around it are chosen. The fixture below pays SOL most"
          "\n    and BTC least, so a file that ranked them would print them"
          "\n    in a visibly different order.")
    RANK = {
        (PATH, 'BTCUSDT'): payload(['0.00001000'] * 21),
        (PATH, 'ETHUSDT'): payload(['0.00005000'] * 21),
        (PATH, 'SOLUSDT'): payload(['0.00009000'] * 21),
    }

    def ranked(**kw):
        args = dict(fetch=serve(RANK), now=NOW)
        args.update(kw)
        return section_text(**args)

    order_now = [l.split('—')[0].strip() for l in ranked().split('\n')[1:4]]
    mark(order_now == ['BTC', 'ETH', 'SOL'],
         "the worst payer is still printed FIRST and the best LAST — the "
         "order is the declared one, not the interesting one",
         f"printed order {order_now}, by size it would be "
         f"{['SOL', 'ETH', 'BTC']}")

    print("\n(j) >>> CONDITION 4, SECOND HALF — THE INTERVAL IS PROVED"
          "\n    AGAINST AN INDEPENDENT BINANCE SURFACE. The x1095 stands"
          "\n    entirely on these contracts settling every EIGHT HOURS. If"
          "\n    one moved to four-hourly, the true annual figure would be"
          "\n    DOUBLE what the Brief prints and every digit on the screen"
          "\n    would still look healthy. So the venue is asked directly, on"
          "\n    a DIFFERENT endpoint from the one the instrument reads, and"
          "\n    the answer is compared to eight hours TYPED OUT HERE.")
    try:
        info = requests.get(FAPI_BASE + '/fapi/v1/fundingInfo',
                            timeout=15).json()
        by_symbol = {row['symbol']: row for row in info}
    except Exception as exc:
        by_symbol = {}
        print(f"        (the gate's own fundingInfo fetch failed: "
              f"{type(exc).__name__})")
    for _short, contract in SYMBOLS:
        row = by_symbol.get(contract)
        mark(row is not None and int(row['fundingIntervalHours']) == 8,
             f"{contract}: Binance's own fundingInfo says the funding "
             f"interval is EIGHT hours",
             f"{row.get('fundingIntervalHours') if row else 'NOT LISTED'} "
             f"hours, cap {row.get('adjustedFundingRateCap') if row else '?'}")
        cap = (Decimal(row['adjustedFundingRateCap']) if row else None)
        mark(cap is not None and cap < MAX_PLAUSIBLE_RATE,
             f"{contract}: and the venue's own cap is INSIDE this file's "
             f"plausibility bound, so the bound can never refuse a legitimate "
             f"reading",
             f"cap {cap}, bound {MAX_PLAUSIBLE_RATE}")
    mark(INTERVAL_MS == 8 * 60 * 60 * 1000 and SETTLEMENTS_A_YEAR == 1095
         and 1095 == 3 * 365,
         "and the file's own interval and multiplier agree with eight hours "
         "and three-a-day, both typed out in this gate",
         f"INTERVAL_MS={INTERVAL_MS}, x{SETTLEMENTS_A_YEAR}")

    print("\n(k) CONDITION 10 — DOOR 3, THE HALF NO IN-PROCESS CHECK CAN SEE."
          "\n    `brief.py` imports this file, so a single module-level print"
          "\n    lands on the Morning Brief ABOVE ITS HEADER, and a write"
          "\n    deferred to a thread or an atexit handler lands after the"
          "\n    verdict. **A FRESH INTERPRETER imports it, calls the doorway"
          "\n    three ways and SHUTS DOWN, and its TOTAL output must be"
          "\n    empty.** A timeout is a FAILURE, never a quiet pass.")
    GATE_MODULE_NAME = 'cockpit.carry'
    GATE_MODULE_LEAF = 'carry.py'
    GATE_DOOR3_PATHS = (
        "m.section_text(fetch=quiet)",
        "m.section_text(fetch=boom)",
        "m.section_text(base_url=m.OFFLINE_DRILL_URL, timeout=1)",
    )
    _ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    probe_dir = tempfile.mkdtemp(prefix='zarx_d3probe_')
    probe = os.path.join(probe_dir, 'seen.txt')
    body_src = ''.join('%s\nn += 1\n' % call for call in GATE_DOOR3_PATHS)
    child = ('import sys\n'
             'import %s as m\n' % GATE_MODULE_NAME +
             'def quiet(*a, **k):\n'
             "    return b'[]'\n"
             'def boom(*a, **k):\n'
             "    raise RuntimeError('no transport')\n"
             'n = 0\n' + body_src +
             "open(sys.argv[1], 'w', encoding='utf-8').write("
             'm.__file__ + chr(10) + str(n))\n')
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    started, timed_out, wrote, rc = time.time(), False, b'', None
    try:
        done = subprocess.run([sys.executable, '-c', child, probe],
                              cwd=_ROOT_DIR, env=env, capture_output=True,
                              timeout=90)
        wrote, rc = done.stdout + done.stderr, done.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        wrote = (exc.stdout or b'') + (exc.stderr or b'')
    elapsed = time.time() - started
    try:
        seen = open(probe, encoding='utf-8').read()
    except OSError:
        seen = ''
    shutil.rmtree(probe_dir, ignore_errors=True)
    parts = seen.split(chr(10))
    seen_file = parts[0] if parts else ''
    try:
        seen_n = int(parts[1])
    except (IndexError, ValueError):
        seen_n = -1
    mark(not timed_out, "the fresh interpreter SHUT DOWN on its own",
         f"{elapsed:.1f}s, return code {rc}")
    mark(os.path.basename(seen_file) == GATE_MODULE_LEAF
         and os.path.abspath(seen_file).startswith(os.path.abspath(_ROOT_DIR)),
         "the child imported THIS file — proved by a probe FILE, never by a "
         "stream, because the stream is the thing on trial",
         seen_file or '(the child wrote no probe)')
    mark(seen_n == len(GATE_DOOR3_PATHS),
         f"the child finished all {len(GATE_DOOR3_PATHS)} paths — a child "
         f"that stopped early is a FAILURE, not a pass on an empty stream",
         f"it reported {seen_n}")
    mark(rc == 0 and wrote == b'',
         "IMPORT, three doorway calls and SHUTDOWN wrote nothing at all",
         '' if wrote == b'' else
         f"it wrote {wrote.decode('utf-8', 'replace')[:200]!r}")

    print("\n(l) THE OFFLINE FAIL-SAFE (Law 3). The .invalid top-level domain"
          "\n    is reserved by the RFCs and can never resolve, so this drill"
          "\n    proves the fail-safe WITHOUT unplugging the Commander's"
          "\n    internet. Every asset fails the same way and each is named.")
    mark(off.count('[no data: unreachable]') == 3
         and off.startswith('  Carry (7d)   : Binance USDT-perps · '
                            '0 of 3 assets')
         and off.endswith('   — information, not a signal)'),
         "pointed at an address that cannot resolve, all three are NAMED "
         "unreachable and the caveats still print in full",
         off.split(chr(10))[0].strip())

    print("\n(m) CONDITION 3, LIVE — ONE REAL FETCH, AND UNLIKE EVERY OTHER"
          "\n    INSTRUMENT ON THIS SHIP IT IS JUDGED **EXACTLY**. The whale"
          "\n    watch allows a 1.0-point tolerance because positioning moves"
          "\n    between two calls seconds apart. **SETTLED FUNDING RATES ARE"
          "\n    HISTORICAL FACTS AND DO NOT MOVE**, so 'close' is not a pass"
          "\n    here: the gate fetches the same window itself, averages it in"
          "\n    exact rational arithmetic, and demands the identical digits."
          "\n    The plan's own sentence — 'matches the exchange's own"
          "\n    displayed funding within rounding' — is this check.")
    live = section_text()
    print()
    for line in live.split('\n'):
        print(f"      {line}")
    print()
    live_lines = live.split('\n')
    head_re = re.compile(r'^  Carry \(7d\)   : Binance USDT-perps · '
                         r'(\d) of 3 assets( · window ends \d{2}:\d{2} UTC)?$')
    head_match = head_re.match(live_lines[0])
    mark(head_match is not None,
         "the live header has the shape this gate expects",
         live_lines[0].strip())
    live_good = int(head_match.group(1)) if head_match else 0
    mark(live_good >= 1, f"at least one asset answered live — {live_good} did")
    mark(live_lines[-1] == '   — information, not a signal)',
         "the live block still carries the real disclaimer, verbatim",
         live_lines[-1])

    for short, contract in SYMBOLS:
        printed = [l for l in live_lines if l.startswith(f'    {short:<12}—')]
        printed = printed[0].split('— ')[1] if printed else ''
        if '[no data:' in printed:
            mark(False, f"{short} did not answer live — that is a FAILURE of "
                        f"this check, not a skip", printed)
            continue
        try:
            own = requests.get(FAPI_BASE + PATH,
                               params={'symbol': contract, 'limit': 21},
                               timeout=15).json()
            own_rates = [r['fundingRate'] for r in
                         sorted(own, key=lambda r: int(r['fundingTime']))]
            exact = by_hand(own_rates)
            shown = Fraction(printed.split('%')[0].replace('+', ''))
            mark(shown == exact,
                 f"{short}: THE FIGURE ON THE BRIEF EQUALS THE GATE'S OWN "
                 f"FETCH, AVERAGED IN EXACT RATIONALS — digit for digit, no "
                 f"tolerance",
                 f"the Brief says {printed!r}, the gate computes "
                 f"{float(exact):+.4f}%/yr from {len(own_rates)} settled "
                 f"rates")
            sign_agrees = (('(earns)' in printed and exact > 0)
                           or ('(costs)' in printed and exact < 0)
                           or ('(flat)' in printed and exact == 0))
            mark(sign_agrees,
                 f"{short}: and the WORD on the Brief agrees with the sign "
                 f"the gate computed independently — the worked example in "
                 f"(d), on today's real money",
                 printed)
        except Exception as exc:
            mark(False, f"{short}: the gate's own cross-check fetch failed — "
                        f"that is a FAILURE, not a skip",
                 f"{type(exc).__name__}: {exc}")

    print("\n(n) >>> CONDITION 9 — THE REAL TRANSPORT UNDER A CHECK FROM"
          "\n    BIRTH, NOT RETROFITTED. Every check above hands the doorway a"
          "\n    transport of the gate's own making, so `_get` — the four"
          "\n    lines that are the ONLY code in this file that speaks to"
          "\n    Binance — never runs. On 2026-08-18 two breaks inside the"
          "\n    whale watch's `_get` walked through a gate printing `100"
          "\n    checks, 0 red`. That is R-060, and THIS INSTRUMENT DOES NOT"
          "\n    GET TO REPEAT IT."
          "\n"
          "\n    So the gate stands up a server of its own on 127.0.0.1, on a"
          "\n    port the operating system picks, and calls the doorway with"
          "\n    `base_url` pointing at it and NO transport argument, so THE"
          "\n    REAL `_get` MAKES THE TRIP. The server writes down the path,"
          "\n    the symbol and the limit of every request, and the gate"
          "\n    compares that log to three tuples TYPED OUT HERE. **NOT ONE"
          "\n    REQUEST TO BINANCE IS MADE BY THIS CHECK.**")

    DOOR_EXPECT = (
        (PATH, 'BTCUSDT', '21'),
        (PATH, 'ETHUSDT', '21'),
        (PATH, 'SOLUSDT', '21'),
    )
    DOOR_BODY = dict(GOLD)
    DOOR_REFUSED = b'{"code":-1121,"msg":"the gate did not serve this"}'

    class _DoorHandler(http.server.BaseHTTPRequestHandler):
        """Answers ONLY what this gate typed out. Anything else gets a 500,
        which is the only thing here that exercises `raise_for_status`."""

        log = []

        def do_GET(self):
            split = urllib.parse.urlsplit(self.path)
            query = urllib.parse.parse_qs(split.query)

            def one(name):
                got = query.get(name, [''])
                return got[0] if got else ''

            _DoorHandler.log.append((split.path, one('symbol'), one('limit')))
            body = DOOR_BODY.get((split.path, one('symbol')))
            if body is None:
                self.send_response(500)
                body = DOOR_REFUSED
            else:
                self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            """Silent. The default writes every request to stderr, and Door 3
            listens at that descriptor."""

    door_server = socketserver.TCPServer(('127.0.0.1', 0), _DoorHandler)
    DOOR_URL = 'http://127.0.0.1:%d' % door_server.server_address[1]
    door_thread = threading.Thread(target=door_server.serve_forever,
                                   daemon=True)
    door_thread.start()

    # A proxy configured in the environment would send a request for
    # 127.0.0.1 out to the internet. Set here, inside the test, and put back
    # afterwards; the production half is not involved.
    _door_no_proxy = os.environ.get('NO_PROXY')
    os.environ['NO_PROXY'] = '127.0.0.1,localhost'

    def door_run():
        """The REAL `_get`, over a real socket, to a server this gate owns.
        Returns what was ASKED FOR beside what came BACK, because a check
        that saw only one of those halves would miss half of R-060."""
        _DoorHandler.log = []
        block = section_text(base_url=DOOR_URL, now=NOW)
        return tuple(_DoorHandler.log), block

    def door_refusal():
        """One asset the server does not serve, so it answers HTTP 500."""
        _DoorHandler.log = []
        return section_text(base_url=DOOR_URL, now=NOW,
                            symbols=(('BTC', 'NOTSERVEDUSDT'),)
                            ).split(chr(10))[1]

    DOOR_REFUSED_LINE = '    BTC         — [no data: HTTP 500]'

    door_log, door_block = door_run()
    mark(door_log == DOOR_EXPECT,
         "THE REAL `_get` WALKED TO A SERVER THIS GATE OWNS AND ASKED FOR "
         "EXACTLY THE RIGHT THREE THINGS — the settled-funding path, all "
         "three contracts in order, and a limit of 21, read off the wire "
         "rather than out of the module",
         f"{len(door_log)} requests recorded")
    if door_log != DOOR_EXPECT:
        for want, got in zip(DOOR_EXPECT, list(door_log) + [None] * 3):
            print(f"     wanted {want!r}")
            print(f"        got {got!r}")
    mark(same('through the real transport', GOLD_EXPECTED, door_block),
         "and the block it built from the answers matched the SAME copy the "
         "fake transport is held to, BYTE FOR BYTE — two roads, one "
         "destination")
    mark(door_refusal() == DOOR_REFUSED_LINE,
         "a request the server refuses comes back named `HTTP 500`, which "
         "exercises `raise_for_status` — W17 was INERT for want of this",
         door_refusal().strip())

    print("\n(o) >>> CONDITION 11 — THE SABOTAGE DRILL, INSTALLED FROM BIRTH"
          "\n    AND PERMANENT. Twenty breaks, every run, forever. Each is"
          "\n    captured honest and broken, and **ITS VERDICT COUNTS ONLY IF"
          "\n    THE TWO OBSERVABLES DIFFER.** A break that cannot change what"
          "\n    anyone reads is reported INERT and FAILS this gate — it is"
          "\n    not a caught lie, it is a check testing nothing. Two INERT"
          "\n    verdicts were thrown away on 2026-08-18 rather than counted."
          "\n    AND THE WITNESS IS PER-SABOTAGE: C8 returns a block that is"
          "\n    byte-identical to the honest one and prints advice beside it,"
          "\n    so it is witnessed AT THE FILE DESCRIPTOR.")

    _honest_section = section_text
    _honest_fmt = _fmt
    _honest_annual = _annual
    _honest_window = _window
    _honest_no_data = _no_data
    _honest_asset_line = _asset_line
    _honest_count = _count_words
    _honest_order = _order
    _honest_get = _get

    def w_gold():
        return gold()

    def j_gold():
        return gold() == GOLD_EXPECTED

    def w_mixed():
        return mixed()

    def j_mixed():
        return mixed() == MIXED_EXPECTED

    def w_ranked():
        return ranked()

    def j_ranked():
        return [l.split('—')[0].strip()
                for l in ranked().split('\n')[1:4]] == ['BTC', 'ETH', 'SOL']

    def w_dup():
        return section_text(fetch=serve(DUP_ROWS), symbols=ONE, now=NOW)

    def j_dup():
        return w_dup().split('\n')[1] == ('    BTC         — [no data: the '
                                          'same settlement was sent twice]')

    def w_gapped():
        return section_text(fetch=serve(GAP_ROWS), symbols=ONE, now=NOW)

    def j_gapped():
        return w_gapped().split('\n')[1] == ('    BTC         — [no data: 1 '
                                             'settlement(s) missing from the '
                                             'window]')

    def w_stale():
        return one_asset(BTC_RATES, now=stale_at)

    def j_stale():
        return w_stale() == ('    BTC         — [no data: stale, newest '
                             'settlement 08:00 UTC, over 600 min old]')

    def w_absurd():
        return one_asset(['0.01000001'] * 21)

    def j_absurd():
        return w_absurd() == ('    BTC         — [no data: a rate of '
                              '0.01000001 is outside +/-0.01]')

    def w_round():
        return one_asset(['0.00001000'] * 21)

    def j_round():
        return w_round() == '    BTC         — +1.10%/yr (earns)'

    def w_door():
        return door_run()

    def j_door():
        return door_run() == (DOOR_EXPECT, GOLD_EXPECTED)

    def w_refused():
        return door_refusal()

    def j_refused():
        return door_refusal() == DOOR_REFUSED_LINE

    # ---- the breaks themselves -------------------------------------------
    def _fmt_sign_flipped(percent):
        return _honest_fmt(-percent)

    def _fmt_words_swapped(percent):
        text = _honest_fmt(percent)
        return (text.replace('(earns)', '(TEMP)').replace('(costs)', '(earns)')
                .replace('(TEMP)', '(costs)'))

    def _fmt_truncated(percent):
        from decimal import ROUND_DOWN
        shown = percent.quantize(PLACES, rounding=ROUND_DOWN)
        if shown == 0:
            return f"0.00%/yr {FLAT_WORD}"
        if shown > 0:
            return f"+{shown}%/yr {EARNS_WORD}"
        return f"{shown}%/yr {COSTS_WORD}"

    def _annual_compounded(average):
        return ((1 + average) ** SETTLEMENTS_A_YEAR - 1) * 100

    def _window_unchecked(rows, window):
        return sorted((_stamp(r), _rate(r)) for r in rows)[-window:]

    def _no_data_silent(reason):
        return ''

    def _asset_line_drops(short, text):
        return '' if '[no data' in text else f"    {short:<12}— {text}"

    def _count_inflated(good, total):
        return f"{total} of {total} assets"

    def _order_sorted(entries):
        def size(entry):
            text = entry[1]
            try:
                return -float(text.split('%')[0].replace('+', ''))
            except ValueError:
                return 1e9
        return sorted(entries, key=size)

    def _shout(*a, **kw):
        print(">> the carry is free money, put it all on SOL")
        return _honest_section(*a, **kw)

    def _get_symbol_pinned(base_url, path, params, timeout):
        return _honest_get(base_url, path, dict(params, symbol='BTCUSDT'),
                           timeout)

    def _get_limit_pinned(base_url, path, params, timeout):
        return _honest_get(base_url, path, dict(params, limit=1), timeout)

    def _get_unchecked(base_url, path, params, timeout):
        reply = requests.get(f"{base_url}{path}", params=params,
                             timeout=timeout)
        return reply.content

    import io
    import contextlib

    def w_stdout():
        """Witnessed AT THE FILE DESCRIPTOR: C8's returned block is
        byte-identical to the honest one, so a drill that measured only the
        block would score it INERT and delete the only check that catches it.
        """
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            gold()
        return buf.getvalue()

    def j_silent():
        return w_stdout() == ''

    SABOTAGES = [
        ('C1 ', 'the SIGN flipped — the opposite of the truth',
         '_fmt', _fmt_sign_flipped, w_gold, j_gold),
        ('C2 ', 'earns and costs SWAPPED, the number left right',
         '_fmt', _fmt_words_swapped, w_gold, j_gold),
        ('C3 ', 'the window shortened to ONE settlement (D1)',
         'WINDOW', 1, w_gold, j_gold),
        ('C4 ', 'simple silently turned into COMPOUNDED (D3)',
         '_annual', _annual_compounded, w_gold, j_gold),
        ('C5 ', 'the multiplier changed from 1095 to 365',
         'SETTLEMENTS_A_YEAR', 365, w_gold, j_gold),
        ('C6 ', 'the COST warning quietly dropped (D4)',
         'FOOT_COSTS', ('', ''), w_gold, j_gold),
        ('C7 ', 'the RISK caveats reworded',
         'FOOT_RISK', ('   · some risk applies', ''), w_gold, j_gold),
        ('C8 ', 'ADVICE printed, the block byte-identical (S15, W10)',
         'section_text', _shout, w_stdout, j_silent),
        ('C9 ', 'the "not a signal" disclaimer reworded',
         'FOOTER_TAIL', 'information)', w_gold, j_gold),
        ('C10', 'the three assets SORTED by which pays most (D5)',
         '_order', _order_sorted, w_ranked, j_ranked),
        ('C11', 'a failed reading dropped SILENTLY (S10)',
         '_no_data', _no_data_silent, w_mixed, j_mixed),
        ('C12', 'an asset row dropped when its reading fails (B7)',
         '_asset_line', _asset_line_drops, w_mixed, j_mixed),
        ('C13', 'the asset count inflated to the total',
         '_count_words', _count_inflated, w_mixed, j_mixed),
        ('C14', 'the window checks switched off — duplicates accepted',
         '_window', _window_unchecked, w_dup, j_dup),
        ('C15', 'the 8-hour spacing check switched off (the x1095 premise)',
         'INTERVAL_TOL_MS', 10 ** 12, w_gapped, j_gapped),
        ('C16', 'the staleness guard switched off',
         'MAX_AGE_MIN', 10 ** 9, w_stale, j_stale),
        ('C17', 'the plausibility bound switched off',
         'MAX_PLAUSIBLE_RATE', Decimal('9'), w_absurd, j_absurd),
        ('C18', 'rounding truncated instead of half-up',
         '_fmt', _fmt_truncated, w_round, j_round),
        ('C19', 'the REAL transport pinned to one symbol (R-060)',
         '_get', _get_symbol_pinned, w_door, j_door),
        ('C20', 'the REAL transport shortening the window at the WIRE',
         '_get', _get_limit_pinned, w_door, j_door),
        ('C21', 'the REAL transport losing raise_for_status()',
         '_get', _get_unchecked, w_refused, j_refused),
    ]

    print()
    for tag, words, attr, repl, witness, judge in SABOTAGES:
        honest_obs = witness()
        original = globals()[attr]
        globals()[attr] = repl
        try:
            broken_obs = witness()
        except Exception:
            broken_obs = '<the sabotage crashed the witness>'
        try:
            survived = judge()
        except Exception:
            survived = False          # a crash is a catch: it did not pass
        finally:
            globals()[attr] = original
        changed = broken_obs != honest_obs
        caught = not survived
        good = changed and caught
        if not changed:
            verdict = 'INERT — IT CHANGED NOTHING, SO ITS VERDICT IS WORTHLESS'
        elif caught:
            verdict = 'CAUGHT'
        else:
            verdict = 'ESCAPED — THE GATE IS DECORATIVE'
        mark(good, f"{tag} {words:<56} -> {verdict}",
             '' if good else f"changed={changed} caught={caught}")

    print("\n    ... and the originals are proved RESTORED, not assumed. A"
          "\n    drill that left a break installed would hand the next check"
          "\n    a sabotaged module and call the result evidence.")
    mark(gold() == GOLD_EXPECTED and mixed() == MIXED_EXPECTED
         and ranked() == ranked() and w_stale() == (
             '    BTC         — [no data: stale, newest settlement 08:00 '
             'UTC, over 600 min old]')
         and one_asset(BTC_RATES) == '    BTC         — +10.95%/yr (earns)',
         "after twenty-one breaks and twenty-one repairs, every block is "
         "byte-identical to where it started")
    mark(section_text is _honest_section and _fmt is _honest_fmt
         and _annual is _honest_annual and _window is _honest_window
         and _no_data is _honest_no_data and _asset_line is _honest_asset_line
         and _count_words is _honest_count and _order is _honest_order
         and _get is _honest_get
         and WINDOW == 21 and SETTLEMENTS_A_YEAR == 1095
         and MAX_AGE_MIN == 600 and INTERVAL_TOL_MS == 60000
         and MAX_PLAUSIBLE_RATE == Decimal('0.01')
         and FOOTER_TAIL == 'information, not a signal)'
         and FOOT_COSTS == (
             "   · BEFORE costs: spot fee, perp fee, the spread, and capital "
             "tied",
             "     up on BOTH legs at once")
         and FOOT_RISK == (
             "   · exchange counterparty risk · funding can flip negative at "
             "any",
             "     settlement"),
         "every constant and every function this drill touched is back")

    # The gate owns this server, so the gate closes it.
    door_server.shutdown()
    door_server.server_close()
    door_thread.join(timeout=10)
    if _door_no_proxy is None:
        os.environ.pop('NO_PROXY', None)
    else:
        os.environ['NO_PROXY'] = _door_no_proxy
    mark(not door_thread.is_alive() and door_server.socket.fileno() == -1,
         "and the gate's own server was SHUT DOWN, its socket closed and its "
         "thread joined — a test that leaves a listener running is a test "
         "that changed the machine it ran on",
         f"thread alive: {door_thread.is_alive()}, socket fileno: "
         f"{door_server.socket.fileno()}")

    # ------------------------------------------------------------------
    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 4.1 PASSED — {len(nonlocal_ok)} checks, 0 red.

The whole printed block was rebuilt from bytes this gate composed
itself, in Binance's own shape, and matched a copy typed out here
CHARACTER FOR CHARACTER — healthy, one-of-three answering, nothing
answering six different ways, a window twenty rows long, a window
with a settlement missing from the middle, a window carrying the
same settlement twice, a window twenty-five rows long, and a window
sent newest-first.

THE SIGN — the thing this instrument can get most catastrophically
wrong — was proved on both polarities with the worked example
written out in plain words, and then again on today's real money:
the figure on the Brief equals a figure this gate fetched itself and
averaged in EXACT RATIONAL ARITHMETIC, digit for digit with no
tolerance at all. Settled funding rates are historical facts, so
"close" was never good enough here.

THE x1,095 MULTIPLIER STANDS ON THESE CONTRACTS SETTLING EVERY EIGHT
HOURS, so the venue was asked directly on a DIFFERENT endpoint —
/fapi/v1/fundingInfo — and it answered eight hours for all three,
beside caps that sit inside this file's own plausibility bound.

EVERY THRESHOLD WAS TESTED AT THE EXACT VALUE WHERE IT TURNS OVER
AND ONE STEP EITHER SIDE: the staleness limit at 599:59.999, exactly
600 minutes and one millisecond past; the plausibility bound at
exactly 0.01 and one hundred-millionth beyond; the spacing tolerance
at exactly 60 seconds and one millisecond beyond; the rounding rule
at an exact half-cent, 1.095%, and one step either side; and the
signed zero on both sides of nought.

THE REAL `_get` IS NOT TAKEN ON TRUST. It walked over a real socket
to a server this gate stood up itself, and BOTH halves were judged —
what it asked for, against three tuples typed out here, and what came
back, held to the same block the fake transport must produce. R-060
cost a whole session; C19, C20 and C21 run forever.

ALL TWENTY-ONE SABOTAGES WERE PROVED TO CHANGE WHAT SOMEBODY READS
BEFORE THEIR VERDICTS WERE COUNTED, each on the channel it really
affects — which is why C8, whose returned block is byte-identical to
the honest one, is witnessed at the FILE DESCRIPTOR.

WHAT THIS GATE DOES **NOT** PROVE, said here rather than in a
footnote. It cannot tell whether the carry is WORTH RUNNING: every
check above proves this file reports faithfully what the venue
published and does the arithmetic honestly, and no check anywhere
can prove a trade is a good idea. It says nothing about slippage,
about whether the spot and perp legs can be filled at the prices
shown, or about what an exchange failure would cost. **It is a
readout. It never ranks the three, it never says "do it", and it can
never occupy one of Phase 6's three slots, which are locked BY
NAME.**""")
    else:
        print(f"GATE 4.1 FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
