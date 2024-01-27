from flask import Blueprint, request, jsonify
from db import connect_db

inventario_entrante_blueprint = Blueprint('inventario_entrante', __name__)

# Endpoint para obtener todos los registros de inventario entrante
@inventario_entrante_blueprint.route('/inventario_entrante', methods=['GET'])
def get_inventario_entrante():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM InventarioEntrante')
    inventario_entrante = cursor.fetchall()
    conn.close()
    return jsonify({'inventario_entrante': inventario_entrante})

# Endpoint para agregar un nuevo registro de inventario entrante
@inventario_entrante_blueprint.route('/agregar_inventario_entrante', methods=['POST'])
def agregar_inventario_entrante():
    data = request.get_json()

    if not data or 'product_id' not in data or 'quantity' not in data or 'entry_date' not in data or 'supplier_id' not in data or 'price' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un registro de inventario entrante'}), 400

    product_id = data['product_id']
    quantity = data['quantity']
    entry_date = data['entry_date']
    supplier_id = data['supplier_id']
    price = data['price']
    owner_id = data['owner_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO InventarioEntrante (product_id, quantity, entry_date, supplier_id, price, owner_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING entry_id', (product_id, quantity, entry_date, supplier_id, price, owner_id))
    entry_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de inventario entrante agregado exitosamente', 'entry_id': entry_id})

# Endpoint para editar un registro de inventario entrante existente
@inventario_entrante_blueprint.route('/editar_inventario_entrante/<int:entry_id>', methods=['POST'])
def editar_inventario_entrante(entry_id):
    data = request.get_json()

    if not data or 'product_id' not in data or 'quantity' not in data or 'entry_date' not in data or 'supplier_id' not in data or 'price' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para editar un registro de inventario entrante'}), 400

    product_id = data['product_id']
    quantity = data['quantity']
    entry_date = data['entry_date']
    supplier_id = data['supplier_id']
    price = data['price']
    owner_id = data['owner_id']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE InventarioEntrante SET product_id=%s, quantity=%s, entry_date=%s, supplier_id=%s, price=%s, owner_id=%s, updated_at=NOW() WHERE entry_id=%s', (product_id, quantity, entry_date, supplier_id, price, owner_id, entry_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de inventario entrante editado exitosamente'})

# Endpoint para eliminar un registro de inventario entrante
@inventario_entrante_blueprint.route('/eliminar_inventario_entrante/<int:entry_id>', methods=['GET'])
def eliminar_inventario_entrante(entry_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM InventarioEntrante WHERE entry_id=%s', (entry_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de inventario entrante eliminado exitosamente'})
