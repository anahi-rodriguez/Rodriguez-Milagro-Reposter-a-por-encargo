import csv
import io


def generar_csv(filas, columnas):
    salida = io.StringIO()
    escritor = csv.DictWriter(salida, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(filas)
    return salida.getvalue()