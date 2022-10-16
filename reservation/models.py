from django.db import models
import random

from user.models import *
from vendorprofile.models import *
from quotation.models import *

paymentstatus = (
    (0, 'Paid'),
    (1, 'Unpaid'),
)
payment_type = (
    (0, 'Wire Transfer'),
    (1, 'Card'),
)

approve = (
    (0, 'Approved'),
    (1, 'Unapproved'),
)


def random_string():
    return str(random.randint(10000, 99999))


# Create your models here.
class Reservation(models.Model):
    reservation_code = models.CharField(max_length=250, unique=True, default=random_string)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2)
    # payment_type = models.IntegerField(choices=payment_type, default=1)
    # customer_payment_status = models.IntegerField(choices=paymentstatus, default=1)
    # vendor_payment_status = models.IntegerField(choices=paymentstatus, default=1)
    # image = models.ImageField(upload_to='uploads/order/images/', blank=True)
    quotation = models.ForeignKey(Quotation, related_name="quotation_reservation", on_delete=models.CASCADE, blank=True,
                                  null=True)
    reservation_date = models.DateField(null=True, blank=True)
    reservation_start_time = models.TimeField(null=True, blank=True)
    reservation_end_time = models.TimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    vendor = models.ForeignKey(VendorProfile, related_name="reservation_vendor", on_delete=models.CASCADE, null=False,
                               blank=False)
    customer = models.ForeignKey(User, limit_choices_to={'user_type': "customer"}, related_name="reservation_customer",
                                 on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    finish_reservation = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name="created_reservation_id", on_delete=models.CASCADE, null=True,
                                   blank=True)
    updated_by = models.ForeignKey(User, related_name="update_reservation_id", on_delete=models.CASCADE, null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.reservation_code

    class Meta:
        db_table = 'reservation'

# class ReservationDetail(models.Model):
#     reservation = models.ForeignKey(
#         Reservation,
#         related_name="reservation_detail",
#         on_delete=models.CASCADE, blank=False
#     )
#     product = models.ForeignKey(
#         'vendorprofile.VendorProfile',
#         related_name="orders_product",
#         on_delete=models.CASCADE, blank=False
#     )
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     discount_coupon_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     class Meta:
#         db_table = 'reservation_detail'


# class ReservationTracking(models.Model):
#     reservatioin = models.ForeignKey(Reservation, on_delete=models.CASCADE, blank=False)
#     reservation_created_by = models.ForeignKey(User, related_name="user_reservation_id", on_delete=models.CASCADE, null=True, blank=True)
#     reservation_creation_date = models.DateTimeField(auto_now_add=True)
#     reservation_confirmed_by = models.ForeignKey(User, related_name="user_reservation_confirmed_id", on_delete=models.CASCADE, null=True, blank=True)
#     reservation_confirmed_date = models.DateField(null=True, blank=True)
#     shipping_processing_by = models.ForeignKey(User, related_name="user_reservation_procrssing_id", on_delete=models.CASCADE, null=True, blank=True)
#     shipping_processing_date = models.DateField(null=True, blank=True)
#     delivery_by_courier_name = models.CharField(max_length=250, unique=False, null=True, blank=True)
#     delivery_date = models.DateTimeField(null=True, blank=True)

#     class Meta:
#         db_table = 'reservation_tracking'
