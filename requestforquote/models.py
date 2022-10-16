from django.db import models
import random

from user.models import *
from vendorprofile.models import *
# Create your models here.

contact_preference = (
    (1, 'email'),
    (2, 'phone')
)

quote_status = (
    (1, 'active'),
    (2, 'close'),
)

def random_string():
    return str(random.randint(10000, 99999))

class RFQ(models.Model):
    rfq_code = models.CharField(max_length=250, unique=True, default=random_string)
    customer = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="rfq_customer",
        limit_choices_to={'user_type': "customer"},
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    vendor = models.ForeignKey(
        VendorProfile,
        blank=True,
        null=True,
        related_name="rfq_vendor",
        on_delete=models.CASCADE
    )
    message = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    preferred_contact = models.IntegerField(choices=contact_preference, default=0)
    # is_accepted = models.BooleanField(default=False)
    status = models.IntegerField(choices=quote_status, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name="rfq_created_by",
        on_delete=models.CASCADE, blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name="rfq_updated_by",
        on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return "%s" % self.rfq_code

    class Meta:
        db_table = 'rfq'
        verbose_name = 'Request For Quote'


# class QuotationDetails(models.Model):
#     quotation = models.ForeignKey(
#         Quotation,
#         related_name="quotation",
#         on_delete=models.CASCADE
#     )
#     user = models.ForeignKey(
#         User,
#         related_name="quotation_user",
#         on_delete=models.CASCADE
#     )    
#     message = models.TextField(blank=True)
#     message_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.id
#     class Meta:
#         db_table = 'quotation_details'
