from datetime import date

from fastapi import APIRouter, HTTPException

from esquemas import PedidoActualizar, PedidoDetalleSalida, PedidoEntrada, PedidoSalida
from modelos.pedido import Pedido
from repositorios.cliente_repositorio import ClienteRepositorio
from repositorios.pedido_repositorio import PedidoRepositorio
from repositorios.producto_repositorio import ProductoRepositorio

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
repo = PedidoRepositorio()
repo_clientes = ClienteRepositorio()
repo_productos = ProductoRepositorio()


def pedido_completo(pedido_id):
    pedido = repo.obtener_por_id(pedido_id)
    pedido["detalles"] = repo.obtener_detalles(pedido_id)
    return pedido


def validar_reglas(pedido: Pedido):
    if not pedido.validar_fecha_entrega():
        raise HTTPException(
            status_code=400,
            detail="La fecha de entrega debe ser al menos 2 días después del pedido",
        )
    if not pedido.validar_anticipo():
        raise HTTPException(
            status_code=400,
            detail=f"El anticipo debe ser al menos el 50 % del total (mínimo: L {pedido.anticipo_minimo():.2f})",
        )


@router.get("/", response_model=list[PedidoSalida])
def listar(estado: str | None = None):
    if estado:
        return repo.listar_por_estado(estado)
    return repo.obtener_todos()


@router.get("/{id}", response_model=PedidoDetalleSalida)
def obtener(id: int):
    if repo.obtener_por_id(id) is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido_completo(id)


@router.post("/", response_model=PedidoDetalleSalida, status_code=201)
def crear(datos: PedidoEntrada):
    if repo_clientes.obtener_por_id(datos.cliente_id) is None:
        raise HTTPException(status_code=400, detail="El cliente no existe")

    lineas = []
    for d in datos.detalles:
        producto = repo_productos.obtener_por_id(d.producto_id)
        if producto is None:
            raise HTTPException(status_code=400, detail=f"El producto {d.producto_id} no existe")
        lineas.append({
            "producto_id": d.producto_id,
            "cantidad": d.cantidad,
            "precio_unitario": producto["precio_base"],
            "personalizacion": d.personalizacion,
        })

    hoy = date.today()
    total = Pedido.calcular_total(lineas)
    validar_reglas(Pedido(hoy, datos.fecha_entrega, datos.anticipo, total))

    nuevo_id = repo.crear_con_detalles(
        {
            "cliente_id": datos.cliente_id,
            "fecha_pedido": hoy.isoformat(),
            "fecha_entrega": datos.fecha_entrega.isoformat(),
            "direccion": datos.direccion,
            "anticipo": datos.anticipo,
            "total": total,
            "estado": "pendiente",
        },
        lineas,
    )
    return pedido_completo(nuevo_id)


@router.put("/{id}", response_model=PedidoDetalleSalida)
def actualizar(id: int, datos: PedidoActualizar):
    existente = repo.obtener_por_id(id)
    if existente is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if existente["estado"] in ("entregado", "cancelado"):
        raise HTTPException(
            status_code=400, detail="No se puede modificar un pedido entregado o cancelado"
        )

    validar_reglas(Pedido(
        date.fromisoformat(existente["fecha_pedido"]),
        datos.fecha_entrega, datos.anticipo, existente["total"],
    ))

    repo.actualizar(id, {
        **existente,
        "fecha_entrega": datos.fecha_entrega.isoformat(),
        "direccion": datos.direccion,
        "anticipo": datos.anticipo,
    })
    return pedido_completo(id)


@router.delete("/{id}")
def eliminar(id: int):
    if not repo.eliminar_con_detalles(id):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado"}