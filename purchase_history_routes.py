from flask import Blueprint, request, jsonify
from db import connect_db

purchase_history_blueprint = Blueprint('purchase_history', __name__)

# Endpoint para obtener todas las compras
@purchase_history_blueprint.route('/compras', methods=['GET'])
def get_compras():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PurchaseHistory')
    compras = cursor.fetchall()
    conn.close()
    return jsonify({'compras': compras})

# Endpoint para agregar una nueva compra
@purchase_history_blueprint.route('/agregar_compra', methods=['POST'])
def agregar_compra():
    data = request.get_json()

    if not data or 'client_id' not in data or 'product_id' not in data or 'quantity' not in data or 'total_amount' not in data or 'purchase_date' not in data:
        return jsonify({'error': 'Datos incompletos para agregar una compra'}), 400

    client_id = data['client_id']
    product_id = data['product_id']
    quantity = data['quantity']
    total_amount = data['total_amount']
    purchase_date = data['purchase_date']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PurchaseHistory (client_id, product_id, quantity, total_amount, purchase_date) VALUES (%s, %s, %s, %s, %s) RETURNING purchase_id', (client_id, product_id, quantity, total_amount, purchase_date))
    purchase_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Compra agregada exitosamente', 'purchase_id': purchase_id})

# Endpoint para editar una compra existente
@purchase_history_blueprint.route('/editar_compra/<int:purchase_id>', methods=['POST'])
def editar_compra(purchase_id):
    data = request.get_json()

    if not data or 'client_id' not in data or 'product_id' not in data or 'quantity' not in data or 'total_amount' not in data or 'purchase_date' not in data:
        return jsonify({'error': 'Datos incompletos para editar una compra'}), 400

    client_id = data['client_id']
    product_id = data['product_id']
    quantity = data['quantity']
    total_amount = data['total_amount']
    purchase_date = data['purchase_date']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE PurchaseHistory SET client_id=%s, product_id=%s, quantity=%s, total_amount=%s, purchase_date=%s, updated_at=NOW() WHERE purchase_id=%s', (client_id, product_id, quantity, total_amount, purchase_date, purchase_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Compra editada exitosamente'})

# Endpoint para eliminar una compra
@purchase_history_blueprint.route('/eliminar_compra/<int:purchase_id>', methods=['GET'])
def eliminar_compra(purchase_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM PurchaseHistory WHERE purchase_id=%s', (purchase_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Compra eliminada exitosamente'})
