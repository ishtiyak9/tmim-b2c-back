import os
from rest_framework import serializers

from django.conf import settings
from vendorprofile.models import *


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        modal = VendorProfile
        fields = ['company', 'slug', 'business_category', 'description', 'user', 'country',
                  'city', 'zip_code', 'address', 'rating', 'discount_status', 'discount_amount', 'cover_photo',
                  'status', 'services', 'facilities', 'reviews', 'attachments']


class VendorProfileAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfileAttachments
        fields = ['id', 'path']


class VendorProfileImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfileImages
        fields = ['id', 'image']


class VendorProfileVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfileVideos
        fields = ['id', 'video']


class VendorFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'vendor']


class VendorServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'vendor']


class VendorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsAndRatings
        fields = ['rating', 'title', 'text', 'customer', 'vendor', 'created_by', 'updated_by']

    def create(self, validated_data):
        review_and_rating = ReviewsAndRatings.objects.create(**validated_data)
        return review_and_rating

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class VendorProfileSerializer(serializers.ModelSerializer):
    facilities = VendorFacilitySerializer(many=True, required=False)
    services = VendorServiceSerializer(many=True, required=False)
    attachments = VendorProfileAttachmentsSerializer(many=True, required=False)
    reviews = VendorReviewSerializer(many=True, required=False)

    class Meta:
        model = VendorProfile
        fields = ['company', 'slug', 'business_category', 'description', 'user', 'country',
                  'city', 'zip_code', 'address', 'rating', 'discount_status', 'discount_amount', 'cover_photo',
                  'status', 'services', 'facilities', 'reviews', 'attachments']

        extra_kwargs = {
            'company': {
                "required": False,
                "error_messages": {"required": "Please provide a company name"}
            },
            'business_category': {
                "required": False,
                "error_messages": {"required": "Please select a business category"}
            },
        }

    def validate(self, data):
        if ('discount_status' in data.keys()) and (data['discount_status'] == True and data['discount_amount'] <= 0):
            raise serializers.ValidationError("To turn on discount, you should must give a discount amount")
        return data

    def create(self, validated_data):
        slug = '-'.join(validated_data['company'].split(' ')).lower()
        vendor_profile = VendorProfile.objects.create(**validated_data, slug=slug)
        return vendor_profile

    def update(self, instance, validated_data):
        instance.company = validated_data.get('company', instance.company)
        instance.business_category = validated_data.get('business_category', instance.business_category)
        instance.description = validated_data.get('description', instance.description)
        # instance.category = validated_data.get('category', instance.category)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.address = validated_data.get('address', instance.address)
        instance.discount_status = validated_data.get('discount_status', instance.discount_status)
        instance.discount_amount = validated_data.get('discount_amount', instance.discount_amount)
        instance.status = validated_data.get('status', instance.status)

        # update the slug
        instance.slug = '-'.join(instance.company.split(' ')).lower()

        cover_photo = validated_data.get('cover_photo', instance.cover_photo)
        # this condition denotes user wanted to remove cover_photo and leave it as empty
        if cover_photo == None and instance.cover_photo != None:
            instance.cover_photo.delete()
        instance.cover_photo = cover_photo

        #  facility
        vendor_facilities = Facility.objects.filter(vendor=instance)
        if vendor_facilities:
            for facility in vendor_facilities:
                facility.delete()

        facilities_list = []
        facilities = validated_data.get('facilities', None)
        if facilities:
            for facility in facilities:
                f = Facility.objects.create(**facility, vendor=instance, created_by=User(instance.user.id),
                                            updated_by=User(instance.user.id))
                facilities_list.append(f)
        instance.facilities.set(facilities_list)

        # service
        vendor_services = Service.objects.filter(vendor=instance)
        if vendor_services:
            for service in vendor_services:
                service.delete()

        services_list = []
        services = validated_data.get('services', None)
        if services:
            for service in services:
                s = Service.objects.create(**service, vendor=instance, created_by=User(instance.user.id),
                                           updated_by=User(instance.user.id))
                services_list.append(s)
        instance.services.set(services_list)

        # only inserting attachemnts, deletion will be handled different place
        attachment_data = validated_data.pop('attachments', None)
        keep_attachment = [attachment for attachment in instance.attachments.all()]
        if attachment_data:
            for attachment in attachment_data:
                c = VendorProfileAttachments.objects.create(**attachment, vendor=instance)
                keep_attachment.append(c)

        instance.attachments.set(keep_attachment)
        instance.save()

        return instance


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = '__all__'


class BusinessSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessSubCategory
        fields = '__all__'


class VendorProfileHomePageSerializer(serializers.ModelSerializer):
    facilities = VendorFacilitySerializer(many=True, required=False)
    services = VendorServiceSerializer(many=True, required=False)
    attachments = VendorProfileAttachmentsSerializer(many=True, required=False)
    image = VendorProfileImagesSerializer(many=True, required=False)
    video = VendorProfileVideosSerializer(many=True, required=False)
    reviews = VendorReviewSerializer(many=True, required=False)

    class Meta:
        model = VendorProfile
        fields = ['company', 'slug', 'business_category', 'description', 'user', 'country',
                  'city', 'zip_code', 'address', 'rating', 'discount_status', 'discount_amount', 'cover_photo', 'image',
                  'video',
                  'status', 'services', 'facilities', 'reviews', 'attachments']
