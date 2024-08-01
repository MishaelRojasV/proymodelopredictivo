from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .serializers import PredictionSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
from django.shortcuts import render
from rest_framework import status
from .models import predict

# Prediccion para el ACV 01 

class PredictView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            features = [
                data['Genero'],
                data['Edad'],
                data['Hipertension'],
                data['Cardiopatia'],
                data['TipoTrabajo'],
                data['Nivel_GlucosaPromedio'],
                data['ICM'],
                data['EstadoFumador']
            ]
            try:
                prediction = predict(features)                
                return Response({'prediction': prediction.tolist()})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Form acv01
@login_required(login_url='login')
def prediction_form(request):
    user = request.user
    request.session['userName_logged'] = user.get_full_name()
    return render(request, 'form-acv1.html',{'userNameLogged':request.session['userName_logged']} )