from pymongo import MongoClient
from fastapi.security import HTTPBasic
import pymongo.errors

# Conexión a la base de datos
client = MongoClient('mongodb+srv://yeml:b1NIwHqUFJ9VJ7Sn@cluster0.tnh0n1t.mongodb.net/?retryWrites=true&w=majority')
#print(client)
# Funciones para interactuar con la base de datos
security = HTTPBasic()

#mostrar usuarios de la coleccion
def read_Career():
    collection = client.pg.careertwo

    try:
        careers = []
        for document in collection.find():
            career = {
                "_id": str(document["_id"]),
                "nombre": document["nombre"],
                "descripcion": document["descripcion"],
                "areas_estudio": document["areas_estudio"],
                "habilidades": document["habilidades"],
                "actividades": document["actividades"],
                "desafios": document["desafios"],
                "entorno_trabajo": document["entorno_trabajo"],
                "interaccion_personas": document["interaccion_personas"],
                "tecnologia": document["tecnologia"],
                "objetivo": document["objetivo"],
                "ubicacion": document["ubicacion"]
            }
            careers.append(career)
        return careers

    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB:", errorConexion)
        return None

# Llamar a la función para obtener los datos de la colección
careers = read_Career()
