import sqlite3

from fastapi import APIRouter, HTTPException

from esquemas import ClienteEntrada, ClienteSalida
from repositorios.cliente_repositorio import ClienteRepositorio

router = APIRouter(prefix="/clientes", tags=["Clientes"])
repo = ClienteRepositorio()


@router.get("/", response_model=list[ClienteSalida])
def listar(buscar: str | None = None):
    if buscar:
        return repo.buscar_por_nombre(buscar)
    return repo.obtener_todos()


@router.get("/{id}", response_model=ClienteSalida)
def obtener(id: int):
    cliente = repo.obtener_por_id(id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/", response_model=ClienteSalida, status_code=201)
def crear(cliente: ClienteEntrada):
    try:
        nuevo_id = repo.crear(cliente.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese correo")
    return repo.obtener_por_id(nuevo_id)


@router.put("/{id}", response_model=ClienteSalida)
def actualizar(id: int, cliente: ClienteEntrada):
    try:
        actualizado = repo.actualizar(id, cliente.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese correo")
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return repo.obtener_por_id(id)


@router.delete("/{id}")
def eliminar(id: int):
    try:
        eliminado = repo.eliminar(id)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="No se puede eliminar: el cliente tiene pedidos"
        )
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"mensaje": "Cliente eliminado"}