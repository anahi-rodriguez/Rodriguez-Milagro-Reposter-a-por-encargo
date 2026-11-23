from datetime import date, timedelta


def datos_pedido(**cambios):
    datos = {
        "cliente_id": 1,
        "fecha_entrega": (date.today() + timedelta(days=10)).isoformat(),
        "direccion": "Col. Palmira, Tegucigalpa",
        "anticipo": 250,
        "detalles": [{"producto_id": 1, "cantidad": 1}],
    }
    datos.update(cambios)
    return datos


# ---------- Seguridad ----------
def test_login_correcto_devuelve_token(cliente):
    r = cliente.post("/auth/login", data={"username": "tester", "password": "clave123"})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"
    assert r.json()["access_token"]


def test_login_con_clave_incorrecta_da_401(cliente):
    r = cliente.post("/auth/login", data={"username": "tester", "password": "mala"})
    assert r.status_code == 401


def test_endpoint_protegido_sin_token_da_401(cliente):
    assert cliente.get("/clientes/").status_code == 401


# ---------- CRUD ----------
def test_listar_clientes_devuelve_los_10_de_prueba(api):
    r = api.get("/clientes/")
    assert r.status_code == 200
    assert len(r.json()) == 10


def test_cliente_inexistente_da_404(api):
    assert api.get("/clientes/999").status_code == 404


def test_borrar_cliente_con_pedidos_da_400(api):
    r = api.delete("/clientes/1")
    assert r.status_code == 400


# ---------- Reglas de negocio ----------
def test_pedido_con_anticipo_menor_al_50_da_400(api):
    r = api.post("/pedidos/", json=datos_pedido(anticipo=100))
    assert r.status_code == 400
    assert "50 %" in r.json()["detail"]


def test_pedido_con_entrega_en_menos_de_2_dias_da_400(api):
    manana = (date.today() + timedelta(days=1)).isoformat()
    r = api.post("/pedidos/", json=datos_pedido(fecha_entrega=manana))
    assert r.status_code == 400


def test_pedido_valido_calcula_el_total(api):
    r = api.post("/pedidos/", json=datos_pedido())
    assert r.status_code == 201
    assert r.json()["total"] == 450
    assert r.json()["estado"] == "pendiente"


def test_confirmar_pedido_sin_ingredientes_da_400(api):
    # 13 cheesecakes necesitan más fresas y queso crema de los que hay
    creado = api.post(
        "/pedidos/",
        json=datos_pedido(anticipo=3575, detalles=[{"producto_id": 5, "cantidad": 13}]),
    )
    assert creado.status_code == 201
    r = api.put(f"/pedidos/{creado.json()['id']}/confirmar")
    assert r.status_code == 400
    assert "faltan ingredientes" in r.json()["detail"]


def test_confirmar_pedido_descuenta_el_inventario(api):
    r = api.put("/pedidos/5/confirmar")
    assert r.status_code == 200
    assert r.json()["estado"] == "confirmado"
    fresas = api.get("/ingredientes/11").json()
    assert fresas["existencia"] == 5.5

def test_reporte_de_ventas_con_datos_de_prueba(api):
    r = api.get("/reportes/ventas")
    assert r.status_code == 200
    datos = r.json()
    assert datos["total_pedidos"] == 10
    assert datos["ventas_total"] == 8360
    assert datos["saldo_por_cobrar"] == 3765


def test_exportar_pedidos_csv(api):
    r = api.get("/reportes/pedidos/csv")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")
    assert len(r.text.strip().splitlines()) == 11  # encabezado + 10 pedidos

def test_crear_respaldo_genera_un_archivo(cliente, tmp_path, monkeypatch):
    from servicios import respaldo

    monkeypatch.setattr(respaldo, "CARPETA", tmp_path / "respaldos")
    nombre = respaldo.crear_respaldo()
    assert (tmp_path / "respaldos" / nombre).exists()