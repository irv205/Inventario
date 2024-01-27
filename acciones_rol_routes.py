from flask import Blueprint, request, jsonify
from db import connect_db

acciones_rol_blueprint = Blueprint('acciones_rol', __name__)

# Endpoint para obtener todas las acciones de un rol
@acciones_rol_blueprint.route('/acciones_rol/<int:role_id>', methods=['GET'])
def get_acciones_rol(role_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM AccionesRol WHERE role_id=%s', (role_id,))
    acciones_rol = cursor.fetchall()
    conn.close()
    return jsonify({'acciones_rol': acciones_rol})

# Endpoint para agregar una nueva acción a un rol
@acciones_rol_blueprint.route('/agregar_accion_rol', methods=['POST'])
def agregar_accion_rol():
    data = request.get_json()

    if not data or 'role_id' not in data or 'action_name' not in data:
        return jsonify({'error': 'role_id y action_name son requeridos'}), 400

    role_id = data['role_id']
    action_name = data['action_name']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO AccionesRol (role_id, action_name) VALUES (%s, %s) RETURNING action_id', (role_id, action_name))
    action_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Acción de rol agregada exitosamente', 'action_id': action_id})

# Endpoint para editar una acción de un rol existente
@acciones_rol_blueprint.route('/editar_accion_rol/<int:action_id>', methods=['POST'])
def editar_accion_rol(action_id):
    data = request.get_json()

    if not data or 'action_name' not in data:
        return jsonify({'error': 'El nuevo nombre de la acción es requerido'}), 400

    new_action_name = data['action_name']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE AccionesRol SET action_name=%s, updated_at=NOW() WHERE action_id=%s', (new_action_name, action_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Acción de rol editada exitosamente'})

# Endpoint para eliminar una acción de un rol
@acciones_rol_blueprint.route('/eliminar_accion_rol/<int:action_id>', methods=['GET'])
def eliminar_accion_rol(action_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM AccionesRol WHERE action_id=%s', (action_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Acción de rol eliminada exitosamente'})
