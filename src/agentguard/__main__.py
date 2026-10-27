import asyncio
from agentguard.adapters.opencode import OpenCodeAdapter
from agentguard.engine import Engine

async def main():
    engine = Engine(OpenCodeAdapter(), session_id="opencode-demo")
    await engine.run()

if __name__ == "__main__":
    asyncio.run(main())
