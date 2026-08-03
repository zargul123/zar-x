"""ZAR X — THE COLLECTION GUARD.

**WHY THIS FILE EXISTS.** On 2026-08-03 the monthly open-interest recorder fired,
told Windows it had succeeded, and collected nothing. Five sibling jobs did the
same thing in the same second. Nothing anywhere noticed, and `CHECK_STATUS.bat`
— the one screen the Commander runs to see whether the ship is healthy — reads
Windows' `LastTaskResult` and would have printed **OK**.

**SO THE STATUS SCREEN WOULD HAVE CONFIRMED THE FAILURE AS A SUCCESS.**

**THIS FILE DOES NOT ASK THE JOB. IT ASKS THE DATA.** It reads the archive off
disk and reports how old the newest row is. That is the only check that survives
a cause nobody has proved — and the cause of Windows' `0` is still unproven,
because the Task Scheduler event log was switched off and the record is gone.

**IT NEVER WRITES TO `data/oi_history/`.** It opens those files for reading and
nothing else. The rows in them cannot be re-bought at any price.

Law 2: this compartment owns its own constants. It deliberately does NOT import
`open_interest.py` and does NOT ask that module where the archive lives —
sabotage B14 moved the archive to another filename with every row inside it
perfect, and twenty-three checks that asked the module for the address followed
it there and certified the move.
"""
from __future__ import annotations

import csv
import os
from datetime import datetime, timedelta, timezone

# This compartment's own copies. Never read from another module. R-014, B14.
HISTORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'oi_history')
SYMBOLS = ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')
CSV_SUFFIX = '_4h.csv'
TS_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# Binance serves a rolling thirty days and refuses anything older. A row that
# ages past this is not late — it is DELETED, everywhere, forever.
SOURCE_WINDOW_DAYS = 30.0

# The recorder runs weekly, so between healthy runs the newest row reaches about
# seven days old. TEN is quiet in normal operation and loud well before the
# thirty-day cliff, which leaves twenty days of warning.
WARN_DAYS = 10.0

HEADER = '--- Open-interest archive (the rows that CANNOT be re-bought) ---'
OK_WORDS = 'ARCHIVE OK - the recorder is keeping up.'
STALE_WORDS = ('STALE - no new rows for %.1f days. Nothing is lost yet. '
               'Run run_oi_recorder.bat.')
LOST_WORDS = ('ROWS ARE BEING LOST RIGHT NOW - the newest row is %.1f days '
              'old and Binance keeps only %.0f. Every hour deletes more, '
              'permanently. Run run_oi_recorder.bat NOW.')
MISSING_WORDS = 'NO ARCHIVE FILE - the recorder has never written this asset.'

OK, STALE, LOST = 0, 1, 2


class GuardError(Exception):
    """Raised when the guard cannot do its job. It never returns a reassuring
    answer it could not verify — that is the recorder's empty-result trap."""


def csv_path(symbol, history_dir=None):
    """`history_dir=None` resolved in the BODY, never frozen as a default.
    `def f(d=HISTORY_DIR)` captures the value when the `def` runs, which is how
    sabotage B9 changed a name nothing read and was scored CAUGHT for four
    generations. Desk item 8 — the pattern, not just the instance."""
    directory = HISTORY_DIR if history_dir is None else history_dir
    return os.path.join(directory, symbol + CSV_SUFFIX)


