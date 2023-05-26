from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import bcrypt
import jwt
import pymongo.errors

# Conexión a la base de datos
client = MongoClient('mongodb+srv://yeml:b1NIwHqUFJ9VJ7Sn@cluster0.tnh0n1t.mongodb.net/?retryWrites=true&w=majority')
#print(client)
# Funciones para interactuar con la base de datos
security = HTTPBasic()

# clave secreta para los tokens
SECRET_KEY = "mi_clave_secreta"

# Función para hashear una contraseña
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Login de usuario
def authenticate_user(credentials: HTTPBasicCredentials):
    users_collection = client.pg.user
    user = users_collection.find_one({"email": credentials.username})
    if user:
        stored_hash = user["password"].encode('utf-8')
        entered_password = credentials.password.encode('utf-8')
        
        if bcrypt.checkpw(entered_password, stored_hash):
            return generate_token(credentials.username, [user["role"]])
    raise HTTPException(status_code=401, detail="Invalid email or password")

# Generar un token JWT 
def generate_token(username, roles):
    payload = {"username": username, "roles": roles}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print("Token generado:", token)
    return token

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

# Roles permitidos
allowed_roles = ['admin', 'student']


# Verificar el rol del usuario y su permiso
def has_role(allowed_roles):
    def decorator(func):
        async def wrapper( request: Request):
            token = get_token_from_cookie(request)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_roles = payload.get("roles", [])
                if any(role in allowed_roles for role in user_roles):
                    return await func(request)
                raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta ruta")
            except jwt.exceptions.DecodeError:
                raise HTTPException(status_code=401, detail="Token inválido")
            except jwt.exceptions.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expirado")
        return wrapper
    return decorator

def get_user_role(username):
    collection = client.pg.user
    user = collection.find_one({"email": username})
    if user:
        return user["role"]
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")


# Obtener el token de la cookie
def get_token_from_cookie(request: Request):
    if "token" in request.cookies:
        return request.cookies["token"]
    raise HTTPException(status_code=401, detail="Token no encontrado en la cookie")




