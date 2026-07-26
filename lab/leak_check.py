"""
Zar X Lab — LAW 7's INSTRUMENT: THE LEAK CHECK (finds smuggled data).

WHY THIS EXISTS (Gate 2.5's finding, 2026-07-26)
The Lab's numbers catch overfitting. They CANNOT catch a leak: a strategy fed
the answers answers correctly everywhere, hold-out included, and Gate 2.5
measured exactly that — `PerfectForesight` cleared every locked Phase 6 bar
(PF 1.39, walk-forward CONSISTENT 6 of 6, Monte Carlo 8.01%) and the too-good
alarm stayed SILENT (1.39 < 2, 57.6% < 70%). A modest leak produces modest,
certifiable numbers. The defence is a human reading the strategy's code —
that is Law 7 — and THIS instrument exists to make that reading harder to
fool: it walks the strategy OBJECT and reports any candle-shaped data it
carries around the engine's feed.

WHAT IT FINDS
The most common shape of leak: data smuggled inside the strategy itself —
a DataFrame in an attribute (PerfectForesight keeps `self.full`), an array in
a closure, a global table the function reads. The scan walks attributes,
closure cells, function defaults and referenced module globals, bounded and
deterministic, and reports every DataFrame / Series / datetime index / large
numeric array it can reach, with its shape and (when dated) its time span —
so the reader can see at once whether a strategy is carrying candles it was
never handed.

WHAT IT CAN NEVER PROVE — READ THIS BEFORE TRUSTING ANY CLEAN SCAN
A clean scan is NOT innocence. This instrument can only find data an object
CARRIES AT SCAN TIME. It cannot see a strategy that opens a file when called,
calls an API, rebuilds the future from something it stashed in compressed
form, or cheats in any way its author bothered to hide. There is no scanner
that makes reading the code unnecessary, and any session that treats this
report as a substitute for Law 7's reading is breaking the law it was built
to serve. The scan narrows the hunt; the reading is the verdict.

RUN (from the zar-x folder):
    set PYTHONUTF8=1
    C:\\Users\\hp\\miniconda3\\envs\\tfdml\\python.exe lab\\leak_check.py
"""
import inspect
import os
import sys

import numpy as np
import pandas as pd

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LAB_DIR)
sys.path.insert(0, os.path.dirname(LAB_DIR))

MAX_DEPTH = 6            # how deep the walk follows attributes/containers
MAX_ITEMS = 5000         # how many entries of one container it will look at
ARRAY_THRESHOLD = 32     # a numeric array this long is "data", not a setting


def _describe(obj):
    """A deterministic one-line description — types and shapes, never memory
    addresses, so two scans of the same object print the same report."""
    if isinstance(obj, pd.DataFrame):
        d = f'DataFrame {len(obj):,} rows x {obj.shape[1]} cols'
        if len(obj) and isinstance(obj.index, pd.DatetimeIndex):
            d += f', index {obj.index[0]} -> {obj.index[-1]}'
        return d
    if isinstance(obj, pd.Series):
        d = f'Series {len(obj):,} values'
        if len(obj) and isinstance(obj.index, pd.DatetimeIndex):
            d += f', index {obj.index[0]} -> {obj.index[-1]}'
        return d
    if isinstance(obj, pd.DatetimeIndex):
        d = f'DatetimeIndex {len(obj):,} timestamps'
        if len(obj):
            d += f', {obj[0]} -> {obj[-1]}'
        return d
    if isinstance(obj, np.ndarray):
        return f'ndarray shape {obj.shape} dtype {obj.dtype}'
    return type(obj).__name__


def _is_candle_shaped(obj):
    """Is this the kind of object market data lives in?"""
    if isinstance(obj, (pd.DataFrame, pd.Series, pd.DatetimeIndex)):
        return True
    if isinstance(obj, np.ndarray):
        return (obj.size >= ARRAY_THRESHOLD
                and obj.dtype.kind in ('f', 'i', 'u', 'M'))
    return False


