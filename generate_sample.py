import json
from pathlib import Path
from datetime import datetime, timezone

raw_path = Path("var/lib/agentguard/sessions") / "opencode-demo.raw.jsonl"
raw_path.parent.mkdir(parents=True, exist_ok=True)

events = [
    {"session_id": "opencode-demo", "seq": 1, "ts": datetime.now(timezone.utc).isoformat(), "type": "tool.call", "tool_name": "Bash", "args_digest": "abc"},
    {"session_id": "opencode-demo", "seq": 2, "ts": datetime.now(timezone.utc).isoformat(), "type": "tool.call", "tool_name": "Write", "path": "/tmp/test.txt", "args_digest": "def"},
]

with raw_path.open("w", encoding="utf-8") as f:
    for e in events:
        f.write(json.dumps(e) + "\n")

print(f"Wrote {raw_path}")
