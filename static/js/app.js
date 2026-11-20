// TaskManager - logica del frontend
const API = "/api/tareas";
const $ = (id) => document.getElementById(id);

function mostrarMensaje(texto, tipo = "ok") {
  const caja = $("mensaje");
  caja.textContent = texto;
  caja.className = "mensaje " + tipo;
  caja.hidden = false;
  clearTimeout(mostrarMensaje.timer);
  mostrarMensaje.timer = setTimeout(() => (caja.hidden = true), 3500);
}

async function peticion(url, opciones = {}) {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  const datos = await resp.json().catch(() => ({}));
  if (!resp.ok) throw new Error(datos.error || "Error inesperado del servidor");
  return datos;
}

function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto ?? "";
  return div.innerHTML;
}

// ==== RF02 - Consultar tareas ====
async function cargarTareas() {
  const params = new URLSearchParams();
  if ($("filtro-estado").value) params.set("estado", $("filtro-estado").value);
  if ($("filtro-prioridad").value) params.set("prioridad", $("filtro-prioridad").value);
  try {
    const tareas = await peticion(API + (params.toString() ? "?" + params : ""));
    pintarTareas(tareas);
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
}

function pintarTareas(tareas) {
  const cuerpo = $("lista-tareas");
  cuerpo.innerHTML = "";
  $("sin-tareas").hidden = tareas.length > 0;
  const conteo = { Pendiente: 0, "En proceso": 0, Terminada: 0 };
  tareas.forEach((t) => {
    conteo[t.estado] = (conteo[t.estado] || 0) + 1;
    const fila = document.createElement("tr");
    if (t.estado === "Terminada") fila.className = "Terminada";
    const opciones = window.ESTADOS.map(
      (e) => `<option ${e === t.estado ? "selected" : ""}>${e}</option>`
    ).join("");
    fila.innerHTML = `
      <td>${t.id}</td>
      <td><strong>${escapar(t.nombre)}</strong><small>${escapar(t.descripcion)}</small></td>
      <td><span class="badge ${t.prioridad}">${t.prioridad}</span></td>
      <td><select data-estado="${t.id}" aria-label="Estado">${opciones}</select></td>
      <td>
        <button class="btn chico" data-editar="${t.id}">Editar</button>
        <button class="btn chico peligro" data-eliminar="${t.id}">Eliminar</button>
      </td>`;
    cuerpo.appendChild(fila);
  });
  $("resumen").textContent =
    `Total: ${tareas.length} · Pendientes: ${conteo.Pendiente} · ` +
    `En proceso: ${conteo["En proceso"]} · Terminadas: ${conteo.Terminada}`;
}

$("filtro-estado").addEventListener("change", cargarTareas);
$("filtro-prioridad").addEventListener("change", cargarTareas);

// ==== RF01 / RF06 - Registrar tareas con prioridad ====
function datosFormulario() {
  return {
    nombre: $("nombre").value.trim(),
    descripcion: $("descripcion").value.trim(),
    prioridad: $("prioridad").value,
    estado: $("estado").value,
  };
}

function limpiarFormulario() {
  $("form-tarea").reset();
  $("tarea-id").value = "";
  $("prioridad").value = "Media";
  $("titulo-formulario").textContent = "Nueva tarea";
  $("btn-guardar").textContent = "Guardar tarea";
  $("btn-cancelar").hidden = true;
  $("nombre").classList.remove("invalido");
}

async function guardarTarea(evento) {
  evento.preventDefault();
  const datos = datosFormulario();
  if (!datos.nombre) {
    $("nombre").classList.add("invalido");
    mostrarMensaje("El nombre de la tarea es obligatorio", "error");
    return;
  }
  const id = $("tarea-id").value;
  try {
    const r = id
      ? await peticion(`${API}/${id}`, { method: "PUT", body: JSON.stringify(datos) })
      : await peticion(API, { method: "POST", body: JSON.stringify(datos) });
    mostrarMensaje(r.mensaje);
    limpiarFormulario();
    cargarTareas();
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
}

$("form-tarea").addEventListener("submit", guardarTarea);

// ==== RF03 - Editar tareas ====
async function editarTarea(id) {
  try {
    const t = await peticion(`${API}/${id}`);
    $("tarea-id").value = t.id;
    $("nombre").value = t.nombre;
    $("descripcion").value = t.descripcion;
    $("prioridad").value = t.prioridad;
    $("estado").value = t.estado;
    $("titulo-formulario").textContent = `Editar tarea #${t.id}`;
    $("btn-guardar").textContent = "Actualizar tarea";
    $("btn-cancelar").hidden = false;
    $("nombre").focus();
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
}

$("btn-cancelar").addEventListener("click", limpiarFormulario);
$("lista-tareas").addEventListener("click", (e) => {
  if (e.target.dataset.editar) editarTarea(e.target.dataset.editar);
});

// ==== RF04 - Eliminar tareas ====
async function eliminarTarea(id) {
  if (!confirm(`¿Eliminar la tarea #${id}?`)) return;
  try {
    const r = await peticion(`${API}/${id}`, { method: "DELETE" });
    mostrarMensaje(r.mensaje);
    cargarTareas();
  } catch (e) {
    mostrarMensaje(e.message, "error");
  }
}

$("lista-tareas").addEventListener("click", (e) => {
  if (e.target.dataset.eliminar) eliminarTarea(e.target.dataset.eliminar);
});

// ==== Inicio ====
cargarTareas();
