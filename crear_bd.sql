PRAGMA foreing_key = ON;

DROP TABLE IF EXISTS detalle_pedido;
DROP TABLE IF EXISTS receta;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS ingredientes;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE clientes(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL,
    telefono    TEXT NOT NULL,
    correo      TEXT UNIQUE,
    direccion   TEXT
);

CREATE TABLE ingredientes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,  
    unidad      TEXT NOT NULL,
    existencia  REAL NOT NULL CHECK (existencia >= 0)
);

CREATE TABLE productos (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre  TEXT NOT NULL UNIQUE,
    tipo    TEXT NOT NULL CHECK (tipo IN ('Pastel', 'cupcake', 'Galleta', 'Postre', 'Otro')),
    precio_base REAL NOT NULL CHECK (precio_base > 0)
);

CREATE TABLE receta (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    ingrediente_id INTEGER NOT NULL,
    cantidad REAL NOT NULL CHECK (cantidad > 0),
    UNIQUE (producto_id, ingrediente_id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id  INTEGER NOT NULL,
    fecha_pedido TEXT NOT NULL,
    fecha_entrega TEXT NOT NULL,
    direccion TEXT NOT NULL,
    anticipo REAL NOT NULL CHECK (anticipo > 0),
    total REAL NOT NULL CHECK (total > 0),
    estado TEXT NOT NULL DEFAULT 'pendiente'
            CHECK (estado IN ('pendiente', 'confirmado', 'en_preparacion', 'entregado', 'cancelado')),
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE detalle_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL NOT NULL CHECK (precio_unitario >= 0),
    personalizacion TEXT,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEy AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('admin', 'empleado')),
    activo  INTEGER NOT NULL DEFAULT 1
);