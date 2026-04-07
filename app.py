import os
import datetime
from pymongo import MongoClient

# --- CONFIGURACIÓN MONGODB ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://ANDRES_VANEGAS:CF32fUhOhrj70dY5@cluster0.dtureen.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['NestleDB']
puntos_col = db['Adminidtrativo']

# --- DICCIONARIO DE USUARIOS (LOGUEO) ---
# Clave: Cédula, Valor: Nombre del colaborador
usuarios_autorizados = {
    "12345678": "Andres Vanegas",
    "87654321": "Maria Lopez",
    "10203040": "Carlos Perez"
}

def iniciar_sesion():
    print("--- SISTEMA DE REGISTRO ADMINISTRATIVO ---")
    cedula = input("Ingrese su número de cédula: ")
    
    if cedula in usuarios_autorizados:
        print(f"\nBienvenido(a), {usuarios_autorizados[cedula]}.")
        return cedula
    else:
        print("Cédula no autorizada.")
        return None

def crear_registro(cedula):
    print("\n--- REQUISITO DE FOTO ---")
    print("⚠️  IMPORTANTE: La foto debe ser:")
    print("👉 Frente al PC.")
    print("👉 Tipo selfie.")
    print("👉 Donde se vea claramente el uniforme.")
    
    # En un entorno real, aquí se usaría una librería de cámara o carga de archivos.
    # Para este ejemplo, simulamos la ruta del archivo/URL.
    foto_entrada = input("\nIngrese el nombre del archivo o URL de la foto: ")
    
    actividad = input("¿Qué se hizo hoy? (Actividad): ")
    resumen = input("Proporcione un resumen detallado de lo realizado: ")
    
    # Estructura del documento para MongoDB
    nuevo_registro = {
        "cedula": cedula,
        "nombre": usuarios_autorizados[cedula],
        "fecha": datetime.datetime.now(), # Fecha y hora actual
        "foto_entrada": foto_entrada,
        "actividad": actividad,
        "resumen_laboral": resumen
    }
    
    try:
        resultado = puntos_col.insert_one(nuevo_registro)
        print(f"\n✅ Registro creado exitosamente. ID: {resultado.inserted_id}")
    except Exception as e:
        print(f"❌ Error al guardar en base de datos: {e}")

# --- FLUJO PRINCIPAL ---
usuario_id = iniciar_sesion()
if usuario_id:
    crear_registro(usuario_id)
