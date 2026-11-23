import threading

from fastapi import APIRouter

from servicios.respaldo import crear_respaldo, listar_respaldos

router = APIRouter(prefix="/respaldos", tags=["Respaldos"])


@router.get("/")
def listar():
    return {"respaldos": listar_respaldos()}


@router.post("/", status_code=202)
def solicitar_respaldo():
    threading.Thread(target=crear_respaldo, daemon=True).start()
    return {"mensaje": "Respaldo iniciado en segundo plano"}