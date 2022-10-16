from pyexpat import model

from rest_framework import serializers

from guest.models import OccasionType
from settings.models import Vat, Commission
from user.models import Country, City


class VatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vat
        fields = ['percentage']


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = ['percentage']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'iso3', 'iso2', 'phone_code']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country']


class OccasionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccasionType
        fields = ['id', 'occasion_type']
