import sqlite3
import threading
from datetime import datetime
from pathlib import Path

import database

CARPETA = Path(__file__).parent.parent / "respaldos"
MAX_RESPALDOS = 5


def crear_respaldo():
    CARPETA.mkdir(exist_ok=True)
    nombre = f"reposteria_{datetime.now():%Y%m%d_%H%M%S}.db"
    origen = sqlite3.connect(database.RUTA_BD)
    copia = sqlite3.connect(CARPETA / nombre)
    try:
        origen.backup(copia)
    finally:
        copia.close()
        origen.close()
    limpiar_antiguos()
    return nombre


def limpiar_antiguos():
    archivos = sorted(CARPETA.glob("reposteria_*.db"))
    for viejo in archivos[:-MAX_RESPALDOS]:
        viejo.unlink()


def listar_respaldos():
    if not CARPETA.exists():
        return []
    return sorted((p.name for p in CARPETA.glob("reposteria_*.db")), reverse=True)


class HiloRespaldo(threading.Thread):
    def __init__(self, intervalo_segundos=300):
        super().__init__(daemon=True)
        self.intervalo = intervalo_segundos
        self._detener = threading.Event()

    def run(self):
        while True:
            try:
                crear_respaldo()
            except Exception as error:
                print(f"[respaldo] error: {error}")
            if self._detener.wait(self.intervalo):
                break

    def detener(self):
        self._detener.set()