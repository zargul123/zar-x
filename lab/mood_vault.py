"""
Zar X Lab — THE FROZEN MOOD (Phase 6, Gauntlet Slot 3).

Slot 3 was re-specified ONCE by the Commander on 2026-11-16, before any slot
had been run, from the on-chain cycle thermometer to THE CROWD-MOOD FADE. It
needs the Fear & Greed index (alternative.me), one value a day. **THE LAB
TESTS ON FROZEN EVIDENCE ONLY**, so that history is fetched ONCE, frozen in
`lab/mood_vault/` beside the vault, checksummed, and never refreshed. The
rules were declared in PROGRESS_LOG.md on 2026-11-16 (late night) and
committed with no code, before this file existed.

THIS FILE IS THE READING HALF: the freeze's one shape, the verifier, the
loader and the join. **IT HOLDS NO NETWORK CODE**: the one fetch lives in
`lab/build_mood_vault.py`, which the gauntlet never imports.

WHAT IS FROZEN: one row for each of the daily vault's 1,094 days
(2023-07-28 to 2026-07-25): the day, the index value (0 to 100), the
publisher's own label, and whether the row was CARRIED. A day the publisher
never published carries the last value published BEFORE it - what a person
reading the index that day would have had - and is marked. No more than 3
carried days in a row and 11 in all, or the freeze is refused.

**>>> THE HOLD-OUT'S VALUES ARE IN THAT FILE. NOTHING HERE PRINTS ONE.** Row
counts, dates and checksums only: how often the hold-out was fearful or
greedy is the trade count, and the trade count is a result.

THE JOIN'S RULE (Law 7 for this slot): the publisher stamps a value with
its day at 00:00 UTC and publishes it at the start of that day. So **THE
VALUE STAMPED DAY D GOES ON THE DAILY CANDLE THAT OPENS ON DAY D** - known
for the whole of that candle, about 24 hours before it closes. Never on the
candle before. The side of a day (fear, neutral, greed) is the publisher's
label, not a number typed here.

RUN (from the zar-x folder):
    python lab/mood_vault.py            (verify the freeze: INTACT or not)
    python lab/mood_vault.py --gate     (GATE 6.5-D, on made-up values)
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
MOOD_DIR = os.path.join(LAB_DIR, 'mood_vault')
MANIFEST_NAME = 'MANIFEST.json'
ATTRIBUTES_NAME = '.gitattributes'
FILE_NAME = 'fear_greed.csv'
HEADER = 'day,value,label,carried'

FIRST_DAY = '2023-07-28'       # the daily vault's first candle
LAST_DAY = '2026-07-25'        # and its last
DAYS = 1094
DAY_MS = 86_400_000
MAX_CARRIED_RUN = 3            # days in a row the publisher may be silent
MAX_CARRIED = 11               # and in all: 1% of 1,094
# The publisher's five labels -> the side of the day. Fear -1, greed +1.
LABELS = {'Extreme Fear': -1, 'Fear': -1, 'Neutral': 0, 'Greed': 1,
          'Extreme Greed': 1}


def day_ms(text):
    """'2023-07-28' -> the millisecond its UTC day begins. No local clock."""
    stamp = datetime.strptime(text, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    return int(stamp.timestamp()) * 1000


def day_text(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime(
        '%Y-%m-%d')


FIRST_MS = day_ms(FIRST_DAY)


def build_rows(published, first_ms=None, days=None):
    """What the publisher published -> the rows to freeze.

    published : {day_ms: (value, label)} - may hold days outside the window
    -> [(day_text, value, label, carried)], one a day. A day with nothing
       published carries the last value published BEFORE it. Raises
       ValueError if the first day has nothing on or before it.
    """
    first_ms = FIRST_MS if first_ms is None else first_ms
    days = DAYS if days is None else days
    earlier = [stamp for stamp in published if stamp < first_ms]
    last = published[max(earlier)] if earlier else None
    rows = []
    for position in range(days):
        stamp = first_ms + position * DAY_MS
        if stamp in published:
            last = published[stamp]
            carried = 0
        else:
            carried = 1
        if last is None:
            raise ValueError(f'{day_text(stamp)} has nothing published on '
                             f'or before it')
        rows.append((day_text(stamp), last[0], last[1], carried))
    return rows


def check_rows(rows, first_ms=None, days=None):
    """The one shape a freeze may have. Raises ValueError naming the first
    fault; never prints a value."""
    first_ms = FIRST_MS if first_ms is None else first_ms
    days = DAYS if days is None else days
    if len(rows) != days:
        raise ValueError(f'{len(rows)} days where exactly {days} are owed')
    run = total = 0
    for position, (day, value, label, carried) in enumerate(rows):
        if day != day_text(first_ms + position * DAY_MS):
            raise ValueError(f'row {position + 1} is not the day it should '
                             f'be: a day missing, twice or out of order')
        if type(value) is not int or not 0 <= value <= 100:
            raise ValueError(f'row {position + 1}: a value that is not a '
                             f'whole number from 0 to 100')
        if label not in LABELS:
            raise ValueError(f'row {position + 1}: a label that is not one '
                             f'of the publisher\'s five')
        if carried not in (0, 1):
            raise ValueError(f'row {position + 1}: a bad carried mark')
        if carried and position and (value, label) != rows[position - 1][1:3]:
            raise ValueError(f'row {position + 1}: a carried day that does '
                             f'not carry the day before it')
        run = run + 1 if carried else 0
        total += carried
        if run > MAX_CARRIED_RUN:
            raise ValueError(f'more than {MAX_CARRIED_RUN} days in a row '
                             f'with nothing published')
    if total > MAX_CARRIED:
        raise ValueError(f'{total} carried days where at most '
                         f'{MAX_CARRIED} are allowed')


def csv_bytes(rows):
    lines = [HEADER] + [f'{day},{value},{label},{carried}'
                        for day, value, label, carried in rows]
    return ('\n'.join(lines) + '\n').encode('ascii')


def read_rows(path):
    """The frozen file -> [(day_text, value, label, carried)]."""
    with open(path, 'rb') as handle:
        lines = handle.read().decode('ascii').split('\n')
    if lines[0] != HEADER or lines[-1] != '':
        raise ValueError(f'{os.path.basename(path)} is not a frozen mood '
                         f'file')
    rows = []
    for line in lines[1:-1]:
        day, value, label, carried = line.split(',')
        if not value.isdigit() or not carried.isdigit():
            raise ValueError('a frozen value that is not a whole number')
        rows.append((day, int(value), label, int(carried)))
    return rows


def _sha(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def write_freeze(directory, rows, note='', first_ms=None, days=None):
    """Write a freeze: the file, the manifest, and the line that tells git
    not to touch a byte. REFUSES if anything is already there."""
    if os.path.isdir(directory) and os.listdir(directory):
        raise RuntimeError(f'REFUSED: {directory} already holds a freeze. '
                           f'The frozen mood is never rebuilt or refreshed.')
    check_rows(rows, first_ms, days)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, FILE_NAME)
    with open(path, 'xb') as handle:
        handle.write(csv_bytes(rows))
    manifest = {
        'what': 'the Fear & Greed index (alternative.me), one value a day',
        'note': note, 'first_day': rows[0][0], 'last_day': rows[-1][0],
        'law': 'This file is evidence. It is never modified, never '
               'refreshed, only verified.',
        'files': {FILE_NAME: {
            'rows': len(rows),
            'carried': sum(row[3] for row in rows),
            'bytes': os.path.getsize(path), 'sha256': _sha(path)}},
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
    A checksum, a byte count, a row count and the list of files. No value
    is read."""
    directory = MOOD_DIR if directory is None else directory
    rows_owed = DAYS if rows_owed is None else rows_owed
    try:
        with open(os.path.join(directory, MANIFEST_NAME),
                  encoding='utf-8') as handle:
            files = json.load(handle)['files']
        present = sorted(os.listdir(directory))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return False, [f'NO READABLE FREEZE in {directory} '
                       f'({type(exc).__name__})']
    lines, ok = [], True
    if sorted(files) != [FILE_NAME]:
        ok = False
        lines.append(f'the manifest lists {sorted(files)}, not {FILE_NAME}')
    extra = sorted(set(present) - {FILE_NAME, MANIFEST_NAME, ATTRIBUTES_NAME})
    if extra:
        ok = False
        lines.append(f'files that are not in the manifest: {extra}')
    entry = files.get(FILE_NAME)
    path = os.path.join(directory, FILE_NAME)
    if not isinstance(entry, dict) or not os.path.isfile(path):
        return False, lines + [f'{FILE_NAME}: MISSING']
    same = (_sha(path) == entry.get('sha256')
            and os.path.getsize(path) == entry.get('bytes')
            and entry.get('rows') == rows_owed)
    lines.append(f'{FILE_NAME}: {entry.get("rows")} rows, '
                 f'{"checksum matches" if same else "DOES NOT MATCH"}')
    return ok and same, lines


