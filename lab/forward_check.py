"""
Zar X Lab — FORWARD CHECK 1: the confluence rule and the trend alone, tried
ONCE on months nobody had seen. **NOT A GAUNTLET SLOT. IT PRINTS NO PASS AND
NO FAIL.**

After Slot 2 failed the Commander ordered the three ideas combined and
tried on unseen data. The vault was frozen on 2026-07-26; this looks at
2026-07-26 to 2026-11-15, 113 days. The rule and this file's rules were
written into PROGRESS_LOG.md on 2026-11-16 before any unseen data was
fetched, and committed with no code before this file existed.

WHAT IT DOES, in order:

  1. Refuses to run without `--go`.
  2. Refuses if its marker exists: THE UNSEEN MONTHS CAN BE UNSEEN ONCE.
  3. THE PRE-FLIGHT - the three forward freezes in `lab/forward_vault/`
     (candles, funding, mood) verified against their checksums and loaded,
     and the frozen past verified. A refusal writes no marker.
  4. Writes the marker. Only then is the vault opened.
  5. Stitches each coin's forward candles onto the vault's daily candles
     (the day after the vault's last, no gap, no day twice), and joins
     funding and mood on with the frozen stores' own join rules.
  6. Runs BOTH rules through the Lab's engine, unchanged, with the hold-out
     line at 2026-07-25: stop 1.5 and target 3.0 times the 14-candle
     range, the gauntlet's costs.
  7. **SHOWS AND SAVES ONLY TRADES ENTERED AFTER 2026-07-25.** The rules
     must walk the whole past to warm up - through the hold-out of Slots 1
     and 3 - and nothing from before the line is printed, saved or
     counted.
  8. Prints, for both rules: trades, wins, Profit Factor, the money on
     1,000 dollars, the worst dip, and buy-and-hold beside them.

**ABOUT 113 DAYS IS ABOUT TWENTY TRADES. FEWER THAN 30 IS NOT A VERDICT.**

**THE ONE PLACE REAL CANDLES REACH THE ENGINE WITHOUT `load_vault`.** The
engine takes candles only through its vault class; this file builds that
object itself from the vault's files plus the forward files, after the
Lab's inspector has passed each forward file. They are frozen and
checksummed, not live. Filed in REVIEW_QUEUE.md.

RUN (from the zar-x folder):
    python lab/forward_check.py              (verify the forward freezes)
    python lab/forward_check.py --gate       (rehearsal on made-up data)
    python lab/forward_check.py --go         (THE LOOK. ONCE.)
"""
import hashlib
import json
import os
import sys
from datetime import datetime

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(LAB_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, LAB_DIR)

import pandas as pd                                        # noqa: E402

import engine                                              # noqa: E402
import funding_vault                                       # noqa: E402
import mood_vault                                          # noqa: E402
from config import GAUNTLET_COSTS                          # noqa: E402
from gauntlet import buy_and_hold, compound, pool          # noqa: E402
from validator import validate_csv                         # noqa: E402

FORWARD_DIR = os.path.join(LAB_DIR, 'forward_vault')
ASSETS = ('BTC-USD', 'ETH-USD', 'SOL-USD')
TIMEFRAME = '1d'
LINE = '2026-07-25'            # the vault's last day: nothing up to it is shown
FIRST_DAY = '2026-07-26'
LAST_DAY = '2026-11-15'
DAYS = 113
SL_ATR = 1.5
TP_ATR = 3.0
START_MONEY = 1000.0
MARKER_NAME = 'FORWARD_CHECK_1_DONE.txt'
COLUMNS = ['open', 'high', 'low', 'close']
MANIFEST_NAME = 'MANIFEST.json'
ATTRIBUTES_NAME = '.gitattributes'


def rules():
    """The two rules, in the order they are reported."""
    from signals.confluence import Confluence, TrendOnly
    return [Confluence(), TrendOnly()]


def _sha(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def check_candles(df, first_day=None, days=None):
    """The one shape a forward candle file may have. Raises ValueError."""
    first_day = FIRST_DAY if first_day is None else first_day
    days = DAYS if days is None else days
    owed = pd.date_range(first_day, periods=days, freq='1D')
    if len(df) != days or not df.index.equals(owed):
        raise ValueError(f'{len(df)} candles where exactly {days} are owed, '
                         f'one a day from {first_day}: a day missing, twice '
                         f'or out of place')
    if list(df.columns) != COLUMNS:
        raise ValueError(f'columns {list(df.columns)}, not {COLUMNS}')
    values = df[COLUMNS].astype(float)
    if not bool(((values > 0) & (values < float('inf'))).all().all()):
        raise ValueError('a price that is not a positive number')


def write_candles(directory, frames, first_day=None, days=None):
    """Freeze the forward candles: one file a coin, a manifest, and the
    line that tells git not to touch a byte. REFUSES to overwrite."""
    if os.path.isdir(directory) and os.listdir(directory):
        raise RuntimeError(f'REFUSED: {directory} already holds a freeze.')
    for asset in ASSETS:
        check_candles(frames[asset], first_day, days)
    os.makedirs(directory, exist_ok=True)
    files = {}
    for asset in ASSETS:
        name = f'{asset}_{TIMEFRAME}.csv'
        path = os.path.join(directory, name)
        frames[asset].to_csv(path, index_label='datetime',
                             lineterminator='\n')
        files[name] = {'rows': len(frames[asset]),
                       'bytes': os.path.getsize(path), 'sha256': _sha(path)}
    with open(os.path.join(directory, MANIFEST_NAME), 'x', encoding='utf-8',
              newline='\n') as handle:
        json.dump({'what': 'forward daily candles, after the vault',
                   'law': 'Evidence. Never modified, never refreshed.',
                   'files': files}, handle, indent=2, sort_keys=True)
        handle.write('\n')
    with open(os.path.join(directory, ATTRIBUTES_NAME), 'x', encoding='ascii',
              newline='\n') as handle:
        handle.write('# Checksummed evidence. Git must not touch a byte.\n'
                     '* -text\n')


def verify_candles(directory, rows_owed=None):
    """-> (ok, lines). Checksums, byte counts, row counts, the file list."""
    rows_owed = DAYS if rows_owed is None else rows_owed
    try:
        with open(os.path.join(directory, MANIFEST_NAME),
                  encoding='utf-8') as handle:
            files = json.load(handle)['files']
        present = sorted(os.listdir(directory))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return False, [f'NO READABLE FREEZE in {directory} '
                       f'({type(exc).__name__})']
    owed = sorted(f'{asset}_{TIMEFRAME}.csv' for asset in ASSETS)
    lines, ok = [], sorted(files) == owed
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
                and entry.get('rows') == rows_owed)
        ok = ok and same
        lines.append(f'{name}: {entry.get("rows")} rows, '
                     f'{"checksum matches" if same else "DOES NOT MATCH"}')
    return ok, lines


