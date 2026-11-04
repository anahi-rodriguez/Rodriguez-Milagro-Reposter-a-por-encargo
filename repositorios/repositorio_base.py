from database import obtener_conexion


class RepositorioBase:
    tabla = ""
    columnas = []  # columnas editables (sin el id)

    def _consultar(self, sql, parametros=()):
        conexion = obtener_conexion()
        try:
            filas = conexion.execute(sql, parametros).fetchall()
            return [dict(fila) for fila in filas]
        finally:
            conexion.close()

    def _modificar(self, sql, parametros=()):
        conexion = obtener_conexion()
        try:
            cursor = conexion.execute(sql, parametros)
            conexion.commit()
            return cursor.lastrowid, cursor.rowcount
        finally:
            conexion.close()

    def obtener_todos(self):
        return self._consultar(f"SELECT * FROM {self.tabla}")

    def obtener_por_id(self, id):
        filas = self._consultar(f"SELECT * FROM {self.tabla} WHERE id = ?", (id,))
        return filas[0] if filas else None

    def crear(self, datos):
        nombres = ", ".join(self.columnas)
        marcadores = ", ".join("?" for _ in self.columnas)
        valores = [datos[c] for c in self.columnas]
        nuevo_id, _ = self._modificar(
            f"INSERT INTO {self.tabla} ({nombres}) VALUES ({marcadores})", valores
        )
        return nuevo_id

    def actualizar(self, id, datos):
        asignaciones = ", ".join(f"{c} = ?" for c in self.columnas)
        valores = [datos[c] for c in self.columnas] + [id]
        _, filas = self._modificar(
            f"UPDATE {self.tabla} SET {asignaciones} WHERE id = ?", valores
        )
        return filas > 0

    def eliminar(self, id):
        _, filas = self._modificar(f"DELETE FROM {self.tabla} WHERE id = ?", (id,))
        return filas > 0