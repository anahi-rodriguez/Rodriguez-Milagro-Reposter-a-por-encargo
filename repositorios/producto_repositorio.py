from repositorios.repositorio_base import RepositorioBase


class ProductoRepositorio(RepositorioBase):
    tabla = "productos"
    columnas = ["nombre", "tipo", "precio_base"]

    def buscar_por_nombre(self, texto):
        return self._consultar(
            "SELECT * FROM productos WHERE nombre LIKE ?", (f"%{texto}%",)
        )

    def listar_por_tipo(self, tipo):
        return self._consultar("SELECT * FROM productos WHERE tipo = ?", (tipo,))