from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import re

app = Flask(__name__)
app.secret_key = '2772'

# Conexión a MongoDB Atlas
client = MongoClient('mongodb+srv://aaronloperena2809_db_user:pmKXBIvTCZo34oNV@cluster0.fj462vw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client['Biblioteca']
usuarios_collection = db['usuarios']

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # --- Obtener datos ---
        nombre = request.form['nombre'].strip()
        correo = request.form['correo'].strip()
        contrasena = request.form['contrasena']

        # ----------- VALIDACIONES -----------
        
        # Nombre: solo letras/números, sin espacios, 3–100 caracteres
        if not re.match(r'^[A-Za-z0-9]{3,100}$', nombre):
            return render_template('error.html', mensaje='El nombre solo puede tener letras y números, sin espacios. Mínimo 3 y máximo 100 caracteres.')

        # Correo: sin &, $, sin espacios, 6–50 caracteres
        if not re.match(r'^[^\s&$]{6,50}$', correo):
            return render_template('error.html', mensaje='El correo no puede contener espacios ni símbolos como & o $. Mínimo 6 y máximo 50 caracteres.')

        # Contraseña: sin espacios, 5–50 caracteres
        if not re.match(r'^\S{5,50}$', contrasena):
            return render_template('error.html', mensaje='La contraseña no puede contener espacios y debe tener entre 5 y 50 caracteres.')

        # Evitar correos duplicados
        if usuarios_collection.find_one({'correo': correo}):
            return render_template('error.html', mensaje='El correo ya está registrado.')

        # Guardar usuario
        usuarios_collection.insert_one({
            'nombre': nombre,
            'correo': correo,
            'contrasena': contrasena
        })

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        
        user = usuarios_collection.find_one({'nombre': nombre, 'contrasena': contrasena})

        if user:
            session['logged_in'] = True
            session['username'] = nombre
            return redirect(url_for('arca'))
        else:
            return 'Nombre de usuario o contraseña incorrectos.'

    return render_template('login.html')

@app.route('/arca')
def arca():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('Arca.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/categoria/<nombre_categoria>')
def categoria(nombre_categoria):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template(f'{nombre_categoria.lower()}.html')

if __name__ == '__main__':
    app.run(debug=True)

