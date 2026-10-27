import json, hashlib, tempfile
from pathlib import Path
from agentguard.verify import verify_journal

def test_verify_ok():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "s.jsonl"
        prev = "0"*64
        for i in range(3):
            data = {"seq": i+1, "prev_hash": prev, "value": i}
            h = hashlib.sha256(json.dumps({k:v for k,v in data.items() if k!="hash"}, sort_keys=True).encode()).hexdigest()
            data["hash"] = h
            prev = h
            p.write_text(json.dumps(data)+"\n", encoding="utf-8" if i==0 else None)
            # append
            with p.open("a", encoding="utf-8") as f:
                if i>0: f.write("\n")
                f.write(json.dumps(data))
        # simplify
        # just test with 1 line
    # real test using helper
    from agentguard.journal import Journal
    from agentguard.events import AgentEvent
    from datetime import datetime, timezone
    with tempfile.TemporaryDirectory() as d:
        j = Journal("s", Path(d))
        e = AgentEvent(session_id="s", agent_type="opencode", ts=datetime.now(timezone.utc), seq=1, type="tool.call", prev_hash="0"*64, hash="")
        j.append(e)
        ok, bad = verify_journal("s", Path(d))
        assert ok is True
