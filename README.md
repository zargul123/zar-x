# ZAR X

A personal trading cockpit. It watches the markets, briefs its pilot, computes honest
signal statistics, and calculates risk — **the pilot decides and clicks.** No auto-trading.

Born 2026-07-19, from the lessons of Zargul Trader 2.0
(museum: https://github.com/zargul123/zargul-trader-2.0 — see its PROGRESS_LOG.md and
the `prediction-chapter-closed` tag for the full honest history that led here).

## The mission
An edge over the undisciplined majority, built in layers (see EDGE_STACK_RESEARCH.md):
1. **Discipline Engine** — sizing, SL/TP, expectancy math, journal (certain edge)
2. **Chaos Avoidance** — regime vane, event calendar, news-storm flag (proven in our own data)
3-5. **Three sealed gauntlet slots** — slow trend core, positioning fade, on-chain cycle
   thermometer (probabilistic edge, honestly tested)
6. **Context Deck** — fear/greed, macro, news, cycles (information, never signals)

## THE PROMISE (carved at founding, unanimous: user + Claude + Kimi advisers)
Exactly **three** signal ideas get tested, with pass/fail gates declared **before** each
test. If all three fail: **no 4th slot, no re-tests, no paper-trading of failed rules.**
The cockpit becomes information-only. No new signal ideas for at least 3 months, and any
future idea must come from a genuinely new data source and face the same gauntlet.
The discipline is in stopping when the data says stop.

## Architecture law
Seven sealed compartments — `data/ indicators/ regime/ signals/ risk/ lab/ cockpit/`.
Each has its own smoke test. Each fails safe ("instrument offline") without stopping the
rest. Compartments talk only through small interfaces. Every change: explained first,
committed with full notes, result recorded in PROGRESS_LOG.md.
