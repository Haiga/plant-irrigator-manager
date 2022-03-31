from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .api.serializers import IrrigatorSerializer
from .models import Plant, Irrigator, Specie
from django.db.models import Avg, Sum, F, ExpressionWrapper, FloatField
from django.core import serializers


# Create your views here.

class IrrigatorManageApi(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get_irrigator_must_supply(self, id):
        necessary_supply_of_irrigator = \
            Plant.objects.filter(irrigator__id=id).aggregate(Sum('specie__water_consumption'))[
                'specie__water_consumption__sum']
        return Response({"irrigator_must_supply": necessary_supply_of_irrigator}
                        , status=status.HTTP_200_OK)

    def get_irrigator_max_supply(self, id):
        return Response({"irrigator_current_supply": Irrigator.objects.get(id=id).water_flow}
                        , status=status.HTTP_200_OK)

    def get_irrigator_report(self, id):
        irrigator = Irrigator.objects.get(id=id)
        irrigator_current_supply = irrigator.water_flow if irrigator.status else 0
        necessary_supply_of_irrigator = \
            Plant.objects.filter(irrigator__id=id).aggregate(Sum('specie__water_consumption'))[
                'specie__water_consumption__sum']
        situation = "Overload" if necessary_supply_of_irrigator > irrigator_current_supply else "Working"
        necessary_action = ""
        if situation == "Overload":
            if not irrigator.status:
                necessary_action = f"Turn On Irrigator and adjust water flow to {necessary_supply_of_irrigator}"
            else:
                necessary_action = f"Increase water flow in {necessary_supply_of_irrigator - irrigator_current_supply}"
        else:
            necessary_action = "None"

        return Response(
            {
                "irrigator_current_supply": irrigator_current_supply,
                "necessary_supply_of_irrigator": necessary_supply_of_irrigator,
                "situation": situation,
                "necessary_action": necessary_action,
            }
            , status=status.HTTP_200_OK)

    def get(self, request, id=None, type=None, *args, **kwargs):
        if type == "get_irrigator_must_supply":
            return self.get_irrigator_must_supply(id)

        if type == "get_irrigator_max_supply":
            return self.get_irrigator_max_supply(id)

        if type == "get_irrigator_report":
            return self.get_irrigator_report(id)

        return Response(status=status.HTTP_404_NOT_FOUND)


class IrrigatorsDetailListApi(APIView):
    def get(self, request, *args, **kwargs):
        irrigators = Plant.objects.values('irrigator__id', 'irrigator__description', 'irrigator__water_flow',
                                          'irrigator__status') \
            .annotate(total_water_consumption=Sum('specie__water_consumption')) \
            .annotate(difference=ExpressionWrapper(
            F('irrigator__water_flow') - F('total_water_consumption'), output_field=FloatField()))
        irrigators_with_low_water_flow = irrigators.filter(difference__lt=0)

        result = {}
        for irrigator in irrigators_with_low_water_flow:
            result[irrigator['irrigator__id']] = irrigator
        return Response(result, status=status.HTTP_200_OK)
