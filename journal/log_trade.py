"""
Zar X journal compartment — the trade logger (Phase 5, first half).

One command the Commander runs after he closes a trade. It asks him TEN
things in plain words — which coin, long or short, the price he got in at,
the price he got out at, where his stop was, how big in DOLLARS, how big his
account was in DOLLARS, how many hours ago he got in, WHY he took it in one
line, and how he felt in one word — and it appends what he said to
`journal/my_trades.csv`.

**IT WAS SEVEN QUESTIONS UNTIL 2026-11-15.** The Mirror was asked to compare
his trades with the same trades sized to risk 1% of his account, and three
of the figures that needs were never asked: his stop, his account, and when
he got in. A fourth was never DEFINED: whether `size` meant coins or dollars.
The Commander ruled on all four that day — ask them, and size is DOLLARS —
which is why the column is now called `size_usd`.

**IT NEVER JUDGES.** Not a verdict, not a score, not a profit figure, not a
word of encouragement. The grading is `journal/mirror.py`'s job. A logger
that told him "nice trade" at the moment he typed it would be teaching him
what to type.

**APPEND-ONLY, AND IT NEVER REWRITES HISTORY.** This file may only ever add a
line to the end. A sabotage on 2026-07-29 deleted thirty-four rows of a real
archive and printed a report that was entirely TRUE about what was left, and
that is the shape this rule exists to make impossible.

**>>> DUPLICATES ARE LEGITIMATE HERE AND ARE NEVER REFUSED, WHICH IS THE
OPPOSITE OF EVERY OTHER RECORDER ON THIS SHIP.** A pilot can genuinely make
the same trade twice in one day, at the same price, in the same size. A
logger that silently swallowed the second one would erase a real trade.

**HIS OWN WORDS ARE THE PAYLOAD AND A COMMA MUST NOT BE ABLE TO DESTROY A
ROW.** The `csv` module writes every row — never a string join — and **the
WHY line is not touched in any way at all**: not stripped, not escaped, not
"made safe". It comes back out of the file byte for byte.

**THE NUMBERS ARE KEPT AS HE TYPED THEM.** `100.50` is stored as `100.50` and
never as `100.5`. A `Decimal` is built to CHECK each number and is then
thrown away.

**A REFUSED ENTRY WRITES NOTHING AT ALL.** Every field is checked before the
file is opened, so a refusal cannot leave a half-written row and cannot even
create the file.

**THE STOP MAY BE THE WORD `none`.** A pilot sometimes trades without one,
and refusing the trade would teach him to invent a stop. **A stop on the
WRONG SIDE of the entry is refused by name** — a long is given up below its
entry and a short above it — because the likeliest way to produce one is
typing the exit and the stop in each other's place, which would silently turn
the Mirror's risk arithmetic upside down.

LAW 2 — the compartment owns its sources: the asset names, the two
directions, the column order and the path all live in THIS file and nowhere
else. It imports nothing from `config.py`.

LAW 3 — the doorway never raises and never prints; it RETURNS. Every failure
becomes one honest, NAMED line the Commander can read and act on.

**THE ASSET IS STORED UNDER THE SHIP'S SNAPSHOT NAME** — `BTC-USD`, not `BTC`
— because every snapshot row says it that way and the Mirror joins on it.

**EVERY STAMP IS UTC WITH THE ZONE ON IT.** The stamp is the moment he LOGGED
the trade. `in_hours_ago` counts back from that same moment to when he got
in, and the Mirror does the subtraction.

Standalone use:
    python journal/log_trade.py          (asks the ten questions)
    python journal/log_trade.py --gate   (gate 5.1-R3, including the drill)
"""
import csv
import io
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
TRADES_FILE = os.path.join(JOURNAL_DIR, 'my_trades.csv')

# The column order. It is read by the Mirror and by the Commander in a
# spreadsheet, so it is written down once, here, and the gate types out its
# own copy rather than importing this one. **THE MIRROR TYPES OUT ITS OWN
# COPY TOO, AND REFUSES A JOURNAL WHOSE HEADER IS NOT THIS ONE.**
FIELDS = ('utc_time', 'asset', 'direction', 'entry', 'exit', 'stop',
          'size_usd', 'account_usd', 'in_hours_ago', 'why', 'feeling')

# Law 2. The SHORT name is what the Brief prints; the FULL name is what every
# snapshot row already says and what is stored.
ASSETS = (('BTC', 'BTC-USD'), ('ETH', 'ETH-USD'), ('SOL', 'SOL-USD'))
DIRECTIONS = ('long', 'short')

NO_STOP = 'none'                           # the word stored when he had none
STAMP_SHAPE = '%Y-%m-%dT%H:%M:%S+00:00'    # UTC, with the zone spelled out


class TradeRefused(Exception):
    """A refusal this compartment turns into a NAMED line on his screen.

    Its message is written to be read by the Commander, not by a programmer:
    it is printed verbatim inside `[not logged: ...]`.
    """


def _text(value):
    """Anything at all -> a string, without ever raising. `None` becomes the
    empty string so that a missing answer is refused BY NAME rather than
    exploding somewhere further down."""
    return '' if value is None else str(value)


def _asset(value, assets):
    """What he typed -> the ship's snapshot name for that coin."""
    typed = _text(value).strip()
    if not typed:
        raise TradeRefused('no asset was given')
    key = typed.upper()
    for short, full in assets:
        if key == short.upper() or key == full.upper():
            return full
    raise TradeRefused(f'unknown asset {typed!r}')


def _direction(value, directions):
    """long or short, in any case he likes. Nothing else is a direction."""
    typed = _text(value).strip()
    if not typed:
        raise TradeRefused('no direction was given')
    if typed.lower() in directions:
        return typed.lower()
    raise TradeRefused(f'direction must be long or short, not {typed!r}')


def _number(value, which, kind):
    """A number he typed -> THE SAME STRING HE TYPED, once it is proved to be
    a real, finite, positive number.

    The `Decimal` built here is a doorman, not a converter: it is looked at
    and thrown away. `Decimal` accepts `NaN` and `Infinity` without complaint
    and neither of those is a price, so being a number is not enough.
    """
    typed = _text(value).strip()
    if not typed:
        raise TradeRefused(f'no {which} was given')
    try:
        number = Decimal(typed)
    except (InvalidOperation, ValueError):
        raise TradeRefused(f'the {which} {typed!r} is not a number')
    if not number.is_finite():
        raise TradeRefused(f'the {which} {typed!r} is not a number')
    if number <= 0:
        raise TradeRefused(f'a {which} of {typed} is not {kind}')
    return typed


def _stop(value, direction, entry):
    """Where he would have given up -> the same string he typed, or `none`.

    `direction` and `entry` are the values ALREADY CHECKED by the two
    functions above, so the comparison here is between two real numbers.

    **THE SIDE IS CHECKED AND IT IS THE ONLY CROSS-FIELD CHECK IN THIS
    FILE.** A long with its stop at or above the entry, or a short with its
    stop at or below, is refused: the Mirror divides by the gap between the
    two, and a swapped pair would print a confident risk figure for a trade
    that never had that risk.
    """
    typed = _text(value).strip()
    if not typed:
        raise TradeRefused('no stop was given (type none if you had no stop)')
    if typed.lower() == NO_STOP:
        return NO_STOP
    kept = _number(typed, 'stop', 'a price')
    stop, price = Decimal(kept), Decimal(entry)
    if direction == 'long' and stop >= price:
        raise TradeRefused(f'a stop of {kept} is not BELOW the entry of '
                           f'{entry}, and a long is given up below its entry')
    if direction == 'short' and stop <= price:
        raise TradeRefused(f'a stop of {kept} is not ABOVE the entry of '
                           f'{entry}, and a short is given up above its '
                           f'entry')
    return kept


def _hours(value):
    """How many hours ago he got in -> the same string he typed.

    **ZERO IS A REAL ANSWER** — "just now" — so this is the one number in the
    file whose turnover is BELOW zero rather than at it.
    """
    typed = _text(value).strip()
    if not typed:
        raise TradeRefused('no hours were given')
    try:
        number = Decimal(typed)
    except (InvalidOperation, ValueError):
        raise TradeRefused(f'the hours {typed!r} are not a number')
    if not number.is_finite():
        raise TradeRefused(f'the hours {typed!r} are not a number')
    if number < 0:
        raise TradeRefused(f'{typed} hours ago is in the future')
    return typed


def _why(value):
    """His one line, UNTOUCHED. The only thing asked of it is that it is not
    blank. Nothing is stripped, escaped or 'made safe' — the `csv` module
    handles every character, and a WHY line that came back changed would be
    him being quietly corrected by his own notebook."""
    typed = _text(value)
    if not typed.strip():
        raise TradeRefused('the WHY line is empty')
    return typed


def _feeling(value):
    """One word, stored lower-cased.

    Lower-cased because the Mirror groups by it, and `Nervous` and `nervous`
    must not become two different feelings in his own record.
    """
    typed = _text(value).strip()
    words = typed.split()
    if not words:
        raise TradeRefused('no feeling was given')
    if len(words) > 1:
        raise TradeRefused(f'the feeling must be ONE word, not {typed!r}')
    return words[0].lower()


