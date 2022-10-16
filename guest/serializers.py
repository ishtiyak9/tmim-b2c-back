from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login, Group
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
import datetime, time
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from guest.models import *


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'customer', 'relationship', 'name','email',  'phone', 'invitation_date',  'created_by', 'updated_by']
        # fields = ['id', 'relationship', 'name', 'phone']
        extra_kwarg = {
            'name': {
                "required": True,
                "error_messages": {"required": "Please provide first name of the guest"}
            },

        }

    def update(self, instance, validated_data):
        # instance.guest_group = validated_data.get('guest_group', instance.guest_group)
        instance.name = validated_data.get('name', instance.name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.relationship = validated_data.get('relationship', instance.relationship)
        # instance.invited_to = validated_data.get('invited_to', instance.invited_to)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        # instance.address = validated_data.get('address', instance.address)
        # instance.city = validated_data.get('city', instance.city)
        # instance.zipcode = validated_data.get('zipcode', instance.zipcode)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.save()
        return instance


class GuestlandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guestlanding
        fields = ['id', 'host', 'image', 'details', 'address', 'address_map', 'date', 'sendstatus', 'created_by', 'updated_by']

    def create(self, validated_data):
        guestlanding = Guestlanding.objects.create(**validated_data)
        return guestlanding

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.details)
        instance.details = validated_data.get('details', instance.details)
        instance.address = validated_data.get('address', instance.address)
        instance.address_map = validated_data.get('address_map', instance.address_map)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccasionType
        fields = ['id', 'occasion_type']
