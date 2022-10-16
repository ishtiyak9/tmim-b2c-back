from django.db import models
import random

from user.models import *
from vendorprofile.models import *
from requestforquote.models import *

contact_preference = (
    (1, 'email'),
    (2, 'phone')
)

quote_status = (
    (1, 'pending'),
    (2, 'closed'),
    (3, 'accepted'),
    (4, 'denied'),
)


def random_string():
    return str(random.randint(10000, 99999))


# Create your models here.
class Quotation(models.Model):
    quotation_code = models.CharField(max_length=250, unique=True, default=random_string)
    rfq = models.ForeignKey(RFQ, related_name='quotation_rfq_code', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(choices=quote_status, default=1)
    customer = models.ForeignKey(User, related_name="customer_quotation", limit_choices_to={'user_type': "customer"},
                                 on_delete=models.PROTECT)
    vendor = models.ForeignKey(VendorProfile, related_name="vendor_quotatioon", on_delete=models.PROTECT)
    attachment = models.FileField(upload_to='uploads/vendor/quotation/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name="quotation_created_by",
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User,
        related_name="quotation_updated_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s" % self.quotation_code

    class Meta:
        db_table = 'quotation'
