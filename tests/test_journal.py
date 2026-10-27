import tempfile
from pathlib import Path
from datetime import datetime, timezone

from agentguard.journal import Journal
from agentguard.events import AgentEvent


def make_event(session_id, seq, prev_hash):
    return AgentEvent(
        session_id=session_id,
        agent_type="claude",
        ts=datetime.now(timezone.utc),
        seq=seq,
        type="tool.call",
        tool_name="test",
        prev_hash=prev_hash,
        hash="",
    )


def test_append_validates_prev_hash():
    with tempfile.TemporaryDirectory() as d:
        j = Journal("s1", Path(d))
        e1 = make_event("s1", 1, "0"*64)
        j.append(e1)
        # wrong prev_hash
        e2 = make_event("s1", 2, "0"*64)
        try:
            j.append(e2)
            assert False, "Expected ValueError for prev_hash mismatch"
        except ValueError as exc:
            assert "prev_hash" in str(exc).lower()


def test_append_validates_seq_monotonic():
    with tempfile.TemporaryDirectory() as d:
        j = Journal("s1", Path(d))
        e1 = make_event("s1", 1, "0"*64)
        j.append(e1)
        # correct prev_hash but seq not increasing
        # need correct prev_hash
        prev = e1.hash
        e2 = make_event("s1", 1, prev)
        try:
            j.append(e2)
            assert False, "Expected ValueError for seq monotonic"
        except ValueError as exc:
            assert "seq" in str(exc).lower()


def test_verify_detects_corruption():
    with tempfile.TemporaryDirectory() as d:
        j = Journal("s1", Path(d))
        e1 = make_event("s1", 1, "0"*64)
        j.append(e1)
        e2 = make_event("s1", 2, e1.hash)
        j.append(e2)
        assert j.verify() is True
        # corrupt second line
        path = Path(d) / "s1.jsonl"
        lines = path.read_text(encoding="utf-8").splitlines()
        import json
        data = json.loads(lines[1])
        data["type"] = "corrupted"
        lines[1] = json.dumps(data)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        assert j.verify() is False


def test_append_persists_chain_across_instances():
    with tempfile.TemporaryDirectory() as d:
        j1 = Journal("s1", Path(d))
        e1 = make_event("s1", 1, "0"*64)
        j1.append(e1)
        # new instance should load last hash/seq
        j2 = Journal("s1", Path(d))
        e2 = make_event("s1", 2, e1.hash)
        j2.append(e2)
        # verify whole journal
        assert j2.verify() is True
