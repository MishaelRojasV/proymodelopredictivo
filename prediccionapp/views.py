from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status
from .models import predict
from .serializers import PredictionSerializer
import numpy as np

class PredictView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            features = [
                data['Genero'],
                data['Edad'],
                data['TipoTrabajo'],
                data['Hipertension'],
                data['Cardiopatia'],
                data['Nivel_GlucosaPromedio'],
                data['ICM'],
                data['EstadoFumador']
            ]
            try:
                # Realizar la predicción
                prediction = predict(features)
                
                #features_array = np.array([features])
                return Response({'prediction': prediction.tolist()})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def prediction_form(request):
    return render(request, 'form-acv1.html')