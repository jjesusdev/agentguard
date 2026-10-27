from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel

class AgentEvent(BaseModel):
    session_id: str
    agent_type: str  # claude | opencode | codex | cursor
    ts: datetime
    seq: int
    type: str  # tool.call | tool.result | file.access
    tool_name: str | None = None
    path: str | None = None
    args_digest: str | None = None
    prev_hash: str
    hash: str

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}
