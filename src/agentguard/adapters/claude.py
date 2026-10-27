from __future__ import annotations
import json
import asyncio
from pathlib import Path
from typing import AsyncIterator
from .base import BaseAdapter
from ..events import AgentEvent
from datetime import datetime, timezone

class ClaudeAdapter(BaseAdapter):
    @property
    def agent_type(self) -> str:
        return "claude"

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

    async def stream_events(self, session_id: str) -> AsyncIterator[AgentEvent]:
        # Claude Code hooks write to ~/.claude/agentguard/<session_id>.jsonl
        hook_path = Path.home() / ".claude" / "agentguard" / f"{session_id}.jsonl"
        if not hook_path.exists():
            return
        def read_lines():
            with hook_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    yield json.loads(line)
        for raw in await asyncio.to_thread(lambda: list(read_lines())):
            yield self.normalize(raw)
