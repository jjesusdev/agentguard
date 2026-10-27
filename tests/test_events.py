def test_events_model():
    from agentguard.events import AgentEvent
    from datetime import datetime, timezone
    e = AgentEvent(
        session_id="s1",
        agent_type="claude",
        ts=datetime.now(timezone.utc),
        seq=1,
        type="tool.call",
        prev_hash="0"*64,
        hash="a"*64,
    )
    assert e.session_id == "s1"
