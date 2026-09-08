-- ============================================================
-- PRACTICA 05
-- CARGA DE DATOS - MYSQL
-- Base de datos: negocios
-- ============================================================

USE negocios;

-- ============================================================
-- LIMPIAR LOS DATOS EXISTENTES
-- ============================================================

-- Desactivar temporalmente el modo seguro
SET SQL_SAFE_UPDATES = 0;

-- Eliminar registros respetando las llaves foráneas
DELETE FROM detalle_ventas;
DELETE FROM ventas;
DELETE FROM productos;
DELETE FROM clientes;


-- ============================================================
-- REINICIAR AUTO_INCREMENT
-- ============================================================

-- La siguiente venta volverá a tener id_venta = 1
ALTER TABLE ventas AUTO_INCREMENT = 1;

-- El siguiente detalle volverá a tener id_detalle = 1
ALTER TABLE detalle_ventas AUTO_INCREMENT = 1;


-- Volver a activar modo seguro
SET SQL_SAFE_UPDATES = 1;


-- ============================================================
-- 1. CLIENTES
-- ============================================================

INSERT INTO clientes
    (id_cliente, nombre, telefono, correo, direccion)
VALUES
    ('CLI0000000001', 'Ana Martinez',   '6181000001',
     'ana@email.com', 'Durango, Dgo.'),

    ('CLI0000000002', 'Carlos Ramirez', '6181000002',
     'carlos@email.com', 'Durango, Dgo.'),

    ('CLI0000000003', 'Laura Hernandez','6181000003',
     'laura@email.com', 'Gomez Palacio, Dgo.'),

    ('CLI0000000004', 'Jose Rodriguez', '6181000004',
     'jose@email.com', 'Lerdo, Dgo.'),

    ('CLI0000000005', 'Maria Lopez',    '6181000005',
     'maria@email.com', 'Durango, Dgo.');


-- ============================================================
-- 2. PRODUCTOS
-- ============================================================

INSERT INTO productos
    (id_producto, nombre, descripcion, precio, existencia)
VALUES
    ('PROD0000000000000001', 'Teclado',
     'Teclado USB', 350.00, 50),

    ('PROD0000000000000002', 'Mouse',
     'Mouse optico USB', 200.00, 60),

    ('PROD0000000000000003', 'Monitor',
     'Monitor LED 24 pulgadas', 3200.00, 20),

    ('PROD0000000000000004', 'Memoria USB',
     'Memoria USB 64 GB', 250.00, 100),

    ('PROD0000000000000005', 'Audifonos',
     'Audifonos con microfono', 600.00, 40);


-- ============================================================
-- 3. VENTAS
-- ============================================================

INSERT INTO ventas
    (id_cliente, total)
VALUES
    ('CLI0000000001', 0),
    ('CLI0000000002', 0),
    ('CLI0000000003', 0),
    ('CLI0000000004', 0),
    ('CLI0000000005', 0);


-- ============================================================
-- 4. DETALLE DE VENTAS
-- ============================================================

-- VENTA 1
INSERT INTO detalle_ventas
    (id_venta, id_producto, cantidad, precio_unitario, subtotal)
VALUES
    (1, 'PROD0000000000000001', 2, 350.00, 700.00),
    (1, 'PROD0000000000000002', 1, 200.00, 200.00);


-- VENTA 2
INSERT INTO detalle_ventas
    (id_venta, id_producto, cantidad, precio_unitario, subtotal)
VALUES
    (2, 'PROD0000000000000003', 1, 3200.00, 3200.00),
    (2, 'PROD0000000000000004', 2, 250.00, 500.00);


-- VENTA 3
INSERT INTO detalle_ventas
    (id_venta, id_producto, cantidad, precio_unitario, subtotal)
VALUES
    (3, 'PROD0000000000000005', 1, 600.00, 600.00),
    (3, 'PROD0000000000000002', 2, 200.00, 400.00),
    (3, 'PROD0000000000000004', 1, 250.00, 250.00);


-- VENTA 4
INSERT INTO detalle_ventas
    (id_venta, id_producto, cantidad, precio_unitario, subtotal)
VALUES
    (4, 'PROD0000000000000001', 1, 350.00, 350.00),
    (4, 'PROD0000000000000005', 2, 600.00, 1200.00);


-- VENTA 5
INSERT INTO detalle_ventas
    (id_venta, id_producto, cantidad, precio_unitario, subtotal)
VALUES
    (5, 'PROD0000000000000003', 1, 3200.00, 3200.00),
    (5, 'PROD0000000000000002', 1, 200.00, 200.00),
    (5, 'PROD0000000000000004', 2, 250.00, 500.00);


-- ============================================================
-- 5. CALCULAR TOTAL DE CADA VENTA
-- ============================================================

UPDATE ventas v
SET total = (
    SELECT SUM(d.subtotal)
    FROM detalle_ventas d
    WHERE d.id_venta = v.id_venta
)
WHERE v.id_venta > 0;


-- ============================================================
-- 6. VERIFICAR RESULTADOS
-- ============================================================

SELECT
    v.id_venta,
    c.nombre AS cliente,
    v.total
FROM ventas v
INNER JOIN clientes c
    ON v.id_cliente = c.id_cliente
ORDER BY v.id_venta;


-- ============================================================
-- 7. COMPROBAR TOTALES
-- La diferencia debe ser 0.00
-- ============================================================

SELECT
    v.id_venta,
    v.total AS total_venta,
    SUM(d.subtotal) AS suma_subtotales,
    v.total - SUM(d.subtotal) AS diferencia
FROM ventas v
INNER JOIN detalle_ventas d
    ON v.id_venta = d.id_venta
GROUP BY
    v.id_venta,
    v.total
ORDER BY v.id_venta;