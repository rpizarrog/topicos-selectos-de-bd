# CMigracionCloud.py

import sqlite3
import os


from dotenv import load_dotenv
from cloudflare import Cloudflare



class Migracion:

    def __init__(self):

        # ---------------------------------------------
        # SQLite local
        # ---------------------------------------------
        self.carpeta = "datos"
        self.bd_sqlite = os.path.join(
            self.carpeta,
            "negocios.db"
        )

        self.conexion_sqlite = None
        self.cursor_sqlite = None

        # ---------------------------------------------
        # Cloudflare
        # ---------------------------------------------
        load_dotenv()

        self.api_token = os.getenv("API_TOKEN")
        self.account_id = os.getenv("ACCOUNT_ID")
        self.database_id = os.getenv("DATABASE_ID")

        self.cliente_cloudflare = None


    # -------------------------------------------------
    # CONECTAR SQLITE LOCAL
    # -------------------------------------------------
    def f_conectar_sqlite(self):

        self.conexion_sqlite = sqlite3.connect(
            self.bd_sqlite
        )

        self.cursor_sqlite = (
            self.conexion_sqlite.cursor()
        )

        self.cursor_sqlite.execute(
            "PRAGMA foreign_keys = ON;"
        )

        print(
            "Conexión a SQLite local realizada correctamente"
        )

    # -------------------------------------------------
    # CONECTAR CLOUDFLARE
    # -------------------------------------------------
    def f_conectar_cloudflare(self):

        self.cliente_cloudflare = Cloudflare(
            api_token=self.api_token
        )

        print(
            "Conexión a Cloudflare configurada correctamente"
        )

    # -------------------------------------------------
    # LEER CLIENTES DE SQLITE LOCAL
    # -------------------------------------------------
    def f_leer_clientes_sqlite(self):

        sql = """
            SELECT
                id_cliente,
                nombre,
                telefono,
                correo,
                direccion
            FROM clientes
            ORDER BY id_cliente
        """

        self.cursor_sqlite.execute(sql)

        clientes = self.cursor_sqlite.fetchall()

        return clientes

    # -------------------------------------------------
    # AGREGAR CLIENTES A CLOUDFLARE
    # -------------------------------------------------
    def f_agregar_clientes_cloudflare(
        self,
        clientes
    ):

        sql = """
            INSERT INTO clientes
            (
                id_cliente,
                nombre,
                telefono,
                correo,
                direccion
            )
            VALUES (?, ?, ?, ?, ?)
        """

        for cliente in clientes:

            parametros = [
                cliente[0],
                cliente[1],
                cliente[2],
                cliente[3],
                cliente[4]
            ]

            self.cliente_cloudflare.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql=sql,
                params=parametros
            )

        print(
            len(clientes),
            "clientes agregados a Cloudflare D1"
        )

    # -------------------------------------------------
    # LEER PRODUCTOS DE SQLITE LOCAL
    # -------------------------------------------------
    def f_leer_productos_sqlite(self):

        sql = """
            SELECT
                id_producto,
                nombre,
                descripcion,
                precio,
                existencia
            FROM productos
            ORDER BY id_producto
        """

        self.cursor_sqlite.execute(sql)

        productos = self.cursor_sqlite.fetchall()

        return productos


    # -------------------------------------------------
    # AGREGAR PRODUCTOS A CLOUDFLARE
    # -------------------------------------------------
    def f_agregar_productos_cloudflare(
        self,
        productos
    ):

        sql = """
            INSERT INTO productos
            (
                id_producto,
                nombre,
                descripcion,
                precio,
                existencia
            )
            VALUES (?, ?, ?, ?, ?)
        """

        for producto in productos:

            parametros = [
                producto[0],
                producto[1],
                producto[2],
                producto[3],
                producto[4]
            ]

            self.cliente_cloudflare.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql=sql,
                params=parametros
            )

        print(
            len(productos),
            "productos agregados a Cloudflare D1"
        )

    # -------------------------------------------------
    # LEER VENTAS DE SQLITE LOCAL
    # -------------------------------------------------
    def f_leer_ventas_sqlite(self):

        sql = """
            SELECT
                id_venta,
                fecha,
                id_cliente,
                total
            FROM ventas
            ORDER BY id_venta
        """

        self.cursor_sqlite.execute(sql)

        ventas = self.cursor_sqlite.fetchall()

        return ventas


    # -------------------------------------------------
    # AGREGAR VENTAS A CLOUDFLARE
    # -------------------------------------------------
    def f_agregar_ventas_cloudflare(
        self,
        ventas
    ):

        sql = """
            INSERT INTO ventas
            (
                id_venta,
                fecha,
                id_cliente,
                total
            )
            VALUES (?, ?, ?, ?)
        """

        for venta in ventas:

            parametros = [
                venta[0],
                venta[1],
                venta[2],
                venta[3]
            ]

            self.cliente_cloudflare.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql=sql,
                params=parametros
            )

        print(
            len(ventas),
            "ventas agregadas a Cloudflare D1"
        )


    # -------------------------------------------------
    # LEER DETALLE DE VENTAS DE SQLITE LOCAL
    # -------------------------------------------------
    def f_leer_detalle_ventas_sqlite(self):

        sql = """
            SELECT
                id_detalle,
                id_venta,
                id_producto,
                cantidad,
                precio_unitario,
                subtotal
            FROM detalle_ventas
            ORDER BY id_detalle
        """

        self.cursor_sqlite.execute(sql)

        detalle_ventas = self.cursor_sqlite.fetchall()

        return detalle_ventas


    # -------------------------------------------------
    # AGREGAR DETALLE DE VENTAS A CLOUDFLARE
    # -------------------------------------------------
    def f_agregar_detalle_ventas_cloudflare(
        self,
        detalle_ventas
    ):

        sql = """
            INSERT INTO detalle_ventas
            (
                id_detalle,
                id_venta,
                id_producto,
                cantidad,
                precio_unitario,
                subtotal
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        for detalle in detalle_ventas:

            parametros = [
                detalle[0],
                detalle[1],
                detalle[2],
                detalle[3],
                detalle[4],
                detalle[5]
            ]

            self.cliente_cloudflare.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql=sql,
                params=parametros
            )

        print(
            len(detalle_ventas),
            "detalles de ventas agregados a Cloudflare D1"
        )


    # -------------------------------------------------
    # CERRAR SQLITE
    # -------------------------------------------------
    def f_cerrar_sqlite(self):

        if self.cursor_sqlite:
            self.cursor_sqlite.close()

        if self.conexion_sqlite:
            self.conexion_sqlite.close()

        print(
            "Conexión a SQLite local cerrada"
        )