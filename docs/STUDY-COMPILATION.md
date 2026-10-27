# Compilación de estudio — AgentGuard y auditoría de agentes

## Resumen ejecutivo

AgentGuard es un proyecto de portafolio que demuestra competencias DevOps/SRE, seguridad Linux y observabilidad de IA. Combina metodologías validadas por la industria: Cloudflare Security Audit Skill y Ponytail.

## Temas técnicos

### 1. Auditoría forense inmutable
- Hash chain SHA-256
- Checkpoints Ed25519
- Verificación offline
- Formatos: JSONL, Evidence Bundles VOLT

### 2. Hooks de Claude Code
- `PostToolUse`: se dispara después de ejecución
- Matcher: `Bash|Edit|Write`
- Entrada JSON con `tool_name`, `tool_input`
- Salida opcional con `systemMessage` y `hookSpecificOutput`

### 3. Monitoreo Linux
- auditd: reglas persistentes en `/etc/audit/rules.d/`
- inotify: monitoreo en tiempo real sin syscall
- `ausearch` para consultas

### 4. Ingeniería de seguridad
- Trust boundaries
- Validación adversarial
- Severity = likelihood x impacto demostrado
- `needs_validation` sin severidad

### 5. DevOps
- Empaquetado DEB/RPM
- Rol Ansible
- systemd service
- FastAPI + Rich CLI

## Mapa de habilidades para CV

- Seguridad Linux: auditd, inotify, permisos, usuarios
- Observabilidad: logging estructurado, hash chain, replay forense
- DevOps: Ansible, empaquetado, despliegue
- Ingeniería de IA: hooks de agentes, políticas YAML, detección de anomalías
- Calidad: TDD, verificación independiente, write isolation

## Preguntas de auto-evaluación

1. ¿Cómo probarías que el journal no fue alterado?
2. ¿Qué diferencia auditd de inotify?
3. ¿Cuándo usar `needs_validation`?
4. ¿Cómo minimizas código con Ponytail sin sacrificar seguridad?
5. ¿Cómo escalarías a múltiples sesiones concurrentes?

## Próximos pasos de aprendizaje

- Implementar parser de eventos Claude Code en Python
- Crear reglas YAML de detección
- Generar reporte HTML con timeline
- Publicar demo en repo
- Escribir post LinkedIn explicando el gap YOLO mode
