"""
Zar X Lab — Step 2.1: THE FROZEN VAULT (build it once, never again).

WHY THIS EXISTS
A live API always hands back fresh data. If the Lab asks the internet for
candles every time it tests something, "hold-out testing" is only a word:
the data under the test keeps moving. So we download deep history ONCE,
write it to disk, checksum every file, and never touch it again. Every
backtest from now on reads these frozen files. That is what makes a
verdict repeatable.

WHAT IT DOES
- Downloads BTC-USD, ETH-USD, SOL-USD on the 4h and 1d timeframes, as far
  back as TwelveData will give (target 3 years, 1 year is the floor).
- Writes lab/vault/{asset}_{timeframe}.csv
- Writes lab/vault/MANIFEST.json — rows, first/last candle, SHA-256, dates.

THE VAULT IS ONLY BORN COMPLETE: every download happens first, in memory.
Not a single file is written unless all six arrived. If anything fails
midway, nothing is written and nothing is half-born.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\build_vault.py
"""
import sys
import os
import json
import time
import hashlib
import subprocess
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ASSETS, TWELVEDATA_CONFIG
from data.market_data import MarketData

VAULT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vault')
MANIFEST_PATH = os.path.join(VAULT_DIR, 'MANIFEST.json')

TIMEFRAMES = ['4h', '1d']
TARGET_DAYS = 1095          # 3 years — what we ask for
MIN_DAYS = 365              # 1 year — the floor; below this we STOP and ask
CANDLE_SECONDS = {'4h': 4 * 3600, '1d': 24 * 3600}
COLUMNS = ['open', 'high', 'low', 'close', 'volume']


def sha256_of_file(path):
    """Checksum of the bytes actually on disk — the vault's fingerprint."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            h.update(block)
    return h.hexdigest()


def git_commit():
    try:
        out = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=os.path.dirname(VAULT_DIR), capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or 'unknown'
    except Exception:
        return 'unknown'


def drop_unclosed_candle(df, timeframe, now_utc):
    """The newest candle from a live API is usually still forming: its high,
    low and close are not final. A frozen vault must hold only FINISHED
    candles, otherwise every future backtest inherits one fake candle."""
    span = timedelta(seconds=CANDLE_SECONDS[timeframe])
    closed = df[df.index + span <= now_utc]
    return closed, len(df) - len(closed)


def main():
    print('=' * 70)
    print('ZAR X LAB — BUILDING THE FROZEN VAULT (Step 2.1)')
    print('=' * 70)

    # --- Law 5: never rewrite evidence. A born vault is never re-born. ---
    if os.path.exists(MANIFEST_PATH):
        print('\nA vault already exists (lab/vault/MANIFEST.json is there).')
        print('The vault is downloaded ONCE and never modified — that is the')
        print('whole point of it. Nothing was changed.')
        print('If a rebuild is truly wanted, the Commander deletes lab/vault')
        print('by hand first, on purpose.')
        return 1

    os.makedirs(VAULT_DIR, exist_ok=True)
    md = MarketData()
    now_utc = datetime.utcnow()

    jobs = [(a, tf) for a in ASSETS for tf in TIMEFRAMES]
    downloaded = {}   # (asset, tf) -> DataFrame, held in memory until all arrive

    print(f'\nAsking TwelveData for {TARGET_DAYS} days ({TARGET_DAYS / 365:.1f} years) '
          f'of history, {len(jobs)} files.')
    print('This is slow on purpose (free tier: 8 requests a minute).\n')

    for i, (asset, tf) in enumerate(jobs, 1):
        print(f'[{i}/{len(jobs)}] {asset} {tf} ...')
        df = md.get_history(asset, timeframe=tf, days=TARGET_DAYS)
        if df is None or df.empty:
            print(f'\n❌ DOWNLOAD FAILED for {asset} {tf}.')
            print('Nothing has been written. The vault is only born complete —')
            print('fix the connection/key and run this again from the start.')
            return 1

        df = df[[c for c in COLUMNS if c in df.columns]].copy()
        df, dropped = drop_unclosed_candle(df, tf, now_utc)
        if dropped:
            print(f'   - dropped {dropped} still-forming candle(s) at the end')

        span_days = (df.index[-1] - df.index[0]).total_seconds() / 86400
        print(f'   - kept {len(df)} candles, {df.index[0].date()} → '
              f'{df.index[-1].date()} ({span_days / 365:.2f} years)')

        if span_days < MIN_DAYS:
            print(f'\n🛑 STOP — {asset} {tf} came back with only {span_days / 365:.2f} '
                  f'years of history.')
            print(f'The plan\'s floor is {MIN_DAYS} days (1 year). Below that a')
            print('backtest cannot be trusted. Nothing was written.')
            print('COMMANDER\'S DECISION NEEDED: pay for deeper history, wait,')
            print('or proceed knowingly thin.')
            return 1

        downloaded[(asset, tf)] = df
        if i < len(jobs):
            time.sleep(TWELVEDATA_CONFIG['chunk_pause_seconds'])

    # --- All six arrived. Only now does anything touch the disk. ---
    print('\nAll files downloaded. Writing the vault...')
    written = []
    files_manifest = {}
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        for (asset, tf), df in downloaded.items():
            name = f'{asset}_{tf}.csv'
            path = os.path.join(VAULT_DIR, name)
            # lineterminator='\n' keeps the bytes identical on every machine,
            # so the checksum means the same thing on the laptop and in the cloud.
            df.to_csv(path, index_label='datetime', lineterminator='\n')
            written.append(path)
            span_days = (df.index[-1] - df.index[0]).total_seconds() / 86400
            files_manifest[name] = {
                'asset': asset,
                'timeframe': tf,
                'rows': int(len(df)),
                'first_candle': df.index[0].strftime('%Y-%m-%d %H:%M:%S'),
                'last_candle': df.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'days_covered': round(span_days, 2),
                'years_covered': round(span_days / 365, 2),
                'bytes': os.path.getsize(path),
                'sha256': sha256_of_file(path),
            }
            print(f'   ✅ {name}: {len(df)} rows, sha256 {files_manifest[name]["sha256"][:16]}...')

        manifest = {
            'vault_version': 1,
            'built_utc': stamp,
            'built_by_git_commit': git_commit(),
            'source': 'TwelveData via data/market_data.py get_history()',
            'requested_days': TARGET_DAYS,
            'timeframes': TIMEFRAMES,
            'assets': list(ASSETS),
            'unclosed_last_candle_dropped': True,
            'law': 'These files are evidence. They are never modified, only verified.',
            'files': files_manifest,
        }
        with open(MANIFEST_PATH, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(manifest, indent=2) + '\n')
        written.append(MANIFEST_PATH)
    except Exception as e:
        print(f'\n❌ WRITING FAILED: {e}')
        for p in written:
            try:
                os.remove(p)
            except OSError:
                pass
        print('Every partial file was deleted. The vault is only born complete.')
        return 1

    total_rows = sum(v['rows'] for v in files_manifest.values())
    print('\n' + '=' * 70)
    print(f'VAULT BUILT: {len(files_manifest)} files, {total_rows} candles, '
          f'MANIFEST.json written.')
    print('From here on the Lab reads these files and nothing else.')
    print('Next: run lab/verify_vault.py — it must say INTACT for all six.')
    print('=' * 70)
    return 0


if __name__ == '__main__':
    sys.exit(main())
