"""
Zar X Lab — THE GAUNTLET RUNNER FOR SLOT 3, the crowd-mood fade.
The one run that counts.

**THE PROMISE: exactly three sealed slots, then the signals chapter closes.**
This file runs Slot 3, ONCE, and prints one verdict. Slot 3 was the on-chain
cycle thermometer; the Commander re-specified it ONCE, on 2026-11-16, before
any slot had been run. Its rules were declared in PROGRESS_LOG.md that night
and committed with no code, before this file existed.

**IT IS THE SLOT 2 RUNNER WITH THE MOOD IN PLACE OF THE FUNDING, AND IT
CHANGES NEITHER SLOT 1 NOR SLOT 2 BY ONE BYTE.** `lab/gauntlet.py` is
imported, not edited: the five bars (`battery`), the pooling (`pool`), the
buy-and-hold yardstick (`buy_and_hold`) and the marker's name are THE SAME
OBJECTS Slot 1 uses, and this file's gate proves it.

WHAT IT DOES, in order:

  1. Refuses to run without `--go`, typed on purpose.
  2. Refuses to run if the slot's marker file exists: THE SLOT IS SPENT.
  3. **THE PRE-FLIGHT - EVERYTHING THAT CAN BE REFUSED BEFORE THE SLOT IS
     SPENT.** The frozen mood is verified against its checksum and loaded;
     and the daily vault's shape is read from its manifest (no candle is
     opened). **A REFUSAL HERE WRITES NO MARKER AND SPENDS NOTHING.**
  4. WRITES THE MARKER. Only then is the vault opened.
  5. Joins each day's mood onto that day's candle, as two more columns
     (`lab/mood_vault.py`: the value stamped day D goes on the candle that
     opens on day D). ALL THREE COINS GET THE SAME MOOD - there is one
     index for the whole market. **A candle with no mood stops the run
     with no verdict.**
  6. Runs the strategy through the Lab's own engine (`lab/engine.py`,
     unchanged) on each coin's DAILY vault file, hold-out line 2025-10-01.
  7. POOLS the three coins' hold-out trades into one list and measures the
     five locked bars on it. **ONE VERDICT FOR THE SLOT.**
  8. Sounds the too-good alarm (Profit Factor above 2.0 or win rate above
     70%): the verdict is then WITHHELD.

**WHAT THIS TEST CANNOT SAY.** One index, three coins: the pooled trades are
nearly one bet, three times. The index is partly made from price. It is a
publisher's number, and Bitcoin's. All said in the bar, before any result.

**THE COSTS ARE THE COMMANDER'S REAL ONES**: Binance futures taker fee 0.05%
a side and slippage 0.05% a side, `config.GAUNTLET_COSTS`. **THE EXIT IS THE
SHIP'S OWN DEFAULT** - 1.5 and 2.0 times the 14-candle range.

**WHAT A PASS MEANS AND DOES NOT MEAN.** A place in Phase 7's proving voyage,
on paper. Not proof it makes money. The Lab's numbers catch overfitting and
CANNOT catch a leak (Law 7).

RUN (from the zar-x folder):
    python lab/gauntlet_slot3.py --gate      (rehearsal on made-up data)
    python lab/gauntlet_slot3.py --go        (THE RUN. ONCE.)
"""
import json
import os
import sys
from datetime import datetime

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(LAB_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, LAB_DIR)

import engine                                              # noqa: E402
import mood_vault                                          # noqa: E402
from config import GAUNTLET_COSTS, LAB_COSTS, RISK_CONFIG  # noqa: E402
import gauntlet as slot1                                   # noqa: E402
from mood_vault import attach, preflight                   # noqa: E402
from gauntlet import (battery, buy_and_hold, holdout_index,  # noqa: E402
                      marker_path, pool, report_lines)

SLOT = 3
TRAIN_END = '2025-10-01'        # the hold-out line, fixed in Phase 2
ASSETS = ('BTC-USD', 'ETH-USD', 'SOL-USD')
TIMEFRAME = '1d'


def slot_strategy():
    """The strategy sealed into Slot 3."""
    from signals.mood_fade import MoodFade
    return MoodFade()


def vault_shape(manifest_path=None):
    """The daily vault's shape, read from its MANIFEST ALONE - no candle is
    opened. Raises RuntimeError('REFUSED ...') unless every coin's daily
    file is the 1,094 days the frozen mood was cut for."""
    path = (os.path.join(engine.VAULT_DIR, 'MANIFEST.json')
            if manifest_path is None else manifest_path)
    try:
        with open(path, encoding='utf-8') as handle:
            files = json.load(handle)['files']
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(f'REFUSED: the vault\'s manifest cannot be read '
                           f'({type(exc).__name__}).')
    for asset in ASSETS:
        entry = files.get(f'{asset}_{TIMEFRAME}.csv')
        entry = entry if isinstance(entry, dict) else {}
        if (entry.get('rows') != mood_vault.DAYS
                or not str(entry.get('first_candle', '')).startswith(
                    mood_vault.FIRST_DAY)
                or not str(entry.get('last_candle', '')).startswith(
                    mood_vault.LAST_DAY)):
            raise RuntimeError(
                f'REFUSED: the vault\'s {asset} daily file is not the '
                f'{mood_vault.DAYS} days {mood_vault.FIRST_DAY} to '
                f'{mood_vault.LAST_DAY} that the frozen mood covers.')


def all_covered(df):
    """Does every candle carry a mood value AND a side?"""
    return not bool(df['mood'].isna().any() or df['mood_side'].isna().any())


