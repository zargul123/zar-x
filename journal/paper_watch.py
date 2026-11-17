"""
Zar X journal compartment — THE PAPER-WATCH (Phase 7: the signal journal).

**PAPER ONLY. NO MONEY. THIS FILE SENDS NO ORDER ANYWHERE AND HOLDS NO KEY.**
It reads public prices and writes text files.

Ordered by the Commander on 2026-11-17 after all three gauntlet slots had
failed: thirteen coins, every signal recorded, both exits side by side from
the same entry, a weekly autopsy. The bar was written into PROGRESS_LOG.md
that night and committed with no code before this file existed.

WHAT A RUN DOES, in order:

  1. Fetches daily candles (Binance spot), funding (Binance futures) and the
     mood (alternative.me) for thirteen coins.
  2. ADDS what is new to its own store in `journal/paper/`. A figure already
     stored is never changed: if the source later serves a different one the
     stored one stands and the difference is counted.
  3. Works the WHOLE record out again from the store, from the start day:
     the two frozen rules of `signals/confluence.py`, called, asked at the
     close of each day on each coin - but only when that rule's fixed-exit
     trade on that coin is closed, exactly as the Lab's engine asks.
  4. Every signal opens ONE trade with TWO endings: the fixed stop and
     target (1.5 and 3.0 times the 14-day range - Forward Check 1's own),
     and a trailing stop from the same entry and the same first stop.
  5. **EVERY ROW ALREADY IN THE LEDGER MUST COME OUT OF THAT WORKING
     IDENTICAL.** If one does not, the run writes nothing and says
     INTEGRITY ALARM. Rows the ledger does not yet hold are appended.
  6. Returns the report.

**LATE IS SAID, NOT HIDDEN.** The laptop is off most days. The rules are
arithmetic on public figures, so a day worked late gives the same signal,
entry, stop and target as on the night - and its row carries the word LATE
and the hours. What a late row cannot show is whether the pilot could have
acted on it; the report counts on-time and late rows apart.

**THE TRAILING EXIT IS A SECOND RECORD AND NEVER REPLACES THE FIRST.** The
ship's own risk calculator says of Zargul 2.0: "trailing stop (our own 2026
data showed it cut winners and kept losers)".

THE ARITHMETIC (declared in the bar):

    signal    at the close of day D, on candles up to and including D
    entry     day D+1's opening price, made worse by the slippage
    range     the ship's 14-day average true range on days up to D
    stop      entry -/+ 1.5 x range;  target  entry +/- 3.0 x range
    size      1% of a pretend 1,000 dollars at risk, position at most 25%
    exits     on each COMPLETED day from the entry day on; stop and target
              inside one day counts the LOSS; a gap through a stop fills
              at the open
    trailing  before day i the stop is the better of the first stop and
              (best CLOSE since entry on days before i, less 3.0 x range)
              for a long; mirror for a short. It never moves back.
    result    as a fraction of the 1,000, after fee and slippage both sides

WHAT IT DOES NOT COUNT: the funding paid or received while a futures
position is held. The candles are spot prices.

LAW 3 — the doorways `run()`, `report()` and `week()` never raise and never
print; they RETURN text. Every failure becomes one named line.

Standalone use:
    python journal/paper_watch.py            (a run: fetch, record, report)
    python journal/paper_watch.py --report   (the report; no network)
    python journal/paper_watch.py --week     (the week's numbers; no network)
    python journal/paper_watch.py --gate     (gate 7.1; opens nothing real)
"""
import csv
import hashlib
import io
import math
import os
import sys
from datetime import datetime, timedelta, timezone
from fractions import Fraction

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(JOURNAL_DIR)
LAB_DIR = os.path.join(ROOT_DIR, 'lab')
PAPER_DIR = os.path.join(JOURNAL_DIR, 'paper')              # the laptop's
CLOUD_DIR = os.path.join(JOURNAL_DIR, 'paper_cloud')        # the cloud's

# TWO RECORDS, TWO WRITERS, NEVER ONE FILE WITH TWO. Each has its own
# folder and its own door to Binance's funding: the documented address
# refuses GitHub's machines (HTTP 451, measured 2026-11-17), the website's
# host serves them the same rows (12,870 of 12,870 identical, the same day).
RECORDS = {'laptop': PAPER_DIR, 'cloud': CLOUD_DIR}
FUNDING_DOORS = {
    'laptop': 'https://fapi.binance.com/fapi/v1/fundingRate',
    'cloud': 'https://www.binance.com/fapi/v1/fundingRate',
}

COINS = ('BTC', 'ETH', 'SOL', 'XRP', 'BNB', 'DOGE', 'NEAR', 'UNI', 'LINK',
         'AVAX', 'ADA', 'AAVE', 'BCH')
ORIGINAL = ('BTC', 'ETH', 'SOL')
RULES = ('confluence-1d-t100', 'trend-only-1d-t100')
RULE_WORDS = {'confluence-1d-t100': 'combined rule',
              'trend-only-1d-t100': 'trend alone'}
EXITS = ('fixed', 'trail')
EXIT_WORDS = {'fixed': 'fixed exit', 'trail': 'trailing exit'}

START_DAY = '2026-11-16'     # the first day asked
SEED_DAYS = 400              # history fetched once, behind the start
SL_ATR = 1.5                 # the first stop, in 14-day ranges
TP_ATR = 3.0                 # the fixed target
TRAIL_ATR = 3.0              # how far the trailing stop sits behind the best close
ATR_PERIOD = 14
FEE = 0.0005                 # 0.05% a side: his Binance futures taker fee
SLIP = 0.0005                # 0.05% a side
ACCOUNT = 1000.0             # the pretend account, in dollars
RISK = Fraction(1, 100)      # at risk on every signal
CAP = Fraction(4, 100)       # the portfolio line's limit on total open risk
ON_TIME_HOURS = 6            # written this soon after the entry day opens
DAY_MS = 86_400_000
MAX_CARRIED_RUN = 3          # days in a row the mood may be carried
TOLERANCE = 1e-9             # two figures this close are the same figure

SPOT_URL = 'https://data-api.binance.vision/api/v3/klines'
TIMEOUT = 30

FILES = {
    'candles': ('candles.csv', ('asset', 'day', 'open', 'high', 'low',
                                'close', 'seen_utc')),
    'opens': ('opens.csv', ('asset', 'day', 'open', 'seen_utc')),
    'funding': ('funding.csv', ('asset', 'time_ms', 'rate')),
    'mood': ('mood.csv', ('day', 'value', 'label', 'carried', 'seen_utc')),
}
LEDGER_NAME = 'ledger.csv'
LEDGER = ('kind', 'id', 'rule', 'asset', 'direction', 'signal_day',
          'entry_day', 'entry_raw', 'entry_fill', 'range', 'stop', 'target',
          'coins', 'position_usd', 'risk_usd', 'exit_kind', 'exit_day',
          'exit_raw', 'exit_fill', 'reason', 'days_held', 'result_usd',
          'result_frac', 'settings', 'written_utc', 'late_hours', 'chain')
