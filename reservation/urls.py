from django.urls import path, include

from reservation.views import *

app_name='reservation'

urlpatterns = [
    path('all', ReservationView.as_view(), name="AllReservation"),
    path('details/<int:pk>', ReservationDetailsView.as_view(), name="DetailsReservation"),
    path('create', ReservationView.as_view(), name="CreateReservation"),
    path('update/<int:reservation_id>', UpdateReservationView.as_view(), name="UpdateReservation")
]
