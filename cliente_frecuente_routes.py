from flask import Blueprint, request, jsonify
from db import connect_db

cliente_frecuente_blueprint = Blueprint('cliente_frecuente', __name__)

# Endpoint para obtener todos los clientes frecuentes
@cliente_frecuente_blueprint.route('/clientes_frecuentes', methods=['GET'])
def get_clientes_frecuentes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ClienteFrecuente')
    clientes_frecuentes = cursor.fetchall()
    conn.close()
    return jsonify({'clientes_frecuentes': clientes_frecuentes})

# Endpoint para agregar un nuevo cliente frecuente
@cliente_frecuente_blueprint.route('/agregar_cliente_frecuente', methods=['POST'])
def agregar_cliente_frecuente():
    data = request.get_json()

    if not data or 'full_name' not in data or 'email' not in data or 'phone_number' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un cliente frecuente'}), 400

    full_name = data['full_name']
    email = data['email']
    phone_number = data['phone_number']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ClienteFrecuente (full_name, email, phone_number) VALUES (%s, %s, %s) RETURNING client_id', (full_name, email, phone_number))
    client_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cliente frecuente agregado exitosamente', 'client_id': client_id})

# Endpoint para editar un cliente frecuente existente
@cliente_frecuente_blueprint.route('/editar_cliente_frecuente/<int:client_id>', methods=['POST'])
def editar_cliente_frecuente(client_id):
    data = request.get_json()

    if not data or 'full_name' not in data or 'email' not in data or 'phone_number' not in data:
        return jsonify({'error': 'Datos incompletos para editar un cliente frecuente'}), 400

    full_name = data['full_name']
    email = data['email']
    phone_number = data['phone_number']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE ClienteFrecuente SET full_name=%s, email=%s, phone_number=%s, updated_at=NOW() WHERE client_id=%s', (full_name, email, phone_number, client_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cliente frecuente editado exitosamente'})

# Endpoint para eliminar un cliente frecuente
@cliente_frecuente_blueprint.route('/eliminar_cliente_frecuente/<int:client_id>', methods=['GET'])
def eliminar_cliente_frecuente(client_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ClienteFrecuente WHERE client_id=%s', (client_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Cliente frecuente eliminado exitosamente'})
