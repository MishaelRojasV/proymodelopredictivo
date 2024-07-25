# prediccionapp/serializers.py

from rest_framework import serializers

""" class PredictionSerializer(serializers.Serializer):
    features = serializers.DictField(
        child=serializers.FloatField()
    ) """

class PredictionSerializer(serializers.Serializer):
    Genero = serializers.FloatField()
    Edad = serializers.FloatField()
    TipoTrabajo = serializers.FloatField()
    Hipertension = serializers.FloatField()
    Cardiopatia = serializers.FloatField()
    Nivel_GlucosaPromedio = serializers.FloatField()
    ICM = serializers.FloatField()
    EstadoFumador = serializers.FloatField()