STAMPED = ('written_utc', 'late_hours', 'chain')   # not part of the working-out
NUMBERS = ('entry_raw', 'entry_fill', 'range', 'stop', 'target', 'coins',
           'position_usd', 'risk_usd', 'exit_raw', 'exit_fill', 'result_usd',
           'result_frac')
STAMP = '%Y-%m-%d %H:%M:%S'
NO_MONEY = 'PAPER ONLY. NO MONEY. NO ORDER IS EVER SENT.'


def asset_of(coin):
    return f'{coin}-USD'


def symbol_of(coin):
    return f'{coin}USDT'


def day_ms(text):
    """'2026-11-16' -> the millisecond its UTC day begins. No local clock."""
    stamp = datetime.strptime(text, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    return int(stamp.timestamp()) * 1000


def day_text(ms):
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).strftime(
        '%Y-%m-%d')


def next_day(text, steps=1):
    return day_text(day_ms(text) + steps * DAY_MS)


def settings():
    """A short stamp of everything that can move a figure. A changed rule
    or a changed number is a different record, and the ledger says so."""
    parts = (RULES, START_DAY, SL_ATR, TP_ATR, TRAIL_ATR, ATR_PERIOD, FEE,
             SLIP, ACCOUNT, str(RISK))
    return hashlib.sha256(repr(parts).encode('utf-8')).hexdigest()[:10]


def _number(text):
    """A stored figure -> a float, or None for an empty cell."""
    return None if text in ('', None) else float(text)


def _positive(text):
    try:
        value = float(text)
    except (TypeError, ValueError):
        return False
    return math.isfinite(value) and value > 0


# --------------------------------------------------------------------------
# THE STORE — append-only. What is written is never changed.
# --------------------------------------------------------------------------

class Store:
    """The paper-watch's own copy of what the sources served, first seen."""

    def __init__(self, directory=None):
        self.directory = PAPER_DIR if directory is None else directory
        self.revisions = 0          # figures the source later changed
        self.candles = {}           # asset -> [(day, o, h, l, c)] as text
        self.opens = {}             # (asset, day) -> open as text
        self.funding = {}           # asset -> [(time_ms, rate text)]
        self.mood = []              # [(day, value, label, carried)]
        self._load()

    def _path(self, what):
        return os.path.join(self.directory, FILES[what][0])

    def _rows(self, what):
        path, header = self._path(what), FILES[what][1]
        if not os.path.exists(path):
            return []
        with open(path, encoding='utf-8', newline='') as handle:
            rows = list(csv.reader(handle))
        if not rows or tuple(rows[0]) != header:
            raise ValueError(f'{FILES[what][0]} does not begin with the '
                             f'header this file writes')
        for row in rows[1:]:
            if len(row) != len(header):
                raise ValueError(f'{FILES[what][0]} holds a row of '
                                 f'{len(row)} cells where {len(header)} '
                                 f'are owed')
        return rows[1:]

    def _load(self):
        for asset, day, o, h, l, c, _seen in self._rows('candles'):
            self.candles.setdefault(asset, []).append((day, o, h, l, c))
        for asset, rows in self.candles.items():
            for (a, *_x), (b, *_y) in zip(rows, rows[1:]):
                if next_day(a) != b:
                    raise ValueError(f'candles.csv: {asset} goes from {a} '
                                     f'to {b} - a day missing or twice')
        for asset, day, value, _seen in self._rows('opens'):
            if (asset, day) in self.opens:
                raise ValueError(f'opens.csv: {asset} {day} is there twice')
            self.opens[(asset, day)] = value
        for asset, stamp, rate in self._rows('funding'):
            rows = self.funding.setdefault(asset, [])
            if rows and int(stamp) <= rows[-1][0]:
                raise ValueError(f'funding.csv: {asset} is not in order')
            rows.append((int(stamp), rate))
        for day, value, label, carried, _seen in self._rows('mood'):
            if self.mood and next_day(self.mood[-1][0]) != day:
                raise ValueError('mood.csv: a day missing or twice')
            self.mood.append((day, int(value), label, int(carried)))

    def _append(self, what, rows):
        if not rows:
            return
        os.makedirs(self.directory, exist_ok=True)
        path, header = self._path(what), FILES[what][1]
        fresh = not os.path.exists(path)
        with open(path, 'a', encoding='utf-8', newline='') as handle:
            writer = csv.writer(handle, lineterminator='\n')
            if fresh:
                writer.writerow(header)
            writer.writerows(rows)

    def last_day(self, asset):
        rows = self.candles.get(asset)
        return rows[-1][0] if rows else None

    def add_candles(self, asset, rows, seen):
        """Completed days, oldest first, as (day, o, h, l, c) text. Days
        already stored are compared and never changed. The new ones must
        carry straight on from the last stored day. -> how many were added.
        Raises ValueError, having written nothing, on any bad row."""
        have = dict((row[0], row[1:]) for row in self.candles.get(asset, []))
        new, last = [], self.last_day(asset)
        for row in rows:
            day, o, h, l, c = (str(cell) for cell in row)
            if day_text(day_ms(day)) != day:
                raise ValueError(f'{asset}: a day that is not a day: {day!r}')
            if not all(_positive(cell) for cell in (o, h, l, c)):
                raise ValueError(f'{asset} {day}: a price that is not a '
                                 f'positive number')
            if float(h) < max(float(o), float(c), float(l)) or float(l) > \
                    min(float(o), float(c)):
                raise ValueError(f'{asset} {day}: a high below or a low '
                                 f'above the candle it belongs to')
            if day in have:
                if any(abs(float(a) - float(b)) > TOLERANCE * abs(float(b))
                       for a, b in zip((o, h, l, c), have[day])):
                    self.revisions += 1
                continue
            if last is not None and day <= last and not new:
                raise ValueError(f'{asset}: {day} is before the store '
                                 f'begins')
            expected = next_day(new[-1][0] if new else last) if (new or last) \
                else day
            if day != expected:
                raise ValueError(f'{asset}: {day} served where {expected} '
                                 f'is owed - a day missing or twice')
            new.append((day, o, h, l, c))
            first_seen = self.opens.get((asset, day))
            if first_seen is not None and abs(
                    float(o) - float(first_seen)) > TOLERANCE * abs(float(o)):
                self.revisions += 1     # the entry written from it stands
        self._append('candles', [(asset,) + row + (seen,) for row in new])
        self.candles.setdefault(asset, []).extend(new)
        return len(new)

    def add_open(self, asset, day, value, seen):
        """The opening price of the day in progress, first seen."""
        value = str(value)
        if not _positive(value):
            raise ValueError(f'{asset} {day}: an opening price that is not '
                             f'a positive number')
        if (asset, day) in self.opens:
            if abs(float(value) - float(self.opens[(asset, day)])) > \
                    TOLERANCE * abs(float(value)):
                self.revisions += 1
            return 0
        if self.last_day(asset) is not None and day <= self.last_day(asset):
            return 0
        self._append('opens', [(asset, day, value, seen)])
        self.opens[(asset, day)] = value
        return 1

    def add_funding(self, asset, rows, check):
        """Settlements as (time_ms, rate text), oldest first. `check` is the
        Lab's own rate reader: it raises on a rate it would refuse."""
        have = dict(self.funding.get(asset, []))
        last = self.funding[asset][-1][0] if self.funding.get(asset) else None
        new = []
        for stamp, rate in rows:
            stamp, rate = int(stamp), str(rate)
            check(rate)
            if stamp in have:
                if check(rate) != check(have[stamp]):
                    self.revisions += 1
                continue
            if last is not None and stamp < last:
                continue            # older than the store reaches: not ours
            if new and stamp <= new[-1][0]:
                raise ValueError(f'{asset}: funding served out of order')
            new.append((stamp, rate))
        self._append('funding', [(asset, stamp, rate) for stamp, rate in new])
        self.funding.setdefault(asset, []).extend(new)
        return len(new)

    def add_mood(self, published, upto_day, first_day, labels, seen):
        """published: {day_ms: (value, label)}. Adds one row a day up to and
        including `upto_day`. A day with nothing published carries the day
        before, for at most three days in a row; then the store waits."""
        added = 0
        while True:
            day = next_day(self.mood[-1][0]) if self.mood else first_day
            if day > upto_day:
                return added
            got = published.get(day_ms(day))
            if got is not None:
                value, label = int(got[0]), str(got[1])
                if label not in labels or not 0 <= value <= 100:
                    return added
                row = (day, value, label, 0)
            else:
                run = 0
                for _d, _v, _l, carried in reversed(self.mood):
                    if not carried:
                        break
                    run += 1
                if not self.mood or run >= MAX_CARRIED_RUN:
                    return added
                row = (day, self.mood[-1][1], self.mood[-1][2], 1)
            self._append('mood', [row + (seen,)])
            self.mood.append(row)
            added += 1


