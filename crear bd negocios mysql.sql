-- Crear BD negocios
drop database if exists negocios;
create database negocios; -- Si ya existe borrar BD

-- Cargar negocios
USE negocios;
-- =====================================================
-- TABLA: clientes
-- =====================================================

CREATE TABLE clientes (
    id_cliente CHAR(13) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100),
    direccion VARCHAR(150),

    CONSTRAINT pk_clientes
        PRIMARY KEY (id_cliente)
);
-- =====================================================
-- TABLA: productos
-- =====================================================

CREATE TABLE productos (
    id_producto CHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200),
    precio DECIMAL(10,2) NOT NULL,
    existencia INT NOT NULL,

    CONSTRAINT pk_productos
        PRIMARY KEY (id_producto)
);
-- =====================================================
-- TABLA: ventas
-- =====================================================
CREATE TABLE ventas (
    id_venta INT NOT NULL AUTO_INCREMENT,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente CHAR(13) NOT NULL,
    total DECIMAL(10,2),


    CONSTRAINT pk_ventas
        PRIMARY KEY (id_venta),

    CONSTRAINT fk_ventas_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);


-- =====================================================
-- TABLA: detalle_ventas
-- =====================================================

CREATE TABLE detalle_ventas (
    id_detalle INT NOT NULL AUTO_INCREMENT,
    id_venta INT NOT NULL,
    id_producto CHAR(20) NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2),

    CONSTRAINT pk_detalle_ventas
        PRIMARY KEY (id_detalle),

    CONSTRAINT fk_detalle_ventas
        FOREIGN KEY (id_venta)
        REFERENCES ventas(id_venta),

    CONSTRAINT fk_detalle_productos
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
);


