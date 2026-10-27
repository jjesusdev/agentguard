# Instalación de Hooks por Agente

## Claude Code

1. Crear directorio de hooks:
```bash
mkdir -p ~/.claude/agentguard
```

2. Añadir a `.claude/settings.json` en el proyecto:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo \"$CLAUDE_INPUT\" >> ~/.claude/agentguard/$(basename $CLAUDE_PROJECT_DIR).jsonl'"
          }
        ]
      }
    ]
  }
}
```

El hook escribe cada evento PostToolUse como JSONL. AgentGuard lo lee con `ClaudeAdapter`.

## OpenCode

OpenCode emite eventos vía plugin. Configurar salida a:
`~/.opencode/agentguard/<session_id>.jsonl`

En `~/.opencode/config.json`:
```json
{
  "agentguard": {
    "output": "~/.opencode/agentguard"
  }
}
```

## Codex

Similar a Claude. Crear directorio:
```bash
mkdir -p ~/.codex/agentguard
```

Hook `post_tool_use` en `~/.codex/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": {
      "output": "~/.codex/agentguard/{{session_id}}.jsonl"
    }
  }
}
```

## Verificación

Después de una sesión:
```bash
uv run agentguard run --session <id> --agent claude
uv run agentguard verify <id>
uv run agentguard report <id> --output report.html
```

El journal queda en `var/lib/agentguard/sessions/<id>.jsonl` con cadena hash verificable.
