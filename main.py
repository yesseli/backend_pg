import uvicorn
from fastapi import HTTPException, Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
<<<<<<< HEAD
from pydantic import BaseModel

from user import authenticate_user, read_User, insert_User, modify_User, delete_User
from user import HTTPBasicCredentials
=======

from auth import authenticate_user
from auth import HTTPBasicCredentials
from response import save_response
>>>>>>> 4645186d6d830a5c183783159d8e6340f178c556

# Datos de prueba para el entrenamiento
data = [    ['tecnologia', 'analisis numerico', 'ingeniero de software'],
    ['arte', 'creatividad', 'disenador grafico'],
    ['ciencias sociales', 'comunicacion', 'periodista'],
    ['salud', 'empatia', 'psicologo clinico'],
    ['deportes', 'trabajo en equipo', 'entrenador deportivo'],
    ['tecnologia', 'comunicacion', 'marketing digital'],
    ['animales', 'empatia', 'veterinario'],
    ['deportes', 'autos', 'piloto de carreras'],
    ['cocina', 'reposteria', 'repostero y pastelero'],
    ['cocina', 'comida', 'cocinero'],
    ['negocios', 'liderazgo', 'analista financiero'],
    ['literatura', 'comprension lectora', 'critico literario'],
    ['arquitectura', 'diseno arquitectonico', 'arquitecto'],
    ['decoracion', 'creatividad', 'disenador de interiores'],
    ['comunicacion', 'pensamiento creativo', 'relaciones publicas'],
    ['educacion', 'comunicacion efectiva', 'profesor'],
    ['quimico', 'notacion cientifica', 'quimico'],
    ['crear', 'curiosidad', 'cientifico'],
    ['arquitectura', 'autos', 'ingeniero mecanico']
]

# Separar los datos en interes, habilidades y profesion
interes = []
habilidades = []
profesion = []
for row in data:
    interes.append(row[0])
    habilidades.append(row[1])
    profesion.append(row[2])

# Convertir interes y habilidades a datos numericos
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([' '.join(i) for i in zip(interes, habilidades)])
encoder = LabelEncoder()
y = encoder.fit_transform(profesion)

# Crear modelo de red neuronal
model = Sequential()
model.add(Dense(10, input_dim=X.shape[1], activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(len(set(profesion)), activation='softmax'))

# Compilar modelo
model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Entrenar modelo
model.fit(X.toarray(), y, epochs=1000, batch_size=8, verbose=0)


# Aplicacion web con FastAPI 
app = FastAPI()

<<<<<<< HEAD
class User(BaseModel):
    name: str
    email: str
    password: str
    role: str

=======
>>>>>>> 4645186d6d830a5c183783159d8e6340f178c556
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#endpoint para obtener una predicción de profesión basada en los datos de entrada
@app.post("/prediccion")
async def obtener_prediccion(datos: dict):

    nuevo_dato = [datos['interes'], datos['habilidades']]
    nuevo_dato_numerico = vectorizer.transform([' '.join(nuevo_dato)])
    nueva_prediccion_numerica = model.predict(nuevo_dato_numerico.toarray())
    nueva_prediccion = encoder.inverse_transform(np.argmax(nueva_prediccion_numerica, axis=-1))
    return {'profesion_predicha': nueva_prediccion[0]}

<<<<<<< HEAD
=======

>>>>>>> 4645186d6d830a5c183783159d8e6340f178c556
@app.post("/login")
def login(credentials: HTTPBasicCredentials):
    if not authenticate_user(credentials):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"mensaje": "Inicio de sesión exitoso"}

<<<<<<< HEAD
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
=======
>>>>>>> 4645186d6d830a5c183783159d8e6340f178c556