# --------------------------------------------------------------------------
# THE FRAMES — the store, joined exactly as the Lab joins it
# --------------------------------------------------------------------------

def _lab():
    """The Lab's two join modules and the frozen rules. Imported late so
    `--report` on a broken install still says what is wrong by name."""
    if LAB_DIR not in sys.path:
        sys.path.insert(0, LAB_DIR)
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
    import funding_vault
    import mood_vault
    from risk.calculator import RiskCalculator
    from signals.confluence import Confluence, TrendOnly
    return funding_vault, mood_vault, RiskCalculator, (Confluence(),
                                                       TrendOnly())


def frame_of(store, asset):
    """One coin's stored candles with `funding`, `mood` and `mood_side`
    joined on by the Lab's own two functions. None if it has no candles."""
    import pandas as pd
    funding_vault, mood_vault = _lab()[:2]
    rows = store.candles.get(asset)
    if not rows:
        return None
    df = pd.DataFrame(
        [[float(cell) for cell in row[1:]] for row in rows],
        index=pd.to_datetime([row[0] for row in rows]),
        columns=['open', 'high', 'low', 'close'])
    settlements = store.funding.get(asset, [])
    df = funding_vault.attach(
        df, [stamp for stamp, _r in settlements],
        [funding_vault.rate_units(rate) for _s, rate in settlements])
    df = mood_vault.attach(
        df, [day_ms(day) for day, _v, _l, _c in store.mood],
        [value for _d, value, _l, _c in store.mood],
        [mood_vault.LABELS[label] for _d, _v, label, _c in store.mood])
    return df


# --------------------------------------------------------------------------
# THE WORKING-OUT — the whole record, from the store, every time
# --------------------------------------------------------------------------

def _result(direction, coins, entry_raw, entry_fill, exit_raw):
    """-> (exit_fill, dollars, fraction of the account), after costs."""
    if direction == 'long':
        exit_fill = exit_raw * (1 - SLIP)
        after_slip = coins * (exit_fill - entry_fill)
    else:
        exit_fill = exit_raw * (1 + SLIP)
        after_slip = coins * (entry_fill - exit_fill)
    fees = FEE * (coins * entry_fill + coins * exit_fill)
    net = after_slip - fees
    return exit_fill, net, net / ACCOUNT


def _row(**cells):
    row = dict.fromkeys(LEDGER, '')
    row.update(cells)
    return row


