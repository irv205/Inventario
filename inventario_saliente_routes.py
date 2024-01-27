from flask import Blueprint, request, jsonify
from db import connect_db

inventario_saliente_blueprint = Blueprint('inventario_saliente', __name__)

# Endpoint para obtener todos los registros de inventario saliente
@inventario_saliente_blueprint.route('/inventario_saliente', methods=['GET'])
def get_inventario_saliente():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM InventarioSaliente')
    inventario_saliente = cursor.fetchall()
    conn.close()
    return jsonify({'inventario_saliente': inventario_saliente})

# Endpoint para agregar un nuevo registro de inventario saliente
@inventario_saliente_blueprint.route('/agregar_inventario_saliente', methods=['POST'])
def agregar_inventario_saliente():
    data = request.get_json()

    if not data or 'product_id' not in data or 'quantity' not in data or 'store_id' not in data or 'exit_date' not in data or 'price' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un registro de inventario saliente'}), 400

    product_id = data['product_id']
    quantity = data['quantity']
    store_id = data['store_id']
    exit_date = data['exit_date']
    price = data['price']
    owner_id = data['owner_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO InventarioSaliente (product_id, quantity, store_id, exit_date, price, owner_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING exit_id', (product_id, quantity, store_id, exit_date, price, owner_id))
    exit_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de inventario saliente agregado exitosamente', 'exit_id': exit_id})

# Endpoint para editar un registro de inventario saliente existente
@inventario_saliente_blueprint.route('/editar_inventario_saliente/<int:exit_id>', methods=['POST'])
def editar_inventario_saliente(exit_id):
    data = request.get_json()

    if not data or 'product_id' not in data or 'quantity' not in data or 'store_id' not in data or 'exit_date' not in data or 'price' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para editar un registro de inventario saliente'}), 400

    product_id = data['product_id']
    quantity = data['quantity']
    store_id = data['store_id']
    exit_date = data['exit_date']
    price = data['price']
    owner_id = data['owner_id']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE InventarioSaliente SET product_id=%s, quantity=%s, store_id=%s, exit_date=%s, price=%s, owner_id=%s, updated_at=NOW() WHERE exit_id=%s', (product_id, quantity, store_id, exit_date, price, owner_id, exit_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de inventario saliente editado exitosamente'})

# Endpoint para eliminar un registro de inventario saliente
@inventario_saliente_blueprint.route('/eliminar_inventario_saliente/<int:exit_id>', methods=['GET'])
def eliminar_inventario_saliente(exit_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM InventarioSaliente WHERE exit_id=%s', (exit_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de inventario saliente eliminado exitosamente'})
