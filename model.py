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
career_collection = client.pg.career

# Obtener datos de carreras desde la base de datos
data = list(career_collection.find())

# Separar los datos en intereses, habilidades y profesiones
intereses = []
habilidades = []
profesiones = []
for carrera in data:
    intereses.append(" ".join(carrera["intereses"]))
    habilidades.append(" ".join(carrera["habilidades"]))
    profesiones.append(carrera["nombre"])

# Convertir intereses y habilidades a datos numéricos
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(["{} {}".format(interes, habilidad) for interes, habilidad in zip(intereses, habilidades)])
encoder = LabelEncoder()
y = encoder.fit_transform(profesiones)

# Crear modelo de red neuronal
model = Sequential()
model.add(Dense(64, input_dim=X.shape[1], activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dense(len(set(profesiones)), activation="softmax"))

# Compilar modelo
model.compile(loss="sparse_categorical_crossentropy", optimizer=Adam(learning_rate=0.01), metrics=["accuracy"])

# Entrenar modelo
model.fit(X.toarray(), y, epochs=1000, batch_size=8, verbose=0)

# Guardar el modelo entrenado
model.save("modelo_carreras.h5")