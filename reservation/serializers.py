from rest_framework import serializers

from reservation.models import *
from vendorprofile.models import *
from user.models import *


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation

        fields = ['id', 'total_amount', 'quotation', 'reservation_code', 'reservation_date', 'reservation_start_time',
                  'reservation_end_time',
                  'is_approved', 'finish_reservation', 'vendor', 'customer', 'address', 'created_by', 'updated_by']

    def create(self, validatd_data):
        reservation = Reservation.objects.create(**validatd_data)
        return reservation


class VendorProfileImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfileImages
        fields = ['id', 'image']


class VendorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsAndRatings
        fields = ['rating', 'title', 'text', 'customer', 'vendor', 'created_by', 'updated_by']


class VendorProfileHomePageSerializer(serializers.ModelSerializer):
    image = VendorProfileImagesSerializer(many=True, required=False)
    reviews = VendorReviewSerializer(many=True, required=False)

    class Meta:
        model = VendorProfile
        fields = ['company', 'slug', 'business_category', 'description', 'user', 'country',
                  'city', 'zip_code', 'address', 'rating', 'discount_status', 'discount_amount', 'cover_photo', 'image',
                  'status', 'reviews']


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['id', 'quotation_code', 'rfq', 'price', 'date', 'start_time', 'end_time', 'message', 'status',
                  'customer', 'vendor', 'attachment', 'created_at', 'updated_at', 'created_by', 'updated_by']


class CustomerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'planning_type', 'email', 'phone', 'about_me', 'self_name', 'partner_name',
                  'dob', 'gender', 'image', 'city', 'zip_code', 'wedding_date', 'user_type']


class ReservationListSerializer(serializers.ModelSerializer):
    vendor = VendorProfileHomePageSerializer()
    quotation = QuotationSerializer()
    customer = CustomerAccountSerializer()

    class Meta:
        model = Reservation

        fields = ['id', 'total_amount', 'quotation', 'reservation_code', 'reservation_date', 'reservation_start_time',
                  'reservation_end_time',
                  'is_approved', 'finish_reservation', 'vendor', 'customer', 'address', 'created_by', 'updated_by']
