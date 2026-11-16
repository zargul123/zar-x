"""
Zar X Lab — THE GAUNTLET RUNNER (Phase 6). The one run per slot that counts.

**THE PROMISE: exactly three sealed slots, then the signals chapter closes.**
This file runs one slot, ONCE, and prints one verdict. Its rules were
declared in PROGRESS_LOG.md on 2026-11-15 and committed with no code,
before this file existed. **ON 2026-11-16 THE COMMANDER RE-SPECIFIED SLOT 1
FROM DAILY TO 4-HOUR CANDLES, BEFORE ANYTHING HAD BEEN RUN**; the new bar
was committed alone that day, before this file was changed. The five bars,
the pooling, the yardstick and the hold-out line did not change.

**ON 2026-11-16 (NIGHT) HE RULED TWO MORE CHANGES, AGAIN BEFORE ANYTHING HAD
BEEN RUN**, and their bar was committed alone before this file was changed:

  * THE GAUNTLET CHARGES HIS REAL EXCHANGE'S FEE: Binance futures taker,
    0.05% a side, with 0.05% slippage a side - `config.GAUNTLET_COSTS`,
    0.20% there and back. (The Lab's own exams keep `LAB_COSTS`.)
  * SLOT 1's STOP AND TARGET ARE DAY-SIZED: 3.75 and 5.0 times the average
    range of the last 84 four-hour candles (14 days) - the ship's 1.5 and
    2.0 applied to a day's move, a day being 2.5 four-hour ranges. The
    ENTRY (`signals/turtle.py`) did not change.

WHAT IT DOES, in order:

  1. Refuses to run without `--go`, typed on purpose.
  2. Refuses to run if the slot's marker file exists: THE SLOT IS SPENT.
  3. WRITES THE MARKER. Only then is the vault opened. A run that dies
     half-way has still spent the slot; a second run needs the Commander's
     ruling written in PROGRESS_LOG.md first.
  4. Runs the strategy through the Lab's own engine (`lab/engine.py`,
     unchanged) on each coin's 4-HOUR vault file, hold-out line 2025-10-01.
  5. POOLS the three coins' hold-out trades into one list, in order of
     entry time. **ONE VERDICT FOR THE SLOT. A coin cannot pass alone.**
  6. Measures the five locked bars on that one list:
       B1  Profit Factor >= 1.15 after costs
       B2  at least 30 trades
       B3  walk-forward CONSISTENT          (lab/walk_forward.py, unchanged)
       B4  Monte Carlo 5th-pct drawdown < 30%  (lab/monte_carlo.py, unchanged)
       B5  beats buy-and-hold with 1% risk sizing on the same window
  7. Sounds the too-good alarm (Profit Factor above 2.0 or win rate above
     70%): the verdict is then WITHHELD until the strategy has been hunted
     for a leak.

**B5, DEFINED HERE BECAUSE NO FILE ON THIS SHIP HAD EVER BUILT IT:** for
each coin, buy at the open of the first hold-out candle, sized by the same
risk-engine call the Lab makes (1% risk, a 1.5-ATR stop distance, the 25%
cap), pay the same costs both sides, never stop out, sell at the last
close. The three coins' results are compounded together, and the
strategy's pooled result, compounded the same way, must be STRICTLY greater.

**WHAT A PASS MEANS AND DOES NOT MEAN.** A pass earns the strategy a place
in Phase 7's proving voyage - on paper. It does not mean it makes money.
The Lab's numbers catch overfitting and CANNOT catch a leak (Law 7).

RUN (from the zar-x folder):
    python lab/gauntlet.py --gate            (rehearsal on made-up candles)
    python lab/gauntlet.py --slot 1 --go     (THE RUN. ONCE.)
"""
import math
import os
import sys
from datetime import datetime

import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(LAB_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, LAB_DIR)

import engine                                              # noqa: E402
from config import GAUNTLET_COSTS, LAB_COSTS, RISK_CONFIG  # noqa: E402
from monte_carlo import monte_carlo                        # noqa: E402
from risk.calculator import RiskCalculator                 # noqa: E402
from trade_stats import summarise                          # noqa: E402
from walk_forward import walk_forward_trades               # noqa: E402

TRAIN_END = '2025-10-01'        # the hold-out line, fixed in Phase 2
ASSETS = ('BTC-USD', 'ETH-USD', 'SOL-USD')
TIMEFRAME = '4h'                # re-specified from '1d' on 2026-11-16

# THE FIVE BARS, copied from EXECUTION_PLAN.md so they cannot drift.
BAR_MIN_PROFIT_FACTOR = 1.15
BAR_MIN_TRADES = 30
BAR_WALK_FORWARD = 'CONSISTENT'
BAR_MAX_MC_DRAWDOWN = 30.0
TOO_GOOD_PF = 2.0
TOO_GOOD_WIN_PCT = 70.0

# SLOT 1's EXIT, ruled 2026-11-16 (night): the ship's 1.5 and 2.0, applied to
# a DAY's typical move. A day is 2.5 four-hour ranges, and 14 days is 84
# four-hour candles.
SLOT1_SL_ATR = 3.75
SLOT1_TP_ATR = 5.0
SLOT1_ATR_PERIOD = 84


def slot_strategy(slot):
    """The strategy sealed into each slot. Slots 2 and 3 are not built."""
    if slot == 1:
        from signals.turtle import TurtleBreakout
        return TurtleBreakout()
    raise ValueError(f'slot {slot} has no strategy built yet')


def marker_path(slot, results_dir):
    return os.path.join(results_dir, f'GAUNTLET_SLOT_{slot}_SPENT.txt')


def holdout_index(df, train_end=TRAIN_END):
    """The candles after the line: the only ones whose trades count."""
    return df.index[df.index > pd.Timestamp(train_end)]


def buy_and_hold(df, train_end=TRAIN_END, capital=engine.INITIAL_CAPITAL,
                 costs=None, sl_atr_mult=None, tp_atr_mult=None,
                 atr_period=None):
    """B5's yardstick for one coin -> its result as a fraction of capital.

    Bought at the first hold-out candle's open, sized by the same
    `plan_trade` call the engine makes, held to the last close, never
    stopped, the gauntlet's costs paid on both sides. The stop distance
    that sizes it is the slot's own: with no exit arguments it is the
    ship's default (1.5 x the 14-candle range), which is what Slot 2 uses.
    """
    costs = dict(costs or GAUNTLET_COSTS)
    sl_atr_mult = (RISK_CONFIG['default_sl_atr'] if sl_atr_mult is None
                   else sl_atr_mult)
    tp_atr_mult = (RISK_CONFIG['default_tp_atr'] if tp_atr_mult is None
                   else tp_atr_mult)
    atr_period = engine.ATR_PERIOD if atr_period is None else atr_period
    fee, slip = float(costs['fee_pct']), float(costs['slippage_pct'])
    after = holdout_index(df, train_end)
    if len(after) == 0:
        raise ValueError('no hold-out candles to hold through')
    first = df.index.get_loc(after[0])
    calc = RiskCalculator()
    atr = calc.atr(df.iloc[:first], atr_period)
    fill = float(df['open'].iloc[first]) * (1 + slip)
    plan = calc.plan_trade(capital=capital, entry_price=fill,
                           direction='long', atr=atr,
                           risk_pct=RISK_CONFIG['risk_per_trade'],
                           sl_atr_mult=sl_atr_mult,
                           tp_atr_mult=tp_atr_mult)
    if not plan:
        raise ValueError('the risk engine could not size the yardstick')
    size = plan['size_units']
    exit_fill = float(df['close'].iloc[-1]) * (1 - slip)
    net = size * (exit_fill - fill) - fee * size * (fill + exit_fill)
    return net / capital


def compound(fractions):
    """Results as fractions of equity, one after another -> the whole."""
    whole = 1.0
    for fraction in fractions:
        whole *= (1.0 + float(fraction))
    return whole - 1.0


