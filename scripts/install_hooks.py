#!/usr/bin/env python3
from __future__ import annotations
import typer
from pathlib import Path

app = typer.Typer(help="AgentGuard hook installer")

AGENTS = {
    "claude": Path.home() / ".claude" / "agentguard",
    "opencode": Path.home() / ".opencode" / "agentguard",
    "codex": Path.home() / ".codex" / "agentguard",
}

@app.command()
def install(agent: str = typer.Argument(..., help="claude|opencode|codex")):
    if agent not in AGENTS:
        raise typer.BadParameter(f"Agente no soportado: {agent}")
    p = AGENTS[agent]
    p.mkdir(parents=True, exist_ok=True)
    typer.echo(f"Created {p}")
    typer.echo(f"Hook output path: {p}/{{session_id}}.jsonl")
    typer.echo("Configure your agent to write PostToolUse events as JSONL to this path.")
    typer.echo("See docs/INSTALL-HOOKS.md for detailed config.")

if __name__ == "__main__":
    app()
