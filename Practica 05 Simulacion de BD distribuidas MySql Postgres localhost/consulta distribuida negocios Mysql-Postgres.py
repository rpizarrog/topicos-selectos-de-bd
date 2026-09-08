from getpass import getpass
from CConexiones import Conexiones


# ============================================================
# EJECUTAR CONSULTA
# ============================================================

def ejecutar_consulta(conexion, sql):

    cursor = conexion.cursor()

    cursor.execute(sql)

    # Nombres de las columnas
    columnas = [columna[0] for columna in cursor.description]

    # Registros obtenidos
    registros = cursor.fetchall()

    cursor.close()

    return columnas, registros


# ============================================================
# CONSULTA DISTRIBUIDA
# ============================================================

def consulta_distribuida(conexiones, sql, opcion):

    conexion = None

    try:

        # ====================================================
        # OPCION 1
        # INTENTAR PRIMERO MYSQL
        # ====================================================

        if opcion == "1":

            try:

                conexion = conexiones.conectar_MySQL("negocios")

                columnas, registros = ejecutar_consulta(
                    conexion,
                    sql
                )

            except Exception:

                # MySQL no respondió.
                # Intentar PostgreSQL sin informar al usuario.

                if conexion is not None:

                    try:
                        conexion.close()
                    except:
                        pass

                conexion = conexiones.conectar_Postgres("negocios")

                columnas, registros = ejecutar_consulta(
                    conexion,
                    sql
                )


        # ====================================================
        # OPCION 2
        # INTENTAR PRIMERO POSTGRESQL
        # ====================================================

        elif opcion == "2":

            try:

                conexion = conexiones.conectar_Postgres("negocios")

                columnas, registros = ejecutar_consulta(
                    conexion,
                    sql
                )

            except Exception:

                # PostgreSQL no respondió.
                # Intentar MySQL sin informar al usuario.

                if conexion is not None:

                    try:
                        conexion.close()
                    except:
                        pass

                conexion = conexiones.conectar_MySQL("negocios")

                columnas, registros = ejecutar_consulta(
                    conexion,
                    sql
                )


        # ====================================================
        # MOSTRAR RESULTADOS
        # ====================================================

        print("\n========================================")
        print("       RESULTADO DE LA CONSULTA")
        print("========================================\n")

        # Encabezados
        for columna in columnas:
            print(f"{columna:<25}", end="")

        print()

        print("-" * (25 * len(columnas)))

        # Registros
        for registro in registros:

            for dato in registro:

                print(f"{str(dato):<25}", end="")

            print()


        print("\nRegistros encontrados:", len(registros))


    except Exception as error:

        # ====================================================
        # NINGUNO DE LOS DOS SERVICIOS RESPONDIO
        # ====================================================

        print("\n========================================")
        print("     CONSULTA NO DISPONIBLE")
        print("========================================")

        print("\nNo fue posible realizar la consulta.")

        # Para fines de desarrollo podemos mostrar el error.
        # Después podemos eliminar esta línea.
        print("\nDetalle técnico:")
        print(error)


    finally:

        if conexion is not None:

            try:
                conexion.close()
            except:
                pass


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("       CONSULTA DISTRIBUIDA")
    print("========================================")

    # ========================================================
    # USUARIO Y CONTRASEÑA
    # ========================================================

    usuario = input("\nUsuario: ")
    password = getpass("Contraseña: ")

    conexiones = Conexiones(
        usuario=usuario,
        password=password
    )


    # ========================================================
    # SELECCIONAR SERVICIO
    # ========================================================

    print("\nSeleccione el servicio preferido:")
    print("1. MySQL")
    print("2. PostgreSQL")

    opcion = input("\nOpción: ")


    if opcion not in ("1", "2"):

        print("\nOpción incorrecta.")

    else:

        # ====================================================
        # CAPTURAR SELECT
        # ====================================================

        print("\nEscriba la consulta SQL")

        sql = input("\nSQL > ")


        # ====================================================
        # SOLO PERMITIR SELECT
        # ====================================================

        if sql.strip().upper().startswith("SELECT"):

            consulta_distribuida(
                conexiones,
                sql,
                opcion
            )

        else:

            print("\nSolo se permiten instrucciones SELECT.")