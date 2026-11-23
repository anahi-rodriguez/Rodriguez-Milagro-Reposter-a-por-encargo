from fastapi import Depends, FastAPI

from routers import auth, clientes, entregas, ingredientes, pedidos, productos, receta, respaldos
from seguridad import obtener_usuario_actual
from routers import reportes
from contextlib import asynccontextmanager

from servicios.respaldo import HiloRespaldo

@asynccontextmanager
async def lifespan(app):
    hilo = HiloRespaldo(intervalo_segundos=300)
    hilo.start()
    yield
    hilo.detener()


app = FastAPI(title="Repostería por encargo", lifespan=lifespan)

protegido = [Depends(obtener_usuario_actual)]

app.include_router(auth.router)
app.include_router(clientes.router, dependencies=protegido)
app.include_router(productos.router, dependencies=protegido)
app.include_router(ingredientes.router, dependencies=protegido)
app.include_router(receta.router, dependencies=protegido)
app.include_router(pedidos.router, dependencies=protegido)
app.include_router(entregas.router, dependencies=protegido)
app.include_router(reportes.router, dependencies=protegido)
app.include_router(respaldos.router, dependencies=protegido)


@app.get("/")
def inicio():
    return {"mensaje": "API de Repostería por encargo funcionando"}