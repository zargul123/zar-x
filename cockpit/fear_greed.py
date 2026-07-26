"""
Zar X cockpit — the Fear & Greed instrument (Context Deck, Phase 3, Step 3.1).

The crowd-mood gauge: alternative.me's Crypto Fear & Greed Index, one number a
day from 0 (Extreme Fear) to 100 (Extreme Greed), free and keyless. A single
request brings today plus a week of history, so the Brief can show not only
where the mood is but which way it has been moving.

INFORMATION, NEVER A SIGNAL. This part describes the crowd; it never says what
to do about it. The signals doorway stands: nothing that proposes a trade may
appear here without first earning a stat card in the Lab.

Fail-safe (Law 3): every failure — no internet, timeout, HTTP error, a schema
that changed overnight — becomes one honest offline line, and the Brief
carries on with everything else intact.

Standalone smoke test:
    python cockpit/fear_greed.py        (live section, then the offline drill)
"""
import sys
from datetime import datetime, timezone

import requests

FNG_URL = 'https://api.alternative.me/fng/'
HISTORY_LIMIT = 8      # today + 7 days of context, in one request
TIMEOUT = 10           # seconds; one attempt, never a retry storm
HEADER = "  CONTEXT DECK"
OFFLINE_WORDS = "Fear & Greed instrument offline"

# Used only by the offline drill: the .invalid top-level domain is reserved by
# the RFCs and can never resolve, so the drill proves the fail-safe without
# unplugging the Commander's internet.
OFFLINE_DRILL_URL = 'https://zar-x-offline-drill.invalid/fng/'


def _get(base_url, limit, timeout):
    """The only network call in this part. One request, no retries."""
    r = requests.get(base_url, params={'limit': limit}, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _parse(payload):
    """Response -> newest-first list of readings.

    Raises on anything unexpected; every caller turns a raise into the offline
    line. Refusing a surprise is honest — printing a number we do not
    understand is not.
    """
    if not isinstance(payload, dict):
        raise ValueError("response is not a JSON object")
    reported = (payload.get('metadata') or {}).get('error')
    if reported:
        raise ValueError(f"source reported an error: {reported}")
    rows = payload.get('data')
    if not isinstance(rows, list) or not rows:
        raise ValueError("response carries no 'data' list")

    readings = []
    for row in rows:
        value = int(str(row['value']).strip())
        if not 0 <= value <= 100:
            raise ValueError(f"value {value} is outside 0-100")
        readings.append({
            'value': value,
            'label': str(row['value_classification']).strip(),
            'date': datetime.fromtimestamp(int(row['timestamp']),
                                           timezone.utc).date(),
        })
    readings.sort(key=lambda r: r['date'], reverse=True)
    return readings


def _age_words(days: int) -> str:
    if days == 1:
        return "yesterday"
    if days == 7:
        return "a week ago"
    return f"{days} days ago"


def _context_words(readings) -> str:
    """The two comparison points, each labelled by its REAL age in days, so a
    gap in the source's history can never be printed under a wrong name."""
    today = readings[0]['date']
    parts = [f"{_age_words((today - r['date']).days)} {r['value']}"
             for r in (readings[i] for i in (1, 7) if i < len(readings))]
    return f"   ({' · '.join(parts)})" if parts else ""


def section_text(base_url=FNG_URL, limit=HISTORY_LIMIT, timeout=TIMEOUT):
    """The Context Deck block the Brief prints — this part's single doorway.

    Never raises. On any failure the deck still appears, carrying one line
    that says so. base_url is injectable so the offline drill can point this
    at an unreachable address without disconnecting anything.
    """
    try:
        readings = _parse(_get(base_url, limit, timeout))
        now = readings[0]
        return "\n".join([
            HEADER,
            f"  Fear & Greed : {now['value']} — {now['label']}"
            f"{_context_words(readings)}"
            f"   [reading of {now['date']} UTC]",
            "  (crowd-mood gauge from alternative.me — information, not a signal)",
        ])
    except Exception as e:
        return f"{HEADER}\n  🔌 {OFFLINE_WORDS} ({type(e).__name__})"


if __name__ == '__main__':
    ok = True

    print("1) LIVE SECTION — what the Brief will print")
    try:
        readings = _parse(_get(FNG_URL, HISTORY_LIMIT, TIMEOUT))
        now = readings[0]
        print(f"   fetched {len(readings)} daily readings, "
              f"{readings[-1]['date']} → {now['date']} (UTC)")
        checks = [
            (0 <= now['value'] <= 100, f"value {now['value']} is within 0-100"),
            (bool(now['label']), f"classification present: {now['label']!r}"),
            (len(readings) >= 8, f"{len(readings)} readings — a week of context"),
        ]
        for passed, words in checks:
            print(f"   {'✓' if passed else '✗'} {words}")
            ok = ok and passed
    except Exception as e:
        print(f"   ✗ live fetch failed: {type(e).__name__}: {e}")
        ok = False

    live = section_text()
    print()
    print(live)
    if OFFLINE_WORDS in live:
        print("   ✗ the live section came back offline")
        ok = False

    print("\n2) OFFLINE DRILL — injected unreachable URL, internet untouched")
    print(f"   pointing the instrument at {OFFLINE_DRILL_URL}")
    drill = section_text(base_url=OFFLINE_DRILL_URL)
    print()
    print(drill)
    lines = drill.splitlines()
    drill_ok = OFFLINE_WORDS in drill and len(lines) == 2 and lines[0] == HEADER
    print(f"   {'✓' if drill_ok else '✗'} degraded to one offline line, "
          f"no traceback, nothing else printed")
    ok = ok and drill_ok

    if ok:
        print("\nSMOKE TEST PASSED — live reading and offline drill both behaved.")
    else:
        print("\nSMOKE TEST FAILED — see the ✗ lines above.")
    sys.exit(0 if ok else 1)
