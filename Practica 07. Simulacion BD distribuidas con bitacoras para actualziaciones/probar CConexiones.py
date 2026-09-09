from getpass import getpass
from CConexiones import Conexiones


if __name__ == "__main__":

    print("========================================")
    print("   PRUEBA DE CONEXIONES")
    print("========================================")

    usuario = input("Usuario: ")
    password = getpass("Contraseña: ")

    conexiones = Conexiones(
        usuario=usuario,
        password=password
    )

    # =====================================================
    # PROBAR MYSQL
    # =====================================================
    try:

        conexion_mysql = conexiones.conectar_MySQL()

        print("✓ Conexión MySQL exitosa")

        conexion_mysql.close()

    except Exception as error:

        print("✗ Error de conexión MySQL")
        print(error)


    # =====================================================
    # PROBAR POSTGRESQL
    # =====================================================
    try:

        conexion_postgres = conexiones.conectar_Postgres()

        print("✓ Conexión PostgreSQL exitosa")

        conexion_postgres.close()

    except Exception as error:

        print("✗ Error de conexión PostgreSQL")
        print(error)