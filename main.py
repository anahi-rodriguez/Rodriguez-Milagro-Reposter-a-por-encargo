from fastapi import Depends, FastAPI

from routers import auth, clientes, entregas, ingredientes, pedidos, productos, receta
from seguridad import obtener_usuario_actual

app = FastAPI(title="Repostería por encargo")

protegido = [Depends(obtener_usuario_actual)]

app.include_router(auth.router)
app.include_router(clientes.router, dependencies=protegido)
app.include_router(productos.router, dependencies=protegido)
app.include_router(ingredientes.router, dependencies=protegido)
app.include_router(receta.router, dependencies=protegido)
app.include_router(pedidos.router, dependencies=protegido)
app.include_router(entregas.router, dependencies=protegido)


@app.get("/")
def inicio():
    return {"mensaje": "API de Repostería por encargo funcionando"}