"""Human-readable terminal report."""

from __future__ import annotations

from rich.console import Console
from rich.markup import escape

from agentaudit.model import ScanResult, Severity

_STYLE = {
    Severity.LOW: "dim",
    Severity.MEDIUM: "yellow",
    Severity.HIGH: "red",
    Severity.CRITICAL: "bold red",
}


def render(result: ScanResult, console: Console) -> None:
    for error in result.errors:
        console.print(f"[bold red]error[/] {escape(str(error.file))}: {escape(error.message)}")

    for finding in result.findings:
        style = _STYLE[finding.severity]
        console.print(
            f"[{style}]{finding.severity.value:<8}[/] [bold]{finding.rule_id}[/] "
            f"{escape(str(finding.file))} ({escape(finding.location)})"
        )
        console.print(f"         {escape(finding.message)}")
        console.print(f"         [green]fix:[/] {escape(finding.fix)}")

    console.print(
        f"{result.files_scanned} file(s) scanned, {len(result.findings)} finding(s), "
        f"{len(result.errors)} error(s)."
    )
