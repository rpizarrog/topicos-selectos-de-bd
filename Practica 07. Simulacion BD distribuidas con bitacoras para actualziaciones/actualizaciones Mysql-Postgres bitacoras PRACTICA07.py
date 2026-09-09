from getpass import getpass
from datetime import datetime
import json
from CConexiones import Conexiones

BITACORA_MYSQL = "bitacora_caidas_mysql.txt"
BITACORA_POSTGRES = "bitacora_caidas_postgres.txt"

def guardar_bitacora(archivo, destino, sql):
    registro = {
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "destino": destino,
        "sql": sql
    }
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

def verificar_mysql(conexiones):
    conexion = None
    try:
        conexion = conexiones.conectar_MySQL("negocios")
        return True
    except Exception:
        return False
    finally:
        if conexion is not None:
            try: conexion.close()
            except Exception: pass

def verificar_postgres(conexiones):
    conexion = None
    try:
        conexion = conexiones.conectar_Postgres("negocios")
        return True
    except Exception:
        return False
    finally:
        if conexion is not None:
            try: conexion.close()
            except Exception: pass

def ejecutar_solo_mysql(conexiones, sql):
    conexion = cursor = None
    try:
        conexion = conexiones.conectar_MySQL("negocios")
        cursor = conexion.cursor()
        conexion.start_transaction()
        cursor.execute(sql)
        conexion.commit()
        print("✓ Operación realizada en MySQL")
        print("✓ COMMIT realizado en MySQL")
        return True
    except Exception as error:
        if conexion is not None:
            try:
                conexion.rollback()
                print("↩ ROLLBACK realizado en MySQL")
            except Exception: pass
        print("\n✗ Error en MySQL:", error)
        return False
    finally:
        if cursor is not None:
            try: cursor.close()
            except Exception: pass
        if conexion is not None:
            try: conexion.close()
            except Exception: pass

def ejecutar_solo_postgres(conexiones, sql):
    conexion = cursor = None
    try:
        conexion = conexiones.conectar_Postgres("negocios")
        cursor = conexion.cursor()
        # psycopg2 inicia la transacción con la primera instrucción
        cursor.execute(sql)
        conexion.commit()
        print("✓ Operación realizada en PostgreSQL")
        print("✓ COMMIT realizado en PostgreSQL")
        return True
    except Exception as error:
        if conexion is not None:
            try:
                conexion.rollback()
                print("↩ ROLLBACK realizado en PostgreSQL")
            except Exception: pass
        print("\n✗ Error en PostgreSQL:", error)
        return False
    finally:
        if cursor is not None:
            try: cursor.close()
            except Exception: pass
        if conexion is not None:
            try: conexion.close()
            except Exception: pass

def ejecutar_en_ambos(conexiones, sql):
    conexion_mysql = conexion_postgres = None
    cursor_mysql = cursor_postgres = None
    mysql_commit = postgres_commit = False

    try:
        conexion_mysql = conexiones.conectar_MySQL("negocios")
        conexion_postgres = conexiones.conectar_Postgres("negocios")
        cursor_mysql = conexion_mysql.cursor()
        cursor_postgres = conexion_postgres.cursor()

        # Transacciones locales; todavía no se confirma ninguna.
        conexion_mysql.start_transaction()

        cursor_mysql.execute(sql)
        print("✓ MySQL aceptó la operación")

        # psycopg2 inicia aquí su transacción local.
        cursor_postgres.execute(sql)
        print("✓ PostgreSQL aceptó la operación")

        # Ambos aceptaron: confirmar.
        conexion_mysql.commit()
        mysql_commit = True
        print("✓ COMMIT realizado en MySQL")

        conexion_postgres.commit()
        postgres_commit = True
        print("✓ COMMIT realizado en PostgreSQL")

        print("\n========================================")
        print("      TRANSACCIÓN COORDINADA EXITOSA")
        print("========================================")
        print("✓ MySQL actualizado")
        print("✓ PostgreSQL actualizado")
        print("✓ No se generó operación pendiente")
        return True

    except Exception as error:
        print("\n========================================")
        print("        ERROR EN LA TRANSACCIÓN")
        print("========================================")
        print(error)

        if conexion_mysql is not None and not mysql_commit:
            try:
                conexion_mysql.rollback()
                print("↩ ROLLBACK realizado en MySQL")
            except Exception: pass

        if conexion_postgres is not None and not postgres_commit:
            try:
                conexion_postgres.rollback()
                print("↩ ROLLBACK realizado en PostgreSQL")
            except Exception: pass

        # Si un COMMIT alcanzó a realizarse y el otro no,
        # conservar la operación como pendiente para recuperación.
        if mysql_commit and not postgres_commit:
            guardar_bitacora(BITACORA_POSTGRES, "PostgreSQL", sql)
            print("⚠ Operación pendiente registrada para PostgreSQL.")
        elif postgres_commit and not mysql_commit:
            guardar_bitacora(BITACORA_MYSQL, "MySQL", sql)
            print("⚠ Operación pendiente registrada para MySQL.")

        return False
    finally:
        for cursor in (cursor_mysql, cursor_postgres):
            if cursor is not None:
                try: cursor.close()
                except Exception: pass
        for conexion in (conexion_mysql, conexion_postgres):
            if conexion is not None:
                try: conexion.close()
                except Exception: pass