def replay(frames, next_opens=None, start_day=None, rules=None, calc=None,
           entry_opens=None):
    """THE WHOLE RECORD, worked from the frames alone.

    frames      {asset: DataFrame of COMPLETED daily candles with funding,
                 mood and mood_side}
    next_opens  {asset: (day, opening price)} - the day in progress
    entry_opens {(asset, day): opening price first seen} - used as the
                 entry price for that day if present
    -> (events, open_trades). Events are ledger rows without their stamps,
       in the one order this file ever writes them.
    """
    start_day = START_DAY if start_day is None else start_day
    next_opens = next_opens or {}
    entry_opens = entry_opens or {}
    if rules is None or calc is None:
        _f, _m, calculator, frozen = _lab()
        rules = frozen if rules is None else rules
        calc = calculator() if calc is None else calc
    stamp = settings()
    events, still_open = [], []

    def open_trade(rule, asset, direction, signal_day, entry_day, raw, past):
        atr = calc.atr(past, ATR_PERIOD)
        if not atr or not atr > 0:
            return None
        fill = raw * (1 + SLIP) if direction == 'long' else raw * (1 - SLIP)
        plan = calc.plan_trade(capital=ACCOUNT, entry_price=fill,
                               direction=direction, atr=atr,
                               risk_pct=float(RISK), sl_atr_mult=SL_ATR,
                               tp_atr_mult=TP_ATR)
        if not plan:
            return None
        trade = {'rule': rule.name, 'asset': asset, 'direction': direction,
                 'signal_day': signal_day, 'entry_day': entry_day,
                 'entry_raw': raw, 'entry_fill': fill, 'atr': float(atr),
                 'stop': plan['stop_loss'], 'target': plan['take_profit'],
                 'coins': plan['size_units'],
                 'id': f'{rule.name}|{asset}|{entry_day}',
                 'trail_stop': plan['stop_loss'], 'best': None,
                 'fixed_open': True, 'trail_open': True}
        events.append(_row(
            kind='OPEN', id=trade['id'], rule=rule.name, asset=asset,
            direction=direction, signal_day=signal_day, entry_day=entry_day,
            entry_raw=raw, entry_fill=fill, range=float(atr),
            stop=trade['stop'], target=trade['target'],
            coins=trade['coins'], position_usd=plan['position_value'],
            risk_usd=plan['risk_money'], settings=stamp))
        return trade

    def close(trade, exit_kind, day, exit_raw, reason, held):
        exit_fill, dollars, fraction = _result(
            trade['direction'], trade['coins'], trade['entry_raw'],
            trade['entry_fill'], exit_raw)
        events.append(_row(
            kind='CLOSE', id=f"{trade['id']}|{exit_kind}",
            rule=trade['rule'], asset=trade['asset'],
            direction=trade['direction'], signal_day=trade['signal_day'],
            entry_day=trade['entry_day'], exit_kind=exit_kind, exit_day=day,
            exit_raw=exit_raw, exit_fill=exit_fill, reason=reason,
            days_held=held, result_usd=dollars, result_frac=fraction,
            settings=stamp))

    for rule in rules:
        for asset, df in frames.items():
            if df is None or not len(df):
                continue
            days = [stamp_.strftime('%Y-%m-%d') for stamp_ in df.index]
            o, h = df['open'].values, df['high'].values
            l, c = df['low'].values, df['close'].values
            first = next((i for i, day in enumerate(days)
                          if day >= start_day), None)
            if first is None:
                continue
            position, pending, trails = None, None, []
            for i in range(first, len(days)):
                # 1. ENTRY: yesterday's signal, at today's opening price
                if position is None and pending is not None:
                    raw = float(entry_opens.get((asset, days[i]), o[i]))
                    trade = open_trade(rule, asset, pending, days[i - 1],
                                       days[i], raw, df.iloc[:i])
                    if trade:
                        trade['entry_i'] = i
                        position = trade
                        trails.append(trade)
                    pending = None
                # 2. THE FIXED EXIT, on today's high and low
                if position is not None:
                    long = position['direction'] == 'long'
                    stop, target = position['stop'], position['target']
                    hit_stop = l[i] <= stop if long else h[i] >= stop
                    hit_target = h[i] >= target if long else l[i] <= target
                    if hit_stop:
                        raw = (min(float(o[i]), stop) if long
                               else max(float(o[i]), stop))
                        close(position, 'fixed', days[i], raw,
                              'stop+target same day (loss counted)'
                              if hit_target else 'stop',
                              i - position['entry_i'] + 1)
                        position['fixed_open'] = False
                        position = None
                    elif hit_target:
                        close(position, 'fixed', days[i], target, 'target',
                              i - position['entry_i'] + 1)
                        position['fixed_open'] = False
                        position = None
                # 2b. THE TRAILING EXIT of every trade still trailing
                for trade in trails:
                    if not trade['trail_open']:
                        continue
                    long = trade['direction'] == 'long'
                    stop = trade['trail_stop']
                    if (l[i] <= stop) if long else (h[i] >= stop):
                        left_at = (min(float(o[i]), stop) if long
                                   else max(float(o[i]), stop))
                        close(trade, 'trail', days[i], left_at,
                              'first stop' if stop == trade['stop']
                              else 'trailing stop',
                              i - trade['entry_i'] + 1)
                        trade['trail_open'] = False
                        continue
                    reach = TRAIL_ATR * trade['atr']
                    if long:
                        best = (float(c[i]) if trade['best'] is None
                                else max(trade['best'], float(c[i])))
                        trade['trail_stop'] = max(stop, best - reach)
                    else:
                        best = (float(c[i]) if trade['best'] is None
                                else min(trade['best'], float(c[i])))
                        trade['trail_stop'] = min(stop, best + reach)
                    trade['best'] = best
                # 3. THE SIGNAL, asked at today's close, only when flat
                if position is None:
                    answer = rule(df.iloc[:i + 1].copy())
                    if answer not in ('long', 'short', 'flat'):
                        raise ValueError(f'{rule.name} answered {answer!r}')
                    if answer != 'flat':
                        pending = answer
            # the day in progress: an entry can be written, nothing closed
            if position is None and pending is not None:
                ahead = next_opens.get(asset)
                if ahead and ahead[0] == next_day(days[-1]):
                    trade = open_trade(rule, asset, pending, days[-1],
                                       ahead[0], float(ahead[1]), df)
                    if trade:
                        trails.append(trade)
            still_open.extend(t for t in trails
                              if t['fixed_open'] or t['trail_open'])

    order = {name: at for at, name in enumerate(RULES)}
    assets = {asset_of(coin): at for at, coin in enumerate(COINS)}

    def key(row):
        day = row['entry_day'] if row['kind'] == 'OPEN' else row['exit_day']
        return (day, 0 if row['kind'] == 'OPEN' else 1,
                order.get(row['rule'], len(order)),
                assets.get(row['asset'], len(assets)), row['asset'],
                row['entry_day'], row['exit_kind'])

    events.sort(key=key)
    return events, still_open


# --------------------------------------------------------------------------
# THE LEDGER — append-only, and never trusted on its own
# --------------------------------------------------------------------------

def read_ledger(directory=None):
    path = os.path.join(PAPER_DIR if directory is None else directory,
                        LEDGER_NAME)
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8', newline='') as handle:
        rows = list(csv.reader(handle))
    if not rows or tuple(rows[0]) != LEDGER:
        raise ValueError('ledger.csv does not begin with the header this '
                         'file writes')
    out = []
    for position, row in enumerate(rows[1:], start=2):
        if len(row) != len(LEDGER):
            raise ValueError(f'ledger.csv line {position} holds {len(row)} '
                             f'cells where {len(LEDGER)} are owed')
        out.append(dict(zip(LEDGER, row)))
    return out


def _text(value):
    return repr(float(value)) if isinstance(value, float) else str(value)


def same_cell(name, written, worked):
    """Is a cell in the ledger the cell the working-out gives?"""
    if name in NUMBERS:
        a, b = _number(written), _number(_text(worked) if worked != ''
                                         else '')
        if a is None or b is None:
            return a is None and b is None
        return abs(a - b) <= TOLERANCE * max(abs(a), abs(b), 1e-300)
    return str(written) == _text(worked)


def chain_of(previous, row):
    """Each written row is tied to the one before it: a row edited, removed
    from the middle or slipped in breaks the chain from there on."""
    text = previous + '|' + '|'.join(str(row[name]) for name in LEDGER
                                     if name != 'chain')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def chain_alarms(written):
    alarms, previous = [], ''
    for position, row in enumerate(written, start=2):
        if row['chain'] != chain_of(previous, row):
            alarms.append(f"ledger.csv line {position} ({row['id']}): the "
                          f"chain is broken here - a row edited, removed or "
                          f"slipped in at or before this line")
            break
        previous = row['chain']
    return alarms


def reconcile(written, worked):
    """-> (alarms, new). Every written row must be worked out identical."""
    alarms, by_id = chain_alarms(written), {}
    for row in worked:
        by_id[row['id']] = row
    seen = set()
    for row in written:
        if row['id'] in seen:
            alarms.append(f"{row['id']}: written twice")
            continue
        seen.add(row['id'])
        twin = by_id.get(row['id'])
        if twin is None:
            alarms.append(f"{row['id']}: in the ledger, and the working-out "
                          f"does not give it")
            continue
        wrong = [name for name in LEDGER if name not in STAMPED
                 and not same_cell(name, row[name], twin[name])]
        if wrong:
            alarms.append(f"{row['id']}: {', '.join(wrong)} in the ledger "
                          f"is not what the working-out gives")
    return alarms, [row for row in worked if row['id'] not in seen]


