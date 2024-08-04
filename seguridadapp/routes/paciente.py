from django.urls import path
from seguridadapp.views import paciente

urlpatterns = [
    path('register/', paciente.register_paciente),
    path('edit/<int:pk>/', paciente.update_paciente),
    #path('create/',agregarusuario ,name="agregarusuario"),
    #path('edit/<int:id>/',editarusuario ,name="editarusuario"),
]