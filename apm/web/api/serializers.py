from rest_framework import serializers
from ..models import *


class SpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specie
        fields = '__all__'


class IrrigatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Irrigator
        fields = '__all__'


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'
