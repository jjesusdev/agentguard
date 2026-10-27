# Guía de Estudio y Presentación para Entrevistas — AgentGuard

## Historia para contar en 90 segundos

“Los agentes en YOLO mode ejecutan sin aprobación. Construí AgentGuard, un daemon Linux que audita forensemente sesiones de Claude Code. Captura cada acción vía PostToolUse hook + inotify/auditd, escribe un journal JSONL hash-chained inmutable y detecta lecturas de secretos o comandos destructivos. Lo empaqueté en DEB/RPM con rol Ansible. Es evidencia verificable de qué hizo el agente, no solo logs.”

## Conceptos clave a dominar

### Seguridad Linux
- auditd: `auditctl -w /etc/passwd -p wa -k passwd_watch`
- inotify: eventos `IN_CLOSE_WRITE`, `IN_MODIFY`
- Principio de menor privilegio, usuarios dedicados, permisos 700
- Socket Unix vs TCP local

### Forense inmutable
- Hash chain: cada evento contiene `prev_hash = sha256(prev_event)`
- Verificación: recomputar cadena, detectar primer `seq` roto
- Checkpoints Ed25519 opcionales

### Observabilidad de agentes
- Claude Code hooks: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`
- Matcher para filtrar herramientas
- Formato de entrada JSON con `tool_name`, `tool_input`

### DevOps / SRE
- Empaquetado DEB/RPM
- Rol Ansible: instalación, usuario, systemd service, audit.rules
- Logging estructurado JSONL
- FastAPI mínima para consulta

## Preguntas esperadas y respuestas

**¿Por qué YOLO mode es riesgoso?**
Permite ejecución sin aprobación. Sin auditoría, no hay trazabilidad post-incidente. Splunk 2026: 88% de pilotos de agentes no llegan a producción por falta de observabilidad.

**¿Cómo garantizas inmutabilidad?**
Hash chain por sesión + permisos de filesystem + usuario separado. `aileron verify` demuestra el concepto.

**¿Cómo evitas falsos positivos?**
Reglas YAML Sigma-like con matchers en nombre de herramienta y contenido, baseline comportamental, validación adversarial independiente.

**¿Qué harías en producción?**
Almacenar en Postgres con partición por sesión, export OTel GenAI, alertas Slack, retención configurada.

## Demostración práctica

1. Iniciar sesión de prueba
2. Mostrar `journal.jsonl` con hash chain
3. Ejecutar `agentguard verify`
4. Mostrar reporte HTML con timeline

## Extensiones para hablar

- Integración con eBPF via logira
- Export a SIEM
- Firma con Sigstore/Rekor
- Políticas OPA

## Recursos de estudio

- Cloudflare Security Audit Skill — 6 fases y write isolation
- Ponytail — mínima implementación efectiva
- Aileron — flight recorder hash-chained
- OWASP Agentic Top 10 2026
- Linux Audit System docs

## Checklist antes de entrevista

- Repo público con README clara
- Demo GIF/screenshot de log forense y alerta
- `ARCHITECTURE.md` con decisiones justificadas
- Historia de problema → solución → impacto
- Métricas: reducción de código, tests por lógica riesgosa
