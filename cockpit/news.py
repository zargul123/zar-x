"""
Zar X cockpit — the News instrument (Context Deck, Phase 3, Step 3.3).

Three crypto headlines and a 24-hour story count, read straight from five
publishers' own public feeds. It tells the pilot what the market has been
reading this morning. Nothing more.

INFORMATION, NEVER A SIGNAL. There is no sentiment score here, no weight, and
no number derived from a sentence. Turning a headline into a number is where a
system starts inventing things, and Phase 6's three signal slots are locked BY
NAME — none of them is news. A headline that is itself advice ("analysts say
buy the dip") is printed IN QUOTES AND ATTRIBUTED, because it is a fact that
someone said it — but this instrument's own voice never adopts it.

**WHY THE PUBLISHERS' OWN FEEDS AND NOT A NEWS API.** CryptoPanic became a paid
product; measured 2026-07-31 it answers HTTP 403 and 404 unauthenticated. The
structural reason matters more than that one death: a news API exists to be
sold, so its fresh usable data always ends up behind a payment. **A publisher's
feed exists to be spread as widely as possible, because that is how the
publisher gets readers.** The incentive points the other way and does not
change. No account, no key, no expiry, and no new dependency — Python's own
`xml.etree.ElementTree` reads them.

**THE TRAP THIS FILE IS SHAPED AROUND, MEASURED 2026-08-04 AND NOT HYPOTHETICAL.
Blockworks answers HTTP 200 with fifty real, well-formed, correctly-dated
stories — and the newest of them is 209 DAYS OLD.** The feed is abandoned and
nothing in the response says so. An instrument written the obvious way would
have printed a January headline on the Brief that morning under today's date,
and nothing anywhere would have said a word. **So a feed whose newest story is
older than DEAD_FEED_H is DEAD: it is named as no-data, and it contributes
neither a headline nor one unit of the count.** This is the same shape as the
recorder's empty-list trap, which is also guarded here: **HTTP 200 with zero
stories is a LOUD FAILURE, never "quiet news".**

The Block was dropped the same day: HTTP 403 on four addresses and two
user-agents. It is edge-blocked to non-browsers and there is no path in.

**LAW 2 — THE COMPARTMENT OWNS ITS SOURCE LIST.** The addresses below live in
this file and nowhere else, so a paid feed could be swapped in for a free one
in an afternoon, and the Commander can strike a publisher with one line.

Fail-safe (Law 3): every failure — no internet, a moved address, a feed that
changed shape overnight, all five publishers down at once — becomes one honest
offline line, and the Brief carries on with everything else intact.

Standalone smoke test:
    python cockpit/news.py          (live section, then the offline drill)
    python cockpit/news.py --gate   (gate 3.3, including the sabotage drill)
"""
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

import requests

# Law 2: the source list lives HERE and nowhere else. Five publishers, five
# different owners. NOT one hundred — beyond a handful, extra sources return
# THE SAME STORY reworded, which adds no information and actively corrupts the
# count: one ordinary story covered by fifty outlets would read as a storm.
# All five measured fresh 2026-08-04; see PROGRESS_LOG.md for the numbers and
# for the two that were dropped.
FEEDS = (
    ('CoinDesk',      'https://www.coindesk.com/arc/outboundfeeds/rss/'),
    ('Cointelegraph', 'https://cointelegraph.com/rss'),
    ('Decrypt',       'https://decrypt.co/feed'),
    ('BeInCrypto',    'https://beincrypto.com/feed/'),
    ('Bitcoin.com',   'https://news.bitcoin.com/feed/'),
)

HEADLINES = 3          # how many stories are quoted; the rest are only counted
WINDOW_H = 24          # the count's window, in hours
DEAD_FEED_H = 48       # newest story older than this => the feed is ABANDONED
TITLE_MAX = 84         # a headline longer than this is clipped VISIBLY
CLIP_MARK = '…'
TIMEOUT = 12           # seconds; one attempt per publisher, never a retry storm

# Sent because several publishers' edges refuse an unlabelled caller outright.
USER_AGENT = 'Mozilla/5.0 (compatible; ZarX/1.0; morning brief reader)'

OFFLINE_WORDS = "News instrument offline"
FOOTER_TAIL = "publishers — information, not a signal)"
ATOM = '{http://www.w3.org/2005/Atom}'

# Used only by the offline drill: the .invalid top-level domain is reserved by
# the RFCs and can never resolve, so the drill proves the fail-safe without
# unplugging the Commander's internet.
OFFLINE_DRILL_URL = 'https://zar-x-offline-drill.invalid/feed'


class FeedError(Exception):
    """One publisher's failure. Never leaks a traceback to the Brief; the
    doorway turns it into a named absence or one honest line."""


def _fetch(url, timeout):
    """The only network call in this part. One request, no retries."""
    r = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=timeout)
    r.raise_for_status()
    return r.content


