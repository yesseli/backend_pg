import uvicorn
import numpy as np
from fastapi import HTTPException, Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from pydantic import BaseModel
from user import authenticate_user, read_User, insert_User, modify_User, delete_User
from user import HTTPBasicCredentials
from model import model, vectorizer, encoder 


# Aplicacion web con FastAPI 
app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    password: str
    role: str

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#endpoint para obtener una predicción de profesión basada en los datos de entrada
@app.post("/prediccion")
async def obtener_prediccion(datos: dict):

    nuevo_dato = [datos['intereses'], datos['habilidades']]
    nuevo_dato_numerico = vectorizer.transform([' '.join(nuevo_dato)])
    nueva_prediccion_numerica = model.predict(nuevo_dato_numerico.toarray())
    nueva_prediccion = encoder.inverse_transform(np.argmax(nueva_prediccion_numerica, axis=-1))

    if nueva_prediccion[0] == "otro":
        raise HTTPException(status_code=404, detail="No se encontró una carrera adecuada para los intereses y habilidades proporcionados.")

    return {'profesion predicha': nueva_prediccion[0]}


@app.post("/login")
def login(credentials: HTTPBasicCredentials):
    if not authenticate_user(credentials):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"mensaje": "Inicio de sesión exitoso"}

@app.get("/users")
def get_users():
    users = read_User()
    return {"users": users}

@app.post("/users")
def create_user(user: User):
    insert_User(user.name, user.email, user.password, user.role)
    return {"message": "Usuario creado correctamente"}

@app.put("/users/{user_id}")
def update_user(user_id: str, user_input: User):
    modify_User(user_id, user_input.name, user_input.email, user_input.password, user_input.role)
    return {"message": "Usuario actualizado correctamente"}

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    delete_User(user_id)
    return {"message": "Usuario eliminado correctamente"}