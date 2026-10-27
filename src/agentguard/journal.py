from __future__ import annotations
import hashlib
import json
from pathlib import Path
from .events import AgentEvent

class Journal:
    def __init__(self, session_id: str, journal_dir: Path):
        self.session_id = session_id
        self.path = journal_dir / f"{session_id}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.prev_hash = "0" * 64

    def append(self, event: AgentEvent) -> None:
        event_data = event.model_dump(mode="json")
        h = hashlib.sha256(json.dumps(event_data, sort_keys=True).encode()).hexdigest()
        event.hash = h
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event_data) + "\n")
        self.prev_hash = h
