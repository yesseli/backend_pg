import numpy as np
from fastapi import HTTPException, Depends, Request
from starlette.responses import Response
from fastapi import FastAPI, APIRouter
from fastapi.security import HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from user import (authenticate_user, read_User, insert_User, modify_User, delete_User, 
generate_token, get_token_from_cookie, has_role, get_user_role, allowed_roles, login_required)
from model import model, vectorizer, encoder
from modeltwo import model as modeltwo, vectorizer as vectorizertwo, encoder as encodertwo
from starlette.responses import JSONResponse
from career import read_Career


# Aplicacion web con FastAPI 
app = FastAPI()
router = APIRouter()

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
    expose_headers=["Set-Cookie"],
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
def login(credentials: HTTPBasicCredentials, response: Response):
    if not authenticate_user(credentials):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    role = get_user_role(credentials.username)

    # Generar el token JWT con los datos del usuario
    token = generate_token(credentials.username, [role])

    # Establecer la cookie en la respuesta
    response.set_cookie(key="token", value=token, samesite="None")
    print("Inicio de sesión exitoso. Rol del usuario:", role)

    return {"message": f"Inicio de sesión exitoso. Rol del usuario: {role}", "token": token, "role": role}
    

def get_users(request: Request):
    users = read_User()
    return {"users": users}
@app.get("/users")
@has_role(["admin"])
@login_required
async def get_users_protected(request: Request):
    return get_users(request)


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


@app.post("/logout")
def logout(response: Response):
    response = JSONResponse({"message": "Cierre de sesión exitoso"})
    response.delete_cookie("token", path="/", domain="localhost")

    return response


@app.post("/predicciontwo")
async def obtener_prediccionn(datos: dict):
    nuevo_dato = {
        "areas_estudio": datos['areas_estudio'],
        "habilidades": datos['habilidades'],
        "actividades": datos['actividades'],
        "desafios": datos['desafios'],
        "entorno_trabajo": datos['entorno_trabajo'],
        "interaccion_personas": datos['interaccion_personas'],
        "tecnologia": datos['tecnologia'],
        "objetivo": datos['objetivo'],
        "ubicacion": datos['ubicacion']
    }

    nuevo_dato_texto = "{} {} {} {} {} {} {} {} {}".format(
        " ".join(nuevo_dato['areas_estudio']),
        " ".join(nuevo_dato['habilidades']),
        " ".join(nuevo_dato['actividades']),
        " ".join(nuevo_dato['desafios']),
        " ".join(nuevo_dato['entorno_trabajo']),
        " ".join(nuevo_dato['interaccion_personas']),
        nuevo_dato['tecnologia'],
        nuevo_dato['objetivo'],
        " ".join(nuevo_dato['ubicacion'])
    )

    nuevo_dato_numerico = vectorizertwo.transform([nuevo_dato_texto])
    nueva_prediccion_numerica = modeltwo.predict(nuevo_dato_numerico.toarray())
    nueva_prediccion = encodertwo.inverse_transform(np.argmax(nueva_prediccion_numerica, axis=-1))

    if nueva_prediccion[0] == "otro":
        raise HTTPException(status_code=404, detail="No se encontró una carrera adecuada para los datos proporcionados.")
    print(nueva_prediccion)
    return {'profesion_predicha': nueva_prediccion[0]}



@app.get("/careers")
def get_career():
    careers = read_Career()
    return {"careers": careers}
    
