from __future__ import annotations
import hashlib
import json
from pathlib import Path

def verify_journal(session_id: str, journal_dir: Path) -> tuple[bool, int | None]:
    path = journal_dir / f"{session_id}.jsonl"
    if not path.exists():
        return False, None
    prev_hash = "0" * 64
    first_bad = None
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            data = json.loads(line)
            # recompute hash without the hash field
            h_data = {k: v for k, v in data.items() if k != "hash"}
            h = hashlib.sha256(json.dumps(h_data, sort_keys=True).encode()).hexdigest()
            if data.get("prev_hash") != prev_hash or data.get("hash") != h:
                first_bad = i
                break
            prev_hash = data.get("hash", "")
    return first_bad is None, first_bad
