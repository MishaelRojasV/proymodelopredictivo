from django.conf import settings
from django.db import models
import numpy as np 
import joblib
import os

try:
    model_path = os.path.join(settings.MEDIA_ROOT, 'kmeans_model.joblib')
    model = joblib.load(model_path)

    scaler_path = os.path.join(settings.MEDIA_ROOT, 'scalerkmeans_model.joblib')
    scaler = joblib.load(scaler_path)

    print("Modelo y escalador cargados con éxito")
except Exception as e:
    print(f"Error al cargar o usar el modelo: {e}")


# Cargar el modelo y el escalador
def predict(data):
    # Ensure data is a list or array
    data = [data]
    # Scale the data
    scaled_data = scaler.transform(data)
    # Make the prediction
    prediction = model.predict(scaled_data)    
    return int(prediction[0])