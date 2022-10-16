from django.urls import path
from .views import VatAmountAPIView, CommissionAmountAPIView, CountryCityAPIView, OccasionTypeAPIView

urlpatterns = [
    path('api/vat/amount', VatAmountAPIView.as_view()),
    path('api/commission/amount', CommissionAmountAPIView.as_view()),
    path('api/country&city', CountryCityAPIView.as_view()),
    path('api/planningtypes', OccasionTypeAPIView.as_view()),
]