from fastapi import APIRouter, Response

from repositorios.cliente_repositorio import ClienteRepositorio
from repositorios.pedido_repositorio import PedidoRepositorio
from servicios.exportador import generar_csv
from servicios.reportes import ServicioReportes

router = APIRouter(prefix="/reportes", tags=["Reportes"])
repo_pedidos = PedidoRepositorio()
servicio = ServicioReportes(repo_pedidos, ClienteRepositorio())

COLUMNAS_PEDIDOS = [
    "id", "cliente", "fecha_pedido", "fecha_entrega",
    "estado", "total", "anticipo", "saldo",
]


@router.get("/ventas")
def reporte_ventas():
    return servicio.resumen()


@router.get("/pedidos/csv")
def exportar_pedidos_csv():
    filas = repo_pedidos.pedidos_con_cliente()
    contenido = generar_csv(filas, COLUMNAS_PEDIDOS)
    return Response(
        content="\ufeff" + contenido,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=pedidos.csv"},
    )