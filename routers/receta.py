import sqlite3

from fastapi import APIRouter, HTTPException

from esquemas import RecetaDetalleSalida, RecetaEntrada, RecetaSalida
from repositorios.ingrediente_repositorio import IngredienteRepositorio
from repositorios.producto_repositorio import ProductoRepositorio
from repositorios.receta_repositorio import RecetaRepositorio

router = APIRouter(prefix="/receta", tags=["Receta"])
repo = RecetaRepositorio()
repo_productos = ProductoRepositorio()
repo_ingredientes = IngredienteRepositorio()


def validar_referencias(datos: RecetaEntrada):
    if repo_productos.obtener_por_id(datos.producto_id) is None:
        raise HTTPException(status_code=400, detail="El producto no existe")
    if repo_ingredientes.obtener_por_id(datos.ingrediente_id) is None:
        raise HTTPException(status_code=400, detail="El ingrediente no existe")


@router.get("/", response_model=list[RecetaSalida])
def listar():
    return repo.obtener_todos()


@router.get("/producto/{producto_id}", response_model=list[RecetaDetalleSalida])
def receta_de_producto(producto_id: int):
    if repo_productos.obtener_por_id(producto_id) is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return repo.obtener_por_producto(producto_id)


@router.get("/{id}", response_model=RecetaSalida)
def obtener(id: int):
    item = repo.obtener_por_id(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return item


@router.post("/", response_model=RecetaSalida, status_code=201)
def crear(datos: RecetaEntrada):
    validar_referencias(datos)
    try:
        nuevo_id = repo.crear(datos.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Ese ingrediente ya está en la receta del producto"
        )
    return repo.obtener_por_id(nuevo_id)


@router.put("/{id}", response_model=RecetaSalida)
def actualizar(id: int, datos: RecetaEntrada):
    validar_referencias(datos)
    try:
        actualizado = repo.actualizar(id, datos.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Ese ingrediente ya está en la receta del producto"
        )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return repo.obtener_por_id(id)


@router.delete("/{id}")
def eliminar(id: int):
    if not repo.eliminar(id):
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return {"mensaje": "Línea de receta eliminada"}