"""CLI entry point for AgentGuard."""
import asyncio
from rich.console import Console
from src.agentguard.adapters.claude import ClaudeAdapter
from src.agentguard.engine import Engine

console = Console()

async def main():
    adapter = ClaudeAdapter()
    engine = Engine(adapter, session_id="demo-session")
    console.print("[bold green]AgentGuard engine starting...[/]")
    # await engine.run()
    console.print("[bold yellow]Stub run complete. Implement adapter streams.[/]")

if __name__ == "__main__":
    asyncio.run(main())
