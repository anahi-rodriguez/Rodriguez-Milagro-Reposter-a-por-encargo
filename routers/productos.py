import sqlite3

from fastapi import APIRouter, HTTPException

from esquemas import ProductoEntrada, ProductoSalida
from repositorios.producto_repositorio import ProductoRepositorio

router = APIRouter(prefix="/productos", tags=["Productos"])
repo = ProductoRepositorio()


@router.get("/", response_model=list[ProductoSalida])
def listar(buscar: str | None = None, tipo: str | None = None):
    if buscar:
        return repo.buscar_por_nombre(buscar)
    if tipo:
        return repo.listar_por_tipo(tipo)
    return repo.obtener_todos()


@router.get("/{id}", response_model=ProductoSalida)
def obtener(id: int):
    producto = repo.obtener_por_id(id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoSalida, status_code=201)
def crear(producto: ProductoEntrada):
    try:
        nuevo_id = repo.crear(producto.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre")
    return repo.obtener_por_id(nuevo_id)


@router.put("/{id}", response_model=ProductoSalida)
def actualizar(id: int, producto: ProductoEntrada):
    try:
        actualizado = repo.actualizar(id, producto.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre")
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return repo.obtener_por_id(id)


@router.delete("/{id}")
def eliminar(id: int):
    try:
        eliminado = repo.eliminar(id)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar: el producto tiene recetas o pedidos",
        )
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}