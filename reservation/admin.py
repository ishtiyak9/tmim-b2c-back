from django.contrib import admin
from .models import *
# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_code', 'vendor', 'customer', 'reservation_date')
    list_filter = ['reservation_date', 'vendor', 'customer', 'is_approved', 'finish_reservation']
admin.site.register(Reservation, ReservationAdmin)