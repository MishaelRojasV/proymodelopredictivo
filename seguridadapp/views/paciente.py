from seguridadapp.serializers import UserSerializer, PacienteSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from seguridadapp.models import Paciente
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from seguridadapp.forms import *

#---------------------------------------------Listar pacientes---------------------------------------------
#@login_required(login_url='login')
def listar_pacientes(request):
    return render(request, 'paciente/listar.html')

#@login_required(login_url='login')
def listar_pacientes_json(request):       
    pacientes = list(Paciente.objects.values())
    data = {'pacientes':pacientes}
    return JsonResponse(data)

#---------------------------------------------Api pacientes---------------------------------------------
@api_view(['POST'])
def register_paciente(request):
    serializer = PacienteSerializer(data=request.data)
    if serializer.is_valid():
        paciente = serializer.save()
        token = Token.objects.get(user=paciente.user)
        return Response({'token': token.key, 'user': serializer.data['user'], 'paciente': serializer.data, "message": "Registro exitoso."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_paciente(request, pk):
    try:
        paciente = Paciente.objects.get(pk=pk)
    except Paciente.DoesNotExist:
        return Response({'error': 'Paciente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PacienteSerializer(paciente, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------------------------Editar paciente---------------------------------------------
#@login_required(login_url='login')
def actualizar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    if request.method == 'POST':
        form = EditarPacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Paciente {paciente} actualizado exitosamente.')
            return redirect('listar_pacientes')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = EditarPacienteForm(instance=paciente)
    return render(request, 'paciente/editar.html', {'form': form})

#------------------------------------------Eliminar paciente ------------------------------------------------
#@login_required
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)   
    paciente.delete()
    messages.success(request, 'Paciente eliminado exitosamente.')
    return redirect('listar_pacientes')

