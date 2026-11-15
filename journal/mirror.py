"""
Zar X journal compartment — the Mirror (Phase 5, second half).

It reads the trades the Commander logged with `LOG_TRADE.bat` and prints, for
each one: what it made or lost, what he actually risked, what the ship's
instruments had recorded just before he got in, and what the SAME trade would
have made sized to risk 1% of his account — two lines, the pure 1% and the 1%
with the ship's 25% position cap. Then totals.

**ARITHMETIC ONLY. NEVER A SIGNAL, NEVER ADVICE, NEVER A WORD ABOUT HIM.**
The plan says "No shaming, arithmetic only" and this is the one instrument on
the ship whose whole subject is the pilot. Nothing here says what he should
have done. The 1% lines are the same trade at another size and nothing more.

**IT READS. IT NEVER WRITES.** There is no call in this file that opens
anything for writing. The journal is his archive and every row is his.

**THE ARITHMETIC** (declared in PROGRESS_LOG.md, 2026-11-15, before this
file existed):

    move        = (exit - entry) / entry        for a long
                = (entry - exit) / entry        for a short
    result $    = size_usd x move                       BEFORE FEES
    stop gap    = |entry - stop| / entry
    risked $    = size_usd x stop gap
    R           = result $ / risked $
    1% size     = 0.01 x account_usd / stop gap
    capped size = the smaller of (1% size) and (0.25 x account_usd)

**SAME ENTRY, SAME EXIT, SAME STOP. ONLY THE SIZE CHANGES.**

**SIZE IS DOLLARS, NOT COINS** — the Commander's ruling of 2026-11-15, and
the reason the journal's column is called `size_usd`.

**THE TIME RULE.** A trade's stamp is the moment he LOGGED it, in UTC with
the zone on it. `in_hours_ago` counts back from that stamp to when he got in.
Every snapshot row is written from `datetime.now(timezone.utc)` with no zone
on it (measured by reading `journal/snapshot.py`), so a snapshot's time is
read as UTC and NEVER as this machine's local time. The reading used is the
NEWEST snapshot for that coin AT OR BEFORE the moment he got in — never one
from after, which would be information he did not have — and if that reading
is more than 8 hours old the Mirror says there is none.

**A ROW IT CANNOT READ IS NAMED AND COUNTED, never dropped in silence and
never guessed at.** A header it does not know stops it, by name: it does not
read columns by position from a file whose columns it cannot vouch for.

LAW 2 — the compartment owns its sources: the eleven column names, the three
notebook addresses and every constant live in THIS file. It imports nothing
from `log_trade.py` or `config.py`, so an edit made there for another reason
cannot quietly move what this file reads.

LAW 3 — the doorway never raises and never prints; it RETURNS the report.

Standalone use:
    python journal/mirror.py                   (every trade in the journal)
    python journal/mirror.py --month 2026-11   (trades logged in that month)
    python journal/mirror.py --gate            (gate 5.2, including the drill)
"""
import csv
import io
import os
import sys
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
TRADES_FILE = os.path.join(JOURNAL_DIR, 'my_trades.csv')

# The three notebooks, in the order that decides a tie: the laptop's, the
# cloud's, then the frozen one from before the two were split.
SNAPSHOT_FILES = (os.path.join(JOURNAL_DIR, 'snapshots_local.csv'),
                  os.path.join(JOURNAL_DIR, 'snapshots_cloud.csv'),
                  os.path.join(JOURNAL_DIR, 'snapshots.csv'))

# TYPED OUT HERE, NOT IMPORTED FROM `log_trade.FIELDS`. If the logger's
# columns ever change, this Mirror stops and says so instead of reading the
# wrong column under the right name.
HEADER = ('utc_time', 'asset', 'direction', 'entry', 'exit', 'stop',
          'size_usd', 'account_usd', 'in_hours_ago', 'why', 'feeling')

NO_STOP = 'none'
RISK_FRACTION = Decimal('0.01')      # "risk 1% of the account"
CAP_FRACTION = Decimal('0.25')       # the ship's 25% position cap
MAX_READING_AGE = timedelta(hours=8)  # two 4h closes: one miss is tolerated
TRADE_STAMP = '%Y-%m-%dT%H:%M:%S+00:00'
SNAPSHOT_STAMP = '%Y-%m-%d %H:%M'
RULE = '-' * 70
DOUBLE = '=' * 70


class Unreadable(Exception):
    """One row of the journal this Mirror cannot vouch for. Its message is
    printed on the report, in plain words, beside the row's number."""


# ---- reading his journal ------------------------------------------------

def _decimal(text, which, minimum_exclusive=True):
    """A number in the journal -> a Decimal, or a NAMED reason it is not."""
    try:
        number = Decimal(text.strip())
    except (InvalidOperation, ValueError, AttributeError):
        raise Unreadable(f'the {which} {text!r} is not a number')
    if not number.is_finite():
        raise Unreadable(f'the {which} {text!r} is not a number')
    if number < 0 or (minimum_exclusive and number == 0):
        raise Unreadable(f'the {which} {text!r} is not above zero'
                         if minimum_exclusive else
                         f'the {which} {text!r} is below zero')
    return number


def _parse_trade(row):
    """Eleven strings -> one trade, or `Unreadable` with the reason."""
    if len(row) != len(HEADER):
        raise Unreadable(f'it has {len(row)} columns, not {len(HEADER)}')
    (stamp, asset, direction, entry, exit_price, stop, size, account, hours,
     why, feeling) = row
    try:
        logged = datetime.strptime(stamp, TRADE_STAMP).replace(
            tzinfo=timezone.utc)
    except ValueError:
        raise Unreadable(f'the time {stamp!r} is not a UTC stamp')
    if direction not in ('long', 'short'):
        raise Unreadable(f'the direction {direction!r} is not long or short')
    trade = {
        'logged': logged, 'asset': asset, 'direction': direction,
        'entry_text': entry, 'exit_text': exit_price, 'stop_text': stop,
        'hours_text': hours, 'why': why, 'feeling': feeling,
        'entry': _decimal(entry, 'entry price'),
        'exit': _decimal(exit_price, 'exit price'),
        'size': _decimal(size, 'size'),
        'account': _decimal(account, 'account size'),
        'hours': _decimal(hours, 'hours', minimum_exclusive=False),
        'stop': None,
    }
    if stop != NO_STOP:
        trade['stop'] = _decimal(stop, 'stop')
        wrong = (trade['stop'] >= trade['entry'] if direction == 'long'
                 else trade['stop'] <= trade['entry'])
        if wrong:
            raise Unreadable(f'the stop {stop} is on the wrong side of the '
                             f'entry {entry} for a {direction}')
    return trade


def _read_trades(path):
    """The journal -> (state, trades, unreadable, found_header).

    `state` is one of `missing`, `empty`, `bad header`, `ok`. `unreadable`
    is a list of (row number, reason); the row number counts the header as
    row 1, the way a spreadsheet shows it.
    """
    if not os.path.exists(path):
        return 'missing', [], [], None
    with open(path, encoding='utf-8', newline='') as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return 'empty', [], [], None
    if tuple(rows[0]) != HEADER:
        return 'bad header', [], [], rows[0]
    trades, unreadable = [], []
    for number, row in enumerate(rows[1:], start=2):
        try:
            trade = _parse_trade(row)
        except Unreadable as exc:
            unreadable.append((number, str(exc)))
            continue
        trade['row'] = number
        trades.append(trade)
    return 'ok', trades, unreadable, rows[0]


# ---- reading the instruments' notebooks ----------------------------------

def _snapshot_time(text):
    """A snapshot's `utc_time` -> a moment. **READ AS UTC**: the writer is
    `datetime.now(timezone.utc)`, and reading it as local time would move
    every reading by this machine's five hours."""
    return datetime.strptime(text.strip(), SNAPSHOT_STAMP).replace(
        tzinfo=timezone.utc)


def _read_snapshots(paths):
    """The notebooks -> (readings, files found, rows read, rows skipped).

    `readings` is a list in NOTEBOOK ORDER, which is what makes "the first
    notebook wins a tie" true rather than an accident of sorting.
    """
    readings, found, skipped = [], 0, 0
    for path in paths:
        if not os.path.exists(path):
            continue
        found += 1
        with open(path, encoding='utf-8', newline='') as handle:
            for row in csv.DictReader(handle):
                try:
                    when = _snapshot_time(row.get('utc_time') or '')
                    asset = row['asset']
                    trend = row['trend']
                except (ValueError, KeyError, TypeError, AttributeError):
                    skipped += 1
                    continue
                if not asset or not trend:
                    skipped += 1
                    continue
                readings.append({'when': when, 'asset': asset,
                                 'trend': trend,
                                 'regime': row.get('regime') or '?',
                                 'rsi': row.get('rsi') or '?',
                                 'adx': row.get('adx') or '?'})
    return readings, found, len(readings), skipped


def _readings_for(readings, asset):
    """Only the readings taken for THIS coin."""
    return [reading for reading in readings if reading['asset'] == asset]


def _got_in(logged, hours):
    """The moment he got in: the stamp minus the hours he typed."""
    return logged - timedelta(microseconds=int(hours * 3600 * 1000000))


def _pick(readings, got_in):
    """The newest reading AT OR BEFORE the moment he got in, if it is no
    more than eight hours old. Otherwise None.

    `>` and not `>=` below: of two readings at the same minute the EARLIER
    in notebook order is kept.
    """
    best = None
    for reading in readings:
        if reading['when'] > got_in:
            continue                      # taken AFTER he got in: never used
        if best is None or reading['when'] > best['when']:
            best = reading
    if best is None or got_in - best['when'] > MAX_READING_AGE:
        return None
    return best


# ---- the arithmetic ---------------------------------------------------------

def _move(direction, entry, exit_price):
    """The fraction the price moved IN HIS FAVOUR."""
    if direction == 'long':
        return (exit_price - entry) / entry
    return (entry - exit_price) / entry


def _result_usd(trade):
    """What the trade made or lost, in dollars, before fees. Size is
    DOLLARS, so it is the size times the fraction the price moved."""
    return trade['size'] * _move(trade['direction'], trade['entry'],
                                 trade['exit'])


def _stop_gap(trade):
    """How far the stop sat from the entry, as a fraction of the entry."""
    return abs(trade['entry'] - trade['stop']) / trade['entry']


