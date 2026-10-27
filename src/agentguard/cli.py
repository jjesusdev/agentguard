from __future__ import annotations
import typer
from pathlib import Path
from agentguard.adapters.opencode import OpenCodeAdapter
from agentguard.adapters.claude import ClaudeAdapter
from agentguard.adapters.codex import CodexAdapter
from agentguard.engine import Engine
from agentguard.verify import verify_journal
from agentguard.generate_report import generate_report

app = typer.Typer(help="AgentGuard forense multi-agente")

def get_adapter(name: str):
    adapters = {
        "opencode": OpenCodeAdapter(),
        "claude": ClaudeAdapter(),
        "codex": CodexAdapter(),
    }
    if name not in adapters:
        raise typer.BadParameter(f"Agente no soportado: {name}")
    return adapters[name]

@app.command()
def run(session_id: str, agent: str = "opencode"):
    import asyncio
    adapter = get_adapter(agent)
    engine = Engine(adapter, session_id)
    asyncio.run(engine.run())
    typer.echo(f"Session {session_id} procesada con {agent}")

@app.command()
def verify(session_id: str):
    from agentguard.config import settings
    ok, bad = verify_journal(session_id, Path(settings.journal_dir))
    if ok:
        typer.echo(f"OK: journal {session_id} verified")
    else:
        typer.echo(f"TAMPERED at seq {bad}")

@app.command()
def report(session_id: str, output: Path = Path("report.html")):
    from agentguard.config import settings
    generate_report(session_id, Path(settings.journal_dir), output)
    typer.echo(f"Report generado en {output}")

if __name__ == "__main__":
    app()
