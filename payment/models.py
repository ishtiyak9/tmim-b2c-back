from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from reservation.models import Reservation

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PayStatus:
    PENDING = 0
    COMPLETE = 1
    FAILED = 2
    EXPIRED = 3
    DELIVERED = 4

    CHOICES = (
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
        (FAILED, "Failed"),
        (EXPIRED, "Expired"),
        (DELIVERED, "Delivered")
    )


class Payment(models.Model):
    gateway = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    to_confirm = models.BooleanField(default=False)
    variant = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=PayStatus.CHOICES)
    fraud_status = models.CharField(_('fraud check'), max_length=10)
    fraud_message = models.TextField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=10,blank=True, null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, default='0.0')
    delivery = models.DecimalField(
        max_digits=9, decimal_places=2, default='0.0')
    tax = models.DecimalField(max_digits=9, decimal_places=2, default='0.0')
    description = models.TextField(blank=True, default='')
    billing_first_name = models.CharField(max_length=256, blank=True)
    billing_last_name = models.CharField(max_length=256, blank=True)
    billing_address_1 = models.CharField(max_length=256, blank=True)
    billing_address_2 = models.CharField(max_length=256, blank=True)
    billing_city = models.CharField(max_length=256, blank=True)
    billing_postcode = models.CharField(max_length=256, blank=True)
    billing_country_code = models.CharField(max_length=2, blank=True)
    billing_country_area = models.CharField(max_length=256, blank=True)
    billing_email = models.EmailField(blank=True)
    customer_ip_address = models.GenericIPAddressField(blank=True, null=True)
    extra_data = models.TextField(blank=True, default='')
    message = models.TextField(blank=True, default='')
    token = models.CharField(max_length=36, blank=True, default='')
    captured_amount = models.DecimalField(max_digits=9, decimal_places=2, default='0.0')
    payment_method_type = models.CharField(max_length=256, blank=True)
    extra_data = models.TextField(blank=True, default="")
    return_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True

    class Meta:
        db_table = 'payment'


class PaymentLog(TimeStampedModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    response_data = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.pk}"


class Transaction(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    payment = models.ForeignKey(
        Payment, related_name="transactions", on_delete=models.PROTECT
    )
    token = models.CharField(max_length=512, blank=True, default="")
    is_success = models.BooleanField(default=False)
    action_required = models.BooleanField(default=False)
    action_required_data = models.DateTimeField(blank=True, null=True)
    currency = models.CharField(max_length=10,blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default='0.0')
    error = models.CharField(max_length=256, null=True,
    )
    customer_id = models.CharField(max_length=256, null=True)
    gateway_response = models.CharField(max_length=512, null=True, blank=True)
    already_processed = models.BooleanField(default=False)
    searchable_key = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        ordering = ("pk",)

    def __repr__(self):
        return "Transaction(type=%s, is_success=%s, created=%s)" % (
            self.kind,
            self.is_success,
            self.created,
        )
    class Meta:
        db_table = 'transaction'


class Refund(models.Model):
    payment = models.ForeignKey(Payment, related_name="users_payment_id", on_delete=models.CASCADE)
    booking = models.ForeignKey(Reservation, related_name="users_reservation_id", on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name