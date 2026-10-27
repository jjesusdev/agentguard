from __future__ import annotations
import asyncio
from pathlib import Path
from typing import AsyncIterator
from .adapters.base import AgentAdapter
from .events import AgentEvent
from .journal import Journal
from .config import settings
from .detector import Detector

class Engine:
    def __init__(self, adapter: AgentAdapter, session_id: str, journal_dir: Path | None = None, rules_dir: Path | None = None):
        self.adapter = adapter
        self.session_id = session_id
        self.journal = Journal(session_id, journal_dir or Path(settings.journal_dir))
        self.detector = Detector(rules_dir or Path(settings.rules_dir) / "rules.yaml")
        self.queue: asyncio.Queue[AgentEvent] = asyncio.Queue(maxsize=1000)

    async def run(self) -> None:
        producer = asyncio.create_task(self._produce())
        consumer = asyncio.create_task(self._consume())
        await asyncio.gather(producer, consumer)

    async def _produce(self) -> None:
        async for event in self.adapter.stream_events(self.session_id):
            await self.queue.put(event)
        await self.queue.put(None)

    async def _consume(self) -> None:
        while True:
            event = await self.queue.get()
            if event is None:
                break
            self.journal.append(event)
            hits = self.detector.check(event)
            for hit in hits:
                # In real impl, emit alert / block via hook
                pass
            self.queue.task_done()
