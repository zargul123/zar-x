"""
Zar X Lab — BUILD THE FROZEN FUNDING. Run ONCE, by hand, never again.

Fetches every funding settlement of BTCUSDT, ETHUSDT and SOLUSDT that
Binance holds for the daily vault's 1,094 days (2023-07-28 00:00 UTC up to
but not including 2026-07-26 00:00 UTC) and freezes it in
`lab/funding_vault/` with checksums. The rules were declared in
PROGRESS_LOG.md on 2026-11-16 (evening), before this file existed.

**THIS IS THE ONLY FILE IN THE LAB'S SLOT 2 MACHINERY THAT TOUCHES THE
NETWORK, AND NOTHING THE GAUNTLET RUNS IMPORTS IT.** Like
`lab/build_vault.py`, it exists to be run once and then left alone.

  * It REFUSES to run if `lab/funding_vault/` already holds anything.
  * It freezes ALL THREE coins or NOTHING: every coin is fetched and
    checked (exactly 3,282 rows, three a day, on the clock, every rate a
    plain number under 5%) before one byte is written.
  * **IT PRINTS NO FUNDING RATE.** Row counts, dates and checksums only:
    the hold-out's rates are in what it fetches, and how often they were
    extreme is a result.

Its gate is GATE 6.3-D, in `lab/funding_vault.py --gate`, which runs this
file's fetch and build against a fake server.

RUN (from the zar-x folder), ONCE:
    python lab/build_funding_vault.py --freeze
"""
import os
import sys
from datetime import datetime, timezone

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)

import funding_vault as vault                              # noqa: E402

FAPI_BASE = 'https://fapi.binance.com'
PATH = '/fapi/v1/fundingRate'
PAGE = 1000            # the most rows Binance serves in one reply
MAX_PAGES = 50         # 3,282 rows is four pages; fifty is a runaway
TIMEOUT = 20


def binance(params):
    """One real request. The only line in the Lab's Slot 2 machinery that
    leaves this machine."""
    import requests
    reply = requests.get(FAPI_BASE + PATH, params=params, timeout=TIMEOUT)
    reply.raise_for_status()
    return reply.json()


def fetch_all(symbol, start_ms, end_ms, get):
    """Every settlement with start_ms <= time < end_ms, oldest first, as
    [(time_ms, rate_text)]. Page by page: each next page is asked from one
    millisecond after the last row of the page before."""
    rows, seen, cursor = [], set(), int(start_ms)
    for _page in range(MAX_PAGES):
        page = get({'symbol': symbol, 'startTime': cursor,
                    'endTime': int(end_ms) - 1, 'limit': PAGE})
        if not isinstance(page, list):
            raise ValueError(f'{symbol}: the reply is not a list of rows')
        if not page:
            return sorted(rows)
        stamped = sorted((int(row['fundingTime']), str(row['fundingRate']))
                         for row in page)
        for stamp, rate in stamped:
            if stamp in seen:
                raise ValueError(f'{symbol}: a settlement was served twice '
                                 f'(repeated time)')
            if not cursor <= stamp < end_ms:
                raise ValueError(f'{symbol}: a settlement outside the days '
                                 f'asked for')
            seen.add(stamp)
            rows.append((stamp, rate))
        if len(page) < PAGE:
            return sorted(rows)
        cursor = stamped[-1][0] + 1
    raise ValueError(f'{symbol}: more than {MAX_PAGES} pages')


def _day(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime(
        '%Y-%m-%d %H:%M')


def build(directory=None, get=None, out=print):
    """THE FREEZE. All three coins or nothing; refuses to overwrite."""
    directory = vault.FUNDING_DIR if directory is None else directory
    get = binance if get is None else get
    if os.path.isdir(directory) and os.listdir(directory):
        raise RuntimeError(f'REFUSED: {directory} already holds a freeze. '
                           f'Frozen funding is never rebuilt or refreshed.')
    fetched = {}
    for asset, contract in vault.CONTRACTS.items():
        rows = fetch_all(contract, vault.FIRST_MS, vault.END_MS, get)
        vault.check_rows(rows)
        fetched[contract] = rows
        out(f'   fetched {contract}: {len(rows)} settlements, '
            f'{_day(rows[0][0])} to {_day(rows[-1][0])} UTC')
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    manifest = vault.write_freeze(directory, fetched,
                                  note=f'frozen {stamp}')
    ok, lines = vault.verify(directory)
    if not ok:
        raise RuntimeError('the freeze did not verify: ' + '; '.join(lines))
    for name, entry in sorted(manifest['files'].items()):
        out(f'   froze {name}: {entry["rows"]} rows, {entry["bytes"]} '
            f'bytes, sha256 {entry["sha256"][:16]}')
    out(f'FROZEN: {len(fetched)} files in {directory}. Never refreshed.')
    return manifest


if __name__ == '__main__':
    if '--freeze' not in sys.argv:
        print(__doc__)
        print('REFUSED without `--freeze`. Nothing was fetched.')
        sys.exit(2)
    build()
