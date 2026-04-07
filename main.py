import os
import datetime
from pymongo import MongoClient

# --- CONFIGURACIÓN MONGODB ---
# Nota: La colección se crea automáticamente al insertar, pero aquí forzamos la verificación
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://ANDRES_VANEGAS:CF32fUhOhrj70dY5@cluster0.dtureen.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['NestleDB']
coleccion_nombre = 'Adminidtrativo'

# Verificar si la colección existe, si no, crearla
if coleccion_nombre not in db.list_collection_names():
    db.create_collection(coleccion_nombre)
    print(f"✔️ Colección '{coleccion_nombre}' creada.")

puntos_col = db[coleccion_nombre]

# --- LOGUEO CON DICCIONARIO ---
usuarios = {
    "123456": "Andres Vanegas",
    "789012": "Colaborador Nestle",
    "112233": "Admin General"
}

def ejecutar_registro():
    print("--- INICIO DE SESIÓN ---")
    cedula = input("Ingrese su cédula: ")

    if cedula in usuarios:
        nombre = usuarios[cedula]
        print(f"\n✅ Bienvenido, {nombre}")
        
        # --- REQUERIMIENTOS DE FOTO ---
        print("\n" + "="*40)
        print("📸 INSTRUCCIONES PARA LA FOTO:")
        print("🤳 La foto debe ser TIPO SELFIE.")
        print("💻 Debe verse usted frente al PC.")
        print("👔 El UNIFORME debe ser visible y la imagen clara.")
        print("="*40)
        
        foto = input("\nIngrese la ruta o nombre del archivo de la foto: ")
        actividad = input("¿Qué actividad se realizó?: ")
        resumen = input("Resumen detallado de lo que se hizo: ")

        # Estructura del registro
        data = {
            "cedula": cedula,
            "nombre": nombre,
            "fecha": datetime.datetime.now(),
            "foto_entrada": foto,
            "actividad": actividad,
            "resumen": resumen
        }

        try:
            puntos_col.insert_one(data)
            print("\n💾 ¡Registro guardado exitosamente en MongoDB!")
        except Exception as e:
            print(f"\n❌ Error al guardar: {e}")
    else:
        print("\n❌ La cédula no se encuentra registrada en el sistema.")

if __name__ == "__main__":
    ejecutar_registro()
