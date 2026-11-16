"""
Zar X signals compartment — GAUNTLET SLOT 1: the Turtle/Donchian breakout,
ON 4-HOUR CANDLES.

**THIS IS ONE OF THE THREE SEALED SLOTS OF THE PROMISE.** The slot was first
declared on DAILY candles (PROGRESS_LOG.md, 2026-11-15) and never run. On
2026-11-16 the Commander re-specified it to 4-HOUR candles, before any
result existed, and the rules below were declared in PROGRESS_LOG.md that
day and committed with no code, before this file was changed. **NOT ONE
NUMBER HERE WAS SEARCHED, TUNED OR TRIED AGAINST ANY RESULT, AND NONE MAY BE
CHANGED:** a change is a different strategy, and the slot is spent on this
one.

THE RULES, asked at the close of a 4-hour candle, using only candles up to
and including that one:

    BREAKOUT  long  if this candle's close is ABOVE the highest high of the
                    20 candles BEFORE it (itself not included);
              short if it is BELOW the lowest low of those same 20.
              Strictly. Equal is not a breakout.
              **20 candles of 4 hours is 80 hours - about three and a third
              days, not twenty days.**
    WEEKLY    long only if the close is ABOVE the average of the last 10
              weekly closes (this candle, 42 candles ago, ... 378 ago: a
              week is 7 days of 6 candles); short only if BELOW.
    REGIME    only if Wilder's ADX(14) on these candles is ABOVE 25.
    WARM-UP   flat until 379 candles exist - the fewest that can answer the
              weekly filter. **It is also the only thing that stops the
              weekly filter reaching before the first candle.**

**WHAT THIS FILE DOES NOT DECIDE.** The exit. The Lab's engine manages every
open trade with the ship's own stop (1.5 ATR) and target (2.0 ATR); this
strategy is only ever asked when no trade is open. So this is a Turtle
ENTRY, not the Turtles' whole system, and the bar says so in bold.

**IT COUNTS CANDLES, NOT CLOCK TIME.** "42 candles ago" is a week ago only
if no candle is missing. The three vault files were measured on 2026-11-16,
from their date column alone: not one step is other than 4 hours.

**LAW 7.** It carries no data. It reads nothing but the frame it is handed:
no file, no network, no clock, no module global that changes. It keeps
nothing between calls. `lab/leak_check.py` scans it, and its code is short
on purpose so that a person can read all of it.

The contract (lab/engine.py):  signal(df) -> 'long' | 'short' | 'flat'

Standalone use:
    python signals/turtle.py --gate     (the setup gate; never opens the vault)
"""
import numpy as np

ENTRY_CANDLES = 20     # the Turtles' / Donchian's channel, in candles traded
WEEKS = 10             # the weekly trend line: 10 weekly closes
WEEK_CANDLES = 42      # one week of 4-hour candles: 7 days x 6
ADX_PERIOD = 14        # Wilder
ADX_MIN = 25.0         # Wilder; also config's adx_trending_threshold
ADX_TAIL = 150         # the ADX is worked on the last 150 candles
WARMUP = 379           # 1 + 9 x 42: the fewest candles the weekly filter needs
NAME = 'turtle-4h-20c-10w-adx25'


def _rma(values, period):
    """Wilder's running average: the plain mean of the first `period`
    values, then each new value moves it by one part in `period`."""
    out = float(np.mean(values[:period]))
    for value in values[period:]:
        out = (out * (period - 1) + float(value)) / period
    return out


def _rma_series(values, period):
    """The same average, every step of it kept (the ADX needs the series)."""
    out = [float(np.mean(values[:period]))]
    for value in values[period:]:
        out.append((out[-1] * (period - 1) + float(value)) / period)
    return np.array(out)


def wilder_adx(high, low, close, period=ADX_PERIOD):
    """Wilder's ADX on three arrays of equal length -> its latest value.

    Written out in full, here, rather than imported: the strategy must be
    readable in one sitting, and the gate checks this arithmetic against the
    ship's own indicator library on candles it makes up itself.
    A market that has not moved at all has an ADX of 0.
    """
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    close = np.asarray(close, dtype=float)
    if len(close) < 2 * period + 1:
        return 0.0
    up = high[1:] - high[:-1]
    down = low[:-1] - low[1:]
    plus_dm = np.where((up > down) & (up > 0), up, 0.0)
    minus_dm = np.where((down > up) & (down > 0), down, 0.0)
    true_range = np.maximum(high[1:] - low[1:],
                            np.maximum(np.abs(high[1:] - close[:-1]),
                                       np.abs(low[1:] - close[:-1])))
    atr = _rma_series(true_range, period)
    plus = _rma_series(plus_dm, period)
    minus = _rma_series(minus_dm, period)
    dx = np.zeros(len(atr))
    for at in range(len(atr)):
        if atr[at] <= 0:
            continue
        plus_di = 100.0 * plus[at] / atr[at]
        minus_di = 100.0 * minus[at] / atr[at]
        total = plus_di + minus_di
        if total > 0:
            dx[at] = 100.0 * abs(plus_di - minus_di) / total
    return _rma(dx, period)


