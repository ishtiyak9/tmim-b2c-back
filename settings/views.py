from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny

from guest.models import OccasionType
from settings.serializers import VatSerializer, CommissionSerializer, CountrySerializer, CitySerializer, \
    OccasionTypeSerializer
from settings.models import Vat, Commission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required

# Create your views here.
from user.models import Country, City


class VatAmountAPIView(APIView):
    def get(self, request):

        try:
            vat = Vat.objects.get(id=1)
        except Vat.DoesNotExist:
            response = {
                "success": "True",
                "status code": status.HTTP_404_NOT_FOUND,
                "message": "Vat is Not Found",
            }
            return Response(response)
        serializer = VatSerializer(vat, many=False)
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "Vat",
            "data": [serializer.data],
        }
        return Response(response)


class CommissionAmountAPIView(APIView):
    def get(self, request):

        try:
            commission_info = Commission.objects.get(id=1)
        except Commission.DoesNotExist:
            response = {
                "success": "True",
                "status code": status.HTTP_404_NOT_FOUND,
                "message": "Commission is Not Found",
            }
            return Response(response)
        serializer = CommissionSerializer(commission_info, many=False)
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "Commission",
            "data": [serializer.data],
        }
        return Response(response)


class CountryCityAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            Country_list = Country.objects.all()
        except Country.DoesNotExist:
            response = {
                "success": "True",
                "status code": status.HTTP_404_NOT_FOUND,
                "message": "Country is Not Found",
            }
            return Response(response)

        try:
            City_list = City.objects.all()
        except City.DoesNotExist:
            response = {
                "success": "True",
                "status code": status.HTTP_404_NOT_FOUND,
                "message": "City is Not Found",
            }
            return Response(response)

        country_serializer = CountrySerializer(Country_list, many=True)
        city_serializer = CitySerializer(City_list, many=True)
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "Country and City List",
            "data": {
                "countryList": country_serializer.data,
                "cityList": city_serializer.data
            }
        }
        return Response(response)


class OccasionTypeAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            OccasionType_list = OccasionType.objects.all()
        except OccasionType.DoesNotExist:
            response = {
                "success": "True",
                "status code": status.HTTP_404_NOT_FOUND,
                "message": "Planning Type is Not Found",
            }
            return Response(response)
        serializer = OccasionTypeSerializer(OccasionType_list, many=True)
        response = {
            "success": "True",
            "status code": status.HTTP_200_OK,
            "message": "Planning Type List",
            "data": [serializer.data],
        }
        return Response(response)