def load(directory=None, first_ms=None, days=None):
    """The frozen mood -> (day_ms list, values, sides). The checksum is
    verified against the manifest first and the shape checked again, on
    every load. A side is the publisher's label: fear -1, neutral 0,
    greed +1."""
    directory = MOOD_DIR if directory is None else directory
    path = os.path.join(directory, FILE_NAME)
    with open(os.path.join(directory, MANIFEST_NAME),
              encoding='utf-8') as handle:
        entry = json.load(handle)['files'][FILE_NAME]
    if _sha(path) != entry['sha256']:
        raise RuntimeError(f'REFUSED: {FILE_NAME} does not match its '
                           f'checksum.')
    rows = read_rows(path)
    check_rows(rows, first_ms, days)
    return ([day_ms(day) for day, _v, _l, _c in rows],
            [value for _d, value, _l, _c in rows],
            [LABELS[label] for _d, _v, label, _c in rows])


def preflight(directory=None, first_ms=None, days=None, rows_owed=None):
    """EVERYTHING THAT CAN BE REFUSED BEFORE A SLOT IS SPENT. Verifies the
    freeze and loads it. Raises RuntimeError('REFUSED ...') on any fault."""
    ok, lines = verify(directory, rows_owed)
    if not ok:
        raise RuntimeError('REFUSED: the frozen mood is not intact - '
                           + '; '.join(lines))
    try:
        return load(directory, first_ms, days)
    except (OSError, ValueError, KeyError) as exc:
        raise RuntimeError(f'REFUSED: the frozen mood cannot be read - '
                           f'{type(exc).__name__}: {exc}')


