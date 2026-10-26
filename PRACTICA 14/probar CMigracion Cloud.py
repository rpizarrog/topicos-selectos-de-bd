from CMigracionCloud import Migracion



# Crear objeto
migracion = Migracion()


# Conectar a SQLite local
migracion.f_conectar_sqlite()


# Leer clientes
clientes = migracion.f_leer_clientes_sqlite()
productos = migracion.f_leer_productos_sqlite()
ventas = migracion.f_leer_ventas_sqlite()
detalle_ventas = migracion.f_leer_detalle_ventas_sqlite()


# Mostrar clientes
print("\nCLIENTES DE SQLITE LOCAL")
print("-" * 70)

for cliente in clientes:
    print(cliente)


# Mostrar cantidad
print("\nTotal de clientes:", len(clientes))

# Mostrar productos
print("\nPRODUCTOS DE SQLITE LOCAL")
print("-" * 70)

for producto in productos:
    print(producto)


# Mostrar cantidad
print("\nTotal de PRODUCTOS:", len(productos))


# Mostrar ventas
print("\nVENTAS DE SQLITE LOCAL")
print("-" * 70)

for venta in ventas:
    print(venta)

# Mostrar cantidad
print("\nTotal de VENTAS:", len(ventas))


# Mostrar detalle_ventas
print("\nDETALLE_VENTAS DE SQLITE LOCAL")
print("-" * 70)

for detalle_venta in detalle_ventas:
    print(detalle_venta)


# Mostrar cantidad
print("\nTotal de DETALLE_VENTAS:", len(detalle_ventas))




# Cerrar SQLite
migracion.f_cerrar_sqlite()

migracion.f_conectar_cloudflare()





migracion.f_agregar_clientes_cloudflare(clientes)
migracion.f_agregar_productos_cloudflare(productos)
migracion.f_agregar_ventas_cloudflare (ventas)
migracion.f_agregar_detalle_ventas_cloudflare(detalle_ventas)


print("TERMINAMOS LA MIGRACION revisar registros en CloudFlare")
