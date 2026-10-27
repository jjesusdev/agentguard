# Arquitectura AgentGuard

## Principios de diseño

1. **Inmutabilidad por defecto**: cada evento se appendea a un journal JSONL con hash SHA-256 encadenado. Editar, borrar o reordenar rompe la cadena.
2. **Observación sin bloqueo**: el daemon es observe-only. Las reglas pueden alertar o bloquear vía hook, pero el registro siempre ocurre.
3. **Separación de escritura**: solo el proceso padre escribe archivos compartidos. Los workers de detección solo escriben en `scratch/`.
4. **Mínimo código efectivo**: enfoque Ponytail — implementar el cambio más pequeño que cumple el requisito, con test para lógica de riesgo.
5. **Verificación independiente**: cada hallazgo de riesgo se revalida por un agente/verificador distinto del que lo encontró.

## Componentes

### 1. Hook Adapter
- Punto de entrada `PostToolUse` de Claude Code.
- Recibe JSON con `tool_name`, `tool_input`, `tool_output`.
- Envía evento al daemon vía socket Unix o HTTP local.

### 2. Kernel Watcher
- **inotify** para cambios de filesystem en tiempo real.
- **auditd** para syscalls críticos: `open`, `execve`, `connect`.
- Filtra rutas sensibles: `~/.ssh`, `.env`, `secrets/`.

### 3. Logger Inmutable
- Formato JSONL por sesión: `session_id`, `seq`, `ts`, `prev_hash`, `hash`, `event`.
- `prev_hash = sha256(prev_event)`; genesis = `0x00…00`.
- Checkpoints Ed25519 opcionales para no-repudio.

### 4. Detector de Riesgo
- Reglas YAML tipo Sigma: `match` sobre `tool.name`, `tool.arguments_contains`, rutas.
- Acciones: `allow`, `alert`, `block`.
- Baseline comportamental: primeras herramientas, picos de tasa >3x.

### 5. API + CLI
- FastAPI mínima para consulta de sesiones.
- CLI Rich con comandos: `start`, `replay`, `report`, `verify`.

### 6. Empaquetado y despliegue
- Paquete DEB/RPM con dependencias auditd/inotify-tools.
- Rol Ansible para instalar daemon, crear usuario `agentguard`, configurar audit.rules.

## Modelo de datos

Event:
```json
{
  "v": "agentguard/0.1",
  "session_id": "claude-01",
  "seq": 42,
  "ts": "2026-10-27T12:00:00Z",
  "type": "tool.call",
  "tool": "Bash",
  "args_digest": "sha256:...",
  "prev_hash": "...",
  "hash": "..."
}
```

## Decisiones de seguridad Linux

- Daemon corre como usuario no-root, auditd reglas cargadas por root vía Ansible.
- Journal ubicado en `/var/lib/agentguard/` con permisos 700 y propietario `agentguard:agentguard`.
- Socket Unix con permisos 660.
- Rotación con preservación de cadena.

## Referencias

- Cloudflare Security Audit Skill — metodología de 6 fases y write isolation.
- Ponytail — mínima implementación efectiva.
- Aileron — flight recorder hash-chained para agentes.
