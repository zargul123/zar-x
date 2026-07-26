"""
Zar X Lab — Step 2.3: THE HONEST BACKTEST ENGINE (the heart).

WHY THIS EXISTS
Every backtest ever published was profitable — that is why backtests are
worthless unless the machine that produced them is built to make lying
impossible. This engine's whole purpose is to be UNABLE to flatter a
strategy. Everything below is a wall against a specific known lie:

  THE LIE                        THE WALL
  "it saw the future"            the strategy is handed df.iloc[:i+1] as its
                                 OWN COPY. Candle i+1 does not exist in the
                                 object it receives. It cannot peek because
                                 there is nothing there to peek at.
  "it bought at the exact top/   entries happen at the NEXT candle's OPEN
   bottom of the signal candle"  after a signal. No same-candle magic.
  "the winner counts when both   if the stop AND the target are touched inside
   were touched"                 one candle, the LOSS is counted. Always.
  "costs are a detail"           fee + slippage on BOTH sides of every trade,
                                 taken from config.LAB_COSTS. Never zero.
  "I tuned it, then tested it    the stat card that COUNTS is computed only on
   on the same data"             candles after `train_end` (the hold-out).
  "the data was fine"            lab/validator.py runs on the file at load; a
                                 FAIL verdict refuses the backtest outright.
  "it used fresher data than     the ONLY way in is load_vault(), which reads
   the strategy would have"      lab/vault/ off the disk. This module never
                                 imports data/market_data.py — there is no
                                 code path from here to a live API.
  "which version produced this   every stat card and every result row is
   number?"                      stamped with strategy name + a fingerprint
                                 (hash of ALL its parameters, costs and risk
                                 settings included) + the git commit.

WHAT IT DOES NOT DO (stated so nobody assumes it)
  - It only asks the strategy for a signal when FLAT. A position is managed
    by the Discipline Engine (ATR stop / target), exactly like the live ship —
    a signal flip does not close a trade.
  - One position at a time, one asset at a time. No pyramiding, no hedging.
  - Position size risks 1% of the CURRENT equity (the live formula, from
    risk/calculator.py). Each trade also records its result as a percentage
    of the equity it started with, so any subset of trades (hold-out,
    walk-forward window, Monte Carlo reshuffle) can be compounded honestly
    without inheriting the balance from trades outside that subset.
  - The equity curve is the CLOSED-TRADE curve. Drawdown is measured on it.

THE CONTRACT — a strategy is any callable:
    signal(df) -> 'long' | 'short' | 'flat'
`df` is candles up to and including "now". Nothing else. Ever.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\gate_2_3.py
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime

import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(LAB_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, LAB_DIR)

from config import LAB_COSTS, RISK_CONFIG          # noqa: E402
from risk.calculator import RiskCalculator          # noqa: E402
from regime.vane import RegimeVane                  # noqa: E402
from validator import validate_csv                  # noqa: E402
# NOTE (structural): data/market_data.py is deliberately NOT imported here and
# must never be. The Lab tests on frozen evidence or it does not test.

VAULT_DIR = os.path.join(LAB_DIR, 'vault')
RESULTS_DIR = os.path.join(LAB_DIR, 'results')

INITIAL_CAPITAL = 10_000.0   # a nominal account; results are reported in %
ATR_PERIOD = 14              # same period the live risk instrument uses
REGIME_LOOKBACK = 300        # candles of history used for the regime reading

SIGNALS = ('long', 'short', 'flat')


# --------------------------------------------------------------------------
# Provenance: where the candles came from, and who wrote the code
# --------------------------------------------------------------------------

class VaultData:
    """Candles from the frozen vault, with their inspection verdict attached.

    The constructor refuses any path outside lab/vault/. This is the wall
    against live data: `run_backtest` accepts nothing else, so there is no
    way to point the Lab at a fresh API response by accident or in a hurry.
    """

    def __init__(self, path, timeframe=None):
        path = os.path.abspath(path)
        if os.path.commonpath([path, VAULT_DIR]) != VAULT_DIR:
            raise ValueError(
                f'REFUSED: {path} is not inside the frozen vault. The Lab '
                f'tests on frozen evidence only — never on live data.')
        if not os.path.exists(path):
            raise FileNotFoundError(f'No such vault file: {path}')

        stem = os.path.splitext(os.path.basename(path))[0]
        self.asset, tf_from_name = stem.rsplit('_', 1)
        self.timeframe = timeframe or tf_from_name
        self.path = path

        # THE DOOR: garbage in = lies out. Inspected on every single load.
        self.report = validate_csv(path, self.timeframe)
        self.verdict = self.report.verdict

        df = pd.read_csv(path, index_col=0, parse_dates=True)
        self.df = df.sort_index()

    @property
    def name(self):
        return f'{self.asset}_{self.timeframe}'

    def __repr__(self):
        return (f'<VaultData {self.name}: {len(self.df)} candles '
                f'{self.df.index[0]} -> {self.df.index[-1]}, '
                f'door verdict {self.verdict}>')


def load_vault(asset, timeframe):
    """The ONLY door into the Lab. Reads a frozen vault file, inspects it,
    and refuses it outright if the inspector says FAIL."""
    path = os.path.join(VAULT_DIR, f'{asset}_{timeframe}.csv')
    data = VaultData(path, timeframe)
    if data.verdict == 'FAIL':
        print(data.report.text())
        raise ValueError(
            f'REFUSED: {data.name} failed the data inspector. A backtest on '
            f'diseased candles is not a weak result, it is a lie. Fix the '
            f'data or drop the asset — do not lower the door.')
    return data


def git_commit():
    """Which version of the ship produced this number."""
    try:
        out = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                             cwd=ROOT_DIR, capture_output=True, text=True,
                             timeout=10)
        return out.stdout.strip() or 'unknown'
    except Exception:
        return 'unknown'


def fingerprint(strategy_name, params):
    """A short hash of EVERYTHING that could change the result. A survivor's
    record dies the moment its parameters change — this is how we can tell."""
    blob = json.dumps({'strategy': strategy_name, 'params': params},
                      sort_keys=True, default=str)
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()[:12]


# --------------------------------------------------------------------------
# The stat card
# --------------------------------------------------------------------------

def _max_drawdown(returns):
    """Worst peak-to-trough fall of the compounded closed-trade equity curve."""
    equity, peak, worst = 1.0, 1.0, 0.0
    for r in returns:
        equity *= (1.0 + r)
        peak = max(peak, equity)
        worst = max(worst, (peak - equity) / peak if peak > 0 else 0.0)
    return worst


class StatCard(dict):
    """The honest scoreboard for one window of trades."""

    def text(self):
        L = []
        L.append(f'  STAT CARD — {self["window"].upper()} '
                 f'({self["window_from"]} -> {self["window_to"]})')
        L.append(f'    strategy      : {self["strategy"]}  '
                 f'[fingerprint {self["fingerprint"]}  commit {self["commit"]}]')
        L.append(f'    market        : {self["asset"]} {self["timeframe"]}   '
                 f'candles in window: {self["candles"]:,}')
        L.append(f'    trades        : {self["trades"]}   '
                 f'({self["longs"]} long / {self["shorts"]} short)')
        if self['trades'] == 0:
            L.append('    net P&L       : 0.00%  (no trades were taken)')
            L.append(f'    time in market: {self["time_in_market"]:.1%}')
            return '\n'.join(L)
        L.append(f'    wins / losses : {self["wins"]} / {self["losses"]}   '
                 f'win rate {self["win_pct"]:.1f}%')
        L.append(f'    profit factor : {self["profit_factor"]:.2f}   '
                 f'(gross wins / gross losses, AFTER costs)')
        L.append(f'    avg win       : {self["avg_win"]:+.2f}% of equity')
        L.append(f'    avg loss      : {self["avg_loss"]:+.2f}% of equity   '
                 f'(win/loss size ratio {self["win_loss_ratio"]:.2f})')
        L.append(f'    max drawdown  : {self["max_drawdown"]:.2f}%')
        L.append(f'    NET RETURN    : {self["net_return"]:+.2f}%   '
                 f'(after every fee and every slippage)')
        L.append(f'    gross return  : {self["gross_return"]:+.2f}%   '
                 f'(the fantasy version, costs switched off)')
        L.append(f'    COST DRAG     : {self["cost_drag"]:.2f} percentage '
                 f'points   (${self["costs_paid"]:,.2f} paid in fees+slippage '
                 f'on ${self["capital"]:,.0f})')
        L.append(f'    time in market: {self["time_in_market"]:.1%}')
        L.append(f'    exits         : {self["exit_summary"]}')
        return '\n'.join(L)


# --------------------------------------------------------------------------
# The result of one run
# --------------------------------------------------------------------------

class BacktestResult:

    def __init__(self, trades, in_market, index, meta):
        self.trades = pd.DataFrame(trades)
        self.in_market = in_market          # per-candle: was a position open
        self.index = index                  # the full candle index walked
        self.meta = meta

    # -- windows -----------------------------------------------------------
    def _window_mask(self, window):
        te = self.meta['train_end']
        if window == 'full' or te is None:
            return pd.Series([True] * len(self.index), index=self.index)
        if window == 'holdout':
            return pd.Series(self.index > te, index=self.index)
        if window == 'train':
            return pd.Series(self.index <= te, index=self.index)
        raise ValueError(f'unknown window {window!r}')

    def window_trades(self, window='holdout'):
        """Trades belong to the window their ENTRY falls in."""
        if self.trades.empty:
            return self.trades
        te = self.meta['train_end']
        if window == 'full' or te is None:
            return self.trades
        if window == 'holdout':
            return self.trades[self.trades['entry_time'] > te]
        if window == 'train':
            return self.trades[self.trades['entry_time'] <= te]
        raise ValueError(f'unknown window {window!r}')

    def card(self, window='holdout'):
        mask = self._window_mask(window)
        candles = int(mask.sum())
        idx = self.index[mask.values]
        tr = self.window_trades(window)

        card = StatCard({
            'window': window,
            'window_from': str(idx[0]) if candles else '-',
            'window_to': str(idx[-1]) if candles else '-',
            'candles': candles,
            'trades': int(len(tr)),
            'longs': int((tr['direction'] == 'long').sum()) if len(tr) else 0,
            'shorts': int((tr['direction'] == 'short').sum()) if len(tr) else 0,
            'time_in_market': float(self.in_market[mask.values].mean()) if candles else 0.0,
        })
        card.update({k: self.meta[k] for k in
                     ('strategy', 'fingerprint', 'commit', 'asset',
                      'timeframe', 'capital', 'train_end')})

        if len(tr) == 0:
            card.update({'wins': 0, 'losses': 0, 'win_pct': 0.0,
                         'profit_factor': 0.0, 'avg_win': 0.0, 'avg_loss': 0.0,
                         'win_loss_ratio': 0.0, 'max_drawdown': 0.0,
                         'net_return': 0.0, 'gross_return': 0.0,
                         'cost_drag': 0.0, 'costs_paid': 0.0,
                         'net_pnl': 0.0, 'exit_summary': '-'})
            return card

        r = tr['return_pct'].values           # net, as a fraction of equity
        g = tr['gross_return_pct'].values     # the same trades with costs off
        wins, losses = r[r > 0], r[r <= 0]
        gross_win = float(wins.sum())
        gross_loss = float(-losses.sum())

        net_equity = float(pd.Series(1.0 + r).prod())
        gross_equity = float(pd.Series(1.0 + g).prod())

        card.update({
            'wins': int(len(wins)),
            'losses': int(len(losses)),
            'win_pct': 100.0 * len(wins) / len(r),
            'profit_factor': (gross_win / gross_loss) if gross_loss > 0
                             else float('inf'),
            'avg_win': 100.0 * float(wins.mean()) if len(wins) else 0.0,
            'avg_loss': 100.0 * float(losses.mean()) if len(losses) else 0.0,
            'win_loss_ratio': (abs(wins.mean() / losses.mean())
                               if len(wins) and len(losses) and losses.mean()
                               else 0.0),
            'max_drawdown': 100.0 * _max_drawdown(r),
            'net_return': 100.0 * (net_equity - 1.0),
            'gross_return': 100.0 * (gross_equity - 1.0),
            'cost_drag': 100.0 * (gross_equity - net_equity),
            'costs_paid': float(tr['costs_paid'].sum()),
            'net_pnl': float(tr['net_pnl'].sum()),
            'exit_summary': ', '.join(
                f'{k}={v}' for k, v in tr['exit_reason'].value_counts().items()),
        })
        return card

    # -- evidence ----------------------------------------------------------
    def save_csv(self, results_dir=RESULTS_DIR):
        """The per-trade X-ray. Every row carries its own provenance so a
        stray CSV can always be traced back to the code that made it."""
        os.makedirs(results_dir, exist_ok=True)
        run_date = self.meta['run_date']
        base = (f'{self.meta["strategy"]}_{self.meta["asset"]}_'
                f'{self.meta["timeframe"]}_{run_date}')
        path = os.path.join(results_dir, base + '.csv')
        n = 2
        while os.path.exists(path):   # evidence is never overwritten
            path = os.path.join(results_dir, f'{base}-{n}.csv')
            n += 1

        out = self.trades.copy()
        if out.empty:   # an empty result is still evidence
            out = pd.DataFrame(columns=TRADE_COLUMNS)
        out.insert(0, 'strategy', self.meta['strategy'])
        out.insert(1, 'fingerprint', self.meta['fingerprint'])
        out.insert(2, 'commit', self.meta['commit'])
        out.insert(3, 'asset', self.meta['asset'])
        out.insert(4, 'timeframe', self.meta['timeframe'])
        out.insert(5, 'train_end', str(self.meta['train_end']))
        out.insert(6, 'run_date', run_date)
        out.to_csv(path, index=False)
        return path

    def print_report(self, windows=('full', 'holdout')):
        m = self.meta
        print('-' * 70)
        print(f'RUN: {m["strategy"]}  on {m["asset"]} {m["timeframe"]}  '
              f'[{m["fingerprint"]} @ {m["commit"]}]')
        print(f'  data      : {os.path.basename(m["source"])}  '
              f'({m["candles_total"]:,} candles, door verdict {m["verdict"]})')
        print(f'  costs     : fee {m["costs"]["fee_pct"]:.3%} per side + '
              f'slippage {m["costs"]["slippage_pct"]:.3%} per side')
        print(f'  risk      : {m["risk_pct"]:.1%} of equity per trade, '
              f'stop {m["sl_atr_mult"]} ATR / target {m["tp_atr_mult"]} ATR')
        print(f'  train_end : {m["train_end"]}  '
              f'(everything after this date is the HOLD-OUT)')
        print(f'  look-ahead audit: {m["audit_calls"]:,} strategy calls, '
              f'{m["audit_violations"]} violations '
              f'(a violation = the strategy was handed a candle at or beyond '
              f'"now")')
        for w in windows:
            print()
            print(self.card(w).text())
        print('-' * 70)


TRADE_COLUMNS = [
    'trade_no', 'window', 'direction', 'entry_time', 'entry_price_raw',
    'entry_price_fill', 'exit_time', 'exit_price_raw', 'exit_price_fill',
    'exit_reason', 'bars_held', 'atr_at_entry', 'stop_loss', 'take_profit',
    'size_units', 'position_value', 'equity_at_entry', 'gross_pnl',
    'fees_paid', 'slippage_paid', 'costs_paid', 'net_pnl', 'return_pct',
    'gross_return_pct', 'equity_after', 'regime_at_entry', 'regime_adx',
    'regime_entropy',
]


# --------------------------------------------------------------------------
# The walk
# --------------------------------------------------------------------------

def _regime_at_entry(vane, past, timeframe):
    """The weather at the moment of entry, computed ONLY from candles the
    market had already closed. `past` never contains the entry candle."""
    if len(past) < REGIME_LOOKBACK // 4:
        return {'regime': 'Unavailable', 'adx': None, 'entropy': None}
    try:
        from indicators.technical import add_indicators
        window = past.iloc[-REGIME_LOOKBACK:]
        return vane.read(add_indicators(window), timeframe)
    except Exception as e:
        return {'regime': f'Offline({e.__class__.__name__})',
                'adx': None, 'entropy': None}


def run_backtest(data, signal, strategy_name, params=None, train_end=None,
                 capital=INITIAL_CAPITAL, costs=None, risk_pct=None,
                 sl_atr_mult=None, tp_atr_mult=None, atr_period=ATR_PERIOD,
                 regime=True, verbose=True):
    """
    Walk the candles once, in order, and let the strategy trade.

    data          : a VaultData from load_vault() — nothing else is accepted
    signal        : callable(df) -> 'long' | 'short' | 'flat'
    strategy_name : the name that goes on the stat card and the CSV
    params        : the strategy's parameters (they go into the fingerprint)
    train_end     : the hold-out line. Trades entered AFTER it are the ones
                    that count. Parameters may only be chosen by looking
                    before it.
    """
    if not isinstance(data, VaultData):
        raise TypeError(
            'run_backtest only accepts VaultData from load_vault(). The Lab '
            'does not test on live or hand-made data — that is the whole '
            'point of the frozen vault.')
    if data.verdict == 'FAIL':
        raise ValueError(f'REFUSED: {data.name} failed the data inspector.')

    costs = dict(costs or LAB_COSTS)
    fee = float(costs['fee_pct'])
    slip = float(costs['slippage_pct'])
    if fee < 0 or slip < 0:
        raise ValueError('costs cannot be negative')
    risk_pct = RISK_CONFIG['risk_per_trade'] if risk_pct is None else risk_pct
    sl_mult = RISK_CONFIG['default_sl_atr'] if sl_atr_mult is None else sl_atr_mult
    tp_mult = RISK_CONFIG['default_tp_atr'] if tp_atr_mult is None else tp_atr_mult
    train_end = pd.Timestamp(train_end) if train_end is not None else None

    df = data.df
    n = len(df)
    times = df.index
    o = df['open'].values
    h = df['high'].values
    l = df['low'].values
    c = df['close'].values

    calc = RiskCalculator()
    vane = RegimeVane() if regime else None

    trades = []
    in_market = pd.Series(False, index=times).values
    equity = float(capital)
    pos = None          # the open position, or None
    pending = None      # a signal waiting for the next candle's open
    audit_calls = 0
    audit_violations = 0

    for i in range(n):

        # --- 1. ENTRY: act on the PREVIOUS candle's signal, at THIS open ---
        if pos is None and pending is not None:
            past = df.iloc[:i]      # everything known when this candle opens
            atr = calc.atr(past, atr_period)
            if atr and atr > 0:
                raw = float(o[i])
                # slippage: the fill is always worse than the printed price
                fill = raw * (1 + slip) if pending == 'long' else raw * (1 - slip)
                plan = calc.plan_trade(capital=equity, entry_price=fill,
                                       direction=pending, atr=atr,
                                       risk_pct=risk_pct, sl_atr_mult=sl_mult,
                                       tp_atr_mult=tp_mult)
                if plan:
                    weather = (_regime_at_entry(vane, past, data.timeframe)
                               if vane else {'regime': 'not computed',
                                             'adx': None, 'entropy': None})
                    pos = {
                        'direction': pending,
                        'entry_i': i,
                        'entry_time': times[i],
                        'entry_raw': raw,
                        'entry_fill': fill,
                        'atr': float(atr),
                        'stop_loss': plan['stop_loss'],
                        'take_profit': plan['take_profit'],
                        'size_units': plan['size_units'],
                        'position_value': plan['position_value'],
                        'equity_at_entry': equity,
                        'regime': weather.get('regime'),
                        'adx': weather.get('adx'),
                        'entropy': weather.get('entropy'),
                    }
            pending = None

        # --- 2. EXITS: checked against THIS candle's high/low (the entry
        #        candle included — a stop can be hit an hour after you buy) ---
        if pos is not None:
            in_market[i] = True
            d = pos['direction']
            sl, tp = pos['stop_loss'], pos['take_profit']
            if d == 'long':
                hit_sl, hit_tp = l[i] <= sl, h[i] >= tp
            else:
                hit_sl, hit_tp = h[i] >= sl, l[i] <= tp

            exit_raw, reason = None, None
            if hit_sl:
                # THE PESSIMISTIC RULE: if both were touched inside one candle
                # we cannot know which came first, so we count the LOSS.
                # A gap through the stop fills at the open, not at the stop.
                exit_raw = min(float(o[i]), sl) if d == 'long' else max(float(o[i]), sl)
                reason = 'stop+target same candle (loss counted)' if hit_tp else 'stop'
            elif hit_tp:
                exit_raw = tp          # never better than the target itself
                reason = 'target'
            elif i == n - 1:
                exit_raw = float(c[i])
                reason = 'end of data (forced close)'

            if exit_raw is not None:
                size = pos['size_units']
                exit_fill = (exit_raw * (1 - slip) if d == 'long'
                             else exit_raw * (1 + slip))
                if d == 'long':
                    gross = size * (exit_raw - pos['entry_raw'])
                    after_slip = size * (exit_fill - pos['entry_fill'])
                else:
                    gross = size * (pos['entry_raw'] - exit_raw)
                    after_slip = size * (pos['entry_fill'] - exit_fill)
                fees = fee * (size * pos['entry_fill'] + size * exit_fill)
                slippage_paid = gross - after_slip
                net = after_slip - fees
                eq_in = pos['equity_at_entry']
                equity = eq_in + net

                trades.append({
                    'trade_no': len(trades) + 1,
                    'window': ('holdout' if train_end is not None
                               and pos['entry_time'] > train_end else 'train'),
                    'direction': d,
                    'entry_time': pos['entry_time'],
                    'entry_price_raw': pos['entry_raw'],
                    'entry_price_fill': pos['entry_fill'],
                    'exit_time': times[i],
                    'exit_price_raw': exit_raw,
                    'exit_price_fill': exit_fill,
                    'exit_reason': reason,
                    'bars_held': i - pos['entry_i'] + 1,
                    'atr_at_entry': pos['atr'],
                    'stop_loss': sl,
                    'take_profit': tp,
                    'size_units': size,
                    'position_value': pos['position_value'],
                    'equity_at_entry': eq_in,
                    'gross_pnl': gross,
                    'fees_paid': fees,
                    'slippage_paid': slippage_paid,
                    'costs_paid': fees + slippage_paid,
                    'net_pnl': net,
                    'return_pct': net / eq_in if eq_in else 0.0,
                    'gross_return_pct': gross / eq_in if eq_in else 0.0,
                    'equity_after': equity,
                    'regime_at_entry': pos['regime'],
                    'regime_adx': pos['adx'],
                    'regime_entropy': pos['entropy'],
                })
                pos = None

        # --- 3. THE SIGNAL, asked at THIS candle's close ------------------
        if pos is None:
            view = df.iloc[:i + 1].copy()   # its OWN copy. The future is not
            audit_calls += 1                # in it — not as a row, not as a
            if len(view) != i + 1 or view.index[-1] != times[i]:
                audit_violations += 1       # shared memory buffer either.
                raise RuntimeError(
                    f'LOOK-AHEAD VIOLATION at candle {i} ({times[i]}): the '
                    f'engine was about to hand the strategy data it must not '
                    f'have. Refusing to produce a number.')
            sig = signal(view)
            if sig not in SIGNALS:
                raise ValueError(
                    f'{strategy_name} returned {sig!r} at {times[i]} — the '
                    f'contract is exactly one of {SIGNALS}.')
            if sig != 'flat':
                pending = sig

    params = dict(params or {})
    # The fingerprint covers everything that can move the number, not just the
    # strategy's own dials. Change a cost and you have a different record.
    stamped = dict(params)
    stamped.update({'_costs': costs, '_risk_pct': risk_pct,
                    '_sl_atr': sl_mult, '_tp_atr': tp_mult,
                    '_atr_period': atr_period, '_capital': capital,
                    '_train_end': str(train_end)})

    meta = {
        'strategy': strategy_name,
        'params': params,
        'fingerprint': fingerprint(strategy_name, stamped),
        'commit': git_commit(),
        'asset': data.asset,
        'timeframe': data.timeframe,
        'source': data.path,
        'verdict': data.verdict,
        'candles_total': n,
        'train_end': train_end,
        'capital': capital,
        'costs': costs,
        'risk_pct': risk_pct,
        'sl_atr_mult': sl_mult,
        'tp_atr_mult': tp_mult,
        'atr_period': atr_period,
        'run_date': datetime.now().strftime('%Y-%m-%d'),
        'audit_calls': audit_calls,
        'audit_violations': audit_violations,
    }
    result = BacktestResult(trades, in_market, times, meta)
    if verbose:
        result.print_report()
    return result


if __name__ == '__main__':
    print(__doc__)
    print('This is the engine. The exam that proves it honest is '
          'lab/gate_2_3.py — run that.')
