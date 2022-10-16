from rest_framework import serializers

from requestforquote.models import *
from user.models import *
from vendorprofile.models import *

class RFQSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQ
        fields = ['id', 'rfq_code', 'customer', 'name', 'email', 'phone', 'vendor', 'date', 'start_time', 'end_time', 'preferred_contact', 'status', 'message', 'created_by', 'updated_by']

    def create(self, validated_data):
        customer = self.context['customer']
        vendor = self.context['vendor']
        customer = User.objects.get(pk=customer)
        vendor = VendorProfile.objects.get(pk=vendor) 

        validated_data['customer'] = customer
        validated_data['vendor'] = vendor
        validated_data['created_by'] = customer
        validated_data['updated_by'] = customer

        rfq = RFQ.objects.create(**validated_data)
        
        return rfq

    # update means closing
    def update(self, instance, validated_data):
        print(validated_data)
        instance.status = validated_data.get('status')
        instance.updated_by = validated_data.get('updated_by')
        instance.save()
        print(instance)

        return instance


class UpdateRFQSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQ
        fields = ['id', 'status', 'updated_by']