def newest_timestamp(symbol, history_dir=None):
    """The newest row's timestamp, as an aware UTC datetime, or None if the
    file is absent. Returns None ONLY for an absent file: a file that exists
    but holds no usable row raises, because 'present but empty' silently
    reported as 'fine' is exactly the trap the recorder's gate exists for."""
    path = csv_path(symbol, history_dir)
    if not os.path.exists(path):
        return None
    newest = None
    with open(path, newline='', encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            raw = (row.get('timestamp') or '').strip()
            if not raw:
                continue
            try:
                stamp = datetime.strptime(raw, TS_FORMAT).replace(
                    tzinfo=timezone.utc)
            except ValueError:
                raise GuardError(
                    "%s: unreadable timestamp %r in %s" % (symbol, raw, path))
            if newest is None or stamp > newest:
                newest = stamp
    if newest is None:
        raise GuardError(
            "%s: %s exists but holds no readable row. This is NOT 'no new "
            "data'." % (symbol, path))
    return newest


def archive_state(now=None, history_dir=None, symbols=None):
    """One dict per asset: its newest row, its age in days, and its verdict."""
    moment = datetime.now(timezone.utc) if now is None else now
    names = SYMBOLS if symbols is None else symbols
    state = []
    for symbol in names:
        newest = newest_timestamp(symbol, history_dir)
        if newest is None:
            state.append({'symbol': symbol, 'newest': None,
                          'age_days': None, 'verdict': LOST})
            continue
        age = (moment - newest).total_seconds() / 86400.0
        verdict = (LOST if age >= SOURCE_WINDOW_DAYS
                   else STALE if age >= WARN_DAYS
                   else OK)
        state.append({'symbol': symbol, 'newest': newest,
                      'age_days': age, 'verdict': verdict})
    return state


def status_lines(now=None, history_dir=None, symbols=None):
    """The block the Commander reads, and the worst verdict in it."""
    state = archive_state(now, history_dir, symbols)
    lines = [HEADER]
    worst = OK
    for row in state:
        worst = max(worst, row['verdict'])
        if row['newest'] is None:
            lines.append('  !! %-8s %s' % (row['symbol'], MISSING_WORDS))
            continue
        stamp = row['newest'].strftime(TS_FORMAT)
        mark = '  ' if row['verdict'] == OK else '  !! '
        lines.append('%s%-8s newest row %s  %.1f days old' % (
            mark, row['symbol'], stamp, row['age_days']))
    oldest = max((r['age_days'] for r in state
                  if r['age_days'] is not None), default=None)
    if worst == OK:
        lines.append('  ' + OK_WORDS)
    elif worst == STALE:
        lines.append('  !! ' + STALE_WORDS % oldest)
    else:
        lines.append('  !! ' + (LOST_WORDS % (oldest, SOURCE_WINDOW_DAYS)
                                if oldest is not None else MISSING_WORDS))
    return lines, worst


def report(now=None, history_dir=None, symbols=None):
    """Print the block. Exit code carries the verdict so a caller can act."""
    lines, worst = status_lines(now, history_dir, symbols)
    for line in lines:
        print(line)
    return worst


if __name__ == '__main__':
    # =====================================================================
    # GATE 3.2c-R1 — declared in PROGRESS_LOG.md and committed ALONE, with no
    # code in that commit, BEFORE this file existed. `git show --stat 30c44b3`.
    #
    # Everything below lives inside `__main__` on purpose: the production half
    # above is what `CHECK_STATUS.bat` runs, and it must be provably untouched
    # by any of this.
    # =====================================================================
    import hashlib
    import shutil
    import subprocess
    import sys
    import tempfile

    # THE PILOT'S PATH. `CHECK_STATUS.bat` runs this with NO arguments and must
    # get the archive block and NOTHING ELSE — a status screen that prints its
    # own self-test is a status screen nobody reads. The gate hides behind
    # --gate, exactly as the recorder's --record does. Check (g) below runs
    # this path in a fresh interpreter and requires its output to be the block
    # exactly, so nothing can quietly start printing here.
    if '--gate' not in sys.argv:
        raise SystemExit(report())

    RED = []

    def check(ok, words):
        print('   %s %s' % ('OK  ' if ok else 'FAIL', words))
        if not ok:
            RED.append(words)
        return ok

    def sha(path):
        return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]

    # The gate's OWN address for the archive — never asked of the code above.
    HERE = os.path.dirname(os.path.abspath(__file__))
    GATE_HISTORY = os.path.join(HERE, 'oi_history')
    GATE_SYMBOLS = ('BTCUSDT', 'ETHUSDT', 'SOLUSDT')
    GATE_SUFFIX = '_4h.csv'
    GATE_FMT = '%Y-%m-%dT%H:%M:%SZ'

    def gate_path(symbol, directory):
        return os.path.join(directory, symbol + GATE_SUFFIX)

    before = {s: sha(gate_path(s, GATE_HISTORY)) for s in GATE_SYMBOLS}

    print(__doc__.strip().splitlines()[0])
    print("GATE 3.2c-R1 — the collection guard's self-test. It breaks itself\n"
          "on purpose every run, because on this ship a check nobody has\n"
          "attacked is a check nobody has tested. The fault it guards against\n"
          "put a green OK on the Commander's screen over a job that collected\n"
          "nothing.\n")

    # -----------------------------------------------------------------
    print("(a) CONTROL — the real archive, untouched. Step 0.1: if the\n"
          "    healthy system does not pass FIRST, nothing below it is\n"
          "    evidence. The ages are read from the gate's own clock.")
    now = datetime.now(timezone.utc)
    try:
        lines, worst = status_lines(now=now, history_dir=GATE_HISTORY,
                                    symbols=GATE_SYMBOLS)
        for line in lines:
            print('     ' + line)
        check(worst == OK, 'the real archive is fresh and the guard is quiet')
    except GuardError as exc:
        check(False, 'the real archive raised: %s' % exc)

    # -----------------------------------------------------------------
    print("\n(b) THE THREE BRANCHES, PROVED EVERY RUN — because a check that\n"
          "    has never been made to fire is decorative, which is the whole\n"
          "    lesson of F10, S6 and B1. These archives are built by THIS\n"
          "    gate from ITS OWN clock, so nothing here depends on the\n"
          "    network or on what the market did today.")

    def build(directory, age_days):
        """A synthetic archive whose newest row is exactly `age_days` old."""
        os.makedirs(directory, exist_ok=True)
        newest = now - timedelta(days=age_days)
        for symbol in GATE_SYMBOLS:
            with open(gate_path(symbol, directory), 'w', newline='',
                      encoding='utf-8') as fh:
                w = csv.writer(fh)
                w.writerow(['timestamp', 'symbol', 'sumOpenInterest',
                            'sumOpenInterestValue'])
                for step in (2, 1, 0):
                    when = newest - timedelta(hours=4 * step)
                    w.writerow([when.strftime(GATE_FMT), symbol,
                                '1.00000000', '2.00000000'])

    scratch = tempfile.mkdtemp(prefix='zarx_guard_')
    try:
        for age, want, words in (
                (0.2, OK, 'a FRESH archive (0.2 days) — the guard stays QUIET'),
                (14.0, STALE, 'a STALE archive (14 days) — the guard goes LOUD '
                              'and nothing is lost yet'),
                (33.0, LOST, 'an archive past BINANCE\'S OWN 30-DAY WINDOW (33 '
                             'days) — the guard must say rows are GONE, which '
                             'is a different sentence from "stale"')):
            directory = os.path.join(scratch, 'age_%s' % age)
            build(directory, age)
            lines, got = status_lines(now=now, history_dir=directory,
                                      symbols=GATE_SYMBOLS)
            ok = check(got == want, words)
            print('        > ' + lines[-1].strip())
            if ok and want != OK:
                check('!!' in lines[-1],
                      '   and it is marked so a stranger would see it')

        # B14's shape: the archive under a DIFFERENT filename. The guard must
        # report it MISSING, never follow it and certify the move.
        moved = os.path.join(scratch, 'moved')
        os.makedirs(moved, exist_ok=True)
        build(os.path.join(scratch, 'src'), 0.2)
        for symbol in GATE_SYMBOLS:
            shutil.copyfile(gate_path(symbol, os.path.join(scratch, 'src')),
                            os.path.join(moved, symbol + '.csv'))
        lines, got = status_lines(now=now, history_dir=moved,
                                  symbols=GATE_SYMBOLS)
        check(got == LOST and MISSING_WORDS in lines[1],
              "B14's shape: the archive under another filename is reported "
              "MISSING, not followed — the guard walks to ITS OWN address")

        # A file that EXISTS and holds no row must RAISE, never read as fine.
        empty = os.path.join(scratch, 'empty')
        os.makedirs(empty, exist_ok=True)
        for symbol in GATE_SYMBOLS:
            with open(gate_path(symbol, empty), 'w', newline='',
                      encoding='utf-8') as fh:
                csv.writer(fh).writerow(['timestamp', 'symbol',
                                         'sumOpenInterest',
                                         'sumOpenInterestValue'])
        try:
            status_lines(now=now, history_dir=empty, symbols=GATE_SYMBOLS)
            check(False, 'a header-only file was accepted as an answer')
        except GuardError:
            check(True, "a file that EXISTS but holds no row FAILS LOUDLY — "
                        "'present but empty' is not 'no new data'")

        # -----------------------------------------------------------------
        print("\n(c) NO TWO UNATTENDED JOBS MAY SHARE A LOG FILE.\n"
              "    On 2026-08-03 six jobs were released in the same second and\n"
              "    the log holds ONE entry for that second. That was\n"
              "    reproduced once, by launching six batches together — but it\n"
              "    could NOT be made to fire on demand, so it is NOT asserted\n"
              "    here. A gate that passes on timing is a gate that lies on a\n"
              "    slow morning (R-039). What IS deterministic is the shape:\n"
              "    the recorder must not write where anything else writes.")

        import re

        def log_targets(text):
            """Every .log this batch appends to, with `set NAME=` resolved."""
            values = dict(re.findall(r'(?im)^\s*set\s+(\w+)\s*=\s*(\S+)\s*$',
                                     text))
            resolved = text
            for name, value in values.items():
                resolved = resolved.replace('%' + name + '%', value)
            return {m.group(1).lower().replace('/', '\\')
                    for m in re.finditer(r'>>\s*"?([^"\s>&|]+\.log)"?',
                                         resolved)}

        def sharers(named_texts):
            """{log: [batch, ...]} for every log written by more than one."""
            owners = {}
            for name, text in named_texts.items():
                for target in log_targets(text):
                    owners.setdefault(target, []).append(name)
            return {k: sorted(v) for k, v in owners.items() if len(v) > 1}

        # POSITIVE CONTROL FIRST — the detector must FIND a planted collision
        # before its silence about the real files means anything. This is the
        # lesson of check (n) in the recorder's own gate: nobody had asked
        # whether the thing that detects could detect.
        planted = {
            'a.bat': '@echo off\r\necho x >> journal\\shared.log\r\n',
            'b.bat': '@echo off\r\nset LOG=journal\\shared.log\r\n'
                     'echo y >> %LOG%\r\n',
        }
        found = sharers(planted)
        check('journal\\shared.log' in found
              and found.get('journal\\shared.log') == ['a.bat', 'b.bat'],
              'POSITIVE CONTROL: the detector FINDS two batches sharing a log '
              'even when one hides the name behind `set LOG=` — reported %s'
              % (found or 'nothing'))

        # NEGATIVE CONTROL — it must stay silent about batches that do not
        # collide, or it would flag everything and mean nothing.
        apart = {
            'a.bat': '@echo off\r\necho x >> journal\\one.log\r\n',
            'b.bat': '@echo off\r\necho y >> journal\\two.log\r\n',
        }
        check(sharers(apart) == {},
              'NEGATIVE CONTROL: two batches with separate logs are NOT '
              'reported — the detector is not simply flagging everything')

        # NOW THE REAL FILES.
        repo = os.path.dirname(HERE)
        bats = {}
        for name in sorted(os.listdir(repo)):
            if name.lower().endswith('.bat'):
                bats[name] = open(os.path.join(repo, name), encoding='utf-8',
                                  errors='replace').read()
        collisions = sharers(bats)
        recorder_logs = log_targets(bats.get('run_oi_recorder.bat', ''))
        check(bool(recorder_logs),
              'the recorder batch names a log at all — found %s'
              % (sorted(recorder_logs) or 'NOTHING'))
        clash = {k: v for k, v in collisions.items() if k in recorder_logs}
        check(not clash,
              'THE RECORDER WRITES WHERE NOTHING ELSE WRITES — it cannot lose '
              'its entry to a sibling job%s'
              % ('' if not clash else ': %s' % clash))
        for target, owners in sorted(collisions.items()):
            print('        · still shared by %d jobs: %s  <- %s'
                  % (len(owners), target, ', '.join(owners)))
        print('        (the snapshot jobs still share one log. They collect '
              'rows that CAN be re-fetched; the recorder\'s cannot. R-040.)')

        # -----------------------------------------------------------------
        print("\n(d) THE HONEST EXIT CODE — Windows recorded `Last Result: 0`\n"
              "    for a job that did nothing, and CHECK_STATUS.bat printed\n"
              "    that 0 to the Commander as 'OK'. A batch that ends on a\n"
              "    `copy` reports the COPY's success, not the recorder's.\n"
              "    BOTH SHAPES RUN: the old one must FAIL here, or the defect\n"
              "    is remembered rather than proved.")

        OLD_TAIL = 'copy /y "%s" "%s" >nul 2>&1'
        NEW_TAIL = 'copy /y "%s" "%s" >nul 2>&1\r\nexit /b %%RC%%'

        def exit_shape(directory, tail, recorder_fails=True):
            """The shipped failure path: the recorder fails and the log IS
            writable, which is the case that produced a reassuring 0."""
            os.makedirs(directory, exist_ok=True)
            log = os.path.join(directory, 'oi_recorder.log')
            copied = os.path.join(directory, 'copy.log')
            open(log, 'w').close()
            inner = ('raise SystemExit(1)' if recorder_fails
                     else "print('Recorded.')")
            bat = os.path.join(directory, 'e.bat')
            with open(bat, 'w', newline='') as fh:
                fh.write('@echo off\r\n'
                         '"' + sys.executable + '" -c "' + inner + '" '
                         '>> "' + log + '" 2>&1\r\n'
                         'set RC=%ERRORLEVEL%\r\n'
                         + tail % (log, copied) + '\r\n')
            return subprocess.run(['cmd', '/c', bat], cwd=directory,
                                  capture_output=True, timeout=180).returncode

        rc_masked = exit_shape(os.path.join(scratch, 'exit_old'), OLD_TAIL)
        check(rc_masked == 0,
              'THE OLD SHAPE — a FAILED recorder ending on `copy` reports %s. '
              'That is the reassuring lie Windows recorded and the status '
              'screen printed as OK' % rc_masked)

        rc_honest = exit_shape(os.path.join(scratch, 'exit_new'), NEW_TAIL)
        check(rc_honest != 0,
              'THE NEW SHAPE — the identical failure now reports %s, so '
              'Windows and CHECK_STATUS.bat are told the truth' % rc_honest)

        rc_healthy = exit_shape(os.path.join(scratch, 'exit_ok'), NEW_TAIL,
                                recorder_fails=False)
        check(rc_healthy == 0,
              'AND A HEALTHY RUN STILL REPORTS 0 — a batch that always fails '
              'is not an alarm, it is a broken part')

        # -----------------------------------------------------------------
        print("\n(e) THE SHIPPED FILES THEMSELVES — the drills above prove the\n"
              "    mechanism on a reconstruction. These read the real files,\n"
              "    so a future session cannot quietly undo the repair without\n"
              "    this gate going red and naming what it lost.")
        repo = os.path.dirname(HERE)
        bat_text = open(os.path.join(repo, 'run_oi_recorder.bat'),
                        encoding='utf-8', errors='replace').read()
        check('journal\\oi_recorder.log' in bat_text,
              'run_oi_recorder.bat writes to its OWN log')
        check('journal\\daily_runs.log' not in bat_text,
              'run_oi_recorder.bat no longer shares daily_runs.log with five '
              'other jobs')
        check('exit /b %RC%' in bat_text,
              'run_oi_recorder.bat ends by reporting the RECORDER\'s exit '
              'code, not the copy\'s')
        status_text = open(os.path.join(repo, 'CHECK_STATUS.bat'),
                           encoding='utf-8', errors='replace').read()
        check('collection_guard' in status_text,
              'CHECK_STATUS.bat asks THIS guard about the archive, instead of '
              'asking Windows how the job felt about itself')
        check('--gate' not in status_text,
              'CHECK_STATUS.bat calls the PILOT path, not the gate — the '
              'Commander must not be shown a self-test where he expects a '
              'status line')

        # -----------------------------------------------------------------
        print("\n(g) THE PILOT'S PATH PRINTS THE BLOCK AND NOTHING ELSE —\n"
              "    run in a FRESH interpreter, because every check above runs\n"
              "    in a process where this file is already imported and could\n"
              "    never see a stray print. The first draft of this repair put\n"
              "    the WHOLE self-test on the Commander's status screen.")
        fresh = subprocess.run([sys.executable, os.path.abspath(__file__)],
                               capture_output=True, text=True, timeout=180,
                               env=dict(os.environ, PYTHONUTF8='1'))
        expected, _ = status_lines(history_dir=GATE_HISTORY,
                                   symbols=GATE_SYMBOLS)
        got = fresh.stdout.replace('\r\n', '\n').strip().split('\n')
        check(got == [line.rstrip() for line in expected],
              'the no-argument run printed EXACTLY the %d-line archive block '
              '— nothing added, no self-test, no traceback' % len(expected))
        check(fresh.stderr.strip() == '',
              'the no-argument run wrote NOTHING to stderr — it reaches the '
              'same screen (F15, S16)')
        for line in got:
            print('        | ' + line)

    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    # -----------------------------------------------------------------
    print("\n(f) THE ARCHIVE IS UNTOUCHED — this guard reads and never writes.\n"
          "    Checksums printed before and after, not asserted.")
    for symbol in GATE_SYMBOLS:
        after = sha(gate_path(symbol, GATE_HISTORY))
        check(after == before[symbol],
              '%s sha256 %s before -> %s after — IDENTICAL'
              % (symbol, before[symbol], after))

    print()
    if RED:
        print('GATE 3.2c-R1 FAILED — %d red:' % len(RED))
        for words in RED:
            print('   - %s' % words)
        sys.exit(1)
    print("GATE 3.2c-R1 PASSED — the guard reads the ARCHIVE rather than the\n"
          "job's own opinion of itself; all three verdicts (fresh, stale, and\n"
          "past Binance's 30-day window) were driven this run from timestamps\n"
          "this gate built itself, so none of them is a branch nobody has\n"
          "seen fire; an archive under another filename is reported MISSING\n"
          "instead of followed; a file that exists but holds no row fails\n"
          "loudly; the log-sharing detector found a PLANTED collision and\n"
          "stayed silent about a clean pair before it was believed about the\n"
          "real files; THE EXIT-CODE FAULT WAS REPRODUCED AND THEN PROVED\n"
          "FIXED, with the old shape REQUIRED to report its reassuring 0 and\n"
          "a healthy run REQUIRED to still report 0; the shipped batch files\n"
          "were read and required to carry the repair; and the three archive\n"
          "files are byte-identical to how this gate found them.\n"
          "\n"
          "AND WHAT THIS GATE DOES NOT TEST, SAID IN ITS OWN PASS LINE\n"
          "BECAUSE R-030 AND R-033 WERE BOTH GATES OVERSTATING THEIR SCOPE:\n"
          "it does NOT reproduce the log CONTENTION that started this. That\n"
          "was seen once in the real log and once in a six-way launch, and it\n"
          "could NOT be made to fire on demand — so this gate asserts only the\n"
          "SHAPE (nothing else writes where the recorder writes), never the\n"
          "race. It does not explain why Windows reported 0, and it does not\n"
          "guard the sibling jobs that still share one log. R-039 and R-040.\n"
          "This test has demonstrated, this run, that it can say no.")
