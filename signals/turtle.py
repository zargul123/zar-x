"""
Zar X signals compartment — GAUNTLET SLOT 1: the Turtle/Donchian breakout.

**THIS IS ONE OF THE THREE SEALED SLOTS OF THE PROMISE.** Its rules and every
number in it were declared in PROGRESS_LOG.md on 2026-11-15 and committed
with no code, before this file existed. **NOT ONE NUMBER HERE WAS SEARCHED,
TUNED OR TRIED AGAINST ANY RESULT, AND NONE MAY BE CHANGED:** a change is a
different strategy, and the slot is spent on this one.

THE RULES, asked at the close of a daily candle, using only candles up to
and including that one:

    BREAKOUT  long  if today's close is ABOVE the highest high of the 20
                    days BEFORE today (today itself not included);
              short if today's close is BELOW the lowest low of those same
                    20 days. Strictly. Equal is not a breakout.
    WEEKLY    long only if today's close is ABOVE the average of the last
              10 weekly closes (today, 7 days ago, ... 63 days ago);
              short only if BELOW.
    REGIME    only if Wilder's ADX(14) is ABOVE 25.
    WARM-UP   flat until 150 candles exist.

**WHAT THIS FILE DOES NOT DECIDE.** The exit. The Lab's engine manages every
open trade with the ship's own stop (1.5 ATR) and target (2.0 ATR); this
strategy is only ever asked when no trade is open. So this is a Turtle
ENTRY, not the Turtles' whole system, and the bar says so in bold.

**LAW 7.** It carries no data. It reads nothing but the frame it is handed:
no file, no network, no clock, no module global that changes. It keeps
nothing between calls. `lab/leak_check.py` scans it, and its code is short
on purpose so that a person can read all of it.

The contract (lab/engine.py):  signal(df) -> 'long' | 'short' | 'flat'

Standalone use:
    python signals/turtle.py --gate     (the setup gate; never opens the vault)
"""
import numpy as np

