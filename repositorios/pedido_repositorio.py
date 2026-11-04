from database import obtener_conexion
from repositorios.repositorio_base import RepositorioBase


class PedidoRepositorio(RepositorioBase):
    tabla = "pedidos"
    columnas = [
        "cliente_id", "fecha_pedido", "fecha_entrega",
        "direccion", "anticipo", "total", "estado",
    ]

    def crear_con_detalles(self, pedido, lineas):
        conexion = obtener_conexion()
        try:
            cursor = conexion.execute(
                """INSERT INTO pedidos (cliente_id, fecha_pedido, fecha_entrega,
                                        direccion, anticipo, total, estado)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                tuple(pedido[c] for c in self.columnas),
            )
            pedido_id = cursor.lastrowid
            for l in lineas:
                conexion.execute(
                    """INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad,
                                                   precio_unitario, personalizacion)
                       VALUES (?, ?, ?, ?, ?)""",
                    (pedido_id, l["producto_id"], l["cantidad"],
                     l["precio_unitario"], l["personalizacion"]),
                )
            conexion.commit()
            return pedido_id
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def obtener_detalles(self, pedido_id):
        return self._consultar(
            """SELECT d.id, d.producto_id, p.nombre AS producto, d.cantidad,
                    d.precio_unitario, d.personalizacion
            FROM detalle_pedido d
            JOIN productos p ON p.id = d.producto_id
            WHERE d.pedido_id = ?""",
            (pedido_id,),
        )

    def listar_por_estado(self, estado):
        return self._consultar("SELECT * FROM pedidos WHERE estado = ?", (estado,))

    def eliminar_con_detalles(self, pedido_id):
        conexion = obtener_conexion()
        try:
            conexion.execute("DELETE FROM detalle_pedido WHERE pedido_id = ?", (pedido_id,))
            cursor = conexion.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            conexion.commit()
            return cursor.rowcount > 0
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def ingredientes_necesarios(self, pedido_id):
        return self._consultar(
            """SELECT i.id AS ingrediente_id, i.nombre AS ingrediente, i.unidad,
                      ROUND(SUM(r.cantidad * d.cantidad), 3) AS necesario,
                    i.existencia
            FROM detalle_pedido d
            JOIN receta r ON r.producto_id = d.producto_id
            JOIN ingredientes i ON i.id = r.ingrediente_id
            WHERE d.pedido_id = ?
            GROUP BY i.id, i.nombre, i.unidad, i.existencia
            ORDER BY i.nombre""",
            (pedido_id,),
        )

    def confirmar_descontando(self, pedido_id, necesidades):
        conexion = obtener_conexion()
        try:
            for n in necesidades:
                conexion.execute(
                    "UPDATE ingredientes SET existencia = existencia - ? WHERE id = ?",
                    (n["necesario"], n["ingrediente_id"]),
                )
            conexion.execute(
                "UPDATE pedidos SET estado = 'confirmado' WHERE id = ?", (pedido_id,)
            )
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def entregas_del_dia(self, fecha):
        return self._consultar(
            """SELECT p.id, c.nombre AS cliente, c.telefono, p.direccion,
                    p.fecha_entrega, p.estado, p.total, p.anticipo,
                    ROUND(p.total - p.anticipo, 2) AS saldo
            FROM pedidos p
            JOIN clientes c ON c.id = p.cliente_id
            WHERE p.fecha_entrega = ? AND p.estado != 'cancelado'
            ORDER BY p.id""",
            (fecha,),
        )