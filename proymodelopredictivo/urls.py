
from django.contrib import admin
from django.urls import path
from seguridadapp.views import views
from django.urls import path,include, re_path
from prediccionapp.views import PredictView, prediction_form
from prediccionapp2.views import PredictView2, prediction_form2
from prediccionapp3.views import PredictView3, prediction_form3
from seguridadapp.views import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('documentacion/', include_docs_urls(title='Api Documentation')),
    
    path('admin/', admin.site.urls),
    path('login/', views.login),
    #path('register/', views.register),
    path('paciente/', include('seguridadapp.routes.paciente')),


    path('profile/', views.profile),

    path('api/acv1', PredictView.as_view(),name="acv1"),    
    path('prediccion/', prediction_form, name='prediction_form'),

    path('api/acv2', PredictView2.as_view(),name="acv2"),
    path('prediccion2/', prediction_form2, name='prediction2_form'),

    path('api/acv3', PredictView3.as_view(),name="acv3"),
    path('prediccion3/', prediction_form3, name='prediction3_form'),
]
