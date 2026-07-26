"""
Zar X Lab — Step 2.2: THE DATA VALIDATOR (the quality inspector at the door).

WHY THIS EXISTS
Garbage in = lies out. A backtest cannot tell the difference between a real
crash and a broken candle — it will happily "buy the dip" at a price that
never existed and report a profit that never existed. So nothing enters the
Lab without passing this door first, and no vault file is born without
passing it either.

WHAT IT LOOKS FOR (the plan's list, in plain words):
  - missing candles     — holes in the timeline vs the timeframe's own grid
  - duplicate timestamps— the same candle counted twice
  - impossible prices   — zero, negative, or blank
  - high below low      — a candle that contradicts itself
  - impossible candles  — a price that moved more than 100% inside ONE candle
                          (a liquid pair does not double or halve in 4 hours;
                          that is the data source glitching, not the market)
  - absurd moves        — more than 25% in one candle: FLAGGED, never deleted.
                          Crypto really does have 30% days; the inspector says
                          "look at this", it does not throw data away.

THE THREE VERDICTS
  PASS — nothing found. Safe to test on.
  WARN — nothing impossible, but something worth a human's eyes (holes in the
         timeline, violent-but-real candles). Usable, knowingly.
  FAIL — the data contradicts reality. Any backtest built on it is a lie.

It never modifies, cleans, or deletes anything. It reads and it reports.
Deciding what to do about a disease is the Commander's job, not the door's.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\validator.py
        ... inspects every file in lab/vault/
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\validator.py <file.csv> [4h|1d]
        ... inspects one file
"""
import sys
import os

import pandas as pd

VAULT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vault')

# How big a single-candle move has to be before the inspector speaks.
ABSURD_MOVE = 0.25        # 25% — "flag, don't delete" (the plan's word)
IMPOSSIBLE_MOVE = 1.00    # 100% inside one candle — not a market, a glitch

# The grid each timeframe's candles must sit on.
TIMEFRAME_STEP = {
    '1m': pd.Timedelta(minutes=1), '5m': pd.Timedelta(minutes=5),
    '15m': pd.Timedelta(minutes=15), '30m': pd.Timedelta(minutes=30),
    '1h': pd.Timedelta(hours=1), '4h': pd.Timedelta(hours=4),
    '1d': pd.Timedelta(days=1),
}

PRICE_COLS = ['open', 'high', 'low', 'close']


class Report:
    """What the inspector saw. Diseases (FAIL) and concerns (WARN) kept apart:
    a disease means the data lies; a concern means a human should look."""

    def __init__(self, name, timeframe):
        self.name = name
        self.timeframe = timeframe
        self.diseases = []    # (headline, [example lines])  -> FAIL
        self.concerns = []    # (headline, [example lines])  -> WARN
        self.facts = []

    def disease(self, headline, examples=None):
        self.diseases.append((headline, examples or []))

    def concern(self, headline, examples=None):
        self.concerns.append((headline, examples or []))

    @property
    def verdict(self):
        if self.diseases:
            return 'FAIL'
        if self.concerns:
            return 'WARN'
        return 'PASS'

    def text(self):
        lines = [f'--- INSPECTING: {self.name}  (timeframe {self.timeframe}) ---']
        lines += [f'  {f}' for f in self.facts]
        if self.diseases:
            lines.append('  DISEASES FOUND (the data contradicts reality):')
            for headline, examples in self.diseases:
                lines.append(f'    ✗ {headline}')
                lines += [f'        {e}' for e in examples]
        if self.concerns:
            lines.append('  FLAGGED FOR HUMAN EYES (not deleted, not judged):')
            for headline, examples in self.concerns:
                lines.append(f'    ! {headline}')
                lines += [f'        {e}' for e in examples]
        if not self.diseases and not self.concerns:
            lines.append('  Nothing wrong found.')
        lines.append(f'  VERDICT: {self.verdict}')
        return '\n'.join(lines)


def _examples(index, limit=5):
    """Name names — a count alone is not evidence."""
    shown = [str(t) for t in list(index)[:limit]]
    extra = len(index) - len(shown)
    if extra > 0:
        shown.append(f'... and {extra} more')
    return shown


