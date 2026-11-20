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

Copiar los valores de la tabla que genera el workflow **Monitoreo** (pestaña Actions → ejecución → Summary).

| Fecha | Endpoint | Código HTTP | Tiempo de respuesta | Observaciones |
|---|---|---|---|---|
| _AAAA-MM-DD_ | /health | 200 | _x.xx s_ | |
| _AAAA-MM-DD_ | / | 200 | _x.xx s_ | |
| _AAAA-MM-DD_ | /api/tareas | 200 | _x.xx s_ | |

## Incidencias documentadas (ver Issues con etiqueta `incidencia`)

| Incidencia | Funcionalidad afectada | Descripción | Responsable | Solución aplicada |
|---|---|---|---|---|
| Primera carga lenta tras inactividad | Disponibilidad | En el plan gratuito de Render el servicio se suspende tras 15 min sin uso; la primera petición tarda ~30–50 s | Ingeniero DevOps / QA | El monitoreo periódico lo registra; para producción se recomienda un plan de pago |
| Pérdida de tareas al redesplegar | Almacenamiento | El disco del plan gratuito es efímero (SQLite en `/tmp`), por lo que las tareas se borran en cada despliegue | Desarrollador backend | Documentado; en v1.1 se migrará a PostgreSQL o a un disco persistente |