def _walk(obj, path, depth, visited, findings):
    if depth > MAX_DEPTH or id(obj) in visited:
        return
    visited.add(id(obj))

    if _is_candle_shaped(obj):
        findings.append((path, _describe(obj)))
        return                      # found data; no need to look inside it
    if isinstance(obj, (str, bytes, int, float, bool, type(None))):
        return

    # containers
    if isinstance(obj, dict):
        for i, (k, v) in enumerate(obj.items()):
            if i >= MAX_ITEMS:
                break
            _walk(v, f'{path}[{k!r}]', depth + 1, visited, findings)
        return
    if isinstance(obj, (list, tuple, set, frozenset)):
        for i, v in enumerate(sorted(obj, key=repr) if isinstance(
                obj, (set, frozenset)) else obj):
            if i >= MAX_ITEMS:
                break
            _walk(v, f'{path}[{i}]', depth + 1, visited, findings)
        return

    # functions and methods: closures, defaults, and the module globals the
    # code actually names (a global table is a classic hiding place)
    if inspect.ismethod(obj):
        _walk(obj.__self__, f'{path}.__self__', depth + 1, visited, findings)
        obj = obj.__func__
    if inspect.isfunction(obj):
        if obj.__closure__:
            names = obj.__code__.co_freevars
            for name, cell in zip(names, obj.__closure__):
                try:
                    _walk(cell.cell_contents, f'{path}<closure {name}>',
                          depth + 1, visited, findings)
                except ValueError:
                    pass
        for i, v in enumerate(obj.__defaults__ or ()):
            _walk(v, f'{path}<default {i}>', depth + 1, visited, findings)
        for k, v in (obj.__kwdefaults__ or {}).items():
            _walk(v, f'{path}<kwdefault {k}>', depth + 1, visited, findings)
        for name in obj.__code__.co_names:
            g = obj.__globals__.get(name)
            if g is not None and not inspect.ismodule(g) \
                    and not isinstance(g, type):
                _walk(g, f'{path}<global {name}>', depth + 1, visited,
                      findings)
        _walk(getattr(obj, '__dict__', {}) or {}, f'{path}.__dict__',
              depth + 1, visited, findings)
        return

    # ordinary objects: their attributes, and their __call__ if they have one
    d = getattr(obj, '__dict__', None)
    if isinstance(d, dict):
        for k, v in d.items():
            _walk(v, f'{path}.{k}', depth + 1, visited, findings)
    call = getattr(type(obj), '__call__', None)
    if inspect.isfunction(call):
        _walk(call, f'{path}.__call__', depth + 1, visited, findings)


class LeakReport:

    def __init__(self, target_name, findings):
        self.target = target_name
        self.findings = sorted(findings)
        self.flagged = len(self.findings) > 0

    def text(self):
        L = []
        L.append('=' * 78)
        L.append(f'LEAK CHECK — {self.target}')
        L.append('=' * 78)
        L.append('  The scan walks the strategy object itself — attributes, '
                 'closures, defaults,')
        L.append('  referenced globals — hunting for candle-shaped data it '
                 'carries AROUND the')
        L.append("  engine's feed. The engine controls what the feed "
                 'delivers; it cannot control')
        L.append('  what an author hands their own object. This looks for '
                 'exactly that.')
        L.append('')
        if self.flagged:
            L.append(f'  !! CARRIES ITS OWN DATA — {len(self.findings)} '
                     f'finding(s). A LEAK IS POSSIBLE.')
            for path, desc in self.findings:
                L.append(f'  !!   {path}')
                L.append(f'  !!       -> {desc}')
            L.append('')
            L.append('  A strategy has no honest reason to carry candles the '
                     'engine did not hand')
            L.append('  it this call. Until a reading of the code explains '
                     'every line above, this')
            L.append("  strategy's results are not evidence and it does not "
                     'enter certification.')
        else:
            L.append('  no smuggled data found: the object carries no '
                     'DataFrame, no Series, no')
            L.append('  datetime index, no large numeric array — in any '
                     'attribute, closure,')
            L.append('  default, or referenced global this scan could reach.')
            L.append('')
            L.append('  THIS IS NOT INNOCENCE. The scan only sees what the '
                     'object CARRIES at scan')
            L.append('  time; a strategy can still open a file when called, '
                     'call an API, or hide')
            L.append('  data in a form this walk does not recognise. LAW 7 '
                     'STANDS: the code gets')
            L.append('  READ, line by line, and the reading gets recorded, '
                     'before any result is')
            L.append('  trusted. The scan narrows the hunt; the reading is '
                     'the verdict.')
        L.append('=' * 78)
        return '\n'.join(L)


