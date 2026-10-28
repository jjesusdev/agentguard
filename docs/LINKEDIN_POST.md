# Post LinkedIn - AgentGuard

🚀 Acabo de cerrar AgentGuard v1.0 — auditoría forense inmutable para agentes en YOLO mode.

Problema: los agentes de coding ejecutan sin aprobación y no hay trazabilidad verificable. Mi solución registra cada acción vía hooks, inotify/auditd, con journal JSONL hash-chained y detector de riesgo YAML.

Stack: Python 3.12, Typer, Pydantic, structlog, async/await, Ansible, DEB/RPM.

Lo que demuestra:
🔒 Seguridad Linux: auditd, inotify, permisos, usuarios dedicados
🪝 Observabilidad de agentes: adapters para Claude Code, OpenCode, Codex
🧪 Calidad 2026: uv, ruff, pyright, pytest, pre-commit, CI
📦 DevOps: empaquetado + rol Ansible

Repo público con arquitectura, metodología forense basada en Cloudflare Security Audit Skill y guía de entrevistas.

¿YOLO mode necesita auditoría? Ahora tiene evidencia verificable.

#DevOps #SRE #AISecurity #Python #OpenSource
