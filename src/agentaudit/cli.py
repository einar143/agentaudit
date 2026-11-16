"""Command-line entry point."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from agentaudit.engine import scan as run_scan
from agentaudit.reporters import json_report, terminal
from agentaudit.rules import all_rules

app = typer.Typer(
    help="Static security scanner for AI-agent configuration.",
    no_args_is_help=True,
    add_completion=False,
)


class OutputFormat(StrEnum):
    terminal = "terminal"
    json = "json"


@app.command()
def scan(
    path: Annotated[Path, typer.Argument(exists=True, help="File or directory to scan.")] = Path(
        "."
    ),
    output_format: Annotated[
        OutputFormat, typer.Option("--format", "-f", help="Report format.")
    ] = OutputFormat.terminal,
) -> None:
    """Scan PATH for insecure agent configuration."""
    result = run_scan(path)

    if output_format is OutputFormat.json:
        typer.echo(json_report.render(result))
    else:
        terminal.render(result, Console())

    if result.errors:
        raise typer.Exit(code=2)
    if result.findings:
        raise typer.Exit(code=1)


@app.command()
def rules() -> None:
    """List every rule."""
    for rule in all_rules():
        typer.echo(f"{rule.id}  {rule.severity.value:<8}  {rule.title}")
