"""Scan pipeline: discover -> parse -> run rules."""

from __future__ import annotations

from pathlib import Path

from agentaudit.discovery import discover_mcp_configs
from agentaudit.model import ScanError, ScanResult, ScanTarget
from agentaudit.parsers import ParseError
from agentaudit.parsers.mcp_config import parse_mcp_config
from agentaudit.rules import all_rules


def scan(path: Path) -> ScanResult:
    target = ScanTarget()
    result = ScanResult()

    for config in discover_mcp_configs(path):
        result.files_scanned += 1
        try:
            target.servers.extend(parse_mcp_config(config))
        except ParseError as exc:
            result.errors.append(ScanError(file=config, message=str(exc)))

    for rule in all_rules():
        result.findings.extend(rule.check(target))

    result.findings.sort(key=lambda f: (-f.severity.rank, str(f.file), f.location, f.rule_id))
    return result
