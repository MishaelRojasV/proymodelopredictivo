from seguridadapp.serializers import UserSerializer, PacienteSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from seguridadapp.models import Medico
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from seguridadapp.forms import *

#---------------------------------------------Listar medico---------------------------------------------
#@login_required(login_url='login')
def listar_medicos(request):
    return render(request, 'medico/listar.html')

#@login_required(login_url='login')
def listar_medicos_json(request):       
    medicos = list(Medico.objects.values())
    data = {'medicos':medicos}
    return JsonResponse(data)

#---------------------------------------------Crear MEDICO---------------------------------------------
#@login_required(login_url='login')
def creacion_medicos(request):
    if request.method == 'POST':
        form = CrearMedicoForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, f'Médico creado exitosamente.')
            return redirect('listar_medicos')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = CrearMedicoForm()
    return render(request, 'medico/agregar.html', {'form': form})

#---------------------------------------------Editar usuarios---------------------------------------------
#@login_required(login_url='login')
def actualizar_medico(request, id):
    medico = get_object_or_404(Medico, pk=id)
    if request.method == 'POST':
        form = EditarMedicoForm(request.POST, instance=medico)
        if form.is_valid():
           form.save()
           messages.success(request, f'Médico actualizado exitosamente.')
           return redirect('listar_medicos')
        else:
           messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = EditarMedicoForm(instance=medico)
    return render(request, 'medico/editar.html', {'form': form})

#------------------------------------------Eliminar USuario ------------------------------------------------
#@login_required
def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, pk=id)   
    medico.delete()
    messages.success(request, 'Médico eliminado exitosamente.')
    return redirect('listar_medicos')