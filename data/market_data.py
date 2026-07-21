"""
Zar X data compartment — clean candles only.

Ported from Zargul 2.0's proven data engine (429-retry, pagination, Yahoo
fallback, hold-out cutoff). This part fetches and cleans OHLC candles and
nothing else: no indicators, no signals (those live in their own
compartments). Fail-safe: on total failure it reports "instrument offline"
and returns None — it never raises into the rest of the ship.
"""
import sys
import os
import time
import json
from datetime import datetime, timedelta

import pandas as pd
import requests
import yfinance as yf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    TWELVEDATA_API_KEY, TWELVEDATA_CONFIG, TWELVEDATA_MAPPING,
    TIMEFRAME_MAP, YAHOO_PERIOD_MAP,
)


def _redact(text):
    """Strip the API key from any message before it reaches a print/log.
    Error messages from requests include the full URL (apikey=... inside);
    daily_runs.log is synced off-machine, so the key must never enter it."""
    text = str(text)
    if TWELVEDATA_API_KEY:
        text = text.replace(TWELVEDATA_API_KEY, '***REDACTED***')
    return text


class MarketData:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })

    # ------------------------------------------------------------------ #
    # TwelveData primary source
    # ------------------------------------------------------------------ #
    def _twelvedata_request(self, symbol, timeframe, params=None):
        mapped = TWELVEDATA_MAPPING.get(symbol, symbol)
        base = {
            'symbol': mapped,
            'interval': TIMEFRAME_MAP.get(timeframe, '1h'),
            'apikey': TWELVEDATA_API_KEY,
            'outputsize': 5000,
            'format': 'JSON',
        }
        if params:
            base.update(params)

        # Free tier: 8 req/min. On 429, wait for the window and retry —
        # giving up silently truncates history (Zargul 2.0 lesson).
        for attempt in range(TWELVEDATA_CONFIG['max_retries'] + 1):
            try:
                r = self.session.get(
                    f"{TWELVEDATA_CONFIG['base_url']}/time_series",
                    params=base, timeout=TWELVEDATA_CONFIG['timeout'])
                if r.status_code == 429:
                    wait = TWELVEDATA_CONFIG['rate_wait_seconds']
                    print(f"⏳ Rate limit (429) for {symbol}. Waiting {wait}s, retry {attempt + 1}...")
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                return r.json()
            except requests.exceptions.RequestException as e:
                print(f"⚠️ TwelveData request failed for {symbol}: {_redact(e)}")
                return None
            except json.JSONDecodeError:
                print(f"⚠️ TwelveData JSON decode error for {symbol}")
                return None
        print(f"⚠️ TwelveData rate limit persisted after retries for {symbol}.")
        return None

    def _parse_twelvedata(self, data, symbol):
        if not data or 'values' not in data:
            return pd.DataFrame()
        try:
            df = pd.DataFrame(data['values']).iloc[::-1]
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.set_index('datetime').rename(columns=str.lower)
            df = df[~df.index.duplicated(keep='first')]
            for col in ['open', 'high', 'low', 'close', 'volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            df.dropna(subset=['open', 'high', 'low', 'close'], inplace=True)
            return df
        except Exception as e:
            print(f"❌ Error parsing TwelveData response for {symbol}: {_redact(e)}")
            return pd.DataFrame()

    # ------------------------------------------------------------------ #
    # Yahoo Finance fallback (spare tire: recent data only)
    # ------------------------------------------------------------------ #
    def _yahoo_fallback(self, symbol, timeframe):
        try:
            df = yf.download(
                symbol,
                period=YAHOO_PERIOD_MAP.get(timeframe, '30d'),
                interval=TIMEFRAME_MAP.get(timeframe, '1h'),
                progress=False, auto_adjust=False)
            if not df.empty:
                df = df.rename(columns=str.lower)
                if df.index.tz is not None:
                    df.index = df.index.tz_localize(None)
                df = df[~df.index.duplicated(keep='first')]
            return df
        except Exception as e:
            print(f"⚠️ Yahoo fallback failed for {symbol}: {_redact(e)}")
            return pd.DataFrame()

    # ------------------------------------------------------------------ #
    # Public doorways
    # ------------------------------------------------------------------ #
    def get_candles(self, symbol, timeframe='4h', limit=None):
        """Latest candles (single request, max 5000). Clean OHLC only."""
        try:
            df = self._parse_twelvedata(
                self._twelvedata_request(symbol, timeframe), symbol)
            if df.empty:
                print(f"📉 TwelveData failed for {symbol}. Falling back to Yahoo Finance.")
                df = self._yahoo_fallback(symbol, timeframe)
            if df is None or df.empty:
                print(f"🔌 DATA INSTRUMENT OFFLINE for {symbol} ({timeframe}).")
                return None
            if limit:
                df = df.tail(int(limit))
            return df
        except Exception as e:
            print(f"🔌 DATA INSTRUMENT OFFLINE for {symbol}: {_redact(e)}")
            return None

    def get_history(self, symbol, timeframe='4h', days=365, end_date=None):
        """
        Deep history via pagination (chunks of 5000, politely paced).
        end_date (datetime or 'YYYY-MM-DD') enables hold-out cutoffs:
        history ends there so later candles stay unseen by any test.
        """
        try:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            anchor = end_date
            target_start = (end_date or datetime.now()) - timedelta(days=days)
            chunks = []
            while True:
                params = ({'end_date': anchor.strftime('%Y-%m-%d %H:%M:%S')}
                          if anchor else {})
                df = self._parse_twelvedata(
                    self._twelvedata_request(symbol, timeframe, params), symbol)
                if df.empty:
                    break
                chunks.append(df)
                oldest = df.index[0]
                print(f"   - Chunk of {len(df)} candles; oldest {oldest.date()}")
                if oldest <= target_start:
                    break
                anchor = oldest - timedelta(seconds=1)
                time.sleep(TWELVEDATA_CONFIG['chunk_pause_seconds'])

            if not chunks:
                print(f"🔌 DATA INSTRUMENT OFFLINE for {symbol} history.")
                return None
            full = pd.concat(chunks).sort_index()
            full = full[~full.index.duplicated(keep='first')]
            if end_date is not None:
                full = full[full.index <= end_date]
            full = full[full.index >= target_start]
            print(f"✅ History ready: {len(full)} {timeframe} candles "
                  f"{full.index[0].date()} → {full.index[-1].date()}")
            return full
        except Exception as e:
            print(f"🔌 DATA INSTRUMENT OFFLINE for {symbol} history: {_redact(e)}")
            return None
