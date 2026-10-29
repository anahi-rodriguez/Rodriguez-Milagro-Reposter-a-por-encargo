import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).parent / "reposteria.db"

def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BD)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_Keys = ON")
    return conexion