def append_ledger(rows, now, directory=None):
    directory = PAPER_DIR if directory is None else directory
    if not rows:
        return
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, LEDGER_NAME)
    fresh = not os.path.exists(path)
    already = read_ledger(directory)
    previous = already[-1]['chain'] if already else ''
    with open(path, 'a', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, lineterminator='\n')
        if fresh:
            writer.writerow(LEDGER)
        for row in rows:
            cells = dict(row)
            cells['written_utc'] = now.strftime(STAMP)
            if row['kind'] == 'OPEN':
                cells['late_hours'] = _text(late_hours(row['entry_day'], now))
            cells = {name: _text(cells[name]) for name in LEDGER}
            cells['chain'] = previous = chain_of(previous, cells)
            writer.writerow([cells[name] for name in LEDGER])


def newest_day(directory):
    """The last completed day any coin has in a record's store, or ''."""
    store = Store(directory)
    return max((store.last_day(asset_of(coin)) or '' for coin in COINS),
               default='')


def compare(mine, other, mine_name='laptop', other_name='cloud'):
    """THE TWO RECORDS CHECK EACH OTHER. Every row dated on or before the
    last day BOTH stores hold must be the same in both ledgers - signal,
    entry, stop, target, ending, result. When a row was WRITTEN is not
    compared: one record is on time and the other catches up.
    -> lines for the HEALTH section. Never raises."""
    try:
        theirs = read_ledger(other)
        if not theirs and not os.path.isdir(other):
            return [f"  the {other_name}'s record does not exist yet - "
                    f"nothing to compare"]
        ours = read_ledger(mine)
        upto = min(newest_day(mine), newest_day(other))
    except Exception as exc:
        return [f"  the {other_name}'s record could not be read "
                f"({type(exc).__name__}: {str(exc)[:80]}) - not compared"]
    if not upto:
        return [f"  the {other_name}'s record holds no finished day yet - "
                f"nothing to compare"]

    def dated(row):
        return (row['entry_day'] if row['kind'] == 'OPEN'
                else row['exit_day']) <= upto

    # A ROW BOTH HOLD MUST BE THE SAME ROW, whatever its date. A row only
    # ONE holds is a disagreement only if it is dated inside the days both
    # stores cover: beyond them one record is simply ahead of the other.
    a = {row['id']: row for row in ours}
    b = {row['id']: row for row in theirs}
    both = a.keys() & b.keys()
    differ = sorted(key for key in both
                    if any(not same_cell(name, a[key][name], b[key][name])
                           for name in LEDGER if name not in STAMPED))
    only_mine = sorted(key for key in a.keys() - b.keys() if dated(a[key]))
    only_other = sorted(key for key in b.keys() - a.keys() if dated(b[key]))
    if not both and not only_mine and not only_other:
        return [f'  the two records hold no row in common yet (last day '
                f'both hold: {upto}) - nothing to compare']
    if differ or only_mine or only_other:
        lines = [f'  !! THE TWO RECORDS DISAGREE up to {upto}: '
                 f'{len(differ)} row(s) differ, {len(only_mine)} only in '
                 f"the {mine_name}'s, {len(only_other)} only in the "
                 f"{other_name}'s"]
        lines += [f'     differs: {key}' for key in differ[:5]]
        lines += [f"     only in the {mine_name}'s: {key}"
                  for key in only_mine[:5]]
        lines += [f"     only in the {other_name}'s: {key}"
                  for key in only_other[:5]]
        return lines
    return [f"  THE TWO RECORDS AGREE: all {len(both)} rows both hold are "
            f"the same in the {mine_name}'s record and the {other_name}'s, "
            f"and neither lacks a row dated up to {upto}"]


def verdict_code(text):
    """What a run's report means for whoever started it: 1 if it holds an
    alarm, says OFFLINE, or the two records disagree; else 0."""
    return int('INTEGRITY ALARM' in text or 'PAPER-WATCH OFFLINE' in text
               or 'THE TWO RECORDS DISAGREE' in text)


def late_hours(entry_day, now):
    """Hours from the entry day's opening (00:00 UTC) to the writing."""
    opened = datetime.fromtimestamp(day_ms(entry_day) / 1000, tz=timezone.utc)
    return round((now - opened).total_seconds() / 3600.0, 4)


def on_time(hours):
    return float(hours) * 3600.0 <= ON_TIME_HOURS * 3600.0 + 1e-6


# --------------------------------------------------------------------------
# THE FETCH — the only lines that leave this machine
# --------------------------------------------------------------------------

def binance_spot(symbol, start_ms):
    import requests
    reply = requests.get(SPOT_URL, timeout=TIMEOUT,
                         params={'symbol': symbol, 'interval': '1d',
                                 'startTime': int(start_ms), 'limit': 1000})
    reply.raise_for_status()
    return reply.json()


def funding_door(url):
    """One record's door to Binance's funding. The address it asks is
    carried on the function, so a gate can read which door a record has."""
    def ask(params):
        import requests
        reply = requests.get(url, params=params, timeout=TIMEOUT,
                             headers={'User-Agent': 'python'})
        reply.raise_for_status()
        return reply.json()
    ask.url = url
    return ask


def real_sources(record='laptop'):
    if LAB_DIR not in sys.path:
        sys.path.insert(0, LAB_DIR)
    import build_mood_vault
    return {'candles': binance_spot,
            'funding': funding_door(FUNDING_DOORS[record]),
            'mood': build_mood_vault.alternative_me}


def split_klines(klines, now_ms):
    """Binance's rows -> (completed days as (day, o, h, l, c) text, the day
    in progress as (day, open) or None). A candle is COMPLETE only when its
    whole day is behind `now_ms`. Raises ValueError on a row not at 00:00."""
    done, ahead = [], None
    for row in klines:
        opened = int(row[0])
        if opened % DAY_MS:
            raise ValueError('a candle that does not open at 00:00 UTC')
        cells = tuple(str(cell) for cell in row[1:5])
        if opened + DAY_MS <= now_ms:
            done.append((day_text(opened),) + cells)
        elif opened <= now_ms and ahead is None:
            ahead = (day_text(opened), cells[0])
    return done, ahead


