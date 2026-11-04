from repositorios.repositorio_base import RepositorioBase


class ClienteRepositorio(RepositorioBase):
    tabla = "clientes"
    columnas = ["nombre", "telefono", "correo", "direccion"]

    def buscar_por_nombre(self, texto):
        return self._consultar(
            "SELECT * FROM clientes WHERE nombre LIKE ?", (f"%{texto}%",)
        )