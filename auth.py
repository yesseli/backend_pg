from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Conexión a la base de datos
client = MongoClient('mongodb+srv://yeml:b1NIwHqUFJ9VJ7Sn@cluster0.tnh0n1t.mongodb.net/?retryWrites=true&w=majority')
print(client)
# Funciones para interactuar con la base de datos
security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials):
    users_collection = client.pg.user
    user = users_collection.find_one({"email": credentials.username})
    if user and user["password"] == credentials.password:
        return True
    raise HTTPException(status_code=401, detail="Invalid email or password")


   