def load_candles(directory, asset, first_day=None, days=None):
    """One coin's forward candles. Checksum, shape and the Lab's own data
    inspector, on every load. A FAIL from the inspector is a refusal."""
    name = f'{asset}_{TIMEFRAME}.csv'
    path = os.path.join(directory, name)
    with open(os.path.join(directory, MANIFEST_NAME),
              encoding='utf-8') as handle:
        entry = json.load(handle)['files'][name]
    if _sha(path) != entry['sha256']:
        raise RuntimeError(f'REFUSED: {name} does not match its checksum.')
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    check_candles(df, first_day, days)
    if validate_csv(path, TIMEFRAME).verdict == 'FAIL':
        raise RuntimeError(f'REFUSED: {name} failed the data inspector.')
    return df


def preflight(directory=None):
    """EVERYTHING THAT CAN BE REFUSED BEFORE THE LOOK IS SPENT. The three
    forward freezes, verified and loaded.
    -> {'candles': {asset: df}, 'funding': {asset: (times, units)},
        'mood': (days, values, sides)}"""
    directory = FORWARD_DIR if directory is None else directory
    first_ms = funding_vault.day_ms(FIRST_DAY)
    ok, lines = verify_candles(os.path.join(directory, 'candles'))
    if not ok:
        raise RuntimeError('REFUSED: the forward candles are not intact - '
                           + '; '.join(lines))
    try:
        candles = {asset: load_candles(os.path.join(directory, 'candles'),
                                       asset) for asset in ASSETS}
    except (OSError, ValueError, KeyError) as exc:
        raise RuntimeError(f'REFUSED: the forward candles cannot be read - '
                           f'{type(exc).__name__}: {exc}')
    funding = funding_vault.preflight(os.path.join(directory, 'funding'),
                                      first_ms, DAYS, DAYS * 3)
    mood = mood_vault.preflight(os.path.join(directory, 'mood'), first_ms,
                                DAYS, DAYS)
    return {'candles': candles, 'funding': funding, 'mood': mood}


def real_past():
    """The frozen past: the vault's daily candles through the Lab's own
    door, the frozen funding and the frozen mood."""
    return {'candles': {asset: engine.load_vault(asset, TIMEFRAME).df
                        for asset in ASSETS},
            'funding': funding_vault.preflight(),
            'mood': mood_vault.preflight()}


def verify_real_past():
    """Checksums of the frozen funding and mood, before the marker."""
    for name, (ok, lines) in (('funding', funding_vault.verify()),
                              ('mood', mood_vault.verify())):
        if not ok:
            raise RuntimeError(f'REFUSED: the frozen {name} is not intact - '
                               + '; '.join(lines))


def stitch(old, new):
    """The vault's candles, then the forward ones: the day after, no gap,
    no day twice."""
    if old.index[-1] + pd.Timedelta(days=1) != new.index[0]:
        raise RuntimeError(
            f'REFUSED: the forward candles begin {new.index[0].date()} but '
            f'the past ends {old.index[-1].date()}. No result is produced.')
    return pd.concat([old[COLUMNS], new[COLUMNS]])


def as_vault(asset, df):
    """Frozen candles, wearing the engine's own class. See the docstring:
    this is the one place real candles reach the engine without
    `load_vault`."""
    data = engine.VaultData.__new__(engine.VaultData)
    data.asset, data.timeframe = asset, TIMEFRAME
    data.path = f'<vault + forward: {asset}>'
    data.report, data.verdict = None, 'PASS'
    data.df = df
    return data


def money(returns, start=None):
    """Results as fractions of the account, one after another -> what
    `start` dollars became."""
    start = START_MONEY if start is None else start
    return start * (1.0 + compound(returns))


def worst_dip(returns):
    """The deepest fall from a high point, as a percentage."""
    equity, peak, worst = 1.0, 1.0, 0.0
    for value in returns:
        equity *= 1.0 + float(value)
        peak = max(peak, equity)
        worst = max(worst, (peak - equity) / peak)
    return 100.0 * worst


def summarise(pooled):
    """The figures printed for one rule, from its forward trades."""
    r = [float(v) for v in pooled['return_pct']] if len(pooled) else []
    wins = [v for v in r if v > 0]
    losses = [v for v in r if v <= 0]
    return {'trades': len(r),
            'longs': int((pooled['direction'] == 'long').sum()) if r else 0,
            'shorts': int((pooled['direction'] == 'short').sum()) if r else 0,
            'wins': len(wins),
            'profit_factor': (sum(wins) / -sum(losses) if losses
                              and sum(losses) < 0 else
                              float('inf') if wins else None),
            'money': money(r), 'dip': worst_dip(r)}


