from getpass import getpass
from CConexiones import Conexiones


# =========================================================
# EJECUTAR SCRIPT MYSQL
# =========================================================
def crear_MySQL(conexiones):

    print("\n========================================")
    print("CREANDO BASE DE DATOS EN MYSQL")
    print("========================================")

    conexion = conexiones.conectar_MySQL()
    cursor = conexion.cursor()

    # Leer archivo SQL
    with open(
        "crear bd negocios mysql.sql",
        "r",
        encoding="utf-8"
    ) as archivo:

        script = archivo.read()

    # Dividir el script por ;
    instrucciones = script.split(";")

    # Ejecutar cada instrucción individualmente
    for instruccion in instrucciones:

        instruccion = instruccion.strip()

        if instruccion:
            cursor.execute(instruccion)

    conexion.commit()

    cursor.close()
    conexion.close()

    print("✓ Base negocios creada en MySQL")

# =========================================================
# CREAR POSTGRESQL
# =========================================================

def crear_Postgres(conexiones):

    print("\n========================================")
    print("CREANDO BASE DE DATOS EN POSTGRESQL")
    print("========================================")

    # -----------------------------------------------------
    # Conectarse inicialmente a postgres
    # -----------------------------------------------------

    conexion = conexiones.conectar_Postgres("postgres")

    # DROP DATABASE y CREATE DATABASE
    # no deben estar dentro de una transacción
    conexion.autocommit = True

    cursor = conexion.cursor()

    # Cerrar conexiones existentes a negocios
    cursor.execute("""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = 'negocios'
        AND pid <> pg_backend_pid();
    """)

    cursor.execute("""
        DROP DATABASE IF EXISTS negocios;
    """)

    cursor.execute("""
        CREATE DATABASE negocios;
    """)

    cursor.close()
    conexion.close()

    print("✓ Base negocios creada")


    # -----------------------------------------------------
    # Conectarse ahora a negocios
    # -----------------------------------------------------

    conexion = conexiones.conectar_Postgres("negocios")

    cursor = conexion.cursor()

    # Leer script PostgreSQL
    with open(
        "crea bd negocios Postgres.sql",
        "r",
        encoding="utf-8"
    ) as archivo:

        script = archivo.read()

    cursor.execute(script)

    conexion.commit()

    cursor.close()
    conexion.close()

    print("✓ Tablas creadas en PostgreSQL")


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

if __name__ == "__main__":

    print("========================================")
    print("     CREACIÓN DE BASES DE DATOS")
    print("========================================")

    usuario = input("Usuario: ")
    password = getpass("Contraseña: ")

    conexiones = Conexiones(
        usuario=usuario,
        password=password
    )

    try:

        crear_MySQL(conexiones)

    except Exception as error:

        print("\n✗ ERROR MYSQL")
        print(error)


    try:

        crear_Postgres(conexiones)

    except Exception as error:

        print("\n✗ ERROR POSTGRESQL")
        print(error)