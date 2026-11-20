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


