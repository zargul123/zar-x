"""
Zar X signals compartment — GAUNTLET SLOT 3: the crowd-mood fade, ON DAILY
CANDLES.

**THIS IS ONE OF THE THREE SEALED SLOTS OF THE PROMISE.** Slot 3 was the
on-chain cycle thermometer; the Commander re-specified it ONCE, on
2026-11-16, before any slot had been run, as the plan allows. Its rules were
declared in PROGRESS_LOG.md that night and committed with no code, before
this file existed. **NOT ONE NUMBER HERE MAY BE CHANGED:** a change is a
different strategy, and the slot is spent on this one.

THE IDEA, in a trader's words: when the crowd is at an extreme of fear, buy;
at an extreme of greed, sell. Bet against the crowd's mood at its extremes.

THE RULES, asked at the close of a daily candle, using only candles up to
and including that one. Each candle carries two extra figures: `mood`, the
Fear & Greed index value published that day (0 to 100), and `mood_side`,
which side the PUBLISHER's own label puts the day on (-1 fear, 0 neutral,
+1 greed).

    FEAR, EXTREME    today is a FEAR day, and today's value is strictly
                     BELOW at least 81 of the previous 90 days'  ->  LONG
    GREED, EXTREME   today is a GREED day, and today's value is strictly
                     ABOVE at least 81 of the previous 90 days'  ->  SHORT
    WARM-UP          flat until 91 candles exist (today + 90)
    Otherwise flat. A neutral day is flat whatever its rank. A day EQUAL
    to another is neither above nor below it.

**NO INDEX VALUE IS TYPED INTO THIS FILE.** "Extreme" is a rank in the
index's own last 90 days, and the side of a day is the publisher's label.
90 and 81 are Slot 2's numbers, carried over.

**WHAT THIS FILE DOES NOT DECIDE.** The exit. The Lab's engine manages every
open trade with the ship's own stop (1.5 ATR) and target (2.0 ATR), enters
at the NEXT day's open, and asks this strategy only when no trade is open.

**LAW 7.** It carries no data: three whole numbers and a name. The mood
reaches it INSIDE the frame the engine hands it, so the engine's own wall
(`df.iloc[:i+1]`) keeps tomorrow's mood out exactly as it keeps tomorrow's
price out. It reads no file, no network, no clock, and never looks at the
frame's dates or prices. It keeps nothing between calls. **A frame missing
either mood column RAISES**: it must never quietly answer "flat" a thousand
times and hand back a false obituary.

The contract (lab/engine.py):  signal(df) -> 'long' | 'short' | 'flat'

Standalone use:
    python signals/mood_fade.py --gate   (the setup gate; opens no vault)
"""
import numpy as np

WINDOW = 90            # the days today is ranked against: a quarter
NEED = 81              # strictly beyond at least this many: nine in ten
WARMUP = 91            # today + 90: the fewest candles that can answer
VALUE = 'mood'         # the index value published that day
SIDE = 'mood_side'     # the publisher's label: -1 fear, 0 neutral, +1 greed
NAME = 'mood-fade-1d-90d-top10'
NO_COLUMN = ('REFUSED: this frame has no `mood` / `mood_side` column. The '
             'fade cannot be judged without the mood, and it must not '
             'answer "flat".')


class MoodFade:
    """Slot 3. Stateless: every call stands on the frame it is handed."""

    def __init__(self, window=WINDOW, need=NEED, warmup=WARMUP):
        self.window = window
        self.need = need
        self.warmup = warmup
        self.name = NAME
        self.params = {'window': window, 'need': need, 'warmup': warmup,
                       'value': VALUE, 'side': SIDE,
                       'kind': 'crowd_mood_fade'}

    def __call__(self, df):
        if VALUE not in df.columns or SIDE not in df.columns:
            raise ValueError(NO_COLUMN)
        if len(df) < self.warmup:
            return 'flat'
        tail = np.asarray(df[VALUE].values[-(self.window + 1):], dtype=float)
        side = float(df[SIDE].values[-1])
        if np.isnan(tail).any() or np.isnan(side):
            return 'flat'
        today = tail[-1]
        before = tail[:-1]
        if side < 0 and int(np.sum(before > today)) >= self.need:
            return 'long'
        if side > 0 and int(np.sum(before < today)) >= self.need:
            return 'short'
        return 'flat'


