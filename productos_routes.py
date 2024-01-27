from flask import Blueprint, request, jsonify
from db import connect_db

productos_blueprint = Blueprint('productos', __name__)

# Endpoint para obtener todos los productos
@productos_blueprint.route('/productos', methods=['GET'])
def get_productos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return jsonify({'productos': productos})

# Endpoint para agregar un nuevo producto
@productos_blueprint.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    data = request.get_json()

    if not data or 'product_name' not in data or 'category_id' not in data or 'stock_quantity' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un producto'}), 400

    product_name = data['product_name']
    category_id = data['category_id']
    stock_quantity = data['stock_quantity']
    owner_id = data['owner_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (product_name, category_id, stock_quantity, owner_id) VALUES (%s, %s, %s, %s) RETURNING product_id', (product_name, category_id, stock_quantity, owner_id))
    product_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Producto agregado exitosamente', 'product_id': product_id})

# Endpoint para editar un producto existente
@productos_blueprint.route('/editar_producto/<int:product_id>', methods=['POST'])
def editar_producto(product_id):
    data = request.get_json()

    if not data or 'product_name' not in data or 'category_id' not in data or 'stock_quantity' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para editar un producto'}), 400

    product_name = data['product_name']
    category_id = data['category_id']
    stock_quantity = data['stock_quantity']
    owner_id = data['owner_id']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE productos SET product_name=%s, category_id=%s, stock_quantity=%s, owner_id=%s, updated_at=NOW() WHERE product_id=%s', (product_name, category_id, stock_quantity, owner_id, product_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Producto editado exitosamente'})

# Endpoint para eliminar un producto
@productos_blueprint.route('/eliminar_producto/<int:product_id>', methods=['GET'])
def eliminar_producto(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE product_id=%s', (product_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Producto eliminado exitosamente'})