def _stamp(now):
    """The moment -> the text in the row. Always UTC, always with the zone.

    A naive time is REFUSED rather than guessed at: guessing is how a row
    written in Karachi and a snapshot written in a datacentre end up five
    hours apart with nothing on either of them saying so.
    """
    moment = datetime.now(timezone.utc) if now is None else now
    if moment.tzinfo is None or moment.tzinfo.utcoffset(moment) is None:
        raise TradeRefused('the time given has no timezone on it')
    return moment.astimezone(timezone.utc).strftime(STAMP_SHAPE)


def _validate(asset, direction, entry, exit_price, stop, size, account,
              hours_ago, why, feeling, assets, directions, now):
    """The ten answers -> the eleven values of one row, or a NAMED refusal.

    **NOTHING IS OPENED, CREATED OR WRITTEN ANYWHERE IN HERE.** Every check
    happens before the journal is touched at all, which is what makes "a
    refused entry writes nothing" true rather than merely intended.
    """
    stamp = _stamp(now)
    coin = _asset(asset, assets)
    side = _direction(direction, directions)
    price_in = _number(entry, 'entry price', 'a price')
    price_out = _number(exit_price, 'exit price', 'a price')
    return [stamp, coin, side, price_in, price_out,
            _stop(stop, side, price_in),
            _number(size, 'size', 'a size'),
            _number(account, 'account size', 'an amount'),
            _hours(hours_ago),
            _why(why),
            _feeling(feeling)]


def _row_text(values):
    """Values -> the exact characters that will land in the file.

    Built through `csv` into memory FIRST so that the whole row reaches the
    disk in a single write, and so that nothing has to be guessed about what
    a comma or a quote in his own words is going to do to it.
    """
    buffer = io.StringIO(newline='')
    csv.writer(buffer).writerow(values)
    return buffer.getvalue()


def _needs_header(path):
    """A header goes on a journal that does not exist yet, or one that exists
    and is empty. Never on one that already has rows in it."""
    if not os.path.exists(path):
        return True
    return os.path.getsize(path) == 0


def _append(path, text):
    """The only write in this part. Mode `a` — **there is no code path in
    this file that can open the journal for writing any other way.**

    `newline=''` is not decoration: without it, Windows turns the `csv`
    module's own line ending into `\\r\\r\\n` and every row in the archive is
    quietly malformed.
    """
    with open(path, 'a', newline='', encoding='utf-8') as handle:
        handle.write(text)


def _not_logged(reason):
    """A trade that was NOT recorded, named. Never a shrug, never silence."""
    return f'[not logged: {reason}]'


def _logged_words(values):
    """What he sees after a trade goes in: the row read back to him, and
    NOT ONE WORD MORE.

    **No verdict, no profit, no encouragement.** The plan forbids judgement at
    entry time in as many words, and this line is the only place a judgement
    could ever appear.
    """
    (stamp, asset, direction, entry, exit_price, stop, size, account, hours,
     _why_, feeling) = values
    return (f'logged: {asset} {direction} {entry} -> {exit_price}, '
            f'stop {stop}, size ${size}, account ${account}, '
            f'in {hours} hours ago, feeling {feeling}, at {stamp}')


def log_trade(asset, direction, entry, exit_price, stop, size, account,
              hours_ago, why, feeling,
              path=None, assets=None, directions=None, now=None):
    """THE DOORWAY. One trade in, one honest line out.

    Never raises and never prints; it RETURNS. The four settings resolve from
    None IN THE BODY rather than being frozen into the signature at import
    time, so a caller can replace any of them and this module's own constants
    are read fresh on every call.
    """
    try:
        path = TRADES_FILE if path is None else path
        assets = ASSETS if assets is None else assets
        directions = DIRECTIONS if directions is None else directions

        try:
            values = _validate(asset, direction, entry, exit_price, stop,
                               size, account, hours_ago, why, feeling,
                               assets, directions, now)
        except TradeRefused as exc:
            return _not_logged(str(exc))

        text = _row_text(values)
        if _needs_header(path):
            text = _row_text(list(FIELDS)) + text
        _append(path, text)
        return _logged_words(values)
    except OSError as exc:
        return _not_logged(f'the journal could not be written '
                           f'({type(exc).__name__})')
    except Exception as exc:
        return _not_logged(type(exc).__name__)