def run_slot3(loader=None, results_dir=None, mood_dir=None,
              manifest_path=None, out=print):
    """THE RUN. Pre-flight, then the marker, then the vault, then the
    verdict.

    The four arguments exist so the gate can rehearse this whole function
    on made-up candles and a made-up mood in temporary folders. The real
    run passes none and gets the vault, the frozen mood and
    `lab/results/`.
    """
    loader = engine.load_vault if loader is None else loader
    results_dir = engine.RESULTS_DIR if results_dir is None else results_dir
    os.makedirs(results_dir, exist_ok=True)
    marker = marker_path(SLOT, results_dir)
    if os.path.exists(marker):
        raise RuntimeError(
            f'REFUSED: slot {SLOT} is SPENT ({marker}). THE PROMISE allows '
            f'each slot one run. A second run needs the Commander\'s ruling '
            f'written in PROGRESS_LOG.md first.')
    strategy = slot_strategy()

    # THE PRE-FLIGHT. A REFUSAL HERE SPENDS NOTHING.
    mood = preflight(mood_dir)
    vault_shape(manifest_path)

    # THE MARKER GOES DOWN BEFORE THE VAULT IS OPENED.
    with open(marker, 'x', encoding='utf-8') as handle:
        handle.write(f'GAUNTLET SLOT {SLOT} — SPENT\n'
                     f'strategy  : {strategy.name}\n'
                     f'params    : {strategy.params}\n'
                     f'commit    : {engine.git_commit()}\n'
                     f'started   : {datetime.now().isoformat(timespec="seconds")}\n'
                     f'train_end : {TRAIN_END}\n')

    out(f'GAUNTLET SLOT {SLOT} — {strategy.name}')
    out(f'  marker written: {marker}')
    out(f'  coins {", ".join(ASSETS)}  timeframe {TIMEFRAME}  hold-out '
        f'line {TRAIN_END}')

    # EVERY COIN IS LOADED AND GIVEN THE MOOD before any is judged. There
    # is ONE index for the whole market: all three coins get the same.
    loaded = []
    for asset in ASSETS:
        data = loader(asset, TIMEFRAME)
        data.df = attach(data.df, *mood)
        if not all_covered(data.df):
            raise RuntimeError(
                f'REFUSED: {asset} has candles with no mood. No verdict '
                f'is produced.')
        loaded.append((asset, data))

    per_asset, yardsticks, indexes, saved = [], [], [], []
    for asset, data in loaded:
        result = engine.run_backtest(
            data, strategy, strategy_name=strategy.name,
            params=strategy.params, train_end=TRAIN_END, verbose=False,
            costs=GAUNTLET_COSTS)
        saved.append(result.save_csv(results_dir))
        held = result.window_trades('holdout')
        per_asset.append((asset, held))
        indexes.append(holdout_index(data.df, TRAIN_END))
        yardsticks.append(buy_and_hold(data.df, TRAIN_END))
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
                               f'gauntlet_slot{SLOT}_pooled_holdout.csv')
    pooled.to_csv(pooled_path, index=False)
    result = battery(pooled, indexes[0], yardsticks)
    out('')
    out(f'  pooled hold-out trades: {len(pooled)}  '
        f'({", ".join(f"{a} {len(t)}" for a, t in per_asset)})')
    out(result['walk_forward'].text()
        if hasattr(result['walk_forward'], 'text') else '')
    for line in report_lines(SLOT, strategy.name, result):
        out(line)
    with open(marker, 'a', encoding='utf-8') as handle:
        handle.write(f'finished  : {datetime.now().isoformat(timespec="seconds")}\n'
                     f'verdict   : {result["verdict"]}\n')
    result['pooled'] = pooled
    result['saved'] = saved + [pooled_path]
    result['marker'] = marker
    return result


