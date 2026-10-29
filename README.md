# Rodriguez-Milagro-Reposter-a-por-encargo

# Repostería por encargo

Sistema para gestionar los pedidos personalizados de una repostería: clientes, productos, recetas, control de inventario de ingredientes y entregas.

- **Estudiante:** Milagro Anahi Rodriguez Rodriguez
- **Asignatura:** Programación III (IS-151) · Ing. Elias Emilio Flores Domínguez, MSc.
- **Período:** IV PAC 2026

## Problema que resuelve

Una repostería recibe pedidos de pasteles por mensaje y a veces olvida una entrega. El sistema registra cada pedido con su anticipo y fecha de entrega, y controla que haya ingredientes suficientes antes de confirmarlo.

## Reglas de negocio

- El pedido requiere al menos 50 % de anticipo.
- La fecha de entrega es al menos 2 días después del pedido.
- No se confirma un pedido si faltan ingredientes.

## Tecnologías

Python, FastAPI, SQLite y Visual Studio Code.

## Base de datos

7 tablas: `clientes`, `productos`, `ingredientes`, `receta`, `pedidos`, `detalle_pedido` y `usuarios`.

![Diagrama ER](docs/diagrama_er.png)

## Diagrama UML de clases

![Diagrama UML](docs/diagrama_uml.png)

Los archivos editables están en `docs/` (formato draw.io).

## Arquitectura en capas

| Capa | Carpeta |
|---|---|
| Presentación (dashboard HTML/JS) | `static/` |
| API (endpoints y validación) | `routers/`, `esquemas.py` |
| Lógica de negocio | `modelos/`, `servicios/` |
| Acceso a datos (Repository) | `repositorios/` |
| Conexión | `database.py` |

## Cómo ejecutar

Crear la base de datos con datos de prueba:

```
python -c "import sqlite3; c=sqlite3.connect('reposteria.db'); c.executescript(open('crear_bd.sql', encoding='utf-8').read())"
```

*(Las instrucciones para iniciar la API, el dashboard y las pruebas se agregarán conforme avance el proyecto.)*

## Avance

- [x] Diseño: repositorio, diagrama ER, UML y `crear_bd.sql`
- [ ] Avance 1: capas y CRUD de 2 tablas
- [ ] Proyecto 2: CRUD completo, reglas de negocio, login y pruebas
- [ ] Avance 2: dashboard
- [ ] Avance 3: reportes, CSV y respaldo
- [ ] Proyecto final