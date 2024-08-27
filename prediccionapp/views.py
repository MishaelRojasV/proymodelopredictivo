from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .serializers import DiagnosticoSerializer,DiagnosticoGetSerializer
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from datetime import date, datetime
from seguridadapp.models import Diagnostico, Paciente
from django.shortcuts import render
from rest_framework import status
from .models import predict
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .ChatBotService import ChatbotService
from django.contrib.sessions.models import Session
from decouple import config

OPENAI_API_KEY = config('OPENAI_API_KEY')
    
@api_view(['POST'])
def chatbot_response(request):
    try:
        paciente = request.user.paciente
        if not paciente:
            return Response({'error': 'Paciente no asociado con el usuario.'}, status=status.HTTP_404_NOT_FOUND)
        diagnosticos = Diagnostico.objects.filter(idPaciente=paciente)
        user_input = request.data.get("message")
        if not user_input:
            return Response({"error": "El campo 'message' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        session_key = request.session.session_key or request.session.create()
        chatbot_service = ChatbotService(openai_api_key=OPENAI_API_KEY,paciente=paciente,diagnosticos=diagnosticos)
        if "imagen" in user_input.lower() or "image" in user_input.lower():
            image_url = chatbot_service.generate_image(prompt="Imagen del cerebro humano afectado por ACV")
            response_message = f"{image_url}"
        else:
            response_message = chatbot_service.get_response(user_input)
            chatbot_service.save_message(user_id=paciente.idPaciente, role='user', content=user_input)
            chatbot_service.save_message(user_id=paciente.idPaciente, role='assistant', content=response_message)
        response = Response({"response": response_message}, status=status.HTTP_200_OK)
        response.set_cookie(key='sessionid', value=request.session.session_key)
        return Response({"response": response_message}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Listado de Diagnosticos para el ACV 01 
@api_view(['GET'])
def get_diagnostico(request):
    try:
        paciente = request.user.paciente
        if not paciente:
            return Response({'error': 'Paciente no asociado con el usuario.'}, status=status.HTTP_404_NOT_FOUND)
        diagnosticos = Diagnostico.objects.filter(idPaciente=paciente)
        if not diagnosticos.exists():
            return Response({'message': 'No se encontraron diagnósticos para este paciente.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiagnosticoGetSerializer(diagnosticos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Prediccion para el ACV 01 
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
            'Genero': 0 if paciente.genero == 'Femenino' else 1,
            'Edad': age,
            'Hipertension': serializer.validated_data.get('Hipertension', 0),
            'Cardiopatia': serializer.validated_data.get('Cardiopatia', 0),
            'TipoTrabajo': serializer.validated_data.get('TipoTrabajo', 0),
            'Nivel_GlucosaPromedio': serializer.validated_data.get('Nivel_GlucosaPromedio', 0),
            'ICM': serializer.validated_data.get('ICM', 0),
            'EstadoFumador': serializer.validated_data.get('EstadoFumador', 0)
        }

        # Mapeo de TipoTrabajo y EstadoFumador
        tipo_trabajo_map = {
            0: 'Trabajador para el gobierno',
            1: 'Nunca trabajó',
            2: 'Trabajador privado',
            3: 'Trabajador por cuenta propia'
        }
        
        estado_fumador_map = {
            0: 'No opina',
            1: 'Anteriormente fumó',
            2: 'Nunca fumó',
            3: 'Fuma'
        }

        # Crear la instancia de Diagnostico
        diagnostico = Diagnostico(
            idPaciente=paciente,
            Genero=paciente.genero,
            Edad=data['Edad'],
            Hipertension=data['Hipertension'],
            Cardiopatia=data['Cardiopatia'],
            TipoTrabajo=tipo_trabajo_map.get(data['TipoTrabajo'], 'Desconocido'),
            Nivel_GlucosaPromedio=data['Nivel_GlucosaPromedio'],
            ICM=data['ICM'],
            EstadoFumador=estado_fumador_map.get(data['EstadoFumador'], 'Desconocido')
        )
        
        # Guardar el diagnostico
        diagnostico.save()

        # Data para la predicción
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

        return Response({'idDiagnostico': diagnostico.idDiagnostico, 'prediccion': diagnostico.prediccion}, status=status.HTTP_201_CREATED)
        # return Response({'prediccion': diagnostico.prediccion}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Form acv01
@login_required(login_url='login')
def prediction_form(request):
    user = request.user
    request.session['userName_logged'] = user.get_full_name()
    return render(request, 'form-acv1.html',{'userNameLogged':request.session['userName_logged']} )