def run_forward(past=None, forward_dir=None, results_dir=None, out=print):
    """THE LOOK. Pre-flight, the marker, the stitch, both rules, and only
    the trades entered after the line.

    `past`, `forward_dir` and `results_dir` exist so the gate can rehearse
    this whole function on made-up data in temporary folders."""
    results_dir = engine.RESULTS_DIR if results_dir is None else results_dir
    os.makedirs(results_dir, exist_ok=True)
    marker = os.path.join(results_dir, MARKER_NAME)
    if os.path.exists(marker):
        raise RuntimeError(
            f'REFUSED: Forward Check 1 has been done ({marker}). The unseen '
            f'months can be unseen once.')
    strategies = rules()

    # THE PRE-FLIGHT. A REFUSAL HERE SPENDS NOTHING.
    forward = preflight(forward_dir)
    if past is None:
        verify_real_past()

    with open(marker, 'x', encoding='utf-8') as handle:
        handle.write(f'FORWARD CHECK 1 — DONE\n'
                     f'rules     : {[s.name for s in strategies]}\n'
                     f'commit    : {engine.git_commit()}\n'
                     f'started   : {datetime.now().isoformat(timespec="seconds")}\n'
                     f'window    : {FIRST_DAY} to {LAST_DAY}\n')
    out('FORWARD CHECK 1 — the confluence rule and the trend alone')
    out(f'  marker written: {marker}')
    out(f'  unseen window {FIRST_DAY} to {LAST_DAY} ({DAYS} days); only '
        f'trades entered after {LINE} are shown')

    before = (real_past if past is None else past)()
    frames = {}
    for asset in ASSETS:
        candles = stitch(before['candles'][asset], forward['candles'][asset])
        times = list(before['funding'][asset][0]) + list(
            forward['funding'][asset][0])
        units = list(before['funding'][asset][1]) + list(
            forward['funding'][asset][1])
        df = funding_vault.attach(candles, times, units)
        df = mood_vault.attach(
            df, *[list(a) + list(b) for a, b in zip(before['mood'],
                                                    forward['mood'])])
        if bool(df[['funding', 'mood', 'mood_side']].isna().any().any()):
            raise RuntimeError(f'REFUSED: {asset} has candles with no '
                               f'funding or no mood. No result is produced.')
        frames[asset] = df

    hold = [buy_and_hold(frames[asset], LINE) for asset in ASSETS]
    results, saved = [], []
    for strategy in strategies:
        per_asset = []
        for asset in ASSETS:
            result = engine.run_backtest(
                as_vault(asset, frames[asset]), strategy,
                strategy_name=strategy.name, params=strategy.params,
                train_end=LINE, verbose=False, costs=GAUNTLET_COSTS,
                sl_atr_mult=SL_ATR, tp_atr_mult=TP_ATR)
            held = result.window_trades('holdout').copy()
            held.insert(0, 'fingerprint', result.meta['fingerprint'])
            held.insert(0, 'asset', asset)
            held.insert(0, 'strategy', strategy.name)
            path = os.path.join(results_dir,
                                f'forward1_{strategy.name}_{asset}.csv')
            held.to_csv(path, index=False)
            saved.append(path)
            per_asset.append((asset, held))
        pooled = pool(per_asset)
        stats = summarise(pooled)
        results.append((strategy.name, stats, pooled))
        pf = stats['profit_factor']
        out('')
        out(f'  --- {strategy.name} ---')
        out(f'    trades entered after {LINE} : {stats["trades"]}  '
            f'({stats["longs"]} long / {stats["shorts"]} short; '
            f'{", ".join(f"{a} {len(t)}" for a, t in per_asset)})')
        out(f'    won                          : {stats["wins"]} of '
            f'{stats["trades"]}')
        out(f'    profit factor after costs    : '
            f'{"no trades" if pf is None else f"{pf:.2f}"}')
        out(f'    1,000 dollars became         : {stats["money"]:,.0f}')
        out(f'    worst dip on the way         : {stats["dip"]:.1f}%')
    out('')
    out(f'  buy-and-hold, 1% risk sizing, same days: 1,000 dollars became '
        f'{money(hold):,.0f}')
    out('')
    fewest = min(stats['trades'] for _n, stats, _p in results)
    out(f'  !! {fewest} TRADES AT THE FEWEST. FEWER THAN 30 IS NOT A VERDICT. '
        f'THIS IS A FIRST LOOK, NOT A PASS AND NOT A FAIL.')
    with open(marker, 'a', encoding='utf-8') as handle:
        handle.write(f'finished  : {datetime.now().isoformat(timespec="seconds")}\n')
    return {'results': results, 'saved': saved, 'marker': marker,
            'hold': hold}


def main(argv, runner=None, results_dir=None):
    """`--go` runs the look. Anything less refuses and touches nothing."""
    runner = run_forward if runner is None else runner
    results_dir = engine.RESULTS_DIR if results_dir is None else results_dir
    if '--go' not in argv:
        print('REFUSED. Forward Check 1 runs ONCE, and only when asked on '
              'purpose:')
        print('    python lab/forward_check.py --go')
        print('Nothing was opened and nothing was written.')
        return 2
    lines = []

    def out(line=''):
        print(line)
        lines.append(str(line))

    try:
        runner(out=out)
    finally:
        os.makedirs(results_dir, exist_ok=True)
        with open(os.path.join(results_dir, 'forward1_report.txt'), 'a',
                  encoding='utf-8') as handle:
            handle.write('\n'.join(lines) + '\n')
    return 0