def pool(trades_by_asset):
    """Each coin's hold-out trades -> ONE list, in order of entry time.
    Ties keep the order of `ASSETS`, so the list is the same every run."""
    frames = []
    for order, (asset, trades) in enumerate(trades_by_asset):
        part = trades.copy()
        part['asset'] = asset
        part['_order'] = order
        frames.append(part)
    if not frames:
        return pd.DataFrame(columns=['entry_time', 'return_pct', 'asset'])
    pooled = pd.concat(frames, ignore_index=True)
    if len(pooled):
        pooled = pooled.sort_values(['entry_time', '_order'],
                                    kind='mergesort').reset_index(drop=True)
    return pooled.drop(columns=['_order'])


def battery(pooled, index, yardsticks):
    """The five bars on the pooled hold-out trades.

    -> a dict: `rows` (name, measured, required, passed), `alarm`, and
    `verdict`, one of PASSED / FAILED / WITHHELD.
    """
    stats = summarise(pooled)
    trades = int(stats['trades'])
    pf = stats['profit_factor']
    win_pct = stats['win_pct']
    wf = walk_forward_trades(pooled, index=index,
                             label='pooled hold-out')
    try:
        if trades < 2:
            raise ValueError('too few trades to reshuffle')
        mc = monte_carlo(pooled['return_pct'].values,
                         label='pooled hold-out')
        mc_dd, mc_text = float(mc['dd_p95']), f"{mc['dd_p95']:.2f}%"
    except ValueError:
        # Fewer than two trades: the Monte Carlo refuses, and a bar that
        # could not be measured is a bar that was not cleared.
        mc_dd, mc_text = float('inf'), 'not measurable'
    strategy_whole = compound(pooled['return_pct'].values) if trades else 0.0
    yardstick_whole = compound(yardsticks)

    rows = [
        ('B1 pooled Profit Factor after costs',
         'no trades' if pf is None else f'{pf:.2f}',
         f'>= {BAR_MIN_PROFIT_FACTOR}',
         pf is not None and pf >= BAR_MIN_PROFIT_FACTOR),
        ('B2 pooled hold-out trades', f'{trades}', f'>= {BAR_MIN_TRADES}',
         trades >= BAR_MIN_TRADES),
        ('B3 walk-forward verdict', wf.verdict, BAR_WALK_FORWARD,
         wf.verdict == BAR_WALK_FORWARD),
        ('B4 Monte Carlo 5th-pct drawdown', mc_text,
         f'< {BAR_MAX_MC_DRAWDOWN:.0f}%', mc_dd < BAR_MAX_MC_DRAWDOWN),
        ('B5 beats buy-and-hold, 1% sizing',
         f'{100 * strategy_whole:+.2f}%',
         f'> {100 * yardstick_whole:+.2f}%',
         strategy_whole > yardstick_whole),
    ]
    alarm = (pf is not None and (pf > TOO_GOOD_PF or math.isinf(pf))) or (
        win_pct is not None and win_pct > TOO_GOOD_WIN_PCT)
    cleared = all(ok for _n, _g, _r, ok in rows)
    if not cleared:
        verdict = 'FAILED'
    elif alarm:
        verdict = 'WITHHELD'
    else:
        verdict = 'PASSED'
    return {'rows': rows, 'alarm': bool(alarm), 'verdict': verdict,
            'stats': stats, 'walk_forward': wf,
            'strategy_whole': strategy_whole,
            'yardstick_whole': yardstick_whole}


def report_lines(slot, name, result):
    """The verdict, in words a non-programmer can read."""
    L = ['', '=' * 78,
         f'GAUNTLET SLOT {slot} — {name} — THE FIVE LOCKED BARS, ON THE '
         f'THREE COINS POOLED', '=' * 78,
         f'    {"bar":<38}{"measured":>16}{"required":>14}   verdict',
         '    ' + '-' * 74]
    for bar, got, need, ok in result['rows']:
        L.append(f'    {bar:<38}{got:>16}{need:>14}   '
                 f'{"PASS" if ok else "FAIL"}')
    L.append('    ' + '-' * 74)
    passed = sum(1 for _b, _g, _n, ok in result['rows'] if ok)
    L.append(f'    bars cleared: {passed} of {len(result["rows"])}')
    L.append('')
    if result['alarm']:
        L.append('    !! THE TOO-GOOD ALARM IS SOUNDING (Profit Factor above '
                 f'{TOO_GOOD_PF} or win rate above {TOO_GOOD_WIN_PCT:.0f}%).')
        L.append('    !! Assume a bug or a leak first. Hunt it before '
                 'believing anything.')
    if result['verdict'] == 'PASSED':
        L.append(f'    VERDICT: SLOT {slot} PASSED. All five bars cleared.')
        L.append('    The strategy earns a place in the Phase 7 proving '
                 'voyage - ON PAPER.')
        L.append('    This is not proof that it makes money.')
    elif result['verdict'] == 'WITHHELD':
        L.append(f'    VERDICT: WITHHELD. All five bars cleared but the '
                 f'alarm is sounding.')
        L.append('    No pass is granted until the strategy has been hunted '
                 'for a leak.')
    else:
        L.append(f'    VERDICT: SLOT {slot} FAILED. A strategy must clear '
                 f'EVERY bar.')
        L.append('    Clearing some of them is not a partial pass. The slot '
                 'is spent.')
        L.append('    No second try and no "just one change".')
    L.append('=' * 78)
    return L


def run_slot(slot, loader=None, results_dir=None, out=print):
    """THE RUN. Writes the marker, then opens the data, then judges.

    `loader` and `results_dir` exist so the gate can rehearse this whole
    function on made-up candles in a temporary folder. The real run passes
    neither and gets the vault and `lab/results/`.
    """
    loader = engine.load_vault if loader is None else loader
    results_dir = engine.RESULTS_DIR if results_dir is None else results_dir
    os.makedirs(results_dir, exist_ok=True)
    marker = marker_path(slot, results_dir)
    if os.path.exists(marker):
        raise RuntimeError(
            f'REFUSED: slot {slot} is SPENT ({marker}). THE PROMISE allows '
            f'each slot one run. A second run needs the Commander\'s ruling '
            f'written in PROGRESS_LOG.md first.')
    strategy = slot_strategy(slot)

    # THE MARKER GOES DOWN BEFORE THE DATA IS OPENED.
    with open(marker, 'x', encoding='utf-8') as handle:
        handle.write(f'GAUNTLET SLOT {slot} — SPENT\n'
                     f'strategy  : {strategy.name}\n'
                     f'params    : {strategy.params}\n'
                     f'commit    : {engine.git_commit()}\n'
                     f'started   : {datetime.now().isoformat(timespec="seconds")}\n'
                     f'train_end : {TRAIN_END}\n')

    out(f'GAUNTLET SLOT {slot} — {strategy.name}')
    out(f'  marker written: {marker}')
    out(f'  coins {", ".join(ASSETS)}  timeframe {TIMEFRAME}  hold-out '
        f'line {TRAIN_END}')

    per_asset, yardsticks, indexes, saved = [], [], [], []
    for asset in ASSETS:
        data = loader(asset, TIMEFRAME)
        result = engine.run_backtest(
            data, strategy, strategy_name=strategy.name,
            params=strategy.params, train_end=TRAIN_END, verbose=False,
            costs=GAUNTLET_COSTS, sl_atr_mult=SLOT1_SL_ATR,
            tp_atr_mult=SLOT1_TP_ATR, atr_period=SLOT1_ATR_PERIOD)
        saved.append(result.save_csv(results_dir))
        held = result.window_trades('holdout')
        per_asset.append((asset, held))
        indexes.append(holdout_index(data.df))
        yardsticks.append(buy_and_hold(
            data.df, sl_atr_mult=SLOT1_SL_ATR, tp_atr_mult=SLOT1_TP_ATR,
            atr_period=SLOT1_ATR_PERIOD))
        card = result.card('holdout')
        out('')
        out(f'  --- {asset}: INFORMATION ONLY. No bar reads this. ---')
        out(card.text())
        out(f'    look-ahead audit: {result.meta["audit_calls"]:,} strategy '
            f'calls, {result.meta["audit_violations"]} violations')
        out(f'    buy-and-hold yardstick for this coin: '
            f'{100 * yardsticks[-1]:+.2f}%')

    # THE THREE COINS MUST COVER THE SAME DAYS, or pooling them by time is
    # a fiction. Checked BEFORE any verdict is worked out.
    for asset, index in zip(ASSETS[1:], indexes[1:]):
        if not index.equals(indexes[0]):
            raise RuntimeError(
                f'REFUSED: {asset} and {ASSETS[0]} do not cover the same '
                f'hold-out days ({len(index)} against {len(indexes[0])}). '
                f'No verdict is produced.')

    pooled = pool(per_asset)
    pooled_path = os.path.join(results_dir,
                               f'gauntlet_slot{slot}_pooled_holdout.csv')
    pooled.to_csv(pooled_path, index=False)
    result = battery(pooled, indexes[0], yardsticks)
    out('')
    out(f'  pooled hold-out trades: {len(pooled)}  '
        f'({", ".join(f"{a} {len(t)}" for a, t in per_asset)})')
    out(result['walk_forward'].text()
        if hasattr(result['walk_forward'], 'text') else '')
    for line in report_lines(slot, strategy.name, result):
        out(line)
    with open(marker, 'a', encoding='utf-8') as handle:
        handle.write(f'finished  : {datetime.now().isoformat(timespec="seconds")}\n'
                     f'verdict   : {result["verdict"]}\n')
    result['pooled'] = pooled
    result['saved'] = saved + [pooled_path]
    result['marker'] = marker
    return result


