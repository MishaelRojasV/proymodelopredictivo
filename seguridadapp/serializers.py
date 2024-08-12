from seguridadapp.models import Paciente, Diagnostico
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']


class PacienteSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Paciente
        fields = ['user', 'nombres', 'apPaterno', 'apMaterno', 'email', 'celular', 'genero', 'fecha_nacimiento', 'eliminado']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(username=user_data['username'])
        user.set_password(user_data['password'])
        user.save()        
        paciente = Paciente.objects.create(user=user, **validated_data)
        # Crear el token
        Token.objects.create(user=user)
        return paciente
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        # Actualizar el usuario
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        password = user_data.get('password', None)
        if password:
            user.set_password(password)
        user.save()

        # Actualizar el paciente
        instance.nombres = validated_data.get('nombres', instance.nombres)
        instance.apPaterno = validated_data.get('apPaterno', instance.apPaterno)
        instance.apMaterno = validated_data.get('apMaterno', instance.apMaterno)
        instance.email = validated_data.get('email', instance.email)
        instance.celular = validated_data.get('celular', instance.celular)
        instance.genero = validated_data.get('genero', instance.genero)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.eliminado = validated_data.get('eliminado', instance.eliminado)
        instance.save()
        
        return instance