def attach(df, days_ms, values, sides):
    """Daily candles + the frozen mood -> A COPY of the candles with two
    more columns: `mood` (the value published that day) and `mood_side`
    (-1 fear, 0 neutral, +1 greed). The value stamped day D goes on the
    candle that opens on day D. A candle the freeze does not cover is left
    empty. Refuses candles that are not daily, at 00:00 UTC, a day apart."""
    import pandas as pd
    epoch = pd.Timestamp('1970-01-01')
    opens = [int(value) for value in
             (df.index - epoch) // pd.Timedelta(milliseconds=1)]
    steps = {b - a for a, b in zip(opens, opens[1:])}
    if steps - {DAY_MS} or any(value % DAY_MS for value in opens):
        raise ValueError('REFUSED: the mood is joined to DAILY candles that '
                         'open at 00:00 UTC, one day apart, and to nothing '
                         'else')
    by_day = {stamp: (float(value), float(side))
              for stamp, value, side in zip(days_ms, values, sides)}
    empty = (float('nan'), float('nan'))
    out = df.copy()
    out['mood'] = [by_day.get(stamp, empty)[0] for stamp in opens]
    out['mood_side'] = [by_day.get(stamp, empty)[1] for stamp in opens]
    return out


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        ok, lines = verify()
        print('FROZEN MOOD — lab/mood_vault/')
        for line in lines:
            print('   ' + line)
        if ok:
            try:
                preflight()
                print(f'   {DAYS} days, {FIRST_DAY} to {LAST_DAY}, one row '
                      f'a day')
            except RuntimeError as exc:
                ok = False
                print(f'   {exc}')
        print(f'FROZEN MOOD {"INTACT" if ok else "NOT INTACT"} — '
              f'{sum("checksum matches" in line for line in lines)} of 1')
        sys.exit(0 if ok else 1)

    # =====================================================================
    # GATE 6.5-D — THE FROZEN MOOD: THE FETCH, THE CARRY RULE, THE FREEZE,
    # THE VERIFIER AND THE JOIN. Declared in PROGRESS_LOG.md on 2026-11-16
    # (late night) and committed with no code, before this file existed.
    #
    # **IT NEVER TOUCHES THE NETWORK, THE REAL FROZEN FOLDER OR THE VAULT.**
    # Every value below is made up. It also gates `lab/build_mood_vault.py`,
    # whose server is replaced by a fake one.
    # =====================================================================
    import math
    import shutil
    import tempfile

    import pandas as pd

    sys.path.insert(0, LAB_DIR)
    import build_mood_vault as builder

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def held(function, *args, **kwargs):
        """A call's answer, or the name of what it raised (rule (k))."""
        try:
            return function(*args, **kwargs)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>'

    def refusal(function, *args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as exc:                           # noqa: BLE001
            return f'{type(exc).__name__}: {exc}'
        return ''

    REAL_BEFORE = (sorted(os.listdir(MOOD_DIR))
                   if os.path.isdir(MOOD_DIR) else None)
    WORK = tempfile.mkdtemp(prefix='zarx_mood_')
    T0 = day_ms('2030-01-01')          # made-up days, far from any real one

    def label_of(value):
        """A made-up publisher's bands, for made-up values only."""
        return ('Extreme Fear' if value <= 25 else 'Fear' if value <= 46
                else 'Neutral' if value <= 54 else 'Greed' if value <= 75
                else 'Extreme Greed')

    def made_up(days, salt=0, first_ms=T0, before=5):
        """{day_ms: (value, label)} for `before` days ahead of the window
        and every day of it."""
        out = {}
        for n in range(-before, days):
            value = (n * 37 + salt * 11 + 500) % 101
            out[first_ms + n * DAY_MS] = (value, label_of(value))
        return out

    def without(published, *positions):
        out = dict(published)
        for position in positions:
            del out[T0 + position * DAY_MS]
        return out

    def changed(rows, at, **new):
        rows = [list(row) for row in rows]
        for key, value in new.items():
            rows[at][('day', 'value', 'label', 'carried').index(key)] = value
        return [tuple(row) for row in rows]

    TEN_PUBLISHED = made_up(10)
    TEN = build_rows(TEN_PUBLISHED, T0, 10)

    print("=" * 70)
    print("GATE 6.5-D — THE FROZEN MOOD. Made-up values only; no network, no")
    print("real freeze, no vault.")
    print("=" * 70)

    print("\n(a) THE DECLARED SHAPE, typed out here.")
    mark((FIRST_DAY, LAST_DAY, DAYS, DAY_MS, MAX_CARRIED_RUN, MAX_CARRIED,
          FILE_NAME) == ('2023-07-28', '2026-07-25', 1094, 86400000, 3, 11,
                         'fear_greed.csv')
         and FIRST_MS == 1690502400000
         and day_text(FIRST_MS + (DAYS - 1) * DAY_MS) == LAST_DAY
         and LABELS == {'Extreme Fear': -1, 'Fear': -1, 'Neutral': 0,
                        'Greed': 1, 'Extreme Greed': 1},
         "1,094 days from 2023-07-28 to 2026-07-25, at most 3 carried days "
         "in a row and 11 in all, and the publisher's five labels with the "
         "side each one is on — every one typed out in this gate")

    print("\n(b) THE CARRY RULE, BY HAND.")
    mark(len(TEN) == 10 and all(row[3] == 0 for row in TEN)
         and TEN[0] == ('2030-01-01',) + TEN_PUBLISHED[T0] + (0,)
         and TEN[9][0] == '2030-01-10',
         "ten made-up days all published: ten rows, none carried, each its "
         "own day's value and label")
    gap = held(build_rows, without(TEN_PUBLISHED, 4), T0, 10)
    mark(isinstance(gap, list) and gap[4] == ('2030-01-05',) + TEN[3][1:3]
         + (1,) and gap[5] == TEN[5] and gap[3] == TEN[3],
         "ONE DAY THE PUBLISHER SKIPPED: it carries THE DAY BEFORE's value "
         "and label, is marked carried, and its neighbours are untouched")
    mark(isinstance(gap, list) and gap[4][1:3] != TEN[5][1:3],
         "and a carried day NEVER takes the NEXT day's value: the made-up "
         "day after it holds a different one, and it was not used")
    three = held(build_rows, without(TEN_PUBLISHED, 4, 5, 6), T0, 10)
    four = held(build_rows, without(TEN_PUBLISHED, 4, 5, 6, 7), T0, 10)
    mark(isinstance(three, list) and refusal(check_rows, three, T0, 10) == ''
         and [row[3] for row in three] == [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
         and all(row[1:3] == TEN[3][1:3] for row in three[4:7])
         and 'in a row' in refusal(check_rows, four, T0, 10),
         "AT THE EXACT NUMBER: three silent days in a row are carried and "
         "ACCEPTED; four in a row are REFUSED")
    first_gone = held(build_rows, without(TEN_PUBLISHED, 0), T0, 10)
    nothing_before = {k: v for k, v in TEN_PUBLISHED.items() if k > T0}
    mark(isinstance(first_gone, list)
         and first_gone[0] == ('2030-01-01',)
         + TEN_PUBLISHED[T0 - DAY_MS] + (1,)
         and 'nothing published on or before'
         in refusal(build_rows, nothing_before, T0, 10),
         "a silent FIRST day carries the day before the window; with "
         "nothing published before it at all, REFUSED")
    forty = made_up(40)
    eleven = held(build_rows, without(forty, *range(2, 35, 3)), T0, 40)
    twelve = held(build_rows, without(forty, *range(2, 38, 3)), T0, 40)
    mark(isinstance(eleven, list) and sum(r[3] for r in eleven) == 11
         and refusal(check_rows, eleven, T0, 40) == ''
         and sum(r[3] for r in twelve) == 12
         and '12 carried days' in refusal(check_rows, twelve, T0, 40),
         "eleven carried days scattered through a freeze are ACCEPTED; "
         "twelve are REFUSED")

    print("\n(c) THE ONE SHAPE A FREEZE MAY HAVE. Each refusal forced alone.")
    mark(refusal(check_rows, TEN, T0, 10) == ''
         and '9 days' in refusal(check_rows, TEN[:-1], T0, 10)
         and '11 days' in refusal(check_rows, TEN + [TEN[-1]], T0, 10),
         "ten good rows ACCEPTED; a row short and a row over REFUSED")
    twice = TEN[:5] + [TEN[4]] + TEN[5:-1]
    swapped = TEN[:4] + [TEN[5], TEN[4]] + TEN[6:]
    mark('row 6 is not the day' in refusal(check_rows, twice, T0, 10)
         and 'row 5 is not the day' in refusal(check_rows, swapped, T0, 10)
         and 'row 1 is not the day' in refusal(check_rows, TEN, T0 + DAY_MS,
                                               10),
         "TEN ROWS IS NOT ENOUGH: a day in twice, two days swapped, and the "
         "right rows for the wrong first day are each REFUSED")
    mark(refusal(check_rows, changed(TEN, 3, value=0), T0, 10) == ''
         and refusal(check_rows, changed(TEN, 3, value=100), T0, 10) == ''
         and all('whole number from 0 to 100' in refusal(
             check_rows, changed(TEN, 3, value=bad), T0, 10)
             for bad in (101, -1, 50.5, '50', True, None)),
         "a value of 0 and of 100 are ACCEPTED; 101, -1, 50.5, the text "
         "'50', True and nothing at all are each REFUSED")
    mark(all("one of the publisher's five" in refusal(
        check_rows, changed(TEN, 3, label=bad), T0, 10)
        for bad in ('extreme fear', 'Extreme  Fear', 'Panic', '', 'Greed '))
         and 'carried mark' in refusal(check_rows,
                                       changed(TEN, 3, carried=2), T0, 10),
         "a label in lower case, with two spaces, with a trailing space, "
         "an unknown one and an empty one are each REFUSED: the side of a "
         "day is the publisher's exact words or it is nothing")
    forged = changed(TEN, 5, carried=1)
    mark('does not carry the day before' in refusal(check_rows, forged, T0,
                                                    10),
         "a row MARKED carried that does not hold the day before's value is "
         "REFUSED")

    print("\n(d) THE FETCH, on a fake server.")

    def server(published, **fault):
        def get():
            data = [{'value': str(value), 'value_classification': label,
                     'timestamp': str(stamp // 1000)}
                    for stamp, (value, label) in sorted(published.items(),
                                                        reverse=True)]
            if 'offclock' in fault:
                data[3]['timestamp'] = str(int(data[3]['timestamp']) + 3600)
            if 'twice' in fault:
                data.insert(2, dict(data[2]))
            if 'decimal' in fault:
                data[3]['value'] = '50.5'
            return {'name': 'made up', 'data': data}
        return get

    got = held(builder.fetch_published, server(TEN_PUBLISHED))
    mark(got == TEN_PUBLISHED,
         "fifteen made-up days served newest-first come back as the same "
         "fifteen, each value a whole number")
    mark('00:00 UTC' in refusal(builder.fetch_published,
                                server(TEN_PUBLISHED, offclock=1))
         and 'twice' in refusal(builder.fetch_published,
                                server(TEN_PUBLISHED, twice=1))
         and 'whole number' in refusal(builder.fetch_published,
                                       server(TEN_PUBLISHED, decimal=1))
         and 'not a list' in refusal(builder.fetch_published,
                                     lambda: {'data': 'no'}),
         "a row stamped one hour after midnight, a day served twice, a "
         "value of 50.5, and a reply with no rows are each REFUSED")

    print("\n(e) THE FREEZE: written once, verified, never overwritten.")
    room = os.path.join(WORK, 'freeze')
    write_freeze(room, TEN, first_ms=T0, days=10)
    ok0, lines0 = verify(room, rows_owed=10)
    mark(ok0 and sorted(os.listdir(room)) == ['.gitattributes',
                                              'MANIFEST.json',
                                              'fear_greed.csv']
         and held(read_rows, os.path.join(room, FILE_NAME)) == TEN,
         "one file, a manifest and the do-not-touch line are written; the "
         "verifier says INTACT; the file reads back identical", f"{lines0}")
    with open(os.path.join(room, FILE_NAME), 'rb') as handle:
        frozen_bytes = handle.read()
    mark(frozen_bytes == csv_bytes(TEN) and b'\r' not in frozen_bytes
         and frozen_bytes.startswith(b'day,value,label,carried\n'),
         "the frozen file is the header and one line a day, with no "
         "carriage return in it")
    mark('already holds a freeze' in refusal(write_freeze, room, TEN,
                                             first_ms=T0, days=10)
         and verify(room, rows_owed=10)[0],
         "A SECOND FREEZE INTO THE SAME FOLDER IS REFUSED and the first is "
         "untouched")
    bad_room = os.path.join(WORK, 'bad')
    mark('9 days' in refusal(write_freeze, bad_room, TEN[:-1], first_ms=T0,
                             days=10) and not os.path.exists(bad_room),
         "a freeze a day short: NOTHING is written")
    built = os.path.join(WORK, 'built')
    full = made_up(DAYS, salt=2, first_ms=FIRST_MS, before=2000)
    full = {k: v for n, (k, v) in enumerate(sorted(full.items()))
            if n not in (2100, 2500, 2501)}          # three silent days
    said = []
    died = refusal(builder.build, built, get=server(full), out=said.append)
    said_text = '\n'.join(str(line) for line in said)
    rows_built = held(read_rows, os.path.join(built, FILE_NAME))
    mark(died == '' and verify(built)[0] and isinstance(rows_built, list)
         and len(rows_built) == 1094 and sum(r[3] for r in rows_built) == 3
         and rows_built == build_rows(full),
         "THE BUILDER, WHOLE, AGAINST A FAKE SERVER holding seven made-up "
         "years with three silent days in the window: it freezes exactly "
         "1,094 rows, three of them carried, and the verifier says INTACT",
         died or f"{verify(built)[1]}")
    mark(died == '' and '1094' in said_text and FIRST_DAY in said_text
         and '3 carried' in said_text
         and not any(label in said_text for label in LABELS)
         and not any(f' {value} ' in said_text or f'={value}' in said_text
                     for value in range(0, 101) if value not in (3, 1)),
         "and the builder PRINTED NO VALUE AND NO LABEL: the row count, the "
         "dates, how many days were carried, and a checksum",
         said_text.replace('\n', ' | ')[:150])
    mark('already holds a freeze' in refusal(builder.build, built,
                                             get=server(full),
                                             out=lambda *a: None),
         "the builder REFUSES to run a second time")
    holes = {k: v for n, (k, v) in enumerate(sorted(full.items()))
             if not 2200 <= n < 2204}
    nowhere = os.path.join(WORK, 'nowhere')
    mark('in a row' in refusal(builder.build, nowhere, get=server(holes),
                               out=lambda *a: None)
         and not os.path.exists(nowhere),
         "a server silent for FOUR days running: the builder refuses and "
         "freezes nothing")

    print("\n(f) THE VERIFIER, against four kinds of damage.")

    def damaged(how):
        copy = os.path.join(WORK, f'damage_{how}')
        shutil.copytree(room, copy)
        target = os.path.join(copy, FILE_NAME)
        if how == 'digit':
            with open(target, 'rb') as handle:
                data = bytearray(handle.read())
            at = data.index(b',', data.index(b'\n') + 1) + 1
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
        return copy, verify(copy, rows_owed=10)

    digit_room, (digit_ok, digit_lines) = damaged('digit')
    mark(not digit_ok and 'DOES NOT MATCH' in ' '.join(digit_lines)
         and 'does not match its checksum' in refusal(load, digit_room, T0,
                                                      10)
         and 'not intact' in refusal(preflight, digit_room, T0, 10, 10),
         "ONE DIGIT of one value changed (the file the same length): NOT "
         "INTACT, the file REFUSES TO LOAD, and the pre-flight refuses",
         f"{digit_lines}")
    mark(not damaged('missing')[1][0] and not damaged('extra')[1][0]
         and not damaged('nomanifest')[1][0]
         and not verify(os.path.join(WORK, 'never_made'))[0]
         and not verify(room)[0] and verify(room, rows_owed=10)[0],
         "a missing file, an unlisted file, a missing manifest, a folder "
         "that does not exist, and an intact freeze of the WRONG LENGTH (10 "
         "rows where 1,094 are owed): each NOT INTACT, none a crash")
    loaded = held(load, room, T0, 10)
    mark(isinstance(loaded, tuple)
         and loaded[0] == [T0 + n * DAY_MS for n in range(10)]
         and loaded[1] == [row[1] for row in TEN]
         and loaded[2] == [LABELS[row[2]] for row in TEN]
         and held(preflight, room, T0, 10, 10) == loaded,
         "an intact freeze loads as days, values and SIDES - the "
         "publisher's label turned into -1, 0 or +1 - and the pre-flight "
         "hands back the same")

    print("\n(g) >>> THE JOIN, BY HAND. This is where a leak would live.")

    def candles(days, first='2030-01-01', freq='1D'):
        index = pd.date_range(first, periods=days, freq=freq)
        return pd.DataFrame({'open': 100.0, 'high': 101.0, 'low': 99.0,
                             'close': 100.5}, index=index)

    D = [T0, T0 + DAY_MS, T0 + 2 * DAY_MS]
    V, SIDE = [10, 50, 90], [-1, 0, 1]
    plain = candles(3)
    joined = held(attach, plain, D, V, SIDE)
    mark(not isinstance(joined, str)
         and list(joined['mood']) == [10.0, 50.0, 90.0]
         and list(joined['mood_side']) == [-1.0, 0.0, 1.0]
         and list(joined.columns) == ['open', 'high', 'low', 'close',
                                      'mood', 'mood_side']
         and 'mood' not in plain.columns,
         "THE VALUE STAMPED DAY D IS ON THE CANDLE THAT OPENS ON DAY D: "
         "three days of 10 (fear), 50 (neutral), 90 (greed) sit on their "
         "own three candles, in two new columns — and the candles handed "
         "in are not changed")
    late = held(attach, candles(3, first='2030-01-02'), D, V, SIDE)
    early = held(attach, candles(3, first='2029-12-31'), D, V, SIDE)
    mark(not isinstance(late, str) and not isinstance(early, str)
         and list(late['mood'])[:2] == [50.0, 90.0]
         and math.isnan(list(late['mood'])[2])
         and math.isnan(list(early['mood'])[0])
         and list(early['mood'])[1:] == [10.0, 50.0]
         and math.isnan(list(early['mood_side'])[0]),
         "candles that start a day LATER or a day EARLIER than the freeze "
         "still get their OWN day's value - nothing slides - and a candle "
         "the freeze does not cover is left EMPTY, not filled")
    mark('DAILY candles' in refusal(attach, candles(6, freq='4h'), D, V, SIDE)
         and 'DAILY candles' in refusal(
             attach, candles(3, first='2030-01-01 04:00'), D, V, SIDE)
         and 'DAILY candles' in refusal(
             attach, candles(3).drop(candles(3).index[1]), D, V, SIDE),
         "4-hour candles, daily candles that open at 04:00, and daily "
         "candles with a day missing are each REFUSED")
    days40 = [T0 + n * DAY_MS for n in range(40)]
    v40 = [(n * 13) % 101 for n in range(40)]
    s40 = [LABELS[label_of(value)] for value in v40]
    poisoned = v40[:25] + [(value + 17) % 101 for value in v40[25:]]
    clean40 = held(attach, candles(40), days40, v40, s40)
    dirty40 = held(attach, candles(40), days40, poisoned, s40)
    cut = held(attach, candles(25), days40, v40, s40)
    mark(not isinstance(clean40, str) and not isinstance(dirty40, str)
         and list(clean40['mood'])[:25] == list(dirty40['mood'])[:25]
         and all(a != b for a, b in zip(list(clean40['mood'])[25:],
                                        list(dirty40['mood'])[25:]))
         and list(cut['mood']) == list(clean40['mood'])[:25],
         ">>> THE POISON TEST: every value from day 26 on is changed, and "
         "NOT ONE of the first 25 candles' mood moves - while all 15 after "
         "do; and the first 25 candles joined on their own carry the same "
         "figures as inside the 40")

    print("\n(h) >>> THE SABOTAGE DRILL, PERMANENT. INERT IS A FAIL.")

    def witness():
        answer = held(attach, candles(3), D, V, SIDE)
        gap_rows = held(build_rows, without(TEN_PUBLISHED, 4), T0, 10)
        return (
            str(list(answer['mood'])) if not isinstance(answer, str)
            else answer,
            str(gap_rows[4][1:]) if isinstance(gap_rows, list) else gap_rows,
            refusal(check_rows, four, T0, 10)[:10],
            refusal(check_rows, twelve, T0, 40)[:10],
            refusal(check_rows, changed(TEN, 3, value=101), T0, 10)[:10],
            refusal(check_rows, changed(TEN, 3, label='Panic'), T0, 10)[:10],
            verify(digit_room, rows_owed=10)[0],
            refusal(write_freeze, room, TEN, first_ms=T0, days=10)[:12],
            str(held(load, room, T0, 10)[2]),
            refusal(check_rows, twice, T0, 10)[:10],
        )

    HONEST = witness()
    EXPECTED = ('[10.0, 50.0, 90.0]', str(TEN[3][1:3] + (1,)), 'ValueError',
                'ValueError', 'ValueError', 'ValueError', False,
                'RuntimeError', str([LABELS[row[2]] for row in TEN]),
                'ValueError')
    G = globals()
    _keep = {name: G[name] for name in
             ('attach', 'build_rows', 'MAX_CARRIED_RUN', 'MAX_CARRIED',
              'LABELS', '_sha', 'check_rows', 'day_text')}
    _real_listdir = os.listdir

    def _yesterday(df, days_ms, values, sides):
        return _keep['attach'](df, [d + DAY_MS for d in days_ms], values,
                               sides)

    def _tomorrow(df, days_ms, values, sides):
        return _keep['attach'](df, [d - DAY_MS for d in days_ms], values,
                               sides)

    def _carry_next(published, first_ms=None, days=None):
        rows = _keep['build_rows'](published, first_ms, days)
        return [rows[n + 1][:1] and (row[0],) + rows[n + 1][1:3] + (1,)
                if row[3] and n + 1 < len(rows) else row
                for n, row in enumerate(rows)]

    def _recorded(path):
        with open(os.path.join(os.path.dirname(path), MANIFEST_NAME),
                  encoding='utf-8') as handle:
            return json.load(handle)['files'][os.path.basename(path)][
                'sha256']

    FLIPPED = dict(LABELS)
    FLIPPED['Fear'] = 1
    BREAKS = [
        ('D1', "each candle carrying TOMORROW's mood", 'attach', _tomorrow),
        ('D2', "each candle carrying YESTERDAY's mood", 'attach', _yesterday),
        ('D3', "a silent day taking the NEXT day's value", 'build_rows',
         _carry_next),
        ('D4', 'any number of silent days in a row accepted',
         'MAX_CARRIED_RUN', 999),
        ('D5', 'any number of carried days accepted', 'MAX_CARRIED', 999),
        ('D6', '"Fear" counted as greed', 'LABELS', FLIPPED),
        ('D7', 'the verifier trusting the manifest, not the file', '_sha',
         _recorded),
        ('D8', 'the shape check switched off', 'check_rows',
         lambda rows, first_ms=None, days=None: None),
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
        good = was_changed and broken_answer != EXPECTED
        mark(good, f"{tag} {words:<50} -> "
                   f"{'CAUGHT' if good else 'INERT — IT CHANGED NOTHING'}")
    os.listdir = lambda path: []                # "nothing is there yet"
    try:
        b9 = witness()
    except Exception:                                      # noqa: BLE001
        b9 = '<crashed>'
    finally:
        os.listdir = _real_listdir
    mark(b9 != HONEST and b9 != EXPECTED,
         f"D9 {'the freeze believing its folder is empty':<50} -> "
         f"{'CAUGHT' if b9 != HONEST else 'INERT — IT CHANGED NOTHING'}")
    mark(all(G[name] is original for name, original in _keep.items())
         and os.listdir is _real_listdir and witness() == HONEST == EXPECTED,
         "and after nine breaks everything is what it started as, and the "
         "ten witnessed answers equal the ten typed out here")

    print("\n(i) NOTHING REAL WAS TOUCHED, AND THE GATE COUNTS ITSELF.")
    shutil.rmtree(WORK, ignore_errors=True)
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        production = handle.read().split("if __name__ == '__main__':")[0]
    mark((sorted(os.listdir(MOOD_DIR)) if os.path.isdir(MOOD_DIR)
          else None) == REAL_BEFORE
         and not any(word in production for word in
                     ('requests', 'urllib', 'http', 'socket', 'print('))
         and 'import build_mood_vault' not in production,
         "the real frozen folder is exactly as it was; and the reading "
         "half of this file names no network library, does not import the "
         "builder, and has no `print` in it at all")
    mark(len(BREAKS) + 1 == 9, "nine breaks, counted against a number "
                               "typed out here")
    EXPECTED_CHECKS = 42
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.5-D PASSED — {len(nonlocal_ok)} checks, 0 red.

THE FREEZE HAS ONE SHAPE AND REFUSES EVERY OTHER: a day short, twice or
out of order; a value outside 0 to 100 or not a whole number; a label
that is not the publisher's exact words. A day the publisher skipped
carries THE DAY BEFORE and is marked; four in a row, or twelve in all,
is a refusal.

THE VERIFIER CAUGHT one changed digit, a missing file, an unlisted
file, a missing manifest and a freeze of the wrong length.

THE JOIN PUTS THE VALUE STAMPED DAY D ON THE CANDLE OF DAY D; with
every value after a chosen day changed, no earlier candle moved.

WHAT THIS GATE DOES **NOT** PROVE. It has never seen a real index
value. It cannot say the publisher's history is what was published on
the day, or that a value stamped day D really was out at the start of
day D in 2023 - that was measured once, live, on 2026-11-16.""")
    else:
        print(f"GATE 6.5-D FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
