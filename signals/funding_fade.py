"""
Zar X signals compartment — GAUNTLET SLOT 2: the funding-rate extreme fade,
ON DAILY CANDLES.

**THIS IS ONE OF THE THREE SEALED SLOTS OF THE PROMISE.** Its rules were
declared in PROGRESS_LOG.md on 2026-11-16 (evening) and committed with no
code, before this file existed. **NOT ONE NUMBER HERE WAS SEARCHED, TUNED OR
TRIED AGAINST ANY RESULT, AND NONE MAY BE CHANGED:** a change is a different
strategy, and the slot is spent on this one.

THE IDEA, in a trader's words: when the funding rate on the perpetual is
extremely positive, longs are crowded and paying heavily - fade them
(short). Extremely negative - the reverse.

THE RULES, asked at the close of a daily candle, using only candles up to
and including that one. Each candle carries one extra figure, `funding`:
the three funding rates Binance settled inside that UTC day (00:00, 08:00,
16:00) added up, as a whole number of hundred-millionths.

    EXTREMELY POSITIVE   today's funding is ABOVE ZERO and strictly above
                         AT LEAST 81 OF THE PREVIOUS 90 DAYS'  ->  SHORT
    EXTREMELY NEGATIVE   today's funding is BELOW ZERO and strictly below
                         AT LEAST 81 OF THE PREVIOUS 90 DAYS'  ->  LONG
    WARM-UP              flat until 91 candles exist (today + 90)
    Otherwise flat. A day EQUAL to another is neither above nor below it.

**"EXTREME" IS A RANK, NOT A RATE.** No funding rate is typed into this
file. What counts as extreme is the top (or bottom) tenth of the coin's own
last 90 days, so there is no threshold that could have been fitted to
anything. 90 and 81 are round figures - a quarter, nine in ten - chosen
before any count and filed against their author.

**WHAT THIS FILE DOES NOT DECIDE.** The exit. The Lab's engine manages every
open trade with the ship's own stop (1.5 ATR) and target (2.0 ATR), enters
at the NEXT day's open, and asks this strategy only when no trade is open.

**LAW 7.** It carries no data: three whole numbers and a name. The funding
reaches it INSIDE the frame the engine hands it, one figure a candle, so the
engine's own wall (`df.iloc[:i+1]`) keeps tomorrow's funding out exactly as
it keeps tomorrow's price out. It reads no file, no network, no clock, and
never looks at the frame's dates or prices. It keeps nothing between calls.
**A frame with no `funding` column RAISES**: it must never quietly answer
"flat" a thousand times and hand back a false obituary.

The contract (lab/engine.py):  signal(df) -> 'long' | 'short' | 'flat'

Standalone use:
    python signals/funding_fade.py --gate   (the setup gate; opens no vault)
"""
import numpy as np

WINDOW = 90            # the days today is ranked against: a quarter
NEED = 81              # strictly above (below) at least this many: nine in ten
WARMUP = 91            # today + 90: the fewest candles that can answer
COLUMN = 'funding'     # the day's funding, joined on by the runner
NAME = 'funding-fade-1d-90d-top10'
NO_COLUMN = ('REFUSED: this frame has no `funding` column. The fade cannot '
             'be judged without funding, and it must not answer "flat".')


class FundingFade:
    """Slot 2. Stateless: every call stands on the frame it is handed."""

    def __init__(self, window=WINDOW, need=NEED, warmup=WARMUP):
        self.window = window
        self.need = need
        self.warmup = warmup
        self.name = NAME
        self.params = {'window': window, 'need': need, 'warmup': warmup,
                       'column': COLUMN, 'kind': 'funding_extreme_fade'}

    def __call__(self, df):
        if COLUMN not in df.columns:
            raise ValueError(NO_COLUMN)
        if len(df) < self.warmup:
            return 'flat'
        tail = np.asarray(df[COLUMN].values[-(self.window + 1):], dtype=float)
        if np.isnan(tail).any():
            return 'flat'
        today = tail[-1]
        before = tail[:-1]
        if today > 0 and int(np.sum(before < today)) >= self.need:
            return 'short'
        if today < 0 and int(np.sum(before > today)) >= self.need:
            return 'long'
        return 'flat'


