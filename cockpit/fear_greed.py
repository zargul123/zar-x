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
    # =====================================================================
    # GATE 3.1-R — rebuilt 2026-07-26, after R-008 put this file under the
    # knife and FIVE OF SIX deliberate sabotages walked through the old
    # smoke test.
    #
    # The worst of them inverted the value: the line read "70 — Fear", a
    # contradiction on its own face, and every check passed. Extreme Fear
    # would have printed as Greed and the gate would have applauded.
    #
    # THE CAUSE, identical to the funding instrument's the same morning:
    # every check interrogated the PARSE — is the number in range, is the
    # label non-empty, did eight rows arrive — and NOT ONE compared the
    # printed sentence to the source. So the two rules from that audit
    # apply here too:
    #
    #   1. VERIFY WHAT THE PILOT READS. Expected strings are derived by this
    #      block's own arithmetic from a raw fetch, never by calling the
    #      helper under test.
    #   2. A CHECK NOBODY HAS TRIED TO BREAK IS A CHECK NOBODY HAS TESTED.
    #      All six sabotages are applied in memory on EVERY run and each
    #      must be caught.
    #
    # Everything lives inside `__main__` on purpose: the production path is
    # untouched, so what the Brief prints cannot have changed.
    # =====================================================================

    # =====================================================================
    # GATE 3.1-R2, added 2026-07-27 after an independent session threw five
    # NEW sabotages at Gate 3.1-R and THREE walked through.
    #
    # F7 turned the disclaimer into a recommendation — "buy when others are
    # fearful" — on the instrument whose whole reason for existing is
    # INFORMATION, NEVER A SIGNAL, and the gate passed. F8 appended
    # ">> strong buy signal" to the reading line and the gate passed. F9
    # credited the number to CNN Business, a source this ship has never
    # called, and the gate passed.
    #
    # THE CAUSE, identical to funding's the same day: every check asked "is
    # this expected string PRESENT?" — a substring test can never notice an
    # ADDITION, and nothing checked the fixed words at all. So the gate now
    # holds its OWN VERBATIM COPY of the wording and rebuilds the WHOLE block
    # for an EXACT-EQUALITY comparison.
    #
    # AND ONE MORE, EARNED THE SAME DAY: this block used to read
    # `HISTORY_LIMIT` from the module it is testing. Cutting that constant to
    # 2 disarmed sabotage F3, which then escaped its own drill. The gate now
    # holds its own copy and checks the module's against it — exactly what
    # `GATE_CONTRACTS` does for funding's tickers.
    # =====================================================================

    # =====================================================================
    # GATE 3.1-R3, added 2026-07-28 after an independent session threw a
    # TWELFTH sabotage at Gate 3.1-R2 and it walked through.
    #
    # R2 rebuilt the WHOLE block and demanded exact equality — ON THE HEALTHY
    # PATH ONLY. The OFFLINE path was still guarded the old way: are the
    # offline words present, are there two lines, is the header first. **All
    # three questions can be satisfied while a fabricated number rides along
    # on the end of the line.**
    #
    # F12 IS SABOTAGE F6 DONE PROPERLY. F6 — "offline path fabricates a
    # number" — is in the drill and is caught, but only because it DROPS the
    # offline words. F12 keeps them and appends the fabrication:
    #
    #     🔌 Fear & Greed instrument offline (ConnectionError) — last known
    #     reading 72 — Extreme Greed
    #
    # The true reading that day was 29 — Fear. The line the pilot would read
    # said Extreme Greed, on an instrument that had just admitted it could not
    # see anything, and the check underneath it said "nothing else printed".
    #
    # SO: THE OFFLINE PATH NOW GETS THE STANDARD THE HEALTHY PATH ALREADY HAS.
    # It is compared for EXACT EQUALITY against the gate's own verbatim copy,
    # because the only check that can enforce "nothing else" is equality.
    # =====================================================================

    GATE_LIMIT = 8          # the test's own copy; never read from the module
    GATE_HEADER = "  CONTEXT DECK"
    GATE_LINE2_PREFIX = "  Fear & Greed : "
    GATE_LINE3_DISCLAIMER = ("  (crowd-mood gauge from alternative.me — "
                             "information, not a signal)")

    # The offline block, held verbatim by the test. `_get` raises requests'
    # ConnectionError against the reserved .invalid domain, so the exception
    # name in the honest line is deterministic.
    #
    # =====================================================================
    # GATE 3.1-R4, added 2026-07-28 (evening) after an independent session
    # threw a THIRTEENTH sabotage at Gate 3.1-R3 and it walked through.
    #
    # **THIS LINE USED TO INTERPOLATE THE MODULE'S OWN `OFFLINE_WORDS`.** So it
    # was never a verbatim copy at all — it was a MIRROR. F13 changed that one
    # production constant to
    #
    #     "Fear & Greed instrument offline — last known reading 72 — Extreme Greed"
    #
    # and the gate's "own copy" changed itself to match, in lockstep. Equality
    # held against the lie, the drill scored F12 CAUGHT in the same run, and
    # section 4 printed the fabricated sentence on its own screen — directly
    # under a paragraph explaining that this exact sentence is what F12 said on
    # a day the index read 29 — Fear. Which it did again.
    #
    # `GATE_LIMIT` exists because reading `HISTORY_LIMIT` from the module
    # silently disarmed F3. **The identical mistake was sitting one constant
    # over the whole time.** The words are now typed out here, and the module's
    # are compared AGAINST them by a named check that says which one moved.
    # =====================================================================
    GATE_OFFLINE_WORDS = "Fear & Greed instrument offline"
    GATE_OFFLINE_BLOCK = (f"{GATE_HEADER}\n"
                          f"  🔌 {GATE_OFFLINE_WORDS} (ConnectionError)")

    def _raw_rows():
        """The source's own JSON, fetched by the TEST, passing through none
        of this file's helpers — and using the TEST'S OWN limit."""
        r = requests.get(FNG_URL, params={'limit': GATE_LIMIT},
                         timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()['data']

    def _expected_from(rows):
        """What the Brief OUGHT to print, built from raw. `_parse`,
        `_age_words` and `_context_words` are all deliberately not called —
        they are the things on trial."""
        dated = sorted(
            ((int(x['timestamp']), str(x['value']).strip(),
              str(x['value_classification']).strip()) for x in rows),
            reverse=True)
        newest_ts, newest_val, newest_lab = dated[0]
        newest_date = datetime.fromtimestamp(newest_ts, timezone.utc).date()
        ctx = []
        for i in (1, 7):
            if i < len(dated):
                ts, val, _ = dated[i]
                d = datetime.fromtimestamp(ts, timezone.utc).date()
                age = (newest_date - d).days
                words = ("yesterday" if age == 1 else
                         "a week ago" if age == 7 else f"{age} days ago")
                ctx.append(f"{words} {val}")
        return {'value': newest_val, 'label': newest_lab,
                'date': str(newest_date), 'context': ctx}

    def _expected_block(want):
        """The ENTIRE block the Brief ought to print, assembled from raw by
        this test's own arithmetic and its own wording. Compared for exact
        equality, so appended rubbish, a corrupted disclaimer or a swapped
        attribution all fail — none of which the old gate could see."""
        ctx = f"   ({' · '.join(want['context'])})" if want['context'] else ""
        return "\n".join([
            GATE_HEADER,
            f"{GATE_LINE2_PREFIX}{want['value']} — {want['label']}{ctx}"
            f"   [reading of {want['date']} UTC]",
            GATE_LINE3_DISCLAIMER,
        ])

    def _core_checks(verbose=True):
        """The checks that guard the printed sentence — and the detector the
        sabotage drill uses on itself.

        NO DRIFT TOLERANCE. alternative.me serves one reading per day and it
        does not move, so funding's before/after allowance is deliberately NOT
        copied here; a tolerance that exists for no reason is a hole with a
        comment on it. The one real boundary is the UTC day rolling over
        mid-run: on a mismatch the raw is re-fetched ONCE, and only a genuinely
        CHANGED newest date excuses it. The allowance is for the calendar,
        never for being wrong.
        """
        say = print if verbose else (lambda *a, **k: None)
        rows = _raw_rows()
        want = _expected_from(rows)
        live = section_text()
        # GATE 3.1-R4: the gate's own copy, never the module's. A guard that
        # asks the module what its own failure looks like stops recognising a
        # failure the moment the module renames it.
        if GATE_OFFLINE_WORDS in live:
            say("   ✗ live section came back offline — the sentence cannot be verified")
            return False

        def _judge():
            return [
                (f"Fear & Greed : {want['value']} — {want['label']}" in live,
                 f"value AND label together: "
                 f"{want['value']} — {want['label']}"),
                (f"[reading of {want['date']} UTC]" in live,
                 f"reading date: {want['date']}"),
            ] + [(c in live, f"context point: {c}") for c in want['context']]

        results = _judge()
        if not all(hit for hit, _ in results):
            rolled = _expected_from(_raw_rows())
            if rolled['date'] != want['date']:
                say(f"   … the UTC day rolled over mid-run "
                    f"({want['date']} → {rolled['date']}); re-comparing")
                want = rolled
                results = _judge()

        ok = True
        for hit, words in results:
            say(f"   {'✓' if hit else '✗'} {words} → the printed line "
                f"{'carries it' if hit else 'DOES NOT CARRY IT'}")
            ok = ok and hit

        # --- GATE 3.1-R2 (e): THE TEST'S OWN LIMIT vs THE MODULE'S ---------
        # Cutting HISTORY_LIMIT used to disarm the F3 detector silently.
        limit_ok = (HISTORY_LIMIT == GATE_LIMIT)
        say(f"   {'✓' if limit_ok else '✗'} the module's HISTORY_LIMIT "
            f"({HISTORY_LIMIT}) equals the gate's own copy ({GATE_LIMIT})")
        ok = ok and limit_ok

        # --- GATE 3.1-R2 (c): THE FIXED WORDS, GUARDED BY NAME -------------
        # Named separately from the block check so a failure says WHICH
        # sentence changed. "information, not a signal" is the ship's founding
        # rule printed on its own instrument; F7 rewrote it into advice and
        # every check passed.
        words_ok = GATE_LINE3_DISCLAIMER.strip() in live
        say(f"   {'✓' if words_ok else '✗'} fixed wording present verbatim: "
            f"{GATE_LINE3_DISCLAIMER.strip()!r}")
        ok = ok and words_ok

        # --- GATE 3.1-R2 (b): THE WHOLE BLOCK, EXACT EQUALITY --------------
        # The check that kills F8. "Contains" can never notice an ADDITION.
        want_block = _expected_block(want)
        block_ok = (live == want_block)
        say(f"   {'✓' if block_ok else '✗'} the WHOLE printed block equals the "
            f"block rebuilt from the source — nothing added, nothing removed")
        if not block_ok:
            for i, (got, exp) in enumerate(
                    zip_longest(live.splitlines(), want_block.splitlines(),
                                fillvalue=''), start=1):
                if got != exp:
                    say(f"      line {i} printed : {got!r}")
                    say(f"      line {i} expected: {exp!r}")
        return ok and block_ok

    def _offline_checks(verbose=True):
        """GATE 3.1-R3 (a): THE OFFLINE BLOCK, EXACT EQUALITY.

        The old bar asked three questions a fabricated number could answer
        correctly. **An instrument that has just admitted it cannot see
        anything must print NOTHING ELSE** — and "nothing else" is a claim only
        equality can enforce. This also becomes the judge for F6, which used to
        be scored by an inline special case in the drill: F6 drops the offline
        words, F12 keeps them, and one bar now catches both.

        GATE 3.1-R4 (b): AND THE WORDING THE BAR IS BUILT FROM IS NOW CHECKED
        AGAINST THE MODULE'S. Equality is only worth something if the thing
        being compared TO cannot move with the thing being tested. It could,
        and F13 moved it."""
        say = print if verbose else (lambda *a, **k: None)

        # --- GATE 3.1-R4 (b): THE MODULE'S WORDING vs THE GATE'S OWN COPY ---
        # Named separately so a failure says WHICH constant moved, rather than
        # leaving the next session to diff two long strings by eye.
        words_ok = (OFFLINE_WORDS == GATE_OFFLINE_WORDS)
        say(f"   {'✓' if words_ok else '✗'} the module's OFFLINE_WORDS equals "
            f"the gate's own copy ({GATE_OFFLINE_WORDS!r})")
        if not words_ok:
            say(f"      module : {OFFLINE_WORDS!r}")
            say(f"      gate   : {GATE_OFFLINE_WORDS!r}")

        drill = section_text(base_url=OFFLINE_DRILL_URL)
        hit = (drill == GATE_OFFLINE_BLOCK)
        say(f"   {'✓' if hit else '✗'} the offline block equals the gate's own "
            f"verbatim copy exactly — the header, one honest line, no "
            f"traceback, and NOTHING appended")
        if not hit:
            for i, (got, exp) in enumerate(
                    zip_longest(drill.splitlines(),
                                GATE_OFFLINE_BLOCK.splitlines(),
                                fillvalue=''), start=1):
                if got != exp:
                    say(f"      line {i} printed : {got!r}")
                    say(f"      line {i} expected: {exp!r}")
        return hit and words_ok

    # =====================================================================
    # GATE 3.1-R5, added 2026-07-28 (night) after an independent session threw
    # a FOURTEENTH sabotage at Gate 3.1-R4 and it walked through.
    #
    # **EVERY CHECK ABOVE INSPECTS THE STRING `section_text` RETURNS.**
    # `cockpit/brief.py` line 90 is `print(fear_greed_section())`, and the
    # function body runs BEFORE the print does. So anything this doorway writes
    # to stdout ITSELF lands on the Brief, directly above its block, where the
    # pilot reads it — and it appears in no returned string, so no equality
    # check can see it.
    #
    # F14 added one `print()` inside `section_text` and changed the returned
    # block by NOT ONE BYTE:
    #
    #     ⚠ extreme fear — historically a buying opportunity
    #
    # The gate reported all THIRTEEN sabotages CAUGHT and exited 0 — **in the
    # same run in which F7, "the disclaimer turned into ADVICE", was scored
    # CAUGHT.** The bar against advice was working perfectly on the one channel
    # it was pointed at, while advice walked in through the other.
    # =====================================================================
    import contextlib
    import io

    def _capture(call):
        """Run `call()` with BOTH streams captured. Returns what it wrote."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            call()
        return buf.getvalue()

    def _silence_checks(verbose=True):
        """GATE 3.1-R5: THE DOORWAY WRITES NOTHING OF ITS OWN.

        The Brief is assembled ONLY from what this compartment RETURNS. stderr
        counts too — it lands on the same terminal the pilot is reading.

        **BOTH paths the pilot can see are held to it**, live and offline: an
        instrument that has just admitted it cannot see anything must print
        nothing else through ANY channel. Only the `section_text` call is
        wrapped, never this gate's own reporting."""
        say = print if verbose else (lambda *a, **k: None)
        ok = True
        for name, call in (
                ('live   ', lambda: section_text()),
                ('offline', lambda: section_text(base_url=OFFLINE_DRILL_URL))):
            written = _capture(call)
            quiet = (written == '')
            say(f"   {'✓' if quiet else '✗'} {name} path: the doorway wrote "
                f"NOTHING to stdout or stderr of its own — the Brief prints "
                f"only what it RETURNS")
            if not quiet:
                say(f"      it wrote: {written!r}")
            ok = ok and quiet
        return ok

    # Imported here rather than at the top so the diff stays inside __main__
    # and the production path is provably untouched.
    from datetime import timedelta
    from itertools import zip_longest

    # The sabotages that wrap a real function need a handle on it, captured
    # before anything is swapped.
    _PARSE_ORIGINAL = _parse
    _SECTION_TEXT_ORIGINAL = section_text
    _CONTEXT_WORDS_ORIGINAL = _context_words
    _GET_ORIGINAL = _get

    # The six from R-008, kept by name so the fix stays legible. The last
    # column is WHICH JUDGE decides: F6 and F12 corrupt only the offline path,
    # which the live core checks cannot see, so judging them by the core checks
    # would record two guaranteed escapes as if the gate were blind.
    _SABOTAGES = [
        ('F1', '_parse — value inverted', 'ESCAPED', '_parse',
         lambda payload: [dict(r, value=100 - r['value'])
                          for r in _PARSE_ORIGINAL(payload)], 'core'),
        ('F2', '_parse — label decoupled', 'ESCAPED', '_parse',
         lambda payload: [dict(r, label='Extreme Greed')
                          for r in _PARSE_ORIGINAL(payload)], 'core'),
        ('F3', '_age_words — all ages "yesterday"', 'ESCAPED', '_age_words',
         lambda days: "yesterday", 'core'),
        ('F4', '_parse — date shifted 3 days', 'ESCAPED', '_parse',
         lambda payload: [dict(r, date=r['date'] + timedelta(days=3))
                          for r in _PARSE_ORIGINAL(payload)], 'core'),
        ('F5', 'section_text — yesterday as today', 'ESCAPED', '_parse',
         lambda payload: _PARSE_ORIGINAL(payload)[1:], 'core'),
        # F6 swaps the doorway itself: the only way to make the offline path
        # lie is to replace the thing that writes it.
        ('F6', 'offline path fabricates a number', 'caught', 'section_text',
         lambda base_url=None, limit=None, timeout=None:
             f"{HEADER}\n  Fear & Greed : 50 — Neutral   [reading unavailable]",
         'offline'),
        # F7-F11, from the independent review of 2026-07-27. Three of these
        # five walked through Gate 3.1-R. They corrupt the OUTPUT rather than
        # editing the file, because that is what a drill running inside the
        # file can do; the proof the repair works is the scratch rig, which
        # edits the file for real — Gate 3.1-R2 check (i).
        ('F7', 'the disclaimer turned into ADVICE', 'ESCAPED', 'section_text',
         lambda *a, **k: _SECTION_TEXT_ORIGINAL(*a, **k).replace(
             'information, not a signal', 'buy when others are fearful'),
         'core'),
        ('F8', 'rubbish appended to the reading line', 'ESCAPED',
         'section_text',
         lambda *a, **k: _SECTION_TEXT_ORIGINAL(*a, **k).replace(
             ' UTC]', ' UTC]   >> strong buy signal'), 'core'),
        ('F9', 'credited to a source never called', 'ESCAPED', 'section_text',
         lambda *a, **k: _SECTION_TEXT_ORIGINAL(*a, **k).replace(
             'from alternative.me', 'from CNN Business'), 'core'),
        ('F10', 'the two context values swapped', 'caught', '_context_words',
         lambda readings: _CONTEXT_WORDS_ORIGINAL(
             [readings[0]]
             + [dict(readings[7], date=readings[1]['date'])]
             + readings[2:7]
             + [dict(readings[1], date=readings[7]['date'])]
             + readings[8:]) if len(readings) > 7
             else _CONTEXT_WORDS_ORIGINAL(readings), 'core'),
        # F11 forces the INSTRUMENT to fetch two days while the gate still
        # fetches eight, so the week-ago context point silently disappears.
        # Sabotaging the constant instead would move both and prove nothing —
        # that is the trap the gate's own GATE_LIMIT now closes.
        ('F11', 'a week of history silently lost', 'caught', '_get',
         lambda base_url, limit, timeout: _GET_ORIGINAL(base_url, 2, timeout),
         'core'),
        # F12, from the independent review of 2026-07-28. It walked through
        # Gate 3.1-R2. **It is F6 done properly:** F6 is caught only because it
        # DROPS the offline words, so the bar never had to prove it could
        # notice an ADDITION. Keep the honest words, append the fabrication,
        # and the pilot reads Extreme Greed on a day the index says Fear.
        ('F12', 'offline line keeps the words AND fabricates', 'ESCAPED',
         'section_text',
         lambda *a, **k: (_SECTION_TEXT_ORIGINAL(*a, **k)
                          + " — last known reading 72 — Extreme Greed"
                          if OFFLINE_WORDS in _SECTION_TEXT_ORIGINAL(*a, **k)
                          else _SECTION_TEXT_ORIGINAL(*a, **k)), 'offline'),
        # F13, from the independent review of 2026-07-28 (evening). It walked
        # through Gate 3.1-R3. **It changes no logic whatsoever** — it rewords
        # one production constant, and the gate's "verbatim copy" of the offline
        # line, which interpolated that same constant, followed it into the lie
        # and confirmed it. It is F12's exact payload delivered through the door
        # the check against F12 was holding open. The pilot reads "Extreme
        # Greed" from an instrument that has just said it cannot see anything.
        ('F13', 'the offline WORDS themselves reworded', 'ESCAPED',
         'OFFLINE_WORDS',
         "Fear & Greed instrument offline — last known reading 72 — Extreme Greed",
         'offline'),
        # F14, from the independent review of 2026-07-28 (night). It walked
        # through Gate 3.1-R4. **It corrupts no string this gate had ever
        # inspected** — the returned block stays byte-identical and the advice
        # reaches the Brief through stdout, because `brief.py` runs this
        # function before it prints what the function returns. It was scored
        # green in the same run that scored F7 — "the disclaimer turned into
        # ADVICE" — as CAUGHT.
        ('F14', 'the doorway PRINTS advice of its own', 'ESCAPED',
         'section_text',
         lambda *a, **k: (
             print("  ⚠ extreme fear — historically a buying opportunity")
             or _SECTION_TEXT_ORIGINAL(*a, **k)), 'silence'),
    ]

    def _sabotage_drill():
        """EXHIBIT A, MADE PERMANENT. Break this file on purpose, one way at a
        time, and require the checks above to FAIL each time."""
        ok = True
        for tag, words, old, attr, repl, judge in _SABOTAGES:
            original = globals()[attr]
            globals()[attr] = repl
            try:
                # F6 used to be judged by an inline copy of the old offline bar
                # — "the words are present, two lines, header first" — which is
                # exactly the bar F12 then satisfied while lying. Both are now
                # judged by the same exact-equality check, so the drill proves
                # THE CHECK rather than a weaker copy of it.
                survived = {'offline': _offline_checks,
                            'silence': _silence_checks}.get(
                    judge, _core_checks)(verbose=False)
            except Exception:
                survived = False        # a crash is a catch: it did not pass
            finally:
                globals()[attr] = original
            caught = not survived
            print(f"   {'✓' if caught else '✗'} {tag:<4} {words:<42} "
                  f"[old gate: {old:<7}] → "
                  f"{'CAUGHT' if caught else 'ESCAPED AGAIN — GATE IS DECORATIVE'}")
            ok = ok and caught
        restored = (_core_checks(verbose=False) and _offline_checks(verbose=False)
                    and _silence_checks(verbose=False))
        print(f"   {'✓' if restored else '✗'} every original restored — the "
              f"clean checks pass again afterwards")
        return ok and restored

    ok = True
    print("GATE 3.1-R5 — the Fear & Greed instrument's self-test, hardened")
    print("2026-07-28 (night). Version 1 let five of six deliberate lies")
    print("through. Version 2 printed '>> strong buy signal' on the deck of an")
    print("information-only ship. Version 3 held both paths to exact equality —")
    print("but built the offline bar out of the MODULE'S OWN wording, so")
    print("rewording that one constant moved the lie and the bar together and")
    print("the gate confirmed it. Version 4 holds its own copy and checks the")
    print("module's against it. Version 5: all four of those judged the string")
    print("this doorway RETURNS, and the Brief prints TWO channels — advice")
    print("written straight to stdout reached the pilot completely unwatched.")

    print("\n1) LIVE SECTION — what the Brief will print")
    try:
        readings = _parse(_get(FNG_URL, HISTORY_LIMIT, TIMEOUT))
        now = readings[0]
        print(f"   fetched {len(readings)} daily readings, "
              f"{readings[-1]['date']} → {now['date']} (UTC)")
        checks = [
            (0 <= now['value'] <= 100, f"value {now['value']} is within 0-100"),
            # NOTE: these two are WEAK on their own — an inverted value stays
            # in range and a wrong label is still a non-empty string. Section 2
            # is what actually guards the sentence.
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
    if GATE_OFFLINE_WORDS in live:      # the gate's own copy — see 3.1-R4 (b)
        print("   ✗ the live section came back offline")
        ok = False

    print("\n2) THE PRINTED SENTENCE vs THE SOURCE (Gate 3.1-R b, c) — the"
          "\n   check whose absence let five lies through. Every expected"
          "\n   string is derived by this block's own arithmetic from raw"
          "\n   JSON; no helper of the instrument judges the instrument."
          "\n   The value and its label are checked TOGETHER, because a"
          "\n   number beside the wrong words is the defect F2 exposed.")
    ok = _core_checks(verbose=True) and ok

    print("\n3) EXHIBIT A, MADE PERMANENT (Gate 3.1-R d · 3.1-R2 f · 3.1-R3 b ·"
          "\n   3.1-R4 d · 3.1-R5 c) — the file is broken FOURTEEN ways and each"
          "\n   break MUST be caught. Five of the first six escaped the gate of"
          "\n   2026-07-26; three of the next five escaped the gate of the day"
          "\n   after; the twelfth escaped the gate of 2026-07-27 by hiding on"
          "\n   the one path it only counted; and the THIRTEENTH escaped the"
          "\n   gate of 2026-07-28 by rewording a constant the gate was reading"
          "\n   its own expectation out of.")
    ok = _sabotage_drill() and ok

    print("\n4) OFFLINE DRILL (Gate 3.1-R3 a) — injected unreachable URL,"
          "\n   internet untouched. Judged by EXACT EQUALITY against the gate's"
          "\n   own verbatim copy: sabotage F12 appended '— last known reading"
          "\n   72 — Extreme Greed' to this line, on a day the index read 29 —"
          "\n   Fear, and the old bar called it 'nothing else printed'.")
    print(f"   pointing the instrument at {OFFLINE_DRILL_URL}")
    print()
    print(section_text(base_url=OFFLINE_DRILL_URL))
    drill_ok = _offline_checks(verbose=True)
    ok = ok and drill_ok

    print("\n5) THE SILENT-DOORWAY CHECK (Gate 3.1-R5 a, b) — the Brief is"
          "\n   assembled ONLY from what this compartment RETURNS. Sabotage F14"
          "\n   printed 'historically a buying opportunity' straight to stdout,"
          "\n   left the returned block byte-identical, and walked through every"
          "\n   check in this file — in the same run that scored F7, 'the"
          "\n   disclaimer turned into ADVICE', as CAUGHT. Held on BOTH paths,"
          "\n   and stderr counts: it reaches the same terminal.")
    silent_ok = _silence_checks(verbose=True)
    ok = ok and silent_ok

    if ok:
        print("\nGATE 3.1-R5 PASSED — the WHOLE printed block was rebuilt from "
              "the\nsource and matched exactly on BOTH paths the pilot can see "
              "— live\nand offline — the disclaimer was checked verbatim, the "
              "gate's own\nhistory limit AND its own offline wording were both "
              "compared to the\nmodule's, THE DOORWAY WAS PROVED SILENT ON BOTH "
              "PATHS so the Brief\ncarries only what it RETURNS, and all "
              "FOURTEEN deliberate sabotages\nwere caught. Every expectation in "
              "this gate is typed out here rather\nthan read from the file on "
              "trial. This test has demonstrated, this\nrun, that it is able to "
              "say no.")
    else:
        print("\nGATE 3.1-R5 FAILED — see the ✗ lines above.")
    sys.exit(0 if ok else 1)
