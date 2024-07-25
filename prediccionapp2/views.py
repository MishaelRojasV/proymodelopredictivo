from .serializers import PredictionSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
from django.shortcuts import render
from rest_framework import status
from .models import predict

# Prediccion para el ACV 02
class PredictView2(APIView):
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
            ]
            try:
                prediction = predict(features)                
                return Response({'prediction': prediction.tolist()})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Form acv02
def prediction_form2(request):
    return render(request, 'form-acv2.html')
