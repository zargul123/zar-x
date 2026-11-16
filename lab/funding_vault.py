"""
Zar X Lab — THE FROZEN FUNDING (Phase 6, Gauntlet Slot 2).

**THE LAB TESTS ON FROZEN EVIDENCE ONLY.** The vault holds candles. Slot 2,
the funding-rate fade, also needs the funding rates Binance settled on its
perpetual contracts - so they are fetched ONCE, frozen in `lab/funding_vault/`
beside the vault, checksummed, and never refreshed. The rules were declared
in PROGRESS_LOG.md on 2026-11-16 (evening) and committed with no code,
before this file existed.

THIS FILE IS THE READING HALF. It verifies the freeze, loads it, and joins
a day's funding onto that day's candle. **IT HOLDS NO NETWORK CODE AT ALL**:
the one fetch lives in `lab/build_funding_vault.py`, which the gauntlet
never imports.

WHAT IS FROZEN: every settlement of BTCUSDT, ETHUSDT and SOLUSDT from
2023-07-28 00:00 UTC up to but not including 2026-07-26 00:00 UTC - the
1,094 days of the daily vault. Three settlements a day (00:00, 08:00,
16:00 UTC): 3,282 rows a coin. **A FREEZE OF ANY OTHER SHAPE IS REFUSED.**

**>>> THE HOLD-OUT'S FUNDING RATES ARE IN THOSE FILES. NOTHING IN THIS FILE
PRINTS A RATE.** It prints row counts, dates and checksums. How often the
hold-out was "extreme" is the trade count, and the trade count is a result.

THE JOIN'S RULE (the heart of Law 7 for this slot): a settlement belongs to
the daily candle whose UTC day contains it -

    candle opening time  <=  settlement time  <  opening time + 24 hours

A settlement stamped exactly at a candle's opening belongs to THAT candle
(24 hours before it closes). One stamped exactly at its close belongs to
the NEXT. So the last rate inside a day settled at 16:00, eight hours
before the candle closes, and nothing settled at or after the close is in
it. The day's funding is the three rates added up, as a whole number of
hundred-millionths (Binance prints eight decimals), so "equal" is exact.

RUN (from the zar-x folder):
    python lab/funding_vault.py            (verify the freeze: INTACT or not)
    python lab/funding_vault.py --gate     (GATE 6.3-D, on made-up settlements)
"""
import bisect
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
FUNDING_DIR = os.path.join(LAB_DIR, 'funding_vault')
MANIFEST_NAME = 'MANIFEST.json'
ATTRIBUTES_NAME = '.gitattributes'
HEADER = 'funding_time_ms,funding_rate'

CONTRACTS = {'BTC-USD': 'BTCUSDT', 'ETH-USD': 'ETHUSDT', 'SOL-USD': 'SOLUSDT'}
FIRST_DAY = '2023-07-28'       # the daily vault's first candle
LAST_DAY = '2026-07-25'        # and its last
DAYS = 1094
SETTLEMENTS_A_DAY = 3
ROWS = 3282                    # 1,094 x 3
DAY_MS = 86_400_000
MARK_MS = 28_800_000           # a settlement every eight hours
SLACK_MS = 1000                # how late after its mark one may be stamped
MAX_RATE = Decimal('0.05')     # cockpit/funding.py's MAX_PLAUSIBLE_RATE
UNITS = 100_000_000            # hundred-millionths: eight decimals


