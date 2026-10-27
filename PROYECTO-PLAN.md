# AgentGuard — Auditoría forense para agentes en YOLO mode

Proyecto principal de portafolio DevOps/SRE
Fecha inicio: 27 octubre 2026

## Problema
Los agentes de coding en YOLO mode ejecutan acciones sin aprobación humana. No hay una capa estándar de auditoría forense que registre qué hizo, qué archivos tocó y qué comandos ejecutó, con trazabilidad inmutable. Es el gap entre sandbox y confianza.

## Oportunidad de mercado
- AWS lanzó open-source sandbox para YOLO mode el 7 oct 2026.
- Docker, VerityAI y medios especializados destacan riesgos de YOLO mode en 2026.
- Splunk State of Observability 2026: 88% de pilotos de agentes no llegan a producción por falta de observabilidad y costos impredecibles.
- Zona 3 del mapa de dolor 2026: verificación / forense es HIGH leverage y poco atendido en OSS.

## Qué construyes
Daemon Linux que audita sesiones de Claude Code/Cursor en YOLO mode:
- Captura cada acción vía PostToolUse hook + inotify/auditd
- Log inmutable JSON con timestamp, sesión, comando, archivos leídos/escritos
- Detección de riesgo: lectura de ~/.ssh, .env, secrets/, comandos rm -rf, curl | bash
- CLI replay y reporte forense
- Empaquetado RPM/DEB + rol Ansible

## Stack
- Python/Go para daemon
- auditd / inotify para monitoreo de sistema
- SQLite/Postgres para almacenamiento
- FastAPI para API mínima
- Rich para CLI TUI
- Ansible para despliegue

## Roadmap 4-6 semanas
Semana 1-2: Core forense
- Hook PostToolUse -> daemon
- Logger JSON inmutable por sesión

Semana 3: Detección de riesgo
- Reglas YAML allow/deny
- Alertas a stdout/Slack

Semana 4: Replay y paquete
- CLI replay --session id
- Empaquetado DEB/RPM + Ansible role
- README con demo ataque bloqueado

## Entregables para empleo
- Repo público con demo
- Screenshot de log forense y alerta
- README con arquitectura y decisiones de seguridad Linux
- Post LinkedIn explicando por qué YOLO mode necesita auditoría

## Relación con perfil
Complementa RHCSA + DevOps certs. Demuestra seguridad Linux, auditoría, logging, empaquetado y despliegue. Perfecto para prácticas SRE/DevOps en Chile.

## Próximo paso
Crear estructura de repo y primer parser de eventos de Claude Code.
