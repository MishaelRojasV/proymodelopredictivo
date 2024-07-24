from django.db.models import Q 
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import is_password_usable
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from email.mime.image import MIMEImage
from seguridadapp.forms import CrearUserForm,EditarUserForm


#---------------------------------------------Listar usuarios---------------------------------------------
@login_required(login_url='login')
def listar_usuarios(request):
    return render(request, 'usuario/listar.html')

@login_required(login_url='login')
def listar_usuarios_json(request):    
    filtro_status = request.GET.get('estado')
    if filtro_status == "activo":
        usuarios = list(User.objects.filter(is_active=True).values())
    elif filtro_status == "inactivo":
        usuarios = list(User.objects.filter(is_active=False).values())
    else:
        usuarios = list(User.objects.values())
    data = {'usuarios':usuarios}
    return JsonResponse(data)

# Actualiza estado del Usuario
@csrf_exempt
def update_user_status(request):
    user_id = request.POST.get('user_id')
    is_active = request.POST.get('is_active') == 'true'  
    try:
        user = User.objects.get(id=user_id)
        user.is_active = is_active
        user.save()
        return JsonResponse({'status': 'success'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    
#---------------------------------------------------------------------------------------------------------


#------------------------------------------Crear USuario --------------------------------------------------
@login_required(login_url='login')
def creacion_usuario(request):
    if request.method == 'POST':
        form = CrearUserForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            evaluador = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            form_instance.save() 
            id = form_instance.id         
            
            #form.save()
            messages.success(request, f'Usuario {username} creado exitosamente.')
            return redirect('listar_usuarios')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = CrearUserForm()
    return render(request, 'usuario/agregar.html', {'form': form})
#---------------------------------------------------------------------------------------------------------

#------------------------------------------Editar USuario ------------------------------------------------
@login_required(login_url='login')
def actualizar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        form = EditarUserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Usuario {username} actualizado exitosamente.')
            return redirect('listar_usuarios')
        else:
            messages.error(request, "El formulario contiene errores. Por favor, corrija")
    else:
        form = EditarUserForm(instance=usuario)
    return render(request, 'usuario/editar.html', {'form': form})

#---------------------------------------------------------------------------------------------------------

#------------------------------------------Eliminar USuario ------------------------------------------------
@login_required
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)   
    if request.user.is_superuser:  
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
    return redirect('listar_usuarios') 

#---------------------------------------------------------------------------------------------------------