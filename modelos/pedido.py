from datetime import date, timedelta

PORCENTAJE_ANTICIPO = 0.5
DIAS_MINIMOS_ENTREGA = 2


class Pedido:
    def __init__(self, fecha_pedido: date, fecha_entrega: date, anticipo: float, total: float):
        self.fecha_pedido = fecha_pedido
        self.fecha_entrega = fecha_entrega
        self.anticipo = anticipo
        self.total = total

    @staticmethod
    def calcular_total(lineas):
        return round(sum(l["precio_unitario"] * l["cantidad"] for l in lineas), 2)

    def anticipo_minimo(self):
        return round(self.total * PORCENTAJE_ANTICIPO, 2)

    def validar_anticipo(self):
        return self.anticipo >= self.anticipo_minimo()

    def validar_fecha_entrega(self):
        return self.fecha_entrega >= self.fecha_pedido + timedelta(days=DIAS_MINIMOS_ENTREGA)