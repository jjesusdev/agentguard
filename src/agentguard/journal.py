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
        self.last_seq = 0
        # load last event if exists to continue chain
        if self.path.exists() and self.path.stat().st_size > 0:
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    last_line = None
                    for line in f:
                        line = line.strip()
                        if line:
                            last_line = line
                    if last_line:
                        last_data = json.loads(last_line)
                        self.prev_hash = last_data.get("hash", self.prev_hash)
                        self.last_seq = int(last_data.get("seq", 0))
            except Exception:
                # if file is corrupted, keep defaults; verify will catch later
                pass

    def append(self, event: AgentEvent) -> None:
        if event.session_id != self.session_id:
            raise ValueError("event session_id does not match journal session_id")
        if event.prev_hash != self.prev_hash:
            raise ValueError(f"prev_hash mismatch: expected {self.prev_hash}, got {event.prev_hash}")
        if event.seq <= self.last_seq:
            raise ValueError(f"seq not monotonic: last_seq {self.last_seq}, got {event.seq}")
        # compute hash over event data without hash field
        event_dict = event.model_dump(mode="json")
        # compute hash excluding hash field
        hash_input = {k: v for k, v in event_dict.items() if k != "hash"}
        h = hashlib.sha256(json.dumps(hash_input, sort_keys=True).encode()).hexdigest()
        event.hash = h
        # dump final event with hash set
        final_dict = event.model_dump(mode="json")
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(final_dict) + "\n")
        self.prev_hash = h
        self.last_seq = event.seq

    def verify(self) -> bool:
        if not self.path.exists():
            return True
        prev_hash = "0" * 64
        try:
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    h_data = {k: v for k, v in data.items() if k != "hash"}
                    h = hashlib.sha256(json.dumps(h_data, sort_keys=True).encode()).hexdigest()
                    if data.get("prev_hash") != prev_hash or data.get("hash") != h:
                        return False
                    prev_hash = data.get("hash", "")
            return True
        except Exception:
            return False
