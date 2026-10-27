import tempfile
from pathlib import Path
from typer.testing import CliRunner
from agentguard.cli import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.stdout
    assert "run" in output
    assert "verify" in output
    assert "report" in output
    assert "list" in output

def test_cli_verify_output():
    # Create a temporary journal dir with a valid journal
    import json
    from agentguard.journal import Journal
    from agentguard.events import AgentEvent
    from datetime import datetime, timezone

    with tempfile.TemporaryDirectory() as tmp:
        journal_dir = Path(tmp)
        # Monkey-patch settings
        from agentguard import config
        original_dir = config.settings.journal_dir
        config.settings.journal_dir = str(journal_dir)
        try:
            # Create a valid journal
            j = Journal("test-session", journal_dir)
            event = AgentEvent(
                session_id="test-session",
                agent_type="opencode",
                ts=datetime.now(timezone.utc),
                seq=1,
                type="tool.call",
                tool_name="test",
                prev_hash="0"*64,
                hash=""
            )
            j.append(event)
            # Run verify command
            result = runner.invoke(app, ["verify", "test-session"])
            assert result.exit_code == 0
            assert "OK: journal test-session verified" in result.stdout
        finally:
            config.settings.journal_dir = original_dir
