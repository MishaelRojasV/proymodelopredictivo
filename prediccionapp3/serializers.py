from seguridadapp.models import Diagnostico3
from rest_framework import serializers
from datetime import date
from rest_framework import serializers

class DiagnosticoSerializer3(serializers.Serializer):
    etnia = serializers.IntegerField()
    fumador = serializers.BooleanField()
    bebedorFrecuente = serializers.BooleanField()
    actividadFisica = serializers.BooleanField()
    horasDormidas = serializers.IntegerField()

class DiagnosticoGetSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico3
        fields = ['idDiagnostico3','genero','edadRango', 'etnia', 'fumador', 'bebedorFrecuente', 'actividadFisica', 'horasDormidas', 'prediccion','fechaRegistro'] 
