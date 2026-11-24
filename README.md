# TaskManager-DevOps

Sistema web para la gestión de tareas.

[![Integracion Continua](https://github.com/taariis/TaskManager-DevOps/actions/workflows/ci.yml/badge.svg)](https://github.com/taariis/TaskManager-DevOps/actions/workflows/ci.yml)

TaskManager es una aplicación web para **TechSolutions** que centraliza el registro, la asignación y el seguimiento de las tareas de los empleados. Sustituye a las hojas de cálculo que se usaban antes. El proyecto se construyó siguiendo las fases del ciclo de vida **DevOps** con GitHub como plataforma principal.

**Aplicación publicada:** https://taskmanager-devops-c1yw.onrender.com

## Funcionalidades

| Código | Funcionalidad | Implementación |
|---|---|---|
| RF01 | Registrar tareas | `POST /api/tareas` + formulario "Nueva tarea" |
| RF02 | Consultar tareas | `GET /api/tareas` (con filtros `?estado=` y `?prioridad=`) |
| RF03 | Editar tareas | `PUT /api/tareas/<id>` + botón "Editar" |
| RF04 | Eliminar tareas | `DELETE /api/tareas/<id>` + botón "Eliminar" |
| RF05 | Cambiar estado | `PATCH /api/tareas/<id>/estado` (Pendiente, En proceso, Terminada) |
| RF06 | Asignar prioridad | Alta, Media o Baja |
| Extra | Monitoreo | `GET /health` y cabecera `X-Response-Time-ms` |

## Tecnologías

- **Frontend:** HTML, CSS y JavaScript
- **Backend:** Python 3.12 con Flask
- **Base de datos:** SQLite
- **Pruebas:** Pytest
- **CI/CD:** GitHub Actions
- **Despliegue:** Render (con Gunicorn)

## Estructura

```text
TaskManager-DevOps/
├── app.py                  # Backend Flask + API REST
├── requirements.txt
├── render.yaml             # Configuración de despliegue en Render
├── templates/index.html
├── static/css/style.css
├── static/js/app.js
├── tests/test_app.py       # Pruebas unitarias (pytest)
├── docs/                   # Historias de usuario, pruebas, monitoreo, mejoras
└── .github/workflows/
    ├── ci.yml              # Integración continua
    ├── cd.yml              # Entrega continua (artefacto al publicar Release)
    ├── deploy.yml          # Despliegue continuo (Render)
    └── monitor.yml         # Monitoreo programado
```

## Ejecución local

```bash
git clone https://github.com/taariis/TaskManager-DevOps.git
cd TaskManager-DevOps
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5000
pytest -v                # ejecutar pruebas
```

## Flujo DevOps

| Fase | Herramienta | Resultado |
|---|---|---|
| Plan | GitHub Projects e Issues | Tablero, historias de usuario e issues |
| Code | Git y GitHub | Ramas `feature/*`, commits y Pull Requests |
| Build / CI | GitHub Actions (`ci.yml`) | Pruebas automáticas en cada push/PR |
| Test | Pytest + matriz de pruebas | [docs/matriz_pruebas.md](docs/matriz_pruebas.md) |
| Release | GitHub Releases + `cd.yml` | Versión v1.0.0 y artefacto `TaskManager-v1` |
| Deploy | Render + `deploy.yml` | Aplicación pública |
| Operate & Monitor | `monitor.yml` + Issues | [docs/monitoreo.md](docs/monitoreo.md) |

## Documentación

- [Historias de usuario](docs/historias_usuario.md)
- [Matriz de casos de prueba](docs/matriz_pruebas.md)
- [Registro de monitoreo e incidencias](docs/monitoreo.md)
- [Propuestas de mejora y plan v1.1](docs/mejoras.md)
- [Preguntas de análisis](docs/preguntas_analisis.md)

## Equipo

| Rol | Integrante |
|---|---|
| Product Owner | _Integrante 1_ |
| Desarrollador (backend) | _Integrante 2_ |
| Desarrollador (frontend) / DevOps-QA | _Integrante 3_ |
