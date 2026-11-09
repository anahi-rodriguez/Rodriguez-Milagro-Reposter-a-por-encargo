from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from esquemas import TokenSalida
from repositorios.usuario_repositorio import UsuarioRepositorio
from seguridad import crear_token, verificar_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])
repo = UsuarioRepositorio()


@router.post("/login", response_model=TokenSalida)
def login(formulario: OAuth2PasswordRequestForm = Depends()):
    usuario = repo.obtener_por_username(formulario.username)
    if (
        usuario is None
        or not usuario["activo"]
        or not verificar_password(formulario.password, usuario["password_hash"])
    ):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = crear_token(usuario["username"], usuario["rol"])
    return {"access_token": token, "token_type": "bearer"}