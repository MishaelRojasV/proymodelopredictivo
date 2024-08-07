from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .serializers import DiagnosticoSerializer
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework.decorators import api_view
from datetime import date, datetime
from seguridadapp.models import Diagnostico, Paciente
from django.shortcuts import render
from rest_framework import status
from .models import predict

# Prediccion para el ACV 01 

""" class PredictView(APIView):
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """


@api_view(['POST'])
def create_diagnostico(request):
    serializer = DiagnosticoSerializer(data=request.data)
    
    if serializer.is_valid():
        paciente = request.user.paciente 
        
        # Calcular la edad
        today = datetime.today().date()
        birth_date = paciente.fecha_nacimiento
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Prepare the Diagnostico data
        data = {
            'Genero': 0 if paciente.genero == 'Masculino' else 1,
            'Edad': age,
            'Hipertension': serializer.validated_data.get('Hipertension', 0),
            'Cardiopatia': serializer.validated_data.get('Cardiopatia', 0),
            'TipoTrabajo': serializer.validated_data.get('TipoTrabajo', 0),
            'Nivel_GlucosaPromedio': serializer.validated_data.get('Nivel_GlucosaPromedio', 0),
            'ICM': serializer.validated_data.get('ICM', 0),
            'EstadoFumador': serializer.validated_data.get('EstadoFumador', 0)
        }

        print(data)

        if data['TipoTrabajo'] == 0:
            tipo_trabajo = 'Trabajador para el gobierno'
        elif data['TipoTrabajo'] == 1:
            tipo_trabajo = 'Nunca trabajó'
        elif data['TipoTrabajo'] == 2:
            tipo_trabajo = 'Trabajador privado'
        elif data['TipoTrabajo'] == 3:
            tipo_trabajo = 'Trabajador por cuenta propia'
            
        if data['EstadoFumador'] == 0:
            estado_fumador = 'No opina'
        elif data['EstadoFumador'] == 1:
            estado_fumador = 'Anteriormente fumó'
        elif data['EstadoFumador'] == 2:
            estado_fumador = 'Nunca fumó'
        elif data['EstadoFumador'] == 3:
            estado_fumador = 'Fuma'

        # Create the Diagnostico instance
        diagnostico = Diagnostico(
            idPaciente=paciente,
            Genero=paciente.genero,
            Edad=data['Edad'],
            Hipertension=data['Hipertension'],
            Cardiopatia=data['Cardiopatia'],
            TipoTrabajo=tipo_trabajo,
            Nivel_GlucosaPromedio=data['Nivel_GlucosaPromedio'],
            ICM=data['ICM'],
            EstadoFumador=estado_fumador
        )
        
        #Guardar el diagnostico
        diagnostico.save()

        # Data para la prediccion
        prediction_data = [
            data['Genero'],
            data['Edad'],
            data['Hipertension'],
            data['Cardiopatia'],
            data['TipoTrabajo'],
            data['Nivel_GlucosaPromedio'],
            data['ICM'],
            data['EstadoFumador']
        ]

        # Prediccion
        prediction = predict(prediction_data)
        
        # Actualizar el diagnotico con la prediccion
        diagnostico.prediccion = prediction
        diagnostico.save()

        return Response({'idDiagnostico': diagnostico.idDiagnostico, 'prediccion': diagnostico.prediccion}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Form acv01
@login_required(login_url='login')
def prediction_form(request):
    user = request.user
    request.session['userName_logged'] = user.get_full_name()
    return render(request, 'form-acv1.html',{'userNameLogged':request.session['userName_logged']} )