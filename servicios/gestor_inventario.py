class GestorInventario:
    def __init__(self, repo_pedidos):
        self.repo = repo_pedidos

    def necesidades(self, pedido_id):
        filas = self.repo.ingredientes_necesarios(pedido_id)
        for fila in filas:
            fila["alcanza"] = fila["existencia"] >= fila["necesario"]
        return filas

    def faltantes(self, pedido_id):
        return [
            {**f, "falta": round(f["necesario"] - f["existencia"], 3)}
            for f in self.necesidades(pedido_id)
            if not f["alcanza"]
        ]

    def verificar_disponibilidad(self, pedido_id):
        return not self.faltantes(pedido_id)

    def descontar_por_pedido(self, pedido_id):
        self.repo.confirmar_descontando(pedido_id, self.necesidades(pedido_id))