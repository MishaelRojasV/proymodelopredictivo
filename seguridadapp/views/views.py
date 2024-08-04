from rest_framework.decorators import api_view
from rest_framework.response import Response
from seguridadapp.serializers import UserSerializer, PacienteSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"message": "Error al Ingresar"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token" : token.key, "user":serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
def profile(request):
    return Response({})