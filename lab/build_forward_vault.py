"""
Zar X Lab — BUILD THE FORWARD STORE for Forward Check 1. Run ONCE.

Fetches the 113 days after the vault's last candle (2026-07-26 to
2026-11-15) - daily candles, funding and the mood index - and freezes them
in `lab/forward_vault/` with checksums. The rules were declared in
PROGRESS_LOG.md on 2026-11-16, before this file existed.

**THE VAULT, THE FROZEN FUNDING AND THE FROZEN MOOD ARE NOT TOUCHED.** This
is the only file in the forward check's machinery that reaches the network,
and nothing the look runs imports it.

  * CANDLES come from the vault's own source (TwelveData, through the
    ship's `data/market_data.py`). **THE SEAM MUST MATCH:** the fetch also
    returns days the vault already holds, and those must equal the vault's
    rows for 2026-07-01 to 2026-07-25, value for value, or nothing is
    frozen.
  * FUNDING and MOOD are fetched and checked by the same code that built
    the frozen funding and the frozen mood, and written by their own
    `write_freeze`.
  * ALL THREE OR NOTHING: everything is fetched and checked before one
    byte is written. It refuses if the folder already holds anything.
  * **IT PRINTS NO PRICE, NO RATE AND NO MOOD.** Counts, dates, checksums.

Its gate is GATE 6.6-F, in `lab/forward_check.py --gate`, against fake
sources.

RUN (from the zar-x folder), ONCE:
    python lab/build_forward_vault.py --freeze
"""
import os
import sys

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(LAB_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, LAB_DIR)

import pandas as pd                                        # noqa: E402

import build_funding_vault                                 # noqa: E402
import build_mood_vault                                    # noqa: E402
import forward_check as forward                            # noqa: E402
import funding_vault                                       # noqa: E402
import mood_vault                                          # noqa: E402

SEAM_FROM = '2026-07-01'       # the overlap that must equal the vault
SEAM_DAYS = 25                 # 2026-07-01 to 2026-07-25
FETCH_DAYS = 170               # how far back the candle fetch reaches


def twelvedata(asset):
    """The vault's own candle source."""
    from data.market_data import MarketData
    return MarketData().get_history(asset, timeframe='1d', days=FETCH_DAYS)


def vault_daily(asset):
    """The vault's daily rows, read for the seam and for nothing else."""
    return pd.read_csv(os.path.join(LAB_DIR, 'vault', f'{asset}_1d.csv'),
                       index_col=0, parse_dates=True)


def real_sources():
    return {'candles': twelvedata, 'funding': build_funding_vault.binance,
            'mood': build_mood_vault.alternative_me}


def seam_matches(fetched, vault):
    """How many of the 25 overlapping days are in both and equal, value
    for value (to one part in a thousand million)."""
    days = pd.date_range(SEAM_FROM, periods=SEAM_DAYS, freq='1D')
    same = 0
    for day in days:
        if day not in fetched.index or day not in vault.index:
            continue
        a = fetched.loc[day, forward.COLUMNS].astype(float)
        b = vault.loc[day, forward.COLUMNS].astype(float)
        same += int(bool(((a - b).abs() <= 1e-9 * b.abs()).all()))
    return same


def build(directory=None, sources=None, vault_rows=None, out=print):
    """THE FREEZE. All three stores or nothing; refuses to overwrite."""
    directory = forward.FORWARD_DIR if directory is None else directory
    sources = real_sources() if sources is None else sources
    vault_rows = vault_daily if vault_rows is None else vault_rows
    if os.path.isdir(directory) and os.listdir(directory):
        raise RuntimeError(f'REFUSED: {directory} already holds a freeze. '
                           f'The forward store is never rebuilt.')
    first_ms = funding_vault.day_ms(forward.FIRST_DAY)
    end_ms = first_ms + forward.DAYS * funding_vault.DAY_MS

    candles = {}
    for asset in forward.ASSETS:
        fetched = sources['candles'](asset)
        if fetched is None or len(fetched) == 0:
            raise RuntimeError(f'the candle source returned nothing for '
                               f'{asset}')
        fetched = fetched[forward.COLUMNS].astype(float)
        fetched = fetched[~fetched.index.duplicated(keep='first')].sort_index()
        same = seam_matches(fetched, vault_rows(asset))
        if same != SEAM_DAYS:
            raise RuntimeError(
                f'REFUSED: the seam does not match for {asset}: {same} of '
                f'{SEAM_DAYS} overlapping days equal the vault. The new '
                f'candles do not continue the old ones.')
        new = fetched[(fetched.index >= forward.FIRST_DAY)
                      & (fetched.index <= forward.LAST_DAY)]
        forward.check_candles(new)
        candles[asset] = new
        out(f'   candles {asset}: {len(new)} days, {new.index[0].date()} to '
            f'{new.index[-1].date()}; seam {same} of {SEAM_DAYS} days equal '
            f'the vault')

    funding = {}
    for asset, contract in funding_vault.CONTRACTS.items():
        rows = build_funding_vault.fetch_all(contract, first_ms, end_ms,
                                             sources['funding'])
        funding_vault.check_rows(rows, first_ms, forward.DAYS)
        funding[contract] = rows
        out(f'   funding {contract}: {len(rows)} settlements')

    published = build_mood_vault.fetch_published(sources['mood'])
    mood_rows = mood_vault.build_rows(published, first_ms, forward.DAYS)
    mood_vault.check_rows(mood_rows, first_ms, forward.DAYS)
    out(f'   mood: {len(mood_rows)} days, '
        f'{sum(row[3] for row in mood_rows)} carried')

    forward.write_candles(os.path.join(directory, 'candles'), candles)
    funding_vault.write_freeze(os.path.join(directory, 'funding'), funding,
                               first_ms=first_ms, days=forward.DAYS)
    mood_vault.write_freeze(os.path.join(directory, 'mood'), mood_rows,
                            first_ms=first_ms, days=forward.DAYS)
    forward.preflight(directory)
    out(f'FROZEN: candles, funding and mood for {forward.FIRST_DAY} to '
        f'{forward.LAST_DAY} in {directory}. Never rebuilt.')


if __name__ == '__main__':
    if '--freeze' not in sys.argv:
        print(__doc__)
        print('REFUSED without `--freeze`. Nothing was fetched.')
        sys.exit(2)
    build()
