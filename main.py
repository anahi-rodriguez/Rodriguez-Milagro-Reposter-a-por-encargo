from fastapi import FastAPI
from routers import clientes 
from routers import clientes, productos
from routers import clientes, productos, ingredientes
from routers import clientes, productos, ingredientes, receta

app = FastAPI(title="Reposteria por encargo")
app.include_router(clientes.router)  
app.include_router(ingredientes.router)
app.include_router(receta.router)

@app.get("/")
def inicio():
    return {"mensaje": "API de Reposteria por encargo funcionando"}