def update(store, now, sources):
    """Fetch and add. One coin failing leaves the others working.
    -> (notes, next_opens): notes are named lines for the health section."""
    if LAB_DIR not in sys.path:
        sys.path.insert(0, LAB_DIR)
    import build_funding_vault
    import build_mood_vault
    import funding_vault
    import mood_vault
    now_ms = int(now.timestamp() * 1000)
    seen = now.strftime(STAMP)
    last_complete = day_text(now_ms - now_ms % DAY_MS - DAY_MS)
    seed_ms = day_ms(START_DAY) - SEED_DAYS * DAY_MS
    notes, next_opens = [], {}
    for coin in COINS:
        asset = asset_of(coin)
        try:
            last = store.last_day(asset)
            start = seed_ms if last is None else day_ms(last) - 2 * DAY_MS
            done, ahead = split_klines(
                sources['candles'](symbol_of(coin), start), now_ms)
            store.add_candles(asset, done, seen)
            if ahead and store.last_day(asset) and \
                    ahead[0] == next_day(store.last_day(asset)):
                store.add_open(asset, ahead[0], ahead[1], seen)
        except Exception as exc:          # one coin's source, named
            notes.append(f'{coin}: candles not updated '
                         f'({type(exc).__name__}: {str(exc)[:80]})')
        try:
            rows = store.funding.get(asset)
            start = seed_ms if not rows else rows[-1][0] - 2 * DAY_MS
            fetched = build_funding_vault.fetch_all(
                symbol_of(coin), start, now_ms + 1, sources['funding'])
            store.add_funding(asset, fetched, funding_vault.rate_units)
        except Exception as exc:
            notes.append(f'{coin}: funding not updated '
                         f'({type(exc).__name__}: {str(exc)[:80]})')
        key = (asset, next_day(store.last_day(asset))) \
            if store.last_day(asset) else None
        if key in store.opens:
            next_opens[asset] = (key[1], store.opens[key])
    try:
        published = build_mood_vault.fetch_published(sources['mood'])
        store.add_mood(published, last_complete, day_text(seed_ms),
                       mood_vault.LABELS, seen)
    except Exception as exc:
        notes.append(f'mood not updated ({type(exc).__name__}: '
                     f'{str(exc)[:80]})')
    return notes, next_opens


def stored_next_opens(store):
    out = {}
    for coin in COINS:
        asset = asset_of(coin)
        last = store.last_day(asset)
        if last and (asset, next_day(last)) in store.opens:
            out[asset] = (next_day(last), store.opens[(asset, next_day(last))])
    return out


# --------------------------------------------------------------------------
# THE FIGURES
# --------------------------------------------------------------------------

def closed_trades(rows, rule, exit_kind, coins=COINS):
    """The closed trades of one record, in the order they closed."""
    assets = {asset_of(coin) for coin in coins}
    return [row for row in rows if row['kind'] == 'CLOSE'
            and row['rule'] == rule and row['exit_kind'] == exit_kind
            and row['asset'] in assets]


def score(trades):
    """The figures of one record, from its closed trades."""
    results = [float(row['result_frac']) for row in trades]
    wins = [value for value in results if value > 0]
    losses = [value for value in results if value <= 0]
    equity = peak = 1.0
    dip = 0.0
    for value in results:
        equity *= 1.0 + value
        peak = max(peak, equity)
        dip = max(dip, (peak - equity) / peak)
    return {'trades': len(results),
            'days': len({row['entry_day'] for row in trades}),
            'won': len(wins),
            'pf': (sum(wins) / -sum(losses) if losses and sum(losses) < 0
                   else None),
            'money': ACCOUNT * equity, 'dip': 100.0 * dip,
            'dollars': ACCOUNT * sum(results)}


def portfolio(rows, rule, exit_kind, coins=COINS, cap=CAP):
    """WAY B. One account; the trades entered on one day share whatever of
    the limit is not already at risk, equally, never more than 1% each.
    -> {'money', 'full', 'reduced', 'not_taken', 'open_risk'}"""
    assets = {asset_of(coin) for coin in coins}
    opens = [row for row in rows if row['kind'] == 'OPEN'
             and row['rule'] == rule and row['asset'] in assets]
    closes = {row['id'].rsplit('|', 1)[0]: row for row in rows
              if row['kind'] == 'CLOSE' and row['rule'] == rule
              and row['exit_kind'] == exit_kind and row['asset'] in assets}
    days = sorted({row['entry_day'] for row in opens}
                  | {row['exit_day'] for row in closes.values()})
    share, live = {}, {}
    equity = 1.0
    counts = {'full': 0, 'reduced': 0, 'not_taken': 0}
    for day in days:
        fresh = [row for row in opens if row['entry_day'] == day]
        if fresh:
            room = cap - sum(live.values(), Fraction(0))
            each = min(RISK, room / len(fresh)) if room > 0 else Fraction(0)
            for row in fresh:
                share[row['id']] = each
                if each > 0:
                    live[row['id']] = each
                counts['full' if each == RISK else 'reduced' if each > 0
                       else 'not_taken'] += 1
        for trade_id, row in closes.items():
            if row['exit_day'] == day and trade_id in share:
                equity *= 1.0 + float(row['result_frac']) * float(
                    share[trade_id] / RISK)
                live.pop(trade_id, None)
    counts.update(money=ACCOUNT * equity,
                  open_risk=float(sum(live.values(), Fraction(0))))
    return counts


# --------------------------------------------------------------------------
# THE REPORTS
# --------------------------------------------------------------------------

def _money(value):
    return f'{value:,.2f}'


def _price(value):
    value = float(value)
    return f'{value:,.2f}' if value >= 100 else f'{value:,.4f}'


def _coin(asset):
    return asset.split('-')[0]


def _record_lines(rows):
    lines = [f"  {'record':44s}  trades  days   won     PF   1,000 became"
             f"   worst dip"]
    for rule in RULES:
        for exit_kind in EXITS:
            for label, coins in (('13 coins', COINS),
                                 ('original 3', ORIGINAL)):
                s = score(closed_trades(rows, rule, exit_kind, coins))
                pf = '   -' if s['pf'] is None else f"{s['pf']:.2f}"
                name = f'{RULE_WORDS[rule]} / {EXIT_WORDS[exit_kind]} / {label}'
                lines.append(f"  {name:44s}  {s['trades']:6d}  {s['days']:4d}"
                             f"  {s['won']:4d}  {pf:>5s}  {s['money']:13,.2f}"
                             f"  {s['dip']:9.1f}%")
    return lines


def _portfolio_lines(rows):
    lines = [f'  limit on total open risk: {float(CAP) * 100:.0f}% of the '
             f'account (not final - his to change)',
             f"  {'record':44s}   1,000 became   full  reduced  not taken"]
    for rule in RULES:
        for exit_kind in EXITS:
            for label, coins in (('13 coins', COINS),
                                 ('original 3', ORIGINAL)):
                p = portfolio(rows, rule, exit_kind, coins)
                name = f'{RULE_WORDS[rule]} / {EXIT_WORDS[exit_kind]} / {label}'
                lines.append(f"  {name:44s}  {p['money']:13,.2f}  "
                             f"{p['full']:5d}  {p['reduced']:7d}  "
                             f"{p['not_taken']:9d}")
    return lines


