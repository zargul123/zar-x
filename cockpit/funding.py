"""
Zar X cockpit — the funding-rate instrument (Context Deck, Phase 3, Step 3.2).

Perpetual futures have no expiry, so an exchange keeps their price tethered to
spot by making one side pay the other every 8 hours. That payment is the
funding rate, and its SIGN says which way the crowd is leaning: when it is
positive, traders holding longs pay traders holding shorts; when it is
negative, shorts pay longs. Binance settles at 00:00, 08:00 and 16:00 UTC.

**These are the USDT PERPETUAL CONTRACTS (BTCUSDT / ETHUSDT / SOLUSDT), not
the spot pairs the rest of the Brief prices.** They are different instruments
that happen to track each other, and saying so plainly is the whole reason
this note exists.

The number printed is Binance's running ESTIMATE for the NEXT settlement, not
a payment that has already happened — `lastFundingRate` moves until it
settles, and Binance's own documentation calls it an estimation. The last
SETTLED rate is read too, but only by the smoke test below, where it serves as
the exact-identity check on this file's parsing: settled rates are fixed
historical facts, so they must match the raw response digit for digit. Both
values pass through the SAME parse and format helpers, so that exact check
guards the printed path as well.

INFORMATION, NEVER A SIGNAL. This part reports crowd positioning; it never
says what to do about it. Stating that longs pay shorts is a fact about the
mechanism, exactly like saying RSI is 46 — it is not a suggestion to trade.
No delta-neutral carry number is computed here: that is Phase 4's job and it
ships with mandatory risk caveats a bare percentage would leave out.

Fail-safe (Law 3): every failure becomes an honest line and the Brief carries
on. If SOME assets answer and others do not, the ones that answered are
printed and the ones that did not are NAMED — partial truth labelled as
partial is honest; silently dropping an asset is not.

Standalone smoke test:
    python cockpit/funding.py       (live block, exact-identity check, drill)
"""
import re
import sys
from datetime import datetime, timezone

import requests

FAPI_BASE = 'https://fapi.binance.com'
TIMEOUT = 10           # seconds; one attempt per asset, never a retry storm
OFFLINE_WORDS = "Funding instrument offline"

# Our assets are spot pairs; funding exists only on the perpetual contracts.
# The mapping lives here because the compartment owns its own source mapping
# (Law 2) — no other part needs to know Binance's naming.
CONTRACTS = {
    'BTC-USD': 'BTCUSDT',
    'ETH-USD': 'ETHUSDT',
    'SOL-USD': 'SOLUSDT',
}

# Sanity bound. Binance caps funding well below this; a value outside it means
# we are reading something that is not a funding rate, and refusing a number we
# do not understand is honest where printing it is not.
MAX_PLAUSIBLE_RATE = 0.05      # 5% per 8h

# Used only by the offline drill: the .invalid top-level domain is reserved by
# the RFCs and can never resolve, so the drill proves the fail-safe without
# unplugging the Commander's internet.
OFFLINE_DRILL_URL = 'https://zar-x-offline-drill.invalid'


