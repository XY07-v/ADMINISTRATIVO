import os
import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# --- CONFIGURACIÓN MONGODB ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://ANDRES_VANEGAS:CF32fUhOhrj70dY5@cluster0.dtureen.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['NestleDB']
puntos_col = db['Adminidtrativo']

usuarios = {"123456": "Andres Vanegas", "789012": "Colaborador Nestle"}

@app.route('/')
def index():
    # Esta es la página de inicio (Login)
    return '''
        <h1>Logueo Administrativo</h1>
        <form action="/registro" method="post">
            Cédula: <input type="text" name="cedula">
            <input type="submit" value="Entrar">
        </form>
    '''

@app.route('/registro', methods=['POST'])
def registro():
    cedula = request.form.get('cedula')
    if cedula in usuarios:
        nombre = usuarios[cedula]
        return f'''
            <h2>Bienvenido, {nombre}</h2>
            <p>📸 <b>Requisito:</b> Selfie frente al PC, con uniforme y clara.</p>
            <form action="/guardar" method="post">
                <input type="hidden" name="cedula" value="{cedula}">
                Foto (Nombre/URL): <input type="text" name="foto"><br><br>
                Actividad: <input type="text" name="actividad"><br><br>
                Resumen: <textarea name="resumen"></textarea><br><br>
                <input type="submit" value="Guardar Registro">
            </form>
        '''
    return "Cédula no autorizada. <a href='/'>Volver</a>"

@app.route('/guardar', methods=['POST'])
def guardar():
    # Aquí se inserta en MongoDB
    data = {
        "cedula": request.form.get('cedula'),
        "nombre": usuarios.get(request.form.get('cedula')),
        "fecha": datetime.datetime.now(),
        "foto_entrada": request.form.get('foto'),
        "actividad": request.form.get('actividad'),
        "resumen": request.form.get('resumen')
    }
    puntos_col.insert_one(data)
    return "✅ Registro guardado con éxito en MongoDB. <a href='/'>Hacer otro</a>"

if __name__ == "__main__":
    app.run(debug=True)
