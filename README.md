# PRÁCTICA 05  
# Bases de Datos Distribuidas con MySQL, PostgreSQL y Python

## Asignatura

**Tópicos de Bases de Datos**

---

## 1. Descripción

Esta práctica tiene como propósito implementar y simular conceptos básicos de **Bases de Datos Distribuidas** utilizando dos Sistemas Gestores de Bases de Datos (SGBD):

- MySQL
- PostgreSQL

Ambos servicios se ejecutan de manera local (`localhost`) y contienen una base de datos denominada:

```text
negocios
```

Python funciona como elemento coordinador entre los dos SGBD.

La práctica permite realizar operaciones sobre ambas bases de datos y experimentar con conceptos como:

- distribución de datos;
- replicación de información;
- conexiones a diferentes SGBD;
- transacciones coordinadas;
- `COMMIT`;
- `ROLLBACK`;
- consultas distribuidas;
- transparencia de localización;
- redundancia;
- tolerancia a fallos.

---

## 2. Objetivo

Implementar mediante Python un entorno que permita interactuar con bases de datos MySQL y PostgreSQL en `localhost`, manteniendo información equivalente en ambos SGBD y simulando operaciones y consultas distribuidas.

Se busca que el estudiante comprenda cómo una aplicación puede coordinar diferentes servicios de bases de datos y responder ante la indisponibilidad de alguno de ellos.

---

## 3. Arquitectura general

La práctica utiliza la siguiente arquitectura:

```text
                         USUARIO
                            │
                            ▼
                          PYTHON
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
              MySQL                PostgreSQL
             localhost              localhost
                 │                     │
                 ▼                     ▼
              negocios               negocios
                 │                     │
          ┌──────┼──────┐       ┌──────┼──────┐
          │      │      │       │      │      │
       clientes ventas productos clientes ventas productos
                 │                     │
          detalle_ventas         detalle_ventas
```

Python funciona como intermediario para acceder a los dos SGBD.

---

## 4. Tecnologías utilizadas

- Python
- MySQL
- PostgreSQL
- Visual Studio Code
- MySQL Workbench
- pgAdmin
- Entorno virtual de Python (`venv`)

Librerías de Python:

```text
mysql-connector-python
psycopg2-binary
```

---

## 5. Creación del entorno virtual

Desde la carpeta de la práctica:

```powershell
python -m venv .venv
```

Activar el entorno virtual en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install mysql-connector-python psycopg2-binary
```

Generar el archivo de dependencias:

```powershell
pip freeze > requirements.txt
```

Posteriormente las dependencias pueden instalarse mediante:

```powershell
pip install -r requirements.txt
```

---

## 6. Base de datos

En ambos SGBD se utiliza una base de datos denominada:

```text
negocios
```

La base contiene cuatro tablas:

```text
clientes
productos
ventas
detalle_ventas
```

### Relaciones

```text
clientes
   │
   │ 1
   │
   └──────────── N
                ventas
                   │
                   │ 1
                   │
                   └──────────── N
                              detalle_ventas
                                   │
                                   │ N
                                   │
                                   └──────── 1
                                           productos
