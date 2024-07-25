from rest_framework import serializers

class PredictionSerializer(serializers.Serializer):
    fumador = serializers.FloatField()
    bebedorFrecuente = serializers.FloatField()
    actividadFisica	 = serializers.FloatField()
    horasDormidas = serializers.FloatField()
    edadRango = serializers.FloatField()
    genero = serializers.FloatField()
    etnia = serializers.FloatField()