from pathlib import Path

import pytest

from agentaudit.engine import scan
from agentaudit.rules.supply_chain import is_pinned, package_name, package_spec, runner_args

FIXTURES = Path(__file__).parent / "fixtures" / "AA001"


def test_bad_fixture_fires_for_every_server():
    result = scan(FIXTURES / "bad")
    assert not result.errors
    assert {f.rule_id for f in result.findings} == {"AA001"}
    assert sorted(f.location for f in result.findings) == [
        "mcpServers.latest-tag",
        "mcpServers.no-version",
        "mcpServers.python-unpinned",
        "mcpServers.windows-wrapper",
    ]


def test_good_fixture_is_clean():
    result = scan(FIXTURES / "good")
    assert not result.errors
    assert result.findings == []


def test_fix_suggests_a_pin_without_the_old_tag():
    result = scan(FIXTURES / "bad")
    fixes = {f.location: f.fix for f in result.findings}
    assert "`@example/mcp-server@1.2.3`" in fixes["mcpServers.latest-tag"]
    assert "`example-mcp-server==1.2.3`" in fixes["mcpServers.python-unpinned"]


@pytest.mark.parametrize(
    ("spec", "ecosystem", "expected"),
    [
        ("pkg", "npm", False),
        ("pkg@latest", "npm", False),
        ("pkg@^1.2.3", "npm", False),
        ("pkg@1", "npm", False),
        ("pkg@1.2.3", "npm", True),
        ("pkg@1.2.3-beta.1", "npm", True),
        ("@scope/pkg", "npm", False),
        ("@scope/pkg@1.2.3", "npm", True),
        ("pkg", "python", False),
        ("pkg>=1.0", "python", False),
        ("pkg==1.0.0", "python", True),
        ("pkg@1.0.0", "python", True),
        ("pkg@latest", "python", False),
    ],
)
def test_is_pinned(spec, ecosystem, expected):
    assert is_pinned(spec, ecosystem) is expected


@pytest.mark.parametrize(
    ("spec", "expected"),
    [
        ("pkg", "pkg"),
        ("pkg@latest", "pkg"),
        ("@scope/pkg", "@scope/pkg"),
        ("@scope/pkg@latest", "@scope/pkg"),
        ("pkg==1.0", "pkg"),
    ],
)
def test_package_name(spec, expected):
    assert package_name(spec) == expected


@pytest.mark.parametrize(
    ("command", "args", "expected"),
    [
        ("npx", ["-y", "pkg"], ("npm", ["-y", "pkg"])),
        ("C:\\Program Files\\nodejs\\npx.cmd", ["pkg"], ("npm", ["pkg"])),
        ("cmd", ["/c", "npx", "pkg"], ("npm", ["pkg"])),
        ("pnpm", ["dlx", "pkg"], ("npm", ["pkg"])),
        ("uv", ["tool", "run", "pkg"], ("python", ["pkg"])),
        ("pipx", ["run", "pkg"], ("python", ["pkg"])),
        ("node", ["server.js"], None),
        ("uv", ["run", "server.py"], None),
    ],
)
def test_runner_args(command, args, expected):
    assert runner_args(command, args) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (["-y", "pkg"], "pkg"),
        (["--package", "pkg", "bin"], "pkg"),
        (["--package=pkg", "bin"], "pkg"),
        (["--from", "pkg", "bin"], "pkg"),
        (["-y"], None),
        ([], None),
    ],
)
def test_package_spec(args, expected):
    assert package_spec(args) == expected
