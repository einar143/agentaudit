"""Find agent configuration files under a path."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

MCP_CONFIG_NAMES    = frozenset({".mcp.json", "mcp.json", "claude_desktop_config.json"})
SKIP_DIRS           = frozenset({".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"})


def discover_mcp_configs(path: Path) -> Iterator[Path]:
    """Yield MCP config files. A file path is yielded as-is, whatever its name."""
    if path.is_file():
        yield path
        return
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if name in MCP_CONFIG_NAMES:
                yield Path(root) / name
