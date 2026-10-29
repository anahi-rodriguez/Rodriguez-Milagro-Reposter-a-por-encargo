from fastapi import FastAPI

app = FastAPI(title="Reposteria por encargo")

@app.get("/")
def inicio():
    return {"mensaje": "API de Reposteria por encargo funcionando"}