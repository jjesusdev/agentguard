# AgentGuard — Auditoría forense para agentes en YOLO mode

[![CI](https://github.com/usuario/agentguard/actions/workflows/ci.yml/badge.svg)](https://github.com/usuario/agentguard/actions/workflows/ci.yml)

**Daemon Linux de auditoría forense inmutable para sesiones de Claude Code / Cursor / OpenCode / Codex en YOLO mode.**

> Proyecto de portafolio DevOps/SRE. Fecha inicio: 27 octubre 2026.

![Demo](docs/demo.gif)

## Problema

Los agentes de coding en YOLO mode ejecutan acciones sin aprobación humana. No existe una capa estándar de auditoría forense que registre qué hizo, qué archivos tocó y qué comandos ejecutó, con trazabilidad inmutable. Es el gap entre sandbox y confianza.

## Solución

Daemon que audita sesiones de Claude Code/Cursor:
- Captura cada acción vía PostToolUse hook + inotify/auditd
- Log inmutable JSON hash-chained por sesión
- Detección de riesgo: lectura de `~/.ssh`, `.env`, `secrets/`, comandos `rm -rf`, `curl | bash`
- CLI replay y reporte forense HTML
- Empaquetado RPM/DEB + rol Ansible

## Stack

Python/Go, auditd/inotify, SQLite/Postgres, FastAPI, Rich CLI, Ansible

## Arquitectura resumida

```
Claude Code --PostToolUse--> Hook -> AgentGuard Daemon
                                   -> inotify/auditd watcher
                                   -> Logger JSONL hash-chained
                                   -> Detector YAML allow/deny
                                   -> API FastAPI + CLI Rich
```

## Roadmap

Semana 1-2: Core forense, Hook + Logger inmutable
Semana 3: Detección de riesgo con reglas YAML
Semana 4: Replay CLI, empaquetado DEB/RPM + Ansible role + demo

## Entregables

- Repo público con demo
- Screenshot log forense y alerta
- README arquitectura y decisiones de seguridad Linux
- Post LinkedIn sobre por qué YOLO mode necesita auditoría

## Documentación

- `PROYECTO-PLAN.md` — plan original
- `docs/ARCHITECTURE.md` — decisiones de diseño
- `docs/AUDIT-METHODOLOGY.md` — metodología forense basada en Cloudflare Security Audit Skill
- `docs/INTERVIEW-GUIDE.md` — guía de estudio y presentación para entrevistas

## Instalación 2026

```bash
uv venv
uv pip install -e .[dev]
uv run pre-commit install
uv run pytest
```

## Uso rápido

Generar datos de prueba:
```bash
python generate_sample.py
```

Ejecutar engine con adapter OpenCode:
```bash
PYTHONPATH=src uv run python -m agentguard
```

Verificar inmutabilidad:
```bash
python verify_cli.py opencode-demo
```

Generar reporte HTML:
```bash
python generate_report.py
```

## Demo rápido

```bash
agentguard start --session claude-01
agentguard replay --session claude-01
agentguard report --session claude-01 --output incident.html
```

## Licencia

MIT
