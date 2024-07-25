from wsgiref.validate import validator
from django.forms import Form
from django.shortcuts import render, redirect
from typing import Generic
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,Permission,Group
from django.core.paginator import Paginator
from django.db.models import Q 
from django.contrib.auth.decorators import login_required

# Create your views here.
def acceder(request):
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario, password=password)
            if usuario is not None:
                login(request, usuario)              
                request.session['userName_logged'] = usuario.first_name + ' '+ usuario.last_name
                request.session['user_logged'] = usuario.username
                return redirect("home")
            else:
                messages.error(request, "Datos incorrecto.")
        else:
            nombre_usuario=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user_exits=(User.objects.filter(username=nombre_usuario).count()>0)
            if user_exits:
                messages.error(request, "Password incorrecto.")
            else:
                messages.error(request, "Usuario incorrecto.")
    form=AuthenticationForm()
    return render(request, "login.html", {"form": form})

#Funcion para mostrar la vista "Home"

def home(request):
    return render(request, "home.html")

#Funcion para "cerrar sesion"
@login_required(login_url='login')
def salir(request):    
    del request.session['user_logged']
    del request.session['userName_logged']
    logout(request)
    messages.info(request,"Sesión cerrada exitosamente")
    return redirect("login")


