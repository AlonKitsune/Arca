from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

# Crea la instancia de la aplicación Flask
app = Flask(__name__)

# La clave secreta es necesaria para las sesiones. ¡No la compartas!
app.secret_key = '2772'

# Conexión a MongoDB Atlas
client = MongoClient('mongodb+srv://aaronloperena2809_db_user:pmKXBIvTCZo34oNV@cluster0.fj462vw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Define la base de datos y la colección AQUÍ, para que estén disponibles globalmente
db = client['Biblioteca']
usuarios_collection = db['usuarios']

# Rutas de la Aplicación
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if usuarios_collection.find_one({'correo': correo}):
            return 'El correo ya está registrado.'
        
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