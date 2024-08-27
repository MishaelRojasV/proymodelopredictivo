from django.urls import path
from seguridadapp.views import medico

urlpatterns = [
    path('', medico.listar_medicos,name="listar_medicos"),
    path('listar_medicos_json', medico.listar_medicos_json,name="listar_medicos_json"),
    path('crear_medico/', medico.creacion_medicos, name='creacion_medicos'),
    path('edit/<int:id>/',medico.actualizar_medico ,name="actualizar_medico"),
    path('delete/<int:id>/',medico.eliminar_medico ,name="eliminar_medico"),

]