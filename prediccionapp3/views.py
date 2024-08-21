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
        
        # Prepare the Diagnostico data
        data = {
            'genero': 0 if paciente.genero == 'Masculino' else 1,
            'edad': age,
            'etnia': serializer.validated_data.get('etnia', ''),
            'fumador': serializer.validated_data.get('fumador', ''),
            'bebedorFrecuente': serializer.validated_data.get('bebedorFrecuente', ''),
            'actividadFisica': serializer.validated_data.get('actividadFisica', ''),
            'horasDormidas': serializer.validated_data.get('horasDormidas', '')
        }

        print(data)

        fumador_map = {
            0: 'paciente no fumador',
            1: 'paciente fumador',
        }
        bebedorFrecuente_map = {
            0: 'no es bebedor frecuente',
            1: 'es bebedor frecuente',
        }
        actividadFisica_map = {
            0: 'no realiza acividad fisica',
            1: 'realiza actividad fisica',
        }

        # Crear la instancia de Diagnostico
        diagnostico = Diagnostico3(
            idPaciente=paciente,
            Genero=data['Genero'],
            Edad=data['Edad'],
            Etnia=data['Etnia'],
            Fumador=fumador_map,
            BebedorFrecuente=bebedorFrecuente_map,
            ActividadFisica=actividadFisica_map,
            HorasDormidas=data['HorasDormidas']
        )
        
        # Guardar el diagnostico
        diagnostico.save()

        # Data para la predicción
        prediction_data = [
            data['Genero'],
            data['Edad'],
            data['Fumador'],
            data['BebedorFrecuente'],
            data['ActividadFisica'],
            data['HorasDormidas']
        ]

        # Predicción
        prediction = predict(prediction_data)        
        # Actualizar el diagnostico con la predicción
        diagnostico.prediccion = prediction
        diagnostico.save()

        
        # Enviar correo electrónico al paciente
        context = {
            'nombre_paciente': f'{paciente.nombres} {paciente.apPaterno} {paciente.apMaterno}',
            'diagnostico': diagnostico,
            'prediccion': diagnostico.prediccion
        }
        html_message = render_to_string('envio-correo.html', context)

        # Crear y enviar el correo
        email = EmailMessage(
            subject='RESULTADO DE DIAGNÓSTICO',
            body=html_message,
            from_email='NEURO IA',
            to=[paciente.email]
        )
        email.content_subtype = "html"  # Indica que el contenido es HTML
        
        try:
            email.send()
        except Exception as e:
            return Response({'error': f'Error al enviar el correo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'idDiagnostico3': diagnostico.idDiagnostico3, 'prediccion': diagnostico.prediccion}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='login')
#Form acv03
def prediction_form3(request):
    user = request.user
    request.session['userName_logged'] = user.get_full_name()
    return render(request, 'form-acv3.html', {'userNameLogged':request.session['userName_logged']})