def health_lines(store, rows, frames, notes):
    lines = []
    opens = [row for row in rows if row['kind'] == 'OPEN']
    prompt = sum(1 for row in opens if on_time(row['late_hours']))
    lines.append(f'  signals written ON TIME (within {ON_TIME_HOURS} hours '
                 f'of the entry day opening): {prompt}')
    lines.append(f'  signals written LATE (worked out afterwards): '
                 f'{len(opens) - prompt}')
    newest = max((store.last_day(asset_of(coin)) or '' for coin in COINS),
                 default='')
    for coin in COINS:
        last = store.last_day(asset_of(coin))
        if last != newest:
            lines.append(f'  {coin}: WAITING - its candles reach '
                         f'{last or "nowhere"}, the others {newest}')
    for asset, df in frames.items():
        if df is None:
            continue
        tail = df.iloc[-91:]
        for column, word in (('funding', 'funding'), ('mood', 'mood')):
            empty = int(tail[column].isna().sum())
            if empty:
                lines.append(
                    f'  {_coin(asset)}: {empty} of the last {len(tail)} days '
                    f'have no {word} reading - the crowd rule that reads it '
                    f'answers "flat" until they are 91 days behind')
    carried = sum(1 for row in store.mood[-91:] if row[3])
    if carried:
        lines.append(f'  mood: {carried} of the last 91 days carried from '
                     f'the day before')
    if store.revisions:
        lines.append(f'  {store.revisions} figure(s) served differently '
                     f'from what is stored - the stored ones stand')
    lines.extend(f'  {note}' for note in notes)
    return lines


def record_line(record):
    return (f"  THIS IS THE {record.upper()}'s RECORD "
            f"(journal/{os.path.basename(RECORDS[record])}/)")


def render(store, rows, still_open, frames, notes, new_ids=(), now=None,
           alarms=(), record=None, versus=()):
    """The report, as text."""
    newest = max((store.last_day(asset_of(coin)) or '' for coin in COINS),
                 default='')
    lines = ['=' * 78, 'ZAR X - THE PAPER-WATCH', NO_MONEY, '=' * 78]
    if record:
        lines.append(record_line(record))
    lines.append(f'  followed since {START_DAY}; last completed day in the '
                 f'store: {newest or "none"}')
    if now is not None:
        lines.append(f'  this run: {now.strftime(STAMP)} UTC')
    if alarms:
        lines += ['', '!! INTEGRITY ALARM - THE LEDGER IS NOT WHAT THE '
                  'WORKING-OUT GIVES. NOTHING WAS WRITTEN.']
        lines += [f'   {alarm}' for alarm in alarms[:20]]
        if len(alarms) > 20:
            lines.append(f'   ... and {len(alarms) - 20} more')
    fresh = [row for row in rows if row['id'] in set(new_ids)]
    lines += ['', f'NEW THIS RUN - {sum(1 for r in fresh if r["kind"] == "OPEN")}'
              f' signal(s), {sum(1 for r in fresh if r["kind"] == "CLOSE")} '
              f'ending(s)']
    for row in fresh:
        if row['kind'] == 'OPEN':
            when = ('ON TIME' if on_time(row['late_hours'])
                    else f"LATE by {float(row['late_hours']):.0f} hours")
            lines.append(
                f"  SIGNAL  {RULE_WORDS[row['rule']]:13s} {_coin(row['asset']):5s}"
                f" {row['direction'].upper():5s} entry {row['entry_day']} at "
                f"{_price(row['entry_raw'])}  stop {_price(row['stop'])}  "
                f"target {_price(row['target'])}  "
                f"size {_money(float(row['position_usd']))} dollars  [{when}]")
        else:
            lines.append(
                f"  ENDED   {RULE_WORDS[row['rule']]:13s} {_coin(row['asset']):5s}"
                f" {row['direction'].upper():5s} {EXIT_WORDS[row['exit_kind']]:13s}"
                f" on {row['exit_day']} ({row['reason']}): "
                f"{float(row['result_usd']):+.2f} dollars")
    lines += ['', f'OPEN NOW - {len(still_open)} trade(s) with at least one '
              f'ending still open']
    for trade in still_open:
        fixed = (f"stop {_price(trade['stop'])} target "
                 f"{_price(trade['target'])}" if trade['fixed_open']
                 else 'ended')
        trail = (f"stop now {_price(trade['trail_stop'])}"
                 if trade['trail_open'] else 'ended')
        lines.append(
            f"  {RULE_WORDS[trade['rule']]:13s} {_coin(trade['asset']):5s} "
            f"{trade['direction'].upper():5s} since {trade['entry_day']} at "
            f"{_price(trade['entry_raw'])} | fixed: {fixed} | trailing: "
            f"{trail}")
    lines += ['', 'THE RECORD - every signal, the same 1% at risk each, on a '
              'pretend 1,000 dollars', '  ("days" = different entry days: ten '
              'coins signalling on one day is one market move)']
    lines += _record_lines(rows)
    lines += ['', 'THE PORTFOLIO LINE - the same trades under a limit '
              '(way B). Not used to judge a rule.']
    lines += _portfolio_lines(rows)
    lines += ['', 'HEALTH']
    lines += health_lines(store, rows, frames, notes)
    lines += list(versus)
    lines += ['', 'Not counted: funding paid or received while a position is '
              'held. Prices are spot.', NO_MONEY, '=' * 78]
    return '\n'.join(lines)


def _where(record, directory, other):
    """A record's own folder and the other record's, unless told."""
    if record is None:
        return directory, other, ()
    mine = RECORDS[record] if directory is None else directory
    twin = 'cloud' if record == 'laptop' else 'laptop'
    theirs = RECORDS[twin] if other is None else other
    return mine, theirs, (twin,)


def _versus(record, mine, theirs, twin):
    return compare(mine, theirs, record, twin[0]) if twin else ()


def _prepare(directory, now, sources):
    """Store, frames, the working-out and the ledger. Shared by the three
    doorways. `sources` None = no network."""
    store = Store(directory)
    notes, next_opens = [], None
    if sources is not None:
        notes, next_opens = update(store, now, sources)
    if next_opens is None:
        next_opens = stored_next_opens(store)
    frames = {asset_of(coin): frame_of(store, asset_of(coin))
              for coin in COINS}
    worked, still_open = replay(frames, next_opens, entry_opens={
        key: float(value) for key, value in store.opens.items()})
    written = read_ledger(directory)
    alarms, new = reconcile(written, worked)
    return store, frames, worked, still_open, written, alarms, new, notes


def run(now=None, sources=None, directory=None, record=None, other=None):
    """A RUN: fetch, add, work out, check, append. Returns the report.
    Never raises. `record` ('laptop' or 'cloud') picks the folder and the
    funding door, and the report then compares the two records."""
    now = datetime.now(timezone.utc) if now is None else now
    try:
        directory, other, twin = _where(record, directory, other)
        sources = (real_sources(record or 'laptop') if sources is None
                   else sources)
        (store, frames, _worked, still_open, written, alarms, new,
         notes) = _prepare(directory, now, sources)
        if alarms:
            return render(store, written, still_open, frames, notes,
                          now=now, alarms=alarms, record=record,
                          versus=_versus(record, directory, other, twin))
        append_ledger(new, now, directory)
        rows = read_ledger(directory)
        return render(store, rows, still_open, frames, notes,
                      new_ids=[row['id'] for row in new], now=now,
                      record=record,
                      versus=_versus(record, directory, other, twin))
    except Exception as exc:
        return (f'PAPER-WATCH OFFLINE - {type(exc).__name__}: {exc}\n'
                f'Nothing is assumed. {NO_MONEY}')


