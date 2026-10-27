import pytest
from agentguard.adapters.claude import ClaudeAdapter
from agentguard.adapters.base import BaseAdapter
from datetime import datetime, timezone


def test_adapter_normalizes_valid_event():
    adapter = ClaudeAdapter()
    raw = {
        "session_id": "sess-123",
        "seq": 1,
        "type": "tool.call",
        "ts": "2026-10-27T12:00:00+00:00",
        "tool_name": "Bash",
        "path": "/tmp",
        "args_digest": "abc",
        "prev_hash": "0"*64,
        "hash": "1"*64,
    }
    event = adapter.normalize(raw)
    assert event.session_id == "sess-123"
    assert event.seq == 1
    assert event.type == "tool.call"
    assert event.agent_type == "claude"
    # event should be AgentEvent instance
    from agentguard.events import AgentEvent
    assert isinstance(event, AgentEvent)


def test_adapter_rejects_invalid_event():
    adapter = ClaudeAdapter()
    raw_missing_session = {
        "seq": 1,
        "type": "tool.call",
    }
    with pytest.raises(ValueError) as exc:
        adapter.normalize(raw_missing_session)
    assert "session_id" in str(exc.value)

    raw_missing_seq = {
        "session_id": "s",
        "type": "tool.call",
    }
    with pytest.raises(ValueError) as exc:
        adapter.normalize(raw_missing_seq)
    assert "seq" in str(exc.value)

    raw_missing_type = {
        "session_id": "s",
        "seq": 1,
    }
    with pytest.raises(ValueError) as exc:
        adapter.normalize(raw_missing_type)
    assert "type" in str(exc.value)
