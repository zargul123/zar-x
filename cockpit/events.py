"""
Zar X cockpit — the Event Calendar (Context Deck, Phase 3, Step 3.4).

What is COMING: "US CPI release today", "FOMC decision in 40 days". So the
pilot is never surprised by a scheduled event he could have seen coming.

INFORMATION, NEVER A SIGNAL. "FOMC in 2 days" is a fact. "FOMC in 2 days —
consider reducing exposure" is advice and is forbidden. Phase 6's three signal
slots are locked BY NAME — Turtle/Donchian, funding-rate fade, on-chain cycle
thermometer — and none of them is a calendar.

**NOT NAMED `calendar.py`.** Python ships a standard-library module by that
name and a file here called `calendar` would shadow it for the whole program.

**THE TRAP THIS FILE IS SHAPED AROUND. A HARDCODED LIST OF DATES GOES STALE,
AND A STALE CALENDAR LOOKS EXACTLY LIKE A HEALTHY ONE.** This is Blockworks
again — the feed that answered HTTP 200 with fifty real, well-formed,
correctly-dated stories whose newest was 209 days old — and it is the recorder's
empty-list trap a third time. **An empty deck line is indistinguishable from a
quiet month.** So:

    a calendar with nothing ahead of it SAYS SO LOUDLY,
    and each built-in list carries the date its authority actually published to.

**AND THAT HORIZON IS NOT DECORATIVE. IT IS A DATED FACT WITH FOUR MONTHS TO
RUN.** The BLS publishes about a year ahead and its schedule stops dead at
10 Dec 2026, so on 11 Dec 2026 the CPI list runs out and this instrument starts
saying so on the Brief. GATE 3.4 proves that by advancing the clock rather than
by waiting for it.

**WHERE THE DATES CAME FROM — read off the issuing authority's own page on
2026-08-07, never remembered by anyone.** A fabricated date is exactly the shape
of lie this instrument exists to prevent.

  * FOMC — `federalreserve.gov/monetarypolicy/fomccalendars.htm`. The decision
    is the SECOND day of each two-day meeting, 14:00 US Eastern. The Fed's own
    page marks the 2027 dates TENTATIVE — "Each meeting date is tentative until
    confirmed at the meeting immediately preceding it" — **and that word is
    carried onto the Commander's screen rather than dropped.**
  * US CPI — `bls.gov/schedule/news_release/cpi.htm`, 08:30 US Eastern.
    **bls.gov answers HTTP 403 to a non-browser fetch**, the same edge block
    that killed The Block on 2026-08-04, so the page was read in a real browser.
    A session that could not reach an authority and filled the gap from memory
    would produce a calendar that looks exactly like this one and is wrong.

**TIME ZONES, WHICH ARE HOW THIS INSTRUMENT WOULD ONE DAY BE A DAY OUT WITH
NOTHING SAYING SO.** Every event here is an INSTANT — a date, a time and a zone
— never a bare date. `data/events.json` declares its own zone INSIDE the file,
and **a file that declares none contributes nothing and is named as such.**
"today" / "tomorrow" / "in N days" are then counted **in the reader's own local
date**, because the Commander reads his Brief nine hours ahead of New York and a
count done in New York's date would tell him "tomorrow" on the very morning a
release lands. The local date and time are printed beside the words, so nothing
is ambiguous.

LAW 2 — THE COMPARTMENT OWNS ITS SOURCES. The built-in lists and the path to
the Commander's file live in THIS file and nowhere else, so he can edit either
with one line.

LAW 3 — THE FAIL-SAFE. Every failure — a missing file, a file he broke while
editing it by hand, a zone this computer has never heard of — becomes one honest
line, and the Brief carries on with everything else intact. **The doorway never
raises and never prints; it RETURNS.**

Standalone smoke test:
    python cockpit/events.py          (live section, then the failure drills)
    python cockpit/events.py --gate   (gate 3.4, including the sabotage drill)
"""
import json
import os
import sys
from datetime import datetime, timezone

try:                                    # 3.9+; absent only on something exotic
    from zoneinfo import ZoneInfo
except ImportError:                     # pragma: no cover - not reachable here
    ZoneInfo = None

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Law 2: the Commander's own file, named HERE and nowhere else.
EVENTS_FILE = os.path.join(_ROOT, 'data', 'events.json')

SHOWN = 3               # how many are quoted; the rest are only counted
NAME_MAX = 60           # a longer name is clipped VISIBLY
CLIP_MARK = '…'
DEFAULT_TIME = '12:00'  # an entry of his with no time: midday in the file's zone

OFFLINE_WORDS = "Event calendar offline"
FOOTER_TAIL = "information, not a signal)"
NOTHING_AHEAD = ("⚠ NOTHING AHEAD — every date this calendar knows is in the "
                 "past")

# Day and month names are built HERE rather than taken from `strftime`, whose
# %a and %b follow the process locale. A machine set to another language would
# quietly print another language onto the Brief, and every expectation typed
# out in the gate would be wrong for a reason nothing named.
DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
          'Nov', 'Dec')

