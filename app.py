import os
import datetime
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- CONFIGURACIÓN MONGODB ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://ANDRES_VANEGAS:CF32fUhOhrj70dY5@cluster0.dtureen.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI) if 'MongoClient' in globals() else None

# Importación tardía para evitar errores de contexto en Render
from pymongo import MongoClient
client = MongoClient(MONGO_URI)
db = client['NestleDB']
puntos_col = db['Adminidtrativo']

# Diccionario de logueo
usuarios = {
    "123456": "Andres Vanegas",
    "789012": "Operador Nestle"
}

# Plantilla HTML simple integrada
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>Registro Nestle</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; margin: 20px; line-height: 1.6; }
        .card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; max-width: 400px; }
        input, textarea { width: 100%; margin-bottom: 10px; padding: 8px; }
        button { background: #0063ad; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    form = """
    <h2>Logueo</h2>
    <form action="/login" method="post">
        <input type="text" name="cedula" placeholder="Número de Cédula" required>
        <button type="submit">Entrar</button>
    </form>
    """
    return render_template_string(HTML_LAYOUT, content=form)

@app.route('/login', methods=['POST'])
def login():
    cedula = request.form.get('cedula')
    if cedula in usuarios:
        nombre = usuarios[cedula]
        form = f"""
        <h2>Bienvenido, {nombre}</h2>
        <p style="color: red;">⚠️ <b>REQUISITO FOTO:</b> Selfie frente al PC, con uniforme visible y clara.</p>
        <form action="/guardar" method="post">
            <input type="hidden" name="cedula" value="{cedula}">
            <input type="text" name="foto" placeholder="Nombre o URL de la foto" required>
            <input type="text" name="actividad" placeholder="¿Qué se hizo hoy?" required>
            <textarea name="resumen" placeholder="Resumen de lo que se hizo" rows="4" required></textarea>
            <button type="submit">Guardar Registro</button>
        </form>
        """
        return render_template_string(HTML_LAYOUT, content=form)
    return render_template_string(HTML_LAYOUT, content="<h3>❌ Cédula no autorizada</h3><a href='/'>Volver</a>")

@app.route('/guardar', methods=['POST'])
def guardar():
    cedula = request.form.get('cedula')
    data = {
        "cedula": cedula,
        "nombre": usuarios.get(cedula),
        "fecha": datetime.datetime.now(),
        "foto_entrada": request.form.get('foto'),
        "actividad": request.form.get('actividad'),
        "resumen": request.form.get('resumen')
    }
    puntos_col.insert_one(data)
    return render_template_string(HTML_LAYOUT, content="<h3>✅ Guardado con éxito</h3><a href='/'>Hacer otro registro</a>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
