# Backlog

Ordered. Each item is under an hour and done only when the rule contract in
`CONTRIBUTING.md` is met (detector, fixtures, tests, doc).

## Foundations

- [ ] **Line numbers in findings.** Parse JSON with position tracking so a
      finding points at `file:line`. Done: AA001 findings carry a line number.
- [ ] **SARIF reporter.** `--format sarif`, valid against the SARIF 2.1.0
      schema. Done: output loads in GitHub code scanning.
- [x] **GitHub Actions CI.** Run `ruff` and `pytest` on push and PR.
- [ ] **Inline suppression.** A documented way to ignore one finding with a
      reason. Done: suppressed findings are counted but not reported.

## Supply chain (AA0xx)

- [ ] **AA002 plain-HTTP server URL.** Remote MCP server over `http://` to a
      non-loopback host.
- [ ] **AA003 server launched from a remote script.** `curl | sh`, `iwr | iex`
      and similar in a server command.
- [ ] **AA004 server launched from a git URL without a commit pin.**

## Secrets (AA3xx)

- [ ] **AA301 hardcoded secret in `env` or `args`.** Known token prefixes plus
      an entropy check; values that are `${VAR}` references are clean.

## Permissions (AA1xx)

- [ ] **Parser: Claude Code `settings.json`.** Normalize permission rules and
      hooks into the model.
- [ ] **AA101 wildcard shell permission.** Unrestricted `Bash` allow rules.
- [ ] **AA102 permission bypass mode enabled by default.**

## Skills and injection (AA2xx)

- [ ] **Parser: `SKILL.md`.** Front matter plus body into the model.
- [ ] **AA201 invisible characters** in skill text or tool descriptions
      (zero-width, bidi overrides, tag characters).
- [ ] **AA202 hidden instructions in HTML comments.**
- [ ] **AA203 skill instructs reading credential paths** (`~/.ssh`, `.env`,
      cloud credential files).

## Hooks (AA4xx)

- [ ] **AA401 tool input interpolated unquoted into a hook command.** Needs a
      shell parser (`tree-sitter-bash`).

## Toxic combinations (AA5xx)

- [ ] **Capability model.** Tag each server as reads-private-data,
      receives-untrusted-content, can-send-out.
- [ ] **AA501 one setup holds all three capabilities.**

## Evidence

- [ ] **Corpus run.** Scan a set of public repos with MCP configs, record
      hit rates and false positives per rule, write it up.
