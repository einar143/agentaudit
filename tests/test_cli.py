import json
from pathlib import Path

from typer.testing import CliRunner

from agentaudit.cli import app

FIXTURES = Path(__file__).parent / "fixtures" / "AA001"
runner = CliRunner()


def test_scan_exits_1_on_findings():
    result = runner.invoke(app, ["scan", str(FIXTURES / "bad")])
    assert result.exit_code == 1
    assert "AA001" in result.output


def test_scan_exits_0_when_clean():
    result = runner.invoke(app, ["scan", str(FIXTURES / "good")])
    assert result.exit_code == 0


def test_scan_json_output_is_valid():
    result = runner.invoke(app, ["scan", str(FIXTURES / "bad"), "--format", "json"])
    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["files_scanned"] == 1
    assert len(payload["findings"]) == 4
    assert payload["findings"][0]["severity"] == "high"


def test_scan_exits_2_on_unparseable_file(tmp_path):
    (tmp_path / ".mcp.json").write_text("{not json", encoding="utf-8")
    result = runner.invoke(app, ["scan", str(tmp_path)])
    assert result.exit_code == 2
    assert "invalid JSON" in result.output


def test_rules_lists_al001():
    result = runner.invoke(app, ["rules"])
    assert result.exit_code == 0
    assert "AA001" in result.output
