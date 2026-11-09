import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from repositorios.usuario_repositorio import UsuarioRepositorio

CLAVE_SECRETA = os.getenv(
    "CLAVE_SECRETA", "clave-secreta-de-desarrollo-cambiar-antes-de-entregar-0123"
)
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 60

esquema_oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")
repo_usuarios = UsuarioRepositorio()


def encriptar_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def crear_token(username: str, rol: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    datos = {"sub": username, "rol": rol, "exp": expira}
    return jwt.encode(datos, CLAVE_SECRETA, algorithm=ALGORITMO)


def obtener_usuario_actual(token: str = Depends(esquema_oauth)):
    error = HTTPException(
        status_code=401,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
    except jwt.PyJWTError:
        raise error

    usuario = repo_usuarios.obtener_por_username(datos.get("sub"))
    if usuario is None or not usuario["activo"]:
        raise error
    return usuario