# Law 2: the built-in lists live HERE. (list tag, name, date, time, zone).
# All times US Eastern; the zone is named on every row rather than assumed, so
# a list from another authority can be added without touching anything else.
_ET = 'America/New_York'
RECURRING = (
    ('US CPI', 'US CPI release',           '2026-08-12', '08:30', _ET),
    ('US CPI', 'US CPI release',           '2026-09-11', '08:30', _ET),
    ('US CPI', 'US CPI release',           '2026-10-14', '08:30', _ET),
    ('US CPI', 'US CPI release',           '2026-11-10', '08:30', _ET),
    ('US CPI', 'US CPI release',           '2026-12-10', '08:30', _ET),
    ('FOMC',   'FOMC decision',            '2026-09-16', '14:00', _ET),
    ('FOMC',   'FOMC decision',            '2026-10-28', '14:00', _ET),
    ('FOMC',   'FOMC decision',            '2026-12-09', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-01-27', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-03-17', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-04-28', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-06-09', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-07-28', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-09-15', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-10-27', '14:00', _ET),
    ('FOMC',   'FOMC decision (tentative)', '2027-12-08', '14:00', _ET),
)

# THE HORIZON OF EACH LIST — the last date its authority has actually published.
# (list tag, through). **This is the whole staleness guard.** Past it, the list
# is EXPIRED and the deck says so by name.
HORIZONS = (
    ('FOMC', '2027-12-08'),
    ('US CPI', '2026-12-10'),
)


class CalendarError(Exception):
    """A failure this compartment turns into a named absence or one honest
    line. It never leaves this file."""


def _label(path):
    """How the file is named on his screen: the last two parts of the path.

    **DERIVED FROM THE PATH ACTUALLY READ, never carried as a constant.** A
    fixed label would let this line name one file while having read another —
    which is B14's shape exactly, where an archive moved to a different
    filename with every row inside it perfect and the report stayed true-
    looking.
    """
    head, tail = os.path.split(path)
    return (os.path.basename(head) + '/' + tail) if os.path.basename(head) \
        else tail


def _zone(name):
    """A zone name -> tzinfo, or None if this computer cannot resolve it.

    None is returned rather than raised because an unknown zone is a NAMED
    absence on the deck, not a crash. A silent fall back to UTC is the one
    thing that must never happen here: it would move an announcement by hours
    and nothing on the screen would say so.
    """
    if ZoneInfo is None or not isinstance(name, str) or not name:
        return None
    try:
        return ZoneInfo(name)
    except Exception:
        return None


def _instant(date_text, time_text, zone):
    """('YYYY-MM-DD', 'HH:MM', tzinfo) -> aware datetime, or None.

    `strptime` is strict on purpose: '2026-13-45' and 'next tuesday' both come
    back None and the entry is REFUSED AND COUNTED. A date this file cannot
    read honestly is not guessed at.
    """
    if zone is None or not isinstance(date_text, str):
        return None
    try:
        day = datetime.strptime(date_text.strip(), '%Y-%m-%d')
        hour, minute = str(time_text).strip().split(':')
        hour, minute = int(hour), int(minute)
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return None
        return datetime(day.year, day.month, day.day, hour, minute, tzinfo=zone)
    except Exception:
        return None


def _clip(name):
    """Whitespace flattened so no entry can break the deck's layout, and
    anything over NAME_MAX clipped with a mark the reader can SEE. A silent
    truncation would be this instrument quietly rewriting what he wrote."""
    flat = ' '.join(str(name).split())
    if len(flat) <= NAME_MAX:
        return flat
    return flat[:NAME_MAX - 1].rstrip() + CLIP_MARK


def _stamp(when):
    """An aware datetime -> 'Wed 12 Aug 2026, 17:30'."""
    return (f"{DAYS[when.weekday()]} {when.day:02d} {MONTHS[when.month - 1]} "
            f"{when.year}, {when.hour:02d}:{when.minute:02d}")


def _date_stamp(text):
    """'2026-12-10' -> '10 Dec 2026', for the horizons in the footer."""
    day = datetime.strptime(text, '%Y-%m-%d')
    return f"{day.day:02d} {MONTHS[day.month - 1]} {day.year}"


def _when_words(days):
    """The wording differs by distance, which is the whole point of the line.
    Never negative: only events still ahead reach here."""
    if days <= 0:
        return "today"
    if days == 1:
        return "tomorrow"
    return f"in {days} days"


def _from_builtin(recurring):
    """The built-in lists -> [(instant, name)]. A row this computer cannot
    resolve a zone for is refused and counted, exactly like one of his."""
    out, refused = [], 0
    for _tag, name, date_text, time_text, zone_name in recurring:
        when = _instant(date_text, time_text, _zone(zone_name))
        if when is None:
            refused += 1
            continue
        out.append((when, name))
    return out, refused


def _from_file(path):
    """The Commander's own file -> ([(instant, name)], note, refused).

    `note` is a NAMED absence for the header, or ''. **Every way this file can
    fail is named separately**, because "the calendar is a bit broken" is not
    something anyone can act on, and he edits this file by hand so it WILL
    happen.
    """
    label = _label(path)
    if not os.path.exists(path):
        return [], f"{label} missing", 0
    try:
        with open(path, encoding='utf-8') as handle:
            raw = json.load(handle)
    except Exception:
        return [], f"{label} unreadable", 0
    if not isinstance(raw, dict) or not isinstance(raw.get('events'), list):
        return [], f'{label} has no "events" list', 0

    # >>> THE ZONE IS REQUIRED. A file that does not say which clock its dates
    # are on cannot be read honestly, and assuming one is how this instrument
    # would be a day out with nothing saying so.
    zone_name = raw.get('timezone')
    zone = _zone(zone_name)
    if zone is None:
        if not isinstance(zone_name, str) or not zone_name:
            return [], f"{label} declares no timezone", 0
        return [], f'{label} timezone "{zone_name}" is unknown here', 0

    out, refused = [], 0
    for entry in raw['events']:
        if not isinstance(entry, dict):
            refused += 1
            continue
        name = entry.get('name')
        if not isinstance(name, str) or not name.strip():
            refused += 1
            continue
        when = _instant(entry.get('date'), entry.get('time', DEFAULT_TIME),
                        zone)
        if when is None:
            refused += 1
            continue
        out.append((when, name.strip()))
    return out, '', refused


def _ahead(known, now):
    """Only what is still to COME, newest first is wrong here — soonest first.

    A separate function so the drill can break it: showing a past event as
    coming is the same lie as a stale feed printing a January headline under
    today's date, and it is the reason this instrument exists.
    """
    return [e for e in known if e[0] >= now]


def _expired(horizons, now, local):
    """The lists whose published horizon is behind us, by name.

    The horizon is compared as a DATE in the reader's own local zone, the same
    clock the "in N days" counts use, so the warning and the counts can never
    disagree with each other.
    """
    today = now.astimezone(local).date()
    out = []
    for tag, through in horizons:
        try:
            last = datetime.strptime(through, '%Y-%m-%d').date()
        except Exception:
            out.append((tag, through))       # unreadable is not a quiet pass
            continue
        if today > last:
            out.append((tag, through))
    return out


def section_text(path=None, now=None, local=None, recurring=None,
                 horizons=None):
    """The Context Deck block the Brief prints — this part's single doorway.

    Never raises and never prints; it RETURNS. Everything it reads is
    injectable so the gate can hand it a file it built itself, a fixed clock
    and a fixed local zone, without touching the Commander's own file or his
    computer's clock.
    """
    try:
        path = EVENTS_FILE if path is None else path
        now = datetime.now(timezone.utc) if now is None else now
        recurring = RECURRING if recurring is None else recurring
        horizons = HORIZONS if horizons is None else horizons
        if local is None:
            local = datetime.now(timezone.utc).astimezone().tzinfo
        if local is None:
            raise CalendarError("this computer would not name its own timezone")

        mine, note, refused_file = _from_file(path)
        theirs, refused_builtin = _from_builtin(recurring)
        refused = refused_file + refused_builtin

        # The same event in his file and in a built-in list counts once.
        known = sorted(set(mine + theirs), key=lambda e: (e[0], e[1]))
        ahead = _ahead(known, now)

        notes = f"   [no data: {note}]" if note else ""
        if refused:
            word = 'entry' if refused == 1 else 'entries'
            notes += f"   [{refused} {word} refused]"

        today = now.astimezone(local).date()
        lines = []
        if not ahead:
            # >>> THE TRAP. Silence here would read as "nothing is coming",
            # which is the one thing this instrument must never say by accident.
            lines.append(f"  {'Events':<12} : {NOTHING_AHEAD}{notes}")
        else:
            first = (ahead[0][0].astimezone(local).date() - today).days
            lines.append(f"  {'Events':<12} : {len(ahead)} ahead · next "
                         f"{_when_words(first)}{notes}")
            for when, name in ahead[:SHOWN]:
                here = when.astimezone(local)
                words = _when_words((here.date() - today).days)
                lines.append(f"    {words:<12}— {_clip(name)} "
                             f"({_stamp(here)} local)")

        for tag, through in _expired(horizons, now, local):
            lines.append(f"    ⚠ the built-in {tag} list ENDED on "
                         f"{_date_stamp(through)} — it needs new dates")

        span = ' · '.join(f"{tag} to {_date_stamp(through)}"
                          for tag, through in horizons)
        lines.append(f"  (from {_label(path)} and the built-in lists — {span}")
        lines.append(f"   — {FOOTER_TAIL}")
        return "\n".join(lines)
    except Exception as e:
        return f"  🔌 {OFFLINE_WORDS} ({type(e).__name__})"


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        print(section_text())
        print()
        print("--- drill: the file is missing, internet and his own file "
              "untouched ---")
        print(section_text(path=os.path.join(_ROOT, 'data',
                                             'no-such-events.json')))
        print()
        print("--- drill: the clock advanced past every published horizon ---")
        print(section_text(now=datetime(2028, 1, 1, 9, 0, tzinfo=timezone.utc)))
        sys.exit(0)

    # =====================================================================
    # GATE 3.4 — declared in PROGRESS_LOG.md on 2026-08-07 and committed
    # ALONE, with no .py in that commit, BEFORE this file existed. Commit
    # 32af26d; `git show --stat 32af26d` is the proof the bar came first.
    #
    # THIS FILE IS THE THIRD ON THIS SHIP BUILT WITH THE RULE FROM BIRTH:
    # **A SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT
    # MEANS ANYTHING.** F10, S6 and B1 were the same fault in three files —
    # a deliberate break that could not change what anyone read, scored
    # ESCAPED, turning a gate red about a lie it had never managed to tell.
    # Each cost a different generation a session to retrofit. Here, every
    # sabotage below is run twice — honest and broken — and its verdict is
    # only counted if the two OBSERVABLES DIFFER. An unprovable sabotage is
    # reported INERT and FAILS this gate.
    #
    # AND THE OBSERVABLE IS PER-SABOTAGE. E10 changes nothing about the
    # returned block — it prints to stdout while returning byte-identical
    # text, exactly as S15 and N10 did. Its witness is therefore CAPTURED
    # OUTPUT AT THE FILE DESCRIPTOR, not the block. A drill that measured
    # every sabotage on one channel would score E10 INERT and delete the
    # only check that catches it.
    # =====================================================================
    import logging
    import re
    import shutil
    import subprocess
    import tempfile
    import time

    def mark(good, text, detail=''):
        nonlocal_ok.append(good)
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    def show(label, expected, got):
        print(f"     ---- the gate expected ({label}) ----")
        for line in expected.split('\n'):
            print(f"     {line!r}")
        print("     ---- the doorway returned ----")
        for line in got.split('\n'):
            print(f"     {line!r}")

    nonlocal_ok = []

    # ---- THE GATE'S OWN CLOCK AND THE GATE'S OWN ZONES ------------------
    # `ZoneInfo` is used DIRECTLY here, never the module's `_zone`: door 1
    # says a gate may not call a helper under test to build its own input,
    # and `_zone` is broken on purpose by sabotage E9 further down.
    #
    # The reader's zone is fixed at Asia/Karachi — UTC+5, no daylight saving —
    # because that is the clock the Commander's own machine keeps, measured
    # 2026-08-07: an 08:30 New York release printed as 17:30 on his Brief.
    LOCAL = ZoneInfo('Asia/Karachi')
    LOCAL_UTC = ZoneInfo('UTC')
    GATE_ET = 'America/New_York'
    NOW = datetime(2026, 8, 7, 9, 0, tzinfo=timezone.utc)      # Fri, 14:00 local

    GATE_DIR = os.path.join(tempfile.mkdtemp(prefix='zarx_events_'), 'gatedata')
    os.makedirs(GATE_DIR)

    def _file(name, obj):
        """A fixture file, built HERE from nothing by a gate that never asks
        the module where to look. The directory is named `gatedata` so the
        label the doorway prints is predictable and can be typed out below."""
        path = os.path.join(GATE_DIR, name)
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump(obj, handle)
        return path

    def _raw(name, text):
        path = os.path.join(GATE_DIR, name)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(text)
        return path

    # The gate's own recurring list and its own horizon — nothing to do with
    # the ones this file ships, which are pinned separately in check (m).
    GATE_RECURRING = (('GateList', 'Gate recurring event', '2026-09-01',
                       '10:00', GATE_ET),)
    GATE_HORIZONS = (('GateList', '2026-09-01'),)

    # Every awkward case the orders named, planted on purpose:
    #   the past one ....... already happened, must NOT be shown
    #   the today one ...... 12:00 New York = 21:00 local, still ahead of NOW
    #   the tomorrow one ... the wording must differ from "in N days"
    #   the token unlock ... 18:00 New York = 03:00 LOCAL THE NEXT DAY. This
    #                        one exists to make the zone MATTER: read as UTC
    #                        it would be 23:00 the evening before and land on
    #                        a different day. It is the control for E9.
    GOLDEN_PATH = _file('golden.json', {
        'timezone': GATE_ET,
        'events': [
            {'date': '2026-08-01', 'time': '12:00',
             'name': 'A meeting that already happened'},
            {'date': '2026-08-07', 'time': '12:00',
             'name': 'Quarterly options expiry'},
            {'date': '2026-08-08', 'time': '09:00',
             'name': 'Exchange maintenance window'},
            {'date': '2026-08-09', 'time': '18:00', 'name': 'Token unlock'},
        ],
    })

    # Typed out HERE, character by character, by a gate that did not build it.
    GOLDEN_EXPECTED = (
        '  Events       : 4 ahead · next today\n'
        '    today       — Quarterly options expiry '
        '(Fri 07 Aug 2026, 21:00 local)\n'
        '    tomorrow    — Exchange maintenance window '
        '(Sat 08 Aug 2026, 18:00 local)\n'
        '    in 3 days   — Token unlock (Mon 10 Aug 2026, 03:00 local)\n'
        '  (from gatedata/golden.json and the built-in lists — '
        'GateList to 01 Sep 2026\n'
        '   — information, not a signal)'
    )

    def golden(**kw):
        args = dict(path=GOLDEN_PATH, now=NOW, local=LOCAL,
                    recurring=GATE_RECURRING, horizons=GATE_HORIZONS)
        args.update(kw)
        return section_text(**args)

    # `shipped` uses the REAL built-in lists and the REAL horizons this file
    # carries, with a fixed clock and a file that is not there — so what it
    # returns is the ship's own calendar and nothing else.
    MISSING_PATH = os.path.join(GATE_DIR, 'nothing-here.json')

    def shipped(**kw):
        args = dict(path=MISSING_PATH, now=NOW, local=LOCAL)
        args.update(kw)
        return section_text(**args)

    SHIPPED_EXPECTED = (
        '  Events       : 16 ahead · next in 5 days   '
        '[no data: gatedata/nothing-here.json missing]\n'
        '    in 5 days   — US CPI release (Wed 12 Aug 2026, 17:30 local)\n'
        '    in 35 days  — US CPI release (Fri 11 Sep 2026, 17:30 local)\n'
        '    in 40 days  — FOMC decision (Wed 16 Sep 2026, 23:00 local)\n'
        '  (from gatedata/nothing-here.json and the built-in lists — '
        'FOMC to 08 Dec 2027 · US CPI to 10 Dec 2026\n'
        '   — information, not a signal)'
    )

    print("=" * 70)
    print("  GATE 3.4 — the Event Calendar")
    print("=" * 70)

    print("\n(a) INJECTED FILE, INJECTED CLOCK, INJECTED ZONE, EXACT EQUALITY"
          "\n    — the gate writes its OWN events file, hands the doorway a"
          "\n    fixed clock and a fixed reader's zone, and demands the WHOLE"
          "\n    block match a copy typed out in this gate, character for"
          "\n    character. 'The words are present' is the bar S14 walked"
          "\n    straight through and it is used nowhere in this file."
          "\n    Folded into this one equality: a PAST event excluded, the"
          "\n    TODAY / TOMORROW / IN N DAYS wordings, and an 18:00 New York"
          "\n    event landing at 03:00 the NEXT day on the reader's clock.")
    got = golden()
    same = got == GOLDEN_EXPECTED
    mark(same, "the whole block matched the gate's own copy BYTE FOR BYTE")
    if not same:
        show('golden', GOLDEN_EXPECTED, got)

    print("\n(a2) AND THE SHIPPED CALENDAR ITSELF, TO THE BYTE. The dates"
          "\n    below were read off federalreserve.gov and bls.gov on"
          "\n    2026-08-07 and typed into this gate BY HAND. If anybody ever"
          "\n    edits the built-in lists, this check goes red and says so —"
          "\n    which is the point: a shipped date is a fact, not a detail.")
    got_ship = shipped()
    same_ship = got_ship == SHIPPED_EXPECTED
    mark(same_ship, "the ship's own next three events matched the gate's copy")
    if not same_ship:
        show('shipped', SHIPPED_EXPECTED, got_ship)

    print("\n(b) >>> THE STALENESS TRAP, WHICH IS THE ONE THING THIS"
          "\n    INSTRUMENT MUST GET RIGHT. A hardcoded list of dates goes"
          "\n    stale and a stale calendar looks EXACTLY like a healthy one —"
          "\n    Blockworks answered HTTP 200 with fifty perfect stories whose"
          "\n    newest was 209 days old. **THE BLS PUBLISHES ABOUT A YEAR"
          "\n    AHEAD AND ITS SCHEDULE STOPS DEAD AT 10 DEC 2026, SO THIS"
          "\n    FIRES FOR REAL IN ROUGHLY FOUR MONTHS.** The clock is"
          "\n    advanced to Jan 2027 rather than waited for: the CPI list must"
          "\n    be named as ENDED while the FOMC list carries on working.")
    EXPIRED_NOW = datetime(2027, 1, 5, 9, 0, tzinfo=timezone.utc)
    EXPIRED_EXPECTED = (
        '  Events       : 8 ahead · next in 23 days   '
        '[no data: gatedata/nothing-here.json missing]\n'
        '    in 23 days  — FOMC decision (tentative) '
        '(Thu 28 Jan 2027, 00:00 local)\n'
        '    in 71 days  — FOMC decision (tentative) '
        '(Wed 17 Mar 2027, 23:00 local)\n'
        '    in 113 days — FOMC decision (tentative) '
        '(Wed 28 Apr 2027, 23:00 local)\n'
        '    ⚠ the built-in US CPI list ENDED on 10 Dec 2026 — '
        'it needs new dates\n'
        '  (from gatedata/nothing-here.json and the built-in lists — '
        'FOMC to 08 Dec 2027 · US CPI to 10 Dec 2026\n'
        '   — information, not a signal)'
    )
    got_exp = shipped(now=EXPIRED_NOW)
    same_exp = got_exp == EXPIRED_EXPECTED
    mark(same_exp,
         "one list ENDED and named by its own name, the other still working")
    if not same_exp:
        show('one list expired', EXPIRED_EXPECTED, got_exp)

    print("\n(c) NOTHING AHEAD AT ALL -> A LOUD LINE, judged by exact"
          "\n    equality. **SILENCE HERE WOULD READ AS 'no events coming',"
          "\n    which is the recorder's empty-list trap in a third hat.** The"
          "\n    clock is pushed past every horizon this file ships.")
    GONE_NOW = datetime(2028, 1, 1, 9, 0, tzinfo=timezone.utc)
    GONE_EXPECTED = (
        '  Events       : ⚠ NOTHING AHEAD — every date this calendar knows '
        'is in the past   [no data: gatedata/nothing-here.json missing]\n'
        '    ⚠ the built-in FOMC list ENDED on 08 Dec 2027 — '
        'it needs new dates\n'
        '    ⚠ the built-in US CPI list ENDED on 10 Dec 2026 — '
        'it needs new dates\n'
        '  (from gatedata/nothing-here.json and the built-in lists — '
        'FOMC to 08 Dec 2027 · US CPI to 10 Dec 2026\n'
        '   — information, not a signal)'
    )
    got_gone = shipped(now=GONE_NOW)
    same_gone = got_gone == GONE_EXPECTED
    mark(same_gone, "an exhausted calendar SAID SO, loudly, and named both "
                    "lists")
    if not same_gone:
        show('nothing ahead', GONE_EXPECTED, got_gone)

    print("\n(d) A 112-CHARACTER NAME IS CLIPPED VISIBLY — never silently. A"
          "\n    silent truncation is this instrument quietly rewriting what"
          "\n    the Commander himself wrote into the file.")
    LONG_NAME = ('Quarterly options and futures expiry across every major '
                 'venue plus the monthly settlement window that follows it')
    LONG_PATH = _file('long.json', {
        'timezone': GATE_ET,
        'events': [{'date': '2026-08-08', 'time': '09:00',
                    'name': LONG_NAME}],
    })
    EXPECT_LONG = ('    tomorrow    — Quarterly options and futures expiry '
                   'across every major ven… (Sat 08 Aug 2026, 18:00 local)')
    long_line = golden(path=LONG_PATH).split('\n')[1]
    mark(long_line == EXPECT_LONG,
         "clipped to 60 characters and marked with a visible ellipsis",
         f"len(name)={len(LONG_NAME)} -> the name printed as "
         f"{len(long_line.split('— ')[1].split(' (Sat')[0])} chars")

    print("\n(e) TWO EVENTS ON THE SAME DAY — both shown, ordered by name so"
          "\n    the same file always produces the same line. 'Beta' is"
          "\n    written FIRST in the file and must print SECOND.")
    SAME_PATH = _file('sameday.json', {
        'timezone': GATE_ET,
        'events': [{'date': '2026-08-08', 'time': '09:00',
                    'name': 'Beta window'},
                   {'date': '2026-08-08', 'time': '09:00',
                    'name': 'Alpha window'}],
    })
    same_day = golden(path=SAME_PATH).split('\n')
    mark(same_day[1] == '    tomorrow    — Alpha window '
                        '(Sat 08 Aug 2026, 18:00 local)'
         and same_day[2] == '    tomorrow    — Beta window '
                            '(Sat 08 Aug 2026, 18:00 local)',
         "both events on the same day printed, in a fixed order",
         same_day[1].strip() + ' | ' + same_day[2].strip())

    print("\n(f) AN EVENT SIX MONTHS OUT — the wording must differ from"
          "\n    'today' and from 'tomorrow', and the year must be on the"
          "\n    absolute date so a February can never be read as this one.")
    FAR_PATH = _file('far.json', {
        'timezone': GATE_ET,
        'events': [{'date': '2027-02-15', 'time': '12:00',
                    'name': 'Far-off audit'}],
    })
    far = golden(path=FAR_PATH).split('\n')
    mark(far[2] == '    in 192 days — Far-off audit '
                   '(Mon 15 Feb 2027, 22:00 local)',
         "a date 192 days away is counted and dated in full",
         far[2].strip() if len(far) > 2 else '(missing)')

    print("\n(g) THE FILE HE EDITED BY HAND AND GOT WRONG. Four entries are"
          "\n    malformed four different ways and ONE is good. **THE REFUSED"
          "\n    ONES ARE COUNTED AND SAID.** A silent drop is S10, and it is"
          "\n    the difference between 'I can see three things coming' and"
          "\n    'I can see three things coming and two I could not read'.")
    BAD_PATH = _file('bad.json', {
        'timezone': GATE_ET,
        'events': [
            {'date': '2026-13-45', 'name': 'An impossible date'},
            {'date': 'next tuesday', 'name': 'Not a date at all'},
            {'date': '2026-08-20', 'name': '   '},
            'just a string, not an object',
            {'date': '2026-08-20', 'time': '09:00',
             'name': 'The one good entry'},
        ],
    })
    BAD_EXPECTED = (
        '  Events       : 2 ahead · next in 13 days   [4 entries refused]\n'
        '    in 13 days  — The one good entry (Thu 20 Aug 2026, 18:00 local)\n'
        '    in 25 days  — Gate recurring event (Tue 01 Sep 2026, 19:00 local)\n'
        '  (from gatedata/bad.json and the built-in lists — '
        'GateList to 01 Sep 2026\n'
        '   — information, not a signal)'
    )
    got_bad = golden(path=BAD_PATH)
    same_bad = got_bad == BAD_EXPECTED
    mark(same_bad, "four bad entries refused AND COUNTED, the good one kept")
    if not same_bad:
        show('bad entries', BAD_EXPECTED, got_bad)

    ONE_BAD_PATH = _file('onebad.json', {
        'timezone': GATE_ET,
        'events': [{'date': '2026-13-45', 'name': 'An impossible date'}],
    })
    mark('[1 entry refused]' in golden(path=ONE_BAD_PATH).split('\n')[0],
         "one refused entry says 'entry', not 'entries'",
         golden(path=ONE_BAD_PATH).split('\n')[0].strip())

    print("\n(h) EVERY WAY THE FILE ITSELF CAN FAIL IS NAMED SEPARATELY."
          "\n    'The calendar is a bit broken' is not something anybody can"
          "\n    act on. **The timezone cases are the important two: a file"
          "\n    that does not say which clock its dates are on contributes"
          "\n    NOTHING and says so** — assuming a zone is how this"
          "\n    instrument would one day be a day out with nothing saying so.")
    NOZONE_PATH = _file('nozone.json', {
        'events': [{'date': '2026-08-20', 'name': 'Whose clock is this on?'}]})
    BADZONE_PATH = _file('badzone.json', {
        'timezone': 'Mars/Olympus',
        'events': [{'date': '2026-08-20', 'name': 'Whose clock is this on?'}]})
    BARE_PATH = _file('barelist.json', [])
    EMPTY_PATH = _file('empty.json', {'timezone': 'UTC', 'events': []})
    BROKEN_PATH = _raw('broken.json', '{ this is not json at all,,,')
    for label, path, expect_note in (
            ('missing entirely  ', MISSING_PATH,
             '[no data: gatedata/nothing-here.json missing]'),
            ('malformed JSON    ', BROKEN_PATH,
             '[no data: gatedata/broken.json unreadable]'),
            ('a bare [] list    ', BARE_PATH,
             '[no data: gatedata/barelist.json has no "events" list]'),
            ('no timezone       ', NOZONE_PATH,
             '[no data: gatedata/nozone.json declares no timezone]'),
            ('an unknown zone   ', BADZONE_PATH,
             '[no data: gatedata/badzone.json timezone "Mars/Olympus" '
             'is unknown here]')):
        head = golden(path=path).split('\n')[0]
        mark(head.endswith(expect_note) and '1 ahead' in head,
             f"{label} -> named by its own name, the built-in list unharmed",
             head.strip())
    empty_head = golden(path=EMPTY_PATH).split('\n')[0]
    mark(empty_head == '  Events       : 1 ahead · next in 25 days',
         "an EMPTY events list is a legitimate state and says nothing extra",
         empty_head.strip())

    print("\n(i) THE READER'S ZONE IS ACTUALLY USED — the control for E9"
          "\n    below. The same file and the same clock, rendered for a"
          "\n    reader in Karachi and one in UTC, MUST differ: the 18:00 New"
          "\n    York token unlock is 03:00 the next day in Karachi and 22:00"
          "\n    the same evening in UTC. **A check that could not tell those"
          "\n    two apart would pass a doorway that ignored the zone"
          "\n    entirely.**")
    in_utc = golden(local=LOCAL_UTC)
    mark(in_utc != golden() and 'in 2 days' in in_utc
         and 'in 3 days' in golden(),
         "Karachi says 'in 3 days' where UTC says 'in 2 days'",
         [l.strip() for l in in_utc.split('\n') if 'Token' in l][0])

    print("\n(m) DOOR 1 — THE GATE HOLDS ITS OWN EXPECTATIONS. Every string"
          "\n    above is typed out in this gate. The things a live check"
          "\n    cannot type out are the constants and the shipped date list,"
          "\n    so they are checked HERE against copies written in this gate"
          "\n    — R-014 was a gate reading its own expectation out of the"
          "\n    file on trial, and B14 was a report that asked the thing it"
          "\n    was judging where to look.")
    EXPECT_RECURRING = (
        ('US CPI', 'US CPI release', '2026-08-12', '08:30', 'America/New_York'),
        ('US CPI', 'US CPI release', '2026-09-11', '08:30', 'America/New_York'),
        ('US CPI', 'US CPI release', '2026-10-14', '08:30', 'America/New_York'),
        ('US CPI', 'US CPI release', '2026-11-10', '08:30', 'America/New_York'),
        ('US CPI', 'US CPI release', '2026-12-10', '08:30', 'America/New_York'),
        ('FOMC', 'FOMC decision', '2026-09-16', '14:00', 'America/New_York'),
        ('FOMC', 'FOMC decision', '2026-10-28', '14:00', 'America/New_York'),
        ('FOMC', 'FOMC decision', '2026-12-09', '14:00', 'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-01-27', '14:00',
         'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-03-17', '14:00',
         'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-04-28', '14:00',
         'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-06-09', '14:00',
         'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-07-28', '14:00',
         'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-09-15', '14:00',
         'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-10-27', '14:00',
         'America/New_York'),
        ('FOMC', 'FOMC decision (tentative)', '2027-12-08', '14:00',
         'America/New_York'),
    )
    mark(tuple(RECURRING) == EXPECT_RECURRING,
         "the module ships exactly the sixteen dates this gate names, read "
         "off the Fed's and the BLS's own pages on 2026-08-07",
         f"{len(RECURRING)} rows")
    mark(tuple(HORIZONS) == (('FOMC', '2027-12-08'), ('US CPI', '2026-12-10')),
         "each list's horizon is the last date its authority has published")
    mark(SHOWN == 3 and NAME_MAX == 60 and CLIP_MARK == '…'
         and DEFAULT_TIME == '12:00',
         "the module's constants equal this gate's own copies",
         f"SHOWN={SHOWN} NAME_MAX={NAME_MAX} DEFAULT_TIME={DEFAULT_TIME!r}")
    mark(OFFLINE_WORDS == 'Event calendar offline'
         and FOOTER_TAIL == 'information, not a signal)'
         and NOTHING_AHEAD == ('⚠ NOTHING AHEAD — every date this calendar '
                               'knows is in the past'),
         "the three fixed wordings equal this gate's own copies")
    mark(DAYS == ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
         and MONTHS == ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                        'Aug', 'Sep', 'Oct', 'Nov', 'Dec'),
         "day and month names are the module's own, not the process locale's")
    mark(EVENTS_FILE.replace('\\', '/').endswith('/data/events.json')
         and os.path.exists(EVENTS_FILE),
         "the Commander's file is where this gate says it is, and it is there",
         EVENTS_FILE)

    print("\n(n) INFORMATION, NEVER A SIGNAL. F8 printed '>> strong buy"
          "\n    signal' on the deck of an information-only ship while its"
          "\n    gate applauded. Every line this instrument speaks is its own"
          "\n    voice — there are no quoted third parties here at all — so"
          "\n    the whole block is held to it, on every path above.")
    ADVICE_WORDS = ('buy', 'sell', 'should', 'consider', 'reduce', 'exposure',
                    'opportunity', '>>')
    for label, block in (('golden', got), ('shipped', got_ship),
                         ('one list expired', got_exp),
                         ('nothing ahead', got_gone),
                         ('a file he broke', got_bad)):
        low = block.lower()
        hits = [w for w in ADVICE_WORDS if w in low]
        mark(not hits, f"{label:<18} -> not one word of advice anywhere",
             '' if not hits else f"found {hits}")

    print("\n(o) DOOR 2 — THE DOORWAY NEVER RAISES. Law 3: the Brief must"
          "\n    survive any failure of any instrument. Nine shapes of broken"
          "\n    input, each one required to RETURN rather than throw.")
    poisons = [
        ('a JSON null', dict(path=_raw('null.json', 'null'))),
        ('a JSON number', dict(path=_raw('num.json', '4242'))),
        ('"events" is a dict', dict(path=_file('dict.json', {
            'timezone': 'UTC', 'events': {'a': 1}}))),
        ('entries are numbers', dict(path=_file('nums.json', {
            'timezone': 'UTC', 'events': [1, 2, 3]}))),
        ('the path is a DIRECTORY', dict(path=GATE_DIR)),
        ('a naive clock', dict(now=datetime(2026, 8, 7, 9, 0))),
        ('no reader zone at all', dict(local='not a timezone')),
        ('a horizon that is not a date',
         dict(horizons=(('GateList', 'whenever'),))),
        ('recurring rows of the wrong shape',
         dict(recurring=(('too', 'few'),))),
    ]
    for label, kw in poisons:
        try:
            out = golden(**kw)
            raised = False
        except Exception as exc:
            out = f'{type(exc).__name__}: {exc}'
            raised = True
        mark(not raised and isinstance(out, str) and out,
             f"{label:<34} -> returned, did not raise",
             out.split('\n')[0].strip()[:72])

    print("\n(p) DOOR 3 — WHAT THE DOORWAY WRITES, LISTENED FOR AT THE FILE"
          "\n    DESCRIPTOR. **`cockpit/news.py` listens only at sys.stdout"
          "\n    and that is R-046, open on the books. This instrument carries"
          "\n    the deeper ear from birth because its doorway is simple"
          "\n    enough to.** Redirecting the NAMES catches `print` and misses"
          "\n    both a raw os.write and a logging handler that took a"
          "\n    reference to the real stream before anyone redirected"
          "\n    anything. And because a DEAF ear also reports silence, the"
          "\n    ear is made to prove it can hear first.")

    def _capture(call):
        """Run `call()` with BOTH streams captured AT THE FILE DESCRIPTOR.
        Returns raw BYTES, so no decoding can manufacture a pass. The restore
        is in `finally` and every dup is closed: this function is a judge
        inside the drill below, and a leaked descriptor would swallow the
        whole run's output."""
        sys.stdout.flush()
        sys.stderr.flush()
        heard = tempfile.TemporaryFile()
        saved_out, saved_err = os.dup(1), os.dup(2)
        try:
            os.dup2(heard.fileno(), 1)
            os.dup2(heard.fileno(), 2)
            try:
                call()
            finally:
                for stream in (sys.stdout, sys.stderr):
                    try:
                        stream.flush()
                    except Exception:
                        pass
        finally:
            os.dup2(saved_out, 1)
            os.dup2(saved_err, 2)
            os.close(saved_out)
            os.close(saved_err)
        heard.seek(0)
        written = heard.read()
        heard.close()
        return written

    # Bound to `sys.stderr` HERE, exactly as a handler created during a module
    # import would be. This is the object a redirect can never take away.
    _EAR_LOGGER = logging.getLogger('zarx.gate.events.ear')
    _EAR_LOGGER.propagate = False
    _EAR_LOGGER.handlers[:] = [logging.StreamHandler(sys.stderr)]
    _EAR_LOGGER.setLevel(logging.INFO)
    _EAR_ROUTES = (
        ('print()          ', ">> EAR CONTROL: the print() route"),
        ('os.write(fd 1)   ', ">> EAR CONTROL: the raw descriptor route"),
        ('logging -> stderr', ">> EAR CONTROL: the logging-handler route"),
    )

    def _shout_all():
        print(_EAR_ROUTES[0][1])
        os.write(1, (_EAR_ROUTES[1][1] + "\n").encode('utf-8'))
        _EAR_LOGGER.info(_EAR_ROUTES[2][1])

    heard_control = _capture(_shout_all).decode('utf-8', 'replace')
    for route, words in _EAR_ROUTES:
        mark(words in heard_control,
             f"the ear HEARD the {route} route — a listener that cannot hear "
             f"this reports silence")

    before_fds = [os.fstat(fd)[:4] for fd in (1, 2)]
    for label, call in (('golden        ', lambda: golden()),
                        ('file missing  ', lambda: shipped()),
                        ('nothing ahead ', lambda: shipped(now=GONE_NOW)),
                        ('a REAL reading', lambda: section_text())):
        written = _capture(call)
        mark(written == b'',
             f"{label} -> the doorway wrote NOTHING to descriptor 1 or 2",
             '' if written == b'' else
             f"it wrote {written.decode('utf-8', 'replace')!r}")
    for label, current, original in (('sys.stdout', sys.stdout, sys.__stdout__),
                                     ('sys.stderr', sys.stderr, sys.__stderr__)):
        if original is None:
            mark(False, f"{label}: the process's original stream is None, so "
                        f"this check CANNOT be performed — that is a FAILURE")
            continue
        mark(current is original,
             f"{label} is still the process's own stream — the doorway did "
             f"not rebind it under the Brief")
    mark(before_fds == [os.fstat(fd)[:4] for fd in (1, 2)],
         "descriptors 1 and 2 came back unchanged — the ear gave the "
         "pilot's screen back")

    print("\n(q) DOOR 3, THE HALF NO IN-PROCESS CHECK CAN SEE. Everything"
          "\n    above runs in a process where this module was imported before"
          "\n    the first check drew breath, and the ear stops listening the"
          "\n    instant the doorway returns. `brief.py` imports this file, so"
          "\n    a single module-level print lands on the Morning Brief ABOVE"
          "\n    ITS HEADER, and a write deferred to a thread or an atexit"
          "\n    handler lands after the verdict. **A FRESH INTERPRETER"
          "\n    imports it, calls the doorway three ways and SHUTS DOWN, and"
          "\n    its TOTAL output must be empty.** A timeout is a FAILURE,"
          "\n    never a quiet pass: 'nothing before we gave up' is exactly"
          "\n    what a sleeping thread looks like.")
    GATE_MODULE_NAME = 'cockpit.events'
    GATE_MODULE_LEAF = 'events.py'
    GATE_DOOR3_PATHS = (
        "m.section_text()",
        "m.section_text(path='no-such-file-anywhere.json')",
        "m.section_text(now=dt.datetime(2028, 1, 1, tzinfo=dt.timezone.utc))",
    )
    probe_dir = tempfile.mkdtemp(prefix='zarx_d3probe_')
    probe = os.path.join(probe_dir, 'seen.txt')
    body = ''.join('%s\nn += 1\n' % call for call in GATE_DOOR3_PATHS)
    child = ('import sys\n'
             'import datetime as dt\n'
             'import %s as m\n' % GATE_MODULE_NAME +
             'n = 0\n' + body +
             "open(sys.argv[1], 'w', encoding='utf-8').write("
             'm.__file__ + chr(10) + str(n))\n')
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    started, timed_out, wrote, rc = time.time(), False, b'', None
    try:
        done = subprocess.run([sys.executable, '-c', child, probe],
                              cwd=_ROOT, env=env, capture_output=True,
                              timeout=90)
        wrote, rc = done.stdout + done.stderr, done.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        wrote = (exc.stdout or b'') + (exc.stderr or b'')
    elapsed = time.time() - started
    try:
        seen = open(probe, encoding='utf-8').read()
    except OSError:
        seen = ''
    shutil.rmtree(probe_dir, ignore_errors=True)
    parts = seen.split(chr(10))
    seen_file = parts[0] if parts else ''
    try:
        seen_n = int(parts[1])
    except (IndexError, ValueError):
        seen_n = -1
    mark(not timed_out,
         "the fresh interpreter SHUT DOWN on its own",
         f"{elapsed:.1f}s, return code {rc}")
    mark(os.path.basename(seen_file) == GATE_MODULE_LEAF
         and os.path.abspath(seen_file).startswith(os.path.abspath(_ROOT)),
         "the child imported THIS file — proved by a probe FILE, never by a "
         "stream, because the stream is the thing on trial",
         seen_file or '(the child wrote no probe)')
    mark(seen_n == len(GATE_DOOR3_PATHS),
         f"the child finished all {len(GATE_DOOR3_PATHS)} paths — a child "
         f"that stopped early is a FAILURE, not a pass on an empty stream",
         f"it reported {seen_n}")
    mark(rc == 0 and wrote == b'',
         "IMPORT, three doorway calls and SHUTDOWN wrote nothing at all",
         '' if wrote == b'' else
         f"it wrote {wrote.decode('utf-8', 'replace')[:200]!r}")

    print("\n(r) A REAL READING — the Commander's OWN file, this computer's"
          "\n    OWN clock and its OWN timezone, through the doorway with no"
          "\n    arguments at all. Everything above judges inputs this gate"
          "\n    handed over, and a gate that ONLY does that never tests the"
          "\n    real thing and is decorative. The bar here is LOOSE ON"
          "\n    PURPOSE — never exact equality, which is R-021 with a new"
          "\n    name — but it is not nothing: the line must be shaped right"
          "\n    and it must not be empty.")
    live = section_text()
    print()
    for line in live.split('\n'):
        print(f"      {line}")
    print()
    live_lines = live.split('\n')
    head_re = re.compile(r'^  Events       : (\d+ ahead · next '
                         r'(today|tomorrow|in \d+ days)|⚠ NOTHING AHEAD)')
    mark(head_re.match(live_lines[0]) is not None,
         "the live line has the shape this gate expects",
         live_lines[0].strip())
    row_re = re.compile(r'^    (today {7}|tomorrow {4}|in \d+ days *)— .+ '
                        r'\(\w{3} \d{2} \w{3} \d{4}, \d{2}:\d{2} local\)$')
    rows = [l for l in live_lines if row_re.match(l)]
    quoted = [l for l in live_lines[1:-2] if l.startswith('    ')
              and not l.startswith('    ⚠')]
    # **A LIVE CALENDAR THAT HAS GENUINELY RUN OUT IS A PASS HERE, NOT A RED.**
    # Written after the first run of this gate: the version before it demanded
    # at least one event line, so on the day the last built-in date passes —
    # 08 Dec 2027 — this check would have gone red about the instrument
    # behaving EXACTLY as designed, and taught whoever saw it that a working
    # loud warning was a fault. The whole point of (c) is that the loud line
    # is the correct output; a live check that punished it would be arguing
    # with the bar this gate was declared under.
    mark(got_gone.split('\n')[0].startswith('  Events       : ⚠ NOTHING '
                                            'AHEAD'),
         "the prefix that branch keys on is the one the doorway REALLY prints "
         "when a calendar runs out — a typo there would make the branch dead "
         "code and nothing anywhere would say so")
    if live_lines[0].startswith('  Events       : ⚠ NOTHING AHEAD'):
        mark(not quoted,
             "the real calendar has run out and said so LOUDLY — the loud "
             "line is the pass here, not a failure")
    else:
        mark(bool(rows) and len(rows) == len(quoted),
             f"every one of the {len(quoted)} live event lines is counted, "
             f"named and dated in full")
    mark(live_lines[-1] == '   — information, not a signal)',
         "the live block still carries the real disclaimer, verbatim",
         live_lines[-1])

    print("\n(s) >>> THE SABOTAGE DRILL. Each break is installed, the"
          "\n    OBSERVABLE IT AFFECTS is captured honest and broken, and its"
          "\n    verdict counts ONLY IF THE TWO DIFFER. A break that cannot"
          "\n    change what anyone reads is reported INERT and FAILS this"
          "\n    gate — it is not a caught lie, it is a check testing nothing."
          "\n    F10, S6 and B1 were all exactly that, each found a"
          "\n    generation late. This file was built with the rule from"
          "\n    birth, and the twelve breaks below were NAMED IN"
          "\n    PROGRESS_LOG.md BEFORE ONE LINE OF THIS FILE WAS WRITTEN.")

    PAST_PATH = _file('pastonly.json', {
        'timezone': GATE_ET,
        'events': [{'date': '2026-01-01', 'name': 'Long gone'}]})
    NOTHING_EXPECTED = (
        '  Events       : ⚠ NOTHING AHEAD — every date this calendar knows '
        'is in the past\n'
        '  (from gatedata/pastonly.json and the built-in lists — '
        'GateList to 01 Sep 2026\n'
        '   — information, not a signal)'
    )
    mark(golden(path=PAST_PATH, recurring=()) == NOTHING_EXPECTED,
         "(the control for E12) a calendar with only past dates says so",
         golden(path=PAST_PATH, recurring=()).split('\n')[0].strip())

    _honest_section = section_text
    _honest_ahead = _ahead
    _honest_from_file = _from_file
    _honest_clip = _clip
    _honest_when = _when_words
    _honest_zone = _zone

    def w_golden():
        return golden()

    def w_long():
        return golden(path=LONG_PATH)

    def w_bad():
        return golden(path=BAD_PATH)

    def w_missing():
        return shipped()

    def w_expired():
        return shipped(now=EXPIRED_NOW)

    def w_nothing():
        return golden(path=PAST_PATH, recurring=())

    def w_stdout():
        return _capture(lambda: golden())

    def j_golden():
        return golden() == GOLDEN_EXPECTED

    def j_long():
        return golden(path=LONG_PATH).split('\n')[1] == EXPECT_LONG

    def j_bad():
        return golden(path=BAD_PATH) == BAD_EXPECTED

    def j_missing():
        return shipped() == SHIPPED_EXPECTED

    def j_expired():
        return shipped(now=EXPIRED_NOW) == EXPIRED_EXPECTED

    def j_nothing():
        return golden(path=PAST_PATH, recurring=()) == NOTHING_EXPECTED

    def j_silent():
        return _capture(lambda: golden()) == b''

    def _horizons_forever():
        return (('FOMC', '2099-01-01'), ('US CPI', '2099-01-01'))

    def _ahead_shows_the_past(known, now):
        return list(known)                      # E2: the past shown as coming

    def _ahead_reversed(known, now):
        return list(reversed(_honest_ahead(known, now)))   # E7: furthest first

    def _when_off_by_one(days):
        return _honest_when(days + 1)

    def _clip_silent(name):
        return ' '.join(str(name).split())[:60]

    def _from_file_no_count(path):
        entries, note, _refused = _honest_from_file(path)
        return entries, note, 0                 # E5: the refusals swallowed

    def _from_file_no_note(path):
        entries, _note, refused = _honest_from_file(path)
        return entries, '', refused             # E6: the absence swallowed

    def _zone_always_utc(name):
        return timezone.utc                     # E9: his declared zone ignored

    def _shout(*a, **k):
        block = _honest_section(*a, **k)
        print("  >> consider trimming exposure before the FOMC")
        return block

    SABOTAGES = [
        ('E1 ', 'the staleness guard switched off',
         'HORIZONS', _horizons_forever(), w_expired, j_expired),
        ('E2 ', 'a PAST event shown as coming',
         '_ahead', _ahead_shows_the_past, w_golden, j_golden),
        ('E3 ', 'the day count off by one',
         '_when_words', _when_off_by_one, w_golden, j_golden),
        ('E4 ', 'a long name clipped with NO visible mark',
         '_clip', _clip_silent, w_long, j_long),
        ('E5 ', 'a refused entry dropped SILENTLY (S10)',
         '_from_file', _from_file_no_count, w_bad, j_bad),
        ('E6 ', 'the missing-file absence swallowed',
         '_from_file', _from_file_no_note, w_missing, j_missing),
        ('E7 ', 'the events reversed — the furthest shown as next',
         '_ahead', _ahead_reversed, w_golden, j_golden),
        ('E8 ', 'the disclaimer quietly reworded',
         'FOOTER_TAIL', 'information)', w_golden, j_golden),
        ('E9 ', 'his declared timezone ignored, UTC assumed',
         '_zone', _zone_always_utc, w_golden, j_golden),
        ('E10', 'ADVICE printed, the block byte-identical (S15)',
         'section_text', _shout, w_stdout, j_silent),
        ('E11', 'a whole built-in list silently emptied',
         'RECURRING', RECURRING[:5], w_missing, j_missing),
        ('E12', 'the "nothing ahead" line replaced by silence',
         'NOTHING_AHEAD', '', w_nothing, j_nothing),
    ]

    print()
    for tag, words, attr, repl, witness, judge in SABOTAGES:
        honest_obs = witness()
        original = globals()[attr]
        globals()[attr] = repl
        try:
            broken_obs = witness()
        except Exception:
            broken_obs = '<the sabotage crashed the witness>'
        try:
            survived = judge()
        except Exception:
            survived = False          # a crash is a catch: it did not pass
        finally:
            globals()[attr] = original
        changed = broken_obs != honest_obs
        caught = not survived
        good = changed and caught
        if not changed:
            verdict = 'INERT — IT CHANGED NOTHING, SO ITS VERDICT IS WORTHLESS'
        elif caught:
            verdict = 'CAUGHT'
        else:
            verdict = 'ESCAPED — THE GATE IS DECORATIVE'
        mark(good, f"{tag} {words:<48} -> {verdict}",
             '' if good else f"changed={changed} caught={caught}")

    print("\n    ... and the originals are proved RESTORED, not assumed. A"
          "\n    drill that left a break installed would hand the next check a"
          "\n    sabotaged module and call the result evidence.")
    mark(golden() == GOLDEN_EXPECTED and shipped() == SHIPPED_EXPECTED,
         "after twelve breaks and twelve repairs, both blocks are byte-"
         "identical to where they started")
    mark(tuple(RECURRING) == EXPECT_RECURRING
         and tuple(HORIZONS) == (('FOMC', '2027-12-08'),
                                 ('US CPI', '2026-12-10'))
         and FOOTER_TAIL == 'information, not a signal)'
         and NOTHING_AHEAD.startswith('⚠ NOTHING AHEAD')
         and section_text is _honest_section and _ahead is _honest_ahead
         and _from_file is _honest_from_file and _clip is _honest_clip
         and _when_words is _honest_when and _zone is _honest_zone,
         "every constant and every function this drill touched is back")

    shutil.rmtree(os.path.dirname(GATE_DIR), ignore_errors=True)

    # ------------------------------------------------------------------
    ok = all(nonlocal_ok)
    reds = sum(1 for g in nonlocal_ok if not g)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 3.4 PASSED — {len(nonlocal_ok)} checks, 0 red.

