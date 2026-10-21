# Sistema Multibase: Migración de MySQL a SQLite

## Descripción

Proyecto de la práctica de **Sistemas Multibase de Datos** para crear
mediante Python la base `negocios` en SQLite y migrar hacia ella los
registros existentes en MySQL, conservando una estructura lógica
equivalente.

## Objetivo

Crear y configurar mediante Python la base de datos `negocios` en SQLite
y desarrollar un proceso de migración que extraiga los registros de
MySQL y los inserte en las tablas correspondientes de SQLite,
conservando llaves primarias, llaves foráneas y correspondencia de
datos.

## Estructura

``` text
multibase/
├── CSQLite.py
├── CMigracion.py
├── ProbarSQLite.py
├── ProbarMigracion.py
├── README.md
└── datos/
    └── negocios.db
```

## Tablas

-   `clientes`
-   `productos`
-   `ventas`
-   `detalle_ventas`

Orden de migración: **clientes → productos → ventas → detalle_ventas**.

# CSQLite.py --- clase SQLite

## `__init__(self)`

Inicializa `carpeta`, ruta de `negocios.db`, conexión y cursor.

## `f_crear_bd(self)`

Crea la carpeta `datos` si no existe, abre o crea `datos/negocios.db`,
crea el cursor y activa:

``` sql
PRAGMA foreign_keys = ON;
```

## `f_crear_tablas(self)`

Crea `clientes`, `productos`, `ventas` y `detalle_ventas` con una
estructura equivalente a MySQL.

Relaciones:

``` text
ventas.id_cliente → clientes.id_cliente
detalle_ventas.id_venta → ventas.id_venta
detalle_ventas.id_producto → productos.id_producto
```

## `f_mostrar_estructura(self)`

Consulta la estructura de cada tabla mediante:

``` sql
PRAGMA table_info(nombre_tabla);
```

## `f_cerrar(self)`

Cierra la conexión SQLite.

# CMigracion.py --- clase Migracion

Administra las conexiones con MySQL y SQLite y realiza la transferencia
de registros.

Dependencias:

``` python
import mysql.connector
import sqlite3
import os
```

## Métodos MySQL

### `f_conectar_mysql(self, usuario, contrasenia, bd)`

Conecta con MySQL y crea el cursor.

### `f_leer_clientes_mysql(self)`

Lee `id_cliente`, `nombre`, `telefono`, `correo` y `direccion`.

### `f_leer_productos_mysql(self)`

Lee `id_producto`, `nombre`, `descripcion`, `precio` y `existencia`.

### `f_leer_ventas_mysql(self)`

Lee `id_venta`, `fecha`, `id_cliente` y `total`.

### `f_leer_detalle_ventas_mysql(self)`

Lee `id_detalle`, `id_venta`, `id_producto`, `cantidad`,
`precio_unitario` y `subtotal`.

### `f_cerrar_mysql(self)`

Cierra cursor y conexión MySQL.

## Métodos SQLite

### `f_conectar_sqlite(self)`

Abre `datos/negocios.db`, crea el cursor y activa las llaves foráneas.

### `f_agregar_clientes_sqlite(self, clientes)`

Inserta en SQLite los clientes recuperados desde MySQL mediante
`executemany()`.

### `f_agregar_productos_sqlite(self, productos)`

Inserta los productos. Los valores `DECIMAL`, como `precio`, se
convierten a `float` cuando es necesario.

### `f_agregar_ventas_sqlite(self, ventas)`

Inserta las ventas conservando el `id_venta` original. Convierte `total`
de `Decimal` a `float` cuando corresponde.

### `f_agregar_detalle_ventas_sqlite(self, detalle_ventas)`

Inserta `detalle_ventas`, convirtiendo `precio_unitario` y `subtotal` de
`Decimal` a `float` cuando es necesario.

### `f_cerrar_sqlite(self)`

Cierra cursor y conexión SQLite.

# Flujo de migración

``` text
MySQL negocios
      │
      │ SELECT + fetchall()
      ▼
CMigracion.py
      │
      │ listas de tuplas
      ▼
    Python
      │
      │ executemany()
      ▼
SQLite negocios.db
```

Correspondencia de métodos:

``` text
f_leer_clientes_mysql()       → f_agregar_clientes_sqlite()
f_leer_productos_mysql()      → f_agregar_productos_sqlite()
f_leer_ventas_mysql()         → f_agregar_ventas_sqlite()
f_leer_detalle_ventas_mysql() → f_agregar_detalle_ventas_sqlite()
```

# Instalación

Python incluye `sqlite3`. Para MySQL:

``` bash
python -m pip install mysql-connector-python
```

# Ejemplo general

``` python
from CMigracion import Migracion

migracion = Migracion()

migracion.f_conectar_mysql(usuario, contrasenia, "negocios")

clientes = migracion.f_leer_clientes_mysql()
productos = migracion.f_leer_productos_mysql()
ventas = migracion.f_leer_ventas_mysql()
detalle_ventas = migracion.f_leer_detalle_ventas_mysql()

migracion.f_cerrar_mysql()

migracion.f_conectar_sqlite()

migracion.f_agregar_clientes_sqlite(clientes)
migracion.f_agregar_productos_sqlite(productos)
migracion.f_agregar_ventas_sqlite(ventas)
migracion.f_agregar_detalle_ventas_sqlite(detalle_ventas)

migracion.f_cerrar_sqlite()
```

# Verificación

Comparar el número de registros de cada tabla en MySQL y SQLite:

``` text
Tabla             MySQL      SQLite
-----------------------------------
clientes            n           n
productos           n           n
ventas              n           n
detalle_ventas      n           n
```

Desde `sqlite3.exe`:

``` text
.tables
.schema clientes
.schema productos
.schema ventas
.schema detalle_ventas
```

Consultas:

``` sql
SELECT * FROM clientes;
SELECT * FROM productos;
SELECT * FROM ventas;
SELECT * FROM detalle_ventas;
```

# Consideraciones

-   Las tablas SQLite deben existir antes de migrar.
-   Las llaves foráneas se activan con `PRAGMA foreign_keys = ON`.
-   Se migran primero `clientes` y `productos`, después `ventas` y al
    final `detalle_ventas`.
-   Los valores `DECIMAL` de MySQL pueden requerir conversión a `float`.
-   Se conservan los identificadores originales para mantener las
    relaciones.
-   Si se vuelve a insertar una llave primaria existente, SQLite puede
    producir un error `PRIMARY KEY`/`UNIQUE`.

# Resultado

``` text
MySQL                           SQLite
negocios                        negocios.db
│                               │
├── clientes        ─────────►  ├── clientes
├── productos       ─────────►  ├── productos
├── ventas          ─────────►  ├── ventas
└── detalle_ventas  ─────────►  └── detalle_ventas
```

La clase `SQLite` administra la creación y estructura de la base SQLite;
la clase `Migracion` lee los registros desde MySQL y los inserta en
SQLite.