if __name__ == '__main__':
    if '--gate' not in sys.argv:
        # THE SHELL. **The only place in this file that calls `input()` or
        # `print()` outside the gate.**
        #
        # **>>> THIS BLOCK IS UNDER A CHECK.** Check (n) runs these ten
        # questions THREE TIMES on every gate run - tidy answers, awkward
        # answers, and a blank last answer - and proves each answer reaches
        # the column of its own name. Reorder them freely; that is not a
        # fault. **RENAME one, or ADD an eleventh, and the gate goes RED** -
        # deliberately, so that a change to the only surface between his
        # fingers and his archive is made by somebody who has looked. The
        # words are typed out in the check; teaching it a new question is
        # one line, made on purpose.
        print()
        print("ZAR X — log a trade you have CLOSED. Ten questions.")
        print("Nothing here judges the trade. That is the Mirror's job.")
        print("Press Ctrl+C to walk away; nothing is written until all ten")
        print("are answered.")
        print()
        try:
            answers = (
                input("  which coin?  (BTC / ETH / SOL)             : "),
                input("  long or short?                             : "),
                input("  price you got IN at                        : "),
                input("  price you got OUT at                       : "),
                input("  where was your STOP? (price, or none)      : "),
                input("  how big? (size in DOLLARS)                 : "),
                input("  account size then? (DOLLARS)               : "),
                input("  how many HOURS ago did you get IN?         : "),
                input("  WHY did you take it? (one line)            : "),
                input("  how did you feel? (ONE word)               : "),
            )
        except (KeyboardInterrupt, EOFError):
            print()
            print("  nothing was written.")
            sys.exit(0)
        print()
        print("  " + log_trade(*answers))
        print(f"  journal: {TRADES_FILE}")
        print()
        sys.exit(0)

    # =====================================================================
    # GATE 5.1-R3 — declared in PROGRESS_LOG.md on 2026-11-15 and committed
    # with no `.py` in that commit, BEFORE the ten-question shape existed.
    # It carries forward every condition of GATE 5.1 (2026-08-19), 5.1-R1
    # (2026-08-20) and 5.1-R2 (2026-09-08), re-proved on the new shape.
    #
    # Everything below lives inside `__main__` on purpose: the production
    # half above is untouched by any of it.
    #
    # **THE GATE NEVER TOUCHES `journal/my_trades.csv`.** Every check writes
    # into a temporary directory it makes and removes itself.
    # =====================================================================
    import hashlib
    import shutil
    import subprocess
    import tempfile
    import threading
    from datetime import timedelta

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def show(label, expected, got):
        print(f"     ---- the gate expected ({label}) ----")
        print(f"     {expected!r}")
        print("     ---- what is actually on the disk ----")
        print(f"     {got!r}")

    def same(label, expected, got):
        ok = expected == got
        if not ok:
            show(label, expected, got)
        return ok

    # ---- THE GATE'S OWN CLOCK, ITS OWN DISK AND ITS OWN BYTES ------------
    # Nothing below asks the module to build anything the gate then judges.
    # Every expectation is typed out here, character for character.
    WHEN = datetime(2026, 8, 20, 9, 30, 15, tzinfo=timezone.utc)
    WHEN_TEXT = '2026-08-20T09:30:15+00:00'      # typed here, not read
    NL = chr(13) + chr(10)
    HEADER = ('utc_time,asset,direction,entry,exit,stop,size_usd,'
              'account_usd,in_hours_ago,why,feeling' + NL)
    COLUMNS = 11

    WORK = tempfile.mkdtemp(prefix='zarx_gate51_')

    def fresh(name='my_trades.csv'):
        """A journal path in a directory of its own, with nothing in it."""
        room = tempfile.mkdtemp(prefix='zarx_g51_', dir=WORK)
        return os.path.join(room, name)

    def disk(path):
        if not os.path.exists(path):
            return None
        with open(path, 'rb') as handle:
            return handle.read()

    def records(raw):
        """Bytes -> csv records. `[]` for nothing at all, so that a check
        standing on a file that was never written goes RED and carries on
        instead of raising (rule (k); R-084 was this, in check (j))."""
        if raw is None:
            return []
        try:
            return list(csv.reader(io.StringIO(raw.decode('utf-8'),
                                               newline='')))
        except (UnicodeDecodeError, csv.Error):
            return []

    def fingerprint(path):
        raw = disk(path)
        return 'NO FILE' if raw is None else hashlib.sha256(raw).hexdigest()

    # **THE REAL JOURNAL, FINGERPRINTED BEFORE THE FIRST CHECK RUNS.** Until
    # 2026-11-15 the closing check was `not os.path.exists(TRADES_FILE)` -
    # which would have turned this gate RED FOR EVER on the day he logged
    # his first real trade. The question was never "does it exist". It is
    # "did this gate change it".
    REAL_JOURNAL_AT_START = fingerprint(TRADES_FILE)

    GOOD = dict(asset='BTC', direction='long', entry='100.50',
                exit_price='111.00', stop='95.25', size='250.00',
                account='10000', hours_ago='30',
                why='trend was up and I waited for the pullback',
                feeling='calm')

    # THE ROW, TYPED OUT BY HAND. Not built by calling anything under test.
    GOOD_ROW = ('2026-08-20T09:30:15+00:00,BTC-USD,long,100.50,111.00,95.25,'
                '250.00,10000,30,trend was up and I waited for the pullback,'
                'calm' + NL)

    print("=" * 70)
    print("GATE 5.1-R3 — THE TRADE LOGGER, TEN QUESTIONS. Declared before")
    print("the ten-question shape existed; carries every earlier condition.")
    print("=" * 70)

    print("\n(a) ONE DOORWAY THAT NEVER RAISES AND NEVER PRINTS, WITH EVERY"
          "\n    SETTING RESOLVED FROM `None` IN THE BODY.")
    path = fresh()
    said = log_trade(path=path, **GOOD)
    mark(isinstance(said, str) and said.startswith('logged: '),
         "the doorway RETURNED a plain-words line rather than raising",
         said)
    TEN = ('asset', 'direction', 'entry', 'exit_price', 'stop', 'size',
           'account', 'hours_ago', 'why', 'feeling')
    hostile = [
        ('every field None', {name: None for name in TEN}),
        ('objects that are not text',
         dict(asset=object(), direction=[1], entry={}, exit_price=set(),
              stop=object(), size=(), account=[], hours_ago={},
              why=object(), feeling=object())),
        ('a path in a directory that does not exist',
         dict(GOOD, path=os.path.join(WORK, 'no_such_room', 'x.csv'))),
    ]
    for words, kw in hostile:
        args = dict(GOOD)
        args.update(kw)
        args.setdefault('path', fresh())
        try:
            answer = log_trade(**args)
            raised = False
        except Exception as exc:                       # noqa: BLE001
            answer, raised = f'{type(exc).__name__}: {exc}', True
        mark(not raised and isinstance(answer, str)
             and answer.startswith('[not logged: '),
             f"{words} -> a NAMED refusal, not an exception", answer)
    mark(log_trade.__defaults__ == (None, None, None, None),
         "and all four settings are `None` in the signature and resolved in "
         "the body — nothing is frozen at import time",
         f"defaults {log_trade.__defaults__}")

    print("\n(b) >>> EXACT EQUALITY ON THE BYTES READ BACK OFF THE DISK,"
          "\n    never on what the function SAYS it wrote.")
    path = fresh()
    log_trade(path=path, now=WHEN, **GOOD)
    mark(same('a new journal', (HEADER + GOOD_ROW).encode('utf-8'),
              disk(path)),
         "a new journal is EXACTLY one header line and one row of ELEVEN "
         "columns, byte for byte, against a copy typed out in this gate",
         f"{len(disk(path) or b'')} bytes on disk")
    raw = disk(path) or b''
    mark(raw.count(b'\r\n') == 2 and raw.count(b'\n') == 2
         and b'\r\r\n' not in raw,
         "the line endings are CRLF and NOT the `\\r\\r\\n` that Windows "
         "writes when `newline=''` is forgotten",
         f"CRLF {raw.count(NL.encode())}, bare LF "
         f"{raw.count(chr(10).encode()) - raw.count(NL.encode())}")
    mark(WHEN_TEXT in raw.decode('utf-8') and raw.decode('utf-8').count(
         '+00:00') == 1,
         "the stamp is UTC WITH THE ZONE ON IT, typed out in this gate "
         "rather than read from the file",
         WHEN_TEXT)
    path = fresh()
    KARACHI = timezone(timedelta(hours=5))
    log_trade(path=path, now=datetime(2026, 8, 20, 14, 30, 15,
                                      tzinfo=KARACHI), **GOOD)
    mark(same('the same moment, given in UTC+5',
              (HEADER + GOOD_ROW).encode('utf-8'), disk(path)),
         "and the SAME MOMENT handed over in Karachi's zone — 14:30:15+05:00 "
         "— lands as the IDENTICAL UTC row: the time is CONVERTED, never "
         "merely relabelled")

    print("\n(c) >>> THE ARCHIVE SURVIVES, PROVED AGAINST ROWS THIS GATE"
          "\n    WROTE ITSELF AND THE LOGGER HAS NEVER SEEN.")
    path = fresh()
    SEEDED = (HEADER
              + '2020-01-01T00:00:00+00:00,ETH-USD,short,1.00,2.00,none,3.00,'
                '4.00,5,a row the logger never wrote,bored' + NL
              + '2020-01-02T00:00:00+00:00,SOL-USD,long,4.00,5.00,3.50,6.00,'
                '7.00,8,and another one,tired' + NL)
    with open(path, 'wb') as handle:
        handle.write(SEEDED.encode('utf-8'))
    before_bytes = disk(path)
    log_trade(path=path, now=WHEN, **GOOD)
    after_bytes = disk(path)
    mark(after_bytes[:len(before_bytes)] == before_bytes,
         "every seeded byte is still there, in the same order, at the same "
         "offset — the new row was ADDED, not merged in",
         f"{len(before_bytes)} bytes before, {len(after_bytes)} after")
    mark(same('seeded + appended', SEEDED.encode('utf-8')
              + GOOD_ROW.encode('utf-8'), after_bytes),
         "and the whole file equals the seed plus exactly one new row, with "
         "NO SECOND HEADER, against a copy typed out here")
    path = fresh()
    with open(path, 'wb') as handle:
        handle.write(b'')
    log_trade(path=path, now=WHEN, **GOOD)
    mark(same('a journal that exists and is empty',
              (HEADER + GOOD_ROW).encode('utf-8'), disk(path)),
         "and a journal that already EXISTS but is EMPTY still gets its "
         "header")

    print("\n(d) >>> A REFUSED ENTRY WRITES NOTHING. Proved by sha256 before"
          "\n    and after, for EVERY refusal shape, on a journal that has"
          "\n    rows AND on one that does not exist — a refusal must not"
          "\n    even CREATE the file.")
    REFUSALS = [
        ('an unknown coin', dict(asset='XRP')),
        ('a coin left blank', dict(asset='')),
        ('a direction that is neither', dict(direction='sideways')),
        ('a direction left blank', dict(direction='   ')),
        ('an entry price that is words', dict(entry='about a hundred')),
        ('an exit price that is words', dict(exit_price='n/a')),
        ('a price of NaN, which Decimal accepts', dict(entry='NaN')),
        ('a price of Infinity', dict(exit_price='Infinity')),
        ('a price of zero', dict(entry='0')),
        ('a negative price', dict(exit_price='-5')),
        ('a size of zero', dict(size='0')),
        ('a negative size', dict(size='-1')),
        ('a size that is words', dict(size='a lot')),
        ('an empty WHY line', dict(why='')),
        ('a WHY line of only spaces', dict(why='     ')),
        ('a feeling of two words', dict(feeling='a bit nervous')),
        ('no feeling at all', dict(feeling='')),
        ('a time with no zone on it',
         dict(now=datetime(2026, 8, 20, 9, 30, 15))),
        # ---- the three new questions, 2026-11-15 ----
        ('a stop left blank', dict(stop='')),
        ('a stop that is words', dict(stop='below the low')),
        ('a stop of zero - NOT read as no stop', dict(stop='0')),
        ('a LONG with its stop ABOVE the entry', dict(stop='120.00')),
        ('a LONG with its stop AT the entry', dict(stop='100.50')),
        ('a SHORT with its stop BELOW the entry',
         dict(direction='short', stop='95.25')),
        ('an account of zero', dict(account='0')),
        ('an account that is words', dict(account='ten grand')),
        ('an account left blank', dict(account='')),
        ('hours left blank', dict(hours_ago='')),
        ('hours that are words', dict(hours_ago='yesterday')),
        ('hours of NaN', dict(hours_ago='NaN')),
        ('hours BELOW zero', dict(hours_ago='-1')),
    ]
    seeded_path = fresh()
    with open(seeded_path, 'wb') as handle:
        handle.write(SEEDED.encode('utf-8'))
    all_silent, all_named, names = True, True, []
    for words, kw in REFUSALS:
        args = dict(GOOD, now=WHEN)
        args.update(kw)
        empty_path = fresh()
        before_fp = fingerprint(seeded_path)
        answer_a = log_trade(path=seeded_path, **args)
        answer_b = log_trade(path=empty_path, **args)
        after_fp = fingerprint(seeded_path)
        wrote_nothing = (before_fp == after_fp
                         and fingerprint(empty_path) == 'NO FILE')
        named = (answer_a.startswith('[not logged: ')
                 and answer_a == answer_b)
        all_silent = all_silent and wrote_nothing
        all_named = all_named and named
        names.append(answer_a)
        print(f"        {words:<40} {answer_a}")
    mark(all_silent,
         f"all {len(REFUSALS)} refusal shapes wrote NOTHING — the seeded "
         f"journal's sha256 never moved once, and the empty path was never "
         f"even created",
         f"seeded sha256 still {fingerprint(seeded_path)[:16]}")

    print("\n(e) >>> EVERY REFUSAL NAMED SEPARATELY. SILENCE IS FORBIDDEN,"
          "\n    and so is one shrug covering six different things.")
    mark(all_named, "every refusal came back as its own `[not logged: ...]` "
                    "line, and the same input refused identically whether the "
                    "journal existed or not")
    REQUIRED_NAMES = ('unknown asset', 'no asset was given',
                      'direction must be long or short', 'is not a number',
                      'is not a price', 'is not a size',
                      'the WHY line is empty', 'must be ONE word',
                      'no feeling was given', 'has no timezone on it',
                      'no stop was given (type none if you had no stop)',
                      'a stop of 0 is not a price',
                      'is not BELOW the entry', 'is not ABOVE the entry',
                      'is not an amount', 'no account size was given',
                      'no hours were given', 'are not a number',
                      'hours ago is in the future')
    joined = ' | '.join(names)
    for needle in REQUIRED_NAMES:
        mark(needle in joined,
             f"the words {needle!r} are on his screen for the case that "
             f"earns them")
    mark(len(set(names)) >= 24,
         f"and the {len(REFUSALS)} shapes produced {len(set(names))} "
         f"DISTINCT sentences, not one catch-all")

    print("\n(f) >>> EVERY THRESHOLD AT THE EXACT VALUE WHERE IT TURNS OVER,"
          "\n    AND ONE STEP EITHER SIDE.")

    def landed(**kw):
        """-> the row that reached the disk, or None if nothing did."""
        args = dict(GOOD, now=WHEN)
        args.update(kw)
        spot = fresh()
        log_trade(path=spot, **args)
        raw = disk(spot)
        if raw is None:
            return None
        return raw.decode('utf-8')[len(HEADER):]

    def has(row, piece):
        return row is not None and piece in row

    mark(landed(size='0') is None
         and landed(size='0.00000000') is None
         and landed(size='-0.00000001') is None,
         "SIZE — zero is refused, and so is zero written eight decimal "
         "places long, and so is one hundred-millionth BELOW zero")
    mark(has(landed(size='0.00000001'), ',0.00000001,'),
         "and one hundred-millionth ABOVE zero is accepted and stored exactly "
         "as typed",
         (landed(size='0.00000001') or '').strip())
    mark(landed(entry='0') is None and landed(exit_price='0') is None
         and landed(entry='0.00000001', stop='none') is not None,
         "PRICE — the same turnover at zero, on BOTH prices")
    mark(landed(feeling='calm') is not None
         and landed(feeling='calm nervous') is None
         and landed(feeling='') is None,
         "FEELING — one word passes, two words are refused, none is refused")
    mark(has(landed(feeling='  calm  '), ',calm' + NL),
         "and one word wrapped in spaces is still ONE word")
    mark(landed(why='x') is not None and landed(why='') is None
         and landed(why=' ') is None,
         "WHY — a single character passes, empty and whitespace-only are "
         "refused")
    mark(has(landed(entry='100.50'), ',100.50,')
         and has(landed(entry='100.5'), ',100.5,'),
         "`100.50` is stored as `100.50` and `100.5` as `100.5`. The "
         "trailing zero he typed SURVIVES")
    mark(landed(stop='100.50') is None and landed(stop='100.51') is None
         and has(landed(stop='100.49'), ',100.49,'),
         "STOP ON A LONG (entry 100.50) — a stop AT the entry is refused, "
         "one cent ABOVE is refused, one cent BELOW is accepted: the "
         "turnover is the entry itself")
    mark(landed(direction='short', stop='100.50') is None
         and landed(direction='short', stop='100.49') is None
         and has(landed(direction='short', stop='100.51'), ',100.51,'),
         "STOP ON A SHORT (entry 100.50) — the mirror image: AT the entry "
         "refused, one cent BELOW refused, one cent ABOVE accepted")
    mark(has(landed(stop='none'), ',111.00,none,250.00,')
         and has(landed(stop='NONE'), ',111.00,none,250.00,')
         and has(landed(stop='  None '), ',111.00,none,250.00,')
         and has(landed(direction='short', stop='none'), ',none,'),
         "NO STOP — `none`, `NONE` and `  None ` are the same answer, stored "
         "as `none`, between the exit and the size, for a long and a short")
    mark(landed(stop='') is None and landed(stop='0') is None
         and landed(stop='nil') is None,
         "and a blank stop, a stop of `0` and any OTHER word are refused — "
         "none of them is quietly read as no stop")
    mark(has(landed(hours_ago='0'), ',10000,0,')
         and landed(hours_ago='-0.01') is None
         and has(landed(hours_ago='0.01'), ',10000,0.01,'),
         "HOURS — ZERO IS ACCEPTED (`just now`), one hundredth BELOW zero is "
         "refused, one hundredth above is accepted: the turnover is below "
         "zero, unlike every other number in this file")
    mark(landed(account='0') is None and landed(account='-1') is None
         and has(landed(account='0.01'), ',250.00,0.01,30,'),
         "ACCOUNT — zero and negative refused, one cent accepted")
    mark(has(landed(stop='95.250', account='10000.00', hours_ago='30.0'),
             ',95.250,250.00,10000.00,30.0,'),
         "and all three new numbers are kept EXACTLY AS TYPED — `95.250`, "
         "`10000.00`, `30.0` — nothing normalised behind him")
    mark(landed(size='20000', account='10000') is not None,
         "a size LARGER than the account is NOT refused — leverage exists "
         "and this file decides nothing on his behalf")

    print("\n(g) >>> A HOSTILE WHY LINE. A comma in his own words must not"
          "\n    be able to destroy a row.")
    HOSTILE = ('   =SUM(A1:A9), he said "buy the dip", then'
               + chr(10) + "I didn't, — 50% ماشاءالله   ")
    path = fresh()
    log_trade(path=path, now=WHEN, why=HOSTILE,
              **{k: v for k, v in GOOD.items() if k != 'why'})
    rows = records(disk(path))
    row = rows[1] if len(rows) > 1 else [''] * COLUMNS
    row = row + [''] * (COLUMNS - len(row))
    mark(len(rows) == 2 and len(rows[1]) == COLUMNS,
         "a WHY line carrying a comma, a double quote, a NEWLINE, a leading "
         "`=` and non-ASCII text still produces ONE row of ELEVEN columns",
         f"{len(rows)} rows, {len(rows[1]) if len(rows) > 1 else 0} columns "
         f"in the second")
    mark(row[9] == HOSTILE,
         "and his words come back BYTE-IDENTICAL — nothing stripped, nothing "
         "escaped, nothing 'made safe', the leading `=` still there",
         repr(row[9]))
    mark(row[9].startswith('   ') and row[9].endswith('   '),
         "INCLUDING THE SPACES AT BOTH ENDS",
         repr(row[9][:5]) + ' ... ' + repr(row[9][-5:]))
    mark(row[0] == WHEN_TEXT and row[1] == 'BTC-USD' and row[5] == '95.25'
         and row[6] == '250.00' and row[7] == '10000' and row[8] == '30'
         and row[10] == 'calm',
         "and every column AROUND it is still in its own place — the stamp, "
         "the coin, the stop, the size, the account, the hours, the feeling")
    raw = disk(path) or b''
    mark(raw.count(b'\r\n') == 2
         and raw.count(b'\n') - raw.count(b'\r\n') == 1
         and len(rows) == 2,
         "the newline he typed is INSIDE the quoted field: the file has TWO "
         "row terminators, not three — the row did not split in two")

    print("\n(h) >>> THE SAME TRADE TWICE IS TWO ROWS. A PILOT CAN GENUINELY"
          "\n    MAKE THE SAME TRADE TWICE.")
    path = fresh()
    first = log_trade(path=path, now=WHEN, **GOOD)
    second = log_trade(path=path, now=WHEN, **GOOD)
    mark(same('the same trade, logged twice',
              (HEADER + GOOD_ROW + GOOD_ROW).encode('utf-8'), disk(path)),
         "the identical trade is TWO IDENTICAL ROWS, byte for byte")
    mark(first == second and first.startswith('logged: '),
         "and he was told the same thing both times")

    print("\n(i) >>> DOOR 3. A FRESH INTERPRETER imports it, calls the"
          "\n    doorway three ways and SHUTS DOWN, and its TOTAL output must"
          "\n    be empty. A timeout is a FAILURE.")
    GATE_MODULE_NAME = 'journal.log_trade'
    GATE_MODULE_LEAF = 'log_trade.py'
    _ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    probe_dir = tempfile.mkdtemp(prefix='zarx_d3probe_')
    probe = os.path.join(probe_dir, 'seen.txt')
    child_journal = os.path.join(probe_dir, 'child.csv')
    PATHS = (
        "m.log_trade('BTC', 'long', '1', '2', '0.5', '3', '4', '5', 'why', "
        "'calm', path=P)",
        "m.log_trade('XRP', 'sideways', 'x', 'y', 'z', 'p', 'q', 'r', '', "
        "'', path=P)",
        "m.log_trade(None, None, None, None, None, None, None, None, None, "
        "None, path=P)",
    )
    body = ''.join('%s\nn += 1\n' % call for call in PATHS)
    child = ('import sys\n'
             'import %s as m\n' % GATE_MODULE_NAME +
             'P = sys.argv[2]\n'
             'n = 0\n' + body +
             "open(sys.argv[1], 'w', encoding='utf-8').write("
             'm.__file__ + chr(10) + str(n))\n')
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    timed_out, wrote, rc = False, b'', None
    try:
        done = subprocess.run([sys.executable, '-c', child, probe,
                               child_journal],
                              cwd=_ROOT_DIR, env=env, capture_output=True,
                              timeout=90)
        wrote, rc = done.stdout + done.stderr, done.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        wrote = (exc.stdout or b'') + (exc.stderr or b'')
    try:
        with open(probe, encoding='utf-8') as handle:
            seen = handle.read()
    except OSError:
        seen = ''
    parts = seen.split(chr(10))
    seen_file = parts[0] if parts else ''
    try:
        seen_n = int(parts[1])
    except (IndexError, ValueError):
        seen_n = -1
    mark(not timed_out, "the fresh interpreter SHUT DOWN on its own",
         f"return code {rc}")
    mark(os.path.basename(seen_file) == GATE_MODULE_LEAF
         and os.path.abspath(seen_file).startswith(os.path.abspath(_ROOT_DIR)),
         "the child imported THIS file — proved by a probe FILE, never by a "
         "stream, because the stream is the thing on trial",
         seen_file or '(the child wrote no probe)')
    mark(seen_n == len(PATHS),
         f"the child finished all {len(PATHS)} calls",
         f"it reported {seen_n}")
    mark(rc == 0 and wrote == b'',
         "IMPORT, three doorway calls and SHUTDOWN wrote nothing at all",
         '' if wrote == b'' else
         f"it wrote {wrote.decode('utf-8', 'replace')[:200]!r}")
    mark((disk(child_journal) or b'').count(b'\r\n') == 2,
         "and the one call that should have written DID write, in that other "
         "interpreter",
         f"{disk(child_journal)!r}"[:120])
    shutil.rmtree(probe_dir, ignore_errors=True)

    print("\n(j) >>> TWO FAKE TRADES, LOGGED AND CHECKED BY HAND HERE, BY TWO"
          "\n    ROUTES. The Mirror half of the plan's sentence — `run"
          "\n    mirror, numbers check out by hand` — is met in"
          "\n    `journal/mirror.py --gate`, which logs its fake trades"
          "\n    THROUGH THIS DOORWAY.")
    path = fresh()
    TRADE_ONE = dict(asset='eth', direction='SHORT', entry='2500.00',
                     exit_price='2410.25', stop='NONE', size='1500',
                     account='8000', hours_ago='6.5',
                     why='funding was extreme, faded it', feeling='Nervous')
    TRADE_TWO = dict(asset='SOL-USD', direction='Long', entry='140.10',
                     exit_price='138.00', stop='137.00', size='600',
                     account='8000', hours_ago='0',
                     why='breakout that failed', feeling='ANNOYED')
    LATER = datetime(2026, 8, 20, 17, 45, 0, tzinfo=timezone.utc)
    log_trade(path=path, now=WHEN, **TRADE_ONE)
    log_trade(path=path, now=LATER, **TRADE_TWO)
    BY_HAND = (HEADER
               + '2026-08-20T09:30:15+00:00,ETH-USD,short,2500.00,2410.25,'
                 'none,1500,8000,6.5,"funding was extreme, faded it",nervous'
               + NL
               + '2026-08-20T17:45:00+00:00,SOL-USD,long,140.10,138.00,'
                 '137.00,600,8000,0,breakout that failed,annoyed' + NL)
    mark(same('two fake trades', BY_HAND.encode('utf-8'), disk(path)),
         "ROUTE ONE — the whole file equals two rows typed out by hand here, "
         "character for character, INCLUDING the quotes the `csv` module put "
         "round the WHY line that has a comma in it")
    # **RULE (k), AND THIS LINE IS THE REPAIR OF R-084.** Until 2026-11-15
    # this check opened the file directly, and an edit that made the logger
    # refuse `SHORT` left the gate printing a traceback and no verdict.
    got = records(disk(path))
    EXPECT = [
        ['utc_time', 'asset', 'direction', 'entry', 'exit', 'stop',
         'size_usd', 'account_usd', 'in_hours_ago', 'why', 'feeling'],
        ['2026-08-20T09:30:15+00:00', 'ETH-USD', 'short', '2500.00',
         '2410.25', 'none', '1500', '8000', '6.5',
         'funding was extreme, faded it', 'nervous'],
        ['2026-08-20T17:45:00+00:00', 'SOL-USD', 'long', '140.10', '138.00',
         '137.00', '600', '8000', '0', 'breakout that failed', 'annoyed'],
    ]
    mark(got == EXPECT,
         "ROUTE TWO — read back field by field, every one of the twenty-two "
         "values equals a value typed out separately here: `eth` became "
         "`ETH-USD`, `SHORT` became `short`, `NONE` became `none`, `Nervous` "
         "became `nervous`, and `2500.00` kept its trailing zero",
         f"{max(len(got) - 1, 0)} trades, "
         f"{len(got[1]) if len(got) > 1 else 0} columns each")
    mark(disk(path) is not None
         and all(word not in disk(path).decode('utf-8').lower()
                 for word in ('profit', 'loss', 'win', 'good', 'bad',
                              'well done', 'mistake')),
         "and NOT ONE WORD OF JUDGEMENT reached the disk")
    said_one = log_trade(path=fresh(), now=WHEN, **TRADE_ONE)
    SAID_BY_HAND = ('logged: ETH-USD short 2500.00 -> 2410.25, stop none, '
                    'size $1500, account $8000, in 6.5 hours ago, feeling '
                    'nervous, at 2026-08-20T09:30:15+00:00')
    mark(said_one == SAID_BY_HAND,
         "and THE LINE HE READS BACK names all ten answers and NOT ONE WORD "
         "MORE — equal, character for character, to a line typed out here",
         said_one)

    print("\n(k) >>> THE SABOTAGE DRILL, PERMANENT. Every break is PROVED TO"
          "\n    CHANGE WHAT SOMEBODY READS OR WHAT LANDS ON DISK before its"
          "\n    verdict is counted. **A BREAK REPORTED `INERT` IS A FAIL.**")

    _honest = {name: globals()[name] for name in
               ('_validate', '_append', '_needs_header', '_row_text', '_why',
                '_number', '_stamp', '_asset', '_feeling', '_logged_words',
                '_stop', '_hours')}

    def w_disk():
        """Witnessed as BYTES ON DISK: trades, a genuine DUPLICATE, a trade
        with NO STOP typed in capitals, and two refusals."""
        spot = fresh()
        log_trade(path=spot, now=WHEN, **GOOD)
        log_trade(path=spot, now=WHEN, **GOOD)   # a real duplicate
        log_trade(path=spot, now=LATER, **TRADE_TWO)
        log_trade(path=spot, now=LATER, **TRADE_ONE)       # NONE, 6.5 hours
        log_trade(path=spot, now=LATER,
                  **dict(GOOD, why='in, out, done'))       # commas
        log_trade(path=spot, now=WHEN, **dict(GOOD, asset='XRP'))
        log_trade(path=spot, now=WHEN, **dict(GOOD, stop='120.00'))
        return disk(spot)

    def w_said():
        """Witnessed as THE WORDS HE READS."""
        spot = fresh()
        return log_trade(path=spot, now=WHEN, **GOOD)

    HONEST_DISK = w_disk()
    HONEST_SAID = w_said()

    def j_disk():
        return w_disk() == HONEST_DISK

    def j_said():
        return w_said() == HONEST_SAID

    def _swap_columns(*args):
        row = _honest['_validate'](*args)
        row[3], row[4] = row[4], row[3]
        return row

    def _swap_stop_account(*args):
        row = _honest['_validate'](*args)
        row[5], row[7] = row[7], row[5]
        return row

    def _why_truncated(value):
        return _honest['_why'](value).split(',')[0]

    def _validate_never_refuses(*args):
        try:
            return _honest['_validate'](*args)
        except TradeRefused:
            return [_honest['_stamp'](args[12])] + [_text(v)
                                                    for v in args[:10]]

    def _append_rewrites(path, text):
        with open(path, 'w', newline='', encoding='utf-8') as handle:
            handle.write(text)

    def _append_dedups(path, text):
        existing = b'' if not os.path.exists(path) else disk(path)
        if text.encode('utf-8') in existing:
            return
        _honest['_append'](path, text)

    def _header_always(path):
        return True

    def _number_rounded(value, which, kind):
        kept = _honest['_number'](value, which, kind)
        return str(Decimal(kept).quantize(Decimal('0.01')))

    def _stamp_no_zone(now):
        return _honest['_stamp'](now).replace('+00:00', '')

    def _stamp_local(now):
        moment = datetime.now(timezone.utc) if now is None else now
        shifted = moment.astimezone(timezone(timedelta(hours=5)))
        return shifted.strftime(STAMP_SHAPE)

    def _asset_short_name(value, assets):
        full = _honest['_asset'](value, assets)
        for short, name in assets:
            if name == full:
                return short
        return full

    def _feeling_as_typed(value):
        typed = _text(value).strip()
        words = typed.split()
        if not words:
            raise TradeRefused('no feeling was given')
        if len(words) > 1:
            raise TradeRefused(f'the feeling must be ONE word, not {typed!r}')
        return words[0]

    def _logged_words_judges(values):
        return _honest['_logged_words'](values) + '  >> a WINNER, well done'

    def _stop_any_side(value, direction, entry):
        typed = _text(value).strip()
        if typed.lower() == NO_STOP:
            return NO_STOP
        return _honest['_number'](typed, 'stop', 'a price')

    def _stop_as_typed(value, direction, entry):
        kept = _honest['_stop'](value, direction, entry)
        return _text(value).strip() if kept == NO_STOP else kept

    def _hours_rounded(value):
        kept = _honest['_hours'](value)
        return str(Decimal(kept).quantize(Decimal('1')))

    BREAKS = [
        ('T1 ', 'a column silently SWAPPED — his exit price into the entry',
         '_validate', _swap_columns, w_disk, j_disk),
        ('T2 ', 'his WHY line TRUNCATED at the first comma',
         '_why', _why_truncated, w_disk, j_disk),
        ('T3 ', 'a REFUSED entry written anyway',
         '_validate', _validate_never_refuses, w_disk, j_disk),
        ('T4 ', 'the append REWRITING the file instead (B13)',
         '_append', _append_rewrites, w_disk, j_disk),
        ('T5 ', 'the header written TWICE',
         '_needs_header', _header_always, w_disk, j_disk),
        ('T6 ', 'a genuine DUPLICATE silently swallowed',
         '_append', _append_dedups, w_disk, j_disk),
        ('T7 ', 'his numbers ROUNDED behind him',
         '_number', _number_rounded, w_disk, j_disk),
        ('T8 ', 'JUDGEMENT printed at entry time — the plan forbids it',
         '_logged_words', _logged_words_judges, w_said, j_said),
        ('T9 ', 'the stamp written with NO ZONE on it',
         '_stamp', _stamp_no_zone, w_disk, j_disk),
        ('T10', 'the stamp written in LOCAL time wearing a UTC zone',
         '_stamp', _stamp_local, w_disk, j_disk),
        ('T11', 'the coin stored as `BTC`, which no snapshot row says',
         '_asset', _asset_short_name, w_disk, j_disk),
        ('T12', 'the feeling left in the case he typed it',
         '_feeling', _feeling_as_typed, w_disk, j_disk),
        ('T13', 'his STOP and his ACCOUNT silently exchanged',
         '_validate', _swap_stop_account, w_disk, j_disk),
        ('T14', 'a stop on the WRONG SIDE of the entry written anyway',
         '_stop', _stop_any_side, w_disk, j_disk),
        ('T15', '`NONE` stored in the case he typed it, not as `none`',
         '_stop', _stop_as_typed, w_disk, j_disk),
        ('T16', 'his HOURS rounded behind him',
         '_hours', _hours_rounded, w_disk, j_disk),
    ]

    print()
    for tag, words, attr, replacement, witness, judge in BREAKS:
        honest_seen = witness()
        original = globals()[attr]
        globals()[attr] = replacement
        try:
            broken_seen = witness()
        except Exception:                                   # noqa: BLE001
            broken_seen = '<the sabotage crashed the witness>'
        try:
            survived = judge()
        except Exception:                                   # noqa: BLE001
            survived = False           # a crash is a catch: it did not pass
        finally:
            globals()[attr] = original
        changed = broken_seen != honest_seen
        caught = not survived
        good = changed and caught
        if not changed:
            verdict = 'INERT — IT CHANGED NOTHING, SO ITS VERDICT IS WORTHLESS'
        elif caught:
            verdict = 'CAUGHT'
        else:
            verdict = 'ESCAPED — THE GATE IS DECORATIVE'
        mark(good, f"{tag} {words:<58} -> {verdict}",
             '' if good else f"changed={changed} caught={caught}")

    print("\n    ... and the originals are proved RESTORED, not assumed.")
    mark(all(globals()[name] is original for name, original
             in _honest.items()),
         "after sixteen breaks and sixteen repairs, every function this "
         "drill touched is the one it started with")
    mark(w_disk() == HONEST_DISK and w_said() == HONEST_SAID,
         "and both witnesses are byte-identical to where they started")

    print("\n(l) >>> A TALLY COUNTS ONLY WHAT A MACHINE ACTUALLY CHECKED, so"
          "\n    this gate is told HERE how many breaks and refusal shapes it"
          "\n    owes, and a deleted one turns it RED.")
    mark(len(BREAKS) == 16 and len(REFUSALS) == 31
         and len(REQUIRED_NAMES) == 19,
         f"the drill still holds all {len(BREAKS)} breaks, the refusal "
         f"table all {len(REFUSALS)} shapes and the name list all "
         f"{len(REQUIRED_NAMES)} sentences, counted against numbers typed "
         f"out here",
         f"{len(BREAKS)} breaks, {len(REFUSALS)} refusal shapes, "
         f"{len(REQUIRED_NAMES)} names")

    print("\n(m) >>> THE PRODUCTION CALLING CONVENTION. **THE ONLY REAL"
          "\n    CALLER IS `log_trade(*answers)` — NO `path`, NO `now`.** A"
          "\n    fresh interpreter calls a COPY in a tree of its own, so"
          "\n    `TRADES_FILE` and the real clock are judged by something. A"
          "\n    `globals()` swap cannot cross into that child, so this check"
          "\n    is CERTIFIED BY ATTACK, not by the drill.")
    R1_TREE = tempfile.mkdtemp(prefix='zarx_g51r1_')
    R1_JOURNAL = os.path.join(R1_TREE, 'journal')
    os.makedirs(R1_JOURNAL)
    shutil.copyfile(os.path.abspath(__file__),
                    os.path.join(R1_JOURNAL, 'log_trade.py'))

    # THE ADDRESS THIS GATE TYPES OUT ITSELF, never read from the module.
    R1_LEAF = 'my_trades.csv'
    R1_MUST_LAND = os.path.join(R1_JOURNAL, R1_LEAF)
    R1_SHAPE = '%Y-%m-%dT%H:%M:%S+00:00'      # typed out here, not imported

    def _inside(stamp_text, opened, closed, slack=2):
        """A stamp -> is it inside the window this gate measured itself?
        PARSED, NEVER PATTERN-MATCHED. Two seconds of slack each way: the
        stamp truncates to whole seconds; the faults this exists to catch
        are five hours and six years out."""
        try:
            when = datetime.strptime(stamp_text, R1_SHAPE)
        except (ValueError, TypeError):
            return False
        when = when.replace(tzinfo=timezone.utc)
        return (opened - timedelta(seconds=slack) <= when
                <= closed + timedelta(seconds=slack))

    r1_probe = os.path.join(R1_TREE, 'said.txt')
    r1_child = ('import sys\n'
                'import journal.log_trade as m\n'
                "said = m.log_trade('BTC', 'long', '100.50', '111.00',\n"
                "                   '95.25', '250', '10000', '30',\n"
                "                   'the production calling convention',\n"
                "                   'calm')\n"
                "open(sys.argv[1], 'w', encoding='utf-8').write(\n"
                '    m.__file__ + chr(10) + said)\n')
    r1_env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')

    R1_OPENED = datetime.now(timezone.utc)
    r1_timed_out, r1_rc = False, None
    try:
        r1_done = subprocess.run([sys.executable, '-c', r1_child, r1_probe],
                                 cwd=R1_TREE, env=r1_env,
                                 capture_output=True, timeout=90)
        r1_rc = r1_done.returncode
    except subprocess.TimeoutExpired:
        r1_timed_out = True
    R1_CLOSED = datetime.now(timezone.utc)

    try:
        with open(r1_probe, encoding='utf-8') as handle:
            r1_seen = handle.read()
    except OSError:
        r1_seen = ''
    r1_parts = r1_seen.split(chr(10))
    r1_file = r1_parts[0] if r1_parts else ''
    r1_said = r1_parts[1] if len(r1_parts) > 1 else ''

    r1_imported_the_copy = bool(r1_file) and os.path.abspath(
        r1_file).startswith(os.path.abspath(R1_TREE))
    mark(not r1_timed_out and r1_rc == 0 and r1_imported_the_copy
         and r1_said.startswith('logged: '),
         "R1 — the doorway was called with NO `path` AND NO `now`, in a "
         "fresh interpreter, against a COPY of this module in a tree of its "
         "own — and the child imported THAT COPY",
         f"exit {r1_rc}, timed out {r1_timed_out}, "
         f"said {r1_said[:60]!r}, from {r1_file}")

    r1_raw = disk(R1_MUST_LAND)
    mark(r1_raw is not None and r1_raw.startswith(HEADER.encode('utf-8'))
         and r1_raw.count(b'\r\n') == 2,
         f"R2 — one header and one row landed at the address THIS GATE typed "
         f"out ({R1_LEAF}, in the copy's own journal folder)",
         f"{0 if r1_raw is None else len(r1_raw)} bytes at {R1_MUST_LAND}")

    try:
        r1_made = sorted(name for name in os.listdir(R1_JOURNAL)
                         if name.lower().endswith('.csv'))
    except OSError:
        r1_made = ['<the folder could not be read>']
    mark(r1_made == [R1_LEAF],
         "R3 — and NO OTHER `.csv` was created beside it (B14's shape)",
         f"the folder holds {r1_made}")

    if r1_raw is None:
        r1_stamp = ''
    else:
        r1_rows = r1_raw.decode('utf-8').split(NL)
        r1_stamp = r1_rows[1].split(',')[0] if len(r1_rows) > 1 else ''

    mark(_inside(r1_stamp, R1_OPENED, R1_CLOSED),
         "R4 — the stamp THE REAL CLOCK PRODUCED lies inside a window this "
         "gate measured ITSELF, either side of the child",
         f"stamp {r1_stamp!r} against "
         f"{R1_OPENED.strftime(R1_SHAPE)} .. {R1_CLOSED.strftime(R1_SHAPE)}")

    mark(r1_stamp.endswith('+00:00') and len(r1_stamp) == 25,
         "R5 — and it carries the zone. A SEPARATE check from R4 on purpose",
         r1_stamp)

    r1_honest = R1_OPENED.strftime(R1_SHAPE)
    r1_five_on = (R1_OPENED + timedelta(hours=5)).strftime(R1_SHAPE)
    r1_frozen = '2020-01-01T00:00:00+00:00'
    mark(_inside(r1_honest, R1_OPENED, R1_CLOSED)
         and not _inside(r1_five_on, R1_OPENED, R1_CLOSED)
         and not _inside(r1_frozen, R1_OPENED, R1_CLOSED)
         and not _inside('', R1_OPENED, R1_CLOSED),
         "R6 — THE WINDOW JUDGE IS PROVED ABLE TO SAY NO, IN THIS RUN: it "
         "ACCEPTS an honest stamp and REJECTS one five hours later, one "
         "dated 2020, and an empty one",
         f"honest {r1_honest} accepted · {r1_five_on} rejected · "
         f"{r1_frozen} rejected")

    shutil.rmtree(R1_TREE, ignore_errors=True)

    print("\n(n) >>> THE TEN QUESTIONS, RUN RATHER THAN READ — THREE TIMES."
          "\n    **THE SHELL IS THE ONLY SURFACE BETWEEN HIS FINGERS AND HIS"
          "\n    ARCHIVE.** `python -u` and a reader on the child's stdout"
          "\n    answer each question BY THE WORDS ON THE SCREEN."
          "\n    R-082 proved one tidy set of answers is not enough: a"
          "\n    default on a blank answer invented a row, and a `.strip()`"
          "\n    on the WHY question quietly corrected him, both at 77/0. So"
          "\n    drive A is tidy, drive B is AWKWARD (mixed case, a WHY line"
          "\n    wrapped in spaces, the stop typed `NONE`), and drive C"
          "\n    leaves the LAST answer BLANK and NOTHING may be written.")

    N_LEAF = 'my_trades.csv'
    # TYPED OUT HERE, NEVER IMPORTED FROM `FIELDS`.
    N_HEADER = ('utc_time', 'asset', 'direction', 'entry', 'exit', 'stop',
                'size_usd', 'account_usd', 'in_hours_ago', 'why', 'feeling')
    N_DEADLINE = 60

    # THE TEN QUESTIONS BY THE WORDS THIS GATE TYPES OUT, the answer each
    # one is given, the column that answer must reach, and what must be in
    # it. **EVERY ANSWER IN DRIVE A IS DIFFERENT**, so a swap anywhere among
    # the ten cannot hide behind two fields that happen to match.
    N_ASK = (
        ('which coin', 'BTC', 'asset', 'BTC-USD'),
        ('long or short', 'long', 'direction', 'long'),
        ('price you got IN at', '100.50', 'entry', '100.50'),
        ('price you got OUT at', '111.00', 'exit', '111.00'),
        ('where was your STOP', '95.25', 'stop', '95.25'),
        ('how big', '250', 'size_usd', '250'),
        ('account size then', '10000', 'account_usd', '10000'),
        ('how many HOURS ago', '30', 'in_hours_ago', '30'),
        ('WHY did you take it', 'ten questions, run rather than read',
         'why', 'ten questions, run rather than read'),
        ('how did you feel', 'calm', 'feeling', 'calm'),
    )
    # DRIVE B — the same ten questions answered the way a person in a hurry
    # answers them. What must land is typed out here from the doorway's own
    # rules, not computed.
    N_ASK_B = (
        ('which coin', ' eth ', 'asset', 'ETH-USD'),
        ('long or short', 'SHORT', 'direction', 'short'),
        ('price you got IN at', '2000.25', 'entry', '2000.25'),
        ('price you got OUT at', '1900.75', 'exit', '1900.75'),
        ('where was your STOP', 'NONE', 'stop', 'none'),
        ('how big', '1500.50', 'size_usd', '1500.50'),
        ('account size then', '8000', 'account_usd', '8000'),
        ('how many HOURS ago', '6.5', 'in_hours_ago', '6.5'),
        ('WHY did you take it', '   range broke, I took it   ',
         'why', '   range broke, I took it   '),
        ('how did you feel', 'Nervous', 'feeling', 'nervous'),
    )
    # DRIVE C — drive A with the LAST answer left blank.
    N_ASK_C = N_ASK[:9] + (('how did you feel', '', 'feeling', None),)

    n_env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')

    def n_shell(ask, state):
        """Run a COPY of this module as `__main__`, under `-u`, in a tree of
        its own, and answer the question that is ASKED.

        **`state` IS SEEDED BY THE CALLER BEFORE THE THREAD STARTS**, so the
        detail lines below can read it whatever happens in here (rule (k)).
        """
        tree = tempfile.mkdtemp(prefix='zarx_g51r3_')
        try:
            journal = os.path.join(tree, 'journal')
            os.makedirs(journal)
            module = os.path.join(journal, 'log_trade.py')
            shutil.copyfile(os.path.abspath(__file__), module)
            # **`-u` IS NOT DECORATION.** `input()` writes its prompt with
            # no newline and a buffered child hands over every prompt in one
            # lump at the end, where no reader can answer any by name.
            child_ = subprocess.Popen([sys.executable, '-u', module],
                                      cwd=tree, env=n_env,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
            seen_ = []

            def drive():
                buffer = ''
                try:
                    while len(state['asked']) < len(ask):
                        byte = child_.stdout.read(1)
                        if not byte:
                            state['ended'] = 'the child stopped talking'
                            return
                        seen_.append(byte)
                        buffer += byte.decode('utf-8', errors='replace')
                        for words, answer, _column, _expected in ask:
                            if words in buffer and words not in state['asked']:
                                state['asked'].append(words)
                                child_.stdin.write(
                                    (answer + chr(10)).encode('utf-8'))
                                child_.stdin.flush()
                                buffer = ''
                                break
                    # **AND THEN NOTHING MORE IS ANSWERED.** An ELEVENTH
                    # question ends the shell at once on an empty stdin.
                    child_.stdin.close()
                    state['ended'] = 'all ten answered'
                except Exception as exc:                    # noqa: BLE001
                    state['error'] = f'{type(exc).__name__}: {exc}'

            reader = threading.Thread(target=drive, daemon=True)
            reader.start()
            reader.join(N_DEADLINE)
            stuck = reader.is_alive()
            try:
                state['rc'] = child_.wait(timeout=15)
            except subprocess.TimeoutExpired:
                child_.kill()
                stuck = True
            try:
                rest = child_.stdout.read()
            except (OSError, ValueError):
                rest = b''
            state['screen'] = (b''.join(seen_) + rest).decode(
                'utf-8', errors='replace')
            state['raw'] = disk(os.path.join(journal, N_LEAF))
            try:
                state['made'] = sorted(name for name in os.listdir(journal)
                                       if name.lower().endswith('.csv'))
            except OSError:
                state['made'] = ['<the folder could not be read>']
            state['stuck'] = stuck
        except Exception as exc:                            # noqa: BLE001
            state['error'] = f'{type(exc).__name__}: {exc}'
        finally:
            shutil.rmtree(tree, ignore_errors=True)

    def n_seed():
        return {'asked': [], 'ended': 'DID NOT FINISH', 'error': None,
                'rc': None, 'stuck': True, 'screen': '', 'raw': None,
                'made': ['<never looked>']}

    n_runs = [(N_ASK, n_seed()), (N_ASK_B, n_seed()), (N_ASK_C, n_seed())]
    # The three shells run SIDE BY SIDE so that a shell which stops asking
    # costs this gate one deadline and not three. Each has a tree of its own.
    n_threads = [threading.Thread(target=n_shell, args=run, daemon=True)
                 for run in n_runs]
    for thread in n_threads:
        thread.start()
    for thread in n_threads:
        thread.join(N_DEADLINE + 30)
    n_a, n_b, n_c = (state for _ask, state in n_runs)
    n_rows = records(n_a['raw'])
    n_rows_b = records(n_b['raw'])

    def n_fine(state):
        return (not state['stuck'] and state['rc'] == 0
                and state['error'] is None)

    mark(n_fine(n_a) and n_fine(n_b) and n_fine(n_c),
         "N1 — THE SHELL WAS RUN, NOT READ, THREE TIMES: each child ran a "
         "COPY of this module as `__main__`, under `-u`, with no `path` and "
         "no `now`, and each finished ON ITS OWN. A hang is RED",
         ' | '.join(f"exit {s['rc']}, stuck {s['stuck']}, {s['ended']}"
                    f"{'' if s['error'] is None else ', ' + s['error']}"
                    for s in (n_a, n_b, n_c)))

    mark(all(len(s['asked']) == len(N_ASK)
             and len(set(s['asked'])) == len(N_ASK)
             for s in (n_a, n_b, n_c)),
         f"N2 — all {len(N_ASK)} questions were asked in every drive and "
         f"each was recognised BY WORDS THIS GATE TYPES OUT, never by "
         f"position. **A RENAMED OR AN ADDED QUESTION LEAVES THIS RED.** "
         f"Asking them in a different order is harmless",
         f"drive A recognised: {n_a['asked']}")

    n_answers = [answer for _w, answer, _c, _e in N_ASK]
    mark(len(N_ASK) == 10 and len(set(n_answers)) == len(N_ASK),
         "N3 — and drive A's ten answers are TEN DIFFERENT VALUES typed out "
         "here: if the stop and the account were both `100`, a swap between "
         "them would be invisible",
         f"{len(set(n_answers))} distinct answers")

    def n_at(rows, column):
        """The value under the column of THIS NAME — the index comes from
        `N_HEADER`, typed out in this gate, never from the file's own first
        line and never from `FIELDS`."""
        if len(rows) < 2 or column not in N_HEADER:
            return None
        at = N_HEADER.index(column)
        row_ = rows[1]
        return row_[at] if at < len(row_) else None

    def n_right(rows, ask):
        """Is every answer in the column its own question feeds?"""
        if len(rows) != 2 or tuple(rows[0]) != N_HEADER:
            return False
        for _words, _answer, column, expected in ask:
            if n_at(rows, column) != expected:
                return False
        return True

    n_header_ok = bool(n_rows) and tuple(n_rows[0]) == N_HEADER
    mark(n_header_ok
         and n_at(n_rows, 'entry') == '100.50'
         and n_at(n_rows, 'exit') == '111.00',
         "N4 — **THE ONE THAT MATTERS.** The answer typed at `price you got "
         "IN at` is in the `entry` column and the answer typed at `price you "
         "got OUT at` is in the `exit` column — the difference between a "
         "winning trade and a losing one in a record nobody re-types",
         f"entry {n_at(n_rows, 'entry')!r}, exit {n_at(n_rows, 'exit')!r}, "
         f"header matched {n_header_ok}")

    n_others = [(column, expected, n_at(n_rows, column))
                for _w, _a, column, expected in N_ASK
                if column not in ('entry', 'exit')]
    mark(n_header_ok and len(n_rows) == 2
         and all(got_ == expected for _c, expected, got_ in n_others),
         "N5 — and every OTHER answer is in its own column too: the coin, "
         "the direction, THE STOP, THE SIZE IN DOLLARS, THE ACCOUNT, THE "
         "HOURS, his own words with a comma in them, and the feeling. A "
         "swap anywhere among the ten is caught",
         '; '.join(f'{c}={g!r}' for c, _e, g in n_others))

    n_pair = f"{n_at(n_rows, 'entry')} -> {n_at(n_rows, 'exit')}"
    n_trio = (f"stop {n_at(n_rows, 'stop')}, size ${n_at(n_rows, 'size_usd')}"
              f", account ${n_at(n_rows, 'account_usd')}, in "
              f"{n_at(n_rows, 'in_hours_ago')} hours ago")
    mark(n_header_ok and 'logged: ' in n_a['screen']
         and n_pair in n_a['screen'] and n_trio in n_a['screen'],
         "N6 — THE SCREEN AND THE NOTEBOOK AGREE: the line printed back to "
         "him names the same two prices in the same order, and the same "
         "stop, size, account and hours, as the row that reached the disk",
         f"looked for {n_pair!r} and {n_trio!r}")

    N_HONEST = [list(N_HEADER),
                ['2026-09-08T00:00:00+00:00', 'BTC-USD', 'long', '100.50',
                 '111.00', '95.25', '250', '10000', '30',
                 'ten questions, run rather than read', 'calm']]
    N_SWAPPED = [list(N_HEADER), list(N_HONEST[1])]
    N_SWAPPED[1][3], N_SWAPPED[1][4] = N_SWAPPED[1][4], N_SWAPPED[1][3]
    N_STOP_ACCT = [list(N_HEADER), list(N_HONEST[1])]
    N_STOP_ACCT[1][5], N_STOP_ACCT[1][7] = (N_STOP_ACCT[1][7],
                                             N_STOP_ACCT[1][5])
    N_RENAMED = [['utc_time', 'asset', 'direction', 'in', 'out', 'stop',
                  'size_usd', 'account_usd', 'in_hours_ago', 'why',
                  'feeling'], list(N_HONEST[1])]
    mark(n_right(N_HONEST, N_ASK) and not n_right(N_SWAPPED, N_ASK)
         and not n_right(N_STOP_ACCT, N_ASK)
         and not n_right(N_RENAMED, N_ASK)
         and not n_right([list(N_HEADER)], N_ASK)
         and not n_right(N_HONEST + [N_HONEST[1]], N_ASK)
         and not n_right([], N_ASK),
         "N7 — THE JUDGE IS PROVED ABLE TO SAY NO, IN THIS RUN: it ACCEPTS "
         "an honest row and REJECTS the two prices exchanged, the stop and "
         "the account exchanged, renamed columns, a header with no row, TWO "
         "rows where one was typed, and nothing at all",
         "honest accepted · six broken shapes rejected")

    mark(n_right(n_rows_b, N_ASK_B),
         "N8 — DRIVE B, THE AWKWARD ONE: ` eth ` landed as `ETH-USD`, "
         "`SHORT` as `short`, `NONE` as `none`, `Nervous` as `nervous`, the "
         "three numbers exactly as typed — AND HIS WHY LINE STILL HAS THE "
         "THREE SPACES HE TYPED AT EACH END. A `.strip()` on the WHY "
         "question went green at 77/0 until this check existed",
         '; '.join(f'{c}={n_at(n_rows_b, c)!r}'
                   for _w, _a, c, _e in N_ASK_B))

    mark(n_c['raw'] is None and n_c['made'] == []
         and '[not logged: no feeling was given]' in n_c['screen']
         and 'logged: ' not in n_c['screen'].replace('[not logged: ', ''),
         "N9 — DRIVE C, THE BLANK LAST ANSWER: NOTHING WAS WRITTEN, no file "
         "was even created, and the refusal is NAMED on his screen. A "
         "default on that question invented a row — a feeling he never gave "
         "— at 77/0 until this check existed",
         f"files made {n_c['made']}, "
         f"screen ends {n_c['screen'].strip()[-60:]!r}")

    shutil.rmtree(WORK, ignore_errors=True)
    # **THE REAL JOURNAL.** Until his first trade it does not exist, and
    # this gate must not create it. Once it exists every row is his, and
    # this gate must not have changed one byte of it. Both are judged by a
    # fingerprint taken BEFORE the first check ran - see the top of the
    # file's gate, where nothing has been written yet.
    mark(fingerprint(TRADES_FILE) == REAL_JOURNAL_AT_START,
         "and the REAL journal is byte-for-byte what it was before this "
         "gate started — never created if it did not exist, never touched "
         "if it did",
         f"{TRADES_FILE}: {REAL_JOURNAL_AT_START[:16]}")

    # THE LAST CHECK OF THE RUN, because it is the only one that can only be
    # answered once every other check has had its say.
    EXPECTED_CHECKS = 101
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes — "
         f"the number is TYPED OUT in this file and is not read from any "
         f"count the run itself produced",
         f"it ran {len(nonlocal_ok) + 1}")

    # ------------------------------------------------------------------
    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 5.1 PASSED — {len(nonlocal_ok)} checks, 0 red.

