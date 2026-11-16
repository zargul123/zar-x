"""
Zar X Lab — BUILD THE FROZEN MOOD. Run ONCE, by hand, never again.

Fetches the Fear & Greed index history (alternative.me) and freezes one row
for each of the daily vault's 1,094 days (2023-07-28 to 2026-07-25) in
`lab/mood_vault/`, with a checksum. The rules were declared in
PROGRESS_LOG.md on 2026-11-16 (late night), before this file existed.

**THIS IS THE ONLY FILE IN SLOT 3's MACHINERY THAT TOUCHES THE NETWORK, AND
NOTHING THE GAUNTLET RUNS IMPORTS IT.**

  * It REFUSES to run if `lab/mood_vault/` already holds anything.
  * The publisher has no end-date: the WHOLE history arrives, the hold-out
    included. **IT PRINTS NO VALUE AND NO LABEL** - the row count, the
    dates, how many days were carried, and a checksum.
  * Every source row must be stamped exactly 00:00 UTC, be a whole number
    and appear once, or nothing is frozen.
  * A day the publisher never published carries the last value published
    BEFORE it and is marked; more than 3 in a row or 11 in all is a
    refusal.

Its gate is GATE 6.5-D, in `lab/mood_vault.py --gate`, which runs this
file's fetch and build against a fake server.

RUN (from the zar-x folder), ONCE:
    python lab/build_mood_vault.py --freeze
"""
import os
import sys
from datetime import datetime, timezone

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)

import mood_vault as vault                                 # noqa: E402

URL = 'https://api.alternative.me/fng/?limit=0&format=json'
TIMEOUT = 30


def alternative_me():
    """One real request. The only line in Slot 3's machinery that leaves
    this machine."""
    import requests
    reply = requests.get(URL, timeout=TIMEOUT,
                         headers={'User-Agent': 'python'})
    reply.raise_for_status()
    return reply.json()


def fetch_published(get):
    """The publisher's whole history -> {day_ms: (value, label)}.
    Refuses a row not stamped 00:00 UTC, a day served twice, and a value
    that is not a whole number. Labels are checked when the rows that are
    actually frozen are checked."""
    reply = get()
    data = reply.get('data') if isinstance(reply, dict) else None
    if not isinstance(data, list) or not data:
        raise ValueError('the reply is not a list of rows')
    published = {}
    for row in data:
        stamp = int(row['timestamp']) * 1000
        if stamp % vault.DAY_MS:
            raise ValueError('a row that is not stamped 00:00 UTC')
        if stamp in published:
            raise ValueError('a day was served twice')
        text = str(row['value']).strip()
        if not text.isdigit():
            raise ValueError('a value that is not a whole number')
        published[stamp] = (int(text), str(row['value_classification']))
    return published


def build(directory=None, get=None, out=print):
    """THE FREEZE. Refuses to overwrite; freezes nothing unless the whole
    shape is right."""
    directory = vault.MOOD_DIR if directory is None else directory
    get = alternative_me if get is None else get
    if os.path.isdir(directory) and os.listdir(directory):
        raise RuntimeError(f'REFUSED: {directory} already holds a freeze. '
                           f'The frozen mood is never rebuilt or refreshed.')
    published = fetch_published(get)
    rows = vault.build_rows(published)
    vault.check_rows(rows)
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    manifest = vault.write_freeze(directory, rows, note=f'frozen {stamp}')
    ok, lines = vault.verify(directory)
    if not ok:
        raise RuntimeError('the freeze did not verify: ' + '; '.join(lines))
    entry = manifest['files'][vault.FILE_NAME]
    out(f'   froze {vault.FILE_NAME}: {entry["rows"]} rows, '
        f'{rows[0][0]} to {rows[-1][0]}, {entry["carried"]} carried, '
        f'sha256 {entry["sha256"][:16]}')
    out(f'FROZEN in {directory}. Never refreshed.')
    return manifest


if __name__ == '__main__':
    if '--freeze' not in sys.argv:
        print(__doc__)
        print('REFUSED without `--freeze`. Nothing was fetched.')
        sys.exit(2)
    build()
