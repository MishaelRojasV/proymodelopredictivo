from .serializers import PredictionSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
from django.shortcuts import render
from rest_framework import status
from .models import predict

# Prediccion para el ACV 03
class PredictView3(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            features = [
                data['fumador'],
                data['bebedorFrecuente'],
                data['actividadFisica'],
                data['horasDormidas'],
                data['edadRango'],
                data['genero'],
                data['etnia'],
            ]
            try:
                prediction = predict(features)                
                return Response({'prediction': prediction.tolist()})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Form acv02
def prediction_form3(request):
    return render(request, 'form-acv3.html')
