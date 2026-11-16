"""Parse MCP client configs that use the `mcpServers` shape.

Covers `.mcp.json`, `claude_desktop_config.json` and Cursor's `mcp.json`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentaudit.model import McpServer
from agentaudit.parsers import ParseError


def parse_mcp_config(path: Path) -> list[McpServer]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError) as exc:
        raise ParseError(f"cannot read file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ParseError(f"invalid JSON at line {exc.lineno}: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ParseError("top level is not a JSON object")

    servers = data.get("mcpServers", {})
    if not isinstance(servers, dict):
        raise ParseError("`mcpServers` is not an object")

    return [_server(name, entry, path) for name, entry in servers.items()]


def _server(name: str, entry: Any, path: Path) -> McpServer:
    if not isinstance(entry, dict):
        raise ParseError(f"server `{name}` is not an object")

    command = entry.get("command")
    args = entry.get("args", [])
    env = entry.get("env", {})
    url = entry.get("url")

    if command is not None and not isinstance(command, str):
        raise ParseError(f"server `{name}`: `command` is not a string")
    if not isinstance(args, list):
        raise ParseError(f"server `{name}`: `args` is not a list")
    if not isinstance(env, dict):
        raise ParseError(f"server `{name}`: `env` is not an object")
    if url is not None and not isinstance(url, str):
        raise ParseError(f"server `{name}`: `url` is not a string")

    return McpServer(
        name=name,
        source=path,
        command=command,
        args=[str(a) for a in args],
        env={str(k): str(v) for k, v in env.items()},
        url=url,
    )
