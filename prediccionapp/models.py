from django.db import models
import joblib # type: ignore


import joblib
import numpy as np

try:
    model = joblib.load('C:/Users/USER/Desktop/proy-analitica_negocios/proymodelopredictivo/prediccionapp/media/rf_model.joblib')
    scaler = joblib.load('C:/Users/USER/Desktop/proy-analitica_negocios/proymodelopredictivo/prediccionapp/media/scaler_rf.joblib')  
    print("Modelo cargado con éxito")



except Exception as e:
    print(f"Error al cargar o usar el modelo: {e}")

# Cargar el modelo y el escalador


def predict(data):
    # Escalar los datos
    scaled_data = scaler.transform([data])
    # Realizar la predicción
    prediction = model.predict(scaled_data)
    return prediction
