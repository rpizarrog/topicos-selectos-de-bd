from CMigracion import Migracion

migracion = Migracion()

# =============================================
# 1. LEER CLIENTES DE MYSQL
# =============================================

migracion.f_conectar_mysql("rpizarro", "rpizarro", "negocios")

clientes = migracion.f_leer_clientes_mysql()
productos = migracion.f_leer_productos_mysql()
ventas = migracion.f_leer_ventas_mysql()
detalle_ventas = migracion.f_leer_detalle_ventas_mysql()

print("\Clientes encontrados en MySQL:")

for cliente in clientes:
    print(cliente)

print("\Productos encontrados en MySQL:")
for producto in productos:
    print(producto)

print("\Ventas encontradas en MySQL:")
for venta in ventas:
    print(venta)

print("\DetalleVentas encontradas en MySQL:")
for detalle_venta in detalle_ventas:
    print(detalle_venta)

migracion.f_cerrar_mysql()

migracion.f_conectar_sqlite()


# =============================================
# 2. MIGRAR CLIENTES A SQLITE
# =============================================

migracion.f_agregar_clientes_sqlite(clientes)

# =============================================
# 3. MIGRAR PRODUCTIOS A SQLITE
# =============================================

migracion.f_agregar_productos_sqlite(productos)

# =============================================
# 3. MIGRAR VENTAS A SQLITE
# =============================================
migracion.f_agregar_ventas_sqlite(ventas)

# =============================================
# 4. MIGRAR DETALLEVENTAS A SQLITE
# =============================================
migracion.f_agregar_detalle_ventas_sqlite(detalle_ventas)

migracion.f_cerrar_sqlite()