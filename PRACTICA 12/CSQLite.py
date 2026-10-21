import sqlite3
import os


class SQLite:

    def __init__(self):

        self.carpeta = "datos"
        self.bd = os.path.join(self.carpeta, "negocios.db")

        self.conexion = None
        self.cursor = None


    # ---------------------------------------------
    # Crear la base de datos
    # ---------------------------------------------
    def f_crear_bd(self):

        # Crear carpeta si no existe
        if not os.path.exists(self.carpeta):
            os.makedirs(self.carpeta)

        # Conectarse crea negocios.db si no existe
        self.conexion = sqlite3.connect(self.bd)

        # Crear cursor
        self.cursor = self.conexion.cursor()

        # Activar llaves foráneas
        self.cursor.execute(
            "PRAGMA foreign_keys = ON;"
        )

        print("Base de datos negocios.db creada correctamente")


    def f_crear_tablas(self):

        # =====================================================
        # TABLA: clientes
        # =====================================================

        self.cursor.execute("""
            CREATE TABLE clientes (
                id_cliente CHAR(13) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                telefono VARCHAR(15),
                correo VARCHAR(100),
                direccion VARCHAR(150),

                CONSTRAINT pk_clientes
                    PRIMARY KEY (id_cliente)
            );
        """)


        # =====================================================
        # TABLA: productos
        # =====================================================

        self.cursor.execute("""
            CREATE TABLE productos (
                id_producto CHAR(20) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                descripcion VARCHAR(200),
                precio DECIMAL(10,2) NOT NULL,
                existencia INTEGER NOT NULL,

                CONSTRAINT pk_productos
                    PRIMARY KEY (id_producto)
            );
        """)


        # =====================================================
        # TABLA: ventas
        # =====================================================

        self.cursor.execute("""
            CREATE TABLE ventas (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                id_cliente CHAR(13) NOT NULL,
                total DECIMAL(10,2),

                CONSTRAINT fk_ventas_clientes
                    FOREIGN KEY (id_cliente)
                    REFERENCES clientes(id_cliente)
            );
        """)


        # =====================================================
        # TABLA: detalle_ventas
        # =====================================================

        self.cursor.execute("""
            CREATE TABLE detalle_ventas (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                id_producto CHAR(20) NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2),

                CONSTRAINT fk_detalle_ventas
                    FOREIGN KEY (id_venta)
                    REFERENCES ventas(id_venta),

                CONSTRAINT fk_detalle_productos
                    FOREIGN KEY (id_producto)
                    REFERENCES productos(id_producto)
            );
        """)


        # =====================================================
        # GUARDAR CAMBIOS
        # =====================================================

        self.conexion.commit()

        print("Tablas creadas correctamente")
    
    def f_mostrar_estructura(self):

        tablas = [
            "clientes",
            "productos",
            "ventas",
            "detalle_ventas"
        ]

        for tabla in tablas:

            print("\nTABLA:", tabla)
            print("-" * 50)

            self.cursor.execute(
                f"PRAGMA table_info({tabla});"
            )

            columnas = self.cursor.fetchall()

            for columna in columnas:
                print(columna)


    def f_cerrar(self):

        if self.conexion:
            self.conexion.close()

            print("Conexión SQLite cerrada")