def day_ms(text):
    """'2023-07-28' -> the millisecond its UTC day begins. No local clock."""
    stamp = datetime.strptime(text, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    return int(stamp.timestamp()) * 1000


FIRST_MS = day_ms(FIRST_DAY)
END_MS = day_ms(LAST_DAY) + DAY_MS      # not included


def rate_units(text):
    """Binance's rate text -> a whole number of hundred-millionths.
    Refuses anything that is not a plain number of at most eight decimals,
    and anything larger than 5% either way."""
    try:
        rate = Decimal(str(text).strip())
    except InvalidOperation:
        raise ValueError(f'a funding rate that is not a number: {text!r}')
    if not rate.is_finite():
        raise ValueError(f'a funding rate that is not a number: {text!r}')
    if abs(rate) > MAX_RATE:
        raise ValueError('a funding rate larger than 5%')
    units = rate * UNITS
    if units != units.to_integral_value():
        raise ValueError('a funding rate with more than eight decimals')
    return int(units)


def check_rows(rows, first_ms=None, days=None):
    """The one shape a freeze may have. `rows` is [(time_ms, rate_text)].
    Raises ValueError naming the first fault; never prints a rate."""
    first_ms = FIRST_MS if first_ms is None else first_ms
    days = DAYS if days is None else days
    owed = days * SETTLEMENTS_A_DAY
    if len(rows) != owed:
        raise ValueError(f'{len(rows)} settlements where exactly {owed} are '
                         f'owed ({days} days x {SETTLEMENTS_A_DAY})')
    for position, (stamp, rate) in enumerate(rows):
        mark = first_ms + position * MARK_MS
        late = int(stamp) - mark
        if not 0 <= late <= SLACK_MS:
            raise ValueError(
                f'settlement {position + 1} is stamped {late} ms from its '
                f'8-hour mark: a day with a settlement missing, added or '
                f'off the clock')
        rate_units(rate)


def csv_bytes(rows):
    lines = [HEADER] + [f'{int(stamp)},{rate}' for stamp, rate in rows]
    return ('\n'.join(lines) + '\n').encode('ascii')


def read_rows(path):
    """A frozen file -> [(time_ms, rate_text)]."""
    with open(path, 'rb') as handle:
        lines = handle.read().decode('ascii').split('\n')
    if lines[0] != HEADER or lines[-1] != '':
        raise ValueError(f'{os.path.basename(path)} is not a frozen funding '
                         f'file')
    rows = []
    for line in lines[1:-1]:
        stamp, rate = line.split(',')
        rows.append((int(stamp), rate))
    return rows


def _sha(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def write_freeze(directory, rows_by_contract, note='', first_ms=None,
                 days=None):
    """Write a freeze: one file a contract, the manifest, and the line that
    tells git not to touch a byte. REFUSES if anything is already there.
    The builder calls this once for the real freeze; the gates call it in
    temporary folders with made-up settlements."""
    if os.path.isdir(directory) and os.listdir(directory):
        raise RuntimeError(f'REFUSED: {directory} already holds a freeze. '
                           f'Frozen funding is never rebuilt or refreshed.')
    for contract, rows in rows_by_contract.items():
        check_rows(rows, first_ms, days)
    os.makedirs(directory, exist_ok=True)
    files = {}
    for contract, rows in rows_by_contract.items():
        name = f'{contract}_funding.csv'
        path = os.path.join(directory, name)
        with open(path, 'xb') as handle:
            handle.write(csv_bytes(rows))
        files[name] = {'contract': contract, 'rows': len(rows),
                       'first_time_ms': int(rows[0][0]),
                       'last_time_ms': int(rows[-1][0]),
                       'bytes': os.path.getsize(path), 'sha256': _sha(path)}
    manifest = {
        'what': 'Binance USD-M perpetual funding rates, as settled',
        'source': '/fapi/v1/fundingRate',
        'note': note,
        'first_day': FIRST_DAY, 'last_day': LAST_DAY,
        'law': 'These files are evidence. They are never modified, never '
               'refreshed, only verified.',
        'files': files,
    }
    with open(os.path.join(directory, MANIFEST_NAME), 'x', encoding='utf-8',
              newline='\n') as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write('\n')
    with open(os.path.join(directory, ATTRIBUTES_NAME), 'x', encoding='ascii',
              newline='\n') as handle:
        handle.write('# Checksummed evidence. Git must not touch a byte.\n'
                     '* -text\n')
    return manifest


def verify(directory=None, rows_owed=None):
    """Is the freeze exactly what its manifest says? -> (ok, lines).
    Checksums, byte counts, row counts and the list of files. No rate is
    parsed and none is printed."""
    directory = FUNDING_DIR if directory is None else directory
    rows_owed = ROWS if rows_owed is None else rows_owed
    lines, ok = [], True
    try:
        with open(os.path.join(directory, MANIFEST_NAME),
                  encoding='utf-8') as handle:
            files = json.load(handle)['files']
        present = sorted(os.listdir(directory))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return False, [f'NO READABLE FREEZE in {directory} '
                       f'({type(exc).__name__})']
    owed = sorted(f'{contract}_funding.csv' for contract in CONTRACTS.values())
    if sorted(files) != owed:
        ok = False
        lines.append(f'the manifest lists {sorted(files)}, not {owed}')
    extra = sorted(set(present) - set(owed) - {MANIFEST_NAME, ATTRIBUTES_NAME})
    if extra:
        ok = False
        lines.append(f'files that are not in the manifest: {extra}')
    for name in owed:
        entry = files.get(name)
        path = os.path.join(directory, name)
        if not isinstance(entry, dict) or not os.path.isfile(path):
            ok = False
            lines.append(f'{name}: MISSING')
            continue
        same = (_sha(path) == entry.get('sha256')
                and os.path.getsize(path) == entry.get('bytes')
                and entry.get('rows') == rows_owed)
        ok = ok and same
        lines.append(f'{name}: {entry.get("rows")} rows, '
                     f'{"checksum matches" if same else "DOES NOT MATCH"}')
    return ok, lines


def load(asset, directory=None, first_ms=None, days=None):
    """One coin's frozen settlements -> (times_ms, units), two lists.
    The file's checksum is verified against the manifest first, and its
    shape checked again, on every load."""
    directory = FUNDING_DIR if directory is None else directory
    name = f'{CONTRACTS[asset]}_funding.csv'
    path = os.path.join(directory, name)
    with open(os.path.join(directory, MANIFEST_NAME),
              encoding='utf-8') as handle:
        entry = json.load(handle)['files'][name]
    if _sha(path) != entry['sha256']:
        raise RuntimeError(f'REFUSED: {name} does not match its checksum.')
    rows = read_rows(path)
    check_rows(rows, first_ms, days)
    return ([int(stamp) for stamp, _rate in rows],
            [rate_units(rate) for _stamp, rate in rows])


def preflight(directory=None, first_ms=None, days=None, rows_owed=None):
    """EVERYTHING THAT CAN BE REFUSED BEFORE A SLOT IS SPENT. Verifies the
    whole freeze and loads all three coins. -> {asset: (times, units)}.
    Raises RuntimeError('REFUSED ...') on any fault."""
    ok, lines = verify(directory, rows_owed)
    if not ok:
        raise RuntimeError('REFUSED: the frozen funding is not intact - '
                           + '; '.join(lines))
    try:
        return {asset: load(asset, directory, first_ms, days)
                for asset in CONTRACTS}
    except (OSError, ValueError, KeyError) as exc:
        raise RuntimeError(f'REFUSED: the frozen funding cannot be read - '
                           f'{type(exc).__name__}: {exc}')


def _owner(opens, stamp):
    """Which candle owns a settlement: the LAST one that opened at or
    before it. (Exactly at an opening -> that candle, not the one ending.)"""
    return bisect.bisect_right(opens, stamp) - 1


def daily_funding(opens_ms, times_ms, units):
    """Each candle's funding, on plain integers.

    opens_ms : the candles' opening times, rising, one day apart
    -> one float a candle: the sum of its three settlements in whole
       hundred-millionths, or NaN if it does not hold exactly three.
    """
    sums = [0] * len(opens_ms)
    counts = [0] * len(opens_ms)
    for stamp, value in zip(times_ms, units):
        at = _owner(opens_ms, stamp)
        if at >= 0 and stamp < opens_ms[at] + DAY_MS:
            sums[at] += int(value)
            counts[at] += 1
    return [float(total) if count == SETTLEMENTS_A_DAY else float('nan')
            for total, count in zip(sums, counts)]


def attach(df, times_ms, units):
    """Daily candles + one coin's settlements -> A COPY of the candles with
    one more column, `funding`. Refuses candles that are not exactly one
    day apart: the rule above is written for the UTC day and nothing else."""
    import pandas as pd
    epoch = pd.Timestamp('1970-01-01')
    opens = [int(value) for value in
             (df.index - epoch) // pd.Timedelta(milliseconds=1)]
    steps = {b - a for a, b in zip(opens, opens[1:])}
    if steps - {DAY_MS} or any(value % DAY_MS for value in opens):
        raise ValueError('REFUSED: funding is joined to DAILY candles that '
                         'open at 00:00 UTC, one day apart, and to nothing '
                         'else')
    out = df.copy()
    out['funding'] = daily_funding(opens, times_ms, units)
    return out


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        ok, lines = verify()
        print('FROZEN FUNDING — lab/funding_vault/')
        for line in lines:
            print('   ' + line)
        if ok:
            try:
                loaded = preflight()
                print(f'   every file: {DAYS} days x {SETTLEMENTS_A_DAY} '
                      f'settlements, {FIRST_DAY} to {LAST_DAY}, on the clock')
            except RuntimeError as exc:
                ok = False
                print(f'   {exc}')
        print(f'FROZEN FUNDING {"INTACT" if ok else "NOT INTACT"} — '
              f'{sum("checksum matches" in line for line in lines)} of '
              f'{len(CONTRACTS)}')
        sys.exit(0 if ok else 1)

    # =====================================================================
    # GATE 6.3-D — THE FROZEN FUNDING: THE FETCH, THE FREEZE, THE VERIFIER
    # AND THE JOIN. Declared in PROGRESS_LOG.md on 2026-11-16 (evening) and
    # committed with no code, before this file existed.
    #
    # **IT NEVER TOUCHES THE NETWORK, THE REAL FROZEN FOLDER OR THE VAULT.**
    # Every settlement below is made up, and every freeze is written into a
    # temporary folder. It also gates `lab/build_funding_vault.py`, whose
    # server is replaced by a fake one.
    # =====================================================================
    import math
    import shutil
    import tempfile

    import pandas as pd

    sys.path.insert(0, LAB_DIR)
    import build_funding_vault as builder

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def held(function, *args, **kwargs):
        """A call's answer, or the name of what it raised."""
        try:
            return function(*args, **kwargs)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>'

    def refusal(function, *args, **kwargs):
        """What a call refuses with, or '' if it does not refuse."""
        try:
            function(*args, **kwargs)
        except Exception as exc:                           # noqa: BLE001
            return f'{type(exc).__name__}: {exc}'
        return ''

    REAL_BEFORE = (sorted(os.listdir(FUNDING_DIR))
                   if os.path.isdir(FUNDING_DIR) else None)
    WORK = tempfile.mkdtemp(prefix='zarx_funding_')
    T0 = day_ms('2030-01-01')          # made-up days, far from any real one

    def made_up(days, salt=0, first_ms=T0):
        """`days` x 3 made-up settlements, a few ms late like real ones."""
        rows = []
        for n in range(days * 3):
            cents = ((n * 37 + salt * 11) % 41) - 12     # -12 .. 28
            rows.append((first_ms + n * MARK_MS + (n * 7) % 30,
                         f'{cents / 100000:.8f}'))
        return rows

    def changed(rows, at, stamp=None, rate=None):
        rows = list(rows)
        rows[at] = (rows[at][0] if stamp is None else stamp,
                    rows[at][1] if rate is None else rate)
        return rows

    TEN = made_up(10)

    print("=" * 70)
    print("GATE 6.3-D — THE FROZEN FUNDING. Made-up settlements only; no")
    print("network, no real freeze, no vault.")
    print("=" * 70)

    print("\n(a) THE DECLARED SHAPE, typed out here.")
    mark((FIRST_DAY, LAST_DAY, DAYS, SETTLEMENTS_A_DAY, ROWS, DAY_MS, MARK_MS,
          SLACK_MS, str(MAX_RATE), UNITS)
         == ('2023-07-28', '2026-07-25', 1094, 3, 3282, 86400000, 28800000,
             1000, '0.05', 100000000)
         and ROWS == DAYS * SETTLEMENTS_A_DAY
         and FIRST_MS == 1690502400000 and END_MS == 1785024000000
         and END_MS - FIRST_MS == DAYS * DAY_MS
         and CONTRACTS == {'BTC-USD': 'BTCUSDT', 'ETH-USD': 'ETHUSDT',
                           'SOL-USD': 'SOLUSDT'},
         "1,094 days from 2023-07-28 to 2026-07-25, three settlements a "
         "day, 3,282 rows a coin, a settlement at most one second after its "
         "8-hour mark, no rate over 5% — every one equal to a number typed "
         "out in this gate, and the first and last millisecond typed out "
         "too (1690502400000, 1785024000000)",
         f"first {FIRST_MS}, end {END_MS}")

    print("\n(b) A RATE, READ EXACTLY.")
    mark(rate_units('0.00010000') == 10000 and rate_units('-0.00005') == -5000
         and rate_units('0') == 0 and rate_units('0.05') == 5000000
         and rate_units('-0.05000000') == -5000000
         and rate_units('1e-8') == 1,
         "+0.0100% is 10,000 hundred-millionths, -0.0050% is -5,000, and 5% "
         "exactly — the limit itself — is accepted on both sides")
    mark('eight decimals' in refusal(rate_units, '0.000100001')
         and 'larger than 5%' in refusal(rate_units, '0.05000001')
         and 'larger than 5%' in refusal(rate_units, '-0.06')
         and 'not a number' in refusal(rate_units, 'abc')
         and 'not a number' in refusal(rate_units, 'NaN')
         and 'not a number' in refusal(rate_units, 'Infinity')
         and 'not a number' in refusal(rate_units, ''),
         "a ninth decimal, a hair over 5% either way, a word, NaN, infinity "
         "and an empty rate are each REFUSED")

    print("\n(c) THE ONE SHAPE A FREEZE MAY HAVE. Each refusal forced alone.")
    mark(refusal(check_rows, TEN, T0, 10) == '',
         "ten made-up days, thirty settlements on the clock: ACCEPTED")
    mark('29 settlements' in refusal(check_rows, TEN[:-1], T0, 10)
         and '31 settlements' in refusal(
             check_rows, TEN + [(T0 + 30 * MARK_MS, '0.0001')], T0, 10),
         "a row short and a row over are REFUSED")
    two_a_day = TEN[:4] + TEN[5:] + [(T0 + 30 * MARK_MS, '0.0001')]
    four_a_day = TEN[:5] + [(TEN[4][0] + 3600000, '0.0001')] + TEN[5:-1]
    mark('settlement 5 ' in refusal(check_rows, two_a_day, T0, 10)
         and 'settlement 6 ' in refusal(check_rows, four_a_day, T0, 10),
         "THIRTY ROWS IS NOT ENOUGH: a day with TWO settlements (and a "
         "spare one tacked on the end) and a day with FOUR (one dropped at "
         "the end) are each REFUSED at the first row off its mark",
         refusal(check_rows, two_a_day, T0, 10)[:74])
    mark(refusal(check_rows, changed(TEN, 7, stamp=T0 + 7 * MARK_MS + 1000),
                 T0, 10) == ''
         and 'off the clock' in refusal(
             check_rows, changed(TEN, 7, stamp=T0 + 7 * MARK_MS + 1001),
             T0, 10)
         and 'off the clock' in refusal(
             check_rows, changed(TEN, 7, stamp=T0 + 7 * MARK_MS - 1), T0, 10),
         "AT THE EXACT VALUE: a settlement 1,000 ms after its mark is "
         "accepted, 1,001 ms is refused, and ONE MILLISECOND BEFORE its "
         "mark is refused — that one would fall into the day before")
    mark('not a number' in refusal(check_rows, changed(TEN, 3, rate='x'),
                                   T0, 10)
         and 'larger than 5%' in refusal(
             check_rows, changed(TEN, 3, rate='0.5'), T0, 10)
         and 'eight decimals' in refusal(
             check_rows, changed(TEN, 3, rate='0.123456789e-1'), T0, 10),
         "one rate that is a word, one of 50%, one with nine decimals: each "
         "REFUSED")
    mark('settlement 1 ' in refusal(check_rows, TEN, T0 + DAY_MS, 10),
         "the right thirty rows for the WRONG first day are REFUSED")

    print("\n(d) THE PAGE-BY-PAGE FETCH, on a fake server.")
    LONG = made_up(700, salt=3)                 # 2,100 rows: three pages
    asked = []

    def server(rows, page=1000, shuffle=False, repeat=False):
        def get(params):
            asked.append(dict(params))
            hits = [r for r in rows
                    if params['startTime'] <= r[0] <= params['endTime']]
            hits = hits[:min(page, params['limit'])]
            if repeat and params['startTime'] > rows[0][0]:
                hits = [rows[0]] + hits[:-1]
            out = [{'fundingTime': s, 'fundingRate': r, 'symbol': 'X'}
                   for s, r in hits]
            return out[::-1] if shuffle else out
        return get

    END = T0 + 700 * DAY_MS
    got = held(builder.fetch_all, 'X', T0, END, server(LONG))
    mark(got == LONG and len(asked) == 3
         and [a['startTime'] for a in asked]
         == [T0, LONG[999][0] + 1, LONG[1999][0] + 1]
         and all(a['endTime'] == END - 1 and a['limit'] == 1000
                 for a in asked),
         "2,100 settlements come back whole in three pages: each next page "
         "is asked from ONE MILLISECOND AFTER the last row of the page "
         "before, and every request is capped one millisecond before the "
         "end", f"{len(got)} rows in {len(asked)} requests")
    asked.clear()
    exact = held(builder.fetch_all, 'X', T0, END, server(LONG[:2000]))
    mark(exact == LONG[:2000] and len(asked) == 3,
         "EXACTLY 2,000 rows — two full pages — needs a third request that "
         "comes back empty, and stops there without losing a row",
         f"{len(exact)} rows in {len(asked)} requests")
    mark(held(builder.fetch_all, 'X', T0, END,
              server(LONG, shuffle=True)) == LONG,
         "pages served newest-first give the identical rows")
    mark('repeated' in refusal(builder.fetch_all, 'X', T0, END,
                               server(LONG, repeat=True)),
         "a server that serves the same settlement twice is REFUSED")
    capped = held(builder.fetch_all, 'X', T0, T0 + 10 * DAY_MS,
                  server(LONG))
    mark(capped == LONG[:30] and capped[-1][0] < T0 + 10 * DAY_MS,
         "the end is NOT INCLUDED: asked for ten days, thirty rows come "
         "back, and the settlement stamped at the end itself is not one of "
         "them", f"{len(capped)} rows")

    print("\n(e) THE FREEZE: written once, verified, never overwritten.")

    def coins(days, first_ms=T0):
        return {contract: made_up(days, salt=k, first_ms=first_ms)
                for k, contract in enumerate(CONTRACTS.values())}

    room = os.path.join(WORK, 'freeze')
    write_freeze(room, coins(10), first_ms=T0, days=10)
    ok0, lines0 = verify(room, rows_owed=30)
    mark(ok0 and len(lines0) == 3 and sorted(os.listdir(room))
         == ['.gitattributes', 'BTCUSDT_funding.csv', 'ETHUSDT_funding.csv',
             'MANIFEST.json', 'SOLUSDT_funding.csv'],
         "three files, a manifest and the do-not-touch line are written, "
         "and the verifier says INTACT", f"{lines0}")
    with open(os.path.join(room, 'BTCUSDT_funding.csv'), 'rb') as handle:
        frozen_bytes = handle.read()
    mark(frozen_bytes == csv_bytes(made_up(10, salt=0))
         and b'\r' not in frozen_bytes
         and frozen_bytes.startswith(b'funding_time_ms,funding_rate\n')
         and read_rows(os.path.join(room, 'BTCUSDT_funding.csv'))
         == made_up(10, salt=0),
         "a frozen file is the header and one line a settlement, the rate "
         "as the TEXT it was served in, and reads back identical")
    mark('already holds a freeze' in refusal(write_freeze, room, coins(10),
                                             first_ms=T0, days=10)
         and verify(room, rows_owed=30)[0],
         "A SECOND FREEZE INTO THE SAME FOLDER IS REFUSED and the first is "
         "untouched")
    bad_room = os.path.join(WORK, 'bad')
    broken = coins(10)
    broken['SOLUSDT'] = broken['SOLUSDT'][:-1]
    mark('29 settlements' in refusal(write_freeze, bad_room, broken,
                                     first_ms=T0, days=10)
         and not os.path.exists(bad_room),
         "ONE coin a row short: NOTHING is written, not even the two good "
         "coins")
    built = os.path.join(WORK, 'built')

    def by_symbol(rows_by_contract):
        def get(params):
            rows = rows_by_contract[params['symbol']]
            hits = [r for r in rows
                    if params['startTime'] <= r[0] <= params['endTime']]
            return [{'fundingTime': s, 'fundingRate': r}
                    for s, r in hits[:params['limit']]]
        return get

    said = []
    full = coins(DAYS, first_ms=FIRST_MS)
    died = refusal(builder.build, built, get=by_symbol(full), out=said.append)
    said_text = '\n'.join(str(line) for line in said)
    mark(died == '' and verify(built)[0]
         and all(read_rows(os.path.join(built, f'{c}_funding.csv')) == full[c]
                 for c in CONTRACTS.values()),
         "THE BUILDER, WHOLE, AGAINST A FAKE SERVER HOLDING THE DECLARED "
         "SHAPE (3,282 made-up rows a coin): it freezes all three, the "
         "verifier says INTACT, and each file is its own coin's rows",
         died or f"{verify(built)[1]}")
    mark(died == '' and '3282' in said_text and FIRST_DAY in said_text
         and not any(rate in said_text for _s, rate in full['BTCUSDT'][:50]
                     if rate not in ('0.00000000',))
         and '0.000' not in said_text,
         "and the builder PRINTED NO RATE: counts, dates and checksums only")
    mark('already holds a freeze' in refusal(builder.build, built,
                                             get=by_symbol(full),
                                             out=lambda *a: None),
         "the builder REFUSES to run a second time")
    short = dict(full)
    short['ETHUSDT'] = full['ETHUSDT'][:-3]
    nowhere = os.path.join(WORK, 'nowhere')
    mark('3279 settlements' in refusal(builder.build, nowhere,
                                       get=by_symbol(short),
                                       out=lambda *a: None)
         and not os.path.exists(nowhere),
         "a server one DAY short on one coin: the builder refuses and "
         "freezes nothing")

    print("\n(f) THE VERIFIER, against three kinds of damage.")

    def damaged(how):
        """A fresh copy of the good freeze with one thing wrong ->
        the verifier's answer."""
        copy = os.path.join(WORK, f'damage_{how}')
        shutil.copytree(room, copy)
        target = os.path.join(copy, 'ETHUSDT_funding.csv')
        if how == 'byte':
            with open(target, 'rb') as handle:
                data = bytearray(handle.read())
            at = len(data) - 3
            data[at] = ord('7') if data[at] != ord('7') else ord('8')
            with open(target, 'wb') as handle:
                handle.write(bytes(data))
        elif how == 'missing':
            os.remove(target)
        elif how == 'extra':
            with open(os.path.join(copy, 'notes.csv'), 'w') as handle:
                handle.write('x')
        elif how == 'nomanifest':
            os.remove(os.path.join(copy, MANIFEST_NAME))
        return copy, verify(copy, rows_owed=30)

    byte_room, (byte_ok, byte_lines) = damaged('byte')
    mark(not byte_ok and 'ETHUSDT_funding.csv: 30 rows, DOES NOT MATCH'
         in byte_lines and sum('checksum matches' in line
                               for line in byte_lines) == 2,
         "ONE DIGIT of one rate changed (the file the same length): the "
         "verifier names that file and only that file", f"{byte_lines}")
    mark('does not match its checksum' in refusal(load, 'ETH-USD', byte_room,
                                                  T0, 10)
         and 'not intact' in refusal(preflight, byte_room, T0, 10, 30)
         and len(load('BTC-USD', byte_room, T0, 10)[0]) == 30,
         "and that file REFUSES TO LOAD, and the pre-flight refuses the "
         "whole freeze — while an undamaged coin beside it still loads")
    mark(not damaged('missing')[1][0] and not damaged('extra')[1][0]
         and not damaged('nomanifest')[1][0]
         and not verify(os.path.join(WORK, 'never_made'))[0],
         "a missing file, a file the manifest does not list, a missing "
         "manifest and a folder that does not exist: each NOT INTACT, none "
         "of them a crash")
    mark(not verify(room)[0] and verify(room, rows_owed=30)[0],
         "a freeze whose manifest says 30 rows is NOT INTACT when 3,282 are "
         "owed: an intact file of the wrong length is still the wrong file")
    times_b, units_b = load('BTC-USD', room, T0, 10)
    mark(times_b == [s for s, _r in made_up(10)]
         and units_b == [rate_units(r) for _s, r in made_up(10)]
         and sorted(preflight(room, T0, 10, 30)) == sorted(CONTRACTS),
         "an intact freeze loads as whole hundred-millionths, and the "
         "pre-flight hands back all three coins")

    print("\n(g) >>> THE JOIN, BY HAND. This is where a leak would live.")
    # Three made-up days. Settlements (in hundred-millionths):
    #   day 0:  00:00 exactly  10,000   08:00  20,000   16:00  -5,000
    #   day 1:  00:00 + 29 ms   1,000   08:00   2,000   16:00   3,000
    #   day 2:  00:00           7,000   08:00   7,000   16:00   7,000
    OPENS = [T0, T0 + DAY_MS, T0 + 2 * DAY_MS]
    TIMES = [T0, T0 + MARK_MS, T0 + 2 * MARK_MS,
             T0 + DAY_MS + 29, T0 + DAY_MS + MARK_MS,
             T0 + DAY_MS + 2 * MARK_MS,
             T0 + 2 * DAY_MS, T0 + 2 * DAY_MS + MARK_MS,
             T0 + 2 * DAY_MS + 2 * MARK_MS]
    VALUES = [10000, 20000, -5000, 1000, 2000, 3000, 7000, 7000, 7000]
    mark(daily_funding(OPENS, TIMES, VALUES) == [25000.0, 6000.0, 21000.0],
         "three days, nine settlements: 10,000 + 20,000 - 5,000 = 25,000; "
         "1,000 + 2,000 + 3,000 = 6,000; 3 x 7,000 = 21,000",
         f"{daily_funding(OPENS, TIMES, VALUES)}")
    # THE BOUNDARY. Day 1's first settlement is stamped EXACTLY at day 1's
    # opening - which is exactly day 0's close. It must be day 1's.
    AT_CLOSE = list(TIMES)
    AT_CLOSE[3] = T0 + DAY_MS
    edge = daily_funding(OPENS, AT_CLOSE, VALUES)
    mark(edge == [25000.0, 6000.0, 21000.0],
         "A SETTLEMENT STAMPED EXACTLY AT MIDNIGHT BELONGS TO THE DAY THAT "
         "IS BEGINNING, NOT THE DAY THAT IS ENDING: day 0 stays 25,000 and "
         "does not become 26,000", f"{edge}")
    # One millisecond BEFORE midnight would be day 0's fourth: day 0 then
    # holds four and day 1 two, and BOTH are empty rather than wrong.
    EARLY = list(TIMES)
    EARLY[3] = T0 + DAY_MS - 1
    early = daily_funding(OPENS, EARLY, VALUES)
    mark(math.isnan(early[0]) and math.isnan(early[1])
         and early[2] == 21000.0,
         "one millisecond BEFORE midnight it would be the ending day's "
         "fourth: that day (four) and the next (two) are both EMPTY, never "
         "a partial or padded sum", f"{early}")
    gap = daily_funding(OPENS, TIMES[:4] + TIMES[5:], VALUES[:4] + VALUES[5:])
    mark(gap[0] == 25000.0 and math.isnan(gap[1]) and gap[2] == 21000.0,
         "a day with one settlement missing is EMPTY (not 4,000), and its "
         "neighbours are untouched", f"{gap}")
    outside = daily_funding(OPENS[1:], TIMES, VALUES)
    mark(outside == [6000.0, 21000.0],
         "settlements from before the first candle belong to no candle and "
         "are dropped, not pushed into the first", f"{outside}")
    last_only = daily_funding(OPENS[:2], TIMES, VALUES)
    mark(last_only == [25000.0, 6000.0],
         "and settlements after the last candle's day are not pulled back "
         "into it", f"{last_only}")

    def candles(days, first='2030-01-01', freq='1D'):
        index = pd.date_range(first, periods=days, freq=freq)
        return pd.DataFrame({'open': 100.0, 'high': 101.0, 'low': 99.0,
                             'close': 100.5}, index=index)

    plain = candles(3)
    joined = attach(plain, TIMES, VALUES)
    mark(list(joined['funding']) == [25000.0, 6000.0, 21000.0]
         and list(joined.columns) == ['open', 'high', 'low', 'close',
                                      'funding']
         and 'funding' not in plain.columns and joined.index.equals(
             plain.index),
         "joined to three daily candles: one new column, the same three "
         "figures, and THE CANDLES HANDED IN ARE NOT CHANGED — a copy "
         "comes back")
    mark('DAILY candles' in refusal(attach, candles(6, freq='4h'), TIMES,
                                    VALUES)
         and 'DAILY candles' in refusal(
             attach, candles(3, first='2030-01-01 04:00'), TIMES, VALUES)
         and 'DAILY candles' in refusal(
             attach, candles(3).drop(candles(3).index[1]), TIMES, VALUES),
         "4-hour candles, daily candles that open at 04:00, and daily "
         "candles with a day missing are each REFUSED")

    # THE POISON TEST. 40 made-up days; every settlement from day 25 on is
    # replaced. Not one of the first 25 days may move, and all 15 after
    # must (the replacement adds 1,000 to every rate).
    forty = made_up(40)
    t40 = [s for s, _r in forty]
    u40 = [rate_units(r) for _s, r in forty]
    poisoned = u40[:75] + [value + 1000 for value in u40[75:]]
    clean40 = list(attach(candles(40), t40, u40)['funding'])
    dirty40 = list(attach(candles(40), t40, poisoned)['funding'])
    mark(clean40[:25] == dirty40[:25]
         and all(d == c + 3000 for c, d in zip(clean40[25:], dirty40[25:])),
         ">>> THE POISON TEST: every settlement from day 26 on is changed, "
         "and NOT ONE of the first 25 days' funding moves — while all 15 "
         "days after it do, by exactly the three changed rates")
    cut = attach(candles(25), t40, u40)
    mark(list(cut['funding']) == clean40[:25],
         "and the first 25 candles joined ON THEIR OWN carry the same "
         "figures as inside the 40: a day's funding does not depend on how "
         "much of the future is in the file")

    print("\n(h) >>> THE SABOTAGE DRILL, PERMANENT. INERT IS A FAIL.")

    def witness():
        return (
            daily_funding(OPENS, AT_CLOSE, VALUES),
            str(daily_funding(OPENS, TIMES[:4] + TIMES[5:],
                              VALUES[:4] + VALUES[5:])),
            refusal(check_rows, changed(TEN, 7,
                                        stamp=T0 + 7 * MARK_MS + 1001),
                    T0, 10)[:10],
            refusal(check_rows, changed(TEN, 3, rate='0.5'), T0, 10)[:10],
            refusal(check_rows, TEN[:-1], T0, 10)[:10],
            verify(byte_room, rows_owed=30)[0],
            refusal(write_freeze, room, coins(10), first_ms=T0,
                    days=10)[:12],
            clean40[:25] == list(attach(candles(40), t40,
                                        poisoned)['funding'])[:25],
            len(held(builder.fetch_all, 'X', T0, END, server(LONG))),
            refusal(rate_units, '0.000100001')[:10],
            held(rate_units, '0.00012345'),
        )

    HONEST = witness()
    EXPECTED = ([25000.0, 6000.0, 21000.0], '[25000.0, nan, 21000.0]',
                'ValueError', 'ValueError', 'ValueError', False,
                'RuntimeError', True, 2100, 'ValueError', 12345)
    G = globals()
    _keep = {name: G[name] for name in
             ('_owner', 'SETTLEMENTS_A_DAY', 'SLACK_MS', 'MAX_RATE',
              'check_rows', '_sha', 'daily_funding', 'UNITS', 'DAY_MS')}
    _keep_page = builder.PAGE
    _real_listdir = os.listdir

    def _recorded(path):
        with open(os.path.join(os.path.dirname(path), MANIFEST_NAME),
                  encoding='utf-8') as handle:
            return json.load(handle)['files'][os.path.basename(path)][
                'sha256']

    def _tomorrow(opens, times, units):
        honest = _keep['daily_funding'](opens, times, units)
        return honest[1:] + [float('nan')]

    BREAKS = [
        ('D1', 'a settlement AT the close counted into the day ending',
         '_owner', lambda opens, stamp: bisect.bisect_left(opens, stamp) - 1),
        ('D2', 'a day with only two settlements accepted as whole',
         'SETTLEMENTS_A_DAY', 2),
        ('D3', 'a settlement a whole day off its mark accepted',
         'SLACK_MS', DAY_MS),
        ('D4', 'a funding rate of 50% accepted', 'MAX_RATE', Decimal('1')),
        ('D5', 'the shape check switched off', 'check_rows',
         lambda rows, first_ms=None, days=None: None),
        ('D6', 'the verifier trusting the manifest, not the file',
         '_sha', lambda path: _recorded(path)),
        ('D7', "each day carrying TOMORROW's funding", 'daily_funding',
         _tomorrow),
        ('D8', 'rates rounded to six decimals', 'UNITS', 1000000),
        ('D9', 'a "day" of 48 hours in the join', 'DAY_MS', 2 * DAY_MS),
    ]
    print()
    for tag, words, name, replacement in BREAKS:
        G[name] = replacement
        try:
            broken_answer = witness()
        except Exception:                                  # noqa: BLE001
            broken_answer = '<crashed>'
        finally:
            G[name] = _keep[name]
        was_changed = broken_answer != HONEST
        caught = broken_answer != EXPECTED
        good = was_changed and caught
        verdict = ('CAUGHT' if good else
                   'INERT — IT CHANGED NOTHING' if not was_changed else
                   'ESCAPED — THE GATE IS DECORATIVE')
        mark(good, f"{tag} {words:<54} -> {verdict}")
    # Two breaks that live outside this module's globals.
    builder.PAGE = 1001         # the fake server still serves 1,000 a page
    try:
        b10 = witness()
    except Exception:                                      # noqa: BLE001
        b10 = '<crashed>'
    finally:
        builder.PAGE = _keep_page
    mark(b10 != HONEST and b10 != EXPECTED,
         f"D10 {'the fetch believing a full page is 1,001 rows':<53} -> "
         f"{'CAUGHT' if b10 != HONEST else 'INERT — IT CHANGED NOTHING'}")
    os.listdir = lambda path: []                # "nothing is there yet"
    try:
        b11 = witness()
    except Exception:                                      # noqa: BLE001
        b11 = '<crashed>'
    finally:
        os.listdir = _real_listdir
    mark(b11 != HONEST and b11 != EXPECTED,
         f"D11 {'the freeze believing its folder is empty':<53} -> "
         f"{'CAUGHT' if b11 != HONEST else 'INERT — IT CHANGED NOTHING'}")
    mark(all(G[name] is original for name, original in _keep.items())
         and builder.PAGE == 1000 and os.listdir is _real_listdir
         and witness() == HONEST == EXPECTED,
         "and after eleven breaks everything is what it started as, and "
         "the eleven witnessed answers equal the eleven typed out here")

    print("\n(i) NOTHING REAL WAS TOUCHED, AND THE GATE COUNTS ITSELF.")
    shutil.rmtree(WORK, ignore_errors=True)
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        production = handle.read().split("if __name__ == '__main__':")[0]
    mark((sorted(os.listdir(FUNDING_DIR)) if os.path.isdir(FUNDING_DIR)
          else None) == REAL_BEFORE
         and not any(word in production for word in
                     ('requests', 'urllib', 'http', 'socket', 'print('))
         and 'import build_funding_vault' not in production,
         "the real frozen folder is exactly as it was; and the reading "
         "half of this file names no network library, does not import the "
         "builder, and has no `print` in it at all")
    mark(len(BREAKS) + 2 == 11, "eleven breaks, counted against a number "
                                "typed out here")
    EXPECTED_CHECKS = 52
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.3-D PASSED — {len(nonlocal_ok)} checks, 0 red.

THE FREEZE HAS ONE SHAPE AND REFUSES EVERY OTHER: a row short or over,
two settlements in a day or four, one a millisecond before its mark or
1,001 after, a rate that is not a plain number of eight decimals under
5%. It is written once and never over.

THE VERIFIER CAUGHT one changed digit, a missing file, an unlisted file
and a missing manifest.

THE JOIN PUTS A SETTLEMENT STAMPED AT MIDNIGHT INTO THE DAY BEGINNING,
never the day ending; a day without exactly three is empty; and with
every settlement after a chosen day changed, no earlier day moved.

WHAT THIS GATE DOES **NOT** PROVE. It has never seen a real funding
rate. It cannot say Binance's history is right, that the freeze on
this disk is the one Binance served, or that the vault's candles are
on the UTC clock this join assumes - that last was measured once by
hand, on early-2024 rows, and is in PROGRESS_LOG.md.""")
    else:
        print(f"GATE 6.3-D FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
