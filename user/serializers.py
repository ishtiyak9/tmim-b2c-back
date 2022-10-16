from django.conf import settings
import os
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login, Group
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
import datetime, time
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode

from user.models import *
from user.token import account_activation_token
from subscription.models import Subscription
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    username = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    group = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user account is not activated yet'
            )
        if user.user_type == 'Vendor' and user.is_approved == False:
            raise serializers.ValidationError(
                'This vendor account is not approved yet'
            )
        # if user.user_type == 'vendor':
        # subscription_plan_info = Subscription.objects.get(vendor_id=user.id)
        subscription_plan_info = Subscription.objects.all().values_list()
        # subscription_plan_info = subscription_plan_info.subscription_plan_id
        print("subscription_plan_info=>", user.id, subscription_plan_info)
        # try:
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user)
        group = Group.objects.get(user=user)
        print("group=>", group)
        # except User.DoesNotExist:
        #     raise serializers.ValidationError(
        #         'User with given email and password does not exists'
        #     )
        return {
            # 'spi': subscription_plan_info,
            'email': user.email,
            'token': jwt_token,
            'group': group
        }


class CustomerRegistratioinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'phone', 'password', 'gender', 'wedding_date',
                  'planning_type', 'user_type']
        extra_kwargs = {
            'wedding_date': {
                'required': True,
                "error_messages": {"required": "Please select an approximate wedding date"}
            },
        }

    def create(self, validated_data):
        group = Group.objects.get(name='customer')
        user = User.objects._create_user(**validated_data)
        group.user_set.add(user)

        # first_name = validated_data['first_name']
        # email = validated_data['email']

        # send_mail(
        #     'Welcome in Tmmim',
        #     f'Hello {first_name}, welcome in Tmmim. Please activate your account: /api/${urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}',
        #     'haris.dipto@gmail.com',
        #     [email],
        #     fail_silently=False
        # )
        print(
            f'activation token: /api/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}')

        return user


class VendorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'password', 'country', 'city', 'zip_code', 'area', 'address', 'user_type']
        extra_kwargs = {
            'country': {
                "required": True,
                "error_messages": {"required": "Please select your country"}
            },
            'city': {
                "required": True,
                "error_messages": {"required": "Please select your city"}
            },
        }

    def create(self, validated_data):
        group = Group.objects.get(name='vendor')
        user = User.objects._create_user(**validated_data)
        group.user_set.add(user)

        # first_name = validated_data['first_name']
        # email = validated_data['email']
        # password = validated_data['password']

        # send_mail(
        #     'Welcome in Tmmim',
        #     f'Hello {first_name}, welcome in Tmmim. Your passowrd is: {password}.',
        #     'haris.dipto@gmail.com',
        #     [email],
        #     fail_silently=False
        # )

        return user


class CustomerAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'planning_type', 'email', 'phone', 'about_me', 'self_name', 'partner_name',
                  'dob', 'gender', 'image', 'city', 'zip_code', 'wedding_date', 'user_type']
        extra_kwargs = {
            'email': {'read_only': True},
        }

    def validate_city(self, value):
        if value == None:
            raise serializers.ValidationError("Please select a wedding city")
        return value

    def validate_wedding_date(self, value):
        if value == None:
            raise serializers.ValidationError("Please give an approximate wedding date")
        return value

    def update(self, instance, validatd_data):
        instance.first_name = validatd_data.get('first_name', instance.first_name)
        instance.last_name = validatd_data.get('last_name', instance.last_name)
        instance.planning_type = validatd_data.get('planning_type', instance.planning_type)
        instance.phone = validatd_data.get('phone', instance.phone)
        instance.self_name = validatd_data.get('self_name', instance.self_name)
        instance.partner_name = validatd_data.get('partner_name', instance.partner_name)
        instance.about_me = validatd_data.get('about_me', "")
        instance.dob = validatd_data.get('dob', "")
        instance.gender = validatd_data.get('gender', "")
        instance.city = validatd_data.get('city', instance.city)
        instance.zip_code = validatd_data.get('zip_code', "")
        instance.wedding_date = validatd_data.get('wedding_date', instance.wedding_date)

        # delete existing image then upload new one
        if instance.image != None:
            instance.image.delete()
        instance.image = validatd_data.get('image', None)

        instance.save()
        return instance


class VendorAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'image', 'dob', 'gender', 'address', 'city', 'zip_code',
                  'country', 'user_type']

        extra_kwargs = {
            "email": {'read_only': True},
        }

    def validate_country(self, value):
        if value == None:
            raise serializers.ValidationError("Please select your country")
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.image = validated_data.get('image', None)
        instance.dob = validated_data.get('dob', None)
        instance.gender = validated_data.get('gender', None)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.zip_code = validated_data.get('zip_code', None)
        instance.country = validated_data.get('country', instance.country)

        instance.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
