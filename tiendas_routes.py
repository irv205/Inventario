from flask import Blueprint, request, jsonify
from db import connect_db

tiendas_blueprint = Blueprint('tiendas', __name__)

# Endpoint para obtener todas las tiendas
@tiendas_blueprint.route('/tiendas', methods=['GET'])
def get_tiendas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Tiendas')
    tiendas = cursor.fetchall()
    conn.close()
    return jsonify({'tiendas': tiendas})

# Endpoint para agregar una nueva tienda
@tiendas_blueprint.route('/agregar_tienda', methods=['POST'])
def agregar_tienda():
    data = request.get_json()

    if not data or 'store_name' not in data or 'location' not in data or 'manager_name' not in data or 'manager_contact' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para agregar una tienda'}), 400

    store_name = data['store_name']
    location = data['location']
    manager_name = data['manager_name']
    manager_contact = data['manager_contact']
    owner_id = data['owner_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Tiendas (store_name, location, manager_name, manager_contact, owner_id) VALUES (%s, %s, %s, %s, %s) RETURNING store_id', (store_name, location, manager_name, manager_contact, owner_id))
    store_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Tienda agregada exitosamente', 'store_id': store_id})

# Endpoint para editar una tienda existente
@tiendas_blueprint.route('/editar_tienda/<int:store_id>', methods=['POST'])
def editar_tienda(store_id):
    data = request.get_json()

    if not data or 'store_name' not in data or 'location' not in data or 'manager_name' not in data or 'manager_contact' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para editar una tienda'}), 400

    store_name = data['store_name']
    location = data['location']
    manager_name = data['manager_name']
    manager_contact = data['manager_contact']
    owner_id = data['owner_id']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE Tiendas SET store_name=%s, location=%s, manager_name=%s, manager_contact=%s, owner_id=%s, updated_at=NOW() WHERE store_id=%s', (store_name, location, manager_name, manager_contact, owner_id, store_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Tienda editada exitosamente'})

# Endpoint para eliminar una tienda
@tiendas_blueprint.route('/eliminar_tienda/<int:store_id>', methods=['GET'])
def eliminar_tienda(store_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Tiendas WHERE store_id=%s', (store_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Tienda eliminada exitosamente'})
