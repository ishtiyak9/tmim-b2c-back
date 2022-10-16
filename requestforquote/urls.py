from django.urls import path, include

from requestforquote.views import *

app_name='requestforquote'

urlpatterns = [
    path('rfq/create/<vendor_profile_id>', CreateRFQView.as_view(), name='CreateRFQ'),
    path('rfq/details/<int:rfq_id>', RFQView.as_view(), name='RFQDetails'),
    path('rfq/response/<int:rfq_id>', RFQView.as_view(), name='UpdateRFQ'),
    path('rfq/all', AllRFQView.as_view(), name='AllFRQs'),
]
