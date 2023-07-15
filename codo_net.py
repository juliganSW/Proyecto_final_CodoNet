#importamos todo lo necesario 
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS

#Nombre del objeto flask
app=Flask(__name__)
CORS(app)

#Nombre del archivo que contiene a la BD
DATABASE= ("codo_netDB.db")

#conectamos con la DB mediante la funcion conectar
def conectar():
    conector=sqlite3.connect(DATABASE)
    conector.row_factory=sqlite3.Row
    return conector

#Funcion que crea la Tabla  productos en la BD si no existe

def create_table():
    conector=conectar()
    cursor=conector.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos(
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        servicio VARCHAR(150),
        plan VARCHAR (150),
        precio FLOAT
    )''')
    conector.commit()
    cursor.close()
    conector.close()
    
def create_table():
    conector=conectar()
    cursor=conector.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers(
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(150),
            apellido VARCHAR(150),
            telefono INT,
            email VARCHAR(150)
                       )''')
    conector.commit()
    cursor.close()
    conector.close()
    
    
 #Funcion para agregar productos    
@app.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    if "codigo" not in data or "servicio" not in data or "plan" not in data or "precio" not in data:
        return  jsonify({'error': 'Falta uno o más campos requeridos'}), 400
    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute("INSERT INTO productos (codigo, servicio, plan, precio) VALUES (?, ?, ?, ?)", 
                       (data['codigo'], data['servicio'], data['plan'], data['precio']))
        conector.commit()
        cursor.close()
        conector.close()
        
        return jsonify({'mensaje': 'producto agregado correctamente'}), 201
    except:
        return jsonify({'error': 'Error al agregar el producto'}), 500
    
#funcion para mostrar en pantalla los productos consultados a partir de su codigo 
@app.route('/productos/<int:codigo>', methods=['GET'])
def consultar_producto(codigo):
    try:
        conector=conectar()
        cursor=conector.cursor()
        cursor.execute('''SELECT * FROM productos
                       WHERE codigo=?''',(codigo,))
        producto = cursor.fetchone()
        
        if producto is None:
            return jsonify({'error': 'El producto no existe'}), 404
        else:
        
             return jsonify({
                    'codigo': producto['codigo'],
                    'servicio': producto['servicio'],
                    'plan': producto['plan'],
                    'precio': producto['precio']
        })
    except:        
           return jsonify({'error': 'Error al consultar el producto'}), 500
    
#Modifica los datos de un producto a partir de su codigo 
@app.route('/productos/<int:codigo>', methods=['PUT'])
def modificar_producto(codigo):
    data = request.get_json()
    if 'servicio' not in data or 'plan' not in data or 'precio' not in data:
        return jsonify({'error': 'Falta uno o más campos requeridos'}), 400
    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute('''SELECT * FROM productos WHERE codigo=?''', (codigo,))
        producto = cursor.fetchone()
        
        if producto is None:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        cursor.execute('''UPDATE productos SET servicio=?, plan=?, precio=?
                          WHERE codigo=?''', (data['servicio'], data['plan'], data['precio'], codigo))
        
        conector.commit()
        cursor.close()
        conector.close()
        
        return jsonify({'mensaje': 'Producto editado con éxito'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Error al editar producto', 'detalle': str(e)}), 500

#Lista todos los productos de la BD
@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute("SELECT * FROM productos")  # Solo selecciona las columnas necesarias
        productos = cursor.fetchall()

        response = []
        for producto in productos:
            response.append({
                'codigo': producto['codigo'],
                'servicio': producto['servicio'],
                'plan': producto['plan'],
                'precio': producto['precio']
            })

        return jsonify(response), 200
    except:
        return jsonify({'error': 'Error al listar los productos'}), 500
    
@app.route('/productos/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))  # Convertir código en una tupla
        if cursor.rowcount > 0:
            conector.commit()
            return jsonify({'message': 'Producto eliminado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404
    except Exception as e:
        return jsonify({'error': 'Error al eliminar el producto', 'detalle': str(e)}), 500
#################################################################################################
#Clientes#
#################################################################################################
@app.route('/clientes', methods=['POST'])
def agregar_cliente():
    data = request.get_json()
    if "codigo" not in data or "nombre" not in data or "apellido" not in data or "telefono" not in data or "email" not in data:
        return  jsonify({'error': 'Falta uno o más campos requeridos'}), 400
    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute("INSERT INTO customers (codigo, nombre, apellido, telefono, email) VALUES (?, ?, ?, ?, ?)", 
                       (data['codigo'], data['nombre'], data['apellido'], data['telefono'], data['email']))
        conector.commit()
        cursor.close()
        conector.close()
        
        return jsonify({'mensaje': 'cliente agregado correctamente'}), 201
    except:
        return jsonify({'error': 'Error al agregar el cliente'}), 500
        
@app.route('/clientes/<int:codigo>', methods=['GET'])          
def consultar_cliente(codigo):
    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute("SELECT * FROM customers WHERE codigo=?",(codigo,))
        cliente=cursor.fetchone()
        if cliente is None:
            return jsonify({'error': 'No se encontró el cliente'}), 404
        else:
            return jsonify({
                    'codigo':cliente['codigo'],
                    'nombre': cliente['nombre'],
                    'apellido': cliente['apellido'],
                    'telefono': cliente['telefono'],
                    'email': cliente['email']
        })
    except:        
        return jsonify({'error': 'Error al consultar el cliente'}), 500
    
@app.route('/clientes/<int:codigo>', methods=['PUT'])
def modificar_cliente(codigo):
    data = request.get_json()
    print(data)
    
    if 'nombre' not in data or 'apellido' not in data or 'telefono' not in data or 'email' not in data:
        return jsonify({'error': 'Falta uno o más campos requeridos'}), 400

    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute("SELECT * FROM customers WHERE codigo=?", (codigo,))
        cliente = cursor.fetchone()
        
        if cliente is None:
            return jsonify({'error': 'cliente no encontrado'}), 404
        
        cursor.execute('''UPDATE customers SET nombre=?, apellido=?, telefono=?, email=?
                  WHERE codigo=?''', (data['nombre'], data['apellido'], data['telefono'], data['email'], codigo))

        
        conector.commit()
        cursor.close()
        conector.close()
        
        return jsonify({'mensaje': 'Cliente editado con éxito'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Error al editar cliente', 'detalle': str(e)}), 500
    
@app.route('/clientes', methods=['GET']) 
def listar_clientes():
    try:
        conector=conectar()
        cursor= conector.cursor()
        cursor.execute("SELECT * FROM customers") 
        clientes = cursor.fetchall()  
        response=[]
        for cliente in clientes:
            response.append({
                'codigo': cliente ['codigo'],
                'nombre': cliente ['nombre'],
                'apellido':cliente ['apellido'],
                'telefono': cliente ['telefono'],
                'email': cliente['email']
            })
            
        return jsonify(response), 200
    except:
        return jsonify({'error': 'Error al listar los clientes'}), 500
    
@app.route('/clientes/<int:codigo>', methods=['DELETE'])
def eliminar_cliente(codigo): 
    try:
        conector=conectar()
        cursor=conector.cursor()
        cursor.execute('''DELETE FROM customers WHERE codigo=?
                       ''',(codigo,))
        if cursor.rowcount > 0:
            conector.commit()
            return jsonify({'message': 'Cliente eliminado con exito '}), 200
        return jsonify({'message': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Error al eliminar el cliente', 'detalle': str(e)}), 500
               
                        
    
    



if __name__ == '__main__':
    create_table()
    app.run()



        
        
        
        
        
    
        
