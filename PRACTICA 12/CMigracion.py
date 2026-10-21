import mysql.connector
import sqlite3
import os


class Migracion:

    def __init__(self):

        # MySQL
        self.conexion_mysql = None
        self.cursor_mysql = None

        # SQLite
        self.carpeta = "datos"

        self.bd_sqlite = os.path.join(
            self.carpeta,
            "negocios.db"
        )

        self.conexion_sqlite = None
        self.cursor_sqlite = None
        
    # -------------------------------------------------
    # CONECTAR A MYSQL
    # -------------------------------------------------
    def f_conectar_mysql(self, usuario, contrasenia, bd):

        self.conexion_mysql = mysql.connector.connect(
            host="localhost",
            user=usuario,
            password=contrasenia,
            database=bd
        )

        self.cursor_mysql = self.conexion_mysql.cursor()

        print("Conexión a MySQL realizada correctamente")


    # -------------------------------------------------
    # LEER CLIENTES DE MYSQL
    # -------------------------------------------------
    def f_leer_clientes_mysql(self):

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

        self.cursor_mysql.execute(sql)

        clientes = self.cursor_mysql.fetchall()

        return clientes


    # -------------------------------------------------
    # CERRAR MYSQL
    # -------------------------------------------------
    def f_cerrar_mysql(self):

        if self.cursor_mysql:
            self.cursor_mysql.close()

        if self.conexion_mysql:
            self.conexion_mysql.close()

        print("Conexión a MySQL cerrada")

    # -------------------------------------------------
    # CONECTAR A SQLITE
    # -------------------------------------------------
    def f_conectar_sqlite(self):

        self.conexion_sqlite = sqlite3.connect(
            self.bd_sqlite
        )

        self.cursor_sqlite = (
            self.conexion_sqlite.cursor()
        )

        # Activar llaves foráneas
        self.cursor_sqlite.execute(
            "PRAGMA foreign_keys = ON;"
        )

        print(
            "Conexión a SQLite realizada correctamente"
        )

        # -------------------------------------------------
    # AGREGAR CLIENTES A SQLITE
    # -------------------------------------------------
    def f_agregar_clientes_sqlite(self, clientes):

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

        self.cursor_sqlite.executemany(
            sql,
            clientes
        )

        self.conexion_sqlite.commit()

        print(
            len(clientes),
            "clientes agregados a SQLite"
        )


    # -------------------------------------------------
    # LEER PRODUCTOS DE MYSQL
    # -------------------------------------------------
    def f_leer_productos_mysql(self):

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

        self.cursor_mysql.execute(sql)

        productos = self.cursor_mysql.fetchall()

        return productos

    def f_agregar_productos_sqlite(self, productos):

        productos_sqlite = []

        for producto in productos:

            id_producto = producto[0]
            nombre = producto[1]
            descripcion = producto[2]
            precio = float(producto[3])
            existencia = producto[4]

            productos_sqlite.append(
                (
                    id_producto,
                    nombre,
                    descripcion,
                    precio,
                    existencia
                )
            )

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

        self.cursor_sqlite.executemany(
            sql,
            productos_sqlite
        )

        self.conexion_sqlite.commit()

        print(
            len(productos_sqlite),
            "productos agregados a SQLite"
        )


    # -------------------------------------------------
    # LEER VENTAS DE MYSQL
    # -------------------------------------------------
    def f_leer_ventas_mysql(self):

        sql = """
            SELECT
                id_venta,
                fecha,
                id_cliente,
                total
            FROM ventas
            ORDER BY id_venta
        """

        self.cursor_mysql.execute(sql)

        ventas = self.cursor_mysql.fetchall()

        return ventas


    # -------------------------------------------------
    # AGREGAR VENTAS A SQLITE
    # -------------------------------------------------
    def f_agregar_ventas_sqlite(self, ventas):

        ventas_sqlite = []

        for venta in ventas:

            id_venta = venta[0]
            fecha = venta[1]
            id_cliente = venta[2]

            # Convertir Decimal de MySQL a float
            if venta[3] is not None:
                total = float(venta[3])
            else:
                total = None

            ventas_sqlite.append(
                (
                    id_venta,
                    fecha,
                    id_cliente,
                    total
                )
            )


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

        self.cursor_sqlite.executemany(
            sql,
            ventas_sqlite
        )

        self.conexion_sqlite.commit()

        print(
            len(ventas_sqlite),
            "ventas agregadas a SQLite"
        )


    # -------------------------------------------------
    # LEER DETALLE DE VENTAS DE MYSQL
    # -------------------------------------------------
    def f_leer_detalle_ventas_mysql(self):

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

        self.cursor_mysql.execute(sql)

        detalle_ventas = self.cursor_mysql.fetchall()

        return detalle_ventas


    # -------------------------------------------------
    # AGREGAR DETALLE DE VENTAS A SQLITE
    # -------------------------------------------------
    def f_agregar_detalle_ventas_sqlite(
        self,
        detalle_ventas
    ):

        detalle_ventas_sqlite = []

        for detalle in detalle_ventas:

            id_detalle = detalle[0]
            id_venta = detalle[1]
            id_producto = detalle[2]
            cantidad = detalle[3]

            # Convertir DECIMAL de MySQL a float
            if detalle[4] is not None:
                precio_unitario = float(detalle[4])
            else:
                precio_unitario = None

            # Convertir DECIMAL de MySQL a float
            if detalle[5] is not None:
                subtotal = float(detalle[5])
            else:
                subtotal = None

            detalle_ventas_sqlite.append(
                (
                    id_detalle,
                    id_venta,
                    id_producto,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
            )


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

        self.cursor_sqlite.executemany(
            sql,
            detalle_ventas_sqlite
        )

        self.conexion_sqlite.commit()

        print(
            len(detalle_ventas_sqlite),
            "detalles de ventas agregados a SQLite"
        )
    # -------------------------------------------------
    # CERRAR SQLITE
    # -------------------------------------------------
    def f_cerrar_sqlite(self):

        if self.cursor_sqlite:
            self.cursor_sqlite.close()

        if self.conexion_sqlite:
            self.conexion_sqlite.close()

        print("Conexión a SQLite cerrada")