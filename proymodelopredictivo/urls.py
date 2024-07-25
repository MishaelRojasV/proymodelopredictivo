
from django.contrib import admin
from django.urls import path
from seguridadapp.views import views, usuario
from django.urls import path,include
from prediccionapp.views import PredictView, prediction_form


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('login/', views.acceder, name='login'),
    path('logout/', views.salir, name="logout"),

    # Usuarios
    path('usuarios/',include('seguridadapp.routes.usuario'),name="usuarios"),
    path('update-status-user/',usuario.update_user_status,name="update-status-user"),

    path('api/acv1', PredictView.as_view(),name="acv1"),    
    path('prediccion/', prediction_form, name='prediction_form'),
]
