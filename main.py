from fastapi import FastAPI
from routers import clientes 
from routers import clientes, productos

app = FastAPI(title="Reposteria por encargo")
app.include_router(clientes.router)  

@app.get("/")
def inicio():
    return {"mensaje": "API de Reposteria por encargo funcionando"}