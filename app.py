"""TaskManager - Sistema web para la gestion de tareas de TechSolutions.

Backend en Flask con base de datos SQLite.
"""
import logging
import os
import sqlite3
import time
from datetime import datetime, timezone

from flask import Flask, g, jsonify, render_template, request

ESTADOS = ("Pendiente", "En proceso", "Terminada")
PRIORIDADES = ("Alta", "Media", "Baja")
VERSION = "1.0.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("taskmanager")


def ahora():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def get_db():
    """Devuelve una conexion SQLite reutilizable durante la peticion."""
    if "db" not in g:
        from flask import current_app

        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(database):
    with sqlite3.connect(database) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL DEFAULT '',
                prioridad TEXT NOT NULL DEFAULT 'Media',
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                creada_en TEXT NOT NULL,
                actualizada_en TEXT NOT NULL
            )
            """
        )


def fila_a_dict(fila):
    return {clave: fila[clave] for clave in fila.keys()}


def error(mensaje, codigo=400):
    return jsonify({"error": mensaje}), codigo


def create_app(config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = os.environ.get(
        "DATABASE_PATH", os.path.join(app.instance_path, "taskmanager.db")
    )
    if config:
        app.config.update(config)

    carpeta = os.path.dirname(app.config["DATABASE"])
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    init_db(app.config["DATABASE"])
    app.teardown_appcontext(close_db)

    @app.route("/")
    def index():
        return render_template("index.html", estados=ESTADOS, prioridades=PRIORIDADES)

    def buscar_tarea(tarea_id):
        return get_db().execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()

    # ==== RF01 / RF02 / RF06 - Registrar y consultar tareas ====
    def validar_tarea(data):
        """Valida los datos de una tarea. Devuelve (tarea, mensaje_error)."""
        if not isinstance(data, dict):
            return None, "Se esperaba un objeto JSON"
        nombre = str(data.get("nombre") or "").strip()
        if not nombre:
            return None, "El nombre de la tarea es obligatorio"
        if len(nombre) > 120:
            return None, "El nombre no puede superar 120 caracteres"
        descripcion = data["descripcion"].strip()
        prioridad = data.get("prioridad") or "Media"
        if prioridad not in PRIORIDADES:
            return None, "Prioridad invalida. Use: " + ", ".join(PRIORIDADES)
        estado = data.get("estado") or "Pendiente"
        if estado not in ESTADOS:
            return None, "Estado invalido. Use: " + ", ".join(ESTADOS)
        return {
            "nombre": nombre,
            "descripcion": descripcion,
            "prioridad": prioridad,
            "estado": estado,
        }, None

    @app.post("/api/tareas")
    def registrar_tarea():
        tarea, mensaje = validar_tarea(request.get_json(silent=True))
        if mensaje:
            return error(mensaje)
        fecha = ahora()
        db = get_db()
        cursor = db.execute(
            "INSERT INTO tareas (nombre, descripcion, prioridad, estado, creada_en, actualizada_en)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (tarea["nombre"], tarea["descripcion"], tarea["prioridad"], tarea["estado"], fecha, fecha),
        )
        db.commit()
        nueva = fila_a_dict(buscar_tarea(cursor.lastrowid))
        return jsonify({"mensaje": "Tarea registrada correctamente", "tarea": nueva}), 201

    @app.get("/api/tareas")
    def consultar_tareas():
        consulta = "SELECT * FROM tareas"
        filtros, valores = [], []
        estado = request.args.get("estado")
        prioridad = request.args.get("prioridad")
        if estado:
            filtros.append("estado = ?")
            valores.append(estado)
        if prioridad:
            filtros.append("prioridad = ?")
            valores.append(prioridad)
        if filtros:
            consulta += " WHERE " + " AND ".join(filtros)
        consulta += " ORDER BY id DESC"
        filas = get_db().execute(consulta, valores).fetchall()
        return jsonify([fila_a_dict(f) for f in filas])

    @app.get("/api/tareas/<int:tarea_id>")
    def consultar_tarea(tarea_id):
        fila = buscar_tarea(tarea_id)
        if fila is None:
            return error("Tarea no encontrada", 404)
        return jsonify(fila_a_dict(fila))

    # ==== RF03 - Editar tareas ====
    @app.put("/api/tareas/<int:tarea_id>")
    def editar_tarea(tarea_id):
        if buscar_tarea(tarea_id) is None:
            return error("Tarea no encontrada", 404)
        tarea, mensaje = validar_tarea(request.get_json(silent=True))
        if mensaje:
            return error(mensaje)
        db = get_db()
        db.execute(
            "UPDATE tareas SET nombre = ?, descripcion = ?, prioridad = ?, estado = ?,"
            " actualizada_en = ? WHERE id = ?",
            (tarea["nombre"], tarea["descripcion"], tarea["prioridad"], tarea["estado"], ahora(), tarea_id),
        )
        db.commit()
        return jsonify({"mensaje": "Tarea actualizada", "tarea": fila_a_dict(buscar_tarea(tarea_id))})

    # ==== RF04 - Eliminar tareas ====
    @app.delete("/api/tareas/<int:tarea_id>")
    def eliminar_tarea(tarea_id):
        if buscar_tarea(tarea_id) is None:
            return error("Tarea no encontrada", 404)
        db = get_db()
        db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        db.commit()
        return jsonify({"mensaje": "Tarea eliminada"})

    # ==== Fin de rutas ====
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
