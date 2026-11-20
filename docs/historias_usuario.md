# Historias de usuario - TaskManager

| HU | Requerimiento | Prioridad | Estimación (h) |
|---|---|---|---|
| HU01 | RF01 Registrar tareas | Crítica | 4 |
| HU02 | RF05 Cambiar estado | Alta | 3 |
| HU03 | RF02 Consultar tareas | Crítica | 3 |
| HU04 | RF03 Editar tareas | Alta | 3 |
| HU05 | RF04 Eliminar tareas | Alta | 2 |
| HU06 | RF06 Asignar prioridad | Media | 2 |
| HU07 | Filtrar tareas | Baja | 2 |
| HU08 | Disponibilidad del sistema (DevOps) | Media | 3 |

## HU01: Registrar tareas
**Como** usuario del sistema, **quiero** registrar nuevas tareas **para** organizar mis actividades.

**Criterios de aceptación**
- El sistema debe permitir ingresar el nombre de la tarea.
- El sistema debe permitir agregar una descripción.
- El sistema debe permitir seleccionar una prioridad.
- El sistema debe guardar la tarea.
- El sistema debe mostrar un mensaje de confirmación.

## HU02: Cambiar estado de tareas
**Como** usuario, **quiero** cambiar el estado de una tarea **para** conocer su progreso.

**Criterios de aceptación**
- Debe permitir seleccionar *Pendiente*.
- Debe permitir seleccionar *En proceso*.
- Debe permitir seleccionar *Terminada*.
- El cambio debe reflejarse en el listado de tareas.

## HU03: Consultar tareas
**Como** usuario, **quiero** ver todas las tareas registradas **para** identificar las pendientes y las terminadas.

**Criterios de aceptación**
- El sistema debe mostrar un listado con nombre, descripción, prioridad y estado.
- Las tareas más recientes deben aparecer primero.
- Debe mostrarse un resumen con el total de tareas por estado.
- Si no hay tareas, debe mostrarse el mensaje "No hay tareas registradas".

## HU04: Editar tareas
**Como** usuario, **quiero** modificar la información de una tarea **para** corregir errores o actualizar sus datos.

**Criterios de aceptación**
- Debe existir un botón "Editar" en cada tarea.
- El formulario debe cargarse con los datos actuales.
- El sistema debe validar que el nombre no quede vacío.
- Los cambios deben guardarse y reflejarse en el listado.
- Debe poder cancelarse la edición.

## HU05: Eliminar tareas
**Como** usuario, **quiero** eliminar tareas que ya no son necesarias **para** evitar duplicidad.

**Criterios de aceptación**
- Debe existir un botón "Eliminar" en cada tarea.
- El sistema debe pedir confirmación antes de eliminar.
- La tarea debe desaparecer del listado.
- Debe mostrarse un mensaje de confirmación.

## HU06: Asignar prioridad
**Como** usuario, **quiero** clasificar las tareas como Alta, Media o Baja **para** atender primero las más importantes.

**Criterios de aceptación**
- El sistema debe ofrecer las prioridades Alta, Media y Baja.
- Si no se elige una, se asigna Media.
- La prioridad debe mostrarse con un color distinto en el listado.
- No se deben aceptar prioridades distintas a las permitidas.

## HU07: Filtrar tareas
**Como** usuario, **quiero** filtrar el listado por estado y prioridad **para** encontrar tareas rápidamente.

**Criterios de aceptación**
- Debe existir un filtro por estado.
- Debe existir un filtro por prioridad.
- Los filtros pueden combinarse.

## HU08: Disponibilidad del sistema
**Como** administrador de TechSolutions, **quiero** saber si el sistema está disponible y qué tan rápido responde **para** detectar fallas a tiempo.

**Criterios de aceptación**
- Debe existir un endpoint `/health` que indique el estado del sistema y de la base de datos.
- Cada respuesta debe incluir su tiempo de respuesta.
- Un workflow debe revisar la aplicación periódicamente y registrar una incidencia si falla.
