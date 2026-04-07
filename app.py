import os
import datetime
from flask import Flask, request, render_template_string, session, redirect, url_for
from flask_session import Session
from pymongo import MongoClient

app = Flask(__name__)

# --- CONFIGURACIÓN DE SESIÓN ---
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=8) # La sesión dura 8 horas
Session(app)

# --- CONEXIÓN MONGODB ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://ANDRES_VANEGAS:CF32fUhOhrj70dY5@cluster0.dtureen.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['NestleDB']
puntos_col = db['Adminidtrativo']

# Usuarios autorizados
usuarios = {"123456": "Andres Vanegas", "789012": "Operador Nestle"}

# --- DISEÑO CSS (ESTÉTICO) ---
CSS = """
<style>
    :root { --primary: #0063ad; --secondary: #00a1e1; --bg: #f4f7f6; }
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
    .container { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
    h2 { color: var(--primary); margin-bottom: 20px; }
    .alert { background: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; font-size: 0.9em; margin-bottom: 15px; border: 1px solid #ffeeba; }
    input, textarea { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
    button { background: var(--primary); color: white; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
    button:hover { background: var(--secondary); }
    .logout { margin-top: 15px; background: #e74c3c; font-size: 0.8em; padding: 8px; }
    .user-info { font-size: 0.9em; color: #666; margin-bottom: 20px; }
</style>
"""

HTML_WRAPPER = f"<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>{CSS}</head><body><div class='container'>{{{{ content | safe }}}}</div></body></html>"

@app.route('/')
def index():
    if "user" in session:
        if "foto" not in session:
            return redirect(url_for('tomar_foto'))
        return redirect(url_for('registro_notas'))
    
    content = """
    <h2>Nestlé Admin</h2>
    <form action="/login" method="post">
        <input type="text" name="cedula" placeholder="Cédula de Identidad" required>
        <button type="submit">Iniciar Sesión</button>
    </form>
    """
    return render_template_string(HTML_WRAPPER, content=content)

@app.route('/login', methods=['POST'])
def login():
    cedula = request.form.get('cedula')
    if cedula in usuarios:
        session["user"] = cedula
        session["nombre"] = usuarios[cedula]
        return redirect(url_for('tomar_foto'))
    return render_template_string(HTML_WRAPPER, content="<h3>❌ Cédula no válida</h3><a href='/'>Reintentar</a>")

@app.route('/foto')
def tomar_foto():
    if "user" not in session: return redirect(url_for('index'))
    
    content = f"""
    <div class="user-info">Hola, <b>{session['nombre']}</b></div>
    <div class="alert">📸 <b>REQUERIMIENTO ÚNICO:</b><br>Toma una selfie frente al PC con el uniforme visible.</div>
    <form action="/guardar_foto" method="post">
        <input type="file" name="file_foto" accept="image/*" capture="user" required>
        <button type="submit">Validar Foto y Continuar</button>
    </form>
    """
    return render_template_string(HTML_WRAPPER, content=content)

@app.route('/guardar_foto', methods=['POST'])
def guardar_foto():
    session["foto"] = "Cargada" # Marcamos que ya cumplió el requisito
    return redirect(url_for('registro_notas'))

@app.route('/registro')
def registro_notas():
    if "foto" not in session: return redirect(url_for('tomar_foto'))
    
    content = f"""
    <div class="user-info">Sesión activa: {session['nombre']}</div>
    <h2>Nueva Nota</h2>
    <form action="/guardar_nota" method="post">
        <input type="text" name="actividad" placeholder="Actividad Realizada" required>
        <textarea name="resumen" placeholder="Resumen detallado..." rows="4" required></textarea>
        <button type="submit">Guardar Nota</button>
    </form>
    <form action="/logout" method="get">
        <button type="submit" class="logout">Cerrar Sesión Final</button>
    </form>
    """
    return render_template_string(HTML_WRAPPER, content=content)

@app.route('/guardar_nota', methods=['POST'])
def guardar_nota():
    if "user" not in session: return redirect(url_for('index'))
    
    data = {
        "cedula": session["user"],
        "nombre": session["nombre"],
        "fecha": datetime.datetime.now(),
        "actividad": request.form.get('actividad'),
        "resumen": request.form.get('resumen'),
        "foto_validada": True
    }
    puntos_col.insert_one(data)
    return render_template_string(HTML_WRAPPER, content="<h3>✅ Nota Guardada</h3><p>Puedes agregar otra.</p><a href='/registro'><button>Nueva Nota</button></a>")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
