# AgentGuard v1.0 Final Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar versión 1.0 de AgentGuard como auditoría forense multi-agente con instalación, empaquetado y demo pública lista para portafolio.

**Architecture:** Core async engine con adapters por agente, journal hash-chained, detector YAML, CLI Typer y despliegue via systemd + Ansible. Observabilidad con logs estructurados.

**Tech Stack:** Python 3.12, pydantic, typer, structlog, pyyaml, pytest, ruff, pyright, uv, GitHub Actions

**Spec:** `/home/champagnejesus/proyectos/agentguard/PROYECTO-PLAN.md`, `/home/champagnejesus/proyectos/agentguard/docs/ARCHITECTURE.md`

## Global Constraints
- Python >=3.12
- No dependencias externas en runtime salvo pydantic, typer, structlog, pyyaml
- Journal en `/var/lib/agentguard/sessions` con permisos 700
- Todos los commits con conventional commits
- Tests >80% cobertura en lógica core

## Review Focus
- Journal corrupto o truncado debe ser detectado por `verify`
- Adapter sin archivo de hook no debe bloquear engine
- Reglas YAML con sintaxis inválida deben fallar en carga, no en runtime
- Sesión con seq duplicado debe ser rechazada
- CLI debe funcionar sin variables de entorno seteadas

---

### Task 1: Journal hash-chain robusto

**Files:**
- Modify: `src/agentguard/journal.py`
- Test: `tests/test_journal.py`

**Interfaces:**
- Consumes: `AgentEvent`
- Produces: `Journal.append(event) -> None`, `Journal.verify() -> bool`

- [ ] Step 1: Write failing test for hash chain break detection
- [ ] Step 2: Run test to verify fail
- [ ] Step 3: Implement `append` with prev_hash validation y seq monotonía
- [ ] Step 4: Run tests
- [ ] Step 5: Commit

### Task 2: Adapter interface y normalización

**Files:**
- Modify: `src/agentguard/adapters/base.py`
- Create: `tests/test_adapters.py`

**Interfaces:**
- Produces: `AgentAdapter.stream_events(session_id) -> AsyncIterator[AgentEvent]`

- [ ] Step 1: Test adapter devuelve eventos normalizados
- [ ] Step 2: Implementar normalización con validación de campos obligatorios
- [ ] Step 3: Tests pasan
- [ ] Step 4: Commit

### Task 3: CLI Typer completo

**Files:**
- Modify: `src/agentguard/cli.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: Engine, Detector, Verify
- Produces: comandos `run`, `verify`, `report`, `list`

- [ ] Step 1: Test CLI `agentguard --help`
- [ ] Step 2: Implementar comandos con Typer
- [ ] Step 3: Tests pasan
- [ ] Step 4: Commit

### Task 4: Detector YAML con validación

**Files:**
- Modify: `src/agentguard/detector.py`
- Test: `tests/test_detector.py`

**Interfaces:**
- Consumes: reglas YAML
- Produces: `Detector.check(event) -> List[Hit]`

- [ ] Step 1: Test reglas inválidas fallan en carga
- [ ] Step 2: Implementar carga segura y match
- [ ] Step 3: Tests pasan
- [ ] Step 4: Commit

### Task 5: Paquete DEB/RPM y Ansible

**Files:**
- Create: `packaging/debian/`, `packaging/rpm/`, `ansible/role/`
- Test: `tests/test_packaging.py`

**Interfaces:**
- Produces: paquete instalable y rol idempotente

- [ ] Step 1: Test rol crea usuario y directorio
- [ ] Step 2: Implementar control files y playbook
- [ ] Step 3: Tests pasan
- [ ] Step 4: Commit

### Task 6: Demo y documentación pública

**Files:**
- Modify: `README.md`, `docs/DEMO.md`
- Create: `docs/demo.gif`

**Interfaces:**
- Produces: demo reproducible

- [ ] Step 1: Script demo genera sesión y reporte
- [ ] Step 2: Generar GIF y actualizar README
- [ ] Step 3: Commit

