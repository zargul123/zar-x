"""
Zar X data — the open-interest recorder (Phase 3, Step 3.2b).

Open interest is the total value of futures contracts currently open. It says
how much money is committed to the market, which is a different question from
price. This part RECORDS it. It displays nothing: the Whale Watch instrument
that will read these files is Phase 3 #5, with its own step and its own gate.

**WHY THIS PART EXISTS AT ALL, AND WHY IT IS URGENT WHEN NOTHING ELSE HERE IS.**
Every other free source this ship uses serves deep history on demand — measured,
not assumed. Open interest does not. **Binance serves a 30-day window and
refuses anything older** (`startTime` 60 days back returns HTTP 400, code
-1130). Whatever falls out of that window is gone permanently and cannot be
bought back later at any price. There is no emergency — every read reaches back
30 days, so a recorder that runs even monthly loses nothing — but there is a
real deadline measured in weeks, and it is the only dataset on this ship with
one.

**THE TRAP THIS FILE IS SHAPED AROUND, MEASURED AND STILL LIVE. A bogus symbol
returns HTTP 200 with an empty list — it does NOT error.** This is the opposite
of the funding endpoint, which returns a clean HTTP 400 for the same mistake. A
recorder written the obvious way would read `[]`, append nothing, print "0 new
rows", exit 0 and report success — every month, while the 30-day window silently
rolled past, on the one dataset that cannot be recovered. **So an empty result
is a LOUD FAILURE here, never "no new data".**

Two smaller traps beside it, both measured: the field is `sumOpenInterest` in
the history endpoint but `openInterest` in the live snapshot endpoint — two
names for one idea, and assuming one from the other silently yields None; and
the payload carries an unplanned `CMCCirculatingSupply`, deliberately NOT stored
(it is not open interest, it is recoverable elsewhere at any time, and an unused
column invites a future session to misread the file).

**PERIOD = 4h, AND THAT IS NOT A PREFERENCE.** At limit=500 it is the only
setting that covers the whole window in one request per asset: 1h reaches back
just 20.8 days, so a recorder using it would silently lose nine days it believed
it had.

**THE NEWEST ROW IS STORED, MEASURED 2026-07-27.** A 4h row is a POINT SAMPLE
taken at the stamped instant, not a running aggregate over the following four
hours — 33 of 33 overlapping rows across the three assets matched the 5m reading
at the same instant exactly, while the 5m series moved on and the 4h row did
not. So a row is final the moment it appears and there is no incomplete period
to hold back. **If that measurement is ever wrong, this file says so instead of
hiding it:** history is never rewritten, and a re-read that disagrees with a
stored row is reported as a finding.

Fail-safe (Law 3): on ANY failure it reports honestly and **writes NOTHING**.
A truncated CSV is worse than no CSV.

Standalone smoke test:
    python data/open_interest.py     (gate 3.2b, including the sabotage drill)
"""
import csv
import os
import sys
from datetime import datetime, timezone

import requests

FAPI_BASE = 'https://fapi.binance.com'
HIST_PATH = '/futures/data/openInterestHist'
PERIOD = '4h'
LIMIT = 500            # 4h at limit 500 returns ~180 rows = the whole window
TIMEOUT = 15           # seconds; one attempt per asset, never a retry storm

HISTORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'oi_history')

# The perpetual contracts, same three assets the rest of the ship prices.
SYMBOLS = ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')

COLUMNS = ('timestamp', 'symbol', 'sumOpenInterest', 'sumOpenInterestValue')

# Used only by the offline drill: the .invalid top-level domain is reserved by
# the RFCs and can never resolve, so the drill proves the fail-safe without
# unplugging the Commander's internet.
OFFLINE_DRILL_URL = 'https://zar-x-offline-drill.invalid'


class RecorderError(Exception):
    """Anything that must stop this symbol's write. Never leaks a traceback to
    the caller; the doorway turns it into an honest line."""


def _utc_iso(ms: int) -> str:
    """Binance milliseconds -> UTC ISO 8601. The 'Z' is written explicitly so a
    stored timestamp can never be mistaken for local time by a later reader."""
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime(
        '%Y-%m-%dT%H:%M:%SZ')


