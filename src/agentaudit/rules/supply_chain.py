"""AA0xx: supply-chain rules."""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import PurePath
from typing import Literal

from agentaudit.model import Finding, ScanTarget, Severity
from agentaudit.rules.base import Rule, register

Ecosystem = Literal["npm", "python"]

_EXACT_NPM = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$")
_EXACT_PYTHON = re.compile(r"^\d+(\.\d+)+([0-9A-Za-z.+-]*)$")
_PACKAGE_FLAGS = frozenset({"-p", "--package", "--from"})


def _program(command: str) -> str:
    name = PurePath(command.replace("\\", "/")).name.lower()
    for suffix in (".exe", ".cmd", ".bat"):
        name = name.removesuffix(suffix)
    return name


def runner_args(command: str, args: list[str]) -> tuple[Ecosystem, list[str]] | None:
    """Identify a package runner and return its ecosystem and remaining args."""
    argv = [_program(command), *args]
    if argv[0] == "cmd" and len(argv) > 2 and argv[1].lower() == "/c":
        argv = [_program(argv[2]), *argv[3:]]

    match argv:
        case ["npx" | "bunx", *rest]:
            return "npm", rest
        case ["pnpm" | "yarn", "dlx", *rest]:
            return "npm", rest
        case ["uvx", *rest]:
            return "python", rest
        case ["pipx", "run", *rest]:
            return "python", rest
        case ["uv", "tool", "run", *rest]:
            return "python", rest
    return None


def package_spec(args: list[str]) -> str | None:
    """Return the package argument a runner would install, if one is present."""
    for index, arg in enumerate(args):
        if arg in _PACKAGE_FLAGS:
            return args[index + 1] if index + 1 < len(args) else None
        for flag in ("--package=", "--from="):
            if arg.startswith(flag):
                return arg.removeprefix(flag)
        if not arg.startswith("-"):
            return arg
    return None


def is_registry_package(spec: str) -> bool:
    """False for local paths and URLs, which other rules cover."""
    return not (spec.startswith((".", "/", "~")) or "://" in spec or "\\" in spec)


def package_name(spec: str) -> str:
    """Strip any version from a package spec."""
    name = spec.split("==", 1)[0]
    at = name.rfind("@")
    return name[:at] if at > 0 else name


def is_pinned(spec: str, ecosystem: Ecosystem) -> bool:
    if ecosystem == "python" and "==" in spec:
        return bool(_EXACT_PYTHON.match(spec.split("==", 1)[1]))
    at = spec.rfind("@")
    if at <= 0:  # no version, or only the leading @ of an npm scope
        return False
    version = spec[at + 1 :]
    pattern = _EXACT_NPM if ecosystem == "npm" else _EXACT_PYTHON
    return bool(pattern.match(version))


@register
class UnpinnedPackage(Rule):
    id = "AA001"
    title = "MCP server launched from an unpinned package"
    severity = Severity.HIGH

    def check(self, target: ScanTarget) -> Iterator[Finding]:
        for server in target.servers:
            if server.command is None:
                continue
            runner = runner_args(server.command, server.args)
            if runner is None:
                continue
            ecosystem, rest = runner
            spec = package_spec(rest)
            if spec is None or not is_registry_package(spec) or is_pinned(spec, ecosystem):
                continue
            name = package_name(spec)
            pin = f"{name}@1.2.3" if ecosystem == "npm" else f"{name}==1.2.3"
            yield self.finding(
                message=(
                    f"Server `{server.name}` runs `{spec}` without an exact version, so each "
                    "start can execute newly published code."
                ),
                file=server.source,
                location=server.location,
                fix=f"Pin an exact version, for example `{pin}`.",
            )
