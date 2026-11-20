# Matriz de casos de prueba

Columna **Prueba automatizada**: función de `tests/test_app.py` que cubre el caso.
Columna **Resultado obtenido**: resultado al ejecutar manualmente cada caso en la aplicación.

| ID | Prueba | Pasos | Resultado esperado | Prueba automatizada | Resultado obtenido |
|---|---|---|---|---|---|
| CP01 | Registrar una tarea | Escribir nombre "Elaborar documentación", descripción, prioridad Alta → Guardar | La tarea se guarda y aparece en el listado con el mensaje "Tarea registrada correctamente" | `test_registrar_tarea` | ✅ Aprobada |
| CP02 | Registrar una tarea sin nombre | Dejar el nombre vacío → Guardar | El sistema muestra "El nombre de la tarea es obligatorio" | `test_registrar_tarea_sin_nombre` | ✅ Aprobada |
| CP03 | Consultar tareas | Abrir el sistema con tareas registradas | Se muestra el listado y el resumen por estado | `test_consultar_tareas` | ✅ Aprobada |
| CP04 | Editar una tarea | Editar → cambiar nombre y prioridad → Actualizar | Se actualiza la información | `test_editar_tarea` | ✅ Aprobada |
| CP05 | Eliminar una tarea | Eliminar → Aceptar confirmación | La tarea desaparece del listado | `test_eliminar_tarea` | ✅ Aprobada |
| CP06 | Cambiar estado | Elegir "En proceso" y luego "Terminada" en el selector | Se actualiza el estado (Terminada se muestra tachada) | `test_cambiar_estado`, `test_cambiar_estado_reflejado_en_listado` | ✅ Aprobada |
| CP07 | Seleccionar prioridad | Registrar tareas con Alta, Media y Baja | Se guarda la prioridad elegida con su color | `test_prioridades_validas` | ✅ Aprobada |
| CP08 | Registrar tarea sin descripción | Escribir sólo el nombre → Guardar | La tarea se guarda con descripción vacía | `test_registrar_tarea_sin_descripcion` | ❌ Falló en la 1.ª ejecución (HTTP 500) → corregido → ✅ |
| CP09 | Filtrar tareas | Filtrar por prioridad Baja | Sólo se muestran tareas de prioridad Baja | `test_filtrar_por_prioridad` | ✅ Aprobada |
| CP10 | Estado inválido | Enviar `{"estado":"Cancelada"}` a la API | HTTP 400 con mensaje de validación | `test_cambiar_estado_invalido` | ✅ Aprobada |
| CP11 | Disponibilidad | Abrir `/health` | `{"status":"ok"}` | `test_health` | ✅ Aprobada |

## Errores encontrados

| Error | Causa | Rama de corrección | Resultado |
|---|---|---|---|
| Error al guardar tareas sin descripción (HTTP 500) | `KeyError: 'descripcion'` en `validar_tarea` | `fix/descripcion-opcional` | La prueba `test_registrar_tarea_sin_descripcion` falló en GitHub Actions; tras la corrección el workflow pasó en verde |
