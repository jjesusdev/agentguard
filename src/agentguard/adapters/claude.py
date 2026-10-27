from __future__ import annotations
from typing import AsyncIterator
from .base import BaseAdapter
from ..events import AgentEvent
from datetime import datetime, timezone

class ClaudeAdapter(BaseAdapter):
    @property
    def agent_type(self) -> str:
        return "claude"

    def normalize(self, raw: dict) -> AgentEvent:
        # Placeholder: real impl parses PostToolUse JSON
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

    async def stream_events(self, session_id: str) -> AsyncIterator[AgentEvent]:
        # TODO: connect to hook socket / log file
        return
        yield  # pragma: no cover
