from getpass import getpass
from CConexiones import Conexiones


# ============================================================
# CARGAR DATOS EN MYSQL
# ============================================================

def cargar_datos_MySQL(conexiones):

    conexion = None
    cursor = None

    try:

        print("\n========================================")
        print("CARGANDO DATOS EN MYSQL")
        print("========================================")

        # Conectarse a la BD negocios
        conexion = conexiones.conectar_MySQL("negocios")
        cursor = conexion.cursor()

        # Leer archivo SQL
        with open(
            "cargar datos BD negocios MySql.sql",
            "r",
            encoding="utf-8"
        ) as archivo:

            script = archivo.read()

        # ----------------------------------------------------
        # MySQL:
        # Ejecutar cada instrucción SQL individualmente
        # ----------------------------------------------------

        instrucciones = script.split(";")

        for instruccion in instrucciones:

            instruccion = instruccion.strip()

            if instruccion:

                cursor.execute(instruccion)

                # Consumir resultados si la instrucción
                # produjo un SELECT
                if cursor.with_rows:
                    cursor.fetchall()

        conexion.commit()

        print("✓ Datos cargados correctamente en MySQL")

    except Exception as error:

        if conexion is not None:
            conexion.rollback()

        print("✗ ERROR AL CARGAR DATOS EN MYSQL")
        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


# ============================================================
# CARGAR DATOS EN POSTGRESQL
# ============================================================

def cargar_datos_Postgres(conexiones):

    conexion = None
    cursor = None

    try:

        print("\n========================================")
        print("CARGANDO DATOS EN POSTGRESQL")
        print("========================================")

        # Conectarse a la BD negocios
        conexion = conexiones.conectar_Postgres("negocios")
        cursor = conexion.cursor()

        # Leer archivo SQL
        with open(
            "cargar datos BD negocios Postgres.sql",
            "r",
            encoding="utf-8"
        ) as archivo:

            script = archivo.read()

        # Ejecutar script PostgreSQL
        cursor.execute(script)

        conexion.commit()

        print("✓ Datos cargados correctamente en PostgreSQL")

    except Exception as error:

        if conexion is not None:
            conexion.rollback()

        print("✗ ERROR AL CARGAR DATOS EN POSTGRESQL")
        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("  CARGA DE DATOS MYSQL Y POSTGRESQL")
    print("========================================")

    # --------------------------------------------------------
    # Credenciales
    # --------------------------------------------------------

    usuario = input("Usuario: ")
    password = getpass("Contraseña: ")

    # Crear objeto Conexiones
    conexiones = Conexiones(
        usuario=usuario,
        password=password
    )

    # --------------------------------------------------------
    # Ejecutar scripts
    # --------------------------------------------------------

    cargar_datos_MySQL(conexiones)

    cargar_datos_Postgres(conexiones)

    print("\n========================================")
    print("        PROCESO FINALIZADO")
    print("========================================")