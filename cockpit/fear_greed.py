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

    GATE_LIMIT = 8          # the test's own copy; never read from the module
    GATE_HEADER = "  CONTEXT DECK"
    GATE_LINE2_PREFIX = "  Fear & Greed : "
    GATE_LINE3_DISCLAIMER = ("  (crowd-mood gauge from alternative.me — "
                             "information, not a signal)")

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
        if OFFLINE_WORDS in live:
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

    # The six from R-008, kept by name so the fix stays legible.
    _SABOTAGES = [
        ('F1', '_parse — value inverted', 'ESCAPED', '_parse',
         lambda payload: [dict(r, value=100 - r['value'])
                          for r in _PARSE_ORIGINAL(payload)]),
        ('F2', '_parse — label decoupled', 'ESCAPED', '_parse',
         lambda payload: [dict(r, label='Extreme Greed')
                          for r in _PARSE_ORIGINAL(payload)]),
        ('F3', '_age_words — all ages "yesterday"', 'ESCAPED', '_age_words',
         lambda days: "yesterday"),
        ('F4', '_parse — date shifted 3 days', 'ESCAPED', '_parse',
         lambda payload: [dict(r, date=r['date'] + timedelta(days=3))
                          for r in _PARSE_ORIGINAL(payload)]),
        ('F5', 'section_text — yesterday as today', 'ESCAPED', '_parse',
         lambda payload: _PARSE_ORIGINAL(payload)[1:]),
        # F6 swaps the doorway itself: the only way to make the offline path
        # lie is to replace the thing that writes it.
        ('F6', 'offline path fabricates a number', 'caught', 'section_text',
         lambda base_url=None, limit=None, timeout=None:
             f"{HEADER}\n  Fear & Greed : 50 — Neutral   [reading unavailable]"),
        # F7-F11, from the independent review of 2026-07-27. Three of these
        # five walked through Gate 3.1-R. They corrupt the OUTPUT rather than
        # editing the file, because that is what a drill running inside the
        # file can do; the proof the repair works is the scratch rig, which
        # edits the file for real — Gate 3.1-R2 check (i).
        ('F7', 'the disclaimer turned into ADVICE', 'ESCAPED', 'section_text',
         lambda *a, **k: _SECTION_TEXT_ORIGINAL(*a, **k).replace(
             'information, not a signal', 'buy when others are fearful')),
        ('F8', 'rubbish appended to the reading line', 'ESCAPED',
         'section_text',
         lambda *a, **k: _SECTION_TEXT_ORIGINAL(*a, **k).replace(
             ' UTC]', ' UTC]   >> strong buy signal')),
        ('F9', 'credited to a source never called', 'ESCAPED', 'section_text',
         lambda *a, **k: _SECTION_TEXT_ORIGINAL(*a, **k).replace(
             'from alternative.me', 'from CNN Business')),
        ('F10', 'the two context values swapped', 'caught', '_context_words',
         lambda readings: _CONTEXT_WORDS_ORIGINAL(
             [readings[0]]
             + [dict(readings[7], date=readings[1]['date'])]
             + readings[2:7]
             + [dict(readings[1], date=readings[7]['date'])]
             + readings[8:]) if len(readings) > 7
             else _CONTEXT_WORDS_ORIGINAL(readings)),
        # F11 forces the INSTRUMENT to fetch two days while the gate still
        # fetches eight, so the week-ago context point silently disappears.
        # Sabotaging the constant instead would move both and prove nothing —
        # that is the trap the gate's own GATE_LIMIT now closes.
        ('F11', 'a week of history silently lost', 'caught', '_get',
         lambda base_url, limit, timeout: _GET_ORIGINAL(base_url, 2, timeout)),
    ]

    def _sabotage_drill():
        """EXHIBIT A, MADE PERMANENT. Break this file on purpose, one way at a
        time, and require the checks above to FAIL each time."""
        ok = True
        for tag, words, old, attr, repl in _SABOTAGES:
            original = globals()[attr]
            globals()[attr] = repl
            try:
                if tag == 'F6':
                    # judged by the ORIGINAL offline bar: the honest words, two
                    # lines, header first
                    drill = section_text(base_url=OFFLINE_DRILL_URL)
                    lines = drill.splitlines()
                    survived = (OFFLINE_WORDS in drill and len(lines) == 2
                                and lines[0] == HEADER)
                else:
                    survived = _core_checks(verbose=False)
            except Exception:
                survived = False        # a crash is a catch: it did not pass
            finally:
                globals()[attr] = original
            caught = not survived
            print(f"   {'✓' if caught else '✗'} {tag:<4} {words:<36} "
                  f"[old gate: {old:<7}] → "
                  f"{'CAUGHT' if caught else 'ESCAPED AGAIN — GATE IS DECORATIVE'}")
            ok = ok and caught
        restored = _core_checks(verbose=False)
        print(f"   {'✓' if restored else '✗'} every original restored — the "
              f"clean checks pass again afterwards")
        return ok and restored

    ok = True
    print("GATE 3.1-R2 — the Fear & Greed instrument's self-test, hardened")
    print("2026-07-27. Its first version let five of six deliberate lies")
    print("through. Its second printed '>> strong buy signal' on the deck of")
    print("an information-only ship and passed. This one rebuilds the WHOLE")
    print("block and compares it exactly.")

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
    if OFFLINE_WORDS in live:
        print("   ✗ the live section came back offline")
        ok = False

    print("\n2) THE PRINTED SENTENCE vs THE SOURCE (Gate 3.1-R b, c) — the"
          "\n   check whose absence let five lies through. Every expected"
          "\n   string is derived by this block's own arithmetic from raw"
          "\n   JSON; no helper of the instrument judges the instrument."
          "\n   The value and its label are checked TOGETHER, because a"
          "\n   number beside the wrong words is the defect F2 exposed.")
    ok = _core_checks(verbose=True) and ok

    print("\n3) EXHIBIT A, MADE PERMANENT (Gate 3.1-R d · 3.1-R2 f) — the file"
          "\n   is broken on purpose ELEVEN ways and each break MUST be"
          "\n   caught. Five of the first six escaped the gate of 2026-07-26;"
          "\n   three of the last five escaped the gate of the day after.")
    ok = _sabotage_drill() and ok

    print("\n4) OFFLINE DRILL — injected unreachable URL, internet untouched")
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
        print("\nGATE 3.1-R2 PASSED — the WHOLE printed block was rebuilt from "
              "the\nsource and matched exactly, the disclaimer was checked "
              "verbatim, the\ngate's own history limit was compared to the "
              "module's, and all ELEVEN\ndeliberate sabotages were caught. "
              "This test has demonstrated, this run,\nthat it is able to say "
              "no.")
    else:
        print("\nGATE 3.1-R2 FAILED — see the ✗ lines above.")
    sys.exit(0 if ok else 1)
