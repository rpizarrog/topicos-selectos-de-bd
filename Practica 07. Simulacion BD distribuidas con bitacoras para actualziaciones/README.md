# PRACTICA 07 --- Simulación de un ambiente distribuido multibase con MySQL y PostgreSQL

## Descripción

Esta práctica simula un **ambiente de bases de datos distribuido y
multibase** utilizando MySQL y PostgreSQL en `localhost`. Ambos SMBD
contienen la base de datos `negocios` con estructuras y datos
equivalentes.

El propósito es estudiar disponibilidad, tolerancia a fallos,
transacciones, bitácoras de recuperación y consistencia eventual.

## Objetivo

Implementar mediante Python una simulación MySQL--PostgreSQL que permita
realizar consultas aunque uno de los servicios esté detenido; ejecutar
operaciones `INSERT`, `UPDATE` y `DELETE`; coordinar actualizaciones
cuando ambos servicios estén disponibles; continuar trabajando con el
servicio disponible cuando el otro esté detenido; registrar
temporalmente las operaciones que quedaron pendientes; y recuperar el
servidor cuando vuelva a estar disponible.

## Arquitectura

``` text
                         Aplicación Python
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
              MySQL                      PostgreSQL
             localhost                    localhost
             negocios                     negocios
                 |                           |
                 +-------------+-------------+
                               |
                       Datos equivalentes
```

Python funciona como coordinador. Para esta simulación no se establece
obligatoriamente un servidor primario y otro secundario.

## Tecnologías

-   Python
-   MySQL
-   PostgreSQL
-   `mysql-connector-python`
-   `psycopg2-binary`
-   entorno virtual `.venv`
-   archivos de texto con registros JSON para las bitácoras

## Preparación del entorno

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install mysql-connector-python psycopg2-binary
python -m pip freeze > requirements.txt
```

Para reconstruir el entorno:

``` powershell
python -m pip install -r requirements.txt
```

## Clase de conexiones

`CConexiones.py` centraliza las conexiones hacia MySQL y PostgreSQL.

``` python
from CConexiones import Conexiones

conexiones = Conexiones(
    usuario=usuario,
    password=password
)
```

## Escenarios de disponibilidad

  -----------------------------------------------------------------------
  MySQL             PostgreSQL        Consultas         INSERT / UPDATE /
                                                        DELETE
  ----------------- ----------------- ----------------- -----------------
  Disponible        Disponible        Se puede          Se actualizan
                                      consultar         ambos

  Detenido          Disponible        PostgreSQL        PostgreSQL se
                                      responde          actualiza y MySQL
                                                        queda pendiente

  Disponible        Detenido          MySQL responde    MySQL se
                                                        actualiza y
                                                        PostgreSQL queda
                                                        pendiente

  Detenido          Detenido          No disponible     No se realiza la
                                                        operación
  -----------------------------------------------------------------------

## Consultas distribuidas

Para una consulta `SELECT`, el usuario no necesita seleccionar
manualmente el SMBD. El programa verifica los servicios y utiliza uno
disponible.

``` sql
SELECT * FROM clientes;
```

Si MySQL está detenido y PostgreSQL activo, PostgreSQL responde. Si
ocurre lo contrario, MySQL responde.

Archivo utilizado:

``` text
consulta distribuida negocios Mysql-Postgres VER 2.py
```

## Actualizaciones con ambos servicios activos

Cuando MySQL y PostgreSQL están disponibles, `INSERT`, `UPDATE` y
`DELETE` se ejecutan en ambos mediante transacciones locales coordinadas
desde Python.

``` text
              INSERT / UPDATE / DELETE
                         |
                       Python
                    try / except
                         |
             +-----------+-----------+
             |                       |
           MySQL                 PostgreSQL
        transacción              transacción
             |                       |
          execute                  execute
             |                       |
             +-----------+-----------+
                         |
                    ambos aceptan
                         |
                       COMMIT
```

Si ocurre un error antes de confirmar, se utiliza `ROLLBACK` según
corresponda.

**Nota académica:** dos `COMMIT` independientes coordinados desde Python
no constituyen por sí mismos un protocolo distribuido atómico de dos
fases (2PC). En esta práctica las bitácoras permiten recuperar
diferencias y alcanzar consistencia eventual.

Archivo utilizado:

``` text
actualizaciones Mysql-Postgres bitacoras PRACTICA07.py
```

## Actualización con un servicio detenido

Si MySQL está detenido y PostgreSQL activo, una operación como:

``` sql
INSERT INTO clientes
(id_cliente,nombre,telefono,correo,direccion)
VALUES
('CLPruebaA','Prueba A','6181234567',
 'pruebaA@email.com','Durango, Dgo.');
