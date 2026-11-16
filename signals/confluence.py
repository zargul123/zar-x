"""
Zar X signals compartment — THE CONFLUENCE RULE and its yardstick, THE TREND
ALONE. For "Forward Check 1". **NOT A GAUNTLET SLOT.**

After Slot 2 (the funding fade) failed, the Commander ordered the three
things the slots look at - the price trend, leverage crowding, the crowd's
mood - combined, and tried once on data nobody had seen. The rule was
written into PROGRESS_LOG.md on 2026-11-16, before any unseen data was
fetched, and its bar committed with no code before this file existed.
**NOT ONE NUMBER HERE MAY BE CHANGED** once the forward check has been run.

THE CONFLUENCE RULE, asked at the close of a daily candle:

    TREND   UP if today's close is strictly above the plain average of the
            last 100 closes (today's included); DOWN if strictly below.
    CROWD   GREEDY/LONG if Slot 2's rule (signals/funding_fade.py) answers
            "short" OR Slot 3's (signals/mood_fade.py) answers "short";
            SCARED/SHORT if either answers "long".
    TRADE   LONG when UP and GREEDY/LONG; SHORT when DOWN and SCARED/SHORT;
            otherwise flat.
    WARM-UP flat until 100 candles exist.

**IT GOES WITH THE CROWD, IN THE DIRECTION OF THE TREND.** That is the
opposite of what Slots 2 and 3 do with the same two readings, and it is
what the training side supported: fading the crowd lost there.

THE YARDSTICK, THE TREND ALONE: LONG when UP, SHORT when DOWN, nothing
else. If the confluence rule cannot beat it, the funding and mood readings
are not earning their place as triggers.

**THE TWO CROWD RULES ARE USED AS BUILT, BY CALLING THEM** - the very
classes Slots 2 and 3 use. This file adds the trend and the combination.

**LAW 7.** It carries no data: one whole number, a name and the two crowd
rules, which carry three whole numbers each. Everything it reads is in the
frame the engine hands it. No file, no network, no clock, no dates.

The contract (lab/engine.py):  signal(df) -> 'long' | 'short' | 'flat'

Standalone use:
    python signals/confluence.py --gate   (the setup gate; opens nothing real)
"""
import numpy as np

try:
    from signals.funding_fade import FundingFade
    from signals.mood_fade import MoodFade
except ImportError:                     # run as a script from its own folder
    from funding_fade import FundingFade
    from mood_fade import MoodFade

TREND = 100            # the closes the trend's average is taken over
NAME = 'confluence-1d-t100'
YARDSTICK_NAME = 'trend-only-1d-t100'


def trend_of(closes, length):
    """+1 if the last close is strictly above the average of the last
    `length` closes, -1 if strictly below, 0 if level with it."""
    window = np.asarray(closes[-length:], dtype=float)
    average = float(window.sum()) / len(window)
    last = float(window[-1])
    return 1 if last > average else -1 if last < average else 0


class Confluence:
    """With the trend AND with the crowd. Stateless."""

    def __init__(self, trend=TREND):
        self.trend = trend
        self.funding = FundingFade()
        self.mood = MoodFade()
        self.name = NAME
        self.params = {'trend': trend, 'funding': self.funding.params,
                       'mood': self.mood.params, 'kind': 'confluence'}

    def __call__(self, df):
        crowd = (self.funding(df), self.mood(df))
        if len(df) < self.trend:
            return 'flat'
        way = trend_of(df['close'].values, self.trend)
        if way > 0 and 'short' in crowd:
            return 'long'
        if way < 0 and 'long' in crowd:
            return 'short'
        return 'flat'


class TrendOnly:
    """The yardstick: the trend alone. Stateless."""

    def __init__(self, trend=TREND):
        self.trend = trend
        self.name = YARDSTICK_NAME
        self.params = {'trend': trend, 'kind': 'trend_only'}

    def __call__(self, df):
        if len(df) < self.trend:
            return 'flat'
        way = trend_of(df['close'].values, self.trend)
        return 'long' if way > 0 else 'short' if way < 0 else 'flat'


