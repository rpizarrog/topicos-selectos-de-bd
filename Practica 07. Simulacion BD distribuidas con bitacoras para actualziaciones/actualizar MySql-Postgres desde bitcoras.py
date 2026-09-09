from getpass import getpass
import json
import os

from CConexiones import Conexiones


BITACORA_MYSQL = "bitacora_caidas_Mysql.txt"
BITACORA_POSTGRES = "bitacora_caidas_Postgres.txt"


# ============================================================
# LEER BITACORA
# ============================================================

def leer_bitacora(nombre_archivo):

    operaciones = []

    if not os.path.exists(nombre_archivo):
        return operaciones

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:

        for linea in archivo:

            linea = linea.strip()

            if linea:
                operaciones.append(json.loads(linea))

    return operaciones


# ============================================================
# LIMPIAR BITACORA
# ============================================================

def limpiar_bitacora(nombre_archivo):

    # Vacía el archivo, pero no lo elimina
    with open(nombre_archivo, "w", encoding="utf-8"):
        pass


# ============================================================
# ACTUALIZAR MYSQL DESDE BITACORA
# ============================================================

def actualizar_mysql(conexiones):

    operaciones = leer_bitacora(BITACORA_MYSQL)

    if len(operaciones) == 0:

        print("\nMySQL:")
        print("No existen operaciones pendientes.")

        return

    conexion = None
    cursor = None

    try:

        # ----------------------------------------------------
        # CONECTAR A MYSQL
        # ----------------------------------------------------

        conexion = conexiones.conectar_MySQL("negocios")

        cursor = conexion.cursor()

        # ----------------------------------------------------
        # INICIAR TRANSACCION MYSQL
        # ----------------------------------------------------

        conexion.start_transaction()

        print("\n========================================")
        print("       ACTUALIZANDO MYSQL")
        print("========================================")

        print(
            "Operaciones pendientes:",
            len(operaciones)
        )

        # ----------------------------------------------------
        # EJECUTAR OPERACIONES PENDIENTES
        # ----------------------------------------------------

        for numero, registro in enumerate(
            operaciones,
            start=1
        ):

            print("\nOperación:", numero)

            print(
                "Fecha/Hora:",
                registro.get("fecha_hora", "")
            )

            print(
                "SQL:",
                registro["sql"]
            )

            cursor.execute(
                registro["sql"]
            )

            print("Operación ejecutada correctamente.")

        # ----------------------------------------------------
        # CONFIRMAR TRANSACCION
        # ----------------------------------------------------

        conexion.commit()

        print("\nCOMMIT realizado en MySQL.")

        # ----------------------------------------------------
        # LIMPIAR BITACORA
        # SOLO DESPUES DEL COMMIT
        # ----------------------------------------------------

        limpiar_bitacora(
            BITACORA_MYSQL
        )

        print("MySQL quedó actualizado.")

        print(
            "bitacora_caidas_Mysql.txt "
            "quedó vacía."
        )


    except Exception as error:

        # ----------------------------------------------------
        # ROLLBACK
        # ----------------------------------------------------

        if conexion is not None:

            try:

                conexion.rollback()

                print(
                    "\nROLLBACK realizado en MySQL."
                )

            except Exception:

                pass

        print(
            "\nNo fue posible actualizar MySQL."
        )

        print(
            "La bitácora NO fue limpiada."
        )

        print(
            "Las operaciones continúan pendientes."
        )

        print("\nDetalle técnico:")

        print(error)


    finally:

        if cursor is not None:

            try:
                cursor.close()
            except Exception:
                pass

        if conexion is not None:

            try:
                conexion.close()
            except Exception:
                pass


# ============================================================
# ACTUALIZAR POSTGRESQL DESDE BITACORA
# ============================================================

def actualizar_postgres(conexiones):

    operaciones = leer_bitacora(
        BITACORA_POSTGRES
    )

    if len(operaciones) == 0:

        print("\nPostgreSQL:")
        print("No existen operaciones pendientes.")

        return

    conexion = None
    cursor = None

    try:

        # ----------------------------------------------------
        # CONECTAR A POSTGRESQL
        # ----------------------------------------------------

        conexion = conexiones.conectar_Postgres(
            "negocios"
        )

        cursor = conexion.cursor()

        print("\n========================================")
        print("      ACTUALIZANDO POSTGRESQL")
        print("========================================")

        print(
            "Operaciones pendientes:",
            len(operaciones)
        )

        # ----------------------------------------------------
        # POSTGRESQL INICIA LA TRANSACCION
        # AL EJECUTAR LA PRIMERA INSTRUCCION
        # ----------------------------------------------------

        for numero, registro in enumerate(
            operaciones,
            start=1
        ):

            print("\nOperación:", numero)

            print(
                "Fecha/Hora:",
                registro.get("fecha_hora", "")
            )

            print(
                "SQL:",
                registro["sql"]
            )

            cursor.execute(
                registro["sql"]
            )

            print("Operación ejecutada correctamente.")

        # ----------------------------------------------------
        # CONFIRMAR TRANSACCION
        # ----------------------------------------------------

        conexion.commit()

        print(
            "\nCOMMIT realizado en PostgreSQL."
        )

        # ----------------------------------------------------
        # LIMPIAR BITACORA
        # SOLO DESPUES DEL COMMIT
        # ----------------------------------------------------

        limpiar_bitacora(
            BITACORA_POSTGRES
        )

        print(
            "PostgreSQL quedó actualizado."
        )

        print(
            "bitacora_caidas_Postgres.txt "
            "quedó vacía."
        )


    except Exception as error:

        # ----------------------------------------------------
        # ROLLBACK
        # ----------------------------------------------------

        if conexion is not None:

            try:

                conexion.rollback()

                print(
                    "\nROLLBACK realizado "
                    "en PostgreSQL."
                )

            except Exception:

                pass

        print(
            "\nNo fue posible actualizar PostgreSQL."
        )

        print(
            "La bitácora NO fue limpiada."
        )

        print(
            "Las operaciones continúan pendientes."
        )

        print("\nDetalle técnico:")

        print(error)


    finally:

        if cursor is not None:

            try:
                cursor.close()
            except Exception:
                pass

        if conexion is not None:

            try:
                conexion.close()
            except Exception:
                pass


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("   ACTUALIZAR MYSQL - POSTGRESQL")
    print("         DESDE BITACORAS")
    print("          PRACTICA 07")
    print("========================================")

    # --------------------------------------------------------
    # CREDENCIALES
    # --------------------------------------------------------

    usuario = input("\nUsuario: ")

    password = getpass(
        "Contraseña: "
    )

    conexiones = Conexiones(
        usuario=usuario,
        password=password
    )

    # --------------------------------------------------------
    # REVISAR BITACORA MYSQL
    # --------------------------------------------------------

    actualizar_mysql(
        conexiones
    )

    # --------------------------------------------------------
    # REVISAR BITACORA POSTGRESQL
    # --------------------------------------------------------

    actualizar_postgres(
        conexiones
    )

    print("\n========================================")
    print("       PROCESO FINALIZADO")
    print("========================================")

