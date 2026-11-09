import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import database
from main import app
from seguridad import encriptar_password

RAIZ = Path(__file__).parent.parent


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    """Cliente de pruebas con una base temporal limpia (sin login)."""
    ruta = tmp_path / "prueba.db"
    monkeypatch.setattr(database, "RUTA_BD", ruta)

    conexion = sqlite3.connect(ruta)
    conexion.executescript((RAIZ / "crear_bd.sql").read_text(encoding="utf-8"))
    conexion.execute(
        "INSERT INTO usuarios (username, password_hash, rol, activo) VALUES (?, ?, 'admin', 1)",
        ("tester", encriptar_password("clave123")),
    )
    conexion.commit()
    conexion.close()
    return TestClient(app)


@pytest.fixture()
def api(cliente):
    """Cliente de pruebas que ya hizo login."""
    respuesta = cliente.post(
        "/auth/login", data={"username": "tester", "password": "clave123"}
    )
    token = respuesta.json()["access_token"]
    cliente.headers.update({"Authorization": f"Bearer {token}"})
    return cliente