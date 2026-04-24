import os
from app.model import Personaje
from app.DB import ConectionDB
from app.Logic.combate import simular_combate
from flask import Flask, request, jsonify, render_template

# Configurar la ruta a la carpeta templates y static
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/personajes', methods=['POST'])
def crear_personaje():
    data = request.get_json()
    nombre = data.get('nombre')
    color_piel = data.get('color_piel')
    raza = data.get('raza')
    fuerza = data.get('fuerza')
    agilidad = data.get('agilidad')
    magia = data.get('magia')
    conocimiento = data.get('conocimiento')

    
    conn = ConectionDB()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO personajes (nombre, color_piel, raza, fuerza, agilidad, magia, conocimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (nombre, color_piel, raza, fuerza, agilidad, magia, conocimiento))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Personaje creado exitosamente'}), 201
@app.route('/personajes', methods=['GET'])
def obtener_personajes():
    conn = ConectionDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personajes')
    personajes = cursor.fetchall()
    conn.close()

    personajes_list = []
    for personaje in personajes:
        personajes_list.append({
            'id': personaje[0],
            'nombre': personaje[1],
            'color_piel': personaje[2],
            'raza': personaje[3],
            'fuerza': personaje[4],
            'agilidad': personaje[5],
            'magia': personaje[6],
            'conocimiento': personaje[7],
            'created_at': personaje[8]
        })

    return jsonify(personajes_list), 200

@app.route('/personajes/<int:id>', methods=['GET'])
def obtener_personaje(id):
    conn = ConectionDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personajes WHERE id = %s', (id,))
    personaje = cursor.fetchone()
    conn.close()

    if personaje:
        personaje_data = {
            'id': personaje[0],
            'nombre': personaje[1],
            'color_piel': personaje[2],
            'raza': personaje[3],
            'fuerza': personaje[4],
            'agilidad': personaje[5],
            'magia': personaje[6],
            'conocimiento': personaje[7],
            'created_at': personaje[8]
        }
        return jsonify(personaje_data), 200
    else:
        return jsonify({'message': 'Personaje no encontrado'}), 404

@app.route('/personajes/<int:id>', methods=['PUT'])
def actualizar_personaje(id):
    data = request.get_json()
    nombre = data.get('nombre')
    color_piel = data.get('color_piel')
    raza = data.get('raza')
    fuerza = data.get('fuerza')
    agilidad = data.get('agilidad')
    magia = data.get('magia')
    conocimiento = data.get('conocimiento')

    conn = ConectionDB()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE personajes
        SET nombre = %s, color_piel = %s, raza = %s, fuerza = %s, agilidad = %s, magia = %s, conocimiento = %s
        WHERE id = %s
    ''', (nombre, color_piel, raza, fuerza, agilidad, magia, conocimiento, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Personaje actualizado exitosamente'}), 200

@app.route('/personajes/<int:id>', methods=['DELETE'])
def eliminar_personaje(id):
    conn = ConectionDB()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM personajes WHERE id = %s', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Personaje eliminado exitosamente'}), 200

@app.route('/combate', methods=['POST'])
def combate_route():
    data = request.get_json()
    id1 = data.get('id1')
    id2 = data.get('id2')
    
    if not id1 or not id2:
        return jsonify({"error": "Faltan luchadores."}), 400
        
    conn = ConectionDB()
    cursor = conn.cursor()
    
    # Obtener personaje 1
    cursor.execute('SELECT * FROM personajes WHERE id = %s', (id1,))
    p1_data = cursor.fetchone()
    
    # Obtener personaje 2
    cursor.execute('SELECT * FROM personajes WHERE id = %s', (id2,))
    p2_data = cursor.fetchone()
    
    conn.close()
    
    if not p1_data or not p2_data:
        return jsonify({"error": "Uno o ambos personajes no existen."}), 404
        
    # Convertir a objetos como los espera la lógica (similar a Personaje de SQLAlchemy)
    class TempP:
        def __init__(self, data_tuple):
            self.id = data_tuple[0]
            self.nombre = data_tuple[1]
            self.color_piel = data_tuple[2]
            self.raza = data_tuple[3]
            self.fuerza = data_tuple[4]
            self.agilidad = data_tuple[5]
            self.magia = data_tuple[6]
            self.conocimiento = data_tuple[7]

    p1 = TempP(p1_data)
    p2 = TempP(p2_data)
    
    resultado = simular_combate(p1, p2)
    return jsonify(resultado), 200


