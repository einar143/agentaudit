"""Machine-readable JSON report."""

from __future__ import annotations

from agentaudit.model import ScanResult


def render(result: ScanResult) -> str:
    return result.model_dump_json(indent=2)
