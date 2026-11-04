from typing import Literal

from pydantic import BaseModel, Field


class ClienteEntrada(BaseModel):
    nombre: str = Field(min_length=1)
    telefono: str = Field(min_length=1)
    correo: str | None = None
    direccion: str | None = None


class ClienteSalida(ClienteEntrada):
    id: int

class ProductoEntrada(BaseModel):
    nombre: str = Field(min_length=1)
    tipo: Literal["pastel", "cupcake", "galleta", "postre", "otro"]
    precio_base: float = Field(gt=0)


class ProductoSalida(ProductoEntrada):
    id: int