from django.urls import path, include

from quotation.views import *

app_name='quotation'

urlpatterns = [
    path('all', QuotationView.as_view(), name='AllQuotation'),
    path('details/<int:quotation_id>', QuotationView.as_view(), name='QuotationDetails'),
    path('create/<int:rfq_id>', QuotationView.as_view(), name='CreateQuote'),
    path('update/<int:quotation_id>', QuotationUpdateView.as_view(), name='UpdateQuote'),
]