ENTRY_DAYS = 20        # the Turtles' published System 1 entry channel
WEEKS = 10             # the weekly trend line: 10 weekly closes
DAYS_PER_WEEK = 7      # crypto trades every day
ADX_PERIOD = 14        # Wilder
ADX_MIN = 25.0         # Wilder; also config's adx_trending_threshold
WARMUP = 150           # candles needed before the first signal
NAME = 'turtle-20d-10w-adx25'


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

    def __init__(self, entry_days=ENTRY_DAYS, weeks=WEEKS, adx_min=ADX_MIN,
                 adx_period=ADX_PERIOD, warmup=WARMUP):
        self.entry_days = entry_days
        self.weeks = weeks
        self.adx_min = adx_min
        self.adx_period = adx_period
        self.warmup = warmup
        self.name = NAME
        self.params = {'entry_days': entry_days, 'weeks': weeks,
                       'adx_min': adx_min, 'adx_period': adx_period,
                       'warmup': warmup, 'kind': 'donchian_breakout'}

    def _breakout(self, df):
        """-> 'long', 'short' or None. Today's own candle is NOT in the
        channel: the 20 days are the 20 BEFORE today."""
        close = float(df['close'].iloc[-1])
        before = df.iloc[-(self.entry_days + 1):-1]
        if close > float(before['high'].max()):
            return 'long'
        if close < float(before['low'].min()):
            return 'short'
        return None

    def _weekly_agrees(self, df, side):
        """Is today's close on the right side of the 10-week average?"""
        closes = df['close'].values
        weekly = [float(closes[-1 - DAYS_PER_WEEK * k])
                  for k in range(self.weeks)]
        average = sum(weekly) / len(weekly)
        close = float(closes[-1])
        return close > average if side == 'long' else close < average

    def _trending(self, df):
        """Is Wilder's ADX ABOVE the line? At the line is not above it."""
        tail = df.iloc[-self.warmup:]
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
    # GATE 6.1-S — THE SETUP GATE FOR SLOT 1. Declared in PROGRESS_LOG.md on
    # 2026-11-15 and committed with no `.py`, before this file existed.
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

    def frame(closes, spread=0.5, highs=None, lows=None):
        """Made-up daily candles. The high is the close plus `spread` and
        the low is the close minus it, unless said otherwise; the open is
        the previous close."""
        closes = [float(c) for c in closes]
        index = pd.date_range('2020-01-01', periods=len(closes), freq='D')
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

    strategy = TurtleBreakout()

    print("=" * 70)
    print("GATE 6.1-S — SLOT 1, THE SETUP. Made-up candles, hand-worked")
    print("answers. The vault is never opened.")
    print("=" * 70)

    print("\n(a) THE NUMBERS ARE THE ONES DECLARED, typed out here.")
    mark(strategy.params == {'entry_days': 20, 'weeks': 10, 'adx_min': 25.0,
                             'adx_period': 14, 'warmup': 150,
                             'kind': 'donchian_breakout'}
         and strategy.name == 'turtle-20d-10w-adx25'
         and (ENTRY_DAYS, WEEKS, DAYS_PER_WEEK, ADX_PERIOD, ADX_MIN,
              WARMUP) == (20, 10, 7, 14, 25.0, 150),
         "20-day channel, 10 weekly closes 7 days apart, ADX(14) above "
         "25.0, 150-candle warm-up — every one equal to a number typed out "
         "in this gate",
         f"{strategy.params}")

    print("\n(b) THE THREE PLAIN CASES, worked by hand.")
    # A STAIRCASE UP: +1 a day, high = close + 0.5. On the last day the
    # close c is above the highest earlier high (c - 1 + 0.5). The ten
    # weekly closes are c, c-7 ... c-63: average c - 31.5, below c. Every
    # day moves up by 1 and never down, so +DM is 1, -DM is 0, DX is 100
    # and the ADX is exactly 100. -> LONG.
    UP = frame([100 + day for day in range(200)])
    mark(strategy(UP) == 'long',
         "a steady staircase UP, 200 days: breakout above the 20-day high, "
         "above the weekly average, ADX 100 -> LONG", strategy(UP))
    DOWN = frame([400 - day for day in range(200)])
    mark(strategy(DOWN) == 'short',
         "the mirror image, a staircase DOWN -> SHORT", strategy(DOWN))
    LEVEL = frame([100.0] * 200, spread=0.0)
    mark(strategy(LEVEL) == 'flat',
         "a price that never moves: no breakout, ADX 0 -> FLAT",
         strategy(LEVEL))

    print("\n(c) THE BREAKOUT, AT THE EXACT VALUE WHERE IT TURNS OVER.")
    # Staircase to day 198, close 298, highs up to 298.5. Day 199's close:
    BASE = [100 + day for day in range(199)]
    at_high = frame(BASE + [298.5], highs=[c + 0.5 for c in BASE] + [300.0])
    above = frame(BASE + [298.51], highs=[c + 0.5 for c in BASE] + [300.0])
    below = frame(BASE + [298.49], highs=[c + 0.5 for c in BASE] + [300.0])
    mark(strategy(at_high) == 'flat' and strategy(above) == 'long'
         and strategy(below) == 'flat',
         "a close EXACTLY EQUAL to the highest earlier high (298.50) is NOT "
         "a breakout; one cent above is; one cent below is not",
         f"at {strategy(at_high)}, above {strategy(above)}, "
         f"below {strategy(below)}")
    wick = frame(BASE + [299.0], highs=[c + 0.5 for c in BASE] + [350.0])
    mark(strategy(wick) == 'long',
         "TODAY'S OWN HIGH IS NOT IN THE CHANNEL: a close of 299 under its "
         "own wick to 350 is still a breakout over the 20 days BEFORE it",
         strategy(wick))
    # The channel is 20 days, not 21 and not 19. One old spike to 500:
    spike21 = [c + 0.5 for c in BASE] + [300.0]
    spike21[199 - 21] = 500.0          # 21 days before today: outside
    spike20 = [c + 0.5 for c in BASE] + [300.0]
    spike20[199 - 20] = 500.0          # 20 days before today: inside
    mark(strategy(frame(BASE + [299.0], highs=spike21)) == 'long'
         and strategy(frame(BASE + [299.0], highs=spike20)) == 'flat',
         "THE CHANNEL IS EXACTLY 20 DAYS: a spike to 500 twenty-one days "
         "ago is outside it and does not block the breakout; the same spike "
         "twenty days ago is inside it and does",
         f"21 days back {strategy(frame(BASE + [299.0], highs=spike21))}, "
         f"20 days back {strategy(frame(BASE + [299.0], highs=spike20))}")

    print("\n(d) THE WEEKLY FILTER. A bounce inside a decline is a breakout"
          "\n    over 20 days and is still BELOW the 10-week average.")
    # 180 days falling 2 a day from 400 to 42, then one day up to 85. The
    # 20 days before it closed at 80, 78 ... 42, so their highest high is
    # 80.5 and 85 breaks out. (THE FIRST DRAFT OF THIS GATE SAID 82.5 - a
    # slip of one day in my own hand arithmetic, caught by this check
    # going red on its first run. The strategy was right; I was not.) The
    # weekly closes are 85 and then 54, 68 ... 166 (42 + 2k for k = 7..63
    # days back counted from the day before): their average is far above
    # 85. -> FLAT, because of the weekly filter and nothing else.
    DECLINE = [400 - 2 * day for day in range(180)]            # ends at 42
    BOUNCE = frame(DECLINE + [85.0])
    weekly_by_hand = [85.0] + [DECLINE[-1 - (7 * k - 1)] for k in range(1, 10)]
    mark(strategy(BOUNCE) == 'flat'
         and BOUNCE['high'].iloc[-21:-1].max() == 80.5
         and 85.0 < sum(weekly_by_hand) / 10 and ship_adx(BOUNCE) > 25,
         "a bounce to 85 after a long decline: above the 20-day high of "
         "80.5, the ship's own ADX well above 25 — and FLAT, because 85 is "
         "below the 10-week average",
         f"signal {strategy(BOUNCE)}, weekly average by hand "
         f"{sum(weekly_by_hand) / 10:.1f}, ship ADX {ship_adx(BOUNCE):.1f}")
    # The same shape with the bounce carried ABOVE the weekly average.
    HIGH_BOUNCE = frame(DECLINE + [140.0])
    weekly_high = [140.0] + weekly_by_hand[1:]
    mark(strategy(HIGH_BOUNCE) == 'long' and 140.0 > sum(weekly_high) / 10,
         "and the same decline with the bounce carried to 140 — above the "
         "weekly average by hand — is LONG: the filter turns on the "
         "average, not on the decline",
         f"signal {strategy(HIGH_BOUNCE)}, weekly average by hand "
         f"{sum(weekly_high) / 10:.1f}")

    print("\n(e) THE REGIME FILTER. A market that only wobbles has an ADX"
          "\n    near zero, and a breakout out of it is not taken.")
    # 199 days alternating 100, 101: every up-move is matched by a
    # down-move, +DI equals -DI, DX is near 0. Then one close at 103:
    # above every earlier high (101.5) and above the weekly average.
    WOBBLE = [100.0 + (day % 2) for day in range(199)]
    QUIET_BREAK = frame(WOBBLE + [103.0])
    mark(strategy(QUIET_BREAK) == 'flat' and ship_adx(QUIET_BREAK) < 25
         and QUIET_BREAK['high'].iloc[-21:-1].max() == 101.5,
         "a breakout to 103 out of a 100/101 wobble: above the 20-day high, "
         "above the weekly average — and FLAT, because the ship's own ADX "
         "is far below 25",
         f"signal {strategy(QUIET_BREAK)}, ship ADX "
         f"{ship_adx(QUIET_BREAK):.1f}")
    # The staircase has an ADX of exactly 100.0 (see (b)).
    mark(TurtleBreakout(adx_min=100.0)(UP) == 'flat'
         and TurtleBreakout(adx_min=99.999)(UP) == 'long'
         and wilder_adx(UP['high'].values, UP['low'].values,
                        UP['close'].values) == 100.0,
         "ADX EXACTLY AT THE LINE IS NOT ABOVE IT: the staircase's ADX is "
         "exactly 100.0, and a line set AT 100.0 gives FLAT while a line a "
         "thousandth below gives LONG",
         f"ADX {wilder_adx(UP['high'].values, UP['low'].values, UP['close'].values)!r}")

    print("\n(f) THE WARM-UP, AND FRAMES TOO SHORT TO SAY ANYTHING.")
    mark(strategy(UP.iloc[:149]) == 'flat' and strategy(UP.iloc[:150])
         == 'long',
         "149 candles: FLAT. 150 candles of the same staircase: LONG")
    short_ok = True
    for rows in (0, 1, 2, 5, 21, 64):
        try:
            short_ok = short_ok and strategy(UP.iloc[:rows]) == 'flat'
        except Exception:                                  # noqa: BLE001
            short_ok = False
    mark(short_ok, "frames of 0, 1, 2, 5, 21 and 64 candles are each FLAT "
                   "and none raises")

    print("\n(g) >>> AN INDEPENDENT REFERENCE, ON 2,000 MADE-UP DAYS. The"
          "\n    rules are written out a second time here, in plain loops,"
          "\n    with the SHIP'S OWN ADX in place of this file's — and the"
          "\n    two must agree on every single day.")
    rng = np.random.default_rng(61)

    def made_up_market(days, drift, seed_rng):
        """Hourly random steps gathered into daily candles, so the highs
        and lows are real ranges and not decoration - AND EVERY DAY OPENS
        WITH A GAP from the day before. Without gaps a day's true range is
        always just its high minus its low, and an ADX that forgot the two
        gap terms went green at 32/0 in this gate's own attack."""
        price, rows = 100.0, []
        for _ in range(days):
            price = price * float(np.exp(seed_rng.normal(0.0, 0.05)))
            steps = price * np.exp(np.cumsum(
                seed_rng.normal(drift / 24, 0.035 / np.sqrt(24), 24)))
            rows.append((price, max(price, steps.max()),
                         min(price, steps.min()), steps[-1]))
            price = float(steps[-1])
        index = pd.date_range('2020-01-01', periods=days, freq='D')
        return pd.DataFrame(rows, columns=['open', 'high', 'low', 'close'],
                            index=index)

    def reference(df):
        """The declared rules, written out again, sharing no code with the
        class above."""
        if len(df) < 150:
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
        weekly = sum(c[-1 - 7 * k] for k in range(10)) / 10
        if side == 'long' and not c[-1] > weekly:
            return 'flat', None
        if side == 'short' and not c[-1] < weekly:
            return 'flat', None
        adx = ship_adx(df)
        return (side if adx > 25.0 else 'flat'), adx

    agree, differ, near_line, taken = 0, [], 0, {'long': 0, 'short': 0}
    for drift in (0.0, 0.004, -0.004, 0.0):
        market = made_up_market(500, drift, rng)
        for day in range(len(market)):
            view = market.iloc[:day + 1]
            want, adx = reference(view)
            got = strategy(view.copy())
            if adx is not None and abs(adx - 25.0) < 0.05:
                near_line += 1          # too close to call between two
                continue                # ADX codes; counted, not judged
            if want == got:
                agree += 1
                if got != 'flat':
                    taken[got] += 1
            else:
                differ.append((day, want, got))
    mark(not differ and agree >= 1990,
         "on four made-up markets of 500 days each — level, rising, "
         "falling, level — the class and the written-out reference gave "
         "THE SAME ANSWER ON EVERY DAY JUDGED",
         f"{agree} days agreed, {len(differ)} differed, {near_line} set "
         f"aside for an ADX within 0.05 of the line; first differences "
         f"{differ[:3]}")
    mark(taken['long'] >= 5 and taken['short'] >= 5 and near_line <= 5,
         "and that agreement is not an agreement about nothing: both "
         "directions were actually signalled, many times",
         f"{taken['long']} long days, {taken['short']} short days")

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

    market = made_up_market(300, 0.003, np.random.default_rng(9))
    before = digest(market)
    first = [strategy(market.iloc[:day + 1]) for day in range(150, 300)]
    again = [strategy(market.iloc[:day + 1])
             for day in reversed(range(150, 300))][::-1]
    fresh = [TurtleBreakout()(market.iloc[:day + 1])
             for day in range(150, 300)]
    mark(digest(market) == before and first == again == fresh
         and vars(strategy) == vars(TurtleBreakout()),
         "450 calls left the frame it was handed byte-identical; asking in "
         "reverse order, or asking a brand-new object, gives the same 150 "
         "answers; and the object holds exactly what it held at birth — "
         "IT REMEMBERS NOTHING BETWEEN CALLS")
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        SOURCE = handle.read().split("\nif __name__ == '__main__':")[0]
    # JUDGED ON THE CODE, NOT ON THE PROSE: the file is parsed and every
    # NAME it uses is collected, so a docstring that says "no clock" is not
    # mistaken for a clock. (The first draft searched the raw text and went
    # red on its own description of what it forbids.)
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
            'today', 'environ'},
         "the strategy's own CODE imports numpy AND NOTHING ELSE, uses none "
         "of eighteen names that open a file, reach a network, read a clock "
         "or run text as code, and declares no global",
         f"imports: {imports}; {len(names)} names used")

    print("\n(j) >>> THE SABOTAGE DRILL, PERMANENT. Every break is PROVED TO"
          "\n    CHANGE AN ANSWER before its verdict counts. INERT IS A FAIL.")
    CASES = [('staircase up', UP, 'long'), ('staircase down', DOWN, 'short'),
             ('level', LEVEL, 'flat'), ('equal to the high', at_high, 'flat'),
             ('one cent above', above, 'long'), ('own wick', wick, 'long'),
             ('spike 21 back', frame(BASE + [299.0], highs=spike21), 'long'),
             ('spike 20 back', frame(BASE + [299.0], highs=spike20), 'flat'),
             ('bounce below weekly', BOUNCE, 'flat'),
             ('bounce above weekly', HIGH_BOUNCE, 'long'),
             ('quiet breakout', QUIET_BREAK, 'flat'),
             ('149 candles', UP.iloc[:149], 'flat')]

    def answers():
        return [strategy(df) for _name, df, _want in CASES]

    def judged():
        return answers() == [want for _n, _d, want in CASES]

    HONEST = answers()
    _keep = {name: getattr(TurtleBreakout, name) for name in
             ('_breakout', '_weekly_agrees', '_trending', '__call__')}

    def b_today_in_channel(self, df):
        close = float(df['close'].iloc[-1])
        window = df.iloc[-self.entry_days:]
        if close > float(window['high'].max()):
            return 'long'
        if close < float(window['low'].min()):
            return 'short'
        return None

    def b_not_strict(self, df):
        close = float(df['close'].iloc[-1])
        before_ = df.iloc[-(self.entry_days + 1):-1]
        if close >= float(before_['high'].max()):
            return 'long'
        if close <= float(before_['low'].min()):
            return 'short'
        return None

    def b_nineteen(self, df):
        close = float(df['close'].iloc[-1])
        before_ = df.iloc[-self.entry_days:-1]
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
        before_ = df.iloc[-(self.entry_days + 1):-1]
        if close > float(before_['close'].max()):
            return 'long'
        if close < float(before_['close'].min()):
            return 'short'
        return None

    def b_no_weekly(self, df, side):
        return True

    def b_weekly_five(self, df, side):
        closes = df['close'].values
        weekly = [float(closes[-1 - 7 * k]) for k in range(5)]
        close = float(closes[-1])
        average = sum(weekly) / 5
        return close > average if side == 'long' else close < average

    def b_no_regime(self, df):
        return True

    def b_no_warmup(self, df):
        if len(df) < 64:
            return 'flat'
        side = self._breakout(df)
        if side is None or not self._weekly_agrees(df, side):
            return 'flat'
        return side if self._trending(df) else 'flat'

    BREAKS = [
        ('S1', "today's own candle counted inside the channel",
         '_breakout', b_today_in_channel),
        ('S2', 'a close EQUAL to the high counted as a breakout',
         '_breakout', b_not_strict),
        ('S3', 'a 19-day channel instead of 20', '_breakout', b_nineteen),
        ('S4', 'LONG and SHORT exchanged', '_breakout', b_swapped),
        ('S5', 'the channel built from CLOSES instead of highs and lows',
         '_breakout', b_closes_not_highs),
        ('S6', 'the weekly filter switched off', '_weekly_agrees',
         b_no_weekly),
        ('S7', 'the weekly average over 5 weeks instead of 10',
         '_weekly_agrees', b_weekly_five),
        ('S8', 'the regime filter switched off', '_trending', b_no_regime),
        ('S9', 'the warm-up cut from 150 candles to 64', '__call__',
         b_no_warmup),
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
        mark(good, f"{tag} {words:<56} -> {verdict}")
    mark(all(getattr(TurtleBreakout, name) is original
             for name, original in _keep.items())
         and answers() == HONEST and judged(),
         "and after nine breaks every method is the one it started with "
         "and all twelve hand cases give their hand-worked answers again")

    print("\n(k) THE VAULT WAS NEVER OPENED, AND THE GATE COUNTS ITSELF.")
    mark(VAULT_OPENED == [],
         "the Lab's door was replaced by one that raises for the whole of "
         "this gate, and nothing knocked on it",
         f"calls: {len(VAULT_OPENED)}")
    mark(len(BREAKS) == 9 and len(CASES) == 12 and len(FORBIDDEN) == 18,
         "nine breaks, twelve hand cases and eighteen forbidden words, "
         "counted against numbers typed out here")
    EXPECTED_CHECKS = 32
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.1-S PASSED — {len(nonlocal_ok)} checks, 0 red.

THE STRATEGY DOES WHAT ITS DECLARED RULES SAY, on made-up candles whose
answers were worked by hand: the breakout at the exact value where it
turns over, a channel of exactly twenty days that leaves today out, a
weekly filter that blocks a bounce inside a decline, a regime filter
that blocks a breakout out of a wobble, and an ADX exactly at the line
counted as not above it.

A SECOND WRITING-OUT OF THE RULES, sharing no code with the first and
using the ship's own ADX, agreed with it on every day of 2,000 made-up
days.

IT CARRIES NO DATA AND REMEMBERS NOTHING. The leak scan is clean and
was proved awake on a deliberate leak in the same run.

WHAT THIS GATE DOES **NOT** PROVE - AND MUST NOT BE READ AS PROVING.
It says NOTHING about whether this strategy makes money. It has never
seen a real candle. And a clean leak scan is not innocence: Law 7's
verdict is the reading of the code, recorded in PROGRESS_LOG.md.""")
    else:
        print(f"GATE 6.1-S FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
