from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from user.models import *


# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.SlugField(max_length=100, null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # def __str__(self):
    #     return self.name

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'slug': self.slug})

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    class Meta:
        db_table = 'category'



# class Facility(models.Model):
#     name = models.CharField(max_length=100, unique=True, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(
#         User,
#         related_name="facility_created_by",
#         on_delete=models.CASCADE
#     )
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(
#         User,
#         related_name="facility_updated_by",
#         on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'facility'


# class Service(models.Model):
#     name = models.CharField(max_length=100, unique=True, blank=True, null=True)
#     facility =models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)
#     # created_by = models.ForeignKey(
#     #     'facility',
#     #     related_name="service_created_by",
#     #     on_delete=models.CASCADE
#     # )
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(
#         User,
#         related_name="service_created_by",
#         on_delete=models.CASCADE
#     )
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey(
#         User,
#         related_name="service_updated_by",
#         on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'service'
