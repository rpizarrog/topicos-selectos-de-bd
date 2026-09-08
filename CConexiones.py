import mysql.connector
import psycopg2


class Conexiones:

    # =====================================================
    # CONSTRUCTOR
    # =====================================================
    def __init__(self, usuario, password):
        self.usuario = usuario
        self.password = password

    # =====================================================
    # CONECTAR MYSQL
    # =====================================================
    def conectar_MySQL(self, bd=None):

        conexion = mysql.connector.connect(
            host="localhost",
            port=3306,
            user=self.usuario,
            password=self.password,
            database=bd
        )

        return conexion

    # =====================================================
    # CONECTAR POSTGRESQL
    # =====================================================
    def conectar_Postgres(self, bd="postgres"):

        conexion = psycopg2.connect(
            host="localhost",
            port=5432,
            database=bd,
            user=self.usuario,
            password=self.password
        )

        return conexion

    