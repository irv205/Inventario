from flask import Blueprint, request, jsonify
from db import connect_db

punto_venta_blueprint = Blueprint('punto_venta', __name__)

# Endpoint para obtener todos los registros de punto de venta
@punto_venta_blueprint.route('/punto_venta', methods=['GET'])
def get_punto_venta():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PuntoDeVenta')
    punto_venta = cursor.fetchall()
    conn.close()
    return jsonify({'punto_venta': punto_venta})

# Endpoint para agregar un nuevo registro de punto de venta
@punto_venta_blueprint.route('/agregar_punto_venta', methods=['POST'])
def agregar_punto_venta():
    data = request.get_json()

    if not data or 'store_id' not in data or 'product_id' not in data or 'quantity_sold' not in data or 'total_amount' not in data or 'sale_date' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un registro de punto de venta'}), 400

    store_id = data['store_id']
    product_id = data['product_id']
    quantity_sold = data['quantity_sold']
    total_amount = data['total_amount']
    sale_date = data['sale_date']
    owner_id = data['owner_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PuntoDeVenta (store_id, product_id, quantity_sold, total_amount, sale_date, owner_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING sale_id', (store_id, product_id, quantity_sold, total_amount, sale_date, owner_id))
    sale_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de punto de venta agregado exitosamente', 'sale_id': sale_id})

# Endpoint para editar un registro de punto de venta existente
@punto_venta_blueprint.route('/editar_punto_venta/<int:sale_id>', methods=['POST'])
def editar_punto_venta(sale_id):
    data = request.get_json()

    if not data or 'store_id' not in data or 'product_id' not in data or 'quantity_sold' not in data or 'total_amount' not in data or 'sale_date' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para editar un registro de punto de venta'}), 400

    store_id = data['store_id']
    product_id = data['product_id']
    quantity_sold = data['quantity_sold']
    total_amount = data['total_amount']
    sale_date = data['sale_date']
    owner_id = data['owner_id']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE PuntoDeVenta SET store_id=%s, product_id=%s, quantity_sold=%s, total_amount=%s, sale_date=%s, owner_id=%s, updated_at=NOW() WHERE sale_id=%s', (store_id, product_id, quantity_sold, total_amount, sale_date, owner_id, sale_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de punto de venta editado exitosamente'})

# Endpoint para eliminar un registro de punto de venta
@punto_venta_blueprint.route('/eliminar_punto_venta/<int:sale_id>', methods=['GET'])
def eliminar_punto_venta(sale_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM PuntoDeVenta WHERE sale_id=%s', (sale_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registro de punto de venta eliminado exitosamente'})
