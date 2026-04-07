import os
import datetime
from flask import Flask, request, render_template_string, session, redirect, url_for
from flask_session import Session
from pymongo import MongoClient

app = Flask(__name__)

# --- CONFIGURACIÓN DE SESIÓN ---
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(hours=8)
Session(app)

# --- CONEXIÓN MONGODB ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://ANDRES_VANEGAS:CF32fUhOhrj70dY5@cluster0.dtureen.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['NestleDB']
puntos_col = db['Adminidtrativo']

# --- DICCIONARIO DE USUARIOS ACTUALIZADO ---
usuarios = {
    "1094938475": "AMADO LOZANO JHEINER ALBEIRO",
    "1042064101": "ARDILA ORTEGA FABIANA",
    "1020811447": "BAQUERO MURCIA CRISTIAN CAMILO",
    "1143360426": "BARRERA DE AVILA KELLY JOHANA",
    "1121833139": "BOCANEGRA GARZON CINDY JULIETH",
    "1053783753": "CARMONA HUERTAS NESTOR ANDRES",
    "52860228": "CASTRILLON URREGO YEIMI PAOLA",
    "1048276830": "CASTRO OROZCO CINDY PAOLA",
    "1085248529": "ERAZO CAICEDO DIANA MARCELA",
    "1023930172": "FORERO VELASQUEZ EDWIN ALEXANDER",
    "1143341974": "GONZALES BERRIO YEISON JOSE",
    "1022404439": "GONZALEZ RODRIGUEZ MICHAEL",
    "1095835233": "GRIMALDO NAVARRO WILSON JAVIER",
    "1015068243": "HINCAPIE ZEA YOANA ANDREA",
    "1053334868": "JIMENEZ JIMENEZ ESNEYDI YELEYSI",
    "1010070556": "KAREN TATIANA DE LA ROSA TORRES",
    "1003634117": "MARIN GALEANO KEVIN SANTIAGO",
    "1037948290": "MAURICIO LADINO LARGO",
    "1072703990": "MERCHAN SEGURA JOHN EDISON",
    "1234990099": "MONTOYA BUITRAGO VANESA",
    "1018438044": "ORJUELA FORIGUA HAYDE CAROLINA",
    "43268846": "OTALVARO METAUTE MONICA MILENA",
    "1002183801": "PADILLA GRAVIER JUAN CAMILO",
    "43753705": "PATIÑO MONICA MARIA",
    "1113661456": "RAMIREZ MORENO GERALDINE",
    "80220107": "RAMIREZ SARAY SIGIFREDO",
    "66771000": "RESTREPO LUZ MARLENE",
    "93236326": "SIERRA PELAEZ RIGOBERTO",
    "43161032": "YEPES BETANCUR SHIRLEY",
    "1130589169": "ELIECER ARDILA LUCIO"
}

CSS = """
<style>
    :root { --primary: #0063ad; --bg: #f4f7f6; }
    body { font-family: 'Segoe UI', sans-serif; background: var(--bg); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
    .container { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
    input, textarea { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
    button { background: var(--primary); color: white; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; }
    .alert { background: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; font-size: 0.85em; margin-bottom: 15px; text-align: left; }
</style>
"""

HTML_WRAPPER = f"<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>{CSS}</head><body><div class='container'>{{{{ content | safe }}}}</div></body></html>"

@app.route('/')
def index():
    if "user" in session:
        return redirect(url_for('registro_notas'))
    content = """<h2>Logueo Nestlé</h2><form action="/login" method="post"><input type="text" name="cedula" placeholder="Cédula" required><button type="submit">Entrar</button></form>"""
    return render_template_string(HTML_WRAPPER, content=content)

@app.route('/login', methods=['POST'])
def login():
    cedula = request.form.get('cedula')
    if cedula in usuarios:
        session["user"] = cedula
        session["nombre"] = usuarios[cedula]
        return redirect(url_for('foto'))
    return "Cédula no autorizada. <a href='/'>Volver</a>"

@app.route('/foto')
def foto():
    if "user" not in session: return redirect(url_for('index'))
    content = f"""
    <h3>Hola, {session['nombre']}</h3>
    <div class="alert">📸 <b>SELFIE OBLIGATORIA:</b><br>Frente al PC, con uniforme y clara.</div>
    <form action="/guardar_foto" method="post">
        <input type="file" accept="image/*" capture="user" name="foto_file" required>
        <button type="submit">Validar e Ir a Notas</button>
    </form>
    """
    return render_template_string(HTML_WRAPPER, content=content)

@app.route('/guardar_foto', methods=['POST'])
def guardar_foto():
    session["foto_ok"] = True
    return redirect(url_for('registro_notas'))

@app.route('/registro')
def registro_notas():
    if "foto_ok" not in session: return redirect(url_for('foto'))
    content = f"""
    <h4>Nueva Nota: {session['nombre']}</h4>
    <form action="/guardar_nota" method="post">
        <input type="text" name="actividad" placeholder="Actividad" required>
        <textarea name="resumen" placeholder="Resumen..." rows="3" required></textarea>
        <button type="submit">Guardar Registro</button>
    </form>
    <br><a href="/logout" style="color:red; font-size:0.8em;">Cerrar Sesión</a>
    """
    return render_template_string(HTML_WRAPPER, content=content)

@app.route('/guardar_nota', methods=['POST'])
def guardar_nota():
    data = {
        "cedula": session["user"],
        "nombre": session["nombre"],
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actividad": request.form.get('actividad'),
        "resumen": request.form.get('resumen')
    }
    puntos_col.insert_one(data)
    return redirect(url_for('registro_notas'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
