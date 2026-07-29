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
    import re
    import shutil
    import subprocess
    import tempfile

    # --- `--record`: DO THE JOB, don't test it ---------------------------
    # The monthly laptop task calls this. It is deliberately NOT the gate:
    # the gate makes many extra requests, writes to scratch directories, and
    # its exit code answers "is the test suite green?" — a different question
    # from "was the data recorded?". A scheduled task must exit non-zero when
    # THE JOB failed, or the alarm is decorative.
    if '--record' in sys.argv:
        print(f"Zar X open-interest recorder — "
              f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC")
        recorded, report = run()
        for line in report:
            print(line)
        if recorded:
            print("Recorded. The 30-day window is captured.")
        else:
            print("NOT RECORDED — see the lines above. Nothing was written.")
        sys.exit(0 if recorded else 1)

    # =====================================================================
    # GATE 3.2b-R2, added 2026-07-28 (evening) after an independent session
    # threw an EIGHTH and a NINTH sabotage at Gate 3.2b-R and BOTH walked
    # through.
    #
    # **THE GATE TOOK ITS LIST OF WHAT TO CHECK FROM THE MODULE IT WAS
    # CHECKING.** Every loop below said `for symbol in SYMBOLS`. B9 cut SYMBOLS
    # from three assets to two; SOLUSDT then appeared nowhere in the recorder,
    # nowhere in the gate, and nowhere in the output — and the gate printed
    # PASSED, exit 0, while announcing in its own words that it now checks
    # "ALL THREE assets".
    #
    # One third of the only dataset on this ship that CANNOT BE BOUGHT BACK AT
    # ANY PRICE would have stopped being collected, permanently, with every
    # check green. That is B7's lesson — two of three assets guarded by a row
    # count — one level up: all three guarded by a list the module hands over.
    #
    # The gate now holds its own list, checks the module's against it by name,
    # and every loop below runs over the GATE'S copy.
    # =====================================================================
    GATE_SYMBOLS = ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')

    ok = True
    print("GATE 3.2b-R5 — the open-interest recorder's self-test.")
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
    print("    Gate 3.2b-R2: the assets are named by THE GATE, not read from")
    print("    the module. `run()` is called with no symbol list, exactly as")
    print("    the monthly task calls it, and must produce a full window for")
    print("    every asset THIS FILE says the ship collects. B9 deleted SOLUSDT")
    print("    from the module's list and the whole gate simply looked away.")
    symbols_ok = (tuple(SYMBOLS) == GATE_SYMBOLS)
    print(f"   {'✓' if symbols_ok else '✗'} the module's SYMBOLS "
          f"{tuple(SYMBOLS)} equals the gate's own copy {GATE_SYMBOLS}")
    ok = ok and symbols_ok
    backfill_dir = _fresh_dir()
    good, lines = run(history_dir=backfill_dir)
    for ln in lines:
        print(ln)
    if not good:
        print("   ✗ the backfill run itself reported a failure")
        ok = False
    for symbol in GATE_SYMBOLS:
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
    before_counts = {s: len(_rows(csv_path(s, backfill_dir)))
                     for s in GATE_SYMBOLS}
    run(history_dir=backfill_dir)
    for symbol in GATE_SYMBOLS:
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

    # ---- (j) THE PATH THAT ACTUALLY RUNS UNATTENDED -----------------------
    print("\n(j) THE `--record` BRANCH IS RUN FOR REAL — Gate 3.2b-R2 (c).")
    print("    `--record` is what the monthly scheduled task calls, and until")
    print("    today NOTHING anywhere ran it. Sabotage B8 changed its exit code")
    print("    to always 0: the job failed, printed NOT RECORDED, wrote nothing")
    print("    and reported SUCCESS to Task Scheduler — and this gate passed,")
    print("    because it never went near the branch. The one path that runs")
    print("    unattended, on the one dataset that expires, was the one path")
    print("    with no coverage. Both outcomes are now driven for real.")

    THIS_FILE = os.path.abspath(__file__)

    def _record_run(work_dir, base_url=None):
        """Run `--record` on a COPY of this file placed in `work_dir`.

        The copy is what makes this safe: `HISTORY_DIR` is derived from the
        file's OWN location, so a copy in a scratch directory can only ever
        write to that scratch directory. **`data/oi_history/` cannot be touched
        by this check even if it is wrong.**"""
        dest = os.path.join(work_dir, 'oi_under_test.py')
        with open(THIS_FILE, encoding='utf-8') as fh:
            src = fh.read()
        if base_url is not None:
            # The newlines are load-bearing. Without them the anchor also
            # matches THIS LINE, because the anchor is written in this file —
            # which the first run of this check discovered by refusing to run.
            # Anchored to a whole line, only the real constant matches.
            anchor = "\nFAPI_BASE = 'https://fapi.binance.com'\n"
            if src.count(anchor) != 1:
                raise RecorderError("the FAPI_BASE anchor matched "
                                    f"{src.count(anchor)} times — refusing to "
                                    "edit rather than guess which")
            src = src.replace(anchor, f"\nFAPI_BASE = '{base_url}'\n")
        with open(dest, 'w', encoding='utf-8', newline='') as fh:
            fh.write(src)
        p = subprocess.run([sys.executable, dest, '--record'],
                           capture_output=True, text=True, timeout=300)
        return p.returncode, (p.stdout or '') + (p.stderr or '')

    def _record_does_the_job(verbose=False):
        """The success half: `--record` must exit 0 AND leave a real window on
        disk for every asset. An exit code nobody earned is not a result."""
        say = print if verbose else (lambda *a, **k: None)
        d = _fresh_dir()
        code, out = _record_run(d)
        hist = os.path.join(d, 'oi_history')
        counts = {}
        for s in GATE_SYMBOLS:
            path = csv_path(s, hist)
            counts[s] = len(_rows(path)) if os.path.exists(path) else 0
        full = all(n >= 175 for n in counts.values())
        good = (code == 0) and ('Recorded.' in out) and full
        say(f"   {'✓' if good else '✗'} the job succeeded → exit {code} "
            f"(must be 0) · 'Recorded.' printed: {'Recorded.' in out} · "
            f"rows written {counts}")
        return good

    def _record_alarm_fires(verbose=False, source_override=None):
        """**THE BAR B8 BROKE.** When the job fails, `--record` must exit
        NON-ZERO. Driven through the real mechanism — a copy pointed at the
        unreachable address, which is exactly what the Commander's laptop looks
        like with no internet on the 1st of the month.

        The drill below judges B8 with THIS function, not with a second copy of
        the same idea, so the drill proves the actual check."""
        say = print if verbose else (lambda *a, **k: None)
        d = _fresh_dir()
        if source_override is not None:
            dest = os.path.join(d, 'oi_under_test.py')
            with open(dest, 'w', encoding='utf-8', newline='') as fh:
                fh.write(source_override)
            p = subprocess.run([sys.executable, dest, '--record'],
                               capture_output=True, text=True, timeout=300)
            code, out = p.returncode, (p.stdout or '') + (p.stderr or '')
        else:
            code, out = _record_run(d, base_url=OFFLINE_DRILL_URL)
        hist = os.path.join(d, 'oi_history')
        wrote = sorted(os.listdir(hist)) if os.path.isdir(hist) else []
        said = 'NOT RECORDED' in out
        good = (code != 0) and said and not wrote
        say(f"   {'✓' if good else '✗'} the job failed → exit {code} (must be "
            f"NON-ZERO, or the alarm is decorative) · 'NOT RECORDED' printed: "
            f"{said} · files written: {wrote or 'none'}")
        return good

    job_ok = _record_does_the_job(verbose=True)
    alarm_ok = _record_alarm_fires(verbose=True)
    ok = ok and job_ok and alarm_ok

    # ---- (g) THE DATA IS PLAUSIBLE ----------------------------------------
    print("\n(g) THE DATA IS PLAUSIBLE — the stored figure for EVERY asset is")
    print("    checked against Binance's own LIVE snapshot endpoint, which is")
    print("    a different endpoint with a different field name. A recorder")
    print("    that faithfully stores nonsense is not a working recorder.")
    print("    Gate 3.2b-R: this compared BTCUSDT alone until 2026-07-28, and")
    print("    sabotage B7 filled ETH and SOL with Bitcoin's figures unseen.")
    for symbol in GATE_SYMBOLS:
        try:
            live = requests.get(f"{FAPI_BASE}/fapi/v1/openInterest",
                                params={'symbol': symbol},
                                timeout=TIMEOUT).json()
            live_oi = float(live['openInterest'])
            stored_oi = float(_rows(csv_path(symbol, backfill_dir))[-1]
                              ['sumOpenInterest'])
            drift = abs(stored_oi - live_oi) / live_oi * 100
            near = drift < 10
            print(f"   {'✓' if near else '✗'} {symbol}: newest stored "
                  f"{stored_oi:,.3f} vs live snapshot {live_oi:,.3f} → "
                  f"{drift:.2f}% apart (the stored row is a point sample up to "
                  f"4h old, so a few percent is expected; 10% is the bar)")
            ok = ok and near
        except Exception as e:
            print(f"   ✗ {symbol}: plausibility check failed: "
                  f"{type(e).__name__}: {e}")
            ok = False

    # ---- (h)+(i) THE SABOTAGE DRILL, AND IT JUDGES THE FILE ON DISK -------
    print("\n(h) THE SABOTAGE DRILL, BUILT IN FROM BIRTH — this file is broken")
    print("    on purpose ELEVEN ways and each break MUST be caught. Gate")
    print("    3.2b-R2 added B8 and B9, which broke no logic whatsoever: one")
    print("    deleted an asset from the module's list and one changed an exit")
    print("    code, and both walked through a gate reporting seven of seven.")
    print("    Gate 3.2b-R3 added B10, which broke no logic the gate had ever")
    print("    executed: B4 with one `if` in front of it, firing only on the")
    print("    path every month after the first one takes. Gate 3.2b-R4 added")
    print("    B11, which broke no logic at all and wrote nothing wrong to")
    print("    disk — it changed only the line the Commander reads.")
    print("(i) AND THE DETECTOR READS THE CSV BACK OFF DISK and compares it,")
    print("    field by field, to a raw fetch the TEST makes itself — never to")
    print("    anything this file parsed. That is the lesson two Context Deck")
    print("    gates cost: check what is WRITTEN, not what the parser returned.")
    print("    Gate 3.2b-R: it now does that for ALL THREE assets. It read")
    print("    BTCUSDT alone until 2026-07-28, so B7 — which leaves BTC")
    print("    perfect — walked straight through a gate that printed PASSED.")

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

    def _symbol_matches_source(symbol, verbose=False):
        """Writes a fresh file for ONE symbol, reads it back off disk, and
        compares every row to raw. True if the file on disk is a faithful
        record of what Binance served for that symbol."""
        d = _fresh_dir()
        good, _ = run(symbols=(symbol,), history_dir=d)
        if not good:
            return False
        path = csv_path(symbol, d)
        if not os.path.exists(path):
            return False
        rows = _rows(path)
        truth = _raw_truth(symbol)
        if len(rows) < 175:
            return False
        for r in rows:
            want = truth.get(r['timestamp'])
            if want is None:
                if verbose:
                    print(f"      {symbol} row {r['timestamp']} is on disk but "
                          f"not in the source")
                return False
            if (r['sumOpenInterest'], r['sumOpenInterestValue']) != want:
                if verbose:
                    print(f"      {symbol} row {r['timestamp']}: disk "
                          f"{r['sumOpenInterest']} vs source {want[0]}")
                return False
            if r['symbol'] != symbol:
                return False
        # every source row inside the written window must be present
        stamps = {r['timestamp'] for r in rows}
        missing = [t for t in truth if t not in stamps]
        if missing:
            if verbose:
                print(f"      {symbol}: {len(missing)} source row(s) never "
                      f"reached disk, e.g. {sorted(missing)[:3]}")
            return False
        return True

    def _disk_matches_source(verbose=False):
        """THE DETECTOR — **FOR EVERY ASSET THIS RECORDER COLLECTS, not just
        the first one.**

        GATE 3.2b-R, 2026-07-28. This function used to be hardcoded to
        BTCUSDT, and it is the ONLY check anywhere in this gate that compares
        what was WRITTEN to what Binance SERVED. So did check (e), and so did
        check (g). **For ETHUSDT and SOLUSDT the entire gate only ever COUNTED:
        180 rows, 30 days, no duplicates.**

        An independent session exploited that with sabotage B7 — a memo cache
        keyed on the timestamp rather than on the (symbol, timestamp) pair, so
        the first asset fetched fills it and every later asset writes the FIRST
        asset's figures under its own name. BTCUSDT stayed perfect. ETH was
        recorded 22x wrong and SOL 80x wrong, for thirty days, and this gate
        printed "all six deliberate sabotages were caught" and exited 0.

        **On the one dataset Binance will not sell back at any price, two of
        three assets were guarded by a row count.**

        GATE 3.2b-R2, 2026-07-28 (evening): the loop runs over the GATE'S list,
        not the module's. It used to say `for symbol in SYMBOLS` — so deleting
        an asset from the module deleted it from its own detector too."""
        for symbol in GATE_SYMBOLS:
            if not _symbol_matches_source(symbol, verbose):
                if verbose:
                    print(f"      ^ {symbol} is where the disk stopped matching "
                          f"the source")
                return False
        return True

    def _covers_every_asset(verbose=False):
        """**THE JUDGE FOR B9.** Run the recorder the way the monthly task runs
        it — with NO symbol list of its own — and require a full window on disk
        for every asset THE GATE says this ship collects.

        `_disk_matches_source` cannot see B9: it passes each symbol explicitly,
        so it happily records SOLUSDT from a module that has stopped collecting
        it. The only way to catch an asset going missing is to let the module
        choose, and then check against a list it did not supply."""
        say = print if verbose else (lambda *a, **k: None)
        if tuple(SYMBOLS) != GATE_SYMBOLS:
            say(f"      the module's SYMBOLS {tuple(SYMBOLS)} is not the "
                f"gate's {GATE_SYMBOLS}")
            return False
        d = _fresh_dir()
        good, _ = run(history_dir=d)
        if not good:
            return False
        for s in GATE_SYMBOLS:
            path = csv_path(s, d)
            n = len(_rows(path)) if os.path.exists(path) else 0
            if n < 175:
                say(f"      {s}: {n} rows on disk — no full window")
                return False
        return True

    # =====================================================================
    # GATE 3.2b-R3, added 2026-07-28 (night) after an independent session threw
    # a TENTH sabotage at Gate 3.2b-R2 and it walked through.
    #
    # **EVERY ROW-LEVEL CHECK IN THIS GATE WRITES INTO AN EMPTY DIRECTORY.**
    # `_symbol_matches_source`, `_covers_every_asset`, `_record_run` and the
    # backfill all start from `_fresh_dir()`, so `exists` is False at write time
    # and any defect confined to the append-to-an-existing-file branch never
    # executes. And the only two checks that DO run against an existing file —
    # (b) idempotence and (e) tamper — append ZERO new rows, so `if new_rows:`
    # is False and the write block never runs at all.
    #
    # **THIS GATE HAD THEREFORE ONLY EVER TESTED MONTH ONE, AND MONTH ONE
    # HAPPENS ONCE.** From month two onward the monthly task takes the append
    # path every single time, and nothing had ever read a row back off it.
    #
    # B10 was sabotage B4 — the VALUE column written into the OI column — with
    # one `if` in front of it, so it fired only when the CSV already existed.
    # Eighty of a hundred and eighty rows landed 64,763x wrong, `record()`
    # reported no disagreement, and this gate printed PASSED with all NINE
    # sabotages CAUGHT — **including B4 itself, in that same run.**
    # =====================================================================
    SEED_ROWS = 100        # a STRICT subset, so there is genuinely something
                           # left for the recorder to append

    def _month_two(symbol, verbose=False):
        """THE APPEND PATH: seed a partial window, let the recorder append the
        rest, then read every row back off disk and compare it to a raw fetch
        the test makes itself.

        **The seed is written by THIS TEST from ITS OWN raw fetch and never
        passes through the module's writer**, so a broken writer cannot make the
        seed agree with itself.

        **It must PROVE it appended something.** A seed that already covers the
        window appends nothing and the check passes having tested nothing — that
        is the B5 failure, where a tick mark appeared for a check that never
        reached what it claimed to prove."""
        say = print if verbose else (lambda *a, **k: None)
        d = _fresh_dir()
        before = _raw_truth(symbol)
        ordered = sorted(before)
        if len(ordered) <= SEED_ROWS:
            say(f"      {symbol}: the source returned only {len(ordered)} rows "
                f"— too few to seed a PARTIAL window, so this proves nothing")
            return False

        path = csv_path(symbol, d)
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            for stamp in ordered[:SEED_ROWS]:
                oi, val = before[stamp]
                w.writerow({'timestamp': stamp, 'symbol': symbol,
                            'sumOpenInterest': oi,
                            'sumOpenInterestValue': val})

        good, _ = run(symbols=(symbol,), history_dir=d)
        if not good:
            say(f"      {symbol}: the month-two run reported a failure")
            return False

        rows = _rows(path)
        appended = len(rows) - SEED_ROWS
        if appended <= 0:
            say(f"      {symbol}: NOTHING WAS APPENDED — this check tested the "
                f"append path not at all and must not pass")
            return False

        # THE 4h BOUNDARY (R-013 doubt 3, never handled until now): a period can
        # close between the test's fetch and the module's, so a row is correct
        # if it matches EITHER snapshot. This does not soften the bar — a
        # transposed, rounded or cross-symbol figure matches NEITHER.
        after = _raw_truth(symbol)
        stamps = {r['timestamp'] for r in rows}
        for r in rows:
            pair = (r['sumOpenInterest'], r['sumOpenInterestValue'])
            if pair not in (before.get(r['timestamp']),
                            after.get(r['timestamp'])):
                want = before.get(r['timestamp'])
                say(f"      {symbol} row {r['timestamp']}: disk "
                    f"{r['sumOpenInterest']} vs source "
                    f"{want[0] if want else 'NOT IN SOURCE AT ALL'}")
                return False
            if r['symbol'] != symbol:
                say(f"      {symbol} row {r['timestamp']} is stamped "
                    f"{r['symbol']!r}")
                return False
        keys = {(r['symbol'], r['timestamp']) for r in rows}
        if len(keys) != len(rows):
            say(f"      {symbol}: {len(rows) - len(keys)} duplicate row(s) "
                f"after the append")
            return False
        missing = [t for t in before if t not in stamps]
        if missing:
            say(f"      {symbol}: {len(missing)} source row(s) never reached "
                f"disk, e.g. {sorted(missing)[:3]}")
            return False
        say(f"   ✓ {symbol}: seeded {SEED_ROWS}, APPENDED {appended}, "
            f"{len(rows)} on disk — every row matches what Binance served and "
            f"there are no duplicates")
        return True

    def _append_matches_source(verbose=False):
        """**THE JUDGE FOR B10** — for every asset THE GATE names, never the
        module's list. That is B9's lesson, one day old, and a repair that drops
        it while quoting it has learned nothing."""
        for symbol in GATE_SYMBOLS:
            if not _month_two(symbol, verbose):
                if verbose:
                    print(f"      ^ {symbol} is where the APPEND path stopped "
                          f"matching the source")
                return False
        return True

    # =====================================================================
    # GATE 3.2b-R4, added 2026-07-29 after an independent session threw an
    # ELEVENTH sabotage at Gate 3.2b-R3 and it walked through.
    #
    # **EVERY DETECTOR IN THIS GATE READS THE CSV BACK OFF DISK.** That was
    # the right lesson and it was learned properly. **But not one check
    # anywhere asserted that the recorder's own REPORT is true.**
    # `_trap_check` looks for the words 'EMPTY LIST' and check (e) looks for
    # 'DISAGREE' — and that is the entire extent to which any printed line
    # was ever inspected.
    #
    # **THE REPORT IS THE ONLY OUTPUT OF THIS PART A HUMAN EVER SEES.** It is
    # written to `journal/daily_runs.log` by `run_daily.bat`, and the standing
    # order on the Commander's desk is to read that log and decide FROM IT
    # whether the recorder worked. A gate that guards the disk perfectly and
    # never looks at the report has guarded everything except the one thing
    # he actually reads.
    #
    # B11 wrote `'appended': len(new_rows)` as `'appended': len(fresh)` — two
    # adjacent keys in one dict literal, both already in scope. The disk
    # stayed byte-perfect, so every check here was happy: TEN OF TEN
    # SABOTAGES CAUGHT, PASSED, exit 0. Run twice against a scratch copy, the
    # healthy recorder reports '0 new row(s) appended' and the broken one
    # reports '180', with nothing on disk having changed either time.
    # =====================================================================

    # The gate's OWN copy of the report's shape, typed out here and never read
    # from the module — the same rule `GATE_SYMBOLS` exists for. Anchored to
    # the start of the line and to the symbol, so a `!!  … DISAGREE` line and a
    # `🔌 … NOT RECORDED` line cannot be mistaken for a report line.
    # GATE 3.2b-R5, 2026-07-29 (afternoon): THE WINDOW IS NO LONGER WHERE THIS
    # PATTERN GIVES UP. B12 printed a window derived from the CLOCK and walked
    # straight through, because this match ended at the word `window ` and
    # nothing anywhere compared those two timestamps to anything at all. The
    # gate's author filed it as his own doubt and could not close it. Both
    # timestamps are captured now, and both are measured against a fetch the
    # gate makes itself.
    GATE_REPORT_RE = re.compile(
        r"^  (?P<symbol>[A-Z]+): (?P<appended>\d+) new row\(s\) appended, "
        r"(?P<total>\d+) stored, window (?P<start>\S+) → (?P<end>\S+)$")

    # The gate's OWN copy of the sampling period, never read from the module it
    # is judging. That is R-014's lesson and a repair that drops it while
    # quoting it has learned nothing.
    GATE_PERIOD_HOURS = 4

    def _window_bounds(symbol):
        """The oldest and newest timestamps Binance is serving RIGHT NOW, taken
        from a fetch THE GATE makes, passing through none of this module's
        helpers and none of its arithmetic."""
        truth = _raw_truth(symbol)
        return min(truth), max(truth)

    def _report_is_true(verbose=False):
        """**THE JUDGE FOR B11.** The printed report must match the disk — and
        the disk is counted BY THE GATE, before and after the run, never taken
        from the module.

        Run TWICE. Month one, where the honest answer is a full window, and
        month two, where the honest answer is zero. **The second run is the one
        that lies loudest**, and it is the path the monthly task takes from now
        on: B11's claim and the truth are identical on the first run and differ
        by 180 on the second.

        THE 4h BOUNDARY, handled by construction rather than patched later: a
        period can close between the two runs, so the second run may
        legitimately append a row. **The bar is therefore NOT "the second run
        must report zero"** — it is "the reported count equals what actually
        landed on disk, whatever that is". That is the correct invariant
        anyway, and it cannot be broken by the calendar.
        """
        say = print if verbose else (lambda *a, **k: None)
        d = _fresh_dir()

        def _count(symbol):
            p = csv_path(symbol, d)
            return len(_rows(p)) if os.path.exists(p) else 0

        for run_no in (1, 2):
            before = {s: _count(s) for s in GATE_SYMBOLS}
            # Bracketed either side of the run: a 4h period can close while the
            # module is fetching, so BOTH snapshots are legitimate answers and
            # the bar accepts either. A fabricated, stale or clock-derived
            # window matches NEITHER, which is the whole point.
            win_before = {s: _window_bounds(s) for s in GATE_SYMBOLS}
            good, lines = run(history_dir=d)
            win_after = {s: _window_bounds(s) for s in GATE_SYMBOLS}
            after = {s: _count(s) for s in GATE_SYMBOLS}
            if not good:
                say(f"      run {run_no} reported a failure")
                return False

            seen = {}
            for ln in lines:
                m = GATE_REPORT_RE.match(ln)
                if m:
                    seen[m.group('symbol')] = (int(m.group('appended')),
                                               int(m.group('total')),
                                               m.group('start'),
                                               m.group('end'))
            # **A line that does not parse is a FAILURE, never a skip.** A
            # check that quietly finds nothing to check and passes is the B5
            # lesson, and the assets are named by THE GATE — B9's lesson.
            if set(seen) != set(GATE_SYMBOLS):
                say(f"      run {run_no}: the report named {sorted(seen)}, "
                    f"the gate expects {sorted(GATE_SYMBOLS)}")
                return False

            for s in GATE_SYMBOLS:
                (claimed_appended, claimed_total,
                 claimed_start, claimed_end) = seen[s]
                really_appended = after[s] - before[s]
                # **THE WINDOW, GATE 3.2b-R5.** The two timestamps the report
                # prints must be the two ends of what the source actually
                # served. Nothing here is taken from the module.
                ok_start = {win_before[s][0], win_after[s][0]}
                ok_end = {win_before[s][1], win_after[s][1]}
                if claimed_start not in ok_start:
                    say(f"      run {run_no} {s}: the report claims the window "
                        f"STARTS at {claimed_start} — the gate's own fetch says "
                        f"{sorted(ok_start)}")
                    return False
                if claimed_end not in ok_end:
                    say(f"      run {run_no} {s}: the report claims the window "
                        f"ENDS at {claimed_end} — the gate's own fetch says "
                        f"{sorted(ok_end)}")
                    return False
                if claimed_appended != really_appended:
                    say(f"      run {run_no} {s}: the report claims "
                        f"{claimed_appended} row(s) appended — the gate "
                        f"counted {really_appended} arriving on disk")
                    return False
                if claimed_total != after[s]:
                    say(f"      run {run_no} {s}: the report claims "
                        f"{claimed_total} stored — the gate counted "
                        f"{after[s]} on disk")
                    return False

            say(f"   ✓ run {run_no}: every asset's printed report matches the "
                f"rows the gate counted itself — appended "
                f"{ {s: after[s] - before[s] for s in GATE_SYMBOLS} }, stored "
                f"{ {s: after[s] for s in GATE_SYMBOLS} }, AND both ends of "
                f"every printed window match the gate's own fetch")
        return True

    # ---- THE SHAPE THIS GATE COULD NEVER BUILD -----------------------------
    ARCHIVE_SEED_ROWS = 12      # ~2 days at 4h — the slice of the real archive
                                # that already sits outside Binance's window

    def _archive_survives(symbol, verbose=False):
        """**THE JUDGE FOR B13, and GATE 3.2b-R5's reason for existing.**

        Every other check in this file hands the recorder an EMPTY directory,
        or a directory seeded from the gate's OWN raw fetch. In both, the rows
        already on disk are a SUBSET of the rows Binance is currently serving.

        **In real life that is false, and it is false from the very next run.**
        The archive begins 2026-06-27 and the source serves a rolling thirty
        days, so its oldest rows exist in our file **and nowhere else on
        earth**. `stored ⊄ fresh` is the ONLY shape in which the archive can be
        DESTROYED, and it was the one shape this gate could not construct —
        which is why B13 deleted thirty-four irreplaceable rows while eleven
        checks stayed green and the printed report stayed TRUE.

        So the gate builds it: rows the source no longer serves are seeded onto
        disk, the recorder runs, and **every one of them must still be there,
        byte for byte, afterwards.**"""
        say = print if verbose else (lambda *a, **k: None)
        d = _fresh_dir()
        truth = _raw_truth(symbol)
        oldest = min(truth)
        # Stepped back in the gate's own 4h strides from the oldest row the
        # source still serves. `timedelta` is deliberately not imported into
        # this module, so the arithmetic is done in seconds.
        base = datetime.strptime(oldest, '%Y-%m-%dT%H:%M:%SZ').replace(
            tzinfo=timezone.utc).timestamp()
        seeded = []
        for i in range(ARCHIVE_SEED_ROWS, 0, -1):
            stamp = datetime.fromtimestamp(
                base - i * GATE_PERIOD_HOURS * 3600,
                timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            seeded.append({'timestamp': stamp, 'symbol': symbol,
                           'sumOpenInterest': f"{1000 + i}.00000000",
                           'sumOpenInterestValue': f"{2000 + i}.00000000"})

        # **PROVE THE SEED IS REALLY OUTSIDE THE WINDOW.** Without this the
        # check quietly becomes a no-op the day the window moves — a tick mark
        # for something never tested, which is the B5 failure this ship has
        # already paid for once.
        inside = [r['timestamp'] for r in seeded if r['timestamp'] in truth]
        if inside:
            say(f"      {symbol}: {len(inside)} seeded row(s) ARE in the "
                f"source window — this check would be proving nothing")
            return False

        path = csv_path(symbol, d)
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            for row in seeded:
                w.writerow(row)

        good, _ = run(symbols=(symbol,), history_dir=d)
        if not good:
            say(f"      {symbol}: the archive run reported a failure")
            return False

        on_disk = {r['timestamp']: r for r in _rows(path)}
        for row in seeded:
            got = on_disk.get(row['timestamp'])
            if got is None:
                say(f"      {symbol}: ARCHIVE ROW {row['timestamp']} WAS "
                    f"DESTROYED — the source no longer serves it and it is no "
                    f"longer on disk, so it is gone for good")
                return False
            if ((got['sumOpenInterest'], got['sumOpenInterestValue'],
                 got['symbol'])
                    != (row['sumOpenInterest'], row['sumOpenInterestValue'],
                        row['symbol'])):
                say(f"      {symbol}: ARCHIVE ROW {row['timestamp']} WAS "
                    f"REWRITTEN — {got['sumOpenInterest']} where "
                    f"{row['sumOpenInterest']} was recorded")
                return False
        # And the run must genuinely have done its job, or a recorder that
        # writes nothing at all would pass this check by touching nothing.
        landed = [t for t in truth if t in on_disk]
        if len(landed) < 175:
            say(f"      {symbol}: only {len(landed)} source row(s) reached "
                f"disk — the archive survived a run that did not happen")
            return False
        say(f"   ✓ {symbol}: {len(seeded)} archive row(s) the source NO LONGER "
            f"SERVES survived byte for byte, and {len(landed)} fresh rows "
            f"still landed — {len(on_disk)} rows on disk")
        return True

    def _archive_survives_all(verbose=False):
        """For every asset THE GATE names, from its own list — B9's lesson."""
        for symbol in GATE_SYMBOLS:
            if not _archive_survives(symbol, verbose):
                if verbose:
                    print(f"      {symbol} failed the archive-preservation "
                          f"check")
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

    _B7_MEMO = {}

    def _sab_cross_symbol(symbol, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
                          period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
        """**B7, from the independent review of 2026-07-28. IT WALKED THROUGH
        THIS GATE.**

        A memo cache keyed on the TIMESTAMP and not on the (SYMBOL, TIMESTAMP)
        pair. The first asset fetched fills it; every later asset reads its own
        timestamps back out and writes the first asset's figures under its own
        name. **That is not a strawman — it is what "let us not re-derive rows
        we have already seen" looks like when written carelessly.**

        The first symbol stays PERFECT, which is the whole point: a detector
        that only ever looked at BTCUSDT could not see this, and for thirty days
        ETH would have carried Bitcoin's open interest 22x wrong and SOL 80x
        wrong on a dataset that cannot be bought back at any price."""
        rep = _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                               timeout)
        path = csv_path(symbol, history_dir)
        rows = _rows(path)
        if symbol == SYMBOLS[0]:
            _B7_MEMO.clear()
            for r in rows:
                _B7_MEMO[r['timestamp']] = (r['sumOpenInterest'],
                                            r['sumOpenInterestValue'])
            return rep
        for r in rows:
            hit = _B7_MEMO.get(r['timestamp'])
            if hit:
                r['sumOpenInterest'], r['sumOpenInterestValue'] = hit
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(rows)
        return rep

    def _sab_append_transposes(symbol, base_url=FAPI_BASE,
                               history_dir=HISTORY_DIR, period=PERIOD,
                               limit=LIMIT, timeout=TIMEOUT):
        """**B10, from the independent review of 2026-07-28 (night). IT WALKED
        THROUGH THIS GATE.**

        Sabotage B4 — the VALUE column written into the OI column — with one
        `if` in front of it, so it fires ONLY on rows appended to a file that
        already existed. **B4 is in this drill and was scored CAUGHT in the very
        run B10 passed**, because every row-level check here started from an
        empty directory and the append branch never executed.

        It corrupts only the NEWLY APPENDED rows, which is both the faithful
        shape of the defect and the harder one to catch."""
        path = csv_path(symbol, history_dir)
        existed = os.path.exists(path)
        already = {r['timestamp'] for r in _rows(path)} if existed else set()
        rep = _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                               timeout)
        if not existed:
            return rep
        rows = _rows(path)
        for r in rows:
            if r['timestamp'] not in already:
                r['sumOpenInterest'] = r['sumOpenInterestValue']
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(rows)
        return rep

    def _sab_report_lies(symbol, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
                         period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
        """**B11, from the independent review of 2026-07-29. IT WALKED THROUGH
        THIS GATE.**

        `'appended': len(new_rows)` written as `'appended': len(fresh)` — two
        adjacent keys in one dict literal, in a function whose keys are
        `fetched`, `stored_before`, `appended`, `total`, with both values
        already in scope. **This is the most ordinary slip available in this
        file**, not a strawman.

        **It writes nothing wrong to disk.** That is the whole point: every
        row-level detector in this gate reads the CSV back and finds it
        perfect, because it IS perfect. Only the printed line lies — and the
        printed line is the only part of this recorder a human ever reads, and
        the only evidence the Commander has been told to judge it by.

        The lie is invisible on the first run, where the count it fakes and
        the truth happen to be equal. It shows on the second, which is every
        month from now on."""
        rep = _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                               timeout)
        rep['appended'] = rep['fetched']
        return rep

    def _sab_window_lies(symbol, base_url=FAPI_BASE, history_dir=HISTORY_DIR,
                         period=PERIOD, limit=LIMIT, timeout=TIMEOUT):
        """**B12, from the independent review of 2026-07-29 (afternoon). IT
        WALKED THROUGH THIS GATE.**

        The report prints `window X → Y`, and `GATE_REPORT_RE` stopped matching
        at the word `window `. **Nothing anywhere compared those two timestamps
        to anything at all** — the gate's own author filed that as his doubt 2
        and could not close it.

        The slip is a window derived from THE CLOCK rather than from the data
        actually fetched: what *"show the window we asked for"* looks like
        written carelessly, one line below the dict key B11 already broke.
        **The counts stay perfectly honest, so check (l) had nothing to say.**

        Why it matters: it prints a flawless thirty-day window every month
        whatever the source really served. If Binance ever returns a short or
        stale set, the one line a human reads still says the window was
        captured whole."""
        rep = _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                               timeout)
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        rep['span'] = (_UTC_ISO_ORIGINAL(now_ms - 30 * 86400 * 1000),
                       _UTC_ISO_ORIGINAL(now_ms))
        return rep

    def _sab_archive_synced(symbol, base_url=FAPI_BASE,
                            history_dir=HISTORY_DIR, period=PERIOD,
                            limit=LIMIT, timeout=TIMEOUT):
        """**B13, from the independent review of 2026-07-29 (afternoon). IT
        WALKED THROUGH THIS GATE, AND IT DESTROYS THE ARCHIVE.**

        A *"keep the file in step with the window the source serves"* tidy-up —
        a rolling-window change, the most ordinary well-intentioned edit
        available on a file like this. It drops stored rows that are no longer
        in `fresh`, and it reports `total` from the rows actually on disk, so
        **its report is TRUE.** Nothing about it looks like a lie.

        **In every scenario this gate could build, the stored rows were a
        SUBSET of what Binance still serves, so this branch never fired and
        eleven checks stayed green.** Run against a copy of the REAL archive it
        deleted thirty-four rows — 11 BTC, 12 ETH, 11 SOL — that Binance will
        not sell back at any price, and printed
        `11 new row(s) appended, 180 stored` where the honest run prints 191.

        It is caught now only because the gate finally builds the shape the
        real world has: rows on disk that the source no longer serves."""
        rep = _RECORD_ORIGINAL(symbol, base_url, history_dir, period, limit,
                               timeout)
        oldest = rep['span'][0]          # the oldest row the source served
        path = csv_path(symbol, history_dir)
        if os.path.exists(path):
            kept = [r for r in read_stored(symbol, history_dir)
                    if r['timestamp'] >= oldest]
            with open(path, 'w', newline='', encoding='utf-8') as fh:
                w = csv.DictWriter(fh, fieldnames=COLUMNS)
                w.writeheader()
                for row in kept:
                    w.writerow(row)
            rep['total'] = len(kept)     # honest about the final state
        return rep

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
        # B7 is the reason `_disk_matches_source` now covers every symbol. It
        # leaves BTCUSDT perfect on purpose, so it is caught ONLY by a detector
        # that looks past the first asset.
        ('B7', 'ETH and SOL written with BTC\'s figures', 'record',
         _sab_cross_symbol, 'disk'),
        # B9, from the independent review of 2026-07-28 (evening). It walked
        # through Gate 3.2b-R. **It breaks no logic at all** — it deletes one
        # asset from the module's list, and every loop in the gate said
        # `for symbol in SYMBOLS`, so the gate deleted it too and reported
        # success. Thirty days of SOL, gone for good, all green.
        ('B9', 'one asset silently dropped from SYMBOLS', 'SYMBOLS',
         ('BTCUSDT', 'ETHUSDT'), 'covers'),
        # B10, from the independent review of 2026-07-28 (night). It walked
        # through Gate 3.2b-R2. **It is B4 restricted to the append path** —
        # the only path the monthly task takes from month two onward, and the
        # one path no row-level check in this gate had ever built.
        ('B10', 'the OI column transposed, but only on append', 'record',
         _sab_append_transposes, 'append'),
        # B11, from the independent review of 2026-07-29. It walked through
        # Gate 3.2b-R3. **It corrupts nothing this gate had ever inspected** —
        # the disk stays byte-perfect and only the REPORT lies, which is the
        # one output of this part a human reads and the one no check here had
        # ever looked at.
        ('B11', 'the report claims rows it never appended', 'record',
         _sab_report_lies, 'report'),
        # B12 and B13, from the independent review of 2026-07-29 (afternoon).
        # Both walked through Gate 3.2b-R4 with all ELEVEN scored CAUGHT.
        # B12 lies in the half of the report line the parser had stopped
        # reading at. B13 lies nowhere at all — its report is TRUE — and
        # destroys the archive in the one shape this gate could not build.
        ('B12', 'the report window comes from the clock', 'record',
         _sab_window_lies, 'report'),
        ('B13', 'the archive pruned to the source window', 'record',
         _sab_archive_synced, 'archive'),
    ]

    # ---- (k) MONTH TWO: THE APPEND PATH -----------------------------------
    # Placed here, after the helpers exist, rather than beside the other numbered
    # sections: the first draft called it fifteen lines before it was defined and
    # the gate died with a NameError. Recorded in PROGRESS_LOG.md rather than
    # quietly fixed.
    print("\n(k) MONTH TWO — THE APPEND PATH (Gate 3.2b-R3). Every other")
    print("    row-level check in this gate writes into an EMPTY directory, so")
    print("    `exists` is False and the append branch never runs; and the two")
    print("    checks that do meet an existing file append ZERO rows, so the")
    print("    write block never runs at all. This gate had only ever tested")
    print("    MONTH ONE — and month one happens once. Sabotage B10 transposed")
    print("    the OI column on append alone: 80 of 180 rows landed 64,763x")
    print("    wrong and all NINE sabotages were scored CAUGHT. A partial window")
    print("    is now seeded BY THIS TEST from its own raw fetch, the recorder")
    print("    appends the rest, and every row is read back and compared.")
    append_ok = _append_matches_source(verbose=True)
    print(f"   {'✓' if append_ok else '✗'} the append path is a faithful record "
          f"for every asset the gate names, and it proved it APPENDED rather "
          f"than passing on an already-complete window")
    ok = ok and append_ok

    # ---- (l) THE REPORT IS TRUE -------------------------------------------
    print("\n(l) THE REPORT MUST MATCH THE DISK (Gate 3.2b-R4). Every other")
    print("    check in this gate reads the CSV back off disk — and NOTHING")
    print("    anywhere asserted that the line this recorder PRINTS is true.")
    print("    That line is the only output of this part a human ever sees:")
    print("    `run_daily.bat` writes it into journal/daily_runs.log, and the")
    print("    Commander's standing order is to read that log and decide from")
    print("    it whether the recorder worked. Sabotage B11 wrote `len(fresh)`")
    print("    where `len(new_rows)` belongs — one word, two adjacent keys in")
    print("    the same dict — and the disk stayed byte-perfect, so all TEN")
    print("    sabotages were scored CAUGHT and the gate exited 0 while the")
    print("    report claimed 180 appended rows on a run that appended none.")
    print("    The gate now counts the rows ITSELF, before and after, and runs")
    print("    the recorder TWICE: the lie is invisible on the first run and")
    print("    plain on the second, which is what every month looks like now.")
    report_ok = _report_is_true(verbose=True)
    print(f"   {'✓' if report_ok else '✗'} the printed report is true for every "
          f"asset the gate names, on the first run AND on the second — "
          f"measured against rows the gate counted, never against the "
          f"module's own arithmetic")
    ok = ok and report_ok

    # ---- (m) THE ARCHIVE SURVIVES -----------------------------------------
    print("\n(m) THE SHAPE THIS GATE COULD NEVER BUILD (Gate 3.2b-R5). Every")
    print("    other check here hands the recorder an EMPTY directory, or one")
    print("    seeded from the gate's OWN raw fetch — so the rows already on")
    print("    disk are always a SUBSET of what Binance is serving now. IN")
    print("    REAL LIFE THAT IS FALSE FROM THE VERY NEXT RUN: the archive")
    print("    begins 2026-06-27, the source serves a rolling thirty days, and")
    print("    its oldest rows exist in our file AND NOWHERE ELSE ON EARTH.")
    print("    Sabotage B13 — an ordinary 'keep the file in step with the")
    print("    source' tidy-up, whose printed report is TRUE — deleted 34 such")
    print("    rows from a copy of the real archive while ELEVEN sabotages")
    print("    were scored CAUGHT and this gate exited 0. Rows the source no")
    print("    longer serves are now seeded on purpose, and every one of them")
    print("    must still be on disk, byte for byte, when the run is over.")
    archive_ok = _archive_survives_all(verbose=True)
    print(f"   {'✓' if archive_ok else '✗'} the archive survives the run for "
          f"every asset the gate names — rows the source has already dropped "
          f"were proved outside the window first, so this check cannot quietly "
          f"become a no-op")
    ok = ok and archive_ok

    drill_ok = True
    for tag, words, attr, repl, judge in _SABOTAGES:
        original = globals()[attr]
        globals()[attr] = repl
        try:
            survived = {'trap': _trap_check,
                        'covers': _covers_every_asset,
                        'append': _append_matches_source,
                        'report': _report_is_true,
                        'archive': _archive_survives_all}.get(
                judge, _disk_matches_source)(verbose=False)
        except Exception:
            survived = False        # a crash is a catch: it did not pass
        finally:
            globals()[attr] = original
        caught = not survived
        print(f"   {'✓' if caught else '✗'} {tag}  {words:<44} → "
              f"{'CAUGHT' if caught else 'ESCAPED — THE GATE IS DECORATIVE'}")
        drill_ok = drill_ok and caught

    # B8 cannot be expressed as a swapped global. It lives in the `--record`
    # branch, which only ever executes in a subprocess — and that is precisely
    # why nothing caught it. So it is applied as a REAL TEXT EDIT to a copy,
    # which is the stronger form of the drill anyway and the form this ship has
    # always used for its evidence. The copy is written to scratch, so the real
    # history is untouchable here.
    with open(THIS_FILE, encoding='utf-8') as _fh:
        _pristine = _fh.read()
    _FILE_SABOTAGES = [
        # Both anchors are whole lines, newlines included, for the reason
        # `_record_run` explains: the anchor text is written in this file, so
        # an un-anchored substring matches itself and the edit is ambiguous.
        ('B8', 'the monthly task always exits 0',
         [("\nFAPI_BASE = 'https://fapi.binance.com'\n",
           f"\nFAPI_BASE = '{OFFLINE_DRILL_URL}'\n"),
          ('\n        sys.exit(0 if recorded else 1)\n',
           '\n        sys.exit(0)\n')],
         _record_alarm_fires),
    ]
    for tag, words, edits, judge in _FILE_SABOTAGES:
        try:
            broken = _pristine
            for anchor, repl in edits:
                if broken.count(anchor) != 1:
                    raise RecorderError(f"{tag}: anchor {anchor!r} matched "
                                        f"{broken.count(anchor)} times — "
                                        f"refusing to guess which")
                broken = broken.replace(anchor, repl)
            survived = judge(verbose=False, source_override=broken)
        except Exception:
            survived = False        # a crash is a catch: it did not pass
        caught = not survived
        print(f"   {'✓' if caught else '✗'} {tag}  {words:<44} → "
              f"{'CAUGHT' if caught else 'ESCAPED — THE GATE IS DECORATIVE'}")
        drill_ok = drill_ok and caught

    restored = (_disk_matches_source(verbose=True) and _trap_check(verbose=False)
                and _covers_every_asset(verbose=True)
                and _record_alarm_fires(verbose=False)
                and _append_matches_source(verbose=True)
                and _report_is_true(verbose=True)
                and _archive_survives_all(verbose=True))
    print(f"   {'✓' if restored else '✗'} every original restored — a freshly "
          f"written CSV matches the source row for row, the APPEND path does "
          f"too, every asset the gate names still reaches disk, the "
          f"empty-result trap still fails loudly, the monthly task's alarm "
          f"still fires, the printed report still matches the disk INCLUDING "
          f"both ends of its window, and rows the source no longer serves "
          f"still survive the run")
    ok = ok and drill_ok and restored

    # ---- (f) THE BRIEF IS UNAFFECTED --------------------------------------
    print("\n(f) THE BRIEF IS UNAFFECTED — this step touches no cockpit file,")
    print("    so this should be trivially true. Verified anyway.")
    print("    (run `python cockpit\\brief.py` — checked in the shell and")
    print("    recorded in PROGRESS_LOG.md; not imported here, because a")
    print("    recorder that imports the cockpit is no longer a sealed part.)")

    shutil.rmtree(SCRATCH, ignore_errors=True)

    if ok:
        print("\nGATE 3.2b-R5 PASSED — the backfill is real, the same run twice")
        print("changes nothing, an empty result fails loudly, the offline drill")
        print("leaves the files byte-identical, tampered history is reported")
        print("rather than overwritten, the `--record` branch the monthly task")
        print("runs was driven for real and its alarm fires on failure, MONTH")
        print("TWO — appending to a file that already holds rows, which is what")
        print("every month after the first one does — was built and read back")
        print("row by row, THE PRINTED REPORT WAS MEASURED AGAINST ROWS THE")
        print("GATE COUNTED ITSELF on two consecutive runs — because that line")
        print("is the only output of this part a human ever reads — BOTH ENDS")
        print("OF THE PRINTED WINDOW were measured against the gate's own")
        print("fetch, ROWS THE SOURCE NO LONGER SERVES were seeded on disk and")
        print("required to survive the run — the shape the real world has and")
        print("this gate could not build until today — and all THIRTEEN")
        print("deliberate sabotages were caught, FOR EVERY ASSET THIS GATE")
        print("NAMES, from its own list, not the module's. This test has")
        print("demonstrated, this run, that it can say no.")
    else:
        print("\nGATE 3.2b-R5 FAILED — see the ✗ lines above. Nothing is")
        print("committed as a pass.")
    sys.exit(0 if ok else 1)
