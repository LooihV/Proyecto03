from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
import logging


app = Flask(__name__)

client = MongoClient('mongodb://mongo:27017')
db = client['ListaCompras']
coleccion = db['producto']

@app.route('/crear', methods=['POST'])
def crear():
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']

    nuevo_producto = {'nombre': nombre, 'cantidad': cantidad}
    coleccion.insert_one(nuevo_producto)

    return redirect('/')

@app.route('/', methods=['GET'])
def leer():
    productos = coleccion.find({})
    return render_template('index.html', productos=productos)

@app.route('/actualizar/<string:id>', methods=['POST', 'PUT'])
def actualizar(id):
    if request.form.get('_method') == 'PUT':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']

        coleccion.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': nombre, 'cantidad': cantidad}})

    return redirect('/')

@app.route('/eliminar/<string:id>', methods=['POST', 'DELETE'])
def eliminar(id):
    if request.form.get('_method') == 'DELETE':
        coleccion.delete_one({'_id': ObjectId(id)})

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')