def report(directory=None, record=None, other=None):
    """The report from what is stored. No network, nothing written."""
    try:
        directory, other, twin = _where(record, directory, other)
        (store, frames, _worked, still_open, written, alarms, _new,
         notes) = _prepare(directory, None, None)
        return render(store, written, still_open, frames, notes,
                      alarms=alarms, record=record,
                      versus=_versus(record, directory, other, twin))
    except Exception as exc:
        return (f'PAPER-WATCH OFFLINE - {type(exc).__name__}: {exc}\n'
                f'Nothing is assumed. {NO_MONEY}')


def week(directory=None, ending=None, record=None, other=None):
    """THE WEEK'S NUMBERS for the weekly autopsy: the seven completed days
    ending at the last one in the store. Numbers only. No network."""
    try:
        directory, other, twin = _where(record, directory, other)
        (store, frames, _worked, still_open, rows, alarms, _new,
         notes) = _prepare(directory, None, None)
        last = ending or max((store.last_day(asset_of(coin)) or ''
                              for coin in COINS), default='')
        if not last:
            return f'THE WEEK - nothing is stored yet. {NO_MONEY}'
        first = next_day(last, -6)
        lines = ['=' * 78, f'ZAR X - THE PAPER-WATCH - THE WEEK {first} to '
                 f'{last}', NO_MONEY, 'NUMBERS ONLY. The reading of them is '
                 'done in a session: say "weekly autopsy".', '=' * 78]
        if alarms:
            lines += ['', '!! INTEGRITY ALARM - the ledger is not what the '
                      'working-out gives:'] + [f'   {a}' for a in alarms[:20]]
        opened = [row for row in rows if row['kind'] == 'OPEN'
                  and first <= row['entry_day'] <= last]
        ended = [row for row in rows if row['kind'] == 'CLOSE'
                 and first <= row['exit_day'] <= last]
        lines += ['', f'SIGNALS THIS WEEK - {len(opened)}']
        for row in opened:
            when = ('on time' if on_time(row['late_hours'])
                    else f"late {float(row['late_hours']):.0f}h")
            lines.append(
                f"  {row['entry_day']}  {RULE_WORDS[row['rule']]:13s} "
                f"{_coin(row['asset']):5s} {row['direction'].upper():5s} at "
                f"{_price(row['entry_raw'])}  [{when}]")
        lines += ['', f'ENDINGS THIS WEEK - {len(ended)}']
        for row in ended:
            lines.append(
                f"  {row['exit_day']}  {RULE_WORDS[row['rule']]:13s} "
                f"{_coin(row['asset']):5s} {row['direction'].upper():5s} "
                f"{EXIT_WORDS[row['exit_kind']]:13s} {row['reason']:36s} "
                f"{float(row['result_usd']):+8.2f} dollars after "
                f"{row['days_held']} day(s)")
        lines += ['', 'THIS WEEK, BY RECORD (dollars on the pretend 1,000, '
                  'every signal at 1% risk)']
        for rule in RULES:
            for exit_kind in EXITS:
                mine = [row for row in ended if row['rule'] == rule
                        and row['exit_kind'] == exit_kind]
                won = sum(1 for row in mine if float(row['result_usd']) > 0)
                lines.append(
                    f"  {RULE_WORDS[rule]:13s} / {EXIT_WORDS[exit_kind]:13s}"
                    f"  {len(mine):3d} ended, {won:3d} won, "
                    f"{sum(float(r['result_usd']) for r in mine):+9.2f} "
                    f"dollars")
        lines += ['', 'THE TWO EXITS ON THE SAME TRADES (every trade both of '
                  'whose endings have happened, since the start)']
        closes = {row['id']: row for row in rows if row['kind'] == 'CLOSE'}
        for rule in RULES:
            pairs = [(closes[f"{row['id']}|fixed"], closes[f"{row['id']}|trail"])
                     for row in rows if row['kind'] == 'OPEN'
                     and row['rule'] == rule
                     and f"{row['id']}|fixed" in closes
                     and f"{row['id']}|trail" in closes]
            fixed = sum(float(a['result_usd']) for a, _b in pairs)
            trail = sum(float(b['result_usd']) for _a, b in pairs)
            better = sum(1 for a, b in pairs
                         if float(b['result_usd']) > float(a['result_usd']))
            worse = sum(1 for a, b in pairs
                        if float(b['result_usd']) < float(a['result_usd']))
            lines.append(
                f"  {RULE_WORDS[rule]:13s}  {len(pairs):3d} trades: fixed "
                f"{fixed:+9.2f}, trailing {trail:+9.2f} dollars; trailing "
                f"did better on {better}, worse on {worse}, the same on "
                f"{len(pairs) - better - worse}")
        lines += ['', 'THE MARKET THIS WEEK']
        above = below = 0
        for coin in COINS:
            df = frames.get(asset_of(coin))
            if df is None or len(df) < 101:
                continue
            closes_ = df['close']
            day_index = [stamp.strftime('%Y-%m-%d') for stamp in df.index]
            if last not in day_index or next_day(first, -1) not in day_index:
                continue
            at = day_index.index(last)
            before = float(closes_.iloc[day_index.index(next_day(first, -1))])
            change = 100.0 * (float(closes_.iloc[at]) / before - 1.0)
            average = float(closes_.iloc[at - 99:at + 1].mean())
            up = float(closes_.iloc[at]) > average
            above += int(up)
            below += int(not up)
            lines.append(f"  {coin:5s} {change:+7.2f}% over the week; "
                         f"{'ABOVE' if up else 'below'} its 100-day average")
        lines.append(f'  above their 100-day average: {above}; below: '
                     f'{below}')
        moods = [row for row in store.mood if first <= row[0] <= last]
        if moods:
            values = [row[1] for row in moods]
            lines.append(f'  mood index this week: from {min(values)} to '
                         f'{max(values)} (last: {moods[-1][1]}, '
                         f'{moods[-1][2]})')
        lines += ['', 'THE RECORD SINCE THE START']
        lines += _record_lines(rows)
        lines += ['', 'THE PORTFOLIO LINE (way B)']
        lines += _portfolio_lines(rows)
        lines += ['', f'OPEN NOW - {len(still_open)}', '', 'HEALTH']
        lines += health_lines(store, rows, frames, notes)
        lines += list(_versus(record, directory, other, twin))
        lines += ['', NO_MONEY, '=' * 78]
        if record:
            lines.insert(3, record_line(record))
        return '\n'.join(lines)
    except Exception as exc:
        return (f'PAPER-WATCH OFFLINE - {type(exc).__name__}: {exc}\n'
                f'Nothing is assumed. {NO_MONEY}')


def main(argv):
    """`--cloud` is the cloud's record; without it, the laptop's."""
    record = 'cloud' if '--cloud' in argv else 'laptop'
    if '--report' in argv:
        text = report(record=record)
    elif '--week' in argv:
        text = week(record=record)
    else:
        text = run(record=record)
    print(text)
    return verdict_code(text)


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        sys.exit(main(sys.argv[1:]))
    import paper_watch_gate
    sys.exit(paper_watch_gate.main())