def fetch_history(symbol, base_url=FAPI_BASE, period=PERIOD, limit=LIMIT,
                  timeout=TIMEOUT):
    """One request, no retries. Returns rows oldest-first.

    **An empty list is raised as an error, not returned as emptiness.** That is
    the whole point of this function: Binance answers a bogus symbol with
    HTTP 200 and `[]`, and treating that as "no new data" is how a recorder
    reports success for months while collecting nothing.
    """
    r = requests.get(f"{base_url}{HIST_PATH}",
                     params={'symbol': symbol, 'period': period,
                             'limit': limit}, timeout=timeout)
    r.raise_for_status()
    payload = r.json()
    if not isinstance(payload, list):
        raise RecorderError(f"{symbol}: response is not a list "
                            f"({type(payload).__name__})")
    if not payload:
        raise RecorderError(
            f"{symbol}: Binance returned HTTP 200 with an EMPTY LIST. This is "
            f"what a wrong symbol looks like — it is NOT 'no new data'.")

    rows = []
    for raw in payload:
        for field in ('timestamp', 'symbol', 'sumOpenInterest',
                      'sumOpenInterestValue'):
            if field not in raw:
                raise RecorderError(f"{symbol}: a row has no {field!r} — the "
                                    f"schema changed")
        if str(raw['symbol']) != symbol:
            raise RecorderError(f"{symbol}: a row is stamped "
                                f"{raw['symbol']!r} — wrong contract")
        rows.append({
            'timestamp': _utc_iso(int(raw['timestamp'])),
            'symbol': str(raw['symbol']),
            'sumOpenInterest': str(raw['sumOpenInterest']),
            'sumOpenInterestValue': str(raw['sumOpenInterestValue']),
        })
    rows.sort(key=lambda r: r['timestamp'])
    return rows


def csv_path(symbol, history_dir=HISTORY_DIR):
    return os.path.join(history_dir, f"{symbol}_{PERIOD}.csv")