if __name__ == '__main__':
    import os
    import sys

    if '--gate' not in sys.argv:
        print(__doc__)
        print('This is a strategy, not a command. Its gate is `--gate`; the '
              'one run is lab/forward_check.py.')
        sys.exit(0)

    # =====================================================================
    # GATE 6.6-S — THE CONFLUENCE RULE AND THE TREND ALONE. Declared in
    # PROGRESS_LOG.md on 2026-11-16 and committed with no code, before this
    # file existed. Made-up frames only; nothing real is opened.
    # =====================================================================
    import ast
    import inspect
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
        raise RuntimeError('the gate must never open the vault')

    _engine.load_vault = _no_vault

    def frame(closes, crowd='none', drop=None):
        """Made-up daily candles. `crowd` sets TODAY's readings:
          'greedy'  funding 9,000 after ninety days at 3,000 (Slot 2: short)
          'scared'  funding -9,000 after ninety at -3,000   (Slot 2: long)
          'mania'   a Greed day at 90 after ninety at 50     (Slot 3: short)
          'panic'   a Fear day at 10 after ninety at 50      (Slot 3: long)
          'split'   funding greedy AND mood panic
          'none'    quiet on both"""
        n = len(closes)
        closes = [float(c) for c in closes]
        funding = [3000.0] * n
        mood, side = [50.0] * n, [0.0] * n
        if crowd in ('scared',):
            funding = [-3000.0] * n
        if n:
            if crowd in ('greedy', 'split'):
                funding[-1] = 9000.0
            if crowd == 'scared':
                funding[-1] = -9000.0
            if crowd == 'mania':
                mood[-1], side[-1] = 90.0, 1.0
            if crowd in ('panic', 'split'):
                mood[-1], side[-1] = 10.0, -1.0
        data = {'open': closes, 'high': [c + 1 for c in closes],
                'low': [c - 1 for c in closes], 'close': closes,
                'funding': funding, 'mood': mood, 'mood_side': side}
        if drop:
            del data[drop]
        return pd.DataFrame(data, index=pd.date_range('2030-01-01',
                                                      periods=n, freq='1D'))

    def said(df, maker=None):
        try:
            return (maker or rule)(df)
        except Exception as exc:                           # noqa: BLE001
            return f'<{type(exc).__name__}>'

    rule, yard = Confluence(), TrendOnly()
    UP = [100 + n for n in range(150)]          # rising: last far above avg
    DOWN = [300 - n for n in range(150)]
    LEVEL = [100.0] * 150

    print("=" * 70)
    print("GATE 6.6-S — THE CONFLUENCE RULE AND THE TREND ALONE. Made-up")
    print("frames, hand-worked answers. Nothing real is opened.")
    print("=" * 70)

    print("\n(a) THE NUMBERS ARE THE ONES DECLARED, typed out here.")
    mark(TREND == 100 and rule.trend == 100 and yard.trend == 100
         and rule.name == 'confluence-1d-t100'
         and yard.name == 'trend-only-1d-t100'
         and rule.params == {
             'trend': 100, 'kind': 'confluence',
             'funding': {'window': 90, 'need': 81, 'warmup': 91,
                         'column': 'funding',
                         'kind': 'funding_extreme_fade'},
             'mood': {'window': 90, 'need': 81, 'warmup': 91,
                      'value': 'mood', 'side': 'mood_side',
                      'kind': 'crowd_mood_fade'}}
         and yard.params == {'trend': 100, 'kind': 'trend_only'}
         and Confluence(trend=60).params['trend'] == 60
         and TrendOnly(trend=60).params['trend'] == 60,
         "a 100-close trend, and the two crowd rules' own numbers (90, 81, "
         "91 each) — every one typed out here AND carried in `params`, "
         "which carries what the object actually uses")
    mark(type(rule.funding).__name__ == 'FundingFade'
         and type(rule.mood).__name__ == 'MoodFade'
         and os.path.basename(inspect.getsourcefile(type(rule.funding)))
         == 'funding_fade.py'
         and os.path.basename(inspect.getsourcefile(type(rule.mood)))
         == 'mood_fade.py'
         and os.path.dirname(os.path.abspath(inspect.getsourcefile(
             type(rule.funding)))) == os.path.dirname(os.path.abspath(
                 __file__)),
         "THE TWO CROWD RULES ARE SLOT 2's AND SLOT 3's OWN CLASSES, loaded "
         "from their own files beside this one — called, not copied")

    print("\n(b) ALL EIGHT CASES OF TREND AND CROWD, by hand.")
    table = {(name, crowd): said(frame(closes, crowd))
             for name, closes in (('up', UP), ('down', DOWN))
             for crowd in ('greedy', 'mania', 'scared', 'panic', 'none')}
    mark(table == {('up', 'greedy'): 'long', ('up', 'mania'): 'long',
                   ('up', 'scared'): 'flat', ('up', 'panic'): 'flat',
                   ('up', 'none'): 'flat',
                   ('down', 'greedy'): 'flat', ('down', 'mania'): 'flat',
                   ('down', 'scared'): 'short', ('down', 'panic'): 'short',
                   ('down', 'none'): 'flat'},
         "UP-TREND: a greedy crowd (by funding, or by mood) -> LONG; a "
         "scared crowd or a quiet one -> FLAT. DOWN-TREND: a scared crowd "
         "(by funding, or by mood) -> SHORT; a greedy or a quiet one -> "
         "FLAT. It goes WITH the crowd, and only with the trend",
         f"{table}")
    mark(said(frame(UP, 'split')) == 'long'
         and said(frame(DOWN, 'split')) == 'short',
         "THE TWO CROWD RULES DISAGREEING (funding greedy, mood in panic): "
         "the day counts as both, and the TREND decides - long in an "
         "up-trend, short in a down-trend",
         f"up {said(frame(UP, 'split'))}, down {said(frame(DOWN, 'split'))}")
    mark([said(frame(LEVEL, crowd)) for crowd in
          ('greedy', 'mania', 'scared', 'panic', 'split', 'none')]
         == ['flat'] * 6,
         "NO TREND (a price that has not moved): flat whatever the crowd")

    print("\n(c) THE TREND, AT ITS LINE AND OVER EXACTLY 100 CLOSES.")
    at_line = [100.0] * 149 + [100.0]
    above = [100.0] * 149 + [100.01]
    below = [100.0] * 149 + [99.99]
    mark((said(frame(at_line, 'greedy')), said(frame(above, 'greedy')),
          said(frame(below, 'scared')), said(frame(at_line, 'scared')))
         == ('flat', 'long', 'short', 'flat')
         and (said(frame(at_line), yard), said(frame(above), yard),
              said(frame(below), yard)) == ('flat', 'long', 'short'),
         "a close EXACTLY EQUAL to its 100-close average is neither up nor "
         "down (flat, for both rules); one cent above is up; one cent below "
         "is down")
    # Today 100; the 98 closes before it 100; the close 99 days back (the
    # 100th in the window) 130: average 100.3, so the trend is DOWN. Over
    # 99 closes it would be level; the close 100 days back (outside), at
    # 10, would make a 101-close average 99.4: UP.
    EDGE = [100.0] * 49 + [10.0, 130.0] + [100.0] * 99
    mark(len(EDGE) == 150 and said(frame(EDGE, 'scared')) == 'short'
         and said(frame(EDGE), yard) == 'short',
         "THE AVERAGE IS OVER EXACTLY 100 CLOSES: a high close 99 days back "
         "is INSIDE it and makes the trend down; a low close 100 days back "
         "is OUTSIDE it and does not make it up — not 99 and not 101",
         f"{said(frame(EDGE, 'scared'))}")

    print("\n(d) THE YARDSTICK IGNORES THE CROWD; THE WARM-UP; MISSING COLUMNS.")
    mark(all(said(frame(UP, crowd), yard) == 'long'
             and said(frame(DOWN, crowd), yard) == 'short'
             for crowd in ('greedy', 'mania', 'scared', 'panic', 'none')),
         "the trend alone answers LONG in an up-trend and SHORT in a "
         "down-trend whatever the crowd is doing")
    mark(said(frame(UP[:99], 'greedy')) == 'flat'
         and said(frame(UP[:100], 'greedy')) == 'long'
         and said(frame(UP[:99]), yard) == 'flat'
         and said(frame(UP[:100]), yard) == 'long'
         and said(frame([], 'none'), yard) == 'flat',
         "99 candles is FLAT and 100 is judged, for both rules; an empty "
         "frame is flat for the yardstick")
    mark(said(frame(UP, 'greedy', drop='funding')) == '<ValueError>'
         and said(frame(UP, 'greedy', drop='mood')) == '<ValueError>'
         and said(frame(UP, 'greedy', drop='mood_side')) == '<ValueError>'
         and said(frame(UP[:1], 'none', drop='funding')) == '<ValueError>'
         and said(frame(UP, 'greedy', drop='funding'), yard) == 'long',
         "A FRAME MISSING THE FUNDING OR EITHER MOOD COLUMN RAISES for the "
         "confluence rule — at the first candle too — and the yardstick, "
         "which reads neither, is unaffected")

    print("\n(e) A SECOND WRITING-OUT, sharing no code, on 3,200 made-up days.")
    rng = np.random.default_rng(66)
    n = 3200
    closes = list(1000 + np.cumsum(rng.normal(0, 9, n)))
    fund = np.round(np.cumsum(rng.integers(-900, 901, n)) * 0.6)
    moodv = np.clip(50 + np.cumsum(rng.integers(-6, 7, n)) * 0.35, 0,
                    100).round()
    sidev = np.where(moodv <= 46, -1.0, np.where(moodv >= 55, 1.0, 0.0))
    BIG = pd.DataFrame({'open': closes, 'high': closes, 'low': closes,
                        'close': closes, 'funding': fund, 'mood': moodv,
                        'mood_side': sidev},
                       index=pd.date_range('2030-01-01', periods=n,
                                           freq='1D'))

    def by_hand(at):
        if at < 99:
            return 'flat', 'flat'
        window = closes[at - 99:at + 1]
        average = sum(window) / 100
        way = 1 if closes[at] > average else -1 if closes[at] < average else 0
        f_today, f_before = fund[at], fund[at - 90:at]
        m_today, m_before = moodv[at], moodv[at - 90:at]
        greedy = ((f_today > 0 and sum(1 for v in f_before if v < f_today)
                   >= 81)
                  or (sidev[at] == 1 and sum(1 for v in m_before
                                             if v < m_today) >= 81))
        scared = ((f_today < 0 and sum(1 for v in f_before if v > f_today)
                   >= 81)
                  or (sidev[at] == -1 and sum(1 for v in m_before
                                              if v > m_today) >= 81))
        combined = ('long' if way > 0 and greedy else
                    'short' if way < 0 and scared else 'flat')
        alone = 'long' if way > 0 else 'short' if way < 0 else 'flat'
        return combined, alone

    got = [(said(BIG.iloc[:k + 1]), said(BIG.iloc[:k + 1], yard))
           for k in range(n)]
    want = [by_hand(k) for k in range(n)]
    differ = [k for k in range(n) if got[k] != want[k]]
    c_long = sum(1 for g in got if g[0] == 'long')
    c_short = sum(1 for g in got if g[0] == 'short')
    mark(not differ and c_long >= 30 and c_short >= 30
         and c_long + c_short < sum(1 for g in got if g[1] != 'flat'),
         "both rules agree with a plain-Python writing-out on EVERY ONE of "
         "3,200 days, with the confluence rule long and short many times "
         "and trading on fewer days than the trend alone",
         f"confluence {c_long} long, {c_short} short; "
         f"{len(differ)} disagreements")
    before_call = BIG.copy()
    said(BIG)
    said(BIG, yard)
    mark(BIG.equals(before_call) and sorted(vars(rule)) == [
        'funding', 'mood', 'name', 'params', 'trend']
        and sorted(vars(yard)) == ['name', 'params', 'trend'],
        "the frame is exactly as it was handed over, and the two objects "
        "hold only what they were made with")

    print("\n(f) LAW 7.")
    from dummies import PerfectForesight
    from leak_check import leak_check
    mark(not leak_check(rule).flagged and not leak_check(yard).flagged
         and leak_check(PerfectForesight(frame(UP))).flagged,
         "the leak scan finds NO carried data on either rule — and in the "
         "same run it FLAGS the Lab's deliberate leak")
    with open(os.path.abspath(__file__), encoding='utf-8') as handle:
        SOURCE = handle.read()
    PRODUCTION = SOURCE.split("if __name__ == '__main__':")[0]
    tree = ast.parse(PRODUCTION)
    imports = sorted({(node.module if isinstance(node, ast.ImportFrom)
                       else alias.name)
                      for node in ast.walk(tree)
                      if isinstance(node, (ast.Import, ast.ImportFrom))
                      for alias in node.names})
    code_only = '\n'.join(PRODUCTION.split('"""')[2::2])
    stores = [node for node in ast.walk(tree)
              if isinstance(node, ast.Attribute)
              and isinstance(node.ctx, ast.Store)]
    WORD = re.compile(chr(92) + 'b(open|high|low|volume)' + chr(92) + 'b')
    mark(imports == ['funding_fade', 'mood_fade', 'numpy',
                     'signals.funding_fade', 'signals.mood_fade']
         and not any(word in code_only for word in
                     ('open(', '.index', 'iloc', 'datetime', 'time.',
                      'global ', 'os.', 'sys.', 'eval', 'exec', '__import__'))
         and not WORD.search(code_only) and WORD.search("df['low']")
         and code_only.count("'close'") == 2 and len(stores) == 8,
         "the code imports numpy and the two crowd rules and nothing else; "
         "names no file, no clock, no date index; of the price columns it "
         "reads the CLOSE, twice (once in each rule) and no other; and "
         "stores eight things on itself, all when it is made")

    print("\n(g) >>> THE SABOTAGE DRILL: REAL TEXT EDITS TO THIS FILE'S OWN"
          "\n    CODE, EVERY RUN. INERT IS A FAIL.")

    def mutant(old, new, which='Confluence'):
        if PRODUCTION.count(old) != 1:
            return None
        space = {'__name__': 'mutant'}
        exec(compile(PRODUCTION.replace(old, new), '<mutant>', 'exec'), space)
        return space[which]()

    def witness(c_maker, y_maker):
        cases = [(UP, 'greedy'), (UP, 'mania'), (UP, 'scared'), (UP, 'panic'),
                 (UP, 'none'), (DOWN, 'greedy'), (DOWN, 'scared'),
                 (DOWN, 'panic'), (DOWN, 'none'), (UP, 'split'),
                 (DOWN, 'split'), (at_line, 'greedy'), (above, 'greedy'),
                 (below, 'scared'), (EDGE, 'scared'), (UP[:99], 'greedy')]
        return (tuple(said(frame(c, k), c_maker) for c, k in cases)
                + (said(frame(UP, 'scared'), y_maker),
                   said(frame(EDGE), y_maker),
                   said(frame(at_line), y_maker),
                   said(frame(UP[:99]), y_maker)))

    HONEST = witness(rule, yard)
    EXPECTED = ('long', 'long', 'flat', 'flat', 'flat', 'flat', 'short',
                'short', 'flat', 'long', 'short', 'flat', 'long', 'short',
                'short', 'flat', 'long', 'short', 'flat', 'flat')
    BREAKS = [
        ('S1', 'BUYING a scared crowd in an up-trend (the fade)',
         "if way > 0 and 'short' in crowd:", "if way > 0 and 'long' in crowd:"),
        ('S2', 'SELLING a greedy crowd in a down-trend (the fade)',
         "if way < 0 and 'long' in crowd:", "if way < 0 and 'short' in crowd:"),
        ('S3', 'the trend ignored on the buy side',
         "if way > 0 and 'short' in crowd:", "if 'short' in crowd:"),
        ('S4', 'the crowd ignored on the sell side',
         "if way < 0 and 'long' in crowd:", "if way < 0:"),
        ('S5', 'a close level with its average called an up-trend',
         'return 1 if last > average', 'return 1 if last >= average'),
        ('S6', 'a close level with its average called a down-trend',
         'else -1 if last < average', 'else -1 if last <= average'),
        ('S7', 'the average over 99 closes', 'TREND = 100 ', 'TREND = 99 '),
        ('S8', 'the average over 101 closes', 'TREND = 100 ', 'TREND = 101 '),
        ('S9', "the mood rule left out of the crowd",
         'crowd = (self.funding(df), self.mood(df))',
         "crowd = (self.funding(df), 'flat')"),
        ('S10', "the funding rule left out of the crowd",
         'crowd = (self.funding(df), self.mood(df))',
         "crowd = ('flat', self.mood(df))"),
        ('S11', 'the trend turned upside down', 'return 1 if last > average',
         'return -1 if last > average'),
        ('S12', "yesterday's close judged against the average",
         'last = float(window[-1])', 'last = float(window[-2])'),
    ]
    print()
    for tag, words, old, new in BREAKS:
        c_m, y_m = mutant(old, new), mutant(old, new, 'TrendOnly')
        if c_m is None or y_m is None:
            mark(False, f"{tag} {words:<50} -> THE EDIT DID NOT APPLY")
            continue
        broken = witness(c_m, y_m)
        good = broken != HONEST and broken != EXPECTED
        mark(good, f"{tag} {words:<50} -> "
                   f"{'CAUGHT' if good else 'INERT — IT CHANGED NOTHING'}")
    same_c = mutant("NAME = 'confluence", "NAME  = 'confluence")
    same_y = mutant("NAME = 'confluence", "NAME  = 'confluence", 'TrendOnly')
    mark(same_c is not None and witness(same_c, same_y) == HONEST == EXPECTED,
         "and an edit that changes NOTHING gives the twenty honest answers, "
         "which equal the twenty typed out here")

    print("\n(h) NOTHING REAL WAS OPENED, AND THE GATE COUNTS ITSELF.")
    mark(VAULT_OPENED == [] and 'funding_vault' not in sys.modules
         and 'mood_vault' not in sys.modules,
         "the Lab's door was never knocked on and no frozen folder's reader "
         "was loaded")
    mark(len(BREAKS) == 12, "twelve breaks, counted against a number typed "
                            "out here")
    EXPECTED_CHECKS = 30
    mark(len(nonlocal_ok) + 1 == EXPECTED_CHECKS,
         f"and this gate ran all {EXPECTED_CHECKS} of the checks it owes",
         f"it ran {len(nonlocal_ok) + 1}")

    ok = all(nonlocal_ok)
    reds = sum(1 for good in nonlocal_ok if not good)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 6.6-S PASSED — {len(nonlocal_ok)} checks, 0 red.

THE CONFLUENCE RULE IS THE ONE DECLARED: long when the close is above
its 100-close average AND the crowd is greedy by funding or by mood;
short when below AND the crowd is scared. The two crowd rules are
Slot 2's and Slot 3's own. The yardstick is the trend and nothing else.

A SECOND WRITING-OUT AGREED ON EVERY ONE OF 3,200 MADE-UP DAYS, AND
TWELVE REAL TEXT EDITS TO THIS FILE'S OWN CODE WERE EACH CAUGHT.

WHAT THIS GATE DOES **NOT** PROVE. That either rule makes money. That
100 is the right length - it was chosen on the training side, a rising
market, from a search of eight variants. And that anybody but its
author has read it.""")
    else:
        print(f"GATE 6.6-S FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
