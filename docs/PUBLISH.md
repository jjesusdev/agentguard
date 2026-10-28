# Publicar AgentGuard v1.0 en GitHub

## 1. Crear repo público
Crea en GitHub: `usuario/agentguard` con README vacío.

## 2. Cambiar remote y push
```bash
cd /home/champagnejesus/proyectos/agentguard
git remote set-url origin git@github.com:usuario/agentguard.git
git branch -M main
git push -u origin main
```

## 3. Actualizar badge CI en README.md
Reemplaza en README.md:
```
[![CI](https://github.com/usuario/agentguard/actions/workflows/ci.yml/badge.svg)](https://github.com/usuario/agentguard/actions/workflows/ci.yml)
```

## 4. Generar demo GIF
```bash
brew install vhs ffmpeg ttyd  # macOS
vhs docs/agentguard.tape
git add docs/demo.gif docs/demo.mp4
git commit -m "docs: add demo GIF for v1.0"
git push
```

## 5. Release v1.0
En GitHub → Releases → v1.0.0
Changelog:
- Auditoria forense hash-chained multi-agente
- CLI Typer run/verify/report/list
- Detector YAML
- Hooks install script
- Demo VHS

## 6. LinkedIn
Usar docs/LINKEDIN_POST.md
```