def read_stored(symbol, history_dir=HISTORY_DIR):
    """Everything already on disk for this symbol, oldest-first. A missing file
    is an empty history, not an error — the first run has to start somewhere."""
    path = csv_path(symbol, history_dir)
    if not os.path.exists(path):
        return []
    with open(path, newline='', encoding='utf-8') as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def record(symbol, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
           period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
    """Fetch, compare, append. Returns a report dict; raises nothing to the
    caller except RecorderError, which `run()` turns into an honest line.

    **Append-only and idempotent.** Existing rows are never modified. Only
    timestamps not already stored are appended, so running this twice in a row
    writes nothing the second time and running it on any schedule is safe.

    **A disagreement is a FINDING, not a value to overwrite.** If Binance now
    reports a different number for a timestamp already on disk, that is
    reported and the stored row is left exactly as it was. Silently accepting
    the new number would erase the evidence that something is wrong.
    """
    fresh = fetch_history(symbol, base_url, period, limit, timeout)
    stored = read_stored(symbol, history_dir)
    by_key = {(r['symbol'], r['timestamp']): r for r in stored}

    new_rows, disagreements = [], []
    for row in fresh:
        key = (row['symbol'], row['timestamp'])
        old = by_key.get(key)
        if old is None:
            new_rows.append(row)
        elif (old['sumOpenInterest'] != row['sumOpenInterest']
              or old['sumOpenInterestValue'] != row['sumOpenInterestValue']):
            disagreements.append((row['timestamp'], old['sumOpenInterest'],
                                  row['sumOpenInterest']))

    if new_rows:
        os.makedirs(history_dir, exist_ok=True)
        path = csv_path(symbol, history_dir)
        exists = os.path.exists(path)
        # newline='' is required on Windows or csv writes a blank line between
        # every row, which would corrupt an append-only file quietly.
        with open(path, 'a', newline='', encoding='utf-8') as fh:
            writer = csv.DictWriter(fh, fieldnames=COLUMNS)
            if not exists:
                writer.writeheader()
            for row in new_rows:
                writer.writerow(row)

    return {
        'symbol': symbol,
        'fetched': len(fresh),
        'stored_before': len(stored),
        'appended': len(new_rows),
        'total': len(stored) + len(new_rows),
        'disagreements': disagreements,
        'span': (fresh[0]['timestamp'], fresh[-1]['timestamp']),
    }


def run(symbols=SYMBOLS, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
        period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
    """This part's single doorway. Never raises.

    Returns (ok, lines). **ok is False if ANY symbol failed** — a partial
    success on a dataset that expires is not a success, and a recorder that
    exits 0 while one asset silently collected nothing is the exact failure
    this part was written to prevent.
    """
    ok, lines = True, []
    for symbol in symbols:
        try:
            rep = record(symbol, base_url, history_dir, period, limit, timeout)
            lines.append(
                f"  {symbol}: {rep['appended']} new row(s) appended, "
                f"{rep['total']} stored, window {rep['span'][0]} → "
                f"{rep['span'][1]}")
            if rep['disagreements']:
                ok = False
                lines.append(
                    f"  !! {symbol}: {len(rep['disagreements'])} STORED ROW(S) "
                    f"DISAGREE with what Binance reports now. Nothing was "
                    f"overwritten. This is a finding, not a fix:")
                for when, was, now in rep['disagreements'][:5]:
                    lines.append(f"     {when}  stored {was}  →  now {now}")
        except Exception as e:
            ok = False
            # The reason is trimmed to one line on purpose. requests' network
            # errors carry a paragraph of urllib3 internals, and an "instrument
            # offline" line that fills the screen is not an honest line, it is
            # a traceback wearing a plug emoji. **RecorderError is never
            # trimmed** — those messages are written by this file, deliberately,
            # and the empty-list one has to be read in full to be understood.
            why = ' '.join(str(e).split())
            if not isinstance(e, RecorderError) and len(why) > 110:
                why = why[:107] + '...'
            lines.append(f"  🔌 {symbol}: NOT RECORDED — "
                         f"{type(e).__name__}: {why}")
    return ok, lines


if __name__ == '__main__':
    # =====================================================================
    # GATE 3.2b — declared 2026-07-26 in SESSION_ORDERS.md, re-confirmed with
    # its two design decisions in the PROGRESS_LOG entry of 2026-07-27, both
    # committed with NO .py file in them (Law 4).
    #
    # This recorder ships with its sabotage drill FROM BIRTH. Every part built
    # on this ship before it shipped with checks that had never been attacked,
    # and every one of them leaked when somebody finally tried: Gate 3.2
    # reported 48/48 with four lies walking through it, Gate 3.1-R let five
    # through, and both rebuilds were failed the next day by a session that
    # invented seven more. **A gate nobody has tried to break is a gate nobody
    # has tested**, and the cost of learning that was a voided 48/48.
    #
    # And the lesson those failures cost, applied here from the start
    # (check (i)): THE DRILL CHECKS WHAT IS WRITTEN TO DISK, not what the
    # parser returned. Both Context Deck instruments failed because every check
    # interrogated the parse and none compared the OUTPUT to the source. **The
    # recorder's equivalent of "the printed sentence" is THE CSV ROW.**
    # =====================================================================
    import shutil
    import tempfile

    ok = True
    print("GATE 3.2b — the open-interest recorder's self-test.")
    print("It breaks itself on purpose and requires every break to be CAUGHT,")
    print("because on this ship a check nobody has attacked is a check nobody")
    print("has tested. The dataset it guards cannot be recovered if it is lost.")

    # A scratch directory so the gate never depends on, or damages, the real
    # history. The real files are written by the live run in section (a) only.
    SCRATCH = tempfile.mkdtemp(prefix='zarx_oi_gate_')

    def _fresh_dir():
        d = tempfile.mkdtemp(prefix='zarx_oi_', dir=SCRATCH)
        return d

    def _rows(path):
        with open(path, newline='', encoding='utf-8') as fh:
            return list(csv.DictReader(fh))

    # ---- (a) BACKFILL ------------------------------------------------------
    print("\n(a) BACKFILL — from empty, one run must write >= 175 rows per")
    print("    asset for all three, spanning >= 29 days at period=4h.")
    backfill_dir = _fresh_dir()
    good, lines = run(history_dir=backfill_dir)
    for ln in lines:
        print(ln)
    if not good:
        print("   ✗ the backfill run itself reported a failure")
        ok = False
    for symbol in SYMBOLS:
        try:
            rows = _rows(csv_path(symbol, backfill_dir))
            first = datetime.strptime(rows[0]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            last = datetime.strptime(rows[-1]['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            days = (last - first).total_seconds() / 86400
            hit = len(rows) >= 175 and days >= 29
            print(f"   {'✓' if hit else '✗'} {symbol}: {len(rows)} rows "
                  f"spanning {days:.1f} days "
                  f"({rows[0]['timestamp']} → {rows[-1]['timestamp']})")
            ok = ok and hit
        except Exception as e:
            print(f"   ✗ {symbol}: could not read back: {type(e).__name__}: {e}")
            ok = False

    # ---- (b) IDEMPOTENCE ---------------------------------------------------
    print("\n(b) IDEMPOTENCE — run again immediately. Row counts identical and")
    print("    zero duplicates: distinct (symbol, timestamp) pairs must EQUAL")
    print("    total rows, printed side by side.")
    before_counts = {s: len(_rows(csv_path(s, backfill_dir))) for s in SYMBOLS}
    run(history_dir=backfill_dir)
    for symbol in SYMBOLS:
        rows = _rows(csv_path(symbol, backfill_dir))
        keys = {(r['symbol'], r['timestamp']) for r in rows}
        same = len(rows) == before_counts[symbol]
        nodupe = len(keys) == len(rows)
        print(f"   {'✓' if same and nodupe else '✗'} {symbol}: "
              f"{before_counts[symbol]} rows before → {len(rows)} after · "
              f"{len(rows)} total rows vs {len(keys)} distinct "
              f"(symbol, timestamp) pairs")
        ok = ok and same and nodupe

    # ---- (c) THE EMPTY-RESULT TRAP ----------------------------------------
    # Written as a function because the sabotage drill below uses THE SAME CODE
    # as its detector for B5. A check and the drill that proves the check works
    # must not be two different pieces of code that merely agree.
    def _trap_check(verbose=True):
        """True only if a bogus symbol FAILS LOUDLY: the run reports failure,
        no file is written, and the empty list is NAMED in the message."""
        say = print if verbose else (lambda *a, **k: None)
        trap_dir = _fresh_dir()
        trap_ok, trap_lines = run(symbols=('NOTAREALSYMBOL',),
                                  history_dir=trap_dir)
        for ln in trap_lines:
            say(ln)
        wrote = os.listdir(trap_dir) if os.path.isdir(trap_dir) else []
        named = any('EMPTY LIST' in ln for ln in trap_lines)
        good = (trap_ok is False) and not wrote and named
        say(f"   {'✓' if good else '✗'} reported failure: {not trap_ok} · "
            f"files written: {wrote or 'none'} · the empty list was NAMED in "
            f"the message: {named}")
        return good

    print("\n(c) THE EMPTY-RESULT TRAP — a bogus symbol returns HTTP 200 and an")
    print("    EMPTY LIST. It must FAIL LOUDLY, write no file, and never report")
    print("    success. A session that cannot demonstrate this has not passed.")
    trap_caught = _trap_check(verbose=True)
    ok = ok and trap_caught

    # ---- (d) OFFLINE DRILL -------------------------------------------------
    print("\n(d) OFFLINE DRILL — injected unreachable URL, internet untouched.")
    print("    Honest offline line, no traceback, and the CSVs byte-identical")
    print("    afterwards (checksum before and after, both printed).")
    import hashlib

    def _sig(d):
        h = hashlib.sha256()
        for name in sorted(os.listdir(d)):
            h.update(name.encode())
            with open(os.path.join(d, name), 'rb') as fh:
                h.update(fh.read())
        return h.hexdigest()[:16]

    before_sig = _sig(backfill_dir)
    off_ok, off_lines = run(base_url=OFFLINE_DRILL_URL,
                            history_dir=backfill_dir)
    for ln in off_lines:
        print(ln)
    after_sig = _sig(backfill_dir)
    off_caught = (off_ok is False and before_sig == after_sig
                  and all('🔌' in ln for ln in off_lines))
    print(f"   {'✓' if off_caught else '✗'} reported failure: {not off_ok} · "
          f"checksum before {before_sig} · after {after_sig} · "
          f"{'IDENTICAL' if before_sig == after_sig else 'CHANGED'}")
    ok = ok and off_caught

    # ---- (e) HISTORY IS NEVER REWRITTEN ------------------------------------
    print("\n(e) HISTORY IS NEVER REWRITTEN — hand-edit one stored value in a")
    print("    scratch copy, re-run, and confirm the tool REPORTS the")
    print("    disagreement instead of silently overwriting it.")
    edit_dir = _fresh_dir()
    shutil.copy(csv_path('BTCUSDT', backfill_dir), csv_path('BTCUSDT', edit_dir))
    rows = _rows(csv_path('BTCUSDT', edit_dir))
    victim = rows[len(rows) // 2]
    original_value = victim['sumOpenInterest']
    victim['sumOpenInterest'] = '999999.99999999'
    with open(csv_path('BTCUSDT', edit_dir), 'w', newline='',
              encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"    tampered with {victim['timestamp']}: "
          f"{original_value} → 999999.99999999")
    edit_ok, edit_lines = run(symbols=('BTCUSDT',), history_dir=edit_dir)
    for ln in edit_lines:
        print(ln)
    after_rows = _rows(csv_path('BTCUSDT', edit_dir))
    still_there = any(r['timestamp'] == victim['timestamp']
                      and r['sumOpenInterest'] == '999999.99999999'
                      for r in after_rows)
    reported = any('DISAGREE' in ln for ln in edit_lines)
    edit_caught = reported and (edit_ok is False) and still_there
    print(f"   {'✓' if edit_caught else '✗'} disagreement REPORTED: {reported} "
          f"· run marked failed: {not edit_ok} · tampered row left untouched "
          f"rather than overwritten: {still_there}")
    ok = ok and edit_caught

    # ---- (g) THE DATA IS PLAUSIBLE ----------------------------------------
    print("\n(g) THE DATA IS PLAUSIBLE — the stored BTC figure is checked")
    print("    against Binance's own LIVE snapshot endpoint, which is a")
    print("    different endpoint with a different field name. A recorder that")
    print("    faithfully stores nonsense is not a working recorder.")
    try:
        live = requests.get(f"{FAPI_BASE}/fapi/v1/openInterest",
                            params={'symbol': 'BTCUSDT'},
                            timeout=TIMEOUT).json()
        live_oi = float(live['openInterest'])
        stored_oi = float(_rows(csv_path('BTCUSDT', backfill_dir))[-1]
                          ['sumOpenInterest'])
        drift = abs(stored_oi - live_oi) / live_oi * 100
        near = drift < 10
        print(f"   {'✓' if near else '✗'} newest stored {stored_oi:,.3f} BTC vs "
              f"live snapshot {live_oi:,.3f} BTC → {drift:.2f}% apart "
              f"(the stored row is a point sample up to 4h old, so a few "
              f"percent is expected; 10% is the bar)")
        ok = ok and near
    except Exception as e:
        print(f"   ✗ plausibility check failed: {type(e).__name__}: {e}")
        ok = False

    # ---- (h)+(i) THE SABOTAGE DRILL, AND IT JUDGES THE FILE ON DISK -------
    print("\n(h) THE SABOTAGE DRILL, BUILT IN FROM BIRTH — this file is broken")
    print("    on purpose SIX ways and each break MUST be caught.")
    print("(i) AND THE DETECTOR READS THE CSV BACK OFF DISK and compares it,")
    print("    field by field, to a raw fetch the TEST makes itself — never to")
    print("    anything this file parsed. That is the lesson two Context Deck")
    print("    gates cost: check what is WRITTEN, not what the parser returned.")

    def _raw_truth(symbol='BTCUSDT'):
        """Fetched by the TEST, straight from Binance, passing through none of
        this file's helpers."""
        payload = requests.get(f"{FAPI_BASE}{HIST_PATH}",
                               params={'symbol': symbol, 'period': PERIOD,
                                       'limit': LIMIT},
                               timeout=TIMEOUT).json()
        truth = {}
        for raw in payload:
            stamp = datetime.fromtimestamp(int(raw['timestamp']) / 1000,
                                           timezone.utc).strftime(
                                               '%Y-%m-%dT%H:%M:%SZ')
            truth[stamp] = (str(raw['sumOpenInterest']),
                            str(raw['sumOpenInterestValue']))
        return truth

    def _disk_matches_source(verbose=False):
        """THE DETECTOR. Writes a fresh file, reads it back off disk, and
        compares every row to raw. Returns True if the file on disk is a
        faithful record of what Binance served."""
        d = _fresh_dir()
        good, _ = run(symbols=('BTCUSDT',), history_dir=d)
        if not good:
            return False
        path = csv_path('BTCUSDT', d)
        if not os.path.exists(path):
            return False
        rows = _rows(path)
        truth = _raw_truth()
        if len(rows) < 175:
            return False
        for r in rows:
            want = truth.get(r['timestamp'])
            if want is None:
                if verbose:
                    print(f"      row {r['timestamp']} is on disk but not in "
                          f"the source")
                return False
            if (r['sumOpenInterest'], r['sumOpenInterestValue']) != want:
                if verbose:
                    print(f"      row {r['timestamp']}: disk "
                          f"{r['sumOpenInterest']} vs source {want[0]}")
                return False
            if r['symbol'] != 'BTCUSDT':
                return False
        # every source row inside the written window must be present
        stamps = {r['timestamp'] for r in rows}
        missing = [t for t in truth if t not in stamps]
        if missing:
            if verbose:
                print(f"      {len(missing)} source row(s) never reached disk, "
                      f"e.g. {sorted(missing)[:3]}")
            return False
        return True

    _UTC_ISO_ORIGINAL = _utc_iso
    _RECORD_ORIGINAL = record

    def _sab_dedup_drops(symbol, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
                         period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
        """De-dup key reduced to the timestamp's DATE, so all but one row per
        day is silently discarded — the classic silent-loss bug."""
        fresh = fetch_history(symbol, base_url, period, limit, timeout)
        seen, keep = set(), []
        for row in fresh:
            day = row['timestamp'][:10]
            if day in seen:
                continue
            seen.add(day)
            keep.append(row)
        os.makedirs(history_dir, exist_ok=True)
        path = csv_path(symbol, history_dir)
        exists = os.path.exists(path)
        with open(path, 'a', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            if not exists:
                w.writeheader()
            w.writerows(keep)
        return {'symbol': symbol, 'fetched': len(fresh), 'stored_before': 0,
                'appended': len(keep), 'total': len(keep), 'disagreements': [],
                'span': (fresh[0]['timestamp'], fresh[-1]['timestamp'])}

    def _sab_wrong_column(symbol, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
                          period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
        """The VALUE column written into the open-interest column: the two
        fields are adjacent in the payload and easy to transpose."""
        rep = _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                               timeout)
        path = csv_path(symbol, history_dir)
        rows = _rows(path)
        for r in rows:
            r['sumOpenInterest'] = r['sumOpenInterestValue']
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(rows)
        return rep

    def _sab_rounded(symbol, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
                     period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
        """The figure rounded to whole coins on the way to disk. Every row
        still looks entirely reasonable — which is exactly why a check that
        only asked "is this a number?" would never see it."""
        rep = _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                               timeout)
        path = csv_path(symbol, history_dir)
        rows = _rows(path)
        for r in rows:
            r['sumOpenInterest'] = f"{float(r['sumOpenInterest']):.0f}"
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(rows)
        return rep

    def _sab_naive_recorder(symbol, base_url=FAPI_BASE,
                            history_dir=HISTORY_DIR, period=PERIOD,
                            limit=LIMIT, timeout=TIMEOUT):
        """**THE WHOLE REASON THIS FILE EXISTS, WRITTEN THE OBVIOUS WAY.**

        Fetch, and if the list comes back empty just report "0 new rows" and
        carry on. No raise, no complaint, exit 0. This is what a careful
        programmer who had not measured the endpoint would produce — and it
        would report success every month while the 30-day window rolled past.
        It is judged by `_trap_check`, the SAME code section (c) uses, so the
        drill proves the actual check rather than a copy of it."""
        r = requests.get(f"{base_url}{HIST_PATH}",
                         params={'symbol': symbol, 'period': period,
                                 'limit': limit}, timeout=timeout)
        r.raise_for_status()
        payload = r.json()
        if not payload:
            return {'symbol': symbol, 'fetched': 0, 'stored_before': 0,
                    'appended': 0, 'total': 0, 'disagreements': [],
                    'span': ('—', '—')}
        return _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                                timeout)

    # The last column is WHICH JUDGE decides. B5 corrupts only the bogus-symbol
    # path, which a healthy BTCUSDT write cannot see; judging it by the disk
    # comparison would record a guaranteed escape as if the gate were blind.
    _SABOTAGES = [
        ('B1', 'timestamps converted as LOCAL time', '_utc_iso',
         lambda ms: datetime.fromtimestamp(ms / 1000).strftime(
             '%Y-%m-%dT%H:%M:%SZ'), 'disk'),
        ('B2', 'timestamps shifted by one hour', '_utc_iso',
         lambda ms: datetime.fromtimestamp(ms / 1000 + 3600,
                                           timezone.utc).strftime(
             '%Y-%m-%dT%H:%M:%SZ'), 'disk'),
        ('B3', 'de-dup key silently drops rows', 'record', _sab_dedup_drops,
         'disk'),
        ('B4', 'the VALUE column written into the OI column', 'record',
         _sab_wrong_column, 'disk'),
        ('B5', 'the naive recorder: empty = "no new data"', 'record',
         _sab_naive_recorder, 'trap'),
        ('B6', 'the number rounded on the way to disk', 'record',
         _sab_rounded, 'disk'),
    ]

    drill_ok = True
    for tag, words, attr, repl, judge in _SABOTAGES:
        original = globals()[attr]
        globals()[attr] = repl
        try:
            survived = (_trap_check(verbose=False) if judge == 'trap'
                        else _disk_matches_source())
        except Exception:
            survived = False        # a crash is a catch: it did not pass
        finally:
            globals()[attr] = original
        caught = not survived
        print(f"   {'✓' if caught else '✗'} {tag}  {words:<44} → "
              f"{'CAUGHT' if caught else 'ESCAPED — THE GATE IS DECORATIVE'}")
        drill_ok = drill_ok and caught

    restored = _disk_matches_source(verbose=True) and _trap_check(verbose=False)
    print(f"   {'✓' if restored else '✗'} every original restored — a freshly "
          f"written CSV matches the source row for row, and the empty-result "
          f"trap still fails loudly")
    ok = ok and drill_ok and restored

    # ---- (f) THE BRIEF IS UNAFFECTED --------------------------------------
    print("\n(f) THE BRIEF IS UNAFFECTED — this step touches no cockpit file,")
    print("    so this should be trivially true. Verified anyway.")
    print("    (run `python cockpit\\brief.py` — checked in the shell and")
    print("    recorded in PROGRESS_LOG.md; not imported here, because a")
    print("    recorder that imports the cockpit is no longer a sealed part.)")

    shutil.rmtree(SCRATCH, ignore_errors=True)

    if ok:
        print("\nGATE 3.2b PASSED — the backfill is real, the same run twice")
        print("changes nothing, an empty result fails loudly, the offline drill")
        print("leaves the files byte-identical, tampered history is reported")
        print("rather than overwritten, and all six deliberate sabotages were")
        print("caught by reading the CSV back off disk and comparing it to")
        print("Binance. This test has demonstrated, this run, that it can say no.")
    else:
        print("\nGATE 3.2b FAILED — see the ✗ lines above. Nothing is committed")
        print("as a pass.")
    sys.exit(0 if ok else 1)
