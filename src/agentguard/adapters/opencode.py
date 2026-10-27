from __future__ import annotations
import json
import asyncio
from pathlib import Path
from .base import BaseAdapter
from ..events import AgentEvent
from datetime import datetime, timezone
from ..config import settings

class OpenCodeAdapter(BaseAdapter):
    @property
    def agent_type(self) -> str:
        return "opencode"

    def normalize(self, raw: dict) -> AgentEvent:
        return AgentEvent(
            session_id=raw.get("session_id", "unknown"),
            agent_type=self.agent_type,
            ts=datetime.fromisoformat(raw.get("ts")) if raw.get("ts") else datetime.now(timezone.utc),
            seq=int(raw.get("seq", 0)),
            type=raw.get("type", "tool.call"),
            tool_name=raw.get("tool_name"),
            path=raw.get("path"),
            args_digest=raw.get("args_digest"),
            prev_hash=raw.get("prev_hash", ""),
            hash=raw.get("hash", ""),
        )

    async def stream_events(self, session_id: str):
        raw_path = Path(settings.journal_dir) / f"{session_id}.raw.jsonl"
        if not raw_path.exists():
            return
        # Read file in thread to avoid blocking event loop
        def read_lines():
            with raw_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    yield json.loads(line)
        for raw in await asyncio.to_thread(lambda: list(read_lines())):
            yield self.normalize(raw)