if __name__ == '__main__':
    if '--gate' not in sys.argv and '--go' not in sys.argv:
        problems = []
        for name, (ok, lines) in (
                ('candles', verify_candles(os.path.join(FORWARD_DIR,
                                                        'candles'))),
                ('funding', funding_vault.verify(
                    os.path.join(FORWARD_DIR, 'funding'), DAYS * 3)),
                ('mood', mood_vault.verify(
                    os.path.join(FORWARD_DIR, 'mood'), DAYS))):
            print(f'FORWARD {name}:')
            for line in lines:
                print('   ' + line)
            problems += [] if ok else [name]
        print(f'FORWARD STORE {"INTACT" if not problems else "NOT INTACT"} '
              f'— {3 - len(problems)} of 3')
        sys.exit(0 if not problems else 1)
    if '--gate' not in sys.argv:
        sys.exit(main(sys.argv[1:]))

    # =====================================================================
    # GATE 6.6-F — FORWARD CHECK 1's REHEARSAL. Declared in PROGRESS_LOG.md
    # on 2026-11-16 and committed with no code, before this file existed.
    # It also gates `lab/build_forward_vault.py` against fake sources.
    #
    # **IT NEVER OPENS THE VAULT, A REAL FROZEN FOLDER OR THE NETWORK.**
    # =====================================================================
    import re
    import shutil
    import tempfile

    import numpy as np

    import build_forward_vault as builder

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def held_or(function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}: {exc}>'

    def same_candles(got, want):
        """Two candle frames equal: the same days, the same prices to the
        last digit a CSV keeps."""
        return (isinstance(got, pd.DataFrame)
                and list(got.index) == list(want.index)
                and list(got.columns) == list(want.columns)
                and bool(np.allclose(got.values.astype(float),
                                     want.values.astype(float),
                                     rtol=1e-12, atol=0.0)))

    def text_of(path):
        try:
            with open(path, encoding='utf-8') as handle:
                return handle.read()
        except OSError:
            return ''

    VAULT_OPENED = []
    _real_door = engine.load_vault

    def _no_vault(*args, **kwargs):
        VAULT_OPENED.append(args)
        raise RuntimeError('the rehearsal must never open the vault')

    engine.load_vault = _no_vault
    REAL_RESULTS_BEFORE = sorted(os.listdir(engine.RESULTS_DIR))
    REAL_FORWARD_BEFORE = (sorted(os.listdir(FORWARD_DIR))
                           if os.path.isdir(FORWARD_DIR) else None)
    REAL_DIRS = [os.path.abspath(d) for d in (
        FORWARD_DIR, funding_vault.FUNDING_DIR, mood_vault.MOOD_DIR)]
    FILES_READ = []
    _shas = (_sha, funding_vault._sha, mood_vault._sha)

    def _spy(real):
        def spy(path):
            FILES_READ.append(os.path.abspath(path))
            return real(path)
        return spy

    _sha = _spy(_shas[0])
    funding_vault._sha = _spy(_shas[1])
    mood_vault._sha = _spy(_shas[2])
    WORK = tempfile.mkdtemp(prefix='zarx_forward_')

    ONE_DAY = pd.Timedelta(days=1)
    PAST_DAYS = pd.date_range('2023-07-28', periods=1094, freq=ONE_DAY)
    NEW_DAYS = pd.date_range('2026-07-26', periods=113, freq=ONE_DAY)
    PAST_MS, NEW_MS = 1690502400000, 1785024000000
    DAY_MS, MARK_MS = 86400000, 28800000

    print("=" * 70)
    print("GATE 6.6-F — FORWARD CHECK 1, REHEARSED. Made-up data only.")
    print("=" * 70)

    print("\n(a) THE DECLARED NUMBERS, typed out here.")
    mark((LINE, FIRST_DAY, LAST_DAY, DAYS, SL_ATR, TP_ATR, START_MONEY,
          TIMEFRAME, ASSETS, MARKER_NAME)
         == ('2026-07-25', '2026-07-26', '2026-11-15', 113, 1.5, 3.0, 1000.0,
             '1d', ('BTC-USD', 'ETH-USD', 'SOL-USD'),
             'FORWARD_CHECK_1_DONE.txt')
         and str(NEW_DAYS[-1].date()) == LAST_DAY
         and str(PAST_DAYS[-1].date()) == LINE
         and funding_vault.day_ms(FIRST_DAY) == NEW_MS
         and GAUNTLET_COSTS == {'fee_pct': 0.0005, 'slippage_pct': 0.0005}
         and [s.name for s in rules()] == ['confluence-1d-t100',
                                           'trend-only-1d-t100'],
         "the line 2026-07-25 (the vault's last day), the unseen window "
         "2026-07-26 to 2026-11-15, 113 days; stop 1.5 and target 3.0; the "
         "gauntlet's costs; the two rules, confluence first — every one "
         "typed out here")

    def walk(seed, count):
        rng = np.random.default_rng(seed)
        price, rows = 100.0, []
        for _ in range(count):
            steps = price * np.exp(np.cumsum(
                rng.normal(0.0004, 0.035 / np.sqrt(24), 24)))
            rows.append((price, max(price, steps.max()),
                         min(price, steps.min()), float(steps[-1])))
            price = float(steps[-1])
        return pd.DataFrame(rows, columns=COLUMNS)

    def made_up_coin(seed):
        whole = walk(seed, 1207)
        old, new = whole.iloc[:1094].copy(), whole.iloc[1094:].copy()
        old.index, new.index = PAST_DAYS, NEW_DAYS
        return old, new

    def made_up_funding(seed, count):
        rng = np.random.default_rng(seed)
        level, out = 8000.0, []
        for _ in range(count):
            level = 0.97 * level + 0.03 * 6000.0 + rng.normal(0, 2500)
            out.append(int(round(level)))
        return out

    def label_of(value):
        return ('Extreme Fear' if value <= 25 else 'Fear' if value <= 46
                else 'Neutral' if value <= 54 else 'Greed' if value <= 75
                else 'Extreme Greed')

    def made_up_mood(seed, count):
        rng = np.random.default_rng(seed)
        level, out = 50.0, []
        for _ in range(count):
            level = 0.96 * level + 0.04 * 50.0 + rng.normal(0, 5.0)
            out.append(int(max(0, min(100, round(level)))))
        return out

    SEEDS = {'BTC-USD': 11, 'ETH-USD': 22, 'SOL-USD': 33}
    COINS = {asset: made_up_coin(SEEDS[asset]) for asset in ASSETS}
    FUNDING = {asset: made_up_funding(SEEDS[asset] + 100, 3282 + 339)
               for asset in ASSETS}
    MOOD = made_up_mood(505, 1094 + 113)

    def the_past():
        return {
            'candles': {a: COINS[a][0] for a in ASSETS},
            'funding': {a: ([PAST_MS + n * MARK_MS for n in range(3282)],
                            FUNDING[a][:3282]) for a in ASSETS},
            'mood': ([PAST_MS + n * DAY_MS for n in range(1094)],
                     MOOD[:1094],
                     [mood_vault.LABELS[label_of(v)] for v in MOOD[:1094]])}

    def freeze(name, funding=None, mood=None, coins=None):
        """A made-up forward store in a temporary folder."""
        folder = os.path.join(WORK, name)
        funding = FUNDING if funding is None else funding
        mood = MOOD if mood is None else mood
        coins = COINS if coins is None else coins
        write_candles(os.path.join(folder, 'candles'),
                      {a: coins[a][1] for a in ASSETS})
        funding_vault.write_freeze(
            os.path.join(folder, 'funding'),
            {funding_vault.CONTRACTS[a]: [
                (NEW_MS + n * MARK_MS, f'{u / 1e8:.8f}')
                for n, u in enumerate(funding[a][3282:])] for a in ASSETS},
            first_ms=NEW_MS, days=113)
        mood_vault.write_freeze(
            os.path.join(folder, 'mood'),
            [(str(day.date()), int(v), label_of(v), 0)
             for day, v in zip(NEW_DAYS, mood[1094:])],
            first_ms=NEW_MS, days=113)
        return folder

    print("\n(b) THE FORWARD CANDLE STORE: one shape, written once, verified.")
    good_new = {a: COINS[a][1] for a in ASSETS}
    one = good_new['BTC-USD']
    mark(held_or(check_candles, one) is None
         and 'exactly 113' in str(held_or(check_candles, one.iloc[:-1]))
         and 'exactly 113' in str(held_or(check_candles, one.drop(
             one.index[50])))
         and 'exactly 113' in str(held_or(
             check_candles, one.set_axis(NEW_DAYS + ONE_DAY)))
         and 'columns' in str(held_or(check_candles, one[['open', 'close',
                                                           'high', 'low']]))
         and 'positive number' in str(held_or(
             check_candles, one.assign(low=[0.0] + list(one['low'])[1:]))),
         "113 made-up candles on the right days are ACCEPTED; a candle "
         "short, a day missing, the right count starting a day late, "
         "columns out of order and a price of zero are each REFUSED")
    FREEZE = freeze('forward')
    room = os.path.join(FREEZE, 'candles')
    mark(verify_candles(room)[0]
         and same_candles(held_or(load_candles, room, 'ETH-USD'),
                          good_new['ETH-USD'])
         and 'already holds' in str(held_or(write_candles, room, good_new)),
         "three files and a manifest are written; the verifier says "
         "INTACT; a file reads back the same and passes the Lab's own data "
         "inspector; a second freeze into the folder is REFUSED")
    hurt = os.path.join(WORK, 'hurt')
    shutil.copytree(FREEZE, hurt)
    target = os.path.join(hurt, 'candles', 'SOL-USD_1d.csv')
    with open(target, 'rb') as handle:
        raw = bytearray(handle.read())
    raw[-4] = ord('7') if raw[-4] != ord('7') else ord('8')
    with open(target, 'wb') as handle:
        handle.write(bytes(raw))
    mark(not verify_candles(os.path.join(hurt, 'candles'))[0]
         and 'does not match' in str(held_or(
             load_candles, os.path.join(hurt, 'candles'), 'SOL-USD'))
         and 'not intact' in str(held_or(preflight, hurt))
         and not verify_candles(os.path.join(WORK, 'nowhere'))[0],
         "ONE DIGIT of one forward price changed: NOT INTACT, the file "
         "refuses to load, the pre-flight refuses; a folder that does not "
         "exist is NOT INTACT and not a crash")

    sick = {a: COINS[a][1].copy() for a in ASSETS}
    sick['ETH-USD'].iloc[40, 1] = sick['ETH-USD'].iloc[40, 2] * 0.99
    sick_room = os.path.join(WORK, 'sick')
    write_candles(sick_room, sick)
    mark(held_or(check_candles, sick['ETH-USD']) is None
         and verify_candles(sick_room)[0]
         and 'failed the data inspector' in str(held_or(
             load_candles, sick_room, 'ETH-USD'))
         and isinstance(held_or(load_candles, sick_room, 'BTC-USD'),
                        pd.DataFrame),
         "A FORWARD FILE THE LAB'S OWN INSPECTOR FAILS (one candle whose "
         "high is below its low) is the right shape and matches its "
         "checksum - and STILL REFUSES TO LOAD. (The inspector skipped "
         "went GREEN at 30/0 in this gate's own attack.)")

    print("\n(c) THE BUILDER, against fake sources.")

    def sources(coins=None, shift_seam=False, gap=False):
        coins = COINS if coins is None else coins

        def candles(asset):
            old, new = coins[asset]
            both = pd.concat([old.iloc[-60:], new])
            if shift_seam:
                both = both.copy()
                both.iloc[45, 3] *= 1.0001      # one overlapping close
            if gap:
                both = both.drop(both.index[80])
            return both

        def funding(params):
            asset = {v: k for k, v in funding_vault.CONTRACTS.items()}[
                params['symbol']]
            rows = [(NEW_MS + n * MARK_MS, f'{u / 1e8:.8f}')
                    for n, u in enumerate(FUNDING[asset][3282:])]
            hits = [r for r in rows
                    if params['startTime'] <= r[0] <= params['endTime']]
            return [{'fundingTime': s, 'fundingRate': r}
                    for s, r in hits[:params['limit']]]

        def mood():
            return {'data': [{'value': str(v),
                              'value_classification': label_of(v),
                              'timestamp': str((PAST_MS + n * DAY_MS)
                                               // 1000)}
                             for n, v in enumerate(MOOD)]}
        return {'candles': candles, 'funding': funding, 'mood': mood}

    def vault_rows(asset):
        return COINS[asset][0]

    built = os.path.join(WORK, 'built')
    said = []
    died = held_or(builder.build, built, sources=sources(),
                   vault_rows=vault_rows, out=said.append)
    said_text = '\n'.join(str(line) for line in said)
    mark(not isinstance(died, str) and held_or(preflight, built) is not None
         and not isinstance(held_or(preflight, built), str)
         and same_candles(held_or(preflight, built)['candles']['BTC-USD'],
                          good_new['BTC-USD'])
         and held_or(preflight, built)['funding']['SOL-USD'][1]
         == FUNDING['SOL-USD'][3282:]
         and held_or(preflight, built)['mood'][1] == MOOD[1094:],
         "the builder freezes all three stores from fake sources, the "
         "pre-flight loads them, and each holds exactly the made-up "
         "candles, funding and mood of the 113 forward days",
         died if isinstance(died, str) else '')
    first_price = f"{good_new['BTC-USD']['open'].iloc[0]:.2f}"
    mark('113' in said_text and '25 of 25' in said_text
         and first_price not in said_text and 'Fear' not in said_text
         and 'Greed' not in said_text and '0.000' not in said_text,
         "it says the seam matched on 25 of 25 overlapping days, and PRINTS "
         "NO PRICE, NO RATE AND NO MOOD",
         said_text.replace('\n', ' | ')[:160])
    seam_room = os.path.join(WORK, 'seam')
    gap_room = os.path.join(WORK, 'gap')
    mark('seam' in str(held_or(builder.build, seam_room,
                               sources=sources(shift_seam=True),
                               vault_rows=vault_rows, out=lambda *a: None))
         and not os.path.exists(seam_room)
         and 'exactly 113' in str(held_or(
             builder.build, gap_room, sources=sources(gap=True),
             vault_rows=vault_rows, out=lambda *a: None))
         and not os.path.exists(gap_room)
         and 'already holds' in str(held_or(
             builder.build, built, sources=sources(), vault_rows=vault_rows,
             out=lambda *a: None)),
         "ONE overlapping close a hundredth of a percent off: REFUSED, "
         "nothing frozen - the new candles must continue the old ones; a "
         "forward day missing: REFUSED, nothing frozen; a second build: "
         "REFUSED")

    print("\n(d) THE STITCH, BY HAND.")
    old, new = COINS['BTC-USD']
    joined = held_or(stitch, old, new)
    mark(isinstance(joined, pd.DataFrame) and len(joined) == 1207
         and joined.index[1093] == pd.Timestamp('2026-07-25')
         and joined.index[1094] == pd.Timestamp('2026-07-26')
         and not joined.index.duplicated().any()
         and set(joined.index.to_series().diff().dropna()) == {ONE_DAY}
         and 'REFUSED' in str(held_or(stitch, old.iloc[:-1], new))
         and 'REFUSED' in str(held_or(stitch, old, new.iloc[1:]))
         and 'REFUSED' in str(held_or(stitch, old, new.set_axis(
             NEW_DAYS - ONE_DAY))),
         "1,094 + 113 = 1,207 candles, 2026-07-25 followed by 2026-07-26, "
         "no day twice and every step one day; a past one day short, a "
         "forward one day late and a forward that overlaps the past are "
         "each REFUSED")

    print("\n(e) >>> THE WHOLE LOOK, REHEARSED THROUGH THE LAB'S REAL ENGINE.")
    _room = [0]

    def rehearse(forward_dir=None, folder=None, past=None):
        if folder is None:
            _room[0] += 1
            folder = os.path.join(WORK, f'run_{_room[0]}')
        said = []
        try:
            result = run_forward(past=the_past if past is None else past,
                                 forward_dir=(FREEZE if forward_dir is None
                                              else forward_dir),
                                 results_dir=folder, out=said.append)
            died = ''
        except Exception as exc:                           # noqa: BLE001
            result, died = None, f'{type(exc).__name__}: {exc}'
        return result, died, said, folder

    main_room = os.path.join(WORK, 'the_look')
    r_hurt = rehearse(forward_dir=hurt, folder=main_room)
    r_none = rehearse(forward_dir=os.path.join(WORK, 'nowhere'),
                      folder=main_room)
    mark(r_hurt[1].startswith('RuntimeError: REFUSED')
         and r_none[1].startswith('RuntimeError: REFUSED')
         and not os.path.exists(os.path.join(main_room, MARKER_NAME)),
         "THE PRE-FLIGHT REFUSES BEFORE THE MARKER: a damaged forward store "
         "and a missing one each stop the look with NO MARKER written",
         r_hurt[1][:80])
    look, died, said, _folder = rehearse(folder=main_room)
    said_text = '\n'.join(str(line) for line in said)
    mark(died == '' and look is not None and len(look['results']) == 2
         and [name for name, _s, _p in look['results']]
         == ['confluence-1d-t100', 'trend-only-1d-t100']
         and len(look['saved']) == 6
         and os.path.exists(os.path.join(main_room, MARKER_NAME)),
         "after two refusals the look was still unspent: it ran both rules "
         "on three made-up coins and saved six trade files",
         died or f"{[(n, s['trades']) for n, s, _p in look['results']]}")
    saved = [held_or(pd.read_csv, path) for path in
             (look['saved'] if look else [])]
    saved = [s for s in saved if isinstance(s, pd.DataFrame)]
    entries = [pd.Timestamp(t) for s in saved for t in s['entry_time']]
    # THE PAST HAD TRADES TO HIDE: the same rules, run by this gate straight
    # through the engine, traded BEFORE the line too.
    hidden = 0
    for strategy in rules():
        for asset in ASSETS:
            frame = mood_vault.attach(
                funding_vault.attach(
                    stitch(*COINS[asset]),
                    [PAST_MS + n * MARK_MS for n in range(3621)],
                    FUNDING[asset]),
                [PAST_MS + n * DAY_MS for n in range(1207)], MOOD,
                [mood_vault.LABELS[label_of(v)] for v in MOOD])
            full = engine.run_backtest(as_vault(asset, frame), strategy,
                                       strategy_name='x', train_end=LINE,
                                       verbose=False, regime=False,
                                       costs=GAUNTLET_COSTS,
                                       sl_atr_mult=1.5, tp_atr_mult=3.0)
            hidden += int((full.trades['entry_time']
                           <= pd.Timestamp(LINE)).sum())
    dates = re.findall(r'20\d\d-\d\d-\d\d', said_text)
    mark(len(saved) == 6 and len(entries) >= 6 and hidden >= 50
         and all(t > pd.Timestamp(LINE) for t in entries)
         and all(d >= LINE for d in dates),
         ">>> ONLY TRADES ENTERED AFTER THE LINE ARE SAVED OR PRINTED: the "
         "same rules made dozens of trades BEFORE 2026-07-25 on this "
         "made-up past, and NOT ONE of them is in the six saved files, and "
         "no date before the line appears in anything the look printed",
         f"{hidden} trades before the line, all hidden; {len(entries)} "
         f"after it, all shown; earliest shown "
         f"{min(entries).date() if entries else '-'}")
    by_rule = {}
    for s in saved:
        if len(s):
            by_rule.setdefault(str(s['strategy'].iloc[0]), []).append(s)
    ok_money = bool(look)
    for name, stats, pooled in (look['results'] if look else []):
        parts = by_rule.get(name, [])
        rows = (pd.concat(parts).assign(_o=lambda d: d['asset'].map(
            {a: i for i, a in enumerate(ASSETS)})).sort_values(
                ['entry_time', '_o'], kind='mergesort') if parts
            else pd.DataFrame({'return_pct': []}))
        by_hand = 1000.0
        for value in rows['return_pct']:
            by_hand *= 1.0 + float(value)
        r = rows['return_pct'].astype(float)
        pf_hand = (r[r > 0].sum() / -r[r <= 0].sum()
                   if (r <= 0).any() and r[r <= 0].sum() < 0 else None)
        ok_money = (ok_money and stats['trades'] == len(rows)
                    and abs(stats['money'] - by_hand) < 1e-6
                    and f'{by_hand:,.0f}' in said_text
                    and (pf_hand is None or stats['profit_factor'] is None
                         or abs(stats['profit_factor'] - pf_hand) < 1e-9)
                    and stats['wins'] == int((r > 0).sum()))
    mark(ok_money and 'FEWER THAN 30 IS NOT A VERDICT' in said_text
         and 'PASSED' not in said_text and 'FAILED' not in said_text,
         "for both rules the trade count, the wins, the Profit Factor and "
         "WHAT 1,000 DOLLARS BECAME equal the same figures re-worked here "
         "from the saved files; the warning about fewer than 30 trades is "
         "printed; and the words PASSED and FAILED are not")
    def hand_signals(asset):
        """Both rules a second time, in plain Python, straight from the
        made-up closes, funding and mood: nothing from the join, the
        strategies or the runner."""
        closes = list(pd.concat([COINS[asset][0], COINS[asset][1]])['close'])
        units = FUNDING[asset]
        fund = [units[3 * d] + units[3 * d + 1] + units[3 * d + 2]
                for d in range(1207)]
        side = [{'Extreme Fear': -1, 'Fear': -1, 'Neutral': 0, 'Greed': 1,
                 'Extreme Greed': 1}[label_of(v)] for v in MOOD]
        both = []
        for at in range(1207):
            if at < 99:
                both.append(('flat', 'flat'))
                continue
            window = closes[at - 99:at + 1]
            average = sum(window) / 100
            way = (1 if closes[at] > average else
                   -1 if closes[at] < average else 0)
            f_now, f_past = fund[at], fund[at - 90:at]
            m_now, m_past = MOOD[at], MOOD[at - 90:at]
            greedy = ((f_now > 0 and sum(1 for v in f_past if v < f_now)
                       >= 81)
                      or (side[at] == 1 and sum(1 for v in m_past
                                                if v < m_now) >= 81))
            scared = ((f_now < 0 and sum(1 for v in f_past if v > f_now)
                       >= 81)
                      or (side[at] == -1 and sum(1 for v in m_past
                                                 if v > m_now) >= 81))
            both.append(('long' if way > 0 and greedy else
                         'short' if way < 0 and scared else 'flat',
                         'long' if way > 0 else
                         'short' if way < 0 else 'flat'))
        return both

    ALL_DAYS = list(PAST_DAYS) + list(NEW_DAYS)
    DAY_AT = {day: n for n, day in enumerate(ALL_DAYS)}
    HAND = {asset: hand_signals(asset) for asset in ASSETS}
    wrong, walked = [], 0
    for s in saved:
        for _i, row in s.iterrows():
            walked += 1
            at = DAY_AT[pd.Timestamp(row['entry_time'])] - 1
            which = 0 if row['strategy'] == 'confluence-1d-t100' else 1
            if HAND[row['asset']][at][which] != row['direction']:
                wrong.append((row['strategy'], row['asset'],
                              str(row['entry_time'])[:10]))
    mark(walked == len(entries) and walked >= 6 and not wrong
         and {str(s['strategy'].iloc[0]) for s in saved if len(s)}
         == {'confluence-1d-t100', 'trend-only-1d-t100'},
         "EVERY TRADE SHOWN, OF BOTH RULES, WAS ENTERED THE DAY AFTER A DAY "
         "ON WHICH THAT RULE - worked a second time here in plain Python "
         "from the made-up closes, funding and mood - GAVE THAT SIGNAL. "
         "(Each candle handed TOMORROW's funding went GREEN at 30/0 in "
         "this gate's own attack: nothing had re-derived a trade.)",
         f"{walked} trades walked, {len(wrong)} wrong {wrong[:3]}")

    def yard_by_hand(asset):
        df = pd.concat([COINS[asset][0], COINS[asset][1]])
        first = 1094                        # the first candle after the line
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

    held_money = 1000.0
    for asset in ASSETS:
        held_money *= 1.0 + yard_by_hand(asset)
    printed_pf = True
    for name, stats, _pooled in (look['results'] if look else []):
        pf = stats['profit_factor']
        printed_pf = printed_pf and (
            f'profit factor after costs    : '
            f'{"no trades" if pf is None else f"{pf:.2f}"}' in said_text)
    mark(look is not None
         and all(abs(a - yard_by_hand(asset)) < 1e-12
                 for a, asset in zip(look['hold'], ASSETS))
         and f'1,000 dollars became {held_money:,.0f}' in said_text
         and printed_pf,
         "BUY-AND-HOLD IS BOUGHT AT THE FIRST CANDLE AFTER 2026-07-25 - "
         "worked a second time here with plain arithmetic at a fee of "
         "0.05% - and the figure printed is that one; and the Profit Factor "
         "PRINTED for each rule is the one re-worked from its saved trades. "
         "(Buy-and-hold from the gauntlet's old line, and a printed Profit "
         "Factor half as big again, both went GREEN in this gate's own "
         "attack.)",
         f"by hand {held_money:,.2f}")

    DECLARED = {
        'confluence-1d-t100': {
            'trend': 100, 'kind': 'confluence',
            'funding': {'window': 90, 'need': 81, 'warmup': 91,
                        'column': 'funding', 'kind': 'funding_extreme_fade'},
            'mood': {'window': 90, 'need': 81, 'warmup': 91, 'value': 'mood',
                     'side': 'mood_side', 'kind': 'crowd_mood_fade'}},
        'trend-only-1d-t100': {'trend': 100, 'kind': 'trend_only'}}
    STAMP = {'_costs': {'fee_pct': 0.0005, 'slippage_pct': 0.0005},
             '_risk_pct': 0.01, '_sl_atr': 1.5, '_tp_atr': 3.0,
             '_atr_period': 14, '_capital': 10000.0,
             '_train_end': '2026-07-25 00:00:00'}
    want = {name: engine.fingerprint(name, dict(params, **STAMP))
            for name, params in DECLARED.items()}
    got = {name: sorted({str(v) for s in parts for v in s['fingerprint']})
           for name, parts in by_rule.items()}
    mark(got == {name: [value] for name, value in want.items()},
         "every saved trade carries the fingerprint of the DECLARED "
         "settings typed out here: each rule's numbers, fee 0.05%, "
         "slippage 0.05%, risk 1%, stop 1.5 and target 3.0 ATR over 14 "
         "candles, the line 2026-07-25", f"{got}")
    again = rehearse(folder=main_room)
    mark(again[1].startswith('RuntimeError: REFUSED')
         and 'unseen once' in again[1],
         "A SECOND LOOK IS REFUSED", again[1][:80])

    def short_past():
        before = the_past()
        before['funding'] = {a: (t[:-3], u[:-3])
                             for a, (t, u) in before['funding'].items()}
        return before

    bare = rehearse(past=short_past)
    mark('no funding or no mood' in bare[1]
         and not any('profit factor' in str(line) for line in bare[2])
         and os.path.exists(os.path.join(bare[3], MARKER_NAME))
         and not [f for f in os.listdir(bare[3]) if f.endswith('.csv')],
         "A CANDLE WITH NO FUNDING (the past one day short of it) stops the "
         "look with NO FIGURE printed and no trade file saved - the marker "
         "is down, because it goes first",
         bare[1][:90])

    print("\n(f) >>> THE POISON TEST, THROUGH THE WHOLE LOOK.")
    CUT = 60                                    # forward day 61 onward
    bad_coins = {}
    for asset in ASSETS:
        old, new = COINS[asset]
        other = walk(SEEDS[asset] + 900, 113)
        scale = float(new['close'].iloc[CUT - 1]) / float(
            other['close'].iloc[CUT - 1])
        changed = new.copy()
        changed.iloc[CUT:] = (other.iloc[CUT:] * scale).values
        bad_coins[asset] = (old, changed)
    bad_funding = {a: FUNDING[a][:3282 + 3 * CUT]
                   + made_up_funding(SEEDS[a] + 700, 339)[3 * CUT:]
                   for a in ASSETS}
    bad_mood = MOOD[:1094 + CUT] + made_up_mood(909, 113)[CUT:]
    dirty = rehearse(forward_dir=freeze('poisoned', bad_funding, bad_mood,
                                        bad_coins))
    cut_day = NEW_DAYS[CUT - 1]
    same, moved = 0, 0
    if dirty[0] and look:
        for clean_path, dirty_path in zip(look['saved'], dirty[0]['saved']):
            a, b = pd.read_csv(clean_path), pd.read_csv(dirty_path)
            keep = ['direction', 'entry_time', 'entry_price_raw',
                    'size_units']
            a1 = a[pd.to_datetime(a['entry_time']) <= cut_day]
            b1 = b[pd.to_datetime(b['entry_time']) <= cut_day]
            same += int(a1[keep].reset_index(drop=True).equals(
                b1[keep].reset_index(drop=True)))
            moved += int(not a.equals(b))
    mark(dirty[1] == '' and same == 6 and moved >= 3,
         "every candle, funding rate and mood value from forward day 61 on "
         "is replaced and the whole look made again: every trade ENTERED up "
         "to day 60 is identical in all six files — and the files as a "
         "whole are not, so the poison was real",
         dirty[1] or f"identical entries before: {same} of 6; files "
                     f"changed: {moved} of 6")

    print("\n(g) THE COMMAND, WITH A SPY WHERE THE LOOK WOULD BE.")
    reached = []

    def spy(out=None):
        reached.append('look')
        raise RuntimeError('the spy was reached')

    spy_room = os.path.join(WORK, 'spy')
    codes = [held_or(main, argv, runner=spy, results_dir=spy_room)
             for argv in ([], ['go'], ['--gate'])]
    went = held_or(main, ['--go'], runner=spy, results_dir=spy_room)
    mark(codes == [2, 2, 2] and reached == ['look']
         and str(went).startswith('<RuntimeError')
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE,
         "without `--go` the command refuses and the look is never "
         "reached; with it the look is reached once",
         f"codes {codes}, reached {reached}")

    print("\n(h) >>> THE SABOTAGE DRILL, PERMANENT. INERT IS A FAIL.")

    def summary(outcome):
        result, died, said, _folder = outcome
        if result is None:
            return died[:40]
        return tuple((name, stats['trades'], round(stats['money'], 4))
                     for name, stats, _p in result['results']) + (
            tuple(round(v, 8) for v in result['hold']),)

    def witness():
        return (summary(rehearse()),
                rehearse(forward_dir=hurt)[1][:22])

    HONEST = witness()
    G = globals()
    _keep = {name: G[name] for name in
             ('LINE', 'TP_ATR', 'SL_ATR', 'GAUNTLET_COSTS', 'rules',
              'preflight', 'stitch', 'compound', 'pool', 'buy_and_hold')}
    _real_attach = funding_vault.attach
    GOOD = preflight(FREEZE)

    def _reversed_rules():
        from signals.confluence import Confluence, TrendOnly
        return [Confluence(trend=5), TrendOnly()]

    BREAKS = [
        ('F1', 'the line moved back a year (old trades shown)', 'LINE',
         '2025-07-25'),
        ('F2', 'the target back at 2.0', 'TP_ATR', 2.0),
        ('F3', 'the stop at 3.0', 'SL_ATR', 3.0),
        ('F4', "the Lab's old fee charged", 'GAUNTLET_COSTS',
         {'fee_pct': 0.001, 'slippage_pct': 0.0005}),
        ('F5', 'the confluence rule on a 5-day trend', 'rules',
         _reversed_rules),
        ('F6', 'the pre-flight skipping the checksums', 'preflight',
         lambda directory=None: GOOD),
        ('F7', 'results ADDED instead of compounded', 'compound',
         lambda fractions: float(sum(float(f) for f in fractions))),
        ('F8', 'the pool dropping the third coin', 'pool',
         lambda coins: _keep['pool'](list(coins)[:2])),
        ('F9', 'buy-and-hold set to nothing', 'buy_and_hold',
         lambda df, train_end=None: 0.0),
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
        mark(broken != HONEST, f"{tag} {words:<48} -> "
             f"{'CAUGHT' if broken != HONEST else 'INERT — IT CHANGED NOTHING'}")

    def _tomorrow(df, times, units):
        out = _real_attach(df, times, units)
        out['funding'] = list(out['funding'].values[1:]) + [0.0]
        return out

    funding_vault.attach = _tomorrow
    try:
        b10 = witness()
    except Exception:                                      # noqa: BLE001
        b10 = '<crashed>'
    finally:
        funding_vault.attach = _real_attach
    mark(b10 != HONEST, f"F10 {'each candle given TOMORROW funding':<47} -> "
         f"{'CAUGHT' if b10 != HONEST else 'INERT — IT CHANGED NOTHING'}")
    first_summary = summary((look, died, said, main_room)) if look else None
    mark(all(G[name] is original for name, original in _keep.items())
         and funding_vault.attach is _real_attach and witness() == HONEST
         and HONEST == (first_summary, 'RuntimeError: REFUSED:'),
         "and after ten breaks everything is what it started as, and the "
         "witness's look is the rehearsal of (e) again, figure for figure")

    print("\n(i) NOTHING REAL WAS OPENED, AND THE GATE COUNTS ITSELF.")
    engine.load_vault = _real_door
    _sha, funding_vault._sha, mood_vault._sha = _shas
    shutil.rmtree(WORK, ignore_errors=True)
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        production = handle.read().split("if __name__ == '__main__':")[0]
    mark(VAULT_OPENED == []
         and sorted(os.listdir(engine.RESULTS_DIR)) == REAL_RESULTS_BEFORE
         and (sorted(os.listdir(FORWARD_DIR)) if os.path.isdir(FORWARD_DIR)
              else None) == REAL_FORWARD_BEFORE
         and len(FILES_READ) > 20
         and not any(path.startswith(real) for path in FILES_READ
                     for real in REAL_DIRS)
         and not any(word in production for word in
                     ('requests', 'urllib', 'socket', 'market_data',
                      'build_forward_vault')),
         "the Lab's door was never knocked on; the real results folder and "
         "the real forward store are as they were; of every frozen file "
         "this gate read not one is in a real frozen folder; and the "
         "runner names no network library, no builder and not the live "
         "candle source",
         f"vault calls {len(VAULT_OPENED)}; frozen files read "
         f"{len(FILES_READ)}, all temporary")
    mark(len(BREAKS) + 1 == 10, "ten breaks, counted against a number "
                                "typed out here")
    EXPECTED_CHECKS = 34
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.6-F PASSED — {len(nonlocal_ok)} checks, 0 red.

THE FORWARD STORE HAS ONE SHAPE; the builder refuses a seam that does
not match the vault, a missing day and a second build, and prints no
price, rate or mood.

THE WHOLE LOOK WAS REHEARSED on made-up data through the Lab's real
engine: the pre-flight refused before the marker; ONLY TRADES ENTERED
AFTER THE LINE WERE SAVED OR PRINTED, though the same rules made
dozens before it; the money figure equals the saved trades re-worked
by hand; a second look was refused; and with everything after a chosen
forward day replaced, every earlier entry was identical.

WHAT THIS GATE DOES **NOT** PROVE. It has never seen a real forward
candle. It rehearses the machinery; it says nothing about whether
either rule makes money, and nothing about whether 113 days can.""")
    else:
        print(f"GATE 6.6-F FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
