from __future__ import annotations
from abc import ABC, abstractmethod
from typing import AsyncIterator
from ..events import AgentEvent

class AgentAdapter(ABC):
    @property
    @abstractmethod
    def agent_type(self) -> str: ...

    @abstractmethod
    async def stream_events(self, session_id: str) -> AsyncIterator[AgentEvent]:
        """Yield normalized AgentEvent for the session."""
        ...

class BaseAdapter(AgentAdapter):
    @abstractmethod
    def normalize(self, raw: dict) -> AgentEvent: ...