class TurtleBreakout:
    """Slot 1. Stateless: every call stands on the frame it is handed."""

    def __init__(self, entry_candles=ENTRY_CANDLES, weeks=WEEKS,
                 week_candles=WEEK_CANDLES, adx_min=ADX_MIN,
                 adx_period=ADX_PERIOD, adx_tail=ADX_TAIL, warmup=WARMUP):
        self.entry_candles = entry_candles
        self.weeks = weeks
        self.week_candles = week_candles
        self.adx_min = adx_min
        self.adx_period = adx_period
        self.adx_tail = adx_tail
        self.warmup = warmup
        self.name = NAME
        self.params = {'entry_candles': entry_candles, 'weeks': weeks,
                       'week_candles': week_candles, 'adx_min': adx_min,
                       'adx_period': adx_period, 'adx_tail': adx_tail,
                       'warmup': warmup, 'kind': 'donchian_breakout'}

    def _breakout(self, df):
        """-> 'long', 'short' or None. This candle is NOT in the channel:
        the 20 candles are the 20 BEFORE it."""
        close = float(df['close'].iloc[-1])
        before = df.iloc[-(self.entry_candles + 1):-1]
        if close > float(before['high'].max()):
            return 'long'
        if close < float(before['low'].min()):
            return 'short'
        return None

    def _weekly_agrees(self, df, side):
        """Is the close on the right side of the 10-week average?"""
        closes = df['close'].values
        weekly = [float(closes[-1 - self.week_candles * k])
                  for k in range(self.weeks)]
        average = sum(weekly) / len(weekly)
        close = float(closes[-1])
        return close > average if side == 'long' else close < average

    def _trending(self, df):
        """Is Wilder's ADX ABOVE the line? At the line is not above it."""
        tail = df.iloc[-self.adx_tail:]
        adx = wilder_adx(tail['high'].values, tail['low'].values,
                         tail['close'].values, self.adx_period)
        return adx > self.adx_min

    def __call__(self, df):
        if len(df) < self.warmup:
            return 'flat'
        side = self._breakout(df)
        if side is None:
            return 'flat'
        if not self._weekly_agrees(df, side):
            return 'flat'
        if not self._trending(df):
            return 'flat'
        return side


