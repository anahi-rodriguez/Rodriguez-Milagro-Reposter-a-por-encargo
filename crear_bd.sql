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