def _when_rss(text):
    """RFC 822 -> aware UTC datetime, or None. A feed that dates its stories in
    a shape we do not understand has NOT given us a date, and a story whose age
    we cannot state is a story we refuse to quote."""
    if not text:
        return None
    try:
        d = parsedate_to_datetime(text)
    except Exception:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _when_atom(text):
    """ISO 8601 -> aware UTC datetime, or None."""
    if not text:
        return None
    try:
        d = datetime.fromisoformat(text.replace('Z', '+00:00'))
    except Exception:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _parse(raw):
    """Feed bytes -> newest-first [(when, title, story_id)]. Raises on anything
    this part cannot honestly read.

    **ZERO STORIES IS RAISED, NOT RETURNED AS EMPTINESS.** That is the whole
    point of this function. A feed answering HTTP 200 with nothing in it is
    broken, and printing "0 headlines" as though the world were quiet is the
    single worst thing this instrument could do.
    """
    root = ET.fromstring(raw)
    found = []
    for item in root.iter('item'):                       # RSS 2.0
        found.append((_when_rss(item.findtext('pubDate')),
                      (item.findtext('title') or '').strip(),
                      (item.findtext('guid') or item.findtext('link')
                       or '').strip()))
    if not found:
        for entry in root.iter(ATOM + 'entry'):          # Atom
            found.append((_when_atom(entry.findtext(ATOM + 'published')
                                     or entry.findtext(ATOM + 'updated')),
                          (entry.findtext(ATOM + 'title') or '').strip(),
                          (entry.findtext(ATOM + 'id') or '').strip()))
    if not found:
        raise FeedError("HTTP 200 with ZERO stories — a broken feed, not "
                        "quiet news")
    usable = [s for s in found if s[0] is not None and s[1] and s[2]]
    if not usable:
        raise FeedError(f"{len(found)} stories and not one with a usable date, "
                        f"title and id")
    usable.sort(key=lambda s: s[0], reverse=True)
    return usable


