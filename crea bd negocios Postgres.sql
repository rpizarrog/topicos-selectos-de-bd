CREATE TABLE clientes (
    id_cliente CHAR(13) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100),
    direccion VARCHAR(150),

    CONSTRAINT pk_clientes
        PRIMARY KEY (id_cliente)
);


CREATE TABLE productos (
    id_producto CHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200),
    precio NUMERIC(10,2) NOT NULL,
    existencia INTEGER NOT NULL,

    CONSTRAINT pk_productos
        PRIMARY KEY (id_producto)
);


CREATE TABLE ventas (
    id_venta INTEGER GENERATED ALWAYS AS IDENTITY,
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cliente CHAR(13) NOT NULL,
    total NUMERIC(10,2),

    CONSTRAINT pk_ventas
        PRIMARY KEY (id_venta),

    CONSTRAINT fk_ventas_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
);


CREATE TABLE detalle_ventas (
    id_detalle INTEGER GENERATED ALWAYS AS IDENTITY,
    id_venta INTEGER NOT NULL,
    id_producto CHAR(20) NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2),

    CONSTRAINT pk_detalle_ventas
        PRIMARY KEY (id_detalle),

    CONSTRAINT fk_detalle_ventas
        FOREIGN KEY (id_venta)
        REFERENCES ventas(id_venta),

    CONSTRAINT fk_detalle_productos
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
);