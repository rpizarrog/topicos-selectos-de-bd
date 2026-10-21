from CSQLite import SQLite


# Crear objeto
sqlite = SQLite()


# Crear base de datos
sqlite.f_crear_bd()


# Crear tablas
sqlite.f_crear_tablas()

sqlite.f_mostrar_estructura()


# Cerrar conexión
sqlite.f_cerrar()