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