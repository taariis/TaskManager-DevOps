# Operación y monitoreo

## Mecanismos implementados

| Qué se verifica | Cómo |
|---|---|
| Disponibilidad | Workflow `monitor.yml` cada 6 horas (y manual) consulta `/health`, `/` y `/api/tareas` |
| Tiempo de respuesta | `curl -w %{time_total}` en el workflow y cabecera `X-Response-Time-ms` en cada respuesta |
| Errores | Logs de Render (cada petición registra método, ruta, código y milisegundos) |
| Almacenamiento | `/health` cuenta las tareas en SQLite y responde 503 si la base de datos falla |
| Funcionalidades principales | Pruebas funcionales CP01–CP07 sobre la URL pública |
| Incidencias | Si el monitoreo falla, se crea automáticamente un Issue con la etiqueta `incidencia` |

## Registro de monitoreo

Aplicación: https://taskmanager-devops-c1yw.onrender.com. Mediciones del 2026-11-24 a las 22:23 UTC, hechas con `curl` desde un equipo local (tres por endpoint).

| Endpoint | Código HTTP | Tiempos (s) |
|---|---|---|
| /health | 200 | 0.250, 0.222, 0.217 |
| / | 200 | 0.234, 0.278, 0.232 |
| /api/tareas | 200 | 0.222, 0.227, 0.240 |

La primera ejecución de **Monitoreo** que consultó la aplicación es la [45500459254](https://github.com/taariis/TaskManager-DevOps/actions/runs/45500459254). Las anteriores terminaron en verde sin revisar nada, porque `APP_URL` no estaba configurada.

## Riesgos previstos (Issues #31 y #32)

Son limitaciones conocidas del plan gratuito de Render; a la fecha **no se han observado** en esta aplicación.

| Riesgo | Funcionalidad | Descripción | Acción prevista |
|---|---|---|---|
| Primera carga lenta tras inactividad | Disponibilidad | El servicio se suspende tras un periodo sin tráfico | Plan de pago en producción |
| Pérdida de tareas al redesplegar | Almacenamiento | SQLite está en `/tmp`, un disco efímero | Base de datos persistente en v1.1.0 (#33) |
