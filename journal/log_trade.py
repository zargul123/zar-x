"""
Zar X journal compartment — the trade logger (Phase 5, first half).

One command the Commander runs after he closes a trade. It asks him seven
things in plain words — which coin, long or short, what price he got in at,
what price he got out at, how big, WHY he took it in one line, and how he felt
in one word — and it appends what he said to `journal/my_trades.csv`.

**IT NEVER JUDGES.** Not a verdict, not a score, not a profit figure, not a
word of encouragement. The grading is `journal/mirror.py`'s job, monthly, and
it is Phase 5's second half. A logger that told him "nice trade" at the moment
he typed it would be teaching him what to type, and the whole point of this
file is a record made before anybody knows how it turned out.

**APPEND-ONLY, AND IT NEVER REWRITES HISTORY.** This file may only ever add a
line to the end. No tidy-up, no re-sorting, no "keeping it in step" with
anything. A sabotage on 2026-07-29 deleted thirty-four rows of a real archive
and printed a report that was entirely TRUE about what was left, and that is
the shape this rule exists to make impossible.

**>>> DUPLICATES ARE LEGITIMATE HERE AND ARE NEVER REFUSED, WHICH IS THE
OPPOSITE OF EVERY OTHER RECORDER ON THIS SHIP.** A settlement or a candle is a
fact that happens once, so those recorders de-duplicate. **A pilot can
genuinely make the same trade twice in one day, at the same price, in the same
size.** A logger that silently swallowed the second one would erase a real
trade, and the Mirror would then grade him on a lie. This is the one place
where the ship's own habit is the wrong instinct.

**HIS OWN WORDS ARE THE PAYLOAD AND A COMMA MUST NOT BE ABLE TO DESTROY A
ROW.** He will type a WHY line with commas, quotes and apostrophes in it. The
`csv` module writes every row — never a string join — and **the WHY line is
not touched in any way at all**: not stripped, not escaped, not "made safe".
It comes back out of the file byte for byte, including a leading `=`. A row
that silently shifted a column would put his exit price in the size field
forever, and no total anywhere would look wrong.

**THE NUMBERS ARE KEPT AS HE TYPED THEM.** `100.50` is stored as `100.50` and
never as `100.5`. A `Decimal` is built to CHECK each number and is then thrown
away — rounding a figure on the way in decides something on his behalf, and
this file decides nothing.

**A REFUSED ENTRY WRITES NOTHING AT ALL.** Every field is checked before the
file is opened, so a refusal cannot leave a half-written row and cannot even
create the file. Half a row is worse than no row.

LAW 2 — the compartment owns its sources: the asset names, the two directions,
the column order and the path all live in THIS file and nowhere else. It
imports nothing from `config.py`, so the journal cannot be moved by an edit
somebody makes for a different reason.

LAW 3 — the doorway never raises and never prints; it RETURNS. Every failure
becomes one honest, NAMED line the Commander can read and act on.

**THE ASSET IS STORED UNDER THE SHIP'S SNAPSHOT NAME** — `BTC-USD`, not `BTC`
— because `journal/snapshots_local.csv` has written it that way in every row
since Phase 2, and the Mirror will one day have to join these two files on it.
He may type `btc`, `BTC`, `btc-usd` or `BTC-USD`; all four are the same coin.

**EVERY STAMP IS UTC WITH THE ZONE ON IT**, because these rows will one day be
compared against snapshots taken by a cloud machine in another timezone, and a
stamp without a zone is a stamp that has to be guessed at.

Standalone use:
    python journal/log_trade.py          (asks the seven questions)
    python journal/log_trade.py --gate   (gate 5.1, including the drill)
"""
import csv
import io
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
TRADES_FILE = os.path.join(JOURNAL_DIR, 'my_trades.csv')

# The column order. It is read by the Mirror one day and by the Commander in
# a spreadsheet today, so it is written down once, here, and the gate types
# out its own copy rather than importing this one.
FIELDS = ('utc_time', 'asset', 'direction', 'entry', 'exit', 'size', 'why',
          'feeling')

# Law 2. The SHORT name is what the Brief prints; the FULL name is what every
# snapshot row already says and what is stored.
ASSETS = (('BTC', 'BTC-USD'), ('ETH', 'ETH-USD'), ('SOL', 'SOL-USD'))
DIRECTIONS = ('long', 'short')

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

    Lower-cased because the Mirror will group by it, and `Nervous` and
    `nervous` must not become two different feelings in his own record.
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