```

---

## 7. Tabla clientes

Almacena la información de los clientes.

Campos principales:

```text
id_cliente
nombre
telefono
correo
direccion
```

`id_cliente` funciona como llave primaria.

---

## 8. Tabla productos

Contiene la información de los productos disponibles.

Campos:

```text
id_producto
nombre
descripcion
precio
existencia
```

`id_producto` funciona como llave primaria.

---

## 9. Tabla ventas

Registra las operaciones de venta.

Campos:

```text
id_venta
fecha
id_cliente
total
```

Cada venta pertenece a un cliente.

En MySQL el identificador se genera mediante:

```sql
AUTO_INCREMENT
```

Mientras que PostgreSQL utiliza:

```sql
GENERATED ALWAYS AS IDENTITY
```

---

## 10. Tabla detalle_ventas

Contiene los productos correspondientes a cada venta.

Campos:

```text
id_detalle
id_venta
id_producto
cantidad
precio_unitario
subtotal
```

El subtotal se determina mediante:

```text
subtotal = cantidad × precio_unitario
```

El total de una venta corresponde a:

```text
total = suma de los subtotales
```

---

## 11. Datos iniciales

Los scripts de carga generan:

```text
5 clientes
5 productos
5 ventas
12 detalles de venta
```

Cada venta contiene al menos dos productos.

Los totales se calculan a partir de los registros almacenados en `detalle_ventas`.

Para comprobar la consistencia se utiliza:

```sql
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
```

La columna:

```text
diferencia
```

debe tener un valor de:

```text
0.00
```

para todas las ventas.

---

# 12. Clase `Conexiones`

El archivo:

```text
CConexiones.py
```

contiene la clase:

```python
class Conexiones:
```

La clase administra las conexiones hacia MySQL y PostgreSQL.

Sus principales atributos son:

```python
self.usuario
self.password
```

Los métodos son:

```python
conectar_MySQL()
conectar_Postgres()
```

Esto permite centralizar la lógica de conexión y reutilizarla desde los diferentes programas de la práctica.

---

## 13. Seguridad de las credenciales

Los programas solicitan el usuario mediante:

```python
input()
```

y la contraseña mediante:

```python
getpass()
```

Ejemplo:

```python
usuario = input("Usuario: ")
password = getpass("Contraseña: ")
```

De esta forma la contraseña no queda escrita directamente dentro del código fuente ni se muestra en pantalla durante su captura.

---

# 14. Creación automática de las bases

Python puede ejecutar los scripts SQL utilizados para crear las bases de datos y sus tablas.

Se utilizan scripts independientes para:

```text
MySQL
PostgreSQL
```

Esto es necesario porque existen diferencias sintácticas entre ambos gestores.

Por ejemplo:

| MySQL | PostgreSQL |
|---|---|
| `AUTO_INCREMENT` | `GENERATED ALWAYS AS IDENTITY` |
| `DECIMAL` | `NUMERIC` |
| `USE negocios` | Se conecta directamente a `negocios` |

---

# 15. Carga automática de datos

Otro programa Python ejecuta los scripts SQL que cargan los datos iniciales.

El proceso general es:

```text
Python
   │
   ├──────────► Script SQL MySQL
   │                   │
   │                   ▼
   │                 MySQL
   │
   └──────────► Script SQL PostgreSQL
                       │
                       ▼
                   PostgreSQL
```

Esto permite reiniciar fácilmente los datos utilizados durante las pruebas.

---

# 16. Simulación de transacciones distribuidas

La práctica incluye un programa que permite ejecutar:

```sql
INSERT
UPDATE
DELETE
```

El usuario proporciona sus credenciales y selecciona el SGBD donde desea iniciar la operación:

```text
1. MySQL
2. PostgreSQL
```

Por ejemplo:

```text
Usuario: rpizarro
Contraseña:

Seleccione el motor donde inicia la operación:

1. MySQL
2. PostgreSQL

Opción: 1
```

Posteriormente escribe una instrucción SQL.

Ejemplo:

```sql
UPDATE productos
SET precio = 400
WHERE id_producto = 'PROD0000000000000001';
```

Python intenta ejecutar la operación en ambos SGBD.

```text
                 UPDATE
                    │
                    ▼
                  Python
                    │
             ┌──────┴──────┐
             ▼             ▼
           MySQL       PostgreSQL
             │             │
          execute()     execute()
             │             │
             └──────┬──────┘
                    ▼
              ¿Ambos OK?
                /      \
              Sí        No
              │          │
              ▼          ▼
           COMMIT     ROLLBACK
```

Si ambas operaciones tienen éxito se realiza `COMMIT`.

Si se produce una excepción antes de confirmar las operaciones, se intenta realizar `ROLLBACK`.

---

## 17. Prueba de tolerancia a fallos en actualizaciones

Una de las pruebas consiste en detener deliberadamente uno de los servicios.

Por ejemplo:

```text
MySQL       → disponible
PostgreSQL  → detenido
```

La aplicación detectará que no es posible completar la operación en los dos servicios y mostrará un mensaje indicando que la transacción no fue realizada.

Esto permite estudiar el comportamiento de una operación distribuida ante la indisponibilidad de un nodo.

> **Nota:** la coordinación mediante dos conexiones y dos `COMMIT` independientes no constituye una transacción distribuida atómica completa. Existe una ventana de fallo si un SGBD confirma y el segundo falla antes de confirmar. Este problema permite introducir posteriormente protocolos como **Two-Phase Commit (2PC)**.

---

# 18. Consultas distribuidas

La práctica también incluye consultas `SELECT`.

El sistema intenta realizar la consulta sobre un servicio determinado.

Si el servicio no está disponible, Python intenta automáticamente realizar la misma consulta sobre el otro SGBD.

```text
                    SELECT
                       │
                       ▼
                     Python
                       │
                       ▼
                Servicio preferido
                    /      \
              responde     falla
                 │           │
                 ▼           ▼
              DATOS      Otro SGBD
                             │
                             ▼
                           DATOS
```

---

## 19. Transparencia para el usuario

Un objetivo de las consultas distribuidas es que el origen físico de los datos sea transparente para el usuario.

El usuario solicita:

```sql
SELECT *
FROM clientes;
```

y recibe los resultados sin necesidad de conocer si fueron obtenidos desde:

```text
MySQL
```

o:

```text
PostgreSQL
```

Esto permite simular el concepto de **transparencia de localización**.

---

## 20. Tolerancia a fallos

Si el servicio seleccionado no responde, la aplicación intenta obtener la información desde el otro servicio.

Por ejemplo:

```text
Usuario
   │
   ▼
