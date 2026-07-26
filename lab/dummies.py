"""
Zar X Lab — the three dummies of Gate 2.3.

These are NOT strategies anyone would trade. They are test instruments: each
one is designed to make the engine misbehave in a specific way, so that when
the engine does NOT misbehave we have earned the right to believe it.

  always_flat        — never trades. If this produces a single trade or a
                       single cent of P&L, the engine invents trades.
  MACross(20, 50)    — an ordinary, honest, unimpressive strategy. It exists
                       to prove the engine can produce a complete stat card
                       with costs visibly subtracted. Step 2.4's lie detectors
                       will be run on this same dummy.
  peek_at_tomorrow   — THE CHEAT. It tries to read the NEXT candle's close.
                       Fed the future it prints money; through the engine's
                       feed it must find nothing to read.
  PerfectForesight   — the same cheat WITH the future handed to it directly
                       (it keeps a reference to the whole file). This is what
                       a leak looks like when it succeeds.
  peek_or_guess      — the cheat with a fallback: when the peek fails it
                       shrugs and guesses. This shows what the cheat DEGRADES
                       to once the future is taken away — noise, not profit.

Every strategy here obeys the one contract:  signal(df) -> long|short|flat
where df is candles up to and including now, and nothing else.
"""


# --------------------------------------------------------------------------
# Dummy 1 — the strategy that does nothing
# --------------------------------------------------------------------------

def always_flat(df):
    """Never takes a position. The engine must report exactly 0 trades."""
    return 'flat'


always_flat.params = {}


# --------------------------------------------------------------------------
# Dummy 2 — an ordinary moving-average cross
# --------------------------------------------------------------------------

class MACross:
    """Classic 20/50 moving-average cross.

    Signals only on the CROSS ITSELF (the candle where the fast average
    changes side), not on every candle the fast average happens to be above
    the slow one. Uses only the closes it was given — the last value of each
    average is computed from the last candle backwards.
    """

    def __init__(self, fast=20, slow=50):
        if fast >= slow:
            raise ValueError('the fast average must be shorter than the slow one')
        self.fast = fast
        self.slow = slow
        self.params = {'fast': fast, 'slow': slow, 'kind': 'sma_cross'}
        self.name = f'ma-cross-{fast}-{slow}'

    def __call__(self, df):
        if len(df) < self.slow + 1:
            return 'flat'                      # not enough history yet
        close = df['close']
        fast_now = close.iloc[-self.fast:].mean()
        slow_now = close.iloc[-self.slow:].mean()
        fast_prev = close.iloc[-self.fast - 1:-1].mean()
        slow_prev = close.iloc[-self.slow - 1:-1].mean()
        if fast_prev <= slow_prev and fast_now > slow_now:
            return 'long'                      # golden cross, this candle
        if fast_prev >= slow_prev and fast_now < slow_now:
            return 'short'                     # death cross, this candle
        return 'flat'


# --------------------------------------------------------------------------
# Dummy 3 — THE CHEAT
# --------------------------------------------------------------------------

def peek_at_tomorrow(df):
    """THE CHEAT, honest version.

    It asks for candle i+1 — the one after "now" — out of the DataFrame the
    engine handed it. `df.iloc[len(df)]` is exactly one row past the end.

    Through the engine's feed that row does not exist: the engine passes a
    private copy containing candles 0..i and nothing more. So the lookup
    raises IndexError, the cheat has nothing to trade on, and it goes flat.
    That IndexError IS the wall. It is not caught by the engine and hidden —
    it is caught here, by the cheat itself, which then has to admit it is
    blind.
    """
    try:
        tomorrow = df['close'].iloc[len(df)]      # <-- the peek at candle i+1
    except IndexError:
        return 'flat'                             # the future was not there
    return 'long' if tomorrow > df['close'].iloc[-1] else 'short'


peek_at_tomorrow.params = {'peek': 'next candle close'}


class PerfectForesight:
    """THE CHEAT WITH THE FUTURE IN ITS POCKET.

    Constructed with the WHOLE file, so it does not need the engine's feed to
    see tomorrow — it looks the candle up by timestamp in its own private
    copy of everything. This is what a real leak looks like: the strategy is
    not reaching past the engine, the future was handed to it around the side.

    It exists to prove the cheat's LOGIC works. When the identical logic
    returns garbage through the engine's feed, the difference is the feed.
    """

    def __init__(self, full_df):
        self.full = full_df                       # <-- THE LEAK, deliberate
        self.params = {'peek': 'next candle close', 'source': 'the whole file'}
        self.name = 'cheat-perfect-foresight'

    def __call__(self, df):
        now = df.index[-1]
        i = self.full.index.get_loc(now)
        if i + 1 >= len(self.full):
            return 'flat'
        tomorrow = self.full['close'].iloc[i + 1]
        return 'long' if tomorrow > df['close'].iloc[-1] else 'short'


def peek_or_guess(df):
    """THE CHEAT THAT REFUSES TO GIVE UP.

    Same peek. But when the future is missing it does not go flat — it guesses
    that the last move continues. This is the honest picture of what a
    look-ahead strategy is once the look-ahead is removed: an ordinary,
    unremarkable momentum guess. Its stat card is the difference between a
    cheat and a strategy.
    """
    try:
        tomorrow = df['close'].iloc[len(df)]      # <-- the same peek
        return 'long' if tomorrow > df['close'].iloc[-1] else 'short'
    except IndexError:
        pass
    if len(df) < 2:
        return 'flat'
    close = df['close']
    return 'long' if close.iloc[-1] > close.iloc[-2] else 'short'


peek_or_guess.params = {'peek': 'next candle close',
                        'fallback': 'last move continues'}
