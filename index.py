import os
import datetime
from pymongo import MongoClient, errors

# --- CONEXIÓN ---
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://ANDRES_VANEGAS:CF32fUhOhrj70dY5@cluster0.dtureen.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['NestleDB']

# --- VALIDACIÓN DE COLECCIÓN ---
nombre_coleccion = 'Adminidtrativo'

if nombre_coleccion not in db.list_collection_names():
    print(f"⚠️ La colección '{nombre_coleccion}' no existe. Creándola...")
    db.create_collection(nombre_coleccion)
    # Opcional: Crear un índice único para la cédula si no quieres registros duplicados
    db[nombre_coleccion].create_index([("cedula", 1)], unique=False) 
    print("✅ Colección creada con éxito.")

puntos_col = db[nombre_coleccion]

# --- DICCIONARIO DE LOGUEO ---
usuarios_autorizados = {
    "12345678": "Andres Vanegas",
    "98765432": "Operador Nestle"
}

def flujo_registro():
    cedula = input("Ingrese su cédula para loguearse: ")
    
    if cedula in usuarios_autorizados:
        nombre_usuario = usuarios_autorizados[cedula]
        print(f"\nAcceso concedido: {nombre_usuario}")
        
        print("\n" + "!"*30)
        print("📸 REQUERIMIENTO DE FOTO:")
        print("🤳 Debe ser tipo SELFIE.")
        print("🖥️  Frente al PC.")
        print("👕 El UNIFORME debe ser visible y la imagen clara.")
        print("!"*30)
        
        foto = input("\n[SISTEMA] Cargue la foto (ruta o nombre de archivo): ")
        actividad = input("¿Qué actividad realizó?: ")
        resumen = input("Resumen de lo hecho: ")

        # Crear el documento
        registro = {
            "cedula": cedula,
            "nombre": nombre_usuario,
            "fecha": datetime.datetime.now(),
            "foto_entrada": foto,
            "actividad": actividad,
            "resumen": resumen,
            "estado_foto": "Validada por usuario"
        }

        # Inserción
        try:
            puntos_col.insert_one(registro)
            print("\n✔️ Registro guardado correctamente en la base de datos.")
        except Exception as e:
            print(f"\n❌ Error al insertar: {e}")
    else:
        print("❌ Error: Cédula no registrada en el sistema.")

# Ejecutar
flujo_registro()
