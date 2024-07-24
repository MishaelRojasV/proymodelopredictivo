
from django.contrib import admin
from django.urls import path
from seguridadapp.views import views, usuario
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.acceder, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.salir, name="logout"),

    # Usuarios
    path('usuarios/',include('seguridadapp.routes.usuario'),name="usuarios"),
    path('update-status-user/',usuario.update_user_status,name="update-status-user"),
]