def main(argv, runner=None, results_dir=None):
    """`--go` runs the slot. Anything less refuses and touches nothing.
    `runner` and `results_dir` exist so the gate can prove a refusal never
    reaches the run, with a spy standing where the run would be."""
    runner = run_slot3 if runner is None else runner
    results_dir = engine.RESULTS_DIR if results_dir is None else results_dir
    if '--go' not in argv:
        print('REFUSED. The gauntlet runs Slot 3 ONCE, and only when asked '
              'on purpose:')
        print('    python lab/gauntlet_slot3.py --go')
        print('Nothing was opened and nothing was written.')
        return 2
    lines = []

    def out(line=''):
        print(line)
        lines.append(str(line))

    try:
        result = runner(out=out)
    finally:
        os.makedirs(results_dir, exist_ok=True)
        log = os.path.join(results_dir, f'gauntlet_slot{SLOT}_report.txt')
        with open(log, 'a', encoding='utf-8') as handle:
            handle.write('\n'.join(lines) + '\n')
    return 0 if result['verdict'] == 'PASSED' else 1


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        sys.exit(main(sys.argv[1:]))

    # =====================================================================
    # GATE 6.5-R — THE SLOT 3 RUNNER'S REHEARSAL. Declared in
    # PROGRESS_LOG.md on 2026-11-16 (late night) and committed with no
    # code, before this file existed.
    #
    # **IT NEVER OPENS THE VAULT OR ANY REAL FROZEN FOLDER.** The Lab's door
    # is replaced by one that raises; every candle and every mood value
    # below is made up; every result is written into a temporary folder.
    # =====================================================================
    import shutil
    import tempfile

    import numpy as np
    import pandas as pd

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def text_of(path):
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
    REAL_MOOD = os.path.abspath(mood_vault.MOOD_DIR)
    FILES_READ = []
    _real_sha, _real_read_rows = mood_vault._sha, mood_vault.read_rows

    def _spy_sha(path):
        FILES_READ.append(os.path.abspath(path))
        return _real_sha(path)

    def _spy_read_rows(path):
        FILES_READ.append(os.path.abspath(path))
        return _real_read_rows(path)

    mood_vault._sha, mood_vault.read_rows = _spy_sha, _spy_read_rows
    WORK = tempfile.mkdtemp(prefix='zarx_slot3_')

    # THE DAILY VAULT'S OWN SHAPE, TYPED OUT: 1,094 candles from 2023-07-28
    # to 2026-07-25; 797 training; 297 hold-out, the first 2025-10-02.
    ONE_DAY = pd.Timedelta(days=1)
    DAYS = pd.date_range('2023-07-28', periods=1094, freq=ONE_DAY)
    HOLD = pd.date_range('2025-10-02', periods=297, freq=ONE_DAY)
    STARTS = [(k * 297) // 6 for k in range(6)]     # 0 49 99 148 198 247

    print("=" * 70)
    print("GATE 6.5-R — THE SLOT 3 RUNNER, REHEARSED. Made-up candles and a")
    print("made-up mood. The vault and the frozen folders are never opened.")
    print("=" * 70)

    print("\n(a) THE LOCKED NUMBERS, AND THE FIVE BARS ARE SLOT 1's OWN.")
    mark((SLOT, TRAIN_END, ASSETS, TIMEFRAME)
         == (3, '2025-10-01', ('BTC-USD', 'ETH-USD', 'SOL-USD'), '1d')
         and (slot1.BAR_MIN_PROFIT_FACTOR, slot1.BAR_MIN_TRADES,
              slot1.BAR_WALK_FORWARD, slot1.BAR_MAX_MC_DRAWDOWN,
              slot1.TOO_GOOD_PF, slot1.TOO_GOOD_WIN_PCT)
         == (1.15, 30, 'CONSISTENT', 30.0, 2.0, 70.0)
         and marker_path(3, 'x').endswith('GAUNTLET_SLOT_3_SPENT.txt')
         and GAUNTLET_COSTS == {'fee_pct': 0.0005, 'slippage_pct': 0.0005}
         and GAUNTLET_COSTS is slot1.GAUNTLET_COSTS
         and LAB_COSTS == {'fee_pct': 0.001, 'slippage_pct': 0.0005}
         and (RISK_CONFIG['default_sl_atr'], RISK_CONFIG['default_tp_atr'],
              engine.ATR_PERIOD) == (1.5, 2.0, 14)
         and (slot1.SLOT1_SL_ATR, slot1.SLOT1_TP_ATR,
              slot1.SLOT1_ATR_PERIOD) == (3.75, 5.0, 84)
         and (mood_vault.DAYS, mood_vault.FIRST_DAY, mood_vault.LAST_DAY)
         == (1094, '2023-07-28', '2026-07-25'),
         "slot 3, the line 2025-10-01, three coins, DAILY candles; the five "
         "bars and the alarm; THE GAUNTLET's COSTS, 0.05% + 0.05% a side, "
         "the same object Slot 1 holds; the ship's own exit, 1.5 and 2.0 "
         "times the 14-candle range, which is NOT Slot 1's; the frozen "
         "mood's 1,094 days — every one equal to a number typed out here")
    mark(battery is slot1.battery and pool is slot1.pool
         and buy_and_hold is slot1.buy_and_hold
         and holdout_index is slot1.holdout_index
         and marker_path is slot1.marker_path
         and report_lines is slot1.report_lines
         and attach is mood_vault.attach
         and preflight is mood_vault.preflight,
         "THE FIVE BARS, THE POOL, THE YARDSTICK AND THE REPORT ARE THE VERY "
         "SAME OBJECTS `lab/gauntlet.py` HOLDS for Slot 1 — imported, not "
         "copied — and the join and the pre-flight are the frozen mood's "
         "own")

    def trades(per_window):
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

    MILD = (0.01, 0.0, -0.005)
    W, L = 0.012, -0.010
    GOOD = [[W, L] * 3] * 6
    TWENTY_NINE = [[W, L, W, L, W]] * 5 + [[W, L, W, L]]
    hand = (judge(GOOD, MILD), judge([[0.0114, L] * 3] * 6, MILD),
            judge(TWENTY_NINE, MILD), judge([[0.03, L] * 3] * 6, MILD))
    mark(hand == (('PASSED', (True,) * 5),
                  ('FAILED', (False, True, True, True, True)),
                  ('FAILED', (True, False, True, True, True)),
                  ('WITHHELD', (True,) * 5)),
         "and they still judge as declared on the daily hold-out's 297 "
         "candles: Profit Factor 1.20 PASSED; 1.14 FAILED on that bar "
         "alone; 29 trades FAILED on the count alone; 3.0 WITHHELD",
         f"{hand}")

    print("\n(b) THE MADE-UP WORLD WEARS THE DAILY VAULT'S OWN SHAPE.")

    def made_up(seed, candles=1094):
        rng = np.random.default_rng(seed)
        price, rows = 100.0, []
        for _ in range(candles):
            steps = price * np.exp(np.cumsum(
                rng.normal(0.0, 0.035 / np.sqrt(24), 24)))
            rows.append((price, max(price, steps.max()),
                         min(price, steps.min()), float(steps[-1])))
            price = float(steps[-1])
        index = pd.date_range('2023-07-28', periods=candles, freq=ONE_DAY)
        return pd.DataFrame(rows, columns=['open', 'high', 'low', 'close'],
                            index=index)

    # A MADE-UP PUBLISHER's BANDS, for made-up values only, typed out here
    # and nowhere in the production code.
    def label_of(value):
        return ('Extreme Fear' if value <= 25 else 'Fear' if value <= 46
                else 'Neutral' if value <= 54 else 'Greed' if value <= 75
                else 'Extreme Greed')

    SIDE_OF = {'Extreme Fear': -1, 'Fear': -1, 'Neutral': 0, 'Greed': 1,
               'Extreme Greed': 1}

    def made_up_mood(seed, poison_from=None, poison_seed=None):
        """1,094 made-up index values, 0 to 100, that wander and cluster.
        With `poison_from` (a day number) every value from that day on is
        drawn again from a different seed."""
        def draw(rng):
            level, out = 50.0, []
            for _ in range(1094):
                level = 0.96 * level + 0.04 * 50.0 + rng.normal(0, 5.0)
                out.append(int(max(0, min(100, round(level)))))
            return out
        values = draw(np.random.default_rng(seed))
        if poison_from is not None:
            values = values[:poison_from] + draw(
                np.random.default_rng(poison_seed))[poison_from:]
        return values

    def rows_of(values):
        return [(str(day.date()), int(value), label_of(value), 0)
                for day, value in zip(DAYS, values)]

    shape = made_up(11)
    shape_hold = holdout_index(shape)
    mark(len(shape) == 1094 and len(shape_hold) == 297
         and shape.index.equals(DAYS) and shape_hold.equals(HOLD)
         and shape_hold[0] == pd.Timestamp('2025-10-02')
         and shape.index[-1] == pd.Timestamp('2026-07-25'),
         "1,094 daily candles from 2023-07-28 to 2026-07-25: 797 training "
         "and 297 hold-out, the hold-out opening on 2025-10-02",
         f"{len(shape)} candles, {len(shape_hold)} hold-out")

    SEEDS = {'BTC-USD': 11, 'ETH-USD': 22, 'SOL-USD': 33}
    MOOD_SEED = 505
    POISON_DAY = 900                    # 2026-01-13: inside the hold-out
    MOOD = made_up_mood(MOOD_SEED)

    def freeze(name, poison=False):
        folder = os.path.join(WORK, name)
        values = made_up_mood(MOOD_SEED, POISON_DAY if poison else None,
                              MOOD_SEED + 7)
        mood_vault.write_freeze(folder, rows_of(values))
        return folder

    def manifest(name, rows=1094, first='2023-07-28 00:00:00',
                 last='2026-07-25 00:00:00'):
        path = os.path.join(WORK, name)
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump({'files': {f'{asset}_1d.csv': {
                'rows': rows, 'first_candle': first, 'last_candle': last}
                for asset in ASSETS}}, handle)
        return path

    FREEZE = freeze('freeze')
    MANIFEST = manifest('vault_manifest.json')

    def fake_door(log, folder, short=None, extra=None):
        def door(asset, timeframe):
            log.append((asset, timeframe,
                        os.path.exists(marker_path(3, folder))))
            data = engine.VaultData.__new__(engine.VaultData)
            data.asset, data.timeframe = asset, timeframe
            data.path = f'<made up: {asset}>'
            data.report, data.verdict = None, 'PASS'
            candles = (1093 if asset == short else
                       1095 if asset == extra else 1094)
            data.df = made_up(SEEDS[asset], candles=candles)
            return data
        return door

    _room = [0]

    def rehearse(mood_dir=None, manifest_path=None, short=None,
                 extra=None, folder=None):
        if folder is None:
            _room[0] += 1
            folder = os.path.join(WORK, f'run_{_room[0]}')
        knocks, said = [], []
        try:
            result = run_slot3(
                loader=fake_door(knocks, folder, short, extra),
                results_dir=folder,
                mood_dir=FREEZE if mood_dir is None else mood_dir,
                manifest_path=(MANIFEST if manifest_path is None
                               else manifest_path),
                out=said.append)
            died = ''
        except Exception as exc:                           # noqa: BLE001
            result, died = None, f'{type(exc).__name__}: {exc}'
        return result, died, knocks, said, folder

    print("\n(c) >>> THE PRE-FLIGHT REFUSES BEFORE THE MARKER, AND A REFUSAL"
          "\n    SPENDS NOTHING.")
    damaged = os.path.join(WORK, 'damaged')
    shutil.copytree(FREEZE, damaged)
    target = os.path.join(damaged, mood_vault.FILE_NAME)
    with open(target, 'rb') as handle:
        raw = bytearray(handle.read())
    at = raw.rindex(b',', 0, raw.rindex(b',', 0, raw.rindex(b','))) + 1
    raw[at] = ord('7') if raw[at] != ord('7') else ord('8')
    with open(target, 'wb') as handle:
        handle.write(bytes(raw))
    main_room = os.path.join(WORK, 'the_run')

    def refused_clean(outcome):
        _result, died, knocks, _said, folder = outcome
        return (died.startswith('RuntimeError: REFUSED') and knocks == []
                and not os.path.exists(marker_path(3, folder)))

    r_damaged = rehearse(mood_dir=damaged, folder=main_room)
    mark(refused_clean(r_damaged) and 'not intact' in r_damaged[1],
         "ONE DIGIT of one frozen value changed: REFUSED - and NO MARKER was "
         "written and the candles were never asked for", r_damaged[1][:88])
    r_absent = rehearse(mood_dir=os.path.join(WORK, 'no_such_freeze'),
                        folder=main_room)
    mark(refused_clean(r_absent),
         "no frozen mood at all: REFUSED, no marker, no knock",
         r_absent[1][:88])
    r_shape = rehearse(manifest_path=manifest('short.json', rows=1093),
                       folder=main_room)
    r_dates = rehearse(manifest_path=manifest(
        'late.json', first='2023-07-29 00:00:00'), folder=main_room)
    r_ends = rehearse(manifest_path=manifest(
        'early.json', last='2026-07-24 00:00:00'), folder=main_room)
    r_nomanifest = rehearse(manifest_path=os.path.join(WORK, 'none.json'),
                            folder=main_room)
    mark(refused_clean(r_shape) and refused_clean(r_dates)
         and refused_clean(r_nomanifest) and refused_clean(r_ends)
         and 'daily file is not' in r_shape[1]
         and 'daily file is not' in r_ends[1],
         "a vault manifest that says 1,093 days, one that starts a day "
         "late, one that ends a day early, and one that is missing: each "
         "REFUSED, no marker, no knock", r_shape[1][:88])

    print("\n(d) >>> THE WHOLE RUN, IN THE SAME FOLDER THOSE SIX REFUSALS"
          "\n    LEFT UNSPENT, THROUGH THE LAB'S REAL ENGINE.")
    JUDGED_ON = []
    _slot1_battery = battery

    def _watching(pooled, index, yardsticks):
        JUDGED_ON.append((len(pooled), index, list(yardsticks)))
        return _slot1_battery(pooled, index, yardsticks)

    battery = _watching
    try:
        rehearsal, died, knocks, said, folder = rehearse(folder=main_room)
    finally:
        battery = _slot1_battery
    mark(died == '' and rehearsal is not None
         and rehearsal['verdict'] in ('PASSED', 'FAILED', 'WITHHELD'),
         "after six refusals the slot was still unspent: the whole run "
         "completed on three made-up coins and reached a verdict",
         died or f"verdict on made-up data: {rehearsal['verdict']} "
                 f"(it means NOTHING about the real coins)")
    mark([k[:2] for k in knocks] == [('BTC-USD', '1d'), ('ETH-USD', '1d'),
                                     ('SOL-USD', '1d')]
         and all(k[2] for k in knocks),
         "THE MARKER WAS ALREADY DOWN WHEN THE CANDLES WERE FIRST ASKED "
         "FOR: three knocks, in the coins' fixed order, FOR THE DAILY "
         "FILES", f"{knocks}")

    said_text = '\n'.join(str(line) for line in said)
    evidence = []
    if rehearsal is not None:
        for path in rehearsal['saved']:
            rows = held_or(pd.DataFrame(), pd.read_csv, path)
            if 'fingerprint' in rows.columns and 'window' in rows.columns:
                evidence.append(rows)
    by_coin = {str(rows['asset'].iloc[0]): rows
               for rows in evidence if len(rows)}
    recount = sum(int((rows['window'] == 'holdout').sum())
                  for rows in evidence)
    pooled_csv = (held_or(pd.DataFrame(), pd.read_csv, rehearsal['saved'][-1])
                  if rehearsal is not None else pd.DataFrame())
    mark(rehearsal is not None and len(evidence) == 3
         and sorted(by_coin) == sorted(ASSETS)
         and recount == len(pooled_csv) == len(rehearsal['pooled'])
         and recount >= 30
         and f'pooled hold-out trades: {recount} ' in said_text,
         "THE POOLED COUNT IS THE THREE COINS' HOLD-OUT TRADES ADDED UP — "
         "recounted from the three per-coin evidence files — and the "
         "made-up world holds at least 30 of them",
         f"{ {k: int((v['window'] == 'holdout').sum()) for k, v in by_coin.items()} } "
         f"-> {recount}")
    if len(pooled_csv):
        r = pooled_csv['return_pct'].astype(float)
        by_hand_pf = r[r > 0].sum() / -r[r <= 0].sum()
        by_hand_whole = float(np.prod(1.0 + r.values)) - 1.0
        times = list(pd.to_datetime(pooled_csv['entry_time']))
    else:
        by_hand_pf, by_hand_whole, times = float('nan'), float('nan'), []
    mark(rehearsal is not None and len(pooled_csv) > 0
         and f'{by_hand_pf:.2f}' == rehearsal['rows'][0][1]
         and f'{100 * by_hand_whole:+.2f}%' == rehearsal['rows'][4][1]
         and times == sorted(times)
         and all(t > pd.Timestamp('2025-10-01') for t in times),
         "the Profit Factor and the compounded result on the report equal "
         "the same figures RE-WORKED HERE from the saved pooled file; the "
         "pooled trades are in time order; every one entered AFTER the line",
         f"PF {by_hand_pf:.2f}, whole {100 * by_hand_whole:+.2f}%")
    verdict_by_hand = (
        'FAILED' if rehearsal is None
        or not all(ok for _b, _g, _n, ok in rehearsal['rows'])
        else 'WITHHELD' if rehearsal['alarm'] else 'PASSED')
    marker_text = text_of(marker_path(3, main_room))
    mark(rehearsal is not None and rehearsal['verdict'] == verdict_by_hand
         and (f'SLOT 3 {verdict_by_hand}' in said_text
              or 'VERDICT: WITHHELD' in said_text)
         and 'GAUNTLET SLOT 3' in said_text
         and 'mood-fade-1d-90d-top10' in marker_text
         and f'verdict   : {verdict_by_hand}' in marker_text
         and 'train_end : 2025-10-01' in marker_text
         and not os.path.exists(marker_path(2, main_room))
         and not os.path.exists(marker_path(1, main_room)),
         "the verdict printed is the one its own five rows imply, it is "
         "printed FOR SLOT 3, the marker names the strategy, the line and "
         "that verdict — and no marker for Slot 1 or Slot 2 was written")
    mark(len(JUDGED_ON) == 1 and JUDGED_ON[0][0] == recount
         and JUDGED_ON[0][1] is not None and len(JUDGED_ON[0][2]) == 3
         and pd.DatetimeIndex(JUDGED_ON[0][1]).equals(HOLD)
         and battery is slot1.battery,
         "THE FIVE BARS WERE HANDED, ONCE: every pooled trade, three "
         "yardsticks, and THE HOLD-OUT'S OWN 297 CANDLES for the "
         "walk-forward to be cut on",
         f"{[(n, None if i is None else len(i), len(y)) for n, i, y in JUDGED_ON]}")

    print("\n(e) >>> HOW THE ENGINE WAS CALLED, AND THAT EVERY TRADE IS WHERE"
          "\n    THE RULE PUTS IT.")
    DECLARED = {'window': 90, 'need': 81, 'warmup': 91, 'value': 'mood',
                'side': 'mood_side', 'kind': 'crowd_mood_fade',
                '_costs': {'fee_pct': 0.0005, 'slippage_pct': 0.0005},
                '_risk_pct': 0.01, '_sl_atr': 1.5, '_tp_atr': 2.0,
                '_atr_period': 14, '_capital': 10000.0,
                '_train_end': '2025-10-01 00:00:00'}
    WANT_PRINT = engine.fingerprint('mood-fade-1d-90d-top10', DECLARED)
    prints = sorted({str(value) for rows in evidence
                     for value in rows['fingerprint'].unique()})
    mark(len(evidence) == 3 and all(len(rows) > 0 for rows in evidence)
         and prints == [WANT_PRINT],
         "EVERY EVIDENCE ROW OF ALL THREE COINS carries one fingerprint, "
         "and it equals the hash of the DECLARED settings typed out here: "
         "the mood fade — 90 days, 81 of them, warm-up 91 — fee 0.05%, "
         "slippage 0.05%, risk 1%, stop 1.5 ATR, target 2.0 ATR over 14 "
         "candles, capital 10,000, line 2025-10-01",
         f"declared {WANT_PRINT}, on the evidence {prints}")
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
            right_way = ((t['stop_loss'] < fill < t['take_profit']) if long
                         else (t['take_profit'] < fill < t['stop_loss']))
            fine = (abs(t['entry_price_fill'] - fill) < 1e-9 * fill
                    and abs(t['exit_price_fill'] - out_fill) < 1e-9 * out_fill
                    and abs(t['fees_paid'] - fees) < 1e-9 * max(fees, 1)
                    and abs(stop_gap - 1.5 * t['atr_at_entry']) < 1e-9 * fill
                    and abs(target_gap - 2.0 * t['atr_at_entry']) < 1e-9 * fill
                    and right_way
                    and t['position_value'] <= 0.25 * equity + 1e-6
                    and (abs(risked - 0.01 * equity) < 1e-6
                         or (is_capped and risked < 0.01 * equity)))
            if not fine:
                bad.append(int(t['trade_no']))
    mark(seen_rows == recount and seen_rows > 0 and not bad,
         "and EVERY HOLD-OUT TRADE'S OWN ROW says the same, re-worked here: "
         "filled 0.05% worse on both sides, a fee of 0.05% on both sides, "
         "the stop 1.5 ATR away on the losing side and the target 2.0 on "
         "the winning one, and the money at risk EXACTLY 1% of equity "
         "unless the 25% cap bound it lower",
         f"{seen_rows} trades re-worked, {capped_rows} of them capped, "
         f"{len(bad)} wrong {bad[:5]}")

    def rule_by_hand(values, at):
        """The rule a THIRD time (the strategy; its own gate's reference;
        this), in plain Python, with the side worked from this gate's own
        made-up bands."""
        if at < 90:
            return 'flat'
        today, ninety = values[at], values[at - 90:at]
        side = SIDE_OF[label_of(today)]
        if side == -1 and sum(1 for v in ninety if v > today) >= 81:
            return 'long'
        if side == 1 and sum(1 for v in ninety if v < today) >= 81:
            return 'short'
        return 'flat'

    SIGNALS = [rule_by_hand(MOOD, at) for at in range(1094)]
    DAY_OF = {day: n for n, day in enumerate(DAYS)}

    def walk_coin(asset, rows, signals):
        """A coin's evidence rows against the signal days worked by hand ->
        faults (empty = every trade is where the rule puts it, and no
        signal was passed over while flat)."""
        faults, free_from = [], 0
        for _i, t in rows.sort_values('trade_no').iterrows():
            entry = DAY_OF[pd.Timestamp(t['entry_time'])]
            exit_at = DAY_OF[pd.Timestamp(t['exit_time'])]
            first = next((j for j in range(free_from, 1093)
                          if signals[j] != 'flat'), None)
            if first is None or first + 1 != entry \
                    or signals[first] != t['direction']:
                faults.append((asset, int(t['trade_no'])))
            free_from = exit_at
        if any(signals[j] != 'flat' for j in range(free_from, 1093)):
            faults.append((asset, 'a signal after the last trade'))
        return faults

    faults, sides, firsts = [], set(), set()
    for asset in ASSETS:
        if asset not in by_coin:
            faults.append((asset, 'no evidence'))
            continue
        faults += walk_coin(asset, by_coin[asset], SIGNALS)
        sides |= set(by_coin[asset]['direction'])
        firsts.add((str(by_coin[asset]['entry_time'].iloc[0]),
                    str(by_coin[asset]['direction'].iloc[0])))
    mark(not faults and sides == {'long', 'short'} and len(firsts) == 1
         and SIGNALS.count('long') >= 20 and SIGNALS.count('short') >= 20,
         "EVERY TRADE OF EVERY COIN, TRAINING SIDE INCLUDED, IS WHERE THE "
         "RULE PUTS IT, RE-DERIVED BY HAND FROM THE MADE-UP MOOD: entered "
         "the day after the FIRST day, since the engine was last flat, "
         "that the hand-worked rule calls extreme, on that side — long and "
         "short both seen, no signal passed over; and all three coins' "
         "FIRST trade is on the same day and side, as one shared mood "
         "demands",
         f"{sum(len(v) for v in by_coin.values())} trades walked, "
         f"{len(faults)} faults {faults[:4]}; first trades {sorted(firsts)}")

    def yard_by_hand(df):
        first = int((df.index > pd.Timestamp('2025-10-01')).argmax())
        h, lo, c = (df['high'].values, df['low'].values, df['close'].values)
        ranges = [max(h[i] - lo[i], abs(h[i] - c[i - 1]),
                      abs(lo[i] - c[i - 1]))
                  for i in range(first - 14, first)]
        atr = sum(ranges) / 14
        fill = df['open'].values[first] * 1.0005
        size = min(100.0 / (1.5 * atr), 2500.0 / fill)
        out_fill = c[-1] * 0.9995
        return (size * (out_fill - fill)
                - 0.0005 * size * (fill + out_fill)) / 10000.0

    whole = 1.0
    for asset in ASSETS:
        whole *= 1.0 + yard_by_hand(made_up(SEEDS[asset]))
    WANT_YARD = f'> {100 * (whole - 1.0):+.2f}%'
    mark(rehearsal is not None and rehearsal['rows'][4][2] == WANT_YARD
         and sum('buy-and-hold yardstick for this coin' in str(line)
                 for line in said) == 3,
         "THE YARDSTICK THE RUN ACTUALLY USED is the buy-and-hold of the "
         "three made-up coins from the first hold-out candle, worked a "
         "second time here with plain arithmetic at a fee of 0.05%",
         f"by hand {WANT_YARD}, on the report "
         f"{rehearsal['rows'][4][2] if rehearsal is not None else '-'}")

    print("\n(f) >>> THE POISON TEST, THROUGH THE WHOLE RUN.")
    poisoned_run = rehearse(mood_dir=freeze('poisoned', poison=True))
    cut = DAYS[POISON_DAY]
    same_before, moved_after = 0, 0
    if poisoned_run[0] is not None and rehearsal is not None:
        for clean_path, dirty_path in zip(rehearsal['saved'][:3],
                                          poisoned_run[0]['saved'][:3]):
            clean_rows = pd.read_csv(clean_path)
            dirty_rows = pd.read_csv(dirty_path)
            keep = ['direction', 'entry_time', 'entry_price_raw',
                    'exit_time', 'exit_price_raw', 'size_units', 'net_pnl']
            a = clean_rows[pd.to_datetime(clean_rows['entry_time']) <= cut]
            b = dirty_rows[pd.to_datetime(dirty_rows['entry_time']) <= cut]
            same_before += int(len(a) > 0 and a[keep].reset_index(
                drop=True).equals(b[keep].reset_index(drop=True)))
            a2 = clean_rows[pd.to_datetime(clean_rows['entry_time']) > cut]
            b2 = dirty_rows[pd.to_datetime(dirty_rows['entry_time']) > cut]
            moved_after += int(list(a2['entry_time'])
                               != list(b2['entry_time']))
    mark(poisoned_run[1] == '' and same_before == 3 and moved_after >= 2,
         "EVERY MOOD VALUE FROM 2026-01-13 ON IS REPLACED and the whole run "
         "is made again: every trade entered up to that day is IDENTICAL, "
         "row for row, on all three coins — and the trades after it are "
         "not, so the poison was real",
         poisoned_run[1] or f"identical before: {same_before} of 3 coins; "
                            f"changed after: {moved_after} of 3")

    print("\n(g) >>> ONE RUN. THE SECOND IS REFUSED; A COIN ON DIFFERENT DAYS"
          "\n    OR A CANDLE WITH NO MOOD STOPS THE RUN BEFORE ANY VERDICT.")
    second = rehearse(folder=main_room)
    mark(second[1].startswith('RuntimeError: REFUSED') and 'SPENT' in second[1]
         and second[2] == [],
         "a SECOND run of the slot is REFUSED, and the candles were not "
         "even asked for", second[1][:90])
    third = rehearse(short='ETH-USD')
    marker3 = text_of(marker_path(3, third[4]))
    mark('do not cover the same hold-out days' in third[1]
         and not any('VERDICT' in str(line) for line in third[3])
         and 'SPENT' in marker3 and 'verdict' not in marker3,
         "a coin ONE CANDLE short stops the run with NO VERDICT printed and "
         "none written — and the slot is still marked spent, because the "
         "marker goes down first", third[1][:90])
    fourth = rehearse(extra='SOL-USD')
    marker4 = text_of(marker_path(3, fourth[4]))
    mark('has candles with no mood' in fourth[1]
         and not any('VERDICT' in str(line) for line in fourth[3])
         and not any('INFORMATION ONLY' in str(line) for line in fourth[3])
         and 'SPENT' in marker4 and 'verdict' not in marker4,
         "a coin with ONE CANDLE the frozen mood does not cover stops the "
         "run before ANY coin is judged: no card, no verdict",
         fourth[1][:90])
    reached = []

    def spy(out=None):
        reached.append('run')
        raise RuntimeError('the spy was reached')

    spy_room = os.path.join(WORK, 'spy')
    codes = [held_or('<crashed>', main, argv, runner=spy,
                     results_dir=spy_room)
             for argv in ([], ['--gate'], ['go'], ['--slot', '3'])]
    mark(codes == [2, 2, 2, 2] and reached == []
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE,
         "without `--go` the command REFUSES and THE RUN IS NEVER REACHED — "
         "proved with a spy standing where the run would be",
         f"exit codes {codes}, spy reached {reached}")
    went = held_or(None, main, ['--go'], runner=spy, results_dir=spy_room)
    mark(reached == ['run'] and str(went).startswith('<RuntimeError')
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE,
         "and WITH `--go` the run IS reached, once — so the refusals above "
         "are refusals and not a command that can never run",
         f"spy reached {reached}")

    print("\n(h) >>> THE SABOTAGE DRILL, PERMANENT. INERT IS A FAIL.")

    def summary(outcome):
        result, died, knocks, _said, _folder = outcome
        if result is None:
            return died[:40]
        rows = [pd.read_csv(path) for path in result['saved'][:3]]
        return (result['verdict'], len(result['pooled']),
                tuple(sorted({str(v) for part in rows
                              for v in part['fingerprint'].unique()})),
                tuple(str(part['entry_time'].iloc[0]) if len(part) else '-'
                      for part in rows),
                tuple(k[1] for k in knocks), result['rows'][4][2])

    def witness():
        return (summary(rehearse()),
                refused_clean(rehearse(mood_dir=damaged)),
                'has candles with no mood' in rehearse(extra='SOL-USD')[1])

    HONEST = witness()
    G = globals()
    _keep = {name: G[name] for name in
             ('TIMEFRAME', 'TRAIN_END', 'slot_strategy', 'preflight',
              'attach', 'battery', 'all_covered', 'vault_shape', 'pool',
              'buy_and_hold', 'GAUNTLET_COSTS')}
    GOOD_MOOD = mood_vault.preflight(FREEZE)

    def _tomorrow(df, days_ms, values, sides):
        return _keep['attach'](df, [d - 86400000 for d in days_ms] + [
            days_ms[-1]], list(values) + [50], list(sides) + [0])

    def _yesterday(df, days_ms, values, sides):
        return _keep['attach'](df, [days_ms[0]] + [d + 86400000
                                                   for d in days_ms],
                               [50] + list(values), [0] + list(sides))

    def _loose():
        from signals.mood_fade import MoodFade
        return MoodFade(need=80)

    def _rubber_stamp(pooled, index, yardsticks):
        honest = _keep['battery'](pooled, index, yardsticks)
        honest['verdict'] = 'PASSED'
        return honest

    BREAKS = [
        ('R1', 'the run asking for the 4-hour files', 'TIMEFRAME', '4h'),
        ('R2', 'the hold-out line moved back three months', 'TRAIN_END',
         '2025-07-01'),
        ('R3', 'the strategy built with 80 of 90, not 81', 'slot_strategy',
         _loose),
        ('R4', 'the pre-flight skipping the checksum', 'preflight',
         lambda directory=None: GOOD_MOOD),
        ('R5', "each candle given TOMORROW's mood", 'attach', _tomorrow),
        ('R6', "each candle given YESTERDAY's mood", 'attach', _yesterday),
        ('R7', 'the verdict rubber-stamped PASSED', 'battery',
         _rubber_stamp),
        ('R8', 'a candle with no mood waved through', 'all_covered',
         lambda df: True),
        ('R9', 'the pool quietly dropping the third coin', 'pool',
         lambda coins: _keep['pool'](list(coins)[:2])),
        ('R10', 'the yardstick set to nothing', 'buy_and_hold',
         lambda df, train_end=None: 0.0),
        ('R11', "the Lab's old fee, 0.1% a side, charged again",
         'GAUNTLET_COSTS', {'fee_pct': 0.001, 'slippage_pct': 0.0005}),
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
        good = broken != HONEST
        mark(good, f"{tag} {words:<48} -> "
                   f"{'CAUGHT' if good else 'INERT — IT CHANGED NOTHING'}")
    WANT_FIRST = (rehearsal['verdict'], recount, (WANT_PRINT,),
                  tuple(str(by_coin[a]['entry_time'].iloc[0]) for a in ASSETS)
                  if len(by_coin) == 3 else (), ('1d', '1d', '1d'),
                  WANT_YARD) if rehearsal is not None else None
    mark(all(G[name] is original for name, original in _keep.items())
         and witness() == HONEST
         and HONEST == (WANT_FIRST, True, True),
         "and after eleven breaks everything is what it started as; the "
         "witness's run is the rehearsal of (d) again — same verdict, same "
         "count, the declared fingerprint, the same first trades, three "
         "knocks for `1d`, the hand-worked yardstick — the damaged freeze "
         "is refused clean, and the candle with no mood stops the run")

    print("\n(i) NOTHING REAL WAS OPENED, AND THE GATE COUNTS ITSELF.")
    engine.load_vault = _real_door
    mood_vault._sha, mood_vault.read_rows = _real_sha, _real_read_rows
    shutil.rmtree(WORK, ignore_errors=True)
    mark(VAULT_OPENED == []
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE
         and len(FILES_READ) > 20
         and not any(path.startswith(REAL_MOOD) for path in FILES_READ)
         and 'funding_vault' not in sys.modules,
         "the Lab's real door was never knocked on, the real results "
         "folder is unchanged, of every mood file this gate read NOT ONE is "
         "in the real frozen folder, and the frozen funding's reader was "
         "never even loaded",
         f"vault calls: {len(VAULT_OPENED)}; mood files read: "
         f"{len(FILES_READ)}, all temporary")
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        production = handle.read().split("if __name__ == '__main__':")[0]
    mark(not any(word in production for word in
                 ('requests', 'urllib', 'socket', 'build_mood_vault',
                  'build_funding_vault', 'market_data')),
         "the runner names no network library, no builder and not the live "
         "candle source: there is no path from the run to anything that is "
         "not frozen")
    mark(len(BREAKS) == 11, "eleven breaks, counted against a number "
                            "typed out here")
    EXPECTED_CHECKS = 39
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.5-R PASSED — {len(nonlocal_ok)} checks, 0 red.

THE FIVE BARS ARE SLOT 1's OWN OBJECTS, imported and not copied.

THE PRE-FLIGHT REFUSED SIX TIMES - a damaged freeze, a missing one,
four wrong vault manifests - AND SPENT NOTHING: the whole run was then
made in that same folder.

THE WHOLE RUN WAS REHEARSED on three made-up coins of 1,094 daily
candles sharing one made-up mood, through the Lab's real engine: the
marker went down before the candles were asked for; every trade of
every coin was re-derived by hand from the mood; and with every value
after a chosen day replaced, every earlier trade was identical.

WHAT THIS GATE DOES **NOT** PROVE. It has never seen a real candle or
a real index value and says NOTHING about what the real run will find.
It rehearses the machinery; it does not review the DESIGN - one index
for three coins, the rank of 81 in 90, the publisher's labels, the
ship's exit on a fade - which are choices made by the same author,
and no second AI has read them.""")
    else:
        print(f"GATE 6.5-R FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
