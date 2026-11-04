from repositorios.repositorio_base import RepositorioBase


class IngredienteRepositorio(RepositorioBase):
    tabla = "ingredientes"
    columnas = ["nombre", "unidad", "existencia"]

    def buscar_por_nombre(self, texto):
        return self._consultar(
            "SELECT * FROM ingredientes WHERE nombre LIKE ?", (f"%{texto}%",)
        )

    def listar_sin_existencia(self):
        return self._consultar("SELECT * FROM ingredientes WHERE existencia = 0")