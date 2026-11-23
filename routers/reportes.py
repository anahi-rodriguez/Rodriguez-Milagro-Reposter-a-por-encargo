from fastapi import APIRouter

from repositorios.cliente_repositorio import ClienteRepositorio
from repositorios.pedido_repositorio import PedidoRepositorio
from servicios.reportes import ServicioReportes

router = APIRouter(prefix="/reportes", tags=["Reportes"])
servicio = ServicioReportes(PedidoRepositorio(), ClienteRepositorio())


@router.get("/ventas")
def reporte_ventas():
    return servicio.resumen()