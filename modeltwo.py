import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from pymongo import MongoClient

# Conexión a la base de datos
client = MongoClient('mongodb+srv://yeml:b1NIwHqUFJ9VJ7Sn@cluster0.tnh0n1t.mongodb.net/?retryWrites=true&w=majority')

# Obtener colección de carreras desde la base de datos
career_collection = client.pg.careertwo

# Obtener datos de carreras desde la base de datos
data = list(career_collection.find())

# Obtener los campos específicos de las carreras
areas_estudio = []
habilidades = []
actividades = []
desafios = []
entorno_trabajo = []
interaccion_personas = []
tecnologia = []
objetivo = []
ubicacion = []
profesiones = []

for carrera in data:
    areas_estudio.append(" ".join(carrera["areas_estudio"]))
    habilidades.append(" ".join(carrera["habilidades"]))
    actividades.append(" ".join(carrera["actividades"]))
    desafios.append(" ".join(carrera["desafios"]))
    entorno_trabajo.append(" ".join(carrera["entorno_trabajo"]))
    interaccion_personas.append(" ".join(carrera["interaccion_personas"]))
    tecnologia.append(carrera["tecnologia"])
    objetivo.append(carrera["objetivo"])
    ubicacion.append(" ".join(carrera["ubicacion"]))
    profesiones.append(carrera["nombre"])


# Convertir los campos a datos numéricos
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(["{} {} {} {} {} {} {} {} {}".format(areas, habilidad, actividades, desafios, entorno, interaccion, tecnologia, objetivo, ubicacion) for areas, habilidad, actividades, desafios, entorno, interaccion, tecnologia, objetivo, ubicacion in zip(areas_estudio, habilidades, actividades, desafios, entorno_trabajo, interaccion_personas, tecnologia, objetivo, ubicacion)])
encoder = LabelEncoder()
y = encoder.fit_transform(profesiones)

# Crear modelo de red neuronal
model = Sequential()
model.add(Dense(128, input_dim=X.shape[1], activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dense(len(set(profesiones)), activation="softmax"))

# Compilar modelo
model.compile(loss="sparse_categorical_crossentropy", optimizer=Adam(learning_rate=0.01), metrics=["accuracy"])

# Entrenar modelo
model.fit(X.toarray(), y, epochs=1000, batch_size=8, verbose=0)

# Guardar el modelo entrenado
model.save("modelo_carreras.h5")
