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
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes(
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(150),
            apellido VARCHAR(150),
            tipo_usuario VARCHAR(150),
            localidad VARCHAR(150)
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
    data=request.get_json()
    if "codigo" not in data or "nombre" not in data or "apellido" not in data or "tipo_usuario" not in data or "localidad" not in data:
        try:
            conector = conectar()
            cursor = conector.cursor()
            cursor.execute('''INSERT INTO CLIENTES(codigo, nombre, apellido, tipo_usuario,
                            localidad) Values (?, ?, ?, ?, ?)''', (data["codigo"], data["nombre"],data["apellido"],
                data["tipo_usuario"],data["localidad"]))
            conector.commit()
            cursor.close()
            conector.close()
            return jsonify({'mensaje': 'cliente agregado con exito'}), 201
        except:
            return jsonify({'error': 'Error al agregar cliente'}), 500
        
@app.route('/clientes/<int:codigo>', methods=['GET'])          
def consultar_cliente(codigo):
    try:
        conector=cursor.conectar()
        cursor= conector.cursor()
        cursor.execute('''SELECT * FROM CLIENTES WHERE codigo=?''',(codigo,))
        cliente=cursor.fetchone()
        if cliente is None:
            return jsonify({'error': 'No se encontró el cliente'}), 404
        else:
            return jsonify({
                    'codigo':cliente['codigo'],
                    'nombre': cliente['nombre'],
                    'apellido': cliente['apellido'],
                    'tipo_usuario': cliente['tipo_usuario'],
                    'localidad': cliente['localidad']
        })
    except:        
        return jsonify({'error': 'Error al consultar el producto'}), 500
    
@app.route('/clientes/<int:codigo>', methods=['PUT'])
def modificar_datos(codigo):
    data = request.get_json()
    if 'nombre' not in data or 'apellido' not in data or 'tipo_usuario' not in data or "localidad":
        return jsonify({'error': 'Falta uno o más campos requeridos'}), 400
    try:
        conector = conectar()
        cursor = conector.cursor()
        cursor.execute('''SELECT * FROM productos WHERE codigo=?''', (codigo,))
        producto = cursor.fetchone()
        
        if producto is None:
            return jsonify({'error': 'No se encontró el cliente'}), 404
        
        cursor.execute('''UPDATE clientes SET nombre=?, apellido=?, tipo_usuario=?, localidad=?
                          WHERE codigo=?''', (data['servicio'], data['plan'], data['precio'], codigo))
        
        conector.commit()
        cursor.close()
        conector.close()
        
        return jsonify({'mensaje': 'Cliente editado con éxito'}), 200
    
    except Exception as e:
        return jsonify({'error': 'Error al editar cliente', 'detalle': str(e)})        

                              
    
    



if __name__ == '__main__':
    create_table()
    app.run()



        
        
        
        
        
    
        
