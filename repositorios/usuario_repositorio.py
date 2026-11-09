from repositorios.repositorio_base import RepositorioBase


class UsuarioRepositorio(RepositorioBase):
    tabla = "usuarios"
    columnas = ["username", "password_hash", "rol", "activo"]

    def obtener_por_username(self, username):
        filas = self._consultar(
            "SELECT * FROM usuarios WHERE username = ?", (username,)
        )
        return filas[0] if filas else None