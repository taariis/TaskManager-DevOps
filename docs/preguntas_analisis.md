# Preguntas de análisis

**1. ¿Qué ventajas ofrece utilizar GitHub Projects para organizar un proyecto de software?**
Concentra en un solo tablero todas las actividades y las enlaza con los Issues y Pull Requests del código. Con eso se ve quién es responsable de cada tarea, en qué estado está (Backlog, To Do, In Progress, Review, Done), qué prioridad tiene, cuántas horas se estimaron y su fecha límite. Así se evitan la pérdida de información y la duplicidad que había con las hojas de cálculo.

**2. ¿Cuál es la diferencia entre Git y GitHub?**
Git es un sistema de control de versiones distribuido que se instala localmente y registra el historial de cambios del código (commits, ramas, merges). GitHub es una plataforma en la nube que aloja repositorios Git y agrega herramientas de colaboración: Issues, Pull Requests, Projects, Actions, Releases y revisiones de código.

**3. ¿Por qué es importante utilizar ramas durante el desarrollo?**
Las ramas permiten que cada integrante trabaje en una funcionalidad aislada sin afectar la rama `main`, que siempre debe ser estable. Facilitan el trabajo en paralelo, la revisión antes de integrar y descartar cambios fallidos sin dañar el proyecto.

**4. ¿Qué función cumple un Pull Request?**
Es una solicitud para integrar los cambios de una rama en otra (normalmente `main`). Muestra las diferencias, permite que otro integrante revise y comente el código, ejecuta automáticamente la integración continua y deja un registro de qué se cambió, por qué y quién lo aprobó.

**5. ¿Qué problemas permite detectar la integración continua?**
Errores de sintaxis, pruebas unitarias que fallan, dependencias faltantes, conflictos entre cambios de distintos desarrolladores y regresiones (funcionalidades que dejan de funcionar). En este proyecto detectó el error HTTP 500 al registrar una tarea sin descripción antes de integrarlo a `main`.

**6. ¿Cuál es la diferencia entre integración continua y entrega continua?**
La integración continua compila y prueba automáticamente el código cada vez que alguien hace un push o un Pull Request. La entrega continua va un paso más allá: deja preparada una versión estable y empaquetada (Release v1.0.0 y artefacto) lista para desplegarse, aunque la publicación final puede requerir aprobación manual.

**7. ¿Qué diferencia existe entre entrega continua y despliegue continuo?**
En la entrega continua la versión queda lista para producción, pero alguien decide cuándo publicarla. En el despliegue continuo cada cambio que pasa las pruebas se publica automáticamente en el servidor (en este proyecto, Render redespliega cada vez que se integra a `main` y la CI pasa).

**8. ¿Por qué es importante automatizar las pruebas?**
Porque se ejecutan siempre, de forma rápida y sin depender de que alguien lo recuerde. Garantizan que los cambios nuevos no rompan lo que ya funcionaba, reducen errores humanos y dan confianza para integrar y publicar con frecuencia.

**9. ¿Qué sucede si se integra código que contiene errores?**
La rama principal deja de ser estable, el error puede llegar a los usuarios finales, otros integrantes trabajan sobre código defectuoso y corregirlo cuesta más tiempo. Por eso la CI bloquea o alerta antes de hacer el merge.

**10. ¿Por qué DevOps requiere monitorear una aplicación después de publicarla?**
Porque en producción aparecen problemas que no se ven en pruebas: caídas del servidor, lentitud, fallas de la base de datos o uso real distinto al esperado. El monitoreo permite detectarlos a tiempo, registrarlos como incidencias y alimentar la planeación de la siguiente versión. Así se cierra el ciclo DevOps.

**11. ¿Qué beneficios obtiene una empresa al implementar DevOps?**
Entregas más rápidas y frecuentes, menos errores en producción, mejor colaboración entre desarrollo y operaciones, trazabilidad de cada cambio, recuperación más rápida ante fallas y clientes más satisfechos.

**12. ¿Cómo podrían mejorar el proceso de desarrollo en una segunda versión?**
Proteger la rama `main` para exigir revisión aprobada y CI en verde antes de cada merge; agregar análisis de cobertura y lint; usar una base de datos persistente; crear entornos separados de *staging* y producción; agregar alertas automáticas del monitoreo; y planificar con milestones y sprints en GitHub Projects (ver [mejoras.md](mejoras.md)).
