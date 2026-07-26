"""
Zar X Lab — Step 2.1: THE VAULT GUARD.

Recomputes the SHA-256 of every vault file and compares it to MANIFEST.json.
If one byte of frozen history ever changes — a stray edit, a bad sync, a
corrupted disk, a line-ending mangling — this says so, loudly, by name.

It reads. It never writes. Its output carries no clock and no randomness,
so running it twice must print exactly the same words twice; that sameness
is itself part of the gate.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\verify_vault.py
"""
import sys
import os
import json
import hashlib

VAULT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vault')
MANIFEST_PATH = os.path.join(VAULT_DIR, 'MANIFEST.json')


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            h.update(block)
    return h.hexdigest()


def main():
    print('=' * 70)
    print('ZAR X LAB — VAULT VERIFICATION')
    print('=' * 70)

    if not os.path.exists(MANIFEST_PATH):
        print('NO VAULT FOUND (lab/vault/MANIFEST.json is missing).')
        print('Build it first: lab/build_vault.py')
        return 1

    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    files = manifest.get('files', {})
    print(f'Vault built: {manifest.get("built_utc", "unknown")}')
    print(f'Source     : {manifest.get("source", "unknown")}')
    print(f'Files      : {len(files)}')
    print('-' * 70)

    intact, corrupted, missing = 0, 0, 0
    for name in sorted(files):
        info = files[name]
        path = os.path.join(VAULT_DIR, name)
        label = f'{name:<20} {info["rows"]:>6} candles  {info["first_candle"][:10]} → {info["last_candle"][:10]}'
        if not os.path.exists(path):
            print(f'VAULT MISSING   {label}')
            missing += 1
            continue
        actual = sha256_of_file(path)
        if actual == info['sha256']:
            print(f'VAULT INTACT    {label}')
            intact += 1
        else:
            print(f'VAULT CORRUPTED {label}')
            print(f'                 expected sha256 {info["sha256"]}')
            print(f'                 found    sha256 {actual}')
            corrupted += 1

    # Anything sitting in the vault that the manifest does not know about is
    # not evidence — it is a stranger. Name it, do not touch it.
    known = set(files) | {'MANIFEST.json', '.gitattributes', 'README.md'}
    strangers = sorted(n for n in os.listdir(VAULT_DIR) if n not in known)
    print('-' * 70)
    for n in strangers:
        print(f'UNKNOWN FILE    {n} (not in MANIFEST — not part of the vault)')

    if corrupted == 0 and missing == 0:
        print(f'RESULT: VAULT INTACT — all {intact} files match their checksums.')
        return 0
    print(f'RESULT: VAULT DAMAGED — {intact} intact, {corrupted} corrupted, '
          f'{missing} missing.')
    print('Frozen history changed. Do NOT run backtests until this is explained.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