if __name__ == '__main__':
    import os
    import sys

    if '--gate' not in sys.argv:
        print(__doc__)
        print('This is a strategy, not a command. Its setup gate is '
              '`--gate`; the one run that counts is lab/gauntlet.py.')
        sys.exit(0)

    # =====================================================================
    # GATE 6.2-S — THE SETUP GATE FOR SLOT 1 ON 4-HOUR CANDLES. Declared in
    # PROGRESS_LOG.md on 2026-11-16 and committed with no `.py`, before this
    # file was changed. It replaces GATE 6.1-S (the daily build, never run).
    #
    # **THIS GATE PROVES THE STRATEGY DOES WHAT ITS RULES SAY, ON CANDLES IT
    # MAKES UP ITSELF AND WHOSE RIGHT ANSWER IS WORKED BY HAND. IT PROVES
    # NOTHING ABOUT WHETHER THE STRATEGY MAKES MONEY AND MUST NOT TRY TO.**
    #
    # **IT NEVER OPENS THE VAULT.** The Lab's door is replaced, for the
    # length of this gate, by one that raises.
    # =====================================================================
    import hashlib

    import pandas as pd

    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, ROOT)
    sys.path.insert(0, os.path.join(ROOT, 'lab'))

    nonlocal_ok = []

    def mark(good, text, detail=''):
        nonlocal_ok.append(bool(good))
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    VAULT_OPENED = []
    import engine as _engine

    def _no_vault(*args, **kwargs):
        VAULT_OPENED.append(args)
        raise RuntimeError('the setup gate must never open the vault')

    _engine.load_vault = _no_vault

    FOUR_HOURS = pd.Timedelta(hours=4)

    def frame(closes, spread=0.5, highs=None, lows=None):
        """Made-up 4-hour candles. The high is the close plus `spread` and
        the low is the close minus it, unless said otherwise; the open is
        the previous close."""
        closes = [float(c) for c in closes]
        index = pd.date_range('2020-01-01', periods=len(closes),
                              freq=FOUR_HOURS)
        highs = [c + spread for c in closes] if highs is None else highs
        lows = [c - spread for c in closes] if lows is None else lows
        opens = [closes[0]] + closes[:-1]
        return pd.DataFrame({'open': opens, 'high': highs, 'low': lows,
                             'close': closes}, index=index)

    def ship_adx(df):
        """THE INDEPENDENT WITNESS: the ADX of the ship's own indicator
        library (pandas_ta), which this file does not use."""
        import pandas_ta as ta
        out = ta.adx(df['high'], df['low'], df['close'], length=14)
        return float(out['ADX_14'].iloc[-1])

    def said(df, maker=None):
        """What the strategy answers - or the name of what it raised. Rule
        (k): a case that raises goes RED and the gate carries on."""
        try:
            return (maker or strategy)(df)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>'

    strategy = TurtleBreakout()

    print("=" * 70)
    print("GATE 6.2-S — SLOT 1 ON 4-HOUR CANDLES, THE SETUP. Made-up candles,")
    print("hand-worked answers. The vault is never opened.")
    print("=" * 70)

    print("\n(a) THE NUMBERS ARE THE ONES DECLARED, typed out here.")
    mark(strategy.params == {'entry_candles': 20, 'weeks': 10,
                             'week_candles': 42, 'adx_min': 25.0,
                             'adx_period': 14, 'adx_tail': 150,
                             'warmup': 379, 'kind': 'donchian_breakout'}
         and strategy.name == 'turtle-4h-20c-10w-adx25'
         and (ENTRY_CANDLES, WEEKS, WEEK_CANDLES, ADX_PERIOD, ADX_MIN,
              ADX_TAIL, WARMUP) == (20, 10, 42, 14, 25.0, 150, 379)
         and WARMUP == 1 + (WEEKS - 1) * WEEK_CANDLES
         and WEEK_CANDLES == 7 * 24 // 4,
         "20-candle channel, 10 weekly closes 42 candles apart, ADX(14) "
         "above 25.0 worked on 150 candles, 379-candle warm-up — every one "
         "equal to a number typed out in this gate AND carried in `params`, "
         "so every one is in the engine's fingerprint; 42 is 7 days of 6 "
         "candles and 379 is 1 + 9 x 42",
         f"{strategy.params}")

    print("\n(b) THE THREE PLAIN CASES, worked by hand.")
    # A STAIRCASE UP: +1 a candle, high = close + 0.5. On the last candle
    # the close c is above the highest earlier high (c - 1 + 0.5). The ten
    # weekly closes are c, c-42 ... c-378: average c - 189, below c. Every
    # candle moves up by 1 and never down, so +DM is 1, -DM is 0, DX is 100
    # and the ADX is exactly 100. -> LONG.
    UP = frame([100 + n for n in range(500)])
    mark(said(UP) == 'long',
         "a steady staircase UP, 500 candles: breakout above the 20-candle "
         "high, above the weekly average, ADX 100 -> LONG", said(UP))
    DOWN = frame([1000 - n for n in range(500)])
    mark(said(DOWN) == 'short',
         "the mirror image, a staircase DOWN -> SHORT", said(DOWN))
    LEVEL = frame([100.0] * 500, spread=0.0)
    mark(said(LEVEL) == 'flat',
         "a price that never moves: no breakout, ADX 0 -> FLAT",
         said(LEVEL))

    print("\n(c) THE BREAKOUT, AT THE EXACT VALUE WHERE IT TURNS OVER.")
    # Staircase to candle 498, close 598, highs up to 598.5. Candle 499:
    BASE = [100 + n for n in range(499)]
    at_high = frame(BASE + [598.5], highs=[c + 0.5 for c in BASE] + [600.0])
    above = frame(BASE + [598.51], highs=[c + 0.5 for c in BASE] + [600.0])
    below = frame(BASE + [598.49], highs=[c + 0.5 for c in BASE] + [600.0])
    mark(said(at_high) == 'flat' and said(above) == 'long'
         and said(below) == 'flat',
         "a close EXACTLY EQUAL to the highest earlier high (598.50) is NOT "
         "a breakout; one cent above is; one cent below is not",
         f"at {said(at_high)}, above {said(above)}, below {said(below)}")
    wick = frame(BASE + [599.0], highs=[c + 0.5 for c in BASE] + [650.0])
    mark(said(wick) == 'long',
         "THIS CANDLE'S OWN HIGH IS NOT IN THE CHANNEL: a close of 599 "
         "under its own wick to 650 is still a breakout over the 20 candles "
         "BEFORE it", said(wick))
    # The channel is 20 candles, not 21 and not 19. One old spike to 900:
    spike21 = [c + 0.5 for c in BASE] + [600.0]
    spike21[499 - 21] = 900.0          # 21 candles before this one: outside
    spike20 = [c + 0.5 for c in BASE] + [600.0]
    spike20[499 - 20] = 900.0          # 20 candles before this one: inside
    SPIKE21 = frame(BASE + [599.0], highs=spike21)
    SPIKE20 = frame(BASE + [599.0], highs=spike20)
    mark(said(SPIKE21) == 'long' and said(SPIKE20) == 'flat',
         "THE CHANNEL IS EXACTLY 20 CANDLES: a spike to 900 twenty-one "
         "candles ago is outside it and does not block the breakout; the "
         "same spike twenty candles ago is inside it and does",
         f"21 back {said(SPIKE21)}, 20 back {said(SPIKE20)}")

    # THE SHORT SIDE, AT ITS OWN EXACT VALUE. (`<=` in place of `<` on
    # the low went GREEN at 37/0 in this gate's own attack: every hand case
    # at the turning point was on the long side.) Staircase down to candle
    # 498, close 502, lows down to 501.5. Candle 499:
    BASE_D = [1000 - n for n in range(499)]
    lows_d = [c - 0.5 for c in BASE_D] + [500.0]
    at_low = frame(BASE_D + [501.5], lows=lows_d)
    under = frame(BASE_D + [501.49], lows=lows_d)
    over = frame(BASE_D + [501.51], lows=lows_d)
    mark(said(at_low) == 'flat' and said(under) == 'short'
         and said(over) == 'flat',
         "AND ON THE SHORT SIDE: a close EXACTLY EQUAL to the lowest earlier "
         "low (501.50) is NOT a breakout; one cent below is; one cent above "
         "is not",
         f"at {said(at_low)}, below {said(under)}, above {said(over)}")

    print("\n(d) THE WEEKLY FILTER, 42 CANDLES TO THE WEEK. A bounce inside a"
          "\n    decline is a breakout over 20 candles and is still BELOW the"
          "\n    10-week average.")
    # 400 candles falling 2 a candle from 1000 to 202, then one candle up.
    # The 20 candles before it closed at 240, 238 ... 202, so their highest
    # high is 240.5. The nine older weekly closes sit 42, 84 ... 378 candles
    # before the bounce: the decline's candle 400 - 42k, which closed at
    # 1000 - 2(400 - 42k) = 200 + 84k -> 284, 368 ... 956. They add up to
    # 9 x 200 + 84 x 45 = 5,580. So for a bounce to X the weekly average is
    # (X + 5,580) / 10, and X is above it only when X is above 620.
    DECLINE = [1000 - 2 * n for n in range(400)]               # ends at 202
    older = [DECLINE[-42 * k] for k in range(1, 10)]
    BOUNCE = frame(DECLINE + [245.0])
    mark(said(BOUNCE) == 'flat'
         and BOUNCE['high'].iloc[-21:-1].max() == 240.5
         and older == [284, 368, 452, 536, 620, 704, 788, 872, 956]
         and sum(older) == 5580 and (245.0 + 5580) / 10 == 582.5
         and ship_adx(BOUNCE) > 25,
         "a bounce to 245 after a long decline: above the 20-candle high of "
         "240.5, the ship's own ADX well above 25 — and FLAT, because 245 "
         "is below the 10-week average of 582.5, worked by hand",
         f"signal {said(BOUNCE)}, the nine older weekly closes {older}, "
         f"ship ADX {ship_adx(BOUNCE):.1f}")
    # ONE CANDLE EITHER WAY IN THE WEEK CHANGES THE ANSWER, so the 42 is
    # pinned from both sides. With the weekly closes 41 candles apart the
    # nine older ones are 200 + 82k and add up to 5,490: the line is 610.
    # With 43 apart they are 200 + 86k, 5,670: the line is 630. With 42 it
    # is 620. A bounce to 615 is therefore FLAT at 42 and LONG at 41; a
    # bounce to 625 is LONG at 42 and FLAT at 43.
    NEAR_BELOW = frame(DECLINE + [615.0])
    NEAR_ABOVE = frame(DECLINE + [625.0])
    mark(said(NEAR_BELOW) == 'flat' and said(NEAR_ABOVE) == 'long'
         and (615.0 + 5580) / 10 == 619.5 and (625.0 + 5580) / 10 == 620.5
         and ship_adx(NEAR_BELOW) > 25,
         "the same decline with the bounce carried to 615 is FLAT (average "
         "619.5) and to 625 is LONG (average 620.5): the filter turns on "
         "the average, and on a week of EXACTLY 42 candles — at 41 the "
         "first would be long, at 43 the second would be flat",
         f"615 -> {said(NEAR_BELOW)}, 625 -> {said(NEAR_ABOVE)}")
    AT_AVERAGE = frame(DECLINE + [620.0])
    mark(said(AT_AVERAGE) == 'flat' and (620.0 + 5580) / 10 == 620.0,
         "a close EXACTLY AT the weekly average (620.0 against 620.0) is "
         "not above it -> FLAT", said(AT_AVERAGE))

    # THE SHORT SIDE OF THE WEEKLY FILTER, the mirror image about 601:
    # 400 candles RISING 2 a candle from 202 to 1000, then one candle down
    # to Y. The nine older weekly closes are 1202 - (200 + 84k) and add up
    # to 9 x 1202 - 5,580 = 5,238, so the average is (Y + 5,238) / 10 and Y
    # is below it only when Y is below 582.
    RISE = [202 + 2 * n for n in range(400)]                   # ends at 1000
    older_up = [RISE[-42 * k] for k in range(1, 10)]
    DROP_AT = frame(RISE + [582.0])
    DROP_UNDER = frame(RISE + [577.0])
    mark(said(DROP_AT) == 'flat' and said(DROP_UNDER) == 'short'
         and sum(older_up) == 5238 and (582.0 + 5238) / 10 == 582.0
         and (577.0 + 5238) / 10 == 581.5
         and DROP_AT['low'].iloc[-21:-1].min() == 961.5,
         "AND ON THE SHORT SIDE: after a long rise, a drop to 582 — EXACTLY "
         "AT the weekly average of 582.0 — is FLAT, and a drop to 577 "
         "(average 581.5) is SHORT",
         f"582 -> {said(DROP_AT)}, 577 -> {said(DROP_UNDER)}")

    print("\n(e) THE REGIME FILTER. A market that only wobbles has an ADX"
          "\n    near zero, and a breakout out of it is not taken.")
    # 499 candles alternating 100, 101: every up-move is matched by a
    # down-move, +DI equals -DI, DX is near 0. Then one close at 103:
    # above every earlier high (101.5). The nine older weekly closes are
    # candles 499 - 42k, all odd-numbered, so all 101: the average is
    # (103 + 909) / 10 = 101.2, below 103. Only the ADX stops it.
    WOBBLE = [100.0 + (n % 2) for n in range(499)]
    QUIET_BREAK = frame(WOBBLE + [103.0])
    mark(said(QUIET_BREAK) == 'flat' and ship_adx(QUIET_BREAK) < 25
         and QUIET_BREAK['high'].iloc[-21:-1].max() == 101.5
         and [WOBBLE[499 - 42 * k] for k in range(1, 10)] == [101.0] * 9,
         "a breakout to 103 out of a 100/101 wobble: above the 20-candle "
         "high, above the weekly average of 101.2 — and FLAT, because the "
         "ship's own ADX is far below 25",
         f"signal {said(QUIET_BREAK)}, ship ADX "
         f"{ship_adx(QUIET_BREAK):.1f}")
    # The staircase has an ADX of exactly 100.0 (see (b)).
    mark(said(UP, TurtleBreakout(adx_min=100.0)) == 'flat'
         and said(UP, TurtleBreakout(adx_min=99.999)) == 'long'
         and wilder_adx(UP['high'].values, UP['low'].values,
                        UP['close'].values) == 100.0,
         "ADX EXACTLY AT THE LINE IS NOT ABOVE IT: the staircase's ADX is "
         "exactly 100.0, and a line set AT 100.0 gives FLAT while a line a "
         "thousandth below gives LONG",
         f"ADX {wilder_adx(UP['high'].values, UP['low'].values, UP['close'].values)!r}")

    print("\n(f) THE WARM-UP, AND FRAMES TOO SHORT TO SAY ANYTHING.")
    mark(said(UP.iloc[:378]) == 'flat' and said(UP.iloc[:379]) == 'long',
         "378 candles: FLAT. 379 candles of the same staircase: LONG",
         f"378 -> {said(UP.iloc[:378])}, 379 -> {said(UP.iloc[:379])}")
    SHORT_FRAMES = (0, 1, 2, 5, 21, 64, 150, 151, 300, 377)
    short_answers = [said(UP.iloc[:rows]) for rows in SHORT_FRAMES]
    mark(short_answers == ['flat'] * len(SHORT_FRAMES),
         "frames of 0, 1, 2, 5, 21, 64, 150, 151, 300 and 377 candles are "
         "each FLAT and none raises — INCLUDING THE ONES LONG ENOUGH FOR "
         "THE ADX AND TOO SHORT FOR THE WEEKLY FILTER, where a raise in the "
         "real run would spend the slot on a crash",
         f"{short_answers}")

    print("\n(g) >>> AN INDEPENDENT REFERENCE, ON 4,400 MADE-UP CANDLES. The"
          "\n    rules are written out a second time here, in plain loops,"
          "\n    with the SHIP'S OWN ADX in place of this file's — and the"
          "\n    two must agree on every single candle.")
    rng = np.random.default_rng(61)

    def made_up_market(candles, drift, seed_rng):
        """Random steps gathered into candles, so the highs and lows are
        real ranges and not decoration - AND EVERY CANDLE OPENS WITH A GAP
        from the one before. Without gaps a candle's true range is always
        just its high minus its low, and an ADX that forgot the two gap
        terms went green in the daily gate's own attack."""
        price, rows = 100.0, []
        for _ in range(candles):
            price = price * float(np.exp(seed_rng.normal(0.0, 0.05)))
            steps = price * np.exp(np.cumsum(
                seed_rng.normal(drift / 24, 0.035 / np.sqrt(24), 24)))
            rows.append((price, max(price, steps.max()),
                         min(price, steps.min()), steps[-1]))
            price = float(steps[-1])
        index = pd.date_range('2020-01-01', periods=candles, freq=FOUR_HOURS)
        return pd.DataFrame(rows, columns=['open', 'high', 'low', 'close'],
                            index=index)

    def reference(df):
        """The declared rules, written out again, sharing no code with the
        class above. Every number is typed here."""
        if len(df) < 379:
            return 'flat', None
        c = list(df['close'])
        h = list(df['high'])
        lo = list(df['low'])
        highest = max(h[-21:-1])
        lowest = min(lo[-21:-1])
        side = 'long' if c[-1] > highest else (
            'short' if c[-1] < lowest else None)
        if side is None:
            return 'flat', None
        weekly = sum(c[-1 - 42 * k] for k in range(10)) / 10
        if side == 'long' and not c[-1] > weekly:
            return 'flat', None
        if side == 'short' and not c[-1] < weekly:
            return 'flat', None
        adx = ship_adx(df)
        return (side if adx > 25.0 else 'flat'), adx

    agree, differ, near_line, taken = 0, [], 0, {'long': 0, 'short': 0}
    for drift in (0.0, 0.004, -0.004, 0.0):
        market = made_up_market(1100, drift, rng)
        for at in range(len(market)):
            view = market.iloc[:at + 1]
            want, adx = reference(view)
            got = said(view.copy())
            if adx is not None and abs(adx - 25.0) < 0.05:
                near_line += 1          # too close to call between two
                continue                # ADX codes; counted, not judged
            if want == got:
                agree += 1
                if got != 'flat':
                    taken[got] += 1
            else:
                differ.append((at, want, got))
    mark(not differ and agree + near_line == 4400 and agree >= 4380,
         "on four made-up markets of 1,100 candles each — level, rising, "
         "falling, level — the class and the written-out reference gave "
         "THE SAME ANSWER ON EVERY CANDLE JUDGED",
         f"{agree} candles agreed, {len(differ)} differed, {near_line} set "
         f"aside for an ADX within 0.05 of the line; first differences "
         f"{differ[:3]}")
    mark(taken['long'] >= 5 and taken['short'] >= 5 and near_line <= 10,
         "and that agreement is not an agreement about nothing: both "
         "directions were actually signalled, many times",
         f"{taken['long']} long candles, {taken['short']} short candles")

    print("\n(h) THE ARITHMETIC OF THE ADX, AGAINST THE SHIP'S OWN LIBRARY.")
    worst = 0.0
    for seed in range(5):
        market = made_up_market(400, 0.002 * (seed - 2),
                                np.random.default_rng(700 + seed))
        tail = market.iloc[-150:]
        mine = wilder_adx(tail['high'].values, tail['low'].values,
                          tail['close'].values)
        worst = max(worst, abs(mine - ship_adx(market)))
    mark(worst < 0.05,
         "on five made-up markets this file's ADX, worked on the last 150 "
         "candles, is within 0.05 of the ship's own, worked on all 400",
         f"largest difference {worst:.6f}")

    print("\n(i) LAW 7 — IT CARRIES NOTHING, KEEPS NOTHING, CHANGES NOTHING.")
    from leak_check import leak_check
    from dummies import PerfectForesight
    report = leak_check(strategy, name=strategy.name)
    control = leak_check(PerfectForesight(UP), name='the deliberate leak')
    mark(not report.flagged and control.flagged,
         "the leak scan finds NO data carried by the strategy — and the "
         "SAME scan, in this run, flags the Lab's deliberate leak, so the "
         "scanner is proved awake",
         f"strategy findings {len(report.findings)}, control findings "
         f"{len(control.findings)}")

    def digest(df):
        return hashlib.sha256(
            pd.util.hash_pandas_object(df, index=True).values.tobytes()
        ).hexdigest()

    market = made_up_market(600, 0.003, np.random.default_rng(9))
    before = digest(market)
    first = [said(market.iloc[:at + 1]) for at in range(379, 600)]
    again = [said(market.iloc[:at + 1])
             for at in reversed(range(379, 600))][::-1]
    fresh = [said(market.iloc[:at + 1], TurtleBreakout())
             for at in range(379, 600)]
    mark(digest(market) == before and first == again == fresh
         and len(first) == 221 and set(first) <= {'long', 'short', 'flat'}
         and vars(strategy) == vars(TurtleBreakout()),
         "663 calls left the frame it was handed byte-identical; asking in "
         "reverse order, or asking a brand-new object, gives the same 221 "
         "answers; and the object holds exactly what it held at birth — "
         "IT REMEMBERS NOTHING BETWEEN CALLS")
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        SOURCE = handle.read().split("\nif __name__ == '__main__':")[0]
    # JUDGED ON THE CODE, NOT ON THE PROSE: the file is parsed and every
    # NAME it uses is collected, so a docstring that says "no clock" is not
    # mistaken for a clock.
    import ast
    tree = ast.parse(SOURCE)
    FORBIDDEN = ('open', 'eval', 'exec', '__import__', 'globals', 'locals',
                 'os', 'sys', 'time', 'datetime', 'random', 'requests',
                 'socket', 'urllib', 'pickle', 'subprocess', 'pd', 'pandas')
    names = {node.id for node in ast.walk(tree)
             if isinstance(node, ast.Name)}
    imports = sorted(
        {alias.name for node in ast.walk(tree)
         if isinstance(node, (ast.Import, ast.ImportFrom))
         for alias in node.names})
    statements = {type(node).__name__ for node in ast.walk(tree)}
    mark(imports == ['numpy'] and not names & set(FORBIDDEN)
         and 'Global' not in statements and 'Nonlocal' not in statements
         and not {node.attr for node in ast.walk(tree)
                  if isinstance(node, ast.Attribute)}
         & {'read_csv', 'load_vault', 'read', 'write', 'urlopen', 'now',
            'today', 'environ', 'index'},
         "the strategy's own CODE imports numpy AND NOTHING ELSE, uses none "
         "of eighteen names that open a file, reach a network, read a clock "
         "or run text as code, declares no global, AND NEVER LOOKS AT THE "
         "FRAME'S DATES — it counts candles",
         f"imports: {imports}; {len(names)} names used")

    print("\n(j) >>> THE SABOTAGE DRILL, PERMANENT. Every break is PROVED TO"
          "\n    CHANGE AN ANSWER before its verdict counts. INERT IS A FAIL.")
    CASES = [('staircase up', UP, 'long'), ('staircase down', DOWN, 'short'),
             ('level', LEVEL, 'flat'), ('equal to the high', at_high, 'flat'),
             ('one cent above', above, 'long'), ('own wick', wick, 'long'),
             ('spike 21 back', SPIKE21, 'long'),
             ('spike 20 back', SPIKE20, 'flat'),
             ('bounce to 245, below weekly', BOUNCE, 'flat'),
             ('bounce to 615, just below weekly', NEAR_BELOW, 'flat'),
             ('bounce to 620, AT weekly', AT_AVERAGE, 'flat'),
             ('bounce to 625, just above weekly', NEAR_ABOVE, 'long'),
             ('quiet breakout', QUIET_BREAK, 'flat'),
             ('378 candles', UP.iloc[:378], 'flat'),
             ('equal to the low', at_low, 'flat'),
             ('one cent below the low', under, 'short'),
             ('drop to 582, AT weekly', DROP_AT, 'flat'),
             ('drop to 577, below weekly', DROP_UNDER, 'short')]

    def answers():
        return [said(df) for _name, df, _want in CASES]

    def judged():
        return answers() == [want for _n, _d, want in CASES]

    HONEST = answers()
    _keep = {name: getattr(TurtleBreakout, name) for name in
             ('_breakout', '_weekly_agrees', '_trending', '__call__')}

    def b_today_in_channel(self, df):
        close = float(df['close'].iloc[-1])
        window = df.iloc[-self.entry_candles:]
        if close > float(window['high'].max()):
            return 'long'
        if close < float(window['low'].min()):
            return 'short'
        return None

    def b_not_strict(self, df):
        close = float(df['close'].iloc[-1])
        before_ = df.iloc[-(self.entry_candles + 1):-1]
        if close >= float(before_['high'].max()):
            return 'long'
        if close <= float(before_['low'].min()):
            return 'short'
        return None

    def b_nineteen(self, df):
        close = float(df['close'].iloc[-1])
        before_ = df.iloc[-self.entry_candles:-1]
        if close > float(before_['high'].max()):
            return 'long'
        if close < float(before_['low'].min()):
            return 'short'
        return None

    def b_swapped(self, df):
        side = _keep['_breakout'](self, df)
        return {'long': 'short', 'short': 'long'}.get(side)

    def b_closes_not_highs(self, df):
        close = float(df['close'].iloc[-1])
        before_ = df.iloc[-(self.entry_candles + 1):-1]
        if close > float(before_['close'].max()):
            return 'long'
        if close < float(before_['close'].min()):
            return 'short'
        return None

    def b_no_weekly(self, df, side):
        return True

    def weekly_with(apart, weeks=10, strict=True):
        """The weekly filter written out again with one thing wrong."""
        def broken(self, df, side):
            closes = df['close'].values
            weekly = [float(closes[-1 - apart * k]) for k in range(weeks)]
            close = float(closes[-1])
            average = sum(weekly) / weeks
            if strict:
                return close > average if side == 'long' else close < average
            return close >= average if side == 'long' else close <= average
        return broken

    def b_no_regime(self, df):
        return True

    def b_old_warmup(self, df):
        if len(df) < 150:
            return 'flat'
        side = self._breakout(df)
        if side is None or not self._weekly_agrees(df, side):
            return 'flat'
        return side if self._trending(df) else 'flat'

    BREAKS = [
        ('S1', "this candle counted inside its own channel",
         '_breakout', b_today_in_channel),
        ('S2', 'a close EQUAL to the high counted as a breakout',
         '_breakout', b_not_strict),
        ('S3', 'a 19-candle channel instead of 20', '_breakout', b_nineteen),
        ('S4', 'LONG and SHORT exchanged', '_breakout', b_swapped),
        ('S5', 'the channel built from CLOSES instead of highs and lows',
         '_breakout', b_closes_not_highs),
        ('S6', 'the weekly filter switched off', '_weekly_agrees',
         b_no_weekly),
        ('S7', 'the weekly average over 5 weeks instead of 10',
         '_weekly_agrees', weekly_with(42, weeks=5)),
        ('S8', "a week of 7 candles — the DAILY build's number left in",
         '_weekly_agrees', weekly_with(7)),
        ('S9', 'a week of 41 candles instead of 42', '_weekly_agrees',
         weekly_with(41)),
        ('S10', 'a week of 43 candles instead of 42', '_weekly_agrees',
         weekly_with(43)),
        ('S11', 'a close AT the weekly average counted as above it',
         '_weekly_agrees', weekly_with(42, strict=False)),
        ('S12', 'the regime filter switched off', '_trending', b_no_regime),
        ('S13', "the warm-up left at the DAILY build's 150 candles",
         '__call__', b_old_warmup),
    ]
    print()
    for tag, words, attr, replacement in BREAKS:
        setattr(TurtleBreakout, attr, replacement)
        try:
            broken = answers()
            survived = judged()
        except Exception:                                  # noqa: BLE001
            broken, survived = '<crashed>', False
        finally:
            setattr(TurtleBreakout, attr, _keep[attr])
        changed = broken != HONEST
        good = changed and not survived
        verdict = ('CAUGHT' if good else
                   'INERT — IT CHANGED NOTHING' if not changed else
                   'ESCAPED — THE GATE IS DECORATIVE')
        raised = [a for a in ([broken] if isinstance(broken, str)
                              else broken) if str(a).startswith('<')]
        note = (f"  (it RAISED {raised[0]} on a short frame: in the real "
                f"run that is a slot spent on a crash)" if raised else '')
        mark(good, f"{tag:<3} {words:<56} -> {verdict}{note}")
    mark(all(getattr(TurtleBreakout, name) is original
             for name, original in _keep.items())
         and answers() == HONEST and judged(),
         "and after thirteen breaks every method is the one it started "
         "with and all eighteen hand cases give their hand-worked answers "
         "again")

    print("\n(k) THE VAULT WAS NEVER OPENED, AND THE GATE COUNTS ITSELF.")
    mark(VAULT_OPENED == [],
         "the Lab's door was replaced by one that raises for the whole of "
         "this gate, and nothing knocked on it",
         f"calls: {len(VAULT_OPENED)}")
    mark(len(BREAKS) == 13 and len(CASES) == 18 and len(FORBIDDEN) == 18,
         "thirteen breaks, eighteen hand cases and eighteen forbidden "
         "words, counted against numbers typed out here")
    EXPECTED_CHECKS = 39
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.2-S PASSED — {len(nonlocal_ok)} checks, 0 red.