def _validate(asset, direction, entry, exit_price, size, why, feeling,
              assets, directions, now):
    """The seven answers -> the eight values of one row, or a NAMED refusal.

    **NOTHING IS OPENED, CREATED OR WRITTEN ANYWHERE IN HERE.** Every check
    happens before the journal is touched at all, which is what makes "a
    refused entry writes nothing" true rather than merely intended.
    """
    return [_stamp(now),
            _asset(asset, assets),
            _direction(direction, directions),
            _number(entry, 'entry price', 'a price'),
            _number(exit_price, 'exit price', 'a price'),
            _number(size, 'size', 'a size'),
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
    stamp, asset, direction, entry, exit_price, size, _why_, feeling = values
    return (f'logged: {asset} {direction} {entry} -> {exit_price}, '
            f'size {size}, feeling {feeling}, at {stamp}')


def log_trade(asset, direction, entry, exit_price, size, why, feeling,
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
            values = _validate(asset, direction, entry, exit_price, size,
                               why, feeling, assets, directions, now)
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
        # `print()` outside the gate.** An interactive prompt is something no
        # gate can reach, so everything that can be tested lives above this
        # line and this shell does nothing but ask and repeat the answer.
        print()
        print("ZAR X — log a trade you have CLOSED. Seven questions.")
        print("Nothing here judges the trade. That is the Mirror's job,")
        print("monthly. Press Ctrl+C to walk away; nothing is written until")
        print("all seven are answered.")
        print()
        try:
            answers = (
                input("  which coin?  (BTC / ETH / SOL)      : "),
                input("  long or short?                      : "),
                input("  price you got IN at                 : "),
                input("  price you got OUT at                : "),
                input("  how big? (size)                     : "),
                input("  WHY did you take it? (one line)     : "),
                input("  how did you feel? (ONE word)        : "),
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
    # GATE 5.1 — declared in PROGRESS_LOG.md on 2026-08-19 (morning, second
    # part) and committed with no `journal/log_trade.py` in that commit,
    # BEFORE this file existed, by a session that did not build it.
    #
    # **NOT ONE OF THE TWELVE CONDITIONS OR FIVE DESIGN DECISIONS WAS
    # LOWERED, REINTERPRETED, OR DECLARED NOT TO APPLY.** Where a condition's
    # literal words could not be met, it is said out loud in the check's own
    # text rather than quietly softened — see (j).
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
    from datetime import timedelta

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(good)
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
    # Every expectation is typed out here, character for character, with its
    # line endings explicit.
    WHEN = datetime(2026, 8, 20, 9, 30, 15, tzinfo=timezone.utc)
    WHEN_TEXT = '2026-08-20T09:30:15+00:00'      # typed here, not read
    HEADER = ('utc_time,asset,direction,entry,exit,size,why,feeling'
              + chr(13) + chr(10))
    NL = chr(13) + chr(10)

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

    def fingerprint(path):
        raw = disk(path)
        return 'NO FILE' if raw is None else hashlib.sha256(raw).hexdigest()

    GOOD = dict(asset='BTC', direction='long', entry='100.50',
                exit_price='111.00', size='0.25000000',
                why='trend was up and I waited for the pullback',
                feeling='calm')

    # THE ROW, TYPED OUT BY HAND. Not built by calling anything under test.
    GOOD_ROW = ('2026-08-20T09:30:15+00:00,BTC-USD,long,100.50,111.00,'
                '0.25000000,trend was up and I waited for the pullback,calm'
                + NL)

    print("=" * 70)
    print("GATE 5.1 — THE TRADE LOGGER. Twelve conditions and five design")
    print("decisions, declared before this file existed, by a session that")
    print("did not build it.")
    print("=" * 70)

    print("\n(a) CONDITION 1 — ONE DOORWAY THAT NEVER RAISES AND NEVER"
          "\n    PRINTS, WITH EVERY SETTING RESOLVED FROM `None` IN THE BODY."
          "\n    A file whose only entry point is `input()` is a file no gate"
          "\n    can reach (D1), so the recorded truth is a function taking"
          "\n    the seven fields, and the asking is a shell over it.")
    path = fresh()
    said = log_trade(path=path, **GOOD)
    mark(isinstance(said, str) and said.startswith('logged: '),
         "the doorway RETURNED a plain-words line rather than raising",
         said)
    hostile = [
        ('every field None', dict(asset=None, direction=None, entry=None,
                                  exit_price=None, size=None, why=None,
                                  feeling=None)),
        ('objects that are not text', dict(asset=object(), direction=[1],
                                           entry={}, exit_price=set(),
                                           size=(), why=object(),
                                           feeling=object())),
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

    print("\n(b) >>> CONDITION 2 — EXACT EQUALITY ON THE BYTES READ BACK OFF"
          "\n    THE DISK, never on what the function SAYS it wrote. B11 wrote"
          "\n    a true-looking report about a disk that had not changed.")
    path = fresh()
    log_trade(path=path, now=WHEN, **GOOD)
    mark(same('a new journal', (HEADER + GOOD_ROW).encode('utf-8'),
              disk(path)),
         "a new journal is EXACTLY one header line and one row, byte for "
         "byte, against a copy typed out in this gate",
         f"{len(disk(path))} bytes on disk")
    raw = disk(path)
    mark(raw.count(b'\r\n') == 2 and raw.count(b'\n') == 2
         and b'\r\r\n' not in raw,
         "the line endings are CRLF — the same as every snapshot row — and "
         "NOT the `\\r\\r\\n` that Windows writes when `newline=''` is "
         "forgotten",
         f"CRLF {raw.count(chr(13).encode() + chr(10).encode())}, bare LF "
         f"{raw.count(chr(10).encode()) - raw.count(chr(13).encode() + chr(10).encode())}")
    mark(WHEN_TEXT in raw.decode('utf-8') and raw.decode('utf-8').count(
         '+00:00') == 1,
         "the stamp is UTC WITH THE ZONE ON IT (condition 12), typed out in "
         "this gate rather than read from the file",
         WHEN_TEXT)
    path = fresh()
    KARACHI = timezone(timedelta(hours=5))
    log_trade(path=path, now=datetime(2026, 8, 20, 14, 30, 15,
                                      tzinfo=KARACHI), **GOOD)
    mark(same('the same moment, given in UTC+5',
              (HEADER + GOOD_ROW).encode('utf-8'), disk(path)),
         "and the SAME MOMENT handed over in Karachi's zone — 14:30:15+05:00 "
         "— lands as the IDENTICAL UTC row: the time is CONVERTED, never "
         "merely relabelled. His machine runs UTC+5 and the cloud watchman "
         "that will one day be compared against these rows does not")

    print("\n(c) >>> CONDITION 3 — THE ARCHIVE SURVIVES, PROVED AGAINST ROWS"
          "\n    THIS GATE WROTE ITSELF AND THE LOGGER HAS NEVER SEEN. B13"
          "\n    deleted thirty-four rows and printed a report that was"
          "\n    entirely TRUE about what was left (D2).")
    path = fresh()
    SEEDED = (HEADER
              + '2020-01-01T00:00:00+00:00,ETH-USD,short,1.00,2.00,3.00,'
                'a row the logger never wrote,bored' + NL
              + '2020-01-02T00:00:00+00:00,SOL-USD,long,4.00,5.00,6.00,'
                'and another one,tired' + NL)
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
         "header — a file somebody created by accident must not cost him "
         "his column names")

    print("\n(d) >>> CONDITION 4 — A REFUSED ENTRY WRITES NOTHING. Proved by"
          "\n    sha256 before and after, for EVERY refusal shape, on a"
          "\n    journal that already has rows in it AND on one that does not"
          "\n    exist at all — a refusal must not even CREATE the file.")
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
        print(f"        {words:<38} {answer_a}")
    mark(all_silent,
         f"all {len(REFUSALS)} refusal shapes wrote NOTHING — the seeded "
         f"journal's sha256 never moved once, and the empty path was never "
         f"even created",
         f"seeded sha256 still {fingerprint(seeded_path)[:16]}")

    print("\n(e) >>> CONDITION 5 — EVERY REFUSAL NAMED SEPARATELY. SILENCE IS"
          "\n    FORBIDDEN, and so is one shrug covering six different things:"
          "\n    an unknown coin and an empty WHY line call for completely"
          "\n    different reactions from him.")
    mark(all_named, "every refusal came back as its own `[not logged: ...]` "
                    "line, and the same input refused identically whether the "
                    "journal existed or not")
    REQUIRED_NAMES = ('unknown asset', 'no asset was given',
                      'direction must be long or short', 'is not a number',
                      'is not a price', 'is not a size',
                      'the WHY line is empty', 'must be ONE word',
                      'no feeling was given', 'has no timezone on it')
    joined = ' | '.join(names)
    for needle in REQUIRED_NAMES:
        mark(needle in joined,
             f"the words {needle!r} are on his screen for the case that "
             f"earns them")
    mark(len(set(names)) >= 10,
         f"and the {len(REFUSALS)} shapes produced {len(set(names))} "
         f"DISTINCT sentences, not one catch-all")

    print("\n(f) >>> CONDITION 6 — EVERY THRESHOLD AT THE EXACT VALUE WHERE"
          "\n    IT TURNS OVER, AND ONE STEP EITHER SIDE. R-054 paid for this"
          "\n    rule: a staleness guard was exercised 26 days and a year past"
          "\n    its horizon and never once on the day it fires.")

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

    mark(landed(size='0') is None
         and landed(size='0.00000000') is None
         and landed(size='-0.00000001') is None,
         "SIZE — zero is refused, and so is zero written eight decimal "
         "places long, and so is one hundred-millionth BELOW zero")
    mark(landed(size='0.00000001') is not None
         and ',0.00000001,' in landed(size='0.00000001'),
         "and one hundred-millionth ABOVE zero is accepted and stored exactly "
         "as typed — the turnover is at zero, to the last decimal place",
         landed(size='0.00000001').strip())
    mark(landed(entry='0') is None and landed(exit_price='0') is None
         and landed(entry='0.00000001') is not None,
         "PRICE — the same turnover at zero, on BOTH prices")
    mark(landed(feeling='calm') is not None
         and landed(feeling='calm nervous') is None
         and landed(feeling='') is None,
         "FEELING — one word passes, two words are refused, none is refused: "
         "the turnover is between one word and two")
    mark(landed(feeling='  calm  ') is not None
         and ',calm' + NL in landed(feeling='  calm  '),
         "and one word wrapped in spaces is still ONE word")
    mark(landed(why='x') is not None and landed(why='') is None
         and landed(why=' ') is None,
         "WHY — a single character passes, empty and whitespace-only are "
         "refused: the turnover is between nothing and one character")
    mark(',100.50,' in landed(entry='100.50')
         and ',100.5,' in landed(entry='100.5'),
         "D5 — `100.50` is stored as `100.50` and `100.5` as `100.5`. The "
         "trailing zero he typed SURVIVES; nothing is normalised behind him")

    print("\n(g) >>> CONDITION 7 — D4 PROVED WITH A HOSTILE WHY LINE. A comma"
          "\n    in his own words must not be able to destroy a row, and a"
          "\n    row that silently shifted a column would put his exit price"
          "\n    in the size field forever.")
    HOSTILE = ('   =SUM(A1:A9), he said "buy the dip", then'
               + chr(10) + "I didn't, — 50% ماشاءالله   ")
    path = fresh()
    log_trade(path=path, now=WHEN, why=HOSTILE,
              **{k: v for k, v in GOOD.items() if k != 'why'})
    with open(path, encoding='utf-8', newline='') as handle:
        rows = list(csv.reader(handle))
    mark(len(rows) == 2 and len(rows[1]) == 8,
         "a WHY line carrying a comma, a double quote, a NEWLINE, a leading "
         "`=` and non-ASCII text still produces ONE row of EIGHT columns",
         f"{len(rows)} rows, {len(rows[1])} columns in the second")
    mark(rows[1][6] == HOSTILE,
         "and his words come back BYTE-IDENTICAL — nothing stripped, nothing "
         "escaped, nothing 'made safe', the leading `=` still there",
         repr(rows[1][6]))
    mark(rows[1][6].startswith('   ') and rows[1][6].endswith('   '),
         "INCLUDING THE SPACES AT BOTH ENDS. A `.strip()` added to `_why` "
         "by a tidy-minded future session would change his sentence and "
         "escaped this gate until this check existed",
         repr(rows[1][6][:5]) + ' ... ' + repr(rows[1][6][-5:]))
    mark(rows[1][0] == WHEN_TEXT and rows[1][1] == 'BTC-USD'
         and rows[1][5] == '0.25000000' and rows[1][7] == 'calm',
         "and every column AROUND it is still in its own place — the stamp, "
         "the coin, the size and the feeling all where they belong")
    raw = disk(path)
    mark(raw.count(b'\r\n') == 2
         and raw.count(b'\n') - raw.count(b'\r\n') == 1
         and len(rows) == 2,
         "the newline he typed is INSIDE the quoted field and is still the "
         "bare character he typed: the file has TWO row terminators, not "
         "three, and `csv` reads back TWO records — the row did not split "
         "in two",
         f"{raw.count(chr(13).encode() + chr(10).encode())} CRLF terminators, "
         f"{raw.count(chr(10).encode()) - raw.count(chr(13).encode() + chr(10).encode())} bare LF inside his words")

    print("\n(h) >>> CONDITION 8 — D3. THE SAME TRADE TWICE IS TWO ROWS, AND"
          "\n    THIS GATE SAYS SO OUT LOUD. Every other recorder on this ship"
          "\n    de-duplicates, because a settlement happens once. **A PILOT"
          "\n    CAN GENUINELY MAKE THE SAME TRADE TWICE**, and swallowing the"
          "\n    second one would erase a real trade and make the Mirror grade"
          "\n    him on a lie.")
    path = fresh()
    first = log_trade(path=path, now=WHEN, **GOOD)
    second = log_trade(path=path, now=WHEN, **GOOD)
    mark(same('the same trade, logged twice',
              (HEADER + GOOD_ROW + GOOD_ROW).encode('utf-8'), disk(path)),
         "the identical trade — same coin, same direction, same prices, same "
         "size, same words, same feeling, same second — is TWO IDENTICAL "
         "ROWS, byte for byte",
         f"{disk(path).decode('utf-8').count(chr(10)) - 1} rows after the "
         f"header")
    mark(first == second and first.startswith('logged: '),
         "and he was told the same thing both times — the second was not "
         "quietly treated as a mistake")

    print("\n(i) >>> CONDITION 9 — DOOR 3, THE HALF NO IN-PROCESS CHECK CAN"
          "\n    SEE. A single module-level print would land on whatever"
          "\n    imports this, and a write deferred to a thread or an atexit"
          "\n    handler would land after the verdict. **A FRESH INTERPRETER**"
          "\n    imports it, calls the doorway three ways and SHUTS DOWN, and"
          "\n    its TOTAL output must be empty. A timeout is a FAILURE.")
    GATE_MODULE_NAME = 'journal.log_trade'
    GATE_MODULE_LEAF = 'log_trade.py'
    _ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    probe_dir = tempfile.mkdtemp(prefix='zarx_d3probe_')
    probe = os.path.join(probe_dir, 'seen.txt')
    child_journal = os.path.join(probe_dir, 'child.csv')
    PATHS = (
        "m.log_trade('BTC', 'long', '1', '2', '3', 'why', 'calm', path=P)",
        "m.log_trade('XRP', 'sideways', 'x', 'y', 'z', '', '', path=P)",
        "m.log_trade(None, None, None, None, None, None, None, path=P)",
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
         f"the child finished all {len(PATHS)} calls — a child that stopped "
         f"early is a FAILURE, not a pass on an empty stream",
         f"it reported {seen_n}")
    mark(rc == 0 and wrote == b'',
         "IMPORT, three doorway calls and SHUTDOWN wrote nothing at all",
         '' if wrote == b'' else
         f"it wrote {wrote.decode('utf-8', 'replace')[:200]!r}")
    mark(disk(child_journal) is not None
         and disk(child_journal).count(b'\r\n') == 2,
         "and the one call that should have written DID write, in that other "
         "interpreter — a silent child that also did nothing would be no "
         "evidence at all",
         f"{disk(child_journal)!r}"[:110])
    shutil.rmtree(probe_dir, ignore_errors=True)

    print("\n(j) >>> CONDITION 10 — THE PLAN'S OWN SENTENCE, ABSORBED: TWO"
          "\n    FAKE TRADES ARE LOGGED AND CHECKED BY HAND HERE. **SAID"
          "\n    PLAINLY RATHER THAN SOFTENED: the plan's sentence is `log 2"
          "\n    fake trades, RUN MIRROR, numbers check out by hand`, and"
          "\n    `journal/mirror.py` is Phase 5's SECOND half, which this same"
          "\n    bar forbids this session to build.** So the half that can be"
          "\n    met is met in full — two trades, every field of both checked"
          "\n    against values typed out in this gate, by TWO different"
          "\n    routes — and the Mirror half is owed by whoever builds it.")
    path = fresh()
    TRADE_ONE = dict(asset='eth', direction='SHORT', entry='2500.00',
                     exit_price='2410.25', size='1.5',
                     why='funding was extreme, faded it', feeling='Nervous')
    TRADE_TWO = dict(asset='SOL-USD', direction='Long', entry='140.10',
                     exit_price='138.00', size='12',
                     why='breakout that failed', feeling='ANNOYED')
    LATER = datetime(2026, 8, 20, 17, 45, 0, tzinfo=timezone.utc)
    log_trade(path=path, now=WHEN, **TRADE_ONE)
    log_trade(path=path, now=LATER, **TRADE_TWO)
    BY_HAND = (HEADER
               + '2026-08-20T09:30:15+00:00,ETH-USD,short,2500.00,2410.25,'
                 '1.5,"funding was extreme, faded it",nervous' + NL
               + '2026-08-20T17:45:00+00:00,SOL-USD,long,140.10,138.00,12,'
                 'breakout that failed,annoyed' + NL)
    mark(same('two fake trades', BY_HAND.encode('utf-8'), disk(path)),
         "ROUTE ONE — the whole file equals two rows typed out by hand here, "
         "character for character, INCLUDING the quotes the `csv` module put "
         "round the WHY line that has a comma in it and NOT round the one "
         "that has none")
    with open(path, encoding='utf-8', newline='') as handle:
        got = list(csv.reader(handle))
    EXPECT = [
        ['utc_time', 'asset', 'direction', 'entry', 'exit', 'size', 'why',
         'feeling'],
        ['2026-08-20T09:30:15+00:00', 'ETH-USD', 'short', '2500.00',
         '2410.25', '1.5', 'funding was extreme, faded it', 'nervous'],
        ['2026-08-20T17:45:00+00:00', 'SOL-USD', 'long', '140.10', '138.00',
         '12', 'breakout that failed', 'annoyed'],
    ]
    mark(got == EXPECT,
         "ROUTE TWO — read back field by field, every one of the sixteen "
         "values equals a value typed out separately here: `eth` became the "
         "snapshot name `ETH-USD`, `SHORT` became `short`, `Nervous` became "
         "`nervous`, and `2500.00` kept its trailing zero",
         f"{len(got) - 1} trades, "
         f"{len(got[1]) if len(got) > 1 else 0} columns each")
    mark(all(word not in disk(path).decode('utf-8').lower()
             for word in ('profit', 'loss', 'win', 'good', 'bad', 'well '
                          'done', 'mistake')),
         "and NOT ONE WORD OF JUDGEMENT reached the disk — no profit, no "
         "verdict, nothing that would teach him what to type next time")

    print("\n(k) >>> CONDITION 11 — THE SABOTAGE DRILL, INSTALLED FROM BIRTH"
          "\n    AND PERMANENT. Every break is PROVED TO CHANGE WHAT SOMEBODY"
          "\n    READS OR WHAT LANDS ON DISK before its verdict is counted."
          "\n    **A BREAK REPORTED `INERT` IS A FAIL** — nine deliberate lies"
          "\n    once walked through two green gates because every check ran,"
          "\n    every check passed, and nobody had tried to break them.")

    _honest = {name: globals()[name] for name in
               ('_validate', '_append', '_needs_header', '_row_text', '_why',
                '_number', '_stamp', '_asset', '_feeling', '_logged_words')}

    def w_disk():
        """Witnessed as BYTES ON DISK: two trades, a genuine DUPLICATE of
        the first, and a refusal. The disk is the only witness that can see
        a refusal that writes anyway or a duplicate that is quietly eaten."""
        spot = fresh()
        log_trade(path=spot, now=WHEN, **GOOD)
        log_trade(path=spot, now=WHEN, **GOOD)   # D3: a real duplicate
        log_trade(path=spot, now=LATER, **TRADE_TWO)
        log_trade(path=spot, now=LATER,
                  **dict(GOOD, why='in, out, done'))   # D4: commas
        log_trade(path=spot, now=WHEN, **dict(GOOD, asset='XRP'))
        return disk(spot)

    def w_said():
        """Witnessed as THE WORDS HE READS: a returned line can carry a
        judgement while the disk stays byte-identical."""
        spot = fresh()
        return log_trade(path=spot, now=WHEN, **GOOD)

    HONEST_DISK = w_disk()
    HONEST_SAID = w_said()

    def j_disk():
        return w_disk() == HONEST_DISK

    def j_said():
        return w_said() == HONEST_SAID

    def _swap_columns(asset, direction, entry, exit_price, size, why,
                      feeling, assets, directions, now):
        row = _honest['_validate'](asset, direction, entry, exit_price, size,
                                   why, feeling, assets, directions, now)
        row[3], row[4] = row[4], row[3]
        return row

    def _why_truncated(value):
        return _honest['_why'](value).split(',')[0]

    def _validate_never_refuses(asset, direction, entry, exit_price, size,
                                why, feeling, assets, directions, now):
        try:
            return _honest['_validate'](asset, direction, entry, exit_price,
                                        size, why, feeling, assets,
                                        directions, now)
        except TradeRefused:
            return [_honest['_stamp'](now), _text(asset), _text(direction),
                    _text(entry), _text(exit_price), _text(size),
                    _text(why), _text(feeling)]

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

    BREAKS = [
        ('T1 ', 'a column silently SWAPPED — his exit price into the entry',
         '_validate', _swap_columns, w_disk, j_disk),
        ('T2 ', 'his WHY line TRUNCATED at the first comma (D4)',
         '_why', _why_truncated, w_disk, j_disk),
        ('T3 ', 'a REFUSED entry written anyway',
         '_validate', _validate_never_refuses, w_disk, j_disk),
        ('T4 ', 'the append REWRITING the file instead (D2, B13)',
         '_append', _append_rewrites, w_disk, j_disk),
        ('T5 ', 'the header written TWICE',
         '_needs_header', _header_always, w_disk, j_disk),
        ('T6 ', 'a genuine DUPLICATE silently swallowed (D3)',
         '_append', _append_dedups, w_disk, j_disk),
        ('T7 ', 'his numbers ROUNDED behind him (D5)',
         '_number', _number_rounded, w_disk, j_disk),
        ('T8 ', 'JUDGEMENT printed at entry time — the plan forbids it',
         '_logged_words', _logged_words_judges, w_said, j_said),
        ('T9 ', 'the stamp written with NO ZONE on it (condition 12)',
         '_stamp', _stamp_no_zone, w_disk, j_disk),
        ('T10', 'the stamp written in LOCAL time wearing a UTC zone',
         '_stamp', _stamp_local, w_disk, j_disk),
        ('T11', 'the coin stored as `BTC`, which no snapshot row says',
         '_asset', _asset_short_name, w_disk, j_disk),
        ('T12', 'the feeling left in the case he typed it',
         '_feeling', _feeling_as_typed, w_disk, j_disk),
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

    print("\n    ... and the originals are proved RESTORED, not assumed. A"
          "\n    drill that left a break installed would hand the next check"
          "\n    a sabotaged module and call the result evidence.")
    mark(all(globals()[name] is original for name, original
             in _honest.items()),
         "after twelve breaks and twelve repairs, every function this drill "
         "touched is the one it started with")
    mark(w_disk() == HONEST_DISK and w_said() == HONEST_SAID,
         "and both witnesses are byte-identical to where they started")

    print("\n(l) >>> THE CHECK THIS SHIP DID NOT HAVE, ADDED BECAUSE THIS"
          "\n    SESSION'S OWN PART 1 PROVED IT WAS MISSING. Five sabotage"
          "\n    entries were deleted from GATE 4.1 this morning and it"
          "\n    printed `PASSED — 82 checks, 0 red` and exited 0, while its"
          "\n    own banner claimed all twenty-one had run. **A TALLY COUNTS"
          "\n    ONLY WHAT A MACHINE ACTUALLY CHECKED**, so this gate is told"
          "\n    HERE how many checks it owes, and a deleted check turns it"
          "\n    RED instead of quietly shrinking the headline.")
    mark(len(BREAKS) == 12 and len(REFUSALS) == 18,
         f"the drill still holds all {len(BREAKS)} breaks and the refusal "
         f"table all {len(REFUSALS)} shapes, both counted against numbers "
         f"typed out here",
         f"{len(BREAKS)} breaks, {len(REFUSALS)} refusal shapes")

    print("\n(m) >>> GATE 5.1-R1 — THE PRODUCTION CALLING CONVENTION, WHICH"
          "\n    NOTHING IN THIS GATE HAD EVER EXERCISED. Added 2026-08-20"
          "\n    (evening) on the Commander's ruling, after a session that did"
          "\n    not build this file installed THREE REAL TEXT EDITS that each"
          "\n    left the gate printing `PASSED — 64 checks, 0 red`: the real"
          "\n    clock relabelled UTC instead of converted, the same clock"
          "\n    frozen at 2020, and the archive moved to another filename."
          "\n    **THE ONLY REAL CALLER IS `log_trade(*answers)` — NO `path`,"
          "\n    NO `now`.** Every check above injects both, or reads only the"
          "\n    first eight characters of the returned line, so `TRADES_FILE`"
          "\n    and `datetime.now(timezone.utc)` were judged by NOTHING."
          "\n    **THE DRILL CANNOT REACH THIS CHECK AND THAT IS THE POINT,"
          "\n    SAID HERE RATHER THAN LEFT AS AN OMISSION:** a `globals()`"
          "\n    swap cannot cross into a child interpreter reading a copy off"
          "\n    the disk — which is exactly why this catches what T10, a"
          "\n    sabotage for this very fault that reports CAUGHT, cannot see."
          "\n    **A DRILL PROVES A GATE CAN CATCH A MONKEYPATCH. THIS CHECK"
          "\n    IS CERTIFIED BY ATTACK INSTEAD.**")

    # A COPY, IN A TREE OF ITS OWN. **A call with no `path` writes into
    # whatever `journal/` folder the module sits in, and against the real
    # module that is the Commander's own archive.** That is the entire
    # difficulty of this check, and the mistake was actually made this
    # morning by the attack rig that found the hole (R-076 doubt 1).
    R1_TREE = tempfile.mkdtemp(prefix='zarx_g51r1_')
    R1_JOURNAL = os.path.join(R1_TREE, 'journal')
    os.makedirs(R1_JOURNAL)
    shutil.copyfile(os.path.abspath(__file__),
                    os.path.join(R1_JOURNAL, 'log_trade.py'))

    # THE ADDRESS THIS GATE TYPES OUT ITSELF, never read from the module.
    # B14 moved an archive with every row inside it perfect, and every check
    # that asked the module where to look followed it there and certified it.
    R1_LEAF = 'my_trades.csv'
    R1_MUST_LAND = os.path.join(R1_JOURNAL, R1_LEAF)
    R1_SHAPE = '%Y-%m-%dT%H:%M:%S+00:00'      # typed out here, not imported

    def _inside(stamp_text, opened, closed, slack=2):
        """A stamp -> is it inside the window this gate measured itself?

        **PARSED, NEVER PATTERN-MATCHED.** A clock frozen at 2020 carries a
        perfect `+00:00` and walks straight past anything that only looks at
        the shape — which is why the zone is a SEPARATE check below.

        The slack is TWO SECONDS EACH WAY and the reason is written down so
        nobody widens it later: the stamp truncates to whole seconds, so an
        honest one can land up to a second before the opening reading. The
        faults this exists to catch are five hours and six years out, and
        nothing on this ship produces a value in between.
        """
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
                "                   '0.25', 'the production calling "
                "convention', 'calm')\n"
                "open(sys.argv[1], 'w', encoding='utf-8').write(\n"
                '    m.__file__ + chr(10) + said)\n')
    r1_env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')

    # THE WINDOW IS MEASURED BY THIS GATE, ON BOTH SIDES OF THE CHILD.
    R1_OPENED = datetime.now(timezone.utc)
    r1_timed_out, r1_rc = False, None
    try:
        r1_done = subprocess.run([sys.executable, '-c', r1_child, r1_probe],
                                 cwd=R1_TREE, env=r1_env,
                                 capture_output=True, timeout=90)
        r1_rc = r1_done.returncode
    except subprocess.TimeoutExpired:
        # A child that hangs is a FAILURE, not a pass. R-077 is a call with
        # no timeout that never came back while its gate printed 107/0, and
        # that shape is not going into the file it was found beside.
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
         "own — and the child imported THAT COPY, proved by the `__file__` "
         "it reported back",
         f"exit {r1_rc}, timed out {r1_timed_out}, "
         f"said {r1_said[:60]!r}, from {r1_file}")

    r1_raw = disk(R1_MUST_LAND)
    mark(r1_raw is not None and r1_raw.startswith(HEADER.encode('utf-8'))
         and r1_raw.count(b'\r\n') == 2,
         f"R2 — one header and one row landed at the address THIS GATE typed "
         f"out ({R1_LEAF}, in the copy's own journal folder) — never at an "
         f"address read back from the module",
         f"{0 if r1_raw is None else len(r1_raw)} bytes at {R1_MUST_LAND}")

    try:
        r1_made = sorted(name for name in os.listdir(R1_JOURNAL)
                         if name.lower().endswith('.csv'))
    except OSError:
        r1_made = ['<the folder could not be read>']
    mark(r1_made == [R1_LEAF],
         "R3 — and NO OTHER `.csv` was created beside it. B14's shape: an "
         "archive under another filename is reported MISSING, not followed. "
         "R2 proves the right file exists; this proves a wrong one was not "
         "made INSTEAD of it",
         f"the folder holds {r1_made}")

    if r1_raw is None:
        r1_stamp = ''
    else:
        r1_rows = r1_raw.decode('utf-8').split(NL)
        r1_stamp = r1_rows[1].split(',')[0] if len(r1_rows) > 1 else ''

    mark(_inside(r1_stamp, R1_OPENED, R1_CLOSED),
         "R4 — the stamp THE REAL CLOCK PRODUCED lies inside a window this "
         "gate measured ITSELF, either side of the child, widened by two "
         "seconds. **This is the check the three escapes needed: a stamp "
         "five hours out or frozen at 2020 lands nowhere near it**",
         f"stamp {r1_stamp!r} against "
         f"{R1_OPENED.strftime(R1_SHAPE)} .. {R1_CLOSED.strftime(R1_SHAPE)}")

    mark(r1_stamp.endswith('+00:00') and len(r1_stamp) == 25,
         "R5 — and it carries the zone. A SEPARATE check from R4 on purpose: "
         "the frozen-2020 fault carries a perfect `+00:00`, so a shape check "
         "alone would have certified it",
         r1_stamp)

    r1_honest = R1_OPENED.strftime(R1_SHAPE)
    r1_five_on = (R1_OPENED + timedelta(hours=5)).strftime(R1_SHAPE)
    r1_frozen = '2020-01-01T00:00:00+00:00'
    mark(_inside(r1_honest, R1_OPENED, R1_CLOSED)
         and not _inside(r1_five_on, R1_OPENED, R1_CLOSED)
         and not _inside(r1_frozen, R1_OPENED, R1_CLOSED)
         and not _inside('', R1_OPENED, R1_CLOSED),
         "R6 — THE WINDOW JUDGE IS PROVED ABLE TO SAY NO, IN THIS RUN, "
         "against three stamps typed out here: it ACCEPTS an honest one and "
         "REJECTS one five hours later, one dated 2020, and an empty one. "
         "**A check whose failure path has never been shown to work is a "
         "check nobody has tested** — R-057 was filed about exactly that",
         f"honest {r1_honest} accepted · {r1_five_on} rejected · "
         f"{r1_frozen} rejected")

    shutil.rmtree(R1_TREE, ignore_errors=True)

    shutil.rmtree(WORK, ignore_errors=True)
    real_journal_touched = os.path.exists(TRADES_FILE)
    mark(not real_journal_touched,
         "and the REAL journal was never created or touched by this gate — "
         "every check wrote into a temporary directory now removed",
         TRADES_FILE)

    # THE LAST CHECK OF THE RUN, because it is the only one that can only be
    # answered once every other check has had its say.
    EXPECTED_CHECKS = 70
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

Every byte judged above was read back OFF THE DISK and compared to a
copy typed out in this gate, never to what the function said it had
written. A journal seeded with two rows this logger has never seen
came back with every seeded byte at the same offset and exactly one
row added — no second header, nothing merged, nothing re-sorted.

EIGHTEEN REFUSAL SHAPES WROTE NOTHING AT ALL. The seeded journal's
sha256 did not move once across all eighteen, and on a path that did
not exist the refusal did not even CREATE the file. Each came back
in its own words, and the same input was refused identically whether
the journal existed or not.

D3 IS THE ONE THAT GOES AGAINST THIS SHIP'S OWN HABIT AND IT IS
PROVED, NOT ASSERTED: the identical trade — same coin, same prices,
same size, same words, same second — is TWO IDENTICAL ROWS. A pilot
can genuinely make the same trade twice, and a logger that swallowed
the second would erase a real trade and make the Mirror grade him on
a lie.

HIS OWN WORDS SURVIVED A HOSTILE LINE carrying a comma, a double
quote, a NEWLINE, a leading `=` and non-ASCII text: one row, eight
columns, the WHY field byte-identical with the `=` still on the
front, and every column around it still in its own place.

EVERY THRESHOLD WAS TESTED AT THE EXACT VALUE WHERE IT TURNS OVER
AND ONE STEP EITHER SIDE: a size of zero written eight decimals
long, one hundred-millionth either side of it, both prices at zero,
one word against two, and one character of WHY against none. And
`100.50` reached the disk as `100.50` — the trailing zero he typed
survives, because rounding a number on the way in decides something
on his behalf.

TWELVE SABOTAGES WERE PROVED TO CHANGE WHAT SOMEBODY READS OR WHAT
LANDS ON DISK BEFORE THEIR VERDICTS WERE COUNTED, each on the
channel it really affects — which is why T8, whose disk output is
byte-identical to the honest one, is witnessed on the RETURNED LINE.

WHAT THIS GATE DOES **NOT** PROVE, said here rather than in a
footnote. It does not prove `journal/mirror.py`, which does not
exist: half of the plan's own sentence for Phase 5 names a file this
bar forbids this session to build, and that half is owed by whoever
builds it. It does not test the seven interactive questions, which
no gate can reach — only the doorway underneath them. And it cannot
tell whether what he typed is TRUE. It is a notebook. It writes down
what he says, exactly as he says it, and it never argues.""")
    else:
        print(f"GATE 5.1 FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