SELECT
   │
   ▼
Python
   │
   ▼
MySQL
   │
   ✗ No disponible
   │
   ▼
PostgreSQL
   │
   ✓ Disponible
   │
   ▼
Resultados
```

Para el usuario, el proceso de recuperación es transparente.

---

# 21. Conceptos estudiados

La práctica permite experimentar con los siguientes conceptos de Bases de Datos Distribuidas:

**Distribución de datos:** la información se encuentra disponible en diferentes SGBD.

**Replicación:** MySQL y PostgreSQL mantienen conjuntos equivalentes de información para los ejercicios.

**Transparencia de localización:** el usuario puede recibir información sin conocer necesariamente el SGBD que respondió.

**Tolerancia a fallos:** cuando un servicio no está disponible, la consulta puede intentar recuperarse desde otro servicio.

**Transacciones coordinadas:** Python coordina operaciones de actualización en dos SGBD.

**COMMIT:** confirma una transacción.

**ROLLBACK:** intenta deshacer los cambios pendientes cuando ocurre una excepción antes de confirmar.

**Redundancia:** existen copias equivalentes de los datos en dos gestores diferentes.

---

# 22. Pruebas sugeridas

Para comprobar el funcionamiento de la práctica se recomienda realizar los siguientes escenarios:

```text
PRUEBA 1
MySQL disponible
PostgreSQL disponible
→ La operación debe realizarse en ambos.

PRUEBA 2
MySQL disponible
PostgreSQL detenido
→ Una actualización coordinada no debe considerarse completada.

PRUEBA 3
MySQL detenido
PostgreSQL disponible
→ Una consulta debe intentar obtener los datos desde PostgreSQL.

PRUEBA 4
PostgreSQL detenido
MySQL disponible
→ Una consulta debe intentar obtener los datos desde MySQL.

PRUEBA 5
MySQL disponible
PostgreSQL disponible
pero SQL incorrecto
→ Debe generarse una excepción y evitar considerar exitosa la operación.

PRUEBA 6
INSERT con llave primaria duplicada
→ Debe producirse un error y activarse la lógica de ROLLBACK.
```

---

# 23. Estructura sugerida del proyecto

```text
PRACTICA_05/
│
├── .venv/
│
├── CConexiones.py
│
├── probar_CConexiones.py
│
├── Crear BD MySql y Postgres.py
├── cargar datos MySql y Postgres.py
│
├── transaccion MySql Postgres.py
├── consulta_distribuida.py
│
├── crear bd negocios mysql.sql
├── crea bd negocios Postgres.sql
│
├── cargar datos BD negocios MySql.sql
├── cargar datos BD negocios Postgres.sql
│
├── requirements.txt
├── .gitignore
│
└── README.md
```

---

# 24. `.gitignore`

El entorno virtual no debe almacenarse en GitHub.

Crear:

```text
.gitignore
```

con:

```text
.venv/
__pycache__/
*.pyc
```

No se deben almacenar contraseñas dentro del repositorio.

---

# 25. Secuencia de ejecución

Para realizar la práctica completa se recomienda seguir este orden:

```text
1. Activar entorno virtual
           ↓
2. Probar conexiones
           ↓
3. Crear BD negocios en ambos SGBD
           ↓
4. Crear las tablas
           ↓
5. Cargar datos iniciales
           ↓
6. Verificar que MySQL y PostgreSQL
   contienen información equivalente
           ↓
7. Probar INSERT / UPDATE / DELETE
           ↓
8. Probar COMMIT y ROLLBACK
           ↓
9. Detener deliberadamente un servicio
           ↓
10. Probar consultas distribuidas
           ↓
11. Analizar transparencia y
    tolerancia a fallos
```

---

# 26. Conclusión

Esta práctica permite implementar un escenario introductorio de Bases de Datos Distribuidas utilizando **MySQL, PostgreSQL y Python**.

Python funciona como una capa de coordinación entre los dos SGBD, permitiendo experimentar con operaciones de actualización, consultas, manejo de excepciones y recuperación ante la indisponibilidad de un servicio.

La práctica permite comprender que un sistema distribuido no consiste solamente en disponer de varias bases de datos, sino también en coordinar su acceso, mantener la consistencia de la información y proporcionar mecanismos de transparencia y tolerancia a fallos.

Como continuación, el ejercicio puede evolucionar hacia mecanismos de coordinación más rigurosos, como **Two-Phase Commit (2PC)**, y hacia escenarios donde los nodos se encuentren físicamente en servidores diferentes.
