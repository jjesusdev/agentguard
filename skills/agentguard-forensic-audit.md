---
name: agentguard-forensic-audit
description: Auditoría forense inmutable para agentes de coding en YOLO mode. Captura eventos vía hooks Claude Code, inotify/auditd, log hash-chained y detecta acceso a secretos o comandos destructivos. Usar para diseñar, implementar o auditar sesiones de agentes.
---

# AgentGuard Forensic Audit

## Objetivo
Proporcionar trazabilidad inmutable de acciones de agentes autónomos, con detección de riesgo y replay forense verificable.

## Principios
- Inmutabilidad por defecto: journal JSONL hash-chained por sesión
- Observe-only: no bloquea a menos que la regla lo exija vía hook
- Validación adversarial: hallazgos confirmados por verificador independiente
- Mínimo código efectivo: Ponytail ladder
- Write isolation: parent único escritor, workers en scratch/

## Flujo base
1. Hook PostToolUse -> evento al daemon
2. Watcher inotify/auditd -> eventos de filesystem/syscall
3. Logger -> append con prev_hash
4. Detector YAML -> alert/block
5. API/CLI -> replay y reporte

## Reglas de riesgo ejemplo
- Lectura de `~/.ssh/*`, `.env`, `secrets/`
- Comandos: `rm -rf`, `curl | bash`, `wget | sh`
- Escritura fuera de workspace

## Salidas
- `sessions/<id>/events.jsonl`
- `sessions/<id>/findings.json`
- `reports/<id>/incident.html`

## Verificación
`agentguard verify --session <id>` recompute hash chain y reporta primer seq roto.
