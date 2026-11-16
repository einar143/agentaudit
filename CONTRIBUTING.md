# Contributing

agentaudit is a static security scanner for AI-agent configuration: MCP server
configs, agent skills, and hooks. These files launch executables, grant
permissions and feed trusted text to a model, yet they are rarely reviewed like
code. Depth and correctness matter more than rule count.

## Principles

- Changes land as a pull request with green CI, never as a direct push to
  `main`.
- Every commit is a real increment: a rule, a parser, a fix, a test. No filler
  commits (whitespace, README shuffles, version bumps with no change).
- Work comes from `BACKLOG.md`. If tests fail, fix them before adding anything.

## Commands

```bash
uv sync                       # install
uv run pytest                 # tests
uv run ruff check .           # lint
uv run ruff format --check .  # formatting
uv run agentaudit scan <path> # run the scanner
uv run agentaudit rules       # list rules
```

## Architecture

```
src/agentaudit/
├── cli.py          entry point (typer): scan, rules
├── discovery.py    find config files under a path
├── parsers/        file -> normalized model (one module per file kind)
├── model.py        McpServer, ScanTarget, Finding, Severity (pydantic)
├── rules/          one module per rule family; rules self-register
├── engine.py       discover -> parse -> run rules -> ScanResult
└── reporters/      terminal, json (SARIF is on the backlog)
```

Data flows one way: discovery -> parsers -> model -> rules -> reporters.
Rules only ever see the normalized model, never raw files. A new file format
means a new parser, not changes to rules.

## The rule contract

A rule is a class in `src/agentaudit/rules/` decorated with `@register`:

- `id`: `AA` + three digits, never reused. Families: `AA0xx` supply chain,
  `AA1xx` permissions, `AA2xx` injection, `AA3xx` secrets, `AA4xx` hooks,
  `AA5xx` toxic combinations.
- `title`, `severity`, and a `check(target)` that yields `Finding`s.
- Every finding carries a concrete `fix`.

A rule is done only when it ships with all four parts:

1. The detector.
2. Fixtures: `tests/fixtures/<id>/bad/` (must fire) and `good/` (must not).
3. A test asserting both, plus unit tests for any parsing helper.
4. `docs/rules/<ID>.md`: what it detects, why it matters, how to fix, known
   limits and false-positive cases.

False positives are bugs. When a detector cannot be sure, it stays silent and
the limit is written down in the rule doc.

## Conventions

- Python 3.11+, type hints everywhere, `ruff` clean.
- No network access during a scan. Static analysis only (a live mode is a
  separate, later feature).
- Fixtures never contain real secrets, real hostnames or anything copied from
  a private setup. Synthesize them.
- Exit codes: `0` clean, `1` findings, `2` a file could not be parsed.

## Roadmap

See `BACKLOG.md`. Items are sized to under an hour each with a definition of
done.
