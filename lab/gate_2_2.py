"""
Zar X Lab — GATE 2.2 (the Data Validator's own exam).

The plan's words: feed it (a) a clean vault file → PASS; (b) a COPY
deliberately corrupted — drop 5 candles, duplicate 2, one negative price →
it must name ALL THREE diseases. If it misses any, it does not get committed.

The corrupted copy lives in memory only. Nothing inside lab/vault/ is ever
written, moved, or touched — it is checksummed evidence.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\gate_2_2.py
"""
import sys
import os

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validator import validate_candles, validate_csv, VAULT_DIR

CLEAN_FILE = 'BTC-USD_1d.csv'   # the vault file that carries no flags at all
CLEAN_TF = '1d'


def part_a():
    print('GATE 2.2 (a) — A CLEAN VAULT FILE MUST PASS')
    print('-' * 70)
    rep = validate_csv(os.path.join(VAULT_DIR, CLEAN_FILE), CLEAN_TF)
    print(rep.text())
    ok = rep.verdict == 'PASS'
    print(f'\n(a) {"PASSED" if ok else "FAILED"} — verdict was {rep.verdict}, '
          f'expected PASS\n')
    return ok


def part_b():
    print('GATE 2.2 (b) — A DELIBERATELY POISONED COPY MUST BE CAUGHT')
    print('-' * 70)
    original = pd.read_csv(os.path.join(VAULT_DIR, CLEAN_FILE),
                           index_col=0, parse_dates=True)
    sick = original.copy()          # a COPY, in memory — the vault is untouched

    # Disease 1 — drop 5 candles out of the middle (holes in the timeline)
    dropped = sick.index[500:505]
    sick = sick.drop(index=dropped)

    # Disease 2 — duplicate 2 candles (the same moment counted twice)
    duped = sick.index[100:102]
    sick = pd.concat([sick, sick.loc[duped]]).sort_index()

    # Disease 3 — one negative price
    poisoned_time = sick.index[300]
    sick.loc[poisoned_time, 'low'] = -1.0

    print(f'Poison planted in a memory copy of {CLEAN_FILE}:')
    print(f'  - dropped 5 candles: {dropped[0]} → {dropped[-1]}')
    print(f'  - duplicated 2 candles: {list(duped)}')
    print(f'  - one negative price at {poisoned_time} (low = -1.0)')
    print(f'  - rows: {len(original)} clean → {len(sick)} poisoned\n')

    rep = validate_candles(sick, timeframe=CLEAN_TF,
                           name=f'{CLEAN_FILE} [POISONED COPY]')
    print(rep.text())

    found = ' '.join(h for h, _ in rep.diseases + rep.concerns).upper()
    checks = {
        'named the missing candles': 'MISSING CANDLES' in found,
        'named the duplicate timestamps': 'DUPLICATE TIMESTAMPS' in found,
        'named the negative price': 'ZERO OR NEGATIVE PRICES' in found,
        'refused the file (verdict FAIL)': rep.verdict == 'FAIL',
    }
    print()
    for label, ok in checks.items():
        print(f'  [{"OK" if ok else "MISSED"}] {label}')
    ok = all(checks.values())
    print(f'\n(b) {"PASSED" if ok else "FAILED"}\n')

    # Prove the vault on disk is exactly as it was.
    after = pd.read_csv(os.path.join(VAULT_DIR, CLEAN_FILE),
                        index_col=0, parse_dates=True)
    untouched = after.equals(original)
    print(f'  [{"OK" if untouched else "VIOLATION"}] the real vault file was '
          f'not modified ({len(after)} rows, unchanged)')
    return ok and untouched


def main():
    print('=' * 70)
    print('ZAR X LAB — GATE 2.2')
    print('=' * 70)
    a = part_a()
    b = part_b()
    print('=' * 70)
    print(f'GATE 2.2: {"PASSED" if (a and b) else "FAILED"}  '
          f'(a={"pass" if a else "fail"}, b={"pass" if b else "fail"})')
    print('=' * 70)
    return 0 if (a and b) else 1


if __name__ == '__main__':
    sys.exit(main())