def validate_candles(df, timeframe='4h', name='(unnamed)',
                     absurd_move=ABSURD_MOVE, impossible_move=IMPOSSIBLE_MOVE):
    """Inspect a candle DataFrame (index = candle open time, columns
    open/high/low/close, volume optional). Returns a Report. Reads only."""
    rep = Report(name, timeframe)

    # --- Can this even be called candles? ---
    if df is None or len(df) == 0:
        rep.disease('The table is empty — there are no candles at all.')
        return rep

    missing_cols = [c for c in PRICE_COLS if c not in df.columns]
    if missing_cols:
        rep.disease(f'Missing price columns: {", ".join(missing_cols)}. '
                    f'Found instead: {", ".join(map(str, df.columns))}.')
        return rep

    if not isinstance(df.index, pd.DatetimeIndex):
        rep.disease('The candle times are not real dates — this table cannot '
                    'be placed on a timeline.')
        return rep

    prices = df[PRICE_COLS]
    rep.facts.append(f'{len(df)} candles, {df.index.min()} → {df.index.max()}')
    if 'volume' not in df.columns:
        rep.facts.append('No volume column (this source gives none) — OHLC only.')

    # --- Out of order? Not a disease, but everything downstream assumes order.
    if not df.index.is_monotonic_increasing:
        rep.concern('The candles are not in time order (the Lab sorts before '
                    'testing, but a shuffled file usually means something odd).')

    # --- DISEASE: the same candle counted twice ---
    dup_mask = df.index.duplicated(keep=False)
    if dup_mask.any():
        dup_times = pd.Index(sorted(set(df.index[dup_mask])))
        rep.disease(
            f'DUPLICATE TIMESTAMPS: {int(dup_mask.sum())} rows share '
            f'{len(dup_times)} candle time(s) — the same moment counted twice.',
            _examples(dup_times))

    # --- DISEASE: blank prices ---
    nan_rows = prices[prices.isna().any(axis=1)]
    if len(nan_rows):
        rep.disease(f'BLANK PRICES (NaN): {len(nan_rows)} candle(s) have an '
                    f'empty open/high/low/close.', _examples(nan_rows.index))

    # --- DISEASE: zero or negative prices ---
    nonpos = prices[(prices <= 0).any(axis=1)]
    if len(nonpos):
        ex = [f'{t}  open={r.open:g} high={r.high:g} low={r.low:g} close={r.close:g}'
              for t, r in nonpos.head(5).iterrows()]
        if len(nonpos) > 5:
            ex.append(f'... and {len(nonpos) - 5} more')
        rep.disease(f'ZERO OR NEGATIVE PRICES: {len(nonpos)} candle(s). '
                    f'A price cannot be zero or below.', ex)

    # --- DISEASE: a candle that contradicts itself ---
    valid = prices.dropna()
    hi_lo = valid[valid['high'] < valid['low']]
    if len(hi_lo):
        ex = [f'{t}  high={r.high:g} < low={r.low:g}' for t, r in hi_lo.head(5).iterrows()]
        rep.disease(f'HIGH BELOW LOW: {len(hi_lo)} candle(s) — the top of the '
                    f'candle is under its bottom.', ex)

    body_max = valid[['open', 'close']].max(axis=1)
    body_min = valid[['open', 'close']].min(axis=1)
    incoherent = valid[(valid['high'] < body_max) | (valid['low'] > body_min)]
    if len(incoherent):
        ex = [f'{t}  open={r.open:g} high={r.high:g} low={r.low:g} close={r.close:g}'
              for t, r in incoherent.head(5).iterrows()]
        rep.disease(f'IMPOSSIBLE CANDLE SHAPE: {len(incoherent)} candle(s) where '
                    f'the high is not the highest price or the low is not the '
                    f'lowest.', ex)

    # --- DISEASE: a move no real market makes inside one candle ---
    positive = valid[(valid > 0).all(axis=1)]
    if len(positive):
        span = positive['high'] / positive['low'] - 1
        impossible = positive[span > impossible_move]
        if len(impossible):
            ex = [f'{t}  low={r.low:g} → high={r.high:g}  '
                  f'({(r.high / r.low - 1) * 100:,.0f}% inside one candle; '
                  f'open={r.open:g} close={r.close:g})'
                  for t, r in impossible.head(5).iterrows()]
            if len(impossible) > 5:
                ex.append(f'... and {len(impossible) - 5} more')
            rep.disease(
                f'IMPOSSIBLE PRICE INSIDE A CANDLE: {len(impossible)} candle(s) '
                f'where the price moved more than {impossible_move:.0%} between '
                f'the low and the high. A liquid pair does not do that — this is '
                f'the data source glitching (usually a decimal point in the wrong '
                f'place).', ex)

        # --- CONCERN: violent but possible ---
        absurd = positive[(span > absurd_move) & (span <= impossible_move)]
        if len(absurd):
            ex = [f'{t}  {(r.high / r.low - 1) * 100:.1f}% low-to-high '
                  f'(low={r.low:g} high={r.high:g})'
                  for t, r in absurd.head(5).iterrows()]
            if len(absurd) > 5:
                ex.append(f'... and {len(absurd) - 5} more')
            rep.concern(f'BIG SINGLE-CANDLE SWINGS: {len(absurd)} candle(s) moved '
                        f'more than {absurd_move:.0%} from low to high. Crypto '
                        f'really does this — flagged, not deleted.', ex)

    closes = valid['close']
    if len(closes) > 1:
        step_move = closes.pct_change().abs()
        jumpy = closes[step_move > absurd_move]
        if len(jumpy):
            ex = [f'{t}  {step_move[t] * 100:.1f}% versus the candle before '
                  f'(close={closes[t]:g})' for t in jumpy.index[:5]]
            if len(jumpy) > 5:
                ex.append(f'... and {len(jumpy) - 5} more')
            rep.concern(f'BIG CANDLE-TO-CANDLE JUMPS: {len(jumpy)} close price(s) '
                        f'moved more than {absurd_move:.0%} from the previous '
                        f'close.', ex)

    # --- CONCERN: holes in the timeline ---
    step = TIMEFRAME_STEP.get(timeframe)
    if step is None:
        rep.concern(f'Unknown timeframe "{timeframe}" — cannot check for missing '
                    f'candles (the grid is unknown).')
    elif df.index.is_monotonic_increasing and len(df) > 1:
        unique_index = pd.DatetimeIndex(sorted(set(df.index)))
        grid = pd.date_range(unique_index[0], unique_index[-1], freq=step)
        off_grid = unique_index.difference(grid)
        holes = grid.difference(unique_index)
        if len(off_grid):
            rep.concern(f'OFF-GRID CANDLES: {len(off_grid)} candle time(s) do not '
                        f'sit on the {timeframe} clock.', _examples(off_grid))
        if len(holes):
            gaps = df.index.to_series().diff().dropna()
            biggest = gaps.max() if len(gaps) else step
            rep.concern(
                f'MISSING CANDLES: {len(holes)} hole(s) in the timeline out of '
                f'{len(grid)} expected ({len(holes) / len(grid) * 100:.2f}%). '
                f'Biggest single gap: {biggest}.', _examples(holes))

    return rep


