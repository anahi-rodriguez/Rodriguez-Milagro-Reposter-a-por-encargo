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
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,
    tipo        TEXT NOT NULL CHECK (tipo IN ('pastel', 'cupcake', 'galleta', 'postre', 'otro')),
    precio_base REAL NOT NULL CHECK (precio_base > 0)
);

CREATE TABLE receta (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id     INTEGER NOT NULL,
    ingrediente_id  INTEGER NOT NULL,
    cantidad        REAL NOT NULL CHECK (cantidad > 0),
    UNIQUE (producto_id, ingrediente_id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
);

CREATE TABLE pedidos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id      INTEGER NOT NULL,
    fecha_pedido    TEXT NOT NULL,
    fecha_entrega   TEXT NOT NULL,
    direccion       TEXT NOT NULL,
    anticipo        REAL NOT NULL CHECK (anticipo > 0),
    total           REAL NOT NULL CHECK (total > 0),
    estado          TEXT NOT NULL DEFAULT 'pendiente'
            CHECK (estado IN ('pendiente', 'confirmado', 'en_preparacion', 'entregado', 'cancelado')),
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE detalle_pedido (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id       INTEGER NOT NULL,
    producto_id     INTEGER NOT NULL,
    cantidad        INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL NOT NULL CHECK (precio_unitario >= 0),
    personalizacion TEXT,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE usuarios (
    id              INTEGER PRIMARY KEy AUTOINCREMENT,
    username        TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    rol             TEXT NOT NULL CHECK (rol IN ('admin', 'empleado')),
    activo          INTEGER NOT NULL DEFAULT 1
);

INSERT INTO clientes (nombre, telefono, correo, direccion) VALUES
('Ana Martínez',     '9876-1234', 'ana.martinez@gmail.com',   'Col. Palmira, Tegucigalpa'),
('Carlos Mejía',     '9988-4521', 'carlos.mejia@gmail.com',   'Barrio Abajo, Comayagua'),
('Lucía Fernández',  '3345-7788', 'lucia.fernandez@gmail.com','Res. Los Pinos, Tegucigalpa'),
('José Alvarado',    '9455-3310', 'jose.alvarado@gmail.com',  'Col. Kennedy, Tegucigalpa'),
('María Reyes',      '8890-2267', 'maria.reyes@gmail.com',    'Barrio Arriba, Comayagua'),
('Pedro Castillo',   '3120-9984', 'pedro.castillo@gmail.com', 'Col. Miraflores, Tegucigalpa'),
('Sofía Ordóñez',    '9712-6543', 'sofia.ordonez@gmail.com',  'Col. San Miguel, Comayagua'),
('Daniel Rivera',    '3398-1175', 'daniel.rivera@gmail.com',  'Col. Loarque, Tegucigalpa'),
('Gabriela Núñez',   '8745-3021', 'gabriela.nunez@gmail.com', 'Col. Las Colinas, Tegucigalpa'),
('Héctor Lagos',     '9630-8812', 'hector.lagos@gmail.com',   'Barrio El Centro, Comayagua');

INSERT INTO ingredientes (nombre, unidad, existencia) VALUES
('Harina de trigo',      'kg',     50),
('Azúcar',               'kg',     40),
('Huevos',               'unidad', 120),
('Mantequilla',          'kg',     15),
('Leche',                'litro',  30),
('Chocolate',            'kg',     10),
('Vainilla',             'ml',     500),
('Polvo de hornear',     'g',      800),
('Crema para batir',     'litro',  12),
('Queso crema',          'kg',     8),
('Fresas',               'kg',     6),
('Colorante vegetal',    'ml',     300);

INSERT INTO productos (nombre, tipo, precio_base) VALUES
('Pastel de chocolate',          'pastel',  450.00),
('Pastel de vainilla',           'pastel',  400.00),
('Pastel tres leches',           'pastel',  500.00),
('Pastel de zanahoria',          'pastel',  480.00),
('Cheesecake de fresa',          'postre',  550.00),
('Cupcakes de vainilla (docena)','cupcake', 300.00),
('Cupcakes de chocolate (docena)','cupcake',320.00),
('Galletas decoradas (docena)',  'galleta', 250.00),
('Brownies (caja de 12)',        'postre',  280.00),
('Pastel de boda (3 pisos)',     'pastel', 2500.00);

INSERT INTO receta (producto_id, ingrediente_id, cantidad) VALUES
(1, 1, 0.5), (1, 2, 0.4), (1, 3, 4), (1, 4, 0.25), (1, 6, 0.3),
(2, 1, 0.5), (2, 2, 0.4), (2, 3, 4), (2, 4, 0.25), (2, 7, 10),
(3, 1, 0.4), (3, 2, 0.4), (3, 3, 5), (3, 5, 1),    (3, 9, 0.5),
(4, 1, 0.5), (4, 2, 0.4), (4, 3, 4), (4, 10, 0.2),
(5, 10, 0.8),(5, 11, 0.5),(5, 2, 0.2),(5, 3, 3),
(6, 1, 0.4), (6, 2, 0.3), (6, 3, 4), (6, 7, 10),
(7, 1, 0.4), (7, 2, 0.3), (7, 3, 4), (7, 6, 0.15),
(8, 1, 0.5), (8, 2, 0.25),(8, 4, 0.25),(8, 12, 10),
(9, 6, 0.3), (9, 4, 0.2), (9, 2, 0.3), (9, 3, 3),
(10, 1, 1.5),(10, 2, 1.2),(10, 3, 12),(10, 4, 0.75),(10, 9, 1);

INSERT INTO pedidos (cliente_id, fecha_pedido, fecha_entrega, direccion, anticipo, total, estado) VALUES
(1,  '2026-10-20', '2026-10-25', 'Col. Palmira, Tegucigalpa',      400.00,  750.00, 'entregado'),
(2,  '2026-10-22', '2026-10-26', 'Barrio Abajo, Comayagua',        250.00,  500.00, 'entregado'),
(3,  '2026-10-25', '2026-10-30', 'Res. Los Pinos, Tegucigalpa',   1500.00, 2500.00, 'confirmado'),
(4,  '2026-10-26', '2026-10-29', 'Col. Kennedy, Tegucigalpa',      325.00,  650.00, 'confirmado'),
(5,  '2026-10-27', '2026-11-01', 'Barrio Arriba, Comayagua',       300.00,  550.00, 'pendiente'),
(6,  '2026-10-27', '2026-10-30', 'Col. Miraflores, Tegucigalpa',   320.00,  640.00, 'pendiente'),
(7,  '2026-10-24', '2026-10-28', 'Col. San Miguel, Comayagua',     400.00,  760.00, 'en_preparacion'),
(8,  '2026-10-27', '2026-11-05', 'Col. Loarque, Tegucigalpa',      600.00, 1010.00, 'pendiente'),
(9,  '2026-10-15', '2026-10-20', 'Col. Las Colinas, Tegucigalpa',  300.00,  550.00, 'cancelado'),
(10, '2026-10-27', '2026-11-10', 'Barrio El Centro, Comayagua',    500.00, 1000.00, 'pendiente');

INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario, personalizacion) VALUES
(1,  1, 1, 450.00, 'Mensaje: Feliz cumpleaños Ana'),
(1,  6, 1, 300.00, NULL),
(2,  3, 1, 500.00, 'Decoración con flores rosadas'),
(3, 10, 1, 2500.00, 'Boda de Maria y Luis, tonos blanco y dorado'),
(4,  2, 1, 400.00, 'Decoración azul con tema de fútbol'),
(4,  8, 1, 250.00, 'Galletas con el logo del equipo'),
(5,  5, 1, 550.00, NULL),
(6,  7, 2, 320.00, 'Chispas de colores'),
(7,  4, 1, 480.00, NULL),
(7,  9, 1, 280.00, NULL),
(8,  1, 1, 450.00, 'Mensaje: Felicidades Graduado'),
(8,  9, 2, 280.00, NULL),
(9,  6, 1, 300.00, NULL),
(9,  8, 1, 250.00, 'Galletas de unicornio'),
(10, 3, 2, 500.00, 'Uno de ellos sin nueces');