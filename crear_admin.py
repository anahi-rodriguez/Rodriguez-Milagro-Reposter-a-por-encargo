import getpass

from repositorios.usuario_repositorio import UsuarioRepositorio
from seguridad import encriptar_password

repo = UsuarioRepositorio()

username = input("Usuario: ").strip()
password = getpass.getpass("Contraseña: ")

if repo.obtener_por_username(username):
    print("Ese usuario ya existe")
    raise SystemExit

repo.crear({
    "username": username,
    "password_hash": encriptar_password(password),
    "rol": "admin",
    "activo": 1,
})
print("Administrador creado")