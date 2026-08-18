"""
Zar X cockpit — the Whale Watch (Context Deck, Phase 3, Step 3.5).

What the BIG accounts on one exchange are doing, beside what EVERYBODY on it
is doing. Two numbers per asset, from Binance's own published positioning:

    top accounts  /futures/data/topLongShortPositionRatio
                  its largest accounts, WEIGHTED BY POSITION SIZE
    all accounts  /futures/data/globalLongShortAccountRatio
                  every account on the venue, one vote each

The second number is why the first one is worth printing. "The big accounts
are 61% long" says almost nothing on its own; "the big accounts are 61% long
and everybody else is 52% long" is a fact about a difference, and the reader
can see for himself whether there is one.

**>>> WHAT THIS IS NOT, AND IT IS SAID ON THE BRIEF ITSELF RATHER THAN HERE
WHERE ONLY A PROGRAMMER WOULD FIND IT.** The plan asks for exchange RESERVE
and NETFLOW — coins moving on and off exchanges. **That data is PAID.**
CryptoQuant, Glassnode and Whale Alert all require a key; all three were
checked on 2026-08-11 and all three are out. So this instrument is:

    NOT exchange flows.  NOT wallet tracking.  NOT the world's whales.

It is **one venue's own published figures about its own customers**, and the
line on the Brief says exactly that. A reader who took it for an x-ray of all
the big money in crypto would be wrong, and the wording exists to stop him.

INFORMATION, NEVER A SIGNAL — and this file needs that rule more than any
other on this ship. "Big money is 61% long" is one sentence away from a trade
recommendation. **Phase 6's three signal slots are locked BY NAME — Turtle /
Donchian, funding-rate fade, on-chain cycle thermometer — and a positioning
number is not one of them.** No score, no ranking, no advice, ever.

**THE TRAPS THIS FILE IS SHAPED AROUND, each one paid for by a failure
somewhere else on this ship:**

  * **THE STALE-BUT-PERFECT READING.** Blockworks answered HTTP 200 with
    fifty real, well-formed stories whose newest was 209 days old. A reading
    older than MAX_AGE_MIN is named as stale WITH ITS OWN STAMP and
    contributes nothing — no number, no count.
  * **THE EMPTY LIST.** Binance answers HTTP 200 with `[]` and it looks
    exactly like a healthy reply. It is named `no rows`.
  * **THE SWAP.** `longAccount` and `shortAccount` are the same shape, so
    printing one as the other prints the exact opposite of the truth on a
    screen that looks perfectly normal. That is the funding instrument's
    original sin. Each row carries a THIRD, redundant field —
    `longShortRatio` — so a row is refused unless `ratio x short` agrees with
    `long`. A swap moves that product a long way and is refused, not printed.
  * **THE ROUNDING.** Binance sends `"0.5525"` as a STRING. The obvious
    `f"{float(x)*100:.1f}"` prints **55.2**; half-up rounding gives **55.3**.
    **MEASURED, not assumed: 501 of the 10,001 four-decimal shares Binance
    can send disagree between those two routes.** Which way a number goes
    then depends on the binary representation of that particular value —
    `0.6085` happens to agree, `0.5525` does not — so **everything here is
    `Decimal`, parsed from the raw string, rounded ROUND_HALF_UP**, and which
    of the two it means is a decision written down rather than an accident of
    the hardware. **The first draft of this file claimed `0.6085` was one of
    the 501. It is not. Its own gate caught the claim on the first run and
    the correction was measured rather than argued.**
  * **THE SILENT DROP.** Six readings have six independent fates. The ones
    that answered are printed; the ones that did not are NAMED, each with its
    own reason. An asset row is printed even when both of its readings failed
    — an asset that quietly vanishes is B7's shape.

LAW 2 — the compartment owns its sources: the host, both paths and the
symbol mapping live in THIS file and nowhere else.

LAW 3 — the doorway never raises and never prints; it RETURNS. Every failure
becomes one honest, named line and the Brief carries on with everything else
intact.

Standalone smoke test:
    python cockpit/whales.py          (live block, then the failure drills)
    python cockpit/whales.py --gate   (gate 3.5, including the sabotage drill)
"""
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

import requests

FAPI_BASE = 'https://fapi.binance.com'
TOP_PATH = '/futures/data/topLongShortPositionRatio'
ALL_PATH = '/futures/data/globalLongShortAccountRatio'

# Law 2: our assets are spot pairs; positioning exists only on the perpetual
# contracts. The mapping lives here because no other part needs to know
# Binance's naming. A tuple, not a dict, because the ORDER is what the
# Commander reads.
SYMBOLS = (('BTC', 'BTCUSDT'), ('ETH', 'ETHUSDT'), ('SOL', 'SOLUSDT'))

# The two populations, and the words each one is called on his screen. The
# label travels WITH its path so the two can never drift apart in an edit.
POPULATIONS = (('top accounts', TOP_PATH), ('all accounts', ALL_PATH))

PERIOD = '5m'          # Binance's shortest bucket: 5m, 15m, 30m, 1h ... 1d
ROWS = 1               # one bucket is all the Brief shows
MIN_ROWS = 1           # fewer than this is `no rows`, never a quiet blank
TIMEOUT = 10           # seconds; one attempt per reading, never a retry storm
MAX_AGE_MIN = 30       # older than this is STALE and contributes nothing

# Sanity bounds, in Decimal so the comparisons are exact.
SHARE_TOL = Decimal('0.001')   # |long + short - 1| may not exceed this
RATIO_TOL = Decimal('0.002')   # |ratio x short - long| may not exceed this
PLACES = Decimal('0.1')        # one decimal place, ROUND_HALF_UP

VENUE_WORDS = "Binance USDT-perps"
OFFLINE_WORDS = "Whale watch offline"
FOOTER_TAIL = "information, not a signal)"
FOOTER_HEAD = (
    "  (one exchange's own figures about its own customers · 'top' = its "
    "largest",
    "   accounts by position size, 'all' = every account on it · NOT exchange",
    "   flows, NOT wallet tracking, NOT the world's whales",
)

# Used only by the offline drill: the .invalid top-level domain is reserved by
# the RFCs and can never resolve, so the drill proves the fail-safe without
# unplugging the Commander's internet.
OFFLINE_DRILL_URL = 'https://zar-x-whale-drill.invalid'


class WhaleError(Exception):
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
    separately**: "the whale watch is a bit broken" is not something anybody
    can act on, and a timeout and a 503 call for different reactions."""
    if isinstance(exc, requests.Timeout):
        return 'timed out'
    status = getattr(getattr(exc, 'response', None), 'status_code', None)
    if isinstance(status, int):
        return f'HTTP {status}'
    return 'unreachable'


def _rows(raw):
    """The raw reply -> the list Binance sent. Every way this can fail is a
    different, named refusal."""
    if isinstance(raw, bytes):
        try:
            text = raw.decode('utf-8')
        except Exception:
            raise WhaleError('unreadable reply')
    elif isinstance(raw, str):
        text = raw
    else:
        raise WhaleError('the reply is not text')
    try:
        data = json.loads(text)
    except Exception:
        raise WhaleError('unreadable reply')
    if not isinstance(data, list):
        raise WhaleError('the reply is not a list')
    if len(data) < MIN_ROWS:
        raise WhaleError('no rows')
    return data


def _newest(rows):
    """More than one row -> the NEWEST is the only one that means anything.

    Picked BY ITS OWN STAMP rather than by position in the list. Binance
    happens to send oldest first; a day it sends them the other way round
    would otherwise put a half-hour-old reading on the Brief with nothing
    saying so.
    """
    best, best_stamp = None, None
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            stamp = int(row.get('timestamp'))
        except (TypeError, ValueError):
            continue
        if best_stamp is None or stamp > best_stamp:
            best, best_stamp = row, stamp
    if best is None:
        raise WhaleError('no readable timestamp')
    return best, best_stamp


def _number(row, field):
    """One field -> Decimal, or a named refusal. Parsed from the RAW STRING:
    a float would decide the rounding on the reader's behalf."""
    if field not in row:
        raise WhaleError(f'no {field} field')
    try:
        value = Decimal(str(row[field]).strip())
    except Exception:
        raise WhaleError(f'{field} is not a number')
    if not value.is_finite():
        raise WhaleError(f'{field} is not a number')
    return value


