# Migración de SQLite local a Cloudflare D1

## Sistemas Multibase de Datos

Este proyecto implementa la migración de la base de datos **negocios**
desde **SQLite local** hacia **Cloudflare D1**, utilizando Python como
capa de integración.

``` text
SQLite local
datos/negocios.db
      |
      | Python
      v
CMigracionCloud.py
      |
      | API Cloudflare
      v
Cloudflare D1
negocios
```

## Objetivo

Migrar los registros almacenados en `datos/negocios.db` hacia la base
`negocios` alojada en Cloudflare D1, conservando llaves primarias,
relaciones y correspondencia de los datos.

## Tablas

  -----------------------------------------------------------------------
  Tabla                   Llave primaria          Relación
  ----------------------- ----------------------- -----------------------
  clientes                id_cliente              \-

  productos               id_producto             \-

  ventas                  id_venta                id_cliente -\> clientes

  detalle_ventas          id_detalle              id_venta -\> ventas;
                                                  id_producto -\>
                                                  productos
  -----------------------------------------------------------------------

El orden de migración es:

``` text
clientes
   ↓
productos
   ↓
ventas
   ↓
detalle_ventas
```

## Archivos principales

### CMigracionCloud.py

Contiene la clase:

``` python
class Migracion:
```

Administra la conexión con SQLite local, carga la configuración de
Cloudflare y transfiere los registros hacia Cloudflare D1.

### probar CMigracion Cloud.py

Crea un objeto `Migracion`, recupera los registros de SQLite local y
ejecuta su inserción en Cloudflare D1.

### .env

Guarda las credenciales e identificadores:

``` text
API_TOKEN=tu_token
ACCOUNT_ID=tu_account_id
DATABASE_ID=tu_database_id
```

El archivo `.env` no debe publicarse en GitHub. Agregar a `.gitignore`:

``` text
.env
```

## Dependencias

El proyecto utiliza:

-   sqlite3
-   os
-   python-dotenv
-   cloudflare

Instalación:

``` bash
python -m pip install python-dotenv cloudflare
```

Actualizar `requirements.txt`:

``` bash
python -m pip freeze > requirements.txt
```

## Métodos de la clase Migracion

### **init**(self)

Inicializa la ruta `datos/negocios.db`, las conexiones de SQLite y carga
desde `.env`:

-   API_TOKEN
-   ACCOUNT_ID
-   DATABASE_ID

### f_conectar_sqlite(self)

Abre `negocios.db`, crea el cursor y activa las llaves foráneas
mediante:

``` sql
PRAGMA foreign_keys = ON;
```

### f_conectar_cloudflare(self)

Configura el cliente de Cloudflare utilizando el API Token.

### f_leer_clientes_sqlite(self)

Lee `id_cliente`, `nombre`, `telefono`, `correo` y `direccion` de la
tabla `clientes`.

### f_agregar_clientes_cloudflare(self, clientes)

Inserta en Cloudflare D1 los clientes recuperados desde SQLite local.

### f_leer_productos_sqlite(self)

Lee `id_producto`, `nombre`, `descripcion`, `precio` y `existencia`.

### f_agregar_productos_cloudflare(self, productos)

Inserta los productos en la tabla `productos` de Cloudflare D1.

### f_leer_ventas_sqlite(self)

Lee `id_venta`, `fecha`, `id_cliente` y `total`.

El `id_venta` se conserva para mantener las relaciones con
`detalle_ventas`.

### f_agregar_ventas_cloudflare(self, ventas)

Inserta las ventas en Cloudflare D1 conservando sus identificadores.

### f_leer_detalle_ventas_sqlite(self)

Lee `id_detalle`, `id_venta`, `id_producto`, `cantidad`,
`precio_unitario` y `subtotal`.

### f_agregar_detalle_ventas_cloudflare(self, detalle_ventas)

Inserta los registros de `detalle_ventas` en Cloudflare D1 conservando
las relaciones con `ventas` y `productos`.

### f_cerrar_sqlite(self)

Cierra el cursor y la conexión con SQLite local.

## Flujo de ejecución

Primero se recuperan los registros:

``` python
migracion = Migracion()

migracion.f_conectar_sqlite()

clientes = migracion.f_leer_clientes_sqlite()
productos = migracion.f_leer_productos_sqlite()
ventas = migracion.f_leer_ventas_sqlite()
detalle_ventas = migracion.f_leer_detalle_ventas_sqlite()

migracion.f_cerrar_sqlite()
```

Después se configura Cloudflare:

``` python
migracion.f_conectar_cloudflare()
```

Finalmente se migran las tablas respetando sus dependencias:

``` python
migracion.f_agregar_clientes_cloudflare(clientes)
migracion.f_agregar_productos_cloudflare(productos)
migracion.f_agregar_ventas_cloudflare(ventas)
migracion.f_agregar_detalle_ventas_cloudflare(detalle_ventas)
```

## Ejecución

Desde la terminal de Visual Studio Code:

``` bash
python "probar CMigracion Cloud.py"
```

## Verificación

Comparar el número de registros entre SQLite local y Cloudflare D1:

``` sql
SELECT COUNT(*) FROM clientes;
SELECT COUNT(*) FROM productos;
SELECT COUNT(*) FROM ventas;
SELECT COUNT(*) FROM detalle_ventas;
```

También pueden revisarse los registros:

``` sql
SELECT * FROM clientes;
SELECT * FROM productos;
SELECT * FROM ventas;
SELECT * FROM detalle_ventas;
```

## Consideraciones

-   Las tablas deben existir previamente en Cloudflare D1.
-   Se debe respetar el orden
    `clientes -> productos -> ventas -> detalle_ventas`.
-   Los identificadores originales se conservan.
-   El API Token debe mantenerse privado.
-   El archivo `.env` no debe subirse al repositorio.
-   Si se repite la migración sobre registros existentes pueden
    producirse errores por llaves primarias duplicadas.

## Resultado

Python funciona como capa de integración entre la base SQLite local y
Cloudflare D1:

``` text
SQLite local
negocios.db
     |
     | SELECT
     v
Python
CMigracionCloud.py
     |
     | API Cloudflare
     v
Cloudflare D1
negocios
```
