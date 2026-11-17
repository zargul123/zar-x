"""
Zar X — THE CLOUD PROBE. One question: can the paper-watch live in the cloud?

Ordered by the Commander on 2026-11-17: "first only test cloud test run. and
tell me first can it work?" It READS and it REPORTS. It writes nothing to
`journal/paper/`, sends no order, holds no key, and prints NO PRICE and NO
RATE: only whether each source answered, and how many rows.

    1. Do the three sources the paper-watch needs answer from here?
    2. If Binance futures refuses, do other doors exist? (status only)
    3. Does THIS machine work the existing ledger out identical?
    4. Does GATE 7.1 pass on this machine?

    python journal/cloud_probe.py
"""
import os
import platform
import subprocess
import sys

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 20


def ask(name, url, params=None):
    """-> one line: the status and the row count. Never a figure."""
    try:
        import requests
        reply = requests.get(url, params=params, timeout=TIMEOUT,
                             headers={'User-Agent': 'python'})
        rows = '-'
        try:
            body = reply.json()
            if isinstance(body, list):
                rows = len(body)
            elif isinstance(body, dict):
                for key in ('data', 'result'):
                    inner = body.get(key)
                    if isinstance(inner, dict):
                        inner = inner.get('list')
                    if isinstance(inner, list):
                        rows = len(inner)
                if rows == '-' and 'msg' in body:
                    rows = f"message: {str(body['msg'])[:70]}"
        except ValueError:
            pass
        return f'{name:34s} status {reply.status_code}  rows {rows}'
    except Exception as exc:
        return f'{name:34s} FAILED  {type(exc).__name__}: {str(exc)[:70]}'


def main():
    lines = ['ZAR X - THE CLOUD PROBE (statuses and counts only; no price, '
             'no rate)',
             f'python {platform.python_version()} on {platform.system()}']
    try:
        import numpy
        import pandas
        lines.append(f'numpy {numpy.__version__}  pandas {pandas.__version__}')
    except Exception as exc:
        lines.append(f'numpy/pandas: {type(exc).__name__}: {exc}')

    lines += ['', '1. WHAT THE PAPER-WATCH NEEDS']
    lines.append(ask('candles  data-api.binance.vision',
                     'https://data-api.binance.vision/api/v3/klines',
                     {'symbol': 'BTCUSDT', 'interval': '1d', 'limit': 5}))
    lines.append(ask('funding  fapi.binance.com',
                     'https://fapi.binance.com/fapi/v1/fundingRate',
                     {'symbol': 'BTCUSDT', 'limit': 5}))
    lines.append(ask('mood     alternative.me',
                     'https://api.alternative.me/fng/',
                     {'limit': 5, 'format': 'json'}))

    lines += ['', '2. OTHER DOORS, IN CASE ONE IS SHUT (status only)']
    for host in ('fapi1', 'fapi2', 'fapi3'):
        lines.append(ask(f'funding  {host}.binance.com',
                         f'https://{host}.binance.com/fapi/v1/fundingRate',
                         {'symbol': 'BTCUSDT', 'limit': 5}))
    lines.append(ask('candles  api.binance.com',
                     'https://api.binance.com/api/v3/klines',
                     {'symbol': 'BTCUSDT', 'interval': '1d', 'limit': 5}))
    lines.append(ask('funding  bybit',
                     'https://api.bybit.com/v5/market/funding/history',
                     {'category': 'linear', 'symbol': 'BTCUSDT',
                      'limit': 5}))
    lines.append(ask('funding  okx',
                     'https://www.okx.com/api/v5/public/funding-rate-history',
                     {'instId': 'BTC-USDT-SWAP', 'limit': 5}))

    lines += ['', '3. DOES THIS MACHINE WORK THE LEDGER OUT IDENTICAL?']
    try:
        sys.path.insert(0, JOURNAL_DIR)
        import paper_watch
        text = paper_watch.report()
        keep = [row for row in text.split('\n')
                if 'ALARM' in row or 'OFFLINE' in row
                or row.startswith('OPEN NOW') or 'written LATE' in row
                or 'written ON TIME' in row]
        verdict = ('NO - INTEGRITY ALARM' if 'INTEGRITY ALARM' in text
                   else 'NO - OFFLINE' if 'OFFLINE' in text
                   else 'YES - every written row comes out identical')
        lines.append(verdict)
        lines += [f'   {row.strip()[:150]}' for row in keep[:8]]
    except Exception as exc:
        lines.append(f'COULD NOT BE ASKED  {type(exc).__name__}: {exc}')

    lines += ['', '4. GATE 7.1 ON THIS MACHINE']
    try:
        done = subprocess.run(
            [sys.executable, os.path.join(JOURNAL_DIR, 'paper_watch.py'),
             '--gate'], capture_output=True, timeout=900)
        out = done.stdout.decode('utf-8', 'replace').split('\n')
        last = [row for row in out if row.startswith('GATE 7.1 ')]
        reds = [row.strip()[:170] for row in out if '✗' in row]
        lines.append(f'exit {done.returncode}  '
                     f'{last[-1] if last else "NO VERDICT LINE"}')
        lines += [f'   RED: {row}' for row in reds[:12]]
        if not last:
            tail = done.stderr.decode('utf-8', 'replace').strip().split('\n')
            lines += [f'   {row[:170]}' for row in tail[-6:]]
    except Exception as exc:
        lines.append(f'COULD NOT RUN  {type(exc).__name__}: {exc}')

    print('\n'.join(lines))
    return 0


if __name__ == '__main__':
    sys.exit(main())
