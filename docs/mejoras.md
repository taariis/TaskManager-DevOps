# Propuestas de mejora y planeación de la versión 1.1.0

| # | Mejora | Justificación | Prioridad | Estimación (h) |
|---|---|---|---|---|
| 1 | Autenticación de usuarios (login y roles) | Cada empleado debe ver y gestionar sólo sus tareas | Alta | 12 |
| 2 | Asignar responsable y fecha límite a cada tarea | La empresa necesita saber quién hace qué y cuándo | Alta | 6 |
| 3 | Base de datos persistente (PostgreSQL) | Evitar la pérdida de datos del disco efímero | Crítica | 5 |
| 4 | Búsqueda por texto | Encontrar tareas cuando el listado crece | Media | 3 |
| 5 | Notificaciones por correo de tareas vencidas | Evitar que se olviden tareas | Baja | 8 |
| 6 | Reportes de productividad (gráficas por estado y responsable) | Apoyar la toma de decisiones | Media | 8 |

## Plan de la versión v1.1.0

1. Crear un milestone **v1.1.0** en GitHub y un Issue por cada mejora (Plan).
2. Desarrollar cada mejora en su rama `feature/*` con Pull Request y revisión (Code).
3. Ampliar `tests/test_app.py` con pruebas de autenticación y persistencia (Test).
4. Añadir cobertura (`pytest-cov`) y lint (`flake8`) al workflow de CI (Build/CI).
5. Publicar el Release `v1.1.0` y desplegar automáticamente (Release/Deploy).
6. Agregar alertas por correo al workflow de monitoreo (Monitor).