def _age_words(seconds: float) -> str:
    """A spoken age. Never negative: a publisher whose clock runs ahead of ours
    must not put '-3m ago' on the Brief."""
    minutes = int(max(0.0, seconds) // 60)
    if minutes < 1:
        return "just now"
    if minutes < 60:
        return f"{minutes}m ago"
    return f"{minutes // 60}h{minutes % 60:02d}m ago"


def _clip(title: str) -> str:
    """Whitespace flattened so a headline can never break the deck's layout,
    and anything over TITLE_MAX clipped with a mark the reader can SEE. A
    silent truncation would be this instrument quietly rewriting a publisher."""
    flat = ' '.join(title.split())
    if len(flat) <= TITLE_MAX:
        return flat
    return flat[:TITLE_MAX - 1].rstrip() + CLIP_MARK


def _gather(now, feeds, fetched, timeout):
    """-> (stories newest-first, names of the publishers that gave nothing).

    `fetched` is the ONE FETCH, TWO READERS door: a caller that already holds
    the raw bytes hands them over, so a judge and this function read byte-
    identical input and cannot disagree merely because a story landed between
    two requests. Measured 2026-08-04: a publisher lands about one story an
    hour, so that collision is rare — but rare is not never, and a gate that
    goes red when nothing is wrong is a gate people learn to ignore.
    """
    live, dead, seen = [], [], set()
    for name, url in feeds:
        try:
            raw = _fetch(url, timeout) if fetched is None else fetched.get(name)
            if raw is None:
                raise FeedError("no bytes for this publisher")
            stories = _parse(raw)
            age_h = (now - stories[0][0]).total_seconds() / 3600.0
            if age_h > DEAD_FEED_H:
                # Blockworks, measured 2026-08-04: HTTP 200, fifty perfect
                # stories, newest 209 days old. It looks healthier than a
                # healthy feed, which is exactly why it needs its own guard.
                raise FeedError(f"newest story is {age_h / 24:.0f} days old — "
                                f"this feed is abandoned")
            for when, title, story_id in stories:
                key = (name, story_id)
                if key in seen:
                    continue                    # the same story twice counts once
                seen.add(key)
                if 0 <= (now - when).total_seconds() <= WINDOW_H * 3600:
                    live.append((when, title, name))
        except Exception:
            dead.append(name)                   # NAMED, never silently dropped
    live.sort(key=lambda s: s[0], reverse=True)
    return live, dead


def section_text(feeds=None, fetched=None, timeout=TIMEOUT, now=None):
    """The Context Deck block the Brief prints — this part's single doorway.

    Never raises and never prints; it RETURNS. On any failure the deck still
    appears, carrying one line that says so. `feeds` and `fetched` are
    injectable so the drills can point this at an unreachable address, or hand
    it known bytes, without disconnecting anything.
    """
    try:
        feeds = FEEDS if feeds is None else feeds
        now = datetime.now(timezone.utc) if now is None else now
        stories, dead = _gather(now, feeds, fetched, timeout)
        alive = len(feeds) - len(dead)
        if not stories:
            # Publishers may all be down, or all be dead feeds, or the window
            # may be genuinely empty. At the measured rate — five publishers,
            # about one story an hour each — an empty 24 hours is not quiet
            # news, it is a fault. It is reported as one.
            raise FeedError(f"no story inside {WINDOW_H}h from any of "
                            f"{len(feeds)} publishers ({alive} answered)")
        missing = f"   [no data: {', '.join(dead)}]" if dead else ""
        lines = [f"  News ({WINDOW_H}h)   : {len(stories)} stories from "
                 f"{alive} of {len(feeds)} publishers{missing}"]
        for when, title, source in stories[:HEADLINES]:
            age = _age_words((now - when).total_seconds())
            lines.append(f'    "{_clip(title)}" — {source}, {age}')
        lines.append(f"  (crypto headlines from {len(feeds)} {FOOTER_TAIL}")
        return "\n".join(lines)
    except Exception as e:
        return f"  🔌 {OFFLINE_WORDS} ({type(e).__name__})"


if __name__ == '__main__':
    if '--gate' not in sys.argv:
        print(section_text())
        print()
        print("--- offline drill: every publisher pointed at an unreachable "
              "address, internet untouched ---")
        print(section_text(feeds=tuple((n, OFFLINE_DRILL_URL)
                                       for n, _ in FEEDS)))
        sys.exit(0)

    # =====================================================================
    # GATE 3.3 — declared in PROGRESS_LOG.md on 2026-08-04 and committed
    # ALONE, with no .py in that commit, BEFORE this file existed. Commit
    # 016024e; `git show --stat 016024e` is the proof the bar came first.
    #
    # THIS FILE IS THE SECOND ON THIS SHIP BUILT WITH THE RULE FROM BIRTH:
    # **A SABOTAGE MUST BE PROVED TO CHANGE THE OUTPUT BEFORE ITS VERDICT
    # MEANS ANYTHING.** F10, S6 and B1 were the same fault in three files —
    # a deliberate break that could not change what anyone read, scored
    # ESCAPED, turning a gate red about a lie it had never managed to tell.
    # Each cost a different generation a session to retrofit. Here, every
    # sabotage below is run twice — honest and broken — and its verdict is
    # only counted if the two OBSERVABLES DIFFER. An unprovable sabotage is
    # reported INERT and FAILS this gate.
    #
    # AND THE OBSERVABLE IS PER-SABOTAGE, WHICH IS THE PART THAT IS EASY TO
    # GET WRONG. N10 changes nothing about the returned block — it prints
    # to stdout while returning byte-identical text, which is exactly what
    # S15 did. Its witness is therefore CAPTURED STDOUT, not the block. A
    # drill that measured every sabotage on one channel would score N10
    # INERT and delete the only check that catches it.
    # =====================================================================
    import io
    import re
    from datetime import timedelta

    NOW = datetime(2026, 8, 4, 12, 0, 0, tzinfo=timezone.utc)

    def mark(good, text, detail=''):
        nonlocal_ok.append(good)
        print(f"   {'✓' if good else '✗'} {text}")
        if detail:
            print(f"        {detail}")
        return good

    nonlocal_ok = []

    # ---- the gate's OWN feed builder. Door 1: this gate never asks the
    # module to make its input, never reads its expectation out of the file
    # on trial, and never calls a helper under test to judge itself.
    def _esc(text):
        return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;'))

    def _rss(items):
        """[(when, title, id)] -> RSS 2.0 bytes, built here from nothing."""
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<rss version="2.0"><channel><title>gate</title>']
        for when, title, sid in items:
            stamp = when.strftime('%a, %d %b %Y %H:%M:%S +0000')
            out.append('<item><title>' + _esc(title) + '</title>'
                       '<guid>' + _esc(sid) + '</guid>'
                       '<pubDate>' + stamp + '</pubDate></item>')
        out.append('</channel></rss>')
        return ''.join(out).encode('utf-8')

    def ago(minutes):
        return NOW - timedelta(minutes=minutes)

    GATE_FEEDS = (('CoinDesk', 'https://gate.invalid/a'),
                  ('Cointelegraph', 'https://gate.invalid/b'),
                  ('Decrypt', 'https://gate.invalid/c'),
                  ('BeInCrypto', 'https://gate.invalid/d'),
                  ('Bitcoin.com', 'https://gate.invalid/e'))

    # Every awkward case the orders named, planted on purpose:
    #   cd-1 twice ......... the same story id twice must count ONCE      (p)
    #   ct-1 ............... accents, a currency symbol and an emoji      (h)
    #   dc-1 ............... a headline that is ADVICE                    (j)
    #   cs-1 ............... a headline carrying our OWN disclaimer words (k)
    #   bc-1 at 1500 min ... outside the 24h window, must NOT be counted  (q)
    ADVICE = 'Analysts say buy the dip as support holds'
    UNICODE_TITLE = "Café's café — a naïve €5 latte, 90% of traders 🚀"
    DISCLAIMER_ECHO = 'Exchange says it is information, not a signal'
    GOLDEN_BYTES = {
        'CoinDesk': _rss([(ago(5), 'Bitcoin ETF inflows hit a fresh weekly high', 'cd-1'),
                          (ago(5), 'Bitcoin ETF inflows hit a fresh weekly high', 'cd-1'),
                          (ago(200), 'Custody firm files for a trust charter', 'cd-2')]),
        'Cointelegraph': _rss([(ago(61), UNICODE_TITLE, 'ct-1')]),
        'Decrypt': _rss([(ago(125), ADVICE, 'dc-1')]),
        'BeInCrypto': _rss([(ago(300), DISCLAIMER_ECHO, 'cs-1')]),
        'Bitcoin.com': _rss([(ago(400), 'Miners report a quiet quarter', 'bc-2'),
                             (ago(1500), 'A story from the day before', 'bc-1')]),
    }
    # Typed out HERE, character by character, by a gate that did not build it.
    GOLDEN_EXPECTED = (
        '  News (24h)   : 6 stories from 5 of 5 publishers\n'
        '    "Bitcoin ETF inflows hit a fresh weekly high" — CoinDesk, 5m ago\n'
        '    "' + UNICODE_TITLE + '" — Cointelegraph, 1h01m ago\n'
        '    "' + ADVICE + '" — Decrypt, 2h05m ago\n'
        '  (crypto headlines from 5 publishers — information, not a signal)'
    )
    OFFLINE_EXPECTED = '  🔌 News instrument offline (FeedError)'

    def golden(**kw):
        args = dict(feeds=GATE_FEEDS, fetched=GOLDEN_BYTES, now=NOW)
        args.update(kw)
        return section_text(**args)

    print("=" * 70)
    print("  GATE 3.3 — the News instrument")
    print("=" * 70)

    print("\n(a) THE MEASUREMENT CAME FIRST. R-036 was measured on 2026-08-04"
          "\n    and written into PROGRESS_LOG.md in commit 016024e, which"
          "\n    carries this gate's bar and NO .py file. 0 of 4 feeds changed"
          "\n    their top story in 90 s; a publisher lands ~1 story an hour."
          "\n    The collision is real but RARE — so the one-fetch-two-readers"
          "\n    door below is insurance, and it is what makes (b) exact.")

    print("\n(b) INJECTED BYTES, EXACT EQUALITY — the gate builds five feeds"
          "\n    from its own constants, hands the SAME bytes to the doorway,"
          "\n    and demands the WHOLE block match a copy typed out in this"
          "\n    gate, character for character. 'The words are present' is the"
          "\n    bar S14 walked straight through and it is not used anywhere"
          "\n    in this file.")
    got = golden()
    same = got == GOLDEN_EXPECTED
    mark(same, "the whole block matched the gate's own copy BYTE FOR BYTE")
    if not same:
        print("     ---- the gate expected ----")
        for line in GOLDEN_EXPECTED.split('\n'):
            print(f"     {line!r}")
        print("     ---- the doorway returned ----")
        for line in got.split('\n'):
            print(f"     {line!r}")

    print("\n(p) DEDUPLICATION and (q) THE WINDOW — both are inside that one"
          "\n    equality and neither is taken on trust: CoinDesk's feed"
          "\n    carries story 'cd-1' TWICE, and Bitcoin.com carries a story"
          "\n    1500 minutes old. Seven story elements went in; the count"
          "\n    line says SIX.")
    mark('6 stories' in got.split('\n')[0],
         "the duplicate counted once and the 25-hour-old story was excluded",
         f"count line: {got.split(chr(10))[0].strip()!r}")

    print("\n(h) NON-ASCII SURVIVES BYTE FOR BYTE — accents, an apostrophe, a"
          "\n    currency symbol and an emoji. This ship has been bitten by"
          "\n    character corruption twice, both times found by a person"
          "\n    reading rather than by any check. This is the check.")
    mark(UNICODE_TITLE in got and got.encode('utf-8').decode('utf-8') == got,
         "the headline round-tripped exactly",
         repr(UNICODE_TITLE))

    print("\n(j) A HEADLINE THAT IS ADVICE is printed IN QUOTES and ATTRIBUTED"
          "\n    — it is a FACT that someone said it — and the instrument's own"
          "\n    voice never adopts it. F7 and S15 exist because a doorway once"
          "\n    printed advice of its own.")
    advice_line = [l for l in got.split('\n') if ADVICE in l]
    voice = [l for l in got.split('\n') if not l.startswith('    "')]
    mark(len(advice_line) == 1
         and advice_line[0] == f'    "{ADVICE}" — Decrypt, 2h05m ago',
         "the advice headline is quoted and attributed to its publisher",
         advice_line[0].strip() if advice_line else '(missing)')
    mark(all(('buy' not in l and 'sell' not in l and 'should' not in l
              and '>>' not in l) for l in voice),
         "every line the instrument speaks in its OWN voice is free of advice",
         f"{len(voice)} own-voice line(s) checked")

    print("\n(k) A HEADLINE CARRYING THIS SHIP'S OWN DISCLAIMER WORDING"
          "\n    satisfies nothing. BeInCrypto's story is literally"
          "\n    'Exchange says it is information, not a signal'. A gate that"
          "\n    checked 'are the words present' would pass on the HEADLINE"
          "\n    while the real disclaimer was gone. That is S14.")
    mark(got.split('\n')[-1]
         == '  (crypto headlines from 5 publishers — information, not a signal)',
         "the real disclaimer is checked as the LAST LINE, not as words "
         "anywhere")

    print("\n(i) A VERY LONG HEADLINE IS CLIPPED VISIBLY — never silently. A"
          "\n    silent truncation is this instrument quietly rewriting a"
          "\n    publisher, and nothing on the screen would say so.")
    LONG = ('Regulators unveil a sweeping new framework for digital asset '
            'custody, reporting and disclosure across every member state')
    long_bytes = dict(GOLDEN_BYTES)
    long_bytes['CoinDesk'] = _rss([(ago(1), LONG, 'cd-long')])
    long_block = golden(fetched=long_bytes)
    long_line = long_block.split('\n')[1]
    expect_long = ('    "Regulators unveil a sweeping new framework for '
                   'digital asset custody, reporting and…" — CoinDesk, '
                   '1m ago')
    mark(long_line == expect_long,
         "clipped to 84 characters and marked with a visible ellipsis",
         f"len(headline)={len(LONG)} -> printed {len(long_line) - 26} chars")

    print("\n(d) >>> THE DEAD-FEED GUARD. EARNED TODAY, NOT IMAGINED."
          "\n    Blockworks answers HTTP 200 with FIFTY real, well-formed,"
          "\n    correctly-dated stories whose newest is 209 DAYS OLD. It looks"
          "\n    healthier than a healthy feed. A January headline would have"
          "\n    gone on the Brief under today's date with nothing saying a"
          "\n    word. Here BeInCrypto is served a feed of that exact shape:"
          "\n    it must be NAMED as no-data and contribute NEITHER a headline"
          "\n    NOR one unit of the count.")
    dead_bytes = dict(GOLDEN_BYTES)
    dead_bytes['BeInCrypto'] = _rss(
        [(ago(209 * 24 * 60 + m), f'A perfectly formed January story {m}',
          f'bw-{m}') for m in range(0, 50)])
    dead_block = golden(fetched=dead_bytes)
    dead_expect = (
        '  News (24h)   : 5 stories from 4 of 5 publishers   '
        '[no data: BeInCrypto]\n'
        '    "Bitcoin ETF inflows hit a fresh weekly high" — CoinDesk, 5m ago\n'
        '    "' + UNICODE_TITLE + '" — Cointelegraph, 1h01m ago\n'
        '    "' + ADVICE + '" — Decrypt, 2h05m ago\n'
        '  (crypto headlines from 5 publishers — information, not a signal)'
    )
    mark(dead_block == dead_expect,
         "fifty perfect stale stories were refused, the publisher was NAMED, "
         "and the count fell 6 -> 5",
         dead_block.split('\n')[0].strip())
    mark(not any('January' in l for l in dead_block.split('\n')),
         "not one stale headline reached the block")

    print("\n(e) THE EMPTY-FEED GUARD — HTTP 200 with ZERO stories is a LOUD"
          "\n    failure for that publisher, never quiet weather. This is the"
          "\n    recorder's empty-list trap in a new hat, and `cryptocurrency.cv`"
          "\n    really did answer this way during the 2026-07-31 probe.")
    empty_bytes = dict(GOLDEN_BYTES)
    empty_bytes['Decrypt'] = _rss([])
    empty_block = golden(fetched=empty_bytes)
    mark('[no data: Decrypt]' in empty_block.split('\n')[0]
         and '4 of 5 publishers' in empty_block.split('\n')[0],
         "an empty feed was named as no-data, not counted as silence",
         empty_block.split('\n')[0].strip())

    print("\n(f) ONE PUBLISHER DOWN, THE OTHERS UP — the block prints what"
          "\n    answered and NAMES what did not, exactly as funding prints"
          "\n    `[no data: SOL]`. Silently dropping a source is S10. Each"
          "\n    publisher takes its TURN at being the one that fails: a"
          "\n    doorway that named every absence 'Decrypt' would agree with a"
          "\n    drill that only ever broke Decrypt.")
    for victim, _url in GATE_FEEDS:
        hurt = dict(GOLDEN_BYTES)
        hurt[victim] = b'<html>404 not found</html>'
        block = golden(fetched=hurt)
        head = block.split('\n')[0]
        mark(f'[no data: {victim}]' in head and '4 of 5 publishers' in head,
             f"{victim} down -> named by its OWN name",
             head.strip())

    print("\n(g) ALL PUBLISHERS DOWN — one honest line, no traceback, nothing"
          "\n    appended. Judged by EXACT EQUALITY against a copy typed out in"
          "\n    this gate: sabotage S13 once appended a fabricated figure to a"
          "\n    line like this and the old 'words present' bar passed it.")
    all_down = golden(fetched={n: None for n, _ in GATE_FEEDS})
    mark(all_down == OFFLINE_EXPECTED,
         "the offline line matched the gate's own copy exactly",
         repr(all_down))

    print("\n    ... and the same on the REAL offline path: every publisher"
          "\n    pointed at an address the RFCs guarantee can never resolve,"
          "\n    the internet untouched.")
    unreachable = golden(feeds=tuple((n, OFFLINE_DRILL_URL)
                                     for n, _ in GATE_FEEDS), fetched=None)
    mark(unreachable == OFFLINE_EXPECTED,
         "a real unresolvable address produced the same honest line",
         repr(unreachable))

    print("\n(m) DOOR 1 — THE GATE HOLDS ITS OWN EXPECTATIONS. Every string"
          "\n    above is typed out in this gate. The one thing a live check"
          "\n    cannot type out is the source list itself, so it is checked"
          "\n    HERE against five names written in this gate — R-014 was a"
          "\n    gate reading its own expectation out of the file on trial.")
    EXPECT_NAMES = ('CoinDesk', 'Cointelegraph', 'Decrypt', 'BeInCrypto',
                    'Bitcoin.com')
    mark(tuple(n for n, _ in FEEDS) == EXPECT_NAMES,
         "the module ships exactly the five publishers this gate names",
         str(tuple(n for n, _ in FEEDS)))
    mark(all(u.startswith('https://') for _, u in FEEDS),
         "every address is https")

    print("\n(n) DOOR 2 — THE DOORWAY NEVER RAISES. Law 3: the Brief must"
          "\n    survive any failure of any instrument. Eight shapes of broken"
          "\n    input, each one required to RETURN rather than throw.")
    poisons = [
        ('not xml at all', b'hello'),
        ('empty bytes', b''),
        ('xml, no feed', b'<?xml version="1.0"?><nothing/>'),
        ('item with no title', b'<rss><channel><item><guid>x</guid>'
                               b'<pubDate>Mon, 04 Aug 2026 11:00:00 +0000'
                               b'</pubDate></item></channel></rss>'),
        ('item with no date', b'<rss><channel><item><title>t</title>'
                              b'<guid>x</guid></item></channel></rss>'),
        ('unparseable date', b'<rss><channel><item><title>t</title><guid>x'
                             b'</guid><pubDate>tomorrow-ish</pubDate></item>'
                             b'</channel></rss>'),
        ('a gigabyte of nothing', b'<rss><channel>' + b'<!-- -->' * 5000
                                  + b'</channel></rss>'),
        ('bytes are None', None),
    ]
    for label, poison in poisons:
        bad = dict(GOLDEN_BYTES)
        bad['Decrypt'] = poison
        try:
            out = golden(fetched=bad)
            raised = False
        except Exception as exc:
            out = f'{type(exc).__name__}: {exc}'
            raised = True
        mark(not raised and isinstance(out, str) and out,
             f"{label:<24} -> returned, did not raise",
             out.split('\n')[0].strip()[:70])

    print("\n(o) DOOR 3 — THE DOORWAY IS SILENT, AND THE EAR IS PROVED TO HEAR"
          "\n    BEFORE ITS SILENCE IS BELIEVED. Three green ticks reading 'it"
          "\n    printed nothing' is exactly what a DEAF listener prints."
          "\n    **WHAT IS ACTUALLY TESTED HERE, said plainly because R-033 is"
          "\n    on the books for a door-3 pass line that claimed more than it"
          "\n    checked: this listens at sys.stdout and sys.stderr — the"
          "\n    PYTHON level — on four paths. It does NOT listen at the file"
          "\n    descriptor, and it does NOT test a write deferred to a thread"
          "\n    or to an atexit handler. Those are named in REVIEW_QUEUE.md as"
          "\n    an open gap, not quietly left out.**")

    def _listen(fn):
        out, err = io.StringIO(), io.StringIO()
        keep_o, keep_e = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = out, err
        try:
            value = fn()
        finally:
            sys.stdout, sys.stderr = keep_o, keep_e
        return value, out.getvalue() + err.getvalue()

    _, heard = _listen(lambda: (print('EAR-MARKER-STDOUT'),
                                print('EAR-MARKER-STDERR', file=sys.stderr)))
    mark('EAR-MARKER-STDOUT' in heard and 'EAR-MARKER-STDERR' in heard,
         "the ear proved it can hear down BOTH routes before being trusted",
         f"heard {len(heard)} bytes")

    for label, fn in (('healthy', lambda: golden()),
                      ('one publisher down',
                       lambda: golden(fetched={**GOLDEN_BYTES,
                                               'Decrypt': None})),
                      ('all publishers down',
                       lambda: golden(fetched={n: None
                                               for n, _ in GATE_FEEDS})),
                      ('a REAL live fetch', lambda: section_text())):
        value, heard = _listen(fn)
        mark(heard == '' and isinstance(value, str),
             f"{label:<20} -> the doorway wrote NOTHING to stdout or stderr",
             f"returned {len(value)} chars, heard {len(heard)}")

    print("\n(c) A REAL LIVE FETCH, LOOSE ON PURPOSE — everything above judges"
          "\n    bytes this gate handed over, and a gate that ONLY does that"
          "\n    never tests the trip to the internet and is decorative. So"
          "\n    this one reaches the real publishers, and the bar is only"
          "\n    that something headline-shaped came back. NEVER exact"
          "\n    equality — that is R-021 with a new name.")
    live = section_text()
    print()
    for line in live.split('\n'):
        print(f"      {line}")
    print()
    lines = live.split('\n')
    head_re = re.compile(r'^  News \(24h\)   : (\d+) stories from (\d) of 5 '
                         r'publishers')
    m = head_re.match(lines[0]) if lines else None
    mark(m is not None, "the live count line has the shape this gate expects",
         lines[0].strip() if lines else '(nothing)')
    if m:
        mark(int(m.group(1)) >= 3,
             f"at least 3 stories inside 24h (got {m.group(1)})")
        mark(int(m.group(2)) >= 3,
             f"at least 3 of 5 publishers answered (got {m.group(2)})")
    story_re = re.compile(r'^    ".+" — .+, (just now|\d+m ago|\d+h\d\dm ago)$')
    quoted = [l for l in lines if l.startswith('    "')]
    mark(len(quoted) >= 1 and all(story_re.match(l) for l in quoted),
         f"every one of the {len(quoted)} live headlines is quoted, "
         f"attributed and aged")
    mark(lines[-1] == '  (crypto headlines from 5 publishers — information, '
                      'not a signal)',
         "the live block still carries the real disclaimer, verbatim")

    print("\n(l) >>> THE SABOTAGE DRILL, AND THE RULE THIS SHIP PAID FOUR"
          "\n    SESSIONS FOR. Each break is installed, the OBSERVABLE IT"
          "\n    AFFECTS is captured honest and broken, and its verdict counts"
          "\n    ONLY IF THE TWO DIFFER. A break that cannot change what"
          "\n    anyone reads is reported INERT and FAILS this gate — it is"
          "\n    not a caught lie, it is a check testing nothing. F10, S6 and"
          "\n    B1 were all exactly that, each found a generation late.")

    def w_golden():
        return golden()

    def w_long():
        return golden(fetched=long_bytes)

    def w_dead():
        return golden(fetched=dead_bytes)

    def w_down():
        hurt = dict(GOLDEN_BYTES)
        hurt['Decrypt'] = b'<html>404</html>'
        return golden(fetched=hurt)

    def w_stdout():
        _, heard = _listen(lambda: golden())
        return heard

    def w_names():
        return str(tuple(n for n, _ in FEEDS))

    def j_golden():
        return golden() == GOLDEN_EXPECTED

    def j_long():
        return golden(fetched=long_bytes).split('\n')[1] == expect_long

    def j_dead():
        return golden(fetched=dead_bytes) == dead_expect

    def j_down():
        hurt = dict(GOLDEN_BYTES)
        hurt['Decrypt'] = b'<html>404</html>'
        head = golden(fetched=hurt).split('\n')[0]
        return '[no data: Decrypt]' in head and '4 of 5 publishers' in head

    def j_silent():
        _, heard = _listen(lambda: golden())
        return heard == ''

    def j_names():
        return tuple(n for n, _ in FEEDS) == EXPECT_NAMES

    def _shout(*a, **k):
        block = _honest_section(*a, **k)
        print("  >> consider trimming exposure before the weekend")
        return block

    def _clip_silent(title):
        flat = ' '.join(title.split())
        return flat[:84]

    def _age_wrong(seconds):
        minutes = int(max(0.0, seconds) // 60) + 60
        if minutes < 60:
            return f"{minutes}m ago"
        return f"{minutes // 60}h{minutes % 60:02d}m ago"

    _honest_gather = _gather

    def _gather_silent_drop(now, feeds, fetched, timeout):
        live, _dead = _honest_gather(now, feeds, fetched, timeout)
        return live, []                      # S10: the absence is swallowed

    def _gather_oldest_first(now, feeds, fetched, timeout):
        live, dead = _honest_gather(now, feeds, fetched, timeout)
        return list(reversed(live)), dead    # the THREE OLDEST, shown as new

    def _gather_misattribute(now, feeds, fetched, timeout):
        live, dead = _honest_gather(now, feeds, fetched, timeout)
        names = [s[2] for s in live]
        return ([(w, t, names[(i + 1) % len(names)])
                 for i, (w, t, _n) in enumerate(live)], dead)

    _honest_section = section_text

    SABOTAGES = [
        ('N1 ', 'the 24h window silently becomes a WEEK',
         'WINDOW_H', 168, w_golden, j_golden),
        ('N2 ', 'only ONE headline is shown, not three',
         'HEADLINES', 1, w_golden, j_golden),
        ('N3 ', 'the DEAD-FEED guard is switched off',
         'DEAD_FEED_H', 10 ** 9, w_dead, j_dead),
        ('N4 ', 'long headlines clipped with NO visible mark',
         '_clip', _clip_silent, w_long, j_long),
        ('N5 ', 'every story aged an hour older than it is',
         '_age_words', _age_wrong, w_golden, j_golden),
        ('N6 ', 'a failed publisher is dropped SILENTLY (S10)',
         '_gather', _gather_silent_drop, w_down, j_down),
        ('N7 ', 'headlines attributed to the WRONG publisher',
         '_gather', _gather_misattribute, w_golden, j_golden),
        ('N8 ', 'the disclaimer is quietly reworded',
         'FOOTER_TAIL', 'publishers)', w_golden, j_golden),
        ('N9 ', 'the THREE OLDEST stories shown as the newest',
         '_gather', _gather_oldest_first, w_golden, j_golden),
        ('N10', 'ADVICE printed to stdout, block unchanged (S15)',
         'section_text', _shout, w_stdout, j_silent),
        ('N11', 'a publisher vanishes from the source list',
         'FEEDS', FEEDS[:4], w_names, j_names),
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
        mark(good, f"{tag} {words:<47} -> {verdict}",
             '' if good else f"changed={changed} caught={caught}")

    print("\n    ... and the originals are proved RESTORED, not assumed. A"
          "\n    drill that left a break installed would hand the next check a"
          "\n    sabotaged module and call the result evidence.")
    mark(golden() == GOLDEN_EXPECTED,
         "after eleven breaks and eleven repairs, the block is byte-identical "
         "to where it started")
    mark(tuple(n for n, _ in FEEDS) == EXPECT_NAMES
         and WINDOW_H == 24 and HEADLINES == 3 and DEAD_FEED_H == 48
         and section_text is _honest_section and _gather is _honest_gather,
         "every constant and every function this drill touched is back")

    # ------------------------------------------------------------------
    ok = all(nonlocal_ok)
    reds = sum(1 for g in nonlocal_ok if not g)
    print("\n" + "=" * 70)
    if ok:
        print(f"""GATE 3.3 PASSED — {len(nonlocal_ok)} checks, 0 red.

The whole printed block was rebuilt from bytes this gate built itself
and matched a copy typed out here CHARACTER FOR CHARACTER, on the
healthy path, with a dead feed, with an empty feed, with each of the
five publishers taking its turn at failing, and with all five down.
Every expectation in this gate is typed out here rather than read from
the file on trial. The real internet was reached once, judged LOOSELY
on purpose, because a gate that only ever judges bytes it handed over
never tests the trip and is decorative.

AND EVERY ONE OF THE ELEVEN SABOTAGES WAS PROVED TO CHANGE WHAT SOMEONE
READS BEFORE ITS VERDICT WAS COUNTED — on the channel it actually
affects, which is why N10, whose returned block is byte-identical to
the honest one, is witnessed at STDOUT and not at the block. F10, S6
and B1 were each a break that could not change anything, scored ESCAPED
by three different gates, and each cost a generation to find. This file
was built with that rule from birth.

WHAT THIS GATE DOES **NOT** PROVE, said here rather than in a footnote:
door 3 listens at sys.stdout and sys.stderr, NOT at the file descriptor,
and nothing here tests a write deferred to a thread or an atexit
handler. The two cockpit instruments have that machinery and this one
does not yet. It is filed OPEN in REVIEW_QUEUE.md.""")
    else:
        print(f"GATE 3.3 FAILED — {reds} red of {len(nonlocal_ok)} checks.")
    print("=" * 70)
    sys.exit(0 if ok else 1)
