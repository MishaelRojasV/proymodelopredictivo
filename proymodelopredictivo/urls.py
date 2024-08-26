
from django.contrib import admin
from django.urls import path
from seguridadapp.views import views
from django.urls import path,include, re_path
from prediccionapp.views import create_diagnostico, prediction_form,get_diagnostico, chatbot_response
from prediccionapp2.views import create_diagnostico2
from prediccionapp2.views import prediction_form2
from prediccionapp3.views import create_diagnostico3, prediction_form3
from seguridadapp.views import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    #Documentacion
    path('documentacion/', include_docs_urls(title='Api Documentation')),

    #administrador
    path('admin/', admin.site.urls),
    
    #Cuenta
    path('login/', views.login),
    path('logout/', views.logout),
    
    path('auth/login/', views.login_view, name='login_view'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout_view'),
    #Paciente
    path('paciente/', include('seguridadapp.routes.paciente')),

    #Prediccion
    path('api/acv1/create/', create_diagnostico,name="acv1"),
    path('api/acv1/', get_diagnostico,name="get_diagnostico"),
    path('api/acv1/chatbot/',chatbot_response,name="chatbot_response" ), 
    # path('prediccion/', prediction_form, name='prediction_form'),

    path('api/acv2/create/', create_diagnostico2,name="acv2"),
    path('prediccion2/', prediction_form2, name='prediction2_form'),

    path('api/acv3/create/', create_diagnostico3,name="acv3"),
    path('prediccion3/', prediction_form3, name='prediction3_form'),
]