THE STRATEGY DOES WHAT ITS DECLARED 4-HOUR RULES SAY, on made-up candles
whose answers were worked by hand: the breakout at the exact value where
it turns over ON BOTH SIDES, a channel of exactly twenty candles that leaves this one
out, a weekly filter of exactly 42 candles to the week that blocks a
bounce inside a decline, a regime filter that blocks a breakout out of a
wobble, an ADX exactly at the line counted as not above it, and a
warm-up of 379 candles below which it is flat and never raises.

A SECOND WRITING-OUT OF THE RULES, sharing no code with the first and
using the ship's own ADX, agreed with it on every judged candle of 4,400
made-up candles.

IT CARRIES NO DATA AND REMEMBERS NOTHING. The leak scan is clean and
was proved awake on a deliberate leak in the same run.

WHAT THIS GATE DOES **NOT** PROVE - AND MUST NOT BE READ AS PROVING.
It says NOTHING about whether this strategy makes money. It has never
seen a real candle. It does not judge the CHOICES - twenty candles
rather than twenty days, the weekly filter kept weekly, the ADX alone
rather than the ship's full vane - which were made by the same author
and read by no second AI. And a clean leak scan is not innocence: Law
7's verdict is the reading of the code, recorded in PROGRESS_LOG.md.""")
    else:
        print(f"GATE 6.2-S FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
