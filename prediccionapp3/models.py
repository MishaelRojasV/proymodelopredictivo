from django.conf import settings
from django.db import models
import numpy as np 
import joblib
import os

try:
    model_path = os.path.join(settings.MEDIA_ROOT, 'kmeans_model2.joblib')
    model = joblib.load(model_path)

    scaler_path = os.path.join(settings.MEDIA_ROOT, 'scalerkmeans_model2.joblib')
    scaler = joblib.load(scaler_path)

    print("Modelo y escalador cargados con éxito")
except Exception as e:
    print(f"Error al cargar o usar el modelo: {e}")


# Cargar el modelo y el escalador
def predict(data):
    # Escalar los datos
    scaled_data = scaler.transform([data])
    # Realizar la predicción
    prediction = model.predict(scaled_data)
    return prediction
