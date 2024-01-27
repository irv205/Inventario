from flask import Blueprint, request, jsonify
from db import connect_db

roles_blueprint = Blueprint('roles', __name__)

# Endpoint para obtener todos los roles
@roles_blueprint.route('/roles', methods=['GET'])
def get_roles():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Roles')
    roles = cursor.fetchall()
    conn.close()
    return jsonify({'roles': roles})

# Endpoint para agregar un nuevo rol
@roles_blueprint.route('/agregar_rol', methods=['POST'])
def agregar_rol():
    data = request.get_json()

    if not data or 'role_name' not in data:
        return jsonify({'error': 'El nombre del rol es requerido'}), 400

    role_name = data['role_name']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Roles (role_name) VALUES (%s) RETURNING role_id', (role_name,))
    role_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Rol agregado exitosamente', 'role_id': role_id})

# Endpoint para editar un rol existente
@roles_blueprint.route('/editar_rol/<int:role_id>', methods=['POST'])
def editar_rol(role_id):
    data = request.get_json()

    if not data or 'role_name' not in data:
        return jsonify({'error': 'El nuevo nombre del rol es requerido'}), 400

    new_role_name = data['role_name']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE Roles SET role_name=%s, updated_at=NOW() WHERE role_id=%s', (new_role_name, role_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Rol editado exitosamente'})

# Endpoint para eliminar un rol
@roles_blueprint.route('/eliminar_rol/<int:role_id>', methods=['GET'])
def eliminar_rol(role_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Roles WHERE role_id=%s', (role_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Rol eliminado exitosamente'})
