import sqlite3

from fastapi import APIRouter, HTTPException

from esquemas import IngredienteEntrada, IngredienteSalida
from repositorios.ingrediente_repositorio import IngredienteRepositorio

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])
repo = IngredienteRepositorio()


@router.get("/", response_model=list[IngredienteSalida])
def listar(buscar: str | None = None):
    if buscar:
        return repo.buscar_por_nombre(buscar)
    return repo.obtener_todos()


@router.get("/sin-existencia", response_model=list[IngredienteSalida])
def sin_existencia():
    return repo.listar_sin_existencia()


@router.get("/{id}", response_model=IngredienteSalida)
def obtener(id: int):
    ingrediente = repo.obtener_por_id(id)
    if ingrediente is None:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


@router.post("/", response_model=IngredienteSalida, status_code=201)
def crear(ingrediente: IngredienteEntrada):
    try:
        nuevo_id = repo.crear(ingrediente.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un ingrediente con ese nombre")
    return repo.obtener_por_id(nuevo_id)


@router.put("/{id}", response_model=IngredienteSalida)
def actualizar(id: int, ingrediente: IngredienteEntrada):
    try:
        actualizado = repo.actualizar(id, ingrediente.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Ya existe un ingrediente con ese nombre")
    if not actualizado:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return repo.obtener_por_id(id)


@router.delete("/{id}")
def eliminar(id: int):
    try:
        eliminado = repo.eliminar(id)
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar: el ingrediente se usa en una receta",
        )
    if not eliminado:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return {"mensaje": "Ingrediente eliminado"}