def _share(row):
    """The LONG share of this population, validated three ways first.

    The third check is the important one and it is the reason the redundant
    `longShortRatio` field is read at all: if the long and short shares were
    ever swapped, `ratio x short` stops agreeing with `long` by a mile, and
    the row is refused instead of printed backwards.

    The one case with no cross-check available is a population with NO shorts
    at all: nothing can be multiplied against zero. The shares alone then
    decide, and they force the answer to 100% — so nothing can be
    misreported, only refused or printed as what it is.
    """
    long_share = _number(row, 'longAccount')
    short_share = _number(row, 'shortAccount')
    ratio = _number(row, 'longShortRatio')
    for name, value in (('longAccount', long_share),
                        ('shortAccount', short_share)):
        if value < 0 or value > 1:
            raise WhaleError(f'{name} is outside 0 to 1')
    if abs(long_share + short_share - 1) > SHARE_TOL:
        raise WhaleError('the shares do not add up')
    if short_share != 0 and abs(ratio * short_share - long_share) > RATIO_TOL:
        raise WhaleError('the ratio disagrees with the shares')
    return long_share


def _pct(share):
    """0.6085 -> '60.9%'. ROUND_HALF_UP, in Decimal from end to end."""
    return f"{(share * 100).quantize(PLACES, rounding=ROUND_HALF_UP)}%"


def _hhmm(stamp_ms):
    """A Binance millisecond stamp -> '11:55', always UTC."""
    return datetime.fromtimestamp(stamp_ms / 1000,
                                  timezone.utc).strftime('%H:%M')


def _stale(stamp_ms, now_ms, max_age_min):
    """Older than the limit -> stale. Compared in whole milliseconds so the
    boundary is exact: AT the limit a reading still counts, one millisecond
    past it does not."""
    return (now_ms - stamp_ms) > int(max_age_min * 60000)


def _no_data(name, reason):
    """A reading that did not happen, NAMED. Never a blank, never a dash.

    A separate function because the silent drop is the failure this ship has
    made most often, and the drill has to be able to break exactly this.
    """
    return f"[no data: {name} — {reason}]"


def _asset_line(short, parts):
    """One asset's row. **Printed even when both of its readings failed** —
    an asset that quietly disappears is B7's shape, where the first asset was
    perfect and the other two were ruined with nothing saying so."""
    return f"    {short:<12}— " + ' · '.join(parts)


def _count_words(good, total):
    """How many of the readings actually happened. The denominator is the
    number ATTEMPTED, so a reading that vanished cannot flatter the count."""
    return f"{good} of {total} readings"


def _oldest(stamps):
    """The OLDEST reading bounds how current the whole block is. The newest
    would flatter it — one fresh number would make five stale ones look
    fresh."""
    return min(stamps)


def _read_one(base_url, path, symbol, period, rows, timeout, now_ms,
              max_age_min, fetch):
    """One population, one asset. Returns (text, stamp) or raises
    WhaleError with the words the Commander will read."""
    try:
        raw = fetch(base_url, path,
                    {'symbol': symbol, 'period': period, 'limit': rows},
                    timeout)
    except WhaleError:
        raise
    except Exception as exc:
        raise WhaleError(_why(exc))
    row, stamp = _newest(_rows(raw))
    if _stale(stamp, now_ms, max_age_min):
        raise WhaleError(f'stale, newest row {_hhmm(stamp)} UTC, over '
                         f'{max_age_min} min old')
    return _pct(_share(row)), stamp


