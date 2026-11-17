"""
Zar X journal compartment — GATE 7.1: the gate of `journal/paper_watch.py`.

Declared in PROGRESS_LOG.md on 2026-11-17 and committed with no code before
either file existed. **MADE-UP DATA ONLY. NO NETWORK. NOTHING REAL IS OPENED
OR WRITTEN:** every run it makes goes to a temporary folder with stand-in
sources, and `journal/paper/` is never touched.

It lives in its own file so that the file on trial can be copied, broken on
purpose and judged from outside (the drill). Every expectation is typed
HERE; none is read out of the file on trial.

    python journal/paper_watch.py --gate
"""
import csv
import hashlib
import importlib.util
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from fractions import Fraction

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(JOURNAL_DIR)
LAB_DIR = os.path.join(ROOT_DIR, 'lab')
for _path in (LAB_DIR, ROOT_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)
SOURCE = os.path.join(JOURNAL_DIR, 'paper_watch.py')

# ---- THE EXPECTATIONS, TYPED ---------------------------------------------
COINS13 = ('BTC', 'ETH', 'SOL', 'XRP', 'BNB', 'DOGE', 'NEAR', 'UNI', 'LINK',
           'AVAX', 'ADA', 'AAVE', 'BCH')
THREE = ('BTC', 'ETH', 'SOL')
RULE_NAMES = ('confluence-1d-t100', 'trend-only-1d-t100')
DAY = 86_400_000
OWED = 116                   # the checks this gate owes, drill included
DRILL_OWED = 27              # of which, sabotages


def ms(text):
    return int(datetime.strptime(text, '%Y-%m-%d').replace(
        tzinfo=timezone.utc).timestamp()) * 1000


def day(stamp):
    return datetime.fromtimestamp(stamp / 1000, tz=timezone.utc).strftime(
        '%Y-%m-%d')


def at(text, hour=0, minute=30, second=0):
    return datetime.strptime(text, '%Y-%m-%d').replace(
        tzinfo=timezone.utc, hour=hour, minute=minute, second=second)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def close_to(a, b, tolerance=1e-9):
    return abs(float(a) - float(b)) <= tolerance * max(abs(float(a)),
                                                       abs(float(b)), 1.0)


# ---- A MADE-UP WORLD ------------------------------------------------------

def label_of(value):
    return ('Extreme Fear' if value < 25 else 'Fear' if value < 47 else
            'Neutral' if value < 55 else 'Greed' if value < 76 else
            'Extreme Greed')


