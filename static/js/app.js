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

// ==== Inicio ====
cargarTareas();
