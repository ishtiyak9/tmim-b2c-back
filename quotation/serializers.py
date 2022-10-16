from rest_framework import serializers

from quotation.models import *
from requestforquote.models import *


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['id', 'quotation_code', 'rfq', 'price', 'date', 'start_time', 'end_time', 'message', 'status',
                  'customer', 'vendor', 'attachment', 'created_at', 'updated_at', 'created_by', 'updated_by']
