from django.urls import path, include
from guest.views import *
from django.contrib.auth import views as auth_views

app_name = 'guest'
urlpatterns = [
    path('all', GuestView.as_view(), name="AllGuest"),
    path('occasion/list', OccasionListView.as_view(), name="OccasionList"),
    path('add', GuestView.as_view(), name="GuestAdd"),
    path('update/<str:pk>', GuestView.as_view(), name="GuestUpdate"),
    path('delete/<str:pk>', GuestView.as_view(), name="GuestDelete"),
    path('landingpage/<int:customer_id>', GuestlandingView.as_view(), name="GuestLandingPage"),
    path('landingpage/<int:customer_id>', GuestlandingView.as_view(), name="CreateGuestLandingPage"),
]