def _get(base_url, path, params, timeout):
    """The only network call in this part. One request, no retries."""
    r = requests.get(f"{base_url}{path}", params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()


def _parse_rate(raw) -> float:
    """Binance sends rates as STRINGS. Shared by the estimate and the settled
    reader so the smoke test's exact check covers the printed path too."""
    rate = float(str(raw).strip())
    if abs(rate) > MAX_PLAUSIBLE_RATE:
        raise ValueError(f"rate {rate} is outside +/-{MAX_PLAUSIBLE_RATE}")
    return rate


def _fmt_pct(rate: float) -> str:
    """Shared formatter. The sign is the whole instrument, so it is always
    shown explicitly — never left implied by its absence."""
    return f"{rate * 100:+.4f}%"


def _utc_hhmm(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime('%H:%M')


def read_estimate(base_url, contract, timeout=TIMEOUT):
    """The running estimate for the NEXT settlement, for one contract.

    Raises on anything unexpected; the doorway below turns a raise into an
    honest line.
    """
    payload = _get(base_url, '/fapi/v1/premiumIndex', {'symbol': contract},
                   timeout)
    if not isinstance(payload, dict):
        raise ValueError("premiumIndex response is not a JSON object")
    for field in ('lastFundingRate', 'nextFundingTime'):
        if field not in payload:
            raise ValueError(f"premiumIndex response has no {field!r}")
    return _parse_rate(payload['lastFundingRate']), int(payload['nextFundingTime'])


def read_settled(base_url, contract, timeout=TIMEOUT):
    """The most recent SETTLED rate — a payment that actually happened.

    Not printed on the Brief (the orders cap this instrument at one request per
    asset). It exists for the exact-identity check in the smoke test.
    """
    payload = _get(base_url, '/fapi/v1/fundingRate',
                   {'symbol': contract, 'limit': 1}, timeout)
    if not isinstance(payload, list) or not payload:
        raise ValueError("fundingRate response carries no rows")
    row = payload[0]
    return _parse_rate(row['fundingRate']), int(row['fundingTime'])


def section_text(base_url=FAPI_BASE, contracts=None, timeout=TIMEOUT):
    """The funding block the Brief prints — this part's single doorway.

    Never raises. Joins the EXISTING Context Deck, so it prints no header of
    its own: one deck, two instruments. base_url and contracts are injectable
    so the drills can point this at an unreachable address, or at a bogus
    symbol, without disconnecting anything.
    """
    contracts = CONTRACTS if contracts is None else contracts
    answered, missing, settlements = [], [], []
    try:
        for asset, contract in contracts.items():
            short = asset.split('-')[0]
            try:
                rate, next_ms = read_estimate(base_url, contract, timeout)
                answered.append(f"{short} {_fmt_pct(rate)}")
                settlements.append(next_ms)
            except Exception:
                missing.append(short)

        if not answered:
            raise ConnectionError("no asset answered")

        line = f"  Funding (8h) : {'  ·  '.join(answered)}"
        if missing:
            line += f"   [no data: {', '.join(missing)}]"
        return "\n".join([
            line,
            f"  (USDT perpetuals · positive = longs pay shorts · next "
            f"settlement {_utc_hhmm(min(settlements))} UTC",
            "   — crowd positioning, information, not a signal)",
        ])
    except Exception as e:
        return f"  🔌 {OFFLINE_WORDS} ({type(e).__name__})"


if __name__ == '__main__':
    ok = True

    print("1) LIVE BLOCK — what the Brief will print")
    live = section_text()
    print()
    print(live)
    print()
    if OFFLINE_WORDS in live:
        print("   ✗ the live block came back offline")
        ok = False
    for short in ('BTC', 'ETH', 'SOL'):
        # _fmt_pct always emits an explicit + or -, so requiring the sign is
        # what separates a printed rate from a name in the "no data" list.
        signed = f"{short} +" in live or f"{short} -" in live
        print(f"   {'✓' if signed else '✗'} {short} rate printed with a sign")
        ok = ok and signed
    # Gate 3.2 (a) also requires the next settlement time, so assert it rather
    # than trusting that it looks present in the block above.
    stamped = bool(re.search(r"next settlement \d{2}:\d{2} UTC", live))
    print(f"   {'✓' if stamped else '✗'} next settlement time printed as HH:MM UTC")
    ok = ok and stamped

    print("\n2) EXACT IDENTITY CHECK (Gate 3.2 b1) — the settled rate this file"
          "\n   parses must match the raw response digit for digit, sign"
          "\n   included. Settled rates are fixed facts, so 'close' is not a"
          "\n   pass. Both values use the same parse/format helpers as the"
          "\n   printed estimate, so this guards the printed path too.")
    for asset, contract in CONTRACTS.items():
        try:
            parsed, when = read_settled(FAPI_BASE, contract)
            raw = requests.get(f"{FAPI_BASE}/fapi/v1/fundingRate",
                               params={'symbol': contract, 'limit': 1},
                               timeout=TIMEOUT).json()[0]['fundingRate']
            exact = parsed == float(raw)
            stamp = datetime.fromtimestamp(when / 1000, timezone.utc)
            print(f"   {'✓' if exact else '✗'} {contract}: parsed {parsed} "
                  f"== raw {raw!r} → {_fmt_pct(parsed)} "
                  f"(settled {stamp:%Y-%m-%d %H:%M} UTC)")
            ok = ok and exact
        except Exception as e:
            print(f"   ✗ {contract}: settled read failed: {type(e).__name__}: {e}")
            ok = False

    print("\n3) PARTIAL-FAILURE DRILL (Gate 3.2 f) — one bogus symbol; the two"
          "\n   that answer must print and the one that does not must be NAMED")
    partial = section_text(contracts={'BTC-USD': 'BTCUSDT',
                                      'ETH-USD': 'ETHUSDT',
                                      'SOL-USD': 'NOTAREALSYMBOL'})
    print()
    print(partial)
    partial_ok = ('no data: SOL' in partial and 'BTC ' in partial
                  and 'ETH ' in partial and OFFLINE_WORDS not in partial)
    print(f"   {'✓' if partial_ok else '✗'} two assets printed, the third named")
    ok = ok and partial_ok

    print("\n4) OFFLINE DRILL — injected unreachable URL, internet untouched")
    print(f"   pointing the instrument at {OFFLINE_DRILL_URL}")
    drill = section_text(base_url=OFFLINE_DRILL_URL)
    print()
    print(drill)
    lines = drill.splitlines()
    drill_ok = OFFLINE_WORDS in drill and len(lines) == 1
    print(f"   {'✓' if drill_ok else '✗'} degraded to one offline line, "
          f"no traceback, nothing else printed")
    ok = ok and drill_ok

    if ok:
        print("\nSMOKE TEST PASSED — live block, exact identity, partial "
              "failure and offline drill all behaved.")
    else:
        print("\nSMOKE TEST FAILED — see the ✗ lines above.")
    sys.exit(0 if ok else 1)
