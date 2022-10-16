from django.db import models

from user.models import *
from checklist.models import *


# class GuestGroup(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(
#         User,
#         related_name="guestgroup_created_by",
#         on_delete=models.CASCADE
#     )
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(
#         User,
#         related_name="guestgroup_updated_by",
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return self.name
#
#
#     class Meta:
#         db_table = 'guest_group'
#
#
#
class OccasionType(models.Model):
    occasion_type = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="occasion_type_created_by",
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="occasion_type_updated_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.occasion_type

    class Meta:
        db_table = 'occasion_type'


#


class Guest(models.Model):
    customer = models.ForeignKey(User, limit_choices_to={'user_type': "customer"}, on_delete=models.CASCADE)
    # guest_group = models.ForeignKey(GuestGroup, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)
    # age = models.CharField(max_length=100, blank=True)
    # invited_to = models.ForeignKey(OccasionType, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(verbose_name='email address', max_length=100, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    # address = models.CharField(max_length=200,blank=True, null=True)
    # country = models.CharField(max_length=100,blank=True, null=True)
    # city = models.CharField(max_length=100,blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    # zipcode = models.CharField(max_length=100,blank=True, null=True)
    invitation_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="guest_created_by",
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="guest_updated_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'guest'


class Guestlanding(models.Model):
    host = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/guestlanding/images/', blank=True)
    details = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    address_map = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(max_length=100, null=True, blank=True)
    sendstatus = models.IntegerField(null=True, blank=True, default=0)
    created_by = models.ForeignKey(
        User,
        related_name="guestlanding_created_by",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="guestlanding_updated_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.details

    class Meta:
        db_table = 'guestlanding'
        verbose_name = 'Guest Landing'
        verbose_name_plural = 'Guest Landings'
