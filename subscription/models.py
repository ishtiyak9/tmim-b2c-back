from django.db import models
from user.models import *

# Create your models here.

plan = (
    ("y", 'Annually'),
    ("h", 'Semi-Annually'),
)
cardType = (
    (1, 'Card'),
)
statusType = (
    (1, 'Paid'),
    (0, 'Unpaid'),
)


class SubscriptionType:
    MONTH3 = 1
    MONTH6 = 2
    YEARLY = 3

    CHOICES = (
        (MONTH3, "3 Months"),
        (MONTH6, "6 Months"),
        (YEARLY, "Yearly")
    )


class SubscriptionRenewAlertStatus:
    RENEWED = 1
    SEVEN_DAYS_TO_EXPIRE = 7
    THREE_DAYS_TO_EXPIRE = 3

    CHOICES = (
        (RENEWED, "Renewed"),
        (SEVEN_DAYS_TO_EXPIRE, "7 Days to expire"),
        (THREE_DAYS_TO_EXPIRE, "3 Days to expire")
    )


class SubscriptionPlan(models.Model):
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_plan = models.CharField(max_length=1, choices=plan)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.subscription_plan == 'y':
            return "Annually" + ' - ' + str(self.fees)
        else:
            return "Semi-Annually" + ' - ' + str(self.fees)

    class Meta:
        db_table = 'subscriptionplan'
        verbose_name_plural = 'Subscription Plans'


class Subscription(models.Model):
    vendor = models.ForeignKey(
        User,
        related_name="subscriptions",
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': "vendor"},
        verbose_name='Vendor'
    )
    subscription_plan = models.ForeignKey(
        'SubscriptionPlan',
        related_name="subscriptions_plan",
        on_delete=models.CASCADE,
        verbose_name='Subscription Plan'
    )
    fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_type = models.IntegerField(choices=cardType, default=1, blank=True)
    payment_status = models.BooleanField(default=False, choices=statusType, blank=True, null=True,
                                         verbose_name='Payment Status')
    total_paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    Subscription_status = models.PositiveSmallIntegerField(choices=SubscriptionRenewAlertStatus.CHOICES,
                                                           default=SubscriptionRenewAlertStatus.RENEWED)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="subscriptions_created_by",
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="subscriptions_updated_by",
        on_delete=models.CASCADE
    )
    is_deleted = models.BooleanField(default=False, verbose_name='Archived')
    paytab_data = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'subscription'
        verbose_name_plural = 'Subscriptions'
