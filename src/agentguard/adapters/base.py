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

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Wrap subclass normalize to validate required fields
        orig_normalize = cls.__dict__.get("normalize")

        if orig_normalize is None:
            # No override in subclass, nothing to wrap
            return

        def _wrapped_normalize(self, raw: dict) -> AgentEvent:
            # Validate required fields
            required = ("session_id", "seq", "type")
            missing = [field for field in required if field not in raw or raw.get(field) is None]
            if missing:
                raise ValueError(f"Missing required field(s): {', '.join(missing)}")
            return orig_normalize(self, raw)

        # Preserve name and docstring
        _wrapped_normalize.__name__ = orig_normalize.__name__
        _wrapped_normalize.__doc__ = orig_normalize.__doc__
        cls.normalize = _wrapped_normalize
