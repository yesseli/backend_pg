from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.security import HTTPAuthorizationCredentials


import pymongo.errors

# Conexión a la base de datos
client = MongoClient('mongodb+srv://yeml:b1NIwHqUFJ9VJ7Sn@cluster0.tnh0n1t.mongodb.net/?retryWrites=true&w=majority')
#print(client)
# Funciones para interactuar con la base de datos
security = HTTPBasic()

# Función para hashear una contraseña
def hash_password(password):
    return generate_password_hash(password)

#login usuario 
def authenticate_user(credentials: HTTPBasicCredentials):
    users_collection = client.pg.user
    user = users_collection.find_one({"email": credentials.username})
    if user and check_password_hash(user["password"], credentials.password):
        return True
    raise HTTPException(status_code=401, detail="Invalid email or password")


#mostrar usuarios de la coleccion
def read_User():
    collection = client.pg.user
    try:
        users = []
        for document in collection.find():
            user = {
                "_id": str(document["_id"]),
                "name": document["name"],
                "email": document["email"],
                "role": document["role"]
            }
            users.append(user)
        return users

    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB:", errorConexion)
        return None

# Llamar a la función para obtener los datos de la coleccion
users = read_User()

#insertar usuario en la coleccion 
def insert_User(name, email, password, role):
    collection = client.pg.user
    try:
        hashed_password = hash_password(password)
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role
        }
        result = collection.insert_one(user_data)
        print("Usuario insertado con el ID:", result.inserted_id)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB:", errorConexion)


#Actualizar usuario en la coleccion
def modify_User(user_id, name, email, password, role):
    collection = client.pg.user
    try:
        # Verificar si el usuario existe en la colección
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            hashed_password = hash_password(password)
            # Actualizar los campos del usuario con los nuevos valores
            user_data = {
                "name": name,
                "email": email,
                "password": hashed_password,
                "role": role
            }
            collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
            print("Usuario actualizado correctamente")
        else:
            print("El usuario no existe en la colección")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB:", errorConexion)

#eliminar un usuario de la coleccion
def delete_User(user_id):
    collection = client.pg.user
    try:
        # Verificar si el usuario existe en la colección
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            collection.delete_one({"_id": ObjectId(user_id)})
            print("Usuario eliminado correctamente")
        else:
            print("El usuario no existe en la colección")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB:", errorConexion)
