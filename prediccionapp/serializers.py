from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    Genero = serializers.FloatField()
    Edad = serializers.FloatField()
    Hipertension = serializers.FloatField()
    Cardiopatia = serializers.FloatField()
    TipoTrabajo = serializers.FloatField()
    Nivel_GlucosaPromedio = serializers.FloatField()
    ICM = serializers.FloatField()
    EstadoFumador = serializers.FloatField()