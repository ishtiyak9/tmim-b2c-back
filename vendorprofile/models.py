import os
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import mark_safe
# from category.models import *
from user.models import *

status_info = (
    (1, 'Published'),
    (0, 'Unpublished'),
)


class VendorCountry(models.Model):
    name = models.CharField(max_length=100, blank=True)
    iso3 = models.CharField(max_length=3, blank=True)
    iso2 = models.CharField(max_length=2, blank=True)
    phone_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'vendor_country'
        verbose_name_plural = 'Vendor Countries'


class VendorCity(models.Model):
    name = models.CharField(max_length=100, blank=True)
    country = models.ForeignKey(VendorCountry, blank=True, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'vendor_city'
        verbose_name_plural = 'Vendor Cities'


class BusinessCategory(models.Model):
    business_category = models.CharField(max_length=100, blank=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.business_category

    class Meta:
        db_table = 'business_category'
        verbose_name_plural = 'Business Categories'


class BusinessSubCategory(models.Model):
    business_category = models.ForeignKey(BusinessCategory, blank=True, null=True, on_delete=models.CASCADE)
    business_sub_category = models.CharField(max_length=255, blank=True)
    business_sub_category_icon = models.FileField(upload_to='uploads/vendor/attachments/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, default="", related_name='created_by_user', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, default="", related_name='updated_by_user', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.business_category

    class Meta:
        db_table = 'business_sub_category'
        verbose_name_plural = 'Business Sub Categories'


class VendorProfile(models.Model):
    company = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, allow_unicode=True)
    business_category = models.ForeignKey(BusinessCategory, on_delete=models.PROTECT)
    occasion_type = models.ForeignKey('guest.OccasionType', related_name="occasions_type", on_delete=models.CASCADE,
                                      blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_json = models.CharField(max_length=250, blank=True, default=dict)
    # category = models.ForeignKey(
    #     Category,
    #     related_name="category",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    user = models.ForeignKey(
        User, related_name="vendor", limit_choices_to={'user_type': "vendor"}, on_delete=models.CASCADE
    )
    country = models.ForeignKey(VendorCountry, blank=True, null=True, on_delete=models.PROTECT)
    city = models.ForeignKey(VendorCity, blank=True, null=True, on_delete=models.PROTECT)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    rating = models.FloatField(blank=True, default=0.0)
    discount_status = models.BooleanField(blank=True, default=False)
    discount_amount = models.FloatField(blank=True, default=0.0)
    stock_quantity = models.IntegerField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='uploads/vendor/images/', blank=True, null=True)
    charge_taxes = models.BooleanField(default=True)
    status = models.IntegerField(choices=status_info, default=0)
    is_deleted = models.BooleanField(default=False, verbose_name='Archived')
    # customer_ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_profile_id", on_delete=models.CASCADE, null=True,
                                   blank=True)
    updated_by = models.ForeignKey(User, related_name="update_profile_id", on_delete=models.CASCADE, null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company}"

    class Meta:
        db_table = 'vendor_profile'
        verbose_name_plural = 'Vendor Profiles'

    # def delete(self, *args, **kwargs):
    #     if os.path.isfile(self.cover_photo.path):
    #         os.remove(self.cover_photo.path)

    #     super(VendorProfile, self).delete(*args, **kwargs)


class VendorProfileAttachments(models.Model):
    path = models.FileField(upload_to='uploads/vendor/attachments/', null=True)
    vendor = models.ForeignKey(VendorProfile, blank=True, related_name='attachments', null=True,
                               on_delete=models.CASCADE)

    class Meta:
        db_table = 'vendor_attachments'

    def __str__(self):
        return f"{self.path}"

    # def delete(self, *args, **kwargs):
    #     if os.path.isfile(self.path.path):
    #         os.remove(self.path.path)

    #     super(VendorProfileAttachments, self).delete(*args, **kwargs)


class VendorProfileImages(models.Model):
    image = models.ImageField(upload_to='uploads/vendor/images/', null=True)
    vendor = models.ForeignKey(VendorProfile, blank=True, related_name='image', null=True,
                               on_delete=models.CASCADE)


class VendorProfileVideos(models.Model):
    video = models.FileField(upload_to='uploads/vendor/videos/', null=True)
    vendor = models.ForeignKey(VendorProfile, blank=True, related_name='video', null=True,
                               on_delete=models.CASCADE)


class Facility(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    vendor = models.ForeignKey(VendorProfile, related_name='facilities', blank=True, null=True,
                               on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="facility_created_by",
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="facility_updated_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'facility'
        verbose_name_plural = 'Facilities'


class Service(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.ForeignKey(VendorProfile, related_name='services', blank=True, null=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="service_created_by",
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="service_updated_by",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'service'
        verbose_name_plural = 'Services'


class ReviewsAndRatings(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=150, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    customer = models.ForeignKey(User, related_name='review_customer', blank=True, null=True, on_delete=models.PROTECT)
    vendor = models.ForeignKey(VendorProfile, related_name='reviews', blank=True, null=True, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="review_created_by",
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        related_name="review_updated_by",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'reviews_and_ratings'

    def __str__(self):
        return f"{self.title}"
