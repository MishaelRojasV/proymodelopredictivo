from rest_framework import serializers

class DiagnosticoSerializer2(serializers.Serializer):
    Hipertension = serializers.FloatField()
    Cardiopatia = serializers.FloatField()
    TipoTrabajo = serializers.FloatField()
    Nivel_GlucosaPromedio = serializers.FloatField()
    ICM = serializers.FloatField()