from getpass import getpass
from CConexiones import Conexiones


# ============================================================
# EJECUTAR TRANSACCION EN MYSQL Y POSTGRESQL
# ============================================================

def ejecutar_transaccion(conexiones, sql, opcion):

    conexion_mysql = None
    conexion_postgres = None

    cursor_mysql = None
    cursor_postgres = None

    try:

        # ====================================================
        # 1. CONECTARSE A LOS DOS MOTORES
        # ====================================================

        print("\nConectando a MySQL...")
        conexion_mysql = conexiones.conectar_MySQL("negocios")
        print("✓ Conexión MySQL correcta")

        print("Conectando a PostgreSQL...")
        conexion_postgres = conexiones.conectar_Postgres("negocios")
        print("✓ Conexión PostgreSQL correcta")

        cursor_mysql = conexion_mysql.cursor()
        cursor_postgres = conexion_postgres.cursor()


        # ====================================================
        # 2. EJECUTAR SEGUN MOTOR ELEGIDO
        # ====================================================

        if opcion == "1":

            # ------------------------------------------------
            # PRIMERO MYSQL
            # ------------------------------------------------

            print("\nMotor origen: MySQL")

            print("Ejecutando en MySQL...")
            cursor_mysql.execute(sql)
            print("✓ MySQL aceptó la instrucción")

            print("Ejecutando en PostgreSQL...")
            cursor_postgres.execute(sql)
            print("✓ PostgreSQL aceptó la instrucción")


        elif opcion == "2":

            # ------------------------------------------------
            # PRIMERO POSTGRESQL
            # ------------------------------------------------

            print("\nMotor origen: PostgreSQL")

            print("Ejecutando en PostgreSQL...")
            cursor_postgres.execute(sql)
            print("✓ PostgreSQL aceptó la instrucción")

            print("Ejecutando en MySQL...")
            cursor_mysql.execute(sql)
            print("✓ MySQL aceptó la instrucción")


        # ====================================================
        # 3. LAS DOS INSTRUCCIONES FUNCIONARON
        # ====================================================

        print("\nLas dos bases aceptaron la operación.")
        print("Realizando COMMIT...")

        conexion_mysql.commit()
        conexion_postgres.commit()

        print("\n========================================")
        print("     TRANSACCIÓN REALIZADA")
        print("========================================")
        print("✓ MySQL actualizado")
        print("✓ PostgreSQL actualizado")


    except Exception as error:

        # ====================================================
        # 4. ERROR -> ROLLBACK
        # ====================================================

        print("\n========================================")
        print("    TRANSACCIÓN NO REALIZADA")
        print("========================================")

        print("\nError:")
        print(error)

        # ----------------------------------------------------
        # ROLLBACK MYSQL
        # ----------------------------------------------------

        if conexion_mysql is not None:

            try:
                conexion_mysql.rollback()
                print("↩ ROLLBACK realizado en MySQL")

            except Exception:
                print("✗ No fue posible realizar ROLLBACK en MySQL")


        # ----------------------------------------------------
        # ROLLBACK POSTGRESQL
        # ----------------------------------------------------

        if conexion_postgres is not None:

            try:
                conexion_postgres.rollback()
                print("↩ ROLLBACK realizado en PostgreSQL")

            except Exception:
                print("✗ No fue posible realizar ROLLBACK en PostgreSQL")

        print("\n✗ No se completó la operación en ambos SGBD.")


    finally:

        # ====================================================
        # 5. CERRAR CURSORES Y CONEXIONES
        # ====================================================

        if cursor_mysql is not None:
            cursor_mysql.close()

        if cursor_postgres is not None:
            cursor_postgres.close()

        if conexion_mysql is not None:
            conexion_mysql.close()

        if conexion_postgres is not None:
            conexion_postgres.close()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("     TRANSACCIÓN DISTRIBUIDA")
    print("       MySQL + PostgreSQL")
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
    # ELEGIR MOTOR DE ORIGEN
    # ========================================================

    print("\nSeleccione el motor donde inicia la operación:")
    print("1. MySQL")
    print("2. PostgreSQL")

    opcion = input("\nOpción: ")


    if opcion not in ("1", "2"):

        print("\n✗ Opción incorrecta.")

    else:

        # ====================================================
        # CAPTURAR INSTRUCCION SQL
        # ====================================================

        print("\nEscriba la instrucción SQL")
        print("Operaciones permitidas: INSERT, UPDATE o DELETE")

        sql = input("\nSQL > ")

        operacion = sql.strip().upper()


        # ====================================================
        # VALIDAR OPERACION
        # ====================================================

        if (
            operacion.startswith("INSERT") or
            operacion.startswith("UPDATE") or
            operacion.startswith("DELETE")
        ):

            ejecutar_transaccion(
                conexiones,
                sql,
                opcion
            )

        else:

            print("\n✗ Instrucción SQL no permitida.")
            print("Solo puede utilizar INSERT, UPDATE o DELETE.")