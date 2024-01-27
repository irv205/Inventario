from flask import Blueprint, request, jsonify
from db import connect_db

product_images_blueprint = Blueprint('product_images', __name__)

# Endpoint para obtener todas las imágenes de productos
@product_images_blueprint.route('/imagenes_productos', methods=['GET'])
def get_imagenes_productos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ProductImages')
    imagenes_productos = cursor.fetchall()
    conn.close()
    return jsonify({'imagenes_productos': imagenes_productos})

# Endpoint para agregar una nueva imagen de producto
@product_images_blueprint.route('/agregar_imagen_producto', methods=['POST'])
def agregar_imagen_producto():
    data = request.get_json()

    if not data or 'product_id' not in data or 'image_url' not in data:
        return jsonify({'error': 'Datos incompletos para agregar una imagen de producto'}), 400

    product_id = data['product_id']
    image_url = data['image_url']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ProductImages (product_id, image_url) VALUES (%s, %s) RETURNING image_id', (product_id, image_url))
    image_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify({'message': 'Imagen de producto agregada exitosamente', 'image_id': image_id})

# Endpoint para editar una imagen de producto existente
@product_images_blueprint.route('/editar_imagen_producto/<int:image_id>', methods=['POST'])
def editar_imagen_producto(image_id):
    data = request.get_json()

    if not data or 'product_id' not in data or 'image_url' not in data:
        return jsonify({'error': 'Datos incompletos para editar una imagen de producto'}), 400

    product_id = data['product_id']
    image_url = data['image_url']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE ProductImages SET product_id=%s, image_url=%s, updated_at=NOW() WHERE image_id=%s', (product_id, image_url, image_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Imagen de producto editada exitosamente'})

# Endpoint para eliminar una imagen de producto
@product_images_blueprint.route('/eliminar_imagen_producto/<int:image_id>', methods=['GET'])
def eliminar_imagen_producto(image_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ProductImages WHERE image_id=%s', (image_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Imagen de producto eliminada exitosamente'})
