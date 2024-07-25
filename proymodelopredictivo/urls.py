
from django.contrib import admin
from django.urls import path
from seguridadapp.views import views, usuario
from django.urls import path,include
from prediccionapp.views import PredictView, prediction_form
from prediccionapp2.views import PredictView2, prediction_form2
from prediccionapp3.views import PredictView3, prediction_form3


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.acceder, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.salir, name="logout"),

    # Usuarios
    path('usuarios/',include('seguridadapp.routes.usuario'),name="usuarios"),
    path('update-status-user/',usuario.update_user_status,name="update-status-user"),

    path('api/acv1', PredictView.as_view(),name="acv1"),    
    path('prediccion/', prediction_form, name='prediction_form'),

    path('api/acv2', PredictView2.as_view(),name="acv2"),
    path('prediccion2/', prediction_form2, name='prediction2_form'),

    path('api/acv3', PredictView3.as_view(),name="acv3"),
    path('prediccion3/', prediction_form3, name='prediction3_form'),
]
