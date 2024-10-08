from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from seguridadapp.serializers import UserSerializer, PacienteSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from seguridadapp.models import Paciente
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
import requests

# Api para Login
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        response = requests.post('http://127.0.0.1:8080/login/', data={'username': username, 'password': password})
        data = response.json()

        if response.status_code == 200:
            token = data.get('token')
            return JsonResponse(data)
        else:
            return JsonResponse({"error": data.get('message', 'Error desconocido')}, status=response.status_code)

    return render(request, 'login.html')

@login_required(login_url='login_view')
def logout_view(request):
    token = request.headers.get('Authorization')
    user = None
    if token:
        try:
            token_key = token.split()[1]
            Token.objects.get(key=token_key).delete()  
        except Token.DoesNotExist:
            pass

    logout(request)  
    return JsonResponse({'message': 'Logout exitoso'}, status=200)

def register_view(request):
    return render(request, 'register.html') 

def home_view(request):    
    return render(request, 'home.html')

def register_view(request):
    return render(request, 'register.html') 

@api_view(['POST'])
def profile(request):
    return Response({})

# Api para Logout
@api_view(['POST',])
def logout(request):
    try:
        # Obtener el token del usuario autenticado y eliminarlo
        request.user.auth_token.delete()
        return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
    except AttributeError:
        return Response({"error": "El usuario no tiene un token de autenticación"}, status=status.HTTP_400_BAD_REQUEST)


