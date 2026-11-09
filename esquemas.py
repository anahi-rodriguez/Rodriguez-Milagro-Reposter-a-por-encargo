from typing import Literal

from pydantic import BaseModel, Field
from datetime import date


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

class IngredienteEntrada(BaseModel):
    nombre: str = Field(min_length=1)
    unidad: str = Field(min_length=1)
    existencia: float = Field(ge=0)


class IngredienteSalida(IngredienteEntrada):
    id: int

class RecetaEntrada(BaseModel):
    producto_id: int
    ingrediente_id: int
    cantidad: float = Field(gt=0)


class RecetaSalida(RecetaEntrada):
    id: int


class RecetaDetalleSalida(BaseModel):
    id: int
    ingrediente_id: int
    ingrediente: str
    unidad: str
    cantidad: float

class DetallePedidoEntrada(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0)
    personalizacion: str | None = None


class PedidoEntrada(BaseModel):
    cliente_id: int
    fecha_entrega: date
    direccion: str = Field(min_length=1)
    anticipo: float = Field(ge=0)
    detalles: list[DetallePedidoEntrada] = Field(min_length=1)


class PedidoActualizar(BaseModel):
    fecha_entrega: date
    direccion: str = Field(min_length=1)
    anticipo: float = Field(ge=0)


class DetallePedidoSalida(BaseModel):
    id: int
    producto_id: int
    producto: str
    cantidad: int
    precio_unitario: float
    personalizacion: str | None = None


class PedidoSalida(BaseModel):
    id: int
    cliente_id: int
    fecha_pedido: date
    fecha_entrega: date
    direccion: str
    anticipo: float
    total: float
    estado: str


class PedidoDetalleSalida(PedidoSalida):
    detalles: list[DetallePedidoSalida]

class IngredienteNecesarioSalida(BaseModel):
    ingrediente_id: int
    ingrediente: str
    unidad: str
    necesario: float
    existencia: float
    alcanza: bool


class EntregaSalida(BaseModel):
    id: int
    cliente: str
    telefono: str
    direccion: str
    fecha_entrega: date
    estado: str
    total: float
    anticipo: float
    saldo: float

class TokenSalida(BaseModel):
    access_token: str
    token_type: str