class World:
    """Thirteen made-up coins, their funding and one mood, 2025-08-01 on."""

    def __init__(self, seed=7, first='2025-08-01', days=560):
        import numpy as np
        rng = np.random.default_rng(seed)
        self.first = ms(first)
        self.candles, self.funding = {}, {}
        for k, coin in enumerate(COINS13):
            drift = np.repeat(rng.choice([-0.006, 0.006, 0.0],
                                         size=days // 40 + 1), 40)[:days]
            close = (50 + 10 * k) * np.exp(np.cumsum(
                drift + rng.normal(0, 0.03, days)))
            open_ = np.concatenate([[close[0]], close[:-1]])
            high = np.maximum(open_, close) * (1.001 + np.abs(
                rng.normal(0, 0.012, days)))
            low = np.minimum(open_, close) * (0.999 - np.abs(
                rng.normal(0, 0.012, days)))
            self.candles[coin] = [
                (self.first + i * DAY, f'{open_[i]:.8f}', f'{high[i]:.8f}',
                 f'{low[i]:.8f}', f'{close[i]:.8f}') for i in range(days)]
            rates = rng.integers(-40000, 40000, days * 3)
            self.funding[coin] = [
                (self.first + j * (DAY // 3), f'{int(rates[j]) / 1e8:.8f}')
                for j in range(days * 3)]
        walk = np.clip(np.cumsum(rng.normal(0, 6, days)) + 50, 3, 97)
        self.mood = {self.first + i * DAY: (int(walk[i]),
                                            label_of(int(walk[i])))
                     for i in range(days)}

    def copy(self):
        other = World.__new__(World)
        other.first = self.first
        other.candles = {coin: list(rows) for coin, rows in
                         self.candles.items()}
        other.funding = {coin: list(rows) for coin, rows in
                         self.funding.items()}
        other.mood = dict(self.mood)
        return other

    def sources(self, now, broken=(), all_broken=False):
        now_ms = int(now.timestamp() * 1000)

        def candles(symbol, start_ms):
            coin = symbol[:-4]
            if all_broken or coin in broken:
                raise ConnectionError('a made-up outage')
            rows = [[stamp, o, h, l, c, '0'] for stamp, o, h, l, c in
                    self.candles[coin] if start_ms <= stamp <= now_ms]
            return rows[:1000]

        def funding(params):
            if all_broken:
                raise ConnectionError('a made-up outage')
            coin = params['symbol'][:-4]
            rows = [{'fundingTime': stamp, 'fundingRate': rate}
                    for stamp, rate in self.funding[coin]
                    if params['startTime'] <= stamp <= params['endTime']
                    and stamp <= now_ms]
            return rows[:params['limit']]

        def mood():
            if all_broken:
                raise ConnectionError('a made-up outage')
            return {'data': [{'timestamp': str(stamp // 1000),
                              'value': str(value),
                              'value_classification': label}
                             for stamp, (value, label) in
                             sorted(self.mood.items()) if stamp <= now_ms]}

        return {'candles': candles, 'funding': funding, 'mood': mood}


def world_frame(world, coin, days=None):
    """A frame built by the gate itself, with the Lab's two join functions
    (which have their own gates)."""
    import funding_vault
    import mood_vault
    import pandas as pd
    rows = world.candles[coin][:days]
    df = pd.DataFrame([[float(x) for x in row[1:]] for row in rows],
                      index=pd.to_datetime([day(row[0]) for row in rows]),
                      columns=['open', 'high', 'low', 'close'])
    settle = [row for row in world.funding[coin]
              if row[0] < rows[-1][0] + DAY]
    df = funding_vault.attach(df, [s for s, _r in settle],
                              [funding_vault.rate_units(r) for _s, r in
                               settle])
    stamps = sorted(world.mood)
    return mood_vault.attach(
        df, stamps, [world.mood[s][0] for s in stamps],
        [mood_vault.LABELS[world.mood[s][1]] for s in stamps])


# ---- THE RULES, WORKED A SECOND TIME IN PLAIN PYTHON ----------------------

def plain_signal(rule_name, closes, funding, mood, side):
    """What a rule answers at the close of the last day handed to it."""
    import numpy as np
    n = len(closes)

    def funding_fade():
        if n < 91:
            return 'flat'
        tail = funding[-91:]
        if any(x != x for x in tail):
            return 'flat'
        today, before = tail[-1], tail[:-1]
        if today > 0 and sum(1 for b in before if b < today) >= 81:
            return 'short'
        if today < 0 and sum(1 for b in before if b > today) >= 81:
            return 'long'
        return 'flat'

    def mood_fade():
        if n < 91:
            return 'flat'
        tail = mood[-91:]
        if any(x != x for x in tail) or side[-1] != side[-1]:
            return 'flat'
        today, before = tail[-1], tail[:-1]
        if side[-1] < 0 and sum(1 for b in before if b > today) >= 81:
            return 'long'
        if side[-1] > 0 and sum(1 for b in before if b < today) >= 81:
            return 'short'
        return 'flat'

    if n < 100:
        return 'flat'
    window = np.asarray(closes[-100:], dtype=float)
    average = float(window.sum()) / 100
    way = 1 if closes[-1] > average else -1 if closes[-1] < average else 0
    if rule_name == 'trend-only-1d-t100':
        return 'long' if way > 0 else 'short' if way < 0 else 'flat'
    crowd = (funding_fade(), mood_fade())
    if way > 0 and 'short' in crowd:
        return 'long'
    if way < 0 and 'long' in crowd:
        return 'short'
    return 'flat'


class Stub:
    """A made-up rule for the hand cases: one answer, on one day."""

    def __init__(self, on_length, side):
        self.on_length, self.side = on_length, side
        self.name, self.params = 'confluence-1d-t100', {}

    def __call__(self, df):
        return self.side if len(df) == self.on_length else 'flat'


def hand_frame(tail, warm=(100.0, 103.0, 97.0, 100.0)):
    import pandas as pd
    rows = [warm] * 20 + list(tail)
    return pd.DataFrame(rows, columns=['open', 'high', 'low', 'close'],
                        index=pd.date_range('2030-01-01', periods=len(rows),
                                            freq='1D'))


def hand_day(position):
    return day(ms('2030-01-01') + position * DAY)


def gate_chain(previous, cells):
    text = previous + '|' + '|'.join(cells[:-1])
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def read_csv(path):
    with open(path, encoding='utf-8', newline='') as handle:
        return list(csv.reader(handle))


def write_csv(path, rows):
    with open(path, 'w', encoding='utf-8', newline='') as handle:
        csv.writer(handle, lineterminator='\n').writerows(rows)


def rechain(rows):
    previous = ''
    for row in rows[1:]:
        row[-1] = previous = gate_chain(previous, row)
    return rows


def file_bytes(directory):
    out = {}
    for name in sorted(os.listdir(directory)):
        with open(os.path.join(directory, name), 'rb') as handle:
            out[name] = handle.read()
    return out


def gate_score(rows, rule, exit_kind, coins):
    """One record's figures, worked by the gate from ledger rows."""
    assets = {f'{coin}-USD' for coin in coins}
    mine = [row for row in rows if row['kind'] == 'CLOSE'
            and row['rule'] == rule and row['exit_kind'] == exit_kind
            and row['asset'] in assets]
    results = [float(row['result_frac']) for row in mine]
    equity = peak = 1.0
    dip = 0.0
    for value in results:
        equity = equity * (1.0 + value)
        peak = max(peak, equity)
        dip = max(dip, (peak - equity) / peak)
    gains = sum(v for v in results if v > 0)
    pains = -sum(v for v in results if v <= 0)
    return {'trades': len(mine),
            'days': len(set(row['entry_day'] for row in mine)),
            'won': sum(1 for v in results if v > 0),
            'pf': gains / pains if pains > 0 else None,
            'money': 1000.0 * equity, 'dip': 100.0 * dip}


# ---- THE SUITE ------------------------------------------------------------

class Suite:
    """Every check, against one copy of the file on trial."""

    def __init__(self, pw, world):
        self.pw, self.world = pw, world
        self.results = []
        self.names = []             # each check's own words, with nothing added
        self.tmp = tempfile.mkdtemp(prefix='zarx_paper_gate_')
        self._cache = {}

    def done(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def mark(self, text, test):
        self.names.append(text)
        try:
            good = bool(test())
        except Exception as exc:            # a check must be able to say no
            good = False
            text = f'{text} [raised {type(exc).__name__}: {str(exc)[:90]}]'
        self.results.append((good, text))

    def folder(self, name):
        path = os.path.join(self.tmp, name)
        os.makedirs(path, exist_ok=True)
        return path

    def ledger(self, directory):
        path = os.path.join(directory, 'ledger.csv')
        if not os.path.exists(path):
            return []
        rows = read_csv(path)
        return [dict(zip(rows[0], row)) for row in rows[1:]]

    # -- scenarios, made once --
    def long_run(self):
        """One late run on 2027-01-25: seventy days worked in one go."""
        if 'long' not in self._cache:
            directory = self.folder('long')
            now = at('2027-01-25', 12, 0)
            text = self.pw.run(now=now, sources=self.world.sources(now),
                               directory=directory)
            self._cache['long'] = (directory, text, now)
        return self._cache['long']

    def daily_runs(self):
        """Five runs, one a morning, 2026-11-17 to 2026-11-21, 00:30 UTC."""
        if 'daily' not in self._cache:
            directory = self.folder('daily')
            texts, snaps = [], []
            for text_day in ('2026-11-17', '2026-11-18', '2026-11-19',
                             '2026-11-20', '2026-11-21'):
                now = at(text_day)
                texts.append(self.pw.run(now=now,
                                         sources=self.world.sources(now),
                                         directory=directory))
                snaps.append(file_bytes(directory))
            self._cache['daily'] = (directory, texts, snaps)
        return self._cache['daily']

    def late_run(self):
        """The same five mornings worked in ONE run, on 2026-11-21."""
        if 'late' not in self._cache:
            directory = self.folder('late')
            now = at('2026-11-21')
            self._cache['late_text'] = self.pw.run(
                now=now, sources=self.world.sources(now),
                directory=directory)
            self._cache['late'] = directory
        return self._cache['late']

    def engine_events(self):
        """Both rules on three made-up coins, by the file on trial and by
        the Lab's engine."""
        if 'engine' not in self._cache:
            import engine
            import forward_check
            from config import GAUNTLET_COSTS
            from signals.confluence import Confluence, TrendOnly
            out = {}
            for rule in (Confluence(), TrendOnly()):
                pairs = []
                for coin in ('BTC', 'NEAR', 'BCH'):
                    df = world_frame(self.world, coin)
                    asset = f'{coin}-USD'
                    theirs = engine.run_backtest(
                        forward_check.as_vault(asset, df), rule,
                        strategy_name=rule.name, params=rule.params,
                        verbose=False, costs=GAUNTLET_COSTS,
                        sl_atr_mult=1.5, tp_atr_mult=3.0, capital=1000.0,
                        regime=False).trades
                    events, still = self.pw.replay(
                        {asset: df}, start_day=day(self.world.first),
                        rules=[rule])
                    pairs.append((df, theirs.to_dict('records'), events,
                                  still))
                out[rule.name] = pairs
            self._cache['engine'] = out
        return self._cache['engine']

    # -- (a) the numbers --
    def g_const(self):
        pw = self.pw
        self.mark('(a) thirteen coins by name, the original three, and both '
                  'rule names are the ones typed here',
                  lambda: tuple(pw.COINS) == COINS13
                  and tuple(pw.ORIGINAL) == THREE
                  and tuple(pw.RULES) == RULE_NAMES)
        self.mark('(a) first stop 1.5, target 3.0, trailing reach 3.0 '
                  'ranges; the range is 14 days',
                  lambda: (pw.SL_ATR, pw.TP_ATR, pw.TRAIL_ATR,
                           pw.ATR_PERIOD) == (1.5, 3.0, 3.0, 14))
        self.mark('(a) 0.05% fee and 0.05% slippage a side - and that IS '
                  'what config.GAUNTLET_COSTS says',
                  lambda: (pw.FEE, pw.SLIP) == (0.0005, 0.0005)
                  and __import__('config').GAUNTLET_COSTS
                  == {'fee_pct': 0.0005, 'slippage_pct': 0.0005})
        self.mark('(a) a pretend 1,000 dollars, 1% at risk a signal, the '
                  'portfolio limit 4%',
                  lambda: pw.ACCOUNT == 1000.0 and pw.RISK == Fraction(1, 100)
                  and pw.CAP == Fraction(4, 100))
        self.mark('(a) the first day asked is 2026-11-16; 400 days behind '
                  'it; on time is 6 hours; the mood is carried 3 days at most',
                  lambda: (pw.START_DAY, pw.SEED_DAYS, pw.ON_TIME_HOURS,
                           pw.MAX_CARRIED_RUN) == ('2026-11-16', 400, 6, 3))
        self.mark('(a) the rules it calls are the frozen classes of '
                  'signals/confluence.py, under their own names',
                  lambda: [(type(r).__module__, type(r).__name__, r.name)
                           for r in pw._lab()[3]]
                  == [('signals.confluence', 'Confluence',
                       'confluence-1d-t100'),
                      ('signals.confluence', 'TrendOnly',
                       'trend-only-1d-t100')])

    # -- (b) the Lab's engine is the witness --
    def g_engine(self):
        for name in RULE_NAMES:
            def compare(name=name):
                wrong = total = 0
                for _df, theirs, events, _still in self.engine_events()[name]:
                    opens = {e['id']: e for e in events if e['kind'] == 'OPEN'}
                    mine = sorted(
                        ((opens[e['id'].rsplit('|', 1)[0]], e) for e in events
                         if e['kind'] == 'CLOSE' and e['exit_kind'] == 'fixed'),
                        key=lambda pair: pair[0]['entry_day'])
                    theirs = [t for t in theirs if t['exit_reason']
                              != 'end of data (forced close)']
                    if len(mine) != len(theirs):
                        return False
                    for (o, c), t in zip(mine, theirs):
                        total += 1
                        same = (o['entry_day'] == str(t['entry_time'])[:10]
                                and o['direction'] == t['direction']
                                and close_to(o['entry_fill'],
                                             t['entry_price_fill'])
                                and close_to(o['stop'], t['stop_loss'])
                                and close_to(o['target'], t['take_profit'])
                                and c['exit_day'] == str(t['exit_time'])[:10]
                                and close_to(c['exit_raw'],
                                             t['exit_price_raw'])
                                and c['reason'].split(' ')[0]
                                == t['exit_reason'].split(' ')[0]
                                and abs(c['result_frac'] - t['return_pct'])
                                <= 1e-12)
                        wrong += not same
                self._cache[('count', name)] = total
                return wrong == 0 and total > 0
            self.mark(f'(b) {name}: every fixed-exit trade equals the Lab '
                      f'engine\'s, trade for trade - day in, side, fill, '
                      f'stop, target, day out, price out, reason, result',
                      compare)

            def not_empty(name=name):
                sides, reasons, total = set(), set(), 0
                for _df, _t, events, _s in self.engine_events()[name]:
                    for e in events:
                        if e['kind'] == 'CLOSE' and e['exit_kind'] == 'fixed':
                            total += 1
                            sides.add(e['direction'])
                            reasons.add(e['reason'])
                return (total >= 20 and sides == {'long', 'short'}
                        and {'stop', 'target'} <= reasons)
            self.mark(f'(b) {name}: and that comparison is not empty - at '
                      f'least 20 trades, both sides, stops and targets',
                      not_empty)

    # -- (c) every signal worked a second time --
    def g_signals(self):
        for name in RULE_NAMES:
            def rederive(name=name):
                asked_days = opens_seen = 0
                for df, _t, events, _s in self.engine_events()[name]:
                    days = [s.strftime('%Y-%m-%d') for s in df.index]
                    closes = [float(x) for x in df['close']]
                    funding = [float(x) for x in df['funding']]
                    mood = [float(x) for x in df['mood']]
                    side = [float(x) for x in df['mood_side']]
                    opens = {e['signal_day']: e for e in events
                             if e['kind'] == 'OPEN'}
                    ends = {e['entry_day']: e['exit_day'] for e in events
                            if e['kind'] == 'CLOSE'
                            and e['exit_kind'] == 'fixed'}
                    held = []
                    for e in opens.values():
                        held.append((e['entry_day'],
                                     ends.get(e['entry_day'], '9999-99-99')))
                    for i, d in enumerate(days[:-1]):
                        busy = any(a <= d < b for a, b in held)
                        answer = plain_signal(name, closes[:i + 1],
                                              funding[:i + 1], mood[:i + 1],
                                              side[:i + 1])
                        if busy:
                            if d in opens:
                                return False
                            continue
                        asked_days += 1
                        if answer == 'flat':
                            if d in opens:
                                return False
                        else:
                            got = opens.get(d)
                            if (got is None or got['direction'] != answer
                                    or got['entry_day'] != days[i + 1]):
                                return False
                            opens_seen += 1
                return asked_days > 100 and opens_seen >= 20
            self.mark(f'(c) {name}: EVERY signal worked a second time in '
                      f'plain Python from the closes, funding and mood - a '
                      f'trade where the rule says one, none where it says '
                      f'none, never while a trade is open', rederive)

        def future_cannot_reach_back():
            import numpy as np
            df, _t, events, _s = self.engine_events()['confluence-1d-t100'][0]
            cut = 400
            poisoned = df.copy()
            poisoned.iloc[cut:, :] = np.nan
            poisoned.loc[poisoned.index[cut:], ['open', 'high', 'low',
                                                'close']] = 1.0
            clean, _ = self.pw.replay({'BTC-USD': df.iloc[:cut]},
                                      start_day=day(self.world.first))
            again, _ = self.pw.replay({'BTC-USD': poisoned.iloc[:cut]},
                                      start_day=day(self.world.first))
            whole = [e for e in self.pw.replay(
                {'BTC-USD': df}, start_day=day(self.world.first))[0]
                if (e['exit_day'] or e['entry_day'])
                <= df.index[cut - 1].strftime('%Y-%m-%d')]
            keys = lambda rows: sorted(
                (e['id'], repr(e['entry_fill']), repr(e['result_frac']))
                for e in rows)
            return (len(clean) > 20 and keys(clean) == keys(again)
                    and keys(whole) == keys(clean))
        self.mark('(c) what happens after a day cannot change one row dated '
                  'on or before it: 400 days alone give the same rows as '
                  'the first 400 of 560', future_cannot_reach_back)

    # -- (d) the trailing exit, by hand, both sides --
    def hand(self, side, tail, warm=(100.0, 103.0, 97.0, 100.0)):
        df = hand_frame(tail, warm)
        events, still = self.pw.replay({'BTC-USD': df},
                                       start_day='2030-01-01',
                                       rules=[Stub(20, side)])
        opened = [e for e in events if e['kind'] == 'OPEN']
        closes = {e['exit_kind']: e for e in events if e['kind'] == 'CLOSE'}
        return opened, closes, still

    @staticmethod
    def expect(side, exit_raw, stop_distance=9.0, cap=False):
        """The typed arithmetic of one trade entered at 100."""
        if side == 'long':
            fill = 100.0 * (1 + 0.0005)
            out = exit_raw * (1 - 0.0005)
        else:
            fill = 100.0 * (1 - 0.0005)
            out = exit_raw * (1 + 0.0005)
        coins = (1000.0 * 0.01) / stop_distance
        if cap:
            coins = 250.0 / fill
        gain = coins * (out - fill) if side == 'long' else coins * (fill - out)
        fees = 0.0005 * (coins * fill + coins * out)
        return fill, coins, (gain - fees) / 1000.0

    def g_hand(self):
        long_fill = 100.0 * 1.0005
        short_fill = 100.0 * 0.9995
        long_stop, long_target = long_fill - 9.0, long_fill + 18.0
        short_stop, short_target = short_fill + 9.0, short_fill - 18.0
        long_tail = [(100, 104, 99, 103), (103, 112, 102, 111),
                     (111, 126, 100, 125), (125, 126, 108, 109)]
        short_tail = [(100, 101, 96, 97), (97, 98, 88, 89),
                      (89, 100, 74, 75), (75, 92, 74, 91)]

        def opening(side, fill, stop, target):
            opened, _c, _s = self.hand(side, (long_tail if side == 'long'
                                              else short_tail))
            o = opened[0]
            return (len(opened) == 1 and o['signal_day'] == hand_day(19)
                    and o['entry_day'] == hand_day(20)
                    and o['direction'] == side
                    and close_to(o['entry_fill'], fill)
                    and close_to(o['range'], 6.0)
                    and close_to(o['stop'], stop)
                    and close_to(o['target'], target)
                    and close_to(o['coins'], 10.0 / 9.0)
                    and close_to(o['risk_usd'], 10.0)
                    and close_to(o['position_usd'], 10.0 / 9.0 * fill))
        self.mark('(d) LONG, the entry by hand: signalled on day 20, in at '
                  'day 21\'s open made worse by 0.05%, stop 9 under, target '
                  '18 over, 10 dollars at risk',
                  lambda: opening('long', long_fill, long_stop, long_target))
        self.mark('(d) SHORT, the mirror: in at 99.95, stop 9 over, target '
                  '18 under, 10 dollars at risk',
                  lambda: opening('short', short_fill, short_stop,
                                  short_target))

        def fixed_target(side, target, tail):
            _o, closes, _s = self.hand(side, tail)
            c = closes['fixed']
            return (c['exit_day'] == hand_day(22) and c['reason'] == 'target'
                    and close_to(c['exit_raw'], target)
                    and abs(c['result_frac']
                            - self.expect(side, target)[2]) <= 1e-12)
        self.mark('(d) LONG: the fixed ending takes the target on day 23, '
                  'at the target and not a cent better',
                  lambda: fixed_target('long', long_target, long_tail))
        self.mark('(d) SHORT: the fixed ending takes its target the same way',
                  lambda: fixed_target('short', short_target, short_tail))

        def trailing(side, tail, last, want_day, want_raw, want_reason):
            _o, closes, still = self.hand(side, list(tail) + [last])
            if want_day is None:
                return ('trail' not in closes and len(still) == 1
                        and still[0]['trail_open'])
            c = closes.get('trail')
            return (c is not None and c['exit_day'] == hand_day(want_day)
                    and c['reason'] == want_reason
                    and close_to(c['exit_raw'], want_raw)
                    and abs(c['result_frac']
                            - self.expect(side, want_raw)[2]) <= 1e-12)
        self.mark('(d) LONG TRAILING: the stop climbs 91.05 -> 93 -> 107, '
                  'does NOT fall back when the close drops to 109, is NOT '
                  'hit on the day whose own close lifted it, and is hit at '
                  'EXACTLY 107.00',
                  lambda: trailing('long', long_tail, (109, 110, 107.0, 108),
                                   24, 107.0, 'trailing stop'))
        self.mark('(d) LONG TRAILING: a low of 107.01 is NOT a hit',
                  lambda: trailing('long', long_tail, (109, 110, 107.01, 108),
                                   None, None, None))
        self.mark('(d) LONG TRAILING: a day that OPENS under the stop (104) '
                  'is left at the open, not at the stop',
                  lambda: trailing('long', long_tail, (104, 105, 103, 104),
                                   24, 104.0, 'trailing stop'))
        self.mark('(d) SHORT TRAILING: the stop falls 108.95 -> 107 -> 93, '
                  'does NOT rise back, is NOT hit on the day whose own '
                  'close lowered it, and is hit at EXACTLY 93.00',
                  lambda: trailing('short', short_tail, (91, 93.0, 90, 92),
                                   24, 93.0, 'trailing stop'))
        self.mark('(d) SHORT TRAILING: a high of 92.99 is NOT a hit',
                  lambda: trailing('short', short_tail, (91, 92.99, 90, 92),
                                   None, None, None))
        self.mark('(d) SHORT TRAILING: a day that OPENS over the stop (96) '
                  'is left at the open',
                  lambda: trailing('short', short_tail, (96, 97, 95, 96),
                                   24, 96.0, 'trailing stop'))

        def never_behind_the_first_stop(side, tail, stop):
            _o, closes, still = self.hand(side, tail)
            f, t = closes.get('fixed'), closes.get('trail')
            return (f and t and not still
                    and t['exit_day'] == hand_day(21) == f['exit_day']
                    and t['reason'] == 'first stop'
                    and close_to(t['exit_raw'], stop)
                    and abs(t['result_frac']
                            - self.expect(side, stop)[2]) <= 1e-12)
        self.mark('(d) LONG TRAILING: while the best close less the reach '
                  'is still UNDER the first stop (103 - 18 = 85), the stop '
                  'stays at the first stop - a low of 91.00 the next day '
                  'ends it at 91.05',
                  lambda: never_behind_the_first_stop(
                      'long', [(100, 104, 99, 103), (103, 104, 91.0, 92)],
                      long_stop))
        self.mark('(d) SHORT TRAILING: the mirror - 97 + 18 = 115 is over '
                  'the first stop, so it stays at 108.95 and a high of '
                  '109.00 ends it there',
                  lambda: never_behind_the_first_stop(
                      'short', [(100, 101, 96, 97), (97, 109.0, 96, 108)],
                      short_stop))

        def gap_through_both(side, tail, opened_at):
            _o, closes, still = self.hand(side, tail)
            f, t = closes.get('fixed'), closes.get('trail')
            want = self.expect(side, opened_at)[2]
            return (f and t and not still and f['reason'] == 'stop'
                    and t['reason'] == 'first stop'
                    and f['exit_day'] == hand_day(21) == t['exit_day']
                    and close_to(f['exit_raw'], opened_at)
                    and close_to(t['exit_raw'], opened_at)
                    and abs(f['result_frac'] - want) <= 1e-12
                    and abs(t['result_frac'] - want) <= 1e-12)
        self.mark('(d) LONG: a day that OPENS under the first stop (88, the '
                  'stop at 91.05) ends BOTH endings at the open - the loss '
                  'is bigger than the 10 dollars planned, and is counted so',
                  lambda: gap_through_both(
                      'long', [(100, 104, 99, 103), (88, 89, 87, 88)], 88.0))
        self.mark('(d) SHORT: the mirror - a day that opens at 112, over '
                  'the stop at 108.95, ends both at 112',
                  lambda: gap_through_both(
                      'short', [(100, 101, 96, 97), (112, 113, 111, 112)],
                      112.0))

        def first_day(side, candle, stop):
            _o, closes, still = self.hand(side, [candle])
            f, t = closes.get('fixed'), closes.get('trail')
            want = self.expect(side, stop)[2]
            return (f and t and not still and f['exit_day'] == hand_day(20)
                    == t['exit_day'] and f['reason'] == 'stop'
                    and t['reason'] == 'first stop'
                    and close_to(f['exit_raw'], stop)
                    and close_to(t['exit_raw'], stop)
                    and abs(f['result_frac'] - want) <= 1e-12
                    and f['result_frac'] == t['result_frac'])
        self.mark('(d) LONG: stopped on the entry day itself, with the low '
                  'EXACTLY on the stop - both endings, the same loss',
                  lambda: first_day('long', (100, 101, long_stop, 99),
                                    long_stop))
        self.mark('(d) SHORT: the same, the high EXACTLY on the stop',
                  lambda: first_day('short', (100, short_stop, 99, 100),
                                    short_stop))

        def just_missed(side, candle):
            _o, closes, still = self.hand(side, [candle])
            return not closes and len(still) == 1
        self.mark('(d) LONG: a low one millionth ABOVE the stop ends nothing',
                  lambda: just_missed('long', (100, 101, long_stop + 1e-6,
                                               100)))
        self.mark('(d) SHORT: a high one millionth BELOW the stop ends '
                  'nothing',
                  lambda: just_missed('short', (100, short_stop - 1e-6, 99,
                                                100)))

        def both_in_one(side, candle, stop):
            _o, closes, _s = self.hand(side, [candle])
            f = closes['fixed']
            return (f['reason'] == 'stop+target same day (loss counted)'
                    and close_to(f['exit_raw'], stop)
                    and f['result_frac'] < 0)
        self.mark('(d) LONG: stop and target inside one day counts the LOSS',
                  lambda: both_in_one('long', (100, 119, 91, 100), long_stop))
        self.mark('(d) SHORT: stop and target inside one day counts the '
                  'LOSS too',
                  lambda: both_in_one('short', (100, 109, 81, 100),
                                      short_stop))

        def capped():
            opened, _c, _s = self.hand('long', [(100, 100.5, 99.9, 100)],
                                       warm=(100.0, 100.5, 99.5, 100.0))
            o = opened[0]
            fill = 100.0 * 1.0005
            return (close_to(o['range'], 1.0)
                    and close_to(o['position_usd'], 250.0)
                    and close_to(o['coins'], 250.0 / fill)
                    and close_to(o['risk_usd'], 250.0 / fill * 1.5))
        self.mark('(d) a tight stop does not buy more than 250 dollars of '
                  'coin: the 25% cap holds and the risk shrinks to match',
                  capped)

    # -- (e) one entry, two endings --
    def g_twins(self):
        def shared():
            for name in RULE_NAMES:
                for _df, _t, events, still in self.engine_events()[name]:
                    opens = {e['id']: e for e in events if e['kind'] == 'OPEN'}
                    if len(opens) != sum(e['kind'] == 'OPEN' for e in events):
                        return False
                    seen = set()
                    for e in events:
                        if e['kind'] != 'CLOSE':
                            continue
                        parent, kind = e['id'].rsplit('|', 1)
                        o = opens.get(parent)
                        if (o is None or e['id'] in seen
                                or kind not in ('fixed', 'trail')
                                or e['entry_day'] != o['entry_day']
                                or e['direction'] != o['direction']
                                or e['exit_day'] < o['entry_day']):
                            return False
                        seen.add(e['id'])
                    waiting = {(t['id'], k) for t in still
                               for k in ('fixed', 'trail')
                               if t[f'{k}_open']}
                    for parent in opens:
                        for k in ('fixed', 'trail'):
                            if ((f'{parent}|{k}' in seen)
                                    == ((parent, k) in waiting)):
                                return False
            return True
        self.mark('(e) every signal has exactly two endings, fixed and '
                  'trailing, each either happened once or still open - and '
                  'both stand on the same entry', shared)

        def overlap():
            for _df, _t, events, _s in self.engine_events()[
                    'trend-only-1d-t100']:
                opens = sorted(e['entry_day'] for e in events
                               if e['kind'] == 'OPEN')
                ends = {e['entry_day']: e['exit_day'] for e in events
                        if e['kind'] == 'CLOSE' and e['exit_kind'] == 'trail'}
                for a, b in zip(opens, opens[1:]):
                    if ends.get(a, '9999') > b:
                        return True
            return False
        self.mark('(e) and the case the bar named does happen: a trailing '
                  'ending still open when the rule signals again on that '
                  'coin', overlap)

    # -- (f) the portfolio line, by hand --
    @staticmethod
    def rows_for(plan):
        """plan: [(coin, entry_day, exit_day or None, fraction)]"""
        rows = []
        for coin, entry, leave, fraction in plan:
            base = f'confluence-1d-t100|{coin}-USD|{entry}'
            rows.append({'kind': 'OPEN', 'id': base,
                         'rule': 'confluence-1d-t100', 'asset': f'{coin}-USD',
                         'entry_day': entry, 'exit_kind': '', 'exit_day': ''})
            if leave:
                rows.append({'kind': 'CLOSE', 'id': f'{base}|fixed',
                             'rule': 'confluence-1d-t100',
                             'asset': f'{coin}-USD', 'entry_day': entry,
                             'exit_kind': 'fixed', 'exit_day': leave,
                             'result_frac': repr(fraction)})
        return rows

    def g_portfolio(self):
        line = lambda plan: self.pw.portfolio(
            self.rows_for(plan), 'confluence-1d-t100', 'fixed', COINS13)
        eight = [(coin, '2030-01-05', '2030-01-09', 0.02)
                 for coin in COINS13[:8]]

        def eight_in_a_morning():
            p = line(eight)
            return (close_to(p['money'], 1000.0 * 1.01 ** 8)
                    and (p['full'], p['reduced'], p['not_taken']) == (0, 8, 0))
        self.mark('(f) EIGHT SIGNALS IN ONE MORNING share the 4%: half a '
                  'percent each, so eight 2% wins make 1,000 x 1.01^8',
                  eight_in_a_morning)

        def two_and_six():
            plan = ([(c, '2030-01-05', '2030-01-20', 0.02)
                     for c in COINS13[:2]]
                    + [(c, '2030-01-06', '2030-01-09', 0.03)
                       for c in COINS13[2:8]])
            p = line(plan)
            want = 1000.0 * (1 + 0.03 / 3) ** 6 * 1.02 ** 2
            return (close_to(p['money'], want)
                    and (p['full'], p['reduced'], p['not_taken']) == (2, 6, 0))
        self.mark('(f) TWO OPEN AND SIX NEW: the six share the 2% left, a '
                  'third of a percent each', two_and_six)

        def no_room():
            plan = ([(c, '2030-01-05', '2030-01-20', 0.01)
                     for c in COINS13[:4]]
                    + [(c, '2030-01-06', '2030-01-09', 0.5)
                       for c in COINS13[4:7]])
            p = line(plan)
            return (close_to(p['money'], 1000.0 * 1.01 ** 4)
                    and (p['full'], p['reduced'], p['not_taken']) == (4, 0, 3))
        self.mark('(f) NO ROOM LEFT: four open at 1% each is the limit, and '
                  'three new ones are NOT TAKEN - their results are not '
                  'counted, however good', no_room)

        def exactly_at_the_limit():
            four = line([(c, '2030-01-05', '2030-01-09', 0.02)
                         for c in COINS13[:4]])
            five = line([(c, '2030-01-05', '2030-01-09', 0.02)
                         for c in COINS13[:5]])
            return ((four['full'], four['reduced']) == (4, 0)
                    and close_to(four['money'], 1000.0 * 1.02 ** 4)
                    and (five['full'], five['reduced']) == (0, 5)
                    and close_to(five['money'], 1000.0 * 1.016 ** 5))
        self.mark('(f) EXACTLY AT THE LIMIT: four at once are each taken in '
                  'full; a fifth makes all five 0.8%', exactly_at_the_limit)

        def room_comes_back_next_day():
            plan = ([(c, '2030-01-05', '2030-01-07' if c == 'BTC'
                      else '2030-01-20', 0.01) for c in COINS13[:4]]
                    + [('BNB', '2030-01-07', '2030-01-09', 0.5),
                       ('DOGE', '2030-01-08', '2030-01-09', 0.02)])
            p = line(plan)
            return ((p['full'], p['reduced'], p['not_taken']) == (5, 0, 1)
                    and close_to(p['money'], 1000.0 * 1.01 ** 4 * 1.02))
        self.mark('(f) a trade that ends on Tuesday frees its room for '
                  'WEDNESDAY\'s signals, not Tuesday\'s: Tuesday\'s is not '
                  'taken, Wednesday\'s is taken in full',
                  room_comes_back_next_day)

    # -- (g) the ledger --
    def copy_long(self, name):
        directory, _text, now = self.long_run()
        target = os.path.join(self.tmp, name)
        shutil.copytree(directory, target)
        return target, now

    def rerun(self, directory, now):
        return self.pw.run(now=now, sources=self.world.sources(now),
                           directory=directory)

    def g_ledger(self):
        def has_rows():
            directory, text, _now = self.long_run()
            rows = self.ledger(directory)
            return (sum(r['kind'] == 'OPEN' for r in rows) >= 40
                    and sum(r['kind'] == 'CLOSE' for r in rows) >= 40
                    and 'INTEGRITY ALARM' not in text
                    and 'OFFLINE' not in text)
        self.mark('(g) a run seventy days late writes a ledger - at least '
                  '40 signals and 40 endings - and raises no alarm',
                  has_rows)

        def second_run_writes_nothing():
            directory, now = self.copy_long('again')
            before = file_bytes(directory)
            text = self.rerun(directory, now)
            return (file_bytes(directory) == before
                    and 'NEW THIS RUN - 0 signal(s), 0 ending(s)' in text
                    and 'INTEGRITY ALARM' not in text)
        self.mark('(g) a second run the same morning writes NOTHING: not '
                  'one byte of any of the five files', second_run_writes_nothing)

        def tamper(name, change, words):
            directory, now = self.copy_long(name)
            path = os.path.join(directory, 'ledger.csv')
            rows = read_csv(path)
            change(rows)
            write_csv(path, rows)
            before = file_bytes(directory)['ledger.csv']
            text = self.rerun(directory, now)
            return ('INTEGRITY ALARM' in text and words in text
                    and file_bytes(directory)['ledger.csv'] == before)

        def one_digit(rows):
            at_ = rows[0].index('stop')
            row = next(r for r in rows[1:] if r[0] == 'OPEN')
            row[at_] = repr(float(row[at_]) * 1.01)
        self.mark('(g) ONE FIGURE changed in a written row (a stop moved by '
                  '1%): INTEGRITY ALARM, and the run writes nothing',
                  lambda: tamper('digit', one_digit, 'chain is broken'))

        def one_digit_and_rechain(rows):
            one_digit(rows)
            rechain(rows)
        self.mark('(g) the same change with the chain repaired after it: '
                  'STILL an alarm - the row is not what the working-out '
                  'gives', lambda: tamper('rechained', one_digit_and_rechain,
                                          'is not what the working-out gives'))

        def result_and_rechain(rows):
            at_ = rows[0].index('result_frac')
            row = next(r for r in rows[1:] if r[0] == 'CLOSE'
                       and float(r[at_]) < 0)
            row[at_] = repr(-float(row[at_]))
            rechain(rows)
        self.mark('(g) a LOSS rewritten as a win, the chain repaired: an '
                  'alarm', lambda: tamper('flip', result_and_rechain,
                                          'is not what the working-out gives'))

        def delete_middle(rows):
            del rows[len(rows) // 2]
        self.mark('(g) a row removed from the middle: an alarm',
                  lambda: tamper('deleted', delete_middle, 'chain is broken'))

        def invent(rows):
            at_id, at_day = rows[0].index('id'), rows[0].index('entry_day')
            row = list(next(r for r in rows[1:] if r[0] == 'OPEN'))
            row[at_day] = '2026-11-01'
            row[at_id] = row[at_id].rsplit('|', 1)[0] + '|2026-11-01'
            rows.append(row)
            rechain(rows)
        self.mark('(g) a signal INVENTED and chained on at the end: an '
                  'alarm - the working-out does not give it',
                  lambda: tamper('invented', invent, 'does not give it'))

    # -- (h) catching up --
    def g_catchup(self):
        def same_rows():
            daily, _texts, _snaps = self.daily_runs()
            late = self.late_run()
            skip = ('written_utc', 'late_hours', 'chain')
            strip = lambda rows: sorted(
                tuple((k, v) for k, v in row.items() if k not in skip
                      and k not in ('entry_raw', 'entry_fill', 'stop',
                                    'target', 'coins', 'position_usd',
                                    'risk_usd', 'range', 'exit_raw',
                                    'exit_fill', 'result_usd', 'result_frac'))
                + tuple(round(float(row[k]), 9) if row[k] else None
                        for k in ('entry_fill', 'stop', 'target',
                                  'result_frac'))
                for row in rows)
            a, b = self.ledger(daily), self.ledger(late)
            return len(a) >= 13 and strip(a) == strip(b)
        self.mark('(h) FIVE MORNINGS WORKED IN ONE GO give the same rows as '
                  'five daily runs - every signal, entry, stop, target and '
                  'result', same_rows)

        def labels():
            daily, texts, _snaps = self.daily_runs()
            late = self.late_run()
            a = [r for r in self.ledger(daily) if r['kind'] == 'OPEN']
            b = [r for r in self.ledger(late) if r['kind'] == 'OPEN']
            report = self.pw.report(late)
            old = [r for r in b if r['entry_day'] < '2026-11-21']
            printed = self._cache.get('late_text', '')
            return (a and all(float(r['late_hours']) == 0.5 for r in a)
                    and printed.count('[LATE by ') == len(old)
                    and printed.count('[ON TIME]') == len(b) - len(old)
                    and all('LATE by' not in text for text in texts)
                    and old and all(close_to(
                        float(r['late_hours']),
                        (ms('2026-11-21') + 1_800_000 - ms(r['entry_day']))
                        / 3_600_000) for r in old)
                    and f'signals written LATE (worked out afterwards): '
                        f'{len(old)}' in report
                    and f'hours of the entry day opening): '
                        f'{len(b) - len(old)}' in report)
        self.mark('(h) and the late ones SAY SO: every daily row is 0.5 '
                  'hours after the open and on time; every row worked days '
                  'afterwards carries its hours and is counted LATE',
                  labels)
        def starts_at_the_start():
            _daily, _texts, snaps = self.daily_runs()
            table = list(csv.reader(
                snaps[0]['ledger.csv'].decode('utf-8').splitlines()))
            first = [dict(zip(table[0], row)) for row in table[1:]]
            directory, _text, _now = self.long_run()
            every = self.ledger(directory)
            trend = [r for r in first if r['rule'] == 'trend-only-1d-t100']
            return (first and all(r['kind'] == 'OPEN'
                                  and r['signal_day'] == '2026-11-16'
                                  and r['entry_day'] == '2026-11-17'
                                  for r in first)
                    and 10 <= len(trend) <= 13
                    and min(r['signal_day'] for r in every) == '2026-11-16')
        self.mark('(h) THE FIRST DAY ASKED IS 2026-11-16 AND NO DAY BEFORE '
                  'IT: the first morning writes only signals of that close, '
                  'entered on the 17th, and the 400 days of history behind '
                  'the start never produce a row', starts_at_the_start)
        self.mark('(h) 6h00m00s after the entry day opens is ON TIME; one '
                  'second more is LATE',
                  lambda: self.pw.on_time(self.pw.late_hours(
                      '2026-11-17', at('2026-11-17', 6, 0, 0)))
                  and not self.pw.on_time(self.pw.late_hours(
                      '2026-11-17', at('2026-11-17', 6, 0, 1)))
                  and self.pw.late_hours('2026-11-17',
                                         at('2026-11-18', 6, 0)) == 30.0)

    # -- (i) the store --
    def g_store(self):
        def only_ever_longer():
            _d, _t, snaps = self.daily_runs()
            names = {'candles.csv', 'opens.csv', 'funding.csv', 'mood.csv',
                     'ledger.csv'}
            return (set(snaps[0]) == names and all(
                later[name].startswith(earlier[name])
                and len(snaps[-1][name]) > len(snaps[0][name])
                for earlier, later in zip(snaps, snaps[1:])
                for name in names))
        self.mark('(i) across five mornings each of the five files only '
                  'ever gets LONGER: every earlier version is the beginning '
                  'of the next', only_ever_longer)

        good = [('2030-01-01', '10', '11', '9', '10.5'),
                ('2030-01-02', '10.5', '12', '10', '11')]

        def refuses(name, rows, words):
            directory = self.folder(name)
            store = self.pw.Store(directory)
            store.add_candles('BTC-USD', good, 'seen')
            before = file_bytes(directory)
            try:
                store.add_candles('BTC-USD', rows, 'seen')
            except ValueError as exc:
                return words in str(exc) and file_bytes(directory) == before
            return False
        self.mark('(i) a day MISSING is refused and nothing is written',
                  lambda: refuses('gap', [('2030-01-04', '11', '12', '10',
                                           '11')], 'a day missing or twice'))
        self.mark('(i) a day TWICE is refused',
                  lambda: refuses('twice', [
                      ('2030-01-03', '11', '12', '10', '11'),
                      ('2030-01-03', '11', '12', '10', '11')],
                      'a day missing or twice'))
        self.mark('(i) a price of zero is refused',
                  lambda: refuses('zero', [('2030-01-03', '11', '12', '0',
                                            '11')], 'not a positive number'))
        self.mark('(i) a high below its own close is refused',
                  lambda: refuses('high', [('2030-01-03', '11', '10.9', '10',
                                            '11')], 'a high below'))

        def finished_or_not():
            rows = [[ms('2030-01-01'), '1', '2', '1', '2'],
                    [ms('2030-01-02'), '2', '3', '2', '3']]
            done, ahead = self.pw.split_klines(rows, ms('2030-01-03'))
            part, coming = self.pw.split_klines(rows, ms('2030-01-03') - 1)
            return ([r[0] for r in done] == ['2030-01-01', '2030-01-02']
                    and ahead is None
                    and [r[0] for r in part] == ['2030-01-01']
                    and coming == ('2030-01-02', '2'))
        self.mark('(i) a day is FINISHED only when the whole of it is '
                  'behind us: at 00:00:00.000 it is, one millisecond '
                  'earlier it is the day in progress and only its opening '
                  'price is kept', finished_or_not)

        def midnight_only():
            try:
                self.pw.split_klines([[ms('2030-01-01') + 3_600_000, '1',
                                       '2', '1', '2']], ms('2030-01-05'))
            except ValueError as exc:
                return '00:00 UTC' in str(exc)
            return False
        self.mark('(i) a candle that does not open at 00:00 UTC is refused',
                  midnight_only)

        def revision():
            directory = self.folder('revised')
            first = at('2026-11-17')
            self.pw.run(now=first, sources=self.world.sources(first),
                        directory=directory)
            changed = self.world.copy()
            rows = changed.candles['BTC']
            spot = next(i for i, row in enumerate(rows)
                        if row[0] == ms('2026-11-15'))
            stamp, o, h, l, c = rows[spot]
            rows[spot] = (stamp, o, f'{float(h) * 1.2:.8f}', l,
                          f'{float(c) * 1.05:.8f}')
            line = next(x for x in file_bytes(directory)['candles.csv']
                        .split(b'\n') if x.startswith(b'BTC-USD,2026-11-15'))
            second = at('2026-11-18')
            text = self.pw.run(now=second, sources=changed.sources(second),
                               directory=directory)
            return (line in file_bytes(directory)['candles.csv'].split(b'\n')
                    and 'served differently' in text
                    and 'INTEGRITY ALARM' not in text)
        self.mark('(i) the source later serving a DIFFERENT figure for a '
                  'stored day changes nothing: the stored row stands, and '
                  'the report counts the difference', revision)

        def what_the_rules_are_handed():
            import numpy as np
            directory, _text, _now = self.long_run()
            store = self.pw.Store(directory)
            for coin in ('BTC', 'XRP', 'BCH'):
                mine = self.pw.frame_of(store, f'{coin}-USD')
                theirs = world_frame(self.world, coin).reindex(mine.index)
                if (len(mine) < 450 or list(mine.columns) != [
                        'open', 'high', 'low', 'close', 'funding', 'mood',
                        'mood_side']
                        or bool(mine.iloc[-300:].isna().any().any())
                        or not np.allclose(mine.values, theirs.values,
                                           rtol=1e-12, atol=0,
                                           equal_nan=True)):
                    return False
            return True
        self.mark('(i) WHAT THE RULES ARE HANDED is the made-up world and '
                  'nothing else: the stored candles with funding and mood '
                  'joined on equal a frame the gate builds itself, day for '
                  'day, for three coins', what_the_rules_are_handed)

        def changed_opening():
            directory = self.folder('opening')
            early = self.world.copy()
            for coin in COINS13:
                rows = early.candles[coin]
                spot = next(i for i, row in enumerate(rows)
                            if row[0] == ms('2026-11-17'))
                stamp, o, h, l, c = rows[spot]
                o = f'{float(o) * 1.01:.8f}'
                rows[spot] = (stamp, o, f'{max(float(h), float(o)):.8f}', l,
                              c)
            first = at('2026-11-17')
            self.pw.run(now=first, sources=early.sources(first),
                        directory=directory)
            written = [r for r in self.ledger(directory)
                       if r['kind'] == 'OPEN']
            second = at('2026-11-18')
            text = self.pw.run(now=second,
                               sources=self.world.sources(second),
                               directory=directory)
            true_open = {coin: float(next(
                row[1] for row in self.world.candles[coin]
                if row[0] == ms('2026-11-17'))) for coin in COINS13}
            after = [r for r in self.ledger(directory) if r['kind'] == 'OPEN'
                     and r['entry_day'] == '2026-11-17']
            return (written and 'INTEGRITY ALARM' not in text
                    and 'served differently' in text
                    and len(after) == len(written)
                    and all(close_to(float(r['entry_raw']), 1.01 * true_open[
                        r['asset'].split('-')[0]], 1e-7) for r in after))
        self.mark('(i) an OPENING PRICE the source changes after a signal '
                  'was written from it: the written entry stands, the next '
                  'run raises no alarm, and the difference is counted',
                  changed_opening)

        def damaged():
            directory, now = self.copy_long('damaged')
            path = os.path.join(directory, 'candles.csv')
            rows = read_csv(path)
            del rows[200]
            write_csv(path, rows)
            before = file_bytes(directory)
            text = self.rerun(directory, now)
            return (text.startswith('PAPER-WATCH OFFLINE')
                    and 'a day missing or twice' in text
                    and file_bytes(directory) == before)
        self.mark('(i) a store with a day cut out of it by hand: the run '
                  'says OFFLINE by name, writes nothing, and does not '
                  'raise', damaged)

    # -- (j) the fetch --
    def g_fetch(self):
        def one_coin_down():
            directory = self.folder('xrp_down')
            now = at('2026-11-17')
            text = self.pw.run(now=now, sources=self.world.sources(
                now, broken=('XRP',)), directory=directory)
            rows = self.ledger(directory)
            return ('XRP: candles not updated (ConnectionError' in text
                    and 'XRP: WAITING' in text
                    and len({r['asset'] for r in rows}) == 12
                    and not any(r['asset'] == 'XRP-USD' for r in rows))
        self.mark('(j) ONE COIN\'s source down: it is named and WAITING, '
                  'and the other twelve are worked as usual', one_coin_down)

        def everything_down():
            directory = self.folder('all_down')
            now = at('2026-11-17')
            text = self.pw.run(now=now, sources=self.world.sources(
                now, all_broken=True), directory=directory)
            return (text.count('candles not updated') == 13
                    and 'mood not updated' in text
                    and 'NO MONEY' in text and not self.ledger(directory))
        self.mark('(j) EVERY source down: thirteen named lines, no ledger, '
                  'nothing raised', everything_down)

        def carried(missing, last_day, flags):
            directory = self.folder(f'mood_{len(missing)}_missing')
            world = self.world.copy()
            for text_day in missing:
                del world.mood[ms(text_day)]
            now = at('2026-11-17')
            self.pw.run(now=now, sources=world.sources(now),
                        directory=directory)
            store = self.pw.Store(directory)
            got = {d: (v, c) for d, v, _l, c in store.mood}
            before = self.world.mood[ms(missing[0]) - DAY][0]
            return (store.mood[-1][0] == last_day and all(
                got.get(d) == (before, 1) for d in flags))
        self.mark('(j) the mood not published for a day is CARRIED from the '
                  'day before and marked',
                  lambda: carried(['2026-11-10'], '2026-11-16',
                                  ['2026-11-10']))
        self.mark('(j) but not for ever: after three carried days the mood '
                  'store WAITS',
                  lambda: carried(['2026-11-10', '2026-11-11', '2026-11-12',
                                   '2026-11-13'], '2026-11-12',
                                  ['2026-11-10', '2026-11-11', '2026-11-12']))

        def empty_reading():
            directory = self.folder('two_settlements')
            world = self.world.copy()
            world.funding['BTC'] = [row for row in world.funding['BTC']
                                    if row[0] != ms('2026-11-12') + DAY // 3]
            now = at('2026-11-17')
            text = self.pw.run(now=now, sources=world.sources(now),
                               directory=directory)
            return ('BTC: 1 of the last 91 days have no funding reading'
                    in text and 'ETH: 1 of the last' not in text)
        self.mark('(j) a day with only two funding settlements is an EMPTY '
                  'reading, and the report says which coin and how many',
                  empty_reading)

    # -- (k) the report --
    def report_line(self, text, name):
        line = next(x for x in text.split('\n')
                    if x.strip().startswith(name))
        return line[len(name) + 2:].replace(',', '').replace('%', '').split()

    def g_report(self):
        def figures(rule, exit_kind, words, coins, label):
            directory, text, _now = self.long_run()
            rows = self.ledger(directory)
            want = gate_score(rows, rule, exit_kind, coins)
            got = self.report_line(text.split('THE PORTFOLIO LINE')[0],
                                   f'{words} / {label}')
            pf = '-' if want['pf'] is None else f"{want['pf']:.2f}"
            return (want['trades'] >= 10
                    and [int(got[0]), int(got[1]), int(got[2])]
                    == [want['trades'], want['days'], want['won']]
                    and got[3] == pf
                    and abs(float(got[4]) - want['money']) < 0.006
                    and abs(float(got[5]) - want['dip']) < 0.051)
        self.mark('(k) the combined rule, fixed exit, 13 coins: trades, '
                  'DIFFERENT ENTRY DAYS, wins, Profit Factor, the money and '
                  'the worst dip on the report are what the gate works from '
                  'the ledger',
                  lambda: figures('confluence-1d-t100', 'fixed',
                                  'combined rule / fixed exit', COINS13,
                                  '13 coins'))
        self.mark('(k) the trend alone, TRAILING exit, 13 coins: the same',
                  lambda: figures('trend-only-1d-t100', 'trail',
                                  'trend alone / trailing exit', COINS13,
                                  '13 coins'))
        self.mark('(k) the ORIGINAL THREE are shown apart and are the three',
                  lambda: figures('trend-only-1d-t100', 'fixed',
                                  'trend alone / fixed exit', THREE,
                                  'original 3'))

        def days_are_fewer():
            directory, _text, _now = self.long_run()
            s = gate_score(self.ledger(directory), 'trend-only-1d-t100',
                           'fixed', COINS13)
            return s['days'] < s['trades']
        self.mark('(k) and the day count earns its place: in this made-up '
                  'world the trend rule\'s trades fall on fewer days than '
                  'there are trades', days_are_fewer)

        def portfolio_line():
            directory, text, _now = self.long_run()
            rows = self.ledger(directory)
            got = self.report_line(text.split('THE PORTFOLIO LINE')[1],
                                   'trend alone / trailing exit / 13 coins')
            opens = [r for r in rows if r['kind'] == 'OPEN'
                     and r['rule'] == 'trend-only-1d-t100']
            return (sum(int(x) for x in got[1:4]) == len(opens)
                    and int(got[3]) > 0 and float(got[0]) > 0)
        self.mark('(k) the portfolio line accounts for every signal - full, '
                  'reduced or not taken - and the trend rule\'s piled-up '
                  'trailing trades are mostly NOT TAKEN, as the bar said',
                  portfolio_line)

        def portfolio_three():
            directory, text, _now = self.long_run()
            rows = self.ledger(directory)
            part = text.split('THE PORTFOLIO LINE')[1]
            three = self.report_line(part,
                                     'combined rule / fixed exit / original 3')
            all_ = self.report_line(part,
                                    'combined rule / fixed exit / 13 coins')
            mine = [r for r in rows if r['kind'] == 'OPEN'
                    and r['rule'] == 'confluence-1d-t100']
            small = [r for r in mine if r['asset'] in
                     ('BTC-USD', 'ETH-USD', 'SOL-USD')]
            return (0 < len(small) < len(mine)
                    and sum(int(x) for x in three[1:4]) == len(small)
                    and sum(int(x) for x in all_[1:4]) == len(mine))
        self.mark('(k) the portfolio line of the ORIGINAL THREE counts the '
                  'signals of those three coins and no others',
                  portfolio_three)

        def says_no_money():
            directory, text, _now = self.long_run()
            words = 'PAPER ONLY. NO MONEY. NO ORDER IS EVER SENT.'
            return all(words in t for t in (text, self.pw.report(directory),
                                            self.pw.week(directory)))
        self.mark('(k) the run, the report and the week all say PAPER ONLY. '
                  'NO MONEY. NO ORDER IS EVER SENT.', says_no_money)

        def report_reads_only():
            directory, now = self.copy_long('readonly')
            before = file_bytes(directory)
            real = self.pw.real_sources

            def forbidden():
                raise AssertionError('the report went to the network')
            self.pw.real_sources = forbidden
            try:
                a, b = self.pw.report(directory), self.pw.week(directory)
            finally:
                self.pw.real_sources = real
            return (file_bytes(directory) == before and 'OFFLINE' not in a
                    and 'OFFLINE' not in b and 'THE RECORD' in a)
        self.mark('(k) `--report` and `--week` write nothing and ask no '
                  'source for anything', report_reads_only)

        def open_now():
            directory, text, _now = self.long_run()
            rows = self.ledger(directory)
            closed = {r['id'] for r in rows if r['kind'] == 'CLOSE'}
            waiting = sum(1 for r in rows if r['kind'] == 'OPEN'
                          and not (f"{r['id']}|fixed" in closed
                                   and f"{r['id']}|trail" in closed))
            return f'OPEN NOW - {waiting} trade(s)' in text and waiting > 0
        self.mark('(k) OPEN NOW counts every signal with an ending still to '
                  'come', open_now)

    # -- (l) the week --
    def g_week(self):
        def counts():
            directory, _text, _now = self.long_run()
            rows = self.ledger(directory)
            text = self.pw.week(directory)
            first, last = '2027-01-18', '2027-01-24'
            opened = sum(1 for r in rows if r['kind'] == 'OPEN'
                         and first <= r['entry_day'] <= last)
            ended = [r for r in rows if r['kind'] == 'CLOSE'
                     and first <= r['exit_day'] <= last]
            mine = [r for r in ended if r['rule'] == 'trend-only-1d-t100'
                    and r['exit_kind'] == 'fixed']
            total = sum(float(r['result_usd']) for r in mine)
            won = sum(1 for r in mine if float(r['result_usd']) > 0)
            return (f'THE WEEK {first} to {last}' in text
                    and f'SIGNALS THIS WEEK - {opened}' in text
                    and f'ENDINGS THIS WEEK - {len(ended)}' in text
                    and len(ended) > 0
                    and f'trend alone   / fixed exit     {len(mine):3d} '
                        f'ended, {won:3d} won, {total:+9.2f} dollars' in text)
        self.mark('(l) THE WEEK is the seven finished days to the last one '
                  'stored, and its signals, endings, wins and dollars are '
                  'what the gate counts in the ledger', counts)

        def two_exits():
            directory, _text, _now = self.long_run()
            rows = self.ledger(directory)
            text = self.pw.week(directory)
            closes = {r['id']: r for r in rows if r['kind'] == 'CLOSE'}
            pairs = [(closes[f"{r['id']}|fixed"], closes[f"{r['id']}|trail"])
                     for r in rows if r['kind'] == 'OPEN'
                     and r['rule'] == 'confluence-1d-t100'
                     and f"{r['id']}|fixed" in closes
                     and f"{r['id']}|trail" in closes]
            fixed = sum(float(a['result_usd']) for a, _b in pairs)
            trail = sum(float(b['result_usd']) for _a, b in pairs)
            better = sum(float(b['result_usd']) > float(a['result_usd'])
                         for a, b in pairs)
            return (len(pairs) >= 5 and
                    f'combined rule  {len(pairs):3d} trades: fixed '
                    f'{fixed:+9.2f}, trailing {trail:+9.2f} dollars; '
                    f'trailing did better on {better},' in text)
        self.mark('(l) THE TWO EXITS ON THE SAME TRADES: only trades both of '
                  'whose endings have happened, and the two totals are what '
                  'the gate adds up', two_exits)

    # -- (o) two records, two doors, each checking the other --
    def g_two(self):
        pw = self.pw
        self.mark('(o) THE TWO DOORS ARE THE TWO TYPED HERE, each with its '
                  'own record: the laptop\'s folder `paper` asks '
                  'fapi.binance.com, the cloud\'s folder `paper_cloud` asks '
                  'www.binance.com - and neither is crossed',
                  lambda: pw.FUNDING_DOORS == {
                      'laptop': 'https://fapi.binance.com/fapi/v1/fundingRate',
                      'cloud': 'https://www.binance.com/fapi/v1/fundingRate'}
                  and {k: os.path.basename(v) for k, v in pw.RECORDS.items()}
                  == {'laptop': 'paper', 'cloud': 'paper_cloud'}
                  and pw.real_sources('laptop')['funding'].url
                  == 'https://fapi.binance.com/fapi/v1/fundingRate'
                  and pw.real_sources('cloud')['funding'].url
                  == 'https://www.binance.com/fapi/v1/fundingRate'
                  and pw.real_sources('cloud')['candles']
                  is pw.real_sources('laptop')['candles'])

        def dated(rows, upto):
            return [r for r in rows if (r['entry_day'] if r['kind'] == 'OPEN'
                                        else r['exit_day']) <= upto]

        def agree():
            daily, _t, _s = self.daily_runs()
            lines = pw.compare(daily, self.late_run(), 'laptop', 'cloud')
            count = len(dated(self.ledger(daily), '2026-11-20'))
            return (count >= 13 and len(lines) == 1 and lines[0] == (
                f"  THE TWO RECORDS AGREE: all {count} rows dated up to "
                f"2026-11-20 are the same in the laptop's record and the "
                f"cloud's"))
        self.mark('(o) TWO RECORDS MADE DIFFERENT WAYS AGREE: five daily '
                  'runs against one late run - it says AGREE, up to the '
                  'last day both hold, and counts the rows', agree)

        def broken_copy(name, change):
            daily, _t, _s = self.daily_runs()
            target = os.path.join(self.tmp, name)
            shutil.copytree(self.late_run(), target)
            path = os.path.join(target, 'ledger.csv')
            rows = read_csv(path)
            touched = change(rows)
            write_csv(path, rows)
            return daily, target, touched

        def one_figure():
            def change(rows):
                at_ = rows[0].index('stop')
                row = next(r for r in rows[1:] if r[0] == 'OPEN')
                row[at_] = repr(float(row[at_]) * 1.001)
                return row[1]
            daily, target, touched = broken_copy('two_figure', change)
            lines = pw.compare(daily, target, 'laptop', 'cloud')
            text = '\n'.join(lines)
            return ('THE TWO RECORDS DISAGREE up to 2026-11-20: 1 row(s) '
                    'differ, 0 only in' in text
                    and f'differs: {touched}' in text
                    and pw.verdict_code(text) == 1)
        self.mark('(o) ONE FIGURE changed in one of them (a stop moved by a '
                  'tenth of a percent): it says DISAGREE and names the row',
                  one_figure)

        def one_missing():
            def change(rows):
                spot = next(i for i, r in enumerate(rows) if r[0] == 'OPEN')
                return rows.pop(spot)[1]
            daily, target, gone = broken_copy('two_missing', change)
            text = '\n'.join(pw.compare(daily, target, 'laptop', 'cloud'))
            return ("0 row(s) differ, 1 only in the laptop's, 0 only in "
                    "the cloud's" in text
                    and f"only in the laptop's: {gone}" in text)
        self.mark('(o) A ROW IN ONE AND NOT THE OTHER, inside the days both '
                  'hold: DISAGREE, and it says which record has it',
                  one_missing)

        def one_ahead():
            _d, _t, snaps = self.daily_runs()
            early = self.folder('two_early')
            for name, data in snaps[2].items():
                with open(os.path.join(early, name), 'wb') as handle:
                    handle.write(data)
            lines = pw.compare(early, self.late_run(), 'laptop', 'cloud')
            count = len(dated(self.ledger(early), '2026-11-18'))
            later = len(self.ledger(self.late_run())) > len(
                self.ledger(early))
            return (later and 0 < count < len(self.ledger(early))
                    and lines == [
                        f"  THE TWO RECORDS AGREE: all {count} rows dated "
                        f"up to 2026-11-18 are the same in the laptop's "
                        f"record and the cloud's"])
        self.mark('(o) ONE RECORD AHEAD OF THE OTHER is not a disagreement: '
                  'only the days BOTH hold are compared, and the newer '
                  'rows of either are left alone', one_ahead)

        def not_there():
            daily, _t, _s = self.daily_runs()
            missing = pw.compare(daily, os.path.join(self.tmp, 'no_such'),
                                 'laptop', 'cloud')
            empty = pw.compare(daily, self.folder('two_empty'), 'laptop',
                               'cloud')
            return (missing == ["  the cloud's record does not exist yet - "
                                "nothing to compare"]
                    and empty == ["  the cloud's record holds no finished "
                                  "day yet - nothing to compare"]
                    and pw.verdict_code('\n'.join(missing + empty)) == 0)
        self.mark('(o) THE OTHER RECORD NOT THERE YET, or there and empty: '
                  'said in one line, and not an alarm', not_there)

        def which_record():
            daily, _t, _s = self.daily_runs()
            late = self.late_run()
            mine = pw.report(directory=daily, record='laptop', other=late)
            theirs = pw.week(directory=late, record='cloud', other=daily)
            return ("THIS IS THE LAPTOP's RECORD (journal/paper/)" in mine
                    and "THIS IS THE CLOUD's RECORD (journal/paper_cloud/)"
                    in theirs
                    and "are the same in the laptop's record and the "
                        "cloud's" in mine
                    and "are the same in the cloud's record and the "
                        "laptop's" in theirs
                    and pw.verdict_code(mine) == 0
                    and pw.verdict_code(theirs) == 0
                    and pw.verdict_code('x INTEGRITY ALARM x') == 1
                    and pw.verdict_code('PAPER-WATCH OFFLINE - y') == 1
                    and pw.verdict_code('THE TWO RECORDS DISAGREE') == 1
                    and "RECORD (journal" not in pw.report(directory=daily))
        self.mark('(o) THE REPORT SAYS WHICH RECORD IT IS and carries the '
                  'comparison; and a run ends 1 on ALARM, OFFLINE or '
                  'DISAGREE and 0 otherwise', which_record)

    GROUPS = ('const', 'engine', 'signals', 'hand', 'twins', 'portfolio',
              'ledger', 'catchup', 'store', 'fetch', 'report', 'week', 'two')

    def run(self, groups=None):
        for name in (self.GROUPS if groups is None else groups):
            before = len(self.results)
            try:
                getattr(self, 'g_' + name)()
            except Exception as exc:
                self.names.append(f'({name}) the group finished')
                self.results.append((False, f'({name}) THE GROUP COULD NOT '
                                     f'FINISH [{type(exc).__name__}: '
                                     f'{str(exc)[:120]}] after '
                                     f'{len(self.results) - before} checks'))
        return self.results


# ---- THE DRILL — real text edits to a copy of the file on trial -----------
# (what is broken, the text as it stands, the text put in its place, the
#  groups that must go red)
SABOTAGES = [
    ('the entry made BETTER by the slippage instead of worse',
     "fill = raw * (1 + SLIP) if direction == 'long' else raw * (1 - SLIP)",
     "fill = raw * (1 - SLIP) if direction == 'long' else raw * (1 + SLIP)",
     ('engine', 'hand')),
    ('the range allowed to see the entry day',
     "days[i], raw, df.iloc[:i])", "days[i], raw, df.iloc[:i + 1])",
     ('engine',)),
    ('THE RULE HANDED TOMORROW (the leak)',
     "answer = rule(df.iloc[:i + 1].copy())",
     "answer = rule(df.iloc[:i + 2].copy())", ('signals', 'engine')),
    ('the rule asked while a trade is still open',
     "                if position is None:\n                    answer = rule",
     "                if True:\n                    answer = rule",
     ('signals', 'engine')),
    ('the fee charged on one side only',
     "fees = FEE * (coins * entry_fill + coins * exit_fill)",
     "fees = FEE * (coins * entry_fill)", ('engine', 'hand')),
    ('the fee switched off', "FEE = 0.0005 ", "FEE = 0.0 ",
     ('const', 'engine')),
    ('stop and target in one day counted as the WIN',
     "                    if hit_stop:\n",
     "                    if hit_stop and not hit_target:\n", ('hand',)),
    ('a fixed stop that needs to be passed, not touched',
     "hit_stop = l[i] <= stop if long else h[i] >= stop",
     "hit_stop = l[i] < stop if long else h[i] > stop", ('hand',)),
    ('a gap through the fixed stop filled at the stop',
     "raw = (min(float(o[i]), stop) if long\n"
     "                               else max(float(o[i]), stop))",
     "raw = (stop if long\n                               else stop)",
     ('hand',)),
    ('THE LONG TRAILING STOP ALLOWED TO SIT BEHIND THE FIRST STOP',
     "trade['trail_stop'] = max(stop, best - reach)",
     "trade['trail_stop'] = best - reach", ('hand',)),
    ('THE SHORT TRAILING STOP ALLOWED TO SIT BEHIND THE FIRST STOP',
     "trade['trail_stop'] = min(stop, best + reach)",
     "trade['trail_stop'] = best + reach", ('hand',)),
    ('the trailing stop following the HIGH instead of the close',
     "else max(trade['best'], float(c[i])))",
     "else max(trade['best'], float(h[i])))", ('hand',)),
    ('a trailing stop that needs to be passed, not touched',
     "if (l[i] <= stop) if long else (h[i] >= stop):",
     "if (l[i] < stop) if long else (h[i] > stop):", ('hand',)),
    ('a gap through the trailing stop filled at the stop',
     "left_at = (min(float(o[i]), stop) if long\n"
     "                                   else max(float(o[i]), stop))",
     "left_at = (stop if long\n                                   else stop)",
     ('hand',)),
    ('the trailing reach halved', "TRAIL_ATR = 3.0 ", "TRAIL_ATR = 1.5 ",
     ('const', 'hand')),
    ('A LEDGER ROW THAT DIFFERS FROM THE WORKING-OUT LET THROUGH',
     "        if wrong:\n", "        if wrong and False:\n", ('ledger',)),
    ('a ledger row the working-out does not give let through',
     "        if twin is None:\n", "        if twin is None and False:\n",
     ('ledger',)),
    ('the chain never checked',
     "if row['chain'] != chain_of(previous, row):",
     "if False and row['chain'] != chain_of(previous, row):", ('ledger',)),
    ('a missing day let into the store',
     "            if day != expected:\n", "            if False:\n",
     ('store',)),
    ('TODAY\'s UNFINISHED CANDLE STORED AS FINISHED',
     "if opened + DAY_MS <= now_ms:", "if opened <= now_ms:", ('store',)),
    ('every signal taken in full whatever the limit',
     "each = min(RISK, room / len(fresh)) if room > 0 else Fraction(0)",
     "each = RISK", ('portfolio',)),
    ('a late row printed as on time',
     "when = ('ON TIME' if on_time(row['late_hours'])",
     "when = ('ON TIME' if True", ('catchup',)),
    ('the count of different days replaced by the count of trades',
     "'days': len({row['entry_day'] for row in trades}),",
     "'days': len(trades),", ('report',)),
    ('the mood carried for a month', "MAX_CARRIED_RUN = 3 ",
     "MAX_CARRIED_RUN = 30 ", ('const', 'fetch')),
    ('THE CLOUD SENT TO THE DOOR THAT REFUSES IT (the doors crossed)',
     "    'cloud': 'https://www.binance.com/fapi/v1/fundingRate',",
     "    'cloud': 'https://fapi.binance.com/fapi/v1/fundingRate',",
     ('two',)),
    ('A COMPARISON THAT ALWAYS SAYS "AGREE"',
     "    if differ or only_mine or only_other:\n", "    if False:\n",
     ('two',)),
    ('the comparison reaching past the days both records hold',
     "upto = min(newest_day(mine), newest_day(other))",
     "upto = max(newest_day(mine), newest_day(other))", ('two',)),
]


def drill(world, results, green):
    """`green` is the set of checks that were GREEN on the untouched file.
    A break is CAUGHT only if it turns one of THOSE red: a check that was
    already red proves nothing about the break (rule (p))."""
    with open(SOURCE, encoding='utf-8', newline='') as handle:
        original = handle.read()
    text = original.replace('\r\n', '\n')
    stamp = hashlib.sha256(original.encode('utf-8')).hexdigest()
    folder = tempfile.mkdtemp(prefix='zarx_paper_drill_')
    try:
        for number, (what, old, new, groups) in enumerate(SABOTAGES, 1):
            line = f'(m) DRILL {number:2d}: {what}'
            if text.count(old) != 1 or old == new:
                results.append((False, f'{line} -> INERT: the text to break '
                                f'is there {text.count(old)} times, not once '
                                f'(INERT IS A FAIL)'))
                continue
            path = os.path.join(folder, f'broken_{number}.py')
            with open(path, 'w', encoding='utf-8', newline='\n') as handle:
                handle.write(text.replace(old, new))
            try:
                broken = load(path, f'paper_watch_broken_{number}')
            except Exception as exc:
                results.append((False, f'{line} -> THE BROKEN COPY DOES NOT '
                                f'LOAD ({type(exc).__name__}): nothing proved'))
                continue
            suite = Suite(broken, world)
            try:
                outcome = suite.run(groups)
            finally:
                suite.done()
            red = [name for name, (good, _t) in zip(suite.names, outcome)
                   if not good and name in green]
            results.append((bool(red), f'{line} -> '
                            + (f'CAUGHT, {len(red)} of {len(outcome)} red '
                               f'in {"/".join(groups)}' if red else
                               f'ESCAPED: of {len(outcome)} checks in '
                               f'{"/".join(groups)} not one that was green '
                               f'on the untouched file went red')))
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    with open(SOURCE, encoding='utf-8', newline='') as handle:
        after = hashlib.sha256(handle.read().encode('utf-8')).hexdigest()
    results.append((after == stamp and len(SABOTAGES) == DRILL_OWED,
                    f'(m) the file on trial is byte for byte what it was '
                    f'before the drill, and the drill made its '
                    f'{DRILL_OWED} breaks'))


def main():
    print('=' * 78)
    print('GATE 7.1 — journal/paper_watch.py, THE PAPER-WATCH')
    print('made-up data, temporary folders, no network; journal/paper/ is '
          'not touched')
    print('=' * 78)
    paper = os.path.join(JOURNAL_DIR, 'paper')
    real_before = file_bytes(paper) if os.path.isdir(paper) else None
    world = World()
    pw = load(SOURCE, 'paper_watch_on_trial')
    suite = Suite(pw, world)
    try:
        results = suite.run()
    finally:
        suite.done()
    green = {name for name, (good, _t) in zip(suite.names, results) if good}
    drill(world, results, green)
    real_after = file_bytes(paper) if os.path.isdir(paper) else None
    results.append((real_before == real_after,
                    '(n) journal/paper/, the real record, is byte for byte '
                    'what it was before this gate ran'))
    results.append((len(results) + 1 == OWED
                    and len(set(suite.names)) == len(suite.names),
                    f'(n) the gate ran the {OWED} checks it owes '
                    f'(it ran {len(results) + 1}), and no two of them '
                    f'carry the same words'))
    for good, text in results:
        print(f"   {'✓' if good else '✗'} {text}")
    reds = sum(1 for good, _t in results if not good)
    print('=' * 78)
    if reds == 0:
        print(f'GATE 7.1 PASSED — {len(results)} checks, 0 red.')
        return 0
    print(f'GATE 7.1 FAILED — {reds} red of {len(results)} checks.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
