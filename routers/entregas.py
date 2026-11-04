from datetime import date

from fastapi import APIRouter

from esquemas import EntregaSalida
from repositorios.pedido_repositorio import PedidoRepositorio

router = APIRouter(prefix="/entregas", tags=["Entregas"])
repo = PedidoRepositorio()


@router.get("/", response_model=list[EntregaSalida])
def entregas_del_dia(fecha: date | None = None):
    dia = fecha or date.today()
    return repo.entregas_del_dia(dia.isoformat())