def main(argv, runner=None, results_dir=None):
    """`--slot N --go` runs a slot. Anything less refuses and touches
    nothing. `runner` and `results_dir` exist so the gate can prove a
    refusal never reaches the run - WITHOUT the gate itself ever being one
    edit away from spending a real slot, and without it writing one byte
    into the real results folder. (The first draft of that check did write
    there: a two-byte report file. Found by the gate's own closing check.)
    """
    runner = run_slot if runner is None else runner
    results_dir = engine.RESULTS_DIR if results_dir is None else results_dir
    slot = None
    if '--slot' in argv:
        at = argv.index('--slot')
        try:
            slot = int(argv[at + 1])
        except (IndexError, ValueError):
            slot = None
    if slot is None or '--go' not in argv:
        print('REFUSED. The gauntlet runs ONE slot ONCE, and only when asked '
              'on purpose:')
        print('    python lab/gauntlet.py --slot 1 --go')
        print('Nothing was opened and nothing was written.')
        return 2
    lines = []

    def out(line=''):
        print(line)
        lines.append(str(line))

    try:
        result = runner(slot, out=out)
    finally:
        os.makedirs(results_dir, exist_ok=True)
        log = os.path.join(results_dir, f'gauntlet_slot{slot}_report.txt')
        with open(log, 'a', encoding='utf-8') as handle:
            handle.write('\n'.join(lines) + '\n')
    return 0 if result['verdict'] == 'PASSED' else 1


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        sys.exit(main(sys.argv[1:]))

    # =====================================================================
    # GATE 6.4-R — THE RUNNER'S REHEARSAL, ON 4-HOUR CANDLES, WITH THE
    # COMMANDER'S REAL FEE AND SLOT 1's DAY-SIZED EXIT. Declared in
    # PROGRESS_LOG.md on 2026-11-16 (night) and committed with no `.py`,
    # before this file was changed. It replaces GATE 6.2-R (never run).
    #
    # **IT NEVER OPENS THE VAULT.** The Lab's door is replaced by one that
    # raises. Every candle below is made up, and every result is written
    # into a temporary folder.
    # =====================================================================
    import shutil
    import tempfile

    import numpy as np

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def text_of(path):
        """A file's text, or '' if it is not there. Rule (k): a check that
        stands on a file some earlier step failed to write goes RED and
        carries on."""
        try:
            with open(path, encoding='utf-8') as handle:
                return handle.read()
        except OSError:
            return ''

    def held_or(default, function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as exc:                           # noqa: BLE001
            return default if default is not None else (
                f'<{type(exc).__name__}: {exc}>')

    VAULT_OPENED = []
    _real_door = engine.load_vault

    def _no_vault(*args, **kwargs):
        VAULT_OPENED.append(args)
        raise RuntimeError('the rehearsal must never open the vault')

    engine.load_vault = _no_vault
    REAL_RESULTS_BEFORE = sorted(os.listdir(engine.RESULTS_DIR))
    WORK = tempfile.mkdtemp(prefix='zarx_gauntlet_')

    # THE VAULT'S OWN HOLD-OUT, TYPED OUT: 1,789 four-hour candles, the
    # first opening at 04:00 on 2025-10-01 (the 00:00 candle is training,
    # by the engine's rule `index > train_end`). Measured on 2026-11-16
    # from the date column of the three vault files, and from nothing else.
    FOUR_HOURS = pd.Timedelta(hours=4)
    HOLD = pd.date_range('2025-10-01 04:00', periods=1789, freq=FOUR_HOURS)
    STARTS = [(k * 1789) // 6 for k in range(6)]  # 0 298 596 894 1192 1490

    def trades(per_window):
        """Six lists of results -> hold-out trades, each list spread inside
        its own walk-forward window (six windows of 298 or 299 candles,
        cut the way lab/walk_forward.py cuts them: typed out above)."""
        rows = []
        for window, results in enumerate(per_window):
            for n, value in enumerate(results):
                rows.append({'entry_time': HOLD[STARTS[window] + 1 + 3 * n],
                             'return_pct': float(value),
                             'direction': 'long'})
        return pd.DataFrame(rows, columns=['entry_time', 'return_pct',
                                           'direction'])

    def judge(per_window, yardsticks):
        try:
            result = battery(trades(per_window), HOLD, yardsticks)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>', ()
        return result['verdict'], tuple(ok for _b, _g, _n, ok
                                        in result['rows'])

    MILD = (0.01, 0.0, -0.005)          # the yardstick: about +0.5% whole
    W, L = 0.012, -0.010
    GOOD = [[W, L] * 3] * 6             # 36 trades, PF 0.216/0.180 = 1.20

    print("=" * 70)
    print("GATE 6.4-R — THE GAUNTLET RUNNER ON 4-HOUR CANDLES, REHEARSED.")
    print("Made-up trades and made-up candles. The vault is never opened.")
    print("=" * 70)

    print("\n(a) THE FIVE BARS ON HAND-MADE TRADES. Each bar is forced red"
          "\n    ALONE, with the other four green, so that no bar can hide"
          "\n    behind another.")
    # 36 trades: 18 wins of +1.2% and 18 losses of -1.0%. PF = 0.216/0.180
    # = 1.20. Every window holds 3 wins and 3 losses: +0.6% each, 6 of 6
    # profitable, 16.7% of the profit each. The whole compounds to
    # (1.012 x 0.990)^18 - 1 = +3.4%, above the +0.5% yardstick.
    mark(judge(GOOD, MILD) == ('PASSED', (True,) * 5),
         "36 trades, Profit Factor 1.20, spread evenly: ALL FIVE CLEARED, "
         "no alarm -> PASSED", str(judge(GOOD, MILD)))
    # Wins of +1.14% instead: PF = 0.2052/0.180 = 1.14, below 1.15.
    mark(judge([[0.0114, L] * 3] * 6, MILD)
         == ('FAILED', (False, True, True, True, True)),
         "B1 ALONE: the same trades with wins of 1.14% — Profit Factor "
         "1.14, one hundredth under the bar -> FAILED",
         str(judge([[0.0114, L] * 3] * 6, MILD)))
    # 29 trades: five windows of 3 wins and 2 losses... kept at PF >= 1.15:
    # windows of [W, L, W, L, W] (5 trades) x 5 = 25, plus [W, L, W, L] = 29.
    TWENTY_NINE = [[W, L, W, L, W]] * 5 + [[W, L, W, L]]
    THIRTY = [[W, L, W, L, W]] * 6
    mark(judge(TWENTY_NINE, MILD)
         == ('FAILED', (True, False, True, True, True))
         and judge(THIRTY, MILD) == ('PASSED', (True,) * 5),
         "B2 ALONE, AT THE EXACT NUMBER: 29 good trades -> FAILED on the "
         "count and nothing else; 30 -> PASSED. Fewer than 30 is a fail, "
         "not 'promising'",
         f"29: {judge(TWENTY_NINE, MILD)}  30: {judge(THIRTY, MILD)}")
    # Three strong windows then three that each lose 0.3%: profitable in 3
    # of 6, which is under the 4 the bar needs. PF = (9 x 0.03 + 9 x 0.009)
    # / 0.18 = 1.95, under the alarm's 2.0.
    LOPSIDED = [[0.03, L] * 3] * 3 + [[0.009, L] * 3] * 3
    mark(judge(LOPSIDED, MILD)
         == ('FAILED', (True, True, False, True, True)),
         "B3 ALONE: all the profit in the first half, the last three "
         "windows each losing — profitable in 3 of 6 -> FAILED",
         str(judge(LOPSIDED, MILD)))
    # Wins of +40% and losses of -25%: PF 0.40/0.25 = 1.60, and each
    # win-loss pair compounds to 1.40 x 0.75 = 1.05, so every window is
    # profitable. But three losses in a row cost 58%: shuffled, the worst
    # twentieth of drawdowns is far over 30%.
    # (THE FIRST DRAFT USED +30% / -25% AND CALLED IT "B4 ALONE". It was
    # not alone: a pair compounds to 0.975, so every window LOSES and B3
    # went red too. The Lab judges a window by what it compounds to, not
    # by what it adds up to - my hand arithmetic had added.)
    WILD = [[0.40, -0.25] * 3] * 6
    ABYSS = (-0.5, -0.5, -0.5)
    mark(judge(WILD, ABYSS) == ('FAILED', (True, True, True, False, True)),
         "B4 ALONE: Profit Factor 1.60 made of 40% wins and 25% losses — "
         "every window profitable, and the shuffled drawdown ruinous -> "
         "FAILED",
         str(judge(WILD, ABYSS)))
    # B4 NEAR ITS OWN LINE. (A drawdown bar tripled to 90% went GREEN at
    # 43/0 in this gate's own attack: the only B4 case was ruinous, far
    # past any line.) The Monte Carlo is seeded, so these two are fixed
    # figures: wins of 5% and losses of 4% reshuffle to a worst-twentieth
    # drawdown of 29.07%, just inside 30%; wins of 6% and losses of 5% to
    # 35.64%, just outside. Both measured on 2026-11-16 and typed here.
    INSIDE = [[0.05, -0.04] * 3] * 6
    OUTSIDE = [[0.06, -0.05] * 3] * 6

    def drawdown_of(per_window):
        try:
            return battery(trades(per_window), HOLD, ABYSS)['rows'][3][1]
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>'

    mark(judge(INSIDE, ABYSS) == ('PASSED', (True,) * 5)
         and judge(OUTSIDE, ABYSS)
         == ('FAILED', (True, True, True, False, True))
         and drawdown_of(INSIDE) == '29.07%'
         and drawdown_of(OUTSIDE) == '35.64%',
         "B4 NEAR ITS LINE: a reshuffled drawdown of 29.07% clears the 30% "
         "bar -> PASSED; one of 35.64% does not -> FAILED on the drawdown "
         "and nothing else",
         f"inside {drawdown_of(INSIDE)} {judge(INSIDE, ABYSS)[0]}, outside "
         f"{drawdown_of(OUTSIDE)} {judge(OUTSIDE, ABYSS)[0]}")
    RICH = (0.05, 0.05, 0.05)           # buy-and-hold made +15.8%
    mark(judge(GOOD, RICH) == ('FAILED', (True, True, True, True, False)),
         "B5 ALONE: the good trades (+3.4%) against a buy-and-hold that "
         "made +15.8% -> FAILED. A strategy that cannot beat sitting still "
         "adds nothing", str(judge(GOOD, RICH)))
    # (1.30 x 0.75)^18 - 1 = -36.6%; the yardstick -20%.
    CHOP = [[0.30, -0.25] * 3] * 6
    mark(judge(CHOP, (-0.2, 0.0, 0.0))
         == ('FAILED', (True, True, False, False, False)),
         "and B5 COMPOUNDS, it does not add: 18 wins of 30% and 18 losses "
         "of 25% ADD to +90% but COMPOUND to -36.6%, which is below a "
         "yardstick of -20% -> B5 red (and B3 and B4 with it: every window "
         "compounds to a loss)",
         str(judge(CHOP, (-0.2, 0.0, 0.0))))

    # THE SAME 36 RESULTS ON BOTH SIDES: the strategy and the yardstick
    # compound to exactly the same figure. "Beats" means strictly more.
    SAME = tuple([W, L] * 18)
    mark(judge(GOOD, SAME) == ('FAILED', (True, True, True, True, False)),
         "B5 AT EXACT EQUALITY: a strategy that only MATCHES buy-and-hold, "
         "to the last digit, has not beaten it -> FAILED. (`>=` in place of "
         "`>` went green at 37/0 in this gate's own attack.)",
         str(judge(GOOD, SAME)))

    print("\n(b) THE TOO-GOOD ALARM, AND THE AWKWARD LISTS.")
    mark(judge([[0.03, L] * 3] * 6, MILD) == ('WITHHELD', (True,) * 5),
         "Profit Factor 3.0, every bar cleared -> WITHHELD, not PASSED: the "
         "alarm outranks the bars", str(judge([[0.03, L] * 3] * 6, MILD)))
    # 30 wins of +0.35% and 6 losses of -1.0%: PF 0.105/0.060 = 1.75,
    # under the alarm's 2.0; win rate 30 of 36 = 83%, over its 70%.
    MANY_SMALL = [[0.0035, 0.0035, 0.0035, L, 0.0035, 0.0035]] * 6
    mark(judge(MANY_SMALL, MILD) == ('WITHHELD', (True,) * 5),
         "a win rate of 83% with a Profit Factor of only 1.75 -> WITHHELD "
         "on the win rate alone", str(judge(MANY_SMALL, MILD)))
    mark(judge([[0.01] * 6] * 6, MILD) == ('WITHHELD', (True,) * 5),
         "NOT ONE LOSING TRADE: Profit Factor is infinite -> WITHHELD",
         str(judge([[0.01] * 6] * 6, MILD)))
    try:
        none = judge([[]] * 6, MILD)
        one = judge([[0.01]] + [[]] * 5, MILD)
        crashed = ''
    except Exception as exc:                               # noqa: BLE001
        none, one, crashed = None, None, f'{type(exc).__name__}: {exc}'
    mark(crashed == '' and none[0] == 'FAILED' and one[0] == 'FAILED'
         and none[1][1] is False and none[1][3] is False
         and one[1][3] is False,
         "NO TRADES AT ALL, and ONE TRADE: each is FAILED, with the Monte "
         "Carlo bar counted as not cleared — and neither crashes the "
         "runner", crashed or f"none {none}  one {one}")

    print("\n(c) B5's YARDSTICK, WORKED BY HAND.")

    def calm(high, low, last_close):
        """30 level candles at 100 with a fixed range, then 10 hold-out
        candles ending at `last_close`. The range sets the ATR exactly.
        The 30th candle opens at 00:00 on 2025-10-01 - the last one that
        is training - and the 31st at 04:00, the first of the hold-out."""
        index = pd.date_range('2025-09-26 04:00', periods=40,
                              freq=FOUR_HOURS)
        closes = [100.0] * 39 + [float(last_close)]
        # THE TEN HOLD-OUT CANDLES SWING FROM 50 TO 150. The yardstick is
        # sized from the candles BEFORE the line and must not feel them: an
        # ATR that took in the first hold-out candle went GREEN at 43/0 in
        # this gate's own attack, because every candle had the same range.
        return pd.DataFrame({'open': [100.0] * 40,
                             'high': [high] * 30 + [150.0] * 10,
                             'low': [low] * 30 + [50.0] * 10,
                             'close': closes}, index=index)

    # Range 99-101: true range 2, ATR 2, stop distance 1.5 x 2 = 3. Fill
    # 100 x 1.0005 = 100.05. Risking 1% of 10,000 = 100 over 3 would buy
    # 33.33 coins = 3,335 - over the 25% cap of 2,500, so the size is
    # 2,500 / 100.05. Sold at 110 x 0.9995 = 109.945. Fees 0.05% each
    # side - the Commander's Binance futures taker fee.
    CAPPED = ((2500 / 100.05) * ((109.945 - 100.05)
                                 - 0.0005 * (100.05 + 109.945)) / 10000)
    got = held_or(float('nan'), buy_and_hold, calm(101.0, 99.0, 110.0))
    mark(abs(got - CAPPED) < 1e-12 and abs(CAPPED - 0.0244628) < 1e-7,
         "a calm coin, range 2: the 25% CAP binds, 2,500 is bought, and "
         "+10% on the coin is +2.44628% on the account at a fee of "
         "0.05% a side — equal to arithmetic typed out here",
         f"{got:.9f} against {CAPPED:.9f}")
    # Range 90-110: ATR 20, stop distance 30, 100 / 30 = 3.333 coins =
    # 333.50: under the cap.
    UNCAPPED = ((100 / 30) * ((109.945 - 100.05)
                              - 0.0005 * (100.05 + 109.945)) / 10000)
    got = held_or(float('nan'), buy_and_hold, calm(110.0, 90.0, 110.0))
    mark(abs(got - UNCAPPED) < 1e-12 and abs(UNCAPPED - 0.0032633) < 1e-7,
         "a wild coin, range 20: the cap does NOT bind, 3.333 coins are "
         "bought, and the same +10% is +0.32633% on the account",
         f"{got:.9f} against {UNCAPPED:.9f}")
    OLD_FEE = ((2500 / 100.05) * ((109.945 - 100.05)
                                  - 0.001 * (100.05 + 109.945)) / 10000)
    got_lab = held_or(float('nan'), buy_and_hold, calm(101.0, 99.0, 110.0),
                      costs={'fee_pct': 0.001, 'slippage_pct': 0.0005})
    mark(abs(got_lab - OLD_FEE) < 1e-12 and abs(OLD_FEE - 0.0242004) < 1e-7
         and abs(OLD_FEE - CAPPED) > 1e-4,
         "and the fee really is what moves it: the same coin charged the "
         "Lab's old 0.1% a side gives +2.42004%, the figure this gate "
         "carried until 2026-11-16 — a different number",
         f"{got_lab:.9f} against {OLD_FEE:.9f}")

    def two_moods(last_close=110.0):
        """100 training candles - 70 wild ones (range 20) and then 30
        calm ones (range 2) - and 10 hold-out candles. The 14-candle range
        is 2; the 84-candle range is (54 x 20 + 30 x 2) / 84 = 13.5714."""
        index = pd.date_range(pd.Timestamp('2025-10-01')
                              - 99 * FOUR_HOURS, periods=110,
                              freq=FOUR_HOURS)
        return pd.DataFrame(
            {'open': [100.0] * 110,
             'high': [110.0] * 70 + [101.0] * 30 + [150.0] * 10,
             'low': [90.0] * 70 + [99.0] * 30 + [50.0] * 10,
             'close': [100.0] * 109 + [float(last_close)]}, index=index)

    # SLOT 1's SIZING: stop distance 3.75 x 13.5714 = 50.893. Risking 100
    # over that buys 1.96491 coins (196.59: under the cap).
    DAY_SIZED = ((100 / (3.75 * (54 * 20 + 30 * 2) / 84))
                 * ((109.945 - 100.05) - 0.0005 * (100.05 + 109.945))
                 / 10000)
    got = held_or(float('nan'), buy_and_hold, two_moods(), sl_atr_mult=3.75,
                  tp_atr_mult=5.0, atr_period=84)
    plain = held_or(float('nan'), buy_and_hold, two_moods())
    short_range = held_or(float('nan'), buy_and_hold, two_moods(),
                          sl_atr_mult=3.75, tp_atr_mult=5.0)
    mark(abs(got - DAY_SIZED) < 1e-12 and abs(DAY_SIZED - 0.0019236) < 1e-7
         and abs(plain - CAPPED) < 1e-12
         and abs(short_range - got) > 1e-4 and abs(short_range - plain) > 1e-4,
         "SLOT 1's DAY-SIZED YARDSTICK, BY HAND: on a coin wild for 70 "
         "candles and calm for the last 30, a stop 3.75 x the 84-CANDLE "
         "range buys 1.965 coins and +10% is +0.19236% — while the same "
         "coin with NO exit arguments is sized the ship's old way (capped, "
         "+2.44628%), which is what Slot 2 gets; and 3.75 x the "
         "14-candle range is a third figure again",
         f"day-sized {got:.9f} against {DAY_SIZED:.9f}; default "
         f"{plain:.9f}; 14-candle {short_range:.9f}")
    mark(abs(compound([0.10, -0.10, 0.50]) - (1.1 * 0.9 * 1.5 - 1)) < 1e-12
         and compound([]) == 0.0,
         "and three results COMPOUND: +10%, -10%, +50% is +48.5%, not +50%")

    print("\n(d) THE POOL: three coins, one list, in order of entry time.")
    A = pd.DataFrame({'entry_time': [HOLD[5], HOLD[1]],
                      'return_pct': [0.01, 0.02], 'direction': ['long'] * 2})
    B = pd.DataFrame({'entry_time': [HOLD[3], HOLD[1]],
                      'return_pct': [0.03, 0.04], 'direction': ['short'] * 2})
    C = pd.DataFrame()                 # a coin that never traded
    pooled = pool([('BTC-USD', A), ('ETH-USD', B), ('SOL-USD', C)])
    mark(list(pooled['return_pct']) == [0.02, 0.04, 0.03, 0.01]
         and list(pooled['asset']) == ['BTC-USD', 'ETH-USD', 'ETH-USD',
                                       'BTC-USD'],
         "four trades from two coins come out in order of entry, and two "
         "entered on the SAME day keep the coins' fixed order — a coin with "
         "no trades at all adds nothing and breaks nothing",
         f"{list(pooled['return_pct'])} {list(pooled['asset'])}")

    print("\n(e) >>> THE WHOLE RUN, REHEARSED ON MADE-UP CANDLES, THROUGH"
          "\n    THE LAB'S REAL ENGINE. Three made-up coins of 5,624 four-"
          "\n    hour candles on the vault's own dates, so the first time"
          "\n    this machinery runs is not the time that counts.")

    def made_up(seed, candles=5624, drift=0.0005):
        """A made-up coin in 4-hour candles: the same 3.5% daily swing and
        the same daily drift as the daily rehearsal used, cut into six
        candles a day, each candle built from eight smaller steps so that
        its high and low are real ranges."""
        rng = np.random.default_rng(seed)
        price, rows = 100.0, []
        for _ in range(candles):
            steps = price * np.exp(np.cumsum(
                rng.normal(drift / 48, 0.035 / np.sqrt(48), 8)))
            rows.append((price, max(price, steps.max()),
                         min(price, steps.min()), float(steps[-1])))
            price = float(steps[-1])
        index = pd.date_range('2024-01-01', periods=candles, freq=FOUR_HOURS)
        return pd.DataFrame(rows, columns=['open', 'high', 'low', 'close'],
                            index=index)

    # THE MADE-UP COINS WEAR THE VAULT'S OWN SHAPE, typed out: 5,624
    # candles, 3,835 of them training, 1,789 hold-out, first hold-out
    # candle 04:00 on 2025-10-01, last candle 04:00 on 2026-07-26.
    shape = made_up(11)
    shape_hold = holdout_index(shape)
    mark(len(shape) == 5624 and len(shape_hold) == 1789
         and len(shape) - len(shape_hold) == 3835
         and shape_hold[0] == pd.Timestamp('2025-10-01 04:00')
         and shape.index[-1] == pd.Timestamp('2026-07-26 04:00')
         and shape_hold.equals(HOLD)
         and set(shape.index.to_series().diff().dropna()) == {FOUR_HOURS},
         "the made-up coins have THE VAULT'S OWN SHAPE: 5,624 four-hour "
         "candles, 3,835 training and 1,789 hold-out, the hold-out opening "
         "at 04:00 on 2025-10-01 — the 00:00 candle of that day is training "
         "— and every step exactly four hours",
         f"{len(shape)} candles, {len(shape_hold)} hold-out, first "
         f"{shape_hold[0]}, last {shape.index[-1]}")

    def fake_door(seeds, log, folder, short=None):
        """A loader that hands the engine made-up candles wearing the
        vault's own class, and notes whether the marker was already down
        when it was first knocked on."""
        def door(asset, timeframe):
            log.append((asset, timeframe,
                        os.path.exists(marker_path(1, folder))))
            data = engine.VaultData.__new__(engine.VaultData)
            data.asset, data.timeframe = asset, timeframe
            data.path = f'<made up: {asset}>'
            data.report, data.verdict = None, 'PASS'
            candles = 5623 if asset == short else 5624
            data.df = made_up(seeds[asset], candles=candles)
            return data
        return door

    SEEDS = {'BTC-USD': 11, 'ETH-USD': 22, 'SOL-USD': 33}
    folder = os.path.join(WORK, 'rehearsal')
    knocks, said = [], []
    try:
        rehearsal = run_slot(1, loader=fake_door(SEEDS, knocks, folder),
                             results_dir=folder, out=said.append)
        died = ''
    except Exception as exc:                               # noqa: BLE001
        rehearsal, died = None, f'{type(exc).__name__}: {exc}'
    mark(died == '' and rehearsal is not None
         and rehearsal['verdict'] in ('PASSED', 'FAILED', 'WITHHELD'),
         "the whole run completed on three made-up coins and reached a "
         "verdict",
         died or f"verdict on made-up candles: {rehearsal['verdict']} "
                 f"(it means NOTHING about the real coins)")
    mark([k[:2] for k in knocks] == [('BTC-USD', '4h'), ('ETH-USD', '4h'),
                                     ('SOL-USD', '4h')]
         and all(k[2] for k in knocks),
         "THE MARKER WAS ALREADY DOWN WHEN THE DATA WAS FIRST ASKED FOR: "
         "three knocks, in the coins' fixed order, FOR THE 4-HOUR FILES, "
         "and the slot was marked spent before the first of them",
         f"{knocks}")

    said_text = '\n'.join(str(line) for line in said)
    per_coin = {}
    if rehearsal is not None:
        for path in rehearsal['saved'][:3]:
            rows = pd.read_csv(path)
            held = rows[rows['window'] == 'holdout']
            per_coin[rows['asset'].iloc[0] if len(rows) else path] = held
    recount = sum(len(v) for v in per_coin.values())
    pooled_csv = (pd.read_csv(rehearsal['saved'][3])
                  if rehearsal is not None and len(rehearsal['saved']) == 4
                  else pd.DataFrame())
    mark(rehearsal is not None and len(per_coin) == 3
         and recount == len(pooled_csv) == len(rehearsal['pooled'])
         and f'pooled hold-out trades: {recount} ' in said_text,
         "THE POOLED COUNT IS THE THREE COINS' HOLD-OUT TRADES ADDED UP — "
         "recounted by this gate from the three per-coin evidence files the "
         "engine saved, not from anything the runner hands over",
         f"{ {k: len(v) for k, v in per_coin.items()} } -> {recount}")
    if len(pooled_csv):
        r = pooled_csv['return_pct'].astype(float)
        by_hand_pf = r[r > 0].sum() / -r[r <= 0].sum()
        by_hand_whole = float(np.prod(1.0 + r.values)) - 1.0
        times = pd.to_datetime(pooled_csv['entry_time'])
    else:
        by_hand_pf, by_hand_whole, times = float('nan'), float('nan'), []
    mark(rehearsal is not None and len(pooled_csv) > 0
         and f'{by_hand_pf:.2f}' == rehearsal['rows'][0][1]
         and f'{100 * by_hand_whole:+.2f}%' == rehearsal['rows'][4][1]
         and list(times) == sorted(times)
         and all(t > pd.Timestamp(TRAIN_END) for t in times),
         "the Profit Factor and the compounded result on the report equal "
         "the same figures RE-WORKED BY THIS GATE from the saved pooled "
         "file; the pooled trades are in time order; and every one was "
         "entered AFTER the hold-out line",
         f"PF {by_hand_pf:.2f}, whole {100 * by_hand_whole:+.2f}%, first "
         f"entry {min(times) if len(times) else '-'}")
    verdict_by_hand = (
        'FAILED' if rehearsal is None
        or not all(ok for _b, _g, _n, ok in rehearsal['rows'])
        else 'WITHHELD' if rehearsal['alarm'] else 'PASSED')
    mark(rehearsal is not None and rehearsal['verdict'] == verdict_by_hand
         and f'VERDICT: ' in said_text
         and (f'SLOT 1 {verdict_by_hand}' in said_text
              or 'VERDICT: WITHHELD' in said_text),
         "and the verdict printed is the one its own five rows imply")
    marker_text = text_of(marker_path(1, folder))
    mark('turtle-4h-20c-10w-adx25' in marker_text and 'verdict   : ' in
         marker_text and 'train_end : 2025-10-01' in marker_text,
         "the marker file names the strategy, the hold-out line and the "
         "verdict")

    print("\n    >>> AND THE THREE THAT WENT GREEN IN THIS GATE'S OWN ATTACK:"
          "\n    costs switched off, risk doubled, and the strategy built"
          "\n    with a different number each left the rehearsal at 37/0,"
          "\n    because nothing checked HOW the engine had been called.")
    # THE FINGERPRINT THE ENGINE STAMPS ON EVERY EVIDENCE ROW is a hash of
    # the strategy's name, its parameters, the costs, the risk, the stop
    # and target multiples, the ATR period, the capital and the hold-out
    # line. Every value below is TYPED OUT HERE. One hash, and any of them
    # moving turns this red.
    DECLARED = {'entry_candles': 20, 'weeks': 10, 'week_candles': 42,
                'adx_min': 25.0, 'adx_period': 14, 'adx_tail': 150,
                'warmup': 379, 'kind': 'donchian_breakout',
                '_costs': {'fee_pct': 0.0005, 'slippage_pct': 0.0005},
                '_risk_pct': 0.01, '_sl_atr': 3.75, '_tp_atr': 5.0,
                '_atr_period': 84, '_capital': 10000.0,
                '_train_end': '2025-10-01 00:00:00'}
    WANT_PRINT = engine.fingerprint('turtle-4h-20c-10w-adx25', DECLARED)
    # Rule (k): only files that ARE per-coin evidence are read as such. With
    # a coin dropped, the list is one file shorter and its third entry is
    # the pooled file - which has no fingerprint column, and the first
    # draft of this check died on it instead of going red.
    evidence = []
    if rehearsal is not None:
        for path in rehearsal['saved']:
            rows = held_or(pd.DataFrame(), pd.read_csv, path)
            if 'fingerprint' in rows.columns and 'window' in rows.columns:
                evidence.append(rows)
    prints = sorted({str(value) for rows in evidence
                     for value in rows['fingerprint'].unique()})
    mark(len(evidence) == 3 and all(len(rows) > 0 for rows in evidence)
         and prints == [WANT_PRINT],
         "EVERY EVIDENCE ROW OF ALL THREE COINS carries one fingerprint, "
         "and it equals the hash of the DECLARED settings typed out in this "
         "gate: the 4-hour strategy — channel 20, 10 weeks of 42 candles, "
         "ADX(14) above 25 on 150 candles, warm-up 379 — fee 0.05%, "
         "slippage 0.05%, risk 1%, stop 3.75 and target 5.0 times the "
         "84-candle range, capital 10,000, line 2025-10-01",
         f"declared {WANT_PRINT}, on the evidence {prints}")
    # AND THE SAME THINGS RE-WORKED FROM THE ROWS THEMSELVES, by this
    # gate's own arithmetic, for every hold-out trade of every coin.
    bad, seen_rows, capped_rows = [], 0, 0
    for rows in evidence:
        for _i, t in rows[rows['window'] == 'holdout'].iterrows():
            seen_rows += 1
            long = t['direction'] == 'long'
            fill = t['entry_price_raw'] * (1.0005 if long else 0.9995)
            out_fill = t['exit_price_raw'] * (0.9995 if long else 1.0005)
            fees = 0.0005 * t['size_units'] * (fill + out_fill)
            stop_gap = abs(t['entry_price_fill'] - t['stop_loss'])
            target_gap = abs(t['take_profit'] - t['entry_price_fill'])
            risked = t['size_units'] * stop_gap
            equity = t['equity_at_entry']
            is_capped = abs(t['position_value'] - 0.25 * equity) < 1e-6
            capped_rows += int(is_capped)
            fine = (abs(t['entry_price_fill'] - fill) < 1e-9 * fill
                    and abs(t['exit_price_fill'] - out_fill) < 1e-9 * out_fill
                    and abs(t['fees_paid'] - fees) < 1e-9 * max(fees, 1)
                    and abs(stop_gap - 3.75 * t['atr_at_entry']) < 1e-9 * fill
                    and abs(target_gap - 5.0 * t['atr_at_entry']) < 1e-9 * fill
                    and t['position_value'] <= 0.25 * equity + 1e-6
                    and (abs(risked - 0.01 * equity) < 1e-6
                         or (is_capped and risked < 0.01 * equity)))
            if not fine:
                bad.append(int(t['trade_no']))
    mark(seen_rows == recount and seen_rows > 0 and not bad,
         "and EVERY HOLD-OUT TRADE'S OWN ROW says the same, re-worked here: "
         "filled 0.05% worse than the printed price on both sides, a fee of "
         "0.05% on both sides, the stop 3.75 ranges away and the target "
         "5.0, and the money at risk EXACTLY 1% of equity unless the 25% "
         "cap bound it lower",
         f"{seen_rows} trades re-worked, {capped_rows} of them capped, "
         f"{len(bad)} wrong {bad[:5]}")

    def yard_by_hand(df):
        """B5's yardstick for one made-up coin, WRITTEN OUT A SECOND TIME
        with plain arithmetic and no call into the runner or the risk
        engine: 1% of 10,000 is 100; the cap is 2,500."""
        first = int((df.index > pd.Timestamp('2025-10-01')).argmax())
        h, lo, c = (df['high'].values, df['low'].values, df['close'].values)
        ranges = [max(h[i] - lo[i], abs(h[i] - c[i - 1]),
                      abs(lo[i] - c[i - 1]))
                  for i in range(first - 84, first)]
        atr = sum(ranges) / 84
        fill = df['open'].values[first] * 1.0005
        size = min(100.0 / (3.75 * atr), 2500.0 / fill)
        out_fill = c[-1] * 0.9995
        return (size * (out_fill - fill)
                - 0.0005 * size * (fill + out_fill)) / 10000.0

    whole = 1.0
    for asset in ('BTC-USD', 'ETH-USD', 'SOL-USD'):
        whole *= 1.0 + yard_by_hand(made_up(SEEDS[asset]))
    WANT_YARD = f'> {100 * (whole - 1.0):+.2f}%'
    mark(rehearsal is not None and rehearsal['rows'][4][2] == WANT_YARD
         and sum(f'buy-and-hold yardstick for this coin' in str(line)
                 for line in said) == 3,
         "THE YARDSTICK THE RUN ACTUALLY USED is the buy-and-hold of the "
         "three made-up coins, worked a second time here from their candles "
         "with plain arithmetic — sized on the 84-candle range with a stop "
         "3.75 of them away, at a fee of 0.05%. (A yardstick quietly set to zero inside "
         "the run went green at 37/0 in this gate's own attack.)",
         f"by hand {WANT_YARD}, on the report "
         f"{rehearsal['rows'][4][2] if rehearsal is not None else '-'}")

    print("\n(f) >>> ONE RUN. THE SECOND IS REFUSED, AND A COIN ON DIFFERENT"
          "\n    DAYS STOPS THE RUN BEFORE ANY VERDICT.")
    knocks2 = []
    try:
        run_slot(1, loader=fake_door(SEEDS, knocks2, folder),
                 results_dir=folder, out=lambda line='': None)
        second = 'IT RAN AGAIN'
    except Exception as exc:                               # noqa: BLE001
        second = f'{type(exc).__name__}: {exc}'
    mark(second.startswith('RuntimeError: REFUSED') and 'SPENT' in second
         and knocks2 == [],
         "a SECOND run of the same slot is REFUSED, and the data was not "
         "even asked for", second[:90])
    folder3 = os.path.join(WORK, 'mismatch')
    said3 = []
    try:
        run_slot(1, loader=fake_door(SEEDS, [], folder3, short='ETH-USD'),
                 results_dir=folder3, out=said3.append)
        third = 'IT PRODUCED A VERDICT'
    except Exception as exc:                               # noqa: BLE001
        third = f'{type(exc).__name__}: {exc}'
    marker3 = text_of(marker_path(1, folder3))
    mark('do not cover the same hold-out days' in third
         and not any('VERDICT' in str(line) for line in said3)
         and 'SPENT' in marker3 and 'verdict' not in marker3,
         "a coin ONE CANDLE short stops the run with NO VERDICT printed and "
         "none written — and the slot is still marked spent, because the "
         "marker goes down first", third[:90])
    # **A SPY STANDS WHERE THE RUN WOULD BE.** The first draft of this
    # check called the real `main`, and its own attack showed what that
    # risks: with the `--go` test deleted, the GATE ITSELF started a run
    # against the real results folder. A gate must never be one edit away
    # from spending a slot.
    reached = []

    def spy(slot, out=None):
        reached.append(slot)
        raise RuntimeError('the spy was reached')

    spy_room = os.path.join(WORK, 'spy')
    codes = [held_or('<crashed>', main, argv, runner=spy,
                     results_dir=spy_room)
             for argv in (['--slot', '1'], ['--go'], [], ['--slot', 'x',
                                                         '--go'])]
    mark(codes == [2, 2, 2, 2] and reached == []
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE,
         "without `--go`, without a slot, or with a slot that is not a "
         "number, the command REFUSES and THE RUN IS NEVER REACHED — proved "
         "with a spy standing where the run would be",
         f"exit codes {codes}, spy reached {reached}")
    went = held_or(None, main, ['--slot', '1', '--go'], runner=spy,
                   results_dir=spy_room)
    mark(reached == [1] and str(went).startswith('<RuntimeError')
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE,
         "and WITH `--slot 1 --go` the run IS reached, once, for slot 1 — "
         "so the refusals above are refusals and not a command that can "
         "never run",
         f"spy reached {reached}")

    print("\n(g) >>> THE SABOTAGE DRILL, PERMANENT. INERT IS A FAIL.")

    def witness():
        return (judge(GOOD, MILD), judge([[0.0114, L] * 3] * 6, MILD),
                judge(TWENTY_NINE, MILD), judge(LOPSIDED, MILD),
                judge(WILD, ABYSS), judge(GOOD, RICH),
                judge(CHOP, (-0.2, 0.0, 0.0)),
                judge([[0.03, L] * 3] * 6, MILD),
                round(held_or(float('nan'), buy_and_hold,
                              calm(101.0, 99.0, 110.0)), 7),
                len(pool([('BTC-USD', A), ('ETH-USD', B), ('SOL-USD', A)])),
                round(held_or(float('nan'), buy_and_hold, two_moods(),
                              sl_atr_mult=SLOT1_SL_ATR,
                              tp_atr_mult=SLOT1_TP_ATR,
                              atr_period=SLOT1_ATR_PERIOD), 7))

    HONEST = witness()
    EXPECTED = (('PASSED', (True,) * 5),
                ('FAILED', (False, True, True, True, True)),
                ('FAILED', (True, False, True, True, True)),
                ('FAILED', (True, True, False, True, True)),
                ('FAILED', (True, True, True, False, True)),
                ('FAILED', (True, True, True, True, False)),
                ('FAILED', (True, True, False, False, False)),
                ('WITHHELD', (True,) * 5), 0.0244628, 6, 0.0019236)
    G = globals()
    _keep = {name: G[name] for name in
             ('BAR_MIN_PROFIT_FACTOR', 'BAR_MIN_TRADES', 'TOO_GOOD_PF',
              'walk_forward_trades', 'monte_carlo', 'compound', 'pool',
              'buy_and_hold', 'BAR_MAX_MC_DRAWDOWN', 'GAUNTLET_COSTS',
              'SLOT1_SL_ATR', 'SLOT1_ATR_PERIOD')}

    class _AlwaysConsistent:
        verdict = 'CONSISTENT'

    BREAKS = [
        ('G1', 'the Profit Factor bar lowered to 1.0',
         'BAR_MIN_PROFIT_FACTOR', 1.0),
        ('G2', 'the trade-count bar lowered to 20', 'BAR_MIN_TRADES', 20),
        ('G3', 'the too-good alarm raised out of reach', 'TOO_GOOD_PF', 99.0),
        ('G4', 'the walk-forward always saying CONSISTENT',
         'walk_forward_trades', lambda *a, **k: _AlwaysConsistent()),
        ('G5', 'the Monte Carlo always reporting no drawdown',
         'monte_carlo', lambda *a, **k: {'dd_p95': 0.0}),
        ('G6', 'results ADDED instead of compounded', 'compound',
         lambda fractions: float(sum(float(f) for f in fractions))),
        ('G7', 'the pool quietly dropping the third coin', 'pool',
         lambda coins: _keep['pool'](list(coins)[:2])),
        ('G8', 'the buy-and-hold yardstick ignoring the 25% cap',
         'buy_and_hold', lambda df, **k: _keep['buy_and_hold'](df) * 1.334),
        ('G9', 'the drawdown bar loosened to 99%', 'BAR_MAX_MC_DRAWDOWN',
         99.0),
        ('G10', "the Lab's old fee, 0.1% a side, charged again",
         'GAUNTLET_COSTS', {'fee_pct': 0.001, 'slippage_pct': 0.0005}),
        ('G11', "Slot 1's stop back to 1.5 ranges", 'SLOT1_SL_ATR', 1.5),
        ('G12', "Slot 1's range worked on 14 candles again",
         'SLOT1_ATR_PERIOD', 14),
    ]
    print()
    for tag, words, name, replacement in BREAKS:
        G[name] = replacement
        try:
            broken = witness()
        except Exception:                                  # noqa: BLE001
            broken = '<crashed>'
        finally:
            G[name] = _keep[name]
        changed = broken != HONEST
        caught = broken != EXPECTED
        good = changed and caught
        verdict = ('CAUGHT' if good else
                   'INERT — IT CHANGED NOTHING' if not changed else
                   'ESCAPED — THE GATE IS DECORATIVE')
        mark(good, f"{tag} {words:<52} -> {verdict}")
    mark(all(G[name] is original for name, original in _keep.items())
         and witness() == HONEST == EXPECTED,
         "and after twelve breaks everything is what it started as, and "
         "the eleven witnessed answers equal the eleven typed out here")

    print("\n(h) THE VAULT WAS NEVER OPENED, AND THE GATE COUNTS ITSELF.")
    engine.load_vault = _real_door
    shutil.rmtree(WORK, ignore_errors=True)
    mark(VAULT_OPENED == []
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE
         and (TRAIN_END, ASSETS, TIMEFRAME, BAR_MIN_PROFIT_FACTOR,
              BAR_MIN_TRADES, BAR_WALK_FORWARD, BAR_MAX_MC_DRAWDOWN,
              TOO_GOOD_PF, TOO_GOOD_WIN_PCT)
         == ('2025-10-01', ('BTC-USD', 'ETH-USD', 'SOL-USD'), '4h', 1.15,
             30, 'CONSISTENT', 30.0, 2.0, 70.0)
         and GAUNTLET_COSTS == {'fee_pct': 0.0005, 'slippage_pct': 0.0005}
         and LAB_COSTS == {'fee_pct': 0.001, 'slippage_pct': 0.0005}
         and engine.LAB_COSTS is LAB_COSTS
         and (SLOT1_SL_ATR, SLOT1_TP_ATR, SLOT1_ATR_PERIOD) == (3.75, 5.0, 84)
         and (RISK_CONFIG['default_sl_atr'], RISK_CONFIG['default_tp_atr'],
              engine.ATR_PERIOD) == (1.5, 2.0, 14)
         and SLOT1_SL_ATR == 1.5 * 2.5 and SLOT1_TP_ATR == 2.0 * 2.5
         and SLOT1_ATR_PERIOD == 14 * 6,
         "the Lab's real door was never knocked on, the real results "
         "folder is unchanged, AND EVERY LOCKED NUMBER — the line, the "
         "coins, the timeframe, the five bars, the alarm, THE GAUNTLET's "
         "COSTS (0.05% + 0.05%), the Lab's own unchanged costs (0.1% + "
         "0.05%), Slot 1's exit (3.75, 5.0, 84 = the ship's 1.5, 2.0 and 14 "
         "times 2.5, 2.5 and 6) and the ship's own default exit — equals a "
         "number typed out in this gate",
         f"vault calls: {len(VAULT_OPENED)}")
    mark(len(BREAKS) == 12, "twelve breaks, counted against a number "
                            "typed out here")
    EXPECTED_CHECKS = 49
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.4-R PASSED — {len(nonlocal_ok)} checks, 0 red.

EACH OF THE FIVE BARS WAS FORCED RED ALONE on hand-made trades, with
the other four green, so no bar can hide behind another; the trade
count was tested at 29 and at 30.

B5's YARDSTICK EQUALS ARITHMETIC TYPED OUT BY HAND, with the 25% cap
binding and with it not binding, at the Commander's real fee (0.05% a
side) - and, for Slot 1, sized on the 84-candle range.

EVERY EVIDENCE ROW CARRIES THE FINGERPRINT OF THE DECLARED COSTS AND
SLOT 1's DAY-SIZED EXIT (stop 3.75, target 5.0, range over 84 candles).

THE WHOLE RUN WAS REHEARSED on three made-up coins of 5,624 four-hour
candles, the vault's own shape, through the Lab's real engine: the
marker went down before the 4-hour files were asked for, the
pooled count equals the three coins' evidence files added up, the
Profit Factor on the report equals the one re-worked from the saved
file, a second run was refused, and a coin on different days stopped
the run with no verdict - here a coin ONE CANDLE short.

WHAT THIS GATE DOES **NOT** PROVE. It has never seen a real candle and
says NOTHING about what the real run will find. It rehearses the
machinery; it does not review the DESIGN - the pooling of three coins
that move together, the yardstick's definition, twenty candles rather
than twenty days and the 10-week filter are choices made by the same
author, and no second AI has read them.""")
    else:
        print(f"GATE 6.4-R FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
