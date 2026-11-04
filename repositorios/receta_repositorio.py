from repositorios.repositorio_base import RepositorioBase


class RecetaRepositorio(RepositorioBase):
    tabla = "receta"
    columnas = ["producto_id", "ingrediente_id", "cantidad"]

    def obtener_por_producto(self, producto_id):
        return self._consultar(
            """
            SELECT r.id, r.ingrediente_id, i.nombre AS ingrediente,
                i.unidad, r.cantidad
            FROM receta r
            JOIN ingredientes i ON i.id = r.ingrediente_id
            WHERE r.producto_id = ?
            ORDER BY i.nombre
            """,
            (producto_id,),
        )