The whole printed block was rebuilt from a file this gate wrote itself
and matched a copy typed out here CHARACTER FOR CHARACTER — on the
healthy path, with a file he broke four ways, with the file missing,
with no timezone declared, with a timezone this computer never heard
of, with two events on one day, with a name too long to print, and
with the clock pushed past every date this calendar knows.

THE STALENESS TRAP IS THE ONE THIS INSTRUMENT EXISTS TO SURVIVE, AND
IT IS NOT HYPOTHETICAL. The BLS publishes about a year ahead and its
schedule stops dead at 10 Dec 2026, so the built-in CPI list runs out
in roughly four months. Check (b) advances the clock to January 2027
rather than waiting for it, and requires the CPI list to be named as
ENDED while the FOMC list carries on working. Check (c) pushes past
both and requires a LOUD line: an empty deck line and a quiet month
look identical, and this ship has been bitten by that shape twice.

AND EVERY ONE OF THE TWELVE SABOTAGES WAS PROVED TO CHANGE WHAT
SOMEONE READS BEFORE ITS VERDICT WAS COUNTED — on the channel it
actually affects, which is why E10, whose returned block is byte-
identical to the honest one, is witnessed at the FILE DESCRIPTOR and
not at the block. The twelve were named in PROGRESS_LOG.md before one
line of this file was written.

WHAT THIS GATE DOES **NOT** PROVE, said here rather than in a footnote:
the FOMC and CPI dates were read off the Fed's and the BLS's own pages
on 2026-08-07 and this gate pins them to the byte — but NOTHING HERE
CAN TELL WHETHER AN AUTHORITY LATER MOVED A DATE. That is R-035, the
question nobody on this ship has ever asked, and here it is a hardcoded
list rather than a live feed, so it cannot even be re-read. The
horizons above are the guard against the list running out; they are
NOT a guard against a date CHANGING inside it.""")
    else:
        print(f"GATE 3.4 FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
