from flask import Blueprint, request, jsonify
from db import connect_db

trabajadores_blueprint = Blueprint('trabajadores', __name__)

# Endpoint para obtener todos los trabajadores
@trabajadores_blueprint.route('/trabajadores', methods=['GET'])
def get_trabajadores():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Trabajadores')
    trabajadores = cursor.fetchall()
    conn.close()
    return jsonify({'trabajadores': trabajadores})

# Endpoint para agregar un nuevo trabajador
@trabajadores_blueprint.route('/agregar_trabajador', methods=['POST'])
def agregar_trabajador():
    data = request.get_json()

    if not data or 'full_name' not in data or 'email' not in data or 'phone_number' not in data or 'role_id' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un trabajador'}), 400

    full_name = data['full_name']
    email = data['email']
    phone_number = data['phone_number']
    role_id = data['role_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Trabajadores (full_name, email, phone_number, role_id) VALUES (%s, %s, %s, %s) RETURNING worker_id', (full_name, email, phone_number, role_id))
    worker_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Trabajador agregado exitosamente', 'worker_id': worker_id})

# Endpoint para editar un trabajador existente
@trabajadores_blueprint.route('/editar_trabajador/<int:worker_id>', methods=['POST'])
def editar_trabajador(worker_id):
    data = request.get_json()

    if not data or 'full_name' not in data or 'email' not in data or 'phone_number' not in data or 'role_id' not in data:
        return jsonify({'error': 'Datos incompletos para editar un trabajador'}), 400

    full_name = data['full_name']
    email = data['email']
    phone_number = data['phone_number']
    role_id = data['role_id']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE Trabajadores SET full_name=%s, email=%s, phone_number=%s, role_id=%s, updated_at=NOW() WHERE worker_id=%s', (full_name, email, phone_number, role_id, worker_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Trabajador editado exitosamente'})

# Endpoint para eliminar un trabajador
@trabajadores_blueprint.route('/eliminar_trabajador/<int:worker_id>', methods=['GET'])
def eliminar_trabajador(worker_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Trabajadores WHERE worker_id=%s', (worker_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Trabajador eliminado exitosamente'})
