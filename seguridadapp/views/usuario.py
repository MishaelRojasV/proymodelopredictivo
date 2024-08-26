from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

#---------------------------------------------Listar usuarios---------------------------------------------
#@login_required(login_url='login')
def listar_usuarios(request):
    return render(request, 'usuario/listar.html')

#@login_required(login_url='login')
def listar_usuarios_json(request):       
    usuarios = list(User.objects.values())
    data = {'usuarios':usuarios}
    return JsonResponse(data)