def _pure_size(account, gap):
    """The size at which losing the whole stop gap costs 1% of the account."""
    return RISK_FRACTION * account / gap


def _capped_size(pure, account):
    """The same, but never more than 25% of the account in one position."""
    return min(pure, CAP_FRACTION * account)


def _work_out(trade):
    """One trade -> every figure the report prints for it."""
    move = _move(trade['direction'], trade['entry'], trade['exit'])
    result = _result_usd(trade)
    # **EVERY DOLLAR RESULT IS ROUNDED TO THE CENT HERE, ONCE, AND THE
    # TOTALS ADD UP THE ROUNDED FIGURES** - so that every total on the
    # report equals the lines above it added up by hand. The percentages
    # and R are worked from the exact value and rounded only for display.
    figures = {'result': _round(result, 2),
               'result_pct': result / trade['account'] * 100,
               'stopped': trade['stop'] is not None}
    if figures['stopped']:
        gap = _stop_gap(trade)
        risked = trade['size'] * gap
        pure = _pure_size(trade['account'], gap)
        capped = _capped_size(pure, trade['account'])
        figures.update(
            risked=risked,
            risked_pct=risked / trade['account'] * 100,
            r=result / risked,
            pure_size=pure, pure_result=_round(pure * move, 2),
            capped_size=capped, capped_result=_round(capped * move, 2),
            cap_reached=capped < pure,
            capped_risk_pct=capped * gap / trade['account'] * 100)
    return figures


def _sum(values):
    """Every total on the report goes through here."""
    total = Decimal(0)
    for value in values:
        total += value
    return total


def _own_on_stopped(worked):
    """HIS result over only the trades that had a stop — the like-for-like
    figure printed beside the two 1% totals."""
    return _sum(figures['result'] for figures in worked
                if figures['stopped'])


# ---- the words ------------------------------------------------------------

def _round(value, places):
    """Half up on the exact decimal value, never through a float."""
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def _usd(value):
    """An amount of money: `$1,234.50`."""
    return f'${_round(value, 2):,.2f}'


def _signed_usd(value):
    """A result: `+$400.00`, `-$37.50`, and plain `$0.00` for nothing."""
    cents = _round(value, 2)
    if cents == 0:
        return '$0.00'
    return f"{'+' if cents > 0 else '-'}${abs(cents):,.2f}"


def _signed(value, places=2):
    rounded = _round(value, places)
    if rounded == 0:
        return f'{abs(rounded):.{places}f}'
    return f"{'+' if rounded > 0 else '-'}{abs(rounded):.{places}f}"


def _pct(value):
    return f'{_round(value, 2):.2f}%'


def _count(number, word='trade'):
    return f"{number} {word}{'' if number == 1 else 's'}"


def _when(moment):
    return moment.strftime('%Y-%m-%d %H:%M') + ' UTC'


def _beside(direction, reading):
    """Which bucket a trade falls in beside the recorded trend."""
    if reading is None:
        return 'none'
    if reading['trend'] == 'UP':
        return 'with' if direction == 'long' else 'against'
    if reading['trend'] == 'DOWN':
        return 'with' if direction == 'short' else 'against'
    return 'mixed'


