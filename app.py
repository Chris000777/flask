from flask import Flask,jsonify
from flask import render_template,request,redirect,url_for,flash
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
app.secret_key="ClaveSecreta"
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='sql10.freemysqlhosting.net'
app.config['MYSQL_DATABASE_USER']='sql10508116'
app.config['MYSQL_DATABASE_PASSWORD']='AwDfcSGdnw'
app.config['MYSQL_DATABASE_BD']='crud'
mysql.init_app(app)

@app.route('/')
def home():
    return "<h1>Corriendo servidor Flask</h1>"


CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA


@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
        return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route('/productos')
def empleados():        
        sql="SELECT * FROM `sql10508116`.`productos`;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        productos=cursor.fetchall()
        conn.commit()
        data = []
        content = {}
        for producto in productos:
                content = {'id': producto[0], 'nombre': producto[1], 'descripcion': producto[2], 'precio': producto[3], 'foto':producto[4]}
                data.append(content)
                content = {}
        return jsonify(data)

@app.route('/index')
def index():
        sql="SELECT * FROM `sql10508116`.`productos`;"
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        productos=cursor.fetchall()
        conn.commit()
        return render_template('productos/index.html', productos=productos)

@app.route('/destroy/<int:id>')
def destroy(id):
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT foto FROM `sql10508116`.`productos` WHERE id=%s",id)
        conn.commit()
        nombreFoto= cursor.fetchone()[0]
        try:
                os.remove(os.path.join('Back/Productos/uploads/', nombreFoto))
        except:
                pass
        cursor.execute("DELETE FROM `sql10508116`.`productos` WHERE id=%s",id)
        conn.commit()
        return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `sql10508116`.`productos` WHERE id=%s", id)  
    productos=cursor.fetchall()
    conn.commit()  
    return render_template('productos/edit.html', productos=productos)

@app.route('/update', methods=['POST'])
def update():
        _nombre=request.form['txtNombre']  
        _descripcion=request.form['txtDescripcion']  
        _precio=request.form['txtPrecio']
        _foto=request.files['txtFoto']
        id=request.form['txtID']

        datos=(_nombre,_descripcion,_precio,id)
        conn = mysql.connect()
        cursor = conn.cursor()
        
        now= datetime.now()
        tiempo= now.strftime("%Y%H%M%S")
        if _foto.filename!='':
                nuevoNombre=tiempo+_foto.filename
                _foto.save("Back/Productos/uploads/"+nuevoNombre)
                cursor.execute("SELECT foto FROM `sql10508116`.`productos` WHERE id=%s",id)
                conn.commit()
                nombreFoto= cursor.fetchone()[0]
                try:
                        os.remove(os.path.join('Back/Productos/uploads/', nombreFoto))
                except:
                        pass
                cursor.execute("UPDATE `sql10508116`.`productos` SET foto=%s WHERE id=%s", (nuevoNombre, id))
                conn.commit()

        sql = "UPDATE `sql10508116`.`productos` SET `nombre`=%s, `descripcion`=%s, `precio`=%s  WHERE id=%s;"
        cursor.execute(sql,datos)
        conn.commit()
        return redirect('/')

@app.route('/create')
def create():
        return render_template('productos/create.html')

@app.route('/store', methods=['POST'])
def storage():
        _nombre=request.form['txtNombre']
        _descripcion=request.form['txtDescripcion']    
        _precio=request.form['txtPrecio']
        _foto=request.files['txtFoto']

        if _nombre=='' or _descripcion=='' or _precio=='' or _foto.filename=='':
                flash('Recuerda llenar todos los campos')
                return redirect(url_for('create'))

        now=datetime.now()
        tiempo=now.strftime("%Y%H%M%S")

        if _foto.filename!='':
                nuevoNombre=tiempo+_foto.filename
                _foto.save("Back/Productos/uploads/"+nuevoNombre)

        
        sql="INSERT INTO `sql10508116`.`productos` (`id`, `nombre`, `descripcion`, `precio`, `foto`) VALUES (NULL, %s, %s, %s, %s);"
        datos=(_nombre,_descripcion ,_precio, nuevoNombre)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,datos)
        conn.commit()
        return redirect('/')


#Programa principal
if __name__=='__main__':
    app.run(debug=True)
