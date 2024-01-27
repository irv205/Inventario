from flask import Blueprint, request, jsonify
from db import connect_db

proveedores_blueprint = Blueprint('proveedores', __name__)

# Endpoint para obtener todos los proveedores
@proveedores_blueprint.route('/proveedores', methods=['GET'])
def get_proveedores():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Proveedores')
    proveedores = cursor.fetchall()
    conn.close()
    return jsonify({'proveedores': proveedores})

# Endpoint para agregar un nuevo proveedor
@proveedores_blueprint.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    data = request.get_json()

    if not data or 'company_name' not in data or 'contact_name' not in data or 'contact_email' not in data or 'contact_phone' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para agregar un proveedor'}), 400

    company_name = data['company_name']
    contact_name = data['contact_name']
    contact_email = data['contact_email']
    contact_phone = data['contact_phone']
    owner_id = data['owner_id']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Proveedores (company_name, contact_name, contact_email, contact_phone, owner_id) VALUES (%s, %s, %s, %s, %s) RETURNING supplier_id', (company_name, contact_name, contact_email, contact_phone, owner_id))
    supplier_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Proveedor agregado exitosamente', 'supplier_id': supplier_id})

# Endpoint para editar un proveedor existente
@proveedores_blueprint.route('/editar_proveedor/<int:supplier_id>', methods=['POST'])
def editar_proveedor(supplier_id):
    data = request.get_json()

    if not data or 'company_name' not in data or 'contact_name' not in data or 'contact_email' not in data or 'contact_phone' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Datos incompletos para editar un proveedor'}), 400

    company_name = data['company_name']
    contact_name = data['contact_name']
    contact_email = data['contact_email']
    contact_phone = data['contact_phone']
    owner_id = data['owner_id']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE Proveedores SET company_name=%s, contact_name=%s, contact_email=%s, contact_phone=%s, owner_id=%s, updated_at=NOW() WHERE supplier_id=%s', (company_name, contact_name, contact_email, contact_phone, owner_id, supplier_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Proveedor editado exitosamente'})

# Endpoint para eliminar un proveedor
@proveedores_blueprint.route('/eliminar_proveedor/<int:supplier_id>', methods=['GET'])
def eliminar_proveedor(supplier_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Proveedores WHERE supplier_id=%s', (supplier_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Proveedor eliminado exitosamente'})
