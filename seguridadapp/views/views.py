from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from seguridadapp.serializers import UserSerializer, PacienteSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from seguridadapp.models import Paciente

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"message": "Error al Ingresar"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    paciente = Paciente.objects.filter(user=user).first()
    user_serializer = UserSerializer(instance=user)
    paciente_serializer = PacienteSerializer(instance=paciente)
    return Response({"token" : token.key, "user":user_serializer.data,"paciente": paciente_serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
def profile(request):
    return Response({})

@api_view(['POST',])
#@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Obtener el token del usuario autenticado y eliminarlo
        request.user.auth_token.delete()
        return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
    except AttributeError:
        return Response({"error": "El usuario no tiene un token de autenticación"}, status=status.HTTP_400_BAD_REQUEST)
