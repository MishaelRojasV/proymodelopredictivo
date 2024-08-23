from rest_framework import serializers

class DiagnosticoSerializer2(serializers.Serializer):
    Hipertension = serializers.IntegerField()
    Cardiopatia = serializers.IntegerField()
    TipoTrabajo = serializers.IntegerField()
    Nivel_GlucosaPromedio = serializers.FloatField()
    ICM = serializers.FloatField()