from flask import Blueprint, request, jsonify
from db import connect_db

clientes_tienda_blueprint = Blueprint('clientes_tienda', __name__)

# Endpoint para obtener todos los clientes de tienda
@clientes_tienda_blueprint.route('/clientes_tienda', methods=['GET'])
def get_clientes_tienda():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ClientesDeTienda')
    clientes_tienda = cursor.fetchall()
    conn.close()
    return jsonify({'clientes_tienda': clientes_tienda})

# Endpoint para agregar un nuevo cliente de tienda
@clientes_tienda_blueprint.route('/agregar_cliente_tienda', methods=['POST'])
def agregar_cliente_tienda():
    data = request.get_json()

    if not data or 'client_id' not in data or 'store_id' not in data or 'discount_percentage' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un cliente de tienda'}), 400

    client_id = data['client_id']
    store_id = data['store_id']
    discount_percentage = data['discount_percentage']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ClientesDeTienda (client_id, store_id, discount_percentage) VALUES (%s, %s, %s) RETURNING client_de_tienda_id', (client_id, store_id, discount_percentage))
    client_de_tienda_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cliente de tienda agregado exitosamente', 'client_de_tienda_id': client_de_tienda_id})

# Endpoint para editar un cliente de tienda existente
@clientes_tienda_blueprint.route('/editar_cliente_tienda/<int:client_de_tienda_id>', methods=['POST'])
def editar_cliente_tienda(client_de_tienda_id):
    data = request.get_json()

    if not data or 'client_id' not in data or 'store_id' not in data or 'discount_percentage' not in data:
        return jsonify({'error': 'Datos incompletos para editar un cliente de tienda'}), 400

    client_id = data['client_id']
    store_id = data['store_id']
    discount_percentage = data['discount_percentage']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE ClientesDeTienda SET client_id=%s, store_id=%s, discount_percentage=%s, updated_at=NOW() WHERE client_de_tienda_id=%s', (client_id, store_id, discount_percentage, client_de_tienda_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cliente de tienda editado exitosamente'})

# Endpoint para eliminar un cliente de tienda
@clientes_tienda_blueprint.route('/eliminar_cliente_tienda/<int:client_de_tienda_id>', methods=['GET'])
def eliminar_cliente_tienda(client_de_tienda_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ClientesDeTienda WHERE client_de_tienda_id=%s', (client_de_tienda_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cliente de tienda eliminado exitosamente'})
