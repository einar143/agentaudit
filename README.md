# agentaudit

[![CI](https://github.com/einar143/agentaudit/actions/workflows/ci.yml/badge.svg)](https://github.com/einar143/agentaudit/actions/workflows/ci.yml)

Static security scanner for AI-agent configuration: MCP server configs, agent
skills and hooks.

> Early skeleton. One rule so far.

## Why

An MCP config launches executables with your privileges. A skill is text the
model obeys. A hook is a shell command that fires on its own. All three are
attack surface, and none of them usually gets a security review.

## Usage

```bash
uv sync
uv run agentaudit scan path/to/project
uv run agentaudit scan path/to/project --format json
uv run agentaudit rules
```

Exit codes: `0` clean, `1` findings, `2` a file could not be parsed.

## Rules

| ID | Severity | Detects |
|---|---|---|
| [AA001](docs/rules/AA001.md) | high | MCP server launched from an unpinned package |

## Development

```bash
uv run pytest
uv run ruff check .
```

See `CONTRIBUTING.md` for the architecture and the rule contract, and `BACKLOG.md`
for what is next.
