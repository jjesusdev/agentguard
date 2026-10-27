# Metodología de Auditoría Forense AgentGuard

Basada en Cloudflare Security Audit Skill y adaptada a forense de agentes YOLO.

## Fases

### 1. Reconocimiento
Mapear arquitectura, trust boundaries, superficies de entrada, evidencia previa.
Para AgentGuard:
- Identificar sesiones activas
- Mapear rutas sensibles
- Cargar reglas YAML existentes

Salida: `session-metadata.json`, `coverage-ledger.json`

### 2. Hunting guiado por cobertura
Asignar hunters a unidades de cobertura: por herramienta, por archivo, por comando.
Ej: `Bash` con `curl | bash`, `Edit` sobre `.env`.

Salida: candidatos de riesgo.

### 3. Validación de candidatos
Cada candidato se entrega a un verificador fresco que intenta desprobarlo.
No se eleva a hallazgo sin trazabilidad de fuente.

### 4. Salida estructurada
`findings.json` con 3 veredictos:
- `confirmed` — trazabilidad completa, resultado acotado
- `needs_validation` — hecho exacto sin resolver
- `rejected` — candidato desprobado

Validar contra schema JSON.

### 5. Verificación independiente de registros
Agente fresco verifica claims de fuente. Reemplazos materiales reciben otro verificador.

### 6. Reporte target-neutral
`REPORT.md`, `FINDINGS-DETAIL.md`, `NEEDS-VALIDATION.md` derivados de registros verificados.

## Principios

- **Solo confirmar fallos de frontera reales**. Sin principal afectado = `needs_validation`.
- **Validación adversarial**. Quien encuentra no valida.
- **Severity requiere impacto**. Likelihood x impacto.
- **Múltiples runs mejoran cobertura**.

## Write isolation

Parent único escritor. Workers solo escriben en `scratch/`. Promoción segura con `fstat`, verificación de tamaño, sin symlinks.

## Anti-patrones

- Checklist sin violación de frontera
- Asumir comportamiento de despliegue no en source
- Reportar severidad a `needs_validation`
- Escribir reporte antes de verificación independiente
