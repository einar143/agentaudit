"""Normalized model. Parsers produce it, rules consume it."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def rank(self) -> int:
        return list(Severity).index(self)


class McpServer(BaseModel):
    """One MCP server entry, whichever client config it came from."""

    name: str
    source: Path
    command: str | None = None
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    url: str | None = None

    @property
    def location(self) -> str:
        return f"mcpServers.{self.name}"


class ScanTarget(BaseModel):
    """Everything discovered under the scanned path."""

    servers: list[McpServer] = Field(default_factory=list)


class Finding(BaseModel):
    rule_id: str
    title: str
    severity: Severity
    message: str
    file: Path
    location: str
    fix: str


class ScanError(BaseModel):
    """A file that was discovered but could not be parsed."""

    file: Path
    message: str


class ScanResult(BaseModel):
    findings: list[Finding] = Field(default_factory=list)
    errors: list[ScanError] = Field(default_factory=list)
    files_scanned: int = 0