if __name__ == '__main__':
    import os
    import sys

    if '--gate' not in sys.argv:
        print(__doc__)
        print('This is a strategy, not a command. Its setup gate is '
              '`--gate`; the one run that counts is lab/gauntlet_slot2.py.')
        sys.exit(0)

    # =====================================================================
    # GATE 6.3-S — THE SETUP GATE FOR SLOT 2. Declared in PROGRESS_LOG.md on
    # 2026-11-16 (evening) and committed with no code, before this file
    # existed.
    #
    # **THIS GATE PROVES THE STRATEGY DOES WHAT ITS RULES SAY, ON FRAMES IT
    # MAKES UP ITSELF AND WHOSE RIGHT ANSWER IS WORKED BY HAND. IT PROVES
    # NOTHING ABOUT WHETHER THE STRATEGY MAKES MONEY AND MUST NOT TRY TO.**
    #
    # **IT NEVER OPENS THE VAULT OR THE FROZEN FUNDING.**
    # =====================================================================
    import ast
    import re

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

    NAN = float('nan')

    def frame(funding, base=100.0, swing=1.0, with_column=True):
        """Made-up daily candles carrying a made-up funding figure each."""
        funding = [float(value) for value in funding]
        index = pd.date_range('2030-01-01', periods=len(funding), freq='1D')
        closes = [base + swing * ((n * 7) % 13) for n in range(len(funding))]
        data = {'open': closes, 'high': [c + swing for c in closes],
                'low': [c - swing for c in closes], 'close': closes}
        if with_column:
            data['funding'] = funding
        return pd.DataFrame(data, index=index)

    def said(df, maker=None):
        """What the strategy answers - or the name of what it raised. Rule
        (k): a case that raises goes RED and the gate carries on."""
        try:
            return (maker or strategy)(df)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>'

    strategy = FundingFade()

    print("=" * 70)
    print("GATE 6.3-S — SLOT 2, THE FUNDING FADE, THE SETUP. Made-up frames,")
    print("hand-worked answers. No vault and no frozen funding is opened.")
    print("=" * 70)

    print("\n(a) THE NUMBERS ARE THE ONES DECLARED, typed out here.")
    mark(strategy.params == {'window': 90, 'need': 81, 'warmup': 91,
                             'column': 'funding',
                             'kind': 'funding_extreme_fade'}
         and strategy.name == 'funding-fade-1d-90d-top10'
         and (WINDOW, NEED, WARMUP, COLUMN) == (90, 81, 91, 'funding')
         and WARMUP == WINDOW + 1 and 10 * NEED == 9 * WINDOW
         and sorted(vars(strategy)) == ['name', 'need', 'params', 'warmup',
                                        'window'],
         "today ranked against the 90 days before it, strictly above (or "
         "below) at least 81 of them, a 91-candle warm-up — every one equal "
         "to a number typed out in this gate AND carried in `params`, so "
         "every one is in the engine's fingerprint; 91 is 90 + 1 and 81 is "
         "nine tenths of 90; and the object holds nothing else",
         f"{strategy.params}")

    other = FundingFade(window=60, need=54, warmup=61)
    mark(other.params == {'window': 60, 'need': 54, 'warmup': 61,
                          'column': 'funding',
                          'kind': 'funding_extreme_fade'}
         and (other.window, other.need, other.warmup) == (60, 54, 61),
         "and `params` carries THE NUMBERS THE OBJECT ACTUALLY USES: one "
         "built with 60, 54 and 61 says 60, 54 and 61 — so a strategy "
         "built differently cannot wear the declared fingerprint. "
         "(`params` quoting the module's constants went GREEN at 43/0 in "
         "this gate's own attack.)", f"{other.params}")

    print("\n(b) THE THREE PLAIN CASES, worked by hand.")
    # Funding in whole hundred-millionths. 3,000 is +0.0100% three times.
    HIGH = frame([3000] * 90 + [9000])
    LOW = frame([-3000] * 90 + [-9000])
    SAME = frame([3000] * 91)
    mark(said(HIGH) == 'short',
         "ninety quiet days at 3,000 and then a day at 9,000: positive, and "
         "above all 90 -> the longs are crowded -> SHORT", said(HIGH))
    mark(said(LOW) == 'long',
         "the mirror image, ninety days at -3,000 then -9,000: negative, "
         "and below all 90 -> LONG", said(LOW))
    mark(said(SAME) == 'flat',
         "ninety-one days all exactly 3,000: today is above NONE of them -> "
         "FLAT", said(SAME))

    print("\n(c) THE RANK, AT THE EXACT NUMBER WHERE IT TURNS OVER — ON BOTH"
          "\n    SIDES (rule (o)).")
    # Today 5,000. The 90 before: `below` of them at 1,000, the rest 9,000.
    def high_case(below, rest=9000, today=5000):
        return frame([1000] * below + [rest] * (90 - below) + [today])

    def low_case(above, rest=-9000, today=-5000):
        return frame([-1000] * above + [rest] * (90 - above) + [today])

    mark(said(high_case(80)) == 'flat' and said(high_case(81)) == 'short'
         and said(high_case(82)) == 'short',
         "ABOVE EXACTLY 80 of the 90 is FLAT; above 81 is SHORT; above 82 "
         "is SHORT",
         f"80 {said(high_case(80))}, 81 {said(high_case(81))}, "
         f"82 {said(high_case(82))}")
    mark(said(low_case(80)) == 'flat' and said(low_case(81)) == 'long'
         and said(low_case(82)) == 'long',
         "THE SHORT SIDE'S MIRROR: BELOW EXACTLY 80 of the 90 is FLAT; "
         "below 81 is LONG; below 82 is LONG",
         f"80 {said(low_case(80))}, 81 {said(low_case(81))}, "
         f"82 {said(low_case(82))}")
    # EQUAL IS NOT ABOVE. 80 below and the other ten EXACTLY today's value:
    # `<=` in place of `<` would count 90 and answer SHORT.
    mark(said(high_case(80, rest=5000)) == 'flat'
         and said(high_case(81, rest=5000)) == 'short',
         "A DAY EQUAL TO TODAY IS NOT BELOW IT: above 80 and level with the "
         "other ten is FLAT; above 81 and level with nine is SHORT",
         f"{said(high_case(80, rest=5000))}, "
         f"{said(high_case(81, rest=5000))}")
    mark(said(low_case(80, rest=-5000)) == 'flat'
         and said(low_case(81, rest=-5000)) == 'long',
         "and on the other side: below 80 and level with ten is FLAT; below "
         "81 and level with nine is LONG",
         f"{said(low_case(80, rest=-5000))}, "
         f"{said(low_case(81, rest=-5000))}")
    # The order of the 90 must not matter: the same 81/9, shuffled.
    mixed = ([9000] * 4 + [1000] * 40 + [9000] * 5 + [1000] * 41 + [5000])
    mark(said(frame(mixed)) == 'short'
         and said(frame(mixed[:89][::-1] + mixed[89:])) == 'short',
         "the ORDER of the ninety days does not matter: the same 81 below "
         "and 9 above, scattered and then reversed, is still SHORT")

    print("\n(d) THE SIGN: extremely POSITIVE, extremely NEGATIVE.")
    mark(said(frame([-9000] * 90 + [-1000])) == 'flat'
         and said(frame([-9000] * 90 + [0])) == 'flat'
         and said(frame([-9000] * 90 + [1])) == 'short',
         "the HIGHEST funding in 90 days that is still NEGATIVE is FLAT — "
         "shorts are still the ones paying; at ZERO exactly, FLAT; one "
         "hundred-millionth above zero, SHORT",
         f"-1000 {said(frame([-9000] * 90 + [-1000]))}, 0 "
         f"{said(frame([-9000] * 90 + [0]))}, +1 "
         f"{said(frame([-9000] * 90 + [1]))}")
    mark(said(frame([9000] * 90 + [1000])) == 'flat'
         and said(frame([9000] * 90 + [0])) == 'flat'
         and said(frame([9000] * 90 + [-1])) == 'long',
         "the LOWEST funding in 90 days that is still POSITIVE is FLAT — "
         "longs are still the ones paying; at zero, FLAT; one "
         "hundred-millionth below zero, LONG",
         f"+1000 {said(frame([9000] * 90 + [1000]))}, 0 "
         f"{said(frame([9000] * 90 + [0]))}, -1 "
         f"{said(frame([9000] * 90 + [-1]))}")
    mark(said(frame([1000] * 81 + [9000] * 9 + [-5000])) == 'long'
         and said(frame([-1000] * 81 + [-9000] * 9 + [5000])) == 'short',
         "and the two rules do not cross: a negative day below every one of "
         "ninety positive days is LONG, never short; a positive day above "
         "ninety negative ones is SHORT, never long")

    print("\n(e) THE WINDOW IS EXACTLY THE 90 DAYS BEFORE TODAY.")
    # 92 candles. The oldest (91 days before today) is 1,000 - "below" -
    # and must NOT be counted: the 90 after it hold only 80 below.
    NOT_91 = frame([1000] + [1000] * 80 + [9000] * 10 + [5000])
    # 91 candles whose OLDEST day (90 days before today) is the 81st
    # "below": it MUST be counted.
    NOT_89 = frame([1000] + [9000] * 9 + [1000] * 80 + [5000])
    mark(said(NOT_91) == 'flat' and said(NOT_89) == 'short',
         "a quiet day 91 days ago is OUTSIDE the window and does not make "
         "81 (FLAT); a quiet day exactly 90 days ago is INSIDE it and does "
         "(SHORT) — the window is 90, not 91 and not 89",
         f"91 back {said(NOT_91)}, 90 back {said(NOT_89)}")
    # Yesterday's extreme is not today's: yesterday 9,000 above all, today
    # back at 1,000 level with the rest.
    mark(said(frame([1000] * 89 + [9000] + [1000])) == 'flat'
         and said(frame([1000] * 89 + [9000] + [1000]).iloc[:-1]) == 'flat'
         and said(frame([1000] * 90 + [9000] + [1000]).iloc[:-1]) == 'short',
         "TODAY'S funding is the one judged, not yesterday's: a spike "
         "yesterday and a quiet day today is FLAT, and the same frame cut "
         "off at the spike (with 90 days before it) is SHORT")

    print("\n(f) THE WARM-UP, AND FRAMES THAT CANNOT BE JUDGED.")
    NINETY = frame([1000] * 89 + [9000])          # 90 candles: 89 below
    mark(said(NINETY) == 'flat' and said(frame([1000] * 90 + [9000]))
         == 'short',
         "90 candles is FLAT even with today above all 89 before it — 89 is "
         "more than 81, so only the warm-up stops it; 91 candles of the "
         "same shape is SHORT", said(NINETY))
    mark([said(frame([1000] * n + [9000])) for n in (0, 1, 30, 80, 85, 88)]
         == ['flat'] * 6 and said(frame([])) == 'flat',
         "frames of 1, 2, 31, 81, 86 and 89 candles, and an EMPTY frame, "
         "are each FLAT and none of them raises")
    mark(said(frame([NAN] + [1000] * 89 + [9000])) == 'flat'
         and said(frame([1000] * 45 + [NAN] + [1000] * 44 + [9000])) == 'flat'
         and said(frame([1000] * 90 + [NAN])) == 'flat'
         and said(frame([NAN] + [1000] * 90 + [9000])) == 'short',
         "AN EMPTY DAY anywhere in the 91 — the oldest, the middle, today — "
         "is FLAT; an empty day 91 days back, outside the window, changes "
         "nothing (SHORT)")
    bare = frame([1000] * 90 + [9000], with_column=False)
    mark(said(bare) == '<ValueError>'
         and said(bare.iloc[:1]) == '<ValueError>'
         and said(bare.rename(columns={'close': 'Funding'}))
         == '<ValueError>',
         "A FRAME WITH NO `funding` COLUMN RAISES — at the very first "
         "candle, not only after the warm-up — and a column spelt "
         "`Funding` is not it. The fade must never answer 'flat' for want "
         "of funding",
         f"{said(bare)}, one candle {said(bare.iloc[:1])}")

    print("\n(g) THE PRICES DO NOT MATTER; THE FRAME IS NOT TOUCHED; NOTHING"
          "\n    IS REMEMBERED.")
    rng = np.random.default_rng(63)
    walk = np.cumsum(rng.integers(-900, 901, 4600))
    walk = (walk - walk.mean()).round()
    walk[rng.integers(0, 4600, 500)] = 3000.0          # exact ties, often
    walk[rng.integers(0, 4600, 12)] = np.nan           # a few empty days
    LONG_RUN = frame(walk)
    OTHER_PRICES = frame(walk, base=50000.0, swing=777.0)
    answers = [said(LONG_RUN.iloc[:n]) for n in range(1, 4601)]
    other = [said(OTHER_PRICES.iloc[:n]) for n in range(1, 4601)]
    mark(answers == other and LONG_RUN['close'].iloc[5]
         != OTHER_PRICES['close'].iloc[5],
         "4,600 made-up days judged twice, on two sets of candles with "
         "nothing in common but the funding: the same answer on every day")
    before_call = LONG_RUN.copy()
    again = [said(LONG_RUN.iloc[:n]) for n in (4600, 200, 3000, 91, 4600)]
    mark(LONG_RUN.equals(before_call)
         and again == [answers[4599], answers[199], answers[2999],
                       answers[90], answers[4599]]
         and vars(strategy) == vars(FundingFade()),
         "the frame is exactly as it was handed over; asked again out of "
         "order the answers are the same; and the object holds what it "
         "held when it was made")

    print("\n(h) A SECOND WRITING-OUT OF THE RULE, sharing no code with the"
          "\n    first, on the same 4,600 days.")

    def by_hand(values, at):
        """The rule again, in plain Python on a plain list: no numpy, no
        frame, nothing from the strategy above."""
        if at < 90:
            return 'flat'
        today = values[at]
        ninety = values[at - 90:at]
        if today != today or any(v != v for v in ninety):
            return 'flat'
        lower = sum(1 for v in ninety if v < today)
        higher = sum(1 for v in ninety if v > today)
        if today > 0 and 10 * lower >= 9 * 90:
            return 'short'
        if today < 0 and 10 * higher >= 9 * 90:
            return 'long'
        return 'flat'

    plain = [float(v) for v in walk]
    reference = [by_hand(plain, at) for at in range(4600)]
    shorts, longs = reference.count('short'), reference.count('long')
    differ = [at for at in range(4600) if reference[at] != answers[at]]
    mark(not differ and shorts >= 50 and longs >= 50
         and reference.count('flat') >= 1000,
         "the two agree on EVERY ONE of 4,600 days, with both directions "
         "signalled many times and most days flat",
         f"{shorts} short, {longs} long, {reference.count('flat')} flat, "
         f"{len(differ)} disagreements")

    print("\n(i) LAW 7: IT CARRIES NOTHING AND READS NOTHING BUT THE FRAME.")
    from dummies import PerfectForesight
    from leak_check import leak_check
    clean = leak_check(strategy)
    awake = leak_check(PerfectForesight(HIGH))
    mark(not clean.flagged and awake.flagged,
         "the leak scan finds NO carried data on the strategy — and in the "
         "same run the same scan FLAGS the Lab's deliberate leak, so a "
         "clean scan is a scan that was awake",
         f"strategy: {len(clean.findings)} findings; the deliberate leak: "
         f"{len(awake.findings)}")
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        SOURCE = handle.read()
    PRODUCTION = SOURCE.split("if __name__ == '__main__':")[0]
    tree = ast.parse(PRODUCTION)
    imports = sorted({alias.name for node in ast.walk(tree)
                      if isinstance(node, (ast.Import, ast.ImportFrom))
                      for alias in node.names})
    code_only = '\n'.join(line for line in PRODUCTION.split('"""')[2::2])
    stores = [node for node in ast.walk(tree)
              if isinstance(node, ast.Attribute)
              and isinstance(node.ctx, ast.Store)]
    init = next(node for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
                and node.name == '__init__')
    init_stores = [node for node in ast.walk(init)
                   if isinstance(node, ast.Attribute)
                   and isinstance(node.ctx, ast.Store)]
    mark(imports == ['numpy']
         and not any(word in code_only for word in
                     ('open(', '.index', 'iloc', 'datetime', 'time.',
                      'global ', 'os.', 'sys.', 'eval', 'exec', '__import__'))
         and not re.search(r'\b(open|high|low|close|volume)\b', code_only)
         and re.search(r'\bclose\b', "x = df['close'].values")
         and not re.search(r'\blow\b', 'window below')
         and len(stores) == len(init_stores) == 5,
         "the strategy's code imports numpy and nothing else; it names no "
         "file, no clock, no date index and NO PRICE COLUMN; and the only "
         "five things it ever stores on itself are stored when it is made")
    # THE ENGINE'S WALL, WALKED: through the Lab's real engine, a strategy
    # that records what it is handed never sees funding from a later day.
    seen = []

    def recorder(df):
        seen.append((len(df), float(df['funding'].iloc[-1]),
                     float(df['funding'].max())))
        return strategy(df)

    data = _engine.VaultData.__new__(_engine.VaultData)
    data.asset, data.timeframe = 'MADE-UP', '1d'
    data.path, data.report, data.verdict = '<made up>', None, 'PASS'
    rising = [float(n) for n in range(1, 301)]     # each day a new record
    data.df = frame(rising, swing=3.0)
    try:
        walked = _engine.run_backtest(data, recorder, 'wall-check',
                                      verbose=False, regime=False)
        wall = ''
    except Exception as exc:                               # noqa: BLE001
        walked, wall = None, f'{type(exc).__name__}: {exc}'
    mark(wall == '' and len(seen) > 20
         and all(last == float(size) == highest
                 for size, last, highest in seen)
         and len(walked.trades) > 0
         and set(walked.trades['direction']) == {'short'},
         "THE ENGINE'S OWN WALL, WALKED: on 300 days whose funding rises "
         "every day, the largest funding the strategy can see at each call "
         "is that day's own — never a later one — and every trade it takes "
         "is a short", wall or f"{len(seen)} calls, "
         f"{0 if walked is None else len(walked.trades)} trades")

    print("\n(j) >>> THE SABOTAGE DRILL, PERMANENT: REAL TEXT EDITS TO THIS"
          "\n    FILE'S OWN CODE, EVERY RUN. INERT IS A FAIL.")

    def mutant(old, new):
        """The strategy as it would be with one piece of its text changed.
        The edit must match EXACTLY ONCE or the break did not happen."""
        if PRODUCTION.count(old) != 1:
            return None
        space = {'__name__': 'mutant'}
        exec(compile(PRODUCTION.replace(old, new), '<mutant>', 'exec'), space)
        return space['FundingFade']()

    def witness(maker):
        cases = [HIGH, LOW, SAME, high_case(80), high_case(81),
                 low_case(80), low_case(81), high_case(80, rest=5000),
                 low_case(80, rest=-5000),
                 frame([-9000] * 90 + [-1000]), frame([9000] * 90 + [1000]),
                 frame([-9000] * 90 + [0]), frame([9000] * 90 + [0]),
                 NOT_91, NOT_89, NINETY,
                 frame([1000] * 89 + [9000] + [1000]),
                 frame([1000] * 45 + [NAN] + [1000] * 44 + [9000]),
                 bare, frame([1000] * 81 + [9000] * 9 + [-5000])]
        return tuple(said(case, maker) for case in cases)

    HONEST = witness(strategy)
    EXPECTED = ('short', 'long', 'flat', 'flat', 'short', 'flat', 'long',
                'flat', 'flat', 'flat', 'flat', 'flat', 'flat', 'flat',
                'short', 'flat', 'flat', 'flat', '<ValueError>', 'long')
    BREAKS = [
        ('S1', 'a day EQUAL to today counted as below it',
         'np.sum(before < today)', 'np.sum(before <= today)'),
        ('S2', 'a day EQUAL to today counted as above it',
         'np.sum(before > today)', 'np.sum(before >= today)'),
        ('S3', 'the "above zero" rule dropped', 'if today > 0 and',
         'if today > -1e18 and'),
        ('S4', 'the "below zero" rule dropped', 'if today < 0 and',
         'if today < 1e18 and'),
        ('S5', 'zero counted as positive', 'if today > 0 and',
         'if today >= 0 and'),
        ('S6', 'zero counted as negative', 'if today < 0 and',
         'if today <= 0 and'),
        ('S7', 'an extreme positive BOUGHT instead of faded',
         ">= self.need:\n            return 'short'",
         ">= self.need:\n            return 'long'"),
        ('S8', 'the window one day short (89 + today)',
         '[-(self.window + 1):]', '[-self.window:]'),
        ('S9', 'the window one day long', 'WINDOW = 90 ', 'WINDOW = 91 '),
        ('S10', 'the warm-up removed', 'if len(df) < self.warmup:',
         'if len(df) < 0:'),
        ('S11', 'an empty day ignored', 'if np.isnan(tail).any():',
         'if False:'),
        ('S12', 'no funding column answered "flat"',
         'raise ValueError(NO_COLUMN)', "return 'flat'"),
        ('S13', 'eighty of ninety called extreme', 'NEED = 81 ',
         'NEED = 80 '),
        ('S14', "YESTERDAY's funding judged, not today's",
         'today = tail[-1]', 'today = tail[-2]'),
        ('S15', 'the long side counting days BELOW',
         'if today < 0 and int(np.sum(before > today))',
         'if today < 0 and int(np.sum(before < today))'),
    ]
    print()
    for tag, words, old, new in BREAKS:
        maker = mutant(old, new)
        if maker is None:
            mark(False, f"{tag} {words:<48} -> THE EDIT DID NOT APPLY")
            continue
        broken = witness(maker)
        was_changed = broken != HONEST
        caught = broken != EXPECTED
        good = was_changed and caught
        verdict = ('CAUGHT' if good else
                   'INERT — IT CHANGED NOTHING' if not was_changed else
                   'ESCAPED — THE GATE IS DECORATIVE')
        mark(good, f"{tag} {words:<48} -> {verdict}")
    untouched = mutant('NAME = ', 'NAME  = ')
    mark(untouched is not None and witness(untouched) == HONEST == EXPECTED
         and witness(FundingFade()) == EXPECTED,
         "and an edit that changes NOTHING (one space) gives the twenty "
         "honest answers, which equal the twenty typed out here — so a "
         "break above is caught for what it broke, not for being a copy")

    print("\n(k) NOTHING REAL WAS OPENED, AND THE GATE COUNTS ITSELF.")
    mark(VAULT_OPENED == [] and 'funding_vault' not in sys.modules
         and 'build_funding_vault' not in sys.modules,
         "the Lab's door was never knocked on, and the frozen funding's "
         "reader was never even loaded",
         f"vault calls: {len(VAULT_OPENED)}")
    mark(len(BREAKS) == 15, "fifteen breaks, counted against a number "
                            "typed out here")
    EXPECTED_CHECKS = 44
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.3-S PASSED — {len(nonlocal_ok)} checks, 0 red.

THE RULE IS THE ONE DECLARED: short when today's funding is above zero
and strictly above at least 81 of the 90 days before it; long when it
is below zero and strictly below at least 81. Each turning point was
pinned from both sides - 80 and 81, equal and not equal, zero and one
hundred-millionth either side of it, 90 candles and 91.

A SECOND WRITING-OUT OF THE RULE, IN PLAIN PYTHON, AGREED ON EVERY ONE
OF 4,600 MADE-UP DAYS. A frame with no funding column raises.

FIFTEEN REAL TEXT EDITS TO THIS FILE'S OWN CODE WERE EACH CAUGHT.

WHAT THIS GATE DOES **NOT** PROVE. That fading funding extremes makes
money - it has never seen a real rate or a real candle. That 90 and 81
are the right numbers - they are the declared ones. That the funding
in the frame is the right day's - that is the join's gate (6.3-D) and
the runner's (6.3-R). And that anybody but its author has read it.""")
    else:
        print(f"GATE 6.3-S FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