if __name__ == '__main__':
    import os
    import sys

    if '--gate' not in sys.argv:
        print(__doc__)
        print('This is a strategy, not a command. Its setup gate is '
              '`--gate`; the one run that counts is lab/gauntlet_slot3.py.')
        sys.exit(0)

    # =====================================================================
    # GATE 6.5-S — THE SETUP GATE FOR SLOT 3. Declared in PROGRESS_LOG.md on
    # 2026-11-16 (late night) and committed with no code, before this file
    # existed.
    #
    # **THIS GATE PROVES THE STRATEGY DOES WHAT ITS RULES SAY, ON FRAMES IT
    # MAKES UP ITSELF. IT PROVES NOTHING ABOUT WHETHER IT MAKES MONEY.**
    # **IT NEVER OPENS THE VAULT OR ANY FROZEN FOLDER.**
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
    FEAR, NEUTRAL, GREED = -1, 0, 1

    def frame(values, today_side, sides=None, base=100.0, swing=1.0,
              drop=None):
        """Made-up daily candles carrying a made-up mood each. `today_side`
        is the LAST day's side; earlier days are neutral unless `sides` is
        given (the rule reads only the last day's side)."""
        values = [float(value) for value in values]
        index = pd.date_range('2030-01-01', periods=len(values), freq='1D')
        closes = [base + swing * ((n * 7) % 13) for n in range(len(values))]
        if sides is None:
            sides = [0.0] * (len(values) - 1) + [float(today_side)]
        data = {'open': closes, 'high': [c + swing for c in closes],
                'low': [c - swing for c in closes], 'close': closes,
                'mood': values, 'mood_side': sides[:len(values)]}
        if drop:
            del data[drop]
        return pd.DataFrame(data, index=index)

    def said(df, maker=None):
        try:
            return (maker or strategy)(df)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>'

    strategy = MoodFade()

    print("=" * 70)
    print("GATE 6.5-S — SLOT 3, THE CROWD-MOOD FADE, THE SETUP. Made-up")
    print("frames, hand-worked answers. Nothing frozen is opened.")
    print("=" * 70)

    print("\n(a) THE NUMBERS ARE THE ONES DECLARED, typed out here.")
    mark(strategy.params == {'window': 90, 'need': 81, 'warmup': 91,
                             'value': 'mood', 'side': 'mood_side',
                             'kind': 'crowd_mood_fade'}
         and strategy.name == 'mood-fade-1d-90d-top10'
         and (WINDOW, NEED, WARMUP, VALUE, SIDE) == (90, 81, 91, 'mood',
                                                     'mood_side')
         and WARMUP == WINDOW + 1 and 10 * NEED == 9 * WINDOW
         and sorted(vars(strategy)) == ['name', 'need', 'params', 'warmup',
                                        'window'],
         "today ranked against the 90 days before it, strictly beyond at "
         "least 81 of them, a 91-candle warm-up — every one typed out here "
         "AND carried in `params`; and the object holds nothing else",
         f"{strategy.params}")
    other = MoodFade(window=60, need=54, warmup=61)
    mark(other.params['window'] == 60 and other.params['need'] == 54
         and other.params['warmup'] == 61
         and (other.window, other.need, other.warmup) == (60, 54, 61),
         "and `params` carries THE NUMBERS THE OBJECT ACTUALLY USES: one "
         "built with 60, 54 and 61 says so, and cannot wear the declared "
         "fingerprint")

    print("\n(b) THE THREE PLAIN CASES, worked by hand.")
    PANIC = frame([50] * 90 + [10], FEAR)
    MANIA = frame([50] * 90 + [90], GREED)
    DULL = frame([50] * 91, NEUTRAL)
    mark(said(PANIC) == 'long',
         "ninety days at 50 and then a FEAR day at 10, below all 90 -> the "
         "crowd is frightened -> LONG", said(PANIC))
    mark(said(MANIA) == 'short',
         "the mirror: a GREED day at 90, above all 90 -> SHORT", said(MANIA))
    mark(said(DULL) == 'flat',
         "ninety-one neutral days all at 50 -> FLAT", said(DULL))

    print("\n(c) THE RANK, AT THE EXACT NUMBER — ON BOTH SIDES (rule (o)).")

    def fear_case(above, rest=5, today=30, side=FEAR):
        """Today 30. `above` of the 90 before it are at 60 (above today);
        the rest at `rest`."""
        return frame([60] * above + [rest] * (90 - above) + [today], side)

    def greed_case(below, rest=95, today=70, side=GREED):
        return frame([40] * below + [rest] * (90 - below) + [today], side)

    mark(said(fear_case(80)) == 'flat' and said(fear_case(81)) == 'long'
         and said(fear_case(82)) == 'long',
         "BELOW EXACTLY 80 of the 90 is FLAT; below 81 is LONG; below 82 "
         "is LONG",
         f"80 {said(fear_case(80))}, 81 {said(fear_case(81))}")
    mark(said(greed_case(80)) == 'flat' and said(greed_case(81)) == 'short'
         and said(greed_case(82)) == 'short',
         "THE MIRROR: ABOVE EXACTLY 80 is FLAT; above 81 is SHORT; above "
         "82 is SHORT",
         f"80 {said(greed_case(80))}, 81 {said(greed_case(81))}")
    mark(said(fear_case(80, rest=30)) == 'flat'
         and said(fear_case(81, rest=30)) == 'long'
         and said(greed_case(80, rest=70)) == 'flat'
         and said(greed_case(81, rest=70)) == 'short',
         "A DAY EQUAL TO TODAY IS NOT BEYOND IT, on either side: below 80 "
         "and level with ten is FLAT; below 81 and level with nine is LONG; "
         "and the same for greed")
    mixed = [5] * 4 + [60] * 40 + [5] * 5 + [60] * 41 + [30]
    mark(said(frame(mixed, FEAR)) == 'long'
         and said(frame(mixed[:89][::-1] + mixed[89:], FEAR)) == 'long',
         "the ORDER of the ninety days does not matter")

    print("\n(d) THE SIDE IS THE PUBLISHER's LABEL.")
    mark(said(fear_case(90, side=NEUTRAL)) == 'flat'
         and said(fear_case(90, side=GREED)) == 'flat'
         and said(fear_case(90, side=FEAR)) == 'long',
         "THE LOWEST READING IN 90 DAYS ON A NEUTRAL DAY IS FLAT, and on a "
         "GREED day is FLAT — the crowd is not afraid; on a FEAR day it is "
         "LONG",
         f"neutral {said(fear_case(90, side=NEUTRAL))}, greed "
         f"{said(fear_case(90, side=GREED))}, fear "
         f"{said(fear_case(90, side=FEAR))}")
    mark(said(greed_case(90, side=NEUTRAL)) == 'flat'
         and said(greed_case(90, side=FEAR)) == 'flat'
         and said(greed_case(90, side=GREED)) == 'short',
         "THE HIGHEST READING IN 90 DAYS ON A NEUTRAL OR A FEAR DAY IS "
         "FLAT; on a GREED day it is SHORT")
    # A fear day that is the HIGHEST in 90 must not be sold; a greed day
    # that is the LOWEST must not be bought.
    mark(said(greed_case(90, side=FEAR)) == 'flat'
         and said(fear_case(90, side=GREED)) == 'flat'
         and said(frame([50] * 90 + [0], FEAR)) == 'long'
         and said(frame([50] * 90 + [100], GREED)) == 'short',
         "the two rules do not cross; and the index's own limits, 0 and "
         "100, are ordinary values")
    # ONLY TODAY's side is read: ninety GREED days before a fear day.
    loud = frame([60] * 90 + [30], FEAR, sides=[1.0] * 90 + [-1.0])
    mark(said(loud) == 'long',
         "ONLY TODAY's label decides the side: ninety greed days and then "
         "a fear day below them all is LONG")

    print("\n(e) THE WINDOW IS EXACTLY THE 90 DAYS BEFORE TODAY.")
    NOT_91 = frame([60] + [60] * 80 + [5] * 10 + [30], FEAR)
    NOT_89 = frame([60] + [5] * 9 + [60] * 80 + [30], FEAR)
    mark(said(NOT_91) == 'flat' and said(NOT_89) == 'long',
         "a high day 91 days ago is OUTSIDE the window and does not make 81 "
         "(FLAT); a high day exactly 90 days ago is INSIDE it and does "
         "(LONG) — the window is 90, not 91 and not 89",
         f"91 back {said(NOT_91)}, 90 back {said(NOT_89)}")
    spike = frame([50] * 89 + [10] + [50], NEUTRAL,
                  sides=[0.0] * 89 + [-1.0] + [0.0])
    mark(said(spike) == 'flat' and said(spike.iloc[:-1]) == 'flat'
         and said(frame([50] * 90 + [10] + [50], NEUTRAL,
                        sides=[0.0] * 90 + [-1.0, 0.0]).iloc[:-1]) == 'long',
         "TODAY's mood is the one judged, not yesterday's: panic yesterday "
         "and a dull day today is FLAT, and the same frame cut off at the "
         "panic (with 90 days before it) is LONG")

    print("\n(f) THE WARM-UP, AND FRAMES THAT CANNOT BE JUDGED.")
    NINETY = frame([50] * 89 + [10], FEAR)
    mark(said(NINETY) == 'flat' and said(frame([50] * 90 + [10], FEAR))
         == 'long',
         "90 candles is FLAT even with today below all 89 before it — only "
         "the warm-up stops it; 91 candles of the same shape is LONG",
         said(NINETY))
    mark([said(frame([50] * n + [10], FEAR)) for n in (0, 1, 30, 80, 88)]
         == ['flat'] * 5 and said(frame([], FEAR)) == 'flat',
         "frames of 1, 2, 31, 81 and 89 candles, and an EMPTY frame, are "
         "each FLAT and none raises")
    mark(said(frame([NAN] + [50] * 89 + [10], FEAR)) == 'flat'
         and said(frame([50] * 45 + [NAN] + [50] * 44 + [10], FEAR)) == 'flat'
         and said(frame([50] * 90 + [NAN], FEAR)) == 'flat'
         and said(frame([50] * 90 + [10], NAN)) == 'flat'
         and said(frame([NAN] + [50] * 90 + [10], FEAR)) == 'long',
         "AN EMPTY DAY anywhere in the 91, or today's SIDE empty, is FLAT; "
         "an empty day 91 days back, outside the window, changes nothing")
    mark(said(frame([50] * 90 + [10], FEAR, drop='mood')) == '<ValueError>'
         and said(frame([50] * 90 + [10], FEAR, drop='mood_side'))
         == '<ValueError>'
         and said(frame([50] * 90 + [10], FEAR, drop='mood').iloc[:1])
         == '<ValueError>'
         and said(frame([50] * 90 + [10], FEAR,
                        drop='mood_side').iloc[:1]) == '<ValueError>',
         "A FRAME MISSING EITHER MOOD COLUMN RAISES — at the very first "
         "candle, not only after the warm-up. The fade must never answer "
         "'flat' for want of the mood")

    print("\n(g) THE PRICES DO NOT MATTER; THE FRAME IS NOT TOUCHED; NOTHING"
          "\n    IS REMEMBERED.")
    rng = np.random.default_rng(65)
    walk = np.clip(50 + np.cumsum(rng.integers(-6, 7, 4600)) * 0.35, 0,
                   100).round()
    walk[rng.integers(0, 4600, 10)] = np.nan
    side_of = np.where(walk <= 46, -1.0, np.where(walk >= 55, 1.0, 0.0))
    side_of[np.isnan(walk)] = np.nan
    LONG_RUN = frame(walk, NEUTRAL, sides=list(side_of))
    OTHER = frame(walk, NEUTRAL, sides=list(side_of), base=50000.0,
                  swing=777.0)
    answers = [said(LONG_RUN.iloc[:n]) for n in range(1, 4601)]
    other_answers = [said(OTHER.iloc[:n]) for n in range(1, 4601)]
    mark(answers == other_answers,
         "4,600 made-up days judged twice, on two sets of candles with "
         "nothing in common but the mood: the same answer on every day")
    before_call = LONG_RUN.copy()
    again = [said(LONG_RUN.iloc[:n]) for n in (4600, 200, 3000, 91)]
    mark(LONG_RUN.equals(before_call)
         and again == [answers[4599], answers[199], answers[2999],
                       answers[90]]
         and vars(strategy) == vars(MoodFade()),
         "the frame is exactly as it was handed over; asked again out of "
         "order the answers are the same; the object holds what it held")

    print("\n(h) A SECOND WRITING-OUT OF THE RULE, sharing no code.")

    def by_hand(values, sides, at):
        if at < 90:
            return 'flat'
        today, ninety, label = values[at], values[at - 90:at], sides[at]
        if today != today or label != label or any(v != v for v in ninety):
            return 'flat'
        if label == -1 and 10 * sum(1 for v in ninety if v > today) >= 810:
            return 'long'
        if label == 1 and 10 * sum(1 for v in ninety if v < today) >= 810:
            return 'short'
        return 'flat'

    plain_values = [float(v) for v in walk]
    plain_sides = [float(s) for s in side_of]
    reference = [by_hand(plain_values, plain_sides, at) for at in range(4600)]
    differ = [at for at in range(4600) if reference[at] != answers[at]]
    mark(not differ and reference.count('short') >= 50
         and reference.count('long') >= 50
         and reference.count('flat') >= 1000,
         "the two agree on EVERY ONE of 4,600 days, with both directions "
         "signalled many times and most days flat",
         f"{reference.count('short')} short, {reference.count('long')} "
         f"long, {reference.count('flat')} flat, {len(differ)} "
         f"disagreements")

    print("\n(i) LAW 7: IT CARRIES NOTHING AND READS NOTHING BUT THE FRAME.")
    from dummies import PerfectForesight
    from leak_check import leak_check
    clean = leak_check(strategy)
    awake = leak_check(PerfectForesight(PANIC))
    mark(not clean.flagged and awake.flagged,
         "the leak scan finds NO carried data on the strategy — and in the "
         "same run it FLAGS the Lab's deliberate leak",
         f"strategy: {len(clean.findings)} findings; the deliberate leak: "
         f"{len(awake.findings)}")
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        SOURCE = handle.read()
    PRODUCTION = SOURCE.split("if __name__ == '__main__':")[0]
    tree = ast.parse(PRODUCTION)
    imports = sorted({alias.name for node in ast.walk(tree)
                      if isinstance(node, (ast.Import, ast.ImportFrom))
                      for alias in node.names})
    code_only = '\n'.join(PRODUCTION.split('"""')[2::2])
    stores = [node for node in ast.walk(tree)
              if isinstance(node, ast.Attribute)
              and isinstance(node.ctx, ast.Store)]
    WORD = re.compile(chr(92) + 'b(open|high|low|close|volume)'
                      + chr(92) + 'b')
    mark(imports == ['numpy']
         and not any(word in code_only for word in
                     ('open(', '.index', 'iloc', 'datetime', 'time.',
                      'global ', 'os.', 'sys.', 'eval', 'exec', '__import__'))
         and not WORD.search(code_only)
         and WORD.search("x = df['close'].values")
         and WORD.search("df[ 'low' ]") and not WORD.search('window below')
         and len(stores) == 5,
         "the strategy's code imports numpy and nothing else; names no "
         "file, no clock, no date index and NO PRICE COLUMN — by a word "
         "search PROVED HERE to see `close` and `low` and not to trip on "
         "`window` or `below`; and stores five things on itself, all when "
         "it is made")
    seen = []

    def recorder(df):
        seen.append((len(df), float(df['mood'].iloc[-1]),
                     float(df['mood'].min())))
        return strategy(df)

    data = _engine.VaultData.__new__(_engine.VaultData)
    data.asset, data.timeframe = 'MADE-UP', '1d'
    data.path, data.report, data.verdict = '<made up>', None, 'PASS'
    falling = [float(1000 - n) for n in range(300)]    # each day a new low
    data.df = frame(falling, FEAR, sides=[-1.0] * 300, swing=3.0)
    try:
        walked = _engine.run_backtest(data, recorder, 'wall-check',
                                      verbose=False, regime=False)
        wall = ''
    except Exception as exc:                               # noqa: BLE001
        walked, wall = None, f'{type(exc).__name__}: {exc}'
    mark(wall == '' and len(seen) > 20
         and all(last == float(1001 - size) == lowest
                 for size, last, lowest in seen)
         and len(walked.trades) > 0
         and set(walked.trades['direction']) == {'long'},
         "THE ENGINE'S OWN WALL, WALKED: on 300 fear days whose mood falls "
         "every day, the lowest mood the strategy can see at each call is "
         "that day's own — never a later one — and every trade is a long",
         wall or f"{len(seen)} calls, "
         f"{0 if walked is None else len(walked.trades)} trades")

    print("\n(j) >>> THE SABOTAGE DRILL, PERMANENT: REAL TEXT EDITS TO THIS"
          "\n    FILE'S OWN CODE, EVERY RUN. INERT IS A FAIL.")

    def mutant(old, new):
        if PRODUCTION.count(old) != 1:
            return None
        space = {'__name__': 'mutant'}
        exec(compile(PRODUCTION.replace(old, new), '<mutant>', 'exec'), space)
        return space['MoodFade']()

    def witness(maker):
        cases = [PANIC, MANIA, DULL, fear_case(80), fear_case(81),
                 greed_case(80), greed_case(81), fear_case(80, rest=30),
                 greed_case(80, rest=70), fear_case(90, side=NEUTRAL),
                 greed_case(90, side=NEUTRAL), fear_case(90, side=GREED),
                 greed_case(90, side=FEAR), NOT_91, NOT_89, NINETY, spike,
                 frame([50] * 45 + [NAN] + [50] * 44 + [10], FEAR),
                 frame([50] * 90 + [10], FEAR, drop='mood_side'),
                 frame([50] * 90 + [10], NAN), loud]
        return tuple(said(case, maker) for case in cases)

    HONEST = witness(strategy)
    EXPECTED = ('long', 'short', 'flat', 'flat', 'long', 'flat', 'short',
                'flat', 'flat', 'flat', 'flat', 'flat', 'flat', 'flat',
                'long', 'flat', 'flat', 'flat', '<ValueError>', 'flat',
                'long')
    BREAKS = [
        ('S1', 'a day EQUAL to today counted as above it',
         'np.sum(before > today)', 'np.sum(before >= today)'),
        ('S2', 'a day EQUAL to today counted as below it',
         'np.sum(before < today)', 'np.sum(before <= today)'),
        ('S3', 'the fear label not needed to buy', 'if side < 0 and',
         'if side < 9 and'),
        ('S4', 'the greed label not needed to sell', 'if side > 0 and',
         'if side > -9 and'),
        ('S5', 'a NEUTRAL day allowed to buy', 'if side < 0 and',
         'if side <= 0 and'),
        ('S6', 'a NEUTRAL day allowed to sell', 'if side > 0 and',
         'if side >= 0 and'),
        ('S7', 'extreme fear SOLD instead of bought',
         ">= self.need:\n            return 'long'",
         ">= self.need:\n            return 'short'"),
        ('S8', 'the window one day short (89 + today)',
         '[-(self.window + 1):]', '[-self.window:]'),
        ('S9', 'the window one day long', 'WINDOW = 90 ', 'WINDOW = 91 '),
        ('S10', 'the warm-up removed', 'if len(df) < self.warmup:',
         'if len(df) < 0:'),
        ('S11', 'an empty day ignored',
         'if np.isnan(tail).any() or np.isnan(side):', 'if np.isnan(side):'),
        # (An empty SIDE today needs no break of its own: with the test
        # for it removed the answer is still flat, because an empty side
        # is neither below nor above zero. It was S12 and came back INERT
        # on this gate's first run.)
        ('S13', 'a missing side column answered "flat"',
         'raise ValueError(NO_COLUMN)', "return 'flat'"),
        ('S14', 'eighty of ninety called extreme', 'NEED = 81 ', 'NEED = 80 '),
        ('S15', "YESTERDAY's mood judged, not today's", 'today = tail[-1]',
         'today = tail[-2]'),
        ('S16', "YESTERDAY's label deciding the side",
         'side = float(df[SIDE].values[-1])',
         'side = float(df[SIDE].values[-2])'),
        ('S17', 'fear bought when it is the HIGHEST in 90',
         'if side < 0 and int(np.sum(before > today))',
         'if side < 0 and int(np.sum(before < today))'),
    ]
    print()
    for tag, words, old, new in BREAKS:
        maker = mutant(old, new)
        if maker is None:
            mark(False, f"{tag} {words:<46} -> THE EDIT DID NOT APPLY")
            continue
        broken = witness(maker)
        was_changed = broken != HONEST
        good = was_changed and broken != EXPECTED
        mark(good, f"{tag} {words:<46} -> "
                   f"{'CAUGHT' if good else 'INERT — IT CHANGED NOTHING'}")
    untouched = mutant('NAME = ', 'NAME  = ')
    mark(untouched is not None and witness(untouched) == HONEST == EXPECTED,
         "and an edit that changes NOTHING (one space) gives the "
         "twenty-one honest answers, which equal the twenty-one typed out "
         "here")

    print("\n(k) NOTHING REAL WAS OPENED, AND THE GATE COUNTS ITSELF.")
    mark(VAULT_OPENED == [] and 'mood_vault' not in sys.modules
         and 'funding_vault' not in sys.modules
         and 'build_mood_vault' not in sys.modules,
         "the Lab's door was never knocked on, and no frozen folder's "
         "reader was even loaded", f"vault calls: {len(VAULT_OPENED)}")
    mark(len(BREAKS) == 16, "sixteen breaks, counted against a number "
                            "typed out here")
    EXPECTED_CHECKS = 45
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.5-S PASSED — {len(nonlocal_ok)} checks, 0 red.

THE RULE IS THE ONE DECLARED: long on a FEAR day whose value is
strictly below at least 81 of the 90 days before it; short on a GREED
day strictly above at least 81. Each turning point was pinned from
both sides, and the label side from all three (fear, neutral, greed).

A SECOND WRITING-OUT, IN PLAIN PYTHON, AGREED ON EVERY ONE OF 4,600
MADE-UP DAYS. A frame missing either mood column raises.

SIXTEEN REAL TEXT EDITS TO THIS FILE'S OWN CODE WERE EACH CAUGHT.

WHAT THIS GATE DOES **NOT** PROVE. That fading the crowd's mood makes
money. That 90 and 81 are the right numbers. That the mood in the
frame is the right day's - that is the join's gate (6.5-D) and the
runner's (6.5-R). And that anybody but its author has read it.""")
    else:
        print(f"GATE 6.5-S FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