def _trade_lines(number, trade, figures, got_in, reading):
    """One trade -> its block on the report."""
    why = ' / '.join(trade['why'].splitlines()) or trade['why']
    lines = [
        RULE,
        f"TRADE {number} - {trade['asset']} {trade['direction']} - logged "
        f"{_when(trade['logged'])}",
        f"  in {trade['entry_text']} -> out {trade['exit_text']}, size "
        f"{_usd(trade['size'])}, account {_usd(trade['account'])}",
        f'  why     : "{why}"',
        f"  feeling : {trade['feeling']}",
        f"  result  : {_signed_usd(figures['result'])}  "
        f"({_signed(figures['result_pct'])}% of account)",
    ]
    if figures['stopped']:
        if figures['cap_reached']:
            cap_note = (f"(capped; risk {_pct(figures['capped_risk_pct'])} "
                        f"of account)")
        else:
            cap_note = '(cap not reached)'
        lines += [
            f"  stop    : {trade['stop_text']} - you risked "
            f"{_usd(figures['risked'])} ({_pct(figures['risked_pct'])} of "
            f"account) - result {_signed(figures['r'])} R",
            f"  same trade at 1% risk  : size {_usd(figures['pure_size'])} "
            f"-> {_signed_usd(figures['pure_result'])}",
            f"  same, with the 25% cap : size "
            f"{_usd(figures['capped_size'])} -> "
            f"{_signed_usd(figures['capped_result'])}  {cap_note}",
        ]
    else:
        lines.append('  stop    : none - the 1% comparison cannot be worked '
                     'out for this trade')
    lines.append(f"  got in  : about {_when(got_in)} (you typed "
                 f"{trade['hours_text']} hours ago)")
    if reading is None:
        lines.append('  reading : none within 8 hours before you got in')
    else:
        age = got_in - reading['when']
        minutes = int(age.total_seconds() // 60)
        lines.append(
            f"  reading : {_when(reading['when'])}, {minutes // 60}h "
            f"{minutes % 60:02d}m before - trend {reading['trend']}, regime "
            f"{reading['regime']}, RSI {reading['rsi']}, ADX "
            f"{reading['adx']}")
        beside = _beside(trade['direction'], reading)
        if beside == 'mixed':
            words = f"the recorded trend was {reading['trend']}"
        else:
            words = f"{beside.upper()} the recorded trend"
        lines.append(f"            you went {trade['direction']}: {words}")
    return lines


def _row(label, text):
    return f'  {label:<23}: {text}'


def _total_lines(trades, worked, besides):
    """Every trade -> the totals block."""
    results = [figures['result'] for figures in worked]
    won = sum(1 for value in results if _round(value, 2) > 0)
    lost = sum(1 for value in results if _round(value, 2) < 0)
    flat = len(results) - won - lost
    lines = [
        DOUBLE,
        f'TOTALS - {_count(len(trades))}',
        _row('your result', f'{_signed_usd(_sum(results))}  '
                            f'(won {won}, lost {lost}, flat {flat})'),
        '',
    ]
    stopped = [figures for figures in worked if figures['stopped']]
    unstopped = len(worked) - len(stopped)
    if stopped:
        reached = sum(1 for figures in stopped if figures['cap_reached'])
        lines += [
            f'  THE SAME TRADES SIZED TO RISK 1% - '
            f'{_count(len(stopped))} had a stop',
            _row('your result on those', _signed_usd(_own_on_stopped(worked))),
            _row('at 1% risk', _signed_usd(
                _sum(figures['pure_result'] for figures in stopped))),
            _row('with the 25% cap',
                 f"{_signed_usd(_sum(f['capped_result'] for f in stopped))}"
                 f'  (cap reached on {reached} of {len(stopped)})'),
        ]
        if unstopped:
            lines.append(f"  {_count(unstopped)} had no stop and "
                         f"{'is' if unstopped == 1 else 'are'} in none of "
                         f"these three lines.")
        risks = [figures['risked_pct'] for figures in stopped]
        above = sum(1 for value in risks if value > 1)
        lines += [
            '',
            f'  WHAT YOU RISKED - {_count(len(stopped))} had a stop',
            f'  smallest {_pct(min(risks))}, largest {_pct(max(risks))} of '
            f'account; above 1% on {above} of {len(stopped)}',
        ]
    else:
        lines.append('  THE SAME TRADES SIZED TO RISK 1% - no trade had a '
                     'stop, so there is nothing to compare.')
    lines += ['', '  BESIDE THE RECORDED TREND']
    for key, label in (('with', 'with the trend'),
                       ('against', 'against the trend'),
                       ('mixed', 'trend was MIXED'),
                       ('none', 'no reading')):
        chosen = [figures['result'] for figures, beside
                  in zip(worked, besides) if beside == key]
        lines.append(_row(label, f'{_count(len(chosen))}, '
                                 f'{_signed_usd(_sum(chosen))}'))
    lines += ['', '  BY FEELING']
    for feeling in sorted({trade['feeling'] for trade in trades}):
        chosen = [figures['result'] for trade, figures
                  in zip(trades, worked) if trade['feeling'] == feeling]
        lines.append(_row(feeling, f'{_count(len(chosen))}, '
                                   f'{_signed_usd(_sum(chosen))}'))
    lines += ['', '  BY MONTH LOGGED']
    for month in sorted({trade['logged'].strftime('%Y-%m')
                         for trade in trades}):
        chosen = [figures['result'] for trade, figures
                  in zip(trades, worked)
                  if trade['logged'].strftime('%Y-%m') == month]
        lines.append(_row(month, f'{_count(len(chosen))}, '
                                 f'{_signed_usd(_sum(chosen))}'))
    lines.append(DOUBLE)
    return lines


def _closing_lines():
    return ['The readings are what the instruments recorded. They are not '
            'predictions.',
            'The 1% lines are the same trades at another size. Nothing '
            'more.']


TITLE = 'ZAR X - THE MIRROR'
DISCLAIMER = 'Arithmetic only. Before fees. Nothing here is a signal or advice.'


def _valid_month(month):
    try:
        datetime.strptime(month, '%Y-%m')
    except (ValueError, TypeError):
        return False
    return len(month) == 7


def mirror_text(trades_path=None, snapshot_paths=None, month=None):
    """THE DOORWAY. The whole report, as text.

    Never raises and never prints; it RETURNS. Settings resolve from None IN
    THE BODY, so this module's own constants are read fresh on every call.
    """
    try:
        trades_path = TRADES_FILE if trades_path is None else trades_path
        snapshot_paths = (SNAPSHOT_FILES if snapshot_paths is None
                          else snapshot_paths)
        head = [TITLE]
        if month is not None and not _valid_month(month):
            return '\n'.join(head + [f'{month!r} is not a month. Write it '
                                     f'like 2026-11.']) + '\n'

        state, trades, unreadable, found = _read_trades(trades_path)
        if state == 'missing':
            return '\n'.join(head + [
                'There is no trade journal yet. Nothing has been logged.',
                '(LOG_TRADE.bat records a trade once it is closed.)']) + '\n'
        if state == 'empty':
            return '\n'.join(head + [
                'The trade journal is empty. Nothing has been logged.']) + '\n'
        if state == 'bad header':
            return '\n'.join(head + [
                'The trade journal does not start with the eleven column '
                'names this Mirror knows, so NOTHING was read from it.',
                '  expected: ' + ','.join(HEADER),
                '  found   : ' + ','.join(found)]) + '\n'

        readings, files, rows_read, rows_skipped = _read_snapshots(
            snapshot_paths)
        head += [
            'Your logged trades, what the instruments had recorded, and the '
            'same trades sized to risk 1%.',
            DISCLAIMER,
            '',
            f'journal   : {_count(len(trades))} read, '
            f'{_count(len(unreadable), "row")} could not be read',
        ]
        head += [f'            row {number}: {reason}'
                 for number, reason in unreadable]
        head.append(f'readings  : {_count(rows_read, "snapshot row")} read '
                    f'from {files} of {len(snapshot_paths)} notebooks, '
                    f'{_count(rows_skipped, "row")} could not be read')
        if month is None:
            head.append('covering  : every trade in the journal')
        else:
            trades = [trade for trade in trades
                      if trade['logged'].strftime('%Y-%m') == month]
            head.append(f'covering  : trades logged in {month}')
        if not trades:
            if month is None:
                head.append('The trade journal has no trades in it that '
                            'could be read.')
            else:
                head.append(f'No trades were logged in {month}.')
            return '\n'.join(head) + '\n'

        body, worked, besides = [], [], []
        for number, trade in enumerate(trades, start=1):
            figures = _work_out(trade)
            got_in = _got_in(trade['logged'], trade['hours'])
            reading = _pick(_readings_for(readings, trade['asset']), got_in)
            worked.append(figures)
            besides.append(_beside(trade['direction'], reading))
            body += _trade_lines(number, trade, figures, got_in, reading)
        lines = (head + body + _total_lines(trades, worked, besides)
                 + _closing_lines())
        return '\n'.join(lines) + '\n'
    except Exception as exc:
        return (f'{TITLE}\n[the Mirror could not finish: '
                f'{type(exc).__name__}]\n')
if __name__ == '__main__':
    if '--gate' not in sys.argv:
        # THE SHELL. The only place outside the gate that writes to a
        # stream. **BYTES, IN UTF-8, WHATEVER THE CONSOLE THINKS IT IS** -
        # his own WHY line may hold any character at all, and a `print()`
        # on a console that cannot show one would greet him with a
        # traceback instead of his report.
        month = None
        if '--month' in sys.argv:
            at = sys.argv.index('--month')
            month = sys.argv[at + 1] if at + 1 < len(sys.argv) else ''
        text = mirror_text(month=month)
        sys.stdout.buffer.write(text.replace('\n', '\r\n').encode('utf-8'))
        sys.stdout.buffer.flush()
        sys.exit(0)

    # =====================================================================
    # GATE 5.2 — declared in PROGRESS_LOG.md on 2026-11-15 and committed
    # with no `.py` in that commit, BEFORE this file existed.
    #
    # Everything below lives inside `__main__` on purpose: the production
    # half above is untouched by any of it.
    #
    # **THE GATE NEVER TOUCHES `journal/my_trades.csv` OR A REAL NOTEBOOK.**
    # Every check reads files it wrote itself into a temporary directory.
    # =====================================================================
    import hashlib
    import re
    import shutil
    import subprocess
    import tempfile

    sys.path.insert(0, JOURNAL_DIR)
    import log_trade as logger          # the REAL logger writes the fakes

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def differ(expected, got):
        """Show the first line where two reports part company."""
        a, b = expected.split('\n'), (got or '').split('\n')
        for at in range(max(len(a), len(b))):
            left = a[at] if at < len(a) else '<nothing>'
            right = b[at] if at < len(b) else '<nothing>'
            if left != right:
                return (f"line {at + 1}: the gate expected {left!r} and the "
                        f"Mirror said {right!r}")
        return ''

    def same(expected, got):
        ok = expected == got
        if not ok:
            print(f"        {differ(expected, got)}")
        return ok

    def fingerprint(path):
        if not os.path.exists(path):
            return 'NO FILE'
        with open(path, 'rb') as handle:
            return hashlib.sha256(handle.read()).hexdigest()

    REAL_JOURNAL_AT_START = fingerprint(TRADES_FILE)
    WORK = tempfile.mkdtemp(prefix='zarx_gate52_')
    NL = chr(13) + chr(10)
    UTC = timezone.utc

    def room():
        return tempfile.mkdtemp(prefix='zarx_g52_', dir=WORK)

    # THE TWO HEADERS, TYPED OUT HERE. Never read from either module.
    J_HEAD = ('utc_time,asset,direction,entry,exit,stop,size_usd,'
              'account_usd,in_hours_ago,why,feeling')
    S_HEAD = ('utc_time,asset,timeframe,close,trend,rsi,atr,atr_pct,regime,'
              'entropy,adx')
    LOGGER_REFUSED = []

    def put(path, lines):
        with open(path, 'wb') as handle:
            handle.write((NL.join(lines) + NL).encode('utf-8'))
        return path

    def journal(trades, by_hand=(), where=None):
        """Fake trades -> a journal. **EVERY TRADE GOES THROUGH THE REAL
        LOGGER'S DOORWAY**; rows in `by_hand` are appended raw, for the
        shapes the logger itself would refuse to write."""
        path = os.path.join(where or room(), 'my_trades.csv')
        for when, answers in trades:
            said = logger.log_trade(*answers, path=path, now=when)
            if not said.startswith('logged: '):
                LOGGER_REFUSED.append(said)
        if by_hand:
            if not os.path.exists(path):
                put(path, [J_HEAD])
            with open(path, 'ab') as handle:
                handle.write((NL.join(by_hand) + NL).encode('utf-8'))
        return path

    def notebooks(local=(), cloud=(), frozen=(), where=None):
        """Snapshot rows -> three notebooks under the ship's own names."""
        folder = where or room()
        return (put(os.path.join(folder, 'snapshots_local.csv'),
                    [S_HEAD] + list(local)),
                put(os.path.join(folder, 'snapshots_cloud.csv'),
                    [S_HEAD] + list(cloud)),
                put(os.path.join(folder, 'snapshots.csv'),
                    [S_HEAD] + list(frozen)))

    def snap(when, asset, trend, regime='Ranging', rsi='50.0', adx='20.0'):
        return f'{when},{asset},4h,100.00,{trend},{rsi},1.00,1.00,{regime},1.950,{adx}'

    # ---- THE THREE FAKE TRADES OF THE PLAN'S SENTENCE --------------------
    # A long that won; a short that lost, held past its stop, and is CAPPED
    # by the 25% rule; and a trade with no stop.
    T1 = (datetime(2026, 10, 10, 12, 0, 0, tzinfo=UTC),
          ('BTC', 'long', '100.00', '110.00', '95.00', '4000', '10000', '6',
           'trend was up and I waited', 'calm'))
    T2 = (datetime(2026, 10, 11, 9, 30, 0, tzinfo=UTC),
          ('eth', 'SHORT', '2000.00', '2050.00', '2020.00', '1500', '10000',
           '30', 'funding was extreme, faded it', 'Nervous'))
    T3 = (datetime(2026, 10, 12, 8, 0, 0, tzinfo=UTC),
          ('SOL', 'long', '80.00', '76.00', 'none', '500', '10000', '0',
           'breakout, no plan', 'calm'))
    # A ROW THE LOGGER WOULD NEVER WRITE: the shape a spreadsheet leaves
    # behind when somebody types in the wrong cell.
    BROKEN = ('2026-10-12T09:00:00+00:00,BTC-USD,long,100.00,abc,95.00,1000,'
              '10000,2,edited in a spreadsheet,calm')

    LOCAL = ('2026-10-10 00:05,BTC-USD,4h,99.00,DOWN,40.0,1.00,1.01,Ranging,'
             '1.900,20.0',
             '2026-10-10 04:05,BTC-USD,4h,99.50,UP,55.4,1.20,1.21,Ranging,'
             '1.952,23.3',
             # TAKEN AFTER HE GOT IN, AND IT SAYS THE OPPOSITE. A trap.
             '2026-10-10 08:05,BTC-USD,4h,105.00,DOWN,60.0,1.30,1.24,'
             'Trending,1.910,31.0')
    CLOUD = ('2026-10-09 23:49,ETH-USD,4h,1990.00,UP,61.0,20.00,1.01,'
             'Trending,1.940,30.5',
             # AFTER HE GOT IN, AND NEARER. Another trap.
             '2026-10-10 04:11,ETH-USD,4h,2001.00,DOWN,48.0,21.00,1.05,'
             'Chaotic,1.990,18.0')
    # EIGHT HOURS AND ONE MINUTE before trade three. One minute too old.
    FROZEN = ('2026-10-11 23:59,SOL-USD,4h,81.00,UP,58.0,1.50,1.85,Ranging,'
              '1.950,22.0',)

    def plan_fixture(where=None):
        folder = where or room()
        return (journal([T1, T2, T3], by_hand=[BROKEN], where=folder),
                notebooks(LOCAL, CLOUD, FROZEN, where=folder))

    # ---- THE WHOLE REPORT, TYPED OUT BY HAND -----------------------------
    # EVERY FIGURE BELOW WAS WORKED BY HAND FROM THE ARITHMETIC IN THE BAR:
    #   T1  move +10/100 = +0.10 .. 4000 x 0.10 = +400.00 = +4.00% of 10000
    #       gap 5/100 = 0.05 .. risked 4000 x 0.05 = 200.00 = 2.00% .. R +2.00
    #       1% size 100 / 0.05 = 2000 -> +200.00 ; cap 2500, not reached
    #   T2  short: move (2000-2050)/2000 = -0.025 .. 1500 x -0.025 = -37.50
    #       = -0.375% -> -0.38 half up ; gap 20/2000 = 0.01 .. risked 15.00
    #       = 0.15% .. R -37.50/15 = -2.50
    #       1% size 100 / 0.01 = 10000 -> -250.00 ; cap 2500 -> -62.50,
    #       capped, risk 2500 x 0.01 = 25 = 0.25%
    #   T3  move -4/80 = -0.05 .. 500 x -0.05 = -25.00 = -0.25% ; no stop
    #   totals  400 - 37.50 - 25 = +337.50 ; with a stop 400 - 37.50 =
    #       +362.50 ; 1% 200 - 250 = -50.00 ; capped 200 - 62.50 = +137.50
    #       calm 400 - 25 = +375.00
    #   times   T1 in at 12:00 - 6h = 06:00, reading 04:05 = 1h 55m before
    #           T2 in at 11th 09:30 - 30h = 10th 03:30, reading 9th 23:49 =
    #           3h 41m before ; T3 in at 08:00, reading 23:59 = 8h 01m: none
    EXPECTED = '\n'.join([
        "ZAR X - THE MIRROR",
        "Your logged trades, what the instruments had recorded, and the "
        "same trades sized to risk 1%.",
        "Arithmetic only. Before fees. Nothing here is a signal or advice.",
        "",
        "journal   : 3 trades read, 1 row could not be read",
        "            row 5: the exit price 'abc' is not a number",
        "readings  : 6 snapshot rows read from 3 of 3 notebooks, 0 rows "
        "could not be read",
        "covering  : every trade in the journal",
        "-" * 70,
        "TRADE 1 - BTC-USD long - logged 2026-10-10 12:00 UTC",
        "  in 100.00 -> out 110.00, size $4,000.00, account $10,000.00",
        '  why     : "trend was up and I waited"',
        "  feeling : calm",
        "  result  : +$400.00  (+4.00% of account)",
        "  stop    : 95.00 - you risked $200.00 (2.00% of account) - result "
        "+2.00 R",
        "  same trade at 1% risk  : size $2,000.00 -> +$200.00",
        "  same, with the 25% cap : size $2,000.00 -> +$200.00  (cap not "
        "reached)",
        "  got in  : about 2026-10-10 06:00 UTC (you typed 6 hours ago)",
        "  reading : 2026-10-10 04:05 UTC, 1h 55m before - trend UP, regime "
        "Ranging, RSI 55.4, ADX 23.3",
        "            you went long: WITH the recorded trend",
        "-" * 70,
        "TRADE 2 - ETH-USD short - logged 2026-10-11 09:30 UTC",
        "  in 2000.00 -> out 2050.00, size $1,500.00, account $10,000.00",
        '  why     : "funding was extreme, faded it"',
        "  feeling : nervous",
        "  result  : -$37.50  (-0.38% of account)",
        "  stop    : 2020.00 - you risked $15.00 (0.15% of account) - "
        "result -2.50 R",
        "  same trade at 1% risk  : size $10,000.00 -> -$250.00",
        "  same, with the 25% cap : size $2,500.00 -> -$62.50  (capped; "
        "risk 0.25% of account)",
        "  got in  : about 2026-10-10 03:30 UTC (you typed 30 hours ago)",
        "  reading : 2026-10-09 23:49 UTC, 3h 41m before - trend UP, regime "
        "Trending, RSI 61.0, ADX 30.5",
        "            you went short: AGAINST the recorded trend",
        "-" * 70,
        "TRADE 3 - SOL-USD long - logged 2026-10-12 08:00 UTC",
        "  in 80.00 -> out 76.00, size $500.00, account $10,000.00",
        '  why     : "breakout, no plan"',
        "  feeling : calm",
        "  result  : -$25.00  (-0.25% of account)",
        "  stop    : none - the 1% comparison cannot be worked out for this "
        "trade",
        "  got in  : about 2026-10-12 08:00 UTC (you typed 0 hours ago)",
        "  reading : none within 8 hours before you got in",
        "=" * 70,
        "TOTALS - 3 trades",
        "  your result            : +$337.50  (won 1, lost 2, flat 0)",
        "",
        "  THE SAME TRADES SIZED TO RISK 1% - 2 trades had a stop",
        "  your result on those   : +$362.50",
        "  at 1% risk             : -$50.00",
        "  with the 25% cap       : +$137.50  (cap reached on 1 of 2)",
        "  1 trade had no stop and is in none of these three lines.",
        "",
        "  WHAT YOU RISKED - 2 trades had a stop",
        "  smallest 0.15%, largest 2.00% of account; above 1% on 1 of 2",
        "",
        "  BESIDE THE RECORDED TREND",
        "  with the trend         : 1 trade, +$400.00",
        "  against the trend      : 1 trade, -$37.50",
        "  trend was MIXED        : 0 trades, $0.00",
        "  no reading             : 1 trade, -$25.00",
        "",
        "  BY FEELING",
        "  calm                   : 2 trades, +$375.00",
        "  nervous                : 1 trade, -$37.50",
        "",
        "  BY MONTH LOGGED",
        "  2026-10                : 3 trades, +$337.50",
        "=" * 70,
        "The readings are what the instruments recorded. They are not "
        "predictions.",
        "The 1% lines are the same trades at another size. Nothing more.",
    ]) + '\n'

    print("=" * 70)
    print("GATE 5.2 — THE MIRROR. Sixteen conditions, declared before this")
    print("file existed.")
    print("=" * 70)

    print("\n(a) M-1 — ONE DOORWAY THAT NEVER RAISES AND NEVER PRINTS.")
    P_JOURNAL, P_BOOKS = plan_fixture()
    said = mirror_text(trades_path=P_JOURNAL, snapshot_paths=P_BOOKS)
    mark(isinstance(said, str) and said.startswith('ZAR X - THE MIRROR'),
         "the doorway RETURNED the report as text")
    mark(LOGGER_REFUSED == [],
         "and all three fake trades went in THROUGH THE REAL LOGGER'S "
         "DOORWAY, which accepted every one",
         f"refusals: {LOGGER_REFUSED}")
    for words, kw in (
            ('a journal path that is not a path at all',
             dict(trades_path=object(), snapshot_paths=P_BOOKS)),
            ('notebook paths that are not paths',
             dict(trades_path=P_JOURNAL, snapshot_paths=[object(), 7])),
            ('notebooks that are not a list',
             dict(trades_path=P_JOURNAL, snapshot_paths=5)),
            ('a month that is not text',
             dict(trades_path=P_JOURNAL, snapshot_paths=P_BOOKS,
                  month=202610))):
        try:
            answer = mirror_text(**kw)
            raised = False
        except Exception as exc:                       # noqa: BLE001
            answer, raised = f'{type(exc).__name__}: {exc}', True
        mark(not raised and isinstance(answer, str)
             and answer.startswith('ZAR X - THE MIRROR')
             and 'TRADE 1' not in answer,
             f"{words} -> a plain line, not an exception and not a report",
             answer.strip().split('\n')[-1][:110])
    mark(mirror_text.__defaults__ == (None, None, None),
         "and all three settings are `None` in the signature and resolved "
         "in the body",
         f"defaults {mirror_text.__defaults__}")

    print("\n(b) >>> M-3 — THE PLAN'S OWN SENTENCE: `log 2 fake trades, run"
          "\n    mirror, numbers check out by hand`. Three fake trades went"
          "\n    through the real logger, a fourth row was broken by hand,"
          "\n    and the WHOLE REPORT must equal one typed out in this gate,"
          "\n    character for character, whose every figure was worked by"
          "\n    hand in the comment above it.")
    mark(same(EXPECTED, said),
         "the report equals the one typed out by hand — every result, "
         "every risk figure, every R, both 1% lines, the cap, all three "
         "times, both readings, the missing reading, the unreadable row and "
         "every total",
         f"{len(said)} characters, {said.count(chr(10))} lines")
    mark(said.count('\n') == EXPECTED.count('\n') == 69
         and len(EXPECTED) > 3000,
         "and the typed-out report is the size it is typed out to be — 69 "
         "lines — so an expectation that had quietly been emptied cannot "
         "pass by matching an empty report")

    print("\n(c) >>> M-2 — IT WRITES NOTHING, EVER. sha256 of the journal and"
          "\n    of every notebook before and after, and the folder's file"
          "\n    list before and after.")
    folder = os.path.dirname(P_JOURNAL)
    before = ({name: fingerprint(os.path.join(folder, name))
               for name in sorted(os.listdir(folder))})
    for _ in range(3):
        mirror_text(trades_path=P_JOURNAL, snapshot_paths=P_BOOKS)
        mirror_text(trades_path=P_JOURNAL, snapshot_paths=P_BOOKS,
                    month='2026-10')
    after = ({name: fingerprint(os.path.join(folder, name))
              for name in sorted(os.listdir(folder))})
    mark(before == after and len(before) == 4,
         "four files before, the same four after, every sha256 unmoved "
         "across six runs",
         ', '.join(f'{name} {digest[:8]}' for name, digest in after.items()))
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        SOURCE = handle.read()
    MAIN_LINE = "if __name__ == '__main__':"
    PRODUCTION = SOURCE.split('\n' + MAIN_LINE)[0]
    opens = re.findall(r'\bopen\(([^)]*)\)', PRODUCTION)
    WRITERS = ("'w'", "'a'", "'x'", "'r+'", "'wb'", "'ab'", '"w"', '"a"',
               'os.remove', 'os.rename', 'os.replace', 'os.unlink',
               'shutil', '.write(', '.writerow', 'os.makedirs', 'os.mkdir',
               'truncate')
    mark(len(opens) == 2
         and all("encoding='utf-8', newline=''" in call for call in opens)
         and not any(word in PRODUCTION for word in WRITERS)
         and SOURCE.count('\n' + MAIN_LINE) == 1,
         "and the production half holds exactly TWO `open(` calls, both "
         "read-only, and not one of eighteen words that write, rename or "
         "delete — counted from the file's own text above its `__main__` "
         "line",
         f"{len(opens)} opens: {opens}")

    print("\n(d) M-4 — NO JOURNAL, AN EMPTY ONE, AND ONE WITH ONLY A HEADER."
          "\n    Never a traceback on the day he first tries it.")
    nowhere = os.path.join(room(), 'my_trades.csv')
    mark(mirror_text(trades_path=nowhere, snapshot_paths=P_BOOKS) == (
         'ZAR X - THE MIRROR\n'
         'There is no trade journal yet. Nothing has been logged.\n'
         '(LOG_TRADE.bat records a trade once it is closed.)\n'),
         "NO JOURNAL -> three calm lines, typed out here")
    mark(not os.path.exists(nowhere),
         "and asking did not CREATE the journal")
    empty = os.path.join(room(), 'my_trades.csv')
    with open(empty, 'wb') as handle:
        handle.write(b'')
    mark(mirror_text(trades_path=empty, snapshot_paths=P_BOOKS) == (
         'ZAR X - THE MIRROR\n'
         'The trade journal is empty. Nothing has been logged.\n'),
         "AN EMPTY FILE -> two calm lines, typed out here")
    only_head = put(os.path.join(room(), 'my_trades.csv'), [J_HEAD])
    answer = mirror_text(trades_path=only_head, snapshot_paths=P_BOOKS)
    mark(answer.endswith('covering  : every trade in the journal\n'
                         'The trade journal has no trades in it that could '
                         'be read.\n')
         and 'journal   : 0 trades read, 0 rows could not be read' in answer
         and 'TOTALS' not in answer,
         "A HEADER AND NOTHING ELSE -> it says so, and prints no totals "
         "about nothing")

    print("\n(e) M-5 — A HEADER THE MIRROR DOES NOT KNOW STOPS IT, BY NAME.")
    OLD_EIGHT = 'utc_time,asset,direction,entry,exit,size,why,feeling'
    old = put(os.path.join(room(), 'my_trades.csv'),
              [OLD_EIGHT,
               '2026-09-08T09:30:15+00:00,BTC-USD,long,100.50,111.00,0.25,'
               'the seven-question shape,calm'])
    answer = mirror_text(trades_path=old, snapshot_paths=P_BOOKS)
    mark('NOTHING was read' in answer and OLD_EIGHT in answer
         and J_HEAD in answer and 'TRADE 1' not in answer
         and 'TOTALS' not in answer,
         "a journal in the OLD seven-question shape is refused whole, and "
         "both headers — the one expected and the one found — are shown",
         answer.strip().split('\n')[1][:100])
    moved = put(os.path.join(room(), 'my_trades.csv'),
                [J_HEAD.replace('entry,exit', 'exit,entry'),
                 '2026-10-10T12:00:00+00:00,BTC-USD,long,110.00,100.00,'
                 '95.00,4000,10000,6,two columns exchanged,calm'])
    answer = mirror_text(trades_path=moved, snapshot_paths=P_BOOKS)
    mark('NOTHING was read' in answer and 'TRADE 1' not in answer,
         "and so is one whose `entry` and `exit` columns were exchanged in "
         "a spreadsheet — the Mirror never reads by position a file whose "
         "columns it cannot vouch for")

    print("\n(f) >>> M-6 — A ROW IT CANNOT READ IS NAMED AND COUNTED, never"
          "\n    dropped in silence and never included. B13 printed a true"
          "\n    report about what was left.")
    GOOD_ROW = ('2026-10-10T12:00:00+00:00,BTC-USD,long,100.00,110.00,95.00,'
                '4000,10000,6,a row that is fine,calm')
    BAD_ROWS = (
        ('2026-10-10T12:00:00+00:00,BTC-USD,long,100.00,110.00,95.00,4000,'
         '10000,6,calm', 'row 3: it has 10 columns, not 11'),
        ('10/10/2026 12:00,BTC-USD,long,100.00,110.00,95.00,4000,10000,6,'
         'x,calm', "row 4: the time '10/10/2026 12:00' is not a UTC stamp"),
        ('2026-10-10T12:00:00+00:00,BTC-USD,LONG,100.00,110.00,95.00,4000,'
         '10000,6,x,calm', "row 5: the direction 'LONG' is not long or "
                           "short"),
        ('2026-10-10T12:00:00+00:00,BTC-USD,long,100.00,110.00,95.00,0,'
         '10000,6,x,calm', "row 6: the size '0' is not above zero"),
        ('2026-10-10T12:00:00+00:00,BTC-USD,long,100.00,110.00,105.00,4000,'
         '10000,6,x,calm', 'row 7: the stop 105.00 is on the wrong side of '
                           'the entry 100.00 for a long'),
        ('2026-10-10T12:00:00+00:00,BTC-USD,long,100.00,110.00,95.00,4000,'
         '10000,-1,x,calm', "row 8: the hours '-1' is below zero"),
        ('2026-10-10T12:00:00+00:00,BTC-USD,long,100.00,110.00,95.00,4000,'
         'NaN,6,x,calm', "row 9: the account size 'NaN' is not a number"),
        ('2026-10-10T12:00:00+00:00,BTC-USD,short,100.00,110.00,100.00,'
         '4000,10000,6,x,calm', 'row 10: the stop 100.00 is on the wrong '
                                'side of the entry 100.00 for a short'),
    )
    mixed = put(os.path.join(room(), 'my_trades.csv'),
                [J_HEAD, GOOD_ROW] + [row_ for row_, _why in BAD_ROWS])
    answer = mirror_text(trades_path=mixed, snapshot_paths=P_BOOKS)
    mark('journal   : 1 trade read, 8 rows could not be read' in answer,
         "one good row among eight broken ones: ONE trade read, EIGHT "
         "rows counted as unreadable")
    mark(all(reason in answer for _row_, reason in BAD_ROWS),
         "and each of the eight is NAMED with its own row number and its "
         "own reason",
         ' | '.join(reason.split(': ')[1][:28] for _r, reason in BAD_ROWS))
    mark(answer.count('\nTRADE ') == 1 and 'TOTALS - 1 trade\n' in answer
         and '  your result            : +$400.00  (won 1, lost 0, flat 0)'
         in answer,
         "and not one of the eight leaked into the totals: one trade, "
         "+$400.00")

    print("\n(g) >>> M-7 — THE TIME RULE, AT EVERY TURNOVER. He got in at"
          "\n    06:00:30 UTC on the 10th (logged 12:00:30, typed 6 hours).")
    T_SEC = (datetime(2026, 10, 10, 12, 0, 30, tzinfo=UTC), T1[1])

    def reading_of(local=(), cloud=(), frozen=(), trade=T_SEC):
        """-> the `reading :` line the Mirror prints for one trade, plus
        the line under it."""
        where = room()
        text = mirror_text(trades_path=journal([trade], where=where),
                           snapshot_paths=notebooks(local, cloud, frozen,
                                                    where=where))
        lines = text.split('\n')
        for at, line in enumerate(lines):
            if line.startswith('  reading :'):
                return line + ' | ' + lines[at + 1].strip()
        return '<no reading line at all>'

    NONE_LINE = '  reading : none within 8 hours before you got in'
    got = reading_of(local=[snap('2026-10-10 06:00', 'BTC-USD', 'UP')])
    mark(got.startswith('  reading : 2026-10-10 06:00 UTC, 0h 00m before'),
         "a snapshot taken in THE SAME MINUTE he got in is used", got[:60])
    got = reading_of(local=[snap('2026-10-10 06:01', 'BTC-USD', 'UP')])
    mark(got.startswith(NONE_LINE),
         "one taken ONE MINUTE AFTER is NOT used — it is information he "
         "did not have", got[:60])
    got = reading_of(local=[snap('2026-10-09 22:01', 'BTC-USD', 'UP')])
    mark(got.startswith('  reading : 2026-10-09 22:01 UTC, 7h 59m before'),
         "one 7h 59m old is used", got[:60])
    T_FLAT = (datetime(2026, 10, 10, 12, 0, 0, tzinfo=UTC), T1[1])
    got = reading_of(local=[snap('2026-10-09 22:00', 'BTC-USD', 'UP')],
                     trade=T_FLAT)
    mark(got.startswith('  reading : 2026-10-09 22:00 UTC, 8h 00m before'),
         "one EXACTLY 8h 00m old is used — the limit itself is inside",
         got[:60])
    got = reading_of(local=[snap('2026-10-10 06:00', 'BTC-USD', 'UP')],
                     trade=T_FLAT)
    mark(got.startswith('  reading : 2026-10-10 06:00 UTC, 0h 00m before'),
         "one taken at THE VERY INSTANT he got in — 06:00:00 against "
         "06:00:00 — is used: `at or before` includes `at`", got[:60])
    T_HALF = (datetime(2026, 10, 10, 12, 0, 0, tzinfo=UTC),
              T1[1][:7] + ('1.5',) + T1[1][8:])
    where = room()
    text = mirror_text(trades_path=journal([T_HALF], where=where),
                       snapshot_paths=notebooks(where=where))
    mark('  got in  : about 2026-10-10 10:30 UTC (you typed 1.5 hours ago)'
         in text,
         "HALF HOURS COUNT: logged at 12:00 and `1.5` hours typed is 10:30, "
         "not 11:00 — the hours are never cut down to a whole number")
    got = reading_of(local=[snap('2026-10-09 21:59', 'BTC-USD', 'UP')],
                     trade=T_FLAT)
    mark(got.startswith(NONE_LINE),
         "and one 8h 01m old is NOT: the turnover is at eight hours, to "
         "the minute", got[:60])
    got = reading_of(local=[snap('2026-10-10 02:00', 'BTC-USD', 'UP'),
                            snap('2026-10-10 05:00', 'BTC-USD', 'DOWN'),
                            snap('2026-10-10 03:00', 'BTC-USD', 'UP')])
    mark('2026-10-10 05:00 UTC' in got and 'trend DOWN' in got
         and 'AGAINST the recorded trend' in got,
         "of three candidates the NEWEST wins, wherever it sits in the "
         "notebook", got[:70])
    got = reading_of(local=[snap('2026-10-10 05:00', 'BTC-USD', 'UP')],
                     cloud=[snap('2026-10-10 05:00', 'BTC-USD', 'DOWN')])
    mark('trend UP' in got and 'WITH the recorded trend' in got,
         "two notebooks, the same coin, THE SAME MINUTE, different values: "
         "the first notebook in the fixed order — the laptop's — wins",
         got[:70])
    got = reading_of(cloud=[snap('2026-10-10 05:00', 'ETH-USD', 'DOWN')])
    mark(got.startswith(NONE_LINE),
         "a reading for ANOTHER COIN is never borrowed", got[:60])
    got = reading_of(frozen=[snap('2026-10-10 05:00', 'BTC-USD', 'MIXED')])
    mark('trend MIXED' in got and 'the recorded trend was MIXED' in got,
         "a MIXED trend is neither with nor against, and says so",
         got[-45:])
    where = room()
    text = mirror_text(
        trades_path=journal([T_SEC], where=where),
        snapshot_paths=notebooks(
            local=[snap('not a time', 'BTC-USD', 'DOWN'),
                   snap('2026-10-10 05:00', 'BTC-USD', 'UP'),
                   '2026-10-10 05:30,BTC-USD'], where=where))
    mark('readings  : 1 snapshot row read from 3 of 3 notebooks, 2 rows '
         'could not be read' in text and '2026-10-10 05:00 UTC' in text,
         "a snapshot row whose time will not parse, and one cut short, are "
         "SKIPPED AND COUNTED on the report — and the good row beside them "
         "is still used")
    where = room()
    text = mirror_text(trades_path=journal([T_SEC], where=where),
                       snapshot_paths=(os.path.join(where, 'a.csv'),
                                       os.path.join(where, 'b.csv'),
                                       os.path.join(where, 'c.csv')))
    mark('readings  : 0 snapshot rows read from 0 of 3 notebooks' in text
         and NONE_LINE in text and 'TOTALS - 1 trade' in text,
         "and with NO notebook on the disk at all the report still comes "
         "out: no reading, and the arithmetic untouched")

    print("\n(h) >>> M-8 AND M-9 — LIKE WITH LIKE, AND THE TOTALS ADD UP."
          "\n    Six trades with awkward numbers and three different account"
          "\n    sizes; every total is re-added by this gate FROM THE PRINTED"
          "\n    LINES, never from anything the Mirror hands over.")
    AWKWARD = [
        (datetime(2026, 9, 3, 10, 0, 0, tzinfo=UTC),
         ('BTC', 'long', '64123.45', '64987.10', '63500.00', '1234.56',
          '7500', '5', 'first', 'calm')),
        (datetime(2026, 9, 9, 10, 0, 0, tzinfo=UTC),
         ('ETH', 'short', '1811.42', '1790.66', '1850.00', '777.77', '7500',
          '12', 'second', 'bored')),
        (datetime(2026, 10, 2, 10, 0, 0, tzinfo=UTC),
         ('SOL', 'long', '71.11', '69.92', '70.50', '3333.33', '12000', '3',
          'third', 'calm')),
        (datetime(2026, 10, 2, 11, 0, 0, tzinfo=UTC),
         ('SOL', 'short', '73.64', '73.64', 'none', '500', '12000', '1',
          'fourth, flat', 'tired')),
        (datetime(2026, 10, 20, 10, 0, 0, tzinfo=UTC),
         ('BTC', 'short', '65216.00', '66001.37', 'none', '901.01', '300',
          '40', 'fifth', 'calm')),
        (datetime(2026, 10, 20, 10, 0, 0, tzinfo=UTC),
         ('BTC', 'short', '65216.00', '66001.37', 'none', '901.01', '300',
          '40', 'fifth', 'calm')),            # THE SAME TRADE TWICE
    ]
    where = room()
    A_TEXT = mirror_text(trades_path=journal(AWKWARD, where=where),
                         snapshot_paths=notebooks(where=where))

    def cents(text):
        """`+$1,234.50` / `-$37.50` / `$0.00` -> an exact Decimal."""
        sign = -1 if text.startswith('-') else 1
        return sign * Decimal(text.lstrip('+-').lstrip('$').replace(',', ''))

    MONEY = r'([+-]?\$[\d,]+\.\d\d)'
    per_trade = [cents(m) for m in re.findall(r'\n  result  : ' + MONEY,
                                              A_TEXT)]
    pure_lines = [cents(m) for m in re.findall(
        r'\n  same trade at 1% risk  : size \$[\d,.]+ -> ' + MONEY, A_TEXT)]
    cap_lines = [cents(m) for m in re.findall(
        r'\n  same, with the 25% cap : size \$[\d,.]+ -> ' + MONEY, A_TEXT)]

    def total(label):
        found = re.findall(r'\n  ' + re.escape(label) + r' *: ' + MONEY,
                           A_TEXT)
        return cents(found[0]) if len(found) == 1 else None

    mark(len(per_trade) == 6 and total('your result') == sum(per_trade),
         "YOUR RESULT equals the six printed per-trade results added up by "
         "this gate",
         f"{' '.join(str(v) for v in per_trade)} = {sum(per_trade)}")
    stopped_own = sum(per_trade[:3])     # the first three have a stop
    mark(len(pure_lines) == 3 and len(cap_lines) == 3
         and total('your result on those') == stopped_own
         and total('at 1% risk') == sum(pure_lines)
         and total('with the 25% cap') == sum(cap_lines),
         "LIKE WITH LIKE: only the three trades that had a stop are in the "
         "three comparison lines — HIS OWN result over those same three, "
         "the 1% total and the capped total each equal the printed lines "
         "added up here",
         f"own {stopped_own}, 1% {sum(pure_lines)}, capped {sum(cap_lines)}")
    mark('  3 trades had no stop and are in none of these three lines.'
         in A_TEXT
         and '  THE SAME TRADES SIZED TO RISK 1% - 3 trades had a stop'
         in A_TEXT,
         "and the three with no stop are counted out loud, in the plural")
    group_rows = re.findall(r'\n  ([a-z0-9 A-Z-]+?) *: (\d+) trades?, '
                            + MONEY, A_TEXT)
    groups = {label: (int(n), cents(m)) for label, n, m in group_rows}
    TREND = ('with the trend', 'against the trend', 'trend was MIXED',
             'no reading')
    FEEL = ('bored', 'calm', 'tired')
    MONTHS = ('2026-09', '2026-10')
    mark(all(sum(groups.get(k, (0, 0))[0] for k in keys) == 6
             and sum(groups.get(k, (0, 0))[1] for k in keys)
             == sum(per_trade) for keys in (TREND, FEEL, MONTHS)),
         "each of the three breakdowns — beside the trend, by feeling, by "
         "month — covers ALL SIX trades exactly once and adds back to the "
         "same total",
         f"{groups}")
    mark(groups.get('2026-09') == (2, sum(per_trade[:2]))
         and groups.get('2026-10') == (4, sum(per_trade[2:]))
         and groups.get('calm', (0, 0))[0] == 4,
         "and the months and feelings hold the trades that belong to them: "
         "two logged in September, four in October, four felt calm")
    mark(A_TEXT.count('TRADE 5 - BTC-USD short') == 1
         and A_TEXT.count('TRADE 6 - BTC-USD short') == 1
         and per_trade[4] == per_trade[5] and per_trade[4] != 0,
         "THE SAME TRADE LOGGED TWICE IS TWO TRADES, both counted — the "
         "logger keeps duplicates on purpose and the Mirror must not quietly "
         "merge them",
         f"{per_trade[4]} and {per_trade[5]}")
    mark(per_trade[3] == 0 and '  result  : $0.00  (0.00% of account)'
         in A_TEXT and 'flat 1)' in A_TEXT,
         "AN EXIT EQUAL TO THE ENTRY is a result of exactly $0.00, with no "
         "sign on it, counted as FLAT and not as a win or a loss")
    # By hand: 901.01 x (65216.00 - 66001.37)/65216.00 = -10.8505.. -> -10.85
    # and -10.8505../300 = -3.6168..% -> -3.62 half up. Account of $300.
    mark('  result  : -$10.85  (-3.62% of account)' in A_TEXT
         and 'size $901.01, account $300.00' in A_TEXT,
         "A SIZE LARGER THAN THE ACCOUNT is worked like any other, and the "
         "percentage is OF THAT TRADE'S OWN ACCOUNT — three different "
         "account sizes are never blended into one",
         "-$10.85 is -3.62% of $300.00")

    # SIXTY TRADES. Every other fixture in this gate holds six or fewer,
    # so a fault that only shows on a long journal - and a real journal
    # gets long - went green at 83/0 in this gate's own certification.
    # By hand: sixty copies of T1 at +$400.00 = +$24,000.00.
    where = room()
    text = mirror_text(trades_path=journal([T1] * 60, where=where),
                       snapshot_paths=notebooks(LOCAL, where=where))
    mark('journal   : 60 trades read, 0 rows could not be read' in text
         and 'covering  : every trade in the journal' in text
         and text.count('\nTRADE ') == 60 and '\nTRADE 60 - BTC-USD' in text
         and 'TOTALS - 60 trades\n' in text
         and '  your result            : +$24,000.00  (won 60, lost 0, '
             'flat 0)' in text
         and '  with the trend         : 60 trades, +$24,000.00' in text
         and '  at 1% risk             : +$12,000.00' in text,
         "A LONG JOURNAL — SIXTY TRADES — is read whole: sixty blocks, "
         "sixty in the totals, +$24,000.00, every one beside its reading, "
         "and nothing quietly narrowed to a month or a page")

    print("\n(i) >>> M-10 — NOT ONE WORD OF ADVICE OR JUDGEMENT. F8 printed"
          "\n    `>> strong buy signal` on an information-only deck and the"
          "\n    gate applauded.")
    FORBIDDEN = ('should', 'must', 'ought', 'buy', 'sell', 'signal',
                 'advice', 'advise', 'recommend', 'suggest', 'well done',
                 'good', 'bad', 'mistake', 'better', 'worse', 'worst',
                 'disciplin', 'careless', 'reckless', 'greed', 'smart',
                 'stupid', 'next time', 'try to', 'avoid', 'consider',
                 'opportunit', 'warning', 'too much', 'too big', 'too '
                 'small', 'shame', 'sorry', 'great', 'poor')
    HIS_DISCLAIMER = ('Arithmetic only. Before fees. Nothing here is a '
                      'signal or advice.')

    def mirror_own_words(text):
        """The report with HIS words and the one fixed disclaimer line
        taken out — what is left is everything the Mirror itself says."""
        kept = [line for line in text.split('\n')
                if not line.startswith('  why     : ')
                and line != HIS_DISCLAIMER]
        return '\n'.join(kept).lower()

    def clean(text):
        own = mirror_own_words(text)
        return not any(word in own for word in FORBIDDEN)

    mark(clean(said) and clean(A_TEXT)
         and said.count(HIS_DISCLAIMER) == 1,
         f"none of {len(FORBIDDEN)} forbidden words appears in anything the "
         f"Mirror itself says, on either report — and the one line that "
         f"names `signal` and `advice` does so to say there is none")
    mark(not clean(said + '\n>> you should size smaller next time')
         and not clean('  got in  : a good entry')
         and clean('  why     : "you should buy the dip, good signal"'),
         "THE JUDGE IS PROVED ABLE TO SAY NO, IN THIS RUN: it rejects a "
         "line of advice and a word of praise, and it does NOT blame the "
         "Mirror for words inside his own WHY line")
    # THREE SPACES AT EACH END, ON PURPOSE. A `.strip()` on the WHY line
    # here went green at 83/0 in this gate's own certification by attack.
    HIS_WORDS = '   I should buy the dip, he said "sell", bad signal   '
    T_WORDS = (T1[0], T1[1][:8] + (HIS_WORDS, 'calm'))
    where = room()
    text = mirror_text(trades_path=journal([T_WORDS], where=where),
                       snapshot_paths=notebooks(where=where))
    mark(f'  why     : "{HIS_WORDS}"' in text and clean(text),
         "HIS OWN WHY LINE IS QUOTED BACK UNTOUCHED — every word AND THE "
         "SPACES AT BOTH ENDS — even when it is full of those words. They "
         "are his, not the Mirror's",
         repr(HIS_WORDS))
    T_LINES = (T1[0], T1[1][:8] + ('first line' + chr(10) + 'second line',
                                   'calm'))
    where = room()
    text = mirror_text(trades_path=journal([T_LINES], where=where),
                       snapshot_paths=notebooks(where=where))
    mark('  why     : "first line / second line"' in text
         and text.count('\n') == mirror_text(
             trades_path=journal([T1], where=room()),
             snapshot_paths=notebooks(where=room())).count('\n'),
         "and a WHY line with a NEWLINE in it — the logger allows one — "
         "does not break the report in two: same number of lines, the two "
         "halves joined by ` / `")

    print("\n(j) THE REMAINING EDGES NAMED IN THE BAR.")
    # A stop exactly 1% away with the whole account as size: risk = 1.00%.
    T_ONE_PCT = (T1[0], ('BTC', 'long', '100.00', '103.00', '99.00', '10000',
                         '10000', '6', 'exactly one percent', 'calm'))
    where = room()
    text = mirror_text(trades_path=journal([T_ONE_PCT, T1], where=where),
                       snapshot_paths=notebooks(where=where))
    mark('you risked $100.00 (1.00% of account)' in text
         and 'above 1% on 1 of 2' in text
         and '  same trade at 1% risk  : size $10,000.00 -> +$300.00' in text
         and '  same, with the 25% cap : size $2,500.00 -> +$75.00  '
             '(capped; risk 0.25% of account)' in text,
         "A RISK OF EXACTLY 1.00% IS NOT `above 1%` — only the other trade, "
         "at 2.00%, is counted; and its capped line is $2,500.00 -> +$75.00, "
         "worked by hand: 2500 x 3/100")
    mark('had no stop' not in text,
         "and when EVERY trade had a stop, no line about missing stops is "
         "printed at all")
    where = room()
    text = mirror_text(trades_path=journal([T3], where=where),
                       snapshot_paths=notebooks(where=where))
    mark('  THE SAME TRADES SIZED TO RISK 1% - no trade had a stop, so '
         'there is nothing to compare.' in text
         and 'WHAT YOU RISKED' not in text and 'at 1% risk' not in text,
         "when NO trade had a stop the comparison says so in one line and "
         "prints no figures about nothing")
    # HALF UP, NOT HALF EVEN. 0.50 x 1/100 = $0.005 -> $0.01 (half-even
    # would give $0.00). 1250 x 1/100 = $12.50 = 0.125% of 10000 -> 0.13%
    # (half-even would give 0.12%). Both worked by hand.
    T_HALF_CENT = (T1[0], ('BTC', 'long', '100.00', '101.00', 'none', '0.50',
                           '10000', '6', 'half a cent', 'calm'))
    T_EIGHTH = (T1[0], ('BTC', 'long', '100.00', '101.00', 'none', '1250',
                        '10000', '6', 'an eighth of a percent', 'calm'))
    where = room()
    text = mirror_text(trades_path=journal([T_HALF_CENT, T_EIGHTH],
                                           where=where),
                       snapshot_paths=notebooks(where=where))
    mark('  result  : +$0.01  (0.00% of account)' in text
         and '  result  : +$12.50  (+0.13% of account)' in text
         and '  your result            : +$12.51  (won 2, lost 0, flat 0)'
         in text,
         "ROUNDING IS HALF UP AT THE EXACT HALF: half a cent is shown as "
         "$0.01 and 0.125% as 0.13% — banker's rounding would print $0.00 "
         "and 0.12% and no other fixture in this gate would notice")
    in_month = mirror_text(trades_path=P_JOURNAL, snapshot_paths=P_BOOKS,
                           month='2026-10')
    mark(in_month == EXPECTED.replace(
         'covering  : every trade in the journal',
         'covering  : trades logged in 2026-10'),
         "`--month 2026-10` gives the same report with ONE line changed — "
         "the line that says what it covers")
    mark(mirror_text(trades_path=P_JOURNAL, snapshot_paths=P_BOOKS,
                     month='2026-09').endswith(
         'covering  : trades logged in 2026-09\n'
         'No trades were logged in 2026-09.\n'),
         "a month with no trades in it says so and prints no totals")
    mark(all(mirror_text(trades_path=P_JOURNAL, snapshot_paths=P_BOOKS,
                         month=wrong) == f"ZAR X - THE MIRROR\n{wrong!r} is "
                                         f"not a month. Write it like "
                                         f"2026-11.\n"
             for wrong in ('2026-13', 'october', '2026-1', '', '26-10')),
         "and five things that are not a month are each refused by name, "
         "never read as `every trade`")

    print("\n(k) >>> M-11 — DOOR 3. A FRESH INTERPRETER imports this file,"
          "\n    calls the doorway three ways and SHUTS DOWN, and its TOTAL"
          "\n    output must be empty. A timeout is a FAILURE.")
    _ROOT_DIR = os.path.dirname(JOURNAL_DIR)
    probe_dir = tempfile.mkdtemp(prefix='zarx_d3mirror_')
    probe = os.path.join(probe_dir, 'seen.txt')
    child = ('import sys\n'
             'import journal.mirror as m\n'
             'J, A, B, C = sys.argv[2:6]\n'
             'n = 0\n'
             'm.mirror_text(trades_path=J, snapshot_paths=(A, B, C))\n'
             'n += 1\n'
             "m.mirror_text(trades_path=J + '.nowhere')\n"
             'n += 1\n'
             "m.mirror_text(trades_path=J, snapshot_paths=(A, B, C), "
             "month='2026-10')\n"
             'n += 1\n'
             "open(sys.argv[1], 'w', encoding='utf-8').write("
             'm.__file__ + chr(10) + str(n))\n')
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    timed_out, wrote, rc = False, b'', None
    try:
        done = subprocess.run([sys.executable, '-c', child, probe,
                               P_JOURNAL] + list(P_BOOKS),
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
    mark(not timed_out and rc == 0,
         "the fresh interpreter SHUT DOWN on its own", f"return code {rc}")
    mark(os.path.basename(seen_file) == 'mirror.py'
         and os.path.abspath(seen_file).startswith(os.path.abspath(_ROOT_DIR))
         and parts[1:] == ['3'],
         "the child imported THIS file and finished all three calls — "
         "proved by a probe FILE, never by a stream",
         seen or '(the child wrote no probe)')
    mark(wrote == b'',
         "IMPORT, three doorway calls and SHUTDOWN wrote nothing at all to "
         "any stream",
         '' if wrote == b'' else
         f"it wrote {wrote.decode('utf-8', 'replace')[:200]!r}")
    shutil.rmtree(probe_dir, ignore_errors=True)

    print("\n(l) >>> M-12 — THE PRODUCTION CALLING CONVENTION. **THE ONLY"
          "\n    REAL CALLER IS `mirror_text()` WITH NO ARGUMENTS.** Every"
          "\n    check above hands it paths, so `TRADES_FILE` and"
          "\n    `SNAPSHOT_FILES` were judged by nothing. A COPY of this file"
          "\n    in a tree of its own is run THE WAY `MIRROR.bat` RUNS IT —"
          "\n    as a script, no arguments — beside a journal and three"
          "\n    notebooks at addresses THIS GATE types out.")
    TREE = tempfile.mkdtemp(prefix='zarx_g52tree_')
    T_JOURNAL = os.path.join(TREE, 'journal')
    os.makedirs(T_JOURNAL)
    shutil.copyfile(os.path.abspath(__file__),
                    os.path.join(T_JOURNAL, 'mirror.py'))
    plan_fixture(where=T_JOURNAL)   # my_trades.csv + the three notebooks
    tree_before = {name: fingerprint(os.path.join(T_JOURNAL, name))
                   for name in sorted(os.listdir(T_JOURNAL))}
    t_out, t_rc, t_timed = b'', None, False
    try:
        t_done = subprocess.run([sys.executable,
                                 os.path.join(T_JOURNAL, 'mirror.py')],
                                cwd=TREE, env=env, capture_output=True,
                                stdin=subprocess.DEVNULL, timeout=90)
        t_out, t_rc = t_done.stdout, t_done.returncode
        t_err = t_done.stderr
    except subprocess.TimeoutExpired:
        t_timed, t_err = True, b''
    tree_after = {name: fingerprint(os.path.join(T_JOURNAL, name))
                  for name in sorted(os.listdir(T_JOURNAL))}
    mark(not t_timed and t_rc == 0 and t_err == b'',
         "the copy ran as a script with no arguments and finished clean",
         f"exit {t_rc}, timed out {t_timed}, stderr {t_err[:120]!r}")
    mark(t_out == EXPECTED.replace('\n', NL).encode('utf-8'),
         "and WHAT IT PRINTED IS THE HAND-TYPED REPORT, byte for byte, in "
         "UTF-8 with CRLF line endings — it found `my_trades.csv`, "
         "`snapshots_local.csv`, `snapshots_cloud.csv` and `snapshots.csv` "
         "beside itself with nobody telling it where to look",
         differ(EXPECTED, t_out.decode('utf-8', 'replace').replace(NL, '\n'))
         or f"{len(t_out)} bytes")
    mark(sorted(tree_before) == ['mirror.py', 'my_trades.csv',
                                 'snapshots.csv', 'snapshots_cloud.csv',
                                 'snapshots_local.csv']
         and tree_before == tree_after,
         "and the copy's folder holds the same five files with the same "
         "sha256 afterwards — the real caller wrote nothing either",
         ', '.join(sorted(tree_after)))
    os.remove(os.path.join(T_JOURNAL, 'my_trades.csv'))
    try:
        t_done = subprocess.run([sys.executable,
                                 os.path.join(T_JOURNAL, 'mirror.py'),
                                 '--month', '2026-10'],
                                cwd=TREE, env=env, capture_output=True,
                                stdin=subprocess.DEVNULL, timeout=90)
        t_first = t_done.stdout.decode('utf-8', 'replace')
        t_rc = t_done.returncode
    except subprocess.TimeoutExpired:
        t_first, t_rc = '<timed out>', None
    mark(t_rc == 0 and t_first == (
         'ZAR X - THE MIRROR' + NL
         + 'There is no trade journal yet. Nothing has been logged.' + NL
         + '(LOG_TRADE.bat records a trade once it is closed.)' + NL)
         and not os.path.exists(os.path.join(T_JOURNAL, 'my_trades.csv')),
         "and THE DAY HE FIRST TRIES IT — no journal at all — the same "
         "script prints three calm lines, exits 0, and does not create one",
         t_first.strip()[-70:])
    shutil.rmtree(TREE, ignore_errors=True)

    print("\n(m) >>> M-13 — THE SABOTAGE DRILL, FROM BIRTH AND PERMANENT."
          "\n    Every break is PROVED TO CHANGE WHAT HE READS (or what is on"
          "\n    the disk) before its verdict is counted. **A BREAK REPORTED"
          "\n    `INERT` IS A FAIL.**")
    HONEST_NAMES = ('_move', '_result_usd', '_pick', '_got_in',
                    '_capped_size', '_pure_size', '_read_trades',
                    '_own_on_stopped', '_sum', '_round', '_snapshot_time',
                    '_closing_lines', '_readings_for', '_stop_gap',
                    '_beside', '_read_snapshots', '_parse_trade')
    _honest = {name: globals()[name] for name in HONEST_NAMES}

    D_JOURNAL, D_BOOKS = plan_fixture()

    def w_report():
        """Witnessed as THE WORDS HE READS."""
        return mirror_text(trades_path=D_JOURNAL, snapshot_paths=D_BOOKS)

    def w_disk():
        """Witnessed as THE BYTES OF HIS JOURNAL after a run."""
        w_report()
        return fingerprint(D_JOURNAL)

    HONEST_DISK = fingerprint(D_JOURNAL)

    def j_report():
        return w_report() == EXPECTED

    def j_words():
        return clean(w_report())

    def j_disk():
        return w_disk() == HONEST_DISK

    def b_move(direction, entry, exit_price):
        return (exit_price - entry) / entry          # a short read as a long

    def b_coins(trade):
        gain = trade['exit'] - trade['entry']
        return trade['size'] * (gain if trade['direction'] == 'long'
                                else -gain)

    def b_pick_nearest(readings, got_in):
        best = None
        for reading in readings:
            if best is None or (abs(reading['when'] - got_in)
                                < abs(best['when'] - got_in)):
                best = reading
        return best

    def b_pick_any_age(readings, got_in):
        best = None
        for reading in readings:
            if reading['when'] > got_in:
                continue
            if best is None or reading['when'] > best['when']:
                best = reading
        return best

    def b_got_in(logged, hours):
        return logged

    def b_no_cap(pure, account):
        return pure

    def b_two_percent(account, gap):
        return Decimal('0.02') * account / gap

    def b_drop_silently(path):
        state, trades, _unreadable, found = _honest['_read_trades'](path)
        return state, trades, [], found

    def b_own_all(worked):
        return _honest['_sum'](figures['result'] for figures in worked)

    def b_sum_short(values):
        return _honest['_sum'](list(values)[:-1])

    def b_round_down(value, places):
        from decimal import ROUND_DOWN
        return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_DOWN)

    def b_local_time(text):
        return _honest['_snapshot_time'](text) - timedelta(hours=5)

    def b_advice():
        return _honest['_closing_lines']() + [
            '>> you should size smaller next time']

    def b_any_coin(readings, asset):
        return list(readings)

    def b_gap_to_exit(trade):
        return abs(trade['entry'] - trade['exit']) / trade['entry']

    def b_tidy_journal(path):
        result = _honest['_read_trades'](path)
        with open(path, encoding='utf-8', newline='') as handle:
            rows_ = list(csv.reader(handle))
        with open(path, 'w', encoding='utf-8', newline='') as handle:
            csv.writer(handle).writerows(rows_[:-1])   # the bad row "fixed"
        return result

    def b_beside_inverted(direction, reading):
        answer_ = _honest['_beside'](direction, reading)
        return {'with': 'against', 'against': 'with'}.get(answer_, answer_)

    def b_one_notebook(paths):
        return _honest['_read_snapshots'](list(paths)[:1])

    def b_size_as_account(row):
        swapped = list(row)
        if len(swapped) == 11:
            swapped[6], swapped[7] = swapped[7], swapped[6]
        return _honest['_parse_trade'](swapped)

    BREAKS = [
        ('M1 ', "a SHORT's result worked as if it were a long",
         '_move', b_move, w_report, j_report),
        ('M2 ', 'his size read as COINS instead of dollars',
         '_result_usd', b_coins, w_report, j_report),
        ('M3 ', 'a reading taken AFTER he got in used, because it is nearer',
         '_pick', b_pick_nearest, w_report, j_report),
        ('M4 ', 'the 8-hour limit ignored',
         '_pick', b_pick_any_age, w_report, j_report),
        ('M5 ', 'the hours ignored — the time he LOGGED it used instead',
         '_got_in', b_got_in, w_report, j_report),
        ('M6 ', 'the 25% cap ignored',
         '_capped_size', b_no_cap, w_report, j_report),
        ('M7 ', 'the 1% line quietly worked at 2%',
         '_pure_size', b_two_percent, w_report, j_report),
        ('M8 ', 'an unreadable row dropped WITHOUT A WORD (B13)',
         '_read_trades', b_drop_silently, w_report, j_report),
        ('M9 ', 'the no-stop trade slipped into `your result on those`',
         '_own_on_stopped', b_own_all, w_report, j_report),
        ('M10', 'every total leaving out the last trade',
         '_sum', b_sum_short, w_report, j_report),
        ('M11', 'rounding that TRUNCATES instead of rounding half up',
         '_round', b_round_down, w_report, j_report),
        ('M12', 'snapshot times read as LOCAL time (five hours out)',
         '_snapshot_time', b_local_time, w_report, j_report),
        ('M13', 'A LINE OF ADVICE printed on the report (F8)',
         '_closing_lines', b_advice, w_report, j_words),
        ('M14', "ANOTHER COIN's reading borrowed",
         '_readings_for', b_any_coin, w_report, j_report),
        ('M15', 'his risk measured to the EXIT instead of the stop',
         '_stop_gap', b_gap_to_exit, w_report, j_report),
        ('M16', 'HIS JOURNAL REWRITTEN — the bad row "tidied" away',
         '_read_trades', b_tidy_journal, w_disk, j_disk),
        ('M17', 'WITH and AGAINST the trend exchanged',
         '_beside', b_beside_inverted, w_report, j_report),
        ('M18', 'only the first notebook read — the cloud and frozen lost',
         '_read_snapshots', b_one_notebook, w_report, j_report),
        ('M19', 'his SIZE and his ACCOUNT exchanged on the way in',
         '_parse_trade', b_size_as_account, w_report, j_report),
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
            # M16 really does rewrite the fixture. Build a fresh one, and
            # prove below that the honest bytes ARE back.
            if fingerprint(D_JOURNAL) != HONEST_DISK:
                D_JOURNAL, D_BOOKS = plan_fixture()
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
         "after nineteen breaks and nineteen repairs, every function this "
         "drill touched is the one it started with")
    mark(w_report() == EXPECTED and fingerprint(D_JOURNAL) == HONEST_DISK,
         "and the honest report is the hand-typed one again, over a journal "
         "whose bytes are what they were before M16 rewrote it")

    print("\n(n) M-14 — A TALLY COUNTS ONLY WHAT A MACHINE ACTUALLY CHECKED.")
    mark(len(BREAKS) == 19 and len(BAD_ROWS) == 8 and len(FORBIDDEN) == 36
         and len(HONEST_NAMES) == 17,
         f"the drill still holds all {len(BREAKS)} breaks, the unreadable "
         f"table all {len(BAD_ROWS)} shapes and the forbidden list all "
         f"{len(FORBIDDEN)} words, counted against numbers typed out here")

    shutil.rmtree(WORK, ignore_errors=True)
    mark(fingerprint(TRADES_FILE) == REAL_JOURNAL_AT_START,
         "and the REAL journal is byte-for-byte what it was before this "
         "gate started — never created if it did not exist, never touched "
         "if it did",
         f"{TRADES_FILE}: {REAL_JOURNAL_AT_START[:16]}")

    EXPECTED_CHECKS = 84
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes — "
         f"the number is TYPED OUT in this file",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 5.2 PASSED — {len(nonlocal_ok)} checks, 0 red.

THE PLAN'S OWN SENTENCE IS MET IN FULL: three fake trades went in
through the real logger, the Mirror was run, and the whole report
equals one typed out by hand in this gate, character for character -
every result, every risk figure, both 1% lines, the cap, the times,
the readings and every total, each worked by hand from the arithmetic
declared before this file existed.

IT WROTE NOTHING. Four files before, the same four after, every
sha256 unmoved; and run the way MIRROR.bat runs it, as a script with
no arguments in a tree of its own, it found the journal and all three
notebooks by itself and printed the same report byte for byte.

THE TIME RULE WAS TESTED AT EVERY TURNOVER: the same minute is used,
one minute after is not; eight hours exactly is used, eight hours and
one minute is not; the newest wins; another coin is never borrowed.

EVERY TOTAL WAS RE-ADDED BY THIS GATE FROM THE PRINTED LINES, on six
awkward trades over three account sizes, and each breakdown covers
every trade exactly once.

NINETEEN SABOTAGES WERE PROVED TO CHANGE WHAT HE READS BEFORE THEIR
VERDICTS WERE COUNTED - including a line of advice, which is judged
by the forbidden-word list and not by the hand-typed report.

WHAT THIS GATE DOES **NOT** PROVE. It cannot tell whether the stop,
the account or the hours he typed are TRUE. It leaves out fees and
funding and says so on the report. And "what the instruments had
recorded" is a reading, not a prediction: in week 1 those readings
scored 40.0% against a parrot's 49.5%. The Mirror puts them beside
his trade because the plan asks for it. It is not a verdict on him.""")
    else:
        print(f"GATE 5.2 FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