def validate_csv(path, timeframe=None):
    """Inspect one candle CSV on disk. Never writes."""
    name = os.path.basename(path)
    if timeframe is None:
        stem = os.path.splitext(name)[0]
        timeframe = stem.rsplit('_', 1)[-1] if '_' in stem else '4h'
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return validate_candles(df, timeframe=timeframe, name=name)


def validate_vault():
    """Inspect every CSV in the frozen vault. Reads only — the vault is
    evidence and is never touched."""
    files = sorted(f for f in os.listdir(VAULT_DIR) if f.endswith('.csv'))
    reports = [validate_csv(os.path.join(VAULT_DIR, f)) for f in files]
    return reports


def main(argv):
    print('=' * 70)
    print('ZAR X LAB — DATA VALIDATOR (the inspector at the door)')
    print('=' * 70)

    if len(argv) > 1:
        path = argv[1]
        tf = argv[2] if len(argv) > 2 else None
        if not os.path.exists(path):
            print(f'No such file: {path}')
            return 1
        rep = validate_csv(path, tf)
        print(rep.text())
        return 0 if rep.verdict != 'FAIL' else 1

    if not os.path.isdir(VAULT_DIR):
        print('No vault found. Build it first: lab/build_vault.py')
        return 1

    reports = validate_vault()
    for rep in reports:
        print(rep.text())
        print()

    print('=' * 70)
    for rep in reports:
        print(f'  {rep.verdict:<5} {rep.name}')
    failed = [r for r in reports if r.verdict == 'FAIL']
    warned = [r for r in reports if r.verdict == 'WARN']
    print('-' * 70)
    if failed:
        print(f'RESULT: {len(failed)} file(s) FAILED the door. '
              f'They must NOT be used for backtesting until this is explained.')
    elif warned:
        print(f'RESULT: no diseases. {len(warned)} file(s) carry flags for '
              f'human eyes.')
    else:
        print('RESULT: every file PASSED. The data is clean.')
    print('=' * 70)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
