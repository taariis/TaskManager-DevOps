"""Pruebas unitarias de TaskManager (pytest)."""
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    with app.test_client() as cliente:
        yield cliente


def crear(client, **datos):
    base = {"nombre": "Realizar actividad DevOps", "descripcion": "Fase de pruebas", "prioridad": "Alta"}
    base.update(datos)
    return client.post("/api/tareas", json=base)


def test_registro_tarea_ejemplo():
    tarea = {"nombre": "Realizar actividad DevOps", "estado": "Pendiente"}
    assert tarea["nombre"] == "Realizar actividad DevOps"
    assert tarea["estado"] == "Pendiente"


def test_pagina_principal(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"TaskManager" in resp.data


# ==== RF01 - Registrar tareas ====
def test_registrar_tarea(client):
    resp = crear(client)
    assert resp.status_code == 201
    datos = resp.get_json()
    assert datos["mensaje"] == "Tarea registrada correctamente"
    assert datos["tarea"]["nombre"] == "Realizar actividad DevOps"
    assert datos["tarea"]["estado"] == "Pendiente"


def test_registrar_tarea_sin_nombre(client):
    resp = crear(client, nombre="   ")
    assert resp.status_code == 400
    assert "obligatorio" in resp.get_json()["error"]


def test_registrar_tarea_sin_json(client):
    resp = client.post("/api/tareas", data="texto", content_type="text/plain")
    assert resp.status_code == 400


# ==== RF06 - Asignar prioridad ====
@pytest.mark.parametrize("prioridad", ["Alta", "Media", "Baja"])
def test_prioridades_validas(client, prioridad):
    resp = crear(client, prioridad=prioridad)
    assert resp.status_code == 201
    assert resp.get_json()["tarea"]["prioridad"] == prioridad


def test_prioridad_invalida(client):
    resp = crear(client, prioridad="Urgentisima")
    assert resp.status_code == 400


def test_prioridad_por_defecto(client):
    resp = client.post("/api/tareas", json={"nombre": "Sin prioridad", "descripcion": "x"})
    assert resp.get_json()["tarea"]["prioridad"] == "Media"


# ==== RF02 - Consultar tareas ====
def test_consultar_tareas(client):
    crear(client, nombre="Tarea 1")
    crear(client, nombre="Tarea 2")
    resp = client.get("/api/tareas")
    assert resp.status_code == 200
    nombres = [t["nombre"] for t in resp.get_json()]
    assert nombres == ["Tarea 2", "Tarea 1"]


def test_consultar_tarea_inexistente(client):
    assert client.get("/api/tareas/999").status_code == 404


def test_filtrar_por_prioridad(client):
    crear(client, nombre="A", prioridad="Alta")
    crear(client, nombre="B", prioridad="Baja")
    resp = client.get("/api/tareas?prioridad=Baja")
    assert [t["nombre"] for t in resp.get_json()] == ["B"]


# ==== RF03 - Editar tareas ====
def test_editar_tarea(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.put(
        f"/api/tareas/{tarea_id}",
        json={"nombre": "Nombre editado", "descripcion": "Nueva", "prioridad": "Baja", "estado": "En proceso"},
    )
    assert resp.status_code == 200
    tarea = client.get(f"/api/tareas/{tarea_id}").get_json()
    assert tarea["nombre"] == "Nombre editado"
    assert tarea["prioridad"] == "Baja"
    assert tarea["estado"] == "En proceso"


def test_editar_tarea_inexistente(client):
    resp = client.put("/api/tareas/999", json={"nombre": "X"})
    assert resp.status_code == 404


def test_editar_tarea_sin_nombre(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.put(f"/api/tareas/{tarea_id}", json={"nombre": ""})
    assert resp.status_code == 400


# ==== RF04 - Eliminar tareas ====
def test_eliminar_tarea(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    assert client.delete(f"/api/tareas/{tarea_id}").status_code == 200
    assert client.get(f"/api/tareas/{tarea_id}").status_code == 404
    assert client.get("/api/tareas").get_json() == []


def test_eliminar_tarea_inexistente(client):
    assert client.delete("/api/tareas/999").status_code == 404


# ==== RF05 - Cambiar estado ====
@pytest.mark.parametrize("estado", ["Pendiente", "En proceso", "Terminada"])
def test_cambiar_estado(client, estado):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.patch(f"/api/tareas/{tarea_id}/estado", json={"estado": estado})
    assert resp.status_code == 200
    assert client.get(f"/api/tareas/{tarea_id}").get_json()["estado"] == estado


def test_cambiar_estado_invalido(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.patch(f"/api/tareas/{tarea_id}/estado", json={"estado": "Cancelada"})
    assert resp.status_code == 400


def test_cambiar_estado_reflejado_en_listado(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    client.patch(f"/api/tareas/{tarea_id}/estado", json={"estado": "Terminada"})
    listado = client.get("/api/tareas?estado=Terminada").get_json()
    assert [t["id"] for t in listado] == [tarea_id]


# ==== Issue de error - tarea sin descripcion ====
def test_registrar_tarea_sin_descripcion(client):
    resp = client.post("/api/tareas", json={"nombre": "Tarea sin descripcion", "prioridad": "Alta"})
    assert resp.status_code == 201
    assert resp.get_json()["tarea"]["descripcion"] == ""


# ==== Operate & Monitor ====
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"
    assert "X-Response-Time-ms" in resp.headers
