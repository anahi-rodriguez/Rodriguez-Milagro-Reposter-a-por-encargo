from collections import Counter, defaultdict


class ServicioReportes:
    def __init__(self, repo_pedidos, repo_clientes):
        self.repo_pedidos = repo_pedidos
        self.repo_clientes = repo_clientes

    def resumen(self):
        pedidos = self.repo_pedidos.obtener_todos()
        validos = [p for p in pedidos if p["estado"] != "cancelado"]

        # Counter: cuenta cuántos pedidos hay en cada estado
        por_estado = Counter(p["estado"] for p in pedidos)

        ventas_total = round(sum(p["total"] for p in validos), 2)
        anticipos = round(sum(p["anticipo"] for p in validos), 2)

        # defaultdict: suma lo comprado por cada cliente
        nombres = {c["id"]: c["nombre"] for c in self.repo_clientes.obtener_todos()}
        por_cliente = defaultdict(float)
        for p in validos:
            por_cliente[nombres[p["cliente_id"]]] += p["total"]
        mejores_clientes = sorted(por_cliente.items(), key=lambda x: x[1], reverse=True)[:5]

        # Counter otra vez: unidades vendidas por producto
        unidades = Counter()
        for d in self.repo_pedidos.detalles_con_producto():
            unidades[d["producto"]] += d["cantidad"]

        return {
            "total_pedidos": len(pedidos),
            "pedidos_por_estado": dict(por_estado),
            "ventas_total": ventas_total,
            "anticipos_cobrados": anticipos,
            "saldo_por_cobrar": round(ventas_total - anticipos, 2),
            "mejores_clientes": [
                {"cliente": n, "total": round(t, 2)} for n, t in mejores_clientes
            ],
            "productos_mas_vendidos": [
                {"producto": n, "unidades": u} for n, u in unidades.most_common(5)
            ],
        }