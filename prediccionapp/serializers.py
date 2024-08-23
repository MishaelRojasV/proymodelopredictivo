from seguridadapp.models import Diagnostico
from rest_framework import serializers
from datetime import date
from rest_framework import serializers


class DiagnosticoSerializer(serializers.Serializer):
    Hipertension = serializers.IntegerField()
    Cardiopatia = serializers.IntegerField()
    TipoTrabajo = serializers.IntegerField()
    Nivel_GlucosaPromedio = serializers.FloatField()
    ICM = serializers.FloatField()
    EstadoFumador = serializers.IntegerField()


# class DiagnosticoGetSerializer(serializers.Serializer):
#     Hipertension = serializers.FloatField()
#     Cardiopatia = serializers.FloatField()
#     TipoTrabajo = serializers.IntegerField()
#     Nivel_GlucosaPromedio = serializers.FloatField()
#     ICM = serializers.FloatField()
#     EstadoFumador = serializers.IntegerField() 

class DiagnosticoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ['idDiagnostico','fechaRegistro','Genero', 'Edad', 'Hipertension', 'Cardiopatia', 'TipoTrabajo', 'Nivel_GlucosaPromedio', 'ICM', 'EstadoFumador','prediccion'] 
