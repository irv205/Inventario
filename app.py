from flask import Flask
from acciones_rol_routes import acciones_rol_blueprint
from roles_routes import roles_blueprint
from trabajadores_routes import trabajadores_blueprint
from cliente_frecuente_routes import cliente_frecuente_blueprint
from clientes_tienda_routes import clientes_tienda_blueprint
from purchase_history_routes import purchase_history_blueprint
from productos_routes import productos_blueprint
from product_images_routes import product_images_blueprint
from categorias_routes import categorias_blueprint
from proveedores_routes import proveedores_blueprint
from inventario_entrante_routes import inventario_entrante_blueprint
from inventario_saliente_routes import inventario_saliente_blueprint
from tiendas_routes import tiendas_blueprint
from punto_venta_routes import punto_venta_blueprint
from db import connect_db

app = Flask(__name__)
app.register_blueprint(acciones_rol_blueprint)
app.register_blueprint(roles_blueprint)
app.register_blueprint(trabajadores_blueprint)
app.register_blueprint(cliente_frecuente_blueprint)
app.register_blueprint(clientes_tienda_blueprint)
app.register_blueprint(purchase_history_blueprint)
app.register_blueprint(productos_blueprint)
app.register_blueprint(product_images_blueprint)
app.register_blueprint(categorias_blueprint)
app.register_blueprint(proveedores_blueprint)
app.register_blueprint(inventario_entrante_blueprint)
app.register_blueprint(inventario_saliente_blueprint)
app.register_blueprint(tiendas_blueprint)
app.register_blueprint(punto_venta_blueprint)

# Crear la conexión a la base de datos
db_connection = connect_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
