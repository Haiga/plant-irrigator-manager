from rest_framework import viewsets
from .serializers import *
from ..models import *


class IrrigatorViewSet(viewsets.ModelViewSet):
    serializer_class = IrrigatorSerializer
    queryset = Irrigator.objects.all()


class SpecieViewSet(viewsets.ModelViewSet):
    serializer_class = SpecieSerializer
    queryset = Specie.objects.all()


class PlantViewSet(viewsets.ModelViewSet):
    serializer_class = PlantSerializer
    queryset = Plant.objects.all()
