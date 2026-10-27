from __future__ import annotations
from .base import BaseAdapter
from ..events import AgentEvent
from datetime import datetime, timezone

class CodexAdapter(BaseAdapter):
    @property
    def agent_type(self) -> str:
        return "codex"

    def normalize(self, raw: dict) -> AgentEvent:
        return AgentEvent(
            session_id=raw.get("session_id", "unknown"),
            agent_type=self.agent_type,
            ts=datetime.now(timezone.utc),
            seq=raw.get("seq", 0),
            type="tool.call",
            tool_name=raw.get("tool_name"),
            args_digest=raw.get("args_digest"),
            prev_hash=raw.get("prev_hash", ""),
            hash=raw.get("hash", ""),
        )

    async def stream_events(self, session_id: str):
        return
        yield
