from django.urls import path
from .views import SubcriptionPlanAPIView, SubcriptionAPIView, RenewSubscriptionAPIView, CancelSubscriptionAPIView, SubscriptionDetailsAPIView, SubscriptionHistoryAPIView

urlpatterns = [
    # list of subscription plan
    path('subscription/plans', SubcriptionPlanAPIView.as_view()),
    # subscribed seller list not needed instead just keep the subscribe functionality
    path('subscribe', SubcriptionAPIView.as_view()),
    # renew subscriptin for seller
    path('subscription/renew', RenewSubscriptionAPIView.as_view()),
    path('subscription/details/<str:pk>', SubscriptionDetailsAPIView.as_view()),
    # cancel subscription
    path('subscription/cancel/<str:pk>', CancelSubscriptionAPIView.as_view()),
    # subscription history
    path('subscription/history', SubscriptionHistoryAPIView.as_view()),
]