```

se ejecuta y confirma en PostgreSQL. La operación que MySQL no pudo
realizar se registra como pendiente.

Otro ejemplo:

``` sql
UPDATE productos
SET precio = 555
WHERE id_producto = 'PROD0000000000000005';
```

El comportamiento es equivalente en sentido inverso si PostgreSQL es el
servicio detenido.

## Bitácoras de caídas

Se utilizan:

``` text
bitacora_caidas_Mysql.txt
bitacora_caidas_Postgres.txt
```

`bitacora_caidas_Mysql.txt` contiene las operaciones que MySQL no pudo
ejecutar. `bitacora_caidas_Postgres.txt` contiene las que PostgreSQL no
pudo ejecutar.

Cada línea almacena un registro JSON, por ejemplo:

``` json
{"fecha_hora":"2026-09-08 18:30:00","destino":"MySQL","sql":"UPDATE productos SET precio = 555 WHERE id_producto = 'PROD0000000000000005'"}
```

Las operaciones se conservan en el orden en que ocurrieron.

## Recuperación desde bitácoras

Cuando el servicio detenido vuelve a funcionar se ejecuta:

``` text
actualizar MySql-Postgres desde bitcoras.py
```

El procedimiento es:

``` text
Leer bitácora
     |
Ejecutar operaciones pendientes
     |
¿Todas correctas?
   /       \
 Sí         No
 |           |
COMMIT    ROLLBACK
 |           |
Vaciar     Conservar
bitácora   bitácora
```

La bitácora **solo se limpia después de un `COMMIT` exitoso**. Si la
recuperación falla, permanece intacta para otro intento.

Ejemplo de ejecución:

``` powershell
python ".\actualizar MySql-Postgres desde bitcoras.py"
```

## Consistencia eventual

Mientras un servicio está detenido puede existir temporalmente una
diferencia entre los datos de MySQL y PostgreSQL. Las bitácoras
conservan las operaciones faltantes. Al restablecerse el servicio y
procesarse su bitácora, ambos nodos vuelven a disponer de la misma
información. Este comportamiento permite estudiar el concepto de
**consistencia eventual**.

## Estructura sugerida

``` text
practica 07/
|
|-- CConexiones.py
|-- probar CConexiones.py
|-- consulta distribuida negocios Mysql-Postgres VER 2.py
|-- actualizaciones Mysql-Postgres bitacoras PRACTICA07.py
|-- actualizar MySql-Postgres desde bitcoras.py
|-- bitacora_caidas_Mysql.txt
|-- bitacora_caidas_Postgres.txt
|-- requirements.txt
|-- .gitignore
|-- README.md
```

Las bitácoras pueden comenzar vacías.

## Pruebas sugeridas

1.  Mantener MySQL y PostgreSQL activos y ejecutar un `SELECT`.
2.  Detener MySQL y comprobar que PostgreSQL atienda el `SELECT`.
3.  Iniciar MySQL, detener PostgreSQL y comprobar que MySQL atienda la
    consulta.
4.  Con ambos activos, realizar un `INSERT`, `UPDATE` o `DELETE` y
    verificar ambos SMBD.
5.  Detener MySQL, realizar varias actualizaciones y revisar
    `bitacora_caidas_Mysql.txt`.
6.  Reiniciar MySQL, ejecutar la recuperación y comprobar que recibe las
    operaciones pendientes.
7.  Verificar que la bitácora quede vacía después del `COMMIT`.
8.  Repetir el experimento deteniendo PostgreSQL.
9.  Detener ambos y comprobar que no existe un nodo disponible para
    ejecutar la operación.

## Conceptos estudiados

-   bases de datos distribuidas;
-   ambiente multibase;
-   heterogeneidad de SMBD;
-   transparencia en consultas;
-   disponibilidad;
-   tolerancia a fallos;
-   transacciones;
-   `COMMIT` y `ROLLBACK`;
-   bitácoras;
-   recuperación;
-   sincronización;
-   consistencia eventual.

## Conclusión

La práctica simula un ambiente distribuido heterogéneo con MySQL y
PostgreSQL en `localhost`. Las consultas pueden continuar mientras
exista al menos un servicio disponible. En las actualizaciones, si ambos
están activos, Python coordina las operaciones sobre ambos SMBD. Si uno
está detenido, el sistema continúa con el nodo disponible y registra las
operaciones faltantes.

Cuando el servicio se restablece, las operaciones pendientes se ejecutan
dentro de una transacción. Después de un `COMMIT` exitoso, la bitácora
correspondiente se limpia. De esta manera se integran los conceptos de
**disponibilidad, tolerancia a fallos, transacciones, recuperación y
consistencia eventual**.
