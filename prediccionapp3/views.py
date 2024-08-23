from rest_framework.views import APIView 
from django.shortcuts import render
from rest_framework import status
from .models import predict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .serializers import DiagnosticoSerializer3, DiagnosticoGetSerializer3
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from datetime import date, datetime
from seguridadapp.models import Diagnostico3, Paciente
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


#Listado de Diagnosticos para el ACV 03
@api_view(['GET'])
def get_diagnostico(request):
    try:
        paciente = request.user.paciente
        if not paciente:
            return Response({'error': 'Paciente no asociado con el usuario.'}, status=status.HTTP_404_NOT_FOUND)
        diagnosticos = Diagnostico3.objects.filter(idPaciente=paciente)
        if not diagnosticos.exists():
            return Response({'message': 'No se encontraron diagnósticos para este paciente.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiagnosticoGetSerializer3(diagnosticos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Prediccion para el ACV 03
@api_view(['POST'])
def create_diagnostico3(request):
    serializer = DiagnosticoSerializer3(data=request.data)
    
    if serializer.is_valid():
        paciente = request.user.paciente 
        
        # Calcular la edad
        today = datetime.today().date()
        birth_date = paciente.fecha_nacimiento
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        data = {
            'genero': 0 if paciente.genero == 'Femenino' else 1,
            'edadRango': obtener_rango_edad(age),
            'etnia': serializer.validated_data.get('etnia', 0),
            'fumador': serializer.validated_data.get('fumador', False),
            'bebedorFrecuente': serializer.validated_data.get('bebedorFrecuente', False),
            'actividadFisica': serializer.validated_data.get('actividadFisica', False),
            'horasDormidas': serializer.validated_data.get('horasDormidas', 0),
        }

        # fumador_map = {
        #     0: 'No',
        #     1: 'Sí',
        # }
        # bebedorFrecuente_map = {
        #     0: 'No',
        #     1: 'Sí',
        # }
        # actividadFisica_map = {
        #     0: 'No',
        #     1: 'Sí',
        # }

        if data['etnia'] == 0:
            etnia = 'Indígena'
        elif data['etnia'] == 1:
            etnia = 'Asiático'
        elif data['etnia'] == 2:
            etnia = 'Negro'
        elif data['etnia'] == 3:
            etnia = 'Hispano'
        elif data['etnia'] == 4:
            etnia = 'Otro'
        elif data['etnia'] == 5:
            etnia = 'Blanco'

        if data['fumador'] == True:
            fumador=1
        else:
            fumador=0
        
        if data['bebedorFrecuente'] == True:
            bebedorFrecuente=1
        else:
            bebedorFrecuente=0
        
        if data['actividadFisica'] == True:
            actividadFisica=1
        else:
            actividadFisica=0

        # Crear la instancia de Diagnostico
        diagnostico = Diagnostico3(
            idPaciente=paciente,
            genero=paciente.genero ,
            edadRango=age,
            etnia=etnia,
            fumador=fumador,
            bebedorFrecuente=bebedorFrecuente,
            actividadFisica=actividadFisica,
            horasDormidas=data['horasDormidas']
        )
        
        # Guardar el diagnostico
        diagnostico.save()

        # Data para la predicción
        prediction_data = [
            data['fumador'],
            data['bebedorFrecuente'],
            data['actividadFisica'],
            data['horasDormidas'],
            data['edadRango'],
            data['genero'],
            data['etnia'],
        ]

        # Predicción
        prediction = predict(prediction_data)        
        # Actualizar el diagnostico con la predicción
        diagnostico.prediccion = prediction
        diagnostico.save()

        return Response({'idDiagnostico3': diagnostico.idDiagnostico3, 'prediccion': diagnostico.prediccion}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='login')
#Form acv03
def prediction_form3(request):
    user = request.user
    request.session['userName_logged'] = user.get_full_name()
    return render(request, 'form-acv3.html', {'userNameLogged':request.session['userName_logged']})


def obtener_rango_edad(edad):
    if 18 <= edad <= 24:
        return 0 
    elif 25 <= edad <= 29:
        return 1  
    elif 30 <= edad <= 34:
        return 2  
    elif 35 <= edad <= 39:
        return 3  
    elif 40 <= edad <= 44:
        return 4 
    elif 45 <= edad <= 49:
        return 5  
    elif 50 <= edad <= 54:
        return 6  
    elif 55 <= edad <= 59:
        return 7  
    elif 60 <= edad <= 64:
        return 8  
    elif 65 <= edad <= 69:
        return 9  
    elif 70 <= edad <= 74:
        return 10  
    elif 75 <= edad <= 79:
        return 11  
    elif edad >= 80:
        return 12 