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

    # Obtener registros
    registros = cursor.fetchall()

    cursor.close()

    return columnas, registros


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

def mostrar_resultados(columnas, registros):

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


# ============================================================
# CONSULTA DISTRIBUIDA
# ============================================================

def consulta_distribuida(conexiones, sql):

    conexion_mysql = None
    conexion_postgres = None

    mysql_disponible = False
    postgres_disponible = False


    # ========================================================
    # 1. VERIFICAR MYSQL
    # ========================================================

    try:

        conexion_mysql = conexiones.conectar_MySQL("negocios")
        mysql_disponible = True

    except Exception:

        mysql_disponible = False


    # ========================================================
    # 2. VERIFICAR POSTGRESQL
    # ========================================================

    try:

        conexion_postgres = conexiones.conectar_Postgres("negocios")
        postgres_disponible = True

    except Exception:

        postgres_disponible = False


    # ========================================================
    # 3. MOSTRAR ESTADO DE LOS SERVICIOS
    # ========================================================

    print("\n========================================")
    print("       ESTADO DE LOS SERVICIOS")
    print("========================================")

    if mysql_disponible:
        print("✓ Servicio MySQL disponible")
    else:
        print("✗ Servicio MySQL detenido o no disponible")

    if postgres_disponible:
        print("✓ Servicio PostgreSQL disponible")
    else:
        print("✗ Servicio PostgreSQL detenido o no disponible")


    # ========================================================
    # 4. REALIZAR CONSULTA
    # ========================================================

    try:

        # ----------------------------------------------------
        # SI MYSQL ESTA DISPONIBLE
        # ----------------------------------------------------

        if mysql_disponible:

            columnas, registros = ejecutar_consulta(
                conexion_mysql,
                sql
            )

            print("\n✓ Consulta exitosa desde MySQL")

            mostrar_resultados(
                columnas,
                registros
            )


        # ----------------------------------------------------
        # SI MYSQL NO ESTA DISPONIBLE
        # USAR POSTGRESQL
        # ----------------------------------------------------

        elif postgres_disponible:

            columnas, registros = ejecutar_consulta(
                conexion_postgres,
                sql
            )

            print("\n✓ Consulta exitosa desde PostgreSQL")

            mostrar_resultados(
                columnas,
                registros
            )


        # ----------------------------------------------------
        # NINGUN SERVICIO ESTA DISPONIBLE
        # ----------------------------------------------------

        else:

            print("\n========================================")
            print("       CONSULTA NO DISPONIBLE")
            print("========================================")

            print("\n✗ MySQL no está disponible")
            print("✗ PostgreSQL no está disponible")

            print("\nNo fue posible realizar la consulta.")


    except Exception as error:

        print("\n========================================")
        print("          ERROR EN CONSULTA")
        print("========================================")

        print("\nNo fue posible ejecutar la consulta SQL.")

        print("\nDetalle técnico:")
        print(error)


    finally:

        # ====================================================
        # CERRAR CONEXIONES
        # ====================================================

        if conexion_mysql is not None:

            try:
                conexion_mysql.close()
            except:
                pass


        if conexion_postgres is not None:

            try:
                conexion_postgres.close()
            except:
                pass


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("       CONSULTA DISTRIBUIDA")
    print("        MySQL - PostgreSQL")
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
    # CAPTURAR CONSULTA
    # ========================================================

    print("\nEscriba la consulta SQL")
    print("Solo se permiten instrucciones SELECT.")

    sql = input("\nSQL > ")


    # ========================================================
    # VALIDAR SELECT
    # ========================================================

    if sql.strip().upper().startswith("SELECT"):

        consulta_distribuida(
            conexiones,
            sql
        )

    else:

        print("\n✗ Solo se permiten instrucciones SELECT.")