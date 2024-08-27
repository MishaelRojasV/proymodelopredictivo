from django.urls import path
from seguridadapp.views import paciente

urlpatterns = [
    path('', paciente.listar_pacientes,name="listar_pacientes"),
    path('listar_pacientes_json', paciente.listar_pacientes_json,name="listar_pacientes_json"),
    path('register/', paciente.register_paciente),
    path('edit/<int:id>/', paciente.actualizar_paciente),
    path('delete/<int:id>/',paciente.eliminar_paciente ,name="eliminar_paciente"),

    #path('create/',agregarusuario ,name="agregarusuario"),
    #path('edit/<int:id>/',editarusuario ,name="editarusuario"),
]