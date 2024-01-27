from flask import Blueprint, request, jsonify
from db import connect_db

categorias_blueprint = Blueprint('categorias', __name__)

# Endpoint para obtener todas las categorías
@categorias_blueprint.route('/categorias', methods=['GET'])
def get_categorias():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Categorias')
    categorias = cursor.fetchall()
    conn.close()
    return jsonify({'categorias': categorias})

# Endpoint para agregar una nueva categoría
@categorias_blueprint.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    data = request.get_json()

    if not data or 'category_name' not in data:
        return jsonify({'error': 'Datos incompletos para agregar una categoría'}), 400

    category_name = data['category_name']
    description = data.get('description', None)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Categorias (category_name, description) VALUES (%s, %s) RETURNING category_id', (category_name, description))
    category_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Categoría agregada exitosamente', 'category_id': category_id})

# Endpoint para editar una categoría existente
@categorias_blueprint.route('/editar_categoria/<int:category_id>', methods=['POST'])
def editar_categoria(category_id):
    data = request.get_json()

    if not data or 'category_name' not in data:
        return jsonify({'error': 'Datos incompletos para editar una categoría'}), 400

    category_name = data['category_name']
    description = data.get('description', None)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE Categorias SET category_name=%s, description=%s, updated_at=NOW() WHERE category_id=%s', (category_name, description, category_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Categoría editada exitosamente'})

# Endpoint para eliminar una categoría
@categorias_blueprint.route('/eliminar_categoria/<int:category_id>', methods=['GET'])
def eliminar_categoria(category_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Categorias WHERE category_id=%s', (category_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Categoría eliminada exitosamente'})
