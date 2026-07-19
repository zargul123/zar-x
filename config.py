"""Zar X — central configuration. Single source of truth for settings."""
import os

from dotenv import load_dotenv
load_dotenv()

# Assets the cockpit watches
ASSETS = ["BTC-USD", "ETH-USD", "SOL-USD"]

# --- TwelveData (primary candle source) ---
TWELVEDATA_API_KEY = os.environ.get("TWELVEDATA_API_KEY")
TWELVEDATA_CONFIG = {
    'base_url': 'https://api.twelvedata.com',
    'timeout': 10,
    'max_retries': 3,          # retries after a 429 rate-limit response
    'rate_wait_seconds': 65,   # wait for the free-tier window to reset
    'chunk_pause_seconds': 8,  # pacing between paginated chunks (8 req/min tier)
}
TWELVEDATA_MAPPING = {
    "BTC-USD": "BTC/USD",
    "ETH-USD": "ETH/USD",
    "SOL-USD": "SOL/USD",
}

# Timeframe naming: Zar X name -> TwelveData interval
TIMEFRAME_MAP = {
    '1m': '1min', '5m': '5min', '15m': '15min', '30m': '30min',
    '1h': '1h', '4h': '4h', '1d': '1day',
}

# Yahoo Finance fallback: how much history each timeframe may request
YAHOO_PERIOD_MAP = {'1h': '60d', '4h': '120d', '1d': '2y', '15m': '30d'}