def leak_check(strategy, name=None):
    """Scan one strategy object. Returns a LeakReport with .flagged/.text()."""
    target = name or getattr(strategy, 'name', None) or getattr(
        strategy, '__name__', type(strategy).__name__)
    findings = []
    _walk(strategy, 'strategy', 0, set(), findings)
    return LeakReport(target, findings)


# --------------------------------------------------------------------------
# The smoke test (Law 3: every part proves itself alive on its own)
# --------------------------------------------------------------------------

_SMOKE_DF = None      # a module global used by one smoke-test dummy below


def _smoke():
    global _SMOKE_DF
    from dummies import MACross, PerfectForesight, always_flat, peek_or_guess

    # candle-shaped synthetic data, clearly labelled: never written anywhere,
    # never a market claim — it exists so this smoke test needs no vault file
    idx = pd.date_range('2024-01-01', periods=200, freq='4h')
    base = 100.0 + np.arange(200) * 0.1
    df = pd.DataFrame({'open': base, 'high': base + 1.0,
                       'low': base - 1.0, 'close': base + 0.5}, index=idx)

    failures = []

    def expect(label, strategy, should_flag):
        rep = leak_check(strategy)
        print(rep.text())
        print()
        ok = rep.flagged == should_flag
        print(f'  [{"OK" if ok else "FAIL"}] {label}: expected '
              f'{"FLAGGED" if should_flag else "clean"}, scan says '
              f'{"FLAGGED" if rep.flagged else "clean"}')
        print()
        if not ok:
            failures.append(label)
        return rep

    print(__doc__)
    print('SMOKE TEST — four honest shapes and three known smugglers, all on '
          'synthetic\ncandles built in memory for this test only.\n')

    expect('MACross carries only its two integers', MACross(20, 50), False)
    expect('always_flat carries nothing', always_flat, False)
    expect('peek_or_guess carries nothing (its cheat needs the feed)',
           peek_or_guess, False)

    rep = expect('PerfectForesight carries the whole file (THE Gate 2.5 leak)',
                 PerfectForesight(df), True)
    if rep.flagged and not any('full' in p for p, _ in rep.findings):
        failures.append('PerfectForesight flagged for the wrong attribute')

    hidden = df['close'].values
    def closure_smuggler(view, _stash=hidden):
        return 'flat'
    closure_smuggler.name = 'closure-smuggler'
    expect('a function with an array hidden in a default argument',
           closure_smuggler, True)

    _SMOKE_DF = df
    def global_smuggler(view):
        return 'flat' if _SMOKE_DF is None else 'flat'
    global_smuggler.name = 'global-smuggler'
    expect('a function reading a module-global DataFrame', global_smuggler,
           True)

    class AttrSmuggler:
        name = 'attribute-smuggler'
        def __init__(self, d):
            self.notes = {'harmless': 1, 'tucked_away': [1, 2, (d,)]}
        def __call__(self, view):
            return 'flat'
    expect('a DataFrame buried two containers deep in an attribute',
           AttrSmuggler(df), True)

    # determinism: the same object scanned twice prints the same report
    r1, r2 = leak_check(PerfectForesight(df)), leak_check(PerfectForesight(df))
    same = r1.text() == r2.text()
    print(f'  [{"OK" if same else "FAIL"}] two scans of the same shape of '
          f'object print identical reports')
    if not same:
        failures.append('determinism')

    print()
    if failures:
        print(f'SMOKE TEST FAILED: {failures}')
        return 1
    print('SMOKE TEST PASSED: 3 honest shapes clean, 4 smugglers flagged, '
          'reports deterministic.')
    return 0


if __name__ == '__main__':
    sys.exit(_smoke())