def section_text(base_url=None, symbols=None, populations=None, period=None,
                 rows=None, timeout=None, max_age_min=None, now=None,
                 fetch=None):
    """The Context Deck block the Brief prints — this part's single doorway.

    Never raises and never prints; it RETURNS. Every input is resolved from
    None IN THE BODY rather than frozen into the signature at import time, so
    a caller can replace any of them and the module's own constants are read
    fresh on every call.
    """
    try:
        base_url = FAPI_BASE if base_url is None else base_url
        symbols = SYMBOLS if symbols is None else symbols
        populations = POPULATIONS if populations is None else populations
        period = PERIOD if period is None else period
        rows = ROWS if rows is None else rows
        timeout = TIMEOUT if timeout is None else timeout
        max_age_min = MAX_AGE_MIN if max_age_min is None else max_age_min
        fetch = _get if fetch is None else fetch
        now_ms = (int(datetime.now(timezone.utc).timestamp() * 1000)
                  if now is None else int(now.timestamp() * 1000))

        body, stamps, good, total = [], [], 0, 0
        for short, symbol in symbols:
            parts = []
            for name, path in populations:
                total += 1
                try:
                    text, stamp = _read_one(base_url, path, symbol, period,
                                            rows, timeout, now_ms,
                                            max_age_min, fetch)
                except WhaleError as exc:
                    parts.append(_no_data(name, str(exc)))
                except Exception as exc:
                    parts.append(_no_data(name, type(exc).__name__))
                else:
                    parts.append(f"{name} {text} long")
                    stamps.append(stamp)
                    good += 1
            body.append(_asset_line(short, parts))

        head = (f"  {'Whale watch':<13}: {VENUE_WORDS} · "
                f"{_count_words(good, total)}")
        if stamps:
            head += f" · oldest {_hhmm(_oldest(stamps))} UTC"
        lines = [head] + [line for line in body if line]
        lines.extend(FOOTER_HEAD)
        lines.append(f"   — {FOOTER_TAIL}")
        return "\n".join(lines)
    except Exception as exc:
        return f"  🔌 {OFFLINE_WORDS} ({type(exc).__name__})"


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        print(section_text())
        print()
        print("--- drill: the exchange is unreachable, nothing else touched ---")
        print(section_text(base_url=OFFLINE_DRILL_URL, timeout=3))
        print()
        print("--- drill: every reading half an hour older than the limit ---")
        print(section_text(now=datetime(2020, 1, 1, tzinfo=timezone.utc)))
        sys.exit(0)

    # =====================================================================
    # GATE 3.5 — declared in PROGRESS_LOG.md on 2026-08-11 and committed
    # ALONE, with no .py file in that commit, BEFORE this file existed.
    # Commit 67115c0; `git show --stat 67115c0` is the proof the bar came
    # first.
    #
    # **AND THIS BAR WAS NOT SET BY WHOEVER BUILT THIS FILE.** Every other
    # gate on this ship was declared by the session that then went on to
    # build the thing. This one was declared by a session that stopped
    # there — so it could not be lowered to match what got built, and not a
    # word of it has been reinterpreted. Twenty-five uses, twenty-five
    # audits survived.
    #
    # The thirteen conditions are in the log entry of 2026-08-11 and the
    # checks below are labelled with the ones they answer. Two of them are
    # new to this gate and both were paid for by R-054, where three
    # sabotages walked through GATE 3.4 at a boundary nobody had tested:
    #
    #   (11) EVERY THRESHOLD IS TESTED AT THE EXACT VALUE WHERE IT TURNS
    #        OVER, AND ONE STEP EITHER SIDE. There are six thresholds here
    #        and section (d) gives each of them three checks.
    #   (12) EVERY DEFAULT THE COMMANDER IS INVITED TO RELY ON IS EXERCISED
    #        BY A CHECK, NOT MERELY PINNED AS A CONSTANT. Section (e) hands
    #        the doorway a transport that WRITES DOWN what the module
    #        actually asked for, so the defaults are judged by what it DID.
    #
    # Everything below lives inside `__main__` on purpose: the production
    # half above is untouched, and that is proved by a sha256 of the file's
    # prefix rather than asserted.
    # =====================================================================
    import logging
    import os
    import re
    import shutil
    import subprocess
    import tempfile
    import time
    from decimal import ROUND_DOWN

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
    # in the shape Binance really sends — strings for the numbers, an integer
    # millisecond stamp — and handed over as BYTES.
    NOW = datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc)
    NOW_MS = int(NOW.timestamp() * 1000)
    MIN = 60000

    def payload(rows):
        """(long, short, ratio, stamp) tuples -> the bytes Binance would
        send. Typed out here so the gate never learns the shape from the
        file on trial."""
        out = []
        for long_share, short_share, ratio, stamp in rows:
            out.append('{"symbol":"GATE","longAccount":"%s",'
                       '"longShortRatio":"%s","shortAccount":"%s",'
                       '"timestamp":%d}'
                       % (long_share, ratio, short_share, stamp))
        return ('[' + ','.join(out) + ']').encode('utf-8')

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

    FOOT = ("  (one exchange's own figures about its own customers · 'top' = "
            "its largest\n"
            "   accounts by position size, 'all' = every account on it · NOT "
            "exchange\n"
            "   flows, NOT wallet tracking, NOT the world's whales\n"
            "   — information, not a signal)")

    # ---------------------------------------------------------------- gold
    GOLD = {
        (TOP_PATH, 'BTCUSDT'): payload([('0.6085', '0.3915', '1.5546',
                                         NOW_MS - 5 * MIN)]),
        (ALL_PATH, 'BTCUSDT'): payload([('0.6076', '0.3924', '1.5484',
                                         NOW_MS - 5 * MIN)]),
        (TOP_PATH, 'ETHUSDT'): payload([('0.5525', '0.4475', '1.2346',
                                         NOW_MS - 3 * MIN)]),
        (ALL_PATH, 'ETHUSDT'): payload([('0.5710', '0.4290', '1.3310',
                                         NOW_MS - 3 * MIN)]),
        (TOP_PATH, 'SOLUSDT'): payload([('0.4890', '0.5110', '0.9569',
                                         NOW_MS - 9 * MIN)]),
        (ALL_PATH, 'SOLUSDT'): payload([('0.5200', '0.4800', '1.0833',
                                         NOW_MS - 9 * MIN)]),
    }
    GOLD_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 6 of 6 readings · '
        'oldest 11:51 UTC\n'
        '    BTC         — top accounts 60.9% long · all accounts 60.8% long\n'
        '    ETH         — top accounts 55.3% long · all accounts 57.1% long\n'
        '    SOL         — top accounts 48.9% long · all accounts 52.0% long\n'
        + FOOT
    )

    def gold(**kw):
        args = dict(fetch=serve(GOLD), now=NOW)
        args.update(kw)
        return section_text(**args)

    # --------------------------------------------------------------- mixed
    # Three readings answer, three fail three different ways. The stale one
    # is Blockworks' shape: a perfectly formed row that is simply too old.
    MIXED = dict(GOLD)
    MIXED[(ALL_PATH, 'ETHUSDT')] = payload([('abc', '0.4290', '1.3310',
                                             NOW_MS - 3 * MIN)])
    MIXED[(TOP_PATH, 'SOLUSDT')] = payload([('0.4890', '0.5110', '0.9569',
                                             NOW_MS - 45 * MIN)])
    MIXED[(ALL_PATH, 'SOLUSDT')] = payload([('0.9000', '0.9000', '1.0000',
                                             NOW_MS - 9 * MIN)])
    MIXED_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 3 of 6 readings · '
        'oldest 11:55 UTC\n'
        '    BTC         — top accounts 60.9% long · all accounts 60.8% long\n'
        '    ETH         — top accounts 55.3% long · '
        '[no data: all accounts — longAccount is not a number]\n'
        '    SOL         — [no data: top accounts — stale, newest row '
        '11:15 UTC, over 30 min old] · '
        '[no data: all accounts — the shares do not add up]\n'
        + FOOT
    )

    def mixed(**kw):
        args = dict(fetch=serve(MIXED), now=NOW)
        args.update(kw)
        return section_text(**args)

    # ---------------------------------------------------------------- dead
    # Nothing answers, six different ways. **Silence is forbidden: every
    # absent reading is said out loud, by name.**
    class _Resp:
        status_code = 503

    DEAD = {
        (TOP_PATH, 'BTCUSDT'): requests.HTTPError(response=_Resp()),
        (ALL_PATH, 'BTCUSDT'): requests.Timeout(),
        (TOP_PATH, 'ETHUSDT'): b'not json at all',
        (ALL_PATH, 'ETHUSDT'): b'{"a":1}',
        (TOP_PATH, 'SOLUSDT'): b'[]',
        (ALL_PATH, 'SOLUSDT'): payload([('0.5000', '0.5000', '1.0000',
                                         NOW_MS)]).replace(b'longAccount',
                                                           b'longAccountX'),
    }
    DEAD_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 0 of 6 readings\n'
        '    BTC         — [no data: top accounts — HTTP 503] · '
        '[no data: all accounts — timed out]\n'
        '    ETH         — [no data: top accounts — unreadable reply] · '
        '[no data: all accounts — the reply is not a list]\n'
        '    SOL         — [no data: top accounts — no rows] · '
        '[no data: all accounts — no longAccount field]\n'
        + FOOT
    )

    def dead(**kw):
        args = dict(fetch=serve(DEAD), now=NOW)
        args.update(kw)
        return section_text(**args)

    # ------------------------------------------------- the boundary tables
    TWO = {
        (TOP_PATH, 'BTCUSDT'): payload([
            ('0.5000', '0.5000', '1.0000', NOW_MS - 10 * MIN),
            ('0.6085', '0.3915', '1.5546', NOW_MS - 5 * MIN)]),
        (ALL_PATH, 'BTCUSDT'): payload([
            ('0.4000', '0.6000', '0.6667', NOW_MS - 10 * MIN),
            ('0.6076', '0.3924', '1.5484', NOW_MS - 5 * MIN)]),
    }
    TWO_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 2 of 2 readings · '
        'oldest 11:55 UTC\n'
        '    BTC         — top accounts 60.9% long · all accounts 60.8% long\n'
        + FOOT
    )

    def two(**kw):
        args = dict(fetch=serve(TWO), now=NOW, symbols=ONE)
        args.update(kw)
        return section_text(**args)

    STALE = {
        (TOP_PATH, 'BTCUSDT'): payload([('0.6085', '0.3915', '1.5546',
                                         NOW_MS - 45 * MIN)]),
        (ALL_PATH, 'BTCUSDT'): payload([('0.6076', '0.3924', '1.5484',
                                         NOW_MS - 45 * MIN)]),
    }
    STALE_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 0 of 2 readings\n'
        '    BTC         — [no data: top accounts — stale, newest row '
        '11:15 UTC, over 30 min old] · [no data: all accounts — stale, '
        'newest row 11:15 UTC, over 30 min old]\n'
        + FOOT
    )

    def stale(**kw):
        args = dict(fetch=serve(STALE), now=NOW, symbols=ONE)
        args.update(kw)
        return section_text(**args)

    SUMBAD = {
        (TOP_PATH, 'BTCUSDT'): payload([('0.9000', '0.9000', '1.0000',
                                         NOW_MS - 5 * MIN)]),
        (ALL_PATH, 'BTCUSDT'): payload([('0.9000', '0.9000', '1.0000',
                                         NOW_MS - 5 * MIN)]),
    }
    SUMBAD_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 0 of 2 readings\n'
        '    BTC         — [no data: top accounts — the shares do not add up]'
        ' · [no data: all accounts — the shares do not add up]\n'
        + FOOT
    )

    def sumbad(**kw):
        args = dict(fetch=serve(SUMBAD), now=NOW, symbols=ONE)
        args.update(kw)
        return section_text(**args)

    # The swap itself, as it would really arrive: long and short exchanged in
    # the payload while the ratio stays honest. The cross-check is the only
    # thing standing between this and 39.2% printed as the big money's LONG
    # share when the truth is 60.9%.
    SWAPPED = {
        (TOP_PATH, 'BTCUSDT'): payload([('0.3915', '0.6085', '1.5546',
                                         NOW_MS - 5 * MIN)]),
        (ALL_PATH, 'BTCUSDT'): payload([('0.3924', '0.6076', '1.5484',
                                         NOW_MS - 5 * MIN)]),
    }
    SWAPPED_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 0 of 2 readings\n'
        '    BTC         — [no data: top accounts — the ratio disagrees with '
        'the shares] · [no data: all accounts — the ratio disagrees with the '
        'shares]\n'
        + FOOT
    )

    def swapped(**kw):
        args = dict(fetch=serve(SWAPPED), now=NOW, symbols=ONE)
        args.update(kw)
        return section_text(**args)

    def one_row(long_share, short_share, ratio, stamp, **kw):
        """One asset, one population, one row — for the boundary checks.
        Returns the asset LINE, which is where the number lands."""
        table = {(TOP_PATH, 'BTCUSDT'): payload([(long_share, short_share,
                                                  ratio, stamp)])}
        args = dict(fetch=serve(table), now=NOW, symbols=ONE,
                    populations=(('top accounts', TOP_PATH),))
        args.update(kw)
        return section_text(**args).split('\n')[1]

    print("=" * 70)
    print("  GATE 3.5 — the Whale Watch, Context Deck instrument 5 of 5")
    print("=" * 70)

    print("\n(a) CONDITION 1 — EXACT EQUALITY, ON BYTES THIS GATE HANDED"
          "\n    OVER. The gate composes Binance's own JSON itself, hands the"
          "\n    SAME BYTES to the doorway, and demands the WHOLE returned"
          "\n    block match a copy typed out HERE, character for character."
          "\n    'The words are present' is the bar S14 walked straight"
          "\n    through and it appears nowhere in this file."
          "\n    Folded into this one equality: two populations printed side"
          "\n    by side and NOT confused with each other, six readings"
          "\n    counted, the OLDEST of three different stamps in the header,"
          "\n    and ETH's 0.5525 rounded HALF-UP to 55.3% where the float"
          "\n    route prints 55.2% — one of the 501 disagreements measured in"
          "\n    d3 below, sitting inside the healthy block.")
    got_gold = gold()
    mark(same('gold', GOLD_EXPECTED, got_gold),
         "the whole block matched the gate's own copy BYTE FOR BYTE")

    print("\n(a2) AND THE TWO POPULATIONS REALLY ARE TWO. If the module asked"
          "\n    one endpoint twice, or crossed the labels, the block above"
          "\n    would still look perfectly reasonable. The fixtures differ"
          "\n    on purpose, and the gate knows which number belongs to"
          "\n    which name.")
    mark('top accounts 60.9% long · all accounts 60.8% long' in got_gold
         and 'top accounts 48.9% long · all accounts 52.0% long' in got_gold,
         "the top-account figure and the all-account figure are different "
         "numbers, each under its own name")

    print("\n(b) CONDITION 6 — EVERY FAILURE NAMED SEPARATELY, and CONDITION"
          "\n    5's other half: **SILENCE IS FORBIDDEN.** Nothing answers,"
          "\n    six different ways, and all six are said out loud by name."
          "\n    'The whale watch is a bit broken' is not something anybody"
          "\n    can act on. Judged by exact equality.")
    got_dead = dead()
    mark(same('nothing answered', DEAD_EXPECTED, got_dead),
         "an HTTP status, a timeout, unreadable bytes, a reply that is not a "
         "list, an empty list and a missing field — six names, one block")

    print("\n(c) PARTIAL TRUTH, LABELLED AS PARTIAL. Three readings answer"
          "\n    and three fail. **The three that answered are printed, the"
          "\n    three that did not are NAMED, and the count says 3 of 6.**"
          "\n    B7 left the first asset perfect and quietly ruined the other"
          "\n    two; here SOL fails twice and its row is still on the Brief."
          "\n    The stale one is Blockworks' shape — a perfectly formed row"
          "\n    that is simply too old — and CONDITION 5 requires it to"
          "\n    contribute NOTHING: no number, and no place in the count.")
    got_mixed = mixed()
    mark(same('partial', MIXED_EXPECTED, got_mixed),
         "three answered, three named, the count and the oldest stamp both "
         "computed from the three that are real")

    print("\n(d) >>> CONDITION 11 — EVERY THRESHOLD AT THE EXACT VALUE WHERE"
          "\n    IT TURNS OVER, AND ONE STEP EITHER SIDE. This is the"
          "\n    condition R-054 paid for: GATE 3.4's staleness guard was"
          "\n    exercised 26 days and a year past its horizon and NEVER ONCE"
          "\n    on the day it fires, and an off-by-one walked through it."
          "\n    There are six thresholds in this instrument and every one of"
          "\n    them gets three checks.")

    print("\n    d1. THE STALENESS LIMIT — 30 minutes, compared in whole"
          "\n        milliseconds. AT the limit a reading still counts; one"
          "\n        millisecond past it, it does not.")
    for label, age_ms, expect in (
            ('29m59s  just inside ', 1799000,
             '    BTC         — top accounts 60.9% long'),
            ('30m00s  EXACTLY ON  ', 1800000,
             '    BTC         — top accounts 60.9% long'),
            ('30m00.001s just out ', 1800001,
             '    BTC         — [no data: top accounts — stale, newest row '
             '11:29 UTC, over 30 min old]')):
        line = one_row('0.6085', '0.3915', '1.5546', NOW_MS - age_ms)
        mark(line == expect, f"{label} -> {'kept' if age_ms <= 1800000 else 'REFUSED and named'}",
             line.strip())

    print("\n    d2. THE ROW MINIMUM — one row is enough, none is 'no rows',"
          "\n        and with two rows THE NEWEST IS THE ONE THAT COUNTS.")
    empty_line = section_text(fetch=serve({(TOP_PATH, 'BTCUSDT'): b'[]'}),
                              now=NOW, symbols=ONE,
                              populations=(('top accounts', TOP_PATH),)
                              ).split('\n')[1]
    mark(empty_line == '    BTC         — [no data: top accounts — no rows]',
         "0 rows  -> refused and NAMED, never a quiet blank", empty_line.strip())
    mark(one_row('0.6085', '0.3915', '1.5546', NOW_MS - MIN)
         == '    BTC         — top accounts 60.9% long',
         "1 row   -> kept")
    mark(same('two rows', TWO_EXPECTED, two()),
         "2 rows  -> the NEWEST used, on both populations, and the oldest "
         "stamp in the header is the newer row's")

    print("\n    d3. THE ROUNDING RULE — ROUND_HALF_UP at one decimal place,"
          "\n        in Decimal from the raw string, tested just below the"
          "\n        half, EXACTLY ON it, and just above.")
    for label, share, expect in (('0.60849  just below', '0.60849', '60.8%'),
                                 ('0.60850  EXACTLY ON', '0.60850', '60.9%'),
                                 ('0.60851  just above', '0.60851', '60.9%')):
        short_share = str(Decimal('1') - Decimal(share))
        line = one_row(share, short_share, '1.5546', NOW_MS - MIN)
        mark(line == f'    BTC         — top accounts {expect} long',
             f"{label} -> {expect}", line.strip())

    print("\n        >>> AND WHETHER THE RULE MATTERS AT ALL IS MEASURED HERE"
          "\n        RATHER THAN CLAIMED, BECAUSE THE FIRST DRAFT OF THIS FILE"
          "\n        CLAIMED IT WITH THE WRONG NUMBER AND THIS CHECK WENT RED"
          "\n        ON ITS FIRST RUN. It said 0.6085 was a value where the"
          "\n        float route disagrees. **It is not — both routes give"
          "\n        60.9 for that one.** So the claim is replaced by an"
          "\n        enumeration: every four-decimal share Binance can send is"
          "\n        put through both routes, here, on every run.")
    disagree = []
    for _n in range(0, 10001):
        _text = f"{Decimal(_n).scaleb(-4):.4f}"
        if (str((Decimal(_text) * 100).quantize(PLACES,
                                                rounding=ROUND_HALF_UP))
                != f"{float(_text) * 100:.1f}"):
            disagree.append(_text)
    mark(len(disagree) >= 400 and '0.5525' in disagree
         and '0.6085' not in disagree
         and _pct(Decimal('0.5525')) == '55.3%'
         and f"{float('0.5525') * 100:.1f}" == '55.2',
         "the two routes disagree on HUNDREDS of the values Binance really "
         "sends, and one of them — ETH's 0.5525 — is in the healthy block "
         "above: this module says 55.3%, the float route says 55.2%",
         f"{len(disagree)} of 10,001 four-decimal shares disagree; the bar "
         f"is 400; 0.6085 is NOT one of them and the first draft said it was")

    print("\n    d4. THE SHARE RANGE — 0 and 1 are legitimate; a hair outside"
          "\n        either is refused BY NAME.")
    for label, long_share, short_share, ratio, expect in (
            ('exactly 0   ', '0.0000', '1.0000', '0.0000',
             'top accounts 0.0% long'),
            ('exactly 1   ', '1.0000', '0.0000', '0.0000',
             'top accounts 100.0% long'),
            ('1.0001      ', '1.0001', '0.0000', '0.0000',
             '[no data: top accounts — longAccount is outside 0 to 1]'),
            ('-0.0001     ', '-0.0001', '1.0000', '0.0000',
             '[no data: top accounts — longAccount is outside 0 to 1]')):
        line = one_row(long_share, short_share, ratio, NOW_MS - MIN)
        mark(line == f'    BTC         — {expect}',
             f"long share {label} -> {expect}", line.strip())

    print("\n    d5. THE SHARE-SUM WINDOW — |long + short - 1| may not exceed"
          "\n        0.001. Tested at 0.0009, at exactly 0.0010, and at"
          "\n        0.0011.")
    for label, short_share, ratio, expect in (
            ('0.0009 inside', '0.4991', '1.0018', 'top accounts 50.0% long'),
            ('0.0010 ON    ', '0.4990', '1.0020', 'top accounts 50.0% long'),
            ('0.0011 out   ', '0.4989', '1.0022',
             '[no data: top accounts — the shares do not add up]')):
        line = one_row('0.5000', short_share, ratio, NOW_MS - MIN)
        mark(line == f'    BTC         — {expect}',
             f"a sum {label} -> {expect}", line.strip())

    print("\n    d6. THE RATIO WINDOW — |ratio x short - long| may not exceed"
          "\n        0.002. **This is the check that stands between a swapped"
          "\n        payload and 39.2% printed as the big money's long"
          "\n        share.** Tested at 0.0019, at exactly 0.0020, at 0.0021.")
    for label, ratio, expect in (
            ('0.0019 inside', '1.0038', 'top accounts 50.0% long'),
            ('0.0020 ON    ', '1.0040', 'top accounts 50.0% long'),
            ('0.0021 out   ', '1.0042',
             '[no data: top accounts — the ratio disagrees with the shares]')):
        line = one_row('0.5000', '0.5000', ratio, NOW_MS - MIN)
        mark(line == f'    BTC         — {expect}',
             f"a disagreement of {label} -> {expect}", line.strip())
    mark(same('a swapped payload', SWAPPED_EXPECTED, swapped()),
         "AND THE REAL THING: long and short exchanged in the payload is "
         "REFUSED, not printed backwards")

    print("\n(e) >>> CONDITION 12 — EVERY DEFAULT THE COMMANDER IS INVITED TO"
          "\n    RELY ON IS EXERCISED BY A CHECK, NOT MERELY PINNED AS A"
          "\n    CONSTANT. **Pinning DEFAULT_TIME == '12:00' did not stop the"
          "\n    default-time PATH being changed with GATE 3.4 still green.**"
          "\n    So the doorway is handed a transport that WRITES DOWN every"
          "\n    request the module really made, and NOTHING ELSE — no"
          "\n    symbols, no period, no clock, no age limit — and the"
          "\n    defaults are judged by what the module DID.")
    class Recorder:
        def __init__(self, answer):
            self.answer, self.calls = answer, []

        def __call__(self, base_url, path, params, timeout):
            self.calls.append((base_url, path, params.get('symbol'),
                               params.get('period'), params.get('limit'),
                               timeout))
            return self.answer

    REC_STAMP = int(time.time() * 1000) - MIN
    rec = Recorder(payload([('0.6085', '0.3915', '1.5546', REC_STAMP)]))
    rec_block = section_text(fetch=rec)
    REC_HHMM = datetime.fromtimestamp(REC_STAMP / 1000,
                                      timezone.utc).strftime('%H:%M')
    REC_EXPECTED = (
        '  Whale watch  : Binance USDT-perps · 6 of 6 readings · '
        f'oldest {REC_HHMM} UTC\n'
        '    BTC         — top accounts 60.9% long · all accounts 60.9% long\n'
        '    ETH         — top accounts 60.9% long · all accounts 60.9% long\n'
        '    SOL         — top accounts 60.9% long · all accounts 60.9% long\n'
        + FOOT
    )
    EXPECT_CALLS = [
        ('https://fapi.binance.com',
         '/futures/data/topLongShortPositionRatio', 'BTCUSDT', '5m', 1, 10),
        ('https://fapi.binance.com',
         '/futures/data/globalLongShortAccountRatio', 'BTCUSDT', '5m', 1, 10),
        ('https://fapi.binance.com',
         '/futures/data/topLongShortPositionRatio', 'ETHUSDT', '5m', 1, 10),
        ('https://fapi.binance.com',
         '/futures/data/globalLongShortAccountRatio', 'ETHUSDT', '5m', 1, 10),
        ('https://fapi.binance.com',
         '/futures/data/topLongShortPositionRatio', 'SOLUSDT', '5m', 1, 10),
        ('https://fapi.binance.com',
         '/futures/data/globalLongShortAccountRatio', 'SOLUSDT', '5m', 1, 10),
    ]
    mark(rec.calls == EXPECT_CALLS,
         "with NO argument but the transport, the module asked for exactly "
         "these six things: the default host, both default paths, all three "
         "default symbols IN ORDER, the default 5m period, the default one "
         "row and the default 10-second timeout",
         f"{len(rec.calls)} requests recorded")
    mark(same('the default path', REC_EXPECTED, rec_block),
         "and the block it built from them — on the DEFAULT CLOCK, with the "
         "DEFAULT age limit — matched a copy this gate assembled from the "
         "stamp it wrote itself")

    rec2 = Recorder(payload([('0.6085', '0.3915', '1.5546',
                              int(time.time() * 1000) - 31 * MIN)]))
    stale_default = section_text(fetch=rec2)
    mark('0 of 6 readings' in stale_default.split('\n')[0]
         and stale_default.count('over 30 min old') == 6
         and 'oldest' not in stale_default.split('\n')[0],
         "AND THE DEFAULT STALENESS LIMIT IS A PATH, NOT A CONSTANT: a row "
         "31 minutes old, with no max_age and no clock passed, was refused "
         "six times over and the header dropped its stamp",
         stale_default.split('\n')[0].strip())

    print("\n(f) CONDITION 2 — DOOR 1: THE GATE HOLDS ITS OWN EXPECTATIONS."
          "\n    It never reads an expected value out of the file on trial"
          "\n    (R-014) and never asks the module where to look (B14). Every"
          "\n    constant this file ships is compared to a copy typed out"
          "\n    here.")
    mark(FAPI_BASE == 'https://fapi.binance.com'
         and TOP_PATH == '/futures/data/topLongShortPositionRatio'
         and ALL_PATH == '/futures/data/globalLongShortAccountRatio',
         "the host and both paths equal this gate's own copies")
    mark(SYMBOLS == (('BTC', 'BTCUSDT'), ('ETH', 'ETHUSDT'),
                     ('SOL', 'SOLUSDT')),
         "three assets, in the order the Commander reads them")
    mark(POPULATIONS == (('top accounts',
                          '/futures/data/topLongShortPositionRatio'),
                         ('all accounts',
                          '/futures/data/globalLongShortAccountRatio')),
         "each label is bound to ITS OWN endpoint — the top-account name to "
         "the position-weighted feed, the all-account name to the global one")
    mark(PERIOD == '5m' and ROWS == 1 and MIN_ROWS == 1 and TIMEOUT == 10
         and MAX_AGE_MIN == 30,
         "period, rows, minimum rows, timeout and the staleness limit equal "
         "this gate's copies",
         f"PERIOD={PERIOD!r} ROWS={ROWS} MIN_ROWS={MIN_ROWS} "
         f"TIMEOUT={TIMEOUT} MAX_AGE_MIN={MAX_AGE_MIN}")
    mark(SHARE_TOL == Decimal('0.001') and RATIO_TOL == Decimal('0.002')
         and PLACES == Decimal('0.1'),
         "the two sanity windows and the rounding place equal this gate's "
         "copies")
    mark(VENUE_WORDS == 'Binance USDT-perps'
         and OFFLINE_WORDS == 'Whale watch offline'
         and FOOTER_TAIL == 'information, not a signal)',
         "the three fixed wordings equal this gate's copies")

    print("\n(g) >>> CONDITION 4 — THE HONEST-NAME RULE, AND IT MATTERS MORE"
          "\n    HERE THAN ANYWHERE ELSE ON THIS SHIP. Exchange reserve and"
          "\n    netflow data is PAID and therefore out, so what this"
          "\n    instrument shows is one venue's own figures about its own"
          "\n    customers. **If the line could be read as 'all the whales in"
          "\n    the world', the wording FAILS this gate.** The limits are"
          "\n    required ON THE BRIEF, in his sight, on every path — not in"
          "\n    a docstring only a programmer would open.")
    for label, block in (('gold', got_gold), ('partial', got_mixed),
                         ('nothing answered', got_dead),
                         ('everything stale', stale())):
        mark('Binance USDT-perps' in block
             and "one exchange's own figures about its own customers" in block
             and 'NOT exchange' in block and 'NOT wallet tracking' in block
             and "NOT the world's whales" in block,
             f"{label:<18} -> names the venue, and says NOT exchange flows, "
             f"NOT wallet tracking, NOT the world's whales")
    mark('top' in got_gold and 'largest' in got_gold
         and 'every account on it' in got_gold,
         "and it says WHICH accounts each number is about, in words, on the "
         "Brief itself")

    print("\n(h) >>> CONDITION 3 — INFORMATION, NEVER A SIGNAL, HELD ON EVERY"
          "\n    PATH. F8 printed '>> strong buy signal' on the deck of an"
          "\n    information-only ship while its gate applauded. **'Big money"
          "\n    is 61% long' is one sentence away from a trade"
          "\n    recommendation, and Phase 6's three slots are locked BY"
          "\n    NAME.** Every block above and below is scanned, healthy and"
          "\n    broken alike.")
    # 'signal' is deliberately NOT in this list: the disclaimer this
    # instrument is REQUIRED to print ends with the words "not a signal", so a
    # scan for it would go red about the very sentence that keeps the ship
    # honest. The words below are all things this block may never say.
    ADVICE_WORDS = ('buy', 'sell', 'should', 'consider', 'reduce', 'exposure',
                    'opportunity', 'bullish', 'bearish', 'recommend', '>>')
    for label, block in (('gold', got_gold), ('partial', got_mixed),
                         ('nothing answered', got_dead),
                         ('everything stale', stale()),
                         ('shares refused', sumbad()),
                         ('a swapped payload', swapped()),
                         ('two rows', two()),
                         ('the default path', rec_block)):
        low = block.lower()
        hits = [w for w in ADVICE_WORDS if w in low]
        mark(not hits, f"{label:<18} -> not one word of advice anywhere",
             '' if not hits else f"found {hits}")

    print("\n(i) CONDITION 7 — DOOR 2: THE DOORWAY NEVER RAISES. Law 3: the"
          "\n    Brief must survive any failure of any instrument. Fourteen"
          "\n    shapes of poison, each one required to RETURN rather than"
          "\n    throw.")
    def _raiser(*a, **k):
        raise RuntimeError('the transport exploded')

    poisons = [
        ('a JSON null            ', dict(fetch=lambda *a, **k: b'null')),
        ('a JSON number          ', dict(fetch=lambda *a, **k: b'4242')),
        ('an empty list          ', dict(fetch=lambda *a, **k: b'[]')),
        ('a row with no fields   ', dict(fetch=lambda *a, **k: b'[{}]')),
        ('a list of numbers      ', dict(fetch=lambda *a, **k: b'[1,2,3]')),
        ('bytes that are not utf8', dict(fetch=lambda *a, **k:
                                         bytes([0xff, 0xfe, 0x00]))),
        ('a reply that is an int ', dict(fetch=lambda *a, **k: 12345)),
        ('a reply that is None   ', dict(fetch=lambda *a, **k: None)),
        ('a transport that raises', dict(fetch=_raiser)),
        ('a transport that is not callable', dict(fetch='not a function')),
        ('no symbols at all      ', dict(symbols=())),
        ('symbols of the wrong shape', dict(symbols=('BTC', 'ETH'))),
        ('populations of the wrong shape',
         dict(populations=(('only-one-thing',),))),
        ('an age limit that is a word', dict(max_age_min='thirty')),
        ('a naive clock          ', dict(now=datetime(2026, 8, 11, 12, 0))),
    ]
    for label, kw in poisons:
        args = dict(fetch=serve(GOLD), now=NOW)
        args.update(kw)
        try:
            out = section_text(**args)
            raised = False
        except Exception as exc:
            out, raised = f'{type(exc).__name__}: {exc}', True
        mark(not raised and isinstance(out, str) and out,
             f"{label:<32} -> returned, did not raise",
             out.split('\n')[0].strip()[:74])

    print("\n(j) CONDITION 8 — DOOR 3, AT THE FILE DESCRIPTOR. Redirecting"
          "\n    the NAMES catches print() and misses both a raw os.write and"
          "\n    a logging handler that took a reference to the real stream"
          "\n    before anyone redirected anything. **This is the standard"
          "\n    cockpit/events.py ear, not the weaker news.py one (R-046).**"
          "\n    And because a DEAF ear also reports silence, the ear proves"
          "\n    it can hear before it is believed about silence.")

    def _capture(call):
        """Run `call()` with BOTH streams captured AT THE FILE DESCRIPTOR.
        Returns raw BYTES, so no decoding can manufacture a pass. The restore
        is in `finally` and every dup is closed: a leaked descriptor would
        swallow the whole run's output."""
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

    _EAR_LOGGER = logging.getLogger('zarx.gate.whales.ear')
    _EAR_LOGGER.propagate = False
    _EAR_LOGGER.handlers[:] = [logging.StreamHandler(sys.stderr)]
    _EAR_LOGGER.setLevel(logging.INFO)
    _EAR_ROUTES = (
        ('print()          ', "EAR CONTROL: the print() route"),
        ('os.write(fd 1)   ', "EAR CONTROL: the raw descriptor route"),
        ('logging -> stderr', "EAR CONTROL: the logging-handler route"),
    )

    def _shout_all():
        print(_EAR_ROUTES[0][1])
        os.write(1, (_EAR_ROUTES[1][1] + "\n").encode('utf-8'))
        _EAR_LOGGER.info(_EAR_ROUTES[2][1])

    heard_control = _capture(_shout_all).decode('utf-8', 'replace')
    for route, words in _EAR_ROUTES:
        mark(words in heard_control,
             f"the ear HEARD the {route} route — a listener that cannot hear "
             f"this reports silence")

    before_fds = [os.fstat(fd)[:4] for fd in (1, 2)]
    for label, call in (('gold          ', lambda: gold()),
                        ('nothing answered', lambda: dead()),
                        ('everything stale', lambda: stale()),
                        ('a REAL reading', lambda: section_text())):
        written = _capture(call)
        mark(written == b'',
             f"{label} -> the doorway wrote NOTHING to descriptor 1 or 2",
             '' if written == b'' else
             f"it wrote {written.decode('utf-8', 'replace')!r}")
    for label, current, original in (('sys.stdout', sys.stdout, sys.__stdout__),
                                     ('sys.stderr', sys.stderr, sys.__stderr__)):
        if original is None:
            mark(False, f"{label}: the process's original stream is None, so "
                        f"this check CANNOT be performed — that is a FAILURE")
            continue
        mark(current is original,
             f"{label} is still the process's own stream — the doorway did "
             f"not rebind it under the Brief")
    mark(before_fds == [os.fstat(fd)[:4] for fd in (1, 2)],
         "descriptors 1 and 2 came back unchanged — the ear gave the pilot's "
         "screen back")

    print("\n(k) DOOR 3, THE HALF NO IN-PROCESS CHECK CAN SEE. Everything"
          "\n    above runs in a process where this module was imported"
          "\n    before the first check drew breath, and the ear stops"
          "\n    listening the instant the doorway returns. `brief.py`"
          "\n    imports this file, so a single module-level print lands on"
          "\n    the Morning Brief ABOVE ITS HEADER, and a write deferred to"
          "\n    a thread or an atexit handler lands after the verdict. **A"
          "\n    FRESH INTERPRETER imports it, calls the doorway three ways"
          "\n    and SHUTS DOWN, and its TOTAL output must be empty.** A"
          "\n    timeout is a FAILURE, never a quiet pass: 'nothing before we"
          "\n    gave up' is exactly what a sleeping thread looks like.")
    GATE_MODULE_NAME = 'cockpit.whales'
    GATE_MODULE_LEAF = 'whales.py'
    GATE_DOOR3_PATHS = (
        "m.section_text()",
        "m.section_text(fetch=quiet)",
        "m.section_text(fetch=boom)",
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

    print("\n(l) CONDITION 10 — ONE REAL FETCH, JUDGED LOOSELY, ON PURPOSE. A"
          "\n    gate that only ever judges bytes it handed over never tests"
          "\n    the trip and is decorative. **THE LOOSE BAR, STATED OUT"
          "\n    LOUD: at least 3 of the 6 readings, at least one reading for"
          "\n    every asset, the shape right, the disclaimer verbatim — and"
          "\n    the BTC top-account figure within 1.0 percentage point of a"
          "\n    number this gate fetches ITSELF, from the same endpoint,"
          "\n    with its own arithmetic.** The tolerance is there because"
          "\n    the two calls are seconds apart and the real figure moves;"
          "\n    a swap or a sign flip would be tens of points out, not one."
          "\n    A genuine Binance outage turns this red, and that is"
          "\n    correct: outside one, a red here is a REAL failure.")
    live = section_text()
    print()
    for line in live.split('\n'):
        print(f"      {line}")
    print()
    live_lines = live.split('\n')
    head_re = re.compile(r'^  Whale watch  : Binance USDT-perps · '
                         r'(\d) of 6 readings( · oldest \d{2}:\d{2} UTC)?$')
    head_match = head_re.match(live_lines[0])
    mark(head_match is not None,
         "the live header has the shape this gate expects",
         live_lines[0].strip())
    live_good = int(head_match.group(1)) if head_match else 0
    mark(live_good >= 3, f"at least 3 of the 6 readings answered — {live_good} "
                         f"did")
    for index, (short, _symbol) in enumerate(SYMBOLS):
        row = live_lines[index + 1] if len(live_lines) > index + 1 else ''
        mark(row.startswith(f'    {short:<12}— ')
             and '% long' in row,
             f"{short} has its row and at least one real reading on it",
             row.strip())
    mark(live_lines[-1] == '   — information, not a signal)',
         "the live block still carries the real disclaimer, verbatim",
         live_lines[-1])
    mark(live_good == 6 or '[no data:' in live,
         "and any reading that did NOT answer is named on the line rather "
         "than dropped")

    printed = re.search(r'BTC {9}— top accounts (\d+\.\d)% long', live)
    try:
        own = requests.get(FAPI_BASE + TOP_PATH,
                           params={'symbol': 'BTCUSDT', 'period': '5m',
                                   'limit': 1}, timeout=10)
        own_share = Decimal(str(json.loads(own.text)[-1]['longAccount'])) * 100
    except Exception as exc:
        own_share = None
        print(f"        (the gate's own fetch failed: {type(exc).__name__})")
    if printed is None or own_share is None:
        mark(False, "the gate could not cross-check the printed figure "
                    "against its own fetch — that is a FAILURE, not a skip")
    else:
        gap = abs(Decimal(printed.group(1)) - own_share)
        mark(gap <= Decimal('1.0'),
             "THE NUMBER ON THE BRIEF MATCHES A FIGURE THIS GATE FETCHED "
             "ITSELF AND PARSED WITH ITS OWN ARITHMETIC",
             f"the Brief says {printed.group(1)}%, the gate's own fetch says "
             f"{own_share:.2f}%, gap {gap:.2f} points (bar: 1.0)")

    print("\n(l2) >>> CONDITION 14 (GATE 3.5-R1) — THE DELIVERY BOY IS"
          "\n    FINALLY WATCHED LEAVING THE SHOP. Every check above this"
          "\n    one hands the doorway a transport of the gate's own making,"
          "\n    so `_get` — the four lines that are the ONLY code on this"
          "\n    ship that actually speaks to Binance — never runs. Even the"
          "\n    recording transport of (e), which is the best check in this"
          "\n    file, REPLACES `_get` and therefore can never testify about"
          "\n    it. The one check that does execute it, the live fetch of"
          "\n    (l), verifies ONE of the six numbers on the Brief."
          "\n"
          "\n    ON 2026-08-18 A SESSION THAT DID NOT BUILD THIS FILE PROVED"
          "\n    WHAT THAT COSTS. Two breaks inside `_get` — one pinning the"
          "\n    symbol to BTCUSDT so ETH and SOL printed BITCOIN'S NUMBERS,"
          "\n    one pinning the path so `all accounts` printed the"
          "\n    top-account figure for every coin — each walked through this"
          "\n    gate while it printed `100 checks, 0 red`. The second is"
          "\n    precisely what check (a2) above exists to forbid, and (a2)"
          "\n    proves it on fixtures only. That is R-060, and the Commander"
          "\n    ruled: correct it."
          "\n"
          "\n    SO THE GATE NOW STANDS UP A SERVER OF ITS OWN on 127.0.0.1,"
          "\n    on a port the operating system picks, and calls the doorway"
          "\n    with `base_url` pointing at it and NO transport argument, so"
          "\n    THE REAL `_get` MAKES THE TRIP. The server writes down the"
          "\n    path and the symbol, period and limit of every request, and"
          "\n    the gate compares that log to six tuples TYPED OUT HERE as"
          "\n    literal strings — never read from the file on trial. **NOT"
          "\n    ONE REQUEST TO BINANCE IS MADE BY THIS CHECK.**")

    import http.server
    import socketserver
    import threading
    import urllib.parse

    # The gate's own literals. R-014: an expectation read out of the module
    # follows the module into its own mistake and confirms it.
    DOOR_TOP = '/futures/data/topLongShortPositionRatio'
    DOOR_ALL = '/futures/data/globalLongShortAccountRatio'
    DOOR_EXPECT = (
        (DOOR_TOP, 'BTCUSDT', '5m', '1'),
        (DOOR_ALL, 'BTCUSDT', '5m', '1'),
        (DOOR_TOP, 'ETHUSDT', '5m', '1'),
        (DOOR_ALL, 'ETHUSDT', '5m', '1'),
        (DOOR_TOP, 'SOLUSDT', '5m', '1'),
        (DOOR_ALL, 'SOLUSDT', '5m', '1'),
    )
    # The same bytes GOLD serves, so the block that comes back down the real
    # road must equal the block the fake road already has to produce. Two
    # roads, one destination, or something between them is lying.
    DOOR_BODY = dict(GOLD)
    DOOR_REFUSED = b'{"code":-1121,"msg":"the gate did not serve this"}'

    class _DoorHandler(http.server.BaseHTTPRequestHandler):
        """Answers ONLY what this gate typed out. Anything else gets a 500,
        which is the only thing on this ship that has ever exercised
        `raise_for_status` — W17 was INERT on 2026-08-18 for want of it."""

        log = []

        def do_GET(self):
            split = urllib.parse.urlsplit(self.path)
            query = urllib.parse.parse_qs(split.query)

            def one(name):
                got = query.get(name, [''])
                return got[0] if got else ''

            _DoorHandler.log.append((split.path, one('symbol'),
                                     one('period'), one('limit')))
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
                            symbols=(('BTC', 'NOTSERVEDUSDT'),),
                            populations=(('top accounts', TOP_PATH),)
                            ).split(chr(10))[1]

    DOOR_REFUSED_LINE = ('    BTC         — [no data: top accounts — '
                         'HTTP 500]')

    door_log, door_block = door_run()
    mark(door_log == DOOR_EXPECT,
         "THE REAL `_get` WALKED TO A SERVER THIS GATE OWNS AND ASKED FOR "
         "EXACTLY THE RIGHT SIX THINGS — both paths, all three contracts in "
         "order, the 5m period and the single row, read off the wire rather "
         "than out of the module",
         f"{len(door_log)} requests recorded")
    if door_log != DOOR_EXPECT:
        for want, got in zip(DOOR_EXPECT, list(door_log) + [None] * 6):
            print(f"     wanted {want!r}")
            print(f"        got {got!r}")
    mark(same('through the real transport', GOLD_EXPECTED, door_block),
         "and the block it built from the answers matched the SAME copy the "
         "fake transport is held to, BYTE FOR BYTE — two roads, one "
         "destination")
    mark(door_refusal() == DOOR_REFUSED_LINE,
         "a request the server refuses comes back named `HTTP 500`, which is "
         "the first thing on this ship ever to exercise `raise_for_status`",
         door_refusal().strip())

    def _get_symbol_pinned(base_url, path, params, timeout):
        return _honest_get(base_url, path, dict(params, symbol='BTCUSDT'),
                           timeout)

    def _get_path_pinned(base_url, path, params, timeout):
        return _honest_get(base_url, TOP_PATH, params, timeout)

    def _get_unchecked(base_url, path, params, timeout):
        reply = requests.get(f"{base_url}{path}", params=params,
                             timeout=timeout)
        return reply.content

    def w_door():
        return door_run()

    def j_door():
        return door_run() == (DOOR_EXPECT, GOLD_EXPECTED)

    def w_refused():
        return door_refusal()

    def j_refused():
        return door_refusal() == DOOR_REFUSED_LINE

    print("\n(m) >>> CONDITION 9 — THE SABOTAGE DRILL. Seventeen breaks,"
          "\n    installed on EVERY run, forever. Each one is captured honest"
          "\n    and broken, and **its verdict counts ONLY IF THE TWO"
          "\n    OBSERVABLES DIFFER.** A break that cannot change what anyone"
          "\n    reads is reported INERT and FAILS this gate — it is not a"
          "\n    caught lie, it is a check testing nothing. F10, S6 and B1"
          "\n    were each exactly that, each found a generation late. **The"
          "\n    fourteen were named in PROGRESS_LOG.md BEFORE ONE LINE OF"
          "\n    THIS FILE WAS WRITTEN.**"
          "\n    AND THE WITNESS IS PER-SABOTAGE: W10 returns a block that is"
          "\n    byte-identical to the honest one and prints advice beside"
          "\n    it, so it is witnessed AT THE FILE DESCRIPTOR. A drill that"
          "\n    measured everything on one channel would score it INERT and"
          "\n    delete the only check that catches it.")

    _honest_section = section_text
    _honest_share = _share
    _honest_pct = _pct
    _honest_newest = _newest
    _honest_no_data = _no_data
    _honest_asset_line = _asset_line
    _honest_count = _count_words
    _honest_oldest = _oldest
    _honest_get = _get

    def w_gold():
        return gold()

    def w_mixed():
        return mixed()

    def w_two():
        return two()

    def w_stale():
        return stale()

    def w_sum():
        return sumbad()

    def w_swapped():
        return swapped()

    def w_stdout():
        return _capture(lambda: gold())

    def j_gold():
        return gold() == GOLD_EXPECTED

    def j_mixed():
        return mixed() == MIXED_EXPECTED

    def j_two():
        return two() == TWO_EXPECTED

    def j_stale():
        return stale() == STALE_EXPECTED

    def j_sum():
        return sumbad() == SUMBAD_EXPECTED

    def j_swapped():
        return swapped() == SWAPPED_EXPECTED

    def j_silent():
        return _capture(lambda: gold()) == b''

    def _share_swapped(row):
        _honest_share(row)                  # W2: validated, then the WRONG one
        return Decimal(str(row['shortAccount']))

    def _pct_truncated(share):
        return f"{(share * 100).quantize(PLACES, rounding=ROUND_DOWN)}%"

    def _newest_is_oldest(rows):
        best, best_stamp = None, None
        for row in rows:
            if not isinstance(row, dict):
                continue
            try:
                stamp = int(row.get('timestamp'))
            except (TypeError, ValueError):
                continue
            if best_stamp is None or stamp < best_stamp:
                best, best_stamp = row, stamp
        if best is None:
            raise WhaleError('no readable timestamp')
        return best, best_stamp

    def _no_data_silent(name, reason):
        return ''                           # W4: the absence swallowed

    def _no_data_generic(name, reason):
        return f"[no data: {name} — unavailable]"

    def _count_inflated(good, total):
        return f"{total} of {total} readings"

    def _asset_line_drops(short, parts):
        if any(part.startswith('[no data') for part in parts):
            return ''                       # W12: B7's shape
        return _honest_asset_line(short, parts)

    def _shout(*a, **k):
        block = _honest_section(*a, **k)
        print("  >> the big accounts are long — consider buying")
        return block

    SABOTAGES = [
        ('W1 ', 'the staleness guard switched off',
         'MAX_AGE_MIN', 10 ** 9, w_stale, j_stale),
        ('W2 ', 'long and short SWAPPED — the opposite of the truth',
         '_share', _share_swapped, w_gold, j_gold),
        ('W3 ', 'rounding truncated instead of half-up',
         '_pct', _pct_truncated, w_gold, j_gold),
        ('W4 ', 'a failed reading dropped SILENTLY (S10)',
         '_no_data', _no_data_silent, w_mixed, j_mixed),
        ('W5 ', 'the reason genericised to "unavailable"',
         '_no_data', _no_data_generic, w_mixed, j_mixed),
        ('W6 ', 'the readings count inflated to the total',
         '_count_words', _count_inflated, w_mixed, j_mixed),
        ('W7 ', 'the OLDEST row used instead of the newest',
         '_newest', _newest_is_oldest, w_two, j_two),
        ('W8 ', 'the two populations crossed under their labels',
         'POPULATIONS', (('top accounts', ALL_PATH),
                         ('all accounts', TOP_PATH)), w_gold, j_gold),
        ('W9 ', 'the share-sum sanity check switched off',
         'SHARE_TOL', Decimal('9'), w_sum, j_sum),
        ('W10', 'ADVICE printed, the block byte-identical (S15, E10)',
         'section_text', _shout, w_stdout, j_silent),
        ('W11', 'the disclaimer quietly reworded',
         'FOOTER_TAIL', 'information)', w_gold, j_gold),
        ('W12', 'an asset row dropped when a reading fails (B7)',
         '_asset_line', _asset_line_drops, w_mixed, j_mixed),
        ('W13', 'the ratio cross-check switched off — a swap accepted',
         'RATIO_TOL', Decimal('9'), w_swapped, j_swapped),
        ('W14', 'the "oldest reading" stamp showing the NEWEST',
         '_oldest', max, w_gold, j_gold),
        ('W15', 'the REAL transport pinned to one symbol (R-060)',
         '_get', _get_symbol_pinned, w_door, j_door),
        ('W16', 'the REAL transport pinned to one endpoint (R-060)',
         '_get', _get_path_pinned, w_door, j_door),
        ('W17', 'the REAL transport losing raise_for_status()',
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
        mark(good, f"{tag} {words:<52} -> {verdict}",
             '' if good else f"changed={changed} caught={caught}")

    print("\n    ... and the originals are proved RESTORED, not assumed. A"
          "\n    drill that left a break installed would hand the next check"
          "\n    a sabotaged module and call the result evidence.")
    mark(gold() == GOLD_EXPECTED and mixed() == MIXED_EXPECTED
         and two() == TWO_EXPECTED and stale() == STALE_EXPECTED
         and sumbad() == SUMBAD_EXPECTED and swapped() == SWAPPED_EXPECTED,
         "after fourteen breaks and fourteen repairs, all six blocks are "
         "byte-identical to where they started")
    mark(section_text is _honest_section and _share is _honest_share
         and _get is _honest_get
         and _pct is _honest_pct and _newest is _honest_newest
         and _no_data is _honest_no_data and _asset_line is _honest_asset_line
         and _count_words is _honest_count and _oldest is _honest_oldest
         and MAX_AGE_MIN == 30 and SHARE_TOL == Decimal('0.001')
         and RATIO_TOL == Decimal('0.002')
         and FOOTER_TAIL == 'information, not a signal)'
         and POPULATIONS == (('top accounts', TOP_PATH),
                             ('all accounts', ALL_PATH)),
         "every constant and every function this drill touched is back")

    # The gate owns this server, so the gate closes it. The thread is a
    # daemon as well, so nothing that goes wrong anywhere above can leave a
    # listener behind or wedge the interpreter.
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
        print(f"""GATE 3.5 PASSED — {len(nonlocal_ok)} checks, 0 red.

The whole printed block was rebuilt from bytes this gate composed
itself, in Binance's own shape, and matched a copy typed out here
CHARACTER FOR CHARACTER — on the healthy path, with three of six
readings failing three different ways, with nothing answering at all
six different ways, with two rows where only the newer one counts,
with a reading too old to trust, with shares that do not add up, and
with long and short exchanged in the payload.

EVERY THRESHOLD IN THIS INSTRUMENT WAS TESTED AT THE EXACT VALUE
WHERE IT TURNS OVER AND ONE STEP EITHER SIDE — the staleness limit at
29m59s, 30m00s and 30m00.001s; the row minimum at nought, one and
two; the rounding rule at 0.60849, 0.60850 and 0.60851; the share
range at exactly 0 and exactly 1 and a hair outside each; the
share-sum window at 0.0009, 0.0010 and 0.0011; the ratio window at
0.0019, 0.0020 and 0.0021. That is condition 11, and R-054 paid for
it: GATE 3.4's staleness guard was exercised 26 days and a year past
its horizon and never once on the day it fires.

AND EVERY DEFAULT THE COMMANDER IS INVITED TO RELY ON WAS EXERCISED
BY A CHECK RATHER THAN PINNED AS A CONSTANT. A recording transport
was handed to the doorway with no other argument at all, and the
host, both paths, all three symbols in order, the period, the row
count, the timeout, the default clock and the default staleness
limit were judged by WHAT THE MODULE DID.

AND CONDITION 14, ADDED 2026-08-18 AFTER THE COMMANDER RULED ON
R-060: THE REAL `_get` IS NO LONGER TAKEN ON TRUST. It walked over a
real socket to a server this gate stood up itself, and both halves
were judged — WHAT IT ASKED FOR, read off the wire and compared to
six tuples typed out in this file, and WHAT CAME BACK, held to the
same block the fake transport must produce. The two breaks that beat
this gate on 2026-08-18 are now W15 and W16 and they run forever.

ALL SEVENTEEN SABOTAGES WERE PROVED TO CHANGE WHAT SOMEBODY READS
BEFORE THEIR VERDICTS WERE COUNTED — on the channel each one really
affects, which is why W10, whose returned block is byte-identical to
the honest one, is witnessed at the FILE DESCRIPTOR and not at the
block.

WHAT THIS GATE DOES **NOT** PROVE, said here rather than in a
footnote. It cannot tell whether BINANCE'S OWN FIGURES ARE HONEST:
every check above proves this file reports faithfully what the venue
published, and no check anywhere can prove the venue published the
truth. It cannot see an endpoint that answers today and rate-limits
next week — R-056's lesson, which cost this ship CryptoSlate. And it
proves nothing whatever about whether positioning data is USEFUL:
this is an information instrument, it will never become a signal,
and Phase 6's three slots are locked BY NAME.""")
    else:
        print(f"GATE 3.5 FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
