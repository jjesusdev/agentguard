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
def run(
    session: str = typer.Option(..., "--session", help="ID de sesión"),
    agent: str = typer.Option("opencode", "--agent", help="Agente a auditar")
):
    import asyncio
    # Validate agent choice
    if agent not in {"opencode", "claude", "codex"}:
        raise typer.BadParameter(f"Agente no soportado: {agent}")
    adapter = get_adapter(agent)
    engine = Engine(adapter, session)
    asyncio.run(engine.run())
    typer.echo(f"Session {session} procesada con {agent}")

@app.command()
def verify(session_id: str):
    from agentguard.config import settings
    ok, bad = verify_journal(session_id, Path(settings.journal_dir))
    if ok:
        typer.echo(f"OK: journal {session_id} verified")
    else:
        typer.echo(f"TAMPERED at seq {bad}")

@app.command()
def report(
    session_id: str = typer.Argument(..., help="ID de sesión"),
    output: Path = typer.Option(..., "--output", help="Ruta de salida HTML")
):
    from agentguard.config import settings
    generate_report(session_id, Path(settings.journal_dir), output)
    typer.echo(f"Report generado en {output}")

@app.command(name="list")
def list_sessions():
    from agentguard.config import settings
    journal_dir = Path(settings.journal_dir)
    if not journal_dir.exists():
        typer.echo("No sessions found")
        return
    sessions = sorted([p.stem for p in journal_dir.glob("*.jsonl")])
    if not sessions:
        typer.echo("No sessions found")
        return
    for s in sessions:
        typer.echo(s)

@app.command()
def install_hooks(agent: str = typer.Argument(..., help="claude|opencode|codex")):
    from pathlib import Path
    agents = {
        "claude": Path.home() / ".claude" / "agentguard",
        "opencode": Path.home() / ".opencode" / "agentguard",
        "codex": Path.home() / ".codex" / "agentguard",
    }
    if agent not in agents:
        raise typer.BadParameter(f"Agente no soportado: {agent}")
    p = agents[agent]
    p.mkdir(parents=True, exist_ok=True)
    typer.echo(f"Created {p}")
    typer.echo(f"Hook output path: {p}/{{session_id}}.jsonl")
    typer.echo("Configure your agent to write PostToolUse events as JSONL to this path.")
    typer.echo("See docs/INSTALL-HOOKS.md for detailed config.")

if __name__ == "__main__":
    app()