def actualizacion_distribuida(conexiones, sql):
    mysql_activo = verificar_mysql(conexiones)
    postgres_activo = verificar_postgres(conexiones)

    print("\n========================================")
    print("       ESTADO DE LOS SERVICIOS")
    print("========================================")
    print("✓ MySQL disponible" if mysql_activo else "✗ MySQL detenido o no disponible")
    print("✓ PostgreSQL disponible" if postgres_activo else "✗ PostgreSQL detenido o no disponible")

    if mysql_activo and postgres_activo:
        print("\nAmbos servicios están disponibles.")
        print("Ejecutando transacción coordinada...")
        ejecutar_en_ambos(conexiones, sql)

    elif mysql_activo and not postgres_activo:
        print("\nPostgreSQL está detenido.")
        print("La operación continuará en MySQL.")
        if ejecutar_solo_mysql(conexiones, sql):
            guardar_bitacora(BITACORA_POSTGRES, "PostgreSQL", sql)
            print("\n✓ MySQL quedó actualizado")
            print("⚠ PostgreSQL quedó pendiente")
            print(f"✓ Pendiente guardado en {BITACORA_POSTGRES}")

    elif not mysql_activo and postgres_activo:
        print("\nMySQL está detenido.")
        print("La operación continuará en PostgreSQL.")
        if ejecutar_solo_postgres(conexiones, sql):
            guardar_bitacora(BITACORA_MYSQL, "MySQL", sql)
            print("\n✓ PostgreSQL quedó actualizado")
            print("⚠ MySQL quedó pendiente")
            print(f"✓ Pendiente guardado en {BITACORA_MYSQL}")

    else:
        print("\n========================================")
        print("       OPERACIÓN NO DISPONIBLE")
        print("========================================")
        print("✗ MySQL está detenido")
        print("✗ PostgreSQL está detenido")
        print("La operación NO fue realizada.")
        print("No se agregó ninguna operación a las bitácoras.")

if __name__ == "__main__":
    print("========================================")
    print("      ACTUALIZACIONES DISTRIBUIDAS")
    print("         MySQL - PostgreSQL")
    print("             PRACTICA 07")
    print("========================================")

    usuario = input("\nUsuario: ")
    password = getpass("Contraseña: ")
    conexiones = Conexiones(usuario=usuario, password=password)

    print("\nEscriba la instrucción SQL.")
    print("Operaciones permitidas: INSERT, UPDATE o DELETE")
    sql = input("\nSQL > ").strip()
    operacion = sql.upper()

    if operacion.startswith(("INSERT", "UPDATE", "DELETE")):
        actualizacion_distribuida(conexiones, sql)
    else:
        print("\n✗ Solo se permiten INSERT, UPDATE o DELETE.")
