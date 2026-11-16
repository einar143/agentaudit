"""Rule base class and registry."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import ClassVar

from agentaudit.model import Finding, ScanTarget, Severity

_REGISTRY: dict[str, type[Rule]] = {}


class Rule(ABC):
    id: ClassVar[str]
    title: ClassVar[str]
    severity: ClassVar[Severity]

    @abstractmethod
    def check(self, target: ScanTarget) -> Iterator[Finding]:
        """Yield a finding for each violation in the target."""

    def finding(self, *, message: str, file: Path, location: str, fix: str) -> Finding:
        return Finding(
            rule_id=self.id,
            title=self.title,
            severity=self.severity,
            message=message,
            file=file,
            location=location,
            fix=fix,
        )


def register(cls: type[Rule]) -> type[Rule]:
    if cls.id in _REGISTRY:
        raise ValueError(f"duplicate rule id {cls.id}")
    _REGISTRY[cls.id] = cls
    return cls


def all_rules() -> list[Rule]:
    return [_REGISTRY[rule_id]() for rule_id in sorted(_REGISTRY)]