TEN QUESTIONS, ELEVEN COLUMNS. Every byte judged above was read back
OFF THE DISK and compared to a copy typed out in this gate, never to
what the function said it had written.

THIRTY-ONE REFUSAL SHAPES WROTE NOTHING AT ALL, and on a path that
did not exist the refusal did not even CREATE the file. Each came
back in its own words.

THE STOP IS CHECKED AT THE ENTRY ITSELF, ONE CENT EITHER SIDE, FOR
BOTH DIRECTIONS. `none` in any case is a real answer; `0` and blank
are not quietly read as it. ZERO HOURS IS ACCEPTED and one hundredth
below it is refused.

THE SHELL WAS RUN THREE TIMES - tidy answers, awkward answers, and a
blank last answer - and each answer reached the column of its own
name, his WHY line kept its spaces, and the blank wrote nothing.

SIXTEEN SABOTAGES WERE PROVED TO CHANGE WHAT SOMEBODY READS OR WHAT
LANDS ON DISK BEFORE THEIR VERDICTS WERE COUNTED.

WHAT THIS GATE DOES **NOT** PROVE. It cannot tell whether what he
typed is TRUE. It drives a PIPE and he uses a KEYBOARD, and no check
proves those are the same path (R-082). It is a notebook. It writes
down what he says, exactly as he says it, and it never argues.""")
    else:
        print(f"GATE 5.1 FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
